"""明示root配下だけへ書き込むatomic JSON store。

削除command、`rm -rf`、recursive clean、home／repository全体scanは実装しない。
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .errors import (
    ExistingFileError,
    HarnessNotInitializedError,
    SymlinkEscapeError,
    UnsafeIdentifierError,
)
from .layout import (
    generated_directories,
    harness_json_path,
    harness_root,
    load_layout_contract,
    describe_harness_metadata,
)

_FORBIDDEN_ID_CHARS = ("/", "\\")


def validate_identifier(value: object, field: str) -> str:
    """world/fold/task/lease等のIDを検証する。pathとしては使わない値だがtraversal耐性を要求する。"""

    if not isinstance(value, str) or not value.strip():
        raise UnsafeIdentifierError(f"{field}には空でない文字列が必要です。")
    if ".." in value.split(os.sep) or ".." in value.split("/"):
        raise UnsafeIdentifierError(f"{field}に'..'を含めることはできません: {value}")
    if any(char in value for char in _FORBIDDEN_ID_CHARS):
        raise UnsafeIdentifierError(f"{field}にpath separatorを含めることはできません: {value}")
    if Path(value).is_absolute():
        raise UnsafeIdentifierError(f"{field}にabsolute pathは使用できません: {value}")
    return value


def resolve_within_root(root: Path, relative: Path) -> Path:
    """symlink解決後のpathがroot内であることを確認し、解決済みpathを返す。"""

    root_real = Path(os.path.realpath(root))
    candidate = root / relative
    candidate_real = Path(os.path.realpath(candidate))
    try:
        candidate_real.relative_to(root_real)
    except ValueError as error:
        raise SymlinkEscapeError(
            f"symlink解決後のpathがharness root外を指しています: {candidate} -> {candidate_real}"
        ) from error
    return candidate_real


def _atomic_write_text(target: Path, root: Path, text: str) -> None:
    # atomic replace前にtargetがroot内であることを再確認する。
    resolve_within_root(root, target.relative_to(root))
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        resolve_within_root(root, target.relative_to(root))
        os.replace(tmp_name, target)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def atomic_write_json(
    target: Path,
    root: Path,
    payload: dict[str, Any],
    *,
    overwrite: bool = False,
) -> None:
    resolve_within_root(root, target.relative_to(root))
    if not overwrite and target.exists():
        raise ExistingFileError(f"既存fileをsilent overwriteしません: {target}")
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    _atomic_write_text(target, root, text)


def append_receipt(target: Path, root: Path, entry: dict[str, Any]) -> None:
    """append-onlyなJSONL receiptへ1行追加する。既存行は書き換えない。"""

    resolve_within_root(root, target.relative_to(root))
    existing_lines: list[str] = []
    if target.exists():
        existing_lines = target.read_text(encoding="utf-8").splitlines()
    new_line = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    text = "\n".join([*existing_lines, new_line]) + "\n"
    _atomic_write_text(target, root, text)


def read_json(target: Path) -> dict[str, Any]:
    with target.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def init_harness(root: Path) -> dict[str, Any]:
    """明示root配下へharness directoryを作成する。既存harness.jsonはsilent overwriteしない。"""

    contract = load_layout_contract()
    base = harness_root(root)
    directories = generated_directories(root)
    for directory in directories:
        resolve_within_root(root, directory.relative_to(root))
        directory.mkdir(parents=True, exist_ok=True)

    metadata_path = harness_json_path(root)
    already_initialized = metadata_path.is_file()
    written = False
    if not already_initialized:
        atomic_write_json(
            metadata_path,
            root,
            describe_harness_metadata(root, contract),
            overwrite=False,
        )
        written = True

    return {
        "schema_version": contract["schema_version"],
        "harness_only": True,
        "production_kernel": False,
        "root": str(root),
        "harness_root": str(base),
        "already_initialized": already_initialized,
        "generated_directories": [str(path) for path in directories],
        "harness_json": str(metadata_path),
        "mutations_performed": written,
    }


def inspect_harness(root: Path) -> dict[str, Any]:
    """filesystemを変更せず、既存harness stateを観測する。"""

    contract = load_layout_contract()
    base = harness_root(root)
    metadata_path = harness_json_path(root)
    if not metadata_path.is_file():
        return {
            "schema_version": contract["schema_version"],
            "harness_only": True,
            "root": str(root),
            "harness_root": str(base),
            "initialized": False,
            "counts": {},
            "mutations_performed": False,
        }

    counts: dict[str, int] = {}
    for directory in generated_directories(root):
        counts[directory.name] = (
            sum(1 for entry in directory.iterdir()) if directory.is_dir() else 0
        )

    return {
        "schema_version": contract["schema_version"],
        "harness_only": True,
        "root": str(root),
        "harness_root": str(base),
        "initialized": True,
        "metadata": read_json(metadata_path),
        "counts": counts,
        "mutations_performed": False,
    }


def require_initialized(root: Path) -> Path:
    metadata_path = harness_json_path(root)
    if not metadata_path.is_file():
        raise HarnessNotInitializedError(
            f"harnessが未初期化です。先に`init --root {root}`を実行してください。"
        )
    return metadata_path
