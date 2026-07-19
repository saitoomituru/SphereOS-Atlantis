from __future__ import annotations

from pathlib import Path
import unittest

from atlantis_cli.release import validate_release


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ReleaseTestCase(unittest.TestCase):
    def test_alpha候補はtag未作成で整合する(self) -> None:
        result = validate_release(PROJECT_ROOT)

        self.assertEqual(result["overall"], "pass")
        self.assertEqual(result["candidate"], "0.25.1-alpha.1")
        self.assertEqual(result["canonical_coordinate"], "0.250.1")
        self.assertEqual(result["tag_state"], "not-created")


if __name__ == "__main__":
    unittest.main()
