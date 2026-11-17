---
id: richness-findings
title: "Are path-length sets rich? Literature and small cases (2026-11-16)"
kind: track-note
topics: ["tracks", "2026-11-halving"]
doc_status: active
date: 2026-11-16
summary: "Question (from sumset_classification.md). In a C4-free graph with two poles and all other degrees ≥ 3, must the set of pole-to-pole path lengths contain a long run of consecutive lengths?"
---

# Are path-length sets rich? Literature and small cases (2026-11-16)

**Question (from `sumset_classification.md`).** In a C4-free graph with two
poles and all other degrees ≥ 3, must the set of pole-to-pole path lengths
contain a long run of consecutive lengths?

**Verdict.** No general richness theorem is available, and the evidence says
one is false in the regime that matters. The stage-3 stop rule is triggered.
A sharper target comes out of the same reading; see the last section.

Sources were read through fetched summaries of the arXiv pages, not line by
line. Items marked [COMPUTED] were run in this session.

## 1. What the literature gives

| Setting | Result | Source |
|---|---|---|
| Two vertices in a 2-connected graph, other degrees ≥ k+1 | k paths whose lengths form a progression with difference 1 or 2. At degree 3 that is **two** lengths. | Gao–Huo–Liu–Ma, arXiv:1904.08126 |
| Hamiltonian, min degree 3 | `n^{1−o(1)}` distinct cycle lengths | Bucić–Gishboliner–Sudakov, arXiv:2104.07633 |
| 3-connected cubic **planar**, circumference ≥ k | a cycle with length in `[k, 2k+9]`, for every k | Merker, arXiv:1905.09101, Thm 2 |
| Same class | infinite families with **no** cycle length in `[k, 2k+1]`, k even | same paper, Thm 7 |
| Large 3-connected cubic | cycle lengths meet every progression with odd modulus | Lyngsie–Merker, cited there |
| Degree-3-critical graphs (2n−2 edges, no proper induced subgraph of min degree 3) | only about `log n` distinct cycle lengths are guaranteed, and that order is attained | Di Braccio et al., arXiv:2504.11656, Thm 1 |
| Same class | a fixed length can be missing entirely (no 23-cycle) | Narins–Pokrovskiy–Szabó, cited there |
| Trees with all degrees 1 or 3 | leaf-to-leaf lengths: at least `log(n+2) − 1`, tight; some trees have only `O(N^0.91)` lengths below `N` | Di Braccio et al., Thms 2, 3 |

Three things follow.

1. **Sparse spectra exist near the tree-like end.** A minimal counterexample
   has no proper subgraph of min degree 3, the same defining property as the
   degree-critical class, which sits at the edge-count extreme `2n − 2`. There,
   logarithmically many lengths is the truth. (Those examples do contain short
   cycles including a C4, so they are not counterexamples.)
2. **Even the best class does not give a doubling window.** For 3-connected
   cubic planar graphs the guaranteed window is `[k, 2k+9]` and windows
   `[k, 2k+1]` can be empty. A graph can be made to skip a whole factor-2
   range at one chosen scale.
3. **So no argument can work one scale at a time.** A counterexample would
   need an empty spot at 4, 8, 16, … up to `n` simultaneously. Any proof has
   to use the interaction between scales.

## 2. Small cases [COMPUTED]

All C4-free graphs on 8 to 13 vertices with exactly two vertices of degree 2
and the rest of degree ≥ 3 (`geng -c -f -d2`, then `poles.c`):

| vertices | pieces | fewest lengths | smallest max/min ratio | pass every ring test up to 60 copies |
|---|---|---|---|---|
| 8 | 1 | 5 | 2.33 | 1 |
| 9 | 2 | 6 | 2.67 | 2 |
| 10 | 22 | 4 | 2.00 | 22 |
| 11 | 125 | 2 | 2.00 | 125 |
| 12 | 1,139 | 2 | 2.00 | 1,139 |
| 13 | 10,966 | 2 | 2.00 | 10,966 |

