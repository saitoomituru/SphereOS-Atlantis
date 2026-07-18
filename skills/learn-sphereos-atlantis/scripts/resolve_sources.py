#!/usr/bin/env python3
"""Atlantisチュートリアルが毎回読むsourceのpathと公開URLを解決する。"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parent.parent
SOURCE_MAP_PATH = SKILL_ROOT / "references" / "source-map.json"


def load_source_map() -> dict[str, Any]:
    with SOURCE_MAP_PATH.open(encoding="utf-8") as stream:
        return json.load(stream)


def parse_repo_roots(values: list[str]) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"--repo-rootはNAME=PATH形式です: {value}")
        name, raw_path = value.split("=", 1)
        roots[name] = Path(raw_path).expanduser().resolve()
    return roots


def find_ancestor_with_marker(start: Path, marker: str) -> Path | None:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / marker).is_file():
            return candidate
    return None


def discover_roots(source_map: dict[str, Any], explicit: dict[str, Path]) -> dict[str, Path]:
    roots = dict(explicit)
    cwd = Path.cwd()

    atlantis = roots.get("SphereOS-Atlantis")
    if atlantis is None:
        marker = source_map["repositories"]["SphereOS-Atlantis"]["marker"]
        atlantis = find_ancestor_with_marker(cwd, marker)
        if atlantis is None:
            atlantis = find_ancestor_with_marker(SKILL_ROOT, marker)
        if atlantis is not None:
            roots["SphereOS-Atlantis"] = atlantis

    manifest = roots.get("ZeroRoomLab-manifest")
    if manifest is None:
        environment_path = os.environ.get("ATLANTIS_MANIFEST_ROOT")
        if environment_path:
            candidate = Path(environment_path).expanduser().resolve()
            marker = source_map["repositories"]["ZeroRoomLab-manifest"]["marker"]
            if (candidate / marker).is_file():
                manifest = candidate

    if manifest is None:
        starts = [cwd, SKILL_ROOT]
        if atlantis is not None:
            starts.append(atlantis)
        marker = source_map["repositories"]["ZeroRoomLab-manifest"]["marker"]
        for start in starts:
            for parent in (start.resolve(), *start.resolve().parents):
                candidate = parent / "ZeroRoomLab-manifest" / "ZeroRoomLab-manifest"
                if (candidate / marker).is_file():
                    manifest = candidate
                    break
            if manifest is not None:
                break

    if manifest is not None:
        roots["ZeroRoomLab-manifest"] = manifest
    return roots


def make_url(remote: str, path: str) -> str:
    return f"{remote}/blob/main/{path}"


def resolve(shelf: str, roots: dict[str, Path], source_map: dict[str, Any]) -> dict[str, Any]:
    entries = [*source_map["common"], *source_map["shelves"][shelf]]
    resolved: list[dict[str, Any]] = []
    missing_required_local = 0

    for entry in entries:
        repository = entry["repository"]
        root = roots.get(repository)
        local_path = root / entry["path"] if root is not None else None
        local_exists = bool(local_path and local_path.is_file())
        if entry.get("required", False) and not local_exists:
            missing_required_local += 1
        remote = source_map["repositories"][repository]["remote"]
        resolved.append(
            {
                **entry,
                "local_path": str(local_path) if local_path else None,
                "local_exists": local_exists,
                "public_url": make_url(remote, entry["path"]),
            }
        )

    return {
        "schema_version": source_map["schema_version"],
        "shelf": shelf,
        "policy": source_map["policy"],
        "repository_roots": {name: str(path) for name, path in sorted(roots.items())},
        "sources": resolved,
        "summary": {
            "sources": len(resolved),
            "local_available": sum(item["local_exists"] for item in resolved),
            "required_missing_locally": missing_required_local,
            "network_access_performed": False,
        },
    }


def format_text(result: dict[str, Any]) -> str:
    lines = [f"棚: {result['shelf']}"]
    for item in result["sources"]:
        state = "LOCAL" if item["local_exists"] else "URL-FALLBACK"
        target = item["local_path"] if item["local_exists"] else item["public_url"]
        lines.append(f"[{state}] {item['repository']}: {target}")
    summary = result["summary"]
    lines.append(
        f"local {summary['local_available']}/{summary['sources']}; "
        f"required missing {summary['required_missing_locally']}; network performed false"
    )
    return "\n".join(lines)


def build_parser(source_map: dict[str, Any]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shelf", required=True, choices=sorted(source_map["shelves"]))
    parser.add_argument(
        "--repo-root",
        action="append",
        default=[],
        metavar="NAME=PATH",
        help="既知のrepository rootを明示する。複数指定可能。",
    )
    parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    parser.add_argument(
        "--require-local",
        action="store_true",
        help="required sourceがローカルにない場合、終了コード2を返す。",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    source_map = load_source_map()
    parser = build_parser(source_map)
    args = parser.parse_args(argv)
    try:
        explicit = parse_repo_roots(args.repo_root)
    except ValueError as error:
        parser.error(str(error))
    roots = discover_roots(source_map, explicit)
    result = resolve(args.shelf, roots, source_map)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))
    if args.require_local and result["summary"]["required_missing_locally"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
