# Triangle Mersenne saturation in a cubic minimal counterexample

**Date:** 2026-08-01
**Status:** hand theorem, conditional only on the already-established nontriangle-edge witness lemma in `contraction.md`.

## Setting

Let `G` be a globally minimal cubic counterexample to the Erdős–Gyárfás conjecture. Thus `G` has no cycle whose length is a power of two. We use the established lemma:

> **Nontriangle-edge witness lemma.** Every edge of `G` that lies in no triangle belongs to a cycle of length `2^k+1`.

Call such a cycle a **Mersenne witness** for the edge.

## Theorem

Let `T=abc` be a triangle of `G`, and let `aa'`, `bb'`, `cc'` be the three edges leaving `T`.

1. At least two of the three triangle edges `ab,bc,ca` lie on Mersenne cycles.
2. Some external edge among `aa',bb',cc'` lies on two distinct Mersenne cycles that traverse two different edges of `T`.
3. Consequently, every edge of `G` except possibly one edge in each triangle lies on a Mersenne cycle.

## Proof

Because `G` is cubic and contains no `C4`, distinct triangles are vertex-disjoint. Two triangles sharing only one vertex would give that vertex at least four distinct neighbours. Two triangles sharing an edge, say `ab`, with third vertices `c,d`, would create the 4-cycle `c-a-d-b-c`.

Hence each external edge `aa'`, `bb'`, `cc'` lies in no triangle. By the nontriangle-edge witness lemma, choose Mersenne cycles `C_a,C_b,C_c` containing these three external edges.

Consider `C_a`. A simple cycle containing `aa'` must enter the triangle at `a` and leave it through exactly one of `bb'` or `cc'`. Suppose it leaves through `bb'`. Inside `T`, it can use either the edge `ab` or the two-edge route `a-c-b`.

The second possibility is impossible. Replacing `a-c-b` by `ab` produces a simple cycle one edge shorter. Since `C_a` has length `2^k+1`, the replacement would have length `2^k`, contrary to the defining property of `G`.

Thus every selected external-edge witness traverses `T` through a single triangle edge. Associate to `C_a,C_b,C_c` the triangle edge each uses. The edge associated to `C_a` is incident with `a`, and similarly at `b,c`. Therefore the set of associated triangle edges covers all three vertices of `T`. One edge cannot cover all three vertices, so at least two distinct triangle edges occur. This proves (1).

Any two distinct edges of a triangle share a vertex, say the two witnessed edges are `ab` and `ac`. A Mersenne cycle using `ab` necessarily contains both external edges `aa'` and `bb'`; a Mersenne cycle using `ac` necessarily contains both `aa'` and `cc'`. Hence `aa'` lies on two distinct Mersenne cycles using different triangle edges. This proves (2).

All nontriangle edges already have witnesses. Part (1) leaves at most one unwitnessed edge in each triangle, proving (3). ∎

## Quantitative corollary

Triangles in a `C4`-free cubic graph are vertex-disjoint, so their number `t` is at most `n/3`. Since a cubic graph has `3n/2` edges, at least

\[
\frac{3n}{2}-t \ge \frac{7n}{6}
\]

edges lie on Mersenne cycles. Thus at least a `7/9` fraction of all edges are Mersenne-witnessed.

## Structural consequence

Every triangle anchors a **forked Mersenne theta**: an external edge is shared by two distinct Mersenne cycles, and the cycles leave the triangle through its two different incident triangle edges. The remaining all-order problem is to control their later reintersections. Equal-length forks cannot rejoin only once, because their symmetric difference would be a power-of-two cycle; unequal-length forks remain the principal arithmetic case.
