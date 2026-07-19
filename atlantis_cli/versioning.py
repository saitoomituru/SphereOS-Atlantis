"""Sphere三層版数座標とWorld接続境界をoffline検証する。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_json
from .note import find_repo_root


COORDINATE_SYSTEM = "sphere-version-coordinate/1"
CONTRACT_PATH = Path("versioning/contract.json")
SCHEMA_PATH = Path("versioning/schemas/sphere-version-coordinate.schema.json")


def _coordinate(value: object, label: str) -> dict[str, int]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} coordinateがobjectではありません。")
    if value.get("coordinate_system") != COORDINATE_SYSTEM:
        raise ValueError(f"{label} coordinate_systemが未対応です。")
    result: dict[str, int] = {}
    for key in ("presentation", "function", "semantic_kernel"):
        part = value.get(key)
        if not isinstance(part, int) or isinstance(part, bool) or part < 0:
            raise ValueError(f"{label} {key}は0以上の整数である必要があります。")
        result[key] = part
    return result


def coordinate_display(value: object) -> str:
    coordinate = _coordinate(value, "version")
    return ".".join(
        str(coordinate[key])
        for key in ("presentation", "function", "semantic_kernel")
    )


def _endpoint(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} endpointがobjectではありません。")
    coordinate = _coordinate(value.get("coordinate"), label)
    world_config_ref = value.get("world_config_ref")
    capabilities = value.get("capabilities")
    authority_allowed = value.get("authority_allowed")
    if not isinstance(world_config_ref, str) or not world_config_ref:
        raise ValueError(f"{label} world_config_refが必要です。")
    if (
        not isinstance(capabilities, list)
        or any(not isinstance(item, str) or not item for item in capabilities)
        or len(capabilities) != len(set(capabilities))
    ):
        raise ValueError(f"{label} capabilitiesは重複のない文字列arrayである必要があります。")
    if authority_allowed not in {True, False, "unknown"}:
        raise ValueError(f"{label} authority_allowedが不正です。")
    return {
        "coordinate": coordinate,
        "world_config_ref": world_config_ref,
        "capabilities": capabilities,
        "authority_allowed": authority_allowed,
    }


def _valid_causal_gateway(
    value: object,
    source_kernel: int,
    target_kernel: int,
) -> bool:
    if not isinstance(value, dict):
        return False
    return (
        value.get("source_semantic_kernel") == source_kernel
        and value.get("target_semantic_kernel") == target_kernel
        and value.get("projection_only") is True
        and value.get("source_mutation") is False
        and value.get("identity_continuity_inferred") is False
    )


def classify_connection(value: dict[str, Any]) -> dict[str, Any]:
    source = _endpoint(value.get("source"), "source")
    target = _endpoint(value.get("target"), "target")
    source_kernel = source["coordinate"]["semantic_kernel"]
    target_kernel = target["coordinate"]["semantic_kernel"]
    shared = sorted(set(source["capabilities"]) & set(target["capabilities"]))
    authority_known_allowed = (
        source["authority_allowed"] is True
        and target["authority_allowed"] is True
    )

    result: dict[str, Any] = {
        "schema_version": "1.0.0",
        "coordinate_system": COORDINATE_SYSTEM,
        "status": "BOTTOM",
        "same_semantic_kernel": source_kernel == target_kernel,
        "same_world_config": source["world_config_ref"] == target["world_config_ref"],
        "negotiated_capabilities": shared,
        "direct_rendering_allowed": False,
        "portal_required": False,
        "projection_only": False,
        "source_mutation": False,
        "identity_continuity_inferred": False,
        "network_access_performed": False,
        "mutations_performed": False,
        "reasons": [],
    }

    if not authority_known_allowed:
        result["status"] = "UNKNOWN-BLOCKED"
        result["reasons"].append("authority／World Visaが許可済みではありません。")
        return result
    if not shared:
        result["reasons"].append("共通capabilityがありません。")
        return result

    if source_kernel != target_kernel:
        if _valid_causal_gateway(value.get("causal_gateway"), source_kernel, target_kernel):
            result["status"] = "CROSS-CAUSAL-GATE-REQUIRED"
            result["portal_required"] = True
            result["projection_only"] = True
            result["reasons"].append(
                "意味・因果Kernelが異なるため、隔離projectionとlineage receiptが必要です。"
            )
        else:
            result["reasons"].append(
                "意味・因果Kernelが異なり、登録済み因果Gateを確認できません。"
            )
        return result

    if source["world_config_ref"] != target["world_config_ref"]:
        result["status"] = "PORTAL-REQUIRED"
        result["portal_required"] = True
        result["reasons"].append(
            "SemanticKernelは一致しますがWorld Configが異なるためPortal境界が必要です。"
        )
        return result

    result["status"] = "CONTIGUOUS-CANDIDATE"
    result["direct_rendering_allowed"] = True
    result["reasons"].append(
        "SemanticKernelとWorld Configが一致し、共通capabilityとauthorityを確認しました。"
    )
    return result


def validate_version_contract(repo_root: Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    contract = load_json(root / CONTRACT_PATH)
    errors: list[str] = []
    try:
        display = coordinate_display(contract.get("current_coordinate"))
        if display != contract.get("canonical_display"):
            errors.append("current coordinateとcanonical displayが一致しません。")
        if not (root / SCHEMA_PATH).is_file():
            errors.append(f"version coordinate schemaがありません: {SCHEMA_PATH}")
        aliases = contract.get("legacy_aliases")
        if not isinstance(aliases, list) or not aliases:
            errors.append("legacy alias migrationがありません。")
        else:
            values = {item.get("value") for item in aliases if isinstance(item, dict)}
            if {"0.25.1", "0.25.1-alpha.1"} - values:
                errors.append("0.25.1 legacy Source Event mappingが不足しています。")
        fixture_paths = contract.get("connection_fixtures")
        if not isinstance(fixture_paths, list) or not fixture_paths:
            errors.append("connection fixturesがありません。")
        else:
            for relative in fixture_paths:
                fixture = load_json(root / relative)
                actual = classify_connection(fixture)
                if actual["status"] != fixture.get("expected_status"):
                    errors.append(
                        f"{relative}: {actual['status']} != {fixture.get('expected_status')}"
                    )
    except (KeyError, TypeError, ValueError) as error:
        errors.append(str(error))
        display = None
    return {
        "schema_version": "1.0.0",
        "overall": "fail" if errors else "pass",
        "coordinate_system": COORDINATE_SYSTEM,
        "canonical_display": display,
        "errors": errors,
        "network_access_performed": False,
        "mutations_performed": False,
    }


def format_version_report(result: dict[str, Any]) -> str:
    lines = [
        f"overall: {result['overall']}",
        f"coordinate-system: {result['coordinate_system']}",
        f"coordinate: {result.get('canonical_display') or 'unknown'}",
    ]
    lines.extend(f"error: {error}" for error in result.get("errors", []))
    return "\n".join(lines)


def format_connection(result: dict[str, Any]) -> str:
    lines = [
        f"status: {result['status']}",
        f"same-semantic-kernel: {str(result['same_semantic_kernel']).lower()}",
        f"same-world-config: {str(result['same_world_config']).lower()}",
        f"direct-rendering: {str(result['direct_rendering_allowed']).lower()}",
        f"portal-required: {str(result['portal_required']).lower()}",
    ]
    lines.extend(f"reason: {reason}" for reason in result["reasons"])
    return "\n".join(lines)
