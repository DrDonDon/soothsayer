# Soothsayer

A strategy-research harness with a hard gate. "Sooth" is the old word for truth.

Agent harnesses work for coding because they run against a real gate: code
compiles or it does not; tests pass or they do not. Strategy harnesses copied the
role structure and inherited none of the gate. Soothsayer adds one. It cannot make
a claim true, but it can refuse to let a sloppy or laundered one through.

Soothsayer is **stateless, like gstack**. It holds no runtime database. Its memory
is the documents it writes — evidence records and decision logs — kept in a
git-backed directory you can read, diff, and share.

## What v0.1 is

The walking skeleton, built around the one part that is not gstack: a
**deterministic gate engine**. Everything here runs offline, with no model calls
and no third-party dependencies.

| Gate | Refuses |
|---|---|
| **T0 ban** | A number recalled from model memory, or any numeric claim without a fetched source and hash. |
| **Reconciliation** | A sizing where top-down and bottom-up disagree beyond tolerance, or segments that do not sum. |
| **Citation** | A source whose content changed, or a quote no longer present when re-fetched. |
| **Staleness** | A source too old for the decision horizon (a 2022 figure for a 2026 call). |
| **Independence** | Three outlets citing one press release counted as three sources. |
| **Tier floor** | A recommendation resting only on a blog. It can support a question, not a recommendation. |

The `/analyze <-> /inhouse` review loop guards two failure modes: **deadlock**
(unresolved objections escalate to a human) and **false convergence** (a reviewer
that agrees too easily is not trusted — an assertion passes only if it survived a
floor of substantive objections).

## Install

```
git clone <your-fork>/soothsayer
cd soothsayer
./setup
export PATH="$PWD/bin:$PATH"
soothsayer demo
```

Python 3.10+ is the only requirement.

## Use

```
soothsayer demo                       # end-to-end: every gate catches its bad case
soothsayer init .soothsayer           # create a git-backed store
soothsayer add-evidence --store .soothsayer --file record.json
soothsayer gate --store .soothsayer --horizon 2026-07-01 --frozen sources.json
```

An evidence record is JSON; see `fixtures/corpus/` for examples.

## How it is built

- `soothsayer/gates/` — the gate engine. Each gate is a pure function: records in,
  a pass/fail result with reasons out. Nothing here calls a model.
- `soothsayer/store.py` — the git-backed document store. Append-only by
  construction (content-hash ids); refuses a different-content write to an
  existing id.
- `soothsayer/loop.py` — the review loop, with the disagreement-floor.
- `soothsayer/modelclient.py` — a pluggable model interface with a mock. v0.1 never
  calls a live model.
- `skills/` — the gstack-style pipeline (define -> scan -> tree -> prune ->
  workplan -> research -> analyze -> synthesize -> communicate), each with the
  refusal that matters most.

Run the tests:

```
python3 -m unittest discover -s tests -t .
```

## What v0.1 deliberately leaves out

Validation is the gates only. There is no long-term scoring, no calibration, no
prediction ledger — the harness is stateless and its documents are its memory.

Before any **public** release, three things must land (see `../TODOS.md`):

- an **injection boundary** — the tool ingests untrusted web content, and a
  planted page could poison a number that then passes the provenance gates;
- **model diversity** — v0.1 runs the reviewer on the same model as the author, so
  the review is phrasing-independent but not error-independent; the
  disagreement-floor narrows that hole but does not close it;
- **packaging hardening** — key provisioning, a dependency lockfile, and a
  cross-platform stance.

## Licence

MIT.
