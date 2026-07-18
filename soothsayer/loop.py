"""The /analyze <-> /inhouse review loop.

Guards TWO failure modes, not one:

  * deadlock (the rare case) -> status ESCALATE. If objections stay unresolved
    after max_rounds, a human decides. A hung jury is not a gate pass.

  * false convergence (the COMMON case with a single model) -> status
    UNDER_REVIEWED. A reviewer that agrees too easily is suspect: an assertion
    may pass ONLY if it survived at least `floor` substantive objections that
    were raised and then addressed. Zero objections is not confidence, it is an
    unexercised gate.

Only CONVERGED means the assertion earned its place in the pack.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import Assertion
from .modelclient import ModelClient, Review

CONVERGED = "converged"
ESCALATE = "escalate"
UNDER_REVIEWED = "under_reviewed"


@dataclass
class LoopResult:
    status: str
    assertion: Assertion
    objections_seen: int = 0
    rounds: int = 0
    trace: list = field(default_factory=list)  # human-readable per-round log


def run_review_loop(
    assertion: Assertion,
    evidence: list,
    model: ModelClient,
    floor: int = 1,
    max_rounds: int = 3,
) -> LoopResult:
    objections_seen = 0
    trace: list = []
    last_had_objections = False

    for rnd in range(1, max_rounds + 1):
        review: Review = model.review(assertion, evidence)
        n = len(review.objections)
        last_had_objections = n > 0

        if n:
            objections_seen += n
            trace.append(f"round {rnd}: {n} objection(s) -> revise")
            assertion = model.revise(assertion, review.objections)
            continue

        # No objections this round.
        if objections_seen >= floor:
            trace.append(f"round {rnd}: clean, survived {objections_seen} objection(s)")
            return LoopResult(CONVERGED, assertion, objections_seen, rnd, trace)
        # Suspiciously fast agreement: floor not met. Force another skeptical pass.
        trace.append(
            f"round {rnd}: clean but only {objections_seen}/{floor} objections seen "
            f"-> disagreement-floor not met, re-review"
        )

    # rounds exhausted
    if last_had_objections:
        trace.append("max rounds reached with unresolved objections -> escalate")
        return LoopResult(ESCALATE, assertion, objections_seen, max_rounds, trace)
    trace.append("max rounds reached, disagreement-floor never met -> under-reviewed")
    return LoopResult(UNDER_REVIEWED, assertion, objections_seen, max_rounds, trace)
