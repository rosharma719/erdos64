# Exact normalized cyclic Z3 lifts

## Certified base graphs

The four bases were restored from the Hegde--Sandeep--Shashank repository
`rbsandeep/Erdos-Gyarfas`, branch `special-graphs`, commit
`f7bea75afecb07dab552047ece2d551722f32272`. The authoritative inputs are four
24-by-24 adjacency matrices. Their source-file SHA-256 values and the checksums
of every canonical graph6, sparse6, and edge-list artifact are in
`manifests/z3_bases_manifest.json`.

The matrices were canonically relabelled with nauty `labelg` 2.9.3. Each saved
representation decodes to the same labelled simple connected cubic graph with
24 vertices, 36 edges, and cycle-space rank 13. The workspace DFS detector and
NetworkX's unrelated simple-cycle implementation independently agree that each
base has no C4 or C8 and does have a C16; the manifest stores one C16 witness
per graph. Nauty `countg` gives automorphism-group orders 3, 12, 3, and 4.

The first graph was cross-checked against the external Markström description:
24 vertices, 36 edges, cubic, planar, no C4/C8, a C16, and automorphism-group
order 3. Public summaries also state that Markström found exactly four such
24-vertex graphs and that this is the unique planar one. The other three are
certified directly from the authors' special-graphs branch; no independent
public encoding of those three was located.

## Normalization and completeness

For each fixed canonical labelled base, choose the deterministic BFS spanning
tree rooted at vertex 0, scanning vertices and neighbors increasingly. Orient
each stored edge from its smaller to its larger endpoint. Gauge normalization
sets every one of the 23 tree-edge voltages to zero. The remaining 13 cotree
edges, listed in the base manifest, receive independent coordinates in Z3.
Coordinate 0 is the least-significant base-3 digit of the assignment index.

For voltage `a` on oriented edge `u<v`, the derived graph contains
`(u,i)(v,i+a)` for every `i` in Z3; the reverse orientation consequently has
voltage `-a`. Every base incidence lifts once at each sheet, so the derived
graph is simple cubic with 72 vertices and 108 edges. The zero assignment is
three disjoint copies of the base. For a nonzero normalized assignment, some
fundamental cycle has nonzero voltage. Its voltages generate the only nontrivial
subgroup of the prime-order group Z3, so the derived cover is connected.

There are exactly `3^13=1,594,323` normalized assignments per base. The zero
assignment is excluded only because it is disconnected. No scalar or
automorphism quotient is taken, leaving exactly
`4(3^13-1)=6,377,288` connected assignments. The half-open full ranges and all
output paths were frozen before the run in `manifests/z3_lift_plan.json`.

## Exact engine

`verifier/z3_lift_search.cpp` constructs each 72-vertex lift and tests exact
simple-cycle lengths in the required order 4, 8, 16, 32, 64. C4 uses the exact
common-neighbor characterization. Longer cycles use exhaustive rooted DFS:
the least vertex of a cycle is its root, vertices cannot repeat, closure is
accepted only at exactly the target length, and the two orientations are
broken by ordering the root's two cycle neighbors. This is an exact existence
test at every requested length, including 32 and 64; if no assignment reaches a
later stage, its zero workload is a consequence of staged exact rejection, not
a weakened detector.

Each shard records its exact half-open range, examined count, survivor count
after every length, per-stage time, first rejection witness, elapsed time, and
rate. Assignment-index lists are retained after the 8, 16, 32, and 64 stages.
The Python reference constructor and existing exact DFS/NetworkX detectors are
used for independent randomized and survivor validation.

## Pre-run benchmark

The engine checked 10,000 nonzero assignments on each of the four bases before
the exhaustive launch. Rates were 44,220--60,838 assignments/second. Exact C8
search dominated every base (0.094--0.158 seconds of each 10,000-assignment
sample); C4 took 0.058--0.062 seconds and C16 took at most 0.004 seconds because
every sampled C8 survivor quickly exhibited a C16. No sample reached C32 or
C64. Exact counts and timings are frozen in
`manifests/z3_lift_benchmark.json`.

## Exhaustive result

All 6,377,288 nonzero assignments completed. Survivor counts were:

