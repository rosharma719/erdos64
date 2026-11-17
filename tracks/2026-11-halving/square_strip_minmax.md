---
id: square-strip-minmax
title: "Research pass IX: square strips, exact rooted blockers, and a four-terminal transfer"
kind: track-note
topics: ["tracks", "2026-11-halving"]
doc_status: active
date: 2026-11-16
summary: "16 November 2026. Status: proved structural statements for cyclically four-edge-connected cubic graphs; exact rooted 4-cycle hitting/packing min-max theorem; arbitrary-depth bridge-survival corollary; constructive path spectra for four-terminal square strips; finite reference checks."
---

# Research pass IX: square strips, exact rooted blockers, and a four-terminal transfer

**16 November 2026.** Status: proved structural statements for cyclically four-edge-connected cubic graphs; exact rooted 4-cycle hitting/packing min-max theorem; arbitrary-depth bridge-survival corollary; constructive path spectra for four-terminal square strips; finite reference checks. This does **not** settle rooted dyadic-cycle robustness for 8-, 16-, or longer cycles, or the Erdős–Gyárfás conjecture. These square-ladder arguments are elementary; originality is **not** established.

## Why two-edge blockers alone are too weak

A bridge of edges `e,f` can destroy an old dyadic cycle only when that cycle uses `e` or `f`. Consequently, failure of a rooted child forces all root-free dyadic parent cycles to meet `{e,f}`. But two-edge transversals actually occur in small cyclically four-edge-connected cubic graphs, including the five-rung prism `Q10`: with root `0`, the disjoint edges `{1,6}` and `{3,8}` hit all three root-avoiding 4-cycles. This means the existence of a two-edge blocker itself cannot contradict cyclic connectivity. The genuinely difficult bridge-repair step still needs shifted `2^k-1`, `2^k-2`, and endpoint-path `2^k-3` spectra.

Here we **fully characterize the four-cycle part** of the blocker condition, rather than claim a general dyadic repair.

## Definitions

Let `G` be a finite simple, 3-connected cubic graph with no cycle-separating edge-cut of size at most three, and with `n>=10` vertices. Thus `G` is cyclically four-edge-connected in the Kingan–Kingan sense. A **square** is a simple 4-cycle. The **square overlap graph** `J(G)` has one vertex per square, joining two squares if they share an edge. For a prescribed root `r`, let `J_r(G)` be the induced subgraph on squares avoiding `r`.

Define the square transversal number

\[
\tau_4(G;r)=\min\{|F|: F\subseteq E(G),\; \forall C\in\mathcal S(G-r),\;E(C)\cap F\ne\varnothing\},
\]

and the rooted square-packing number

\[
\nu_4(G;r)=\max\{|\mathcal P|:\mathcal P\subseteq\mathcal S(G-r),\; C,D\in\mathcal P\text{ are vertex-disjoint}\}.
\]

Both numbers are zero when there are no root-avoiding squares.

## Theorem 1: square-strip decomposition

**Theorem.** For every such `G` on `n>=10` vertices:

1. An edge belongs to at most two squares, and a vertex belongs to at most two squares.
2. Two distinct squares meet in vertices if and only if they share **exactly one** edge.
3. Each component of `J(G)` is a path or a cycle. If a cycle component occurs, it accounts for all of `G`, which is a prism or a Möbius ladder.
4. Otherwise the square components are vertex-disjoint **open ladder strips**. A component with `k` squares has `2k+2` vertices and exactly four edges to the rest of `G`; hence it is a four-terminal cubic pole.

The eight-vertex cube is a real exception to the vertex bound: its six squares put three squares through each vertex. Its overlap graph is not a disjoint union of paths/cycles.

### Proof

A cyclically four-edge-connected cubic graph of order at least eight is triangle-free. A triangle with its three leaving edges would give a cyclic three-edge cut: the complement, with at least five vertices, has a cycle by the cubic degree sum.

**Two squares cannot share a two-edge path.** If two distinct squares share consecutive edges `ab,bc`, their fourth vertices `d,e` are distinct and both adjacent to `a,c`. The five-vertex subgraph on `{a,b,c,d,e}` contains `K_{2,3}` with bipartition `{a,c}` and `{b,d,e}`. Since `a,c` are saturated, this subgraph has at most three external edges. It contains cycles. Its complement has at least three vertices and at least one cycle: if it has `h>=3` vertices and the boundary size is at most three, the cubic degree sum yields at least `(3h-3)/2 >=h` internal edges. A cyclic cut of size at most three is forbidden. If two squares shared two *opposite* edges instead, their union would be a saturated `K4`, contradicting connectedness and `n>=8`. Thus distinct squares share at most one edge. In cubic graphs any two distinct squares meeting at a vertex share an incident edge (two two-element subsets of three incident edges intersect). This proves the intersection statement.

