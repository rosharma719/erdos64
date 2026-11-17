# Pass XVII — Short cycles of nonzero residue in 2-connected expanders, and the constant-specials reduction

**Date:** 17 November 2026. **Status:**
- Theorem 1: **PROVED** (full proof below; needs independent refereeing).
- Lemma 2: **PROVED**.
- The robust, multi-copy version needed by the program: **OPEN**, with the exact obstacle
  stated.
- No claim of EG.

Notation as in Pass XVI. G is an α-expander on n vertices; FK refers to
Friedman–Krivelevich (arXiv:1912.11011).

## 1. Theorem 1 (short cycles of nonzero residue)

**Theorem 1.** For every α ∈ (0, 1] there are C = C(α) and n₀ such that the following
holds. Let G be a 2-connected α-expander on n ≥ n₀ vertices with δ(G) ≥ 3, and let p be
an odd prime. Then G contains a cycle of length ≢ 0 (mod p) and of length at most
C log n. No bound on the maximum degree is needed.

*Context.*
- Martinsson–Steiner show all residues mod k for α > 1/(p−1), and that some threshold is
  needed for general expanders: subdivisions, which have δ = 2.
- Fan's theorem gives, in 2-connected δ ≥ 3 graphs, cycles of lengths differing by 1 or 2,
  hence a nonzero residue, but with **no length bound**.
- Theorem 1 gives a nonzero residue at length O(log n) for **every** α. The 2-connectivity
  and δ ≥ 3 hypotheses are exactly what Proposition 1 of Pass XVI shows to be necessary.

### Proof

Suppose, for contradiction, that every cycle of length ≤ L := C log n has length ≡ 0
(mod p). Call such cycles *short*. The constant C is fixed at the end.

**Step 0 (a short induced cycle).**
- FK Lemma 2.1 gives diam(G) ≤ c₁ log n/α.
- Let Q be a shortest cycle. Then q := |Q| ≤ 2 diam(G) + 1, Q is induced, and q ≡ 0
  (mod p).
- Every x ∈ V(Q) has a neighbour x′ ∉ V(Q), because deg x ≥ 3 and Q is induced.

**Step 1 (structure of G − V(Q)).**
- Let Γ be the largest component of G − V(Q). Every other component X has |X| ≤ n/2,
  so α|X| ≤ |N(X)| ≤ q, giving |X| ≤ q/α. Call these components *pockets*.
- By FK Lemma 2.2 applied with V₀ = V(Q), Γ contains an α/2-expanding core U with
  |Γ ∖ U| ≤ 3q/α. Moreover diam(G[U]) ≤ c₂ log n/α.
- So any two vertices of Γ are joined inside Γ by a path of length at most
  r_max := 2(3q/α + 1) + c₂ log n/α.

**Step 2 (giant-attached vertices share one residue).** Let x, y ∈ V(Q) have neighbours
x′, y′ ∈ Γ, and let d be the length of one x–y arc of Q.
- Join x′ to y′ by a path R inside Γ, of length r ≤ r_max (r = 0 if x′ = y′). Closing
  x x′ R y′ y with each arc gives two simple cycles, of lengths r + 2 + d and
  r + 2 + q − d.
- Both are short once L ≥ q + 2 + r_max, so both are ≡ 0 (mod p).
- Subtracting gives q − 2d ≡ 0, so 2d ≡ q ≡ 0, so d ≡ 0 (mod p), since p is odd.
- In particular, **no two adjacent vertices of Q** (d = 1) both have neighbours in Γ.

**Step 3 (no pocket vertex sees Q twice).** Suppose some y in a pocket X is adjacent to
x₁ ≠ x₂ ∈ V(Q), with arc lengths d and q − d.
- The cycles y x₁ (arc) x₂ y have lengths 2 + d and 2 + q − d, both ≤ q + 2, so both
  are short.
- They give 2d ≡ q ≡ 0, so d ≡ 0, and then 2 ≡ 0 (mod p). This is a contradiction.
- Hence every pocket vertex has at most one neighbour on Q.

**Step 4 (a pocket yields two short cycles whose lengths differ by 1 or 2).** Let X be a
pocket and N(X) ⊆ V(Q) its attachment set. Since G is 2-connected, |N(X)| ≥ 2. Every
vertex of X has all its G-neighbours in X ∪ N(X), so it has degree ≥ 3 there.

