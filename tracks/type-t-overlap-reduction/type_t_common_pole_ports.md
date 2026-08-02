# Degree-four Type-T common-pole shared ports

**Status (2026-07-28): REDUCTION — EXPLICIT INFINITE PORT RESIDUAL.**
This file localizes every part of a shared-port outcome that the current
degree-four hypotheses actually determine, gives the complete local route
formulas, tests the proposed port-normalization argument, and proves that the
currently available local inputs cannot yield a finite rooted metric list.
The surviving family is a rooted incidence family, not a completed
minimum-degree-three graph and not a counterexample candidate.

## 1. Setup and the exact meaning of `P`

Work in the only live pole geometry and specialize to degree four:

\[
 T=\{x,y,z_0\},\qquad d(x)=d(y)=3,\qquad d(z_0)=4,
 \qquad X_x=X_y=z_0.
\]

For `Theta_x`, write

\[
 p=z_0,\qquad q=x',\qquad v=x,
\]

and let its three `p`--`q` branches be

\[
 P_0=p-v-q\quad(|P_0|=2),\qquad
 A\quad(|A|=M=2^{\rho_x}-1),\qquad
 B\quad(|B|=N=2^{s_x}).
\]

The `y`-theta uses `C,D` symmetrically.  Degree four permits only
`E2_parallel` (`AC | BD`) and `E2_cross` (`AD | BC`).

A genuine MA2 shared-port output retains more than the number 2.  It consists
of a selected multiply-marked leaf of the central bridge, two distinct theta
attachments `r,s`, and one component vertex `u` adjacent to both:

\[
 r-u-s.
\]

The path lies outside the relevant theta except at `r,s`.  For every simple
`r`--`s` route `R` that is internally disjoint from `u`, `R union r-u-s` is a
simple cycle of length `|R|+2`.  Therefore

\[
 |R|=2^m-2
\]

is the exact contradiction criterion.  Routes meeting `u` internally do not
combine with the port path into a simple cycle and must not be counted.

## 2. Exact attachment-location classification [PROVED]

Every vertex of `Theta_x` is exactly one of

\[
 p=z_0,\quad q=x',\quad v=x,\quad
 \operatorname{int}(A),\quad \operatorname{int}(B).
\]

Hence every unordered shared-port attachment pair has one of the following
types:

1. two internal points of `A`;
2. two internal points of `B`;
3. one internal point of each of `A,B`;
4. `q=x'` and one internal branch point;
5. `p=z_0` and `v=x`;
6. `p=z_0` and an internal point which is literally `y'`;
7. `v=x` and an internal point which is literally `y'`;
8. both theta poles, retained only as an abstract route case—it is locally
   impossible at degree four.

There are no other types.  The named four-color locations in the task refine
types 1--4, rather than creating new theta-route formulas:

- “on a common prefix”, “at the first divergence”, “after a
  reconvergence”, and “on a later shared segment” mark a coordinate on `A`
  or `B` together with extra cross-color incidence;
- “on two suffixes of one shared bundle” can only mean two marked positions
  on the same relevant branch after its cross-theta split;
- “branches using different first edges” is type 3, since `A,B` have
  different first edges in both E2 states.

The effect of later cross-color incidence is addressed in Section 4.  It can
add routes, but it does not alter the exhaustive list of possible attachment
vertices on the relevant theta.

### 2.1 Special named vertices

For a nontrivial component central bridge, `y` is outside `Theta_x`; if `y`
were on `Theta_x`, the central bridge containing `xy` would be the chord
case, not an attachment-rich leaf.  Thus `y` is not a `P_x` attachment.

The center `x`, however, is the pinned central-bridge attachment carried by
the edge `xy`.  It cannot be discarded from this Type-T specialization by
the generic “center is vacuous” row of the old leaf-block route census.  The
actual central bridge has attachments `x,z_0` through the triangle vertex
`y`, and the route formulas below retain this fact.

Lemma NE gives `x'!=y'`.  The vertex `y'` creates no new location type: it can
be a `P_x` attachment only if cross-theta incidence places it at an internal
point of `A` or `B`.  The point `x'` is already the far pole `q`.

## 3. Complete port-compatible route formulas [PROVED]

There is no pole edge `pq=z_0x'`: Lemma NA in
`central_bridge_triangle.md` excludes it.  On the other hand the triangle
adds a simple `p`--`q` route

\[
 p-y-v-q
\]

of length 3, beside `P_0` of length 2.  For a generic port `u!=y`, both
routes must be included.  This is the extra route source that a theta-only
`P` template does not see.

Distances below are measured from `p`.

