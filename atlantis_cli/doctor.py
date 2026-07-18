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
