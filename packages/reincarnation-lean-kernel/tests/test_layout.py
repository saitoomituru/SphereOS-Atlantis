from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from sphere_reincarnation_harness import layout
from sphere_reincarnation_harness.errors import UnsafeRootError


class LayoutContractTestCase(unittest.TestCase):
    def test_layout契約はharness_onlyとproduction_kernel境界を宣言する(self) -> None:
        contract = layout.load_layout_contract()

        self.assertTrue(contract["harness_only"])
        self.assertFalse(contract["production_kernel"])
        self.assertEqual(contract["authority"], "none")
        self.assertEqual(contract["persistence_scope"], "explicit-test-root")
        self.assertIn(".spheredos-harness/harness.json", contract["generated_paths"])


class ValidateRootTestCase(unittest.TestCase):
    def test_root省略はUnsafeRootErrorで停止する(self) -> None:
        with self.assertRaises(UnsafeRootError):
            layout.validate_root(None)

    def test_空文字rootを拒否する(self) -> None:
        with self.assertRaises(UnsafeRootError):
            layout.validate_root("")

    def test_filesystem_rootを拒否する(self) -> None:
        with self.assertRaises(UnsafeRootError):
            layout.validate_root("/")

    def test_user_homeを拒否する(self) -> None:
        with self.assertRaises(UnsafeRootError):
            layout.validate_root(str(Path.home()))

    def test_repository_rootを拒否する(self) -> None:
        repo_root = Path(__file__).resolve()
        while not (repo_root / ".git").exists():
            if repo_root == repo_root.parent:
                self.fail("repository rootが見つかりませんでした。")
            repo_root = repo_root.parent
        with self.assertRaises(UnsafeRootError):
            layout.validate_root(str(repo_root))

    def test_明示rootは許可されresolve済みpathを返す(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            resolved = layout.validate_root(temporary)
            self.assertTrue(resolved.is_absolute())


class PlanTestCase(unittest.TestCase):
    def test_planはfilesystemを変更しない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-test-root"
            root.mkdir()

            result = layout.plan(str(root))

            self.assertFalse(result["mutations_performed"])
            self.assertFalse(result["already_initialized"])
            self.assertFalse((root / ".spheredos-harness").exists())
            self.assertTrue(result["harness_root"].endswith(".spheredos-harness"))


if __name__ == "__main__":
    unittest.main()
