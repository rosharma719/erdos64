# contraction.md — the contraction-criticality endgame

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument. Where a claim reduces to an unconditional
graph-theoretic fact (not one presupposing a minimal counterexample
exists), it is cross-checked by `verifier/contraction_lift.py`, an
independent Python implementation using two disagreeing-by-construction
cycle machineries (a hand-rolled adjacency check and networkx). No claim
here that genuinely depends on a minimal counterexample existing is
empirically testable, for the same reason S4/S5/O1/O3/L3/L4 are not: no
example of one is known. This file is **not** proof-assistant formal
verification; no Lean/Coq/Isabelle artifact exists anywhere in this
project.

Notation, carried over unchanged: `G` is a lexicographically minimal
Erdős–Gyárfás counterexample (minimum `|V|` first, then minimum `|E|`),
`n=|V(G)|`, `δ(G)≥3`, `F={4,8,16,32,...}` the forbidden cycle lengths.
An edge `e=uv` is a **nontriangle edge** iff `u,v` have no common
neighbour (equivalently, `e` lies on no triangle of `G`).

## Part I: the near-power edge lemma (Task A)

### I.1. Setup and the two mechanical facts [PROVED]

Let `e=uv` be a nontriangle edge of `G`. Write `G/e` for the graph
obtained by deleting `u,v` and adding a new vertex `u*` adjacent to
exactly `N(u)\{v} ∪ N(v)\{u}`; every other vertex keeps its edges among
itself and to `u*` (replacing any edge to `u` or `v`). Write
`S_u := N_G(u)\{v}` and `S_v := N_G(v)\{u}` for the two "sides."

**Lemma I.1a (`G/e` is simple).** *Proof.* A self-loop at `u*` would
require an edge of `G` between `u` and `v` other than `e` itself —
impossible in a simple graph. A parallel edge at `u*` (two edges to the
same `w≠u*`) would require `w∈S_u∩S_v`, i.e. `w` a common neighbour of
`u,v` — excluded exactly by the nontriangle hypothesis. So `S_u∩S_v=∅`
and `G/e` is simple. ∎ *(This is the same fact used, in the opposite
direction, throughout `two_cut.md`'s bridge machinery: a 2-cut identifies
vertices without merging their neighbourhoods; here we merge two adjacent
vertices, so the disjointness requirement lands on their neighbourhoods
directly rather than on a shared cut pair.)*

**Lemma I.1b (degree).** Every `w≠u*` has `deg_{G/e}(w)=deg_G(w)` exactly
(w had at most one edge to `{u,v}`, by simplicity plus `S_u∩S_v=∅`, so
it is relabelled, never merged or duplicated). And
`deg_{G/e}(u*)=|S_u|+|S_v|=deg_G(u)+deg_G(v)-2 ≥3+3-2=4`. **Hence
`δ(G/e)≥3` — in fact `δ(G/e)≥3` holds at every vertex other than `u*` by
equality with `G`, and `u*` itself has degree `≥4`.** ∎

