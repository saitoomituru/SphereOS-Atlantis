"""利用者をexpertと仮定せず、現在能力と入口を読み取り専用で案内する。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_json
from .note import find_repo_root
from .tutorial import start_tutorial


CAPABILITY_REGISTRY_PATH = Path("help/capabilities.json")


def load_capability_registry(root: Path) -> dict[str, Any]:
    registry = load_json(root / CAPABILITY_REGISTRY_PATH)
    if registry.get("schema_version") != "1.0.0":
        raise ValueError("capability registry schema_versionは1.0.0である必要があります。")
    for key in ("proficiency_values", "intent_values", "states", "entry_options", "capabilities"):
        value = registry.get(key)
        if not isinstance(value, list) or not value:
            raise ValueError(f"capability registryに{key}がありません。")
    defaults = registry.get("defaults")
    if not isinstance(defaults, dict):
        raise ValueError("capability registryにdefaultsがありません。")
    if defaults.get("proficiency") not in registry["proficiency_values"]:
        raise ValueError("既定proficiencyが未登録です。")
    if defaults.get("intent") not in registry["intent_values"]:
        raise ValueError("既定intentが未登録です。")
    seen: set[str] = set()
    for capability in registry["capabilities"]:
        if not isinstance(capability, dict) or not isinstance(capability.get("id"), str):
            raise ValueError("capabilityには文字列idが必要です。")
        if capability["id"] in seen:
            raise ValueError(f"capability idが重複しています: {capability['id']}")
        seen.add(capability["id"])
        if capability.get("state") not in registry["states"]:
            raise ValueError(f"capability stateが未登録です: {capability['id']}")
        if not isinstance(capability.get("evidence"), list) or not capability["evidence"]:
            raise ValueError(f"capability evidenceがありません: {capability['id']}")
    return registry


def build_help(
    *,
    personas: list[str] | None = None,
    proficiency: str | None = None,
    intent: str | None = None,
    state: str | None = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_capability_registry(root)
    selected_proficiency = proficiency or registry["defaults"]["proficiency"]
    selected_intent = intent or registry["defaults"]["intent"]
    if selected_proficiency not in registry["proficiency_values"]:
        raise ValueError(f"未登録のproficiencyです: {selected_proficiency}")
    if selected_intent not in registry["intent_values"]:
        raise ValueError(f"未登録のintentです: {selected_intent}")
    if state is not None and state not in registry["states"]:
        raise ValueError(f"未登録のcapability stateです: {state}")

    declared = personas or []
    tutorial = (
        start_tutorial(
            declared,
            proficiency=selected_proficiency,
            intent=selected_intent,
            repo_root=root,
        )
        if declared
        else None
    )
    capabilities = [
        item for item in registry["capabilities"] if state is None or item["state"] == state
    ]
    return {
        "schema_version": "1.0.0",
        "status": "HELP-READY",
        "proficiency": selected_proficiency,
        "intent": selected_intent,
        "declared_personas": declared,
        "tutorial": tutorial,
        "capabilities": capabilities,
        "entry_options": registry["entry_options"],
        "implementation_requires_explicit_selection": True,
        "context_status": "CONTEXT-READ-REQUIRED",
        "identity_inferred": False,
        "permissions_granted": False,
        "mutation_performed": False,
        "mutations_performed": False,
        "network_access_performed": False,
    }


def format_help(result: dict[str, Any]) -> str:
    lines = [
        f"status: {result['status']}",
        f"proficiency: {result['proficiency']}",
        f"intent: {result['intent']}",
        "capabilities:",
    ]
    lines.extend(
        f"  - [{item['state']}] {item['label_ja']}: {item['summary_ja']}"
        for item in result["capabilities"]
    )
    lines.append("entry-options:")
    lines.extend(
        f"  - {index}. {item['label_ja']}"
        for index, item in enumerate(result["entry_options"], start=1)
    )
    lines.append("まだrepositoryへ変更は加えていません。")
    return "\n".join(lines)
