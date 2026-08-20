"""疑似transaction fixtureをdecision envelopeへ評価する。

acceptedでも実Effectは適用しない。`effect_applied`は常にfalseである。
これは正式OAE Schemaではない。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import FixtureError
from .store import append_receipt, resolve_within_root, validate_identifier

_LEASE_HELD_STATES = {"held", "active"}
_REQUIRED_FIXTURE_MARKERS = {
    "harness_only": True,
    "canonical_contract": False,
    "authority": "none",
}


def _require_markers(fixture: dict[str, Any]) -> None:
    for key, expected in _REQUIRED_FIXTURE_MARKERS.items():
        if fixture.get(key) != expected:
            raise FixtureError(
                f"fixtureの{key}は{expected!r}である必要があります: {fixture.get(key)!r}"
            )


def _requested_paths(fixture: dict[str, Any]) -> list[str]:
    requested = fixture.get("requested_paths") or []
    if not isinstance(requested, list):
        raise FixtureError("requested_pathsはlistである必要があります。")
    return [str(item) for item in requested]


def _envelope(
    fixture: dict[str, Any],
    *,
    decision: str,
    reason_code: str,
    unknown: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": "0.1-harness",
        "harness_only": True,
        "canonical_contract": False,
        "authority": "none",
        "decision": decision,
        "reason_code": reason_code,
        "effect_applied": False,
        "world": {"world_ref": fixture.get("world_ref", "unknown")},
        "fold": {"fold_ref": fixture.get("fold_ref", "unknown")},
        "task": {
            "task_id": fixture.get("task_id", "unknown"),
            "base_revision": fixture.get("base_revision"),
            "observed_revision": fixture.get("observed_revision"),
        },
        "lease": {
            "lease_id": fixture.get("lease_id"),
            "lease_state": fixture.get("lease_state", "unknown"),
        },
        "provider": {
            "provider_process_state": fixture.get("provider_process_state", "unknown"),
            "provider_control_state": fixture.get("provider_control_state", "unknown"),
        },
        "oae": {
            "oae_transaction_state": fixture.get("oae_transaction_state", "unknown"),
        },
        "receipt": {},
        "unknown": unknown or list(fixture.get("unknown") or []),
        "provenance": fixture.get("provenance", {}),
    }


def evaluate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    """疑似transaction fixtureをdecision envelopeへ評価する。acceptedでもEffectを適用しない。"""

    if not isinstance(fixture, dict):
        raise FixtureError("fixtureはobjectである必要があります。")
    _require_markers(fixture)

    task_id = fixture.get("task_id")
    if task_id is not None:
        validate_identifier(task_id, "task_id")

    write_set = fixture.get("write_set") or []
    if not isinstance(write_set, list):
        raise FixtureError("write_setはlistである必要があります。")
    requested_paths = _requested_paths(fixture)

    lease_id = fixture.get("lease_id")
    lease_state = fixture.get("lease_state")
    wants_write = bool(write_set) or bool(requested_paths)

    if wants_write and (not lease_id or lease_state not in _LEASE_HELD_STATES):
        return _envelope(fixture, decision="rejected", reason_code="lease-missing")

    base_revision = fixture.get("base_revision")
    observed_revision = fixture.get("observed_revision")
    if base_revision is not None and observed_revision is not None:
        if base_revision != observed_revision:
            return _envelope(fixture, decision="rejected", reason_code="stale-base-revision")

    out_of_scope = [path for path in requested_paths if path not in write_set]
    if requested_paths and out_of_scope:
        return _envelope(fixture, decision="rejected", reason_code="write-set-violation")

    artifact_claims = fixture.get("artifact_claims") or []
    if not isinstance(artifact_claims, list):
        raise FixtureError("artifact_claimsはlistである必要があります。")
    for claim in artifact_claims:
        if isinstance(claim, dict) and claim.get("conflicts_with_task"):
            return _envelope(
                fixture, decision="rejected", reason_code="duplicate-artifact-claim"
            )

    provider_state = fixture.get("provider_process_state")
    exit_code = fixture.get("provider_exit_code")
    oae_state = fixture.get("oae_transaction_state")
    if provider_state == "exited" and exit_code == 0 and oae_state != "committed":
        # provider exit 0 != OAE commit。自動commitへ変換しない。
        return _envelope(
            fixture,
            decision="suspended",
            reason_code="provider-exit-zero-not-commit",
        )

    return _envelope(fixture, decision="accepted", reason_code="preconditions-satisfied")


def evaluate_and_record(
    fixture: dict[str, Any],
    root: Path,
    receipt_path: Path,
) -> dict[str, Any]:
    envelope = evaluate_fixture(fixture)
    resolve_within_root(root, receipt_path.relative_to(root))
    append_receipt(receipt_path, root, envelope)
    return envelope
