"""Layer A — skill-artifact contract/schema tests.

Valid artifacts validate cleanly; malformed ones produce specific problems.
Deterministic, no model.
"""

import unittest

from soothsayer.artifacts import (
    GhostCell,
    GhostPack,
    IgnoranceMap,
    IssueTree,
    Synthesis,
    TreeNode,
)


class IgnoranceMapContract(unittest.TestCase):
    def test_valid(self):
        m = IgnoranceMap(known=["a"], contested=["b"], unknown=["c"])
        self.assertEqual(m.validate(), [])

    def test_overlap_flagged(self):
        m = IgnoranceMap(known=["a"], contested=["a"], unknown=["c"])
        self.assertTrue(any("both" in p for p in m.validate()))

    def test_empty_unknown_flagged(self):
        m = IgnoranceMap(known=["a"], contested=["b"], unknown=[])
        self.assertTrue(any("narrow" in p for p in m.validate()))

    def test_from_dict(self):
        m = IgnoranceMap.from_dict({"known": ["a"], "unknown": ["c"]})
        self.assertEqual(m.known, ["a"])


class IssueTreeContract(unittest.TestCase):
    def test_valid(self):
        t = IssueTree.from_dict(
            {"root": {"label": "root", "children": [{"label": "a"}, {"label": "b"}]}}
        )
        self.assertEqual(t.validate(), [])

    def test_duplicate_siblings_flagged(self):
        t = IssueTree(TreeNode("root", children=[TreeNode("a"), TreeNode("a")]))
        self.assertTrue(any("duplicate" in p for p in t.validate()))


class GhostPackContract(unittest.TestCase):
    def test_valid(self):
        p = GhostPack([GhostCell(id="c1", label="TAM", source="filing")])
        self.assertEqual(p.validate(), [])

    def test_empty_flagged(self):
        self.assertTrue(any("empty" in x for x in GhostPack([]).validate()))

    def test_duplicate_ids_flagged(self):
        p = GhostPack([GhostCell(id="c1", source="s"), GhostCell(id="c1", source="s")])
        self.assertTrue(any("duplicate" in x for x in p.validate()))

    def test_missing_source_flagged(self):
        p = GhostPack([GhostCell(id="c1", label="TAM")])
        self.assertTrue(any("source" in x for x in p.validate()))


class SynthesisContract(unittest.TestCase):
    def test_valid(self):
        s = Synthesis.from_dict({"claims": [{"text": "x", "evidence_ids": ["e1"]}]})
        self.assertEqual(s.validate(), [])

    def test_empty_flagged(self):
        self.assertTrue(Synthesis([]).validate())


if __name__ == "__main__":
    unittest.main()
