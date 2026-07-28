# Type-T joint bridge universalization: the two-central-bridge interaction

**Status (historical; identical-terminal row structurally superseded).** Hand-written dependency audit plus one new proved lemma
(the cross-exponent obstruction, Part 3). Everything else in this file
either cites an existing proved result exactly, or reports an existing
open item exactly as it stands. Nothing here is proof-assistant formal
verification. **Type T is NOT eliminated by this file.** No row of the
joint outcome matrix (Part 4) is fully closed; this is stated
explicitly rather than rounded up.

**Later dependency correction.**  Ancestor commit `7a3c1f7`
(`central_bridge_triangle_pole_forcing.md`) already proves that the aligned
pole of a cubic Type-T vertex cannot be cubic.  Hence the T2 assumptions
`X_x=y,X_y=x` in Part 3.1 are impossible: `x,y` are cubic and the only
surviving pole choice is `X_x=X_y=z_0`.  Part 3.1's overlap arithmetic is
conditional historical analysis, not a live row.  Part 3.2 is the surviving
one-common-terminal geometry.

## 0. Scope and what this file adds

Fifteen files were read and dependency-audited for this pass:
`contraction_saturation.md`, `contraction_central_bridge.md`,
`contraction_separator_integration.md`, `contraction_block_cut_tree.md`,
`contraction_leaf_blocks.md`, `contraction_ma2_integration.md`,
`central_bridge_templates.md`, `central_bridge_triangle.md`,
`central_bridge_triangle_s5.md`, `central_bridge_triangle_final.md`,
`type_t_recovery_audit.md`, `type_t_exact_two_a.md`, `two_cut.md`,
`type_b_realizability.md`, `type_b_compatibility.md`. Part 1 gives the
dependency audit. Part 2 recaps the notation the joint analysis needs.
**Part 3 is the new content of this file**: working through the
identical-terminal and one-common-terminal sub-cases of the joint
`(A,A)` outcome using information genuinely unavailable to either
vertex's single-bridge analysis (specifically: that the two central
bridges, in the exact-two-attachment case, are forced to *be* bridges
of an honest `two_cut.md` 2-cut, which lets the two vertices'
otherwise-independent theta exponents interact directly). **The two
rows have different certainty levels and must not be conflated:** the
one-common-terminal row gets a short, fully rigorous, unconditional
proof that `rho_x != rho_y` is forced (Part 3.2); the identical-terminal
row instead requires classifying how two paths *inside the same merged
bridge* can overlap (Part 3.1.1) — this resolves to `rho_x != rho_y`
being forced *only* in the vertex-disjoint sub-case, with an explicit
proof that cell arithmetic alone does *not* exclude the overlapping
sub-case (a genuine, exhibited residual, not a closed theorem). Part 4
is the requested joint outcome matrix, citing both results at their
correct scope plus the existing per-cell results. Part 5 makes explicit
that the order-40 frontier computation already run this session is
relevant infrastructure for the single-vertex-anchored sub-cases this
file's `(A,A)` cell reduces to, but does not by itself resolve the
enriched two-exponent-system bridge this file introduces. Part 6 is the
dependency diagram with PROVED/CONDITIONAL/FALSE/OPEN labels. Part 7
scopes (without yet building) the smallest computational model for the
part of the residual it can actually cover.

## 1. Dependency audit of the fifteen files

