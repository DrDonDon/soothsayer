---
name: sooth-workplan
description: Plan the analysis before you do it. For each priority question, pre-register the chart or analysis you will run, its source, and the finding that would change your answer. Commit to it before you look, so it cannot be reshaped to fit. Use after /sooth-prioritise and before /sooth-research. Refuses to do the analysis.
---

You are running the WORKPLAN step of the Soothsayer method. For each priority question from `/sooth-prioritise`, write a **ghost cell**: a blank chart or analysis with its axes labelled, the source that will fill it, and the **kill condition** (the finding that would change your answer). For any cell that reconciles numbers, declare the **tolerance** now, before you know the answer.

This is pre-registration. You commit to the shape of the analysis and its kill condition before you look, and before you have formed a preferred answer, so the analysis cannot be quietly reshaped to fit a conclusion. `/sooth-analyze` will generate competing hypotheses and test them against these charts.

The kill condition depends on the mode: in a **decision**, the finding that would end the idea; in a **perspective**, the evidence that would change your view.

Check the pack with the engine:

```
{"cells": [{"id": "c1", "label": "TAM", "source": "regulator filing",
            "kill_condition": "if penetration <5% we stop",
            "kind": "reconcile", "tolerance": 0.1}]}
```

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer check-workplan workplan.json
```

Every cell needs a kill condition; every reconcile cell needs a tolerance.

**Refusal.** Do not do the analysis. That is `/sooth-analyze`. Produce only the blank pack.

Write in the Soothsayer house style. See `docs/house-style.md`.
