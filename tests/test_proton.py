from __future__ import annotations

from pathlib import Path
import unittest

from atlantis_cli.proton import validate_proton_document


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ProtonTestCase(unittest.TestCase):
    def test_有効なProton文書を副作用なしで検査する(self) -> None:
        result = validate_proton_document(
            Path("proton/fixtures/valid.proton.md"), PROJECT_ROOT
        )

        self.assertEqual(result["status"], "pass", result["errors"])
        self.assertEqual(result["manifest"]["document_kind"], "wisdom")
        self.assertFalse(result["network_access_performed"])
        self.assertFalse(result["mutation_performed"])
        self.assertFalse(result["execution_performed"])

    def test_権限とOAEなしのexecuteを拒否する(self) -> None:
        result = validate_proton_document(
            Path("proton/fixtures/invalid-execution.proton.md"), PROJECT_ROOT
        )

        self.assertEqual(result["status"], "fail")
        self.assertIn(
            "executeにはauthority_required=trueが必要です。", result["errors"]
        )
        self.assertIn(
            "executeにはoae_transaction_required=trueが必要です。", result["errors"]
        )

    def test_FoldAccessMapper_Betaを検査する(self) -> None:
        result = validate_proton_document(
            Path("proton/modules/FoldAccessMapper.proton.md"), PROJECT_ROOT
        )

        self.assertEqual(result["status"], "pass", result["errors"])
        self.assertEqual(result["manifest"]["document_version"], "0.210.1-Beta")
        self.assertEqual(
            result["manifest"]["lineage"]["source_document_version"],
            "0.2.1-alpha",
        )
        self.assertGreaterEqual(result["blocks_checked"], 8)

    def test_FAM_Family責務文書を検査する(self) -> None:
        result = validate_proton_document(
            Path("proton/modules/FAMFamily.proton.md"), PROJECT_ROOT
        )

        self.assertEqual(result["status"], "pass", result["errors"])
        self.assertEqual(result["manifest"]["document_kind"], "architecture")
        self.assertIn("DESIGN-DECISION", result["manifest"]["claim_scopes"])


if __name__ == "__main__":
    unittest.main()
