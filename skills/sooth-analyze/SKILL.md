---
name: sooth-analyze
description: Solve each part of the structure to a mechanism-level answer, not a thin spray of methods. Works node by node: frame the sub-question, pick the reasoning that fits, reason to a "so what" with a range and the one thing that would flip it, then falsify it. Holds competing hypotheses per node and refuses shallow, generic, or fabricated answers. Writes analysis.json for /sooth-synthesize. Use after /sooth-research and before /sooth-synthesize. Refuses to recommend.
---

You are running the ANALYSE step of the Soothsayer method. This is where reasoning does the work. Be **deliberately more exhaustive than a human consultant**: the cost of a reasoning step is low, so where a person would run one line of argument, you run several and cross-check them.

The unit of work is the **node**: one part of the structure `/sooth-structure` built. Read `structure.json` and solve each surviving part to a real answer. Do not spray ten methods thinly across a few big questions. Grind each node.

Follow the per-node loop in `docs/reasoning-protocol.md`. In short, for each surviving node: frame the sub-question, decompose it, pick the one or two methods that fit and push them hard, reason to a mechanism-level "so what" with a range and the one fact that would flip it, then try to disprove it.

## First, open the answer space

For each node, hold **several competing hypotheses**, not one: the obvious answer, a contrarian one a smart sceptic would hold, and one from a different frame. No straw men; each must be the strongest version a serious person would argue. This is the second divergence of the double diamond, so do not converge on the overall answer yet. What is new is that each node reaches a supported verdict, rather than an open spray of methods.

## The reasoning methods

Pick the ones that fit the node. Where methods disagree, that disagreement is a signal; chase it.

- **Deductive.** From established principles to what must follow. "If X holds, Y must too. Does Y?"
- **Inductive.** From the observations to a general pattern. "Across these cases, what repeats?"
- **Abductive.** The best explanation for what we see. "What single story accounts for all the evidence, including the awkward bits?"
- **Analogical.** Comparable situations, industries, precedents. "Where has this played out before, and how did it end? Where does the analogy break?"
- **Causal.** Mechanisms, drivers, causal chains, second-order and feedback effects. "What actually causes this, and what does it cause next?"
- **Probabilistic.** Base rates, ranges not point estimates, expected value, and how confident. "What is the base rate for this kind of thing? Give a range, not a number."
- **Falsification (assume the opposite).** Take the answer you are drifting towards, assume it is false, and build the strongest case for the opposite. Then look for the evidence that would prove the original wrong. Run this on every node, not just once at the end. An answer you have only tried to confirm has not been tested.
- **Thought experiments.** Extremes, inversions, pre-mortems, counterfactuals. "Assume it has failed in three years, why? What would have to be true for this to work?"
- **First-principles.** Strip the question to fundamentals and rebuild, ignoring how it is usually framed.
- **Systems.** Stocks, flows, feedback loops, and where the equilibrium sits.

Run independent paths where you can, then reconcile. If your host offers parallel subagents, use them on the hardest nodes and compare what they conclude.

## The depth bar

A node answer passes when it names the dominant driver or mechanism, gives a range not a point, and states the one thing that would flip it. Refuse it and reason again when it restates the question, is generic enough to fit any company, or rests on no evidence and no mechanism.

If a node cannot be answered from the store, mark it **"unresolved, needs X"**. Do not invent a mechanism, and do not recall a number (that is the T0 ban). An honest unresolved is a pass, not a failure.

## When the evidence is missing: the research callback

The harness is stateless, so there is no live callback. When a node needs a figure the store does not hold, write the gap to `open_items` in `analysis.json`, run `/sooth-research` to fill the store from real, dated sources, then run `/sooth-analyze` again to close the node. Keep the rounds few, so the loop ends. See `docs/reasoning-protocol.md`.

## Write the artifact

Write `analysis.json` so the solved tree reaches `/sooth-synthesize`, which is a separate, stateless invocation. Same documents-as-memory pattern as `structure.json`. Per node: the question, the "so what", the methods used, the confidence, the flip condition, the evidence ids, and whether it is unresolved. The full shape is in `docs/reasoning-protocol.md`.

## Run the checks

Every figure must pass the Soothsayer gates:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer gate --store .soothsayer --horizon <date> --frozen <sources.json>
```

No recalled numbers, sizing reconciles, citations still hold, sources are fresh, corroboration is independent, thin sources do not carry recommendations, no source carries a planted instruction.

**Refusal.** Solving a node is not recommending. Do not converge on one overall answer. That is `/sooth-synthesize`, and it earns the convergence from this work. Report, per node, what the reasoning and the evidence show.

Write in the Soothsayer house style. See `docs/house-style.md`.
