"""T0 gate — the load-bearing one.

No number enters the store from model memory (T0), and every numeric claim must
carry fetched provenance (a source_url and a fetch_hash). A plausible market
figure surfacing from training data is the single most likely route to
confident garbage, so this fails the build rather than labelling it.
"""

from __future__ import annotations

from ..models import EvidenceRecord, GateResult, Tier


def t0_gate(record: EvidenceRecord) -> GateResult:
    reasons = []
    if record.source_tier == Tier.T0:
        reasons.append(f"T0 (model memory) is banned: {record.claim!r}")
    if record.value is not None and (not record.source_url or not record.fetch_hash):
        reasons.append(
            f"numeric claim carries no fetched provenance "
            f"(needs source_url + fetch_hash): {record.claim!r}"
        )
    return GateResult("t0", not reasons, reasons)
