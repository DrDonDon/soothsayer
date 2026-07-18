---
name: sooth-synthesize
description: Turn findings into a recommendation as a pyramid, answer first then support. Use after /sooth-analyze and before /sooth-communicate. Refuses to introduce any fact that does not trace to an evidence record in the store.
---

You are running the SYNTHESIZE step of the Soothsayer strategy method.

Turn the analysed charts into a recommendation. Lead with the answer (the so-what), then the two or three findings that support it, then the evidence under each. This is the pyramid: conclusion first, support beneath.

**Refusal.** Every claim must trace to a record in the evidence store. Do not introduce a fact, a number, or a "well-known" figure that is not in the store. If you need something that is not there, go back to `/sooth-research`.

Check traceability with the engine. Write the synthesis as JSON:

```
{"claims": [{"text": "entry is attractive", "evidence_ids": ["<id1>", "<id2>"]}]}
```

Run:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer check-synthesis synthesis.json --store .soothsayer
```

Every claim must cite an evidence id that exists in the store. Fix any that do not before moving to `/sooth-communicate`.

Write in the Soothsayer house style. See `docs/house-style.md`.
