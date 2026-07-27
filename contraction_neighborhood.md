# contraction_neighborhood.md — closed-neighborhood contraction at a cubic vertex

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. This file builds on `contraction_atoms.md` (the general
atom-lifting lemma, Type N/T dichotomy, triangle-pair lemma) and keeps
those proofs as independent derivations. Throughout: `G` is a
lexicographically minimal Erdős–Gyárfás counterexample, `F={4,8,16,...}`.

## Part I: closed-neighborhood contraction, `A=N[v]`

Let `v` be cubic, `N(v)=\{a,b,c\}`, `A=N[v]=\{v,a,b,c\}`.

### I.1. Boundary injectivity, and why `v` itself is never a boundary attachment [PROVED]

**No outside vertex is adjacent to `v`.** `v`'s entire neighbourhood
`\{a,b,c\}` already lies in `A`, so `v` has no edge leaving `A` at all —
`v` contributes **zero** boundary vertices.

**No outside vertex has two neighbours in `A`.** The only way this could
happen (given the above) is an outside `x` adjacent to two of
`\{a,b,c\}`, say `a,b`. Then `x{-}a{-}v{-}b{-}x` is a `C_4` (edges
`xa,av,vb,bx`) — forbidden. So **(H2) holds automatically for `A=N[v]`,
exactly as it did for a bare triangle** (`contraction_atoms.md` III.1) —
no selection needed, C4-freeness alone gives it for every cubic vertex.

**Consequence (Lemma I.1 of `contraction_atoms.md`, applied here).**
Every outside vertex keeps its exact degree under contraction;
simplicity is automatic under the standard minor-contraction convention
used throughout this project (never re-derived per atom).

### I.2. The contracted degree, by local type [PROVED]

`\deg_{G/A}(t)=\sum_{x\in A}\deg_G(x)-2\,|E(G[A])|` (Part I.2 of
`contraction_atoms.md`, since (H2) holds). `G[A]` always contains the
three spokes `va,vb,vc`; it additionally contains `ab` iff `v` is Type
T (no edge among `a,b,c` iff Type N).

**Type N.** `|E(G[A])|=3`. Each of `a,b,c` has exactly one `A`-neighbour
(`v` — no edges among `a,b,c`, none of them adjacent to any other
element of `A`), so its remaining `\deg_G(x)-1\ge2` edges are **all**
boundary edges. `\deg_{G/A}(t)=(\deg(a)-1)+(\deg(b)-1)+(\deg(c)-1)\ge
2+2+2`:
\[
\boxed{\deg_{G/A}(t)\ge6}\qquad(\text{Type N}).
\]

**Type T** (`ab\in E(G)`, WLOG). `|E(G[A])|=4`. `a`'s `A`-neighbours are
`v,b` (2), leaving `\deg(a)-2\ge1` boundary edges; symmetrically `b`.
`c`'s only `A`-neighbour is `v` (Type T: `ac,bc\notin E(G)`), leaving
`\deg(c)-1\ge2` boundary edges.
\[
\deg_{G/A}(t)=(\deg(a)-2)+(\deg(b)-2)+(\deg(c)-1)\ge1+1+2,
\qquad
\boxed{\deg_{G/A}(t)\ge4}\qquad(\text{Type T}).
\]

**Either way `\delta(G/A)\ge3`** — outside vertices by I.1, `t` by the
bounds above (both `\ge3`). `A=N[v]` is therefore always a valid atom
((H2),(H3) automatic), for *every* cubic vertex regardless of local
type — the same automatic-contractibility pattern as the triangle atom,
now for a strictly larger atom.

### I.3. Forced-distinct attachment, restricted to `\{a,b,c\}` [PROVED]

`|V(G/A)|<|V(G)|`, so order-minimality forces a power-of-two cycle `D`
in `G/A` (`contraction_atoms.md` I.3); `D` contains `t` (else verbatim
cycle of `G`, I.4). `D`'s two `t`-edges attach at elements of `A` — but
by I.1, **`v` has no boundary edges at all**, so neither attachment can
be `v`: both lie in `\{a,b,c\}`, not merely by convention but because no
outside vertex's unique `A`-attachment can possibly be `v`. If both
attach at the same `p\in\{a,b,c\}`, replacing `t` by `p` reproduces a
same-length cycle of `G` — contradiction (`contraction_atoms.md` I.4,
verbatim). **So the two attachment vertices are distinct
`p,q\in\{a,b,c\}`.**

