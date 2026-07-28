# The identical-terminal joint four-path spectrum: quantifier audit

**Status (corrected 2026-07-28; structurally superseded).**  This file
audits commit `3ba40fc`.
The earlier version confused an existential arithmetic escape with a
universal safety statement for three cross-theta pair types.  Those claims
are withdrawn below.  The audit is a hand proof about path-incidence
arithmetic, not a proof-assistant verification and not a graph census.
Its pairwise quantifier corrections remain valid conditionally, but
`type_t_ladder_saturation.md` observes that the identical-terminal premise
`X_x=y,X_y=x` was already eliminated by the pole-forcing theorem in ancestor
commit `7a3c1f7`.  Thus none of the incidence rows below is a live Type-T row.

The word attached to this continuation is **REDUCTION**.

## 0. Setup and the two different quantifiers

In the identical-terminal row, `X_x=y`, `X_y=x`, and the merged bridge
`B_2^{joint}` contains four distinguished `x`--`y` paths

\[
 |R_x|=2^{\rho_x},\quad |S_x|=2^{s_x}+1,
 \quad |R_y|=2^{\rho_y},\quad |S_y|=2^{s_y}+1,
\]

where all exponents are at least two.  After deleting the two gateway edges,
the four colored theta branches are

\[
 A=P_1^x,\quad B=P_2^x,\quad C=P_1^y,\quad D=P_2^y,
\]

of lengths `2^{rho_x}-1, 2^{s_x}, 2^{rho_y}-1, 2^{s_y}`.  Same-theta
branch-disjointness gives

\[
 \operatorname{int}(A)\cap\operatorname{int}(B)=\varnothing,
 \qquad
 \operatorname{int}(C)\cap\operatorname{int}(D)=\varnothing.
\]

There is no analogous conclusion for `A-C`, `A-D`, `B-C`, or `B-D`.

For two paths with no common-edge component, a noncrossing incidence with
`k` divergent cells has positive arc lengths `(a_i,b_i)`.  Each cell is an
actual simple cycle of length `a_i+b_i>=3`; the pair `(1,1)` cannot be a
divergent cell in a simple graph because both arcs would be the same edge.
The statements

- **existential escape:** some valid decomposition has no dyadic cell; and
- **universal safety:** every valid decomposition has no dyadic cell

are different.  An existential escape disproves forced contradiction, but
does not prove universal safety.  Common-edge components only add further
incidence freedom and cannot repair that quantifier implication.

## 1. A universal countertest for cross-theta pairs

Let two path lengths be `m,n>=2`.  For a fixed `k`, a positive composition
has `a_i,b_i>=1`, `sum a_i=m`, and `sum b_i=n`.  If `k=2` and `m+n>=7`, one
can choose the first arcs with `a_1+b_1=4`: choose

\[
 a_1\in[1,m-1],\qquad b_1=4-a_1\in[1,n-1].
\]

Such an integer exists because the two intervals overlap when `m,n>=2` and
`m+n>=6`.  In the applications below `m+n>=8`, so the remaining cell has
length at least four as well (and is therefore a valid simple-graph cell).
A two-rung ladder realizes these compositions as two simple paths, so the
first divergent cell is an actual `C_4`.

All four cross-theta path pairs in this problem have `m,n>=4`; consequently
every one admits an incidence pattern containing a forbidden `C_4`.  The
other two theta branches can be routed on fresh vertices, so this is also a
rooted four-path incidence realization respecting `A cap B` and `C cap D`.
This is a topological path-system statement only; it does not assert that the
ambient minimum-degree, bridge, and global cleanliness hypotheses can all be
completed.

Conversely, the following safe incidences exist.

- For unequal `(R_x,R_y)` exponents, the disjoint one-cell length is a sum of
  two distinct powers and hence is not a power of two.
- For equal `(R_x,R_y)` exponents, the two-cell family
  `(1,2^rho-1)` versus `(2,2^rho-2)` has cell lengths `3` and
  `2^{rho+1}-3`, both non-dyadic.
- For a mixed pair, the disjoint one-cell length
  `2^rho+2^s+1` is odd.
- For `(S_x,S_y)`, the disjoint one-cell length
  `2^{s_x}+2^{s_y}+2` has 2-adic valuation one and odd cofactor greater
  than one, so it is non-dyadic.

Thus all cross-theta types are **ESCAPABLE**, but none is universally safe.

## 2. Correct classification of all six unordered pairs

The requested categories refer to actual incidence patterns, not merely to
the existence of a convenient replacement pattern.

