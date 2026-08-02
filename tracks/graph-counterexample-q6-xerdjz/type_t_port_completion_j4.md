# Type-T same-vertex completion at `j=4`

**Status (2026-07-28): COMPLETION — ALL ORDINARY `j=4` INSTANCES
CLOSED.**  Every one of the 324 valid expanded ordinary cores has no
same-vertex minimum-degree-three completion avoiding all power-of-two cycle
lengths.  The completed graph would be cubic except for the intrinsic
degree-four vertex `z0`; the precise claim is therefore minimum degree three,
not regular cubicity.

This is a finite theorem for the entire `j=4` translation family.  It is not
an all-`j` theorem and it says nothing about added vertices, degree five, or
placement of `Q`.

## 1. The theorem

Let `G(4,a,c)` be the expanded ordinary Type-T `E2_parallel` port core from
`verifier/type_t_port_core_export.py`, where

\[
  2\le a\le55,\qquad 2\le c\le7.
\]

Its 76 deficient vertices are intrinsically exactly its degree-two vertices.
A same-vertex completion is therefore a perfect matching on this set, using
no core edge.  Adding such a matching gives a simple graph of order 87 and
size 131 in which `z0` has degree four and every other vertex has degree
three.

The exact computation proves:

> **Finite `j=4` completion theorem.** For every valid `(a,c)`, every
> same-vertex completion of `G(4,a,c)` contains a power-of-two cycle.  More
> precisely, a matching using an individually unsafe edge immediately closes
> a `C4`, `C8`, `C16`, `C32`, or `C64`; every perfect matching left after
> that screening contains a `C4`, `C8`, or `C16`.

All higher-order rejection clauses in the completed sweep came from literal
ordinary `C4`, `C8`, or `C16` witnesses.  The detector nevertheless checked
`C4,C8,C16,C32,C64` in every proposed completion.

## 2. Ordinary-core canonicalization

Rooted, path-coloured inequivalence does not by itself settle equivalence of
the relaxed ordinary completion instances.  The 324 expanded cores were
therefore canonicalized only after forgetting the Type-T root and path
colours.  This is the exact equivalence relation relevant to the completion
problem because degree is intrinsic and an ordinary graph isomorphism
preserves the deficient set, perfect matchings, and cycle lengths.

The result is unexpectedly rigid:

| quantity | result |
|---|---:|
| rooted translations | 324 |
| ordinary uncoloured isomorphism classes | 324 |
| class sizes | 324 classes of size 1 |
| automorphism groups | 324 of order 1 |
| explicit source-to-representative maps | 324 identities |
| explicit source-to-canonical maps | 324 verified maps |

Dense nauty canonical labeling, sparse nauty, Traces, and `shortg` agree on
the class count.  NetworkX independently verified every emitted map and
every trivial automorphism group.  Sorted all-vertex distance profiles and
20-round Weisfeiler--Lehman hashes also separate all 324 graphs; these latter
invariants are corroboration, not the canonical proof.

There is a structural explanation.  Suppressing all degree-two paths gives
an intrinsic weighted multigraph.  Its variable edge lengths are

\[
 a-1,\quad 56-a,\quad c-1,\quad 8-c,
\]

along the two port branches, while the parallel port routes have fixed
lengths 2 and 7.  The unique degree-four vertex and the asymmetric fixed
kernel distinguish the `z0`, `w_AC`, and `w_BD` sides.  Direct inspection of
this weighted kernel then fixes the long `A` branch and short `C` branch.
A branch reflection in an automorphism would require `2a=57` or `2c=9`,
both impossible over integers; exchanging `A` and `C` is incompatible with
their fixed total lengths.  Once the kernel and weights are fixed, every
subdivision vertex is fixed.  Thus `(a,c)` is intrinsic even in the
uncoloured ordinary graph.

The canonical graph streams and all maps are preserved in
`data/type_t_port_completion/j4_classes/`.

## 3. Exact conflict-hypergraph search

For each core, first remove every candidate completion edge that by itself
closes a power-of-two cycle.  Give each remaining safe edge `e` a variable
`x_e` and impose exactly one selected edge at each deficient vertex.  For a
SAT model, materialize the completed graph and find its shortest
power-of-two cycles.  If a cycle uses matching edges `e1,...,ek`, add the
sound conflict clause

\[
 \lnot x_{e1}\lor\cdots\lor\lnot x_{ek}.
\]

The loop is exact: each cut forbids only matchings containing a witnessed
ordinary cycle, and final UNSAT exhausts the remaining perfect matchings.
Enumeration caps affect how many valid cuts can be learned from one model,
not the soundness of any cut or the final conclusion.

| exact quantity across 324 classes | minimum | median | maximum | total |
|---|---:|---:|---:|---:|
| safe completion edges | 656 | 749 | 843 | 243,581 |
| SAT variables | 1,892 | 2,171 | 2,453 | 706,119 |
| models checked | 1,105 | 2,735.5 | 5,939 | 951,844 |
| learned cycle clauses | 38,284 | 122,644.5 | 310,824 | 43,094,034 |
| final CNF clauses | 42,154 | 126,970.5 | 315,648 | 44,481,648 |
| CEGAR seconds | 17.28 | 64.87 | 277.50 | 23,301.90 |

The 951,844 rejected models split by shortest witnessed cycle as 166,403
`C4`, 759,578 `C8`, and 25,863 `C16`.  Every one of the 324 classes required
models at all three short lengths; none required a higher-order `C32` or
`C64` cut.  The single first-pass timeout `(a,c)=(2,6)` closed at 2,414
models under the resumed 1,200-second cap.

