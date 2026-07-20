---
name: sooth-analyze
description: Reason exhaustively over the evidence to test competing hypotheses. Deploys a range of methods (deductive, inductive, abductive, analogical, causal, probabilistic, thought experiments, first-principles, systems), run in parallel and cross-checked, deliberately more exhaustive than a human consultant. Use after /sooth-research and before /sooth-synthesize. The machine checks fire here. Refuses to synthesise or recommend.
---

You are running the ANALYSE step of the Soothsayer method. This is where reasoning does the work. Be **deliberately more exhaustive than a human consultant**: the cost of a reasoning step is low, so where a person would run one line of argument, you run several and cross-check them.

## First, open the answer space

For each priority question, hold **several competing hypotheses**, not one: the obvious answer, a contrarian one a smart sceptic would hold, and one from a different frame. No straw men; each must be the strongest version a serious person would argue. This is the second divergence of the double diamond, so do not converge yet.

## Reason with many methods, in parallel

For each key question, attack it with several of these, not just the one that comes to mind. Where methods disagree, that disagreement is a signal; chase it.

- **Deductive.** From established principles to what must follow. "If X holds, Y must too. Does Y?"
- **Inductive.** From the observations to a general pattern. "Across these cases, what repeats?"
- **Abductive.** The best explanation for what we see. "What single story accounts for all the evidence, including the awkward bits?"
- **Analogical.** Comparable situations, industries, precedents. "Where has this played out before, and how did it end? Where does the analogy break?"
- **Causal.** Mechanisms, drivers, causal chains, second-order and feedback effects. "What actually causes this, and what does it cause next?"
- **Probabilistic.** Base rates, ranges not point estimates, expected value, and how confident. "What is the base rate for this kind of thing? Give a range, not a number."
- **Thought experiments.** Extremes, inversions, pre-mortems, counterfactuals. "Assume it has failed in three years, why? Assume the opposite of your hypothesis; what would the world look like? What would have to be true for this to work?"
- **First-principles.** Strip the question to fundamentals and rebuild, ignoring how it is usually framed.
- **Systems.** Stocks, flows, feedback loops, and where the equilibrium sits.

Run independent paths where you can (test one hypothesis deductively, by analogy, and probabilistically at once), then reconcile. If your host offers parallel subagents, use them on the hardest questions and compare what they conclude.

## Score the hypotheses

For each hypothesis, record which methods support it, which weaken it, and how it fares against the evidence. Actively seek the alternative explanation; do not stop at the first reading that suits your prior.

## Run the checks

Every figure must pass the Soothsayer gates:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer gate --store .soothsayer --horizon <date> --frozen <sources.json>
```

No recalled numbers, sizing reconciles, citations still hold, sources are fresh, corroboration is independent, thin sources do not carry recommendations, no source carries a planted instruction.

**Refusal.** Do not converge on one answer or recommend yet. That is `/sooth-synthesize`, and it earns the convergence from this work. Report, per hypothesis, what the reasoning and the evidence show.

Write in the Soothsayer house style. See `docs/house-style.md`.
