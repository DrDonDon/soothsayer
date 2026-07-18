# Contributing to Soothsayer

Thanks for helping. Soothsayer aims to be small, honest, and well-tested.

## Ground rules

- **The gates are the product.** New gates and changes to existing ones need
  tests against a seeded good/bad corpus: the gate must pass its good case and
  fail its bad case. See `tests/test_gates.py`.
- **No silent failure.** A gate or model call that cannot run should fail loud,
  never pass by omission.
- **Zero runtime dependencies for the core.** v0.1 is stdlib-only. A live model
  client may add an optional provider dependency, kept out of the import path so
  the gate engine still runs with nothing installed.
- **House style: The Economist.** Short words, active voice, no jargon, British
  spelling. This applies to skill prose and user-facing output.

## Setup

```
git clone https://github.com/DrDonDon/soothsayer.git
cd soothsayer
./setup                 # checks Python and runs the tests
```

## Tests

```
python3 -m unittest discover -s tests -t .
```

Every pull request must keep the suite green and add tests for new behaviour.

## Making a change

1. Branch from `main`.
2. Add the change and its tests.
3. Run the suite and `soothsayer demo`.
4. Open a pull request describing what the change refuses, not just what it does.

## Scope

Soothsayer validates with in-loop gates only; it does not do longitudinal
scoring or calibration by design. Proposals that add a persistent scored ledger
are a different project — discuss in an issue first.
