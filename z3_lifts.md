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
