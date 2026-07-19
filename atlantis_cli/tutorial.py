"""自己申告personaから、非越権なtutorial入口を宣言的に解決する。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_json
from .note import find_repo_root


PERSONA_REGISTRY_PATH = Path("tutorial/personas.json")
SOURCE_MAP_PATH = Path("skills/learn-sphereos-atlantis/references/source-map.json")


def _clean(value: str) -> str:
    return value.strip().casefold()


def load_persona_registry(root: Path) -> dict[str, Any]:
    registry = load_json(root / PERSONA_REGISTRY_PATH)
    if registry.get("schema_version") != "1.0.0":
        raise ValueError("persona registry schema_versionは1.0.0である必要があります。")
    profiles = registry.get("profiles")
    routes = registry.get("routes")
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("persona registryには1件以上のprofilesが必要です。")
    if not isinstance(routes, dict) or not routes:
        raise ValueError("persona registryにはroutesが必要です。")
    seen_ids: set[str] = set()
    alias_owners: dict[str, str] = {}
    for profile in profiles:
        if not isinstance(profile, dict) or not isinstance(profile.get("id"), str):
            raise ValueError("persona profileには文字列idが必要です。")
        profile_id = profile["id"]
        if profile_id in seen_ids:
            raise ValueError(f"persona profile idが重複しています: {profile_id}")
        seen_ids.add(profile_id)
        aliases = profile.get("aliases")
        shelves = profile.get("entry_shelves")
        if not isinstance(aliases, list) or not aliases:
            raise ValueError(f"persona profileにaliasesがありません: {profile_id}")
        if not isinstance(shelves, list) or not shelves:
            raise ValueError(f"persona profileにentry_shelvesがありません: {profile_id}")
        route = profile.get("recommended_route")
        if route not in routes:
            raise ValueError(f"persona profileのrouteが未登録です: {profile_id}: {route}")
        for alias in [profile_id, *aliases]:
            normalized = _clean(alias)
            if not normalized:
                raise ValueError(f"persona aliasが空です: {profile_id}")
            owner = alias_owners.get(normalized)
            if owner is not None and owner != profile_id:
                raise ValueError(f"persona aliasが重複しています: {alias}")
            alias_owners[normalized] = profile_id
    return registry


def _source_ref(item: dict[str, Any]) -> str:
    return f"{item['repository']}:{item['path']}"


def start_tutorial(
    personas: list[str],
    *,
    route: str = "auto",
    proficiency: str = "unknown",
    intent: str = "look-around",
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_persona_registry(root)
    source_map = load_json(root / SOURCE_MAP_PATH)
    if not personas or not any(value.strip() for value in personas):
        raise ValueError("tutorial startには1件以上の自己申告personaが必要です。")
    if route != "auto" and route not in registry["routes"]:
        raise ValueError(f"未登録のtutorial routeです: {route}")
    proficiency_values = {"unknown", "newcomer", "explorer", "contributor", "maintainer"}
    intent_values = {"look-around", "learn", "write-note", "report-experience", "inspect", "implement"}
    if proficiency not in proficiency_values:
        raise ValueError(f"未登録のproficiencyです: {proficiency}")
    if intent not in intent_values:
        raise ValueError(f"未登録のintentです: {intent}")

    alias_map: dict[str, dict[str, Any]] = {}
    for profile in registry["profiles"]:
        for alias in [profile["id"], *profile["aliases"]]:
            alias_map[_clean(alias)] = profile

    declared = [value.strip() for value in personas if value.strip()]
    matched: list[dict[str, Any]] = []
    unresolved: list[str] = []
    seen_profiles: set[str] = set()
    for value in declared:
        profile = alias_map.get(_clean(value))
        if profile is None:
            unresolved.append(value)
        elif profile["id"] not in seen_profiles:
            matched.append(profile)
            seen_profiles.add(profile["id"])

    shelves: list[str] = []
    for profile in matched:
        for shelf in profile["entry_shelves"]:
            if shelf not in shelves:
                shelves.append(shelf)
    if not shelves:
        shelves.append("cross-shelf")

    known_shelves = source_map.get("shelves", {})
    sources = [_source_ref(item) for item in source_map.get("common", [])]
    for shelf in shelves:
        for item in known_shelves.get(shelf, []):
            reference = _source_ref(item)
            if reference not in sources:
                sources.append(reference)

    requested_route = route
    selected_route = route
    if intent == "implement":
        selected_route = "full-development" if route == "auto" else route
    elif intent in {"write-note", "report-experience"}:
        selected_route = "note-only" if route == "auto" else route
    else:
        selected_route = "help"

    return {
        "schema_version": "1.0.0",
        "status": "PROVISIONAL-USER-CONFIRMATION" if unresolved else "HELP-READY",
        "declared_personas": declared,
        "matched_profiles": [profile["id"] for profile in matched],
        "unresolved_personas": unresolved,
        "entry_shelves": shelves,
        "proficiency": proficiency,
        "intent": intent,
        "requested_route": requested_route,
        "route": selected_route,
        "route_contract": registry["routes"][selected_route],
        "required_sources": sources,
        "context_status": "CONTEXT-READ-REQUIRED",
        "next_actions": [
            "本人のpersona、入口、裁定しない範囲を確認する。",
            "required_sourcesの現行原文を読み、要約を正本化しない。",
            (
                "Note雛形を作り、forkまたはbranchからdraft PRを送る。"
                if selected_route == "note-only"
                else (
                    "doctorとtestを実行し、branchからdraft PRを送る。"
                    if selected_route == "full-development"
                    else "現在能力と未実装境界を確認し、次の入口を本人が選ぶ。"
                )
            ),
        ],
        "identity_inferred": False,
        "permissions_granted": False,
        "network_access_performed": False,
        "mutation_performed": False,
        "mutations_performed": False,
    }


def format_tutorial(result: dict[str, Any]) -> str:
    lines = [
        f"status: {result['status']}",
        f"route: {result['route']}",
        f"proficiency: {result['proficiency']}",
        f"intent: {result['intent']}",
        f"profiles: {', '.join(result['matched_profiles']) or 'unresolved'}",
        f"shelves: {', '.join(result['entry_shelves'])}",
        f"context: {result['context_status']}",
    ]
    if result["unresolved_personas"]:
        lines.append(f"user-confirmation: {', '.join(result['unresolved_personas'])}")
    lines.append("required-sources:")
    lines.extend(f"  - {source}" for source in result["required_sources"])
    lines.append("next-actions:")
    lines.extend(f"  - {action}" for action in result["next_actions"])
    return "\n".join(lines)
