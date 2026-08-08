# Soothsayer reasoning protocol

How `/sooth-analyze` solves each part of the structure. The unit of work is the
**node**, one part of whatever `/sooth-structure` built: a branch of an issue tree,
a cell of a 2x2, a link in a causal chain. The old habit was to spray ten reasoning
methods thinly across a few big questions. Thin spraying is its own kind of brute
force. This protocol grinds each node to a real answer instead.

Depth per node, not breadth of options. A branch is done when it reaches a
mechanism-level answer or an honest "not yet answerable", never a hand-wave.

## The per-node loop

Work the surviving (prioritised) nodes in dependency order, leaves first. Nodes that
`/sooth-prioritise` dropped are not solved; they carry only their kill-reason.

For each node:

1. **Frame.** State the node as one sharp question. Say what a real answer would even
   look like: a number, a mechanism, a judgement.
2. **Decompose.** Break the node into its own drivers. If it does not decompose
   cleanly and cannot be answered directly, it is a candidate for recursion (deferred
   to v2) or for the research callback below.
3. **Pick the method that fits.** Choose the one or two reasoning methods that suit
   this node and push them hard. A sizing question wants probabilistic reasoning and a
   top-down/bottom-up reconciliation. A defensibility question wants causal and
   game-theoretic reasoning and an analogy. Do not run all ten thinly. Depth comes
   from grinding one line, not from touching many.
4. **Reason to a "so what".** Reach a mechanism-level conclusion, not a restatement.
   Name the driver that dominates. Give a range, not a point estimate.
5. **Stress it.** Steelman the opposite, take the answer to its second order, and try
   to disconfirm it. This is the falsification method, run per node rather than once at
   the end. An answer you only tried to confirm has not been tested.
6. **Verdict and depth bar.** Record the answer with its confidence and the single
   fact or assumption that would flip it. Refuse and send the node back down if the
   answer is generic (it would fit any company), a restatement of the question, or
   unsupported by evidence or a named mechanism.
7. **Roll up (issue trees only).** A parent is solved once its surviving children pass
   the bar. The parent runs the loop again with the children's answers as its input:
   do they jointly answer the parent, where do they conflict, which child dominates. A
   contradiction between children is not averaged away. It is the parent's key tension,
   and if it drives the answer it is flagged for `/sooth-synthesize`. For a hypothesis
   tree the parent is true or false on the evidence, not a function of child verdicts,
   so there is no roll-up: each hypothesis node is solved directly, and its children
   are supporting sub-claims. For non-tree structures (2x2, spectrum, map) solve each
   node with steps 1 and 3 to 6 and skip roll-up; `/sooth-synthesize` reads the solved
   nodes directly.

## The depth bar

A node answer passes when it:

- names the dominant driver or the mechanism,
- gives a range rather than a single number, and
- states the one thing that would change it.

It fails, and goes back down, when it:

- restates the question,
- is generic enough to fit any company or market, or
- rests on no evidence and no named mechanism.

## No fabricated depth

If a node cannot be answered from the evidence in the store, the answer is an explicit
**"unresolved, needs X"**, never a manufactured mechanism. The depth bar must never
push the reasoning to invent support it does not have. Unsupported depth is the exact
failure Soothsayer exists to stop. An honest "unresolved" is a pass, and it routes the
gap to research.

## The research callback

The harness is stateless. Skills share nothing but files, so there is no live callback.
When a node needs evidence the store does not hold, do not recall it (the T0 ban) and do
not settle for "unresolved" if the gap is fillable. Instead:

1. `/sooth-analyze` writes the gap to the analysis artifact as an open item: the
   sub-question and what source would answer it.
2. `/sooth-research` fills the `.soothsayer` store from real, dated sources.
3. `/sooth-analyze` runs again, now reading the updated store, and closes the node.

This is a document-mediated loop, not an in-process call. Set a budget: a small number
of callback rounds per run, so the loop terminates. Research fills the store; analyse
decides whether to close the node or ship it as a named gap.

## The artifact

`/sooth-analyze` writes `analysis.json` so the solved tree survives to
`/sooth-synthesize`, which is a separate, stateless invocation. This is the same
documents-as-memory pattern as `structure.json` and `synthesis.json`. Shape:

```json
{
  "nodes": [
    {
      "node_id": "market-size",
      "question": "How large is the serviceable market by 2028?",
      "so_what": "Bounded at $2-3bn; the binding driver is seat penetration, not price.",
      "method": ["probabilistic", "bottom-up reconciliation"],
      "confidence": "medium",
      "flip_condition": "Penetration above 40% would push it past $4bn.",
      "children": [],
      "unresolved": false,
      "evidence_ids": ["<id1>", "<id2>"]
    }
  ],
  "open_items": [
    {"node_id": "churn-driver", "needs": "cohort retention by segment, 2024-2026"}
  ]
}
```

`unresolved: true` nodes carry an `open_items` entry instead of a settled `so_what`.
A formal typed artifact and a deterministic `check-analysis` gate are deferred; for now
the file is a plain document the skill emits, like the other steps.

## The boundary

Solving a node is not recommending. `/sooth-analyze` still holds competing hypotheses
and still refuses to pick the overall answer. Converging a sub-question is not
converging the strategy. The recommendation is `/sooth-synthesize`, and it earns its
convergence from this work.

Write in the Soothsayer house style. See `house-style.md`.