### 3.1 Generic ports (`u!=y`)

**Same branch `A`.**  For positions `0<a<b<M`, the complete four-route list
is

\[
\boxed{
 b-a,\quad
 a+2+(M-b),\quad
 a+3+(M-b),\quad
 a+N+(M-b)}.
\]

For two points on `B`, exchange `M,N`.

**Different branches.**  For `r in A` at distance `a` and `s in B` at
distance `b`, the complete six-route list is

\[
\boxed{
\begin{aligned}
 &a+b,\quad (M-a)+(N-b),\\
 &a+2+(N-b),\quad (M-a)+2+b,\\
 &a+3+(N-b),\quad (M-a)+3+b.
\end{aligned}}
\]

The first line closes at one pole, the second uses `P_0`, and the third uses
the triangle detour.

**Far pole.**  For `q=x'` and a point of `A` at distance `a`, the four routes
are

\[
\boxed{M-a,\quad a+2,\quad a+3,\quad a+N}.
\]

Again exchange `M,N` for a point on `B`.

For every displayed value `d`, the port survives only if

\[
 d\ne2^m-2.
\]

The formulas are exhaustive in the triangle-plus-theta subgraph.  Any later
four-color reconvergence can add further routes; it cannot delete these.

### 3.2 A port containing `z_0` or `x`

At degree four, the only edge at `p=z_0` outside `Theta_x` is `z_0y`, and
the only edge at `v=x` outside `Theta_x` is `xy`.  Thus any shared port
containing `p` or `v` has

\[
 u=y.
\]

Since `y` is cubic with neighbours exactly `x,z_0,y'`, its other attachment
is forced to be one of those vertices and must also lie on `Theta_x`.

- `p,v` give the fixed path `z_0-y-x`.  The internally `y`-avoiding theta
  routes have lengths
  \[
  \boxed{1,\quad M+1,\quad N+1}.
  \]
- If `p` is paired with `y'` at distance `a` on `A`, the internally
  `y`-avoiding routes are
  \[
  \boxed{a,\quad M-a+2,\quad M-a+N}.
  \]
- If `v` is paired with that same point, the internally `y`-avoiding routes
  are
  \[
  \boxed{1+a,\quad1+M-a,\quad1+N+a,\quad1+N+M-a}.
  \]

The symmetric `B` formulas exchange `M,N`.  The length-three triangle route
is omitted here for a precise reason: it passes through the port vertex
`u=y`, so adjoining the port path would repeat `u` and would not form a
simple cycle.

The pair `p,q` is impossible at degree four: its port would have to be `y`,
but Lemma NA says `yx'` is not an edge.  Abstractly, even if a different
shared port existed, the theta route `P_0` has length 2 and would close with
the port path to a `C_4`.  The pair `v,q` is likewise impossible because
`v`'s only port is `y` and `yq` is absent.

## 4. E2 placement and cubic saturation [PROVED where stated]

In either E2 state, each nontriangle first neighbour of `z_0` is cubic.
For `P_x`, both such vertices lie on `A` or `B`, hence on `Theta_x`.
The internal port `u` is outside `Theta_x`; consequently:

- `u` cannot be either first neighbour;
- `u` cannot lie on an `A`/`B` common prefix or be its divergence vertex;
- `u` may lie on an other-theta-only suffix after divergence, or outside
  the four-color union entirely.

Thus a port edge need not leave the entire four-color union, but it always
leaves the relevant theta.

If a shared cross-theta pair splits immediately at its first neighbour, that
cubic vertex uses the edge to `z_0` and the two outgoing branch edges.  It is
saturated and cannot be a port attachment.  If the common prefix continues,
the first neighbour uses two prefix incidences and has exactly one spare
cubic incidence, so it can be one attachment but cannot support two distinct
port edges.

The same conclusion does **not** propagate to every later prefix vertex.
M1 forces a neighbour of the high-degree vertex `z_0` to be cubic; it does
not force vertices at distance two or more from `z_0` to be cubic.  A later
prefix or divergence vertex may be cubic or high-degree.  Therefore the
suggested statement “every internal prefix vertex has exactly one ambient
edge” is not available.

No separator or replaceable ear follows from these incidences.  A port is a
literal adjacency in one selected MA2 leaf.  Other branch groups and the leaf
remainder can bypass its rooted segment, while T9B replaces only a complete
Type-B bridge under its full spectrum and connectivity hypotheses.

## 5. Why the proposed port normalization fails

Choose a shared-port realization lexicographically by distance, common
components, divergence/re-entry events, and rooted size, as proposed.  This
selects one of the shared ports already present in the graph.  It does not
create a new common neighbour closer to `z_0`.

