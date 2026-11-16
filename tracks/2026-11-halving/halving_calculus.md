# Halving calculus for Erdős 64 — candidate definition (draft 1, 2026-11-16)

**Status.** Hand-written, checked once by the author of this draft, not
machine-checked and not reviewed. Labels: **[PROVED-HERE]** has a complete
argument below; **[KNOWN]** is a restatement of a published or repo result;
**[OPEN]** is a question; **[CANDIDATE]** is a conjecture that may be false.

`F = {4, 8, 16, …}`. A graph is *F-clean* if it has no cycle with length in
`F`. `G` is a minimal counterexample: min degree ≥ 3, F-clean, minimising
`(|V|, |E|)`. `n = |V(G)|`.

## 1. The idea in one paragraph

Every reduction that has worked on `G` builds a smaller object `K` whose cycle
lengths, multiplied by a power of two, are cycle lengths of `G`. Since
`2^j · F ⊆ F`, the smaller object is F-clean too, and minimality finishes.
The reductions differ in two ways only: how `K` sits inside `G` (as a
subgraph, a subdivision, or a hypergraph), and whether copies of `K` are glued
together first. The definition below separates those two choices.

## 2. Objects: hypergraphs with Berge cycles

A *hypergraph* `𝓗` has vertices and edges, each edge a set of ≥ 2 vertices.
A graph is the case where every edge has size 2.

A *Berge cycle of length t* is a cyclic sequence
`v_1, e_1, v_2, e_2, …, v_t, e_t` of distinct vertices and distinct edges with
`v_i, v_{i+1} ∈ e_i`. For graphs this is an ordinary cycle (`t = 2` is a pair
of parallel edges).

The *incidence graph* `I(𝓗)` is bipartite: one vertex per vertex of `𝓗`, one
per edge, adjacency = membership.

**Fact 1 [KNOWN, standard].** Berge cycles of length `t` in `𝓗` correspond
exactly to cycles of length `2t` in `I(𝓗)`.

For a graph `K`, `I(K)` is `K` with every edge subdivided once.

## 3. The two operations

**Embedding.** A *Berge embedding* of a graph `B` into a hypergraph `𝓐` is a
pair of injective maps `V(B) → V(𝓐)` and `E(B) → E(𝓐)` such that the image of
each edge contains the images of its two ends. If `𝓐` is a graph this is a
subgraph embedding.

**Lemma 1 [PROVED-HERE].** A Berge embedding sends each cycle of `B` to a
Berge cycle of `𝓐` of the same length.
*Proof.* Distinct vertices and edges of the cycle go to distinct vertices and
edges, and consecutive incidences are preserved. ∎

**Halving.** `𝓗` is a *half* of `𝓐` if `I(𝓗)` Berge-embeds in `𝓐`.

**Lemma 2 [PROVED-HERE].** If `𝓗` is a half of `𝓐`, every Berge cycle of
length `t` in `𝓗` gives a Berge cycle of length `2t` in `𝓐`.
*Proof.* Fact 1, then Lemma 1. ∎

A *scale-`2^j` descendant* of `G` is the end of a chain
`G = 𝓗_0, 𝓗_1, …, 𝓗_j` with each `𝓗_{i+1}` a half of `𝓗_i`.

**Gluing.** If `K_1, K_2` share exactly one vertex, every (Berge) cycle of
`K_1 ∪ K_2` lies in one of them. **[KNOWN, standard]**

## 4. The descent principle

**Proposition 3 [PROVED-HERE].** Let `𝓗` be a scale-`2^j` descendant of an
F-clean graph, `j ≥ 1`. Then `𝓗` has no Berge cycle of length `2^i` for any
`i ≥ 1` with `i + j ≥ 2`. In particular for `j ≥ 1` it has no Berge 4-, 8-,
16-cycle, and no Berge 2-cycle (two edges sharing two vertices), so `𝓗` is
linear.
*Proof.* Lemma 2 applied `j` times gives a cycle of length `2^{i+j} ∈ F`. ∎

So F-cleanness is inherited at every scale. This is the multiplicative
structure of the target set, used directly.

## 5. Known results as instances

