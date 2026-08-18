# Triangle chords in the 5-odd-connected factor reduction

**Date:** 2026-08-01
**Status:** hand reduction from the Candráková–Lukoťka 2-factor theorem and elementary cycle switching.

## Theorem

Let `G` be a connected bridgeless simple cubic graph with no power-of-two cycle. Choose a perfect matching `M` whose complementary 2-factor `F=G-M` has 5-odd-edge-connected contraction, as supplied by Candráková–Lukoťka.

Then:

1. `F` has no triangle component.
2. Every triangle of `G` contains exactly one edge of `M`.
3. On its factor component, that matching edge is a chord joining vertices at cyclic distance two.
4. The length-two factor arcs supporting distinct triangles are vertex-disjoint.
5. If a factor component has length `m` and supports `t` triangles, then `G` contains cycles of every length

   `m-t, m-t+1, ..., m`.

Consequently, writing `P(m)=2^floor(log2 m)`,

\[
t\le m-P(m)-1.
\]

In particular, a factor cycle of length `2^r+1` supports no triangle.

## Proof

Contract every component of `F`. If `F` contained a triangle component, the corresponding quotient vertex would have exactly three matching edges leaving it. Its singleton cut would be an odd cut of size three, contrary to 5-odd-edge-connectivity. This proves (1).

A matching contains at most one edge of a triangle. If a triangle contained no matching edge, all three of its edges would belong to `F`, making it a triangle component. Therefore it contains exactly one matching edge, proving (2).

The other two triangle edges lie consecutively on one component of `F`; the matching edge joins the endpoints of this two-edge arc. This proves (3).

A cubic graph with no `C4` has vertex-disjoint triangles. Hence the supporting two-edge arcs are vertex-disjoint, proving (4).

Start with the factor cycle of length `m`. For any selected subset of `s` triangle chords, replace each of the corresponding two-edge factor arcs by its matching chord. The arcs are vertex-disjoint, so all replacements can be made independently and the result remains one simple cycle. Each replacement shortens the cycle by one, yielding a cycle of length `m-s`. As `s` ranges from zero through `t`, every length from `m-t` through `m` occurs. This proves (5).

The interval cannot contain the largest power of two `P(m)` below `m`. Since `m` itself is not a power of two, one must have `m-t>P(m)`, or `t<=m-P(m)-1`. ∎

## Additional quotient constraints

Let `x(C)` be the number of matching edges with both endpoints on a factor component `C`.

- If `|C|` is odd, the singleton quotient cut has odd size `|C|-2x(C)` and therefore has size at least five. Hence
  \[
  x(C)\le \frac{|C|-5}{2}.
  \]
- If `|C|` is even, connectedness and parity force at least two matching edges to leave `C`, so
  \[
  x(C)\le \frac{|C|-2}{2}.
  \]

Every triangle chord is one of these internal matching edges. Thus the triangle count on a factor component obeys both the dyadic-gap bound above and the relevant quotient-capacity bound.
