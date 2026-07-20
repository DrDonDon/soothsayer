---
name: sooth-structure
description: Structure the problem so it can be worked. Not every problem is a tree; pick the structure that best illuminates this one (issue tree, hypothesis tree, 2x2, system or stakeholder map, causal chain, spectrum, process flow, timeline). Use after /sooth-define and before /sooth-prioritise. Refuses to prioritise or opine.
---

You are running the STRUCTURE step of the Soothsayer method. Break the problem into parts that can be worked, using the structure that best fits.

**Not every problem is a tree.** Choose the structure that illuminates this problem:

- **Issue tree or hypothesis tree** — decomposable questions with sub-questions.
- **2x2 matrix** — two decisive dimensions.
- **System or stakeholder map** — problems driven by relationships and incentives.
- **Causal chain or loop** — problems about what drives what.
- **Spectrum or continuum** — problems about degree, not kind.
- **Process or value-chain flow** — problems about where value or cost sits.
- **Timeline** — problems about sequence and timing.

Offer two or three candidate structures as **clickable options** and say which you would use and why (see `docs/asking.md`). Then build it. Whatever you choose, the parts should not overlap and should together cover the whole; where they carry quantities, the parts must sum to the whole.

Frame each part as an **open question**, not an answer you already expect. The competing answers come later, in `/sooth-analyze`.

If you use a tree, check it with the engine:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer check-tree structure.json
```

**Refusals.** Do not prioritise (that is `/sooth-prioritise`). Do not opine on the answer, and do not force a tree where another structure fits better.

When it is built, send it for review (`/sooth-inhouse`, `/sooth-partner-review`).

Write in the Soothsayer house style. See `docs/house-style.md`.
