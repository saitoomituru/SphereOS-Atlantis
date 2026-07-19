"""repository-nativeなCORN work itemとcontext closureをofflineで扱う。"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping

from .config import load_json
from .note import find_repo_root


CORN_ROOT = Path("corn")
REGISTRY_PATH = CORN_ROOT / "registry.json"
WORK_ITEM_ID = re.compile(r"^CORN-[0-9]{4,}$")
EVENT_ID = re.compile(r"^CORN-EVENT-[0-9]{4,}$")
REQUIRED_WORK_ITEM_FIELDS = {
    "schema_version",
    "work_item_id",
    "title",
    "kind",
    "workflow_state",
    "authority",
    "status_axes",
    "context",
    "projections",
    "provenance",
    "unknowns",
}
REQUIRED_EVENT_FIELDS = {
    "event_id",
    "work_item_id",
    "event_type",
    "observed_at",
    "clock_calibration",
    "actor_or_adapter",
    "source_ref",
    "result",
    "conflicts",
    "receipt_hash",
}


def _safe_relative(value: object, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}には空でないrelative pathが必要です。")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field}がrepository外を指しています: {path}")
    return path


def _hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _hash_file(path: Path) -> str:
    return _hash_bytes(path.read_bytes())


def _canonical_hash(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _hash_bytes(payload)


def load_corn_registry(root: Path) -> dict[str, Any]:
    registry = load_json(root / REGISTRY_PATH)
    if registry.get("schema_version") != "1.0.0":
        raise ValueError("CORN registry schema_versionは1.0.0である必要があります。")
    if not isinstance(registry.get("repositories"), dict):
        raise ValueError("CORN registryにはrepositoriesが必要です。")
    sources = registry.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("CORN registryには1件以上のsourcesが必要です。")
    source_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("CORN sourceはobjectである必要があります。")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id.strip():
            raise ValueError("CORN sourceにはidが必要です。")
        if source_id in source_ids:
            raise ValueError(f"CORN source idが重複しています: {source_id}")
        source_ids.add(source_id)
        repository = source.get("repository")
        if repository not in registry["repositories"]:
            raise ValueError(f"{source_id}のrepositoryが未登録です: {repository}")
        _safe_relative(source.get("path"), f"sources[{source_id}].path")
        if not isinstance(source.get("required"), bool):
            raise ValueError(f"{source_id}のrequiredはbooleanである必要があります。")
    registry["_source_ids"] = source_ids
    return registry


def _load_relative_json(root: Path, raw_path: object, field: str) -> dict[str, Any]:
    path = _safe_relative(raw_path, field)
    return load_json(root / path)


def load_hook_registry(root: Path, registry: dict[str, Any]) -> dict[str, Any]:
    hooks = _load_relative_json(root, registry.get("hook_registry"), "hook_registry")
    if hooks.get("schema_version") != "1.0.0" or not isinstance(hooks.get("hooks"), list):
        raise ValueError("CORN hook registryが不正です。")
    seen: set[str] = set()
    for hook in hooks["hooks"]:
        hook_id = hook.get("id") if isinstance(hook, dict) else None
        if not isinstance(hook_id, str) or not hook_id:
            raise ValueError("CORN hookにはidが必要です。")
        if hook_id in seen:
            raise ValueError(f"CORN hook idが重複しています: {hook_id}")
        seen.add(hook_id)
        for source_id in hook.get("source_ids", []):
            if source_id not in registry["_source_ids"]:
                raise ValueError(f"{hook_id}が未登録sourceを要求しています: {source_id}")
    return hooks


def load_projection_registry(root: Path, registry: dict[str, Any]) -> dict[str, Any]:
    projections = _load_relative_json(
        root,
        registry.get("projection_registry"),
        "projection_registry",
    )
    if projections.get("schema_version") != "1.0.0" or not isinstance(
        projections.get("adapters"), list
    ):
        raise ValueError("CORN projection registryが不正です。")
    adapter_ids = [item.get("id") for item in projections["adapters"]]
    if any(not isinstance(item, str) or not item for item in adapter_ids):
        raise ValueError("CORN projection adapterにはidが必要です。")
    if len(set(adapter_ids)) != len(adapter_ids):
        raise ValueError("CORN projection adapter idが重複しています。")
    return projections


def _work_item_path(root: Path, work_item_id: str) -> Path:
    if not WORK_ITEM_ID.fullmatch(work_item_id):
        raise ValueError(f"不正なCORN work item IDです: {work_item_id}")
    return root / CORN_ROOT / "work-items" / f"{work_item_id}.json"


def load_work_item(root: Path, work_item_id: str) -> dict[str, Any]:
    path = _work_item_path(root, work_item_id)
    if not path.is_file():
        raise ValueError(f"CORN work itemが見つかりません: {work_item_id}")
    item = load_json(path)
    if item.get("work_item_id") != work_item_id:
        raise ValueError(f"work item IDとfilenameが一致しません: {work_item_id}")
    return item


def _validate_work_item(
    item: dict[str, Any],
    registry: dict[str, Any],
    hook_ids: set[str] | None = None,
    adapter_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_WORK_ITEM_FIELDS - item.keys())
    if missing:
        errors.append(f"required field欠損: {', '.join(missing)}")
        return errors
    work_item_id = item.get("work_item_id")
    if not isinstance(work_item_id, str) or not WORK_ITEM_ID.fullmatch(work_item_id):
        errors.append("work_item_idがCORN-NNNN形式ではない")
    if not isinstance(item.get("title"), str) or not item["title"].strip():
        errors.append("titleが空")
    if item.get("workflow_state") not in registry.get("workflow_states", []):
        errors.append(f"workflow_stateが未登録: {item.get('workflow_state')}")
    axes = item.get("status_axes")
    if not isinstance(axes, dict):
        errors.append("status_axesがobjectではない")
    else:
        for axis, allowed in registry.get("status_axes", {}).items():
            if axes.get(axis) not in allowed:
                errors.append(f"status_axes.{axis}が未登録: {axes.get(axis)}")
    context = item.get("context")
    if not isinstance(context, dict):
        errors.append("contextがobjectではない")
    else:
        for source_id in context.get("required_sources", []):
            if source_id not in registry["_source_ids"]:
                errors.append(f"未登録required source: {source_id}")
        if hook_ids is not None:
            for hook_id in context.get("required_hooks", []):
                if hook_id not in hook_ids:
                    errors.append(f"未登録required hook: {hook_id}")
    if not isinstance(item.get("projections"), list):
        errors.append("projectionsがlistではない")
    elif adapter_ids is not None:
        for projection in item["projections"]:
            adapter = projection.get("adapter") if isinstance(projection, dict) else None
            if adapter not in adapter_ids:
                errors.append(f"未登録projection adapter: {adapter}")
    if not isinstance(item.get("unknowns"), list):
        errors.append("unknownsがlistではない")
    return errors


def event_receipt_hash(event: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in event.items() if key != "receipt_hash"}
    return _canonical_hash(payload)


def _validate_events(root: Path, known_items: set[str]) -> tuple[int, list[str]]:
    event_dir = root / CORN_ROOT / "events"
    errors: list[str] = []
    count = 0
    if not event_dir.is_dir():
        return 0, ["corn/eventsが見つかりません"]
    for path in sorted(event_dir.glob("*.jsonl")):
        expected_item = path.stem
        for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw_line.strip():
                continue
            count += 1
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as error:
                errors.append(f"{path.name}:{line_number}: JSON不正: {error}")
                continue
            missing = REQUIRED_EVENT_FIELDS - event.keys()
            if missing:
                errors.append(
                    f"{path.name}:{line_number}: event field欠損: {', '.join(sorted(missing))}"
                )
                continue
            if not EVENT_ID.fullmatch(str(event.get("event_id", ""))):
                errors.append(f"{path.name}:{line_number}: event_id不正")
            if event.get("work_item_id") != expected_item:
                errors.append(f"{path.name}:{line_number}: filenameとwork_item_idが不一致")
            if event.get("work_item_id") not in known_items:
                errors.append(f"{path.name}:{line_number}: 未登録work item event")
            if event.get("receipt_hash") != event_receipt_hash(event):
                errors.append(f"{path.name}:{line_number}: receipt_hash不一致")
    return count, errors


def validate_corn(repo_root: Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_corn_registry(root)
    hook_registry = load_hook_registry(root, registry)
    projection_registry = load_projection_registry(root, registry)
    hook_ids = {item["id"] for item in hook_registry["hooks"]}
    adapter_ids = {item["id"] for item in projection_registry["adapters"]}
    work_item_dir = root / CORN_ROOT / "work-items"
    errors: list[str] = []
    item_results: list[dict[str, Any]] = []
    known_items: set[str] = set()
    if not work_item_dir.is_dir():
        errors.append("corn/work-itemsが見つかりません")
    else:
        for path in sorted(work_item_dir.glob("*.json")):
            item = load_json(path)
            item_id = str(item.get("work_item_id", ""))
            item_errors = _validate_work_item(item, registry, hook_ids, adapter_ids)
            if item_id in known_items:
                item_errors.append("work_item_idが重複")
            if item_id:
                known_items.add(item_id)
            if path.stem != item_id:
                item_errors.append("filenameとwork_item_idが不一致")
            errors.extend(f"{path.name}: {message}" for message in item_errors)
            item_results.append(
                {
                    "work_item_id": item_id or path.stem,
                    "status": "pass" if not item_errors else "fail",
                    "errors": item_errors,
                }
            )
    event_count, event_errors = _validate_events(root, known_items)
    errors.extend(event_errors)
    return {
        "schema_version": "1.0.0",
        "stack_id": registry.get("stack_id"),
        "stack_version": registry.get("stack_version"),
        "overall": "pass" if not errors else "fail",
        "work_items": item_results,
        "event_count": event_count,
        "hooks": len(hook_registry["hooks"]),
        "projection_adapters": [item["id"] for item in projection_registry["adapters"]],
        "errors": errors,
        "mutations_performed": False,
        "network_access_performed": False,
    }


def _repository_roots(
    root: Path,
    registry: dict[str, Any],
    overrides: Mapping[str, Path] | None,
) -> dict[str, Path]:
    resolved = {name: Path(path).expanduser().resolve() for name, path in (overrides or {}).items()}
    for repository, config in registry["repositories"].items():
        if repository in resolved:
            continue
        if config.get("root_strategy") == "self":
            resolved[repository] = root
            continue
        environment = config.get("environment")
        if isinstance(environment, str) and os.environ.get(environment):
            candidate = Path(os.environ[environment]).expanduser().resolve()
            marker = _safe_relative(config.get("marker"), f"repositories[{repository}].marker")
            if (candidate / marker).is_file():
                resolved[repository] = candidate
                continue
        marker = _safe_relative(config.get("marker"), f"repositories[{repository}].marker")
        candidates = config.get("relative_candidates", [])
        for ancestor in (root, *root.parents):
            for raw_candidate in candidates:
                candidate = ancestor / _safe_relative(
                    raw_candidate,
                    f"repositories[{repository}].relative_candidates",
                )
                if (candidate / marker).is_file():
                    resolved[repository] = candidate.resolve()
                    break
            if repository in resolved:
                break
    return resolved


def _public_url(registry: dict[str, Any], repository: str, path: Path) -> str:
    remote = str(registry["repositories"][repository]["remote"]).rstrip("/")
    return f"{remote}/blob/main/{path.as_posix()}"


def _context_fingerprint(sources: list[dict[str, Any]]) -> str:
    return _canonical_hash(
        [
            {"id": item["id"], "sha256": item["sha256"]}
            for item in sources
            if item.get("local_exists")
        ]
    )


def build_context_receipt(
    work_item_id: str,
    repo_root: Path | None = None,
    repository_roots: Mapping[str, Path] | None = None,
    write_capsule: bool = False,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_corn_registry(root)
    hooks = load_hook_registry(root, registry)
    item = load_work_item(root, work_item_id)
    item_errors = _validate_work_item(item, registry)
    if item_errors:
        raise ValueError(f"{work_item_id}が不正です: {'; '.join(item_errors)}")
    roots = _repository_roots(root, registry, repository_roots)
    source_by_id = {item["id"]: item for item in registry["sources"]}
    required_ids = list(
        dict.fromkeys(
            [
                *registry["context"]["required_sources"],
                *item["context"].get("required_sources", []),
            ]
        )
    )
    resolved_sources: list[dict[str, Any]] = []
    for source_id in required_ids:
        source = source_by_id[source_id]
        repository = source["repository"]
        relative = _safe_relative(source["path"], f"sources[{source_id}].path")
        repository_root = roots.get(repository)
        local_path = repository_root / relative if repository_root else None
        local_exists = bool(local_path and local_path.is_file())
        resolved_sources.append(
            {
                "id": source_id,
                "repository": repository,
                "path": str(relative),
                "required": source["required"],
                "local_path": str(local_path) if local_path else None,
                "local_exists": local_exists,
                "sha256": _hash_file(local_path) if local_exists and local_path else None,
                "public_url": _public_url(registry, repository, relative),
            }
        )
    work_item_path = _work_item_path(root, work_item_id)
    resolved_sources.append(
        {
            "id": "work-item",
            "repository": "SphereOS-Atlantis",
            "path": str(work_item_path.relative_to(root)),
            "required": True,
            "local_path": str(work_item_path),
            "local_exists": True,
            "sha256": _hash_file(work_item_path),
            "public_url": _public_url(
                registry,
                "SphereOS-Atlantis",
                work_item_path.relative_to(root),
            ),
        }
    )
    requested_hooks = item["context"].get("required_hooks", [])
    hook_by_id = {hook["id"]: hook for hook in hooks["hooks"]}
    hook_results: list[dict[str, Any]] = []
    for hook_id in requested_hooks:
        if hook_id not in hook_by_id:
            raise ValueError(f"{work_item_id}が未登録hookを要求しています: {hook_id}")
        hook = hook_by_id[hook_id]
        hook_sources = set(hook.get("source_ids", []))
        ready_sources = {
            source["id"]
            for source in resolved_sources
            if source["local_exists"]
        }
        hook_results.append(
            {
                "id": hook_id,
                "mode": hook.get("mode"),
                "required": hook.get("required", False),
                "source_status": "ready" if hook_sources <= ready_sources else "incomplete",
                "execution_status": "not-executed-by-context-reader",
            }
        )
    missing = [source["id"] for source in resolved_sources if source["required"] and not source["local_exists"]]
    fingerprint = _context_fingerprint(resolved_sources)
    capsule_path = root / ".atlantis/corn/capsules" / f"{work_item_id}.json"
    capsule_status = "missing"
    if capsule_path.is_file():
        try:
            capsule = load_json(capsule_path)
        except (OSError, ValueError, json.JSONDecodeError):
            capsule_status = "invalid"
        else:
            capsule_status = (
                "current" if capsule.get("context_fingerprint") == fingerprint else "stale"
            )
    observed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    capsule_written = False
    if write_capsule and missing:
        capsule_status = "not-written-context-incomplete"
    elif write_capsule:
        capsule_path.parent.mkdir(parents=True, exist_ok=True)
        capsule_payload = {
            "schema_version": "1.0.0",
            "work_item_id": work_item_id,
            "generated_at": observed_at,
            "clock_calibration": "unverified",
            "context_fingerprint": fingerprint,
            "sources": [
                {"id": source["id"], "sha256": source["sha256"]}
                for source in resolved_sources
                if source["local_exists"]
            ],
            "canonical": False,
        }
        temporary = capsule_path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(capsule_payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        temporary.replace(capsule_path)
        capsule_status = "current"
        capsule_written = True
    overall = "complete" if not missing else "incomplete"
    return {
        "schema_version": "1.0.0",
        "work_item_id": work_item_id,
        "overall": overall,
        "observed_at": observed_at,
        "clock_calibration": "unverified",
        "repository_roots": {name: str(path) for name, path in sorted(roots.items())},
        "sources": resolved_sources,
        "missing_required_sources": missing,
        "required_hooks": hook_results,
        "context_fingerprint": fingerprint,
        "capsule": {
            "path": str(capsule_path),
            "status": capsule_status,
            "canonical": False,
        },
        "last_order": None if not missing else registry["context"]["incomplete_last_order"],
        "mutations_performed": capsule_written,
        "network_access_performed": False,
    }


def forge_projection_plan(
    work_item_id: str,
    adapter_id: str,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_corn_registry(root)
    projections = load_projection_registry(root, registry)
    adapter_by_id = {item["id"]: item for item in projections["adapters"]}
    if adapter_id not in adapter_by_id:
        raise ValueError(f"未登録のForge adapterです: {adapter_id}")
    item = load_work_item(root, work_item_id)
    matches = [
        projection
        for projection in item.get("projections", [])
        if projection.get("adapter") == adapter_id
    ]
    if len(matches) > 1:
        raise ValueError(f"{work_item_id}の{adapter_id} projectionが重複しています。")
    projection = matches[0] if matches else None
    return {
        "schema_version": "1.0.0",
        "work_item_id": work_item_id,
        "adapter": adapter_by_id[adapter_id],
        "mode": "plan-only",
        "action": "observe-existing" if projection else "create-projection",
        "projection": projection,
        "canonical_direction": projections["canonical_direction"],
        "forge_import_policy": projections["forge_import_policy"],
        "conflict_last_order": projections["conflict_last_order"],
        "mutations_performed": False,
        "network_access_performed": False,
    }


def tick_corn(
    work_item_id: str,
    reason: str,
    repo_root: Path | None = None,
    repository_roots: Mapping[str, Path] | None = None,
) -> dict[str, Any]:
    if not reason.strip():
        raise ValueError("tick reasonは空にできません。")
    root = find_repo_root(repo_root)
    context = build_context_receipt(
        work_item_id,
        root,
        repository_roots=repository_roots,
        write_capsule=False,
    )
    observed = datetime.now(timezone.utc)
    result = {
        "schema_version": "1.0.0",
        "work_item_id": work_item_id,
        "activation_reason": reason.strip(),
        "observed_at": observed.isoformat(timespec="seconds"),
        "clock_calibration": "unverified",
        "status": "plan-ready" if context["overall"] == "complete" else "context-blocked",
        "action": "await-authorized-runner",
        "context_fingerprint": context["context_fingerprint"],
        "last_order": context["last_order"],
        "authorized_mutation": False,
        "project_mutations_performed": False,
        "network_access_performed": False,
    }
    receipt_dir = root / ".atlantis/corn/receipts"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / f"tick-{observed.strftime('%Y%m%dT%H%M%S%fZ')}.json"
    receipt_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    result["receipt_path"] = str(receipt_path)
    result["mutations_performed"] = True
    return result


def format_corn_report(result: dict[str, Any]) -> str:
    title = result.get("work_item_id") or result.get("stack_id") or "CORN"
    state = result.get("overall") or result.get("status") or result.get("action")
    lines = [f"{title}: {str(state).upper()}"]
    for error in result.get("errors", []):
        lines.append(f"ERROR {error}")
    if result.get("missing_required_sources"):
        lines.append(
            "missing required: " + ", ".join(result["missing_required_sources"])
        )
    if result.get("receipt_path"):
        lines.append(f"receipt: {result['receipt_path']}")
    lines.append(
        f"mutations: {str(result.get('mutations_performed', False)).lower()}; "
        f"network: {str(result.get('network_access_performed', False)).lower()}"
    )
    return "\n".join(lines)
