---
id: pass-18-robust-specials
title: "Pass XVIII — robust specials"
kind: pass
topics: ["run-2026-11"]
doc_status: active
date: 2026-11-17
summary: "Anchoring and nesting lemmas: only O(|W|) of many disjoint candidate cycles can be rigid, for any α; free-entry gadget types; chain sketch with gaps G1–G3."
---

# Pass XVIII — Few rigid candidates, free-entry gadgets, and the chain: toward (S)

**Date:** 17 November 2026. **Status:**
- Lemmas 1–3: **PROVED** (needs refereeing).
- The chain assembly (§4): **SKETCH** with two named gaps.
- If completed, §4 would answer Martinsson–Steiner's open question for **bounded-degree**
  3-connected expanders, since 3-connected implies 2-connected with δ ≥ 3.
- No claim of EG.

**Setting throughout.**
- G is a 2-connected α-expander with δ(G) ≥ 3 and Δ(G) ≤ Δ.
- W′ ⊆ V(G) is the set of vertices "already used" (chain built so far, plus junk), and
  U = G − W′ is a β-expanding core.
- *Defects:* D := N_G(W′) ∩ U, so |D| ≤ Δ|W′|.
- p is an odd prime. A *candidate* is a cycle Q ⊆ U of length q ∈ [q_min, q_max], where
  q_max/q_min ≤ κ (a constant) and q_max = O(log n).
- Fix a candidate Q:
  - Γ_Q is the largest component of U − V(Q).
  - A **pocket** of Q is any other component of U − V(Q). Each pocket X has N_U(X) ⊆ V(Q),
    so |X| ≤ q/β.
  - x ∈ V(Q) is **giant-attached** if it has a neighbour in Γ_Q.
  - A pocket is **clean** if it contains no defect.
- *Short* means length ≤ L := C log n, for a suitable C = C(α, β, Δ, κ).
- Q is **rigid** (mod p) if every short cycle built from Q, its pockets and routes in Γ_Q,
  as in Pass XVII Steps 2–4, has length ≡ 0 (mod p).

## 1. Lemma 1 (rigid candidates are anchored)

If β ≤ 1/p and Q is rigid, then Q is **anchored**: either some vertex of Q is a defect,
or some pocket of Q contains a defect.

*Proof.*
- By Pass XVII Step 2, run inside U with routes in Γ_Q, the giant-attached vertices of a
  rigid Q lie in one residue class along Q. So there are at most ⌈q/p⌉ of them, and since
  q ≥ 3 at least two vertices of Q are not giant-attached.
- Take such a vertex x. Its G-neighbours off Q are in W′ (then x is a defect) or in
  pockets.
- If one of them lies in a clean pocket X, then N_G(X) = N_U(X) ⊆ V(Q), and every vertex
  of X has all its G-edges in X ∪ V(Q). The Fan argument (Pass XVII Steps 3–4, which uses
  only 2-connectivity and δ ≥ 3 of G) yields a short cycle ≢ 0 (mod p), contradicting
  rigidity. ∎

## 2. Lemma 2 (each defect anchors O(κ/β) disjoint candidates)

Let 𝒬 be a family of pairwise vertex-disjoint candidates. A defect v lies in pockets of
at most κ/β + 1 members of 𝒬. Hence at most (κ/β + 2)·Δ·|W′| members of 𝒬 are rigid
(for β ≤ 1/p).

*Proof (nesting).* Suppose v lies in pockets X_i of Q_i and X_j of Q_j, with
Q_i ∩ Q_j = ∅.

- **Case Q_j ∩ X_i = ∅.** X_i is connected, avoids Q_j and contains v, so
  X_i ⊆ X_j. Q_i is connected, disjoint from Q_j, and adjacent to X_i, so Q_i ⊆ X_j as
  well. Hence |X_j| ≥ |X_i| + q_min.
