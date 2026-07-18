"""Atlantis noteを、既存ファイルを上書きせずに生成する。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re


SHELVES = (
    "spiritual",
    "gaming-trpg",
    "engineering",
    "infoton-engineering",
    "sphere-architecture",
    "cross-shelf",
)

KINDS = (
    "brainstorm",
    "observation",
    "research",
    "review",
    "transfer-candidate",
)

TEMPLATE_PATH = Path("note/templates/brainstorm.ja.md")
INVALID_FILENAME = re.compile(r"[\\/:*?\"<>|\x00-\x1f\x7f]+")
WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class NoteResult:
    path: Path
    content: str
    dry_run: bool


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).expanduser().resolve()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / TEMPLATE_PATH).is_file():
            return candidate
    raise ValueError("SphereOS Atlantis repository rootを解決できません。--repo-rootを指定してください。")


def sanitize_title(title: str) -> str:
    value = INVALID_FILENAME.sub("_", title.strip())
    value = WHITESPACE.sub("_", value)
    value = re.sub(r"_+", "_", value).strip("._")
    if not value:
        raise ValueError("titleから安全なファイル名を生成できません。")
    return value[:100].rstrip("._")


def parse_timestamp(value: str | None) -> datetime:
    if value is None:
        return datetime.now().astimezone()
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError("--timestampはISO 8601形式で指定してください。") from error
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed


def timezone_label(value: datetime) -> str:
    offset = value.strftime("%z")
    formatted_offset = f"{offset[:3]}:{offset[3:]}" if offset else "unknown"
    name = value.tzname() or "unknown"
    return f"{name} ({formatted_offset})"


def format_sources(sources: list[str]) -> str:
    public_sources = [source.strip() for source in sources if source.strip()]
    if not public_sources:
        return "- 未記載"
    return "\n".join(f"- {source}" for source in public_sources)


def render_template(
    template: str,
    *,
    title: str,
    shelf: str,
    kind: str,
    created_at: datetime,
    clock_calibration: str,
    authoring_agent: str,
    scope: str,
    exclusions: str,
    sources: list[str],
) -> str:
    replacements = {
        "{{TITLE}}": title.strip(),
        "{{SHELF}}": shelf,
        "{{KIND}}": kind,
        "{{CREATED_AT}}": created_at.isoformat(timespec="seconds"),
        "{{TIMEZONE}}": timezone_label(created_at),
        "{{CLOCK_CALIBRATION}}": clock_calibration,
        "{{AUTHORING_AGENT}}": authoring_agent.strip() or "human-or-unspecified",
        "{{SCOPE}}": scope.strip() or "未整理。",
        "{{EXCLUSIONS}}": exclusions.strip() or "未整理。",
        "{{SOURCES}}": format_sources(sources),
    }
    rendered = template
    for marker, value in replacements.items():
        rendered = rendered.replace(marker, value)
    unresolved = re.findall(r"\{\{[A-Z_]+\}\}", rendered)
    if unresolved:
        raise ValueError(f"templateに未解決markerがあります: {', '.join(unresolved)}")
    return rendered.rstrip() + "\n"


def collision_safe_path(note_dir: Path, stem: str) -> Path:
    candidate = note_dir / f"{stem}.ja.md"
    if not candidate.exists():
        return candidate
    for sequence in range(2, 1000):
        candidate = note_dir / f"{stem}_{sequence:02d}.ja.md"
        if not candidate.exists():
            return candidate
    raise ValueError("同一時刻・題名のnoteが999件あり、安全なpathを生成できません。")


def create_note(
    *,
    title: str,
    shelf: str,
    kind: str = "brainstorm",
    scope: str = "未整理。",
    exclusions: str = "未整理。",
    sources: list[str] | None = None,
    authoring_agent: str = "human-or-unspecified",
    clock_calibration: str = "unverified",
    repo_root: Path | None = None,
    dry_run: bool = False,
    timestamp: str | None = None,
) -> NoteResult:
    if shelf not in SHELVES:
        raise ValueError(f"未対応のshelfです: {shelf}")
    if kind not in KINDS:
        raise ValueError(f"未対応のkindです: {kind}")
    if clock_calibration not in {"calibrated", "unverified", "unknown"}:
        raise ValueError(f"未対応のclock calibrationです: {clock_calibration}")

    root = find_repo_root(repo_root)
    template_path = root / TEMPLATE_PATH
    note_dir = root / "note"
    if not note_dir.is_dir():
        raise ValueError(f"note directoryがありません: {note_dir}")

    created_at = parse_timestamp(timestamp)
    filename_title = sanitize_title(title)
    stem = f"{created_at.strftime('%Y%m%d-%H%M')}__{filename_title}"
    destination = collision_safe_path(note_dir, stem)
    template = template_path.read_text(encoding="utf-8")
    content = render_template(
        template,
        title=title,
        shelf=shelf,
        kind=kind,
        created_at=created_at,
        clock_calibration=clock_calibration,
        authoring_agent=authoring_agent,
        scope=scope,
        exclusions=exclusions,
        sources=sources or [],
    )

    if not dry_run:
        destination.write_text(content, encoding="utf-8", newline="\n")
    return NoteResult(path=destination, content=content, dry_run=dry_run)
