# Type-T common-pole branch allocation

**Status (2026-07-28): REDUCTION.**  Pole forcing leaves one live T2
geometry.  This file proves the exact first-edge theorem there, classifies all
rooted first-edge allocations, relates them to `deg(z_0)`, and identifies the
precise point where a finite state list stops.  It is a hand proof with a
symbolic verifier, not proof-assistant formal verification and not a graph
census.

## 1. Surviving geometry and branch data

Work throughout with

\[
 T=\{x,y,z_0\},\qquad d(x)=d(y)=3,\qquad d(z_0)\ge4,
 \qquad X_x=X_y=z_0.
\]

Write `x'` and `y'` for the external neighbours of `x` and `y`.  Lemma NE
in `central_bridge_triangle.md` gives

\[
 x'\ne y'.
\]

The two canonical thetas have poles `z_0,x'` and `z_0,y'`.  Orient their
non-`P_0` branches away from `z_0` and put

\[
 A=P_1^x,\quad B=P_2^x,\quad C=P_1^y,\quad D=P_2^y,
\]

with

\[
 |A|=2^{\rho_x}-1,\quad |B|=2^{s_x},\quad
 |C|=2^{\rho_y}-1,\quad |D|=2^{s_y},
 \qquad \rho_x,s_x,\rho_y,s_y\ge2.
\]

Within a canonical theta the branches meet only at their two poles.  Thus
`A,B` have distinct first edges at `z_0`, as do `C,D`.

## 2. First-edge theorem [PROVED]

**Theorem 2.1.**  *All four of `A,B,C,D` leave `z_0` through nontriangle
edges.  Moreover*

\[
 \operatorname{first}(A)\ne\operatorname{first}(B),\qquad
 \operatorname{first}(C)\ne\operatorname{first}(D).
\]

**Proof.**  The `P_0^x` branch is `z_0-x-x'`.  Theta branch-disjointness
therefore prevents both `A` and `B` from using `z_0x`.

The outside-arc definition of `B=P_2^x` makes its interior avoid `N[x]`.
In particular it avoids `y`, so it cannot use `z_0y`.

Suppose instead that `A=P_1^x` begins `z_0-y`.  Removing this first edge
leaves a simple `y`--`x'` subpath of `A` of length

\[
 (2^{\rho_x}-1)-1=2^{\rho_x}-2.
\]

The branch `A` avoids the internal vertex `x` of `P_0^x`.  Hence that
subpath, together with `x'x` and `xy`, is a simple cycle of length

\[
 (2^{\rho_x}-2)+1+1=2^{\rho_x},
\]

contrary to the defining power-cycle-free hypothesis.  Thus `A` uses neither
triangle edge at `z_0`.  The symmetric argument applies to `C,D`: `D` avoids
`x` by the outside-arc mechanism, and `C` beginning `z_0-x` would close a
simple `2^{\rho_y}`-cycle through `y'y` and `yx`.

Finally, if `A,B` had the same first edge, they would share its non-pole
endpoint, contradicting theta branch-disjointness.  The same proves the
claim for `C,D`.  `square`

This proof uses the actual first edge only.  It does not assert that `A`
never meets `y` later, that `C` never meets `x` later, or that two branches
with different first edges never reconverge.

## 3. The six rooted allocation states [PROVED]

Equality of first edges partitions `{A,B,C,D}`.  A block cannot contain
`A,B` or `C,D`.  Consequently every block has size at most two and the only
possible equality pairs are

\[
 AC,\quad AD,\quad BC,\quad BD.
\]

There are seven labelled partitions.  Under the only role-preserving local
symmetry, `x<->y`, acting as `(A C)(B D)`, they form six orbits:

