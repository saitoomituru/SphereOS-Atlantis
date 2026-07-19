from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from atlantis_cli.corn import (
    build_context_receipt,
    forge_projection_plan,
    tick_corn,
    validate_corn,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def make_atlantis_fixture(target: Path) -> None:
    for relative in (
        Path("AGENTS.md"),
        Path("README.md"),
        Path("workspace/components.json"),
        Path("docs/operations/corn-stack.ja.md"),
        Path("note/templates/brainstorm.ja.md"),
    ):
        copy_file(PROJECT_ROOT / relative, target / relative)
    shutil.copytree(PROJECT_ROOT / "corn", target / "corn")


def make_manifest_fixture(target: Path, atlantis_root: Path) -> None:
    registry = json.loads((atlantis_root / "corn/registry.json").read_text(encoding="utf-8"))
    for source in registry["sources"]:
        if source["repository"] != "ZeroRoomLab-manifest":
            continue
        path = target / source["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# fixture {source['id']}\n", encoding="utf-8")
    marker = target / registry["repositories"]["ZeroRoomLab-manifest"]["marker"]
    marker.parent.mkdir(parents=True, exist_ok=True)
    if not marker.exists():
        marker.write_text("{}\n", encoding="utf-8")


class CornTestCase(unittest.TestCase):
    def test_repository内CORN正本はoffline検証できる(self) -> None:
        result = validate_corn(PROJECT_ROOT)

        self.assertEqual(result["overall"], "pass", result["errors"])
        self.assertEqual(result["event_count"], 1)
        self.assertIn("github", result["projection_adapters"])
        self.assertFalse(result["network_access_performed"])

    def test_contextはManifestとAGENTSをhash化しcapsule_staleを検出する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            atlantis = base / "SphereOS-Atlantis"
            manifest = base / "ZeroRoomLab-manifest"
            make_atlantis_fixture(atlantis)
            make_manifest_fixture(manifest, atlantis)

            first = build_context_receipt(
                "CORN-0001",
                atlantis,
                repository_roots={"ZeroRoomLab-manifest": manifest},
                write_capsule=True,
            )

            self.assertEqual(first["overall"], "complete")
            self.assertEqual(first["capsule"]["status"], "current")
            self.assertIn("manifest-agents", {item["id"] for item in first["sources"]})
            self.assertFalse(first["network_access_performed"])

            (manifest / "AGENTS.md").write_text("# changed\n", encoding="utf-8")
            second = build_context_receipt(
                "CORN-0001",
                atlantis,
                repository_roots={"ZeroRoomLab-manifest": manifest},
            )

            self.assertEqual(second["overall"], "complete")
            self.assertEqual(second["capsule"]["status"], "stale")
            self.assertNotEqual(first["context_fingerprint"], second["context_fingerprint"])

    def test_Manifest欠損はCONTEXT_INCOMPLETEで停止する(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            atlantis = Path(temporary) / "SphereOS-Atlantis"
            make_atlantis_fixture(atlantis)

            result = build_context_receipt("CORN-0001", atlantis, write_capsule=True)

            self.assertEqual(result["overall"], "incomplete")
            self.assertIn("manifest-agents", result["missing_required_sources"])
            self.assertEqual(result["last_order"]["code"], "CONTEXT-INCOMPLETE")
            self.assertEqual(result["capsule"]["status"], "not-written-context-incomplete")
            self.assertFalse(result["mutations_performed"])

    def test_tickはrunnerを起動せずactivation_receiptだけを残す(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            atlantis = base / "SphereOS-Atlantis"
            manifest = base / "ZeroRoomLab-manifest"
            make_atlantis_fixture(atlantis)
            make_manifest_fixture(manifest, atlantis)

            result = tick_corn(
                "CORN-0001",
                "unit-test",
                atlantis,
                repository_roots={"ZeroRoomLab-manifest": manifest},
            )

            self.assertEqual(result["status"], "plan-ready")
            self.assertEqual(result["action"], "await-authorized-runner")
            self.assertFalse(result["authorized_mutation"])
            self.assertFalse(result["project_mutations_performed"])
            self.assertTrue(Path(result["receipt_path"]).is_file())
            self.assertFalse(result["network_access_performed"])

    def test_既存GitHub_Issueはofflineでobserve_existingになる(self) -> None:
        result = forge_projection_plan("CORN-0001", "github", PROJECT_ROOT)

        self.assertEqual(result["mode"], "plan-only")
        self.assertEqual(result["action"], "observe-existing")
        self.assertEqual(result["projection"]["remote_number"], 2)
        self.assertFalse(result["mutations_performed"])
        self.assertFalse(result["network_access_performed"])


if __name__ == "__main__":
    unittest.main()
