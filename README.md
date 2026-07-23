# Soothsayer

Rigour for strategy work, inside Claude Code.

Soothsayer is a set of Claude Code skills for strategy consultants. It runs a real
problem-solving method, the kind a good strategy team uses, and it refuses to let a
made-up number, a stale source, or a story that drifts from the evidence get
through. It reasons harder than a person would: for an AI a line of reasoning is
cheap, so it runs several and cross-checks them.

It runs on your existing Claude Code subscription. No API key, no account.

## Who it is for

Strategy consultants, and anyone doing decision-grade thinking, who already work in
Claude Code. It works two ways: for a **decision** (a specific choice, with a
decider) or a **perspective** (a briefing paper or point of view, with no single
decision behind it).

## The process

Soothsayer runs as a **double diamond**: it opens the problem wide before defining
it, then opens the answer wide before converging. You move through it one skill at
a time, and it holds the standard at each step.

```
The problem      DEFINE  ->  STRUCTURE  ->  PRIORITISE
                 (open wide)          (converge)

The answer   WORKPLAN -> RESEARCH -> ANALYSE  ->  SYNTHESISE  ->  COMMUNICATE
                             (open wide)          (converge)

Reviewed after   DEFINE, STRUCTURE, and SYNTHESISE
```

## The skills

Each step is a skill you invoke by name in Claude Code. The names are prefixed
`sooth-` so they never clash with your own. Where it can, it asks its questions as
clickable options, so you pick a tile rather than typing.

| Skill | What it does |
|---|---|
| `/sooth-define` | Clarifies the problem and tests whether it is worth solving, with hard Socratic questions. The most important step. |
| `/sooth-client-context` | Understands the client: what they really want, their biases and politics, and where the work must be guarded against telling them what they want to hear. Run early. |
| `/sooth-structure` | Structures the problem the way that fits it: a tree, a 2x2, a system map, a causal chain. Not always a tree. |
| `/sooth-prioritise` | Keeps the parts that matter, on impact, influence, and knowability, and says why it dropped the rest. |
| `/sooth-workplan` | Pre-registers the analyses, and what finding would change your answer, before you look. |
| `/sooth-research` | Gathers evidence into a store, every figure traced to a real, dated source. |
| `/sooth-analyze` | Reasons over the evidence with a range of methods, in parallel, to test competing answers. |
| `/sooth-synthesize` | Converges on the answer, and says what it beat. |
| `/sooth-communicate` | Writes the decision pack or the briefing paper. |
| `/sooth-inhouse` | Reviews from the inside: is this true about us? |
| `/sooth-partner-review` | Reviews as the partner: will this survive the room? |

## How it reasons

Ordinary AI help writes one plausible line of argument. `/sooth-analyze` runs
several and cross-checks them, because a reasoning step is cheap:

- **Deductive** and **inductive**: from principles to conclusions, and from cases
  to patterns.
- **Abductive**: the best explanation for the evidence.
- **Analogical**: where has this played out before, and how did it end?
- **Causal** and **systems**: what drives what, and the second-order effects.
- **Probabilistic**: base rates and ranges, not point estimates.
- **Falsification**: assume the thesis is wrong and try hard to disprove it. A favourite that was never attacked is advocacy.
- **Thought experiments**: pre-mortems, inversions, "what would have to be true".
- **First-principles**: strip it to fundamentals and rebuild.

Where the methods disagree, that is a signal, and it chases it.

## What it refuses to let through

- **A number you cannot source.** Every figure traces to a real, dated source.
- **Sizing that does not add up.** Top-down and bottom-up must agree.
- **A figure that quietly changed.** Sources are re-checked; if it moved, you are told.
- **Stale data.** A 2022 figure cannot carry a 2026 decision.
- **Fake corroboration.** Three outlets citing one press release count as one.
- **Thin evidence under a big claim.** A blog can raise a question, not settle it.
- **A planted instruction** in a web page trying to steer the analysis.

## Getting started

Install the skills into Claude Code. No API key: they run on your Claude
subscription.

```
git clone https://github.com/DrDonDon/soothsayer.git
cd soothsayer
./install
```

Restart Claude Code, then start with `/sooth-define`. Remove them later with
`./uninstall`. You need Python 3.10+ for the checking engine (standard on macOS and
Linux).

To see the checks on their own, without Claude Code:

```
python3 -m soothsayer demo
```

## Under the hood

The checks are plain, deterministic tools, not an AI guessing whether a number is
sourced. Reconciliation runs as arithmetic, citations are re-fetched and re-hashed,
provenance is traced to its origin. Python, no dependencies. Run the tests with
`python3 -m unittest discover -s tests -t .`. See `skills/PIPELINE.md`,
`docs/house-style.md`, and `CONTRIBUTING.md`.

## Acknowledgements

Inspired by gstack (https://garryslist.org): refusals as the feature, cross-model
review, and the stateless documents-as-memory pattern. Independent project, not
affiliated with gstack. See `ACKNOWLEDGEMENTS.md`.

## Licence

MIT. See `LICENSE`.
