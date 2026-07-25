from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

from atlantis_cli.lineage import (
    inspect_lineage_receipt,
    load_lineage_contract,
    validate_lineage_receipt,
    validate_lineage_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = PROJECT_ROOT / "lineage" / "fixtures"


class LineageContractTests(unittest.TestCase):
    def test_contractと正負fixtureが成立する(self) -> None:
        result = validate_lineage_contract(PROJECT_ROOT)
        self.assertEqual(result["overall"], "pass", result["errors"])
        self.assertEqual(result["fixture_count"], 7)
        self.assertFalse(result["rights_adjudication_performed"])
        self.assertFalse(result["network_access_performed"])
        self.assertFalse(result["mutations_performed"])
        self.assertFalse(result["implicit_repository_scan_performed"])

    def test_local_onlyはpublic_manifest欠損ではない(self) -> None:
        result = inspect_lineage_receipt(
            FIXTURE_ROOT / "private-local-pass.json",
            PROJECT_ROOT,
        )
        self.assertEqual(result["status"], "PASS", result["errors"])
        self.assertEqual(result["distribution"], "local-only")

    def test狭いcommercial_extensionはcoreを囲い込まない(self) -> None:
        result = inspect_lineage_receipt(
            FIXTURE_ROOT / "narrow-commercial-pass.json",
            PROJECT_ROOT,
        )
        self.assertEqual(result["status"], "PASS", result["errors"])

    def test_official表示はscope付き制定authorityを必要とする(self) -> None:
        receipt = json.loads(
            (FIXTURE_ROOT / "gift-commons-pass.json").read_text(encoding="utf-8")
        )
        receipt["asset"]["designation"] = "official"
        contract = load_lineage_contract(PROJECT_ROOT)
        blocked = validate_lineage_receipt(receipt, contract)
        self.assertEqual(blocked["status"], "BLOCK")
        self.assertIn("designation_authority_ref", "\n".join(blocked["errors"]))

        receipt["asset"]["designation_authority_ref"] = "authority://selected-world/author"
        passed = validate_lineage_receipt(receipt, contract)
        self.assertEqual(passed["status"], "PASS", passed["errors"])

    def test_Roleはauthority_API_本人性を生成しない(self) -> None:
        result = inspect_lineage_receipt(
            FIXTURE_ROOT / "role-authority-leak-blocked.json",
            PROJECT_ROOT,
        )
        self.assertEqual(result["status"], "BLOCK")
        message = "\n".join(result["errors"])
        self.assertIn("claims.identity", message)
        self.assertIn("claims.authority", message)
        self.assertIn("claims.api_capability", message)
        self.assertIn("claims.religious_representation", message)

    def test_commons_captureと生secretとglobal_stopを拒否する(self) -> None:
        expectations = {
            "commons-capture-blocked.json": "open-core",
            "raw-secret-blocked.json": "生secret",
            "global-stop-blocked.json": "global stop",
        }
        for filename, fragment in expectations.items():
            with self.subTest(filename=filename):
                result = inspect_lineage_receipt(FIXTURE_ROOT / filename, PROJECT_ROOT)
                self.assertEqual(result["status"], "BLOCK")
                self.assertIn(fragment, "\n".join(result["errors"]))

    def test_CLIは明示receiptだけを検査する(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "atlantis_cli",
                "lineage",
                "inspect",
                "--receipt",
                str(FIXTURE_ROOT / "gift-commons-pass.json"),
                "--repo-root",
                str(PROJECT_ROOT),
                "--json",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["implicit_repository_scan_performed"])
        self.assertFalse(result["rights_adjudication_performed"])


if __name__ == "__main__":
    unittest.main()
