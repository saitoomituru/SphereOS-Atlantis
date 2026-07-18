from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .agent import (
    build_contract,
    initialize_agent,
    plan_agent,
    resolve_root,
    verify_agent,
)
from .config import load_agent_registry
from .doctor import doctor_json, format_doctor, run_doctor
from .links import check_markdown_links, format_link_report
from .note import KINDS, SHELVES, create_note


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlantis",
        description="SphereOS Atlantisの文書・環境契約を補助する従属CLI",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    doctor_parser = commands.add_parser("doctor", help="環境を変更せずに診断する。")
    doctor_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    doctor_parser.add_argument("--json", action="store_true", help="JSONで出力する。")
    doctor_parser.add_argument(
        "--require-container",
        action="store_true",
        help="container runtime未検出をfailにする。",
    )

    links_parser = commands.add_parser("links", help="Markdownのrepository内参照をoffline検査する。")
    links_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    links_parser.add_argument("--json", action="store_true", help="JSONで出力する。")

    agent_parser = commands.add_parser("agent", help="コードエージェントの拘束付き初期化を行う。")
    agent_commands = agent_parser.add_subparsers(dest="agent_command", required=True)
    for name, help_text in (
        ("detect", "provider CLIを実行せず、PATH上の存在だけを検出する。"),
        ("plan", "生成予定のsession contractを表示する。"),
        ("init", "モデルを呼ばずsession contractだけを生成する。"),
        ("verify", "生成済みcontractと現行policy hashを検証する。"),
    ):
        subparser = agent_commands.add_parser(name, help=help_text)
        subparser.add_argument("--provider", action="append", default=[], help="provider ID。複数指定可能。")
        subparser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
        subparser.add_argument("--json", action="store_true", help="JSONで出力する。")
        if name == "init":
            subparser.add_argument("--refresh", action="store_true", help="差分のある生成済みcontractを更新する。")

    note_parser = commands.add_parser("note", help="未確定のブレストや観測をnoteへ保存する。")
    note_commands = note_parser.add_subparsers(dest="note_command", required=True)
    new_parser = note_commands.add_parser("new", help="雛形から衝突安全なnoteを作成する。")
    new_parser.add_argument("--title", required=True, help="noteの題名。")
    new_parser.add_argument("--shelf", required=True, choices=SHELVES, help="主に使用する棚。")
    new_parser.add_argument("--kind", default="brainstorm", choices=KINDS, help="noteの種別。")
    new_parser.add_argument("--scope", default="未整理。", help="対象・範囲の初期値。")
    new_parser.add_argument("--exclusions", default="未整理。", help="除外範囲の初期値。")
    new_parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="公開可能なsource。複数指定できる。秘密値を渡さない。",
    )
    new_parser.add_argument(
        "--authoring-agent",
        default="human-or-unspecified",
        help="作成主体。認証情報やsession IDを含めない。",
    )
    new_parser.add_argument(
        "--clock-calibration",
        default="unverified",
        choices=("calibrated", "unverified", "unknown"),
        help="ホスト時計の校正状態。既定は未確認。",
    )
    new_parser.add_argument("--repo-root", type=Path, help="Atlantis repository root。")
    new_parser.add_argument("--dry-run", action="store_true", help="予定pathだけを表示し、書き込まない。")
    new_parser.add_argument(
        "--timestamp",
        help="作成時刻の上書き。import・fixture用ISO 8601値。通常は指定しない。",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        try:
            result = run_doctor(args.repo_root, args.require_container)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(doctor_json(result) if args.json else format_doctor(result))
        return 1 if result["overall"] == "fail" else 0

    if args.command == "links":
        try:
            result = check_markdown_links(args.repo_root)
        except (OSError, ValueError) as error:
            parser.error(str(error))
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if args.json
            else format_link_report(result)
        )
        return 1 if result["status"] == "fail" else 0

    if args.command == "agent":
        try:
            root = resolve_root(args.repo_root)
            registry = load_agent_registry(root)
            known = [item["id"] for item in registry["providers"]]
            providers = args.provider or known
            output: list[dict[str, object]] = []
            failed = False
            for provider_id in providers:
                if args.agent_command == "detect":
                    contract = build_contract(root, provider_id)
                    provider = contract["provider"]
                    output.append({"provider": provider_id, "available": provider["available"], "executable": provider["detected_executable"]})
                elif args.agent_command == "plan":
                    plan = plan_agent(root, provider_id)
                    output.append({"provider": provider_id, "available": plan.available, "destination": str(plan.destination), "action": plan.action})
                elif args.agent_command == "init":
                    plan = initialize_agent(root, provider_id, args.refresh)
                    output.append({"provider": provider_id, "available": plan.available, "destination": str(plan.destination), "action": plan.action, "model_invoked": False, "network_access_performed": False})
                elif args.agent_command == "verify":
                    ok, message = verify_agent(root, provider_id)
                    failed = failed or not ok
                    output.append({"provider": provider_id, "ok": ok, "message": message})
            if args.json:
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                for item in output:
                    print(json.dumps(item, ensure_ascii=False))
            return 1 if failed else 0
        except (OSError, ValueError) as error:
            parser.error(str(error))

    if args.command == "note" and args.note_command == "new":
        try:
            result = create_note(
                title=args.title,
                shelf=args.shelf,
                kind=args.kind,
                scope=args.scope,
                exclusions=args.exclusions,
                sources=args.source,
                authoring_agent=args.authoring_agent,
                clock_calibration=args.clock_calibration,
                repo_root=args.repo_root,
                dry_run=args.dry_run,
                timestamp=args.timestamp,
            )
        except (OSError, ValueError) as error:
            parser.error(str(error))
        state = "DRY-RUN" if args.dry_run else "CREATED"
        print(f"[{state}] {result.path}")
        return 0

    parser.error("未対応のcommandです。")
    return 2


if __name__ == "__main__":
    sys.exit(main())
