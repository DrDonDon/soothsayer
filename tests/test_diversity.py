"""Model-diversity + degraded-mode tests."""

import unittest

from soothsayer.config import Config
from soothsayer.loop import BLOCKED, run_review_loop
from soothsayer.models import Assertion
from soothsayer.modelclient import ClientPair, MockModel, Review


class Diversity(unittest.TestCase):
    def test_same_model_refused(self):
        a = MockModel(name="claude-opus-4-8")
        r = MockModel(name="claude-opus-4-8")
        with self.assertRaises(ValueError):
            ClientPair(author=a, reviewer=r)

    def test_different_models_ok(self):
        a = MockModel(name="claude-opus-4-8")
        r = MockModel(name="claude-sonnet-5")
        pair = ClientPair(author=a, reviewer=r)
        self.assertIsNotNone(pair)

    def test_override_allows_same(self):
        a = MockModel(name="m")
        r = MockModel(name="m")
        ClientPair(author=a, reviewer=r, allow_same_model=True)  # no raise


class ConfigValidation(unittest.TestCase):
    def test_identical_models_flagged(self):
        cfg = Config(author_model="x", reviewer_model="x")
        self.assertTrue(cfg.validate())

    def test_distinct_models_ok(self):
        cfg = Config(author_model="x", reviewer_model="y")
        self.assertEqual(cfg.validate(), [])

    def test_stringy_allow_same_model_still_flags(self):
        # Regression: BUG-2 — a JSON string "false" for allow_same_model was
        # truthy and silently disabled the diversity gate.
        # Found by /qa on 2026-07-18.
        cfg = Config(author_model="x", reviewer_model="x", allow_same_model="false")
        self.assertTrue(cfg.validate(), "stringy 'false' must not disable the diversity check")

    def test_load_coerces_string_bools(self):
        import json, tempfile, os
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "config.json")
            with open(p, "w") as fh:
                json.dump({"author_model": "x", "reviewer_model": "x",
                           "allow_same_model": "false"}, fh)
            cfg = Config.load(p, environ={})
            self.assertIs(cfg.allow_same_model, False)
            self.assertTrue(cfg.validate())

    def test_key_present(self):
        cfg = Config(provider_key_env="SOOTHSAYER_TEST_KEY")
        self.assertFalse(cfg.key_present({}))
        self.assertTrue(cfg.key_present({"SOOTHSAYER_TEST_KEY": "abc"}))


class DegradedMode(unittest.TestCase):
    def test_reviewer_unavailable_blocks_loud(self):
        model = MockModel(fail=True, name="reviewer")
        res = run_review_loop(Assertion("x", evidence_ids=[]), [], model, retries=1)
        self.assertEqual(res.status, BLOCKED)


if __name__ == "__main__":
    unittest.main()
