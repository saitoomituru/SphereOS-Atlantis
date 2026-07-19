from __future__ import annotations

from pathlib import Path
import unittest

from atlantis_cli.help_mode import build_help, load_capability_registry


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class HelpModeTestCase(unittest.TestCase):
    def test_Helpはexpertを推定せず何も変更しない(self) -> None:
        result = build_help(repo_root=PROJECT_ROOT)

        self.assertEqual(result["status"], "HELP-READY")
        self.assertEqual(result["proficiency"], "unknown")
        self.assertEqual(result["intent"], "look-around")
        self.assertFalse(result["identity_inferred"])
        self.assertFalse(result["permissions_granted"])
        self.assertFalse(result["mutation_performed"])
        self.assertFalse(result["network_access_performed"])

    def test_工学personaも既定では実装を開始しない(self) -> None:
        result = build_help(personas=["サーバーレスエンジニア"], repo_root=PROJECT_ROOT)

        self.assertEqual(result["tutorial"]["route"], "help")
        self.assertEqual(result["tutorial"]["proficiency"], "unknown")
        self.assertFalse(result["tutorial"]["route_contract"]["allows_code_change"])

    def test_能力状態を分離して表示する(self) -> None:
        registry = load_capability_registry(PROJECT_ROOT)
        states = {item["state"] for item in registry["capabilities"]}

        self.assertTrue(
            {"AVAILABLE-NOW", "SCAFFOLDED", "NOT-IMPLEMENTED", "NOT-TESTED", "RESOURCE-WAIT"}
            <= states
        )
        result = build_help(state="NOT-IMPLEMENTED", repo_root=PROJECT_ROOT)
        self.assertTrue(result["capabilities"])
        self.assertTrue(all(item["state"] == "NOT-IMPLEMENTED" for item in result["capabilities"]))


if __name__ == "__main__":
    unittest.main()
