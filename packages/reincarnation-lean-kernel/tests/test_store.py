from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from sphere_reincarnation_harness import store
from sphere_reincarnation_harness.errors import (
    ExistingFileError,
    HarnessNotInitializedError,
    SymlinkEscapeError,
    UnsafeIdentifierError,
)


class ValidateIdentifierTestCase(unittest.TestCase):
    def test_空文字を拒否する(self) -> None:
        with self.assertRaises(UnsafeIdentifierError):
            store.validate_identifier("", "task_id")

    def test_親ディレクトリ参照を拒否する(self) -> None:
        with self.assertRaises(UnsafeIdentifierError):
            store.validate_identifier("../escape", "task_id")

    def test_path_separatorを拒否する(self) -> None:
        with self.assertRaises(UnsafeIdentifierError):
            store.validate_identifier("nested/id", "task_id")

    def test_absolute_pathを拒否する(self) -> None:
        with self.assertRaises(UnsafeIdentifierError):
            store.validate_identifier("/etc/passwd", "task_id")

    def test_正当なIDは通過する(self) -> None:
        self.assertEqual(store.validate_identifier("synthetic-task-0001", "task_id"), "synthetic-task-0001")


class ResolveWithinRootTestCase(unittest.TestCase):
    def test_symlinkでroot外へ出るpathを拒否する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "root"
            outside = base / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "escape-link").symlink_to(outside, target_is_directory=True)

            with self.assertRaises(SymlinkEscapeError):
                store.resolve_within_root(root, Path("escape-link/artifact.json"))

    def test_root内のpathは許可される(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            resolved = store.resolve_within_root(root, Path("nested/artifact.json"))
            self.assertTrue(str(resolved).startswith(str(Path(temporary).resolve())))


class AtomicWriteJsonTestCase(unittest.TestCase):
    def test_atomic_writeはtempfileを残さずcreateする(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "artifact.json"

            store.atomic_write_json(target, root, {"value": 1})

            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), {"value": 1})
            self.assertEqual(list(root.iterdir()), [target])

    def test_既定でsilent_overwriteしない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "artifact.json"
            store.atomic_write_json(target, root, {"value": 1})

            with self.assertRaises(ExistingFileError):
                store.atomic_write_json(target, root, {"value": 2})

            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), {"value": 1})

    def test_overwrite指定時はatomicに置換する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "artifact.json"
            store.atomic_write_json(target, root, {"value": 1})

            store.atomic_write_json(target, root, {"value": 2}, overwrite=True)

            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), {"value": 2})


class AppendReceiptTestCase(unittest.TestCase):
    def test_append_onlyで既存行を書き換えない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "receipts" / "decisions.jsonl"

            store.append_receipt(target, root, {"decision": "accepted", "seq": 1})
            store.append_receipt(target, root, {"decision": "rejected", "seq": 2})

            lines = target.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["seq"], 1)
            self.assertEqual(json.loads(lines[1])["seq"], 2)


class InitAndInspectTestCase(unittest.TestCase):
    def test_initは生成pathを作りharness_jsonをcreateする(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-test-root"
            root.mkdir()

            result = store.init_harness(root)

            self.assertTrue(result["mutations_performed"])
            self.assertFalse(result["already_initialized"])
            harness_json = Path(result["harness_json"])
            self.assertTrue(harness_json.is_file())
            payload = json.loads(harness_json.read_text(encoding="utf-8"))
            self.assertTrue(payload["harness_only"])
            self.assertFalse(payload["production_kernel"])

    def test_2回目のinitはharness_jsonをsilent_overwriteしない(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-test-root"
            root.mkdir()
            store.init_harness(root)

            second = store.init_harness(root)

            self.assertTrue(second["already_initialized"])
            self.assertFalse(second["mutations_performed"])

    def test_inspectは未初期化rootをfilesystem変更なしで報告する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-test-root"
            root.mkdir()

            result = store.inspect_harness(root)

            self.assertFalse(result["initialized"])
            self.assertFalse(result["mutations_performed"])
            self.assertFalse((root / ".spheredos-harness").exists())

    def test_require_initializedは未初期化で例外を返す(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "explicit-test-root"
            root.mkdir()

            with self.assertRaises(HarnessNotInitializedError):
                store.require_initialized(root)


if __name__ == "__main__":
    unittest.main()
