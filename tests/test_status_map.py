from __future__ import annotations

from pathlib import Path
import unittest

from atlantis_cli.status_map import validate_status_maps


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class StatusMapTestCase(unittest.TestCase):
    def test_全itemが五軸と証拠を持つ(self) -> None:
        result = validate_status_maps(PROJECT_ROOT)

        self.assertEqual(result["overall"], "pass")
        self.assertEqual(result["project_version"], "0.25.1-alpha.1")
        self.assertEqual(result["canonical_coordinate"], "0.250.1")
        self.assertEqual([item["items"] for item in result["maps"]], [9, 5])
        self.assertEqual(result["capability_matrix"]["items"], 5)
        self.assertEqual(result["capability_matrix"]["as_of"], "2026-08-21")

    def test_能力状態表が実装と配布を別軸で保持する(self) -> None:
        result = validate_status_maps(PROJECT_ROOT)

        self.assertEqual(result["overall"], "pass")
        self.assertEqual(result["capability_matrix"]["path"], "status/capability-matrix.json")


if __name__ == "__main__":
    unittest.main()
