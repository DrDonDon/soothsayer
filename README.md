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

The method is a **double diamond**. It opens the problem wide before defining it,
then opens the answer wide before converging. Divergence then convergence, twice,
so it explores rather than just confirming a first hunch.

1. `/sooth-define` sets the real question and interrogates it until it is sharp.
2. `/sooth-scan` opens the problem wide: several framings, and what you know, what
   is contested, and what nobody knows. It will not settle on one framing.
3. `/sooth-tree` breaks the problem into a clean tree of open questions.
4. `/sooth-prune` cuts to the fifth that matters, and says why it dropped the rest.
5. `/sooth-explore` opens the answer wide: several competing hypotheses per issue,
   including the uncomfortable one. It will not pick a favourite.
6. `/sooth-workplan` designs the charts to tell those hypotheses apart, and names
   what would kill each, before you look.
7. `/sooth-research` gathers evidence for the plan, with a small budget for
   disconfirming inquiry.
8. `/sooth-analyze` fills the charts and works out which hypothesis they favour.
   The checks fire here.
9. `/sooth-synthesize` converges on the answer, and says what it beat.
10. `/sooth-communicate` writes the pack or the briefing paper. It will not soften
    the answer to make the story cleaner.

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
