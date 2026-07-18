"""Gate engine tests: a seeded corpus of good and known-bad records.

Each gate must PASS its good case and FAIL its bad case. This is the PRD's M1
("provable against a seeded corpus with known-bad citations") — the real unit
test for a gate.
"""

import unittest

from soothsayer.gates import (
    FrozenFetcher,
    citation_gate,
    content_hash,
    independence_gate,
    reconcile_gate,
    segments_sum_gate,
    staleness_gate,
    t0_gate,
    tier_floor_gate,
)
from soothsayer.models import Assertion, EvidenceRecord, Tier

SRC = "The regulator reported market penetration of 12% in 2025."
SRC_HASH = content_hash(SRC)


def good_record(**over):
    base = dict(
        claim="Penetration was 12% in 2025",
        source_url="https://regulator.example/report-2025",
        verbatim_extract="market penetration of 12% in 2025",
        source_tier=Tier.T1,
        fetch_date="2026-07-18",
        fetch_hash=SRC_HASH,
        publication_date="2025-11-01",
        value=12.0,
    )
    base.update(over)
    return EvidenceRecord(**base)


class T0Gate(unittest.TestCase):
    def test_good_passes(self):
        self.assertTrue(t0_gate(good_record()))

    def test_t0_tier_banned(self):
        r = good_record(source_tier=Tier.T0)
        self.assertFalse(t0_gate(r))

    def test_number_without_provenance_fails(self):
        r = good_record(fetch_hash="", source_url="")
        self.assertFalse(t0_gate(r))


class CitationGate(unittest.TestCase):
    def setUp(self):
        self.fetcher = FrozenFetcher({"https://regulator.example/report-2025": SRC})

    def test_verbatim_present_passes(self):
        self.assertTrue(citation_gate(good_record(), self.fetcher))

    def test_quote_missing_fails(self):
        r = good_record(verbatim_extract="market penetration of 20% in 2025")
        self.assertFalse(citation_gate(r, self.fetcher))

    def test_hash_mismatch_fails(self):
        r = good_record(fetch_hash="deadbeefdeadbeef")
        self.assertFalse(citation_gate(r, self.fetcher))

    def test_fetch_failure_fails_loud(self):
        r = good_record(source_url="https://missing.example")
        res = citation_gate(r, self.fetcher)
        self.assertFalse(res)
        self.assertTrue(any("fetch" in reason for reason in res.reasons))


class ReconcileGate(unittest.TestCase):
    def test_ties_within_tolerance(self):
        self.assertTrue(reconcile_gate(100, 108, 0.10))

    def test_out_of_tolerance_fails(self):
        self.assertFalse(reconcile_gate(100, 140, 0.10))

    def test_segments_sum(self):
        self.assertTrue(segments_sum_gate(100, [40, 35, 25]))
        self.assertFalse(segments_sum_gate(100, [40, 35, 15]))


class StalenessGate(unittest.TestCase):
    def test_recent_passes(self):
        self.assertTrue(staleness_gate(good_record(), "2026-07-01", 365))

    def test_stale_fails(self):
        r = good_record(publication_date="2022-01-01")
        self.assertFalse(staleness_gate(r, "2026-07-01", 365))

    def test_missing_pubdate_fails(self):
        r = good_record(publication_date=None)
        self.assertFalse(staleness_gate(r, "2026-07-01", 365))


class IndependenceGate(unittest.TestCase):
    def test_two_origins_pass(self):
        a = good_record(source_url="https://a.example", origin_trace="https://o1")
        b = good_record(source_url="https://b.example", origin_trace="https://o2")
        self.assertTrue(independence_gate([a, b]))

    def test_laundered_single_origin_fails(self):
        a = good_record(source_url="https://a.example", origin_trace="https://press")
        b = good_record(source_url="https://b.example", origin_trace="https://press")
        c = good_record(source_url="https://c.example", origin_trace="https://press")
        self.assertFalse(independence_gate([a, b, c]))


class TierFloorGate(unittest.TestCase):
    def setUp(self):
        self.t3 = good_record(source_url="https://blog.example", source_tier=Tier.T3,
                              value=None, fetch_hash="9", verbatim_extract="")
        self.t1 = good_record()
        self.by_id = {self.t3.id: self.t3, self.t1.id: self.t1}

    def test_recommendation_on_t3_fails(self):
        a = Assertion("enter", strength="recommendation", evidence_ids=[self.t3.id])
        self.assertFalse(tier_floor_gate(a, self.by_id))

    def test_question_on_t3_passes(self):
        a = Assertion("should we?", strength="question", evidence_ids=[self.t3.id])
        self.assertTrue(tier_floor_gate(a, self.by_id))

    def test_recommendation_on_t1_passes(self):
        a = Assertion("enter", strength="recommendation", evidence_ids=[self.t1.id])
        self.assertTrue(tier_floor_gate(a, self.by_id))


if __name__ == "__main__":
    unittest.main()
