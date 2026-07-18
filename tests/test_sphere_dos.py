from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from atlantis_cli.sphere_dos import boot_sphere_dos, sphere_dos_status


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
    (target / "sphere-dos").mkdir()
    (target / "sphere-dos/profile.json").write_text(
        (PROJECT_ROOT / "sphere-dos/profile.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )


class SphereDosTestCase(unittest.TestCase):
    def test_bootはstandalone_runtimeを偽装しない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repository_fixture(root)
            receipt = boot_sphere_dos(root)

            self.assertFalse(receipt["standalone_runtime_implemented"])
            self.assertEqual(
                receipt["deployment_scope"],
                "local-development-scaffold-only",
            )
            self.assertEqual(receipt["component_runtimes_started"], [])
            self.assertFalse(receipt["network_access_performed"])
            self.assertEqual(receipt["runtime_state"], "development-shell-partial")

            status = sphere_dos_status(root)
            self.assertEqual(status["session_id"], receipt["session_id"])
            self.assertFalse(status["mutations_performed"])
            self.assertFalse(status["standalone_runtime_implemented"])


if __name__ == "__main__":
    unittest.main()
