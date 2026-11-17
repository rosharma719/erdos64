---
id: sumset-classification
title: "The integer question behind Theorem B (2026-11-16)"
kind: track-note
topics: ["tracks", "2026-11-halving"]
doc_status: active
date: 2026-11-16
summary: "Question. F = {4, 8, 16, …}. For a finite set P of positive integers let mP be the set of sums of m elements of P, repeats allowed. Which P satisfy mP ∩ F ≠ ∅ for every 3 ≤ m ≤ M?"
status_line: "Status. Theorem C and its corollaries: proved by hand below, then tested"
---

# The integer question behind Theorem B (2026-11-16)

**Question.** `F = {4, 8, 16, …}`. For a finite set `P` of positive integers
let `mP` be the set of sums of `m` elements of `P`, repeats allowed. Which `P`
satisfy `mP ∩ F ≠ ∅` for every `3 ≤ m ≤ M`?

By Theorem B of `halving_calculus.md`, the set of pole-to-pole path lengths of
a two-terminal piece `K` of a minimal counterexample `G` satisfies this with
`M` just under `n / (|V(K)| − 1)`.

**Status.** Theorem C and its corollaries: proved by hand below, then tested
on all 1,470 sets of at most four integers from `{1,…,14}` with zero
violations (`sumset_check.py`). Not machine-checked, not reviewed.

Notation: `a = min P`, `b = max P`, `g = gcd{p − a : p ∈ P}`,
`g = 2^e · g'` with `g'` odd.

## Theorem C — necessary conditions [PROVED-HERE]

Suppose `mP ∩ F ≠ ∅` for all `3 ≤ m ≤ M`.

1. **More than one length.** If `M ≥ 3` then `|P| ≥ 2`.
   *Proof.* `3a` is not a power of two. ∎
2. **No odd modulus.** `g' = 1` or `g' > M`.
   *Proof.* Every element of `mP` is `≡ ma (mod g')`. Take `m = g' ≥ 3`: all
   sums are divisible by `g'`, and no power of two is. ∎
3. **Scale divides everything.** If `M ≥ 3` then `2^e` divides every element
   of `P`.
   *Proof.* Sums in `3P` are `3a + g·t`. If `v_2(a) < e` then every such sum
   has 2-adic valuation exactly `v_2(a)`, so the only power of two it could
   equal is `2^{v_2(a)} ≤ a < 3a`. ∎
4. **Width.** If `b < 2a` then `M < 8a / (2a − b)`.
   *Proof.* `mP ⊆ [ma, mb]`. An integer `m` with `2^k < ma` and
   `mb < 2^{k+1}` misses every power of two. Such `m` lies in an open interval
   of length `2^k (2a − b)/(ab)`. Take the least `k` making this length exceed
   1, then the next `k`: this gives an integer `m ≥ 3` with
   `m < 8a/(2a − b)`. ∎

**Consequence of 2 and 3.** For large `M`, `P = 2^e · P'` with `P'` having
`gcd` of differences 1. The condition on `P` is the condition on `P'` against
the rescaled target. So the integer problem is scale-invariant in the same way
the graph problem is, and only primitive `P'` need studying.

## Proposition — two lengths [PROVED-HERE]

If `|P| = 2` and the condition holds for all `m ≥ 3`, then
`P = {2^e, 2^{e+1}}`.
*Proof.* By 2 and 3, `P = 2^e{a', a'+1}`. If `a' ≥ 2` then
`a' + 1 < 2a'` and part 4 gives a failing `m`. So `a' = 1`. ∎

Conversely `{1, 2}` works for every `m`: `mP = [m, 2m]` always contains a
power of two.

## What survives [COMPUTED, range stated]

Among sets of ≤ 4 integers from `{1,…,14}`, tested for `3 ≤ m ≤ 400`:

- 793 of 1,470 survive; 738 distinct primitive shapes.
- No survivor has `b < 2a` (as part 4 requires). The smallest ratio is exactly 2.
- The only two-element primitive survivor is `{1, 2}`.
- 133 primitive sets with `b > 2a` still fail, all at small `m` (latest:
  `{5, 10, 12}` at `m = 21`). Example: `{1, 3, 8}` fails at `m = 3`.

So with three or more lengths the condition is mild. Roughly: after removing
the power-of-two scale, a set survives when its largest element is at least
twice its smallest and a few small-`m` cases work out.

## Graph corollaries [PROVED-HERE, given Theorem B]

Let `K` be a two-pole piece of `G` at any scale, `N = |V(K)| − 1`, `d` the
distance between the poles in `K`, `ℓ` the longest pole-to-pole path.

- **D (width).** Either `ℓ ≥ 2d`, or `n ≤ 8dN / (2d − ℓ)`.
- **E (odd residues).** If all pole-path lengths are congruent modulo an odd
  `q ≥ 3`, then `n ≤ qN`.
- **E′ (parity).** If `3N < n` and all pole-path lengths have the same parity
  (for instance `K` bipartite), they are all even. More generally, if they all
  agree modulo `2^e`, they are all divisible by `2^e`.
- **Two-length pieces.** If `K` has exactly two pole-path lengths, they are
  `2^e` and `2^{e+1}`, unless `n ≤ N · max(q, 8d/(2d − ℓ))` with `q` the odd
  part of their difference.

## What this means for the roadmap

**The arithmetic is not the bottleneck.** Necklaces rule out pieces whose
path-length sets are narrow or locked to a residue class. They do not rule
out a piece with a wide, irregular set of lengths, and most pieces of min
degree 3 should have one. So 3-connectivity will not follow from Theorem B
alone.

**The tension worth attacking.** Two facts now point in opposite directions
for the two sides `A`, `B` of a 2-cut:

- Necklaces: `P_A` must be *wide* (`ℓ ≥ 2d`) and hit powers of two under
  every admissible `m`-fold sum.
- Cleanness of `G`: `(P_A + P_B) ∩ F = ∅`. So `P_A` misses `2^k − q` for
  every `q ∈ P_B` and every `k`. If `P_A` contained a run of consecutive
  lengths from `u` to beyond `2u + q`, `G` would have a power-of-two cycle.
  So `P_A` must be *gappy at every scale*.

On integers alone these are compatible (`P_A = {1,2}`, `P_B ⊇ {4,5}`), so the
missing input is about graphs, not numbers.

**The sharpened question for stage 3 [OPEN].**
*Richness.* Let `K` be a C4-free two-pole graph with all non-pole degrees
≥ 3 and `N` vertices. How sparse can its set of pole-path lengths be? Is
there a function `w(N) → ∞` such that the set contains `w(N)` consecutive
lengths, or consecutive lengths of one parity?

A window of length growing with `N` on one side of a 2-cut, combined with
cleanness, would bound how unbalanced a 2-cut can be, with no order
restriction. The published tool here gives two lengths differing by 1 or 2
(Gao–Huo–Liu–Ma, used in the repo's T2); the question is whether min degree 3
plus C4-freeness gives more. The other direction is equally useful: an
explicit family of pieces with sparse spectra would be the first ingredient
of a counterexample.
