---
id: extremal24-findings
title: "How the 24-vertex extremal graphs avoid 4 and 8 (2026-11-16)"
kind: track-note
topics: ["tracks", "2026-11-halving"]
doc_status: active
date: 2026-11-16
summary: "Question. The smallest min-degree-3 graph with no 4-cycle has 10 vertices (Petersen). The smallest with no 4- or 8-cycle has 24. Do the 24-vertex graphs contain a \"half\" that is a Petersen-like object, as the halving calculus would want?"
---

# How the 24-vertex extremal graphs avoid 4 and 8 (2026-11-16)

**Question.** The smallest min-degree-3 graph with no 4-cycle has 10 vertices
(Petersen). The smallest with no 4- or 8-cycle has 24. Do the 24-vertex graphs
contain a "half" that is a Petersen-like object, as the halving calculus would
want?

**Verdict.** No. Halving is not what relates the two scales. The 24-vertex
graphs are small cubic graphs with some vertices replaced by triangles, and
the triangles shift cycle lengths past 8. The stop rule for the revised stage
3 is triggered for halving; the doubling inequality itself is untouched.

Graphs used: the four 24-vertex graphs frozen in the repo's
`manifests/z3_bases_manifest.json` (Markström's, and three from
Hegde–Sandeep–Shashank). Everything below is [COMPUTED] in this session
(`extremal24.py`, `quotient24.py`, `truncation_check.py`) unless marked.

## 1. What the four graphs look like

| graph | bipartite | triangles (all disjoint) | cycle lengths missing from 3…24 | after contracting triangles |
|---|---|---|---|---|
| Markström | no | 7 | 4, 8 | 10 vertices, cubic, 3 triangles again |
| HSS 1 | no | 4 | 4, 5, 8 | 16 vertices, cubic, girth 5 |
| HSS 2 | no | 3 | 4, 8 | 18 vertices, cubic, girth 4 |
| HSS 3 | no | 6 | 4, 8 | 12 vertices, cubic, girth 4 |

- **None is bipartite**, so none has a Berge half in the sense of
  `halving_calculus.md`.
- **None contains a subdivided min-degree-3 graph that avoids 4**, by the
  counting argument already recorded (it would need 25 vertices).
- **None reduces to the Petersen graph.** Markström's graph contracts to a
  10-vertex cubic graph, but that graph has three triangles; contracting again
  gives `K4`. So Markström's graph is `K4` with vertices replaced by nested
  triangle gadgets. It also has three 3-edge cuts with a 7-vertex side.
- **Every one is almost pancyclic.** They contain every cycle length from 3 to
  24 except the forbidden ones (one also lacks 5). They avoid 4 and 8 with
  precisely placed holes, not with high girth.

## 2. The truncation formula [PROVED-HERE, and checked on all four graphs]

Let `Q` be a cubic graph and `S` a set of its vertices. Replace each vertex of
`S` by a triangle (its three edges go to the three corners). Call the result
`G`.

*The cycle lengths of `G` are 3 (if `S` is nonempty) together with every
integer in `[ℓ + t, ℓ + 2t]`, for each cycle `C` of `Q` with length `ℓ` and
`t = |C ∩ S|`.*

*Proof.* A cycle of `G` other than a triangle projects to a cycle `C` of `Q`.
At each truncated vertex on `C` it enters and leaves by two distinct corners
and joins them by the direct edge (1 extra edge) or the other way round the
triangle (2 extra edges), independently at each such vertex. ∎

So `G` avoids `2^k` exactly when no cycle of `Q` has
`ℓ + t ≤ 2^k ≤ ℓ + 2t`. In the four graphs, every 4-cycle and 8-cycle of the
quotient passes through at least one triangle (so it gets longer), and the
5-, 6- and 7-cycles carry triangle counts that make their windows jump over 8:
for example length 5 with 4 triangles gives `[9, 13]`.

The triangle, seen as a two-pole piece, has path lengths `{1, 2}`. By the
Proposition in `sumset_classification.md` that is the **only** two-length set
that ring-gluing can never exclude. The extremal graphs are built from exactly
the gadget the reduction theorems cannot touch.

## 3. What this changes

1. **Halving is a source of reductions, not the engine of the doubling
   inequality.** Theorems A and B stand. Open question 3 of
   `halving_calculus.md` (forced self-similarity) should be dropped as a route.
2. **The right object is gadget replacement.** The known constructions at
   every scale are of this kind: triangles at 24 vertices, and per Garcia
   (arXiv:2609.04686) larger gadgets on small cubic bases at 78 and 450. The
   truncation formula is the smallest case of his window calculus.
3. **The repo's Type-T programme was aimed at the right feature.** Triangle
   vertices are where length-avoidance happens. What was wrong was the method
   (open-ended casework), not the target. The formula above replaces much of
   that casework with one inequality per quotient cycle.
4. **A concrete form of the doubling question.** For which cubic `Q` and `S`
   does no quotient cycle have a window containing 4, 8 **or 16**? All four
   24-vertex graphs fail at 16 (between 31 and 226 quotient cycles have a
   window containing it). Understanding why 16 cannot be dodged at this size,
   in terms of `(ℓ, t)` pairs, is a hand-sized problem and is the first place
   the interaction between scales becomes visible.

## 4. Suggested next step

Take the `(ℓ, t)` formulation and ask: given that windows must miss 4 and 8,
what do the short cycles of `Q` force about longer ones? Two quotient cycles
sharing a path combine into a third, whose `ℓ` and `t` are determined by
theirs. If missing 4 and 8 on short cycles forces some combined cycle's window
onto 16 until the graph is large, that is a doubling argument for truncations,
and a template for general gadgets.
