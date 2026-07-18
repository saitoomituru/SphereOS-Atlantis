from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BOOTSTRAP = PROJECT_ROOT / "scripts" / "bootstrap_venv.py"


class BootstrapVenvTestCase(unittest.TestCase):
    def test_外部依存なしでvenvを作り再実行できる(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture_root = Path(temporary)
            command = [
                sys.executable,
                "-B",
                str(BOOTSTRAP),
                "--repo-root",
                str(fixture_root),
                "--json",
            ]
            first = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(first.returncode, 0, first.stderr)
            first_receipt = json.loads(first.stdout)
            self.assertTrue(first_receipt["created"])
            self.assertEqual(first_receipt["network_access"], "not-requested")
            self.assertFalse(first_receipt["model_invoked"])
            self.assertFalse(first_receipt["authentication_started"])
            self.assertTrue(Path(first_receipt["venv_python"]).is_file())

            second = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(second.returncode, 0, second.stderr)
            second_receipt = json.loads(second.stdout)
            self.assertFalse(second_receipt["created"])

            self_bootstrap = subprocess.run(
                [second_receipt["venv_python"], *command[1:]],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(self_bootstrap.returncode, 0, self_bootstrap.stderr)
            self.assertFalse(json.loads(self_bootstrap.stdout)["created"])

            version = subprocess.run(
                [second_receipt["venv_python"], "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(version.returncode, 0)
            self.assertIn("Python", version.stdout or version.stderr)


if __name__ == "__main__":
    unittest.main()