- **Case Q_j ∩ X_i ≠ ∅.** Then Q_j ⊆ X_i by connectivity.
  - If moreover Q_i ∩ X_j = ∅, the first case with the roles exchanged gives
    |X_i| ≥ |X_j| + q_min.
  - If instead Q_i ⊆ X_j as well, consider Γ_i ∪ Q_i. Some vertex of Q_i is
    giant-attached (U is connected and Γ_i is non-empty), so Γ_i ∪ Q_i is connected and
    avoids Q_j ⊆ X_i. It meets X_j (at Q_i), so Γ_i ⊆ X_j. Then |X_j| ≥ |Γ_i| > q/β,
    which contradicts the pocket bound.

So the candidates whose pockets contain v are totally ordered by pocket inclusion, with
sizes growing by ≥ q_min. Since all pockets have size ≤ q_max/β, there are at most
κ/β + 1 of them.

Counting rigid candidates: by Lemma 1 each rigid candidate is anchored at a defect,
either one of its own vertices or a pocket defect. Disjoint candidates own disjoint
vertices. Hence the number of rigid candidates is at most |D|(κ/β + 2). ∎

**Consequence.** U contains Ω(βn/q_max) vertex-disjoint candidates: apply FK repeatedly
in robust cores. That is far more than O(|W′|/β) = O(log n). So **non-rigid candidates
always exist in the residual graph**, for every α. Choosing gadgets one at a time no
longer reintroduces the Martinsson–Steiner threshold at the level of *existence*.

## 3. Lemma 3 (gadgets with free entry and exit)

Let Q be non-rigid, or just pocketed, with at least three escapable vertices
a₁, a₂, a₃ ∈ V(Q) (Pass XVI Lemma 5). Then one of the following gadgets exists. In each,
a cycle may enter and leave at **some two of a₁, a₂, a₃**, chosen freely, through their
escape routes, with two internal options whose lengths differ by a step s.

1. **(Pocket, two attachments.)** A clean pocket X with N(X) = {x₁, x₂}.
   - Rooted Fan gives x₁–x₂ paths through X with lengths differing by s ∈ {1, 2}.
   - Among the three escapable vertices, two lie in the same component of Q − {x₁, x₂}
     (pigeonhole). Enter at one and leave at the other along the arc through x₁, x₂,
     detouring through X.
   - *Works for every odd p and for mod 4,* since s ∈ {1, 2}.
2. **(Pocket, ≥ 3 attachments.)** Let x₀ be the attachment of the common edge in Fan's
   corollary on H′, and let x₁, x₂ be the attachments where the two Fan cycles return.
   - Two x₀–exit paths are formed. One runs through X to x₁, then along Q; the other
     runs through X to x₂, then along Q.
   - Their lengths differ by (|C₂| − |C₁|) + (difference of Q-arcs). The arc difference is
     ≡ 0 (mod p) in the rigid-attachment situation, so s ≢ 0 (mod p).
   - *Works mod odd p.* **Gap G1:** mod 4 the arc difference can be ≡ 2 and cancel.
3. **(Θ-gadget, no pockets.)** All of Q is giant-attached. Take adjacent x, y ∈ V(Q) and
   a route R of length r in Γ_Q from x′ to y′. The traversal options between x and y are
   the edge xy (length 1) and x x′ R y′ y (length r + 2), so s = r + 1.
   - If the cycle x x′ R y′ y x is ≡ 0 (mod p), then r ≡ −3, so s ≡ −2 ≢ 0 (mod p).
     *The same holds mod 4:* s ≡ 2 (mod 4).
   - **Gap G2:** if instead that cycle is ≢ 0 (mod p), we hold a short cycle Z of nonzero
     residue but not yet a gadget with s ≢ 0. Fix: feed Z back as a candidate. Its length
     is ≢ 0 (mod p), so if it has three escapable vertices, Pass XVI Lemma 4 applies.
     This needs |Z| ≥ 6/β + 3. Choose the pair (x, y), or the route R, so that
     r ≥ 6/β; routes can be lengthened inside the expander core by FK.
4. **(q ≢ 0 mod p.)** Pass XVI Lemma 4 directly, with entry and exit chosen among the
   three escapable vertices.