| Result | Object `K` | How it sits in `G` | Gluing |
|---|---|---|---|
| S4, bridgeless (repo; Ducoffe–Dumitru Cor. 2.2) | one side of the bridge | subgraph (scale 1) | two copies at the bridge end |
| S5, cut vertex (repo; D–D Thm 2.3) | a lobe | subgraph | two copies at the cut vertex |
| Leaf graph `L(G)` (repo `defect.md` I.2; D–D Lemma 3.5) | graph on the high-degree vertices | half: each edge is a path `a–x–b`, `x` cubic with two high neighbours | none |
| No `2^j`-subdivision of a min-degree-3 multigraph (D–D Thm 3.8) | the multigraph | scale-`2^j` descendant that is a graph | none |
| Rainbow form of the bipartite case (D–D Thm 4.4) | hypergraph on one side of the bipartition | half, with `I(𝓗) = G` | none |

Two observations.

- The leaf graph is a special case of Thm 3.8 with `j = 1`. **[PROVED-HERE:
  the paths `a–x–b` are internally disjoint because distinct edges have
  distinct midpoints.]**
- Thm 4.4 in this language: for a C4-free bipartite graph `B` with min degree
  ≥ 3, the half `𝓗` is a linear hypergraph with all degrees ≥ 3 and all edge
  sizes ≥ 3, and `B` has a cycle in `F` iff `𝓗` has a Berge cycle with length
  in `F`. **The target set is the same on both sides.** The bipartite
  conjecture is literally invariant under halving. **[PROVED-HERE from Fact 1
  and Prop. 3: Berge 2-cycles are excluded by linearity, and `2t ∈ {8,16,…}`
  iff `t ∈ F`.]**

## 6. What falls out that is not in the table

### Theorem A [PROVED-HERE] — one low-degree vertex is still forbidden at every scale

*`G` contains no subdivision of a graph `K` in which every edge of `K` becomes
a path of length exactly `2^j` (`j ≥ 1`), where `K` has exactly one vertex of
degree 2 and all other vertices of degree ≥ 3.*

*Proof.* Let `r` be the degree-2 vertex.
`K` has no parallel edges, since they would give a cycle of length
`2^{j+1} ∈ F` in `G`. `K` has no loop: for `j ≥ 2` it would give a
`2^j`-cycle, and for `j = 1` a closed path of length 2, impossible in a
simple graph. So `K` is simple, and each cycle of `K` of length `ℓ` gives a
cycle of length `2^j ℓ` in `G`, so `ℓ ∉ F`.
Take two disjoint copies of `K` and identify the two copies of `r`. The result
`K*` is simple, has min degree ≥ 3 (`r` now has degree 4), and by the gluing
fact every cycle lies in one copy, so `K*` is F-clean.
Order: `|V(K*)| = 2|V(K)| − 1`. The subdivision uses
`|V(K)| + (2^j − 1)|E(K)| ≥ |V(K)| + |E(K)|` vertices of `G`, and
`|E(K)| ≥ (3(|V(K)| − 1) + 2)/2 ≥ |V(K)|`. So `n ≥ 2|V(K)| > |V(K*)|`,
contradicting minimality. ∎

This strengthens D–D Thm 3.8 (which needs min degree ≥ 3 in `K`). Whether it
is already known was not checked beyond that paper's theorem list.

**Corollary A1 [PROVED-HERE].** If the `2^j`-subdivision of a graph `K` lies in
`G` (`j ≥ 1`), then every subgraph of `K` with at least one vertex of degree
≥ 3 has at least two vertices of degree ≤ 2. In particular this holds for the
leaf graph `L(G)`.
*Proof.* A subgraph `K'` of `K` also has its subdivision in `G`. Suppose `K'`
has at most one vertex of degree ≤ 2. If it has none, Thm 3.8 is contradicted;
if it has one of degree 2, Theorem A is. If it has one of degree 1, delete it:
its neighbour had degree ≥ 3 and now has degree ≥ 2, every other vertex still
has degree ≥ 3, and one of the first two cases applies. If it has one of
degree 0, delete it and the rest has min degree ≥ 3. ∎

### Theorem B [PROVED-HERE] — the necklace condition for two-terminal pieces

Let `K` be a graph with two distinguished vertices `r_1, r_2` (*poles*), every
other vertex of degree ≥ 3, and `deg r_1 + deg r_2 ≥ 3`. Let `P(K)` be the set
of lengths of `r_1`–`r_2` paths in `K`. Suppose the `2^j`-subdivision of `K`
lies in `G` (`j ≥ 0`; for `j = 0`, `K ⊆ G`).

