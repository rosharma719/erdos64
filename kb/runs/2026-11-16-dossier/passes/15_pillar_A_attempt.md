---
id: pass-15-pillar-a-attempt
title: "Pass XV — Pillar A attempt"
kind: pass
topics: ["run-2026-11"]
doc_status: active
date: 2026-11-17
summary: "Friedman–Krivelevich construction read in full; exactness of cycle lengths reduces to attaching adjusters (the Attachable Adjuster Lemma); triangle adjusters work position-free."
---

# Pass XV — Attempt on Pillar A (exact even lengths in sparse expanders with δ ≥ 3)

**Date:** 17 November 2026. **Status:** attempt record. Pillar A is **not** proved. This
note isolates the single missing lemma, explains why it is the crux, records a
conditional mechanism that does work, and states what to try next. Tags as in
`../program/STRATEGY_2026-11-17.md`.

## 1. Setting

Write N(U) for the external neighbourhood of a vertex set U.

- G is an **α-expander** if |N(U)| ≥ α|U| for every U with |U| ≤ n/2 (Friedman–Krivelevich).
- Target A: for fixed α > 0 and Δ, every α-expander with 3 ≤ δ ≤ Δ(G) ≤ Δ on n ≥ n₀
  vertices has a cycle of every even length in a linear range. In particular it has a
  cycle whose length is a power of two.
- For bounded-degree cubic-like graphs α ≤ 1 is forced: a path on k vertices has only
  about k + 2 outside neighbours. So we are always in the **weak-expansion** regime.

## 2. What Friedman–Krivelevich actually build (EXTERNAL, read in full)

Source: arXiv:1912.11011, *Combinatorica* 41 (2021). Their Theorem 1 gives, for every
ℓ ∈ [a₁ log n, a₂ n], a cycle C_ℓ with ℓ ≤ |C_ℓ| ≤ ℓ + A, where A = O(1/α). The
construction is:

1. A BFS tree T of size α²n/16. Outside its region they extract a robust α/2-expanding
   core U₁ (their Lemma 2.2).
2. A root y ∈ N(T) ∩ U₁, and a second tree T′ grown from y inside U₁ (their Lemma 2.7).
   - Its first k₀ = O(log n) levels are BFS levels.
   - Between levels k₁ and k₂ = k₁ + O(1/α), every vertex has degree ≤ Δ′ in T′.
   - The subtrees hanging from level k₁ contain an expander D.
3. A fixed path Q, from y through T to a carefully chosen x₀, then by short paths to
   u₀ ∈ D. It is chosen to "eliminate" only O(1) vertices of T′ (their Lemmas 2.3 and
   2.5, pigeonhole over levels).
4. A long path P from u₀ inside D that visits each hanging subtree at most once.
5. The cycle C_ℓ = Q + P[u₀ … p] + a return to y through T′, closing at the **first
   vertex of a newly entered subtree**.

The additive error A comes only from step 5. A cycle can close only at subtree entries,
and P spends up to 2C₂ = O(1/α) vertices inside each subtree. Their optimality example
subdivides every edge of a bounded-degree expander m times, so every cycle length is
divisible by m + 1. **It has minimum degree 2.** This confirms the §4 diagnosis of the
strategy note: their obstruction is exactly the absence of free edges.

## 3. Exactness reduces to one lemma

**PROVED (transfer).**
- Suppose the fixed part Q of the FK family also threads adjusters whose available length
  corrections, as subset sums, cover every integer in [0, A].
- Then every length in [a₁′ log n, a₂ n] is attained exactly: pick C_ℓ′ with
  ℓ′ = ℓ − A, then correct by the needed amount. For even targets, steps of 2 suffice
  if the base length is even.
- Threading adjusters into Q must keep Q disjoint from D (except at u₀) and keep the
  elimination set O(1). The section of Q that runs through the first tree T lies
  outside U₁, so detours there touch neither T′ nor D. Doing this rigorously needs the
  adjuster chain to be attached on both sides of T's region; it is fiddly but believed
  routine.

**What is needed — the Attachable Adjuster Lemma (TARGET AAL).** For every α, Δ and K
there is n₀ such that the following holds in every α-expander G with 3 ≤ δ ≤ Δ(G) ≤ Δ on
n ≥ n₀ vertices, and every vertex set W with |W| ≤ log² n:

