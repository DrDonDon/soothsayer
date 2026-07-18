"""Tier-floor gate — a finding resting only on T3 cannot support a recommendation.

It can support a question. This keeps thin evidence from carrying decision weight.
"""

from __future__ import annotations

from ..models import Assertion, EvidenceRecord, GateResult, Tier


def tier_floor_gate(assertion: Assertion, records_by_id: dict) -> GateResult:
    recs = [records_by_id[i] for i in assertion.evidence_ids if i in records_by_id]
    best_rank = max((r.source_tier.rank for r in recs), default=0)

    if assertion.strength == "recommendation" and best_rank < Tier.T2.rank:
        best = _rank_name(best_rank)
        return GateResult(
            "tier_floor",
            False,
            [
                f"recommendation rests only on {best} evidence (below T2); "
                f"it can support a question, not a recommendation"
            ],
        )
    return GateResult("tier_floor", True, [])


def _rank_name(rank: int) -> str:
    return {0: "no/T0", 1: "T3", 2: "T2", 3: "T1"}.get(rank, f"rank{rank}")
