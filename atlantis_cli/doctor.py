"""Atlantis開発環境を変更せずに診断する。"""

from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from typing import Any

from .config import load_adapter, load_agent_registry, load_json, policy_paths
from .corn import validate_corn
from .experience import validate_experience
from .help_mode import load_capability_registry
from .links import check_markdown_links
from .note import find_repo_root, load_note_registry
from .release import validate_release
from .status_map import validate_status_maps
from .tutorial import load_persona_registry
from .versioning import validate_version_contract


def check(name: str, status: str, detail: str) -> dict[str, str]:
    return {"name": name, "status": status, "detail": detail}


def find_vscode() -> tuple[str | None, str]:
    path_command = shutil.which("code")
    if path_command:
        return path_command, "cli-on-path"
    candidates: list[Path] = []
    if sys.platform == "darwin":
        candidates.extend(
            [
                Path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"),
                Path("/Applications/Visual Studio Code - Insiders.app/Contents/Resources/app/bin/code-insiders"),
            ]
        )
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            candidates.append(Path(local_app_data) / "Programs/Microsoft VS Code/bin/code.cmd")
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate), "application-found-cli-not-on-path"
    return None, "not-found"


def git_description(root: Path) -> tuple[bool, str]:
    git = shutil.which("git")
    if not git:
        return False, "git commandがPATHにありません。"
    completed = subprocess.run(
        [git, "-C", str(root), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    if completed.returncode != 0 or completed.stdout.strip() != "true":
        return False, "repositoryをGit worktreeとして確認できません。"
    return True, git


def run_doctor(repo_root: Path | None = None, require_container: bool = False) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    checks: list[dict[str, str]] = []

    git_ok, git_detail = git_description(root)
    checks.append(check("git-worktree", "pass" if git_ok else "fail", git_detail))

    python_ok = sys.version_info >= (3, 11)
    checks.append(
        check(
            "python",
            "pass" if python_ok else "fail",
            platform.python_version(),
        )
    )

    vscode_path, vscode_state = find_vscode()
    vscode_status = "pass" if vscode_state == "cli-on-path" else "warn"
    checks.append(check("vscode", vscode_status, f"{vscode_state}: {vscode_path or 'unknown'}"))

    container_candidates = [value for value in ("docker", "podman") if shutil.which(value)]
    if container_candidates:
        checks.append(check("container-runtime", "pass", ", ".join(container_candidates)))
    else:
        status = "fail" if require_container else "warn"
        checks.append(check("container-runtime", status, "docker／podmanを検出できません。"))

    try:
        registry = load_agent_registry(root)
        paths = policy_paths(root)
        for path in paths.values():
            load_json(path)
        for provider in registry["providers"]:
            load_adapter(root, provider["id"])
    except ValueError as error:
        checks.append(check("agent-policy", "fail", str(error)))
    else:
        checks.append(check("agent-policy", "pass", f"{len(registry['providers'])} adapters"))

    source_map = root / "skills/learn-sphereos-atlantis/references/source-map.json"
    try:
        source_map_value = load_json(source_map)
        shelf_count = len(source_map_value["shelves"])
    except (KeyError, TypeError, ValueError) as error:
        checks.append(check("tutorial-source-map", "fail", str(error)))
    else:
        checks.append(check("tutorial-source-map", "pass", f"{shelf_count} shelves"))

    corn_result = validate_corn(root)
    checks.append(
        check(
            "corn-stack",
            "pass" if corn_result["overall"] == "pass" else "fail",
            (
                f"{len(corn_result['work_items'])} work items; "
                f"{corn_result['event_count']} events"
                if corn_result["overall"] == "pass"
                else "; ".join(corn_result["errors"])
            ),
        )
    )

    experience_result = validate_experience(root)
    checks.append(
        check(
            "experience-receipts",
            "pass" if experience_result["overall"] == "pass" else "fail",
            (
                f"{experience_result['receipt_count']} receipts"
                if experience_result["overall"] == "pass"
                else "; ".join(experience_result["errors"])
            ),
        )
    )

    status_result = validate_status_maps(root)
    checks.append(
        check(
            "forge-quest-status",
            "pass" if status_result["overall"] == "pass" else "fail",
            (
                f"{sum(item['items'] for item in status_result['maps'])} items"
                if status_result["overall"] == "pass"
                else "; ".join(status_result["errors"])
            ),
        )
    )

    release_result = validate_release(root)
    checks.append(
        check(
            "release-candidate",
            "pass" if release_result["overall"] == "pass" else "fail",
            (
                f"{release_result['candidate']}; tag {release_result['tag_state']}"
                if release_result["overall"] == "pass"
                else "; ".join(release_result["errors"])
            ),
        )
    )

    template = root / "note/templates/brainstorm.ja.md"
    checks.append(
        check(
            "note-template",
            "pass" if template.is_file() else "fail",
            str(template),
        )
    )

    try:
        note_registry = load_note_registry(root)
    except (KeyError, TypeError, ValueError) as error:
        checks.append(check("note-registry", "fail", str(error)))
    else:
        checks.append(
            check(
                "note-registry",
                "pass",
                f"{len(note_registry['shelves'])} shelves; {len(note_registry['kinds'])} kinds",
            )
        )

    try:
        persona_registry = load_persona_registry(root)
    except (KeyError, TypeError, ValueError) as error:
        checks.append(check("persona-registry", "fail", str(error)))
    else:
        checks.append(
            check(
                "persona-registry",
                "pass",
                f"{len(persona_registry['profiles'])} profiles",
            )
        )

    try:
        capability_registry = load_capability_registry(root)
    except (KeyError, TypeError, ValueError) as error:
        checks.append(check("help-capabilities", "fail", str(error)))
    else:
        checks.append(
            check(
                "help-capabilities",
                "pass",
                f"{len(capability_registry['capabilities'])} capabilities; default unknown/look-around",
            )
        )

    version_result = validate_version_contract(root)
    checks.append(
        check(
            "version-coordinate",
            "pass" if version_result["overall"] == "pass" else "fail",
            (
                f"{version_result['canonical_display']}; {version_result['fixture_count']} fixtures"
                if version_result["overall"] == "pass"
                else "; ".join(version_result["errors"])
            ),
        )
    )

    try:
        bundle = load_json(root / "magi/0.2.1/bundle.json")
        source_policy = load_json(root / "magi/0.2.1/source-map.json")
        temporal_policy = load_json(root / "magi/0.2.1/oae-temporal-policy.json")
        audit_ids = [item["id"] for item in bundle["audit_slots"]]
        support_slots = bundle["support_slots"]
        invariants = bundle["invariants"]
        if bundle.get("version") != "0.2.1":
            raise ValueError("MAGI bundle versionは0.2.1である必要があります。")
        if bundle.get("canonical_coordinate") != "0.200.1":
            raise ValueError("MAGI legacy 0.2.1を三層座標0.200.1へ解決できません。")
        if audit_ids != ["maxwell", "uriel", "raphael"]:
            raise ValueError("MAGI監査slotの順序または構成が契約と一致しません。")
        if len(support_slots) != 1 or support_slots[0].get("id") != "chikuwa-cannon":
            raise ValueError("ちくわ砲support slotを一意に確認できません。")
        if support_slots[0].get("is_audit_dimension") is not False:
            raise ValueError("ちくわ砲を監査次元または第四票にしてはいけません。")
        if any(value is not False for value in invariants.values()):
            raise ValueError("MAGIの非人格・非神託・非多数決不変条件が崩れています。")
        if temporal_policy.get("version") != "0.2.1":
            raise ValueError("OAE時間整合性policy versionが0.2.1ではありません。")
        kernel_change = temporal_policy.get("semantic_kernel_change", {})
        if (
            temporal_policy.get("canonical_coordinate") != "0.200.1"
            or kernel_change.get("source_coordinate") != "0.200.0"
            or kernel_change.get("target_coordinate") != "0.200.1"
            or kernel_change.get("same_worldline_oae_relocation_allowed") is not False
            or kernel_change.get("source_event_preserved") is not True
        ):
            raise ValueError("MAGI意味Kernel 0.200.1の同一世界線OAE再配置拒否が崩れています。")
        last_order = temporal_policy.get("last_order", {})
        if (
            last_order.get("code") != "OAE-HISTORY-UNKNOWN"
            or last_order.get("action") != "stop-retroactive-backfill"
        ):
            raise ValueError("OAE historical unknownのLast Order契約が崩れています。")
        dimensions = temporal_policy.get("provisional_branch_dimensions", [])
        if len(dimensions) != 7 or len(set(dimensions)) != 7:
            raise ValueError("Akasha Driver仮設profileは一意な七軸候補を持つ必要があります。")
        if temporal_policy.get("branch_dimension_profile_status") != "PROVISIONAL_VALIDATOR_PROFILE":
            raise ValueError("7D軸名を正規Registryとして過剰確定してはいけません。")
        if temporal_policy.get("final_branch_dimension_registry") != "unknown-user-gate-required":
            raise ValueError("最終7D RegistryはUser gate前に確定してはいけません。")
        branch_requirements = temporal_policy.get("branch_requirements", {})
        if branch_requirements.get("source_mutation") is not False:
            raise ValueError("7D FoldはSource World／Instance Ghostを変更してはいけません。")
        if temporal_policy.get("ux_boundary", {}).get("physical_time_travel") is not False:
            raise ValueError("backup UXを物理空間の時間移動として扱ってはいけません。")
        policy = source_policy["policy"]
        if policy.get("network_access_performed_by_resolver") is not False:
            raise ValueError("source resolverはnetwork accessを実行してはいけません。")
        if policy.get("secret_scan") is not False:
            raise ValueError("source resolverはsecret scanを実行してはいけません。")
        skill_paths = [item["skill"] for item in bundle["audit_slots"]]
        skill_paths.extend(item["skill"] for item in support_slots)
        skill_paths.append(bundle["composite_skill"])
        missing_skills = [path for path in skill_paths if not (root / path / "SKILL.md").is_file()]
        if missing_skills:
            raise ValueError(f"MAGI Skillがありません: {', '.join(missing_skills)}")
        validator = root / bundle["temporal_validator"]
        if not validator.is_file():
            raise ValueError(f"OAE時間整合性validatorがありません: {validator}")
    except (KeyError, TypeError, ValueError) as error:
        checks.append(check("magi-skill-bundle", "fail", str(error)))
    else:
        checks.append(check("magi-skill-bundle", "pass", "0.200.1 (legacy 0.2.1): 3 audit slots + OAE temporal gate"))

    development_files = [
        ".vscode/extensions.json",
        ".vscode/settings.json",
        ".vscode/tasks.json",
        ".vscode/launch.json",
        ".devcontainer/devcontainer.json",
        ".github/workflows/verify.yml",
        "scripts/bootstrap_venv.py",
        "scripts/clean_room_test.py",
    ]
    missing_development_files = [path for path in development_files if not (root / path).is_file()]
    try:
        for path in development_files[:5]:
            load_json(root / path)
    except ValueError as error:
        checks.append(check("development-profile", "fail", str(error)))
    else:
        if missing_development_files:
            checks.append(
                check(
                    "development-profile",
                    "fail",
                    f"開発環境fileがありません: {', '.join(missing_development_files)}",
                )
            )
        else:
            checks.append(check("development-profile", "pass", f"{len(development_files)} files"))

    link_report = check_markdown_links(root)
    if link_report["status"] == "pass":
        checks.append(
            check(
                "markdown-links",
                "pass",
                f"{link_report['local_references_checked']} local references",
            )
        )
    else:
        checks.append(
            check(
                "markdown-links",
                "fail",
                f"{len(link_report['failures'])} failures",
            )
        )

    statuses = {item["status"] for item in checks}
    overall = "fail" if "fail" in statuses else "warn" if "warn" in statuses else "pass"
    observed = datetime.now().astimezone()
    return {
        "schema_version": "1.0.0",
        "overall": overall,
        "repository_root": str(root),
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "observation_clock": {
            "observed_at_system": observed.isoformat(timespec="seconds"),
            "source": "host_system_clock",
            "calibration": "unverified",
        },
        "checks": checks,
        "mutations_performed": False,
        "network_access_performed": False,
    }


def format_doctor(result: dict[str, Any]) -> str:
    lines = [f"Atlantis doctor: {result['overall'].upper()}"]
    for item in result["checks"]:
        lines.append(f"[{item['status'].upper()}] {item['name']}: {item['detail']}")
    lines.append("clock calibration: unverified")
    lines.append("mutations: false; network: false")
    return "\n".join(lines)


def doctor_json(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)
