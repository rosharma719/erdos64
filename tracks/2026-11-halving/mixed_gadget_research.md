---
id: mixed-gadget-research
title: "Mixed three-port gadget search: exact constraints, catalogues, and a 78-vertex family"
kind: track-note
topics: ["tracks", "2026-11-halving"]
doc_status: active
date: 2026-11-16
summary: "Research notebook, 2026-11-16. Continuation of partial_triangle_expansion_census.md following erdos64 PR #2. This is computational/structural progress on construction families; it does not settle the Erdős–Gyárfás conjecture."
---

# Mixed three-port gadget search: exact constraints, catalogues, and a 78-vertex family

**Research notebook, 2026-11-16.** Continuation of `partial_triangle_expansion_census.md` following `erdos64` PR #2. This is computational/structural progress on construction families; it **does not settle the Erdős–Gyárfás conjecture**. The search results have reproducible code and independent graph-level checks, not formal SAT/DRAT certificates.

## Relation to prior literature

The general projection onto base cycles is Garcia's published **window lemma**, not an original result of this project: [Garcia (2026), arXiv:2609.04686](https://arxiv.org/abs/2609.04686), §3. Exoo's known 78-vertex construction avoids 4, 8 and 16, and Garcia discusses its optimality within a restricted gadget design space on small bases. This notebook independently reconstructs one 78-vertex family and provides checkable certificates. Novelty of the six-class decomposition has **not been established**. Published counts of connected cubic graphs are [OEIS A002851](https://oeis.org/A002851): 1, 2, 5, 19, 85 for orders 4, 6, 8, 10, 12.

## Exact path-spectrum calculus

A cubic **three-port gadget** is a connected simple graph with three marked degree-2 vertices (ports), all remaining vertices degree 3. Connect one external edge at each port. A single *untouched* degree-3 vertex is also permitted as a degenerate gadget with three coincident ports and zero internal path length.

Given a simple cubic base `B`, put one gadget at each base vertex. For a simple base cycle `C=(v_0,...,v_{L-1})`, let `S_v(a,b)` be the set of lengths (in **internal** edges) of simple paths between the two ports used by `C` at `v`. Then the full lifted cycle spectrum is

```
    L + S_v0 + S_v1 + ... + S_v(L-1)
```

where `+` on sets denotes Minkowski sum. All other output cycles lie entirely within one gadget. Each attached gadget is visited by at most two of its three external edges, so a non-internal simple cycle projects to a simple base cycle. The path choices are independent because gadgets are disjoint. The algorithm uses this exact characterization, including all port orientations, before building an expanded graph.

For the current gadgets, every port-pair length spectrum is an **integer interval**, so each lifted spectrum is itself an interval `[L+sum(min S_v), L+sum(max S_v)]`. The solver backtracks over gadget assignments with an exact per-cycle interval test and a sound partial-assignment lookahead. `predicted_spectrum` also implements general bitset sum convolution; the fast search deliberately rejects non-interval spectra until a general-domain propagation algorithm is implemented.

## A complete gadget classification up to 11 internal vertices

Every connected three-port gadget on `n>=3` vertices extends to a connected simple cubic graph on `n+1` vertices by adding one apex joined to its three distinct ports. Thus the complete small cubic catalogs classify every candidate at these sizes. We require gadgets to have **no internal 4- or 8-cycle**, a necessary condition for use in a power-of-two-avoiding construction.

| Gadget order | Rooted candidate source | Connected allowed gadget classes |
|---:|---|---:|
| 1 | Single untouched cubic vertex | 1 (degenerate identity) |
| 3 | Cubic graphs of order 4 | 1 (triangle) |
| 5 | 2 connected cubic graphs of order 6 | 0 |
| 7 | 5 connected cubic graphs of order 8 | **2** |
| 9 | 19 connected cubic graphs of order 10 | 0 |
| 11 | 85 connected cubic graphs of order 12 | 0 |

For order 12, we regenerated **85 distinct adjacency walk-count signatures** from 84 two-edge-insertion graphs and one edge-switch, verified that each graph is connected and cubic, and matched the published count of 85. This is a finite **conditional completeness argument** based on the published cubic count, not a new from-first-principles enumeration proof. `derive_cubic_12_catalog.py` reproduces the fixture.

The gadgets with clean interiors have these attachment-aware path intervals:

| Gadget | Possible path lengths (three unordered port pairs) | Internal cycles |
|---|---|---|
| Identity | `{0}`, `{0}`, `{0}` | None |
| Triangle `T3` | `[1,2]` for all three pairs | `{3}` |
| Seven-vertex skew `H7` | `[3,6]`, `[2,6]`, `[2,6]` | `{3,5,6,7}` |
| Seven-vertex uniform `H7` | `[2,6]` for all three pairs | `{3,5,6}` |
| Exoo 15-vertex `H15` (added separately) | `[3,14]`, `[3,14]`, `[5,14]` | `{3,5,6,7,9,10,11,12,13,14,15}` |

The skew H7 and H15 are related to the standard Exoo gadgets as described by Garcia. H15 is **one explicitly constructed 15-vertex gadget**, not a census of all gadgets that size. The three H7-skew port orientations and three H15 orientations are essential: the special terminal pair changes the possible lengths.

## A simple forced-power density obstruction

Consider one base cycle of length `L`, with `t` triangle gadgets and `h` seven-vertex gadgets, of which `d` traverse the longer-minimum path pair `[3,6]` of the skew H7. Let `e` be the number of H15 gadgets, of which `f` traverse the special `[5,14]` pair. All other gadgets are unchanged. The lifted spectrum is exactly

```
    [ L + t + 2h + d + 3e + 2f,
      L + 2t + 6h + 14e ]     (both endpoints included)
```

Any integer interval `[m,M]` with `m>=3` and `M>=2m` contains a power of 2. Therefore **a sufficient condition for this base cycle to force a power-of-two cycle** is

```
    2(h - d) + 8e - 4f >= L.
```

This is an elementary corollary of the window lemma; novelty is not asserted. It is useful for eliminating dense configurations even without enumerating specific powers. The actual solver tests particular forbidden powers exactly, so it also handles cases where `M<2m`.

## Complete base census through order 10

The 27 pairwise nonisomorphic **connected** cubic bases of orders 4, 6, 8 and 10 were checked without a bound on the number of expanded vertices.

| Available gadget choices | Forbidden lengths | Result across all 27 bases |
|---|---|---|
| Identity, T3, both H7 types, all port orientations | 4, 8, 16 | **No feasible assignment** |
| Previous choices plus one H15 Exoo gadget and all orientations | 4, 8, 16, 32 | **No feasible assignment** |

The second family can produce graphs of order up to `10*15=150`. Thus these finite results exclude some construction outputs beyond the order covered by broad graph-enumeration checks. They **do not** exclude arbitrary cubic graphs of those orders, other larger gadgets, or other base graphs.

As a sanity check, allowing H15 but forbidding **only** 4, 8, 16 gives feasible assignments on 1 of the 2 order-6 bases, 4 of the 5 order-8 bases, and 14 of the 19 order-10 bases. The additional 32-cycle restriction matters.

## The order-12 base recovers a six-class 78-vertex family

For the explicit 12-vertex cubic base

```
KL`AOWo?[G?R
```

the `4/8/16`-avoidance solver found **48** attachment-aware assignments: each uses **eleven skew H7 gadgets and one untouched vertex**. All 48 outputs are connected cubic graphs of order **78** and size **117 edges**. Isomorphism grouping with NetworkX VF2++ gives **six nonisomorphic classes**, with assignment multiplicities `12, 12, 6, 6, 6, 6`. None is planar. These numbers classify this **one base graph under this finite gadget library**, not every 78-vertex cubic graph or every 12-base construction.

Every one of the six classes was independently checked by a fixed-length DFS oracle and has **no 4-, 8-, or 16-cycle**. Every class **does have a 32-cycle and a 64-cycle**. `exoo78_family.json` includes graph6 encodings and actual ordered cycles of lengths 32 and 64 for all six graph classes; these are explicit positive certificates verifiable by checking that every listed successive vertex pair (including the closing pair) is an edge. `exoo78_certificate.json` supplies a smaller single-graph example. No conjecture counterexample is claimed.

## Reproduction

Run from the `erdos64` repository root, after the prior triangle-expansion patch is present:

```bash
python -m pytest -q tracks/2026-11-halving/scripts/test_mixed_gadget_solver.py
python tracks/2026-11-halving/scripts/derive_cubic_12_catalog.py
python tracks/2026-11-halving/scripts/mixed_gadget_census.py
python tracks/2026-11-halving/scripts/mixed_gadget_census.py --include-h15 --forbid 4 8 16 32
python tracks/2026-11-halving/scripts/exoo78_witness.py
python tracks/2026-11-halving/scripts/exoo78_family.py
```

Dependencies are Python 3, NetworkX, NumPy and pytest (tests only). Tests check the gadget catalog constraints, 85 distinct n12 bases, fast CSP vs brute force, the independent graph-level cycle oracle, the small-base exclusion, and explicit witness certificates.

**Scope limits / next step:** The full 85-base order-12 *assignment* census was attempted but not completed; only the explicit base above is classified. The order-14 base-generator attempt yielded only 506 of the published 509 isomorphism classes, so no complete 13-vertex gadget classification is claimed. The strongest next direction is a generic forbidden-sum CSP supporting non-interval gadget spectra and/or a SAT/PB encoding with proof certificates to scale beyond 12-base instances. The gadget library and exact cycle formula are already suitable for that extension.
