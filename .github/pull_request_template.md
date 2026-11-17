## What this adds

<!-- One or two sentences. List new claim / open-problem ids. -->

## Labels and evidence

- [ ] Every new result has a claim file in `kb/claims/` with a label and evidence paths
- [ ] No label was upgraded without new evidence; history lines added where labels changed
- [ ] Literature citations state their verification level (read / abstract / secondary)
- [ ] Computations are reproducible from the repo (command, parameters, counts recorded)

## Hygiene

- [ ] Only additive changes, or edits explained in `## History`
- [ ] No hash-locked file edited
- [ ] `python tools/kb.py index` run; `python tools/kb.py check` prints OK
- [ ] `kb/STATE.md` updated if the big picture changed