| state | first-edge blocks | number of nontriangle first edges | forced common prefixes |
|---|---|---:|---|
| `E2_parallel` | `AC | BD` | 2 | `A,C` and `B,D` |
| `E2_cross` | `AD | BC` | 2 | `A,D` and `B,C` |
| `E3_near` | `AC | B | D` | 3 | `A,C` |
| `E3_power` | `BD | A | C` | 3 | `B,D` |
| `E3_mixed` | `AD | B | C` | 3 | `A,D`; its mirror has `B,C` |
| `E4_discrete` | `A | B | C | D` | 4 | none |

The near-power and power branches are not interchangeable: their lengths
and canonical origins differ.  Thus no additional `A<->B` or `C<->D`
quotient is licensed.

For every equality pair `UV`, let `I_{UV}` be its maximal common initial
edge segment from `z_0`, let

\[
 h_{UV}=|I_{UV}|\ge1,
\]

and mark its last vertex `w_{UV}`.  At `w_{UV}` the two paths either take
different next edges or one path terminates there.  The latter boundary case
is possible because `x'!=y'` only says that both paths cannot terminate
together.  In particular, equality of first edges has **not** been replaced
by equality of whole branches.

## 4. Degree of the common pole [PROVED]

The two triangle edges `z_0x,z_0y` are already present.  If an allocation
uses `r` distinct nontriangle first edges, then

\[
 r\le d(z_0)-2.
\]

Therefore:

| degree | possible allocation orbits |
|---|---|
| `d(z_0)=4` | exactly `E2_parallel`, `E2_cross` |
| `d(z_0)=5` | all `E2` and `E3` states; an `E2` state leaves one nontriangle edge unused by the four branches |
| `d(z_0)>=6` | all six states; lower-edge states may leave further edges unused |

Thus degree 5 does not force three first edges, and degree at least 6 does
not force four.  The allocation records branch use, not every edge incident
with `z_0`.

By M1, vertices of degree at least four form an independent set.  Since
`z_0` is such a vertex, **every neighbour of `z_0` is cubic**.  In particular
all nontriangle first neighbours are cubic.  If a shared pair splits
immediately after its first edge, that neighbour has exactly the three used
incidences: the edge to `z_0` and the two outgoing branch edges.  A singleton
first neighbour uses two incidences in the rooted core and has exactly one
ambient cubic edge not recorded there.  If a shared prefix continues, its
first neighbour uses the two prefix incidences and likewise has one ambient
incidence not determined by the prefix data.

These facts do not make a first edge a separator of `G`: the other branch
groups and unrecorded ambient edges can bypass it.

## 5. Exact prefix-only cycle census

First consider the **genuine-split prefix-only rooted core**: equality pairs
share exactly their displayed initial prefixes, both branches continue after
the marked split vertex, and after those prefixes all branch interiors are
disjoint from the other theta's branches and from the connector

\[
 K=x'-x-y-y',\qquad |K|=3.
\]

Put `h_{UV}=0` when `U,V` have different first edges.  The six cycles made
from a branch pair (and `K` for a cross pair) are exactly:

| branches | exact length |
|---|---:|
| `A,B` | `2^{rho_x}+2^{s_x}-1` |
| `C,D` | `2^{rho_y}+2^{s_y}-1` |
| `A,C` plus `K` | `2^{rho_x}+2^{rho_y}+1-2h_AC` |
| `A,D` plus `K` | `2^{rho_x}+2^{s_y}+2-2h_AD` |
| `B,C` plus `K` | `2^{s_x}+2^{rho_y}+2-2h_BC` |
| `B,D` plus `K` | `2^{s_x}+2^{s_y}+3-2h_BD` |

There is one essential simultaneous correction to that pair table.  Every
`E2` or `E3` core also has a seventh simple cycle using all four branch
colors and no connector.  If `\mathcal P` is the set of forced equality
pairs in the state, its exact length is

\[
 L_4=|A|+|B|+|C|+|D|-2\sum_{UV\in\mathcal P}h_{UV}
 =2^{\rho_x}+2^{s_x}+2^{\rho_y}+2^{s_y}-2
  -2\sum_{UV\in\mathcal P}h_{UV}.
\]

