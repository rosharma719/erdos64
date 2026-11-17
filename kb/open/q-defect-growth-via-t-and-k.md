---
id: q-defect-growth-via-t-and-k
title: "Defect growth: is q(G) unbounded via finiteness of t(h) and K(h)?"
kind: open-problem
label: "OPEN"
topics: ["defect", "2026-11-halving"]
doc_status: active
date: 2026-11-17
summary: "For a minimal counterexample, every fixed q bounds n via n ≤ h + c1 + c3 + t(h)(c1+3c3)/2 + K(h)t(h). If the clean-path length t(h) and the clean cyclic-component count K(h) are finite for every h, then q → ∞ with n (m ≤ 2n − g(n)); polynomial bounds would give m ≤ 2n − n^c."
evidence: ["kb/open/assets/2026-11-17-defect-growth-screenshot.jpg", "tracks/2026-11-halving/q4_independent_check.md", "kb/notes/defect/linear_defect_growth_audit.md", "kb/notes/defect/defect.md"]
depends_on: ["q4-independent-check", "linear-defect-growth-audit"]
---

# Defect growth via finiteness of t(h) and K(h)

**Provenance.** This was transcribed on 2026-11-17 from a photo of a terminal running another
Claude Code session (§5, "How the paper could become much stronger"). The photo is
stored as `kb/open/assets/2026-11-17-defect-growth-screenshot.jpg`. The session's
text is cut off at the bottom, and "the paper" is not identified in the photo. The
notation matches `tracks/2026-11-halving/q4_independent_check.md`, which this
generalizes. **Nothing below has been re-derived or re-computed in this repository
yet.**

## Setting (from `q4_independent_check.md`)

- G is a minimal counterexample, with q = 2n − 2 − m.
- H is the set of vertices of degree ≥ 4 ("hubs"), with h = |H|.
- F = G[C] is the subgraph induced by the degree-3 vertices, and
  C_i = {v ∈ C : deg_F(v) = i}, with c_i = |C_i|.
- Known: h ≤ q, c1 ≤ 2h − 3, and c3 + 2h ≤ 2q + 1 (for h ≥ 2).
- Each C₂ vertex is coloured by its unique hub. The components of F[C₂] are paths or
  cycles.
- A component is *clean* if, together with the hubs, it contains no C₄ and no C₈.

## The proposed bound (as transcribed)

For any fixed q, every quantity except c₂ is bounded, and

```
n ≤ h + c1 + c3 + t(h)·(c1 + 3c3)/2 + K(h)·t(h)
```

where
- **t(h)** is the longest clean coloured path with h hubs;
- **K(h)** is the largest number of cyclic components that can coexist cleanly.

Path components of F[C₂] have two ends, each attached to C₁ ∪ C₃. There are at most
c1 + 3c3 attachment edges, so at most (c1 + 3c3)/2 path components, each with at most
t(h) vertices.

## The question

**Are t(h) and K(h) finite for every h?**
- If so, n ≤ f(q) for some function f, so q grows without bound as n grows, i.e.
  m ≤ 2n − g(n) with g(n) → ∞.
- If both are bounded polynomially in h, this gives something like m ≤ 2n − n^c.
- The session calls that "a real theorem on D-D's question, not a constant
  improvement". D-D is Ducoffe–Dumitru (arXiv:2609.28594), whose estimate is
  m ≤ 2n − 2.

## What was reported

| Quantity | Reported | Status in this repo |
|---|---|---|
| t(h), h = 1, 2, 3 | 2, 5, 8 | Matches `q4_check.py` and the repo's earlier `t ≤ 2, 5, 8` (independent implementations). |
| t(4), t(5) | 12, 18 | **Reported only.** No script or log in the repo. Computed "using only 4- and 8-cycles". |
| t(h) ≥ h | giving every vertex its own hub creates no cycles | Elementary, as stated. |
| K(h), triangle components | two triangle components sharing two hubs always produce a C₈, so triangle components number O(h²) | Argument stated, not checked. |
| K(h), 5-cycle components | some pairs can coexist cleanly; "the general case needs real work" | Open. |

The session proposed "a bounded effort, a week or two" of computation at small h before
attempting proofs. The truncated last line reads: "The general bound also explains why
q ≥ 5 d[…] the crude count gives n ≤ 48 when h = 2 and n […]".

## Relation to existing work

- **`kb/notes/defect/linear_defect_growth_audit.md`.** An external report claimed
  n ≤ 15q − 17, i.e. linear growth of q. Its overlap with this repo (the leaf/hub graph,
  c1 ≤ 2h − 3, h ≤ q) checked out, but its new core lemma was **not** verified. Linear
  bounds on t(h) and K(h) would essentially give such a statement. That report's core
  lemma should be compared with this formulation before new work starts.
- **`kb/notes/defect/defect_q_ge6_audit.md`** records an unsupported "provisional
  q ≥ 6" claim (one-hub / two-hub / three-hub cores), with no artifact found.
- **Proved so far:** q ≥ 4 (`kb/core/proof.md` P9–P12; independently
  `q4_independent_check.md`).

## Suggested next steps

1. Re-run `tracks/2026-11-halving/scripts/q4_check.py`, extended to h = 4, 5, to
   reproduce t(4) = 12 and t(5) = 18 with a recorded command and counts. Then upgrade
   those two rows to COMPUTATIONALLY VERIFIED in a new claim file.
2. Write out the triangle-component O(h²) argument. Classify which pairs of 5-cycle
   components coexist cleanly.
3. Derive the q = 4 and q = 5 consequences from the general bound, as a check against
   the truncated "n ≤ 48 when h = 2" remark.

## History

- 2026-11-17: created from a screenshot of another session; transcribed, not verified.
- 2026-11-17: reported answer — yes, both finite, by a short hand argument; n ≤ (3q² + 7q − 4)/2 for q ≥ 2 (see `c-defect-quadratic-bound`, SKETCH pending write-up; computer check of the key lemma recorded as passed). The question stays open until the proof is written here; a linear bound remains open.