In the versioned certificate bundle, each class directory contains
`result.json` and a deterministic compressed `final.cnf.gz`.  The final CNF
was solved independently with CaDiCaL 1.9.5 and Lingeling.  Both solvers
returned UNSAT for every class.  The jobs used deterministic construction,
independent processes, and resumable outputs; the Git-resident aggregate
`sweep.json` records the limits and every result.

Because every ordinary class is a singleton, transfer back to the 324 rooted
translations uses the recorded identity source-to-representative maps.  The
separate source-to-canonical maps verify the canonical labelings but are not
needed to alter a completion.

## 4. Proof-core extraction

For every final CNF, Glucose generated a fresh DRAT trace.  `drat-trim`
verified the trace, extracted its input-clause dependency core, generated a
proof for that core, and verified the reduced proof again.  CaDiCaL then
independently solved the extracted core as UNSAT.  The transient per-class
DRAT traces are not retained; their verification transcript hashes,
compressed proof-core CNFs, semantic analyses, and exact checker outcomes
are retained.  The full detailed DRAT trace for `(4,2,2)` is preserved
separately.

| proof-core quantity across 324 classes | minimum | median | maximum | total |
|---|---:|---:|---:|---:|
| retained clauses | 161 | 6,594 | 20,070 | 2,200,561 |
| retained matching/cardinality clauses | 106 | 2,503.5 | 4,209 | 750,872 |
| retained cycle cuts | 55 | 4,115.5 | 15,861 | 1,449,689 |
| deficient vertices in retained cuts | 23 | 76 | 76 | 23,870 |
| safe matching variables in retained cuts | 38 | 628.5 | 827 | 186,154 |
| coarse topology-aware motif clusters | 35 | 852.5 | 3,045 | 323,728 |

The one-pass dependency cores remove between 86.10% and 99.63% of their
final formulas, with median reduction 95.34%.  Their retained cuts classify
as 57,441 `C4`, 418,608 `C8`, and 973,640 `C16`.  `C8` and `C16` occur in
all 324 cores; `C4` occurs in 320.  Across translations there are 12,544
distinct coarse keys `(source length, number of matching edges, named core
paths)`.  Most certificates remain global: 284 of 324 use all 76 deficient
vertices in retained cuts.  The small extreme certificates are real—the
smallest has 161 clauses—but they do not extend to a uniform bounded-window
explanation of the family.

The semantic analysis for every class identifies each retained matching
constraint and maps each retained conflict clause to:

- its safe matching-edge variables and endpoint labels;
- all endpoint branch coordinates;
- a canonical literal ordinary-cycle witness;
- every realizable short source length;
- the named core paths supporting the cycle; and
- the smallest hull on each intrinsic `A/B/C/D` coordinate path.

There is no honest single scalar interval on this branched core.  A matching
chord can join distant short path segments, so the preserved topology-aware
per-branch hulls are the appropriate interval representation.

The most aggressively reduced fixed-point core at `(4,2,2)` has 10,548
clauses, down from 109,419 (90.36% removed): 3,289 matching/cardinality
clauses and 7,259 cuts, sourced by 331 `C4`s, 2,283 `C8`s, and 4,645 `C16`s.
It still involves all 76 deficient vertices and all 76 cardinality blocks.
Removing any whole length family makes this reduced formula SAT, and keeping
only any single family also makes it SAT.  This is an aggressively reduced
proof-dependency core, not a clause-minimal MUS.

## 5. What the cores explain

Deleting the `k` matching edges from any forbidden cycle leaves `k`
vertex-disjoint nonempty core paths.  Their total core length is `L-k`.
After individually unsafe completion edges have been removed, `k>=2`; hence
every `C4`, `C8`, or `C16` conflict has total core-path support at most 2, 6,
or 14 respectively.  This proves a bounded metric-composition alphabet
uniform in `j,a,c`.

It does not prove bounded global coordinate diameter.  The `(4,2,2)` fixed
core is global, uses 830 coarse topology-aware motif clusters, and retains
642 of 703 safe edge variables in its cuts.  The data therefore close every
`j=4` instance computationally while pointing toward a finite
alternating-path motif theorem, not yet supplying one.  The full structural
analysis is in `type_t_port_completion_obstruction.md`.

## 6. Adversarial `j=5` search

The bounded parallel search did not attempt exhaustive `j=5` certification.
Randomized allowed matchings, exact-incremental 2/3/4-edge switches,
annealing/tabu, and beam refinement found a stronger `(5,2,2)` near miss:

\[
  (\#C_4,\#C_8,\#C_{16})=(0,0,1270).
\]

It has at least 10,000 `C32`s, at least 10,000 `C64`s, and a `C128` witness.
All 78 matching edges participate in a `C16`, so the residual obstruction is
again global rather than a small repair neighborhood.  An independent
NetworkX checker confirms simplicity, connectedness, order 167, size 251,
degree distribution `3^166,4^1`, and the exact short-cycle counts.

## 7. Reproduction and scope

The principal commands are recorded verbatim in
`manifests/type_t_port_completion_j4_manifest.json`.  Large bit-for-bit
certificates live in the immutable GitHub Release asset named there rather
than in Git history.  Restore and validate the complete tree with

```text
PYTHONPATH=verifier python verifier/type_t_port_artifacts.py fetch
```

The fetcher verifies the 317 MiB archive before extraction, then runs the
deterministic `inventory.json` audit over every class result, final CNF,
proof-core summary, proof-core CNF, and semantic analysis.  Reports,
canonical representatives and maps, sweep summaries, the aggregate motif
analysis, and both levels of cryptographic inventory remain in Git.

The proved scope is exactly same-vertex completion of the 324 ordinary
`j=4` cores.  No all-`j` theorem is inferred.  Added vertices, degree five,
and `Q` remain deliberately untouched.
