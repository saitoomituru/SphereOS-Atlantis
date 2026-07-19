from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = PROJECT_ROOT / "skills" / "learn-sphereos-atlantis"


class TutorialSkillTestCase(unittest.TestCase):
    def load_source_map(self) -> dict[str, object]:
        return json.loads(
            (SKILL_ROOT / "references" / "source-map.json").read_text(encoding="utf-8")
        )

    def test_検疫製品ではなく抽象契約を棚へルーティングする(self) -> None:
        source_map = self.load_source_map()
        shelves = source_map["shelves"]
        engineering_paths = {item["path"] for item in shelves["engineering"]}
        gaming_paths = {item["path"] for item in shelves["gaming-trpg"]}
        sphere_paths = {item["path"] for item in shelves["sphere-architecture"]}

        browser_contract = "docs/development/browser-source-observation.ja.md"
        governance_contract = "docs/architecture/governance-scope-and-world-visa.ja.md"
        self.assertIn(browser_contract, engineering_paths)
        self.assertIn(governance_contract, engineering_paths)
        self.assertIn(governance_contract, gaming_paths)
        self.assertIn(governance_contract, sphere_paths)

        all_paths = {
            item["path"]
            for entries in shelves.values()
            for item in entries
        }
        self.assertFalse(any(path.startswith("note/") for path in all_paths))

    def test_engineering棚は追加正本をlocal解決する(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SKILL_ROOT / "scripts" / "resolve_sources.py"),
                "--shelf",
                "engineering",
                "--repo-root",
                f"SphereOS-Atlantis={PROJECT_ROOT}",
                "--json",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        resolved = {
            item["path"]: item
            for item in result["sources"]
            if item["repository"] == "SphereOS-Atlantis"
        }
        self.assertTrue(
            resolved["docs/development/browser-source-observation.ja.md"]["local_exists"]
        )
        self.assertTrue(
            resolved["docs/architecture/governance-scope-and-world-visa.ja.md"]["local_exists"]
        )
        self.assertFalse(result["summary"]["network_access_performed"])

    def test_全棚共通sourceにCORNとMAGIと参加契約を含む(self) -> None:
        source_map = self.load_source_map()
        common_paths = {item["path"] for item in source_map["common"]}

        self.assertIn("docs/operations/corn-stack.ja.md", common_paths)
        self.assertIn("docs/tutorial/help-and-capabilities.ja.md", common_paths)
        self.assertIn("docs/operations/corn-work-item-stack.ja.md", common_paths)
        self.assertIn(
            "docs/operations/participation-nonjurisdiction-and-experience.ja.md",
            common_paths,
        )
        self.assertIn("docs/theory/atlantis-magi-sdk-0.2.1.ja.md", common_paths)
        self.assertIn("docs/operations/context-ruler-and-causality-audit.ja.md", common_paths)
        self.assertIn("docs/operations/help-and-capability-discovery.ja.md", common_paths)
        self.assertIn("docs/theory/sphereos-atlantis-versioning-and-bootstrap.ja.md", common_paths)


if __name__ == "__main__":
    unittest.main()
