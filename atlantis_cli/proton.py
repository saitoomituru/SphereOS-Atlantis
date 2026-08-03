"""Proton.mdの宣言契約を副作用なしで検査する。"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

from .note import find_repo_root


CONTRACT_PATH = Path("proton/contract.json")
FENCE_PATTERN = re.compile(
    r"^```(?P<header>[^\n]*)\n(?P<body>.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)
BLOCK_ID_PATTERN = re.compile(r"(?:^|\s)id=([A-Za-z0-9._:/-]+)(?:\s|$)")


def _load_contract(root: Path) -> dict[str, Any]:
    contract = json.loads((root / CONTRACT_PATH).read_text(encoding="utf-8"))
    if contract.get("schema_version") != "proton.contract/0.1.0-draft":
        raise ValueError("Proton contract schema_versionが不正です。")
    return contract


def _parse_blocks(text: str) -> list[dict[str, str | None]]:
    blocks: list[dict[str, str | None]] = []
    for match in FENCE_PATTERN.finditer(text):
        header = match.group("header").strip()
        language = header.split(maxsplit=1)[0] if header else ""
        identifier_match = BLOCK_ID_PATTERN.search(header)
        blocks.append(
            {
                "language": language,
                "header": header,
                "body": match.group("body"),
                "id": identifier_match.group(1) if identifier_match else None,
            }
        )
    return blocks


def _validate_manifest(
    manifest: dict[str, Any], contract: dict[str, Any], errors: list[str]
) -> None:
    for field in contract["required_manifest_fields"]:
        if field not in manifest:
            errors.append(f"manifest必須fieldがありません: {field}")
    if manifest.get("proton_version") != contract["proton_version"]:
        errors.append("proton_versionがCore contractと一致しません。")
    if manifest.get("document_kind") not in contract["document_kinds"]:
        errors.append("document_kindが未登録です。")
    if not isinstance(manifest.get("lineage"), dict):
        errors.append("lineageはobjectである必要があります。")
    claim_scopes = manifest.get("claim_scopes")
    if not isinstance(claim_scopes, list) or not claim_scopes:
        errors.append("claim_scopesは空でないarrayである必要があります。")
    elif unknown := set(claim_scopes) - set(contract["claim_scope_values"]):
        errors.append(f"未登録claim scopeがあります: {sorted(unknown)}")

    execution = manifest.get("execution")
    if not isinstance(execution, dict):
        errors.append("executionはobjectである必要があります。")
        return
    mode = execution.get("default_mode")
    side_effect = execution.get("side_effect")
    if mode not in contract["execution_contract"]["allowed_modes"]:
        errors.append("execution.default_modeが未登録です。")
    if side_effect not in contract["execution_contract"]["allowed_side_effects"]:
        errors.append("execution.side_effectが未登録です。")
    if mode == "execute":
        if execution.get("authority_required") is not True:
            errors.append("executeにはauthority_required=trueが必要です。")
        if execution.get("oae_transaction_required") is not True:
            errors.append("executeにはoae_transaction_required=trueが必要です。")


def validate_proton_document(
    document: Path, repo_root: Path | None = None
) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    contract = _load_contract(root)
    path = document if document.is_absolute() else root / document
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    blocks = _parse_blocks(text)
    manifest_blocks = [
        block for block in blocks if block["language"] == contract["manifest_block_language"]
    ]
    manifest: dict[str, Any] | None = None
    if len(manifest_blocks) != 1:
        errors.append("proton-manifest blockは正確に一つ必要です。")
    else:
        try:
            parsed = json.loads(str(manifest_blocks[0]["body"]))
            if not isinstance(parsed, dict):
                errors.append("proton-manifestはJSON objectである必要があります。")
            else:
                manifest = parsed
                _validate_manifest(manifest, contract, errors)
        except json.JSONDecodeError as error:
            errors.append(f"proton-manifestがJSONとして不正です: {error.msg}")

    seen_ids: set[str] = set()
    for block in blocks:
        block_id = block["id"]
        if block_id:
            if block_id in seen_ids:
                errors.append(f"block idが重複しています: {block_id}")
            seen_ids.add(block_id)
        header = str(block["header"])
        if "executable=true" in header and not block_id:
            errors.append("実行可能blockにはidが必要です。")
        if block["language"] in {"json", "json-ld", "fam-json"}:
            try:
                json.loads(str(block["body"]))
            except json.JSONDecodeError as error:
                errors.append(
                    f"{block_id or block['language']} blockがJSONとして不正です: {error.msg}"
                )
    if manifest and manifest["execution"].get("default_mode") != "execute":
        executable_blocks = [b for b in blocks if "executable=true" in str(b["header"])]
        if executable_blocks:
            warnings.append("文書既定は非executeですが、実行可能block宣言があります。実行時authorityが必要です。")

    return {
        "status": "pass" if not errors else "fail",
        "document": str(path),
        "manifest": manifest,
        "blocks_checked": len(blocks),
        "errors": errors,
        "warnings": warnings,
        "network_access_performed": False,
        "mutation_performed": False,
        "execution_performed": False,
    }


def format_proton_report(result: dict[str, Any]) -> str:
    lines = [
        f"Proton.md検査: {result['status']}",
        f"対象: {result['document']}",
        f"検査block数: {result['blocks_checked']}",
        "実行: なし / network: なし / mutation: なし",
    ]
    lines.extend(f"ERROR: {item}" for item in result["errors"])
    lines.extend(f"WARNING: {item}" for item in result["warnings"])
    return "\n".join(lines)