### I.4. The cubic power-path lemma, CN1 [PROVED]

Write `|D|=2^k` (`k\ge2`, since power-of-two cycles have length `\ge4`).
Removing `t` from `D` leaves the outside arc `Q_{\text{out}}` from `w_1`
to `w_2` (`|Q_{\text{out}}|=2^k-2`, untouched by the contraction — a
genuine path of `G`, entirely outside `A`, in particular avoiding `v`).
Adding back the two original attachment edges `w_1p`, `qw_2` gives a
path
\[
p{-}w_1{-}Q_{\text{out}}{-}w_2{-}q
\]
in `G`, of length `1+(2^k-2)+1=2^k`. **This path is simple and lies
entirely in `G-v`:** `p\ne q` (I.3); `p,q\notin Q_{\text{out}}`
(`Q_{\text{out}}\subseteq V(G)\setminus A`, while `p,q\in A`); `w_1\ne
w_2` (forced by `D`'s own simplicity, `2^k\ge4>2`); and `v\notin
\{p,q\}\cup Q_{\text{out}}` (`v\ne p,q` since `p,q\in\{a,b,c\}`; `v\notin
Q_{\text{out}}` since `v\in A`).

**CN1 (cubic power-path lemma) [PROVED].** *For every cubic vertex `v`,
some two neighbours `p,q\in N(v)` are joined in `G-v` by a simple path
of length `2^k`, `k\ge2`.*

**Corollary (via the closure `p{-}v{-}q`) [PROVED].** `p{-}v{-}q` is
itself a simple path of length 2 (both edges exist, `v\notin\{p,q\}`),
sharing with the power path **only** its endpoints `p,q` (the power
path avoids `v` entirely, by construction). By Lemma D
(`contraction_atoms.md`), the two combine into a genuine simple cycle
of `G`:
\[
\boxed{\text{every cubic vertex } v \text{ lies on a simple cycle of
length } 2^k+2.}
\]

*(This corollary is exactly the general atom-lifting lemma applied with
`r=2`, using the internal path `p{-}v{-}q\subseteq G[A]` — CN1 itself is
the `r=0` "raw" content before that closure; both are recorded since
CN1's `G-v` path form is what Parts III–VII below actually manipulate.)*

**Audit.**
- *Path simplicity:* shown in full above (five pairwise-distinctness
  facts, not asserted).
- *Cycle simplicity:* the closure adds only `v`, which is disjoint from
  every other vertex of the power path by construction.
- *No hidden case at `k=2` itself:* `2^k=4` is the minimum power-of-two
  cycle length, giving the shortest possible power path (`|D|=4`,
  `Q_{\text{out}}` length `2`); nothing in the proof needs `k\ge3`.

**Computational cross-check.** `verifier/neighborhood_lift.py`'s
`check_cn1` contracts `A=N[v]` for every cubic vertex of every fixture
graph, verifies (H2)/(H3)/`\delta(G/A)\ge3` directly, confirms every
`t`-attachment lies in `\{a,b,c\}` (never `v`), lifts every cycle of
`G/A` through `t` (not just power-of-two ones) up to a length bound, and
checks the exact `2^k`/`2^k+2` arithmetic of CN1 and its corollary
against the literal reconstructed path/cycle. Run separately from
`contraction_lift.py`'s and `atom_lift.py`'s existing audits (neither
touched). See Part IX for the full run record.

## Part II: additional Type T offsets from `N[v]`

Let `v` be Type T, `ab\in E(G)` the unique edge among `\{a,b,c\}`.
`G[A]` (`A=N[v]`) is the triangle `\{v,a,b\}` plus the pendant edge `vc`
— **`v` is a cut vertex of `G[A]` separating `c` from `\{a,b\}`** (`c`'s
only `A`-neighbour is `v`).

### II.1. Enumerating internal paths per attachment pair [PROVED]

**Pair `(a,b)`.** Simple `a`–`b` paths inside `G[A]`: the direct edge
(`r=1`), and `a{-}v{-}b` (`r=2`) — no third option (any path
through `c` would need to leave `c` back through `v`, revisiting `v`,
impossible in a simple path). **Identical to the internal-path set of
the bare triangle `\{v,a,b\}`** (`contraction_atoms.md` III.2) — `c`'s
presence in the larger atom adds nothing here. By the atom-lifting
lemma:
\[
\boxed{2^k+1,\quad2^k+2}\qquad(\text{pair }(a,b)).
\]

**Pair `(a,c)`** (symmetric for `(b,c)`, swap `a,b`). Since `v` cuts
`G[A]` between `c` and `\{a,b\}`, every `a`–`c` path must pass through
`v`. From `v`, `a` is reached directly (edge `va`) or via `b`
(`v{-}b{-}a`) — exactly two routes, giving `a`–`c` paths `c{-}v{-}a`
(`r=2`) and `c{-}v{-}b{-}a` (`r=3`), no others. By the atom-lifting
lemma:
\[
\boxed{2^k+2,\quad2^k+3}\qquad(\text{pair }(a,c)\text{ or }(b,c)).
\]

**Conclusion.** *`N[v]`-contraction at a Type T vertex forces one of two
paired-offset systems, depending only on which pair `D` happens to
attach at:* `\{2^k+1,2^k+2\}` (pair `(a,b)`) *or* `\{2^k+2,2^k+3\}`
(pair `(a,c)`/`(b,c)`).

**Computational cross-check.** `check_type_T_offsets` builds explicit
gadgets for each attachment pair and confirms exactly these two path
sets and cycle-length pairs, for several `k`.

### II.2. Relation to the independent triangle-contraction witness [PROVED — exact structural relationship, not assumed]

**The pair-`(a,b)` case of `N[v]`-contraction is literally the same
internal-path content as the triangle-contraction `\{v,a,b\}`'s
`(a,b)`-attachment case** (II.1, noted above) — `N[v]` is not offering
new information there.

**`(a,c)`/`(b,c)` attachment is where `N[v]` genuinely exceeds the
triangle atom**, since `c\notin\{v,a,b\}` — the bare triangle atom
cannot produce a `c`-involving attachment at all (`c` is not even a
vertex of that atom).

**A clean compositional fact.** `A=N[v]=\{v,a,b,c\}` decomposes as
`T'\cup\{c\}` where `T'=\{v,a,b\}` is the triangle. In `G/T'`, the
vertex `t'` and `c` are joined by exactly one edge (`c`'s unique
`T'`-neighbour, `v`, becomes `t'`); one checks directly that
**`G/A=(G/T')/(t'c)`** — closed-neighbourhood contraction is exactly
triangle contraction followed by contracting the resulting `t'c` edge
of the quotient. This is recorded as a structural remark, not used
below to force a relationship between the two witnesses' exponents.

**Do the two atoms use compatible outside attachment pairs, forced?
[Answered precisely: no, not in general.]** A power-of-two cycle `D'`
of `G/T'` and a power-of-two cycle `D` of `G/A` are found independently
(via order-minimality applied to two *different* quotient graphs, of
different orders); nothing forces `D` and `D'` to be "the same" cycle
under the compositional relationship above, or forces their exponents
`t,s` to coincide, **even when both happen to attach at `(a,b)`** (the
one case where the internal-path *content* genuinely agrees — content
agreement is not witness agreement). **This is stated as the honest
answer, not assumed either way**, exactly as instructed. Any future
argument forcing `D=D'` (e.g. via a canonical-witness minimality
argument, `contraction_atoms.md` V.1's style) would need its own proof;
none is given here.

**Computational cross-check.** `check_triangle_vs_neighborhood` builds
a single gadget graph containing both a bare triangle and its
closed-neighbourhood extension, contracts each independently, and
confirms the `(a,b)`-pair internal-path sets coincide exactly while the
`(a,c)` set is unavailable to the triangle-only contraction.
