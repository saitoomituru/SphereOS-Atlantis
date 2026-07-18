from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAGI_ROOT = PROJECT_ROOT / "magi" / "0.2.0"


class MagiSkillBundleTestCase(unittest.TestCase):
    def load_json(self, path: Path) -> dict[str, object]:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_三監査slotと支援slotを混ぜない(self) -> None:
        bundle = self.load_json(MAGI_ROOT / "bundle.json")
        self.assertEqual(bundle["version"], "0.2.0")
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


if __name__ == "__main__":
    unittest.main()