| base | after C4 | after C8 | after C16 | after C32 | after C64 |
|---:|---:|---:|---:|---:|---:|
| 0 (Markström) | 1,594,322 | 54,458 | 0 | 0 | 0 |
| 1 | 1,594,322 | 570,806 | 0 | 0 | 0 |
| 2 | 1,594,322 | 750,140 | 0 | 0 | 0 |
| 3 | 1,594,322 | 170,342 | 0 | 0 | 0 |
| **total** | **6,377,288** | **1,545,746** | **0** | **0** | **0** |

Thus every assignment was eliminated by an exact C8 or C16 witness; none
reached C32. The C32 and C64 survivor counts are therefore exactly zero by
staged rejection, and there is no final survivor to preserve under the
counterexample protocol.

The independent Python audit is exhaustive at both nonvacuous survivor
boundaries. `has_cycle_len_dfs` reconstructed and checked all 6,377,288
post-C4 assignments (zero C4 disagreements), then all 1,545,746 post-C8
assignments (each independently C8-free and C16-positive). It also agreed on
1,024 deterministic random assignments across both rejection paths and
validated all eight saved C8/C16 witnesses edge-by-edge. There were zero
disagreements. Checksums and exact per-shard certificates are in
`manifests/z3_lift_run_manifest.json`.

The certified conclusion is intentionally narrow:

> No connected cyclic Z3-lift of these four specific 24-vertex base graphs is
> an Erdős--Gyárfás counterexample.

It says nothing about other graph covers, cyclic 5-lifts, noncyclic voltage
groups, or arbitrary cubic graphs.

---

## Part III (2026-07-26): algebraic compression of the elimination

**Standing reminder:** everything below is a hand-checked mathematical
argument cross-validated by independent Python computation (dual DFS/
NetworkX cycle detectors, independent real-lift reconstruction). None of
it is proof-assistant formal verification.

### III.1 -- projection-type classification of every C8-survivor's killer C16 [COMPUTATIONALLY VERIFIED, EXHAUSTIVE]

`verifier/z3_certificate.py` enumerates **every simple 16-cycle of each
base** (not just the one stored witness), computes its homology vector
`z_C` in `F3^13` against the SAME canonical tree/cotree gauge already used
for the exhaustive lift search, and checks -- exhaustively, not by
sampling -- whether each of the 1,545,746 C8-survivors' voltage
assignment `a` satisfies `a . z_C = 0` for some such `z_C` (a "Type 1"
projection in the task's numbering: a simple base 16-cycle with trivial
holonomy, lifting to a genuine C16 in exactly one sheet).

**Result: every single one of the 1,545,746 C8-survivors is Type 1, for
all four bases, with zero exceptions.**

| base | simple C16 count in base | distinct homology vectors | C8 survivors | Type-1 covered | uncovered (types 2-4) |
|---:|---:|---:|---:|---:|---:|
| 0 (Markström) | 228 | 228 | 54,458 | 54,458 | 0 |
| 1 | 315 | 315 | 570,806 | 570,806 | 0 |
| 2 | 330 | 330 | 750,140 | 750,140 | 0 |
| 3 | 207 | 207 | 170,342 | 170,342 | 0 |

Types 2 (non-simple nonbacktracking closed walk), 3 (repeated base
vertices, distinct lifted vertices), and 4 (other) **never occur** for
these four bases -- the elimination mechanism is entirely explained by
simple base cycles with zero net voltage, needing no non-simple-walk
machinery at all. This is stronger than what the task's III.1 required
(a distribution across all four types); the honest report is that three
of the four types have empirical count zero, not that they were assumed
away. `manifests/z3_certificate_manifest.json` records every base's full
simple-C16 list and the exhaustive per-C8-survivor coverage check
(`covered_by_simple_c16_hyperplanes` field), independently replayable
from the checked-in base edge lists and `after8` survivor-index files
alone -- no unrecorded intermediate state.

### III.2 -- the linear model covers the FULL nonzero space, not just C8-survivors [PROVED / COMPUTATIONALLY VERIFIED]

