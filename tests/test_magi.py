from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAGI_ROOT = PROJECT_ROOT / "magi" / "0.2.1"


class MagiSkillBundleTestCase(unittest.TestCase):
    def load_json(self, path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_三監査slotと支援slotを混ぜない(self) -> None:
        bundle = self.load_json(MAGI_ROOT / "bundle.json")
        self.assertEqual(bundle["version"], "0.2.1")
        self.assertEqual(
            [item["id"] for item in bundle["audit_slots"]],
            ["maxwell", "uriel", "raphael"],
        )
        self.assertEqual(len(bundle["support_slots"]), 1)
        chikuwa = bundle["support_slots"][0]
        self.assertEqual(chikuwa["id"], "chikuwa-cannon")
        self.assertIs(chikuwa["is_audit_dimension"], False)
        self.assertTrue(all(value is False for value in bundle["invariants"].values()))

    def test_Skillは人格でも神託でも外部操作でもない(self) -> None:
        bundle = self.load_json(MAGI_ROOT / "bundle.json")
        skill_paths = [item["skill"] for item in bundle["audit_slots"]]
        skill_paths.extend(item["skill"] for item in bundle["support_slots"])
        skill_paths.append(bundle["composite_skill"])
        for relative in skill_paths:
            skill_root = PROJECT_ROOT / relative
            text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue((skill_root / "agents" / "openai.yaml").is_file())
            self.assertIn("【告】", text)
            self.assertIn("神託: false", text)
            self.assertIn("外部操作: false", text)

    def test_resolverは隔離cloneでも公開参照だけを案内する(self) -> None:
        source_map = self.load_json(MAGI_ROOT / "source-map.json")
        for slot in source_map["slots"]:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(MAGI_ROOT / "resolve_sources.py"),
                    "--slot",
                    slot,
                    "--repo-root",
                    "ZeroRoomLab-manifest=/__atlantis_missing_manifest__",
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertFalse(result["summary"]["network_access_performed"])
            self.assertFalse(result["summary"]["secret_scan_performed"])
            self.assertGreater(result["summary"]["required_missing_locally"], 0)
            for source in result["sources"]:
                self.assertTrue(source["public_url"].startswith("https://github.com/"))

    def test_resolverの厳格modeは欠損を成功扱いしない(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(MAGI_ROOT / "resolve_sources.py"),
                "--slot",
                "composite",
                "--repo-root",
                "ZeroRoomLab-manifest=/__atlantis_missing_manifest__",
                "--require-local",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        result = json.loads(completed.stdout)
        self.assertGreater(result["summary"]["required_missing_locally"], 0)

    def validate_temporal(self, value: dict[str, object]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(MAGI_ROOT / "validate_temporal_receipt.py")],
            cwd=PROJECT_ROOT,
            input=json.dumps(value, ensure_ascii=False),
            capture_output=True,
            text=True,
            check=False,
        )

    def historical_unknown_receipt(self) -> dict[str, object]:
        return {
            "version": "0.2.1",
            "observation_mode": "current-interpretation-of-history",
            "observed_at": "2026-07-18T20:23:06+09:00",
            "historical_oae_status": "historical-oae-unavailable",
            "historical_oae_ref": None,
            "historical_role_attribution": "none",
            "retroactive_backfill": False,
            "same_worldline_mutation": False,
            "claims_physical_time_travel": False,
            "last_order": {
                "code": "OAE-HISTORY-UNKNOWN",
                "action": "stop-retroactive-backfill",
            },
        }

    def test_過去OAE不明はunknownとLast_Orderで停止する(self) -> None:
        completed = self.validate_temporal(self.historical_unknown_receipt())
        self.assertEqual(completed.returncode, 0, completed.stdout)
        self.assertTrue(json.loads(completed.stdout)["valid"])

    def test_過去OAE不明をLast_Orderなしで埋めない(self) -> None:
        value = self.historical_unknown_receipt()
        value.pop("last_order")
        completed = self.validate_temporal(value)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("Last Order", completed.stdout)

    def test_同一世界線への遡及OAE生成を拒否する(self) -> None:
        value = self.historical_unknown_receipt()
        value["retroactive_backfill"] = True
        value["historical_role_attribution"] = "commit-author-as-observer"
        completed = self.validate_temporal(value)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("retroactive_backfill", completed.stdout)
        self.assertIn("Agency role", completed.stdout)

    def test_7D_FoldはWorldとInstance_Ghostを共にsplitする(self) -> None:
        value = {
            "version": "0.2.1",
            "observation_mode": "counterfactual-branch",
            "observed_at": "2026-07-18T20:23:06+09:00",
            "historical_oae_status": "historical-oae-unavailable",
            "historical_oae_ref": None,
            "historical_role_attribution": "none",
            "retroactive_backfill": False,
            "same_worldline_mutation": False,
            "claims_physical_time_travel": False,
            "last_order": {
                "code": "OAE-HISTORY-UNKNOWN",
                "action": "stop-retroactive-backfill",
            },
            "branch_receipt": {
                "profile_ref": "fold://atlantis/akasha-driver@7d",
                "source_world_ref": "world://source",
                "source_instance_ghost_ref": "ghost://source",
                "target_world_ref": "world://branch",
                "target_instance_ghost_ref": "ghost://branch",
                "fork_point_ref": "event://fork",
                "provenance_ref": "evidence://source",
                "source_mutation": False,
                "status": "hypothetical",
            },
        }
        completed = self.validate_temporal(value)
        self.assertEqual(completed.returncode, 0, completed.stdout)

        value["branch_receipt"]["target_instance_ghost_ref"] = "ghost://source"
        completed = self.validate_temporal(value)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("Instance Ghost", completed.stdout)

    def test_物理空間のタイムマシン主張を拒否する(self) -> None:
        value = self.historical_unknown_receipt()
        value["claims_physical_time_travel"] = True
        completed = self.validate_temporal(value)
        self.assertEqual(completed.returncode, 2)
        self.assertIn("物理空間", completed.stdout)

    def test_将来依存を実装済みに見せない(self) -> None:
        bundle = self.load_json(MAGI_ROOT / "bundle.json")
        status = bundle["status"]
        for key in (
            "seven_d_fold_runtime",
            "akasha_driver",
            "backup_sdk",
            "kamui_collective_intelligence_gateway",
        ):
            self.assertEqual(status[key], "NOT_IMPLEMENTED")

    def test_7D軸名を正規Registryへ過剰確定しない(self) -> None:
        policy = self.load_json(MAGI_ROOT / "oae-temporal-policy.json")
        self.assertEqual(
            policy["branch_dimension_profile_status"],
            "PROVISIONAL_VALIDATOR_PROFILE",
        )
        self.assertEqual(
            policy["final_branch_dimension_registry"],
            "unknown-user-gate-required",
        )
        self.assertEqual(len(set(policy["provisional_branch_dimensions"])), 7)


if __name__ == "__main__":
    unittest.main()
