# Exact-two-attachment Type-T A spectrum

**Status.** Hand-written structural and arithmetic audit, independently
cross-checked by finite symbolic calculation and explicit NetworkX fixtures.
This is not proof-assistant formal verification. No literature-novelty claim is
made.

## 1. The topology must be split before doing arithmetic

There are two different A configurations in the committed files.

### 1.1 Generic pole-to-pole A

In `contraction_leaf_blocks.md` VI.1 Case 3, a theta bridge `K` attaches at
the two theta poles `p,q`. Its interior is disjoint from the theta. The theta
supplies routes of lengths

\[
1\quad(\text{if }pq\in E(G)),\qquad 2,\qquad
M=2^\rho-1,\qquad N=2^s.
\]

T2 supplies paths in `K` of lengths `ell,ell+delta`, with
`delta in {1,2}`. Here the continuation prompt's proposed disjointness is
correct: a `K`-internal path and a theta route meet only at `p,q`, so each
union is a simple cycle. The guaranteed lengths are

| outside route | first cycle | second cycle |
|---|---:|---:|
| pole edge, if present | `ell+1` | `ell+delta+1` |
| `P_0` | `ell+2` | `ell+delta+2` |
| near-power branch | `ell+2^rho-1` | `ell+delta+2^rho-1` |
| power branch | `ell+2^s` | `ell+delta+2^s` |

This is exactly the already-valid generic A table. It is **not** the residual
triangle-anchored configuration.

### 1.2 Actual triangle-anchored exact-two A

Use the committed notation of `central_bridge_triangle.md` IV. Let the cubic
triangle vertex be `x`, let `X=X_x` be the selected mate/pole, and let `Y=Y_x`
be the other mate. The central bridge is `K=B_x`, with

\[
\operatorname{att}(K)=\{x,X\},\qquad
xY,YX\in E(K),\qquad xX\notin E(K).
\]

The known path

\[
R_0=x-Y-X
\]

has length `2` **inside `K`**, not outside it. Since `x` is cubic and its
other two edges are `xX` and `xx'`, `xY` is its unique `K`-edge. Therefore
every `x`-`X` path in `K`, including both T2 paths, begins with `xY`.
Consequently

\[
\operatorname{int}(R_0)\cap\operatorname{int}(P_i)=\{Y\},
\qquad E(R_0)\cap E(P_i)=\{xY\}.
\]

The prompt's requested claim that the length-two path has interior disjoint
from `P_1,P_2` is false in the actual residual geometry. Thus `R_0 union P_i`
is not a simple cycle and `ell+2,ell+delta+2` are not guaranteed here.

## 2. Correct dependency audit

| committed statement | classification after removing false anchoring |
|---|---|
| T1/T2 for an exact two-attachment central bridge (`contraction_separator_integration.md` VI--VII) | **Still valid.** T2 supplies some pair `ell,ell+delta`; it says nothing about the shortest path. |
| Generic A route census (`contraction_leaf_blocks.md` VI; `central_bridge_templates.md`) | **Still valid without anchoring.** Every theta route is outside the bridge and closes each admissible path simply. |
| Triangle gateway and isolated shortest path (`central_bridge_triangle.md` IV.1--IV.2) | **Still valid.** `K` contains `x-Y-X`, and every `K`-path starts with `xY`. |
| `ell=2`, `ell' in {3,4}` | **Withdrawn.** The length-two path need not be in T2's pair. |
| Conditional exclusion of length `3` and `4` bridge paths | **Still valid, strengthened below.** Every non-short bridge path of length `L` yields cycles of lengths `L` and `L+1`. |
| Terminal-pair exhaustion (`central_bridge_triangle_final.md` X.0) | **Still valid.** It concerns the terminal sets, not the path lengths. |
| P and S templates | **Unaffected.** No P/S statement is modified here. |
| Historical pinned A/A and A/P arithmetic (`central_bridge_triangle_s5.md`, `central_bridge_triangle_final.md`) | **Withdrawn.** It may not be reused with `ell=2`; the symbolic A table remains available. |
| T3 three-way choice consistency | **Valid after wording correction.** The isolated length-two gateway path is fixed by each `X_x` choice, but is not an admissible-path label. |
| T8/T8R/T8P applied directly to this `K` | **Conditional/not inherited.** Those results assume a separately minimal, self-sum-clean Type-A copy gadget. The present cut is globally Type B (two nontrivial bridges plus the edge `xX`), and self-sum cleanliness of `K` is not inherited. |

