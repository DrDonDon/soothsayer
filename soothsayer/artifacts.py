"""Skill output artifacts and their contract validators (test layer A).

Each pipeline skill emits a structured artifact. These dataclasses parse it and
`validate()` checks it conforms to the contract — deterministically, no model.
The refusals that are ALSO mechanically checkable live in skillgates.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IgnoranceMap:
    """/scan output: known / contested / unknown."""

    known: list = field(default_factory=list)
    contested: list = field(default_factory=list)
    unknown: list = field(default_factory=list)

    def validate(self) -> list:
        problems = []
        for name in ("known", "contested", "unknown"):
            if not isinstance(getattr(self, name), list):
                problems.append(f"{name} must be a list")
        # A term must not sit in two buckets at once.
        seen = {}
        for bucket in ("known", "contested", "unknown"):
            for term in getattr(self, bucket):
                if term in seen:
                    problems.append(f"term {term!r} appears in both {seen[term]} and {bucket}")
                seen[term] = bucket
        # /scan refuses to narrow: an empty unknown bucket suggests it did.
        if isinstance(self.unknown, list) and not self.unknown:
            problems.append("scan produced no unknowns — did it narrow prematurely?")
        return problems

    @classmethod
    def from_dict(cls, d: dict) -> "IgnoranceMap":
        return cls(
            known=list(d.get("known", [])),
            contested=list(d.get("contested", [])),
            unknown=list(d.get("unknown", [])),
        )


@dataclass
class TreeNode:
    label: str
    value: Optional[float] = None
    children: list = field(default_factory=list)  # list[TreeNode]

    @classmethod
    def from_dict(cls, d: dict) -> "TreeNode":
        return cls(
            label=d["label"],
            value=d.get("value"),
            children=[TreeNode.from_dict(c) for c in d.get("children", [])],
        )


@dataclass
class IssueTree:
    """/tree output."""

    root: TreeNode

    def validate(self) -> list:
        problems = []

        def walk(node: TreeNode, path: str) -> None:
            if not node.label:
                problems.append(f"node at {path or '/'} has no label")
            labels = [c.label for c in node.children]
            if len(labels) != len(set(labels)):
                problems.append(f"duplicate sibling labels under {node.label!r}")
            for c in node.children:
                walk(c, f"{path}/{node.label}")

        walk(self.root, "")
        return problems

    @classmethod
    def from_dict(cls, d: dict) -> "IssueTree":
        return cls(root=TreeNode.from_dict(d["root"]))


@dataclass
class GhostCell:
    id: str
    label: str = ""
    source: str = ""
    kill_condition: str = ""
    kind: str = "chart"           # chart | reconcile
    tolerance: Optional[float] = None

    @classmethod
    def from_dict(cls, d: dict) -> "GhostCell":
        return cls(
            id=d["id"],
            label=d.get("label", ""),
            source=d.get("source", ""),
            kill_condition=d.get("kill_condition", ""),
            kind=d.get("kind", "chart"),
            tolerance=d.get("tolerance"),
        )


@dataclass
class GhostPack:
    """/workplan output: the pre-registered blank charts."""

    cells: list = field(default_factory=list)  # list[GhostCell]

    def validate(self) -> list:
        problems = []
        if not self.cells:
            problems.append("ghost pack is empty")
        ids = [c.id for c in self.cells]
        if len(ids) != len(set(ids)):
            problems.append("duplicate ghost cell ids")
        for c in self.cells:
            if not c.id:
                problems.append("ghost cell missing id")
            if not c.source:
                problems.append(f"ghost cell {c.id!r} names no source")
        return problems

    def cell_ids(self) -> set:
        return {c.id for c in self.cells}

    @classmethod
    def from_dict(cls, d: dict) -> "GhostPack":
        return cls(cells=[GhostCell.from_dict(c) for c in d.get("cells", [])])


@dataclass
class SynthClaim:
    text: str
    evidence_ids: list = field(default_factory=list)
    value: Optional[float] = None

    @classmethod
    def from_dict(cls, d: dict) -> "SynthClaim":
        return cls(
            text=d["text"],
            evidence_ids=list(d.get("evidence_ids", [])),
            value=d.get("value"),
        )


@dataclass
class Synthesis:
    """/synthesize output: claims, each traceable to evidence."""

    claims: list = field(default_factory=list)  # list[SynthClaim]

    def validate(self) -> list:
        problems = []
        if not self.claims:
            problems.append("synthesis has no claims")
        for c in self.claims:
            if not c.text:
                problems.append("synthesis claim has no text")
        return problems

    @classmethod
    def from_dict(cls, d: dict) -> "Synthesis":
        return cls(claims=[SynthClaim.from_dict(c) for c in d.get("claims", [])])
