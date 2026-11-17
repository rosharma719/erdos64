---
id: q4-independent-check
title: "q(G) ≥ 4: independent check (2026-11-16)"
kind: track-note
topics: ["tracks", "2026-11-halving"]
doc_status: active
date: 2026-11-16
summary: "Result. Every minimal Erdős–Gyárfás counterexample on at least 37 vertices has q(G) = 2n − 2 − m ≥ 4, i.e. m ≤ 2n − 6. Since no counterexample has order ≤ 40 (Ducoffe–Dumitru, arXiv:2609.28594, Theorem 5.1 — not re-verified here), this confirms the repo's q(G) ≥ 4."
status_line: "Status. Hand argument plus one brute-force script (q4_check.py), both"
---

# q(G) ≥ 4: independent check (2026-11-16)

**Result.** Every minimal Erdős–Gyárfás counterexample on at least 37 vertices
has `q(G) = 2n − 2 − m ≥ 4`, i.e. `m ≤ 2n − 6`. Since no counterexample has
order ≤ 40 (Ducoffe–Dumitru, arXiv:2609.28594, Theorem 5.1 — not re-verified
here), this confirms the repo's `q(G) ≥ 4`.

**Status.** Hand argument plus one brute-force script (`q4_check.py`), both
written without using the repo's `defect_three.md` case analysis. Not
machine-checked. The route is shorter than the repo's because it leans on the
order bound instead of reconstructing each case.

## Setup

`G` minimal counterexample. `C` = degree-3 vertices, `H` = degree-≥4 vertices,
`h = |H|`, `F = G[C]`, `C_i = {v ∈ C : deg_F(v) = i}`, `c_i = |C_i|`.

Inputs, each checked by hand:

1. `H` is independent (delete an edge between two high vertices).
2. Every cubic vertex has a cubic neighbour, so `C = C1 ∪ C2 ∪ C3`
   (Carr's M2; also Ducoffe–Dumitru Lemma 3.2(2)). **Taken from the literature.**
3. Identity `c1 = c3 + 4h − 2q − 4` (pure counting; re-derived).
4. Leaf graph: put an edge `ab` on `H` for each `x ∈ C1` with hubs `a, b`.
   It is simple (else a C4), has no power-of-two cycle (an `r`-cycle lifts to
   a `2r`-cycle), hence is 2-degenerate by minimality, so `c1 ≤ 2h − 3` for
   `h ≥ 2`. This is the same statement as Ducoffe–Dumitru Lemma 3.5.
5. From 3 and 4: `c3 + 2h ≤ 2q + 1` for `h ≥ 2`, so `h ≤ q`.

## Path lemma (brute force, `q4_check.py`)

Colour each `C2` vertex by its unique hub. A component of `F[C2]` is a path or
a cycle. Requiring only that hubs + component contain no C4 and no C8:

| h | longest clean path (vertices) | clean cyclic components | two cyclic components jointly clean |
|---|---|---|---|
| 1 | 2 | none | — |
| 2 | 5 | none | — |
| 3 | 8 | lengths 3 and 5 only | never |

These match the repo's `t ≤ 2, 5, 8` and its "exactly s = 3, 5" cyclic
classification, from a separate implementation.

## Case analysis for q ≤ 3

Each path component of `F[C2]` has two ends, and each end has an `F`-neighbour
in `C1 ∪ C3`. There are at most `c1 + 3·c3` such attachment edges.

- **h = 0.** `G` cubic, so `q = n/2 − 2` and `n = 2q + 4 ≤ 10`.
- **h = 1.** `c1 = 0`, so `c3 = 2q`. Each `C2` vertex has at most one
  `F`-neighbour in `N(z)` and each `C3` vertex has at most one neighbour in
  `N(z)` (else a C4 through the hub), so `c2 ≤ c3` and `n ≤ 4q + 1 ≤ 13`.
- **h = 2.** `c1 ≤ 1`, `c3 = c1 + 2q − 4 ≤ 3`. At most 10 attachments, so at
  most 5 path components of ≤ 5 vertices, no cyclic component:
  `n ≤ 2 + 1 + 3 + 25 = 31`.
- **h = 3** (needs `q = 3`). `c1 ≤ 3`, `c3 = c1 − 2 ≤ 1`. At most 6
  attachments, so at most 3 path components of ≤ 8 vertices, plus at most one
  cyclic component of ≤ 5 vertices: `n ≤ 3 + 3 + 1 + 24 + 5 = 36`.
- **h ≥ 4** is excluded by `h ≤ q`.

So `q ≤ 3` forces `n ≤ 36`. ∎

## What this does and does not establish

- Confirms the repo's conclusion and three of its intermediate facts.
- Does **not** audit `defect_three.md` line by line; it replaces it.
- Depends on the external order bound (≥ 37 needed, ≥ 41 published) and on M2.
- Does not use the Erdős–Faudree–Gyárfás–Schelp theorem that the repo's G2 needed.

## Where this could go

The same counting gives `n ≤ f(q)` for every `q` once the path bound `t(h)` and
the cyclic components are controlled for `h ≤ q`. With the repo's `t(4) = 12`,
the crude count at `q = 4` gives a bound above 41, so `q ≥ 5` does not follow
yet. It needs a sharper count of how path and cyclic components can coexist.
An explicit `f` would be a real theorem: an edge bound `m ≤ 2n − 2 − g(n)`
that improves as the verified order grows.
