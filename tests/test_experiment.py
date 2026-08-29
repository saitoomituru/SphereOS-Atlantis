from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from atlantis_cli.config import load_adapter
from atlantis_cli.experiment import (
    TargetBinding,
    build_plan,
    build_snapshot,
    attach_observation_metadata,
    load_experiment_contract,
    write_local_receipt,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def make_git_repo(root: Path, remote: str, dirty: bool = False) -> None:
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "試験者"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
    (root / "README.md").write_text("# fixture\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "試験初期化"], check=True)
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", remote], check=True)
    if dirty:
        (root / "秘密にしたい差分名.txt").write_text("not secret content\n", encoding="utf-8")


class AgentExperimentTestCase(unittest.TestCase):
    def test_Grokは実行せずadapterとして解決する(self) -> None:
        adapter = load_adapter(PROJECT_ROOT, "grok-cli")
        self.assertEqual(adapter["executable_candidates"], ["grok"])
        self.assertEqual(adapter["invocation"], "never-automatic")
        self.assertEqual(adapter["capability_state"], "unknown-until-explicit-probe")

    def test_snapshotはdirty_pathを公開しない(self) -> None:
        contract = load_experiment_contract(PROJECT_ROOT)
        with tempfile.TemporaryDirectory() as temporary:
            target_root = Path(temporary) / "fold-nic"
            make_git_repo(
                target_root,
                "https://github.com/saitoomituru/fold-nic.git",
                dirty=True,
            )
            result = build_snapshot(
                contract,
                {"fold-nic": TargetBinding("fold-nic", target_root)},
            )
        encoded = json.dumps(result, ensure_ascii=False)
        observed = result["targets"][0]
        self.assertEqual(observed["state"], "dirty-worktree")
        self.assertEqual(observed["dirty_entry_count"], 1)
        self.assertFalse(observed["dirty_paths_disclosed"])
        self.assertNotIn("秘密にしたい差分名", encoded)
        self.assertFalse(result["network_access_performed"])
        self.assertFalse(result["mutations_performed"])

    def test_planはclean_room_laneを実行せず分離する(self) -> None:
        contract = load_experiment_contract(PROJECT_ROOT)
        with tempfile.TemporaryDirectory() as temporary:
            target_root = Path(temporary) / "edohage"
            make_git_repo(
                target_root,
                "https://github.com/saitoomituru/EDOHAGE-TUBO.git",
            )
            result = build_plan(
                PROJECT_ROOT,
                contract,
                {"edohage-tubo": TargetBinding("edohage-tubo", target_root)},
            )
        clean_room = [packet for packet in result["packets"] if packet["clean_room_group"]]
        self.assertEqual({packet["provider"] for packet in clean_room}, {"gemini-cli", "grok-cli"})
        self.assertTrue(all(packet["other_agent_output_as_input"] is False for packet in clean_room))
        self.assertTrue(all(packet["execution_gate"] == "ready-to-render-only" for packet in clean_room))
        self.assertFalse(result["model_invoked"])
        self.assertFalse(result["mutations_performed"])

    def test_clean_room_taskは同一baseと相互非参照を拘束する(self) -> None:
        contract = load_experiment_contract(PROJECT_ROOT)
        task_path = PROJECT_ROOT / contract["task_packet_refs"][0]
        task = task_path.read_text(encoding="utf-8")
        self.assertIn("9d1b88517cf03c2dfe45603e641c43ed60b7a81d", task)
        self.assertIn("他方agentのbranch、worktree、transcript、未公開成果を読むこと", task)
        self.assertIn("INSECURE_PUBLIC_TEST_KEY", task)
        self.assertIn("production profile", task)
        self.assertIn("git add .", task)

    def test_runは明示的な未実装境界で終了する(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "atlantis_cli",
                "experiment",
                "run",
                "--json",
            ],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 3, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["state"], "NOT IMPLEMENTED")
        self.assertTrue(result["user_gate_required"])
        self.assertFalse(result["model_invoked"])
        self.assertFalse(result["mutations_performed"])

    def test_local_receiptはraw会話なしでignore領域へ保存する(self) -> None:
        result = attach_observation_metadata(
            {
                "schema_version": "1.0.0",
                "raw_transcript_included": False,
                "mutations_performed": False,
            },
            "snapshot",
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination, recorded = write_local_receipt(root, "snapshot", result)
            self.assertTrue(destination.is_file())
            self.assertTrue(destination.is_relative_to(root / ".atlantis"))
            on_disk = json.loads(destination.read_text(encoding="utf-8"))
        self.assertEqual(on_disk, recorded)
        self.assertFalse(recorded["local_receipt"]["public_source"])
        self.assertFalse(recorded["local_receipt"]["raw_transcript_included"])
        self.assertFalse(recorded["local_receipt"]["target_repository_mutated"])


if __name__ == "__main__":
    unittest.main()
