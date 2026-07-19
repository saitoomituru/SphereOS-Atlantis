from __future__ import annotations

from pathlib import Path
import unittest

from atlantis_cli.doctor import run_doctor


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class DoctorTestCase(unittest.TestCase):
    def test_doctorは読み取り専用で契約を検査する(self) -> None:
        result = run_doctor(PROJECT_ROOT)
        self.assertIn(result["overall"], {"pass", "warn"})
        self.assertFalse(result["mutations_performed"])
        self.assertFalse(result["network_access_performed"])
        self.assertEqual(result["observation_clock"]["calibration"], "unverified")
        checks = {item["name"]: item for item in result["checks"]}
        self.assertEqual(checks["git-worktree"]["status"], "pass")
        self.assertEqual(checks["agent-policy"]["status"], "pass")
        self.assertEqual(checks["tutorial-source-map"]["status"], "pass")
        self.assertEqual(checks["corn-stack"]["status"], "pass")
        self.assertEqual(checks["experience-receipts"]["status"], "pass")
        self.assertEqual(checks["forge-quest-status"]["status"], "pass")
        self.assertEqual(checks["release-candidate"]["status"], "pass")
        self.assertEqual(checks["note-template"]["status"], "pass")
        self.assertEqual(checks["note-registry"]["status"], "pass")
        self.assertEqual(checks["persona-registry"]["status"], "pass")
        self.assertEqual(checks["help-capabilities"]["status"], "pass")
        self.assertEqual(checks["version-coordinate"]["status"], "pass")
        self.assertEqual(checks["magi-skill-bundle"]["status"], "pass")
        self.assertEqual(checks["development-profile"]["status"], "pass")
        self.assertEqual(checks["markdown-links"]["status"], "pass")


if __name__ == "__main__":
    unittest.main()
