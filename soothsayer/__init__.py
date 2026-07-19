"""Soothsayer — a stateless, gstack-style strategy-research harness.

Its memory is the documents it writes, not runtime state. The one part that is
not gstack is the deterministic gate engine (soothsayer.gates): reconciliation,
citation re-verification, independence tracing, staleness, tier-floor, and the
T0 (model-memory) ban. Those gates prove the work is not sloppy or laundered.
Nothing here claims the conclusion is true — validation is the gates, not a score.
"""

__version__ = "0.1.4"
