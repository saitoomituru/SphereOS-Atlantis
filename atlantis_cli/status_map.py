"""Forge MapとQuest Mapの状態軸を検証する。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_json
from .note import find_repo_root


STATUS_REGISTRY_PATH = Path("status/registry.json")
MAP_PATHS = (Path("status/forge-map.json"), Path("status/quest-map.json"))


def validate_status_maps(repo_root: Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_json(root / STATUS_REGISTRY_PATH)
    errors: list[str] = []
    maps: list[dict[str, Any]] = []
    axes = registry.get("axes")
    if registry.get("schema_version") != "1.0.0" or not isinstance(axes, dict):
        raise ValueError("status registry契約が不正です。")
    expected_axes = set(axes)
    seen_ids: set[str] = set()
    for relative in MAP_PATHS:
        value = load_json(root / relative)
        items = value.get("items")
        if value.get("project_version") != registry.get("project_version"):
            errors.append(f"{relative}: project_versionがregistryと一致しません。")
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
    return {
        "schema_version": "1.0.0",
        "overall": "fail" if errors else "pass",
        "project_version": registry.get("project_version"),
        "maps": maps,
        "errors": errors,
        "network_access_performed": False,
        "mutations_performed": False,
    }


def format_status_maps(result: dict[str, Any]) -> str:
    lines = [f"overall: {result['overall']}", f"version: {result['project_version']}"]
    lines.extend(f"{item['path']}: {item['items']} items" for item in result["maps"])
    lines.extend(f"error: {error}" for error in result["errors"])
    return "\n".join(lines)
