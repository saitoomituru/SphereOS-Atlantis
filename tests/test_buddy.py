from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys
import unittest

from atlantis_cli.buddy import evaluate_buddy_action


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class BuddyActionGateTestCase(unittest.TestCase):
    def test_設計原文付き耳打ちは許可する(self) -> None:
        result = evaluate_buddy_action(
            PROJECT_ROOT,
            {
                "actor_role": "buddy-reviewer",
                "action": "EVIDENCE_WHISPER",
                "architect_source_refs": ["issue://architect/28#comment-1"],
                "transport_capabilities": ["POSIX_PIPE", "SESSION_RESUME"],
            },
        )
        self.assertTrue(result.allowed)
        self.assertEqual(result.code, "BUDDY_NON_CONTROL_ACTION_ALLOWED")

    def test_耳打ち依頼とpipe到達性からprocess停止を導出しない(self) -> None:
        result = evaluate_buddy_action(
            PROJECT_ROOT,
            {
                "actor_role": "buddy-reviewer",
                "action": "PROCESS_INTERRUPT",
                "architect_source_refs": ["issue://architect/28#comment-1"],
                "transport_capabilities": ["POSIX_PIPE", "TTY", "SESSION_RESUME"],
                "reason": "DESIGN_DISAGREEMENT",
            },
        )
        self.assertFalse(result.allowed)
        self.assertTrue(result.user_gate_required)
        self.assertEqual(result.code, "BUDDY_PROCESS_CONTROL_NOT_AUTHORIZED")

    def test_未commit差分とtest失敗はemergency_brakeにならない(self) -> None:
        result = evaluate_buddy_action(
            PROJECT_ROOT,
            {
                "actor_role": "buddy-reviewer",
                "action": "PROCESS_INTERRUPT",
                "emergency_brake": {
                    "class": "UNCOMMITTED_DIFF",
                    "in_flight": True,
                    "evidence_refs": ["git-diff://local"],
                },
            },
        )
        self.assertFalse(result.allowed)

    def test_Userが明示したprocess停止は許可する(self) -> None:
        result = evaluate_buddy_action(
            PROJECT_ROOT,
            {
                "actor_role": "buddy-reviewer",
                "action": "PROCESS_INTERRUPT",
                "user_authorization_ref": "conversation://current/user-order-42",
            },
        )
        self.assertTrue(result.allowed)
        self.assertEqual(result.code, "USER_AUTHORIZED_PROCESS_INTERRUPT")

    def test_秘密漏えい実行中は証拠付き最小停止候補になる(self) -> None:
        result = evaluate_buddy_action(
            PROJECT_ROOT,
            {
                "actor_role": "buddy-reviewer",
                "action": "PROCESS_INTERRUPT",
                "emergency_brake": {
                    "class": "SECRET_DISCLOSURE_IN_FLIGHT",
                    "in_flight": True,
                    "evidence_refs": ["event://stdout-secret-boundary-crossing"],
                },
            },
        )
        self.assertTrue(result.allowed)
        self.assertEqual(result.code, "EMERGENCY_BRAKE_ALLOWED")

    def test_review_challengeには設計原文と問いが必要(self) -> None:
        missing = evaluate_buddy_action(
            PROJECT_ROOT,
            {"actor_role": "buddy-reviewer", "action": "REVIEW_CHALLENGE"},
        )
        self.assertFalse(missing.allowed)
        self.assertEqual(missing.code, "ARCHITECT_SOURCE_REQUIRED")

        result = evaluate_buddy_action(
            PROJECT_ROOT,
            {
                "actor_role": "buddy-reviewer",
                "action": "REVIEW_CHALLENGE",
                "architect_source_refs": ["manifest://samurai-coding"],
                "question_for_coder": "このDiffは設計原文のどの条件を保持していますか？",
            },
        )
        self.assertTrue(result.allowed)

    def test_CLIはrequestを実行せず停止権限を拒否する(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "atlantis_cli",
                "agent",
                "buddy-check",
                "--request",
                "-",
                "--json",
            ],
            cwd=PROJECT_ROOT,
            input=json.dumps(
                {
                    "actor_role": "buddy-reviewer",
                    "action": "PROCESS_INTERRUPT",
                    "transport_capabilities": ["POSIX_PIPE"],
                    "reason": "DESIGN_DISAGREEMENT",
                }
            ),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertFalse(result["allowed"])
        self.assertTrue(result["user_gate_required"])
        self.assertFalse(result["mutations_performed"])


if __name__ == "__main__":
    unittest.main()
