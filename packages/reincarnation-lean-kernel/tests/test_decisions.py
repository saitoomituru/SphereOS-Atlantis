from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from sphere_reincarnation_harness import decisions
from sphere_reincarnation_harness.errors import FixtureError

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures"


def load_fixture(name: str) -> dict:
    with (FIXTURES_DIR / f"{name}.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


class EvaluateFixtureTestCase(unittest.TestCase):
    def test_valid_preparedはacceptedだがeffect_appliedはfalse(self) -> None:
        envelope = decisions.evaluate_fixture(load_fixture("valid-prepared"))

        self.assertEqual(envelope["decision"], "accepted")
        self.assertFalse(envelope["effect_applied"])

    def test_lease_missingはrejectedになる(self) -> None:
        envelope = decisions.evaluate_fixture(load_fixture("lease-missing"))

        self.assertEqual(envelope["decision"], "rejected")
        self.assertEqual(envelope["reason_code"], "lease-missing")
        self.assertFalse(envelope["effect_applied"])

    def test_stale_base_revisionはrejectedになる(self) -> None:
        envelope = decisions.evaluate_fixture(load_fixture("stale-base-revision"))

        self.assertEqual(envelope["decision"], "rejected")
        self.assertEqual(envelope["reason_code"], "stale-base-revision")
        self.assertFalse(envelope["effect_applied"])

    def test_write_set_violationはrejectedになる(self) -> None:
        envelope = decisions.evaluate_fixture(load_fixture("write-set-violation"))

        self.assertEqual(envelope["decision"], "rejected")
        self.assertEqual(envelope["reason_code"], "write-set-violation")
        self.assertFalse(envelope["effect_applied"])

    def test_duplicate_artifact_claimはrejectedになる(self) -> None:
        envelope = decisions.evaluate_fixture(load_fixture("duplicate-artifact-claim"))

        self.assertEqual(envelope["decision"], "rejected")
        self.assertEqual(envelope["reason_code"], "duplicate-artifact-claim")
        self.assertFalse(envelope["effect_applied"])

    def test_provider_exit_zero_not_commitはsuspendedで自動commitしない(self) -> None:
        envelope = decisions.evaluate_fixture(load_fixture("provider-exit-zero-not-commit"))

        self.assertEqual(envelope["decision"], "suspended")
        self.assertEqual(envelope["reason_code"], "provider-exit-zero-not-commit")
        self.assertFalse(envelope["effect_applied"])
        self.assertNotEqual(envelope["oae"]["oae_transaction_state"], "committed")

    def test_harness_onlyでないfixtureはFixtureErrorで停止する(self) -> None:
        fixture = load_fixture("valid-prepared")
        fixture["harness_only"] = False

        with self.assertRaises(FixtureError):
            decisions.evaluate_fixture(fixture)

    def test_canonical_contractがtrueのfixtureはFixtureErrorで停止する(self) -> None:
        fixture = load_fixture("valid-prepared")
        fixture["canonical_contract"] = True

        with self.assertRaises(FixtureError):
            decisions.evaluate_fixture(fixture)


class EvaluateAndRecordTestCase(unittest.TestCase):
    def test_evaluate_and_recordはappend_onlyでreceiptを残す(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt_path = root / "receipts" / "decisions.jsonl"

            first = decisions.evaluate_and_record(load_fixture("valid-prepared"), root, receipt_path)
            second = decisions.evaluate_and_record(load_fixture("lease-missing"), root, receipt_path)

            self.assertNotEqual(first["reason_code"], second["reason_code"])
            lines = receipt_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)


if __name__ == "__main__":
    unittest.main()
