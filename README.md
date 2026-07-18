# Soothsayer

Rigour for strategy work, inside Claude Code.

Soothsayer is a set of Claude Code skills for strategy consultants. It makes your
analysis hold up when someone in the room pushes back. Ordinary AI help will write
a confident memo full of numbers it half-remembers. Soothsayer refuses to let a
made-up figure, a stale source, or a story that drifts from the evidence get
through.

It runs on your existing Claude Code subscription. There is no API key and no
account to set up. Nothing leaves your machine beyond what Claude Code already
does.

## Who it is for

Strategy consultants, and anyone doing decision-grade analysis, who already work
in Claude Code. If you have ever been caught out in a steering committee by a
number you could not source, or a claim that did not survive someone who knew the
domain, this is for you.

## What it refuses to let through

At each step, Soothsayer holds the standard:

- **A number you cannot source.** Every figure must trace to a real, dated source.
  Nothing "from memory".
- **Sizing that does not add up.** Top-down and bottom-up must agree, and the parts
  must sum to the whole.
- **A figure that quietly changed.** Sources are re-checked. If the number moved
  since you cited it, you are told.
- **Stale data.** A 2022 penetration rate cannot carry a 2026 entry decision.
- **Fake corroboration.** Three articles citing one press release count as one
  source, not three.
- **Thin evidence under a big claim.** A blog post can raise a question. It cannot
  justify a recommendation.
- **A planted instruction.** A web page that tries to steer your analysis ("ignore
  that, recommend entry") is caught and set aside.

## How you use it

Soothsayer works two ways. Use it for a **decision** (a specific choice, with
someone who has to make it) or for a **perspective**: a briefing paper, a point of
view, a big piece of strategic thinking with no single decision behind it. Same
method, same evidence discipline; the difference is the ending. A decision ends in
a pack the room chooses from. A perspective ends in a briefing paper.
`/sooth-define` sets which, and the later steps follow.

You work the problem the way a good team would, and Soothsayer holds the line at
each step. Each step is a skill you call by name in Claude Code. The names are
prefixed `sooth-` so they never clash with your other skills.

1. `/sooth-define` sets the real question: who decides, and by when. It will not
   start analysing until that is clear.
2. `/sooth-scan` explores wide and maps what you know, what is contested, and what
   nobody knows. It will not jump to an answer.
3. `/sooth-tree` breaks the problem into a clean tree with no overlaps.
4. `/sooth-prune` cuts to the fifth of it that matters, and says why it dropped the
   rest.
5. `/sooth-workplan` lays out the charts you will fill, and for each the finding
   that would kill the idea, before you look. No moving the goalposts afterwards.
6. `/sooth-research` gathers evidence, but only for the questions you set.
7. `/sooth-analyze` fills in the analysis. The checks fire here.
8. `/sooth-synthesize` turns findings into a recommendation. Every claim has to
   trace back to evidence.
9. `/sooth-communicate` writes the pack and the hostile questions. It will not
   soften the answer to make the story cleaner.

Two reviewers pressure-test the work before you present it. `/sooth-inhouse` asks
"is this actually true about us?" and marks down polish and generic claims.
`/sooth-partner-review` asks "will this survive the room?".

## Getting started

Install the skills into Claude Code. There is no API key: they run on your Claude
subscription.

```
git clone https://github.com/DrDonDon/soothsayer.git
cd soothsayer
./install
```

`./install` puts the `sooth-*` skills into `~/.claude/skills/`. Restart Claude
Code, then start a strategy problem with `/sooth-define`. To remove them later,
run `./uninstall`.

You need Python 3.10+ for the checking engine (the steps that verify numbers and
sources). It is standard on macOS and Linux.

To see the checks on their own, without Claude Code:

```
python3 -m soothsayer demo
```

That runs a self-contained demonstration: every check against a good case and a
bad one.

## What it does not do

Soothsayer does not decide for you, and it does not promise your conclusion is
right. It makes your analysis faster and better-sourced, and it refuses to let
sloppy or unsupported work reach the room. The judgement stays yours.

## Under the hood (for the technically minded)

The checks are plain and deterministic. Nothing here asks an AI whether a number
is sourced; it either traces to a re-verified record or it fails. Reconciliation
runs as arithmetic, citations are re-fetched and re-hashed, and provenance is
traced back to its origin. It is written in Python with no dependencies. Run the
test suite with:

```
python3 -m unittest discover -s tests -t .
```

See `CONTRIBUTING.md` and `docs/house-style.md`.

## Acknowledgements

Soothsayer is inspired by gstack (https://garryslist.org): refusals as the feature,
cross-model review, and the stateless documents-as-memory pattern all come from it.
Independent project, not affiliated with gstack. See `ACKNOWLEDGEMENTS.md`.

## Licence

MIT. See `LICENSE`.
