"""Markdownのrepository内参照をnetworkなしで検査する。"""

from __future__ import annotations

from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit
from typing import Any

from .note import find_repo_root


LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)]+)\)")
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(?P<title>.+?)\s*#*\s*$")
SCHEME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
EXTERNAL_URL_PATTERN = re.compile(r"https?://[^\s<>)\]\"']+")
EXCLUDED_DIRECTORIES = {
    ".agents",
    ".codex",
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
}


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(root).parts)
    )


def remove_code_regions(text: str) -> str:
    """行番号を保ったままfenceとinline code内の擬似linkを除外する。"""

    output: list[str] = []
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        marker = "```" if stripped.startswith("```") else "~~~" if stripped.startswith("~~~") else None
        if marker:
            fence = None if fence == marker else marker if fence is None else fence
            output.append("\n" if line.endswith("\n") else "")
            continue
        if fence:
            output.append("\n" if line.endswith("\n") else "")
            continue
        output.append(re.sub(r"`[^`\n]*`", "", line))
    return "".join(output)


def normalized_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    return target


def github_slug(title: str) -> str:
    title = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", title)
    title = re.sub(r"<[^>]+>", "", title)
    title = title.replace("`", "")
    title = unicodedata.normalize("NFKC", title).strip().lower()
    kept: list[str] = []
    for character in title:
        category = unicodedata.category(character)
        if character in {"-", "_"} or character.isspace() or category[0] in {"L", "N", "M"}:
            kept.append(character)
    return re.sub(r"\s+", "-", "".join(kept))


def heading_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    text = remove_code_regions(path.read_text(encoding="utf-8"))
    for line in text.splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        base = github_slug(match.group("title"))
        if not base:
            continue
        duplicate_index = counts.get(base, 0)
        counts[base] = duplicate_index + 1
        anchors.add(base if duplicate_index == 0 else f"{base}-{duplicate_index}")
    return anchors


def is_external(target: str) -> bool:
    return bool(SCHEME_PATTERN.match(target)) or target.startswith("//")


def check_markdown_links(repo_root: Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    failures: list[dict[str, object]] = []
    files = markdown_files(root)
    local_count = 0
    external_urls: set[str] = set()
    anchors_by_path: dict[Path, set[str]] = {}

    for source in files:
        cleaned = remove_code_regions(source.read_text(encoding="utf-8"))
        external_urls.update(EXTERNAL_URL_PATTERN.findall(cleaned))
        for line_number, line in enumerate(cleaned.splitlines(), start=1):
            for match in LINK_PATTERN.finditer(line):
                target = normalized_target(match.group("target"))
                if not target:
                    failures.append(
                        {
                            "source": str(source.relative_to(root)),
                            "line": line_number,
                            "target": target,
                            "reason": "empty-target",
                        }
                    )
                    continue
                if is_external(target):
                    continue

                local_count += 1
                parsed = urlsplit(target)
                path_text = unquote(parsed.path)
                fragment = unquote(parsed.fragment)
                destination = source if not path_text else source.parent / path_text
                destination = destination.resolve()
                try:
                    destination.relative_to(root.resolve())
                except ValueError:
                    failures.append(
                        {
                            "source": str(source.relative_to(root)),
                            "line": line_number,
                            "target": target,
                            "reason": "repository-boundary-escape",
                        }
                    )
                    continue

                if not destination.exists():
                    failures.append(
                        {
                            "source": str(source.relative_to(root)),
                            "line": line_number,
                            "target": target,
                            "reason": "missing-target",
                        }
                    )
                    continue

                if fragment and destination.is_file() and destination.suffix.lower() == ".md":
                    anchors = anchors_by_path.setdefault(destination, heading_anchors(destination))
                    if fragment not in anchors:
                        failures.append(
                            {
                                "source": str(source.relative_to(root)),
                                "line": line_number,
                                "target": target,
                                "reason": "missing-anchor",
                            }
                        )

    return {
        "schema_version": "1.0.0",
        "status": "fail" if failures else "pass",
        "repository_root": str(root),
        "markdown_files_checked": len(files),
        "local_references_checked": local_count,
        "external_references_observed": len(external_urls),
        "external_urls": sorted(external_urls),
        "failures": failures,
        "network_access_performed": False,
        "mutations_performed": False,
    }


def format_link_report(report: dict[str, Any]) -> str:
    lines = [f"Atlantis links: {str(report['status']).upper()}"]
    lines.append(f"markdown files: {report['markdown_files_checked']}")
    lines.append(f"local references: {report['local_references_checked']}")
    lines.append(f"external references: {report['external_references_observed']} (not fetched)")
    for failure in report["failures"]:
        lines.append(
            f"[FAIL] {failure['source']}:{failure['line']} {failure['target']} ({failure['reason']})"
        )
    lines.append("network/mutations: false")
    return "\n".join(lines)
