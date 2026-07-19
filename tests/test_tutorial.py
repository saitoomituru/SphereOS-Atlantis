from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from atlantis_cli.tutorial import start_tutorial


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TutorialTestCase(unittest.TestCase):
    def test_複数の自己申告personaを同時に解決する(self) -> None:
        result = start_tutorial(
            ["カソリック", "SRハンター"],
            repo_root=PROJECT_ROOT,
        )

        self.assertEqual(result["status"], "HELP-READY")
        self.assertEqual(result["route"], "help")
        self.assertIn("catholic-practitioner", result["matched_profiles"])
        self.assertIn("sr-hunter", result["matched_profiles"])
        self.assertFalse(result["identity_inferred"])
        self.assertFalse(result["permissions_granted"])
        self.assertEqual(result["context_status"], "CONTEXT-READ-REQUIRED")

    def test_未登録personaは拒否せず本人確認へ返す(self) -> None:
        result = start_tutorial(["まだ名前のない遊び方"], repo_root=PROJECT_ROOT)

        self.assertEqual(result["status"], "PROVISIONAL-USER-CONFIRMATION")
        self.assertEqual(result["unresolved_personas"], ["まだ名前のない遊び方"])
        self.assertEqual(result["entry_shelves"], ["cross-shelf"])

    def test_registry追加だけで新しいprofileを解決できる(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in (
                "AGENTS.md",
                "note/templates/brainstorm.ja.md",
                "note/registry.json",
                "tutorial/personas.json",
                "skills/learn-sphereos-atlantis/references/source-map.json",
            ):
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(
                    (PROJECT_ROOT / relative).read_text(encoding="utf-8"),
                    encoding="utf-8",
                )
            registry_path = root / "tutorial/personas.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["profiles"].append(
                {
                    "id": "new-player",
                    "aliases": ["新しい遊び手"],
                    "entry_shelves": ["gaming-trpg"],
                    "recommended_route": "note-only",
                }
            )
            registry_path.write_text(
                json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            result = start_tutorial(["新しい遊び手"], repo_root=root)

            self.assertEqual(result["matched_profiles"], ["new-player"])
            self.assertEqual(result["status"], "HELP-READY")

    def test_工学personaでも既定でcodingを開始しない(self) -> None:
        result = start_tutorial(["サーバーレスエンジニア"], repo_root=PROJECT_ROOT)

        self.assertEqual(result["route"], "help")
        self.assertEqual(result["proficiency"], "unknown")
        self.assertEqual(result["intent"], "look-around")
        self.assertFalse(result["route_contract"]["allows_code_change"])
        self.assertFalse(result["mutation_performed"])

    def test_明示implementでも実装routeの計画だけを返す(self) -> None:
        result = start_tutorial(
            ["サーバーレスエンジニア"],
            intent="implement",
            repo_root=PROJECT_ROOT,
        )

        self.assertEqual(result["route"], "full-development")
        self.assertEqual(result["context_status"], "CONTEXT-READ-REQUIRED")
        self.assertFalse(result["mutations_performed"])


if __name__ == "__main__":
    unittest.main()
