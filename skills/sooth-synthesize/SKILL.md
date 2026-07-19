---
name: sooth-synthesize
description: Turn findings into the answer, as a pyramid (point first, then support). For a decision this is a recommendation; for a perspective it is the thesis. Use after /sooth-analyze and before /sooth-communicate. Refuses to introduce any fact that does not trace to an evidence record in the store.
---

You are running the SYNTHESIZE step of the Soothsayer strategy method.

Turn the analysed charts into the answer. Lead with the point, then the two or three findings that support it, then the evidence under each. This is the pyramid: conclusion first, support beneath.

Read the mode from the brief:

- **Decision mode.** The point is a recommendation: what to do, and why.
- **Perspective mode.** The point is your thesis: the point of view the paper argues, in one sentence, then the pillars that hold it up.

This is the **second convergence of the double diamond**. You held several competing hypotheses through the analysis; now converge honestly. State which one best survived and, briefly, why it beat the others you held. Name the alternatives and why you rejected them. An answer that never says what it beat is advocacy dressed as analysis.

**Refusal.** Every claim must trace to a record in the evidence store. Do not introduce a fact, a number, or a "well-known" figure that is not in the store. If you need something that is not there, go back to `/sooth-research`.

Check traceability with the engine. Write the synthesis as JSON:

```
{"claims": [{"text": "the market is consolidating faster than priced in", "evidence_ids": ["<id1>", "<id2>"]}]}
```

Run:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer check-synthesis synthesis.json --store .soothsayer
```

Every claim must cite an evidence id that exists in the store. Fix any that do not before moving to `/sooth-communicate`.

Write in the Soothsayer house style. See `docs/house-style.md`.
