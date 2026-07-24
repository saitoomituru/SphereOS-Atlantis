"""明示されたasset lineage receiptを権利審判せずoffline検査する。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_json
from .note import find_repo_root


CONTRACT_PATH = Path("lineage/contract.json")
FORBIDDEN_SECRET_KEYS = {
    "api_key",
    "access_token",
    "auth_token",
    "credential",
    "password",
    "private_key",
    "secret",
    "secret_value",
    "token",
}
REQUIRED_CLAIM_KEYS = {
    "identity",
    "authority",
    "api_capability",
    "official_partnership",
    "religious_representation",
    "rights_verdict",
}
REQUIRED_ASSET_KEYS = {
    "asset_id",
    "author",
    "source_refs",
    "revision",
    "scope_ref",
    "declared_license",
    "reference_kind",
    "designation",
    "distribution",
    "public_manifest_presence",
}


def _string(value: object, label: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}は空でない文字列である必要があります。")
        return None
    return value


def _forbidden_secret_paths(value: object, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key.lower() in FORBIDDEN_SECRET_KEYS:
                found.append(child_path)
            found.extend(_forbidden_secret_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_forbidden_secret_paths(child, f"{path}[{index}]"))
    return found


def load_lineage_contract(root: Path) -> dict[str, Any]:
    contract = load_json(root / CONTRACT_PATH)
    if contract.get("schema_version") != "1.0.0":
        raise ValueError("lineage contract schema_versionは1.0.0である必要があります。")
    if contract.get("receipt_version") != "1.0.0":
        raise ValueError("lineage receipt_versionは1.0.0である必要があります。")
    if contract.get("default_mode") != "open-gift-commons-non-exclusive":
        raise ValueError("lineage default modeがgift commonsではありません。")

    non_inference = contract.get("non_inference")
    if not isinstance(non_inference, dict) or any(
        value is not False for value in non_inference.values()
    ):
        raise ValueError("lineage非推定契約は全項目falseである必要があります。")

    boundary = contract.get("implementation_boundary")
    required_boundary = {
        "explicit_receipt_only": True,
        "implicit_repository_scan": False,
        "asset_auto_mount": False,
        "pointer_config": "NOT_IMPLEMENTED",
        "rights_adjudication": "NOT_IMPLEMENTED",
        "network_access": False,
        "mutation": False,
    }
    if not isinstance(boundary, dict) or any(
        boundary.get(key) != expected for key, expected in required_boundary.items()
    ):
        raise ValueError("lineage implementation boundaryが不正です。")
    return contract


def validate_lineage_receipt(
    value: object,
    contract: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return {
            "schema_version": "1.0.0",
            "status": "BLOCK",
            "errors": ["receiptはobjectである必要があります。"],
            "rights_adjudication_performed": False,
            "network_access_performed": False,
            "mutations_performed": False,
            "implicit_repository_scan_performed": False,
        }

    if value.get("receipt_version") != contract["receipt_version"]:
        errors.append("receipt_versionがcontractと一致しません。")

    asset = value.get("asset")
    if not isinstance(asset, dict):
        errors.append("asset metadataが必要です。")
        asset = {}
    missing_asset_keys = sorted(REQUIRED_ASSET_KEYS - set(asset))
    if missing_asset_keys:
        errors.append(f"asset metadataが不足しています: {', '.join(missing_asset_keys)}")

    for key in (
        "asset_id",
        "author",
        "revision",
        "scope_ref",
        "declared_license",
    ):
        _string(asset.get(key), f"asset.{key}", errors)

    source_refs = asset.get("source_refs")
    if (
        not isinstance(source_refs, list)
        or not source_refs
        or any(not isinstance(item, str) or not item.strip() for item in source_refs)
    ):
        errors.append("asset.source_refsは空でない文字列arrayである必要があります。")

    enum_contracts = {
        "reference_kind": "reference_kinds",
        "designation": "designations",
        "distribution": "distribution_states",
    }
    for asset_key, contract_key in enum_contracts.items():
        if asset.get(asset_key) not in contract[contract_key]:
            errors.append(f"asset.{asset_key}が未登録です。")

    presence = asset.get("public_manifest_presence")
    if presence not in {"declared", "not-required"}:
        errors.append("asset.public_manifest_presenceが不正です。")
    if asset.get("distribution") in {"local-only", "private"}:
        if presence != "not-required":
            errors.append("local-only／private assetをpublic Manifest必須にできません。")
    elif presence != "declared":
        errors.append("public／selected-world assetは公開宣言状態を明示してください。")

    edges = value.get("lineage_edges")
    if not isinstance(edges, list):
        errors.append("lineage_edgesはarrayである必要があります。")
        edges = []
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"lineage_edges[{index}]はobjectである必要があります。")
            continue
        if edge.get("relation") not in contract["relation_types"]:
            errors.append(f"lineage_edges[{index}].relationが未登録です。")
        if edge.get("dimension") not in contract["lineage_dimensions"]:
            errors.append(f"lineage_edges[{index}].dimensionが未登録です。")
        for key in ("source_ref", "observer_ref", "claim_scope_ref"):
            _string(edge.get(key), f"lineage_edges[{index}].{key}", errors)

    claims = value.get("claims")
    if not isinstance(claims, dict):
        errors.append("claims objectが必要です。")
        claims = {}
    missing_claim_keys = sorted(REQUIRED_CLAIM_KEYS - set(claims))
    if missing_claim_keys:
        errors.append(f"claimsが不足しています: {', '.join(missing_claim_keys)}")
    for key in sorted(REQUIRED_CLAIM_KEYS):
        if claims.get(key) is not False:
            errors.append(f"Role／lineageからclaims.{key}を生成できません。")
    if value.get("rights_adjudication_performed") is not False:
        errors.append("lineage validatorはrights verdictを実行できません。")

    extension = value.get("extension")
    if not isinstance(extension, dict):
        errors.append("extension boundaryが必要です。")
        extension = {}
    if extension.get("scope") not in contract["extension_scopes"]:
        errors.append("extension.scopeが未登録です。")
    if extension.get("proprietary") not in {True, False}:
        errors.append("extension.proprietaryはbooleanである必要があります。")
    if extension.get("proprietary") is True and extension.get("scope") == "open-core":
        errors.append("proprietary scopeをopen-coreへ設定できません。")
    for key in (
        "propagates_to_core",
        "captures_existing_commons",
        "captures_unrelated_worlds",
    ):
        if extension.get(key) is not False:
            errors.append(f"extension.{key}はfalseである必要があります。")
    secret_ref = extension.get("secret_ref")
    if secret_ref is not None and (
        not isinstance(secret_ref, str) or not secret_ref.startswith("secret://")
    ):
        errors.append("secretは値でなくsecret://外部参照として宣言してください。")

    secret_paths = _forbidden_secret_paths(value)
    if secret_paths:
        errors.append(f"生secret候補fieldを含められません: {', '.join(secret_paths)}")

    routing = value.get("routing")
    if not isinstance(routing, dict):
        errors.append("routing recovery boundaryが必要です。")
        routing = {}
    for key in ("unmount", "replacement", "fork", "alternate_world"):
        _string(routing.get(key), f"routing.{key}", errors)

    conflict = value.get("conflict")
    if not isinstance(conflict, dict):
        errors.append("conflict boundaryが必要です。")
        conflict = {}
    state = conflict.get("state")
    stop_scope = conflict.get("stop_scope")
    if state not in {"none", "semantic-stop"}:
        errors.append("conflict.stateが不正です。")
    if stop_scope not in contract["conflict_boundary"]["asset_conflict_stop_scopes"]:
        errors.append("asset conflictからglobal stopを生成できません。")
    if state == "none" and stop_scope != "none":
        errors.append("競合なしの場合stop_scopeはnoneです。")
    if state == "semantic-stop" and stop_scope != "selected-route":
        errors.append("asset Semantic Stopはselected-routeへ局所化してください。")

    return {
        "schema_version": "1.0.0",
        "status": "BLOCK" if errors else "PASS",
        "asset_id": asset.get("asset_id"),
        "distribution": asset.get("distribution"),
        "errors": errors,
        "rights_adjudication_performed": False,
        "network_access_performed": False,
        "mutations_performed": False,
        "implicit_repository_scan_performed": False,
    }


def inspect_lineage_receipt(
    receipt_path: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    contract = load_lineage_contract(root)
    receipt = load_json(receipt_path)
    result = validate_lineage_receipt(receipt, contract)
    result["receipt_path"] = str(receipt_path)
    return result


def validate_lineage_contract(repo_root: Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    errors: list[str] = []
    fixture_results: list[dict[str, Any]] = []
    try:
        contract = load_lineage_contract(root)
        fixture_paths = contract.get("fixtures")
        if not isinstance(fixture_paths, list) or not fixture_paths:
            errors.append("lineage fixturesがありません。")
            fixture_paths = []
        for relative in fixture_paths:
            if not isinstance(relative, str):
                errors.append("fixture pathは文字列である必要があります。")
                continue
            fixture = load_json(root / relative)
            actual = validate_lineage_receipt(fixture, contract)
            expected = fixture.get("expected_status")
            fixture_results.append(
                {
                    "path": relative,
                    "expected": expected,
                    "actual": actual["status"],
                    "errors": actual["errors"],
                }
            )
            if actual["status"] != expected:
                errors.append(f"{relative}: {actual['status']} != {expected}")
    except (KeyError, TypeError, ValueError) as error:
        errors.append(str(error))

    return {
        "schema_version": "1.0.0",
        "overall": "fail" if errors else "pass",
        "contract": str(CONTRACT_PATH),
        "fixture_count": len(fixture_results),
        "fixtures": fixture_results,
        "errors": errors,
        "rights_adjudication_performed": False,
        "network_access_performed": False,
        "mutations_performed": False,
        "implicit_repository_scan_performed": False,
    }


def format_lineage_report(result: dict[str, Any]) -> str:
    lines = [
        f"status: {result.get('status', result.get('overall', 'unknown'))}",
        f"rights-adjudication: {str(result['rights_adjudication_performed']).lower()}",
        f"network-access: {str(result['network_access_performed']).lower()}",
        f"mutation: {str(result['mutations_performed']).lower()}",
        f"implicit-repository-scan: {str(result['implicit_repository_scan_performed']).lower()}",
    ]
    if "fixture_count" in result:
        lines.append(f"fixtures: {result['fixture_count']}")
    if result.get("asset_id"):
        lines.append(f"asset: {result['asset_id']}")
    lines.extend(f"error: {error}" for error in result.get("errors", []))
    return "\n".join(lines)
