# Type-T identical-terminal overlap reduction

**Status (2026-07-28).**  This continues the corrected Phase-0 audit in
`type_t_identical_terminal_joint_spectrum.md`.  It proves the exact arithmetic
classification for arbitrary valid cell counts, defines the four-color
incidence core, records the precise limit of path splicing and canonical
tie-breaking, and exhibits one scalable alternating-ladder residual.  It does
not claim a full minimal-counterexample realization or eliminate Type T.

## 1. The four-color incidence object

In the merged bridge `B_2^{joint}`, retain the two gateway edges and the four
theta branches

\[
 A=P_1^x,\quad B=P_2^x,\quad C=P_1^y,\quad D=P_2^y.
\]

Their branch lengths are

\[
 |A|=2^{\rho_x}-1,\quad |B|=2^{s_x},\quad
 |C|=2^{\rho_y}-1,\quad |D|=2^{s_y}.
\]

The gateway-completed paths are `R_x=x x'+A`, `S_x=x x'+B`,
`R_y=y y'+C`, and `S_y=y y'+D`.  By theta geometry,

\[
 \operatorname{int}(A)\cap\operatorname{int}(B)=\varnothing,
 \qquad
 \operatorname{int}(C)\cap\operatorname{int}(D)=\varnothing.
\]

No cross-theta disjointness is inherited.

For a realization `H=A union B union C union D`, mark:

1. `x,y,x',y'` and all theta poles;
2. every endpoint of a maximal common colored segment;
3. every divergence or convergence vertex;
4. every vertex where the set of incident colors changes; and
5. every vertex whose degree in `H` is not two.

Suppress every unmarked degree-two vertex.  Each resulting edge records its
nonempty color set, its orientation within each color that uses it, and its
positive subdivision length.  The roots and color names are fixed: neither
interchanging `x,y` nor permuting `A,B,C,D` is an equivalence unless it is
explicitly part of the rooted data.  Thus equivalence is rooted,
color-preserving topological isomorphism with the same integer edge lengths.

This core is finite for each realization, but its size is not bounded by the
four prescribed path lengths uniformly over the exponents.

## 2. Exact arithmetic for every cell count

Let two actual simple paths have divergent colored edge totals `m,n`.  Common
segments have already been removed from these totals.  Suppose a chosen
noncrossing symmetric-difference decomposition has `k` divergent cells, with
positive arc contributions `(a_i,b_i)`.  Because the ambient graph is simple,

\[
 a_i+b_i\ge3;
\]

`(1,1)` would be the same edge twice and is a common component, not a
divergent cell.  Hence a valid `k` must satisfy

\[
 k\le m,\qquad k\le n,\qquad 3k\le m+n.
\]

Call a decomposition **forced** when it contains a cell in
`F={4,8,16,...}`, **safe** when it contains none, and **escapable** when at
least one safe decomposition exists.

### Theorem 2.1 (complete composition classification)

Put `T=m+n`.

| cell count | classification |
|---|---|
| `k=1` and `T` dyadic | **FORCED** |
| `k=1` and `T` not dyadic | **UNIVERSALLY SAFE** |
| `k>=2` and `T=3k` | **UNIVERSALLY SAFE** |
| `k>=2` and `T=3k+1` | **FORCED** |
| `k>=2` and `T>=3k+2` | **ESCAPABLE, BUT NOT UNIVERSALLY SAFE** |

**Proof.**  Record only the cell sums `c_i=a_i+b_i`.  Conversely, for any
`c_i>=3` with sum `T`, all integer totals from `k` through `T-k` can be
obtained as `sum a_i` with `1<=a_i<=c_i-1`: sums of integer intervals are
integer intervals.  The prescribed `m` is in that range because `m,n>=k`.
Thus it is enough to classify compositions of `T` into `k` integers at least
three.

For one cell the assertion is immediate.  For `k>=2`, `T=3k` forces every
cell sum to be three.  If `T=3k+1`, exactly one cell sum is four and all
others are three, so a `C_4` is unavoidable.

For `T>=3k+2`, an unsafe decomposition is obtained by fixing one cell sum
four, fixing `k-2` sums to three, and putting the remaining value (at least
five) in the last cell.  A safe decomposition is obtained by reserving
`k-2` sums equal to three and writing

\[
 U=T-3(k-2)\ge8
\]

as two non-dyadic integers at least three.  If `U` is even, use
`3+(U-3)`, whose second term is odd.  If `U` is odd and `U-3` is not a power
of two, use the same split.  Otherwise `U-3=2^j`; since `U>=9`, `j>=3`, and
`5+(2^j-2)` works because `2^j-2` is even with an odd cofactor greater than
one.  This proves existence in every case.  `square`

The exceptional forced layer `T=3k+1` is invisible if one permits the
non-simple `(1,1)` cell.  Enforcing simple-graph validity is therefore
essential, not cosmetic.

