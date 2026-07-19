from __future__ import annotations

import json
from pathlib import Path
import subprocess
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


def make_git_component(target: Path, remote: str) -> str:
    target.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(target)], check=True)
    subprocess.run(
        ["git", "-C", str(target), "config", "user.name", "Atlantis Test"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(target), "config", "user.email", "test@example.invalid"],
        check=True,
    )
    (target / "README.md").write_text("fixture\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(target), "add", "README.md"], check=True)
    subprocess.run(
        ["git", "-C", str(target), "commit", "-q", "-m", "fixture"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(target), "remote", "add", "origin", remote],
        check=True,
    )
    return subprocess.run(
        ["git", "-C", str(target), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def write_component_manifest(root: Path, components: list[dict[str, object]]) -> None:
    payload = {
        "schema_version": "1.0.0",
        "workspace_id": "test-forge-profile",
        "workspace_root": ".atlantis/workspace/components",
        "components": components,
    }
    (root / "workspace/components.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


class WorkspaceTestCase(unittest.TestCase):
    def test_manifestとplanは既存環境を変更しない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository_fixture(root)
            manifest = load_workspace_manifest(root)
            self.assertEqual(manifest["workspace_id"], "sphereos-atlantis-0.25.1-forge")

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

    def test_GitLabのnetwork_remoteも受理する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository_fixture(root)
            manifest_path = root / "workspace/components.json"
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            payload["components"][0]["repository"] = "https://gitlab.com/example/project.git"
            manifest_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            manifest = load_workspace_manifest(root)

            self.assertEqual(
                manifest["components"][0]["repository"],
                "https://gitlab.com/example/project.git",
            )

    def test_dirty_worktreeはreadyにならない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository_fixture(root)
            remote = "https://gitlab.com/example/dirty.git"
            destination = root / ".atlantis/workspace/components/dirty"
            revision = make_git_component(destination, remote)
            write_component_manifest(
                root,
                [
                    {
                        "id": "dirty",
                        "role": "test",
                        "repository": remote,
                        "tracking_ref": "main",
                        "revision": revision,
                        "path": "dirty",
                        "required": True,
                    }
                ],
            )
            (destination / "untracked.txt").write_text("dirty\n", encoding="utf-8")

            result = workspace_status(root)

            self.assertEqual(result["components"][0]["state"], "dirty-worktree")
            self.assertEqual(result["overall"], "partial")

    def test_component指定初期化でも既存ready_componentをworkspaceから落とさない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository_fixture(root)
            first_remote = "https://gitlab.com/example/first.git"
            second_remote = "git@gitlab.com:example/second.git"
            first = root / ".atlantis/workspace/components/first"
            second = root / ".atlantis/workspace/components/second"
            first_revision = make_git_component(first, first_remote)
            second_revision = make_git_component(second, second_remote)
            write_component_manifest(
                root,
                [
                    {
                        "id": "first",
                        "role": "test",
                        "repository": first_remote,
                        "tracking_ref": "main",
                        "revision": first_revision,
                        "path": "first",
                        "required": True,
                    },
                    {
                        "id": "second",
                        "role": "test",
                        "repository": second_remote,
                        "tracking_ref": "main",
                        "revision": second_revision,
                        "path": "second",
                        "required": False,
                    },
                ],
            )

            from atlantis_cli.workspace import initialize_workspace

            result = initialize_workspace(root, ["first"])
            payload = json.loads(Path(result["workspace_file"]).read_text(encoding="utf-8"))

            self.assertEqual(result["requested_components"], ["first"])
            self.assertEqual(
                [folder["name"] for folder in payload["folders"]],
                ["SphereOS-Atlantis", "first", "second"],
            )


if __name__ == "__main__":
    unittest.main()
