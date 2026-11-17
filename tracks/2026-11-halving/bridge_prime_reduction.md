---
id: bridge-prime-reduction
title: "Research pass VII: exact bridge transfer and the rooted prime induction barrier"
kind: track-note
topics: ["tracks", "2026-11-halving"]
doc_status: active
date: 2026-11-16
summary: "16 November 2026. Mathematical status: a proved general cycle-decomposition theorem and exact rooted obstruction for edge-bridging operations. A conditional reduction for the root-robust prime conjecture. No proof of the prime conjecture or the Erdős–Gyárfás conjecture is claimed."
---

# Research pass VII: exact bridge transfer and the rooted prime induction barrier

**16 November 2026.** Mathematical status: a proved general cycle-decomposition
theorem and exact rooted obstruction for edge-bridging operations. A conditional
reduction for the root-robust prime conjecture. **No proof of the prime
conjecture or the Erdős–Gyárfás conjecture is claimed.** The cycle transfer is
elementary and has not been established as novel.

## Why this is a conceptual change

Pass VI suggested balancing one or two ears around a chosen dyadic cycle.
An arbitrary rerouting argument has no mechanism to force the correct cycle
length. A better abstraction comes from a published construction theorem:
Kingan & Kingan (2024) characterize cyclically four-edge-connected cubic
graphs using ladders, Möbius ladders, the Petersen graph, and repeated
*bridging* of suitably separated pairs of edges starting from the 8- or
10-vertex ladder, with the exact restrictions stated in their paper.

This suggests reducing a **rooted cycle assertion about an expanded graph**
to **cycles and terminal-to-terminal paths in its smaller parent**, in one
step. The transfer is exact; no probabilistic argument or cycle-length
heuristic is involved.

## 1. Exact bridge-cycle transfer theorem

Let `G` be any finite simple graph, let `e={a,b}` and `f={c,d}` be
**vertex-disjoint edges**, and form `B=B(G;e,f)` by removing `e,f`,
adding new vertices `x,y`, and adding

```
a--x--b       c--y--d
   |             |
   +------ ------+
          xy
```

(The schematic means precisely: `ax,bx,xy,cy,dy`; only five new
edges and two new vertices.)

**Theorem A (bijection).** Every simple cycle in `B` occurs in
exactly one of these two classes:

1. **Lifted parent cycle.** A unique simple cycle `C` of `G` is
   transformed by subdividing each selected edge it uses. Its new
   length is

   `|C| + 1[e in C] + 1[f in C]`.

   This class consists exactly of child cycles avoiding the bridge
   edge `xy`.

2. **New bridge cycle.** Choose endpoints `u in e` and `w in f`,
   and a simple `u-w` path `P` in `G-{e,f}`. The child cycle is
   `u-P-w-y-x-u`, of length `|E(P)|+3`. This class consists exactly
   of cycles containing the bridge edge `xy`.

*Proof.* If a child cycle avoids `xy`, any use of a new degree-three
vertex `x` must traverse both its other incident edges `ax,bx`,
and similarly at `y`. Suppressing these vertices recovers a unique
simple cycle of `G`. Conversely each parent cycle lifts uniquely.

If the child cycle uses `xy`, it uses exactly one edge from `x`
to `{a,b}` and exactly one edge from `y` to `{c,d}`. Delete `x,y`
and the three cycle edges incident with them. What remains is a
simple endpoint-to-endpoint path in `G-{e,f}`. Conversely every such
path closes through the three-edge route `w-y-x-u`. These
correspondences are inverse and the two classes are disjoint. QED.

### Four predecessor lengths

For a dyadic target `q=2^k` (`k>=2`), there are **exactly four** possible
parent lengths that can create it:

| Source object | Required source length | Additional condition |
|---|---|---|
| Cycle | `q` | uses neither `e` nor `f` |
| Cycle | `q-1` | uses exactly one of `e,f` |
| Cycle | `q-2` | uses both `e,f` |
| Simple endpoint path in `G-{e,f}` | `q-3` | ends at opposite edge endpoints |

This is an exact **four-predecessor ladder**, not a numerical approximation.
It directly accounts for the length changes that unconstrained ear
rerouting failed to control.

## 2. Exact rooted barrier

For an **old root** `r in V(G)`, append the requirement `r notin C` in the
first three cases and `r notin P` in the fourth.

For the **new root `x`**, no bridge-cycle can avoid the root: every
bridge-cycle uses both `x` and `y`. Therefore a dyadic child cycle
avoiding `x` exists **if and only if** a parent cycle occurs in
either of the following classes:

- length `q`, using neither `e` nor `f`;
- length `q-1`, using `f` but *not* `e`.

The analogous statement for `y` interchanges `e` and `f`.

**Corollary B (exact contrapositive).** A root-critical child must
simultaneously exclude all applicable predecessor patterns above.
In particular, an old root-critical child has a two-edge hitting
barrier on all root-free dyadic parent cycles *and* exclusions of
root-free path lengths `2^k-3` between endpoints of the two edges.

This is a sharper obstruction than finding one or two ears around a
single specified cycle. It constrains entire parent cycle and path
spectra at once.

## 3. A width theorem for entire path families

Let `S_r(e,f)` be the set of lengths of simple paths in `G-{e,f}`
joining *some* endpoint of `e` to *some* endpoint of `f` and avoiding
an old root `r`.

**Proposition C (spectrum-width forcing).** Suppose `S_r(e,f)`
contains every integer in `[a,b]`, with `a>=1` and

`b >= 2*a+3`.

Then the bridged graph has a dyadic cycle avoiding `r`.

