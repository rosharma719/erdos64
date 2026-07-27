# contraction_central_bridge.md — the central-bridge lemma and topological-K4 reduction

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Builds on `contraction_atoms.md`, `contraction_neighborhood.md`,
`contraction_mixed_witness.md`, `contraction_intersections.md`,
`contraction_saturation.md`, and the pre-existing `lemmas.md`/`two_cut.md`
separator machinery (S4, S5, T1-T5).

## Part I: the central-bridge lemma

Let `\Theta=P_0\cup P_1\cup P_2` be a canonical NPT theta with poles
`p,q`, `P_0=p{-}v{-}q` the length-2 branch through the cubic vertex `v`.
Let `e_v=vw` be `v`'s third edge (not part of `\Theta`), and `B_v` the
`\Theta`-bridge containing `e_v` — a chord `vw` if `w\in V(\Theta)`, or
the component of `G-V(\Theta)` containing `w` (with all its edges to
`\Theta`) otherwise.

### I.1. CB1 — the central return lemma [PROVED]

**Claim.** `|\operatorname{att}(B_v)|\ge2`.

**Chord case, trivial.** If `e_v` is itself a chord `vw`
(`w\in V(\Theta)`), `\operatorname{att}(B_v)=\{v,w\}` already has size 2
by definition — nothing to prove.

**Component case.** Suppose for contradiction
`\operatorname{att}(B_v)=\{v\}`: every edge from `B_v`'s component `C`
to `\Theta` lands on `v` (however many such edges, from however many
`C`-vertices). `C`'s only edges leave to `\Theta}` (definition of
"component of `G-V(\Theta)`") or stay inside `C` — and by hypothesis
every `\Theta`-directed edge lands on `v`. **So `G-v` disconnects `C`
from the rest of `G`**: `v` is a cut vertex.

By **S5** (`lemmas.md`): *every cut vertex of a minimal counterexample
has degree exactly 4.* But `v` is cubic, `\deg_G(v)=3\ne4`. Contradiction.
**So `\operatorname{att}(B_v)\ne\{v\}`, i.e. `|\operatorname{att}(B_v)|\ge2`.** ∎

**This is strictly sharper than `contraction_saturation.md` VI.2's "at
most one theta vertex can support a single-attachment bridge"**: that
was a global count over the whole theta; CB1 pins down that *this
specific* bridge — the one carrying the cubic center's own third edge —
can *never* be single-attachment, because `v`'s own degree (3) already
falls outside S5's forced value (4) for the one exceptional vertex S5
would otherwise allow.

**Computational cross-check.** `verifier/central_bridge.py`'s
`check_cb1` builds fixtures with a component attached at a single
theta-vertex and confirms directly that this vertex is a cut vertex
(disconnection on removal) whenever such a configuration is constructed
around a cubic branch-vertex — this is a structural/definitional check
(cut-vertex detection), not a test of S5 itself, which is cited, not
re-derived.

### I.2. Canonical return attachment [definitional]

Fix `x\in\operatorname{att}(B_v)\setminus\{v\}` (nonempty by CB1) and a
simple path `R:v\to x` with internal vertices avoiding `V(\Theta)`,
chosen among all such `(x,R)` pairs by, in order: (1) shortest `|R|`;
(2) shortest distance from `x` to `\{p,q\}` along its own theta branch;
(3) fewest intersections with the previously-selected contraction
witnesses (`P_a,P_b,P_c,Q_{pq}` etc.); (4) a fixed lexicographic
tie-break. A unique minimizer exists (`G` finite).

**What this licenses.** Criterion (1) makes `R` a *bona fide shortest*
`B_v`-internal `v`–`x` path — any argument assuming `R` cannot be
shortcut is licensed directly. Criterion (2) breaks ties toward
attachments close to the poles, keeping subsequent `d,M-d` arithmetic
(Part IV) as simple as the graph allows. Criterion (3) is exactly the
minimal-overlap licensing already used in `contraction_mixed_witness.md`
III.2 and `contraction_intersections.md`: it makes "assume clean
relative to the other witnesses" the best-available hypothesis, not an
arbitrary one — though, per `contraction_intersections.md` V.2, it does
**not** by itself force zero overlap; it only guarantees the canonical
choice achieves the least overlap available for the fixed `|R|`,
distance, and profile already fixed by (1)–(2).