## 3. Full guaranteed cycle spectrum in the actual anchored case

Let T2 give simple paths

\[
P_1,P_2\subseteq K,\qquad |P_1|=\ell,\quad
|P_2|=\ell+\delta,\quad\delta\in\{1,2\}.
\]

The earlier C4 audit excludes bridge-path lengths `3,4`; neither T2 path can
be the unique length-two path, so `ell>=5`.

### 3.1 Two closures of every individual bridge path

For any simple `x`-`X` path `P` in `K` of length `L>2`, write
`P=xY+P[Y,X]`. Since `P` is simple, `P[Y,X]` is a simple path of length
`L-1`. It cannot use the edge `YX`: a simple path starting at `Y` that uses
`YX` must terminate at `X` immediately, which would give `L=2`. Hence:

- `P[Y,X] union YX` is a simple cycle of length `L` inside `K`;
- `P union xX` is a simple cycle of length `L+1`, using the separate trivial
  bridge `xX`.

This proves four guaranteed lengths before using the rest of the theta:

\[
\ell,\quad\ell+1,\quad\ell+\delta,\quad\ell+\delta+1.
\]

It also subsumes the previous short-detour checks: `L=3` makes `L+1=4`,
while `L=4` makes `L=4`.

### 3.2 The other nontrivial bridge at the same cut

The remainder of `Theta_x` through `x'` is a different
`x`-`X` bridge. Its two simple route lengths are

\[
D_1=1+(2^{\rho_x}-1)=2^{\rho_x},\qquad
D_2=1+2^{s_x}=2^{s_x}+1.
\]

Distinct 2-cut bridges share only `x,X`, so the global bridge-spectrum
identity proves all four unions below are simple cycles. Including the two
individual closures gives the exact guaranteed table:

| source | using `P_1` | using `P_2` |
|---|---:|---:|
| suffix plus `YX` | `ell` | `ell+delta` |
| full path plus `xX` | `ell+1` | `ell+delta+1` |
| other bridge, near-power route | `ell+2^rho` | `ell+delta+2^rho` |
| other bridge, power route | `ell+2^s+1` | `ell+delta+2^s+1` |

The isolated path `R_0` separately produces lengths

\[
3,\qquad 2^\rho+2,\qquad 2^s+3,
\]

all automatically nonpowers for `rho,s>=2`. No path-union between `P_1`
and `P_2` is included in the table: their mutual internal disjointness is not
known.

## 4. Complete arithmetic classification of the guaranteed table

Put

\[
\mathcal D=\{0,1,2^\rho,2^s+1\}.
\]

The actual anchored table is F-clean exactly when

\[
\ell+d\ne2^k,\qquad \ell+\delta+d\ne2^k
\quad(d\in\mathcal D,k\ge2).
\]

Equivalently, the complete forbidden set is

\[
\ell\in
\{2^k-d,\;2^k-d-\delta:
k\ge2,\ d\in\mathcal D\}.
\]

This is an explicit infinite complement, not a contradiction or a finite list
of `ell` values. A uniform infinite surviving family for both offsets is

\[
\boxed{\ell=2^t+1,\qquad t>\max\{\rho,s,3\}.}
\]

Proof by parity and 2-adic valuation:

- the local values are `2^t+q`, `1<=q<=4`, strictly between consecutive
  powers for `t>=4`;
- adding `2^rho` gives an odd number for odd residual offsets, or a number
  of 2-adic valuation `1` with odd quotient greater than `1` for residual
  offset `2`;
