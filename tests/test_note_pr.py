from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.validate_note_pr import validate


NOTE = """# test

状態: `[DRAFT]`

## 事実・観測
未観測。
## 考察
未整理。
## 仮説・ブレスト
unknown
## 内観メモ
なし
## 未解決・⊥
- unknown
## source・Provenance
- 未記載
"""


class NotePullRequestTestCase(unittest.TestCase):
    def run_git(self, root: Path, *arguments: str) -> None:
        subprocess.run(["git", "-C", str(root), *arguments], check=True, capture_output=True)

    def test_noteだけの追加を受理する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.run_git(root, "init")
            self.run_git(root, "config", "user.email", "test@example.invalid")
            self.run_git(root, "config", "user.name", "test")
            (root / "README.md").write_text("base\n", encoding="utf-8")
            self.run_git(root, "add", "README.md")
            self.run_git(root, "commit", "-m", "base")
            base = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
            ).strip()
            (root / "note").mkdir()
            (root / "note/20260719-1000__test.ja.md").write_text(NOTE, encoding="utf-8")
            self.run_git(root, "add", "note")
            self.run_git(root, "commit", "-m", "note")

            status, lines = validate(root, base, "HEAD")

            self.assertEqual(status, 0)
            self.assertIn("NOTE-PR-PASS", lines)

    def test_note外を含む差分は通常CIへ渡す(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.run_git(root, "init")
            self.run_git(root, "config", "user.email", "test@example.invalid")
            self.run_git(root, "config", "user.name", "test")
            (root / "README.md").write_text("base\n", encoding="utf-8")
            self.run_git(root, "add", "README.md")
            self.run_git(root, "commit", "-m", "base")
            base = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
            ).strip()
            (root / "code.py").write_text("pass\n", encoding="utf-8")
            self.run_git(root, "add", "code.py")
            self.run_git(root, "commit", "-m", "code")

            status, lines = validate(root, base, "HEAD")

            self.assertEqual(status, 0)
            self.assertIn("NOTE-ONLY-NOT-APPLICABLE: note/外の差分は通常CIが担当します。", lines)


if __name__ == "__main__":
    unittest.main()