## Part II: classifying the return location

Four geometric locations for `x`: **(1)** `x=p`; **(2)** `x=q`; **(3)**
`x` internal to `P_1`; **(4)** `x` internal to `P_2`. **(1) and (2) are
equivalent under `p\leftrightarrow q` only when the theta's own data
share that symmetry** — i.e. only if `P_1,P_2}` are *interchangeable*
(same length, same role/origin). For a generic NPT theta with `|P_1|=
2^r-1\ne2^s=|P_2|` (or even if numerically equal, `P_1`'s origin as a
nontriangle-edge witness and `P_2`'s as a closed-neighbourhood witness
are structurally different objects), **no such quotient is taken
automatically** — cases (1)/(2) and (3)/(4) are each treated on their
own throughout. **Whether `pq\in E(G)`** is recorded explicitly (it can
occur in Type T configurations where `\{p,q\}` are the triangle pair)
and folded into the cycle lists below wherever relevant.

## Part III: the endpoint-return case (`x=p`, symmetrically `x=q`)

Write `|R|=\ell`. `R` touches `\Theta` only at its endpoints `v,p`
(internal vertices avoid `V(\Theta)`, by I.2). Every simple cycle of
`\Theta\cup R` containing `R` closes `R` via some `p`-to-`v` route
inside `\Theta` (plus the extra `pq` edge, if present):

\[
\boxed{\ell+1}\ (\text{via direct edge }pv),\qquad
\boxed{\ell+1+M}\ (\text{via }P_1\text{ then edge }qv),\qquad
\boxed{\ell+1+N}\ (\text{via }P_2\text{ then edge }qv),
\]
and, **only if `pq\in E(G)`**,
\[
\boxed{\ell+2}\ (\text{via edge }pq\text{ then edge }qv).
\]

**Exhaustiveness.** A `p`-to-`v` route inside `\Theta` not reusing `R`
must reach `v` via one of `v`'s two `\Theta`-edges, both landing at
`q` first except the direct `pv` edge — so it either uses `pv` directly,
or reaches `q}` first (via `P_1`, `P_2`, or the `pq` edge if present)
then closes with the `qv` edge; no route uses both `P_1` and `P_2}`
(that would revisit `p` or `q}`). Exactly the four listed, no more.

**Structural relationship to `e_v`.** `v` is cubic with edges to
`p,q\in\Theta` and `e_v` into `B_v}` — so `R`, leaving `v` into `B_v`,
**must begin with `e_v` itself**: `R=v{-}w{-}[\text{rest}]`, where
`[\text{rest}]` is a `w`-to-`p` path of length `\ell-1` inside `B_v`
(this is the precise sense in which `R` is *not* automatically the full
outside portion of `e_v`'s near-power witness — it is a `B_v`-internal
fragment sharing `e_v` as its first edge; Part V determines exactly how
far this relationship extends).

**Forbidden-length conditions [PROVED, symbolic normal form].** None of
the (three or four) lengths above may equal a power of two:
\[
\ell+1\ne2^m,\qquad \ell+1+M\ne2^m,\qquad \ell+1+N\ne2^m,\qquad
(\text{if }pq\in E(G):)\ \ell+2\ne2^m
\]
for every valid `m`. **No contradiction follows from these alone** —
each excludes only finitely many residues of `\ell` locally, and `\ell`
is not otherwise bounded by this file's tools alone (Part V is exactly
where a tighter bound on `\ell` — via its relationship to `e_v`'s own
near-power exponent — would have to come from, and is not established
there either). **This is the one exact endpoint-return normal form**:
`R`'s length must avoid the listed residues, `R` necessarily begins
with `e_v`, and no further conclusion is drawn without Part V's
(unresolved) itinerary analysis.

