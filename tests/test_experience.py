from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from atlantis_cli.experience import create_experience_receipt, validate_experience


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ExperienceTestCase(unittest.TestCase):
    def make_repo(self, base: Path) -> Path:
        for relative in (
            "AGENTS.md",
            "note/templates/brainstorm.ja.md",
            "experience/registry.json",
        ):
            destination = base / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                (PROJECT_ROOT / relative).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        return base

    def test_生の表現と自己申告clusterを保存する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repo(Path(temporary))
            result = create_experience_receipt(
                summary="祈りUIのずれ",
                raw_signals=["波動が合わない"],
                self_clusters=["律令神道の実践者"],
                world="shrine-world",
                request_cluster_review=True,
                timestamp="2026-07-19T10:10:00+09:00",
                repo_root=root,
            )

            value = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
            self.assertEqual(value["raw_experience_signals"], ["波動が合わない"])
            self.assertEqual(value["cluster_review"], "requested")
            self.assertFalse(value["identity_inferred"])
            self.assertFalse(value["specification_changed"])
            self.assertEqual(validate_experience(root)["overall"], "pass")

    def test_by_designはscope等がなければfailする(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_repo(Path(temporary))
            (root / "experience/receipts").mkdir(parents=True)
            value = {
                "schema_version": "1.0.0",
                "raw_experience_signals": ["面白くない"],
                "identity_inferred": False,
                "selected_disposition": "by-design-with-scope",
                "by_design_claim": None,
            }
            (root / "experience/receipts/test.json").write_text(
                json.dumps(value, ensure_ascii=False), encoding="utf-8"
            )

            result = validate_experience(root)

            self.assertEqual(result["overall"], "fail")
            self.assertIn("by-design", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
