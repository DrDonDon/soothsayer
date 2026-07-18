# Changelog

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

### Store, loop, CLI, docs
- Git-backed append-only document store.
- CLI: `version`, `init`, `add-evidence`, `gate`, `check`, `demo`.
- README, SECURITY, CONTRIBUTING, ACKNOWLEDGMENTS (gstack), MIT LICENSE.

Validation is the in-loop gates only. There is no longitudinal scoring or
calibration, by design.
