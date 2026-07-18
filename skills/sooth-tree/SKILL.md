---
name: sooth-tree
description: Break a strategy problem into a clean issue/hypothesis tree. Use after /sooth-scan and before /sooth-prune. Branches must not overlap and, where they carry numbers, must sum. Refuses to prioritise or opine.
---

You are running the TREE step of the Soothsayer strategy method.

Break the problem into an issue tree: branches that do not overlap and together cover the whole problem (mutually exclusive, collectively exhaustive). Where branches carry quantities, the children must sum to the parent.

**Refusals.** Do not prioritise (that is `/sooth-prune`). Do not opine on the answer.

Check the tree with the Soothsayer engine before you present it. Write the tree as JSON:

```
{"root": {"label": "market", "value": 100,
          "children": [{"label": "enterprise", "value": 60},
                       {"label": "SMB", "value": 40}]}}
```

Save it (say `tree.json`) and run:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer check-tree tree.json
```

Fix anything it flags (duplicate siblings, children that do not sum) before showing the tree.

Write in the Soothsayer house style. See `docs/house-style.md`.
