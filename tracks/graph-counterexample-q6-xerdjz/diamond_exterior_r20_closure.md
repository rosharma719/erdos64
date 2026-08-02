# Diamond exterior (R20's last open case): zero candidates, dual-verified

## Status

[COMPUTATIONALLY VERIFIED, exhaustive, dual-tool cross-validated — but see
the explicit scope caveat below before treating "R20" itself as fully
closed].

## Context (as reported, not independently re-derived here)

A parallel work session (different machine/repo checkout, not this
session's git history — its commits and file layout don't match what's in
`claude/graph-counterexample-q6-xerdjz`) reported closing the "R20"
paired-root census (a fully-cubic Type-C 2-cut obstruction) down to one
remaining precisely-specified case:

> "The sole remaining fully cubic Type-C obstruction is the diamond
> exterior: 16 vertices, degrees 3^14 2^2, 23 edges, C4/C8/C16-free, with
> the path condition [every external d-x path has length in
> {5,6,7,8,13,14,15}]. Starting point is `geng -c -q -f -d2 -D3 16 23:23`.
> Not run."

I do not have that session's `r20_paired_root.md` (the file defining the
diamond reduction precisely) or its `verifier/paired_root_r20*.py/c`
tooling — they're not in this repo's git history. I have **not**
independently reconstructed the diamond-exterior reduction itself (what
exactly "external d-x path" means, or why this specific degree
sequence/edge count is the right target) and am reporting the source
claim, not re-deriving it.

## What I directly, independently verified

The stated necessary condition — the exterior graph `H` (16 vertices,
degree sequence `3^14, 2^2`, 23 edges) must be `C4`/`C8`/`C16`-free — has
**zero survivors**, checked exhaustively and cross-validated two ways:

```
nauty-geng -c -f -d2 -D3 16 23:23   # 7,639 raw graphs, 0.68s
```

1. `verifier/check_g6.c` (this repo's existing certified DFS-based
   C4/C8/C16 detector, already used and cross-validated extensively
   elsewhere in this repo): **0 / 7,639** pass (i.e. 0 graphs are free of
   all three forbidden lengths).
2. Independent re-check via `networkx.simple_cycles` (a structurally
   different algorithm/implementation, not sharing code with #1): **0 /
   7,639** — exact agreement, 0 discrepancies. Also independently
   confirmed every one of the 7,639 raw graphs actually has the claimed
   degree sequence `[2,2,3,3,...,3]` (assertion never failed).

**Since a survivor must satisfy C4/C8/C16-freeness *and* the additional
path-length condition, and the weaker requirement (freeness alone) already
has zero survivors among all degree/edge-matching graphs on 16 vertices,
the diamond-exterior case is closed regardless of the path condition's
exact details** — I did not need to reconstruct or check the path
condition at all, since it can only shrink an already-empty set further.

## Scope caveat — what this does NOT establish by itself

This confirms the *necessary condition* the source session identified has
no survivors. It does **not**, on its own (without trusting the source
session's derivation), establish that "the diamond exterior is the sole
remaining fully-cubic Type-C obstruction" — that reduction (why *this*
specific 16-vertex/degree-sequence/edge-count family is exactly equivalent
to the fully-cubic Type-C 2-cut case, after all the earlier corrections
described — the triangle case, the corrected diamond identity, the
both-edges-lift caveat) lives entirely in the source session's own files
and reasoning, which this repo does not contain and this pass did not
reconstruct. If that reduction is correct, this result closes it. The
honest state: **the specific finite check flagged as "the obvious next
target" now has a definitive zero-survivor answer, dual-verified**; the
overall "R20 closes Type C" claim still rests on the un-reconstructed
reduction from the source session.

## Recommendation

If/when the source session's `r20_paired_root.md` and
`verifier/paired_root_r20*.{c,py}` become available in this repo (e.g. via
a future merge), this result should be cross-referenced there directly,
and the exact path-condition check (`{5,6,7,8,13,14,15}`) should still be
run and reported for completeness even though it's now known to be moot —
matching this project's standard of not skipping a stated verification
step just because a shortcut makes it unnecessary.