*Proof.* The bridge cycles realize all lengths from `a+3` through
`b+3`. The stated inequality is equivalent to
`b+3 >= 2(a+3)`, and any integer interval `[m,2m]` contains a
power of two. QED.

A useful **parity-aware** variant requires only all *odd* lengths
`a,a+2,...,b` (odd `a,b`) in the path spectrum, with
`b>=2a+3`: then the constructed cycles have the even lengths
`a+3,a+5,...,b+3`, and the power of two in
`[a+3,2(a+3)]` is even and is realized. Without the parity condition
on the path spectrum, step-two intervals can be exclusively *odd*
after adding 3 and cannot certify a power of two.

Thus a hypothetical root-critical child must have *short,
possibly gapped* terminal path spectra in a precise multiplicative
sense. This resembles the interval phenomena seen in prior gadget
passes, now without assuming any fixed gadget library or a three-cut.

## 4. A packing/transversal obstruction

Let `nu_D(G)` be the maximum number of pairwise **vertex-disjoint**
dyadic cycles in `G`.

**Proposition D (bridge survival).**
For a bridge addition,

`nu_D(B(G;e,f)) >= max(0, nu_D(G)-2)`.

*Proof.* Choose a disjoint packing in `G`. Because the two bridge
edges touch at most two packed cycles, all other cycles survive
unchanged in `B`, still disjoint. QED.

In particular, **four disjoint dyadic parent cycles guarantee that
every root in the child can be avoided by some dyadic cycle**, under
*every* choice of disjoint bridging edges. At most two packed cycles
are affected and at most one surviving packed cycle contains a
prescribed old root. New roots lie on none of the surviving parent
cycles.

This provides an unrestricted, infinite-family bridge-stability
result under a strong but checkable packing hypothesis.
**Limitation:** along many successive bridge steps, this bound loses
two packed cycles per step and is not strong enough by itself to
establish the general conjecture.

Equivalently, to have a root-critical child at an old root `r`,
the pair `{e,f}` must intersect **every** dyadic parent cycle
avoiding `r`. This is an edge-transversal condition; the shifted
and path predecessors in Theorem A make it strictly stronger.

## 5. An explicit counterexample to a tempting simplification

The 14-vertex cubic prime graph encoded as

`MGBAOWo?[_?Ra?K?_`

has a prime bridge expansion using edges `e={0,12}` and `f={9,11}`.
Set the prescribed *old* root to `r=3`.

- There is **no** dyadic lifted parent cycle avoiding `3` after
  subdividing the chosen two edges (checked against the complete base
  cycle set).
- Nevertheless, `0-5-1-2-8-9` is a simple five-edge path of
  `G-{e,f}` avoiding `3`.
- The child cycle
  `0-5-1-2-8-9-y-x-0` has exactly eight edges, avoids `3`,
  and is simple.

Both parent and child pass independent cubic and cyclic
four-edge-connectivity checks. This is a concrete witness that the
`q-3` bridge-path class is **necessary**: a proof relying only on
surviving/shifted old cycles is incomplete.

The example comes from a **nonexhaustive** order-14 sample; no
classification at order 14 is claimed.

A smaller example illustrates the opposite extreme. A `K4` root is
critical (its only dyadic cycles are spanning 4-cycles). Bridging
two opposite edges produces `K3,3`, which is root-robust via 4-cycles.
The new path cycles repair the property even when there is no parent
root-avoiding dyadic cycle to inherit.

## 6. Exact inductive research program

Kingan & Kingan's published construction theorem motivates the
following **bridge-stability statement**:

> If `G` is a rooted-robust cyclically four-edge-connected cubic
> graph and `B(G;e,f)` is another cyclically four-edge-connected cubic
> graph obtained by an admissible bridge, then the child is
> root-robust at every vertex.

**This statement is open**. Establishing it, alongside the known
root-robust base families (prisms, Möbius ladders and the Petersen
graph), would prove the proposed root-robust prime conjecture using
the published construction characterization.

Theorem A tells us **exactly** how such an induction could work.
The most substantive remaining question is:

> Does cyclic four-edge-connectivity force at least one of the four
> rooted predecessor patterns in every admissible bridge operation?

Unlike a free-form two-ear existence conjecture, this is anchored to a
complete structural construction and has explicit spectral failure
conditions. A plausible strategy is to use cycle switching to force
the `q-3` path alternative *when the three lifted-cycle alternatives
are all obstructed*.

This research plan addresses cyclic prime **cubic** graphs; it
does not yet establish the general Erdős–Gyárfás conjecture for
minimum-degree-three graphs.

## 7. Verification and references

Implementation:
`tracks/2026-11-halving/scripts/bridge_reduction.py`

New tests:
`tracks/2026-11-halving/scripts/test_bridge_reduction.py`

The tests independently enumerate cycles of the expanded graphs using
NetworkX directed simple cycles, compare their **complete edge sets**
with the predictions from Theorem A, and check the rooted
counterexample-to-naive-lifting certificate. Existing tests are
unmodified. Run:

`python -m pytest -q tracks/2026-11-halving/scripts/`

References:

- R. J. Kingan and S. R. Kingan, *On cyclically 4-connected cubic
  graphs*, AKCE International Journal of Graphs and Combinatorics
  **21** (2024), 255–260.
  https://doi.org/10.1080/09728600.2024.2333397
- Heckman and Krakovski, *Erdős–Gyárfás Conjecture for Cubic Planar
  Graphs*, Electronic Journal of Combinatorics **20** (2013), #P7.
  https://doi.org/10.37236/3252
- Garcia, *Small graphs without power-of-two cycles*, 2026,
  arXiv:2609.04686. https://arxiv.org/abs/2609.04686

The elementary bridge transfer may be independently known in the
graph-reduction literature. We make no claim of publication novelty.
