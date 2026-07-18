"""Atlantisの機械可読契約を安全に読み込む。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


AGENT_REGISTRY = Path("agents/registry.json")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"設定ファイルがありません: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"JSONを解釈できません: {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON rootはobjectである必要があります: {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def load_agent_registry(root: Path) -> dict[str, Any]:
    registry = load_json(root / AGENT_REGISTRY)
    providers = registry.get("providers")
    if not isinstance(providers, list):
        raise ValueError("agents/registry.jsonのprovidersはarrayである必要があります。")
    seen: set[str] = set()
    for item in providers:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("providerには文字列idが必要です。")
        if item["id"] in seen:
            raise ValueError(f"provider idが重複しています: {item['id']}")
        seen.add(item["id"])
    return registry


def provider_map(root: Path) -> dict[str, dict[str, Any]]:
    registry = load_agent_registry(root)
    return {item["id"]: item for item in registry["providers"]}


def load_adapter(root: Path, provider_id: str) -> dict[str, Any]:
    providers = provider_map(root)
    try:
        entry = providers[provider_id]
    except KeyError as error:
        raise ValueError(f"未登録のproviderです: {provider_id}") from error
    relative = Path(entry["adapter"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"adapter pathがrepository外を指しています: {relative}")
    adapter = load_json(root / relative)
    if adapter.get("id") != provider_id:
        raise ValueError(f"adapter idがregistryと一致しません: {provider_id}")
    return adapter


def policy_paths(root: Path) -> dict[str, Path]:
    registry = load_agent_registry(root)
    result: dict[str, Path] = {}
    for key in ("default_constraints", "secret_boundaries", "cost_policy"):
        relative = Path(registry[key])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"policy pathがrepository外を指しています: {relative}")
        result[key] = root / relative
    return result
