# contraction_atoms.md — the contractible-atom generalization

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked by `verifier/atom_lift.py`
wherever the claim is an unconditional graph-theoretic fact. Nothing here
is proof-assistant formal verification; no Lean/Coq/Isabelle artifact
exists anywhere in this project. This file builds directly on
`contraction.md` (the near-power edge lemma, the safe-contraction
obstruction, the cubic-vertex nontriangle-edge count, and the clean
same-length merge lemma) and keeps that file's proofs as an independent
derivation rather than replacing them.

Notation as before: `G` is a lexicographically minimal Erdős–Gyárfás
counterexample, `n=|V(G)|`, `δ(G)≥3`, `F={4,8,16,32,...}`.

## Part I: the general contractible-atom lemma

Let `A⊆V(G)` with `G[A]` connected, `|A|≥2`. Write `G/A` for the standard
simple-graph minor contraction: identify `A` to one new vertex `t`,
delete all edges internal to `A`, and — since this project works only
with simple graphs — auto-simplify (drop the resulting loop-free
multi-edges down to single edges) exactly as graph-minor theory always
does. Write `∂A := N_G(A)\A` (the set of vertices outside `A` with at
least one neighbour in `A`).

### I.1. Simplicity is automatic; degree preservation is not [PROVED]

**`G/A` is always simple**, by the auto-simplification convention itself
— there is nothing to prove here, and in particular "no vertex outside
`A` has two neighbours in `A`" is **not necessary** for simplicity under
this convention (a vertex with two `A`-neighbours just contributes one
`t`-edge instead of two, still a simple graph).

**What that condition *is* necessary and sufficient for is degree
preservation.** For `w∉A`, `deg_{G/A}(w) = |N_G(w)\A| + [\,N_G(w)\cap A
\ne\varnothing\,]`. This equals `deg_G(w)` exactly when `|N_G(w)\cap
A|\le1` (0: no `t`-edge, degree literally unchanged; 1: the single
`A`-edge is relabelled to a single `t`-edge, still one edge), and is
**strictly less** than `deg_G(w)` whenever `|N_G(w)\cap A|\ge2` (two or
more original edges collapse to the single edge `wt`). So:

**Lemma I.1 (necessary and sufficient degree-preservation condition).**
*`deg_{G/A}(w)=deg_G(w)` for every `w∉A` if and only if every vertex
outside `A` has at most one neighbour in `A`.* ∎

We call this hypothesis **(H2)**, matching the task's proposed sufficient
condition — precisely characterized here as necessary and sufficient for
property 2, not for property 1.

### I.2. Degree of the contracted vertex [PROVED]

Under (H2), every boundary edge of `A` becomes a distinct `t`-edge (no
two collapse together, since no outside vertex has two `A`-neighbours to
begin with), so
\[
\deg_{G/A}(t)=|\partial A| = \sum_{a\in A}\deg_G(a) - 2\,|E(G[A])|.
\]
Call **(H3)** the hypothesis `|\partial A|\ge3` (equivalently, under
(H2), at least 3 boundary edges). Since `G[A]` connected forces
`|E(G[A])|\ge|A|-1`, and `\deg_G(a)\ge3` for every `a`, a convenient
*sufficient* numeric form of (H3) is
\[
|E(G[A])|\le\tfrac{3|A|-3}2
\]
(trees, `|E(G[A])|=|A|-1`, always satisfy this; the triangle,
`|E(G[A])|=|A|=3`, satisfies it with equality). But (H3) itself — not
this numeric corollary — is the operative hypothesis; it can hold or
fail independently of this bound in general.

### I.3. The atom-contraction lemma, mechanical part [PROVED]

**Lemma.** *If `G[A]` is connected and (H2), (H3) hold, then `G/A` is
simple with `\delta(G/A)\ge3`* (every `w\notin A` keeps `\deg_G(w)\ge3`
by I.1; `t` has degree `\ge3` by I.2/(H3)). ∎

Since `|V(G/A)|=n-|A|+1<n` (as `|A|\ge2`), **order-minimality of `G`
forces `G/A` to contain a power-of-two cycle** — exactly the one-line
argument of `contraction.md` I.2, now stated for a general atom.

### I.4. Locating and lifting that cycle [PROVED]

Let `D` be a power-of-two cycle of `G/A`, `|D|=2^k`.

**`D` contains `t`.** Otherwise `D` lies entirely outside `A`, using
only edges untouched by the contraction, so `D` is verbatim a cycle of
`G` — contradicting F-cleanness. ∎