> there are K vertex-disjoint induced cycles Q₁, …, Q_K of length O(log n / α), avoiding
> W, and on each Qᵢ two vertices aᵢ, bᵢ such that
> - (i) the two aᵢ–bᵢ arcs of Qᵢ differ in length by sᵢ ∈ {1, 2}; and
> - (ii) aᵢ and bᵢ have vertex-disjoint routes, avoiding everything else, into a prescribed
>   expanding core.

AAL plus the transfer gives Target A.

## 4. Why AAL is the crux

**PROVED.** For any short cycle Q, Menger's theorem plus FK Lemma 2.3 give at least
α|Q|/(1+α) vertices of Q with vertex-disjoint escape routes. Their **positions on Q are
not controlled**.
- If the escape vertices cluster on one arc, every usable pair has arcs differing by
  about (1 − α)|Q|. Then the steps are large.
- Many adjusters with large steps help only if the gcd of the steps is 1 or 2, and
  nothing so far controls that gcd.
- This is precisely the step Liu–Montgomery solve with **large** degree: they build
  enough disjoint connections to enter "on almost-but-not-quite opposite sides".
- Montgomery's 2026 survey (arXiv:2607.26049, §5) says a positive answer to Erdős–Gyárfás
  "would require very substantial new ideas". Our analysis locates that difficulty at AAL.

**PROVED (triangles bypass position control).**
- For a triangle, *any* two vertices split it into arcs of lengths 1 and 2, so the step
  is s = 1 regardless of position.
- For a 4-cycle, any adjacent pair gives s = 2. For a 5-cycle, a pair at distance 2
  gives s = 1.
- So for cycles of length ≤ 5 only "two escapable vertices, suitably placed" are needed.
  A triangle needs only two escapable vertices.
- With δ ≥ 3, a short cycle fails to have two escapable vertices only if a single vertex
  separates it from the core. The separated side U then has |N(U)| ≤ 1, so |U| ≤ 1/α.
  Hence only cycles inside pockets of size ≤ 1/α can fail.

**CONDITIONAL THEOREM (TARGET T, proof routine modulo §3's threading).** Every α-expander
with δ ≥ 3 and bounded degree that contains ≥ K(α)·log n vertex-disjoint triangles, for
n large, has a cycle of every length in [a₁′ log n, a₂ n]. In particular it satisfies EG.
- This is the Draganić–Munhá Correia–Sudakov "path with attached triangles" mechanism
  (Chvátal–Erdős pancyclicity) transplanted to weak expanders.
- It is modest: it does not cover high-girth expanders, which are exactly where AAL has
  content.

## 5. Honest assessment and next decisions

- **Target A in general = AAL.** That is the specialists' "substantial new idea" at
  δ = 3. It is not a routine adaptation, and it should not be advertised as one.
- **Is AAL even true?** It could fail. Consider bounded-degree, δ ≥ 3 expanders in which
  every short cycle meets its escape routes only at positions forcing steps ≡ 0 (mod p)
  for an odd prime p.
  - Global obstructions of that type are ruled out for large 3-connected cubic graphs by
    Lyngsie–Merker (all residues mod k occur), but only for cycles of *some* length, not
    short attachable ones.
  - A construction defeating AAL would be a genuine negative result for the whole
    adjuster approach at degree 3, and worth knowing either way.

**Options, in order of expected value.**

1. **Attack AAL with the escape-set geometry.** Consider the set E ⊆ V(Q) of escapable
   vertices, |E| ≥ α|Q|/2, on a shortest cycle Q.
   - If E has two points at near-antipodal positions, done.
   - Otherwise E is concentrated on an arc. Then the ear structure of Q (shortest
     Q-ears, thetas) gives *several* route-length differences per gadget. The goal is to
     show their gcd is ≤ 2 for some gadget among many. This is the cleanest
     open sub-problem.
2. **Look for an AAL counterexample** (a mod-p-rigid sparse expander). That is a
   construction problem, theoretical first.
3. **Write up Target T rigorously** as a short self-contained result. It is low risk and
   low novelty.

**No claim beyond the above is made.** In particular EG for bounded-degree expanders
with δ ≥ 3 remains open here, as far as this pass can tell.

## Sources

- Friedman–Krivelevich: https://arxiv.org/abs/1912.11011
- Montgomery et al., survey: https://arxiv.org/abs/2607.26049
- Draganić–Munhá Correia–Sudakov, pancyclicity: https://jamathr.org/index.php/jamr/article/download/Vol-2Issue-1Paper-1/6903/30301
- Hamiltonicity of expanders: https://arxiv.org/abs/2402.06603
