# Type-T completion obstruction

**Status (2026-07-28): OBSTRUCTION — BOUNDED METRIC MOTIFS, GLOBAL
CERTIFICATE SUPPORT.**  Exact completion failure is governed by conflict
hyperedges representing `C4`, `C8`, and `C16`.  Every individual conflict has
uniformly bounded total core-path support, but the aggressively reduced
certificate at `(j,a,c)=(4,2,2)` still uses the entire deficit set.  Thus the
data support a bounded-metric-motif program, not yet a bounded-coordinate
window theorem.

## 1. Conflict hypergraph

Let `G0` be an expanded ordinary port core, let `D` be its intrinsic set of
degree-two vertices, and let `K` be the graph of individually safe completion
edges.  A vertex of the conflict hypergraph is an edge of `K`.  A hyperedge is
the set of completion edges on one ordinary `C4`, `C8`, or `C16` in `G0+M`.
The completion problem is precisely:

> Does `K` have a perfect matching that contains no conflict hyperedge?

The ordinary compatibility graph alone cannot answer this.  Every `j=4`
compatibility graph has a perfect matching; the obstruction begins with two
or more completion edges.

## 2. Alternating-path decomposition [PROVED]

Let `M` be a perfect matching on `D`, disjoint from `E(G0)`, and let `C` be a
simple cycle of `G0+M`.  Put

\[
 k=|E(C)\cap M|.
\]

Deleting these `k` matching edges from `C` leaves exactly `k` pairwise
vertex-disjoint, nonempty simple paths `P1,...,Pk` in `G0`, cyclically joined
by the deleted matching edges, with

\[
 \sum_i |E(P_i)|=|C|-k.
\]

Indeed, deleting `k` distinct edges from a cycle produces `k` path
components, and all remaining edges lie in `G0`.  No path component is empty:
two consecutive matching edges would share their intervening vertex, which
is impossible because `M` is a matching.  Conversely, any such cyclic
collection reconstructs a simple cycle.

The bare core has no dyadic cycle.  After individually unsafe matching edges
are removed, a forbidden cycle cannot have `k=0` or `k=1`.  Consequently:

| cycle | possible `k` | total core-path length `L-k` | maximum |
|---|---|---|---:|
| `C4` | 2 | 2 | 2 |
| `C8` | 2, 3, 4 | 6, 5, 4 | 6 |
| `C16` | 2,...,8 | 14,...,8 | 14 |

This bound is uniform in `j,a,c`.  It bounds total core metric support, not
the coordinate diameter: matching chords may join two arbitrarily distant
short windows.

Before quotienting cyclic order, reversal, or core topology, the possible
positive ordered core-path length compositions number 1 for `C4`, 12 for
`C8`, and

\[
 \sum_{k=2}^{8}\binom{15-k}{k-1}=609
\]

for `C16`.  This is a finite motif alphabet at the metric-composition level.

### Two-chord criterion

For `k=2`, matching edges form a `C_L` exactly when an endpoint pairing admits
two internally vertex-disjoint core paths whose lengths sum to `L-2`.  On one
subdivided branch, let four endpoints occur as

\[
 x_1<x_2<x_3<x_4.
\]

A crossing or nested pairing closes a cycle of length

\[
 (x_2-x_1)+(x_4-x_3)+2.
\]

Thus the exposed gap sum may not be `2,6,14` in a `C4/C8/C16`-free matching.
This is a genuine coordinate obstruction, but it covers only the two-chord
part of the hypergraph.

## 3. Reduced proof-dependency core

The verified final `(4,2,2)` CNF has 2,033 variables and 109,419 clauses.
Repeatedly extracting its `drat-trim` proof core, freshly reproving the
smaller formula, and independently verifying the new trace reaches the fixed
point:

| item | count |
|---|---:|
| retained clauses | 10,548 |
| matching/cardinality clauses | 3,289 |
| cycle cuts | 7,259 |
| `C4`-sourced cuts | 331 |
| `C8`-sourced cuts | 2,283 |
| `C16`-sourced cuts | 4,645 |

