# Soothsayer pipeline skills

The backbone is the McKinsey seven-step process. Each skill's **refusal** matters
more than its instruction: the constraint is the feature. In v0.1 these are the
contracts; v0.2 splits each into an individually invocable skill file that calls
the gate engine (`soothsayer.gates`) at the points marked below.

House style for all output: The Economist (short words, active voice, no jargon,
British spelling). See `../../.gstack/projects/Coding/steerco-house-style.md`.

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
