"""CLI tests — exercise every subcommand the skills call.

Added in the v0.2 line: the CLI (check-tree, check-workplan, check-synthesis,
gate, add-evidence, version, demo) had no coverage. These drive main() directly
and assert exit codes, so a broken skill-facing command fails the build.
"""

import contextlib
import io
import json
import os
import tempfile
import unittest

from soothsayer.cli import main
from soothsayer.gates import content_hash


def _run(args) -> int:
    """Call the CLI, swallowing its stdout so the test output stays clean."""
    with contextlib.redirect_stdout(io.StringIO()):
        return main(args)


def _write(directory, name, obj) -> str:
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh)
    return path


class Cli(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def test_version(self):
        self.assertEqual(_run(["version"]), 0)

    def test_demo(self):
        self.assertEqual(_run(["demo"]), 0)

    def test_check_tree(self):
        good = _write(self.d, "t.json", {"root": {"label": "t", "value": 100,
                     "children": [{"label": "a", "value": 60}, {"label": "b", "value": 40}]}})
        bad = _write(self.d, "tb.json", {"root": {"label": "t", "value": 100,
                     "children": [{"label": "a", "value": 60}, {"label": "b", "value": 20}]}})
        self.assertEqual(_run(["check-tree", good]), 0)
        self.assertEqual(_run(["check-tree", bad]), 1)

    def test_check_workplan(self):
        good = _write(self.d, "w.json", {"cells": [{"id": "c1", "source": "f", "kill_condition": "k"}]})
        bad = _write(self.d, "wb.json", {"cells": [{"id": "c1", "source": "f"}]})  # no kill condition
        self.assertEqual(_run(["check-workplan", good]), 0)
        self.assertEqual(_run(["check-workplan", bad]), 1)

    def test_add_evidence_gate_and_synthesis(self):
        store = os.path.join(self.d, "store")
        src = "Regulator: penetration was 12% in 2025."
        rec = {
            "claim": "pen 12", "source_url": "https://r.example",
            "verbatim_extract": "penetration was 12% in 2025", "source_tier": "T1",
            "fetch_date": "2026-07-18", "fetch_hash": content_hash(src),
            "publication_date": "2025-11-01", "value": 12.0,
        }
        recf = _write(self.d, "rec.json", rec)
        self.assertEqual(_run(["add-evidence", "--store", store, "--file", recf]), 0)
        # gate with no fetcher/horizon: t0 passes, single-record independence passes (P2)
        self.assertEqual(_run(["gate", "--store", store]), 0)

        eid = os.listdir(os.path.join(store, "evidence"))[0].replace(".json", "")
        good_syn = _write(self.d, "s.json", {"claims": [{"text": "ok", "evidence_ids": [eid]}]})
        bad_syn = _write(self.d, "sb.json", {"claims": [{"text": "bad", "evidence_ids": ["ghost"]}]})
        self.assertEqual(_run(["check-synthesis", good_syn, "--store", store]), 0)
        self.assertEqual(_run(["check-synthesis", bad_syn, "--store", store]), 1)


if __name__ == "__main__":
    unittest.main()
