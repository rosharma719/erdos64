---
id: pass-20-closing-status
title: "Pass XX — closing status"
kind: pass
topics: ["run-2026-11"]
doc_status: active
date: 2026-11-17
summary: "Π-gadget lemma (position- and modulus-free adjuster), coin lemma, parity lemma, G3 for odd primes; honest list of what remains open in the expander pillar."
---

# Pass XX — Closing what closes: Π-gadgets, the coin lemma, parity, G3 for odd primes; what remains

**Date:** 17 November 2026. Honest outcome of the "close it all" pass:
- **Closed (PROVED):** four new lemmas (§1–§3, §4.1).
- **Closed modulo one tiny-cycle subcase:** G3 for odd primes (§4).
- **Still open:** mod-4 rigidity in bipartite cores (G1′), and the single-vertex
  robust-linkage steps that the sketches (M1, chain) rely on.
- The expander theorem is **not** yet proved. No claim of EG.

## 1. The Π-gadget lemma (PROVED)

**Lemma 1.** Let M be a path (part of the chain). Let x, y, w ∈ V(M) occur in this order
along M, with M-distances d₁ = d_M(x, y) and d₂ = d_M(y, w). Let Π be a path internally
disjoint from M, containing vertices a, b, c in this order along Π. Let there be rung
paths x–a, y–b and w–c of lengths t_x, t_y and t_w, pairwise disjoint and internally
disjoint from M and Π. Set r = |Π[a, b]| and r′ = |Π[b, c]|. Then the three re-routings
of M have length changes

- s₁ = t_x + r + t_y − d₁ (replace M[x, y]),
- s₂ = t_y + r′ + t_w − d₂ (replace M[y, w]),
- s₃ = t_x + r + r′ + t_w − d₁ − d₂ (replace M[x, w]; y is skipped and its rung unused),

and **s₁ + s₂ − s₃ = 2t_y**. In particular:
- **Direct middle rung (t_y = 1):** for every m ≥ 3, some sᵢ ≢ 0 (mod m), since
  otherwise 2 ≡ 0 (mod m). This holds for odd primes and for m = 4, for **all positions**
  of x, y, w and all lengths r, r′, t_x, t_w.
- **General rung:** the conclusion holds whenever 2t_y ≢ 0 (mod m).

*Proof.* Each re-routing replaces a sub-path of M by a path through the rungs and Π, and
the lengths are read off. The resulting closed walks are simple cycles because all
pieces are disjoint and y's rung is unused in s₃. The identity is direct algebra. ∎

**Lemma 2 (monotone rungs).** If Π has five rungs, to five distinct vertices of M, then
three of them have their Π-order equal to their M-order (Erdős–Szekeres). So Lemma 1
applies to a sub-gadget.

*Significance.*
- Lemma 1 gives position-free, modulus-free adjusters needing only **one direct rung in
  the middle**.
- It needs no candidate cycles, no pockets, and no Fan's lemma. Rigidity can only arise
  through the middle rung's length.

## 2. Coin lemma (PROVED)

**Lemma 3.** Let v₁, …, v_t ≤ h be positive integers with gcd g, each available with
multiplicity M ≥ (t+1)h² + Ag. Then the subset sums contain every multiple of g in
[t h², M v₁]. This interval has length ≥ Ag.

