"""Buddyの情報注入と別agentへの制御作用を分離して判定する。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import load_json


BUDDY_ACTION_POLICY = Path("policy/buddy-actions.json")


@dataclass(frozen=True)
class BuddyActionDecision:
    allowed: bool
    code: str
    user_gate_required: bool


def load_buddy_action_policy(root: Path) -> dict[str, Any]:
    return load_json(root / BUDDY_ACTION_POLICY)


def _non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item for item in value)


def evaluate_buddy_action(root: Path, request: dict[str, Any]) -> BuddyActionDecision:
    """Buddy action requestをoffline判定する。

    この関数はsignal送信やsession操作を行わない。呼出側が制御作用の前に使うvalidatorであり、
    全providerへ強制接続済みであることは意味しない。
    """

    policy = load_buddy_action_policy(root)
    action = request.get("action")
    rules = policy.get("actions", {})
    if action not in rules:
        return BuddyActionDecision(False, "BUDDY_ACTION_UNKNOWN", True)

    actor_role = request.get("actor_role")
    if actor_role != "buddy-reviewer":
        return BuddyActionDecision(False, "BUDDY_ROLE_MISMATCH", True)

    rule = rules[action]
    if rule.get("requires_architect_source_refs") and not _non_empty_list(
        request.get("architect_source_refs")
    ):
        return BuddyActionDecision(False, "ARCHITECT_SOURCE_REQUIRED", False)

    if rule.get("requires_question_for_coder") and not isinstance(
        request.get("question_for_coder"), str
    ):
        return BuddyActionDecision(False, "CODER_QUESTION_REQUIRED", False)

    if action == "PROCESS_INTERRUPT":
        if request.get("user_authorization_ref"):
            return BuddyActionDecision(True, "USER_AUTHORIZED_PROCESS_INTERRUPT", False)

        emergency = request.get("emergency_brake")
        emergency_policy = policy["emergency_brake"]
        if isinstance(emergency, dict):
            emergency_class = emergency.get("class")
            in_flight = emergency.get("in_flight") is True
            evidence_present = _non_empty_list(emergency.get("evidence_refs"))
            if (
                emergency_class in emergency_policy["classes"]
                and in_flight
                and evidence_present
            ):
                return BuddyActionDecision(True, "EMERGENCY_BRAKE_ALLOWED", False)
        return BuddyActionDecision(False, "BUDDY_PROCESS_CONTROL_NOT_AUTHORIZED", True)

    authority_fields = {
        "DECISION_SUBSTITUTION": "user_authorization_ref",
        "WORKTREE_MUTATION": "task_authority_ref",
        "REMOTE_PUBLICATION": "publication_authority_ref",
    }
    authority_field = authority_fields.get(action)
    if authority_field and not request.get(authority_field):
        return BuddyActionDecision(False, f"{action}_NOT_AUTHORIZED", True)

    return BuddyActionDecision(True, "BUDDY_NON_CONTROL_ACTION_ALLOWED", False)
