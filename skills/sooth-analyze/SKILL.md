---
name: sooth-analyze
description: Fill the ghost charts with gathered evidence and run the machine checks. Use after /sooth-research and before /sooth-synthesize. The reconciliation, citation, staleness, independence, tier-floor, and injection checks fire here. Refuses to synthesise or recommend.
---

You are running the ANALYZE step of the Soothsayer strategy method.

Fill each ghost chart with the evidence in the store. As you go, run the Soothsayer checks and fix what they flag:

```
PYTHONPATH="$(cat ~/.soothsayer/root)" python3 -m soothsayer gate --store .soothsayer --horizon <decision-date> --frozen <sources.json>
```

The checks confirm: no recalled numbers, the sizing reconciles, cited figures still hold when re-fetched, sources are fresh enough for the decision horizon, corroboration is genuinely independent (not three outlets citing one press release), thin sources do not carry recommendations, and no source carries a planted instruction.

As each chart fills, ask which of the competing hypotheses from `/sooth-explore` it **favours** and which it **weakens**. Actively look for the alternative explanation: could a different hypothesis fit the same data? Do not stop at the first reading that suits your prior. Holding several hypotheses through the workplan was so this step can tell them apart, not so you can wave the survivors through.

**Refusal.** Do not synthesise or recommend yet. That is `/sooth-synthesize`. Fill the charts, pass the checks, and report what the charts show for each hypothesis.

If a result will not fit its ghost chart, that is information. Send it back to `/sooth-workplan` rather than reshaping the chart to fit the finding.

Write in the Soothsayer house style. See `docs/house-style.md`.
