from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from atlantis_cli.workspace import (
    load_workspace_manifest,
    workspace_plan,
    workspace_status,
    write_code_workspace,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def make_repository_fixture(target: Path) -> None:
    (target / "note/templates").mkdir(parents=True)
    (target / "note/templates/brainstorm.ja.md").write_text("# template\n", encoding="utf-8")
    (target / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    (target / "workspace").mkdir()
    (target / "workspace/components.json").write_text(
        (PROJECT_ROOT / "workspace/components.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )


class WorkspaceTestCase(unittest.TestCase):
    def test_manifestとplanは既存環境を変更しない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository_fixture(root)
            manifest = load_workspace_manifest(root)
            self.assertEqual(manifest["workspace_id"], "sphereos-atlantis-0.2.1-forge")

            result = workspace_plan(root)
            self.assertEqual(result["overall"], "partial")
            self.assertFalse(result["mutations_performed"])
            self.assertFalse(result["network_access_performed"])
            self.assertEqual(result["components"][0]["state"], "missing")
            self.assertEqual(result["actions"][0]["action"], "clone-pinned-revision")

    def test_VSCode_workspaceはreadyなcomponentだけを含む(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository_fixture(root)
            status = workspace_status(root)
            path = write_code_workspace(root, status)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["folders"],
                [{"name": "SphereOS-Atlantis", "path": ".."}],
            )


if __name__ == "__main__":
    unittest.main()