**An edge is in at most two squares.** If `ab` occurs in three squares, the two remaining neighbors of `a` and the two remaining neighbors of `b` span at least three cross-edges. By triangle-freeness, these are four distinct vertices. The six-vertex set consisting of the endpoints and those neighbors has at least eight internal edges, hence at most two outgoing edges, contradicting three-edge-connectivity.

**A vertex is in at most two squares.** Suppose `v` is in three squares. The no-shared-two-edge-path result means the squares use the three distinct pairs from its neighbors `a,b,c`; call their fourth vertices `x_ab,x_ac,x_bc`. Their union has at most seven vertices, contains cycles, and has at most three outward edges (check the three possible equality patterns among the `x` vertices). For `n>=10` its complement has at least three vertices and hence contains a cycle by the same degree sum, giving a forbidden cyclic three-edge cut. The equality pattern in which exactly two fourth vertices coincide even produces a two-edge cut. For `n=8` the all-distinct configuration closes to the cube, which explains the exception.

**Strips.** A square in `J(G)` has at most two neighbors: three neighboring squares would require three disjoint shared edges among the four edges of the square, since overlapping shared edges would put three squares through one vertex. If it has two neighbors, their shared edges are opposite. Thus `J(G)` is a union of paths and cycles. If a component forms a cycle, each vertex of every participating square already has all three incident edges inside the union. Connectedness forces the union to be `G`, and sequential opposite-edge gluings are precisely the prism/Möbius-ladder closures. For a path of `k` squares, each successive square shares one edge (two vertices) with its predecessor and shares no vertices with any earlier non-neighbor. The union therefore has `4+2(k-1)=2k+2` vertices. All but four endpoint vertices have their full degree within the union. If the union were proper, the cut size must be exactly four, since it is even and the graph is 3-edge-connected; if it were all of `G`, the only possible cubic closure of its four free stubs would create a closing square, contradicting the assumption that the overlap component is a path. Hence these are precisely four-poles. QED.

## Theorem 2: exact rooted square blocker min-max

**Theorem.** `J_r(G)` is always a disjoint union of paths. If its path components contain `k_1,...,k_s` squares, then

\[
\boxed{\tau_4(G;r)=\nu_4(G;r)=\sum_{i=1}^s\left\lceil\frac{k_i}{2}\right\rceil.}
\]

**Proof.** Deleting the squares containing `r` from each path component of `J(G)` leaves paths. A cycle component of `J(G)` can only be the whole prism/Möbius ladder, and every root then lies on two of its squares, so deleting those squares opens the cycle into a path. Thus `J_r` is a path forest.

Within a rooted path component of `k` squares, choose alternating square nodes `1,3,5,...`; these `ceil(k/2)` squares are pairwise vertex-disjoint, because in this class vertex intersection is exactly adjacency in `J`. Conversely, any edge of `G` belongs to at most two root-free squares, which, if there are two, are adjacent nodes in the *same* path. Covering the component requires at least `ceil(k/2)` edges; choose each shared edge of consecutive square pairs `(1,2),(3,4),...`, and if an unpaired last square remains, choose any edge on it. This achieves the lower bound. Edges cannot hit squares in distinct components. Sum over components. QED.

**Corollary (exact square-blocker screen).** An edge set of size two can hit every root-avoiding square **if and only if** the displayed sum is at most two. This characterizes general two-edge sets; actual edge bridges additionally require the two selected edges to be disjoint. In particular, if the sum is at least three, every bridge preserves a 4-cycle avoiding the old root, without relying on any 7-/8-/16-cycle search.

## Theorem 3: arbitrary-depth bridge resilience from rooted packing

Let `m(G)=min_r tau_4(G;r)`. After any `t` successive edge-bridging operations (the intermediate graphs need not remain prime), if

\[
\boxed{m(G)>2t,}
\]

then **every vertex in the final graph** can be avoided by a 4-cycle inherited *unchanged* from `G`.

**Proof.** Each bridge subdivides at most two edges that belonged to the original graph. Let `B` be the set of original edges ever subdivided, so `|B|<=2t`. For any original root `r`, `|B|<tau_4(G;r)` implies that some root-free square avoids every edge in `B`; it therefore survives as an original square. New subdivision vertices are absent from every untouched original square, and at least one original square survives (apply the same argument to any old root). QED.