The only available upstream port conversion is the distinct-port theorem in
`contraction_leaf_blocks.md` VII.2--3.  It produces an A-type admissible pair
when the two attachments have **different** ports.  It does not apply to the
defining `P` case `phi(r)=phi(s)=u`.  Moving one attachment to a different
port would require a new adjacency and would not preserve the selected MA2
leaf or its shared-port origin.

Likewise, swapping tails at a later intersection preserves a shared port
only if the same literal vertices remain adjacent to the same `u`; in that
case the attachment positions have not moved.  No current canonical-witness
or replacement theorem proves a closer shared port exists.  Minimality is
therefore descriptive, not a normalization operation.

The next section supplies a scalable family in which the only displayed
nontriangle ports can be placed arbitrarily far from `z_0`, while every cycle
of the full displayed triangle/theta/port union remains non-dyadic.

## 6. Explicit infinite degree-four `(P,P)` port-incidence family [PROVED]

Let

\[
 Y=2^j\quad(j\ge4),
\]

and choose

\[
 (\rho_x,s_x,\rho_y,s_y)=(j+2,2,j,2).
\]

Thus

\[
 |A|=4Y-1,\quad |B|=4,\quad |C|=Y-1,\quad |D|=4.
\]

Use `E2_parallel` with

\[
 h_{AC}=h_{BD}=1,
\]

so both first neighbours split immediately and are saturated cubic vertices.
Choose arbitrary integers

\[
 2\le a\le |A|-8,
 \qquad 2\le c\le |C|-8.
\]

Put a port pair at the two `A`-positions `a,a+7`, with a new common neighbour
`u_x`, and a second port pair at the `C`-positions `c,c+7`, with common
neighbour `u_y`.  Each attachment uses its two branch edges and one port
edge, so it is cubic.  Give each `u_i` one pending edge into its selected MA2
leaf remainder; then `u_i` also has the required cubic local incidence.

The displayed rooted graph includes all of:

- the full triangle `z_0xy`;
- both `P_0` branches `z_0-x-x'` and `z_0-y-y'`;
- all four branches `A,B,C,D` with the two length-one common prefixes; and
- both length-two port paths.

It has exactly **61 simple cycles**.  Their lengths do not depend on `a` or
`c`: in every cycle, entering a marked branch interval forces the complementary
left/right coordinates to cancel.  Every length has the form `kY+b` in one
of the following exact bands:

| `k` | possible `b` |
|---:|---|
| 0 | `3,6,7,9,10` |
| 1 | `-4,-3,-2,1,2,3,6,7,8` |
| 4 | `-4,-3,-2,1,2,3,6,7,8` |
| 5 | `-11,-10,-8,-7,-6,-5,-3,-2,-1,0,2,3` |

None is a power of two:

- the five constants are non-dyadic;
- `Y+b` lies strictly between `Y/2` and `Y`, or strictly between `Y` and
  `2Y`;
- `4Y+b` lies strictly between the adjacent powers `2Y,4Y` or `4Y,8Y`;
- `5Y+b` lies strictly between `4Y` and `8Y` because `Y>=16` and
  `|b|<=11` (including `5Y`, which has odd factor 5).

The verifier enumerates all 61 cycles, derives 35 distinct affine forms with
their exact multiplicities, proves the `a,c` coefficients vanish, and checks
three widely separated translations for every `j+2` from 6 through 14.
Deleting either port leaves a one-port core with 40 simple cycles, all a
subset of the same safe spectrum.

This is an **explicit infinite rooted metric family**: `Y`, `a`, and `c` are
unbounded, and the marked distances from `z_0` are preserved by rooted
isomorphism.  It disproves localization of all minimal ports to poles, first
neighbours, or first divergences from the presently available local and
cycle-arithmetic inputs.

### Exact scope of the family

The pending leaf edges record the incidence required for `u_x,u_y` to enter
their selected leaf remainders, but those remainders and the rest of the
ambient minimum-degree-three graph are not completed.  A completion can add
new cycles.  Therefore this is a port-incidence residual, not a graph
realization, not an MA2-leaf completion certificate, and not a counterexample
candidate.  What it proves is the obstruction to deriving the proposed finite
localization lemma from the current inputs: the full displayed rooted data and
all of its cycles impose no such bound.

## 7. Simultaneous port relations

Let two `P` paths be `r-u-s` and `r'-u'-s'`.

1. **Same attachment pair, distinct ports:** if `{r,s}={r',s'}` and
   `u!=u'`, the two length-two paths form the simple cycle
   `r-u-s-u'-r` of length 4.  **CONTRADICTION.**
