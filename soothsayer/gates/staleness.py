"""Staleness gate — publication date vs decision horizon.

A 2023 penetration rate cannot support a 2026 entry decision. If a source is
older than the allowed age relative to the decision horizon, it fails.
"""

from __future__ import annotations

from datetime import date

from ..models import EvidenceRecord, GateResult


def _parse(d: str) -> date:
    return date.fromisoformat(d)


def staleness_gate(
    record: EvidenceRecord, decision_horizon: str, max_age_days: int = 365
) -> GateResult:
    if not record.publication_date:
        return GateResult(
            "staleness", False, ["no publication_date, so staleness cannot be checked"]
        )
    try:
        age = (_parse(decision_horizon) - _parse(record.publication_date)).days
    except ValueError as exc:
        return GateResult("staleness", False, [f"unparseable date: {exc}"])

    passed = age <= max_age_days
    reasons = (
        []
        if passed
        else [
            f"source dated {record.publication_date} is {age}d before horizon "
            f"{decision_horizon} (> {max_age_days}d allowed)"
        ]
    )
    return GateResult("staleness", passed, reasons)