*Case |N(X)| = 2, say N(X) = {x₁, x₂}.*
- Let F = G[X ∪ {x₁, x₂}]. Every end-block of F contains x₁ or x₂ as a non-cut vertex.
  Otherwise its cut vertex would be a cut vertex of G, because vertices of X have no
  neighbours outside F.
- The blocks of F therefore form a path from x₁ to x₂. Not every block is an edge, since
  vertices of X have degree ≥ 3.
- Pick a 2-connected block B with ends u, v. Every other vertex of B has degree ≥ 3 in B.
  Fan's lemma gives u–v paths in B with lengths differing by 1 or 2.
- Concatenating with fixed paths through the other blocks gives x₁–x₂ paths R₁, R₂
  through X with 1 ≤ |R₂| − |R₁| ≤ 2.
- Closing both with the same arc of Q gives two cycles of length ≤ |X| + 1 + q ≤
  q/α + q + 1. Their lengths differ by 1 or 2, so they are not both ≡ 0 (mod p). This
  is a contradiction.

*Case |N(X)| ≥ 3.*
- Let H′ be G[X] plus one new vertex z, joined to every vertex of X that has a neighbour
  on Q. By Step 3 the graph H′ is simple, and every vertex of X has degree ≥ 3 in H′.
  Also deg z ≥ 3, because distinct attachment vertices give distinct X-neighbours.
- H′ is 2-connected. G[X] is connected, so z is not a cut vertex. If w ∈ X were a cut
  vertex, some component Y ⊆ X of H′ − w would miss z, and then N_G(Y) = {w}, a cut
  vertex of G.
- By Fan's corollary applied to H′ − zy for an edge zy (Pass XVI, Corollary 3), there are
  cycles C₁, C₂ of H′ through z with 1 ≤ |C₂| − |C₁| ≤ 2.
- Each Cᵢ is z y₁ (path in X) y₂ z, where y₁, y₂ have unique Q-neighbours x_a, x_b.
  - If x_a = x_b, replacing z by x_a gives a cycle of G of length |Cᵢ|.
  - Otherwise, replacing z by x_a, then a Q-arc of length d_ab, then x_b gives a cycle of
    length |Cᵢ| + d_ab.
- Both are short (≤ q/α + 1 + q). By Step 2 applied to pocket attachments, d_ab ≡ 0:
  - two attachments of one pocket are joined through X by a path of length r ≤ |X| + 1;
  - the two closing cycles give 2d_ab ≡ q ≡ 0.
- So the lifted lengths are ≡ |C₁| and ≡ |C₂| (mod p). These differ by 1 or 2, so they are
  not both ≡ 0. This is a contradiction.

**Step 5 (conclusion).**
- By Step 4 there are no pockets, so every vertex of Q has a neighbour in Γ.
- Since q ≥ 3, Q has two adjacent vertices, both giant-attached. That contradicts Step 2.
- All the cycles used have length ≤ max(q + 2 + r_max, q/α + q + 1) = O(log n/α²). So
  choosing C = C(α) large enough makes all of them short. ∎

*Remarks.*
1. Only these were used: 2-connectivity, δ ≥ 3, α-expansion (diameter, pocket size, and a
   core in G − V(Q)), and Fan's lemma.
2. The argument is **local to Q** apart from the routes in Step 2. It shows that *every*
   short induced cycle Q certifies a nonzero-residue cycle inside Q ∪ (pockets of Q) ∪ (one
   route of length O(log n)).
3. The mod-4 analogue fails at Step 4: d_ab may be ≡ 2 (mod 4), and steps 2 + 2 can
   cancel. The 2-adic part needs a separate argument; see §3.

## 2. Lemma 2 (only constantly many special gadgets are needed)

Let A = A(α) be the FK window constant, and let Λ(α) := lcm(1, 2, …, A+1).

**Lemma 2.**
- (a) **Prime-power steps.** Let m be a prime power (odd or a power of 2). If a cycle Q has
  three escapable vertices and m ∤ |Q|, then some pair has step ≢ 0 (mod m).
- (b) **Large prime powers are free.** For every prime power m > A + 1, FK applied in a
  robust core with a window ℓ ≡ 1 (mod m) yields cycles with q ≢ 0 (mod m). Such cycles
  have length O(log n), and by Pass XVI Lemma 5 they have three escapable vertices.
