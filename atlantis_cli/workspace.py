"""SphereOS Atlantisの複数repository作業環境を安全に展開する。"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any, Iterable

from .config import load_json
from .note import find_repo_root


WORKSPACE_MANIFEST = Path("workspace/components.json")
DEFAULT_WORKSPACE_FILE = Path(".atlantis/SphereOS-Atlantis.code-workspace")


def _safe_relative(value: object, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}には空でない文字列pathが必要です。")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field}がrepository外を指しています: {path}")
    return path


def load_workspace_manifest(root: Path) -> dict[str, Any]:
    manifest = load_json(root / WORKSPACE_MANIFEST)
    if manifest.get("schema_version") != "1.0.0":
        raise ValueError("workspace manifest schema_versionは1.0.0である必要があります。")
    workspace_root = _safe_relative(manifest.get("workspace_root"), "workspace_root")
    components = manifest.get("components")
    if not isinstance(components, list) or not components:
        raise ValueError("workspace manifestには1件以上のcomponentsが必要です。")

    seen_ids: set[str] = set()
    seen_paths: set[Path] = set()
    for item in components:
        if not isinstance(item, dict):
            raise ValueError("workspace componentはobjectである必要があります。")
        component_id = item.get("id")
        if not isinstance(component_id, str) or not component_id.strip():
            raise ValueError("workspace componentには文字列idが必要です。")
        if component_id in seen_ids:
            raise ValueError(f"workspace component idが重複しています: {component_id}")
        seen_ids.add(component_id)

        component_path = _safe_relative(item.get("path"), f"components[{component_id}].path")
        if component_path in seen_paths:
            raise ValueError(f"workspace component pathが重複しています: {component_path}")
        seen_paths.add(component_path)

        repository = item.get("repository")
        if not isinstance(repository, str) or not repository.startswith("https://github.com/"):
            raise ValueError(f"{component_id}のrepositoryはGitHub HTTPS URLである必要があります。")
        revision = item.get("revision")
        if (
            not isinstance(revision, str)
            or len(revision) != 40
            or any(character not in "0123456789abcdef" for character in revision.lower())
        ):
            raise ValueError(f"{component_id}のrevisionは40桁Git SHAである必要があります。")
        tracking_ref = item.get("tracking_ref")
        if not isinstance(tracking_ref, str) or not tracking_ref.strip():
            raise ValueError(f"{component_id}にはtracking_refが必要です。")
        if not isinstance(item.get("required"), bool):
            raise ValueError(f"{component_id}のrequiredはbooleanである必要があります。")
        if not isinstance(item.get("role"), str) or not item["role"].strip():
            raise ValueError(f"{component_id}にはroleが必要です。")

    manifest["_workspace_root_path"] = workspace_root
    return manifest


def _run_git(arguments: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    git = shutil.which("git")
    if not git:
        raise RuntimeError("git commandがPATHにありません。")
    completed = subprocess.run(
        [git, *arguments],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"git commandに失敗しました: {' '.join(arguments)}: {detail}")
    return completed


def _git_value(destination: Path, *arguments: str) -> str | None:
    git = shutil.which("git")
    if not git:
        return None
    completed = subprocess.run(
        [git, "-C", str(destination), *arguments],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def _component_destination(root: Path, workspace_root: Path, component_path: Path) -> Path:
    destination = (root / workspace_root / component_path).resolve()
    repository_root = root.resolve()
    if destination == repository_root or repository_root not in destination.parents:
        raise ValueError(f"component destinationがrepository外を指しています: {destination}")
    return destination


def select_components(manifest: dict[str, Any], requested: Iterable[str] | None) -> list[dict[str, Any]]:
    components = list(manifest["components"])
    requested_ids = [value for value in (requested or []) if value]
    if not requested_ids:
        return components
    mapping = {item["id"]: item for item in components}
    unknown = sorted(set(requested_ids) - mapping.keys())
    if unknown:
        raise ValueError(f"未登録のworkspace componentです: {', '.join(unknown)}")
    return [mapping[value] for value in requested_ids]


def inspect_component(root: Path, workspace_root: Path, component: dict[str, Any]) -> dict[str, Any]:
    relative = workspace_root / _safe_relative(component["path"], f"{component['id']}.path")
    destination = _component_destination(root, workspace_root, Path(component["path"]))
    expected_revision = component["revision"]

    if not destination.exists():
        state = "missing"
        actual_revision = None
        remote = None
    elif not (destination / ".git").exists():
        state = "blocked-non-git-path"
        actual_revision = None
        remote = None
    else:
        actual_revision = _git_value(destination, "rev-parse", "HEAD")
        remote = _git_value(destination, "remote", "get-url", "origin")
        if actual_revision == expected_revision and remote == component["repository"]:
            state = "ready"
        elif actual_revision != expected_revision:
            state = "revision-mismatch"
        else:
            state = "remote-mismatch"

    return {
        "id": component["id"],
        "role": component["role"],
        "required": component["required"],
        "path": str(relative),
        "destination": str(destination),
        "repository": component["repository"],
        "tracking_ref": component["tracking_ref"],
        "expected_revision": expected_revision,
        "actual_revision": actual_revision,
        "remote": remote,
        "state": state,
    }


def workspace_status(
    repo_root: Path | None = None,
    requested: Iterable[str] | None = None,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    manifest = load_workspace_manifest(root)
    workspace_root = Path(manifest["_workspace_root_path"])
    selected = select_components(manifest, requested)
    components = [inspect_component(root, workspace_root, item) for item in selected]
    required_failures = [
        item["id"]
        for item in components
        if item["required"] and item["state"] != "ready"
    ]
    return {
        "schema_version": "1.0.0",
        "workspace_id": manifest["workspace_id"],
        "repository_root": str(root),
        "workspace_root": str((root / workspace_root).resolve()),
        "components": components,
        "required_failures": required_failures,
        "overall": "ready" if not required_failures else "partial",
        "mutations_performed": False,
        "network_access_performed": False,
    }


def workspace_plan(
    repo_root: Path | None = None,
    requested: Iterable[str] | None = None,
) -> dict[str, Any]:
    status = workspace_status(repo_root, requested)
    actions: list[dict[str, str]] = []
    for item in status["components"]:
        if item["state"] == "missing":
            action = "clone-pinned-revision"
        elif item["state"] == "ready":
            action = "keep"
        else:
            action = "block-preserve-existing-path"
        actions.append({"id": item["id"], "state": item["state"], "action": action})
    return {
        **status,
        "actions": actions,
        "mode": "plan-only",
    }


def write_code_workspace(
    root: Path,
    status: dict[str, Any],
    destination: Path | None = None,
) -> Path:
    target = (root / (destination or DEFAULT_WORKSPACE_FILE)).resolve()
    if root.resolve() not in target.parents:
        raise ValueError(f"VS Code workspace出力先がrepository外です: {target}")
    folders = [{"name": "SphereOS-Atlantis", "path": ".."}]
    for item in status["components"]:
        if item["state"] == "ready":
            relative = Path(item["destination"]).resolve().relative_to(target.parent)
            folders.append({"name": item["id"], "path": str(relative)})
    payload = {
        "folders": folders,
        "settings": {
            "python.defaultInterpreterPath": "${workspaceFolder:SphereOS-Atlantis}/.venv",
            "files.exclude": {
                "**/__pycache__": True,
                "**/.pytest_cache": True,
            },
        },
    }
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(target)
    return target


def _clone_component(destination: Path, component: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise RuntimeError(f"既存pathは上書きしません: {destination}")
    try:
        _run_git(["-c", "init.defaultBranch=main", "init", str(destination)])
        _run_git(["-C", str(destination), "remote", "add", "origin", component["repository"]])
        _run_git(
            [
                "-C",
                str(destination),
                "fetch",
                "--depth",
                "1",
                "--no-tags",
                "origin",
                component["revision"],
            ]
        )
        _run_git(["-C", str(destination), "checkout", "--detach", component["revision"]])
    except Exception:
        if destination.exists():
            shutil.rmtree(destination)
        raise


def initialize_workspace(
    repo_root: Path | None = None,
    requested: Iterable[str] | None = None,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    manifest = load_workspace_manifest(root)
    workspace_root = Path(manifest["_workspace_root_path"])
    selected = select_components(manifest, requested)
    attempted: list[str] = []
    cloned: list[str] = []
    blocked: list[dict[str, str]] = []

    for component in selected:
        state = inspect_component(root, workspace_root, component)
        if state["state"] == "ready":
            continue
        if state["state"] != "missing":
            blocked.append({"id": component["id"], "state": state["state"]})
            continue
        attempted.append(component["id"])
        destination = Path(state["destination"])
        try:
            _clone_component(destination, component)
        except (OSError, RuntimeError, subprocess.SubprocessError) as error:
            blocked.append({"id": component["id"], "state": f"clone-failed: {error}"})
        else:
            cloned.append(component["id"])

    status = workspace_status(root, [item["id"] for item in selected])
    workspace_file = write_code_workspace(root, status)
    observed = datetime.now(timezone.utc)
    receipt = {
        **status,
        "observed_at": observed.isoformat(timespec="seconds"),
        "mode": "materialize-pinned-components",
        "attempted": attempted,
        "cloned": cloned,
        "blocked": blocked,
        "workspace_file": str(workspace_file),
        "mutations_performed": bool(cloned) or workspace_file.is_file(),
        "network_access_performed": bool(attempted),
        "model_invoked": False,
        "authentication_started": False,
        "existing_repositories_updated": False,
    }
    receipts = root / ".atlantis" / "receipts"
    receipts.mkdir(parents=True, exist_ok=True)
    receipt_path = receipts / f"workspace-{observed.strftime('%Y%m%dT%H%M%S%fZ')}.json"
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    receipt["receipt_path"] = str(receipt_path)
    return receipt


def format_workspace_report(result: dict[str, Any]) -> str:
    lines = [f"Atlantis workspace: {str(result['overall']).upper()}"]
    for item in result["components"]:
        lines.append(
            f"[{str(item['state']).upper()}] {item['id']} @ {item['expected_revision'][:12]}"
        )
    if "actions" in result:
        for action in result["actions"]:
            lines.append(f"plan {action['id']}: {action['action']}")
    if result.get("workspace_file"):
        lines.append(f"workspace file: {result['workspace_file']}")
    lines.append(
        "mutations: "
        f"{str(result['mutations_performed']).lower()}; "
        f"network: {str(result['network_access_performed']).lower()}"
    )
    return "\n".join(lines)
