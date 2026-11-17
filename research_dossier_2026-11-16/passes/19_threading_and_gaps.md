# Pass XIX — Threading (M1) designed, Gap G2 closed in outline, mod-4 reduced

**Date:** 17 November 2026. **Status:**
- M1: **SKETCH**. The design is complete; it reuses FK's proof with two root choices
  changed.
- G2: **SKETCH**, closed modulo routine linkage.
- G1 (mod 4): **REDUCED** to one configuration.
- G3: unchanged.
- No claim of EG.

## 1. M1 — threading the gadget chain into a near-length cycle

Recall FK's cycle (arXiv:1912.11011, §2.3):

> y →(T)→ x₀ →(Q_{x₀})→ v₀ →(Q′)→ u₀ →(P)→ … →(down to L_{k₁}, then up T′)→ y.

**Observation.** FK's proof uses y ∈ X₀ = N(T) ∩ U₁ only to have a short y–x₀ connection
avoiding U₁. If the cycle instead arrives at x₀ from some other vertex through T, then
the root y of T′ need not be adjacent to T at all. It only needs to lie in U₁ and to be
reachable by a route whose other vertices avoid U₁.

**Design.**
1. **Chain.** Build the gadget chain 𝒞 (Pass XVIII §4) from a start v to an end x, inside
   a set of O(log n) vertices. Let W be 𝒞 together with *all* gadget alternatives and
   pockets used, so |W| = O(log n).
2. **T rooted at the chain end.** Grow T by BFS from x in G − (W ∖ {x}) until it has
   α²n/16 vertices. FK's Lemma 2.1 bound on depth still holds: depth ≤ diam + O(1).
3. **Core.** Let U₁ be the FK Lemma 2.2 core of G − (W ∪ T), and Z := V ∖ (W ∪ T ∪ U₁),
   so |Z| = O(αn) + O(|W|/α). Absorb Z-neighbours of T into T as FK do, for at most
   6/α² rounds. Then X₀ := N(T) ∩ U₁ has |X₀| ≥ α³n/32 − O(Δ log n).
4. **Root y from the chain start.** Take a shortest path from v to U₁ in G − (W ∖ {v}) − T.
   Its first vertex in U₁ is y, and its interior lies in Z, so its length is ≤ |Z| + 1.
   - Choose v so that this path exists, i.e. v is not cut off from U₁ by T ∪ W. Since v
     is the start of a chain we build, take v from a large robust set: any vertex of the
     core of G − T with a neighbour in U₁ works, and the chain is then grown from v.
   - Hence y ∈ U₁ and **no route vertex other than y lies in U₁**.
5. **Rest of FK unchanged.**
   - Grow T′ from y in G₁ = G[U₁] (FK Lemma 2.7).
   - Set X₁ := X₀ ∖ {y}. Build FK's disjoint short X₁–U₂ paths, choose x₀ with small
     elimination, and build Q′, D and P exactly as in FK.
   - The cycle is

     > v →(𝒞)→ x →(T)→ x₀ →(Q_{x₀}, Q′)→ u₀ →(P)→ … →(T′)→ y →(route)→ v.

**Disjointness checks.**
- 𝒞 ⊆ W, and W is excluded from T and U₁. T ∩ U₁ = ∅.
- The route from v to y meets U₁ only at y, and avoids T and W except at v.
- T′, D, P, Q_{x₀} and Q′ lie in U₁, and avoid the route because only y lies in U₁.
- FK's elimination accounting is unchanged: the new route adds no vertex of U₁ besides
  the root y.

**Length control.** The total length is |𝒞| + |T-path| + |route| + (FK variable part),
where the FK variable part takes, for each target, a value in a window of width A. The
gadget states change only |𝒞|, by any amount in the subset-sum set S. If S contains A+1
consecutive admissible values (consecutive integers, or consecutive even integers with
matching parity), every length in the linear range of the theorem is attained exactly.

**What remains in M1.** Re-check the constants in FK Lemmas 2.2–2.7 with the extra
O(log n) removed set W. FK already handle removed sets of size O(αn), so O(log n) is
harmless. Also confirm that choosing x₀ is unaffected by excluding the route.

## 2. Gap G2 — the Θ-gadget when the route cycle is nonzero

Setting: Q is a candidate, x and y are adjacent giant-attached vertices, and x′, y′ are
their neighbours in Γ_Q.
- **Case A:** some short x′–y′ route R in Γ_Q has r + 1 ≢ 0 (mod p). The Θ-gadget
  (edge xy versus x x′ R y′ y) has step r + 1 ≢ 0. Entry and exit are any two escapable
  vertices of Q other than x and y.
- **Case B:** every short x′–y′ route has r ≡ −1 (mod p). Choose one of length
  ≥ 6/β + 3 within Γ_Q's core. Expanders contain x′–y′ paths of every length window in a
  logarithmic range, by FK-type arguments; a long simple path suffices. The cycle
  Z = x x′ R y′ y x then has |Z| ≡ 2 ≢ 0 (mod p). By Pass XVI Lemma 5 it has three
  escapable vertices, and by Pass XVI Lemma 4 it is a gadget with step ≢ 0 (mod p).