The discrete `E4` core has no such four-color cycle: all four branches meet
only at `z_0`, so a cycle not using `K` must use the same terminal pair and
is one of the two same-theta cycles already listed.  Thus the complete
prefix-only census has seven simple cycles in every `E2`/`E3` state and six
in `E4`.

The first two are odd.  The `AC` and `BD` lengths are also odd, for every
allowed prefix length.  If `h_AD=h_BC=0`, each mixed-role length is `2 mod
4`, and hence is not a power of two.  A positive mixed-role prefix is
different: for example

\[
 \rho_x=s_y=2,\quad h_{AD}=1
 \quad\Longrightarrow\quad |\text{outer cycle}|=4+4+2-2=8,
\]

whereas the same exponents with `h_{AD}=2` give length 6.  Precisely, the
mixed outer cycle is dyadic only when

\[
 h_{AD}=2^{\rho_x-1}+2^{s_y-1}+1-2^{k-1}
\]

for an integer `k` and a geometrically valid prefix; the `BC` equation is
the symmetric one.

The four-color length can be dyadic in every shared-prefix state.  For
example, with all four exponents equal to 2, `E2_parallel` and prefix lengths
`h_AC=1,h_BD=2` give `L_4=8`.  For `E3_near`, exponents
`(rho_x,s_x,rho_y,s_y)=(2,2,2,3)` and `h_AC=1` give `L_4=16`.
The verifier finds analogous examples for `E2_cross`, `E3_power`, and
`E3_mixed`.  It also finds fully non-dyadic prefix-only instances for every
one of those states.  Consequently:

- `E2_cross` and `E3_mixed` can expose a dyadic mixed-role pair cycle;
- every `E2`/`E3` state can expose a dyadic four-color cycle;
- neither failure is forced by the allocation state; and
- `E4_discrete` is the only state whose entire prefix-only core is
  unconditionally non-dyadic, but later reconvergences remain unclassified.

Hence **no allocation orbit is eliminated by first-edge and prefix
arithmetic alone.**

For completeness, the following simultaneous assignments witness the
classification.  The exponent tuple is `(rho_x,s_x,rho_y,s_y)`; “safe” here
means all six or seven cycles of this prefix-only core are non-dyadic.

| state | failing prefix-only instance | safe prefix-only instance |
|---|---|---|
| `E2_parallel` | `(2,2,2,2)`, `(h_AC,h_BD)=(1,2)`: `L_4=8` | `(2,2,2,2)`, `(1,1)` |
| `E2_cross` | `(2,2,2,2)`, `(h_AD,h_BC)=(1,1)`: both mixed cycles have length 8 | `(2,2,2,2)`, `(2,2)` |
| `E3_near` | `(2,2,2,3)`, `h_AC=1`: `L_4=16` | `(2,2,2,2)`, `h_AC=1` |
| `E3_power` | `(2,2,2,2)`, `h_BD=3`: `L_4=8` | `(2,2,2,2)`, `h_BD=1` |
| `E3_mixed` | `(2,2,2,2)`, `h_AD=1`: the mixed cycle has length 8 | `(2,2,2,2)`, `h_AD=2` |
| `E4_discrete` | none: its six formulas are always safe | `(2,2,2,2)` |

The verifier exhaustively derives the partitions, checks the four pair
formulas over all exponents from 2 through 10 and every positive
genuine-split prefix length, enumerates all six or seven simple cycles of
each suppressed prefix-only core, and tests simultaneous core instances
through exponent 6.  The parity statements above are proofs for all
exponents; the finite sweeps are mechanical cross-checks and sources of
explicit failing/safe examples.

## 6. What happens after the first divergence

The prefix-only census is not the general intersection census.  It also
deliberately excludes the marked boundary case from Section 3 in which one
branch terminates at the end of the common prefix: then that endpoint lies on
the other branch, the connector meets the branch union there, and the seven-
edge suppressed core is no longer the right topology.  That case is retained
as terminal-incidence data, not forced into a false positive-length suffix.