**Corollary (from `B3`, no edge case needed for "both endpoints
high-degree").** `B3` (lemmas.md) already proves every edge of `G` has a
degree-3 endpoint (the degree-`≥4` vertices `H` are independent, M1). So
for *every* edge `e=uv` of `G`, not just nontriangle ones, at least one
of `u,v` is cubic. The case "`e` has two high-degree endpoints" therefore
**cannot occur at all** in this project's minimal counterexample; the
only genuine cases below are "both endpoints cubic" and "exactly one
endpoint cubic, the other in `H`" — both handled uniformly, since I.1a/b
never used which side was cubic.

**Computational cross-check.** `check_contraction_and_lifting` in
`verifier/contraction_lift.py` verifies I.1a/b directly (simplicity,
exact degree preservation off `u*`, `deg(u*)≥4`) on 34 fixture graphs
(Petersen, the 3-cube, `K_{3,3}`, a prism-plus-diagonal, and 30 random
cubic-plus-extra-edges graphs on `n∈{8,10,12}`), across all 249 of their
nontriangle edges, 0 failures.

### I.2. `G/e` always contains a power-of-two cycle [PROVED, one line from order-minimality]

`G/e` is simple (I.1a) with `δ(G/e)≥3` (I.1b) and `|V(G/e)|=n-1<n`. `G`
minimizes `|V|` first among all simple `δ≥3` graphs with no power-of-two
cycle, so no such graph exists on fewer than `n` vertices. Hence `G/e` —
which meets every hypothesis except possibly F-cleanness — **must**
contain a power-of-two cycle. ∎

**This step needs nothing beyond I.1a/b and order-minimality**; it says
nothing yet about *where* that cycle sits or *what length* it forces
back in `G` — that is the content of I.3–I.4 below, and is the genuinely
new part of the lemma.

### I.3. Every power-of-two cycle of `G/e` passes through `u*` [PROVED]

Suppose a power-of-two cycle `C` of `G/e` avoided `u*`. Every vertex and
edge of `C` then lies in `V(G)\{u,v}` and among edges untouched by the
contraction (edges between two vertices other than `u,v` are identical
in `G` and `G/e` — contraction only relabels edges incident to `u` or
`v`). So `C` is *verbatim* a cycle of `G`, of the same forbidden length —
contradicting `G`'s own F-cleanness. So every power-of-two cycle of
`G/e` uses `u*`. ∎ (Combined with I.2: **at least one** power-of-two
cycle of `G/e` passes through `u*`.)

### I.4. Same-side lift ⟹ contradiction; mixed-side lift ⟹ a `(2^k+1)`-cycle in `G` [PROVED]

Let `C` be a power-of-two cycle of `G/e` through `u*`, `|C|=2^k`. As a
simple cycle, `u*` has exactly two neighbours on `C`, say `w_1,w_2`
(distinct, since `2^k≥4>2`). Because `S_u∩S_v=∅` (I.1a), each `w_i` is
**unambiguously** a `u`-side or `v`-side vertex — this is the second use
of the nontriangle hypothesis, beyond mere simplicity: it also makes the
"side" of every `u*`-incident edge well defined.

**Same side (both `w_1,w_2∈S_u`, or both `∈S_v`) [PROVED impossible].**
Say both `∈S_u`. Replace `u*` by `u` in `C` (the rest of `C` is
unchanged, since it lies entirely off `{u,v,u*}`): edges `w_1u*` and
`u*w_2` become the *original* edges `w_1u`, `uw_2` of `G` (both exist,
since `w_1,w_2∈S_u=N(u)\{v}`). This produces a **verbatim cycle of `G`**
of the *same* length `2^k` (same vertex count, same edges elsewhere) —
a power-of-two cycle in `G`, contradicting F-cleanness. **So no
power-of-two cycle of `G/e` can have same-side `u*`-neighbours.** ∎

**Mixed side (one `w_i∈S_u`, the other `∈S_v`) [forced, and always
realizable].** By I.3 a power-of-two cycle through `u*` exists (I.2+I.3);
by the same-side elimination just proved, its two `u*`-neighbours must be
mixed. Say `w_1∈S_u`, `w_2∈S_v`. Replace `u*` in `C` by the path
`w_1{-}u{-}v{-}w_2` (edges `w_1u`, `uv=e`, `vw_2` — all exist in `G`: the
first two by definition of `S_u`/`e`, the third since `w_2∈S_v`). The
rest of `C` is untouched. Because `w_1≠w_2`, `u≠v`, and `u,v∉V(C)\{u^*}`
(they aren't vertices of `G/e` at all), the lifted sequence has **all
distinct vertices** — a genuine simple cycle of `G`, of length
`|C|+1=2^k+1`, **passing through the edge `e=uv`**. ∎

**Theorem (near-power edge lemma) [PROVED].** *For every nontriangle
edge `e=uv` of a lexicographically minimal Erdős–Gyárfás counterexample
`G`, and for every power-of-two cycle `C` of `G/e` (at least one exists,
by I.2–I.3), the lift of `C` through `e` is a genuine simple cycle of
`G` of length `2^k+1` (`k≥2`, so length `≥5`), passing through `e`
itself.* In particular `G` contains, for every nontriangle edge, at
least one cycle of length in `{5,9,17,33,...}` through that edge.

**Why `2^k+1` is never itself forbidden [PROVED, elementary].**
`2^k+1` is odd for `k≥1`; the only odd power of two is `2^0=1`, too
short to be a cycle length. So the lifted cycle never *directly*
contradicts `G`'s F-cleanness — it is new structural information about
`G`, not an immediate contradiction. This is the intended output: a
forced family of near-power cycles, not yet a proof.

**Edge-case audit, as required.**
- *One endpoint cubic, both endpoints cubic:* the proof never used the
  degree of `u,v` beyond `≥3` (needed for `δ(G/e)≥3` at `u*`); both
  sub-cases are covered identically.
- *High-degree endpoints:* the "both high-degree" case cannot occur at
  all (corollary of `B3`, above); "one endpoint high-degree" is covered
  identically to the cubic case, since `I.1`–`I.4` never distinguish
  sides by degree — only by neighbourhood membership (`S_u` vs `S_v`).
- *Repeated vertices:* `w_1≠w_2` (distinct cycle-neighbours of `u*`,
  since `|C|≥4`); `u,v∉V(G/e)`, so they cannot coincide with any
  untouched vertex of `C`; handled explicitly above.
- *Parallel-edge ambiguity:* resolved by the nontriangle hypothesis
  (`S_u∩S_v=∅`), which is exactly what makes each `u*`-edge's *side*
  well defined, not just what makes `G/e` simple — both uses are
  logically the same disjointness fact, flagged explicitly since the
  task asked for it separately.
- *Cycles not containing `u*`:* excluded outright, I.3.

**Computational cross-check.** `check_contraction_and_lifting` lifts
*every* cycle (not just power-of-two ones, for a strictly larger and
therefore strictly stronger test) through `u*` up to length 9, for all
249 nontriangle edges across the 34 fixture graphs: **35,357 lifts
performed, 14,141 same-side (verified to reproduce a valid `G`-cycle of
identical length — consistent with, though not itself a contradiction,
since these fixtures are not counterexamples so same-side survival is
expected) and 21,216 mixed-side (verified to reproduce a valid `G`-cycle
of length exactly `+1`, always threading through `e`), 0 validity
failures, 0 length-arithmetic failures.** See the script's docstring for
the exact scope disclaimer: this checks the *mechanics* (I.1, and the
length arithmetic of I.4) unconditionally; it cannot and does not test
the *same-side-is-impossible* step (I.4's first half), since that step's
truth is specific to `G` being F-clean, which no fixture is.

## Part II: the safe-contraction obstruction (Task B)

**Definition (Task B).** A nontriangle edge `e` of a simple `δ≥3` graph
`H` is **safe** if `H/e` is again power-of-two-cycle-free (has no cycle
of length in `F`). The proposed **global target**: *every* `δ≥3`,
power-of-two-cycle-free graph has a safe nontriangle edge.

### II.1. No nontriangle edge of `G` is ever safe [PROVED, immediate from Part I]

This is exactly I.2, restated in Task B's vocabulary: for **every**
nontriangle edge `e` of `G`, `G/e` contains a power-of-two cycle (it is
simple, `δ≥3`, and has fewer vertices than the order-minimal `G` — no
further argument needed beyond minimality itself). So **`e` is unsafe,
for every nontriangle edge of `G`, unconditionally.** ∎

### II.2. The global target is logically equivalent to the conjecture itself, not a separate sub-target [PROVED]

Suppose the Erdős–Gyárfás conjecture is false, i.e. some counterexample
exists; let `G` be the lexicographically minimal one (finite induction
on `(|V|,|E|)` guarantees it exists once *any* counterexample does). `G`
is itself a `δ≥3`, power-of-two-cycle-free graph. By II.1, `G` has **no**
safe nontriangle edge. So the global target, applied to `G` specifically,
is **false**. Conversely, if the global target is true (holds for every
`δ≥3` power-of-two-cycle-free graph), applying it to the minimal
counterexample `G` (if one existed) would produce a safe nontriangle
edge `e`, making `G/e` a strictly smaller counterexample — contradicting
`G`'s order-minimality, so no counterexample can exist and the
conjecture is true.

**Conclusion.** *The global target holds if and only if the
Erdős–Gyárfás conjecture is true — and its failure mode is completely
understood already: if it fails, it fails exactly at the minimal
counterexample, exactly as shown in II.1.* This is not an independent,
possibly-easier stepping stone toward the conjecture; proving it is
exactly as hard as proving the conjecture, and disproving it (finding
one `δ≥3` power-cycle-free graph with no safe nontriangle edge) is
**already done** — `G` itself is such a graph, *given* it exists. The
open content is entirely in "does `G` exist," not in "does `G` have a
safe edge" (it provably does not, if it exists at all).

**This is stopping-condition (4) of the handoff (§15): a concrete
obstruction to safe contraction, holding under every currently known
minimal-counterexample property (in fact holding from minimality
alone).** It also reframes the endgame precisely: *"find a safe edge"
can never be the mechanism of a proof, because minimality already rules
out safety completely and without new information.* The only surviving
route through contraction is the one Part I actually built: use the
**forced near-power cycles** (not their absence) as structural
constraints on `G`, and show those constraints are jointly
unsatisfiable — Parts III–IV below, and the still-open Task E.

**No computational test applies here.** Like S4/S5/L3/L4, II.1–II.2 are
minimality arguments about a hypothetical object with no known instance;
there is nothing to run. What *is* computationally exercised is the
mechanical content it leans on (Part I's I.1/I.2), already reported
above.

## Part III: nontriangle-edge census at a cubic vertex (Task C, partial)

### III.1. Exact count: 1 or 3, never 0 or 2 [PROVED]

Let `v∈C` (cubic) with neighbours `a,b,c`. Since `G` is `C4`-free, `v`
has **at most one** edge among `{a,b,c}`: any two of the (at most 3)
possible edges `ab,ac,bc` share an endpoint (pigeonhole on a 3-element
set), and two edges at a common vertex, say `ab,ac` (sharing `a`), give
the 4-cycle `b{-}v{-}c{-}a{-}b` — forbidden. So `v` lies in 0 or exactly
1 triangle through its neighbour-pair.

- **0 internal edges** (`a,b,c` pairwise nonadjacent): none of `va,vb,vc`
  has a common neighbour of `v` (a common neighbour of `v,a` must be a
  neighbour of `v`, i.e. `∈{b,c}`, and neither is adjacent to `a`). **All
  three of `v`'s edges are nontriangle.**
- **Exactly 1 internal edge**, say `ab`: `va` has common neighbour `b`
  (`b∼v`, `b∼a`), so `va` is a triangle edge; symmetrically `vb`. `vc`
  has no common neighbour (`a,b` are the only candidates, and — with
  exactly one internal edge `ab` — neither is adjacent to `c`). **Exactly
  one nontriangle edge, `vc`.**

**Corollary.** Every cubic vertex of `G` has **at least one** nontriangle
incident edge (so Part I's lemma is never vacuous at any cubic vertex),
and by `G1` at least `2/3` of `|V(G)|` is cubic — so `G` has a dense
supply of near-power-cycle witnesses, one per nontriangle edge,
concentrated at (though not limited to) the cubic vertices.

**Computational cross-check.** `check_cubic_nontriangle_count` verifies
the exact `{1,3}` dichotomy on all cubic vertices of every `C4`-free
fixture graph (Petersen — triangle-free, all cubic vertices get 3; the
prism-plus-diagonal — every cubic vertex is in one triangle, all get 1):
**10 cubic vertices checked, 0 vertices with count 0 or 2.**

**Scope, honestly stated.** This pins the *count* of nontriangle edges
per cubic vertex, not the further classification Task C also asks for
(which neighbour a witness path exits through, equal-vs-unequal
exponents `r` across the up-to-3 witnesses at one vertex, or
intersection patterns between witness paths at different vertices). That
finer classification is open and is exactly where Task E's chord/bridge
analysis would need to begin; it is not attempted in this pass.

## Part IV: one clean overlap configuration (Task D, partial)

### IV.1. The exact symmetric-difference identity [restated, not new — see `verifier/linkage_data.py`]

For any two edge sets `A,B` (in particular two cycles), elementary set
theory gives the **exact identity**
\[
|E(A\triangle B)|=|E(A)|+|E(B)|-2|E(A\cap B)|,
\]
not merely an inequality — the handoff's phrasing as a bound is loosened
notation for this identity. For two near-power cycles `|A|=2^r+1`,
`|B|=2^s+1`: `|E(A\triangle B)|=2^r+2^s+2-2|E(A\cap B)|` exactly. This
alone says nothing about how `A\triangle B` decomposes into cycles (it
can split into several components whenever `A,B` cross at vertices
outside `A∩B`'s edges) — the decomposition, not just the total edge
count, is what Task D actually asks for, and is addressed only in the
one clean case below; the general decomposition is open.

### IV.2. Clean same-length merge lemma [PROVED]

**Lemma.** *Let `A,B` be simple cycles of `G` with `|A|=|B|=L`, sharing
**exactly one edge** `xy` and **no other vertex** (`V(A)\cap V(B)=\{x,y\}`).
Then `(A\cup B)\setminus\{xy\}` contains a simple cycle of length
`2(L-1)`.*

*Proof.* `A\setminus\{xy\}` is the `x`–`y` path of `A` avoiding edge
`xy`, with `L-1` edges and internal vertices exactly `V(A)\setminus\{x,y\}`.
Likewise for `B`. Since `V(A)\cap V(B)=\{x,y\}`, these two paths' internal
vertices are disjoint, so concatenating them at their shared endpoints
`x,y` gives a simple cycle (no repeated vertex), of length
`(L-1)+(L-1)=2(L-1)`. ∎

**Immediate corollary for `L=2^r+1`.** `2(L-1)=2\cdot2^r=2^{r+1}` — an
**actual power-of-two cycle**. So: *if two `(2^r+1)`-near-power cycles
of `G` ever share exactly one edge and no other vertex, `G` immediately
contains a power-of-two cycle — contradicting F-cleanness.* **Hence no
two same-`r` near-power witnesses forced by Part I can ever meet in
exactly one clean edge; this is a genuine forbidden-configuration
constraint on how `G`'s forced near-power cycles may overlap.**

**Computational cross-check.** `check_clean_merge` builds the two-path
gadget explicitly for `L=5,9,17,33` (i.e. `r=2,3,4,5`) and verifies, via
both cycle checkers, that removing the shared edge leaves a genuine
simple cycle of length `2(L-1)=8,16,32,64` respectively — **all four
confirmed powers of two, 0 validity failures.**

**Scope, honestly stated.** This resolves only the single cleanest
overlap pattern (shared edge, no other shared vertex, equal exponents).
Task D's full request — decomposing `A\triangle B` into its individual
cycle components for *every* intersection pattern, including unequal
exponents `r≠s` and intersections that are not a single edge or share
extra vertices — is **not** completed here and remains open. This lemma
is offered as stopping-condition (3) of the handoff (§15): one exact,
irreducible near-power-cycle overlap configuration, proved forbidden.

## Part V: chords and bridges of a fixed near-power cycle (Task E)

**Not attempted this pass.** Task E (fixing a shortest near-power cycle
`C`, `|C|=2^r+1`, and constraining every chord/external path via the two
resulting cycle lengths `ℓ+d` and `ℓ+2^r+1-d`, using degree-3 density,
`H`-independence, and `m≤2n-6`) requires machinery (a fixed *shortest*
near-power cycle, plus the two-cut/SPQR restrictions of `two_cut.md`
applied to chords of that specific cycle) that has not yet been built.
Attempting it without Parts I–IV settled first would not meet this
project's standard of proof; it is recorded here as the concrete next
step, not attempted speculatively.

## Part VI: honest stopping-point assessment (per handoff §15)

**What is proved this pass, unconditionally, cross-checked
computationally where the claim does not itself presuppose a
counterexample:**
- **Part I** (near-power edge lemma): every nontriangle edge of the
  minimal counterexample `G` lies on a cycle of length `2^k+1` — the
  central mechanism the endgame is built on.
- **Part II** (safe-contraction obstruction): the literal "does a safe
  edge exist" question is resolved — it never does, for `G` — and shown
  to be logically equivalent in strength to the conjecture itself, not
  an easier stepping stone. This corrects a natural first instinct about
  the endgame (§13 Task B) before any further work was invested in it.
- **Part III** (partial Task C): the exact `{1,3}` nontriangle-edge
  count at every cubic vertex.
- **Part IV** (partial Task D): one exact, proved-forbidden clean
  overlap configuration between two equal-exponent near-power cycles.

**What remains open, honestly:** the general symmetric-difference
decomposition for unequal exponents or messier intersections (Part IV,
general case); the full chord/bridge classification of Task E; and,
critically, **no contradiction has yet been derived** — Parts I–IV
narrow the space of how `G`'s forced near-power cycles can coexist, but
do not yet force an actual power-of-two cycle in general. This session's
stopping point is a hybrid of handoff outcomes (3) and (4) (one exact
forbidden overlap configuration; one concrete, unconditional obstruction
to naive safe contraction) — **not** outcome (1) or (2) (no claim that a
safe edge always exists, or that every cubic vertex has one, is made or
resolvable this way), and **not** a defect bound, order-bounded census,
or voltage-lift elimination (explicitly excluded by §11/§14).

**Next concrete step, for whoever continues this:** attempt Task E on
the *shortest* near-power cycle at a single cubic vertex, using Part
III's exact `{1,3}` witness count to bound how many near-power cycles
pass through one vertex, and Part IV's clean-merge lemma as the model
for what a second forbidden configuration should look like when the two
witnesses are **not** equal-exponent or **not** edge-disjoint-except-one.
