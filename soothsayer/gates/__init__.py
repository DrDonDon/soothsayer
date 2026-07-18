"""The gate engine — the one part of Soothsayer that is not gstack.

Each gate is a pure function: records (or numbers) in, a GateResult out. Nothing
here calls a model. These prove the work is not sloppy or laundered; they do not
claim it is true.
"""

from __future__ import annotations

from ..models import Assertion, EvidenceRecord, GateResult
from .citation import Fetcher, FrozenFetcher, SourceFetchError, citation_gate, content_hash
from .independence import independence_gate
from .reconcile import reconcile_gate, segments_sum_gate
from .staleness import staleness_gate
from .t0 import t0_gate
from .tier_floor import tier_floor_gate

__all__ = [
    "t0_gate",
    "reconcile_gate",
    "segments_sum_gate",
    "citation_gate",
    "staleness_gate",
    "independence_gate",
    "tier_floor_gate",
    "content_hash",
    "Fetcher",
    "FrozenFetcher",
    "SourceFetchError",
    "gate_records",
]


def gate_records(
    records: list,
    fetcher: Fetcher | None = None,
    decision_horizon: str | None = None,
    max_age_days: int = 365,
) -> list:
    """Run every per-record gate that applies, plus independence across the set.

    Returns a flat list of GateResult. A record with no publication_date is not
    failed for staleness unless a decision_horizon is supplied.
    """
    results: list = []
    for r in records:
        results.append(t0_gate(r))
        if fetcher is not None:
            results.append(citation_gate(r, fetcher))
        if decision_horizon is not None:
            results.append(staleness_gate(r, decision_horizon, max_age_days))
    if records:
        results.append(independence_gate(records))
    return results
