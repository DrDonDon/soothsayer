---
name: sooth-workplan
description: Build the ghost pack before doing the analysis. For each kept branch, name the blank chart you will fill, its source, and the finding that would kill the idea. Pre-registration you commit to before you look. Use after /sooth-prune and before /sooth-research. Refuses to do the analysis.
---

You are running the WORKPLAN step of the Soothsayer strategy method.

For each kept branch, write a **ghost cell**: a blank chart with its axes labelled, the source that will fill it, and the **kill condition** (the finding that would end the idea). For any cell that reconciles numbers, declare the **tolerance** now, before you know the answer.

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