2. **Same pair, same port:** these are one literal path, not two independent
   templates.
3. **Same port, one shared attachment:** `u` sees three distinct theta
   attachments and at least one incidence into its leaf remainder, so
   `d(u)>=4`.  M1 then makes all its neighbours cubic.
4. **Same port, disjoint attachment pairs:** the corresponding bound is
   `d(u)>=5`, again with cubic neighbours.
5. **Distinct ports, one shared attachment:** there is no automatic cycle;
   the two port paths meet only at that attachment.
6. **Crossing, nesting, or different E2 bundles:** these are order labels on
   the attachment coordinates.  They add cycles only through their actual
   theta/four-color routes and cannot be selected independently.

The infinite family in Section 6 is the clean “different bundles, distinct
ports” case and retains both ports simultaneously.  Hence `(P,P)` has status

\[
 \boxed{\text{EXPLICIT INFINITE PORT RESIDUAL}}.
\]

## 8. The `(A,P)` cell

Let A supply two bridge paths of lengths `ell,ell+delta`,
`delta in {1,2}`, between attachments `alpha,beta`; let P supply `r-u-s`.
The complete unconditional information remains:

- for every theta `alpha`--`beta` route `d`, A gives cycles
  `ell+d,ell+delta+d`;
- for every port-compatible `r`--`s` route `e`, P gives `2+e`;
- if the terminal pairs literally coincide and the A paths are internally
  disjoint from the P path, the two additional direct cycles have lengths
  `ell+2,ell+delta+2`.

No further “Type-B cross sum” is automatic.  Such a sum is genuine only when
the two paths lie in different bridges of the **same** 2-cut.  The A-side
Type-B reduction has its own cut (for example `{x,z_0}`), while a P pair on
the other theta has unpinned attachments.  Until those terminals are proved
to coincide with the cut, importing a cross-cut sum would be invalid.

If an A path and the P path overlap, their cells and common components must
be retained; neither `ell+2` formula is then automatically a simple cycle.
The translated one-port subfamily of Section 6 already leaves unbounded
rooted port distances before this A data is attached.  No theorem converts
that P path to A or pins its terminals relative to the A cut.  Thus `(A,P)`
and `(P,A)` retain status

\[
 \boxed{\text{EXPLICIT INFINITE PORT RESIDUAL}},
\]

with the explicit caveat that this report does not construct a full graph
simultaneously realizing a selected A outcome and the family.

## 9. Later reconvergences and `Q`

The route tables in Section 3 are complete in the triangle-plus-relevant-
theta subgraph.  Section 6 goes further and enumerates every route/cycle in
one full E2 four-color incidence.  For an arbitrary later reconvergence,
however, the new port-compatible routes depend on the ordered common
components and divergent cells actually met between `r,s`.  There is no
formula depending only on the words “after a reconvergence.”

`Q` supplies no additional condition until its actual attachment pair is
fixed.  It is not introduced as a freely placeable fifth color here.  If a
future argument locates `Q` so that it gives another port-compatible
`r`--`s` route, that route must be added to the exact list and tested against
`2^m-2`.

## 10. Degree five and computation scope

The task authorized degree five only if degree-four P outcomes were
eliminated or finitely normalized.  They are neither: Section 6 gives an
explicit infinite degree-four residual.  Therefore no degree-five or
degree-at-least-six analysis is started.

No SAT model is built.  There is no complete finite rooted port-core list to
encode, and bounding `a,c,Y` would silently discard the proved scalable
family.

## 11. Reduction achieved

1. All degree-four P attachment locations reduce to eight exact theta types,
   with common-prefix/divergence/reconvergence labels recorded as additional
   four-color incidence.
2. The complete local port-compatible route formulas include the triangle
   detour for generic ports and exclude it precisely when the port is `y`.
3. Cubic saturation eliminates immediate-split first neighbours as
   attachments and excludes the port itself from the relevant prefixes, but
   does not control later prefix degrees.
4. The proposed lexicographic port normalization has no replacement theorem
   behind it; an explicit scalable E2-parallel family refutes its derivation
   from the current local/core arithmetic.
5. A narrow `(P,P)` subcase—same attachment pair, different ports—is
   eliminated by a `C_4`; the general `(P,P)` and `(A,P)` cells remain
   explicit infinite port residuals.
6. The exact next dependency is a global completion or replacement theorem
   for the selected MA2 leaf, not more first-edge arithmetic.

This is a genuine negative normalization result and a sharper description of
the shared-port branch.  It does not eliminate Type T.
