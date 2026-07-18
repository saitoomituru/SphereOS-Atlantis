from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from atlantis_cli.note import create_note, find_repo_root, sanitize_title


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = PROJECT_ROOT / "note" / "templates" / "brainstorm.ja.md"


class NoteTestCase(unittest.TestCase):
    def make_repo(self, base: Path) -> Path:
        (base / "note" / "templates").mkdir(parents=True)
        (base / "AGENTS.md").write_text("# test\n", encoding="utf-8")
        (base / "note" / "templates" / "brainstorm.ja.md").write_text(
            TEMPLATE.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        return base

    def test_noteを固定時刻と未校正時計で作る(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repo(Path(temporary))
            result = create_note(
                title="川の神様OAEブレスト",
                shelf="spiritual",
                repo_root=root,
                timestamp="2026-07-18T16:45:00+09:00",
                sources=["user brainstorm"],
            )
            self.assertEqual(
                result.path.name,
                "20260718-1645__川の神様OAEブレスト.ja.md",
            )
            self.assertTrue(result.path.is_file())
            text = result.path.read_text(encoding="utf-8")
            self.assertIn("clock_calibration: unverified", text)
            self.assertIn("## 内観メモ `[POEM]`", text)
            self.assertIn("- user brainstorm", text)

    def test_同じ分と題名でも既存noteを上書きしない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repo(Path(temporary))
            arguments = {
                "title": "同じ話",
                "shelf": "gaming-trpg",
                "repo_root": root,
                "timestamp": "2026-07-18T16:45:00+09:00",
            }
            first = create_note(**arguments)
            second = create_note(**arguments)
            self.assertEqual(first.path.name, "20260718-1645__同じ話.ja.md")
            self.assertEqual(second.path.name, "20260718-1645__同じ話_02.ja.md")
            self.assertTrue(first.path.is_file())
            self.assertTrue(second.path.is_file())

    def test_dry_runは書き込まない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repo(Path(temporary))
            result = create_note(
                title="書かない",
                shelf="engineering",
                repo_root=root,
                timestamp="2026-07-18T16:45:00+09:00",
                dry_run=True,
            )
            self.assertFalse(result.path.exists())
            self.assertTrue(result.dry_run)

    def test_危険なファイル名文字を除去する(self) -> None:
        self.assertEqual(sanitize_title('A/B:C*D? "E"'), "A_B_C_D_E")

    def test_子directoryからrepository_rootを解決する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repo(Path(temporary))
            child = root / "docs" / "nested"
            child.mkdir(parents=True)
            self.assertEqual(find_repo_root(child), root.resolve())


if __name__ == "__main__":
    unittest.main()