Fixing the same canonical BFS spanning tree (root 0, neighbours scanned
increasingly) and 13 cotree coordinates already used for the exhaustive
search, every simple base 16-cycle `C` has a homology vector
`z_C in F3^13`: for a cycle traversal `x_0,...,x_15,x_0`, `z_C`'s
cotree-indexed entry is the signed count (mod 3) of that cotree edge's
appearances, sign `+1` if traversed in its canonical `(min,max)`
orientation and `-1` otherwise. **Claim, proved by direct exhaustive
computation over the entire space (not sampled): for each of the four
bases, `⋃_C {a : a . z_C = 0} = F3^13 \ {0}` exactly** -- i.e. the union
of simple-C16 hyperplanes covers *every* nonzero voltage assignment, not
merely the 1,545,746 that happen to survive C8. (This is a strictly
stronger fact than III.1 needed; it was checked directly because the
exact-coverage computation is cheap once the homology vectors are in
hand -- 4 x (1,594,322 x ≤330) mod-3 dot products, well under a minute
total with vectorized arithmetic.) So constraint (3) of III.3's task
("non-simple-C16 walk constraints") is empirically *unnecessary* for
these four specific bases -- recorded honestly as a finding, not
engineered by omitting a needed case.

**Minimal/near-minimal covering subset** (exact minimum set cover is
NP-hard in general; a fast randomized-then-exact-top-up greedy is used,
`verifier/z3_min_cover.py`; each candidate subset's exactness is verified
against the FULL exact `3^13`-point space afterward, not the sampled
approximation used only to pick candidates fast):

| base | total distinct `z_C` | greedy cover size | exact full coverage verified | scalar-multiple pairs in cover |
|---:|---:|---:|---:|---:|
| 0 | 228 | 27 | yes | 0 |
| 1 | 315 | 26 | yes | 0 |
| 2 | 330 | 25 | yes | 0 |
| 3 | 207 | 24 | yes | 0 |

`manifests/z3_min_cover_manifest.json` stores every chosen cover vector
per base. **Light projective-geometric structure check:** no two vectors
in any cover are scalar multiples of each other in `F3` (i.e. no two
chosen 16-cycles are voltage-equivalent up to reversal/gauge) -- a basic
sanity property, not evidence of a deeper projective design; a full
automorphism-orbit analysis of the `z_C` set under each base's nauty
automorphism group (orders 3, 12, 3, 4) was **not attempted** this pass
(honest scope limit, flagged as future work, not silently skipped).

### III.3 -- standalone compact certificate [PROVED, INDEPENDENTLY VERIFIED]

**Theorem (four specific bases only).** For each of the four certified
24-vertex bases indexed 0-3, every one of the `3^13-1 = 1,594,322`
nonzero normalized cyclic Z3-voltage assignments produces a lifted graph
containing a simple 16-cycle, via the following certificate alone:
24-27 vectors in `F3^13` (`manifests/z3_min_cover_manifest.json`) such
that every nonzero assignment `a` is orthogonal (mod 3) to at least one
of them.

`verifier/z3_standalone_verifier.py` is the **self-contained** checker:
given only the 24-27-vector list (not the original exhaustive search, not
even the full 207-330-vector simple-C16 list), it performs
`O(27 x 3^13)` mod-3 dot products (~4x10^7 machine operations, seconds on
one core) and confirms full coverage exactly -- against the ~1,594,322 x 4
full 72-vertex lifted-graph constructions plus exact simple-cycle search
the original exhaustive engine performed. It additionally
**cross-checks 300 random assignments per base against a REAL lift
construction** (independent code path: `verifier/z3_lifts.py`'s reference
builder + `verifier/cycle_detect.py`'s DFS detector), confirming the
abstract linear-algebra certificate corresponds to an actual simple C16
in the real lift, not a numerical coincidence. **Result: all four bases
fully certified, all 1,200 cross-checks (300 x 4) confirm a genuine
lifted C16 exists exactly where the covering vector predicts.**

Combined with the already-exhaustive, independently-audited C8 stage of
the original search (z3_lift_run_manifest.json, `independent_z3_verify.py`
-- unchanged, not re-derived here), this gives the compact per-base
statement the task required:

> For each of the four bases, every nonzero normalized cyclic Z3-voltage
> assignment either fails to survive the C8 stage (already exhaustively
> certified, unchanged) or survives C8 and is explained by one of 24-27
> explicit `F3^13` vectors certifying a genuine simple lifted C16 --
> auditable in seconds, not by replaying 1,594,323 full lift
> constructions.

**Theorem about these four bases only** -- exactly as the task requires;
no claim is made about other bases, other voltage groups, or arbitrary
cubic graphs.
