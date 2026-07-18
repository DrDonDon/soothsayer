"""Layer C — golden-transcript replay.

A committed cassette of recorded model responses replays through the review loop
deterministically: same result every run, no live call, no flakiness. This tests
the skill orchestration (assemble -> parse -> gate -> next step), not the model.
"""

import os
import unittest

from soothsayer.loop import CONVERGED, run_review_loop
from soothsayer.models import Assertion
from soothsayer.modelclient import MockModel

CASSETTE = os.path.join(os.path.dirname(__file__), "cassettes", "inhouse_converges.json")


class Replay(unittest.TestCase):
    def test_cassette_loads(self):
        m = MockModel.from_cassette(CASSETTE)
        self.assertEqual(m.name, "claude-sonnet-5")
        r = m.review(Assertion("x"), [])
        self.assertEqual(len(r.objections), 1)

    def test_deterministic_replay(self):
        a = Assertion("Entry is attractive", evidence_ids=["e1"])
        first = run_review_loop(a, [], MockModel.from_cassette(CASSETTE), floor=1)
        second = run_review_loop(a, [], MockModel.from_cassette(CASSETTE), floor=1)
        self.assertEqual(first.status, CONVERGED)
        self.assertEqual(first.status, second.status)
        self.assertEqual(first.objections_seen, second.objections_seen)


if __name__ == "__main__":
    unittest.main()
