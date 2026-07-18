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

import json
from dataclasses import dataclass, field
from typing import Protocol

from .models import Assertion


class ReviewerUnavailable(Exception):
    """The reviewer model could not be reached. The loop hard-blocks, never
    ships an un-reviewed assertion silently."""


@dataclass
class Review:
    objections: list = field(default_factory=list)  # substantive objections raised
    note: str = ""


class ModelClient(Protocol):
    name: str

    def review(self, assertion: Assertion, evidence: list) -> Review:
        """Trace-starved review: sees only the assertion and its evidence."""

    def revise(self, assertion: Assertion, objections: list) -> Assertion:
        """Produce a revised assertion that addresses the objections."""


@dataclass
class ClientPair:
    """Author + reviewer, with model diversity enforced.

    A reviewer on the same model as the author is phrasing-independent but not
    error-independent: it shares blind spots and rubber-stamps correlated
    mistakes. This refuses that configuration unless explicitly overridden.
    """

    author: object
    reviewer: object
    allow_same_model: bool = False

    def __post_init__(self) -> None:
        an = getattr(self.author, "name", None)
        rn = getattr(self.reviewer, "name", None)
        if not self.allow_same_model and an is not None and an == rn:
            raise ValueError(
                f"author and reviewer both use model {an!r}; model diversity is "
                f"required for real error-independence. Set allow_same_model=True "
                f"to override (not recommended)."
            )


class MockModel:
    """Scripted reviewer for tests and the demo.

    `scripted` is a list of Review objects, returned one per review() call. When
    exhausted, returns an empty Review (no objections). `revise` just annotates
    the assertion text so successive rounds are distinguishable. Pass `fail=True`
    to simulate an unavailable provider (raises ReviewerUnavailable).
    """

    def __init__(self, scripted: list | None = None, name: str = "mock", fail: bool = False):
        self._scripted = list(scripted or [])
        self._i = 0
        self.name = name
        self._fail = fail

    def review(self, assertion: Assertion, evidence: list) -> Review:
        if self._fail:
            raise ReviewerUnavailable(f"model {self.name!r} unavailable")
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

    @classmethod
    def from_cassette(cls, path: str, name: str = "replay") -> "MockModel":
        """Replay recorded model responses (test layer C).

        A cassette is JSON: {"name": "...", "reviews": [{"objections": [...]}, ...]}.
        Recording a real transcript once and replaying it keeps the full skill
        orchestration testable in CI — deterministic, no live calls, no flakiness.
        """
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        reviews = [
            Review(objections=list(r.get("objections", [])), note=r.get("note", ""))
            for r in data.get("reviews", [])
        ]
        return cls(scripted=reviews, name=data.get("name", name))


def anthropic_client(model: str = "claude-sonnet-5"):  # pragma: no cover
    """Lazily construct a real client. Not exercised in v0.1 tests."""
    raise NotImplementedError(
        "Live model client is not part of v0.1. Wire the Anthropic SDK here, "
        "keeping review() trace-starved (assertion + evidence only)."
    )
