#!/usr/bin/env python3
"""MAGI 0.2.1 Skillが毎回読む現行sourceを解決する。network accessは行わない。"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any


MAGI_ROOT = Path(__file__).resolve().parent
SOURCE_MAP_PATH = MAGI_ROOT / "source-map.json"


def load_map() -> dict[str, Any]:
    return json.loads(SOURCE_MAP_PATH.read_text(encoding="utf-8"))


def parse_roots(values: list[str]) -> dict[str, Path]:
    roots: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"--repo-rootはNAME=PATH形式です: {value}")
        name, raw = value.split("=", 1)
        roots[name] = Path(raw).expanduser().resolve()
    return roots


def ancestor_with_marker(start: Path, marker: str) -> Path | None:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / marker).is_file():
            return candidate
    return None


def discover_roots(
    source_map: dict[str, Any],
    explicit: dict[str, Path],
    profile: str | None,
) -> dict[str, Path]:
    roots = dict(explicit)
    atlantis_marker = source_map["repositories"]["SphereOS-Atlantis"]["marker"]
    atlantis = roots.get("SphereOS-Atlantis") or ancestor_with_marker(MAGI_ROOT, atlantis_marker)
    if atlantis:
        roots["SphereOS-Atlantis"] = atlantis

    if profile != "zeroroomlab":
        return roots

    manifest = roots.get("ZeroRoomLab-manifest")
    manifest_marker = source_map["repositories"]["ZeroRoomLab-manifest"]["marker"]
    configured = os.environ.get("ATLANTIS_MANIFEST_ROOT")
    if manifest is None and configured:
        candidate = Path(configured).expanduser().resolve()
        if (candidate / manifest_marker).is_file():
            manifest = candidate
    if manifest is None:
        starts = [Path.cwd(), MAGI_ROOT]
        if atlantis:
            starts.append(atlantis)
        for start in starts:
            for parent in (start.resolve(), *start.resolve().parents):
                candidate = parent / "ZeroRoomLab-manifest" / "ZeroRoomLab-manifest"
                if (candidate / manifest_marker).is_file():
                    manifest = candidate
                    break
            if manifest:
                break
    if manifest:
        roots["ZeroRoomLab-manifest"] = manifest
    return roots


def resolve(
    slot: str,
    profile: str | None,
    roots: dict[str, Path],
    source_map: dict[str, Any],
) -> dict[str, Any]:
    entries = [
        *({"source_layer": "core", **entry} for entry in source_map["common"]),
        *(
            {"source_layer": "core", **entry}
            for entry in source_map["slots"][slot]
        ),
    ]
    if profile:
        profile_map = source_map["profiles"][profile]
        entries.extend(
            {"source_layer": f"profile:{profile}", **entry}
            for entry in [*profile_map["common"], *profile_map["slots"][slot]]
        )
    sources: list[dict[str, Any]] = []
    for entry in entries:
        repository = entry["repository"]
        root = roots.get(repository)
        local_path = root / entry["path"] if root else None
        remote = source_map["repositories"][repository]["remote"]
        sources.append(
            {
                **entry,
                "local_path": str(local_path) if local_path else None,
                "local_exists": bool(local_path and local_path.is_file()),
                "public_url": f"{remote}/blob/main/{entry['path']}",
            }
        )
    missing = sum(item["required"] and not item["local_exists"] for item in sources)
    return {
        "schema_version": source_map["schema_version"],
        "slot": slot,
        "profile": profile,
        "sources": sources,
        "summary": {
            "sources": len(sources),
            "local_available": sum(item["local_exists"] for item in sources),
            "required_missing_locally": missing,
            "network_access_performed": False,
            "secret_scan_performed": False,
        },
    }


def main(argv: list[str] | None = None) -> int:
    source_map = load_map()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slot", required=True, choices=sorted(source_map["slots"]))
    parser.add_argument("--profile", choices=sorted(source_map["profiles"]))
    parser.add_argument("--repo-root", action="append", default=[], metavar="NAME=PATH")
    parser.add_argument("--require-local", action="store_true")
    args = parser.parse_args(argv)
    try:
        roots = discover_roots(source_map, parse_roots(args.repo_root), args.profile)
    except ValueError as error:
        parser.error(str(error))
    result = resolve(args.slot, args.profile, roots, source_map)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.require_local and result["summary"]["required_missing_locally"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
