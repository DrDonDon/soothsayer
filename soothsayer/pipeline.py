"""Pack-level gate oracle (test layer E).

Runs the full gate stack over the evidence set plus a synthesis, so an
adversarial integration test can feed poisoned sources through and assert that
nothing poisoned or untraceable reaches the pack. The gate engine is the
ground-truth oracle: the model-driven skills are checked against deterministic
gates, not against another model.
"""

from __future__ import annotations

from .artifacts import Synthesis
from .gates import gate_records
from .skillgates import traceability_gate


def gate_pack(
    records: list,
    synthesis: Synthesis,
    fetcher=None,
    decision_horizon=None,
    max_age_days: int = 365,
) -> list:
    """Every evidence gate over the record set, plus traceability of the synthesis."""
    results = gate_records(
        records, fetcher=fetcher, decision_horizon=decision_horizon, max_age_days=max_age_days
    )
    results.append(traceability_gate(synthesis, {r.id for r in records}))
    return results


def pack_is_clean(results: list) -> bool:
    return all(r.passed for r in results)


def failed_gates(results: list) -> list:
    return [r.gate for r in results if not r.passed]