*Then for every `m ≥ 3` with `m(|V(K)| − 1) < n`, some sum
`p_1 + … + p_m` with all `p_i ∈ P(K)` lies in `F`. The same holds for `m = 2`
when `r_1 r_2` is not an edge of `K`.*

*Proof.* Cycles of `K` have lengths outside `F` (they are cycles of `G`, or
for `j ≥ 1` their `2^j` multiples are, and `K` is simple as in Theorem A).
Form the necklace `R_m`: `m` copies of `K` in a ring, the `r_2` of each copy
identified with the `r_1` of the next. It has `m(|V(K)| − 1)` vertices and min
degree ≥ 3, and it is simple (for `m = 2` this is where `r_1 r_2 ∉ E(K)` is
used). A cycle of `R_m` either lies in one copy or passes through every glue
vertex once, using one pole-to-pole path in each copy; so the new cycle
lengths are exactly the sums `p_1 + … + p_m`. If no such sum lay in `F`, the
necklace would be an F-clean graph of min degree ≥ 3 on fewer than `n`
vertices. ∎

So a small two-terminal piece of `G` must have pole-path lengths whose 2-fold,
3-fold, …, `m`-fold sums each hit a power of two, for every `m` up to about
`n/|V(K)|`. The repo's Type A/B/C analysis of 2-cuts and its three-copy lifts
are the cases `m = 2, 3` at `j = 0`; the statement for all `m` and all scales
should be compared against `two_cut.md` before it is called new.

**Why Theorem B matters for the roadmap.** It converts the connectivity stage
into additive number theory: a set `P` of positive integers such that every
`m`-fold sumset for `2 ≤ m ≤ M` meets the powers of two. For large `M` this is
very restrictive. For example, if `P = {p}` is a single length then `m·p`
must be a power of two for every admissible `m`, which fails as soon as
`m = 3` is admissible. Parity and 2-adic constraints accumulate as `m` grows.
Classifying such sets is a clean, self-contained problem.

## 7. The same algebra builds counterexample candidates

Garcia's "window calculus" (arXiv:2609.04686) computes the cycle spectrum of a
graph made by replacing vertices with gadgets: base cycles, with lengths
shifted by sums of gadget path lengths. Theorem B's proof is that calculus run
backwards. **A reduction is a gadget construction that comes out smaller.**
So one piece of machinery serves both the proof search and the
counterexample search.

## 8. Open questions, ranked

1. **[OPEN] Sumset classification.** Describe all finite `P ⊂ ℕ` with
   `mP ∩ {2^k} ≠ ∅` for all `2 ≤ m ≤ M`. Target: show that for `M ≥ M_0` no
   such `P` arises as a pole-path spectrum of a C4-free piece. That would
   bound the small side of every 2-cut from below by `n/M_0`, with no order
   restriction. (Stage 3 of the roadmap.)
2. **[OPEN] Poles beyond two.** State and prove the gluing rule for `k` poles
   (cycles of a glued object as sums over a linkage pattern). Needed for
   3-cuts and for the "cut or expand" stage.
3. **[OPEN] Forced self-similarity.** Does every F-clean graph of min degree
   ≥ 3 contain the `2^j`-subdivision of a graph with at most one vertex of
   degree ≤ 2, for some `j ≥ 1`? By Theorem A a yes proves the conjecture.
   This is the precise form of "find a halving step".
4. **[CANDIDATE] Mixed-rank Berge form.** Every linear hypergraph with all
   vertex degrees ≥ 3 and all edge sizes ≥ 2 has a Berge cycle with length a
   power of two. Edge sizes all 2 is the conjecture itself; all ≥ 3 is the
   bipartite case. The mixed case is not obviously implied by either and
   could be false. If true it is the natural class closed under halving.

## 9. What to check before building on this

- Theorem A and Theorem B: a second reader, then Lean. Both proofs are short
  and use only minimality, the gluing fact and counting.
- Novelty of Theorem A against the full text of arXiv:2609.28594 Section 3.3
  and of Theorem B against the repo's `two_cut.md`, `s6_case_tree.md`.
- The mixed-rank candidate: a small search for counterexamples is justified
  here, because the outcome decides whether question 4 or question 3 is the
  right induction class.
