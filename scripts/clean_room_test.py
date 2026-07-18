#!/usr/bin/env python3
"""Git追跡済みrevisionだけを隔離展開し、offlineで最小再構築を試す。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = "\n".join(part for part in (completed.stdout, completed.stderr) if part).strip()
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{detail}")
    return completed


def safe_extract(archive: Path, destination: Path) -> None:
    destination_root = destination.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for item in bundle.infolist():
            target = (destination_root / item.filename).resolve()
            if target != destination_root and destination_root not in target.parents:
                raise RuntimeError(f"archive pathが隔離directory外を指しています: {item.filename}")
        bundle.extractall(destination_root)


def clean_room(ref: str = "HEAD") -> dict[str, object]:
    revision = run(["git", "rev-parse", "--verify", ref], PROJECT_ROOT).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="atlantis-clean-room-") as temporary:
        base = Path(temporary)
        archive = base / "tracked.zip"
        checkout = base / "checkout"
        checkout.mkdir()

        run(["git", "archive", "--format=zip", "-o", str(archive), ref], PROJECT_ROOT)
        safe_extract(archive, checkout)
        run(["git", "-c", "init.defaultBranch=main", "init", "-q"], checkout)

        bootstrap = run(
            [
                sys.executable,
                "-B",
                "scripts/bootstrap_venv.py",
                "--repo-root",
                str(checkout),
                "--json",
            ],
            checkout,
        )
        bootstrap_receipt = json.loads(bootstrap.stdout)
        python = str(bootstrap_receipt["venv_python"])
        tests = run([python, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], checkout)
        doctor = run([python, "-B", "-m", "atlantis_cli", "doctor", "--json"], checkout)
        doctor_receipt = json.loads(doctor.stdout)

        test_lines = [line for line in tests.stderr.splitlines() if line.strip()]
        return {
            "schema_version": "1.0.0",
            "source_revision": revision,
            "archive_scope": "git-tracked-files-only",
            "venv_created": bootstrap_receipt["created"],
            "network_access": bootstrap_receipt["network_access"],
            "unit_test_summary": test_lines[-1] if test_lines else "completed",
            "doctor_overall": doctor_receipt["overall"],
            "model_invoked": False,
            "authentication_started": False,
            "secret_scan_performed": False,
            "temporary_checkout_removed_on_exit": True,
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="検証するGit revision。既定はHEAD。")
    parser.add_argument("--json", action="store_true", help="receiptをJSONで出力する。")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        receipt = clean_room(args.ref)
    except (OSError, RuntimeError, subprocess.SubprocessError, zipfile.BadZipFile) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    else:
        print(f"Atlantis clean room: {str(receipt['doctor_overall']).upper()}")
        print(f"revision: {receipt['source_revision']}")
        print(f"tests: {receipt['unit_test_summary']}")
        print("network/model/auth/secret-scan: not performed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
