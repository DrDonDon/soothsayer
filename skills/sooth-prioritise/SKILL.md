---
name: sooth-prioritise
description: Prioritise the parts of the problem that matter, on impact, influence, and knowability. Works on whatever structure you built, not just a tree. Use after /sooth-structure and before /sooth-workplan. Emits a kill list with a reason for every part it drops. Refuses to add new parts.
---

You are running the PRIORITISE step of the Soothsayer method. Whatever structure `/sooth-structure` produced, keep only the parts worth the work.

Judge each part on:

- **Impact** — how much the answer changes the outcome.
- **Influence** — how much can actually be affected.
- **Knowability** — whether it can be answered in the time available.

Produce two lists:

- **Keep** — the parts you will work, ranked, with a one-line reason each.
- **Kill** — every part you drop, each with a reason. The kill list is not optional; dropping work silently is how scope creep hides.

Present the keep-or-kill call on each part as **clickable options** so the user can confirm or overturn it with a click (see `docs/asking.md`).

**Refusal.** Do not add new parts. If something is missing, send it back to `/sooth-structure`; do not invent it here.

Write in the Soothsayer house style. See `docs/house-style.md`.
