from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from sphere_reincarnation_harness import cli

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"


def run_cli(argv: list[str]) -> tuple[int, dict]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exit_code = cli.main(argv)
    return exit_code, json.loads(buffer.getvalue())


class CliRootTestCase(unittest.TestCase):
    def test_root省略時はエラーで停止しfilesystemを変更しない(self) -> None:
        exit_code, payload = run_cli(["plan", "--json"])

        self.assertEqual(exit_code, 1)
        self.assertEqual(payload["decision"], "rejected")
        self.assertEqual(payload["reason_code"], "harness-error")


class CliPlanInitInspectTestCase(unittest.TestCase):
    def test_plan_init_inspectの一連flowが動く(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-test-root"
            root.mkdir()

            plan_code, plan_payload = run_cli(["plan", "--root", str(root), "--json"])
            self.assertEqual(plan_code, 0)
            self.assertFalse(plan_payload["mutations_performed"])
            self.assertFalse((root / ".spheredos-harness").exists())

            init_code, init_payload = run_cli(["init", "--root", str(root), "--json"])
            self.assertEqual(init_code, 0)
            self.assertTrue(init_payload["mutations_performed"])
            self.assertTrue((root / ".spheredos-harness" / "harness.json").is_file())

            inspect_code, inspect_payload = run_cli(["inspect", "--root", str(root), "--json"])
            self.assertEqual(inspect_code, 0)
            self.assertTrue(inspect_payload["initialized"])


class CliEvaluateTestCase(unittest.TestCase):
    def test_evaluateはinit前だとharness_not_initializedで停止する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-test-root"
            root.mkdir()
            fixture = FIXTURES_DIR / "lease-missing.json"

            exit_code, payload = run_cli(
                ["evaluate", "--root", str(root), "--fixture", str(fixture), "--json"]
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(payload["decision"], "rejected")

    def test_evaluateはinit後にdecision_envelopeとreceiptを返す(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-test-root"
            root.mkdir()
            run_cli(["init", "--root", str(root), "--json"])
            fixture = FIXTURES_DIR / "lease-missing.json"

            exit_code, payload = run_cli(
                ["evaluate", "--root", str(root), "--fixture", str(fixture), "--json"]
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["decision"], "rejected")
            self.assertEqual(payload["reason_code"], "lease-missing")
            self.assertFalse(payload["effect_applied"])
            self.assertTrue(Path(payload["receipt_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