**Computational cross-check.** `check_endpoint_return` builds an
explicit `\Theta\cup R` gadget (with and without the `pq` edge) for
several `(\ell,M,N)` and confirms all three/four predicted cycle
lengths by direct construction with both cycle checkers.

## Part IV: interior return gives a topological `K_4`

Assume `x` is internal to `P_1`, `|P_1|=M`, `|P_2|=N`,
`d=d_{P_1}(p,x)`, `M-d=d_{P_1}(x,q)` (`1\le d\le M-1`), `|R|=\ell`.

### IV.0. `\Theta\cup R` is a topological `K_4` [PROVED]

Branch vertices `p,q,v,x`; six branch paths: `pv` (length 1, part of
`P_0`), `vq` (length 1, part of `P_0`), `px` (length `d`, part of
`P_1`), `xq` (length `M-d`, part of `P_1`), `pq` (length `N`, all of
`P_2`), `vx` (length `\ell`, `=R`). **Pairwise internal disjointness:**
`P_0`, `P_1`, `P_2` are pairwise disjoint except at shared theta-poles
(theta hypothesis); splitting `P_1` at `x` keeps its two halves disjoint
from each other and from `P_0,P_2` for the same reason; `R`'s internal
vertices avoid all of `V(\Theta)` entirely (I.2), so `R` is disjoint
from the interiors of all five other paths. **This is exactly the
definition of a topological `K_4`** (a `K_4`-subdivision) with the
stated branch-path lengths. ∎

### IV.1. The seven core cycles, exact lengths [PROVED]