| unordered pair | correct classification | reason |
|---|---|---|
| `(R_x,S_x)` | **fixed by same-theta geometry; forced safe** | The paths share the gateway edge and then use the internally disjoint branches `A,B`.  Their unique divergent cell has length `2^{rho_x}+2^{s_x}-1`, which is odd. |
| `(R_y,S_y)` | **fixed by same-theta geometry; forced safe** | Symmetric to the preceding row, using `C,D`. |
| `(R_x,R_y)` | **safe incidence exists, but others may fail** | If disjoint, equal exponents force `C_{2^{rho+1}}` while unequal exponents are safe.  Even with equal exponents a safe two-cell incidence exists; for all exponents another two-cell incidence can expose `C_4`. |
| `(R_x,S_y)` | **safe incidence exists, but others may fail** | Disjoint is safe by parity.  The old two-cell construction proves only another safe incidence.  The countertest in Section 1 gives a valid two-cell incidence with a `C_4`. |
| `(S_x,R_y)` | **safe incidence exists, but others may fail** | Symmetric to `(R_x,S_y)`. |
| `(S_x,S_y)` | **safe incidence exists, but others may fail** | Disjoint is safe by valuation, but it is not a rerouting theorem for the supplied paths.  The countertest in Section 1 gives a two-cell incidence with a `C_4`. |

No cross-theta pair is a forced contradiction for every incidence pattern,
and no cross-theta pair is forced safe for every incidence pattern.  This
table deliberately does not promote an abstract path-system incidence to a
fully realizable `B_2^{joint}` under all ambient graph hypotheses.

## 3. What was wrong in commit `3ba40fc`

### 3.1 Mixed pairs

The construction

\[
 (1,2^\rho-1)\quad\hbox{versus}\quad(2,2^s-1)
\]

has safe cell lengths `3` and `2^rho+2^s-2`.  It proves **ESCAPABLE**.
It does not classify an arbitrary number of cells, and therefore does not
prove “always safe.”  For example, totals `(4,5)` admit

\[
 (a_1,a_2)=(1,3),\qquad (b_1,b_2)=(3,2),
\]

whose first cell is a `C_4`.

### 3.2 The `(S_x,S_y)` pair

The fact that a safe disjoint path system can be drawn does not permit the
actual supplied paths to be replaced by that drawing.  Without a rerouting
theorem preserving endpoints, lengths, simplicity, theta branch conditions,
and the canonical choices, this proves only **ESCAPABLE**.  For the smallest
totals `(5,5)`, the compositions `(1,4)` and `(3,2)` already expose a first
cell of length four.

### 3.3 The simultaneous conclusion

The former Level 2 asserted that only `A-C` mattered because the other five
pairs imposed no constraint under any configuration.  Sections 1--2 refute
that premise.  In particular, branch-disjointness within each theta says
that `B` avoids `A` and `D` avoids `C`; it says nothing about `A-D`, `B-C`,
or `B-D`.  A coincidence on `A-C` can constrain those other crossings, and
their divergent cells can themselves be dyadic.

Therefore the claimed reduction to the single yes/no question

> do `P_1^x` and `P_1^y` share an internal vertex?

is **withdrawn**.  A single shared vertex does not record the order of all
intersection components, shared segments, divergence/convergence points, or
the other three cross-theta incidences.  The correct primary object is the
rooted, color-preserving four-path incidence core with positive subdivision
lengths.

## 4. Consequences retained from the audited dependencies

The following statements survive this correction.

1. Same-theta pairs are fixed and safe by theta geometry.
2. Vertex-disjoint equal-length `R_x,R_y` force a dyadic cycle.
3. Equal-length `R_x,R_y` are not forced contradictory by arithmetic alone,
   because the displayed safe two-cell family exists.
4. Canonical tie-breaking does not imply one cell or zero overlap;
   `contraction_intersections.md` V.2 explicitly prevents that inference.
5. `B_1` and `B_2^{joint}` are distinct bridges of the same 2-cut, so their
   cross-bridge spectrum sums remain genuine cycles.  They do not determine
   the internal four-path incidence of `B_2^{joint}`.
6. T9B may be used only with its paired-replacement or deletion hypotheses;
   it supplies no finite incidence-core theorem by itself.

## 5. Correct residual scope, including `Q`

Before ambient graph structure is restored, the residual is the complete
rooted colored union `A union B union C union D`, with all terminals,
gateways, divergence/convergence points, common-component endpoints, and
color changes marked, degree-two unmarked vertices suppressed, and every
core edge assigned a positive subdivision length.  Isomorphisms must preserve
roots and colors.  Pairwise arithmetic is necessary but not sufficient;
all four colors must be handled simultaneously.

The triangle-contraction witness `Q` remains separate.  Conditional on `Q`
not adding another `x`--`y` path in `B_2^{joint}`, the residual is the
four-color incidence problem just stated.  If `Q` attaches at `{x,y}`, its
outside arc is a fifth distinguished color.  Attachments `{x,z}` and `{y,z}`
must be analyzed through their actual terminal pairs.  No statement in this
audit claims that the whole identical-terminal row has reduced to four paths
without this condition.

## 6. Audit conclusion

Commit `3ba40fc` correctly identified the same-theta geometry and exhibited
useful escaping decompositions, but its universal conclusions for both mixed
pairs and `(S_x,S_y)` were too broad.  The exact Phase-0 outcome is:

- two unordered pairs are fixed safe by same-theta geometry;
- the four cross-theta unordered pairs are escapable, with both safe and
  failing incidence patterns available at the abstract colored-path level;
- no cross-theta pair is universally safe or universally contradictory; and
- the one-question `A-C` reduction is invalid, so the four-color incidence
  core (and later `Q`) is the honest residual.