Fix any
cross pair `U,V`.  Whenever the two paths diverge at `p` and next reconverge
at `q`, with internally disjoint `p`--`q` arcs of lengths `a_i,b_i`, those
arcs form the exact simple cell cycle

\[
 a_i+b_i.
\]

It is contradictory exactly when `a_i+b_i` is a power of two.  Repeated
reconvergences give repeated cells.  Shared edge components cancel from the
symmetric difference.  If the common vertices occur in different orders on
the two paths, even the choice of a noncrossing cell decomposition is extra
incidence data.

The connector `K` closes the remaining `x'`--`y'` symmetric-difference trail
only when that trail and `K` are internally disjoint.  In the prefix-only
case this is exactly the table in Section 5.  In general its length depends
on **all** common components and cells, not only `h_{UV}`.  Moreover `A` may
meet `y` later and `C` may meet `x` later, so connector-disjointness is not
automatic for pairs involving them.  The outside branches `B,D` avoid both
triangle centres, but they may still meet cross endpoints or other branch
segments.

All four colors must be retained simultaneously.  Later intersections can
create cycles using arcs from three or four colors that are not determined
by any independently chosen pairwise decomposition.  Thus a full residual
state must mark terminals, every maximal common colored segment, every
divergence/convergence, color changes, orientations, and positive segment
lengths.  The six allocation orbits are finite **roots** for that incidence
object; they are not six finite graph cores.

### 6.1 Splicing, separators, and replacement

A divergent cell permits an equal-length tail swap only if it preserves all
of: path length, simplicity, disjointness from the same-theta mate, and the
canonical witness definition.  A common prefix by itself supplies none of
those four conditions and yields no shorter canonical witness—deleting it
would move the theta pole from `z_0`.

Nor does a maximal prefix force a separator or a replaceable rooted segment
of `G`.  T9B can replace a complete Type-B bridge only under closure
2-connectivity, internal minimum degree, internal cleanliness, and spectrum
inclusion.  It does not authorize deleting or rerouting one colored prefix.

## 7. Other structural inputs and their exact effect

### 7.1 Ordering defect and local excess

The contribution of `z_0` to degree excess is exactly

\[
 d(z_0)-3.
\]

Globally,

\[
 \sum_v(d(v)-3)=n-4-2q(G),
 \qquad q(G)=2n-2-m\ge4.
\]

Hence `d(z_0)-3` is one nonnegative summand, but no theorem in the current
dependency chain bounds that summand sharply enough to exclude degree 4, 5,
or at least 6.  Unused nontriangle incidences at `z_0` meet cubic vertices,
so edge deletion is not licensed merely by excess bookkeeping.

### 7.2 The `(A,A)` exponent inequality and T9B

Only after both MA2 outcomes are `A` does the established common-terminal
Type-B reduction apply.  In that cell the cross-cut cycle argument forces

\[
 \rho_x\ne\rho_y.
\]

This condition does not remove any of the six first-edge states.  It enriches
the paired Type-B spectra downstream.  T9B then gives paired replacement and
deletion criticality under its exact hypotheses; as noted above, it does not
collapse the four-color incidence core or license a local prefix splice.

### 7.3 `Q`

The triangle-contraction witness `Q` belongs to a chosen contracted power
cycle and an attachment pair in `T`.  Existing results do not pin its outside
arc to a first neighbour, shared prefix, or later cell of `A,B,C,D`.
Therefore `Q` eliminates no allocation state.  If a later argument locates
its attachment pair or makes it meet the incidence core, it must be added as
another rooted path with its actual endpoints; it is not an independent
fifth color that can be positioned arbitrarily.

### 7.4 S5

