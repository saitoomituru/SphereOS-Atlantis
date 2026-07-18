#!/usr/bin/env python3
"""標準PythonだけでAtlantis用venvを再構築する。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import venv


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def venv_python(root: Path) -> Path:
    windows = root / "Scripts" / "python.exe"
    return windows if windows.is_file() else root / "bin" / "python"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=PROJECT_ROOT,
        help="Atlantis repository root。fixture以外では通常指定しない。",
    )
    parser.add_argument(
        "--venv",
        type=Path,
        default=Path(".venv"),
        help="venv path。相対pathはrepository root基準。",
    )
    parser.add_argument(
        "--install-dev",
        action="store_true",
        help="requirements-dev.txtをpipで導入する。networkを使用する可能性がある。",
    )
    parser.add_argument("--json", action="store_true", help="receiptをJSONで出力する。")
    return parser


def bootstrap(
    repo_root: Path,
    requested_venv: Path,
    install_dev: bool = False,
) -> dict[str, object]:
    if sys.version_info < (3, 11):
        raise RuntimeError("Atlantis開発環境にはPython 3.11以上が必要です。")
    root = repo_root.expanduser().resolve()
    target = requested_venv.expanduser()
    if not target.is_absolute():
        target = root / target
    target = target.resolve()
    python = venv_python(target)
    existed = target.is_dir() and (target / "pyvenv.cfg").is_file() and python.is_file()
    if not existed:
        builder = venv.EnvBuilder(with_pip=True, clear=False, upgrade=False)
        builder.create(target)
        python = venv_python(target)
    if not python.is_file():
        raise RuntimeError(f"venv Pythonを確認できません: {python}")

    dependency_state = "not-requested"
    network_state = "not-requested"
    if install_dev:
        requirements = root / "requirements-dev.txt"
        if not requirements.is_file():
            raise RuntimeError(f"開発依存定義がありません: {requirements}")
        completed = subprocess.run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "-r",
                str(requirements),
            ],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise RuntimeError(f"開発依存の導入に失敗しました: {detail}")
        dependency_state = "installed-or-already-satisfied"
        network_state = "unknown-pip-may-use-index"

    version = subprocess.run(
        [str(python), "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    return {
        "schema_version": "1.0.0",
        "repository_root": str(root),
        "venv_root": str(target),
        "venv_python": str(python),
        "python_version": (version.stdout or version.stderr).strip(),
        "created": not existed,
        "dev_dependencies": dependency_state,
        "network_access": network_state,
        "model_invoked": False,
        "authentication_started": False,
    }


def format_receipt(receipt: dict[str, object]) -> str:
    return "\n".join(
        [
            f"Atlantis venv: {receipt['venv_root']}",
            f"Python: {receipt['python_version']}",
            f"created: {str(receipt['created']).lower()}",
            f"dev dependencies: {receipt['dev_dependencies']}",
            f"network: {receipt['network_access']}",
            "model invoked: false; authentication: false",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        receipt = bootstrap(args.repo_root, args.venv, args.install_dev)
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        parser.error(str(error))
    print(json.dumps(receipt, ensure_ascii=False, indent=2) if args.json else format_receipt(receipt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
