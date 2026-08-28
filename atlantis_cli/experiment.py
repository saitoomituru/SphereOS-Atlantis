"""異種agent実験を起動せず、明示対象だけを観測・計画する。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Any

from .agent import build_contract
from .config import load_json


DEFAULT_CONTRACT = Path("experiments/m6xx-agent-orchestration/contract.json")


@dataclass(frozen=True)
class TargetBinding:
    target_id: str
    root: Path


def load_experiment_contract(root: Path, contract_path: Path | None = None) -> dict[str, Any]:
    path = contract_path or root / DEFAULT_CONTRACT
    if not path.is_absolute():
        path = root / path
    contract = load_json(path)
    targets = contract.get("targets")
    lanes = contract.get("lanes")
    if not isinstance(targets, list) or not targets:
        raise ValueError("実験contractにはtargetsが必要です。")
    if not isinstance(lanes, list) or not lanes:
        raise ValueError("実験contractにはlanesが必要です。")
    target_ids = {item.get("id") for item in targets if isinstance(item, dict)}
    if None in target_ids or len(target_ids) != len(targets):
        raise ValueError("target idが欠損または重複しています。")
    for lane in lanes:
        if not isinstance(lane, dict) or lane.get("target") not in target_ids:
            raise ValueError("laneが未登録targetを参照しています。")
        if lane.get("other_agent_output_as_input") is not False:
            raise ValueError("初期clean-room laneは他agent outputを入力にできません。")
    return contract


def parse_target_bindings(values: list[str], contract: dict[str, Any]) -> dict[str, TargetBinding]:
    known = {item["id"] for item in contract["targets"]}
    bindings: dict[str, TargetBinding] = {}
    for value in values:
        target_id, separator, raw_path = value.partition("=")
        if not separator or not target_id or not raw_path:
            raise ValueError("--target-rootはtarget-id=/absolute/path形式で指定してください。")
        if target_id not in known:
            raise ValueError(f"未登録targetです: {target_id}")
        if target_id in bindings:
            raise ValueError(f"target rootが重複しています: {target_id}")
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            raise ValueError(f"target rootは絶対pathで指定してください: {target_id}")
        bindings[target_id] = TargetBinding(target_id, path.resolve(strict=False))
    return bindings


def _git(root: Path, *arguments: str, allow_failure: bool = False) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        if allow_failure:
            return None
        message = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise ValueError(f"Git観測に失敗しました: {root}: {message}")
    return completed.stdout.strip()


def snapshot_target(target: dict[str, Any], binding: TargetBinding | None) -> dict[str, Any]:
    base: dict[str, Any] = {
        "target": target["id"],
        "repository_url": target["repository_url"],
        "resolved": binding is not None,
        "network_access_performed": False,
        "mutations_performed": False,
        "dirty_paths_disclosed": False,
    }
    if binding is None:
        return {**base, "state": "target-root-not-provided"}
    root = binding.root
    if not root.is_dir() or _git(root, "rev-parse", "--is-inside-work-tree", allow_failure=True) != "true":
        return {**base, "state": "not-a-git-worktree"}

    branch = _git(root, "symbolic-ref", "--short", "-q", "HEAD", allow_failure=True)
    head = _git(root, "rev-parse", "HEAD")
    remote = _git(root, "remote", "get-url", "origin", allow_failure=True)
    porcelain = _git(root, "status", "--porcelain", "--untracked-files=normal") or ""
    dirty_count = len(porcelain.splitlines()) if porcelain else 0
    upstream = _git(root, "rev-parse", "--abbrev-ref", "@{upstream}", allow_failure=True)
    tracking_state = "no-upstream"
    ahead = behind = None
    if upstream:
        counts = _git(root, "rev-list", "--left-right", "--count", f"HEAD...{upstream}")
        ahead, behind = (int(value) for value in counts.split())
        if ahead == behind == 0:
            tracking_state = "aligned-with-local-upstream-ref"
        elif ahead and behind:
            tracking_state = "diverged-from-local-upstream-ref"
        elif ahead:
            tracking_state = "ahead-of-local-upstream-ref"
        else:
            tracking_state = "behind-local-upstream-ref"
    return {
        **base,
        "state": "dirty-worktree" if dirty_count else "clean-worktree",
        "branch": branch or "DETACHED",
        "head": head,
        "origin_matches_contract": remote == target["repository_url"],
        "dirty": bool(dirty_count),
        "dirty_entry_count": dirty_count,
        "upstream": upstream,
        "ahead": ahead,
        "behind": behind,
        "tracking_state": tracking_state,
    }


def build_snapshot(contract: dict[str, Any], bindings: dict[str, TargetBinding]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "experiment_id": contract["id"],
        "observation_mode": "offline-explicit-targets-only",
        "targets": [snapshot_target(target, bindings.get(target["id"])) for target in contract["targets"]],
        "model_invoked": False,
        "network_access_performed": False,
        "mutations_performed": False,
    }


def build_doctor(root: Path, contract: dict[str, Any], bindings: dict[str, TargetBinding]) -> dict[str, Any]:
    providers = []
    for provider_id in contract["roles"]["coders"]:
        provider = build_contract(root, provider_id)["provider"]
        providers.append(
            {
                "provider": provider_id,
                "executable_detected": provider["available"],
                "executable": provider["detected_executable"],
                "capability_state": "unknown-until-explicit-probe",
                "model_invoked": False,
            }
        )
    return {
        "schema_version": "1.0.0",
        "experiment_id": contract["id"],
        "providers": providers,
        "snapshot": build_snapshot(contract, bindings),
        "run_state": "NOT IMPLEMENTED",
        "network_access_performed": False,
        "mutations_performed": False,
    }


def build_plan(root: Path, contract: dict[str, Any], bindings: dict[str, TargetBinding]) -> dict[str, Any]:
    snapshots = {item["target"]: item for item in build_snapshot(contract, bindings)["targets"]}
    packets = []
    for lane in contract["lanes"]:
        target = snapshots[lane["target"]]
        provider = build_contract(root, lane["provider"])["provider"]
        if not target["resolved"]:
            gate = "blocked-target-root-not-provided"
        elif target["state"] == "not-a-git-worktree":
            gate = "blocked-not-a-git-worktree"
        elif lane["mode"] == "isolated-worktree-candidate" and target.get("dirty"):
            gate = "blocked-shared-root-dirty"
        elif not target.get("origin_matches_contract", False):
            gate = "blocked-origin-mismatch"
        else:
            gate = "ready-to-render-only"
        packets.append(
            {
                "lane_id": lane["id"],
                "provider": lane["provider"],
                "provider_executable_detected": provider["available"],
                "target": lane["target"],
                "base_sha": target.get("head"),
                "branch": target.get("branch"),
                "mode": lane["mode"],
                "write_scope": lane["write_scope"],
                "clean_room_group": lane["clean_room_group"],
                "other_agent_output_as_input": False,
                "architect_source_refs": contract["architect_source_refs"],
                "buddy_allowed_actions": ["EVIDENCE_WHISPER", "REVIEW_CHALLENGE"],
                "automatic_process_interrupt": False,
                "automatic_merge": False,
                "automatic_publication": False,
                "execution_gate": gate,
            }
        )
    return {
        "schema_version": "1.0.0",
        "experiment_id": contract["id"],
        "packets": packets,
        "run_state": "NOT IMPLEMENTED",
        "model_invoked": False,
        "network_access_performed": False,
        "mutations_performed": False,
    }


def build_run_boundary(contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "experiment_id": contract["id"],
        "state": "NOT IMPLEMENTED",
        "code": "EXPLICIT_NATIVE_INVOCATION_NOT_IMPLEMENTED",
        "model_invoked": False,
        "network_access_performed": False,
        "mutations_performed": False,
        "user_gate_required": True,
    }