The vertex/edge incidence limits also recover the simpler sufficient bound: if `G` has `s` squares, then `tau_4(G;r)>=ceil((s-2)/2)`. Hence `s>4t+2` suffices, generalizing the earlier prism/Möbius-ladder count to **every cyclically four-edge-connected cubic graph with at least ten vertices**. The exact strip formula is strictly stronger.

### A stronger example with only six squares

Start with the 20-vertex, ten-rung prism `Q20`. Bridge its two well-separated rung edges `{0,10}` and `{5,15}`. The 22-vertex child is cyclically four-edge-connected and has exactly **six squares in two disjoint three-square strips**. Its rooted transversal minimum is `m=3`, so **every subsequent bridge preserves a root-avoiding original 4-cycle**. The crude square count would require `s>=7` and cannot certify this case.

A complete graph6 encoding, all six square cycles, and the rooted transversal values appear in `scripts/square_strip_22_certificate.json`. The `test_square_strip_obstruction.py` checker constructs the graph directly and checks all eligible next bridge edge pairs independently.

## Theorem 4: exact four-terminal transfer for one open strip

A `k`-square open strip is the ladder `L_k=P_{k+1} x K2` with terminal vertices `LT,LB` on the left and `RT,RB` on the right. Its **entire simple-path length spectrum** between terminals is:

| Pair type | Exact attainable path lengths |
|---|---|
| Same end: `LT-LB`, `RT-RB` | `1,3,...,2k+1` |
| Opposite ends, same rail: `LT-RT`, `LB-RB` | `k,k+2,...,2k+(k mod 2)` |
| Opposite ends, different rail: `LT-RB`, `LB-RT` | `k+1,k+3,...,2k+(1-k mod 2)` |

**Proof.** Bipartiteness fixes path parity; the terminal distance fixes the minimum; at most `2k+2` distinct vertices bounds the maximum. All lengths in these ranges are attained: for a same-end pair, run out on the top rail to rung `j`, cross, and return on the bottom rail (`2j+1` edges); for opposite-end terminals, traverse left-to-right monotonically and switch rails at any chosen `s` distinct rungs, giving `k+s` edges, with the parity of `s` chosen to match the ending rail. These cover every allowed value. QED.

This is a **four-pole analogue** of the three-terminal path-spectra from earlier passes. It can be composed with path spectra outside the strip to predict exact crossing-cycle lengths. The proof is constructive and does not require enumerating cycles of the full graph.

## What is and is not resolved

This pass *fully resolves the topology and minimum blockers of root-avoiding 4-cycles* within the prime cubic setting, and turns all square-rich cases into immediate bridge-survival certificates. It provides a canonical four-edge-interface reduction for every remaining open square strip.

It does **not** force a root-avoiding 8- or 16-cycle when `m(G)<=2`: the five-rung prism has genuine disjoint two-edge blockers of its rooted square family. And even a square-free graph may have many dyadic cycles of larger lengths, for which the overlap graph has far more complicated topology.

**Next conceptual step:** seek a four-terminal **spectrum composition theorem** for the strip versus the square-free/square-poor core. Focus on the *joint* absence of 4-, 8-, and 16-cycle witnesses after bridging. In particular, ask whether a minimum rooted two-edge blocker of square strips forces one of the precise `2^k-1`, `2^k-2`, `2^k-3` bridge-repair signatures. Counterexample search should test proposed length forcing, not generate large cubic graph catalogs without a structural hypothesis.

## Reproduction

```sh
python -m pytest -q tracks/2026-11-halving/scripts/test_square_strip_obstruction.py
python -m pytest -q tracks/2026-11-halving/scripts/
```

`scripts/square_strip_obstruction.py` supplies square certificates, 4-edge strip decomposition, exact rooted hitting/packing certificates, and explicit four-pole paths. Tests compare the min-max formula against independent exhaustive edge covers across all complete prime cubic catalogs through order 12 (excluding the eight-vertex cube where the formula is inapplicable), verify closed and open strip structures, and check every next bridge pair in the six-square, order-22 witness. The transfer formula is independently checked against all simple paths of ladders with 1–6 squares.

**Related literature:** Kingan & Kingan, *On cyclically 4-connected cubic graphs* (2024), DOI 10.1080/09728600.2024.2333397 (exchange lemma on bridging squares); Roman Nedela, *Generation of cyclically 4-connected cubic graphs* (seminar notes on 4-reductions); On-Hei Solomon Lo, *A note on cycles in cyclically 4-edge-connected cubic planar graphs* (2026), DOI 10.1016/j.ejc.2026.104395. These references provide context; no priority or publication novelty is asserted for the min-max/strip calculus here.
