#!/usr/bin/env python3
"""MAGI 0.2.1のOAE時間receiptを検証し、同一世界線への遡及生成を拒否する。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


MAGI_ROOT = Path(__file__).resolve().parent
POLICY_PATH = MAGI_ROOT / "oae-temporal-policy.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON rootはobjectである必要があります。")
    return value


def require_string(value: dict[str, Any], key: str, errors: list[str]) -> None:
    if not isinstance(value.get(key), str) or not value[key].strip():
        errors.append(f"{key}は空でない文字列である必要があります。")


def validate(value: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if value.get("version") != "0.2.1":
        errors.append("versionは0.2.1である必要があります。")

    mode = value.get("observation_mode")
    if mode not in policy["allowed_observation_modes"]:
        errors.append("observation_modeが0.2.1 policyにありません。")
    require_string(value, "observed_at", errors)

    historical_status = value.get("historical_oae_status")
    if historical_status not in policy["historical_oae_statuses"]:
        errors.append("historical_oae_statusが0.2.1 policyにありません。")

    if value.get("retroactive_backfill") is not False:
        errors.append("retroactive_backfillはfalseである必要があります。")
    if value.get("same_worldline_mutation") is not False:
        errors.append("same_worldline_mutationはfalseである必要があります。")
    if value.get("claims_physical_time_travel") is not False:
        errors.append("物理空間の時間移動を主張してはいけません。")

    historical_ref = value.get("historical_oae_ref")
    role_attribution = value.get("historical_role_attribution", "none")
    if historical_status == "referenced":
        require_string(value, "historical_oae_ref", errors)
    elif historical_ref not in (None, ""):
        errors.append("同時点OAEが未確認のときhistorical_oae_refを生成してはいけません。")

    if role_attribution != "none" and historical_status != "referenced":
        errors.append("同時点OAE参照なしに過去のAgency roleを帰属してはいけません。")

    historical_modes = {"current-interpretation-of-history", "counterfactual-branch"}
    if mode in historical_modes:
        if historical_status not in ("referenced", "historical-oae-unavailable"):
            errors.append("過去資料を扱うmodeにはhistorical OAE状態が必要です。")
        if historical_status == "historical-oae-unavailable":
            last_order = value.get("last_order")
            expected = policy["last_order"]
            if not isinstance(last_order, dict):
                errors.append("historical OAE不明時はLast Orderが必要です。")
            elif (
                last_order.get("code") != expected["code"]
                or last_order.get("action") != expected["action"]
            ):
                errors.append("Last OrderがOAE-HISTORY-UNKNOWN契約と一致しません。")

    if mode == "contemporaneous-oae-reference" and historical_status != "referenced":
        errors.append("contemporaneous-oae-referenceには同時点OAE参照が必要です。")

    if mode == "counterfactual-branch":
        branch = value.get("branch_receipt")
        if not isinstance(branch, dict):
            errors.append("counterfactual-branchにはbranch_receiptが必要です。")
        else:
            for key in (
                "source_world_ref",
                "source_instance_ghost_ref",
                "target_world_ref",
                "target_instance_ghost_ref",
                "fork_point_ref",
                "provenance_ref",
            ):
                require_string(branch, key, errors)
            requirements = policy["branch_requirements"]
            if branch.get("profile_ref") != requirements["profile_ref"]:
                errors.append("branch profileはAkasha Driver 7D Foldである必要があります。")
            if branch.get("source_mutation") is not False:
                errors.append("Source World／Instance Ghostを変更してはいけません。")
            if branch.get("status") != "hypothetical":
                errors.append("反実仮想branchはhypotheticalである必要があります。")
            if branch.get("source_world_ref") == branch.get("target_world_ref"):
                errors.append("Target WorldはSource Worldからsplitする必要があります。")
            if branch.get("source_instance_ghost_ref") == branch.get("target_instance_ghost_ref"):
                errors.append("Target Instance GhostはSource Instance Ghostからsplitする必要があります。")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="-", help="receipt JSON。既定はstdin。")
    args = parser.parse_args(argv)
    try:
        policy = load_json(POLICY_PATH)
        if args.input == "-":
            value = json.load(sys.stdin)
            if not isinstance(value, dict):
                raise ValueError("JSON rootはobjectである必要があります。")
        else:
            value = load_json(Path(args.input))
        errors = validate(value, policy)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"valid": False, "errors": [str(error)]}, ensure_ascii=False, indent=2))
        return 2

    print(
        json.dumps(
            {
                "valid": not errors,
                "policy_id": policy["policy_id"],
                "errors": errors,
                "mutations_performed": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
