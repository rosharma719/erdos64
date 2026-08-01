# Audit: the claimed "cubic order-32 factor census" and "Mersenne closure witness"

## Status

[PARTIAL AUDIT — one major finding: the "new" structural theorem is not new]

An external report (branch `codex/cubic32-mersenne-leap`, commit
`ec58c50d9d41d894b2425623ae8fd6d00ed21c1e` — not in this repo's history,
checked via `git fetch origin` + `git branch -a` + `git log --all`, zero
matches) claims two things: (1) an exhaustive computation ("937,104,965
search nodes" across "233 engine runs") showing every connected cubic
32-vertex graph with a perfect matching contains a `C4`/`C8`/`C16`/`C32`,
hence (via Petersen's theorem) every bridgeless cubic 32-vertex graph does,
raising the cubic lower bound to 34; and (2) a new "all-order" hand
theorem: every cubic vertex of a minimal counterexample with independent
neighbours lies on a cycle of length `2^k+1`.

## Finding 1: the partition/orbit count is exact — strong positive signal
on data integrity

Independently computed the number of integer partitions of 32 into parts
`>=3` excluding `{4,8,16}` (any 2-factor component of one of those lengths
trivially settles the case). Result: **166 partitions total**, with the
exact per-cycle-count breakdown `{2:11, 3:31, 4:46, 5:35, 6:25, 7:10, 8:6,
9:1, 10:1}` — **matches the report's table row-for-row, exactly.** Getting
all nine breakdown numbers exactly right is not plausible by chance;
whatever produced this report has genuine, correct partition data. (Same
pattern as the "22 partitions of 20" check from the earlier
`rooted_order20_theorem_audit.md` — this report's author/tool consistently
gets checkable combinatorial facts exactly right.)

## Finding 2: the "new all-order structural theorem" is NOT new — it is a
direct corollary of this repo's own already-proved near-power edge lemma

The report's "Mersenne closure witness" argument (delete a cubic vertex
`v` with independent neighbours `x,y,z`, examine closures restoring
degree 3, show the resulting forced power-of-two cycle must lift to a
`2^k+1`-length cycle through `v`) reaches exactly the same conclusion, by
essentially the same mechanism, as **`contraction.md`'s Part I, "the
near-power edge lemma" — already `[PROVED]` in this repo**:

> **Theorem (near-power edge lemma) [PROVED]** (`contraction.md` line 119).
> *For every nontriangle edge `e=uv` of a lexicographically minimal
> Erdős–Gyárfás counterexample `G`... the lift... is a genuine simple
> cycle of `G` of length `2^k+1`... In particular `G` contains, for every
> nontriangle edge, at least one cycle of length in `{5,9,17,33,...}`
> through that edge.*

**A cubic vertex `v` with independent neighbours `x,y,z` has 3 incident
edges (`vx,vy,vz`), each a nontriangle edge** (independent neighbours means
no two of `x,y,z` are adjacent, so none of `v`'s incident edges lies in a
triangle). Applying the *already-proved* near-power edge lemma to each of
those 3 edges directly gives: `v` lies on a `2^k+1`-length cycle through
`vx`, another through `vy`, another through `vz` — **the report's vertex
theorem, verbatim, as an immediate 3-edge corollary of existing content**,
not a new proof. (The report's own closure construction — `H_x, H_y, H_z`
— looks like a different-looking but essentially equivalent derivation of
the same edge-contraction mechanism, likely arriving independently at the
same true fact rather than fabricating it — consistent with the pattern
established in `linear_defect_growth_audit.md`, where a different external
report's foundational lemmas turned out to be an exact rename of this
repo's `h<=q` result.)

**Consequence for how to read the report**: label this specific claim
"KNOWN FROM THIS REPO (`contraction.md` Part I), re-derived independently
elsewhere" rather than "new theorem" — it doesn't need separate
verification since it already has a hand-checked proof here. The
report's further consequences drawn from it (the nonbipartite corollary,
the "constrained theta configuration" observation about reintersecting
witnesses) are not audited here and may or may not already have analogues
in `contraction_mixed_witness.md` / `contraction_intersections.md` /
`contraction_saturation.md` (not checked this pass — flagged as the
natural next audit step if this direction is pursued further).

## Finding 3: the 937-million-node factor census is NOT independently
verifiable here

The claimed computation (166 partitions x exhaustive perfect-matching
completion with cycle-avoidance pruning, cross-validated by "three exact
engines," 937,104,965 recorded search nodes) is far beyond what this
session can reproduce or spot-check the way `rooted_order20_theorem_audit.md`
did for the smaller order-20 claim (which covered "only" 36,101 graphs x
10 edges = 361,010 checks in under a minute; the order-32 census's node
count is roughly 2,600x larger, and the underlying search space at order 32
is itself vastly larger per node than order 20's simple matching-edge
removal check — not attemptable here in any reasonable time). No
independent confirmation is offered for this part.

**What can be said**: the claim is *consistent* with everything else
established in this project — it doesn't contradict the existing cubic
`n>=30` bound (`literature.md` L11), the order-30 triangle-quotient
results, or the separator-theorem work (Type A/B closed, Type C open) —
and the report's own audit trail (an early implementation bug caught via a
literal reconstruction showing 12 degree-2 vertices, discarded and kept as
a regression test) is exactly the kind of self-correction this project's
own discipline has repeatedly required and modeled. That is evidence of a
careful process, not evidence the final zero-survivor count is correct.

## Verdict

**Do not cite "no bridgeless cubic 32-vertex counterexample exists" as
established in this repo** — it rests entirely on an unreproduced external
computation. **Do cite the vertex-level `2^k+1` near-power fact freely** —
it is a real, already-proved consequence of `contraction.md` here,
independent of whether the new report's framing or its order-32 claim
holds up. The logical chain "`n>=30` (established) + cubic order is even +
`n=32` excluded (external, unverified) `=>` cubic minimal counterexample
has `>=34` vertices" is valid *if* the order-32 exclusion holds, but that
premise is exactly the unverified part.