An `S` outcome gives the exact S5 cut vertex and equal-lobe structure.  In an
`(S,S)` cell, uniqueness gives the same cut vertex and, in the generic case
where it is not in `T`, the same attachment-free lobe.  A mixed `S` cell
places the other central bridge in the theta lobe unless it enters the S5
lobe through the cut vertex.  The detour's spectrum remains open.  None of
this changes the canonical first edges at `z_0`; the degenerate S5 case with
its cut vertex in `T` also remains open.

## 8. Rebuilt live `(A,P,S) x (A,P,S)` matrix

The following matrix contains only the live common-pole geometry.  Each cell
has exactly one of the requested statuses.

| `tau_x \ tau_y` | `A` | `P` | `S` |
|---|---|---|---|
| **`A`** | **REDUCED TO ENRICHED TYPE-B.** Two coupled Type-B cuts, `rho_x!=rho_y`; allocation/tail incidence remains part of their joint realization problem. | **ONE EXPLICIT OPEN RESIDUAL.** A symbolic A pair and a shared P port must be located in one four-color tail core; no theorem pins the port relative to a prefix or `Q`. | **REDUCED TO AN S5 LOBE.** Generic non-detouring A stays in the theta lobe; an A route entering the attachment-free lobe has the explicit unresolved lobe-spectrum term. |
| **`P`** | **ONE EXPLICIT OPEN RESIDUAL.** Symmetric A/P residual. | **ONE EXPLICIT OPEN RESIDUAL.** Two shared ports plus the common-pole incidence core and `Q`; their coincidences and ordered intersections are unpinned. | **REDUCED TO AN S5 LOBE.** The P bridge stays in the theta lobe unless a port route detours through the S5 cut vertex into the other lobe. |
| **`S`** | **REDUCED TO AN S5 LOBE.** Symmetric mixed-S residual. | **REDUCED TO AN S5 LOBE.** Symmetric mixed-S residual. | **REDUCED TO AN S5 LOBE.** S5 uniqueness gives one cut vertex and, generically, one literal attachment-free lobe; the cut-vertex-in-`T` degeneration remains open. |

No cell is a contradiction, and no cell has become a finite full graph core.
The finite result upstream is the six-state first-edge root classification.

One completely explicit surviving residual, sufficient to show the stopping
point, is

\[
 (\tau_x,\tau_y)=(P,P),\quad E2_{\rm cross},\quad
 h_{AD},h_{BC}\ge1,
\]

with both shared ports, all later common colored components, and `Q`'s actual
attachment pair retained as rooted data.  Its prefix arithmetic can be
simultaneously safe: `(rho_x,s_x,rho_y,s_y)=(2,2,3,3)` and
`h_AD=h_BC=1` give both mixed outer cycles length 12 and the four-color cycle
length 18.  The later cell lengths and port incidences are nevertheless not
determined.  This is an explicit open residual specification, not a claimed
counterexample or graph realization.

## 9. Why no SAT or direct graph generator is built

An exact finite **first-edge** state list survives, but an exact finite
common-pole graph core does not.  The number and order of post-prefix
four-color intersections are unbounded by the cited theorems.  A generator
over two independently created thetas would silently assume away precisely
that residual, while a bounded incidence generator would have no proved
completeness bound.  The requested symbolic state verifier is therefore the
correct mechanical artifact at this stage; no SAT claim is made.

## 10. Reduction achieved

1. Every live Type-T instance has the common pole `z_0` and one of exactly
   six rooted first-edge allocation orbits.
2. Degree 4, degree 5, and degree at least 6 reduce to exact subsets of those
   orbits; none is eliminated.
3. Equality of first edges is represented by maximal common prefixes, never
   by whole-branch equality.
4. Prefix-only cores have exact pair-cycle and four-color-cycle formulas.
   Shared-state dyadic hits are conditional rather than forced; the discrete
   core is prefix-only safe.
5. The remaining obstruction is the rooted four-color post-prefix incidence
   core, enriched downstream by A/P/S data and `Q` only when their locations
   are actually known.

This is a genuine structural reduction, but not an elimination of Type T.