- adding `2^s+1` gives residual offsets `2,3,4`; offsets `2,3` are handled
  as above, and offset `4` has valuation `2` when `s>2`, while for `s=2`
  it is the sum of the distinct powers `2^t+2^3`.

Thus every guaranteed length is non-dyadic for infinitely many parameter
tuples. `verifier/type_t_exact_two_a.py` exhaustively agrees with the forbidden
formula for `delta=1,2`, `2<=rho,s<=7`, and `5<=ell<=512`.

The pair's three self-sums are non-dyadic on the same family:
`2ell=2^{t+1}+2`, `2ell+delta`, and `2ell+2delta` lie strictly off a power
(with the middle value odd when `delta=1`). Thus even self-sum cleanliness is
arithmetically compatible. T3/T5 may consequently impose signature
balance/maximality, but do not contradict this length family.

For comparison, the generic pole-to-pole model of section 1.1 also has an
explicit infinite safe family:

\[
\ell=2^t,\qquad t>\max\{\rho,s,2\}.
\]

Therefore neither topology is eliminated by the guaranteed cycle arithmetic.

## 5. The Heawood regression under every requested hypothesis

For the subdivided-Heawood bridge in `type_t_recovery_audit.md`, use terminals
`x,X=0`, subdivision vertex `Y`, and spectrum
`{2,7,9,11,13,15}`.

| hypothesis | status | exact reason |
|---|---|---|
| internal minimum degree | **passes** | every nonterminal has degree `3` |
| `K+xX` 2-connected | **passes** | recomputed by NetworkX |
| internal power-cycle cleanliness | **fails** | `K` contains a `C8` |
| all theta cross-cycle conditions | **fails already at the trivial edge** | terminal paths `7,15` plus `xX` give `C8,C16` |
| terminal degrees in `K` | **passes local Type-B profile** | `(d_K(x),d_K(X))=(1,3)`; the other bridge and edge can complete `x` to degree `3` |
| T8 | **not applicable** | no self-sum-clean, lex-minimal Type-A gadget was selected |
| T8R/T8P | **not applicable** | they inherit T8's scope |
| T3 | **does not eliminate it as a local fixture** | its self-sum already hits `4` and `16`, the conclusion T3 would force in a smaller-copy case |
| T5 | **does not eliminate it as a local fixture** | T5 is a conditional signature comparison and likewise concludes self-sum dirtiness, already present |
| exact Type-T gateway geometry | **passes locally** | `xY,YX` give the required bridge and `xX` can be the separate triangle edge |
| simplicity after reconstruction | **passes locally** | outside theta paths can use fresh internal vertices |
| full minimal-counterexample realization | **fails** | the internal `C8` and trivial-edge cross cycles are forbidden |

So the Heawood fixture is not a rooted obstruction under the full hypotheses.
It refutes only the invalid theorem inference.

## 6. Strong anchoring substitutes, in the requested order

1. **One T2 path may be chosen shortest: false under T2's hypotheses.** The
   Heawood spectrum already refutes it. The stronger Balaban fixture below is
   also C4/C8-free and has shortest path `2` but admissible pair `11,13`.
2. **Full F-clean hypotheses force a pair beginning at `2`: not proved or
   refuted.** Every current explicit local counterexample fails a higher
   power-cycle condition. None licenses the claimed anchoring in a minimal
   counterexample.
3. **The smallest admissible pair has a universal bound: no bound follows from
   the current workspace lemmas.** The Balaban fixture raises its first term to
   `11` under T1/T2 plus C4/C8-freeness. A bound under full F-cleanness remains
   open.
4. **If `ell>=5`, then `K` contains C4 or C8: false under the local theorem
   hypotheses, even with C4/C8-freeness imposed.** Subdivide edge `0-1` of the
   cubic Balaban 10-cage, attach `x` at the subdivision vertex, and root at
   `X=0`. The resulting bridge has girth `10`, `K+xX` is 2-connected, every
   internal vertex has degree `3`, and paths through length `14` have lengths
   `{2,11,13}`. Thus `11,13` is an admissible pair and there is no C4/C8.
   The fixture contains a C16, so it is not fully F-clean.