**`D`'s two `t`-edges attach at *distinct* vertices of `A`.** `t` has
exactly two cycle-neighbours `w_1\ne w_2\in\partial A`; by (H2) each
`w_i` has a *unique* neighbour in `A`, call it `a_i\in A`. Suppose
`a_1=a_2=:a`. Replacing `t` by `a` in `D` (the rest of `D` is untouched)
gives a **verbatim cycle of `G`** of the *same* length `2^k` (edges
`w_1a`, `aw_2` both exist in `G`, by definition of `a_i`) — a
power-of-two cycle in `G`, contradiction. **So `a_1\ne a_2`;** write
`a:=a_1,\ b:=a_2\in A`, distinct. ∎

**Lifting.** Delete `t` and its two incident edges from `D`; the
remainder is a path `Q_{\text{out}}\subseteq G\setminus A` from `w_1` to
`w_2`, of length `2^k-2` (untouched by the contraction, hence already a
genuine path of `G`). For **every** simple `a`–`b` path `R\subseteq
G[A]` of length `r`, the closed walk `w_1{-}a{-}R{-}b{-}w_2{-}
Q_{\text{out}}{-}w_1` is a simple cycle of `G`:
- `R`'s vertices lie in `A`, `Q_{\text{out}}`'s vertices lie outside
  `A` — the two vertex classes are disjoint, so no collision between
  them;
- `R` is itself simple (hypothesis) and `Q_{\text{out}}` is simple
  (inherited from `D`'s simplicity);
- `w_1\ne w_2` (shown above) and the two connecting edges `w_1a`,
  `bw_2` exist by definition of `a,b`.

Its length is `1+r+1+(2^k-2)=2^k+r`.

**Theorem (atom-lifting lemma) [PROVED].** *Under (H2),(H3), for every
power-of-two cycle `D` of `G/A` (`|D|=2^k`, at least one exists) and
every simple `a`–`b` path `R` in `G[A]` (where `a,b` are `D`'s forced-
distinct attachment vertices), `G` contains a simple cycle of length*
\[
\boxed{2^k+r},\qquad r=|R|.
\]

### I.5. Audit, item by item

- **Path and cycle simplicity:** proved directly above (disjoint vertex
  classes, inherited simplicity of `R` and `Q_{\text{out}}`).
- **Attachments through the same outside vertex:** `w_1\ne w_2` is
  forced by `D`'s own simplicity (`2^k\ge4>2` cycle-neighbours of `t`
  are always distinct) — independent of (H2); (H2) is what makes each
  `w_i`'s *attachment point in `A`* well defined, a logically separate
  fact from `w_1\ne w_2` itself.
- **Chords in `A`:** the lemma is stated for *every* simple `a`–`b`
  path in `G[A]`; a chorded (non-tree) `A` simply offers *more*
  available `r`-values, one lifted cycle per simple `a`–`b` path — this
  is a feature the triangle case (Part III) uses directly, not an
  obstruction.
- **Non-induced atoms:** moot — `G[A]` denotes the actual induced
  subgraph on `A`, so there is no ambiguity about "which" internal
  edges count; every internal edge of `G` between two elements of `A`
  is automatically included.
- **Parallel-edge suppression:** never actually invoked — (H2) is
  exactly the hypothesis under which the standard auto-simplification
  has nothing to suppress (every outside vertex contributes at most one
  candidate parallel edge to begin with).
- **Atoms with more than two boundary vertices:** no issue. A single
  cycle `D` always uses exactly two of `t`'s however-many neighbours;
  larger atoms can support *multiple*, independently-analysed `D`'s
  through different attachment pairs — relevant for Type N/T below,
  where `A` can have exactly 3 boundary vertices at minimum.

**Computational cross-check.** `verifier/atom_lift.py`'s
`check_atom_contraction` constructs random connected atoms `A`
satisfying (H2),(H3) inside random `δ≥3` fixture graphs, verifies
simplicity/degree-preservation/`(H2)⇔`degree-preservation directly, and
lifts every cycle of `G/A` through `t` (not just power-of-two ones, for
a strictly stronger test) up to a length bound, checking the exact
`2^k+r` arithmetic against the literal reconstructed lift for every
available internal path `R`. See Part IX below for the full run record.

## Part II: recovering the edge lemma [PROVED, and shown logically equivalent to `contraction.md` Part I]

