"""Layer B — refusal-as-gate tests.

Each pipeline skill's mechanically-checkable refusal, expressed as a gate that
passes its good case and fails its bad case.
"""

import unittest

from soothsayer.artifacts import GhostCell, GhostPack, IssueTree, Synthesis, SynthClaim, TreeNode
from soothsayer.models import EvidenceRecord, Tier
from soothsayer.skillgates import (
    ghost_pack_gate,
    research_scope_gate,
    traceability_gate,
    tree_partition_gate,
)


class Traceability(unittest.TestCase):
    def test_all_claims_traceable_passes(self):
        s = Synthesis([SynthClaim("entry attractive", evidence_ids=["e1", "e2"])])
        self.assertTrue(traceability_gate(s, {"e1", "e2", "e3"}))

    def test_unknown_id_fails(self):
        s = Synthesis([SynthClaim("entry attractive", evidence_ids=["ghost"])])
        self.assertFalse(traceability_gate(s, {"e1"}))

    def test_no_evidence_fails(self):
        s = Synthesis([SynthClaim("entry attractive", evidence_ids=[])])
        res = traceability_gate(s, {"e1"})
        self.assertFalse(res)
        self.assertTrue(any("no evidence" in r for r in res.reasons))


class TreePartition(unittest.TestCase):
    def test_summing_levels_pass(self):
        t = IssueTree(TreeNode("total", value=100, children=[
            TreeNode("a", value=60), TreeNode("b", value=40)]))
        self.assertTrue(tree_partition_gate(t))

    def test_non_summing_fails(self):
        t = IssueTree(TreeNode("total", value=100, children=[
            TreeNode("a", value=60), TreeNode("b", value=20)]))
        self.assertFalse(tree_partition_gate(t))

    def test_duplicate_siblings_fail(self):
        t = IssueTree(TreeNode("root", children=[TreeNode("a"), TreeNode("a")]))
        self.assertFalse(tree_partition_gate(t))


class GhostPackRefusal(unittest.TestCase):
    def test_kill_condition_present_passes(self):
        p = GhostPack([GhostCell(id="c1", source="filing", kill_condition="if <5% we stop")])
        self.assertTrue(ghost_pack_gate(p))

    def test_missing_kill_condition_fails(self):
        p = GhostPack([GhostCell(id="c1", source="filing")])
        self.assertFalse(ghost_pack_gate(p))

    def test_reconcile_without_tolerance_fails(self):
        p = GhostPack([GhostCell(id="c1", source="filing", kill_condition="k", kind="reconcile")])
        self.assertFalse(ghost_pack_gate(p))

    def test_reconcile_with_tolerance_passes(self):
        p = GhostPack([GhostCell(id="c1", source="filing", kill_condition="k",
                                 kind="reconcile", tolerance=0.1)])
        self.assertTrue(ghost_pack_gate(p))


class ResearchScope(unittest.TestCase):
    def _rec(self, cell):
        return EvidenceRecord(claim="x", source_url="u", verbatim_extract="x",
                              source_tier=Tier.T1, fetch_date="2026-07-18", fetch_hash="h",
                              ghost_cell_id=cell)

    def test_records_fill_named_cells_pass(self):
        recs = [self._rec("c1"), self._rec("c2")]
        self.assertTrue(research_scope_gate(recs, {"c1", "c2"}))

    def test_record_with_no_cell_fails(self):
        self.assertFalse(research_scope_gate([self._rec(None)], {"c1"}))

    def test_record_filling_unknown_cell_fails(self):
        self.assertFalse(research_scope_gate([self._rec("c9")], {"c1"}))


if __name__ == "__main__":
    unittest.main()
