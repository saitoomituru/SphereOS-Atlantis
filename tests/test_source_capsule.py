from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.build_m6xx_source_capsule import build_capsule, parse_repositories, safe_relative


def make_repo(root: Path) -> str:
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "試験者"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
    (root / "AGENTS.md").write_text("# fixture\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "AGENTS.md"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "fixture"], check=True)
    return subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


class SourceCapsuleTestCase(unittest.TestCase):
    def test_明示fileだけをread_only展開する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repository = base / "repo"
            output = base / "capsule"
            revision = make_repo(repository)
            contract = {
                "id": "source-capsule://fixture",
                "sources": [
                    {"id": "fixture", "revision": revision, "files": ["AGENTS.md"]}
                ],
            }
            receipt = build_capsule(contract, {"fixture": repository}, output)
            self.assertEqual(receipt["file_count"], 1)
            self.assertFalse(receipt["whole_repository_archive"])
            self.assertFalse(receipt["agent_output_included"])
            self.assertEqual((output / "fixture/AGENTS.md").read_text(), "# fixture\n")
            self.assertEqual((output / "fixture/AGENTS.md").stat().st_mode & 0o222, 0)

    def test_repositoryとsource_pathの越境を拒否する(self) -> None:
        with self.assertRaises(ValueError):
            parse_repositories(["fixture=relative/path"])
        with self.assertRaises(ValueError):
            safe_relative("../secret")


if __name__ == "__main__":
    unittest.main()
