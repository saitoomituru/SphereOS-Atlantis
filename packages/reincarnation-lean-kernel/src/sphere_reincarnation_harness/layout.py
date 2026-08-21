"""明示root限定のfilesystem layout契約。

正式dotfiles仕様ではない。`~/.spheredos`やrepository rootへ自動作成しない。
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .errors import UnsafeRootError

_LAYOUT_CONTRACT_PATH = Path(__file__).resolve().parents[2] / "layout.json"
HARNESS_DIR_NAME = ".spheredos-harness"

_SUBDIRECTORIES = (
    "worlds",
    "folds",
    "tasks",
    "leases",
    "transactions",
    "receipts",
    "artifacts",
    "providers",
    "decisions",
)


def load_layout_contract() -> dict[str, Any]:
    """packageに同梱されたlayout契約を読む。root非依存。"""

    with _LAYOUT_CONTRACT_PATH.open("r", encoding="utf-8") as handle:
        contract = json.load(handle)
    if contract.get("harness_only") is not True:
        raise UnsafeRootError("layout契約のharness_onlyがtrueではありません。")
    if contract.get("production_kernel") is not False:
        raise UnsafeRootError("layout契約のproduction_kernelがfalseではありません。")
    return contract


def _is_repository_root(path: Path) -> bool:
    return (path / ".git").exists()


def validate_root(raw_root: str | os.PathLike[str] | None) -> Path:
    """明示rootを検証し、resolve済みPathを返す。書き込みは行わない。"""

    if raw_root is None:
        raise UnsafeRootError("rootが省略されています。homeやcwdを既定値にしません。")
    text = os.fspath(raw_root)
    if not text.strip():
        raise UnsafeRootError("空文字のrootは使用できません。")

    root = Path(text).expanduser()
    resolved = Path(os.path.realpath(root))

    if resolved == resolved.parent:
        raise UnsafeRootError(f"filesystem rootをharness rootにはできません: {resolved}")

    home = Path(os.path.realpath(Path.home()))
    if resolved == home:
        raise UnsafeRootError(f"user homeそのものをharness rootにはできません: {resolved}")

    if _is_repository_root(resolved):
        raise UnsafeRootError(f"repository rootをharness rootにはできません: {resolved}")

    return resolved


def harness_root(root: Path) -> Path:
    return root / HARNESS_DIR_NAME


def harness_json_path(root: Path) -> Path:
    return harness_root(root) / "harness.json"


def generated_directories(root: Path) -> list[Path]:
    base = harness_root(root)
    return [base / name for name in _SUBDIRECTORIES]


def plan(raw_root: str | os.PathLike[str] | None) -> dict[str, Any]:
    """filesystemを変更せず、初期化予定のpathと安全判定だけを返す。"""

    root = validate_root(raw_root)
    contract = load_layout_contract()
    base = harness_root(root)
    directories = generated_directories(root)
    harness_json = harness_json_path(root)
    return {
        "schema_version": contract["schema_version"],
        "harness_only": True,
        "production_kernel": False,
        "root": str(root),
        "harness_root": str(base),
        "already_initialized": harness_json.is_file(),
        "generated_directories": [str(path) for path in directories],
        "harness_json": str(harness_json),
        "prohibited_roots": contract["prohibited_roots"],
        "unknowns": contract["unknowns"],
        "mutations_performed": False,
    }


def describe_harness_metadata(root: Path, contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": contract["schema_version"],
        "harness_only": True,
        "production_kernel": False,
        "authority": "none",
        "persistence_scope": contract["persistence_scope"],
        "protocol_generation": contract["protocol_generation"],
        "function_series": contract["function_series"],
        "root": str(root),
    }
