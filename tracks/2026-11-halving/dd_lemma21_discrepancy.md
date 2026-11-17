# The Ducoffe–Dumitru Lemma 2.1 discrepancy (2026-11-17)

**Resolved: no contradiction.** Ducoffe–Dumitru Lemma 2.1 allows `k ≥ 1`, so a
triangle edge is covered trivially by the triangle itself (length 3 = 2¹+1).
The repo's audit asks for a cycle of length `2^k+1` with `k ≥ 2` (length 5, 9,
17, …), which is what contracting an edge actually produces. Under that
stronger reading, triangle edges remain an open gap, and the published lemma
does not close it.

## Background

A minimal counterexample `G` is minimal first in order, then in size. Both
sources contract an edge `e = uv` lying in no triangle: `G/e` keeps minimum
degree 3, so by minimality it has a cycle of length `2^k`. That cycle must pass
through the merged vertex, and lifting it through `e` gives a cycle of length
`2^k + 1` through `e` in `G`. Since `2^k ≥ 4` here, `k ≥ 2`.

Ducoffe–Dumitru use Lemma 2.1 only for Corollary 2.2 (every edge lies on a
cycle, so `G` is bridgeless). The repo uses the same lift as the near-power
edge lemma (`contraction.md` Part I) in the Type N / Type T contraction track.

## The two statements

| | Ducoffe–Dumitru Lemma 2.1 | Repo: near-power edge lemma + audit |
|---|---|---|
| Statement | Every edge lies on a cycle of length `2^k+1`, some `k ≥ 1` | Every nontriangle edge lies on a cycle of length `2^k+1`, `k ≥ 2` |
| Allowed lengths | 3, 5, 9, 17, … | 5, 9, 17, 33, … |
| Triangle edges | "the result follows for `k = 1`": the triangle is the cycle | Not covered; no `k ≥ 2` witness found for all three edges |
| Nontriangle edges | Contract `e`, lift a `2^k` cycle (`k ≥ 2`) | Same argument, `contraction.md` I.1–I.4 |

The note in `literature_update_2026-11.md` read both as "`2^k+1` cycle through
every edge" and missed the change in `k`.

## Why triangle edges get no `k ≥ 2` witness

From `every_edge_witness_audit.md` (commit 7640d5a):

1. **Contract the edge.** Not possible: the endpoints of a triangle edge share
   a neighbour, so the merged vertex can drop below degree 3.
2. **Contract the triangle** (`contraction_atoms.md` III.2). The power-of-two
   cycle `D` of `G/T` meets `T` at two vertices; only the edge between them
   gets a `2^k+1` lift. Which pair depends on `G`.
3. **Contract `N[v]`** at a Type T vertex (`contraction_neighborhood.md`
   Part II). Pair `(a,b)` forces `{2^k+1, 2^k+2}`; pairs `(a,c)`, `(b,c)` force
   `{2^k+2, 2^k+3}`, with no `2^k+1`.
4. **Recentre at `a` or `b`.** Each has its own unfavourable case, and
   `contraction_mixed_witness.md` Part IV shows every `{2^k+2, 2^k+3}`
   combination is arithmetically consistent.

The audit's second claim, that some single edge has two distinct `2^k+1`
witnesses, has no support in either source.

## Impact

| Result | Needs from Lemma 2.1 | Status |
|---|---|---|
| D–D Cor. 2.2 / repo S4 (bridgeless) | every edge on some cycle | safe |
| D–D Thm 2.3 / repo S5 (cut vertex) | Cor. 2.2 | safe |
| Repo near-power edge lemma | `k ≥ 2`, nontriangle edges | safe as stated in `lemmas.md`, `proof.md` |
| Type N vertices (`cubic32_mersenne_audit.md`) | `k ≥ 2` on all three edges | safe: all nontriangle |
| "Every edge has a `k ≥ 2` witness" as a search constraint | `k ≥ 2` on triangle edges | not established; do not use |

When citing D–D Lemma 2.1, state `k ≥ 1`. For the `k ≥ 2` lift, cite the
repo's nontriangle lemma or the nontriangle case of the D–D proof.

## Open

- Does every triangle edge of a minimal counterexample lie on a cycle of length
  5, 9, 17, …? A proof must rule out `v`, `a`, `b` all landing on the
  unfavourable pair.
- Does some edge carry two distinct `2^k+1` witnesses?

## Sources

- Ducoffe, Dumitru, *Towards a more structured search for Erdős–Gyárfás
  counter-examples*, arXiv:2609.28594, Sec. 2 (Lemma 2.1, Cor. 2.2), read from
  the arXiv HTML on 2026-11-17. https://arxiv.org/abs/2609.28594