- (c) **The gcd is bounded.** Consequently a family of gadgets built from such cycles,
  available in any robust core and in unlimited supply, has step gcd g₀ dividing Λ(α), a
  constant depending only on α.

*Proof.*
- (a) If all three pair-steps are ≡ 0 (mod m), then 2gᵢ ≡ q for each i. Summing gives
  2q ≡ 3q, so q ≡ 0 (mod m).
- (b) A window of A + 1 consecutive integers starting at a residue 1 (mod m) contains no
  multiple of m when m > A + 1.
- (c) Every prime power dividing g₀ is ≤ A + 1, by (a) and (b). ∎

**Consequence (reduction).** The exactness machinery needs, beyond the free gadgets:

> **(S)** a *constant* number s(α) ≤ Λ(α) of vertex-disjoint "special" gadgets. Their
> steps must, together with the free family, generate every residue modulo g₀ (and fix
> the 2-adic part). Each must be a short cycle with ≥ 2 escapable vertices into one common
> robust core.

Theorem 1 supplies **one** short certified nonzero-residue cycle per odd prime. What is
missing is s(α) **disjoint** ones, each escapable into a common core.

## 3. The remaining obstacle, stated exactly

Choose specials greedily. Let W be the union of those already chosen, with |W| = O(log n).
Run the Theorem 1 argument in G − W. It breaks only through **W-pockets**: components of
G − W − V(Q), other than the giant, that touch W. Their vertices have lost degree, so
Fan's lemma does not apply to them.

A rigid survivor Q must send all but ≤ q/p + 1 of its vertices into W-pockets or into W
itself. Expansion then gives |N(S_Q) ∩ W| ≥ (α − 1/p)q − 1, where S_Q = Q ∪ (W-pockets
of Q).
- This is a contradiction only when α > 1/p. That is precisely the Martinsson–Steiner
  threshold, now reappearing as the cost of disjointness.

**Two routes forward.**
1. **Simultaneous selection.**
   - Take M ≫ s(α) disjoint short induced cycles in a robust core. Each, *in G*, certifies
     a nonzero-residue cycle within its local region (Remark 2) plus one route.
   - Show that s(α) of these certificates can be chosen with disjoint local regions, with
     routes realised disjointly in the core.
   - The local regions are disjoint by construction when the pockets of different
     candidates are disjoint. The routes are linkages in an expander. A linkage lemma for
     s(α) = O(1) pairs, with all pairs in the core, is standard.
   - The delicate point is that attachment vertices x′ may fall into the junk created by
     removing other candidates. With M ≫ s(α) candidates, choose ones whose attachment
     vertices avoid the O(s(α) log n/α) junk.
   - **This looks feasible and is the next thing to write.**
2. **Avoid W-pockets by design.** Take W to be closed under adding pockets: replace W by
   W ∪ (all non-giant components of G − W). Then G − W is connected, and new pockets of Q
   that touch W must have been created by removing Q. A sharper Step 4 that tolerates a
   single defective attachment would suffice, perhaps via Liu–Ma's rooted version of Fan.

## 4. Where the whole program now stands

| Link | Status |
|---|---|
| Position control for adjusters (Pass XVI L4, L5) | PROVED |
| Pockets at 2-separations are step-1/2 adjusters (Fan) | EXTERNAL |
| Free gadget family; gcd g₀ ∣ Λ(α), a constant (Lemma 2) | PROVED |
| One short nonzero-residue cycle per odd prime, any α (Theorem 1) | PROVED (referee) |
| s(α) disjoint specials in a common core (S) | OPEN — route 1 looks feasible |
| 2-adic part (mod 4) | OPEN — Theorem 1 does not cover it; in bipartite graphs it is a separate question |
| Threading into the FK cycle (M1) | OPEN — believed routine |
| ⇒ EG, and exact even lengths, for 2-connected bounded-degree expanders with δ ≥ 3 | conditional on (S), mod 4, M1 |

The decisive open item has shrunk from "gcd control in weak expanders" (the
Martinsson–Steiner question) to a **disjointness/linkage statement for constantly many
locally certified gadgets**, plus a 2-adic analogue.

## Sources

- Friedman–Krivelevich: https://arxiv.org/abs/1912.11011
- Martinsson–Steiner: https://arxiv.org/abs/2204.09107
- Fan (2002), via Liu–Ma: https://arxiv.org/abs/1508.07912
