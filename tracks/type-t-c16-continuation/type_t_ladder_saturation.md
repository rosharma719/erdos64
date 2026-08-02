# Type-T ladder saturation: the prerequisite row is impossible

**Status (2026-07-28).**  The proposed saturation program stops before ear
classification.  The alternating ladder was derived inside the
identical-terminal row `X_x=y, X_y=x`.  That row is already excluded by
`central_bridge_triangle_pole_forcing.md`, commit `7a3c1f7`, which is an
ancestor of the requested base commit `3ba40fc`.  Hence no canonical Type-T
alternating ladder exists to saturate.  This is stronger than proving that a
particular degree saturation fails.

The word remains **REDUCTION**.

## 1. Dependency audit before saturation

In the only surviving Type-T triangle type T2, write

\[
 T=\{x,y,z_0\},
\]

where `x,y` are cubic and `z_0` is the unique non-cubic triangle vertex.
For each cubic vertex `v`, its canonical theta has aligned pole
`X_v in T-{v}`.

`central_bridge_triangle_pole_forcing.md` proves:

> **Pole-forcing theorem.**  The aligned pole of a cubic Type-T vertex
> cannot be cubic.

The proof is local.  If `X_x` is cubic, its three incident edges are to `x`,
to the other triangle mate `Y_x`, and to its external neighbour.  `P_0`
uses `X_x x`; the outside-arc branch `P_2` avoids `Y_x`; and the two non-`P_0`
theta branches need distinct first edges at `X_x`.  Thus `P_1` is forced
through `Y_x`.  The chord `xY_x` then closes the `P_0/P_1` route into a
simple cycle of length exactly `2^{rho_x}`.

Therefore T2 forces

\[
 X_x=z_0,\qquad X_y=z_0.
\]

The identical-terminal row instead assumes

\[
 X_x=y,\qquad X_y=x.
\]

Both assumed poles are cubic, contradicting the pole-forcing theorem twice.
Already either equality alone is impossible.

### Theorem 1.1 (identical-terminal elimination)

There is no Type-T realization of the identical-terminal row.  In
particular, there is no merged bridge `B_2^{joint}` carrying the reported
four canonical paths, no alternating-ladder core arising from those paths,
and no minimum-degree-three saturation of such a core.

This conclusion does not use the A/A output, cell arithmetic, bridge
criticality, `B_1`, or `Q`.

## 2. What happened to the reported alternating ladder

The family in `type_t_overlap_reduction.md` remains a valid **abstract
four-colored path union**, but it is not a residual family of the Type-T
problem.  Its parameterization was:

\[
 \mathcal L=\{L_{\rho,k,t}: k\ge2\text{ even},\ 3k\le2^\rho,
 \ t\ge\rho+2\}.
\]

Put `L=2^rho` and `r=L-3k`.  In a chain of `k` cells, the two R-colored
arcs have alternating lengths `(1,5)` and `(5,1)`; add `r` to both arcs
of the first cell.  Both R paths then have length `L`.  The first cell has
length `6+2r=2(3+r)`, and every other cell has length six.  Fresh S branches
have stripped length `2^t`.

This scales for every **permitted value in that definition**, namely every
even `k`: choose any `rho` with `3k<=2^rho` and any `t>=rho+2`.  It was never
proved for odd `k`.  The smallest member is `L_{3,2,5}`, not the
`L_{2,2,t}` mistakenly suggested in the former search paragraph, since
`3*2>2^2`.

The colored-union cycle calculation remains correct as an abstract graph:
ladder-only cycles are the cells; a cycle using one long branch lies strictly
between `2^t` and `2^{t+1}`; and one using both lies strictly between
`2^{t+1}` and `2^{t+2}`.  What fails is the upstream claim that the colors
can simultaneously be the canonical thetas of the identical-terminal T2
row.

## 3. Arithmetic classification retained, with exact scope

The cell theorem is independent of pole forcing.  For two abstract paths,
let `m,n` be their divergent edge totals and let `k` be the number of
divergent simple-graph cells.  Every cell has length at least three, so
`3k<=m+n`; also `k<=m,n`.

For `k>=2`, writing `T=m+n`:

| total | exact classification |
|---|---|
| `T=3k` | universally safe: every cell is a triangle |
| `T=3k+1` | forced: exactly one cell is a `C4` |
| `T>=3k+2` | escapable but not universally safe |