- **Theorem B excludes none of the 12,255 pieces.** Every one has its longest
  pole path at least twice its shortest and hits a power of two under every
  multiplicity tested.
- The two-length pieces have lengths `{1, 2}`: the poles are adjacent and
  share their only other neighbour (a triangle hanging from one vertex).
- **None of these pieces is also C8-free.** Pieces of an actual
  counterexample are larger than anything enumerable this way.

So Theorem B and Theorem C are correct but have no bite on small pieces.
They stay as lemmas; they are not a route to 3-connectivity.

## 3. A sharper target: the doubling inequality

Let `f(k)` be the least order of a graph with min degree ≥ 3 and no cycle of
length `4, 8, …, 2^k`.

**Reformulation [PROVED-HERE, elementary].** The conjecture holds iff
`f(k) ≥ 2^{k+1}` for every `k ≥ 2`.
*Proof.* A counterexample on `n` vertices with `2^k ≤ n < 2^{k+1}` avoids all
lengths up to `2^k`, so `f(k) ≤ n < 2^{k+1}`. Conversely a graph on fewer than
`2^{k+1}` vertices avoiding lengths up to `2^k` has no power-of-two cycle. ∎

**Sufficient condition [PROVED-HERE].** If `f(k+1) ≥ 2·f(k)` for all `k ≥ 2`,
the conjecture holds.
*Proof.* `f(2) = 10` (the Petersen graph; no C4-free graph of min degree 3 has
fewer vertices). Then `f(k) ≥ 10·2^{k−2} = 2.5·2^k > 2^{k+1}`. ∎

**How much room there is.**

| k | lengths avoided | f(k) | needed by the conjecture | needed by doubling |
|---|---|---|---|---|
| 2 | 4 | 10 | 8 | — |
| 3 | 4, 8 | 24 (Garcia, arXiv:2609.04686) | 16 | 20 |
| 4 | 4, 8, 16 | ≤ 78; ≥ 54 reported by Markström, unpublished | 32 | 48 |
| 5 | 4 … 32 | ≤ 450 | 64 | — |
| 6 | 4 … 64 | ≤ 32,640 | 128 | — |

The known constructions grow far faster than the conjecture needs. Each extra
scale appears to cost much more than a factor of two.

**This is the multi-scale statement section 1 asks for**: it says exactly
that avoiding one more power of two forces the graph to at least double.

**First test of the obvious mechanism [PROVED-HERE, by counting].**
The halving calculus suggests proving doubling by finding, inside a graph
avoiding `4 … 2^{k+1}`, the 2-subdivision of a min-degree-3 graph avoiding
`4 … 2^k`. That fails at the first step: a 24-vertex graph avoiding 4 and 8
would need to contain the 2-subdivision of a C4-free graph of min degree 3,
which has at least 10 vertices and 15 edges, so 25 vertices. **Graph halves
alone cannot prove the doubling inequality.** Whatever does must allow
low-degree vertices or hyperedges in the half, which is where the open
questions 2 and 4 of `halving_calculus.md` point.

## 4. Revised stage 3

Replace "prove 3-connectivity through rich spectra" with:

> **Prove `f(k+1) ≥ 2 f(k)`**, or any bound of the form `f(k) ≥ 2^{k+1}`.

First concrete step, small and decisive: work out by hand how the four
24-vertex extremal graphs for `{4, 8}` relate to the Petersen graph, the
extremal graph for `{4}`. If the larger graphs contain a generalised half
(Berge, or with a few low-degree vertices) that is a Petersen-like object,
that names the right class. If they do not, halving is the wrong mechanism
for doubling and the calculus should be kept only for its reductions.

## Sources

- https://arxiv.org/abs/1905.09101
- https://arxiv.org/pdf/2504.11656
- https://arxiv.org/pdf/2104.07633
- https://ar5iv.labs.arxiv.org/html/1904.08126
- https://arxiv.org/html/2609.04686