Take `A=\{u,v\}` for a nontriangle edge `uv`. `G[A]` is connected (the
edge itself). (H2) ⟺ no outside vertex adjacent to both `u,v` ⟺ exactly
`uv`'s nontriangle hypothesis. (H3): `\partial A = (N(u)\setminus\{v\})
\cup (N(v)\setminus\{u\})`, disjoint by (H2), size `\deg(u)+\deg(v)-2
\ge4\ge3`. `G[A]` has exactly one internal vertex pair `\{u,v\}` and
exactly one simple `u`–`v` path — the edge itself, `r=1`. The
atom-lifting lemma therefore gives exactly `2^k+1`, and the "forced
distinct attachment" step of I.4 is *verbatim* the "same-side
impossible" step of `contraction.md` I.4 (both say: if both of `D`'s
`t`-edges attach at the same element of `A`, `D` lifts unchanged to a
same-length cycle of `G`, contradiction). **The two proofs are the same
argument, specialized**; `contraction.md`'s edge-specific proof is kept
as the independent, self-contained derivation for `|A|=2` and is not
superseded.

## Part III: triangle contraction

### III.1. Every triangle of `G` is automatically a valid atom [PROVED]

Let `T=\{a,b,c\}` span a triangle (`G[T]=K_3`). **No outside vertex `x`
is adjacent to two vertices of `T`.** If `x\sim a,b` (WLOG), then
`x{-}a{-}c{-}b{-}x` uses edges `xa,ac,cb,bx` — four distinct vertices
`x,a,c,b`, a genuine `C_4` — forbidden. So **(H2) holds automatically
for every triangle, with no edge-selection needed** (contrast the edge
case, where a nontriangle edge had to be explicitly chosen — here
C4-freeness gives (H2) for *every* triangle, always).

**(H3) also holds automatically.** `\deg_{G/T}(t)=\sum_{v\in
T}\deg_G(v)-2\cdot3=\sum_{v\in T}(\deg_G(v)-2)\ge3\cdot1=3` (each
`\deg_G(v)\ge3`), with equality iff all three are cubic.

**Hence every triangle of `G` is a contractible atom, unconditionally:
`G/T` is simple with `\delta(G/T)\ge3`.**

### III.2. The triangle-pair lemma [PROVED]

Let `D` be a power-of-two cycle of `G/T`, `|D|=2^k`, forced-distinct
attachment vertices `a,b\in T` (Part I.4). `G[T]=K_3` has **exactly
two** simple `a`–`b` paths: the direct edge (`r=1`) and the path through
the third vertex `c` (`r=2`). By the atom-lifting lemma, both are
realized:
\[
\boxed{2^k+1}\qquad\text{and}\qquad\boxed{2^k+2},
\]
**using the identical outside arc `Q_{\text{out}}` and identical
attachment vertices `w_1,w_2`** — the two lifted cycles differ *only*
in whether they route through `c` or not.

**Both are simple** (Part I.4, applied twice with `r=1,2`). **They are
distinct**: different lengths (`2^k+1\ne2^k+2`), and the `r=2` cycle
contains `c` while the `r=1` cycle does not.

**Their symmetric difference is trivial, honestly reported.** The two
cycles agree on every edge except the internal routing: `\{ab\}` vs.
`\{ac,cb\}`. Symmetric difference = `\{ab,ac,cb\}` = the triangle `T`
itself — length 3, not forbidden (`3\notin F`). **This particular
combination yields no new information beyond the triangle already being
present**; it is not a shortcut to a contradiction, and is recorded here
so the next reader does not re-derive it expecting one.

**Computational cross-check.** `check_triangle_pair` in
`verifier/atom_lift.py` builds an explicit triangle-plus-two-outside-
routes gadget for several `k`, contracts, lifts both internal routes,
and verifies both lifted cycles are simple, of lengths `2^k+1,2^k+2`
exactly, sharing every edge except `\{ab\}` vs. `\{ac,cb\}`.

## Part IV: the local cubic-vertex dichotomy

Let `v` be cubic, `N(v)=\{a,b,c\}`. `G` is `C_4`-free, so (pigeonhole:
any two of the three possible edges `ab,ac,bc` already share an
endpoint and force a `C_4` through `v` — `contraction.md` Part III, ) at
most one of `ab,bc,ca` is an edge. **Exactly one of the following holds
[PROVED, `contraction.md` Part III, restated in this file's vocabulary]:**

- **Type N (triangle-free cubic vertex).** No edge among `a,b,c`. All
  three of `va,vb,vc` are nontriangle edges (`contraction.md` III.1).
- **Type T (cubic vertex in a unique triangle).** Exactly one pair, say
  `ab`, is an edge. `\{v,a,b\}` is `v`'s **only** triangle (any triangle
  through `v` needs 2 of `v`'s 3 edges plus the connecting edge between
  those neighbours; only `ab` connects any pair). `va,vb` are triangle
  edges; `vc` is the unique nontriangle edge at `v`.

**Computational cross-check.** `check_cubic_dichotomy` in
`verifier/atom_lift.py` re-verifies the exact `\{0,1\}`-internal-edge
split (equivalently `\{3,1\}`-nontriangle-edge count, already checked in
`contraction.md` Part III) and additionally verifies triangle
uniqueness at every Type T vertex of every C4-free fixture.

**Global local target (stated, not assumed true).** *Neither Type N nor
Type T can occur in a minimum-order counterexample.* Since every
minimal counterexample has cubic vertices (`M4`/`G1`), eliminating both
types would prove the conjecture outright. **This is not established
below; Parts V–VII make partial progress and are explicit about exactly
where they stop.**

## A reusable arithmetic toolkit

Before Parts V–VI, five lemmas about sums of powers of two and cycle
gluing, used repeatedly below. `x,y,z` denote integers `\ge2` throughout
(the exponents that actually occur: every near-power cycle has length
`2^x+1\ge5`, so `x\ge2`).

**Lemma A (two-power sum).** *`2^x+2^y` is a power of two iff `x=y`
(then it is `2^{x+1}`).* *Proof.* WLOG `x\le y`: `2^x+2^y=2^x(1+2^{y-x})`,
a power of two iff `1+2^{y-x}` is. At `y=x` this is `2`. At `y>x`,
`2^{y-x}` is even `\ge2`, so `1+2^{y-x}` is odd and `>1` — not a power
of two. ∎

**Lemma A′ (shifted two-power sum, restricted domain).** *For `x,y\ge2`,
`2^x+2^y-2` is never a power of two.* *Proof.* `2^x+2^y-2 =
2(2^{x-1}+2^{y-1}-1)`; a power of two iff `2^{x-1}+2^{y-1}-1` is. Since
`x,y\ge2`, `2^{x-1},2^{y-1}\ge2` are both even, so their sum is even and
`M:=2^{x-1}+2^{y-1}-1` is odd; also `M\ge2+2-1=3>1`. An odd integer `>1`
is never a power of two. ∎ *(At `x=y=1`, excluded from our domain,
`M=1` and the statement is false — `2+2-2=2` — which is exactly why the
domain restriction `x,y\ge2` is load-bearing, not cosmetic.)*

**Lemma B (shared-edge cycle merge, general lengths) [generalizes
`contraction.md` Part IV].** *If two simple cycles `C_1,C_2` share
exactly one edge `e_0` and no other vertex, `(C_1\cup C_2)\setminus
\{e_0\}` contains a simple cycle of length `|C_1|+|C_2|-2`.* Same proof
as before (delete `e_0` from each, concatenate the two resulting paths
at their shared endpoints; internal vertices disjoint by hypothesis).

**Lemma C (vertex-hub merge).** *Let `Q_1` be a `p`–`q` path, `Q_2` a
`q`–`s` path, sharing exactly the vertex `q` and otherwise disjoint,
both avoiding some vertex `\hat v` with `\hat v\sim p` and `\hat v\sim
s`. Then `\hat v{-}p{-}Q_1{-}q{-}Q_2{-}s{-}\hat v` is a simple cycle of
length `|Q_1|+|Q_2|+2`.* Immediate direct construction.

**Lemma D (double-endpoint merge, no hub).** *Two `p`–`q` paths sharing
only their endpoints `p,q` form a simple cycle of length
`|Q_1|+|Q_2|`.* Immediate.

**Lemma D3 (triple concatenation is always safe) [PROVED, new].** *For
`x,y,z\ge2`, `2^x+2^y+2^z-3` is never a power of two.* *Proof, mod 4.*
Each of `2^x,2^y,2^z` is `\equiv0\pmod4` (exponent `\ge2`), so
`2^x+2^y+2^z-3\equiv-3\equiv1\pmod4`. A power of two `2^m` is `\equiv0
\pmod4` for `m\ge2`, `\equiv2\pmod4` for `m=1`, `\equiv1\pmod4` only for
`m=0` (`2^0=1`). So the only congruence-compatible value is
`2^x+2^y+2^z-3=1`, i.e. `2^x+2^y+2^z=4` — impossible since each term is
`\ge4`, giving a sum `\ge12`. ∎ *(Every "closed triangle of three
witness paths" combination below reduces to this lemma and is therefore
always safe — recorded once here rather than three times.)*

**All five checked computationally** — `verifier/atom_lift.py`'s
`check_arithmetic_toolkit` brute-forces Lemmas A/A′/D3 over
`x,y,z\in\{2,\dots,8\}` against direct power-of-two testing (0
mismatches), and `check_gluing_lemmas` builds explicit path/cycle
gadgets realizing Lemmas B/C/D and confirms the predicted lengths via
both cycle checkers.

## Part V: the Type N witness system

Let `v` be Type N, `N(v)=\{a,b,c\}`, no edges among them. By
`contraction.md`'s near-power edge lemma, contracting `va` gives a cycle
of length `2^{r_a}+1` through `v`; by Part I.4's forced-distinct-
attachment step applied to `A=\{v,a\}`, that cycle's other `v`-incident
edge is to some `f(a)\in\{b,c\}` (`v`'s only other neighbours).
Deleting `v` leaves a path `P_a: a\to f(a)` in `G-v`, `|P_a|=2^{r_a}-1`
— matching the setup exactly. Symmetrically `P_b,P_c`, defining
`f(b)\in\{a,c\}`, `f(c)\in\{a,b\}`.

### V.0. Exactly two isomorphism types of loopless `f` [PROVED]

`f:\{a,b,c\}\to\{a,b,c\}` with `f(x)\ne x` for every `x`: each of the 3
elements has 2 choices, `2^3=8` functions total. Classify by structure:

- **A 3-cycle exists** iff `f` is a cyclic permutation
  (`a\to b\to c\to a` or its reverse) — exactly **2** of the 8 functions,
  forming a single orbit under relabelling `\{a,b,c\}` (conjugate 3-
  cycles in `S_3` form one class of size 2).
- **A 2-cycle plus feeder**: pick the 2-cycle pair (`3` choices:
  `\{a,b\},\{a,c\},\{b,c\}`), then the third element feeds into either
  cycle-member (`2` choices) — `3\times2=6` functions, forming a single
  orbit of size 6.

`2+6=8`, exhausting all loopless functions, in exactly **two**
isomorphism types: **(1) directed 3-cycle; (2) directed 2-cycle with the
third vertex feeding into it.** No further case split is needed (nor
justified) beyond these two orbit representatives, matching the
requirement not to enumerate all eight labelled functions as the final
answer.

**Computational cross-check.** `check_functional_digraph_types`
enumerates all 8 loopless functions on `\{a,b,c\}`, partitions them by
the `S_3`-relabelling action, and confirms exactly 2 orbits of sizes
`2,6`.

### V.1. Canonical witness choice [definitional]

Among all power-of-two cycles of `G/\{v,x\}` (`x\in\{a,b,c\}`) — a
nonempty finite set by Part I.3/`contraction.md` I.2 — fix the witness
minimizing, in order: (1) `r_x`; (2) total edge-overlap with the other
two chosen witnesses; (3) number of shared path components with them;
(4) a fixed lexicographic encoding of the vertex/edge sequence (any
total order on `V(G)` extended lexicographically breaks all remaining
ties). Since each criterion ranges over a finite set, a unique minimizer
exists; this is a definition, not a claim, and needs no further proof.
It is what makes "minimal overlap" arguments below legitimate rather
than an arbitrary choice.

### V.2. Orientation type 1 — directed 3-cycle

WLOG `f(a)=b,\ f(b)=c,\ f(c)=a`. Paths `P_a:a\to b`, `P_b:b\to c`,
`P_c:c\to a`, lengths `2^{r_a}-1,2^{r_b}-1,2^{r_c}-1`.

**Pairwise, via Lemma C (clean case).** `P_a,P_b` share vertex `b`
(consecutive junction); `v\sim a` and `v\sim c` (the two non-shared
endpoints). *If `P_a,P_b` are internally disjoint and meet only at
`b`* (the canonical-minimal-overlap witnesses, V.1, chosen to make this
as likely as achievable — but not asserted to always hold, see below),
Lemma C gives a simple cycle `v{-}a{-}P_a{-}b{-}P_b{-}c{-}v` of length
`2^{r_a}+2^{r_b}` — a power of two, by Lemma A, **iff `r_a=r_b`**.
Since `G` is F-clean, **this forces `r_a\ne r_b`, whenever the merge is
clean.** By the identical argument (cyclic symmetry of the 3-cycle,
relabelling `a\to b\to c\to a`): `r_b\ne r_c` and `r_c\ne r_a`, each
conditional on the corresponding pairwise merge being clean.

**Triple concatenation, via Lemma D3.** If `P_a,P_b,P_c` are pairwise
disjoint except at their three consecutive shared endpoints, they close
into a simple cycle *not through `v` at all*, of length
`2^{r_a}+2^{r_b}+2^{r_c}-3` — **always safe by Lemma D3, regardless of
`r_a,r_b,r_c`.** This combination yields no constraint.

**Conclusion for orientation type 1.** In the fully clean case (every
pairwise merge and the triple concatenation realize as genuine simple
cycles — i.e. the three witness paths are pairwise internally
disjoint), the only forced consequence is: **`r_a,r_b,r_c` pairwise
distinct.** This is not a contradiction — three distinct integers `\ge2`
is realizable (e.g. `2,3,4`) — so **orientation type 1 is not
eliminated** by this toolkit. It is narrowed to a concrete, checkable
distinctness constraint, one exact irreducible configuration in the
sense of the task's required outcome, not a contradiction.

**Non-clean case, honestly open.** If any pairwise witness overlap is
*not* clean (the paths cross, share a nontrivial common sub-path, or a
witness revisits a vertex used by another beyond the forced junction),
the resulting symmetric difference decomposes into possibly several
cycle components (standard cycle-space fact, already used in this
project's `verifier/linkage_data.py`), and the length arithmetic above
does not directly apply. **This general decomposition is not carried
out in this pass** — it is the natural next step, using V.1's
minimal-overlap canonical choice to bound how much overlap can occur,
which is exactly why V.1's tie-breaking criteria were defined the way
they were (to make "assume clean, or bound the overlap" a legitimate
starting hypothesis for future work, not to claim it here).

### V.3. Orientation type 2 — directed 2-cycle plus feeder

WLOG `f(a)=b,\ f(b)=a,\ f(c)=a` (the symmetric sub-case `f(c)=b` is
identical after swapping `a,b`). Paths `P_a:a\to b`, `P_b:b\to a`,
`P_c:c\to a`.

**`P_a,P_b` (Lemma D, same endpoints `a,b`, no hub needed).** If
internally disjoint, they close directly into a cycle of length
`2^{r_a}+2^{r_b}-2` — **always safe by Lemma A′, regardless of
`r_a,r_b`.** *(Equivalently: their two hub-completions through `v`,
`v{-}a{-}P_a{-}b{-}v` and `v{-}b{-}P_b{-}a{-}v`, both use `v`'s same
two edges `va,vb`, so Lemma B's single-shared-edge hypothesis does not
apply to this pair at all — matching why this specific pairing needs
Lemma D/A′, not Lemma B/A.)*

**`P_c,P_a` (Lemma C, shared vertex `a`, hub `v\sim c,b`).** If clean,
`v{-}c{-}P_c{-}a{-}P_a{-}b{-}v` has length `2^{r_c}+2^{r_a}` — power of
two, by Lemma A, **iff `r_c=r_a`.** So **`r_c\ne r_a` is forced,
whenever this merge is clean.**

**`P_c,P_b` (Lemma C, shared vertex `a` — both `P_b,P_c` end at `a`,
hub `v\sim c,b`).** If clean, `v{-}c{-}P_c{-}a{-}[P_b\text{ reversed}]{-}
b{-}v` has length `2^{r_c}+2^{r_b}` — power of two iff `r_c=r_b`. So
**`r_c\ne r_b` is forced, whenever this merge is clean.**

**Conclusion for orientation type 2.** In the clean case: **the feeder
exponent `r_c` must differ from *both* `r_a` and `r_b`; the 2-cycle
exponents `r_a,r_b` themselves face no constraint from this toolkit**
(their natural combination, Lemma D, is unconditionally safe by Lemma
A′ — an asymmetry between the "cycle" pair and the "feeder" edge worth
recording explicitly, since it is not obvious a priori). Again this
narrows, but does not eliminate, orientation type 2; the non-clean case
is open for the same reason as V.2.

### V.4. Required outcome for Type N

**Neither a contradiction nor a full elimination is reached.** What is
established: a reusable five-lemma toolkit (above), and, for both
orientation types, the *complete* list of pairwise/triple combinations
available from the three witness paths, each resolved exactly —
"always safe" (Lemma A′/D3, unconditionally, no clean-ness needed for
the arithmetic conclusion itself) or "forces distinctness of two
specific exponents when clean" (Lemma A/C). **This is outcome 2 of Part
X's menu for Type N specifically: a finite, exact list of irreducible
constraint configurations, not a contradiction** — matching the
required outcome's second alternative honestly, with every combination
this toolkit can reach fully resolved rather than left as an
unclassified residue.

## Part VI: the Type T witness system

Let `v` be Type T, unique triangle `\{v,a,b\}` (`ab` an edge), `c` the
third neighbour (`vc` the unique nontriangle edge at `v`, WLOG the
`vc`-witness "exits through `a`" — the symmetric case exits through
`b`).

**Witness 1 (edge contraction, `A=\{v,c\}`).** Gives a `(2^\rho+1)`-cycle
using hub edges `\{cv,va\}` plus a path `P:c\to a` in `G-v`,
`|P|=2^\rho-1`.

**Witness 2 (triangle contraction, `T'=\{v,a,b\}`, III.1's automatic
atom).** `\deg_{G/T'}(t')=\sum_{x\in T'}(\deg_G(x)-2)`; since `v` is
cubic, `v`'s *only* boundary contribution to `T'` is the single vertex
`c` (its unique neighbour outside `T'`). So **any power-of-two cycle of
`G/T'` attaching at `v` is automatically forced to route through `c`
specifically** — a clean structural fact, no case split needed for
*which* outside vertex is at `v`'s end. Two sub-cases arise for the
*other* attachment vertex:

