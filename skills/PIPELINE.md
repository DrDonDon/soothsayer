# Soothsayer pipeline

The skills live one per directory under `skills/sooth-*`, installed into Claude
Code by `./install`. The backbone is the McKinsey seven-step method. Each skill's
**refusal** matters more than its instruction: the constraint is the feature.

House style for all output: The Economist (short words, active voice, British
spelling, no em dashes). See `../docs/house-style.md`.

| Step | Skill | Does | **Refuses** | Checked by |
|---|---|---|---|---|
| 1 Define | `/sooth-define` | problem, decision-maker, date, success criteria | to analyse; **hard gate**: no decision-maker + date, no proceed | — |
| 2 Scan | `/sooth-scan` | ignorance map; hunts the reframe | to recommend or narrow | — |
| 2 Tree | `/sooth-tree` | issue/hypothesis tree | to prioritise or opine | `soothsayer check-tree` |
| 3 Prune | `/sooth-prune` | 80/20; kill list with reasons | to add branches | — |
| 4 Workplan | `/sooth-workplan` | ghost pack (pre-registration) | to do the analysis | `soothsayer check-workplan` |
| 5 Research | `/sooth-research` | gather into the evidence store | to gather off-plan | `soothsayer add-evidence` (T0 ban) |
| 5 Analyse | `/sooth-analyze` | fill the charts | to synthesise or recommend | `soothsayer gate` |
| 6 Synthesise | `/sooth-synthesize` | findings to recommendation (pyramid) | any fact not in the store | `soothsayer check-synthesis` |
| 7 Communicate | `/sooth-communicate` | SCQA, the pack, hostile Q&A | to change the answer for a cleaner story | — |

Reviewers, run before presenting:

- `/sooth-inhouse` asks "is this true about us?"; penalises polish; kills the false, stale, generic, laundered.
- `/sooth-partner-review` asks "will this survive the room?"; kills the obvious, unactionable, wrong-question.

The model is your Claude Code subscription. There is no API key. The `soothsayer`
CLI is the deterministic checking engine the gate-bearing skills call; it never
calls a model.

## Testing the skills

Skills are prompts, so they split into what is mechanically checkable (tested,
offline, in CI) and what needs judgement (evals, next). The checking engine is
the test oracle: the checkable refusals are gates, so model-driven output is
graded against deterministic ground truth.

- **Contract/schema** (`soothsayer/artifacts.py`, `tests/test_artifacts.py`).
- **Refusals as gates** (`soothsayer/skillgates.py`, `tests/test_skillgates.py`):
  traceability, tree partition, ghost-pack pre-registration, research scope.
- **Adversarial integration** (`soothsayer/pipeline.py`,
  `tests/test_pipeline_adversarial.py`): a poisoned pack is rejected by the oracle.
- **Evals** (next): the judgement the gates cannot check, for example whether
  `/sooth-inhouse` catches a planted falsehood. Needs a labelled gold set.
