#!/usr/bin/env python3
"""固定revisionの明示fileだけを読み取り専用source capsuleへ展開する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONTRACT = PROJECT_ROOT / "experiments/m6xx-agent-orchestration/source-capsule.json"
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def load_contract(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("sources"), list):
        raise ValueError("source capsule contractにはsources arrayが必要です。")
    return value


def parse_repositories(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        source_id, separator, raw_path = value.partition("=")
        if not separator or not SAFE_ID.fullmatch(source_id) or not raw_path:
            raise ValueError("--repoはsource-id=/absolute/path形式で指定してください。")
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            raise ValueError(f"repository pathは絶対pathで指定してください: {source_id}")
        if source_id in result:
            raise ValueError(f"repository指定が重複しています: {source_id}")
        result[source_id] = path.resolve(strict=True)
    return result


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError(f"source file pathが安全な相対pathではありません: {value}")
    return path


def git_file(repository: Path, revision: str, relative: Path) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(repository), "show", f"{revision}:{relative.as_posix()}"],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"固定sourceを解決できません: {revision}:{relative}: {detail}")
    return completed.stdout


def build_capsule(contract: dict[str, Any], repositories: dict[str, Path], output: Path) -> dict[str, Any]:
    output = output.expanduser()
    if not output.is_absolute():
        raise ValueError("--outputは絶対pathで指定してください。")
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output directoryは空である必要があります: {output}")
    output.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, object]] = []
    total_bytes = 0
    for source in contract["sources"]:
        source_id = source.get("id")
        revision = source.get("revision")
        files = source.get("files")
        if not isinstance(source_id, str) or not SAFE_ID.fullmatch(source_id):
            raise ValueError("source idが不正です。")
        if not isinstance(revision, str) or not FULL_SHA.fullmatch(revision):
            raise ValueError(f"source revisionは40桁SHAである必要があります: {source_id}")
        if not isinstance(files, list) or not files:
            raise ValueError(f"source filesがありません: {source_id}")
        repository = repositories.get(source_id)
        if repository is None:
            raise ValueError(f"--repo指定がありません: {source_id}")
        for raw_relative in files:
            if not isinstance(raw_relative, str):
                raise ValueError(f"source fileは文字列である必要があります: {source_id}")
            relative = safe_relative(raw_relative)
            payload = git_file(repository, revision, relative)
            destination = output / source_id / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
            os.chmod(destination, 0o444)
            total_bytes += len(payload)
            entries.append(
                {
                    "source": source_id,
                    "revision": revision,
                    "path": relative.as_posix(),
                    "bytes": len(payload),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }
            )

    directories = sorted(
        (path for path in output.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    )
    for directory in directories:
        os.chmod(directory, 0o555)
    os.chmod(output, 0o555)
    return {
        "schema_version": "1.0.0",
        "capsule_id": contract.get("id"),
        "output": str(output),
        "file_count": len(entries),
        "total_bytes": total_bytes,
        "rough_token_upper_bound": (total_bytes + 2) // 3,
        "whole_repository_archive": False,
        "agent_output_included": False,
        "network_access_performed": False,
        "source_entries": entries,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--repo", action="append", default=[], help="source-id=/absolute/path")
    parser.add_argument("--output", type=Path, required=True, help="空の絶対path。")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        contract = load_contract(args.contract)
        receipt = build_capsule(contract, parse_repositories(args.repo), args.output)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    else:
        print(f"source capsule: {receipt['file_count']} files / {receipt['total_bytes']} bytes")
        print(f"output: {receipt['output']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
