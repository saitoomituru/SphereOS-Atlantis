from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .note import KINDS, SHELVES, create_note


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlantis",
        description="SphereOS Atlantisの文書・環境契約を補助する従属CLI",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

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
