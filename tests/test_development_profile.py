from __future__ import annotations

import json
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class DevelopmentProfileTestCase(unittest.TestCase):
    def test_VSCodeとDevContainerは共同設定だけを持つ(self) -> None:
        vscode = PROJECT_ROOT / ".vscode"
        for name in ("extensions.json", "settings.json", "tasks.json", "launch.json"):
            json.loads((vscode / name).read_text(encoding="utf-8"))

        container = json.loads(
            (PROJECT_ROOT / ".devcontainer" / "devcontainer.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            container["image"],
            "mcr.microsoft.com/devcontainers/python:3-3.12-bookworm",
        )
        self.assertEqual(container["remoteUser"], "vscode")
        self.assertIn("bootstrap_venv.py --install-dev", container["postCreateCommand"])
        self.assertNotIn("mounts", container)
        self.assertNotIn("forwardPorts", container)
        self.assertNotIn("repositories", json.dumps(container))

    def test_CIはread_only権限と公式Actionを使う(self) -> None:
        workflow = (PROJECT_ROOT / ".github" / "workflows" / "verify.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("contents: read", workflow)
        self.assertIn("actions/checkout@v6", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("actions/setup-python@v6", workflow)
        self.assertIn('python-version: ["3.11", "3.14"]', workflow)
        self.assertIn("clean_room_test.py", workflow)
        self.assertNotIn("git push", workflow)


if __name__ == "__main__":
    unittest.main()
