---
name: sooth-research
description: Gather evidence into the Soothsayer store. Mostly fills the workplan's ghost cells, with a small budget for open, disconfirming inquiry. Every record must trace to a real, dated source, never a recalled number. Use after /sooth-workplan and before /sooth-analyze. Refuses to let off-plan gathering take over, but routes genuine surprises back rather than discarding them.
---

You are running the RESEARCH step of the Soothsayer strategy method.

Most of your gathering fills the ghost cells the workplan named. But keep a **small budget for open, disconfirming inquiry**: actively look for evidence that would kill one of your live hypotheses, or surface a framing the earlier steps missed. This is within reason, not a licence to boil the ocean; the bulk of the work stays on-plan.

For every fact, record: the claim, the source URL, the publication date, a verbatim extract, and the source tier (T1 filings and primary data, T2 named trade press, T3 secondary press and blogs). Never record a number "from memory".

**Refusal.** Do not let off-plan gathering take over; the plan exists for a reason. But do not bury a genuine surprise either. If open inquiry turns up a finding that reframes the problem, send it back to `/sooth-define` or `/sooth-structure` rather than discarding it.

Write each record as JSON and add it to the store:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer add-evidence --store .soothsayer --file record.json
```

The store enforces provenance: a numeric claim with no source and no hash is refused. That is the point, not a bug.

Write in the Soothsayer house style. See `docs/house-style.md`.
