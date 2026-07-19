"""利用者をexpertと仮定せず、現在能力と入口を読み取り専用で案内する。"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from .config import load_json
from .note import find_repo_root
from .tutorial import start_tutorial


CAPABILITY_REGISTRY_PATH = Path("help/capabilities.json")
INTERFACE_REGISTRY_PATH = Path("help/interfaces.json")
MACHINE_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


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


def load_interface_registry(root: Path) -> dict[str, Any]:
    registry = load_json(root / INTERFACE_REGISTRY_PATH)
    if registry.get("schema_version") != "1.0.0":
        raise ValueError("interface registry schema_versionは1.0.0である必要があります。")
    if registry.get("contract_state") not in {"ALPHA", "STABLE"}:
        raise ValueError("interface registry contract_stateが未登録です。")

    interfaces = registry.get("interfaces")
    envelopes = registry.get("execution_envelopes")
    defaults = registry.get("default_interface_by_entry")
    presentation = registry.get("presentation_contract")
    authenticity = registry.get("authenticity_contract")
    if not isinstance(interfaces, list) or not interfaces:
        raise ValueError("interface registryにinterfacesがありません。")
    if not isinstance(envelopes, list) or not envelopes:
        raise ValueError("interface registryにexecution_envelopesがありません。")
    if not isinstance(defaults, dict) or not defaults:
        raise ValueError("interface registryにdefault_interface_by_entryがありません。")
    if not isinstance(presentation, dict):
        raise ValueError("interface registryにpresentation_contractがありません。")
    if not isinstance(authenticity, dict):
        raise ValueError("interface registryにauthenticity_contractがありません。")

    seen_interfaces: set[str] = set()
    for item in interfaces:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("interfaceには文字列idが必要です。")
        interface_id = item["id"]
        if not MACHINE_ID_PATTERN.fullmatch(interface_id):
            raise ValueError(f"interface idはkebab-caseである必要があります: {interface_id}")
        if interface_id in seen_interfaces:
            raise ValueError(f"interface idが重複しています: {interface_id}")
        seen_interfaces.add(interface_id)
        if item.get("kind") != "interaction-surface":
            raise ValueError(f"interface kindが不正です: {interface_id}")
        for key in ("display_name", "scoped_alias", "input_contract", "tradeoff_ja"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f"interface {interface_id}に{key}がありません。")
        primary_fit = item.get("primary_fit")
        if not isinstance(primary_fit, dict) or primary_fit.get("axis") not in {"D", "L"}:
            raise ValueError(f"interface primary_fitが不正です: {interface_id}")
        if not isinstance(primary_fit.get("summary_ja"), str):
            raise ValueError(f"interface primary_fit summaryがありません: {interface_id}")
        for nullable_key in ("command_name", "file_extension"):
            if item.get(nullable_key) is not None and not isinstance(item[nullable_key], str):
                raise ValueError(f"interface {nullable_key}が不正です: {interface_id}")
        non_inference = item.get("does_not_infer")
        bindings = item.get("bindings")
        required_non_inference = {
            "execution_envelope",
            "actor_role",
            "persona",
            "world",
            "authority",
            "implementation_state",
        }
        if not isinstance(non_inference, dict) or any(
            non_inference.get(key) is not True for key in required_non_inference
        ):
            raise ValueError(f"interfaceの非推定契約が不足しています: {interface_id}")
        if not isinstance(bindings, dict):
            raise ValueError(f"interface bindingsがありません: {interface_id}")

    for entry, interface_id in defaults.items():
        if not isinstance(entry, str) or interface_id not in seen_interfaces:
            raise ValueError(f"既定interfaceが未登録です: {entry}={interface_id}")

    required_presentation = {
        "route_subject": "current-request-and-explicit-context",
        "persistent_person_classification": False,
        "default_boundary_disclosure": "on-operation-request",
        "permission_disclosure": "on-write-request",
        "unknown_route": "help",
        "default_help_detail": "summary",
    }
    for key, expected in required_presentation.items():
        if presentation.get(key) != expected:
            raise ValueError(f"presentation contractが不正です: {key}")
    if presentation.get("explicit_detail_values") != ["summary", "all"]:
        raise ValueError("presentation detail値はsummaryとallである必要があります。")
    if not isinstance(presentation.get("prompt_line_startup_label_ja"), str):
        raise ValueError("Prompt Line起動labelがありません。")

    if {"prompt-line", "command-line"} - seen_interfaces:
        raise ValueError("prompt-lineとcommand-lineの両interfaceが必要です。")
    prompt_line = next(item for item in interfaces if item["id"] == "prompt-line")
    if prompt_line["command_name"] is not None or prompt_line["file_extension"] is not None:
        raise ValueError("prompt-lineをcommand名またはfile extensionとして公開してはいけません。")

    seen_envelopes: set[str] = set()
    for item in envelopes:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("execution envelopeには文字列idが必要です。")
        envelope_id = item["id"]
        if envelope_id in seen_envelopes:
            raise ValueError(f"execution envelope idが重複しています: {envelope_id}")
        seen_envelopes.add(envelope_id)
        if item.get("layer") != "execution-envelope":
            raise ValueError(f"execution envelope layerが不正です: {envelope_id}")
        if item.get("selects_interface") is not False:
            raise ValueError(f"execution envelopeがinterfaceを決定しています: {envelope_id}")

    required_authenticity = {
        "prompt_line_is_cli_emulation": False,
        "command_line_is_prompt_line_emulation": False,
        "natural_language_is_fake_programming_language": False,
        "interface_does_not_grant_authority": True,
        "interface_does_not_prove_runtime": True,
    }
    for key, expected in required_authenticity.items():
        if authenticity.get(key) is not expected:
            raise ValueError(f"interface authenticity contractが不正です: {key}")
    if authenticity.get("ranking_axis", "missing") is not None:
        raise ValueError("interface間に真贋・優劣ranking axisを置いてはいけません。")
    return registry


def resolve_interface(root: Path, interface_id: str) -> dict[str, Any]:
    registry = load_interface_registry(root)
    for item in registry["interfaces"]:
        if item["id"] == interface_id:
            return item
    raise ValueError(f"未登録のinterfaceです: {interface_id}")


def list_interfaces(
    *, interface_id: str | None = None, repo_root: Path | None = None
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_interface_registry(root)
    selected = (
        [resolve_interface(root, interface_id)]
        if interface_id is not None
        else registry["interfaces"]
    )
    return {
        "schema_version": registry["schema_version"],
        "status": "INTERFACE-CONTRACT-READY",
        "contract_state": registry["contract_state"],
        "interfaces": selected,
        "execution_envelopes": registry["execution_envelopes"],
        "presentation_contract": registry["presentation_contract"],
        "authenticity_contract": registry["authenticity_contract"],
        "mutation_performed": False,
        "network_access_performed": False,
    }


def format_interfaces(result: dict[str, Any]) -> str:
    lines = [
        f"status: {result['status']}",
        f"contract-state: {result['contract_state']}",
        "interfaces:",
    ]
    lines.extend(
        f"  - {item['id']}: {item['display_name']} / primary-fit={item['primary_fit']['axis']}"
        for item in result["interfaces"]
    )
    lines.append("execution-envelopes:")
    lines.extend(
        f"  - {item['id']}: {item['display_name']} (selects-interface=false)"
        for item in result["execution_envelopes"]
    )
    lines.append(result["presentation_contract"]["prompt_line_startup_label_ja"])
    lines.append("boundary-disclosure: on-operation-request")
    lines.append("interfaceは真贋・権限・実装状態を決定しません。")
    return "\n".join(lines)


def build_help(
    *,
    personas: list[str] | None = None,
    proficiency: str | None = None,
    intent: str | None = None,
    state: str | None = None,
    detail: str = "summary",
    interface_id: str = "command-line",
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    registry = load_capability_registry(root)
    interface = resolve_interface(root, interface_id)
    selected_proficiency = proficiency or registry["defaults"]["proficiency"]
    selected_intent = intent or registry["defaults"]["intent"]
    if selected_proficiency not in registry["proficiency_values"]:
        raise ValueError(f"未登録のproficiencyです: {selected_proficiency}")
    if selected_intent not in registry["intent_values"]:
        raise ValueError(f"未登録のintentです: {selected_intent}")
    if state is not None and state not in registry["states"]:
        raise ValueError(f"未登録のcapability stateです: {state}")
    if detail not in {"summary", "all"}:
        raise ValueError(f"未登録のhelp detailです: {detail}")

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
        item
        for item in registry["capabilities"]
        if (
            item["state"] == state
            if state is not None
            else detail == "all" or item["state"] == "AVAILABLE-NOW"
        )
    ]
    state_counts = {
        known_state: sum(
            item["state"] == known_state for item in registry["capabilities"]
        )
        for known_state in registry["states"]
    }
    return {
        "schema_version": "1.0.0",
        "status": "HELP-READY",
        "interface": interface,
        "detail": detail,
        "boundary_disclosure": "on-operation-request",
        "proficiency": selected_proficiency,
        "intent": selected_intent,
        "declared_personas": declared,
        "tutorial": tutorial,
        "capabilities": capabilities,
        "capability_state_counts": state_counts,
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
        f"interface: {result['interface']['id']} ({result['interface']['display_name']})",
        f"detail: {result['detail']}",
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