| file | what it establishes | status |
|---|---|---|
| `contraction_saturation.md` | Theta-bridge classification (chord vs. component bridge); S5 cut-vertex bound (at most one theta-internal vertex saturated "for free"); same-branch (3-way) and cross-branch (4-way) bridge arithmetic; Type-T witness system setup | PROVED (the arithmetic); saturation target itself NOT resolved |
| `contraction_central_bridge.md` | CB1 (central bridge attachment `>=2`, via S5 since `v` cubic `!=4`); endpoint-return vs. interior-return classification; interior return gives a topological `K4` with 7 exact cycle formulas, 3 unconditionally safe; third-edge witness itinerary (first excursion in `B_v`, proved); CB2 (one-excursion canonical witness) | PROVED (CB1, K4 formulas, first-excursion fact); CB2 likely FALSE, not settled either way |
| `contraction_separator_integration.md` | CB3' trichotomy (exactly-2-attachment clean / S5-coincident / >=3-attachment genuinely new case); paired admissible-path `K4` systems; cross-branch vs. `{p,q}`-separator dichotomy, mapping the no-cross-branch case to Type A exactly | PROVED (CB3', the dichotomy); `Lambda_0`'s full determination OPEN |
| `contraction_block_cut_tree.md` | Attachment-core pruning (5 claims, PROVED); attachment-free leaf forces an S5 cut vertex with exact lobe structure; MA1 (admissible pair from a singly-marked leaf); MA2 (trichotomy: admissible pair / S5 leaf / multiply-marked leaf — proved sharper: outcomes 1 or 3 always hold from mere nonemptiness) | PROVED throughout |
| `contraction_leaf_blocks.md` | Exhaustive theta-route census for an admissible pair (3 same-branch, 4-6 cross-branch routes); shared-port template (`2+d_i`, forbidden iff `d_i=2^m-2`); distinct-port case reduces directly to an admissible pair (no separate "port-saturated" regime) | PROVED (arithmetic + reduction); no contradiction forced, by design |
| `contraction_ma2_integration.md` | S5 outcome integrated (lobe replacement test not carried out); Type-T joint two-bridge setup, 5 priority questions listed | 5 questions OPEN, explicitly not resolved |
| `central_bridge_templates.md` | Normalizes the frozen A/P/S output templates | organizational, no new claim |
| `central_bridge_triangle.md` | Lemma NE (distinct external neighbours, PROVED); triangle-contraction witness `Q`; per-vertex theta/central-bridge construction; **corrected** anchored-detour lemma (lengths 3,4 excluded, but `ell=2` is NOT part of T2's admissible pair — the original R2/S2 error); 4-row `(X_x,X_y)` classification; V.2's 6 component-sharing possibilities, (1)-(3) settled, (4)-(6) OPEN | PROVED where marked; (4)-(6) explicitly OPEN |
| `central_bridge_triangle_s5.md` | VI.1 double-S5 (same `z`, forced lobe distribution, `L=L'` per addendum) PROVED for generic `z not in T`; `z in T` degenerate case OPEN; VI.2 mixed S/(A,P) (vacuous-crossing case eliminated, generic non-touching case unaffected, touching-and-detour-into-`L` OPEN); VIII/IX `(P,P)`/`(A,P)` sketched, explicitly not eliminated | mixed |
| `central_bridge_triangle_final.md` | X.0 (terminal-pair relationship: identical or one-common, crossing arithmetically impossible in this anchored setting) PROVED; X.1/X.2's concrete R2/S2 arithmetic SUPERSEDED (refuted); XI (T3 3-way consistency — no cross-pair dependency exists to be inconsistent about) | X.0 PROVED; X.1/X.2 FALSE (refuted, not just superseded loosely) |
| `type_t_recovery_audit.md` | Forensic recovery of the interrupted R2/S2 claim; conditional anchored-detour lemma (PROVED); explicit Heawood regression fixture refuting the "shortest path is in the admissible pair" inference; 7-row residual table | the R2/S2 claim: FALSE (refuted with an explicit fixture); residuals: OPEN |
| `type_t_exact_two_a.md` | Full corrected guaranteed-cycle table for anchored exact-two-attachment A (8 lengths: own-bridge closures `ell,ell+1,ell+delta,ell+delta+1` plus cross-cut `ell+2^rho,ell+delta+2^rho,ell+2^s+1,ell+delta+2^s+1`); explicit infinite safe family `ell=2^t+1,t>max{rho,s,3}`; Heawood/Balaban regression fixtures | PROVED (the table, the safe family); exact-two-A NOT eliminated |
| `two_cut.md` | The entire 2-cut machinery: T1 (closure 2-connected), T2 (Gao-Huo-Liu-Ma admissible pair, cited from literature), T4 (exact Type A/B/C classification of every 2-cut), T3/T5 (self-sum replacement forcing, Type-A-scoped), T6 (copy-gadget construction), T8/T8R/T8P (Type-A gadget criticality + SPQR real-edge rule, self-sum-clean-scoped), T9B (whole-pair Type-B criticality, does NOT need self-sum-cleanliness) | PROVED throughout; T7/the general Type-A self-sum conjecture remains CONJECTURAL |
| `type_b_realizability.md` | Freezes the Type-B tuple `Pi=(rho,s,t,u,delta,epsilon)`, `S1={2,ell,ell+delta}`, `S2={2^rho,2^s+1,m,m+epsilon}`; order/edge lower bounds; fixed-template UNSAT certificate for `Pi_0=(2,2,4,4,1,1)` at order 36; Balaban `5+11` ear-closure mechanism | PROVED (bounds, UNSAT certificate for one embedding); ICF/realizability in general OPEN |
| `type_b_compatibility.md` | Maps the triangle-anchored exact-two-attachment-A configuration onto an actual `two_cut.md` Type-B 2-cut, `B_1` = the central bridge (carrying `S1`), `B_2` = the bridge through the external neighbour (carrying `S2`); proves T9B in this setting | PROVED (the mapping, T9B); Type B NOT eliminated |

**Overall: neither Type N nor Type T is eliminated by any of the
fifteen files, individually or in combination, as of this audit.** The
single most consequential repeatedly-flagged open item across this
entire sequence is the joint two-central-bridge interaction at a shared
Type-T triangle (`contraction_saturation.md` VII.3,
`contraction_separator_integration.md` Part IX,
`contraction_ma2_integration.md` Part X) — exactly the target of this
file.

## 2. Notation recap

Fix a triangle `T={x,y,z_0}` of a minimal counterexample `G`, `x,y`
cubic (T2: `z_0` in `H`; T3: `z_0` also cubic — both covered uniformly
below unless noted). Each cubic vertex `v in {x,y}` has: its own
canonical theta `Theta_v` (poles `{X_v,v'}`, `v'` = external neighbour,
`X_v in T\{v}` = whichever triangle-mate the canonical `vv'`-edge
witness exits through); its central bridge `B_v` (the `Theta_v`-bridge
carrying `v`'s *other* triangle edge `v{-}Y_v`, `Y_v:=T\{v,X_v}`); and
an MA2 output `tau_v in {A,P,S}` (admissible pair / shared port / S5
leaf). By Lemma NE, `x'!=y'`. By `central_bridge_triangle_final.md`
X.0, the terminal *sets* `{x,X_x}` and `{y,X_y}` are always either
identical (`X_x=y,X_y=x`, the **identical-terminal** row) or share
exactly one element (representative case `X_x=X_y=z_0`, the
**one-common-terminal** row) — never four genuinely distinct vertices
(only 3 candidates exist in `T`).

## 3. New result: the cross-exponent obstruction in the joint `(A,A)` outcome

Assume `tau_x=tau_y=A` (CB3' case 1 at both `x` and `y`): `att(B_x)=
{x,X_x}` exactly, `att(B_y)={y,X_y}` exactly.

### 3.1. Identical-terminal row (`X_x=y, X_y=x`): `B_x=B_y` as literal vertex sets [PROVED]

Here `{x,X_x}={y,X_y}={x,y}`: both central bridges are attached at the
*same* pair of vertices. By `contraction_separator_integration.md`
VI.1, `att(B_v)={v,x}` exactly makes `{v,x}` a genuine 2-cut of `G` and
`B_v` a genuine `two_cut.md`-style nontrivial `xy`-bridge at that
cut — i.e. `B_v`, as a vertex set, is **exactly one full connected
component** of `G-{v,x}` (not merely contained in one). Applying this
with `v=x`: `B_x` is the connected component of `G-{x,y}` containing
`Y_x=z_0`. Applying it with `v=y`: `B_y` is the connected component of
`G-{y,x}=G-{x,y}` containing `Y_y=z_0`. **This is the same deletion
`G-{x,y}`, and connected components of a fixed graph partition its
vertex set** — a vertex lies in exactly one component. Since both
`B_x` and `B_y` are asserted to be *the entire* component containing
the same vertex `z_0`, they must be the same component:

\[
\boxed{B_x=B_y\text{ as vertex sets (hence as bridges).}}
\]

This resolves, in this specific sub-case, the question
`central_bridge_triangle.md` V.2(2) left open ("same component...
realizable as a special case of row 4, not provable in general") — it
**is** provable here, precisely because both bridges are independently
certified (via CB3' case 1) to be *entire* connected components of the
*identical* deletion `G-{x,y}`.

**Consequence: `{x,y}` is a Type-B 2-cut with a merged second bridge.**
`xy in E(G)` (a triangle edge), so by `two_cut.md` T4's exact
classification, the 2-cut `{x,y}` has **exactly 2** nontrivial bridges
(Type B, not Type A's 3). One of them is `B_1:=B_x=B_y`. Since
`att(B_x)={x,y}` *exactly* (no third attachment), `B_1` has no edge to
`x'` or to any `Theta_x`-branch-internal vertex; symmetrically no edge
to `y'` or any `Theta_y`-branch-internal vertex. So `x'` and `y'` both
lie in `G-{x,y}` but not in `B_1` — and since Type B admits only one
*other* nontrivial bridge, **`x'` and `y'` (distinct, by Lemma NE) lie
in the same single remaining bridge**, call it `B_2^{joint}`.

**`B_2^{joint}`'s spectrum is enriched, not merely `x`'s own.** `B_2^{joint}`
contains `x'` plus the `rho_x,s_x` branch-internal vertices of
`Theta_x` (giving `x`-`y` path lengths `2^{rho_x}` and `2^{s_x}+1`, via
the edge `x{-}x'` plus each branch to the pole `y=X_x`) **and**,
simultaneously, `y'` plus the `rho_y,s_y` branch-internal vertices of
`Theta_y` (giving `x`-`y` path lengths `2^{rho_y}` and `2^{s_y}+1`).
So:
\[
\Lambda(B_2^{\rm joint})\supseteq\{2^{\rho_x},\,2^{s_x}+1,\,2^{\rho_y},\,2^{s_y}+1\}.
\]

**Scope note on the other 5 pairs of this 4-element spectrum.** Only
the `(2^{\rho_x},2^{\rho_y})` pair is analysed below (3.1.1) — this is
the specific pair the task asked to resolve, and the one this file's
headline result concerns. The other 5 pairs (`rho_x`-vs-`s_y`,
`s_x`-vs-`rho_y`, `s_x`-vs-`s_y`, and each against itself) all involve
paths living in the *same* bridge `B_2^{joint}` too, so they carry the
identical same-bridge overlap ambiguity — an "odd total" is **not**
by itself a safety guarantee once overlap is allowed (a quick check
shows an overlapping split of an odd-length pair can still expose an
even, individually-`\mathcal F`-hitting cell — e.g. `rho_x=s_y=2`,
paths of length `4,5`, split `(1,3)`/`(3,2)` gives a first cell of
length `4`). **These 5 pairs are not analysed in this file** — flagged
honestly as unaudited, not silently assumed safe.

**3.1.1. The overlap dichotomy, resolved [PROVED for one branch, REFUTED
for the other — this is the corrected, precise scope of this row's
obstruction].** `P_x` (`x`-`x'`-...-`y`, length `2^{rho_x}`) and `P_y`
(`y`-`y'`-...-`x`, length `2^{rho_y}`) are both simple `x`-`y` paths
lying inside the same bridge `B_2^{joint}`. By Lemma NE, `x'!=y'`, so
they diverge immediately, but nothing proved so far rules out a *later*
reconvergence at a shared internal vertex — whether they are internally
disjoint is a genuine open structural question (of exactly the kind
`contraction_intersections.md` V.2 already showed canonicalization does
**not** resolve in general), not settled by any existing lemma. The
`two_cut.md` §11 symmetric-difference identity applies to *any* two
`x`-`y` paths regardless of overlap: writing `omega` for their shared-
edge count and `C_1,...,C_k` for the edge-disjoint cycles the symmetric
difference decomposes into,
\[
|P_x|+|P_y| = 2\,\omega + \sum_i|C_i|,
\]
and *each* `C_i` is an actual cycle of `G`, so **every one** must avoid
`\mathcal F`. This splits the question into exactly the two cases the
overlap taxonomy allows:

- **Internally vertex-disjoint (`omega=0`, one cell: `P_x,P_y` share
  only the endpoints `x,y`).** Then `k=1` and the single cycle
  `C_1=P_x\cup P_y` has length exactly `2^{\rho_x}+2^{\rho_y}` — a power
  of two **exactly when `rho_x=rho_y`** (`2^a+2^b\in\mathcal F` iff
  `a=b`, giving `2^{a+1}`; verified computationally for `a,b\in[2,19]`
  as a hygiene check). **So in this sub-case, `rho_x=rho_y` forces an
  immediate `C_{2^{\rho_x+1}}` — outcome (1) of the task, genuinely
  established, but scoped exactly to this sub-case.**
- **Sharing an internal vertex (`omega=0`, `k\ge2`; or `omega>0`, fewer/
  shorter cells).** Here `rho_x=rho_y` does **not** force a
  contradiction by cell arithmetic alone. **Explicit general refutation
  [PROVED]:** for every `rho\ge2`, split `P_x`'s length `L=2^{\rho}`
  into two cells `a_1=1,a_2=L-1` and `P_y`'s length `L` into
  `b_1=2,b_2=L-2` (valid: `b_2\ge1` for `L\ge3`, true for `rho\ge2`).
  The resulting cell-cycle lengths are `a_1+b_1=3` and
  `a_2+b_2=2^{\rho+1}-3`. `3` is below `\mathcal F`'s smallest element
  (4), and `2^{\rho+1}-3` is odd (even minus odd), hence never in
  `\mathcal F` (all of `\mathcal F` is even) — **both cell-cycles are
  clean for every `rho\ge2`, verified computationally for
  `rho\in[2,19]`.** So **a two-cell overlap pattern exists, for every
  exponent, that is completely invisible to cell arithmetic** — the
  naive hope of extending outcome (1) to the overlapping case is
  **REFUTED** by this explicit family (matching exactly the same
  cancellation phenomenon `type_t_exact_two_a.md` §7 already documented
  for the *different* problem of overlapping T2 admissible-pair paths
  within one bridge — this is not a new phenomenon, but its
  applicability to *this* pair of paths had not been checked before).

**Honest scope, corrected.** The identical-terminal row's cross-exponent
claim is **not** a general theorem: it holds unconditionally only in
the internally-vertex-disjoint sub-case. The overlapping sub-case is
**not excluded by arithmetic** — this is a genuine, exhibited residual
(outcome (4) of the task, not outcome (1) or (2)): whether an *actual
graph* realizes an overlapping `B_2^{joint}` with `rho_x=rho_y` (i.e.
whether the abstract escaping cell-assignment above, or one like it, is
graph-realizable once `B_2^{joint}`'s own internal degree-`\ge3`,
2-connected-closure, and `s_x,s_y`-branch requirements are all imposed
simultaneously) is **not resolved by this file** and is the precise
next question — a genuinely different, and harder, target than the
abstract arithmetic escape alone, exactly parallel to how
`type_t_exact_two_a.md` §7 flagged its own path-incidence
counterexamples as "not settling whether degree-three saturation plus
full `F`-cleanness eliminates every such overlap." Part 3.2 below gives
a version of the exponent-inequality conclusion that needs **no**
overlap assumption at all, because it compares two paths in
*different* bridges (automatically disjoint), not two paths in the
*same* bridge.

### 3.2. One-common-terminal row (`X_x=X_y=z_0`): a fully rigorous cross-cut version [PROVED unconditionally]

Here `{x,X_x}={x,z_0}` and `{y,X_y}={y,z_0}` are two *different* 2-cuts
(sharing only the vertex `z_0`), so the identical-bridge argument of
3.1 does not apply directly. Instead: `xz_0 in E(G)` (triangle edge), so
by T4 the 2-cut `{x,z_0}` is Type B with exactly 2 nontrivial bridges.
One is `B_x` (`=` the component of `G-{x,z_0}` containing `Y_x=y`,
since `att(B_x)={x,z_0}` exactly); call the other (containing `x'`)
`B_2^{(x)}`, with `Lambda(B_2^{(x)})\supseteq\{2^{\rho_x},2^{s_x}+1\}`
exactly as in the single-vertex analysis.

**`B_x` inherits `y`'s own branch lengths.** Since `B_x` contains
`Y_x=y` and (by the same containment argument as 3.1) all of `Theta_y`
except its own pole `z_0` — in particular `y'` and `y`'s
`rho_y,s_y`-branches — every `x`-to-`z_0` path in `B_x` begins with
the forced edge `x{-}y` (`x`'s unique edge into `B_x`) and can continue
along `y`'s own branch to `z_0`, giving `x`-`z_0` path lengths
`1+(2^{\rho_y}-1)=2^{\rho_y}` and `1+2^{s_y}=2^{s_y}+1`. So:
\[
\Lambda(B_x)\supseteq\{2,\ \ell_x,\ \ell_x+\delta_x,\ 2^{\rho_y},\ 2^{s_y}+1\}.
\]

**The cross-cut sum, fully rigorous.** `B_x` and `B_2^{(x)}` are two
*different* nontrivial bridges of the *same* 2-cut `{x,z_0}` —
`two_cut.md` §2's global bridge-spectrum identity applies directly, no
disjointness assumption needed (distinct bridges of a 2-cut share only
the two terminals, by definition):
\[
(\Lambda(B_x)+\Lambda(B_2^{(x)}))\cap\mathcal F=\varnothing.
\]
In particular `2^{\rho_y}+2^{\rho_x}\notin\mathcal F`. Since
`2^a+2^b in F` iff `a=b`:
\[
\boxed{\rho_x\ne\rho_y\text{ is forced (else an actual cross-cut cycle
of length }2^{\rho_x+1}\text{ exists, a direct contradiction).}}
\]

**The other three cross-terms are automatically safe, checked
exhaustively.** `2^{s_x}+1+2^{s_y}+1=2^{s_x}+2^{s_y}+2` is a power of
two only if `s_x=s_y` *and* `2^{s_x}+1` is itself a power of two
(needs `s_x=0`, excluded since `s_x\ge2`) — never in `F` (verified
computationally for `s_x,s_y in [2,11]`, matching the elementary
argument). `2^{\rho_y}+2^{s_x}+1` and `2^{\rho_x}+2^{s_y}+1` are each
(even)+(odd)`=`odd, never in `F` (all elements of `F` are even). **So
`rho_x!=rho_y` is the unique new necessary condition** this
cross-interaction produces; nothing else is forced by it.

### 3.3. What this does and does not establish — precise per-row scope

**The two rows have genuinely different certainty levels; this is not
a single theorem with one uniform scope, and must not be summarized as
one.**

- **One-common-terminal row (3.2): `rho_x!=rho_y` is forced,
  unconditionally, PROVED.** The two paths compared live in two
  *different* bridges of the same 2-cut `{x,z_0}`, which are
  automatically vertex-disjoint except at the terminals — no overlap
  question arises at all.
- **Identical-terminal row (3.1.1): `rho_x!=rho_y` is forced *only* in
  the internally-vertex-disjoint sub-case of the two paths inside the
  single merged bridge `B_2^{joint}`.** In the overlapping sub-case,
  arithmetic alone does **not** force a contradiction — an explicit
  general two-cell escape family (valid for every `rho\ge2`) was
  exhibited that evades every individual cell-cycle length landing in
  `\mathcal F`. **This sub-case is a genuine open residual, not a
  proved theorem** — whether it is graph-realizable once every other
  constraint on `B_2^{joint}` (internal degree `\ge3`, 2-connected
  closure, the `s_x,s_y` branches, `Q`) is imposed simultaneously is
  the precise next question, not resolved here.
- **Not established in either row:** that `rho_x!=rho_y` (where it is
  forced) is *sufficient* for a survivor — the full guaranteed-length
  tables of both vertices (`type_t_exact_two_a.md`'s 8-length table,
  applied at each vertex) still need joint cross-checking against each
  other and against `Q` (the triangle-contraction witness), which is
  not carried out here. `(A,A)` is **narrowed, not eliminated**, and
  narrowed unconditionally only via the one-common-terminal row.
- **Scope:** this argument uses only the `rho` exponents (the
  near-power-edge-witness branch). The `s` exponents (closed-
  neighbourhood witness branch) were checked and found safe in every
  combination — this is not an oversight, it is the complete case
  check (Section 3.2's "automatically safe" paragraph).

## 4. The joint outcome matrix

| `tau_x \ tau_y` | `A` | `P` | `S` |
|---|---|---|---|
| **`A`** | **Split by row, not one outcome.** *One-common-terminal:* **(a)** `rho_x!=rho_y` forced unconditionally (Part 3.2, PROVED); given that, reduces to a genuine Type-B 2-cut per Part 5; residual survives for `rho_x!=rho_y` — **(d)**. *Identical-terminal:* `B_x=B_y` forced (PROVED); `rho_x!=rho_y` forced *only* in the vertex-disjoint sub-case — **(a)** there, but **(d)**, a genuine open residual, in the overlapping sub-case (Part 3.1.1; arithmetic alone does not exclude it, an explicit escape family exists) | **(d):** not eliminated; terminal-set relationship (coincide / meet-once / disjoint) depends on unresolved P-port geometry (`central_bridge_triangle_s5.md` IX, corrected scope); no new joint arithmetic beyond the two independent frozen templates found | **(c)+(d):** vacuous-crossing case eliminated (PROVED); generic non-touching case leaves `tau_x=A`'s own single-vertex reduction (Part 5) untouched; touching-and-detour-into-`L` OPEN (needs `L`'s internal spectrum) |
| **`P`** | *(symmetric to above)* | **(d):** not eliminated, not reducible further than the two independent shared-port templates plus `Q`'s pair, unless port vertices coincide with `Q`'s own attachment pair (unresolved geometry, `central_bridge_triangle_s5.md` VIII) | **(c)+(d):** same structure as `(A,S)` but with `P`'s shared-port arithmetic in place of `A`'s admissible pair |
| **`S`** | *(symmetric)* | *(symmetric)* | **(c):** `z_x=z_y=z` forced by S5 uniqueness (PROVED); generic `z notin T` forces `T` and both thetas into one lobe, the two attachment-free leaves into the *same* literal component `L=L'` (PROVED, per the addendum correction cited in `central_bridge_triangle_s5.md` VI.1); degenerate `z in T` case **OPEN** |

**Every cell is resolved to the extent the cited files (plus Part 3's
new lemma) resolve it; no cell is claimed closed.** The `(A,A)` cell is
the only one with new content in this pass; every other cell's entry
is a citation of existing, already-published results in the fifteen
audited files, not a new derivation.

## 5. The order-40 frontier is relevant infrastructure — not a resolution — for the `(A,A)` residual

This connection is not stated explicitly anywhere in the fifteen
audited files, and is worth making explicit: **the `S1={2,ell,ell+delta}`,
`S2={2^rho,2^s+1,m,m+epsilon}` tuple frozen in `type_b_realizability.md`
is exactly the spectrum of the Type-B 2-cut `type_b_compatibility.md`
Section 3 constructs from a single triangle-anchored central bridge**
(`B_1=` the central bridge carrying the isolated length-2 path, `B_2=`
the bridge through the external neighbour). The bridge-order lower
bounds derived there (`|V(B_1)|>=ell+delta+1`) match, exactly, the
naming of this session's earlier work: `ell=17,delta=1 -> |V(B_1)|>=19`
is `B19`; the order-20/order-21 layers extend this to larger `delta`
and larger bridge order.

**What this means concretely.** Every negative result already
established this session for the fixed tuple `Pi_0=(2,2,4,4,1,1)` and
its order-21 (`t` one step higher) extensions — B19 (bridge order 19
impossible), B20/B20D2 (order 20 impossible, both gap types), and the
four order-21 `E=29`/`E=30` layers (all empty, fully cross-validated)
— is **literal progress on the single-vertex-anchored realizability
question underlying the `(A,A)` residual of this file's joint matrix**
(the one-common-terminal row's forced-`rho_x!=rho_y` case, and the
identical-terminal row's vertex-disjoint sub-case — see Part 6's
diagram), restricted to that one specific `(rho,s,t,u,delta,epsilon)`
range, and **not** the identical-terminal row's overlapping sub-case
(Part 3.1.1), which the order-40 generators do not model at all. It is
not "generic Type-B lower-bound raising" in the sense the
earlier strategic redirection worried about; it is the concrete,
already-running computational attack on exactly the residual this Part
4's `(A,A)` cell identifies.

**What this does not yet mean.** The order-40 frontier work covers only
`Pi_0` (`rho=s=2`, one specific `t=u=4`) at bridge orders up to 21
(`E=31` still open). It does not (yet) address:
- the full parameter range `rho,s>=2`, arbitrary `t,u>max{rho,s,3}`
  (only the smallest instantiation has been attacked computationally);
- **Part 3's new joint constraint**, which requires *two* copies of the
  `S2`-side spectrum simultaneously (`{2^{rho_x},2^{s_x}+1,2^{rho_y},
  2^{s_y}+1}` with `rho_x!=rho_y}`, in the merged-`B_2` sub-case of
  `(A,A)`) — a strictly richer object than the single-vertex `S2` the
  order-40 frontier generators currently target.

So the order-40 frontier's continued success is **conditionally
relevant**: if it is eventually extended to an all-orders
non-realizability theorem for the single-vertex `B_1`/`S1` family, that
would resolve the single-vertex-anchored sub-cases of `(A,·)`/`(·,A)`
directly; as it stands (finite orders only, one tuple), it is a
nonzero but incomplete fragment, exactly as the earlier strategic
message anticipated ("do not spend the majority of effort extending
conditional finite lower bounds").

## 6. Dependency diagram

```text
arbitrary Type-T triangle T={x,y,z_0}, x,y cubic
  |
  +-- M1/Lemma NE: x'!=y' [PROVED]
  |
  +-- per-vertex Theta_v, B_v (contraction_saturation.md VII.2,
  |     contraction_central_bridge.md CB1) [PROVED]
  |
  +-- per-vertex MA2 output tau_v in {A,P,S}
  |     (contraction_block_cut_tree.md MA2) [PROVED]
  |
  +-- X.0: terminal-pair relationship exhausted to
  |     identical-terminal or one-common-terminal, never crossing
  |     (central_bridge_triangle_final.md) [PROVED]
  |
  +-- joint matrix (tau_x,tau_y):
        |
        +-- (S,S) --[S5 uniqueness]--> one exact lobe config,
        |            L=L' literally, generic z notin T [PROVED]
        |            z in T degenerate case [OPEN]
        |
        +-- (S,A)/(S,P) mixed --> vacuous-crossing eliminated [PROVED]
        |            non-touching case: other vertex's own branch
        |            unaffected --> falls through to that branch's
        |            own row/column
        |            touching-and-detour-into-L [OPEN, needs L's
        |            internal spectrum]
        |
        +-- (A,A) --[Part 3, NEW]--> reduces to enriched Type-B 2-cut(s)
        |            [PROVED reduction, Part 3.1/3.2, both rows]
        |            |
        |            +-- one-common-terminal row: rho_x != rho_y
        |            |     forced UNCONDITIONALLY [PROVED, Part 3.2 --
        |            |     cross-cut sum between automatically-disjoint
        |            |     bridges of the same 2-cut]
        |            |     --> residual for rho_x != rho_y: [OPEN]
        |            |
        |            `-- identical-terminal row: B_x=B_y forced
        |                  [PROVED, Part 3.1]; rho_x != rho_y forced
        |                  ONLY in the vertex-disjoint sub-case
        |                  [PROVED, Part 3.1.1]; in the overlapping
        |                  sub-case, an explicit escape family REFUTES
        |                  the naive extension [PROVED counterexample,
        |                  Part 3.1.1] --> graph-realizability of the
        |                  escape [OPEN, the precise next question]
        |            --> single-vertex-anchored realizability =
        |            order-40 frontier's own computational program
        |            [CONDITIONAL: resolves the single-vertex sub-cases
        |            only if that program reaches an all-orders
        |            theorem; currently a finite fragment; does NOT
        |            address the enriched joint spectrum at all]
        |
        +-- (A,P)/(P,A) --> [OPEN, corrected scope, no false pinning]
        |
        `-- (P,P) --> [OPEN, not reducible further than independent
                     per-vertex templates + Q's pair]
```

**No arrow in this diagram is marked FALSE except one, noted for
completeness: the historical R2/S2 concrete arithmetic candidate
(`central_bridge_triangle_s5.md`/`final.md`'s pinned `ell=2,ell'in{3,4}`
inference) is FALSE, refuted with an explicit fixture
(`type_t_recovery_audit.md`), and does not appear in this diagram at
all — it has been fully superseded by the corrected, unpinned A
templates used throughout Parts 3-4 above.**

## 7. Proposed next computational model (not built this pass)

**This step is deliberately deferred until the overlap question (Part
3.1.1) is resolved further, or at least explicitly scoped as the
generator's known blind spot** — building it now, without that
resolution, would silently bake in the unproved vertex-disjointness
assumption for the identical-terminal row.

The natural smallest next target, following directly from Part 3.2's
fully rigorous (one-common-terminal, automatically-disjoint) cross-cut
version: extend `type_b_realizability.py`'s frozen-tuple generator to a
**joint tuple** `Pi_J=(rho_x,s_x,rho_y,s_y,t,u,delta,epsilon)` with the
constraint `rho_x!=rho_y` built in, and `B_2`'s spectrum enriched to
`{2^{rho_x},2^{s_x}+1,2^{rho_y},2^{s_y}+1}` (four forced lengths
instead of two) rather than the single-vertex `S2`. The smallest such
instantiation is `rho_x=2,rho_y=3` (or the symmetric `rho_x=3,rho_y=2`),
`s_x=s_y=2` (checked safe in Part 3.2, imposes no extra constraint),
with `t,u` as small as the existing frontier's own bookkeeping allows.

**Scope this generator would actually cover, stated precisely.** Such a
generator would resolve realizability for: the one-common-terminal
row's `rho_x!=rho_y` case (Part 3.2, unconditional), and the
identical-terminal row's *vertex-disjoint* sub-case (Part 3.1.1, where
`rho_x!=rho_y` is likewise unconditional there). It would **not**
address the identical-terminal row's *overlapping* sub-case (Part
3.1.1's escape family) at all — that sub-case's residual is a
different, harder question (whether an overlapping `B_2^{joint}` is
graph-realizable), not answerable by the same fixed-non-overlapping-
path-union template `type_b_realizability.py` uses. Building a model
for the overlapping sub-case specifically would need to additionally
parametrize the *cell structure* of the two paths' shared vertices,
which is a genuinely new generator design, not a straightforward
extension. This is proposed here as the next step, per the user's
explicit instruction to build such a model *if* a residual obstruction
survives, but **not attempted in this pass** — the primary deliverable
this turn was resolving the overlap question itself (Part 3.1.1), which
is now done to the extent it currently can be (a proved dichotomy, not
a closed theorem).

## 8. What is explicitly claimed and what is not

- **Claimed (new, PROVED, unconditional):** in the joint `(A,A)`
  outcome's one-common-terminal row, `rho_x!=rho_y` is forced (Part
  3.2) — an unconditional cross-cut-sum argument between two
  automatically-disjoint bridges of the same 2-cut.
- **Claimed (new, PROVED, unconditional):** in the identical-terminal
  row, `B_x=B_y` as literal vertex sets (Part 3.1), and `rho_x!=rho_y`
  is forced *specifically and only* in the sub-case where the two
  `2^{rho_x}`/`2^{rho_y}`-length paths inside the merged bridge
  `B_2^{joint}` are internally vertex-disjoint (Part 3.1.1).
- **Claimed (new, PROVED, a refutation not a theorem):** in that same
  identical-terminal row, the *overlapping* sub-case is **not** excluded
  by cell arithmetic alone — an explicit general two-cell escape family,
  valid for every `rho\ge2`, was exhibited (Part 3.1.1). **This is
  explicitly a proof that a naive unconditional extension would be
  false, not a proof that the overlapping sub-case survives as an
  actual graph** — whether it is graph-realizable remains the open
  residual.
- **Claimed (synthesis, not a new theorem):** the order-40 frontier
  computation already run this session is relevant infrastructure for
  the single-vertex-anchored sub-cases of `(A,·)`/`(·,A)` (Part 5), but
  it does **not** already resolve the enriched joint bridge `B_2^{joint}`
  (which simultaneously carries both vertices' exponent systems,
  `{2^{\rho_x},2^{s_x}+1,2^{\rho_y},2^{s_y}+1}`) — the prior frozen
  tuples were single-vertex anchored, and this is a strictly richer
  object the existing generators do not target.
- **Claimed (audit only, no new derivation):** the status of every
  other cell of the joint matrix (Part 4), each citing the exact
  existing file and result.
- **Not claimed:** that Type T (or Type N) is eliminated; that any
  matrix cell is fully closed; that the identical-terminal row's
  overlapping-sub-case residual is resolved; that the proposed
  joint-tuple model (Part 7) has been built or run; any all-orders
  theorem of any kind.