### 2.2 Application to the six path pairs

The same-theta pairs remain fixed safe, not instances of the free
composition theorem.  For each cross-theta pair, apply Theorem 2.1 to the
divergent totals after subtracting all common colored segments.  In the
no-common-edge model, use the whole-path totals

\[
 (2^{\rho_x},2^{\rho_y}),\quad
 (2^{\rho_x},2^{s_y}+1),\quad
 (2^{s_x}+1,2^{\rho_y}),\quad
 (2^{s_x}+1,2^{s_y}+1).
\]

The result is not a single label per exponent pair: it depends on the actual
cell count.  In particular, every cross-pair type has safe incidences and
incidences containing `C_4`, while some high-cell-count layers satisfying
`T=3k+1` are forced contradictory.  This is the exact existential/universal
separation requested in Phase 2.

`verifier/type_t_cell_decompositions.py` independently enumerates every valid
composition for `m,n<=10`, proves exact agreement with the table, and then
checks the closed classification for all four cross-pair length types, all
exponent pairs through 12, and every cell count allowed by the three displayed
inequalities.  Its saved smallest counterexamples include totals `(4,5)` for
a mixed pair and `(5,5)` for the `S-S` pair.

## 3. What minimality and splicing actually license

Suppose two cross-theta colors meet at `u`, separate, and next meet at `v`.
If the two `u`--`v` arcs have lengths `a,b`, replacing the first arc by the
second changes its path length by `b-a`.  It preserves the prescribed length
only when `a=b`.  Even then, four further facts must be checked:

1. the replacement does not meet the retained prefix or suffix internally;
2. the result is a simple path with the same ordered endpoints;
3. it remains internally disjoint from its same-theta mate; and
4. it remains an eligible canonical theta branch with the same witness data.

Neither `contraction_intersections.md` nor the canonical tuple in
`contraction_central_bridge.md` supplies these facts automatically.  In
particular, minimizing shared edges or common components does not minimize
the number of divergent cells.  T9B also does not license this splice: its
replacement form requires a complete two-terminal replacement satisfying
closure 2-connectivity, internal degree, internal cleanliness, and the paired
spectrum inclusion conditions.

Consequently, lexicographic minimality gives the following valid but limited
statement: a selected residual cannot contain an **eligible equal-length
splice** that passes all four checks and strictly improves the selected core
tuple.  It does not remove a general repeated intersection component, does
not bound the number of cells, and does not reduce arbitrary crossings to a
single common vertex or segment.

## 4. A precise scalable alternating-ladder residual

The absence of a general splicing theorem is witnessed by an explicit
simultaneous four-path family.  This is a colored incidence family, not a
completed minimum-degree-three counterexample.

Choose an even integer `k>=2`, an exponent `rho` with `3k<=2^rho`, and put

\[
 L=2^\rho,\qquad r=L-3k.
\]

Then `r` is a nonnegative even integer.  Form a series chain of `k` divergent
cells between `x` and `y`.  In odd-numbered cells give the `R_x,R_y` arcs
lengths `(1,5)`; in even-numbered cells use `(5,1)`.  Add `r` to both arc
lengths in the first cell.  Because `k` is even, each of the two colored
`x`--`y` routes has length

\[
 3k+r=L=2^\rho.
\]

Every cell except the first has length six.  The first has length

\[
 6+2r=2(3+r),
\]

whose cofactor is odd and at least three; hence it is not dyadic.  Designate
the first edge on the `R_x` route as `x x'` and the last edge on the `R_y`
route as `y y'`.  Removing these edges leaves branches `A,C` of the required
length `2^rho-1`, with `x'!=y'`.

Now choose `t>=rho+2`.  Attach a fresh `x'`--`y` branch `B` of length `2^t`
and a fresh `y'`--`x` branch `D` of length `2^t`, internally disjoint from the
ladder and from one another.  The gateway-completed `S` paths have length
`2^t+1`, and `A\cap B`, `C\cap D` have only their theta poles in common.
This realizes the prescribed equal-exponent choice
`rho_x=rho_y=rho`, `s_x=s_y=t`.

### 4.1 All cycles in the colored union are non-dyadic

A cycle using neither long branch is one ladder cell, already checked.  A
cycle using exactly one of `B,D` has length `2^t+q`, where `q` is a positive
route length in the ladder union and `q<2^t` because that union has total
length `2L<2^t`.  It lies strictly between consecutive powers of two.  A
cycle using both long branches has length `2^{t+1}+q`, with
`0<q<2^{t+1}`; again it lies strictly between powers.  The outer `B-D` cycle
has the familiar length `2^{t+1}+2`, also non-dyadic.  Thus the entire colored
union, not merely the four distinguished pair sums, is power-cycle-free.