5. **A smaller spectrum-safe replacement for every `ell>=5`: unproved.** A
   replacement must preserve terminal/global degrees, exact gateway geometry,
   internal F-cleanness, and spectrum inclusion against both outside bridges.
   No committed lemma constructs such a replacement.
6. **A minimal obstruction has a deletable real SPQR edge contradicting T8:
   false as an inference.** T8 is a criticality conclusion, not a deletability
   theorem, and its self-sum-clean Type-A hypotheses are not inherited here.
   R1/R2 show that deleting real R/P edges preserves closure 2-connectivity;
   T8R/T8P then allow the edge to remain critical through an incident cubic
   vertex. They do not guarantee any noncritical real edge.

The Balaban LCF data are embedded in the verifier and its order, size,
cubicity, girth, closure connectivity, short rooted spectrum, and C16 failure
are recomputed rather than trusted as metadata.

## 7. Overlap of the two admissible paths

Cancel their common edges and split at consecutive divergence/reconvergence
vertices whenever the common vertices occur in compatible order. For cell
`i`, let the two arc lengths be `a_i,b_i` and orient the sign so that

\[
\sum_i(b_i-a_i)=\delta.
\]

Each cell gives a simple cycle of length `a_i+b_i`, but the small total signed
difference does not make an individual difference small: large positive and
negative differences can cancel.

Two exact incidence counterexamples are:

| `delta` | cell arc pairs | signed differences | cell cycle lengths |
|---:|---|---|---|
| 1 | `(2,5),(4,2)` | `3,-2` | `7,6` |
| 2 | `(1,5),(4,2)` | `4,-2` | `6,6` |

Neither forces C4/C8. These are path-incidence counterexamples only—their
internal vertices have degree two—so they do not settle whether degree-three
saturation plus full F-cleanness eliminates every such overlap. They do prove
that `delta in {1,2}` alone cannot support a one-cell assumption or a
short-cell conclusion.

If there is exactly one cell, its length is `2a+delta`: it is odd for
`delta=1`, while for `delta=2` it is a power of two exactly when
`a=2^j-1`. Multiple cells permit cancellation and require new structural
control. Closing a cell through the isolated path `R_0` is not automatic,
because `R_0` shares `xY` and its internal vertex `Y` with both full paths.

## 8. Minimal rooted obstruction and SPQR scope

The subsequent whole-pair audit `type_b_compatibility.md` replaces this
conditional sketch with T9B. Retaining the other Type-B bridge and `xX`, any
smaller internally clean rooted graph whose closure is 2-connected and whose
terminal spectrum is contained in `Lambda(K)` would create a smaller
counterexample. Exact terminal degree equality and preservation of the
triangle gateway are unnecessary for that contradiction: the retained bridge
and edge already contribute two at each terminal.

For edge deletion, T9B says that an internal degree constraint fails or the
closure loses 2-connectivity. R1/R2 remove the latter alternative for real
R/P edges, so every such edge meets an internal cubic vertex. This is stronger
and more accurately scoped than importing T8R/T8P's Type-A terminal list.
It still does not give a finite SPQR family: internal cubic vertices can cover
arbitrarily many real edges, and the self-sum-dependent Type-A rigid-leaf
dichotomy is not inherited. No bound on the number or arrangement of R-nodes
or universal spectrum-safe replacement is proved.

## 9. Result

The exact-two-attachment A configuration is not eliminated. The correct
anchored spectrum is fully explicit, and its arithmetic has an infinite safe
family. The Heawood and Balaban fixtures show that T1/T2, local degree,
closure connectivity, and even C4/C8-freeness do not anchor the admissible
pair. Every explicit fixture fails a stronger full-F condition, so no rooted
counterexample to the entire minimal-counterexample package is claimed.

**Stopping condition: proof that the present minimal-counterexample hypotheses do not control the admissible pair enough.**
