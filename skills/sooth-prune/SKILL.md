---
name: sooth-prune
description: Cut a strategy issue tree down to the few branches that matter, on impact, influence, and knowability. Use after /sooth-tree and before /sooth-workplan. Must emit a kill list with a reason for every branch it drops. Refuses to add new branches.
---

You are running the PRUNE step of the Soothsayer strategy method.

Take the issue tree and keep only the branches worth the team's time. Judge each on three things:

- **Impact**: how much the answer changes the decision.
- **Influence**: how much the team can actually affect it.
- **Knowability**: whether it can be answered in the time available.

Produce two lists:

- **Keep**: the branches you will work, ranked, with a one-line reason each.
- **Kill**: every branch you drop, each with a reason. The kill list is not optional. Dropping work silently is how scope creep hides.

**Refusal.** Do not add new branches. If the tree is missing something, say so and send it back to `/sooth-tree`; do not quietly invent a branch here.

Write in the Soothsayer house style. See `docs/house-style.md`.
