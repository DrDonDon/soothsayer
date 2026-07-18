"""Reconciliation gate — the closest thing strategy has to `npm test`.

Top-down and bottom-up estimates must agree within a stated tolerance; segments
must sum to the total. This runs as arithmetic, not prose, so a sizing that does
not tie fails the build. The tolerance is declared before the answer is known
(in /workplan), not tuned afterwards to make the number pass.
"""

from __future__ import annotations

from ..models import GateResult


def reconcile_gate(
    topdown: float, bottomup: float, tolerance: float = 0.10, label: str = "sizing"
) -> GateResult:
    denom = max(abs(topdown), abs(bottomup)) or 1.0
    diff = abs(topdown - bottomup) / denom
    passed = diff <= tolerance
    reasons = (
        []
        if passed
        else [
            f"{label}: top-down {topdown:g} vs bottom-up {bottomup:g} "
            f"differ by {diff:.1%} (> tolerance {tolerance:.0%})"
        ]
    )
    return GateResult("reconcile", passed, reasons)


def segments_sum_gate(
    total: float, segments: list, tolerance: float = 0.01, label: str = "segments"
) -> GateResult:
    s = sum(segments)
    denom = abs(total) or 1.0
    diff = abs(total - s) / denom
    passed = diff <= tolerance
    reasons = (
        []
        if passed
        else [
            f"{label}: segments sum to {s:g} but total is {total:g} "
            f"({diff:.1%} off, > tolerance {tolerance:.0%})"
        ]
    )
    return GateResult("reconcile_segments", passed, reasons)
