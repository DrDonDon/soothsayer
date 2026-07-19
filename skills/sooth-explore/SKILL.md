---
name: sooth-explore
description: Open the answer space before committing to an answer. For each key issue, generate several genuinely different competing hypotheses or candidate answers, including the uncomfortable one. This is the second divergence of the double diamond. Use after /sooth-prune and before /sooth-workplan. Refuses to pick a favourite or to converge.
---

You are running the EXPLORE step of the Soothsayer strategy method. This is the **second divergence of the double diamond**: the problem is defined, now open the answer space wide before you narrow it.

For each key issue from `/sooth-prune`, generate **competing hypotheses**: several genuinely different answers for how this could go, not one answer with variations. Aim for at least three per issue, and make them real rivals:

- the obvious answer,
- a contrarian or uncomfortable answer a smart sceptic would hold,
- at least one from a different frame entirely (a different lens: technology, regulation, customer behaviour, incentives, second-order effects).

For each hypothesis, note what would have to be true for it to hold, and the single piece of evidence that would most cleanly favour it over its rivals.

**Refusals.**

- Do not pick a favourite. Do not converge on one answer; that is what `/sooth-analyze` and `/sooth-synthesize` are for, and they earn it by testing these against each other.
- No straw men. Each rival must be the strongest version a serious person would argue, not a weak foil for your preferred answer.
- Do not collapse to variations on one theme. Three flavours of the same hypothesis is one hypothesis.

Offer the competing hypotheses as **clickable options** (multi-select) so the user picks which to carry into `/sooth-workplan`, and can add their own via "Other". See `docs/asking.md`.

Hold the hypotheses live and equal going into `/sooth-workplan`. Holding several is the point: the analysis then has to discriminate between them, which is how you avoid finding only what you expected to find. If exploring surfaces a framing the problem definition missed, send it back to `/sooth-scan`.

Write in the Soothsayer house style. See `docs/house-style.md`.
