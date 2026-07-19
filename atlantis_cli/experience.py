"""Experience Receiptを生の表現を潰さずrepositoryへ保存する。"""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any

from .config import load_json
from .note import find_repo_root, parse_timestamp, sanitize_title


EXPERIENCE_REGISTRY_PATH = Path("experience/registry.json")
RECEIPT_DIRECTORY = Path("experience/receipts")


def load_experience_registry(root: Path) -> dict[str, Any]:
    registry = load_json(root / EXPERIENCE_REGISTRY_PATH)
    if registry.get("schema_version") != "1.0.0":
        raise ValueError("experience registry schema_versionは1.0.0である必要があります。")
    defaults = registry.get("default_status")
    dispositions = registry.get("dispositions")
    if not isinstance(defaults, dict) or not defaults:
        raise ValueError("experience registryにdefault_statusが必要です。")
    if not isinstance(dispositions, list) or not dispositions:
        raise ValueError("experience registryにdispositionsが必要です。")
    if any(not isinstance(item, str) or not item for item in dispositions):
        raise ValueError("experience dispositionは空でない文字列である必要があります。")
    return registry


def _destination(root: Path, created_at: datetime, summary: str) -> Path:
    directory = root / RECEIPT_DIRECTORY
    stem = f"{created_at.strftime('%Y%m%d-%H%M')}__{sanitize_title(summary)}"
    candidate = directory / f"{stem}.json"
    if not candidate.exists():
        return candidate
    for sequence in range(2, 1000):
        candidate = directory / f"{stem}_{sequence:02d}.json"
        if not candidate.exists():
            return candidate
    raise ValueError("同一時刻・要約のExperience Receiptが999件あります。")


def create_experience_receipt(
    *,
    summary: str,
    raw_signals: list[str],
    self_clusters: list[str] | None = None,
    world: str = "not-declared",
    context: str = "not-declared",
    request_cluster_review: bool = False,
    timestamp: str | None = None,
    repo_root: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_experience_registry(root)
    clean_summary = summary.strip()
    signals = [value.strip() for value in raw_signals if value.strip()]
    clusters = [value.strip() for value in (self_clusters or []) if value.strip()]
    if not clean_summary:
        raise ValueError("Experience Receiptにはsummaryが必要です。")
    if not signals:
        raise ValueError("Experience Receiptには1件以上のraw signalが必要です。")
    created_at = parse_timestamp(timestamp)
    destination = _destination(root, created_at, clean_summary)
    receipt_id = destination.stem.replace("__", "-").upper()
    value = {
        "schema_version": "1.0.0",
        "receipt_id": f"EXP-{receipt_id}",
        "created_at_system": created_at.isoformat(timespec="seconds"),
        "clock_calibration": "unverified",
        "summary": clean_summary,
        "raw_experience_signals": signals,
        "reporter_self_declared_clusters": clusters,
        "world": world.strip() or "not-declared",
        "context": context.strip() or "not-declared",
        "status": dict(registry["default_status"]),
        "cluster_review": "requested" if request_cluster_review else "not-requested",
        "candidate_dispositions": registry["dispositions"],
        "selected_disposition": None,
        "by_design_claim": None,
        "hypotheses": [],
        "evidence": [],
        "identity_inferred": False,
        "specification_changed": False,
        "report_rejected": False,
        "network_access_performed": False,
    }
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return {
        "path": str(destination),
        "dry_run": dry_run,
        "receipt": value,
    }


def validate_experience(root: Path | None = None) -> dict[str, Any]:
    repo_root = find_repo_root(root)
    registry = load_experience_registry(repo_root)
    errors: list[str] = []
    receipts: list[str] = []
    for path in sorted((repo_root / RECEIPT_DIRECTORY).glob("*.json")):
        try:
            value = load_json(path)
            if value.get("schema_version") != "1.0.0":
                raise ValueError("schema_versionが1.0.0ではありません。")
            signals = value.get("raw_experience_signals")
            if not isinstance(signals, list) or not signals:
                raise ValueError("raw_experience_signalsがありません。")
            if value.get("identity_inferred") is not False:
                raise ValueError("identity_inferredはfalseである必要があります。")
            disposition = value.get("selected_disposition")
            if disposition is not None and disposition not in registry["dispositions"]:
                raise ValueError(f"未登録dispositionです: {disposition}")
            if disposition == "by-design-with-scope":
                claim = value.get("by_design_claim")
                required = registry["by_design_requirements"]
                if not isinstance(claim, dict) or any(not claim.get(key) for key in required):
                    raise ValueError("by-designにはscope、evidence、reconsider triggerが必要です。")
        except (KeyError, TypeError, ValueError) as error:
            errors.append(f"{path.relative_to(repo_root)}: {error}")
        else:
            receipts.append(str(path.relative_to(repo_root)))
    return {
        "schema_version": "1.0.0",
        "overall": "fail" if errors else "pass",
        "receipt_count": len(receipts),
        "receipts": receipts,
        "errors": errors,
        "network_access_performed": False,
        "mutations_performed": False,
    }


def format_experience(result: dict[str, Any]) -> str:
    if "receipt" in result:
        state = "DRY-RUN" if result["dry_run"] else "CREATED"
        return f"[{state}] {result['path']}\nstatus: received; triage: pending"
    lines = [f"overall: {result['overall']}", f"receipts: {result['receipt_count']}"]
    lines.extend(f"error: {error}" for error in result["errors"])
    return "\n".join(lines)