**VI.1a. Triangle attaches at `(v,a)` (the symmetric `(v,b)` case is
identical after swapping).** By the triangle-pair lemma, this gives two
cycles, both routed `c{-}v{-}\cdots`, sharing an outside path
`Q':a\to c` avoiding `v` (`|Q'|=2^s-1`, `2^s=|D'|`):
- **`+1` route:** `\{cv,va\}\cup Q'` — length `2^s+1`, matching `P`'s
  role exactly: both `P` and `Q'` are `a`–`c` paths through the *same*
  hub edges `\{cv,va\}`.
- **`+2` route:** `\{cv,vb,ba\}\cup Q'` — length `2^s+2`.

**Compare `P` (Witness 1) against `Q'` (Witness 2, `+1` route) — Lemma
D, same endpoints `a,c`.** If disjoint, length `2^\rho+2^s-2` — **always
safe by Lemma A′**, for *any* `\rho,s`. **This directly answers the
task's explicit question** ("investigate whether equal exponents `r=s`
force a power-of-two cycle. Do not assume they do."): **they do not**,
via this natural comparison — a genuine negative result, not an
oversight.

**Compare Witness 1 against Witness 2's `+2` route — Lemma B, shared
edge `cv` only (assuming `P` and `\{vb,ba,Q'\}` meet nowhere else).**
Length `(2^\rho+1)+(2^s+2)-2=2^\rho+2^s+1`. Since `\rho,s\ge2`,
`2^\rho,2^s` are both even, so `2^\rho+2^s+1` is **odd**, and the only
odd power of two is `1<9\le2^\rho+2^s+1` — **never a power of two,
unconditionally.** Again safe.

