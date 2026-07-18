"""モデルを呼び出さずにコードエージェント用session contractを生成する。"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
from typing import Any

from .config import load_adapter, load_json, policy_paths, sha256_file
from .note import find_repo_root


GENERATED_ROOT = Path(".atlantis/generated")


@dataclass(frozen=True)
class AgentPlan:
    provider_id: str
    available: bool
    detected_executable: str | None
    destination: Path
    action: str


def detect_adapter(adapter: dict[str, Any]) -> tuple[bool, str | None]:
    if adapter.get("kind") == "mock":
        return True, None
    for executable in adapter.get("executable_candidates", []):
        detected = shutil.which(executable)
        if detected:
            return True, detected
    return False, None


def build_contract(root: Path, provider_id: str) -> dict[str, Any]:
    adapter = load_adapter(root, provider_id)
    paths = policy_paths(root)
    policies = {name: load_json(path) for name, path in paths.items()}
    hashes = {name: sha256_file(path) for name, path in paths.items()}
    available, executable = detect_adapter(adapter)
    return {
        "schema_version": "1.0.0",
        "provider": {
            "id": provider_id,
            "vendor": adapter.get("vendor"),
            "kind": adapter.get("kind"),
            "available": available,
            "detected_executable": executable,
            "authentication": adapter.get("authentication"),
            "instruction_entrypoints": adapter.get("instruction_entrypoints", []),
        },
        "initialization_receipt": {
            "action": "render-contract-only",
            "model_invoked": False,
            "network_access_performed": False,
            "authentication_started": False,
            "paid_service_started": False,
        },
        "policy_hashes_sha256": hashes,
        "effective_contract": {
            "model_invocation": policies["default_constraints"]["initialization"]["model_invocation"],
            "parallel_write_mode": policies["default_constraints"]["parallel_work"]["parallel_write_mode"],
            "secret_default_action": policies["secret_boundaries"]["default_action"],
            "cost_class": policies["cost_policy"]["initialization_cost_class"],
            "generated_contract_is_canonical": False,
        },
    }


def contract_destination(root: Path, provider_id: str) -> Path:
    return root / GENERATED_ROOT / provider_id / "session-contract.json"


def plan_agent(root: Path, provider_id: str) -> AgentPlan:
    contract = build_contract(root, provider_id)
    destination = contract_destination(root, provider_id)
    if not destination.exists():
        action = "create"
    else:
        current = load_json(destination)
        action = "unchanged" if current == contract else "refresh-required"
    provider = contract["provider"]
    return AgentPlan(
        provider_id=provider_id,
        available=provider["available"],
        detected_executable=provider["detected_executable"],
        destination=destination,
        action=action,
    )


def initialize_agent(root: Path, provider_id: str, refresh: bool = False) -> AgentPlan:
    contract = build_contract(root, provider_id)
    destination = contract_destination(root, provider_id)
    plan = plan_agent(root, provider_id)
    if plan.action == "refresh-required" and not refresh:
        raise ValueError(
            f"生成済みcontractと現行policyが異なります: {destination}. --refreshで明示更新してください。"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    if plan.action != "unchanged":
        destination.write_text(
            json.dumps(contract, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    completed_action = {
        "create": "created",
        "refresh-required": "refreshed",
        "unchanged": "unchanged",
    }[plan.action]
    completed = plan_agent(root, provider_id)
    return AgentPlan(
        provider_id=completed.provider_id,
        available=completed.available,
        detected_executable=completed.detected_executable,
        destination=completed.destination,
        action=completed_action,
    )


def verify_agent(root: Path, provider_id: str) -> tuple[bool, str]:
    destination = contract_destination(root, provider_id)
    if not destination.is_file():
        return False, f"contractがありません: {destination}"
    current = load_json(destination)
    expected = build_contract(root, provider_id)
    if current != expected:
        return False, f"contractが現行policyと一致しません: {destination}"
    return True, f"contractは現行policyと一致します: {destination}"


def resolve_root(value: Path | None) -> Path:
    return find_repo_root(value)
