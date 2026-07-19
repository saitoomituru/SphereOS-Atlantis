"""Sphere-DOS開発shellを、standalone runtimeと偽装せず起動する。"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from .config import load_json
from .note import find_repo_root
from .workspace import workspace_status, write_code_workspace


SPHERE_DOS_PROFILE = Path("sphere-dos/profile.json")
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
STATE_ROOT = Path(".atlantis/sphere-dos")


def load_sphere_dos_profile(root: Path) -> dict[str, Any]:
    profile = load_json(root / SPHERE_DOS_PROFILE)
    if profile.get("schema_version") != "1.0.0":
        raise ValueError("Sphere-DOS profile schema_versionは1.0.0である必要があります。")
    if profile.get("distribution") != "sphere-dos":
        raise ValueError("Sphere-DOS profile distributionが一致しません。")
    if profile.get("standalone_runtime_implemented") is not False:
        raise ValueError("0.25.1ではstandalone runtimeを実装済みとして表示できません。")
    worlds = profile.get("world_profiles")
    if not isinstance(worlds, list) or not worlds:
        raise ValueError("Sphere-DOS profileには1件以上のworld_profilesが必要です。")
    seen: set[str] = set()
    for world in worlds:
        if not isinstance(world, dict):
            raise ValueError("world profileはobjectである必要があります。")
        world_id = world.get("id")
        if not isinstance(world_id, str) or not SAFE_ID.fullmatch(world_id):
            raise ValueError("world profile idは安全なlowercase slugである必要があります。")
        if world_id in seen:
            raise ValueError(f"world profile idが重複しています: {world_id}")
        seen.add(world_id)
        for key in ("authority", "fact_scope", "registry_ref", "causality_profile"):
            if not isinstance(world.get(key), str) or not world[key]:
                raise ValueError(f"{world_id}には{key}が必要です。")
    return profile


def _select_world(profile: dict[str, Any], world_id: str | None) -> dict[str, Any]:
    selected_id = world_id or profile["default_world_profile"]
    for world in profile["world_profiles"]:
        if world["id"] == selected_id:
            return world
    raise ValueError(f"未登録のworld profileです: {selected_id}")


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def boot_sphere_dos(
    repo_root: Path | None = None,
    world_id: str | None = None,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    profile = load_sphere_dos_profile(root)
    world = _select_world(profile, world_id)
    workspace = workspace_status(root)
    workspace_file = write_code_workspace(root, workspace)
    observed = datetime.now(timezone.utc)
    session_id = f"{observed.strftime('%Y%m%dT%H%M%S%fZ')}-{world['id']}"
    session_root = root / STATE_ROOT / "sessions" / session_id

    present = [item["id"] for item in workspace["components"] if item["state"] == "ready"]
    missing = [item["id"] for item in workspace["components"] if item["state"] != "ready"]
    runtime_state = "development-shell-ready" if not missing else "development-shell-partial"
    receipt = {
        "schema_version": "1.0.0",
        "session_id": session_id,
        "product": profile["product"],
        "coordinate_system": profile["coordinate_system"],
        "canonical_coordinate": profile["canonical_coordinate"],
        "design_line": profile["design_line"],
        "edition": profile["edition"],
        "distribution": profile["distribution"],
        "distribution_role": profile["distribution_role"],
        "runtime_state": runtime_state,
        "deployment_scope": "local-development-scaffold-only",
        "standalone_runtime_implemented": False,
        "world_profile": world,
        "workspace_file": str(workspace_file),
        "workspace_components_present": present,
        "workspace_components_unavailable": missing,
        "component_runtimes_started": [],
        "model_invoked": False,
        "network_access_performed": False,
        "authentication_started": False,
        "secret_scan_performed": False,
        "observed_at": observed.isoformat(timespec="seconds"),
        "clock_source": "host_system_clock",
        "clock_calibration": "unverified",
        "unknowns": list(profile.get("unknowns", [])),
    }
    _atomic_json(session_root / "receipt.json", receipt)
    current = {
        "schema_version": "1.0.0",
        "session_id": session_id,
        "runtime_state": runtime_state,
        "receipt": str(session_root / "receipt.json"),
        "updated_at": observed.isoformat(timespec="seconds"),
    }
    _atomic_json(root / STATE_ROOT / "current.json", current)
    return receipt


def sphere_dos_status(repo_root: Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    profile = load_sphere_dos_profile(root)
    current_path = root / STATE_ROOT / "current.json"
    if not current_path.is_file():
        return {
            "schema_version": "1.0.0",
            "distribution": profile["distribution"],
            "canonical_coordinate": profile["canonical_coordinate"],
            "runtime_state": "not-booted",
            "standalone_runtime_implemented": False,
            "mutations_performed": False,
            "network_access_performed": False,
        }
    current = load_json(current_path)
    receipt_path = Path(current.get("receipt", ""))
    if not receipt_path.is_absolute():
        receipt_path = root / receipt_path
    try:
        receipt_path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ValueError("Sphere-DOS current receiptがrepository外を指しています。") from error
    receipt = load_json(receipt_path)
    return {
        "schema_version": "1.0.0",
        "distribution": profile["distribution"],
        "canonical_coordinate": profile["canonical_coordinate"],
        "runtime_state": current.get("runtime_state", "unknown"),
        "session_id": current.get("session_id"),
        "receipt": str(receipt_path),
        "world_profile": receipt.get("world_profile"),
        "workspace_components_present": receipt.get("workspace_components_present", []),
        "workspace_components_unavailable": receipt.get(
            "workspace_components_unavailable", []
        ),
        "standalone_runtime_implemented": False,
        "mutations_performed": False,
        "network_access_performed": False,
    }


def format_sphere_dos(result: dict[str, Any]) -> str:
    lines = [
        f"Sphere-DOS: {str(result['runtime_state']).upper()}",
        "standalone runtime: NOT IMPLEMENTED",
    ]
    if result.get("session_id"):
        lines.append(f"session: {result['session_id']}")
    present = result.get("workspace_components_present", [])
    missing = result.get("workspace_components_unavailable", [])
    if present:
        lines.append(f"components ready: {', '.join(present)}")
    if missing:
        lines.append(f"components unavailable: {', '.join(missing)}")
    lines.append(
        "model: false; network: "
        f"{str(result.get('network_access_performed', False)).lower()}"
    )
    return "\n".join(lines)
