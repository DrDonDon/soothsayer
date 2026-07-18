# Acknowledgments

Soothsayer is inspired by **gstack** (https://garryslist.org), the skill harness
whose design taught most of the ideas this project rests on. What Soothsayer
borrows, gratefully:

- **Refusals as the feature.** Each skill's constraint matters more than its
  instruction. gstack's skills refuse to overstep (`/ship` may not debate whether
  a feature should exist; `/review` may not commit). Soothsayer's pipeline skills
  refuse in the same spirit — `/scan` may not recommend, `/analyze` may not
  synthesise.
- **Cross-model adversarial review.** gstack runs an independent second model
  against its own work. Soothsayer takes the same idea and makes it a gate, with
  a disagreement-floor and enforced model diversity.
- **Stateless harness, documents as memory.** gstack holds no runtime state; its
  artifacts on disk are the memory, git-tracked and shareable. Soothsayer copies
  that model wholesale.
- **Packaging shape.** The `setup` + `bin/` + markdown-skills layout, and
  clone-and-run distribution, follow gstack's pattern.

The one part Soothsayer adds that gstack does not have is the deterministic gate
engine (reconciliation, citation re-verification, independence tracing). That is
Soothsayer's own contribution; everything around it owes gstack a debt.

Soothsayer is released under the MIT License (see LICENSE). It is an independent
project and is not affiliated with or endorsed by gstack or its authors.
