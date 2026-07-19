from __future__ import annotations

import json
from pathlib import Path
import unittest

from atlantis_cli.versioning import (
    classify_connection,
    coordinate_display,
    validate_version_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class VersioningTestCase(unittest.TestCase):
    def load_fixture(self, name: str) -> dict[str, object]:
        return json.loads(
            (PROJECT_ROOT / "versioning/fixtures" / name).read_text(encoding="utf-8")
        )

    def test_三層座標はSemVer_patchとしてparseしない(self) -> None:
        contract = json.loads(
            (PROJECT_ROOT / "versioning/contract.json").read_text(encoding="utf-8")
        )

        self.assertEqual(coordinate_display(contract["current_coordinate"]), "0.250.1")
        result = validate_version_contract(PROJECT_ROOT)
        self.assertEqual(result["overall"], "pass", result["errors"])

    def test_十世代離れてもKernelとWorldが一致すれば陸続き候補(self) -> None:
        result = classify_connection(self.load_fixture("contiguous.json"))

        self.assertEqual(result["status"], "CONTIGUOUS-CANDIDATE")
        self.assertTrue(result["direct_rendering_allowed"])
        self.assertEqual(result["negotiated_capabilities"], ["oae-read"])

    def test_Kernel一致でもWorld_Config違いはPortal(self) -> None:
        result = classify_connection(self.load_fixture("portal.json"))

        self.assertEqual(result["status"], "PORTAL-REQUIRED")
        self.assertFalse(result["direct_rendering_allowed"])
        self.assertTrue(result["portal_required"])

    def test_Kernel違いは隔離projection付き因果Gate(self) -> None:
        result = classify_connection(self.load_fixture("cross-causal.json"))

        self.assertEqual(result["status"], "CROSS-CAUSAL-GATE-REQUIRED")
        self.assertTrue(result["projection_only"])
        self.assertFalse(result["source_mutation"])
        self.assertFalse(result["identity_continuity_inferred"])

    def test_Kernel違いでGate不明ならbottom(self) -> None:
        result = classify_connection(self.load_fixture("blocked.json"))

        self.assertEqual(result["status"], "BOTTOM")
        self.assertFalse(result["direct_rendering_allowed"])


if __name__ == "__main__":
    unittest.main()