For the last row, an unsafe composition uses cell sums
`4,3,...,3,T-3k+2`.  A safe composition reserves `k-2` triangles and
splits the remainder `U>=8` into two non-dyadic summands at least three.
Use `3+(U-3)` unless `U-3` is dyadic; in that exceptional odd case use
`5+(U-5)=5+(2^j-2)`.  For `k=1`, the only cell is forced exactly when
`m+n` is dyadic and otherwise is universally safe.

Thus the arithmetic theorem and its exponent-12 verification remain useful
elsewhere.  They no longer describe a live identical-terminal Type-T row.

## 4. Off-core components and ears: the valid generic lemma

For completeness, suppose some unrelated two-terminal bridge `B` has
2-connected closure `J=B+xy`, and let `H` be any connected core containing
the terminals.  If `K` is a component of `B-V(H)`, then

\[
 |N_H(K)|\ge2.
\]

Indeed, zero attachments contradict connectivity.  With one attachment `v`,
deleting `v` separates `K` from the rest of `J`, contradicting
2-connectivity.

This does **not** prove the proposed ear normal form.  If `|N_H(K)|=2`, the
component plus its attachment edges is a two-terminal network and contains
an attachment-to-attachment path, but replacing the whole component by that
path can destroy internal minimum degree, closure 2-connectivity, and the
terminal spectrum required by T9B.  If `|N_H(K)|>=3`, the block-cut lemmas
retain a genuine multi-terminal outcome; they do not reduce it to one ear.
Consequently no bounded local attachment state follows from the existing
lemmas alone.

## 5. Single-ear arithmetic, conditionally

If an internally core-disjoint ear `E` of length `e` joins core vertices
`u,v`, let

\[
 D_H(u,v)=\{|P|:P\text{ is a simple }u\text{-}v\text{ path in }H\}.
\]

Every cycle using `E` is exactly `E union P` for some such path, and hence
has length `e+d`, `d in D_H(u,v)`.  Therefore:

- it forces a `C4` exactly when `4-e in D_H(u,v)`;
- it forces a `C8` exactly when `8-e in D_H(u,v)`;
- it forces some power cycle exactly when
  `D_H(u,v)` meets `{2^j-e:j>=2}`; and
- it is arithmetically safe by itself exactly when that intersection is
  empty.

This is the complete single-ear arithmetic.  Endpoint distance, rail,
cell index, and subdivision offset are simply coordinates for computing
`D_H(u,v)`.  There is no reason to enumerate those coordinates for the
eliminated Type-T ladder.

## 6. Why no transfer or saturation search is run

A sound transfer model must first have a realizable start state.  The
pole-choice constraints give none for the identical-terminal row.  Hence the
complete state graph has:

\[
 \text{initial states}=\text{accepting states}=0.
\]

Adding degree-deficit, open-ear, connectivity, residue, criticality, or `Q`
fields cannot restore a state already excluded by the canonical-theta
prerequisites.  Running SAT on chord matchings or longer ladders would answer
only a detached abstract-graph question and could not establish a Type-T
realization.

`verifier/type_t_ladder_states.py` independently enumerates the four T2 pole
rows and confirms that pole forcing leaves only `(X_x,X_y)=(z_0,z_0)`, the
one-common-terminal row.  `verifier/type_t_ladder_saturation_sat.py` takes the
pole-forcing theorem as an input, encodes it together with the
identical-terminal requirements as a Boolean prerequisite CNF, and confirms
their inconsistency by exhaustive assignments and elementary DPLL.  It is a
prerequisite-consistency check, **not** an independent verification of the
pole-forcing theorem.  Neither script calls the abstract colored core a graph
realization.

## 7. Q track

`Q` cannot rescue the eliminated row.  For any quotient cycle, `Q` chooses
one pair of triangle attachments, but it does not change the canonical pole
of `Theta_x` or `Theta_y` and cannot make a cubic aligned pole permissible.
The live T2 row is `(X_x,X_y)=(z_0,z_0)`; any future `Q` analysis belongs to
that one-common-terminal geometry, not to a fifth-color extension of an
identical-terminal ladder.

## 8. Saturation conclusion

The preferred outcome is stronger than the proposed ear alternatives:

\[
 \boxed{\text{No alternating-ladder saturation exists, because the
 identical-terminal canonical-theta row itself is impossible.}}
\]

The infinite colored ladder is useful negative information about abstract
path arithmetic, but it is not an infinite residual family of the current
Type-T proof.
