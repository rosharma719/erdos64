# Audit: the claimed "cubic order-34 factor census" and "Two-witness theorem"

## Status

[PARTIAL AUDIT — partition count independently confirmed exact after fixing
a bug in my own first attempt; the "Two-witness theorem" is, like the prior
"Mersenne closure witness" claim, not new content]

An external report (attributed to "GPT," not present in this repo's history
— no matching branch/commit found via `git fetch origin` + `git branch -a`
+ `git log --all`) extends the previously-audited order-32 factor census
(`cubic32_mersenne_audit.md`) to order 34, citing the Candráková–Lukoťka
2-factor theorem to reduce the search to 2-factor completions, and claims:
(1) "227 partitions of 34 into factor-cycle lengths avoiding {4,8,16,32},
only 127 of which can represent the theorem-selected factor" (breakdown:
109 partitions with <=4 parts, plus 18 more with 5-6 parts that are also
triangle-free); (2) an exhaustive computation ("648,370,974 endpoint
nodes") finding zero survivors; (3) a "Two-witness theorem" — every cubic
vertex of a minimal counterexample lies on at least two distinct cycles of
length `2^a+1` and `2^b+1`, arising from two different neighbour pairs;
(4) a boxed conclusion that a cubic minimal counterexample, if one exists,
has `>=36` vertices — contingent on the order-32 exclusion (itself already
flagged "do not cite" in `cubic32_mersenne_audit.md`) also holding.

## Finding 1: the partition count is exact — matches, after fixing a bug in
my own first attempt

Independently computed the number of integer partitions of 34 into parts
`>=3` excluding `{4,8,16,32}`. My first attempt used
`range(3, 34)` for the candidate part sizes, which silently excludes 34
itself (a single-cycle Hamiltonian "factor" `[34]`) — an off-by-one from
Python's exclusive-upper-bound `range`, not a mathematical error in the
approach. This gave 226 total / 108 with `<=4` parts, one short of the
report's 227/109 in both figures (the "18" for 5-6-part triangle-free
factors matched exactly even before the fix, since a single-cycle `[34]`
factor is never in that bucket). Diagnosed and fixed to `range(3, 35)`;
rerun gives:

- **227 total partitions**, breakdown by cycle count
  `{1:1, 2:12, 3:37, 4:59, 5:50, 6:37, 7:16, 8:10, 9:3, 10:2}`.
- **<=4 parts: 109.**
- **5-6 parts, triangle-free (no part equal to 3): 18.**
- **Sum: 127.**

All four numbers match the report exactly, including the full nine-bucket
breakdown by cycle count. As with the order-32 report's 166-partition
table, getting every bucket exactly right is a strong positive signal
about the underlying data's integrity — whatever produced this also has
correct partition arithmetic here, once my own off-by-one was fixed. (The
bug was mine, in the independent verification script — not a defect found
in the external report.)

## Finding 2: the "Two-witness theorem" is not new — it restates (and is in
fact slightly weaker than) an already-derived 3-edge corollary from this
repo's own machinery

The report's claim — every cubic vertex with independent neighbours lies
on `>=2` distinct `2^k+1`-length cycles, from two different neighbour
pairs — is **the same mechanism already identified in
`cubic32_mersenne_audit.md` Finding 2**: applying `contraction.md`'s
already-`[PROVED]` near-power edge lemma to each of a cubic vertex `v`'s 3
incident edges (all nontriangle edges, when `v`'s neighbours are
independent) gives **three** distinct `2^k+1`-length witness cycles
through `v` — one per incident edge — not merely two. The "Two-witness
theorem" is thus implied outright by the "at least 3" fact already on
record; asking for 2 of the 3 available witnesses is a strictly weaker
statement.

Checked the three files flagged as the natural next audit step in
`cubic32_mersenne_audit.md` (`contraction_mixed_witness.md`,
`contraction_intersections.md`, `contraction_saturation.md`) for whether
they contain a comparison of two of these three per-vertex witnesses
against each other specifically (as opposed to the single-edge lemma
alone). They do: `contraction_mixed_witness.md` Part IV (the "NPT theta"
analysis, orbits T1/T2a/T2b/T2c) is exactly a case analysis of what
happens when two of a Type-N vertex's three witness paths are compared
pairwise (together with the closed-neighbourhood witness `Q_{pq}` from
`contraction_neighborhood.md`) — already `[PROVED]` there, with the
conclusion that every such pairwise combination is "unconditionally safe"
(never itself a power of two) rather than a source of contradiction.
`contraction_intersections.md` and `contraction_saturation.md` extend this
further (non-clean witness overlaps, theta-bridge saturation) but do not
add a distinct "two-witness existence" claim beyond what the single-edge
lemma already supplies three times over.

**Consequence for how to read the report**: label this claim, like the
order-32 report's vertex theorem, "KNOWN FROM THIS REPO
(`contraction.md` Part I + `contraction_mixed_witness.md` Part IV),
re-derived independently elsewhere, and in fact weaker than the 3-witness
statement already on record" — it needs no separate verification. This is
the same pattern noted twice already in this project (`linear_defect_
growth_audit.md`'s `h<=q` rename; `cubic32_mersenne_audit.md`'s Mersenne
witness): independently-generated reports keep re-deriving true facts
this repo already has, under new names.

## Finding 3: the 648-million-node census is NOT independently verifiable
here, and is contingent on the unverified order-32 result

The claimed computation is larger than the already-unverifiable order-32
census (937,104,965 nodes) audited previously, and this session has no
more ability to reproduce or spot-check it now than then — nothing here
changes that assessment. Beyond its own scale, **the report's final
boxed conclusion ("cubic minimal counterexample has `>=36` vertices") is
explicitly a two-stage claim**: it requires *both* this order-34 result
*and* the order-32 result from the prior report to hold (order 32 and
order 34 both excluded, cubic order is even, so the next open order is
36). The order-32 exclusion was already flagged "do not cite" in
`cubic32_mersenne_audit.md`; that verdict is unchanged, so the order-34
report's own conclusion inherits the same caveat even if the order-34
computation itself is entirely correct.

## Verdict

**Do not cite "no bridgeless cubic 34-vertex counterexample exists," nor
the "cubic minimal counterexample has `>=36` vertices" conclusion, as
established in this repo** — both rest on unreproduced external
computations, and the latter additionally inherits the already-flagged
order-32 gap. **Do cite the underlying vertex-level `2^k+1` witness fact
freely** (as already noted in `cubic32_mersenne_audit.md`) — it, and now
also its "two witnesses" special case, are real, already-proved
consequences of `contraction.md` and `contraction_mixed_witness.md`,
independent of whether this new report's order-34 claim holds up. The
partition-count arithmetic (227/109/18/127) is independently confirmed
exact, which is corroborating-but-not-dispositive evidence for the rest of
the report, exactly as with the order-32 case.
