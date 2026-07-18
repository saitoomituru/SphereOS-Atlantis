from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from atlantis_cli.agent import build_contract, initialize_agent, plan_agent, verify_agent
from atlantis_cli.config import load_adapter, load_agent_registry


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class AgentContractTestCase(unittest.TestCase):
    def make_repo(self, base: Path) -> Path:
        (base / "note" / "templates").mkdir(parents=True)
        (base / "AGENTS.md").write_text("# test\n", encoding="utf-8")
        (base / "note" / "templates" / "brainstorm.ja.md").write_text("# {{TITLE}}\n", encoding="utf-8")
        shutil.copytree(PROJECT_ROOT / "agents", base / "agents")
        shutil.copytree(PROJECT_ROOT / "policy", base / "policy")
        return base

    def test_全adapterをregistryから解決する(self) -> None:
        registry = load_agent_registry(PROJECT_ROOT)
        for provider in registry["providers"]:
            adapter = load_adapter(PROJECT_ROOT, provider["id"])
            self.assertEqual(adapter["id"], provider["id"])

    def test_モック2体を別directoryへ初期化する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repo(Path(temporary))
            first = initialize_agent(root, "mock-a")
            second = initialize_agent(root, "mock-b")
            self.assertEqual(first.action, "created")
            self.assertEqual(second.action, "created")
            self.assertNotEqual(first.destination.parent, second.destination.parent)
            self.assertTrue(verify_agent(root, "mock-a")[0])
            self.assertTrue(verify_agent(root, "mock-b")[0])

            contract = json.loads(first.destination.read_text(encoding="utf-8"))
            receipt = contract["initialization_receipt"]
            self.assertFalse(receipt["model_invoked"])
            self.assertFalse(receipt["network_access_performed"])
            self.assertFalse(receipt["authentication_started"])
            self.assertEqual(
                contract["effective_contract"]["parallel_write_mode"],
                "isolated-git-worktree",
            )

    def test_policy変更後は明示refreshなしで上書きしない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repo(Path(temporary))
            initialize_agent(root, "mock-a")
            policy_path = root / "policy" / "constraints.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["test_revision"] = 2
            policy_path.write_text(json.dumps(policy), encoding="utf-8")

            self.assertEqual(plan_agent(root, "mock-a").action, "refresh-required")
            self.assertFalse(verify_agent(root, "mock-a")[0])
            with self.assertRaises(ValueError):
                initialize_agent(root, "mock-a")
            refreshed = initialize_agent(root, "mock-a", refresh=True)
            self.assertEqual(refreshed.action, "refreshed")
            self.assertTrue(verify_agent(root, "mock-a")[0])

    def test_未登録providerを拒否する(self) -> None:
        with self.assertRaises(ValueError):
            build_contract(PROJECT_ROOT, "../../outside")


if __name__ == "__main__":
    unittest.main()
