"""alpha release候補のmachine-readable境界を検証する。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import __version__
from .config import load_json
from .note import find_repo_root


RELEASE_PATH = Path("release/0.25.1-alpha.1.json")


def validate_release(repo_root: Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    value = load_json(root / RELEASE_PATH)
    errors: list[str] = []
    candidate = value.get("candidate")
    expected_cli = candidate.replace("-alpha.", "a") if isinstance(candidate, str) else None
    if value.get("schema_version") != "1.0.0":
        errors.append("release schema_versionが1.0.0ではありません。")
    if value.get("release_state") != "alpha-candidate":
        errors.append("review前にalpha-candidate以外を名乗れません。")
    if value.get("tag") != f"v{candidate}" or value.get("tag_state") != "not-created":
        errors.append("候補tagまたはtag未作成境界が不正です。")
    if expected_cli != __version__:
        errors.append(f"CLI versionが候補と一致しません: {__version__} != {expected_cli}")
    profile = load_json(root / "sphere-dos/profile.json")
    if profile.get("design_line") != value.get("design_line"):
        errors.append("Sphere-DOS design lineがrelease候補と一致しません。")
    for key in ("status_maps", "release_notes"):
        paths = value.get(key)
        if not isinstance(paths, list) or not paths:
            errors.append(f"release manifestに{key}がありません。")
            continue
        for relative in paths:
            if not isinstance(relative, str) or not (root / relative).is_file():
                errors.append(f"release artifactがありません: {relative}")
    return {
        "schema_version": "1.0.0",
        "overall": "fail" if errors else "pass",
        "candidate": candidate,
        "tag_state": value.get("tag_state"),
        "errors": errors,
        "network_access_performed": False,
        "mutations_performed": False,
    }


def format_release(result: dict[str, Any]) -> str:
    lines = [
        f"overall: {result['overall']}",
        f"candidate: {result['candidate']}",
        f"tag: {result['tag_state']}",
    ]
    lines.extend(f"error: {error}" for error in result["errors"])
    return "\n".join(lines)
