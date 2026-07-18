# Changelog

## 0.1.3 — /sooth-define interrogates

Feedback: define was good but too easily satisfied. It now asks hard clarifying
questions, one at a time, and pushes on vague answers before it writes the brief.
Specificity is the currency: a category is not a person, "soon" is not a date, and
a thesis everyone agrees with is not a perspective. It will say the ask is not
ready rather than dress a fuzzy brief up as a clear one. Mode-specific probes for
both decisions and perspectives.

## 0.1.2 — two modes: decisions and perspectives

Feedback: Soothsayer only worked for a decision. `/sooth-define` hard-refused
without a decision-maker and a date, so a briefing paper or point of view (a big
piece of strategic thinking with no single decision) was blocked at the door.

- **`/sooth-define` is now mode-aware.** It settles the mode first: a **decision**
  (a specific choice) or a **perspective** (a briefing paper, point of view, or
  strategic thesis). Each mode has its own gate: a decision needs a decider and a
  date; a perspective needs a named audience and a sharp question or thesis.
- **`/sooth-synthesize`** leads with a recommendation (decision) or a thesis
  (perspective). **`/sooth-communicate`** produces the decision pack or a briefing
  paper (thesis up front, argument, implications, what would change the view,
  hostile Q&A).
- **`/sooth-workplan`** and **`/sooth-partner-review`** read the mode too: kill
  conditions become "what would change the view", and the reviewer's "room"
  becomes the audience.
- The evidence discipline is identical in both modes. No engine change.

## 0.1.1 — a real Claude Code harness

Feedback: the audience is strategy consultants with a Claude Code subscription,
not developers. v0.1.0 read like a dev tool and demanded an API key.

- **The skills are now real, invocable Claude Code commands.** Eleven skills under
  `skills/sooth-*` (`/sooth-define` … `/sooth-communicate`, `/sooth-inhouse`,
  `/sooth-partner-review`), installed by `./install` into `~/.claude/skills/`.
  They run on your Claude subscription and call the checking engine for the
  deterministic gates.
- **No API key.** Removed the standalone model-client, config, and `check`
  machinery (`config.py`, `modelclient.py`, `loop.py`) that assumed a separate
  app calling the API. The review discipline now lives in the reviewer skills.
- **CLI gains skill-gate checks:** `check-tree`, `check-workplan`,
  `check-synthesis`, so the gate-bearing skills can call the engine.
- **README rewritten** for strategy consultants: plain language, the skills and
  how to use them, no jargon up top. Follows the house style.
- **Fix (P2):** a single evidence record no longer produces a scary `independence`
  FAIL; independence applies once you have two or more sources.

## 0.1.0 — first public release

The walking skeleton, hardened for a public release.

### Gate engine (the part that is not gstack)
- T0 ban, reconciliation, citation re-verification, staleness, independence
  tracing, and tier floor — each a pure, tested function.

### Injection boundary (pre-public blocker, done)
- `ingest.detect_injection` flags planted instructions in source content.
- `ingest.ground_extract` refuses to create a record for a figure not present in
  the source (extraction cannot invent a number).
- `ingest.as_data` passes untrusted content to models as inert data.
- `gates.injection` fails loud on flagged sources.

### Model diversity + degraded mode (pre-public blocker, done)
- `modelclient.ClientPair` refuses an author == reviewer configuration unless
  explicitly overridden.
- `config.Config.validate` flags identical author/reviewer models.
- The review loop retries an unavailable reviewer, then hard-blocks (never ships
  an un-reviewed assertion).

### Packaging hardening (pre-public blocker, done)
- Keys read from the environment, never the repo; `.soothsayer/` gitignored.
- Cross-platform entrypoint `python -m soothsayer`; `pip install` console script.
- `soothsayer check` validates config (model diversity + key presence).
- CI runs the test suite on Linux, macOS, and Windows.

### Skill testing (layers A, B, C, E — deterministic, in CI)
- `artifacts.py` — skill output artifacts (ignorance map, issue tree, ghost pack,
  synthesis) with contract validators (layer A).
- `skillgates.py` — mechanically-checkable refusals as gates: traceability,
  tree partition, ghost-pack pre-registration, research scope (layer B).
- `MockModel.from_cassette` — replay recorded transcripts deterministically (layer C).
- `pipeline.py` — pack-level gate oracle; adversarial integration test feeds a
  poisoned pack through and it is rejected (layer E).
- Layer D (live-model evals with a gold set) remains v0.2.

### Store, loop, CLI, docs
- Git-backed append-only document store.
- CLI: `version`, `init`, `add-evidence`, `gate`, `check`, `demo`.
- README, SECURITY, CONTRIBUTING, ACKNOWLEDGEMENTS (gstack), MIT LICENSE.

Validation is the in-loop gates only. There is no longitudinal scoring or
calibration, by design.
