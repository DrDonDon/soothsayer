"""Review-loop tests: converge, escalate, under-review (false-convergence guard)."""

import unittest

from soothsayer.loop import CONVERGED, ESCALATE, UNDER_REVIEWED, run_review_loop
from soothsayer.models import Assertion
from soothsayer.modelclient import MockModel, Review


def _assertion():
    return Assertion("Entry is attractive", evidence_ids=["e1"])


class ReviewLoop(unittest.TestCase):
    def test_converges_after_surviving_objections(self):
        model = MockModel([Review(["sizing optimistic"]), Review([])])
        res = run_review_loop(_assertion(), [], model, floor=1, max_rounds=3)
        self.assertEqual(res.status, CONVERGED)
        self.assertGreaterEqual(res.objections_seen, 1)

    def test_escalates_on_unresolved_objections(self):
        model = MockModel([Review(["a"]), Review(["b"]), Review(["c"])])
        res = run_review_loop(_assertion(), [], model, floor=1, max_rounds=2)
        self.assertEqual(res.status, ESCALATE)

    def test_under_reviewed_when_floor_never_met(self):
        # Reviewer never objects: agreement is too easy -> not trusted.
        model = MockModel([])
        res = run_review_loop(_assertion(), [], model, floor=1, max_rounds=2)
        self.assertEqual(res.status, UNDER_REVIEWED)
        self.assertEqual(res.objections_seen, 0)

    def test_higher_floor_needs_more_scrutiny(self):
        # One objection then clean, but floor is 2 -> not enough scrutiny.
        model = MockModel([Review(["a"]), Review([]), Review([])])
        res = run_review_loop(_assertion(), [], model, floor=2, max_rounds=3)
        self.assertEqual(res.status, UNDER_REVIEWED)


if __name__ == "__main__":
    unittest.main()