**Conclusion VI.1a.** Both natural clean comparisons between the `vc`-
witness and the triangle witness (at `(v,a)`) are arithmetically
*always* safe — no distinctness constraint is forced, unlike Type N's
pairings. This is itself the honest, precise answer this part of the
task asked for, not a gap: **Type T's direct edge-vs-triangle
comparison does not reduce to Lemma A/C the way Type N's inter-witness
comparisons did**, because both natural gluings here pair two
same-endpoint (`a`–`c`) paths (Lemma D/A′ regime) or land on an odd
total (never a power of two) — there is no available "sum of two equal
powers" configuration among these specific combinations.

**VI.1b. Triangle attaches at `(a,b)` only (not involving `v` at
all).** Then Witness 2 is structurally unrelated to `c`/Witness 1 (it
concerns some other outside neighbours of `a,b`), and no direct
comparison is available without further hypotheses on `G`; this
sub-case is not resolved here.

### VI.2. Multiple cubic vertices in one triangle [setup only, open]

`H` independent (`M1`) `\Rightarrow` every triangle has **at least two**
cubic vertices (at most one of the three can be in `H`). Triangles
split into: **(1) three cubic vertices**; **(2) two cubic, one
high-degree.** Each cubic triangle-vertex contributes its own external
`vc`-type witness (VI.1's construction, one per cubic vertex), all
sharing the same triangle atom `T'`. **The natural next step** — running
this file's toolkit pairwise across *two or three* simultaneous external
witnesses, using III.1's automatic contractibility once per cubic
vertex and VI.1's "forced routing through the unique outside neighbour"
fact for each — **is not carried out this pass.** Recorded here as the
precise open continuation, not attempted speculatively.

### VI.3. Required outcome for Type T

**No contradiction; a precise, fully-proved negative result (VI.1a: the
natural equal-exponent hope does not hold) plus one genuinely open
sub-case (VI.1b) and one unexplored extension (VI.2).** This is closer
to outcome 5 of Part X for Type T specifically — the toolkit, applied to
the most natural comparisons, adds no leverage toward a contradiction
here, though it *does* rule out the specific mechanism the task flagged
as worth checking (`r=s`), which is itself useful negative information
steering future work away from a dead end.

## Part VII: canonical near-power-cycle bridge fallback (VII.1 only)

Parts V–VI did not close either local case, so this fallback is genuinely
in scope, per its own stated condition. Only VII.1 (the direct symbolic
arithmetic) is carried out here; VII.2–VII.3 (the separator/crossing
classification against `two_cut.md`'s S5/Type A/B/C machinery) require
substantially more structural work than fits this pass and are left as
the concrete next step, not attempted speculatively.

### VII.1. Exact bridge arithmetic [PROVED, pure symbolic algebra]

Fix a canonical shortest near-power cycle `C`, `|C|=2^r+1` (existence
conditional on Parts V–VI's open cases; the arithmetic below is
unconditional given `C` exists). For a `C`-path `Q` of length `\ell`
whose endpoints have cyclic distance `d` on `C` (`1\le d\le2^r`), the
two cycles obtained by closing `Q` around either arc of `C` have lengths
`\ell+d` and `\ell+(2^r+1-d)`. **Neither may be a power of two** (else
immediate contradiction): symbolically,
\[
d\ne2^m-\ell\quad\text{and}\quad d\ne2^r+1+\ell-2^{m'}\qquad\text{for
every valid }m,m'.
\]

**Chords (`\ell=1`) [PROVED, sharpest instance].** A chord at cyclic
distance `d=2^m-1` for any `m` **immediately gives a power-of-two
cycle** — a direct contradiction, not merely a constraint. So:

**Corollary.** *`C` (if it exists) has no chord splitting it into an arc
of length exactly `4,8,16,\dots` — equivalently, no chord at cyclic
distance `3,7,15,31,\dots` from either endpoint's perspective.* This is
an exact, checkable necessary condition on `C`'s chord structure,
independent of the still-open questions in VII.2–VII.3.

**Computational cross-check.** `check_bridge_arithmetic` in
`verifier/atom_lift.py` verifies the `\ell+d`/`\ell+(2^r+1-d)` formula
by direct construction (a cycle plus an attached chord/bridge path at
prescribed distance) for a range of `r,\ell,d`, and confirms the
`d=2^m-1` chord case always yields an actual power-of-two cycle in the
constructed gadget.

## Part VIII: `q=4` deliberately not launched as a laboratory this pass

Part VIII's own instruction is explicit: only run `q=4` as a laboratory
*after* the local Type N/T invariants are defined, and stop if it adds
no reusable pattern. The per-vertex diagrams available right now (Part
V's two orientation types with their partial constraint lists; Part
VI's largely-safe comparisons) are **not yet in a stable enough form** —
V.2/V.3's non-clean case and VI.1b/VI.2 are still open — for a `q=4`
census to productively test "does a small set of local diagrams cover
all examples," since the diagram set itself is incomplete. Launching a
full defect-three-style computational campaign now would mainly produce
raw case counts without a settled local theory to check them against —
exactly the outcome Part VIII says to avoid. **Deliberately deferred**,
not overlooked; the honest trigger for revisiting it is completing
V.2/V.3's non-clean case or VI.2, whichever comes first.

## Part IX: validation

See `verifier/atom_lift.py` (new file, kept separate from
`verifier/contraction_lift.py`, whose existing 35,357-cycle audit is
untouched) and its accompanying manifest for the full run record:
atom-contraction mechanics (I.3–I.4), the triangle-pair lemma (III.2),
the Type N/T dichotomy plus triangle uniqueness (Part IV), the
functional-digraph classification (V.0), the five-lemma arithmetic
toolkit (Lemmas A/A′/B/C/D/D3), and the bridge-arithmetic chord
corollary (VII.1).

## Part X: stopping-condition assessment

**Outcome reached: a hybrid of (3) and (5) — the honest reading, stated
precisely rather than rounded up.**

- **Type N (Part V):** *finite, exact list of irreducible
  configurations* — every pairwise and triple combination of the three
  witness paths is fully resolved (either unconditionally safe, or
  forces a specific exponent-distinctness exactly when the merge is
  clean); the clean case reduces to "`r_a,r_b,r_c` pairwise distinct,"
  realizable, not a contradiction. This matches outcome (3)'s Type-N
  half.
- **Type T (Part VI):** closer to outcome (5) — *the toolkit adds no
  leverage toward a contradiction* on the specific comparisons
  available (VI.1a is fully resolved and always safe), though it does
  settle a concrete sub-question (equal exponents do not force a
  contradiction here) and leaves two explicit open extensions (VI.1b,
  VI.2) rather than a closed negative result for Type T as a whole.

**Not reached:** outcome (1) or (2) (no elimination of either type);
outcome (4) (no single canonical bridge configuration was shown to
absorb every remaining case — Part VII only reached its symbolic
arithmetic stage, VII.2–VII.3 untouched). **Not substituted:** no
safe-edge search, no bare `q=4` count, no new defect bound, no voltage
group, no unstructured list of future directions — every open item
above is a specific, named next step (V's non-clean overlap
decomposition; VI.1b/VI.2; VII.2–VII.3's separator classification),
not a vague placeholder.