*Proof.* Each case is the stated computation. The free-choice claim in case 1 is the
pigeonhole on the circle: x₁ and x₂ split Q into two arcs, and two of the three escapable
vertices lie in the same one. Cases 2–4 use entry and exit among the escapable
vertices in the same way. ∎

## 4. The chain (SKETCH)

This mirrors Martinsson–Steiner's Claim 1 with three changes:
- gadgets come from Lemma 3 instead of bare FK cycles;
- entry and exit are both chosen from escapable vertices, instead of a fixed entry and a
  "bad set" of exits;
- the survival requirement is placed on the **escapable set**.

**Procedure.** The chain ends at a vertex e in the current core U_i. To add one gadget:
1. Choose a candidate of length q_i ∈ [ℓ_i, κℓ_i], where ℓ_{i+1} = Dℓ_i, D = D(β, Δ).
   It must be non-rigid for the needed prime, which exists by Lemma 2.
2. Take its escapable set E, of size ≥ βq_i/3 by Lemma 5, with disjoint routes into the
   far core.
3. Discard the at most O(|W′_i|/β²) escapable vertices whose routes end in the junk created
   by the chain so far. Exponential growth of ℓ_i keeps the remainder large:
   βℓ_i/3 ≫ |W′_i|/β², since |W′_i| = O(ℓ_{i−1}·i).
4. Pick entry and exit among the survivors by Lemma 3, and link e to the entry route's
   endpoint by a short path in the core (a linkage of O(1) paths in an expander).
5. Stop once the stabiliser argument (Martinsson–Steiner) has driven the subset-sum set of
   steps to all of Z_k, or once the steps cover all residues needed for EG.

**Gap G3.** Lemma 3 picks entry and exit from *some* three escapable vertices. After the
discard in step 3, the survivors may all lie on one side of the pocket attachments, or in
one residue class, for case 4.
- Cases 1–3 tolerate any three survivors, because the gadget's step does not depend on
  which escapable vertices are used.
- Case 4 can fail if all survivors share a residue class. Then fall back to the
  Θ-gadget or pocket gadget built on Q, which exist whenever Q has pockets or adjacent
  giant-attached pairs.
- A careful case analysis should close this. It is not yet written.

**What a completed §4 gives.**
1. **Residues.** For every α > 0, Δ and odd k: every sufficiently large 2-connected
   α-expander with 3 ≤ δ ≤ Δ(G) ≤ Δ has cycles of all residues mod k. Since 3-connected
   implies 2-connected with δ ≥ 3, this answers the second question in
   Martinsson–Steiner §4 for bounded degree.
2. **Exact lengths.** Assume Gap G1 is closed, or bypassed by using only cases 1 and 3
   mod 4, and assume M1 threading. Then: every even length in a linear range, hence EG,
   for 2-connected bounded-degree expanders with δ ≥ 3.

## 5. Ledger update

| Item | Status |
|---|---|
| Lemma 1 (anchoring) | PROVED |
| Lemma 2 (nesting; few rigid candidates) | PROVED |
| Lemma 3 (free-entry gadgets) | PROVED except Gap G1 (mod 4, case 2) and Gap G2 (lengthening Z) |
| Chain with survival on escapable sets | SKETCH, Gap G3 |
| M1 threading into the FK cycle | open (routine expected) |

**Next concrete tasks.**
1. Close G2. FK windows control lengths only up to ±A, so "lengthen within a window" does
   **not** preserve residues; that idea is withdrawn. Better: the Θ-structure
   Q ∪ (x x′ R y′ y) already has three x–y routes, of lengths 1, q − 1 and r + 2.
   - If r + 1 ≡ 0 (mod p), the cycle x x′ R y′ y x has length ≡ 2.
   - Then compare the other pair of routes, (q − 1) versus (r + 2), for an entry/exit
     pair on the short side. The step q − r − 3 ≡ q − 2 ≢ 0 when q ≡ 0.
   - Check whether this pair placement is always available among three escapable
     vertices.
2. Close G3 by the case analysis above.
3. G1: find a mod-4 gadget for pockets with ≥ 3 attachments, or show that cases 1 and 3
   always suffice mod 4.
4. Write M1.
