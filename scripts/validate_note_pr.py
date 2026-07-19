#!/usr/bin/env python3
"""fork-safeなNote-only PRを、networkとsecretなしで検査する。"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


REQUIRED_SECTIONS = (
    "## 事実・観測",
    "## 考察",
    "## 仮説・ブレスト",
    "## 内観メモ",
    "## 未解決・⊥",
    "## source・Provenance",
)
EXEMPT_PREFIXES = ("note/templates/", "note/transfer_plan/")
EXEMPT_FILES = {"note/AGENTS.md", "note/README.ja.md", "note/registry.json"}


def git_lines(root: Path, *arguments: str) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(completed.stderr.strip() or "git diffに失敗しました。")
    return [line for line in completed.stdout.splitlines() if line]


def validate(root: Path, base: str, head: str) -> tuple[int, list[str]]:
    changed = git_lines(root, "diff", "--name-only", base, head)
    if not changed:
        return 1, ["NOTE-PR-INVALID: 差分がありません。"]
    outside = [path for path in changed if not path.startswith("note/")]
    if outside:
        return 0, [
            "NOTE-ONLY-NOT-APPLICABLE: note/外の差分は通常CIが担当します。",
            *[f"outside: {path}" for path in outside],
        ]

    added = git_lines(root, "diff", "--diff-filter=A", "--name-only", base, head)
    errors: list[str] = []
    checked = 0
    for relative in added:
        path = root / relative
        if path.is_symlink():
            errors.append(f"symbolic linkはNote PRで追加できません: {relative}")
            continue
        if path.stat().st_size > 1_000_000:
            errors.append(f"1MBを超えるfileは別途reviewが必要です: {relative}")
        if relative in EXEMPT_FILES or relative.startswith(EXEMPT_PREFIXES):
            continue
        if path.suffix != ".md":
            errors.append(f"Note本文はMarkdownで追加してください: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        missing = [section for section in REQUIRED_SECTIONS if section not in text]
        if missing:
            errors.append(f"必須section不足: {relative}: {', '.join(missing)}")
        if "状態: `[DRAFT]`" not in text:
            errors.append(f"新規NoteはDRAFTで開始してください: {relative}")
        checked += 1

    if errors:
        return 1, ["NOTE-PR-FAIL", *errors]
    return 0, [
        "NOTE-PR-PASS",
        f"changed_files: {len(changed)}",
        f"new_note_documents_checked: {checked}",
        "network_access_performed: false",
        "secrets_required: false",
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        status, lines = validate(args.repo_root.resolve(), args.base, args.head)
    except (OSError, ValueError) as error:
        print(f"NOTE-PR-FAIL: {error}", file=sys.stderr)
        return 1
    print("\n".join(lines))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