This is a 90.36% clause reduction.  It is an aggressively reduced
proof-dependency core, not a clause-minimal MUS.  Its DRAT proof independently
verifies.  Removing every cut of any one of the three length families makes
the reduced formula SAT; keeping only any single family is also SAT.  Hence
`C4`, `C8`, and `C16` all participate essentially in this particular
contradiction.

The negative structural result is equally important:

- all 76 deficient vertices occur in retained cycle cuts;
- 642 of 703 individually safe matching variables occur;
- all 76 vertex-cardinality blocks retain clauses;
- 73 of 76 explicit at-least-one clauses remain.

The three missing at-least-one clauses are at `A_right:16`, `A_right:19`, and
`A_right:21`, but their cardinality blocks still retain other clauses.  This
certificate is therefore global.  It does not live in a bounded coordinate
window near either port.

Every retained cut is mapped back to its matching endpoints, all realizable
source lengths, a canonical ordinary-cycle witness, named exporter paths, and
separate `A/B/C/D` coordinate hulls in
`data/type_t_port_completion/j4_a2_c2_reduced_core_analysis.json.gz`.

## 4. Motif diversity

The reduced `(4,2,2)` core contains 830 distinct coarse clusters when a motif
is keyed by source length, number of matching chords, and its set of named
core paths.  This is already incompatible with a proof based on one obvious
same-branch pattern.

The completed 324-class sweep sharpens this conclusion.  A fresh verified
DRAT dependency core was extracted and semantically mapped for every class.
The cores retain 161 to 20,070 clauses (median 6,594), removing 86.10% to
99.63% of the corresponding final formulas.  Their cycle cuts contain 12,544
distinct coarse topology-aware motif keys across the family.  `C8` and
`C16` cuts occur in all 324 cores, while `C4` cuts occur in 320.

Some extreme translations do admit small local certificates.  For example,
`(a,c)=(54,7)` has a 161-clause dependency core with 55 cycle cuts and no
retained `C4` cut; `(51,7)` uses only 23 deficient vertices in its retained
cuts.  These exceptions do not yield a uniform window theorem.  In 284 of
324 classes the retained cuts touch all 76 deficient vertices, and the
median support is all 76.  Thus the negative bounded-window result is not an
artifact of the single `(2,2)` fixed-point reduction: global certificate
support is typical, even though small proof-relative cores occur near some
boundaries.

An additional discovery sample—a `C4/C8`-free exact-domain matching—contained
1,653 `C16` cycles with matching-chord counts

\[
 85,198,504,469,294,97,6
\]

for `k=2,...,8`.  Its 85 two-chord cycles used 71 different named-path
support types, and only four were wholly inside `A_right`.  This sample is
discovery evidence rather than a manifest artifact, but it reinforces the
certificate conclusion: bounded *total path support* is the right invariant;
bounded global position is not yet supported.

## 5. Adversarial `j=5` search

The bounded `j=5` campaign used randomized individually safe matchings,
exact-incremental 2/3/4-edge switches, tabu/annealing, and beam refinement.
The strongest saved near miss is `(j,a,c)=(5,2,2)`:

\[
 (\#C_4,\#C_8,\#C_{16})=(0,0,1270).
\]

It also has at least 10,000 `C32`s, at least 10,000 `C64`s, and a `C128`
witness.  All 78 matching edges occur in `C16`; their `C16` participation
counts have minimum/median/maximum `39/78/118`.  An independent NetworkX
recount verifies order 167, size 251, connectedness, degree distribution
`3^166,4^1`, and the exact short profile.

This is materially stronger than the initial `j=5` baselines, but it is not
close to a counterexample in a localized sense: the `C16` residue covers the
entire matching.

## 6. What is and is not proved

The alternating-path lemma gives a uniform finite metric-composition alphabet
for short conflicts.  It does **not** show that every perfect matching
contains one of them, nor does the `j=4` computation alone imply an all-`j`
theorem.  A parametric closure still needs one of:

1. a finite list of topology-aware alternating-path motifs meeting every
   perfect matching;
2. a forced periodic structure for `C4/C8`-free partial matchings followed by
   a `C16` closure;
3. a matching-theoretic dual certificate for the conflict hypergraph.

Added vertices, degree five, and `Q` remain outside this analysis.
