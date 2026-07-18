"""Citation gate — re-fetch and re-extract.

Every cited source is fetched again; the content must still hash to what was
recorded, and the verbatim extract must still be present. A number that quietly
changed, or a quote that vanished, fails the build. Fetching goes through a
Fetcher so the gate is testable offline against a frozen source set (which is
also how a real backtest would pin sources).
"""

from __future__ import annotations

import hashlib
from typing import Protocol

from ..models import EvidenceRecord, GateResult


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class SourceFetchError(Exception):
    pass


class Fetcher(Protocol):
    def fetch(self, url: str) -> str: ...


class FrozenFetcher:
    """Serves source text from an in-memory (or on-disk) frozen mapping."""

    def __init__(self, mapping: dict):
        self._mapping = dict(mapping)

    def fetch(self, url: str) -> str:
        if url not in self._mapping:
            raise SourceFetchError(f"no frozen source for {url}")
        return self._mapping[url]


def citation_gate(record: EvidenceRecord, fetcher: Fetcher) -> GateResult:
    reasons = []
    try:
        content = fetcher.fetch(record.source_url)
    except Exception as exc:  # fetch failure is a gate failure, never silent
        return GateResult("citation", False, [f"re-fetch failed: {exc}"])

    if content_hash(content) != record.fetch_hash:
        reasons.append("source content changed since citation (hash mismatch)")
    if record.verbatim_extract and record.verbatim_extract not in content:
        reasons.append("verbatim extract no longer present in the source")
    return GateResult("citation", not reasons, reasons)