*Proof.*
- **Representability.** Every multiple N of g with N ≥ h² is a non-negative combination
  Σ cᵢvᵢ. The Frobenius number of {vᵢ/g} is < h² (Schur's bound (a₁ − 1)(a_t − 1)).
- **Bounding the coefficients.** Trading (v₁/g)·vᵢ = (vᵢ/g)·v₁ makes cᵢ < v₁/g ≤ h for
  i ≥ 2. Then c₁ = (N − Σ_{i≥2} cᵢvᵢ)/v₁ ≥ 0 once N ≥ t h², and c₁ ≤ N/v₁ ≤ M. ∎

**gcd reduction (PROVED, given gadget supply).**
- Repeatedly pick a modulus m: an odd prime p dividing the current gcd, or m = 4 if 4
  divides it.
- Collect h·M gadgets with steps ≢ 0 (mod m). By pigeonhole, some value v ≢ 0 (mod m)
  occurs M times.
- The gcd strictly drops, so there are at most log₂h + 1 rounds.
- Total: O(h³ log h) gadgets. With h = O(log n) and gadgets of size O(log n), this uses
  O(log⁴ n · log log n) vertices, which is negligible.

## 3. Parity (PROVED)

**Lemma 4.** If G is 2-connected and non-bipartite, its shortest odd cycle O
(|O| ≤ 2 diam + 1) has two vertices a, b with vertex-disjoint routes to any target set
Y with |Y| ≥ 2. The gadget "enter at a, leave at b" has an **odd** step |O| − 2d_O(a, b).

*Proof.*
- **Two routes.** A single vertex separating V(O) from Y would be a cut vertex. By
  Menger's theorem, two disjoint V(O)–Y paths exist, and they start at distinct vertices
  a, b.
- **Odd step.** |O| is odd, so |O| − 2d is odd. ∎

**Use.** If the reduced gcd is 2:
- in bipartite G, all cycles are even, so the even target is consistent;
- in non-bipartite G, place the odd gadget first in the chain, when nothing has been
  removed yet. The sums then fill every integer in the interval of Lemma 3, shifted by
  the odd step.

## 4. G3 for odd primes (closed except subcase T)

Pass XVIII's chain needs, at each step, a gadget whose step lies outside the current
stabiliser and which works with **whichever** escapable vertices survive.

### 4.1 Reduction to certificate cycles (PROVED)

**Claim.** Pick an unanchored candidate Q; all but O(|W′|κ/β) candidates are unanchored
(Pass XVIII Lemma 2). Then:
- Q is non-rigid (Pass XVIII Lemma 1, contrapositive).
- So there is a short **certificate cycle** Z, built from Q, its clean pockets and routes
  in Γ_Q, with |Z| ≢ 0 (mod p).
- If Z has **any** three escapable vertices, Pass XVI Lemma 4 gives a pair with step
  ≢ 0 (mod p). This is **independent of which three survive**.

That is exactly the position-freeness G3 asked for. It remains to show certificates
can be taken with ≥ 3 escapable vertices. By Pass XVI Lemma 5 this holds if
|Z| ≥ 6/β + 3.

### 4.2 Certificate lengths (PROVED except subcase T)

Using the certificate types of Pass XVII:
- **Giant-route certificates** (x x′ R y′ y plus an arc). Pass XVII Step 2 works for every
  route R, so take R long. Then |Z| ≥ 6/β + 3. ✓
- **Pocket certificates** (Fan). Close with the longer arc, so |Z| ≥ q/2 + 1. ✓
- **Two-neighbour certificates** (pocket vertex y adjacent to x₁, x₂ ∈ Q). These are
  2 + d and 2 + q − d. If the long one is ≢ 0 (mod p), it serves. ✓

**Subcase T (open, technical).** Only the short one is nonzero: d < 6/β and d ≡ 2 (mod p).
- Then Z₀ = y x₁ (short arc) x₂ y has |Z₀| ≡ 4 and is tiny, so Lemma 5 does not apply.
- Expected fix: route three escapes from Z₀. Two go along Q's long arc in opposite
  directions; the third goes through y's pocket to another attachment x₃ and then along
  Q. Choose the escapable vertices of Q (there are ≥ βq/3) to interleave correctly.
  Alternatively, if y's pocket has only the attachments x₁, x₂, use the Fan pocket gadget
  (step 1 or 2).
- Not yet written.

## 5. What remains open

1. **G1′ — mod 4 in bipartite cores.**
   - Π-gadgets (Lemma 1) solve mod 4 whenever a direct middle rung is available.
   - Fan pocket gadgets solve it for clean pockets with two attachments.
   - The remaining configuration: every relevant middle rung runs through a pendant or
     pocketed region, and every clean pocket has ≥ 3 attachments. There the lifted Fan
     cycles can cancel mod 4.
   - **This is a genuine open case.**
2. **Single-vertex robust linkage.** Several steps need a *specific* vertex to have
   further disjoint routes into the core after a short path has been removed:
   - the middle rung vertex of a Π-gadget, which needs two routes;
   - the chain passing through a rung vertex;
   - the endpoint vertices in M1.
   Weak expansion (α < 1) does not guarantee this for a given vertex. The tools that do
   work are statements about *sets*: escapability counts for long paths, and the
   anchoring/nesting counts.
   - Every place we used single-vertex robustness has to be rewritten as a selection
     from a large set, as was done for G3.
   - I believe this is achievable, but it is **not** done. It is the same difficulty
     that produces the threshold in Martinsson–Steiner's own proof.
3. **M1 constants.** FK's proof must be rechecked with the O(log n) removed set and the
   two new root choices.
4. **Subcase T** (§4.2).

## 6. Honest status of the expander pillar

| Component | Status |
|---|---|
| Adjuster mechanisms: Π-gadget (new), Fan pockets, Θ, Lemma 4 on certificates | PROVED |
| Supply: few anchored candidates, any α | PROVED |
| Number theory: coin lemma, gcd reduction, parity | PROVED |
| Position-freeness for odd primes | PROVED except subcase T |
| Mod 4 (bipartite) | **OPEN (G1′)** |
| Robust linkage of specific vertices | **OPEN** (believed routine, not written) |
| M1 threading | design complete, constants unchecked |

**Bottom line.** The expander pillar is now a well-scaffolded **conditional** result.
- Its number theory and adjuster mechanisms are proved.
- Its remaining gaps are one genuine combinatorial case (bipartite mod 4) and a body of
  robust-linkage technicalities of the kind that fill most of the pages of
  Friedman–Krivelevich and Martinsson–Steiner.
- Even when completed it yields EG only for 2-connected bounded-degree expanders with
  δ ≥ 3, not EG itself.
