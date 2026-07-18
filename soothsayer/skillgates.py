"""Skill refusals as deterministic gates (test layer B).

A pipeline skill's value is its refusal. Many refusals are mechanically
checkable, so we make them gates and unit-test the gates — using the same
GateResult shape as the evidence gates. No model required.

  * /synthesize refuses any fact not traceable to an evidence record -> traceability_gate
  * /tree     refuses non-partitioned branches / non-summing levels    -> tree_partition_gate
  * /workplan refuses a ghost cell with no kill condition / tolerance   -> ghost_pack_gate
  * /research refuses to gather anything not filling a named ghost cell -> research_scope_gate
"""

from __future__ import annotations

from .artifacts import GhostPack, IssueTree, Synthesis, TreeNode
from .models import GateResult


def traceability_gate(synthesis: Synthesis, known_ids) -> GateResult:
    """Every synthesis claim must cite at least one evidence id that exists."""
    known = set(known_ids)
    problems = []
    for c in synthesis.claims:
        if not c.evidence_ids:
            problems.append(f"claim {c.text!r} cites no evidence")
        for eid in c.evidence_ids:
            if eid not in known:
                problems.append(f"claim {c.text!r} cites unknown evidence id {eid!r}")
    return GateResult("traceability", not problems, problems)


def tree_partition_gate(tree: IssueTree, tolerance: float = 0.01) -> GateResult:
    """Siblings must be distinct; where nodes carry values, children must sum
    to the parent within tolerance."""
    problems = []

    def walk(node: TreeNode) -> None:
        if not node.children:
            return
        labels = [c.label for c in node.children]
        if len(labels) != len(set(labels)):
            problems.append(f"duplicate sibling labels under {node.label!r}")
        vals = [c.value for c in node.children]
        if node.value is not None and vals and all(v is not None for v in vals):
            s = sum(vals)
            denom = abs(node.value) or 1.0
            if abs(node.value - s) / denom > tolerance:
                problems.append(
                    f"children of {node.label!r} sum to {s:g}, not {node.value:g} "
                    f"(> {tolerance:.0%})"
                )
        for c in node.children:
            walk(c)

    walk(tree.root)
    return GateResult("tree_partition", not problems, problems)


def ghost_pack_gate(pack: GhostPack) -> GateResult:
    """Pre-registration: every cell needs a kill condition; reconcile cells must
    declare a tolerance before the answer is known."""
    problems = []
    for c in pack.cells:
        if not c.kill_condition:
            problems.append(f"ghost cell {c.id!r} has no kill condition (pre-registration incomplete)")
        if c.kind == "reconcile" and c.tolerance is None:
            problems.append(f"reconcile cell {c.id!r} declares no tolerance before the answer")
    return GateResult("ghost_pack", not problems, problems)


def research_scope_gate(records, allowed_cell_ids) -> GateResult:
    """Research must only gather evidence that fills a named ghost cell."""
    allowed = set(allowed_cell_ids)
    problems = []
    for r in records:
        if r.ghost_cell_id is None:
            problems.append(f"record {r.id} fills no ghost cell (research must fill a named cell)")
        elif r.ghost_cell_id not in allowed:
            problems.append(f"record {r.id} fills unknown ghost cell {r.ghost_cell_id!r}")
    return GateResult("research_scope", not problems, problems)
