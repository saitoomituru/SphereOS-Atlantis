#!/usr/bin/env python3
"""Pinned revisionからSphereOS Atlantisの複数repository workspaceを展開する。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from atlantis_cli.workspace import (  # noqa: E402
    format_workspace_report,
    initialize_workspace,
    workspace_plan,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=PROJECT_ROOT,
        help="SphereOS Atlantis repository root。",
    )
    parser.add_argument(
        "--component",
        action="append",
        default=[],
        help="対象component ID。複数指定可能。省略時は全component。",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="networkを使用し、不足componentを固定revisionでcloneする。",
    )
    parser.add_argument("--json", action="store_true", help="receiptをJSONで出力する。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = (
            initialize_workspace(args.repo_root, args.component)
            if args.apply
            else workspace_plan(args.repo_root, args.component)
        )
    except (OSError, RuntimeError, ValueError) as error:
        parser.error(str(error))
    print(
        json.dumps(result, ensure_ascii=False, indent=2)
        if args.json
        else format_workspace_report(result)
    )
    blocked = result.get("blocked", [])
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
