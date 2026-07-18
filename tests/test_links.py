from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from atlantis_cli.links import check_markdown_links


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class MarkdownLinkTestCase(unittest.TestCase):
    def test_repository内参照とanchorが全て解決できる(self) -> None:
        report = check_markdown_links(PROJECT_ROOT)
        self.assertEqual(report["status"], "pass", report["failures"])
        self.assertGreater(report["markdown_files_checked"], 10)
        self.assertGreater(report["local_references_checked"], 20)
        self.assertGreater(report["external_references_observed"], 10)
        self.assertIn("https://github.com/saitoomituru/SphereOS-Atlantis", report["external_urls"])
        self.assertFalse(report["network_access_performed"])
        self.assertFalse(report["mutations_performed"])

    def test_missing_pathとanchorを別々に報告する(self) -> None:
        with tempfile.TemporaryDirectory(prefix="atlantis-links-") as temporary:
            root = Path(temporary)
            (root / "AGENTS.md").write_text("# fixture\n", encoding="utf-8")
            template = root / "note/templates/brainstorm.ja.md"
            template.parent.mkdir(parents=True)
            template.write_text("# fixture template\n", encoding="utf-8")
            (root / "target.md").write_text("# 実在する見出し\n", encoding="utf-8")
            (root / "README.md").write_text(
                "[ok](target.md#実在する見出し)\n"
                "[missing](missing.md)\n"
                "[anchor](target.md#存在しない見出し)\n"
                "[external](https://example.com)\n",
                encoding="utf-8",
            )

            report = check_markdown_links(root)

        self.assertEqual(report["status"], "fail")
        self.assertEqual(
            {failure["reason"] for failure in report["failures"]},
            {"missing-target", "missing-anchor"},
        )
        self.assertEqual(report["external_references_observed"], 1)


if __name__ == "__main__":
    unittest.main()