A `K_4`-subdivision has exactly seven simple cycles: four triangles
(each omitting one branch vertex) and three Hamiltonian 4-cycles (each
omitting one of the three perfect matchings of `K_4`'s edge set).
Labelling edges `pv{=}1,\,vq{=}1,\,px{=}d,\,xq{=}M{-}d,\,pq{=}N,\,vx{=}\ell`:

| cycle (omits) | edges used | length |
|---|---|---|
| triangle, omits `x` | `pv,vq,pq` | `N+2` |
| triangle, omits `q` | `pv,vx,px` | `\ell+d+1` |
| triangle, omits `p` | `vq,vx,xq` | `\ell+(M-d)+1` |
| triangle, omits `v` | `pq,qx,xp` | `M+N` |
| 4-cycle, excludes `\{pq,vx\}` | `pv,vq,px,xq` | `M+2` |
| 4-cycle, excludes `\{vq,px\}` | `pv,vx,xq,pq` | `\ell+(M-d)+N+1` |
| 4-cycle, excludes `\{pv,xq\}` | `vq,vx,px,pq` | `\ell+d+N+1` |

**These are always seven *structurally* distinct simple cycles**
(different edge subsets), even when two happen to share a numeric
length for special `(\ell,d,M,N)` (e.g. `d=M-d`) — the task's requested
distinction between graph-structural and arithmetic duplication.
**By symmetry, `x` internal to `P_2` gives the identical table with
`M,N` (and `d`, measured now along `P_2`) relabelled.**

**Computational cross-check.** `check_topological_k4` builds the
subdivision explicitly for several `(\ell,d,M,N)`, independently
enumerates its **complete** simple-cycle set via networkx (not just the
seven predicted ones — confirming there are exactly seven, not fewer or
more), and matches every length against the table.

### IV.2. Substituting NPT branch lengths [PROVED, symbolic]

`P_0` (length 2) is fixed as the `v`-branch; `\{P_1,P_2\}=\{P_x,Q_{pq}\}`
in either order — `\{M,N\}=\{2^r-1,2^s\}`, both assignments checked
(not assumed equivalent, per Part II).

**Three of the seven formulas are already unconditionally safe, by
previously-proved lemmas — a direct reuse, not new arithmetic:**
- `N+2` (or `M+2}`, whichever slot holds `2^s`): **Lemma F**
  (`contraction_mixed_witness.md`) — never a power of two, `s\ge2`.
- `M+N=(2^r-1)+2^s=2^r+2^s-1`: **Lemma E** — never a power of two,
  `r,s\ge2`.
- The other of `\{M+2,N+2\}` (whichever slot holds `2^r-1`): `2^r-1+2=
  2^r+1`, odd for `r\ge1`, `\ge5` — never a power of two.

**The remaining four formulas are genuine, unresolved `(\ell,d)`-dependent
constraints** — assigning `M=2^r-1,N=2^s`:
\[
\ell+d+1\ne2^m,\qquad \ell+(2^r-1-d)+1=\ell+2^r-d\ne2^m,
\]
\[
\ell+(2^r-1-d)+2^s+1=\ell+2^r-d+2^s\ne2^m,\qquad
\ell+d+2^s+1\ne2^m.
\]
(The `M=2^s,N=2^r-1` assignment gives the structurally analogous four
conditions with `r,s`'s roles exchanged in the `d`-dependent terms —
recorded, not re-derived, by the same symmetry.)

**Theorem table (compact, as instructed — not merely a bounded numeric
search).**

| formula slot | value | status |
|---|---|---|
| triangle omit `x` | `N+2` (`=2^s+2`) | unconditionally safe (Lemma F) |
| triangle omit `v` | `M+N` (`=2^r+2^s-1`) | unconditionally safe (Lemma E) |
| 4-cycle excl. `\{pq,vx\}` | `M+2` (`=2^r+1`) | unconditionally safe (odd) |
| triangle omit `q` | `\ell+d+1` | open: excluded residues on `(\ell,d)` |
| triangle omit `p` | `\ell+2^r-d` | open: excluded residues on `(\ell,d)` |
| 4-cycle excl. `\{vq,px\}` | `\ell+2^r-d+2^s` | open: excluded residues |
| 4-cycle excl. `\{pv,xq\}` | `\ell+d+2^s+1` | open: excluded residues |

**No contradiction is forced by arithmetic alone** — as instructed, this
is not expected; the table above is the exact surviving parameter
system, three formulas permanently closed, four left as concrete,
checkable symbolic conditions on `(\ell,d)` for future work (Part VII
below revisits these once a second admissible path is available).

**Computational cross-check.** `check_npt_k4_substitution` substitutes
`\{M,N\}=\{2^r-1,2^s\}` (both assignments) for a range of `r,s`,
confirms the three closed formulas are power-of-two-free in every case,
and confirms the four open formulas' *arithmetic* matches the
substituted symbolic expressions exactly (not that they are safe —
they are not claimed to be).

## Part V: integrating the third-edge near-power witness

`e_v=vw` is a nontriangle edge (Type N: always; Type T: when `\Theta`'s
`P_0` uses `v`'s two triangle-edges, leaving `e_v` as `v`'s unique
external edge — the convention carried from `contraction_saturation.md`
VII.2). By the original near-power edge lemma (`contraction.md`), `e_v`
has a witness cycle `W_v`, `|W_v|=2^t+1`; removing `v` gives a path from
`w` to `p` or `q`, length `2^t-1`.

### V.1. Bridge itinerary [PROVED, first-excursion fact; relationship to `R` bounded, not settled]

Trace `W_v` from `v` along `e_v`, recording alternating theta-bridge
excursions and theta-arc traversals until reaching `p` or `q`.

**The first excursion lies in `B_v`, ending at some attachment of
`B_v` [PROVED].** `w\in C`, the component defining `B_v`. Any path
continuing from `w` while staying off `V(\Theta)` must remain inside
`C`: `C` is by definition a connected component of `G-V(\Theta)`, so no
edge leaves `C` for a *different* component of `G-V(\Theta)` without
first passing through `\Theta}` — the only two kinds of edges available
from a `C`-vertex are internal to `C` or directly to `\Theta}`. So the
walk cannot reach any other bridge before it first reaches `\Theta}`
again, and when it does, that landing vertex is (by definition) an
attachment of `B_v`. ∎

**Is `R` (Part I.2) necessarily an initial segment of some canonical
`W_v`? [Answered: not necessarily, only an inequality is established.]**
`R` and `W_v` are chosen by *different* canonicalization procedures over
*different* candidate sets (`R` minimizes length among all `B_v`-internal
`v`-to-*any-attachment* paths; `W_v` is whatever the near-power-cycle
minimality argument produces, canonicalized by exponent and cross-witness
overlap, `contraction_mixed_witness.md` III.2) — nothing forces them to
coincide as literal paths or even in length. **What does follow:**
`W_v`'s first excursion is itself one valid candidate in `R`'s own
minimization set (a `B_v`-internal `v`-to-some-attachment path), so by
`R`'s own minimality,
\[
\boxed{\ell=|R|\ \le\ (\text{length of }W_v\text{'s first excursion}).}
\]
This one-directional bound is the honest, fully justified relationship
— equality is not claimed.

**Computational cross-check.** `check_first_excursion` builds a
multi-component gadget (`B_v` plus a second, separate component `B'`)
and confirms directly that a path from `w` cannot reach `\Theta}` via
`B'` before first landing on a `B_v`-attachment vertex — validating the
component-separation argument mechanically.

### V.2. CB2 — the one-excursion target, tested [likely FALSE by direct structural analogy; no numeric-minimality proof either way]

**Claim tested:** *a canonical third-edge witness `W_v` can be chosen
with exactly one excursion outside `\Theta`.*

**Why this is the correct replacement for the disproved one-cell
conjecture, and why it is suspect for the same reason.**
`contraction_intersections.md` V.2 disproved the analogous "canonical
witnesses give one cell" claim precisely because minimizing overlap/
exponent criteria does not bound how many *distinct* vertices two
witnesses cross. The same gap applies here: `W_v`'s canonicalization
(shortest exponent, least cross-witness overlap) supplies **no
mechanism preventing** a shortest `w`-to-`\{p,q\}` route from legitimately
exiting `B_v`, crossing a theta arc, and continuing through a *second*,
separate bridge if that route is genuinely shorter than continuing
within `B_v}` alone or along theta arcs directly.

**Structural (not fully minimality-verified) witness that CB2 is not a
theorem.** A graph gadget with `B_v` attaching at theta-point `y_1}`
(not `p,q}` directly) and a **second**, disjoint component `B'`
attaching at `y_1` (or a nearby theta point reached from `y_1}` by a
short theta arc) and at a point close to `p`, provides a concrete,
valid, itinerary-respecting two-excursion path `w\to(\text{via }B_v)\to
y_1\to(\text{theta arc})\to(\text{via }B')\to p`. **`check_cb2_structural_instance`**
constructs this explicitly and confirms it is a genuine simple path
respecting the itinerary definition (first excursion in `B_v`, ending
at a `B_v`-attachment; a theta arc; a second excursion in a *different*
component `B'}`). **What is not established:** that this specific
two-excursion route is actually *shorter* than every single-excursion
alternative in the same gadget (which would be needed to certify it as
the *canonical* choice, not merely *a* valid one) — a full minimality
certificate is not constructed. **Honest status:** CB2 is not proved;
a structurally valid multi-excursion configuration is exhibited, but it
is not certified as the smallest possible or as forced by the canonical
choice specifically — matching the task's own weaker fallback ("classify
the minimum irreducible multi-excursion itinerary") only partially: the
itinerary shape (one excursion, arc, second excursion) is identified and
exhibited, its *canonical minimality* is not certified.

**What changes if `W_v` needs a second excursion.** The near-power
length `2^t-1` (the `w`-to-`\{p,q\}` path) would then decompose as
(first-excursion length) `+` (theta-arc length) `+` (second-excursion
length), rather than being wholly internal to `B_v` — meaning Part
III/IV's `\ell`-based arithmetic (which assumed the *return path* `R`
stays within `B_v`) does **not** directly bound `2^t-1`, since `W_v`'s
own path need not equal `R` end-to-end. This is exactly why V.1 only
established an inequality, not equality: multi-excursion is the
structural reason the gap can be strict.
