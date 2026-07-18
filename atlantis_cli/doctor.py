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
from .note import find_repo_root


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

    template = root / "note/templates/brainstorm.ja.md"
    checks.append(
        check(
            "note-template",
            "pass" if template.is_file() else "fail",
            str(template),
        )
    )

    try:
        bundle = load_json(root / "magi/0.2.0/bundle.json")
        source_policy = load_json(root / "magi/0.2.0/source-map.json")
        audit_ids = [item["id"] for item in bundle["audit_slots"]]
        support_slots = bundle["support_slots"]
        invariants = bundle["invariants"]
        if bundle.get("version") != "0.2.0":
            raise ValueError("MAGI bundle versionは0.2.0である必要があります。")
        if audit_ids != ["maxwell", "uriel", "raphael"]:
            raise ValueError("MAGI監査slotの順序または構成が契約と一致しません。")
        if len(support_slots) != 1 or support_slots[0].get("id") != "chikuwa-cannon":
            raise ValueError("ちくわ砲support slotを一意に確認できません。")
        if support_slots[0].get("is_audit_dimension") is not False:
            raise ValueError("ちくわ砲を監査次元または第四票にしてはいけません。")
        if any(value is not False for value in invariants.values()):
            raise ValueError("MAGIの非人格・非神託・非多数決不変条件が崩れています。")
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
    except (KeyError, TypeError, ValueError) as error:
        checks.append(check("magi-skill-bundle", "fail", str(error)))
    else:
        checks.append(check("magi-skill-bundle", "pass", "3 audit slots + 1 support slot"))

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
