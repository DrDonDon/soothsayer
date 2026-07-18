"""Store tests: add/read round-trip, idempotent re-add, immutability enforcement."""

import tempfile
import unittest
from pathlib import Path

from soothsayer.models import EvidenceRecord, Tier
from soothsayer.store import ImmutabilityError, Store


def rec(claim="x", value=1.0):
    return EvidenceRecord(
        claim=claim, source_url="https://s.example", verbatim_extract="x",
        source_tier=Tier.T1, fetch_date="2026-07-18", fetch_hash="abc", value=value,
    )


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        # git off in tests to keep them fast and hermetic
        self.store = Store(self.tmp.name)
        self.store.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.store.decisions_log.parent.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_roundtrip(self):
        r = rec()
        self.store.add_evidence(r)
        loaded = self.store.evidence()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].id, r.id)
        self.assertEqual(loaded[0].claim, "x")

    def test_idempotent_re_add(self):
        r = rec()
        self.store.add_evidence(r)
        self.store.add_evidence(r)  # same content -> same id, no error
        self.assertEqual(len(self.store.evidence()), 1)

    def test_immutability_enforced(self):
        r = rec()
        self.store.add_evidence(r)
        # forge a different-content file at the same id path
        forged = self.store.evidence_dir / f"{r.id}.json"
        forged.write_text('{"claim": "tampered"}', encoding="utf-8")
        r2 = rec()  # same id as r
        with self.assertRaises(ImmutabilityError):
            self.store.add_evidence(r2)

    def test_decision_log_append(self):
        self.store.append_decision({"decision": "accept", "id": 1})
        self.store.append_decision({"decision": "reject", "id": 2})
        lines = self.store.decisions_log.read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(lines), 2)


if __name__ == "__main__":
    unittest.main()
