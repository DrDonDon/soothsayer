"""Core data models for Soothsayer.

An EvidenceRecord is immutable and content-addressed: its id is a hash of its
fields, so the store is append-only by construction (same content -> same id).
An Assertion links back to the evidence ids it rests on; that provenance chain
is what the gates check.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Tier(str, Enum):
    """Source tiers. T0 is model memory and is banned outright.

    rank orders evidential strength: T1 (filings/primary) is strongest.
    """

    T0 = "T0"  # model memory — banned
    T1 = "T1"  # filings, regulator data, primary transcripts
    T2 = "T2"  # trade press with a named reporter; disclosed-method analyst notes
    T3 = "T3"  # secondary press, vendor content, blogs

    @property
    def rank(self) -> int:
        return {"T0": 0, "T3": 1, "T2": 2, "T1": 3}[self.value]


def content_hash(text: str) -> str:
    """Stable short hash of raw text (used for source fetch_hash)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _hash_payload(payload: dict) -> str:
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class EvidenceRecord:
    claim: str
    source_url: str
    verbatim_extract: str
    source_tier: Tier
    fetch_date: str            # ISO date the source was fetched this session
    fetch_hash: str            # hash of the fetched source content
    publication_date: Optional[str] = None   # ISO date the source was published
    value: Optional[float] = None             # numeric value the claim carries, if any
    ghost_cell_id: Optional[str] = None       # which pre-registered chart cell this fills
    origin_trace: Optional[str] = None        # canonical origin URL if this is derivative
    id: str = ""               # content hash — computed in __post_init__

    def __post_init__(self) -> None:
        if not self.id:
            # Hash EVERY persisted field (all of to_dict except id). Keep this in
            # sync with to_dict: if the id omitted a stored field, two records
            # that differ only in that field would collide on id, and the store's
            # content-equality immutability check would then raise a false
            # ImmutabilityError on a legitimate write.
            payload = {
                "claim": self.claim,
                "source_url": self.source_url,
                "verbatim_extract": self.verbatim_extract,
                "source_tier": self.source_tier.value,
                "fetch_date": self.fetch_date,
                "fetch_hash": self.fetch_hash,
                "publication_date": self.publication_date,
                "value": self.value,
                "ghost_cell_id": self.ghost_cell_id,
                "origin_trace": self.origin_trace,
            }
            object.__setattr__(self, "id", _hash_payload(payload))

    def to_dict(self) -> dict:
        d = asdict(self)
        d["source_tier"] = self.source_tier.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "EvidenceRecord":
        d = dict(d)
        d["source_tier"] = Tier(d["source_tier"])
        d.pop("id", None)  # recomputed
        return cls(**d)


@dataclass
class Assertion:
    """What we believe, and what it rests on."""

    text: str
    confidence: str = "med"                 # low | med | high
    evidence_ids: list = field(default_factory=list)  # ids of EvidenceRecords
    kills_it: str = ""                       # what would falsify it
    strength: str = "recommendation"         # recommendation | question

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class GateResult:
    gate: str
    passed: bool
    reasons: list = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.passed

    def to_dict(self) -> dict:
        return {"gate": self.gate, "passed": self.passed, "reasons": list(self.reasons)}
