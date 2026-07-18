"""Model client — a thin, pluggable interface with a deterministic mock.

v0.1 never calls a live model. The loop depends only on this protocol, so it is
fully testable offline. A real Anthropic-backed client is sketched at the bottom
and imported lazily, so the package has zero hard dependencies.

Note on isolation: the reviewer (`/inhouse`) is given only the assertion and its
evidence, never the author's reasoning trace. In v0.1 that isolation is enforced
by the call shape (we pass exactly those two things); the production build runs
it as a separate process (see TODOS: real process isolation).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .models import Assertion


@dataclass
class Review:
    objections: list = field(default_factory=list)  # substantive objections raised
    note: str = ""


class ModelClient(Protocol):
    def review(self, assertion: Assertion, evidence: list) -> Review:
        """Trace-starved review: sees only the assertion and its evidence."""

    def revise(self, assertion: Assertion, objections: list) -> Assertion:
        """Produce a revised assertion that addresses the objections."""


class MockModel:
    """Scripted reviewer for tests and the demo.

    `scripted` is a list of Review objects, returned one per review() call. When
    exhausted, returns an empty Review (no objections). `revise` just annotates
    the assertion text so successive rounds are distinguishable.
    """

    def __init__(self, scripted: list | None = None):
        self._scripted = list(scripted or [])
        self._i = 0

    def review(self, assertion: Assertion, evidence: list) -> Review:
        if self._i < len(self._scripted):
            r = self._scripted[self._i]
            self._i += 1
            return r
        return Review(objections=[])

    def revise(self, assertion: Assertion, objections: list) -> Assertion:
        return Assertion(
            text=assertion.text + f" [revised: addressed {len(objections)} objection(s)]",
            confidence=assertion.confidence,
            evidence_ids=list(assertion.evidence_ids),
            kills_it=assertion.kills_it,
            strength=assertion.strength,
        )


def anthropic_client(model: str = "claude-sonnet-5"):  # pragma: no cover
    """Lazily construct a real client. Not exercised in v0.1 tests."""
    raise NotImplementedError(
        "Live model client is not part of v0.1. Wire the Anthropic SDK here, "
        "keeping review() trace-starved (assertion + evidence only)."
    )