The union is connected after deleting `x,y`, so it is a genuine component
bridge of `{x,y}` at the colored-union level.  Adding `xy` makes the closure
2-connected: deleting a ladder junction leaves the two sides joined through
`xy`, deleting an internal arc or long-branch vertex leaves its alternate
route, and deleting either terminal leaves the chain connected through the
other colored routes.

The rooted incidence cores are pairwise nonisomorphic as `k` varies, because
they contain different numbers of ordered divergence/convergence junctions.
This is therefore one precise infinite residual family:

\[
 \boxed{\mathcal L=\{L_{\rho,k,t}: k\ge2\text{ even},\ 3k\le2^\rho,
 \ t\ge\rho+2\}.}
\]

It proves that four-path incidence plus complete cycle arithmetic and closure
2-connectivity do not yield a finite core list.

## 5. Restoring ambient graph structure: the remaining bottleneck

The family `\mathcal L` deliberately exposes the exact missing hypothesis.
The internal vertices subdividing its colored arcs and long branches have
degree two in the union, whereas an internal vertex of the actual bridge has
ambient degree at least three.  Additional ears or attachments must saturate
them.  Those additions can create new `C_4,C_8,C_16,...` cycles and can change
the attachment core.

The audited structural lemmas imply:

- extra edges cannot leave the genuine `{x,y}` component bridge except
  through `x` or `y`;
- the closure must remain 2-connected;
- deleting an irrelevant attachment is licensed only when the degree,
  closure, and paired-spectrum hypotheses of T9B still hold; and
- every real R/P-skeleton edge covered by T9B meets an internal cubic vertex,
  but this criticality statement does not bound the number of such vertices
  or ears.

No cited theorem bounds a saturation of `mathcal L`, and no valid contraction
of all degree-two positions follows from T9B.  Therefore the honest Phase-4
residual is:

> classify or eliminate minimum-degree-three, power-cycle-free saturations of
> the rooted weighted ladder family `mathcal L`, while preserving the genuine
> bridge, closure, same-theta, and paired-spectrum conditions.

This is more precise than “arbitrary large graph”: the unsaturated colored
core is fixed by `(rho,k,t)` and only its degree-saturating attachments remain
unknown.  It is not yet a bounded attachment pattern.

The other bridge `B_1` continues to impose all cross-cut spectrum sums.  The
known high-exponent arithmetic families show these sums do not by themselves
eliminate `mathcal L`; constructing an actual compatible `B_1` is nevertheless
part of full realizability and is not asserted here.

## 6. The triangle-contraction witness `Q`

The reduction above is conditional on `Q` not supplying another `x`--`y`
path inside `B_2^{joint}`.

- If `att(Q)={x,y}`, its outside arc is a fifth distinguished color.  It must
  be added to the already-defined weighted core; the four-color arithmetic
  cannot be reused as if the path were absent.
- If `att(Q)={x,z}`, it is not an additional `x`--`y` path in this bridge.
  Its cycles must be closed through the actual `x`--`z` routes and its
  interaction belongs to that terminal pair.
- If `att(Q)={y,z}`, the symmetric statement holds for `y,z`.

The last two cases justify the conditional four-color formulation but do not
make `Q` irrelevant globally.  The first case is a five-color extension of
`mathcal L`, not a restart from unrestricted graphs.

## 7. Why realizability search is deferred

Phase 6 was conditioned on obtaining finitely many reduced colored cores.
Section 4 instead proves a precise infinite incidence family, and Section 5
identifies degree saturation as the unresolved structural step.  Accordingly
no unrestricted graph search, SAT model, or claimed equal-exponent
realizability test is started here.  A sound next model would parameterize a
fixed small member such as `L_{2,2,t}`, require every added edge to saturate a
recorded degree-two position, and enforce the bridge, closure, all-cycle, and
T9B conditions explicitly.  A result for that one member would not eliminate
the scalable family without a symbolic saturation reduction.

## 8. Reduction achieved

Conditional on `Q` adding no fifth `x`--`y` color, the identical-terminal
overlap question has the following exact status.

1. Pairwise cell arithmetic is completely classified for every valid cell
   count by Theorem 2.1.
2. Same-theta pairs are fixed safe; every cross-theta type has both safe and
   failing incidences, with additional forced `T=3k+1` layers.
3. Canonical minimality does not license unequal-length splicing and hence
   does not bound repeated intersection components.
4. Complete four-path incidence arithmetic admits the explicit infinite
   alternating-ladder family `mathcal L`.
5. The remaining graph-theoretic question is the saturation of that rooted
   family (plus compatible `B_1`), and `{x,y}`-attached `Q` adds a fifth color.

Thus the outcome at the present proved boundary is one precise infinite
residual family, not a contradiction and not a finite gadget list.
