"""Independence gate — trace to origin.

Three sources citing one press release is one source. Records are collapsed by
origin_trace (falling back to source_url when no trace is recorded); if the
effective count of distinct origins is below the required number, the claim of
independent corroboration fails. Citation laundering is endemic in market
sizing; tracing provenance chains is tedious work a machine does better than a
tired analyst at 1am.
"""

from __future__ import annotations

from ..models import EvidenceRecord, GateResult


def independence_gate(records: list, required: int = 2) -> GateResult:
    origins = set()
    for r in records:
        origins.add(r.origin_trace or r.source_url)
    effective = len(origins)
    passed = effective >= required
    reasons = (
        []
        if passed
        else [
            f"{len(records)} source(s) collapse to {effective} independent "
            f"origin(s); need {required}"
        ]
    )
    return GateResult("independence", passed, reasons)