Mod 4: Case A gives step ≢ 0 (mod 4). In bipartite graphs steps are even, so this means
≡ 2 (mod 4). Case B gives |Z| ≡ 2 (mod 4) and Lemma 4(ii). So **the Θ-gadget works mod 4
as well.**

Remaining care: the route R must avoid the escape routes of the chosen entry and exit.
Choose R after the escape routes, inside the core of Γ_Q minus those routes. This is
O(1) paths removed from an expander, so x′ and y′ stay connected unless they lie in
O(1/β)-size pockets; avoid those by choice of the pair (x, y).

## 3. Gap G1 (mod 4) — reduction

A candidate Q is **mod-4-good** if any of the following holds:
- (i) q ≢ 0 (mod 4) and Q has three escapable vertices;
- (ii) two adjacent vertices of Q are giant-attached (then the Θ-gadget applies, §2);
- (iii) Q has a clean pocket with exactly two attachments (Fan step ∈ {1, 2}).

Otherwise Q is **mod-4-bad**:
- 4 ∣ q;
- the giant-attached vertices are pairwise non-adjacent, so at least half of Q is not
  giant-attached;
- every clean pocket has ≥ 3 attachments.

The anchoring argument (Pass XVIII Lemma 1) does **not** bound mod-4-bad candidates. Their
non-giant vertices may feed clean pockets with ≥ 3 attachments, where the Fan lift loses
control mod 4 (Pass XVIII, Gap G1).

**Open sub-question G1′.** In a 2-connected bounded-degree α-expander with δ ≥ 3, can
*all but O(log n)* of a family of disjoint short candidates be mod-4-bad?
- A mod-4-bad candidate has more than half its vertices feeding pockets with ≥ 3
  attachments.
- By the nesting lemma (Pass XVIII Lemma 2), each vertex lies in pockets of ≤ κ/β + 1
  candidates. So bad candidates have pocket mass ≥ q/2 each, all inside a bounded-overlap
  family. This bounds them by O(n/q), which is not enough on its own.
- **Idea:** recurse into the pockets. A clean pocket X with ≥ 3 attachments, together
  with the Q-arcs, contains new short cycles Q′ = (X-path) + (Q-arc). Their structure is
  constrained by rigidity, and a descent on pocket size should terminate in a mod-4-good
  candidate.

**Why mod 4 may be dispensable for EG in non-bipartite graphs.** If the residual graph
contains a robust odd cycle O with three escapable vertices, every pair gives an odd
step. Two copies of an odd-step gadget give 2s ≡ 2 (mod 4). So G1 matters only when the
relevant cores are bipartite. In that case Fan's bipartite version (Liu–Ma Theorem 2.1)
gives clean 2-attached pockets step exactly 2 ≡ 2 (mod 4), and §2 handles Θ. The
bipartite ≥3-attachment case is exactly G1′.

## 4. Consolidated ledger (Passes XVI–XIX)

| Item | Status |
|---|---|
| δ ≥ 3 alone insufficient (rigid-pocket example) | PROVED |
| Pockets at 2-separations are step-1/2 adjusters (Fan) | EXTERNAL |
| Three-escapable lemma; escapability from expansion | PROVED |
| Short nonzero-residue cycles, any α (Thm 1, Pass XVII) | PROVED |
| Free gadgets; gcd g₀ ∣ lcm(1..A+1) | PROVED |
| Anchoring + nesting: few rigid candidates | PROVED |
| Free-entry gadgets (pocket-2, pocket-≥3 mod p, Θ) | PROVED / G2 closed in outline |
| Chain with survival on escapable sets | SKETCH (G3) |
| M1 threading | SKETCH (design complete) |
| Mod 4 | REDUCED to G1′ (bipartite cores, pockets with ≥ 3 attachments) |
| ⇒ all residues mod odd k for bounded-degree 2-connected δ ≥ 3 expanders (Martinsson–Steiner Q, bounded degree) | conditional on G3 + routine linkage |
| ⇒ EG for 2-connected bounded-degree δ ≥ 3 expanders | conditional on G3, G1′, routine linkage |

## 5. What this does and does not mean

- **If the sketches close,** the expander pillar holds: EG for every 2-connected,
  bounded-degree expander with δ ≥ 3, plus a resolution of the Martinsson–Steiner question
  for bounded degree. These would be genuine theorems.
- **They do not prove EG.** A minimal counterexample need not be an expander. Pillar B
  (graphs with no large expanding piece, including low-connectivity gadget compositions)
  is untouched, apart from the observation that 2-separations supply Fan adjusters.
- **Before any external claim,** Passes XVII–XIX need a full write-up and independent
  refereeing. The M1 and G2 sketches also lean on standard but unchecked linkage
  statements in expanders.
