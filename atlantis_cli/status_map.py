"""Forge MapとQuest Mapの状態軸を検証する。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_json
from .note import find_repo_root
from .versioning import validate_version_contract


STATUS_REGISTRY_PATH = Path("status/registry.json")
MAP_PATHS = (Path("status/forge-map.json"), Path("status/quest-map.json"))
CAPABILITY_MATRIX_PATH = Path("status/capability-matrix.json")


def validate_status_maps(repo_root: Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_json(root / STATUS_REGISTRY_PATH)
    errors: list[str] = []
    maps: list[dict[str, Any]] = []
    axes = registry.get("axes")
    capability_axes = registry.get("capability_matrix_axes")
    if (
        registry.get("schema_version") != "1.0.0"
        or not isinstance(axes, dict)
        or not isinstance(capability_axes, dict)
    ):
        raise ValueError("status registry契約が不正です。")
    expected_axes = set(axes)
    version_result = validate_version_contract(root)
    if version_result["overall"] != "pass":
        errors.extend(f"version contract: {error}" for error in version_result["errors"])
    elif registry.get("canonical_coordinate") != version_result["canonical_display"]:
        errors.append("status registryのcanonical coordinateがversion contractと一致しません。")
    seen_ids: set[str] = set()
    for relative in MAP_PATHS:
        value = load_json(root / relative)
        items = value.get("items")
        if value.get("project_version") != registry.get("project_version"):
            errors.append(f"{relative}: project_versionがregistryと一致しません。")
        if value.get("canonical_coordinate") != registry.get("canonical_coordinate"):
            errors.append(f"{relative}: canonical_coordinateがregistryと一致しません。")
        if not isinstance(items, list):
            errors.append(f"{relative}: itemsがarrayではありません。")
            continue
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                errors.append(f"{relative}: item idがありません。")
                continue
            item_id = item["id"]
            if item_id in seen_ids:
                errors.append(f"status item idが重複しています: {item_id}")
            seen_ids.add(item_id)
            statuses = item.get("status_axes")
            if not isinstance(statuses, dict) or set(statuses) != expected_axes:
                errors.append(f"{relative}: {item_id}: status_axesが不完全です。")
                continue
            for axis, state in statuses.items():
                if state not in axes[axis]:
                    errors.append(f"{relative}: {item_id}: {axis}={state}は未登録です。")
            if not isinstance(item.get("evidence"), list) or not item["evidence"]:
                errors.append(f"{relative}: {item_id}: evidenceがありません。")
            if not isinstance(item.get("unknowns"), list):
                errors.append(f"{relative}: {item_id}: unknownsがarrayではありません。")
        maps.append({"path": str(relative), "items": len(items)})
    matrix = load_json(root / CAPABILITY_MATRIX_PATH)
    matrix_items = matrix.get("items")
    if matrix.get("schema_version") != "1.0.0":
        errors.append("capability matrixのschema_versionが不正です。")
    if matrix.get("canonical_owner") != "SphereOS-Atlantis":
        errors.append("capability matrixの正本ownerがSphereOS-Atlantisではありません。")
    if not isinstance(matrix.get("as_of"), str) or not matrix["as_of"]:
        errors.append("capability matrixにas_ofがありません。")
    if not isinstance(matrix_items, list) or not matrix_items:
        errors.append("capability matrixにitemsがありません。")
        matrix_items = []

    expected_capability_axes = set(capability_axes)
    seen_capability_ids: set[str] = set()
    for item in matrix_items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append("capability matrixに文字列idのないitemがあります。")
            continue
        item_id = item["id"]
        if item_id in seen_capability_ids:
            errors.append(f"capability matrix item idが重複しています: {item_id}")
        seen_capability_ids.add(item_id)
        for key in ("label_ja", "responsibility_ja", "claim_scope_ja"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"capability matrix: {item_id}: {key}がありません。")
        statuses = item.get("status_axes")
        if not isinstance(statuses, dict) or set(statuses) != expected_capability_axes:
            errors.append(f"capability matrix: {item_id}: status_axesが不完全です。")
        else:
            for axis, state in statuses.items():
                if state not in capability_axes[axis]:
                    errors.append(
                        f"capability matrix: {item_id}: {axis}={state}は未登録です。"
                    )
        if not isinstance(item.get("evidence"), list) or not item["evidence"]:
            errors.append(f"capability matrix: {item_id}: evidenceがありません。")
        if not isinstance(item.get("unknowns_ja"), list):
            errors.append(f"capability matrix: {item_id}: unknowns_jaがarrayではありません。")

    return {
        "schema_version": "1.0.0",
        "overall": "fail" if errors else "pass",
        "project_version": registry.get("project_version"),
        "canonical_coordinate": registry.get("canonical_coordinate"),
        "maps": maps,
        "capability_matrix": {
            "path": str(CAPABILITY_MATRIX_PATH),
            "items": len(matrix_items),
            "as_of": matrix.get("as_of"),
        },
        "errors": errors,
        "network_access_performed": False,
        "mutations_performed": False,
    }


def format_status_maps(result: dict[str, Any]) -> str:
    lines = [f"overall: {result['overall']}", f"version: {result['project_version']}"]
    lines.extend(f"{item['path']}: {item['items']} items" for item in result["maps"])
    matrix = result["capability_matrix"]
    lines.append(f"{matrix['path']}: {matrix['items']} items / as-of={matrix['as_of']}")
    lines.extend(f"error: {error}" for error in result["errors"])
    return "\n".join(lines)
