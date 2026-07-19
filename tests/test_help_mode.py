from __future__ import annotations

from pathlib import Path
import json
from tempfile import TemporaryDirectory
import unittest

from atlantis_cli.help_mode import (
    build_help,
    format_help,
    list_interfaces,
    load_capability_registry,
    load_interface_registry,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class HelpModeTestCase(unittest.TestCase):
    def test_Helpはexpertを推定せず何も変更しない(self) -> None:
        result = build_help(repo_root=PROJECT_ROOT)

        self.assertEqual(result["status"], "HELP-READY")
        self.assertEqual(result["proficiency"], "unknown")
        self.assertEqual(result["intent"], "look-around")
        self.assertEqual(result["interface"]["id"], "command-line")
        self.assertEqual(result["detail"], "summary")
        self.assertTrue(result["capabilities"])
        self.assertTrue(
            all(item["state"] == "AVAILABLE-NOW" for item in result["capabilities"])
        )
        self.assertNotIn("standalone Atlantis runtime", format_help(result))
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

        all_result = build_help(detail="all", repo_root=PROJECT_ROOT)
        self.assertEqual(
            len(all_result["capabilities"]), len(registry["capabilities"])
        )
        self.assertIn(
            "standalone Atlantis runtime",
            {item["label_ja"] for item in all_result["capabilities"]},
        )

    def test_PLIとCLIを真贋ではなく操作面として分離する(self) -> None:
        registry = load_interface_registry(PROJECT_ROOT)
        interfaces = {item["id"]: item for item in registry["interfaces"]}

        prompt_line = interfaces["prompt-line"]
        command_line = interfaces["command-line"]
        self.assertEqual(prompt_line["primary_fit"]["axis"], "D")
        self.assertEqual(command_line["primary_fit"]["axis"], "L")
        self.assertIsNone(prompt_line["command_name"])
        self.assertIsNone(prompt_line["file_extension"])
        self.assertFalse(registry["authenticity_contract"]["prompt_line_is_cli_emulation"])
        self.assertFalse(
            registry["authenticity_contract"]["natural_language_is_fake_programming_language"]
        )

    def test_interfaceからdriverや権限やWorldを推定しない(self) -> None:
        result = list_interfaces(interface_id="prompt-line", repo_root=PROJECT_ROOT)
        prompt_line = result["interfaces"][0]

        self.assertTrue(all(prompt_line["does_not_infer"].values()))
        self.assertTrue(all(value is None for value in prompt_line["bindings"].values()))
        self.assertTrue(
            all(not item["selects_interface"] for item in result["execution_envelopes"])
        )
        self.assertFalse(result["mutation_performed"])
        self.assertFalse(result["network_access_performed"])
        self.assertEqual(
            result["presentation_contract"]["route_subject"],
            "current-request-and-explicit-context",
        )
        self.assertFalse(
            result["presentation_contract"]["persistent_person_classification"]
        )
        self.assertEqual(
            result["presentation_contract"]["default_boundary_disclosure"],
            "on-operation-request",
        )

    def test_prompt_lineを実行コマンド化するregistryを拒否する(self) -> None:
        registry = load_interface_registry(PROJECT_ROOT)
        for item in registry["interfaces"]:
            if item["id"] == "prompt-line":
                item["command_name"] = "pli"

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "help").mkdir()
            (root / "help/interfaces.json").write_text(
                json.dumps(registry, ensure_ascii=False), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "command名"):
                load_interface_registry(root)


if __name__ == "__main__":
    unittest.main()
