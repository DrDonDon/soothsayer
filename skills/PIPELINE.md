# Soothsayer pipeline skills

The backbone is the McKinsey seven-step process. Each skill's **refusal** matters
more than its instruction: the constraint is the feature. In v0.1 these are the
contracts; v0.2 splits each into an individually invocable skill file that calls
the gate engine (`soothsayer.gates`) at the points marked below.

House style for all output: The Economist (short words, active voice, no jargon,
British spelling). See [`../docs/house-style.md`](../docs/house-style.md).

| Step | Skill | Does | **Refuses** | Gate tie-in |
|---|---|---|---|---|
| 1 Define | `/define` | Problem, decision-maker, decision date, success criteria, out-of-scope. | To analyse anything. **Hard gate:** no named decision-maker and date -> no proceed. | — |
| 2 Structure | `/scan` | Exploratory, unfocused; hunts the reframe; emits an ignorance map (known / contested / unknown). | To recommend. To narrow. | — |
| 2 Structure | `/tree` | Issue and hypothesis tree. | To prioritise or opine. | Machine-checked: branches partition, levels sum. |
| 3 Prioritise | `/prune` | 80/20 on impact x influence x knowability. | To add branches. Must emit a kill list with reasons. | — |
| 4 Workplan | `/workplan` | Ghost pack: blank charts, axes labelled, source named, kill condition per branch. **Pre-registration** — commit the chart shape and its tolerance before the answer is known. | To do the analysis. | Declares reconciliation tolerances up front. |
| 5 Research | `/research` | Targeted gathering into the evidence store. | To gather anything that does not fill a named ghost cell. | Writes records; `t0_gate` fires at write. |
| 5 Analyse | `/analyze` | Fills ghost charts. | To synthesise or recommend. | `reconcile`, `citation`, `staleness`, `independence`, `tier_floor` fire here. |
| 6 Synthesise | `/synthesize` | Findings -> so-what -> pyramid. | To introduce any fact not traceable to an evidence record. | Every claim must resolve to a stored record id. |
| 7 Communicate | `/communicate` | SCQA, the pack, hostile Q&A. | To change the answer to make the story cleaner. | — |

## Reviewers (run on the pack, starved of the reasoning trace)

| Skill | Asks | Kills for | Instruction |
|---|---|---|---|
| `/inhouse` | Is this true about *us*? | False, stale, generic, laundered. | **Penalise polish.** Score down framework use, MECE-shaped prose, and confident language on inferred claims. *What would make me look stupid if I greenlit this?* Sees the claims and (in a full build) the client's numbers. Never sees the narrative. |
| `/partner-review` | Will this survive the room? | Obvious, unactionable, wrong question. | Pattern priors; is there a so-what. Sees the pack, not the reasoning trace. |

Both run trace-starved. In v0.1 they run on the same model as the author, so the
review is phrasing-independent but not error-independent — the `/analyze <->
/inhouse` loop's **disagreement-floor** (`soothsayer.loop`) guards the resulting
false-convergence risk. Model diversity is the real fix and is a pre-public TODO.

## E2 — always-on red-team

Before an assertion reaches the pack, a trace-starved adversary tries to generate
its single strongest disconfirming case from date-restricted evidence. The
assertion must survive it or be weakened. This widens the second diamond's
divergence: falsification on every live assertion, not a pre-mortem at the end.

## Testing the skills

A skill is a prompt that drives a model, so it splits into what is mechanically
checkable (tested now, offline, in CI) and what needs judgment (evals, v0.2).

- **Layer A — contract/schema** (`soothsayer/artifacts.py`, `tests/test_artifacts.py`):
  each skill's output artifact (ignorance map, issue tree, ghost pack, synthesis)
  parses and validates against its contract.
- **Layer B — refusals as gates** (`soothsayer/skillgates.py`, `tests/test_skillgates.py`):
  the checkable refusals, as deterministic gates —
  `traceability_gate` (`/synthesize` cites only real evidence),
  `tree_partition_gate` (`/tree` partitions and sums),
  `ghost_pack_gate` (`/workplan` pre-registers a kill condition + tolerance),
  `research_scope_gate` (`/research` only fills named ghost cells).
- **Layer C — golden-transcript replay** (`MockModel.from_cassette`,
  `tests/test_replay.py`): recorded model responses replay deterministically
  through the loop, testing orchestration with no live call.
- **Layer E — adversarial integration** (`soothsayer/pipeline.py`,
  `tests/test_pipeline_adversarial.py`): a poisoned pack is fed through the gate
  oracle and rejected; the gate engine is the ground truth for the skills' output.
- **Layer D — evals** (v0.2, needs the live model + a gold set): the judgment the
  gates cannot check — does `/inhouse` catch a planted falsehood, does E2 produce
  a real disconfirming case. N-sample scoring, pinned model versions, a
  different-model judge.
