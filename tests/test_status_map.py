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
        self.assertEqual([item["items"] for item in result["maps"]], [7, 4])


if __name__ == "__main__":
    unittest.main()
