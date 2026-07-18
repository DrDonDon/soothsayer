"""Injection gate — fail loud on planted instructions in a source.

Re-fetches the source and scans it for instruction-injection patterns. Flagged
content is quarantined: it fails the gate rather than silently supporting a
claim. This closes the hole provenance cannot: a source can be real and dated and
still be trying to steer you.
"""

from __future__ import annotations

from ..ingest import detect_injection
from ..models import EvidenceRecord, GateResult
from .citation import Fetcher


def injection_gate(record: EvidenceRecord, fetcher: Fetcher) -> GateResult:
    try:
        content = fetcher.fetch(record.source_url)
    except Exception as exc:
        return GateResult("injection", False, [f"re-fetch failed: {exc}"])

    hits = detect_injection(content)
    if hits:
        return GateResult(
            "injection",
            False,
            [f"source contains instruction-injection patterns: {', '.join(hits)}"],
        )
    return GateResult("injection", True, [])
