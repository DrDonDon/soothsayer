# Asking the user (clickable options)

When a Soothsayer skill needs a decision or a clarification, ask it with the
**AskUserQuestion** tool so the answer is a click, not a paragraph. This is the
same clickable-tile experience as gstack, and it is much kinder to a
non-technical user than a wall of open prompts.

Rules:

- **One question per call.** Do not batch several questions into one tile set.
- **Two to four concrete options.** Make them real, distinct choices, not
  "yes / no / maybe".
- **Mark the option you would recommend**, and give a one-line reason in its
  description. Put the recommended one first.
- **The user can always pick "Other" and type their own.** Never force a choice
  that does not fit; the tool provides the escape hatch automatically.
- **Use plain text only when the answer is genuinely open**: a name, a date, a
  one-sentence thesis. Anything with a small set of sensible answers should be
  tiles.
- **Short labels** (a few words). Put the detail in the option's description.
- Multi-select is fine when the user can pick several (for example, which framings
  or hypotheses to carry forward).

Keep the Soothsayer house style in the question text and the option descriptions:
plain words, short sentences, no jargon, no em dashes.
