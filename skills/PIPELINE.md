# Soothsayer pipeline

Ten skills under `skills/sooth-*`, installed into Claude Code by `./install`. The
backbone is the McKinsey method, run as a **double diamond**: the problem opens
wide in `/sooth-define` before `/sooth-structure` and `/sooth-prioritise`
converge; the answer opens wide in `/sooth-analyze` (competing hypotheses, many
reasoning methods) before `/sooth-synthesize` converges. Each skill's **refusal**
matters more than its instruction.

House style: The Economist (`../docs/house-style.md`). Ask with clickable options
(`../docs/asking.md`).

## The core steps

| Step | Skill | Does | Refuses | Checked by |
|---|---|---|---|---|
| 1 Define | `/sooth-define` | Socratic clarify + is-it-worth-solving; framings | to proceed on a fuzzy or pointless problem | — |
| 2 Structure | `/sooth-structure` | the structure that fits (tree, 2x2, map, causal, spectrum) | to prioritise or force a tree | `check-tree` (if a tree) |
| 3 Prioritise | `/sooth-prioritise` | keep the parts that matter; kill list | to add parts | — |
| 4 Workplan | `/sooth-workplan` | pre-register the analyses and kill conditions | to do the analysis | `check-workplan` |
| 5 Research | `/sooth-research` | gather sourced evidence into the store | recalled numbers; letting off-plan take over | `add-evidence` (T0 ban) |
| 6 Analyse | `/sooth-analyze` | competing hypotheses tested with many reasoning methods, in parallel | to converge or recommend | `gate` |
| 7 Synthesise | `/sooth-synthesize` | converge; say what the answer beat | any fact not in the store | `check-synthesis` |
| — Communicate | `/sooth-communicate` | the pack (decision) or briefing paper (perspective) | to bend a finding for a cleaner story | — |

## Reasoning methods (in `/sooth-analyze`)

Deductive, inductive, abductive, analogical, causal, probabilistic, thought
experiments, first-principles, systems. Run several on each key question, in
parallel, and cross-check them. Deliberately more exhaustive than a human, because
a reasoning step is cheap.

## Reviews at three checkpoints

`/sooth-inhouse` ("is this true about us?") and `/sooth-partner-review` ("will this
survive the room?") run after **Define** (right problem?), **Structure** (sound
shape?), and **Synthesise** (true answer?). Reviewing early is far cheaper than
reviewing only at the end.

## Testing the skills

The checking engine is the test oracle. See `soothsayer/skillgates.py`
(`tests/test_skillgates.py`), `soothsayer/artifacts.py` (`tests/test_artifacts.py`),
and `soothsayer/pipeline.py` (`tests/test_pipeline_adversarial.py`, a poisoned pack
is rejected). The judgement quality of the model-driven skills is measured by
evals, next.
