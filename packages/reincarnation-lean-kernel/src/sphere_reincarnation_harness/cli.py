"""filesystem Harness CLI。production Kernel CLIではない。

`plan`／`inspect`はfilesystemを変更しない。`init`／`evaluate`は明示root外へ書かない。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import layout, store
from .decisions import evaluate_and_record
from .errors import HarnessError


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _cmd_plan(args: argparse.Namespace) -> dict[str, Any]:
    return layout.plan(args.root)


def _cmd_init(args: argparse.Namespace) -> dict[str, Any]:
    root = layout.validate_root(args.root)
    return store.init_harness(root)


def _cmd_inspect(args: argparse.Namespace) -> dict[str, Any]:
    root = layout.validate_root(args.root)
    return store.inspect_harness(root)


def _cmd_evaluate(args: argparse.Namespace) -> dict[str, Any]:
    root = layout.validate_root(args.root)
    store.require_initialized(root)
    fixture_path = Path(args.fixture)
    with fixture_path.open("r", encoding="utf-8") as handle:
        fixture = json.load(handle)
    receipt_path = layout.harness_root(root) / "receipts" / "decisions.jsonl"
    envelope = evaluate_and_record(fixture, root, receipt_path)
    envelope["mutations_performed"] = True
    envelope["receipt_path"] = str(receipt_path)
    return envelope


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sphere_reincarnation_harness",
        description=(
            "Sphere Reincarnation Lean Kernel filesystem Harness "
            "(harness_only, production Kernelではない)"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    common_root = argparse.ArgumentParser(add_help=False)
    common_root.add_argument(
        "--root",
        default=None,
        help="明示test root。省略時はエラーで停止する(home/cwd既定値なし)。",
    )
    common_root.add_argument("--json", action="store_true", help="JSON出力する。")

    plan_parser = subparsers.add_parser(
        "plan", parents=[common_root], help="read-only: 初期化予定pathを表示する。"
    )
    plan_parser.set_defaults(handler=_cmd_plan)

    init_parser = subparsers.add_parser(
        "init", parents=[common_root], help="明示root配下へharness directoryを作成する。"
    )
    init_parser.set_defaults(handler=_cmd_init)

    inspect_parser = subparsers.add_parser(
        "inspect", parents=[common_root], help="read-only: harness stateを観測する。"
    )
    inspect_parser.set_defaults(handler=_cmd_inspect)

    evaluate_parser = subparsers.add_parser(
        "evaluate", parents=[common_root], help="synthetic fixtureをdecision envelopeへ評価する。"
    )
    evaluate_parser.add_argument("--fixture", required=True, help="fixture JSONへのpath。")
    evaluate_parser.set_defaults(handler=_cmd_evaluate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
    except HarnessError as error:
        _print_json(
            {
                "harness_only": True,
                "decision": "rejected",
                "reason_code": "harness-error",
                "message": str(error),
                "mutations_performed": False,
            }
        )
        return 1

    if args.json:
        _print_json(result)
    else:
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
