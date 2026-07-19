---
name: sooth-workplan
description: Build the ghost pack before doing the analysis. Design each blank chart to discriminate between the competing hypotheses, name its source, and the finding that would kill each hypothesis. Pre-registration you commit to before you look. Use after /sooth-explore and before /sooth-research. Refuses to do the analysis.
---

You are running the WORKPLAN step of the Soothsayer strategy method.

You are holding several competing hypotheses from `/sooth-explore`. Design the pack to **discriminate between them**, not to confirm a favourite. For each key issue, write a **ghost cell**: a blank chart with its axes labelled, the source that will fill it, and the **kill condition**. A good ghost cell can come out in a way that favours one hypothesis over its rivals; a chart every hypothesis predicts the same is not worth filling, so replace it. Pre-register, per hypothesis, the finding that would kill it. For any cell that reconciles numbers, declare the **tolerance** now, before you know the answer.

The kill condition depends on the mode (from the brief). In a **decision**, it is the finding that would end the idea. In a **perspective**, it is the evidence that would change your view on that branch. Either way you commit to it before you look.

This is pre-registration. You commit to the chart's shape and its kill condition before you look, so the result cannot be quietly reshaped to fit what you find.

**Refusal.** Do not do the analysis. That is `/sooth-analyze`. Produce only the blank pack.

Check the pack with the engine. Write it as JSON:

```
{"cells": [{"id": "c1", "label": "TAM", "source": "regulator filing",
            "kill_condition": "if penetration <5% we stop",
            "kind": "reconcile", "tolerance": 0.1}]}
```

Run:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer check-workplan workplan.json
```

Every cell needs a kill condition; every reconcile cell needs a tolerance. Fix what it flags.

Write in the Soothsayer house style. See `docs/house-style.md`.
