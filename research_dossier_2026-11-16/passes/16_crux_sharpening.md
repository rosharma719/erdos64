# Pass XVI — Sharpening the crux: rigid pockets, Fan adjusters, and the Martinsson–Steiner question

**Date:** 17 November 2026. **Status:** two proved lemmas, one proved counterexample (to
our own Target A as first stated), two external results identified as load-bearing, and
a corrected decisive conjecture. No claim of EG.

Notation follows Pass XV:
- G is an **α-expander** if |N(U)| ≥ α|U| whenever |U| ≤ n/2.
- For a cycle Q of length q and two of its vertices a, b, the **step** is the difference
  between the lengths of the two a–b arcs of Q.
- A vertex set S ⊆ V(Q) is **escapable** (towards a target Y, inside a host H) if H
  contains vertex-disjoint paths, one from each vertex of S to Y, internally disjoint
  from Q.

## 1. Target A, as first stated, is false (PROVED, modulo a standard expansion estimate)

**Proposition 1.** Fix an odd prime p. There are α = α(p) > 0 and arbitrarily large cubic
α-expanders in which every cycle of length > 5 has length divisible by p.

*Construction.*
1. Take cubic α₀-expanders Hₙ.
2. Subdivide every edge p − 1 times. This gives a c·α₀/p-expander Sₙ (Martinsson–Steiner,
   proof of Prop. 1.4, citing Krivelevich's survey, Prop. 4.2), and every cycle of Sₙ
   has length divisible by p.
3. To each subdivision vertex w attach, by a single edge, a private copy of
   B = K₄ with one edge subdivided, joining w to the subdivision vertex of B.

*Why it works.*
- **Degrees.** Every vertex now has degree 3: the subdivision vertices gain one edge, the
  blob's subdivision vertex gains one, and the K₄ vertices already have three.
- **Cycles.** Each attaching edge is a bridge, so every cycle lies inside one blob or inside
  Sₙ. Blob cycles have length ≤ 5. Every other cycle lies in Sₙ, so its length is
  divisible by p.
- **Expansion.** Attaching pendant pieces of bounded size to the vertices of a
  bounded-degree expander preserves α-expansion up to a constant factor. Group each vertex
  with its pendant blob into a unit of ≤ 6 vertices. A unit only partly inside U
  contributes a boundary vertex. Units wholly inside U inherit expansion from Sₙ, with the
  usual complement argument for sets above half size.

**Consequences.**
- Bounded degree, δ ≥ 3 and α-expansion together do **not** force long cycles of length
  ≢ 0 (mod p).
- So no exact-length theorem over a linear range can hold under those hypotheses alone.
  Pillar A needs connectivity.
- The example has bridges, so it is irrelevant to EG itself. Minimal counterexamples are
  2-edge-connected and almost biconnected (Ducoffe–Dumitru), and the blobs contain C₄
  anyway.

## 2. 2-separations are free adjusters (EXTERNAL, Fan 2002)

**Fan's lemma.** Fan, *J. Combin. Theory Ser. B* 84 (2002), Cor. 3.1. Special case as
quoted in Liu–Ma, arXiv:1508.07912, proof of Lemma 2.2. Let H be 2-connected, and let
every vertex of H other than two distinct vertices u, v have degree ≥ 3 in H. Then H
contains u–v paths R₁, R₂ with |R₁| ≥ 2 and 1 ≤ |R₂| − |R₁| ≤ 2.

**Corollary 2 (pocket adjusters).** Let G have δ ≥ 3, let (A, B) be a separation with
A ∩ B = {u, v}, and suppose (G[B], u, v) is a 2-connected rooted graph in the Liu–Ma
sense. Then every cycle of G that passes through B (entering at u, leaving at v) can be
re-routed inside B to change its length by 1 or 2, and by nothing else.

*Proof.* Every vertex of B − {u, v} keeps all its edges inside G[B]. Apply Fan's lemma in
G[B]. ∎

**Corollary 3.** In a 2-connected graph with δ ≥ 3, every edge uv lies on two cycles
whose lengths differ by 1 or 2. Hence every edge lies on a cycle of length ≢ 0 (mod p)
for every odd prime p, and on one of length ≢ 0 (mod 4).

*Proof.* Liu–Ma note that (G − uv, u, v) is a 2-connected rooted graph, and only u, v lose
degree. Apply Fan's lemma and close each path with uv. ∎

**Meaning for the program.** Low-connectivity structure (2-separations) cannot be rigid.
The pockets attached at two vertices are the very structure the known near-counterexamples
are built from (gadget compositions; 59–90% of vertices in triangles). They supply
step-1/2 adjusters automatically. The gcd problem lives entirely in **3-connected,
expanding** regions.

## 3. The three-escapable-vertices lemma (PROVED)

**Lemma 4.** Let Q be a cycle of length q, and let a, b, c ∈ V(Q) be distinct, with
cyclic gaps g₁, g₂, g₃ (so g₁ + g₂ + g₃ = q).
- (i) If p is an odd prime with p ∤ q, then some pair from {a, b, c} has step ≢ 0 (mod p).
- (ii) If 4 ∤ q, then some pair has step ≢ 0 (mod 4).

*Proof.* The pair at gap gᵢ has step ±(q − 2gᵢ).
- (i) If all three steps are ≡ 0 (mod p), then 2gᵢ ≡ q for each i. Summing gives
  2q ≡ 3q, so q ≡ 0, a contradiction.
- (ii) If all three are ≡ 0 (mod 4), then q ≡ 2gᵢ is even. Summing gives 2q ≡ 3q (mod 4),
  so q ≡ 0 (mod 4), a contradiction. ∎

**Lemma 5 (escapability from expansion, PROVED).** Let H be a β-expander on m vertices,
and Y ⊆ V(H) with |Y| > m/2 + k. Let Q be a cycle of H, Y ∩ V(Q) = ∅, with
q ≥ 2k/β + k. Then some k vertices of Q are escapable towards Y.

*Proof.* By Menger's theorem, otherwise a set S with |S| ≤ k − 1 separates V(Q) ∖ S from
Y ∖ S. Let U be the union of the components of H − S meeting V(Q) ∖ S.
- **U is not the big side.** If |U| > m/2, the complementary side contains Y ∖ S,
  of size > m/2. So |U| ≤ m/2.
- **Expansion bounds U.** N(U) ⊆ S, so β|U| ≤ |N(U)| ≤ k − 1, giving |U| < k/β.
- **But U is large.** |U| ≥ q − (k − 1) ≥ 2k/β + 1, a contradiction. ∎

**Consequence.** For every odd prime p, any cycle of length ≢ 0 (mod p) and at least
6/β + 3, placed in a β-expanding core, yields a usable adjuster with step ≢ 0 (mod p).
The adjuster is attached through two disjoint routes into the core, with no control
needed over *which* vertices escape. The same holds mod 4. The **position** half of the
Attachable Adjuster Lemma is therefore solved. What remains is to **find such cycles**.

## 4. The decisive problem is now a published open question

Martinsson–Steiner (*Cycle lengths modulo k in expanders*, arXiv:2204.09107):

- **Thm 1.3.** For α > 1/(p−1), where p is the least prime factor of k, every large
  α-expander has cycles of every residue mod k. Their proof is an adjuster chain: cycles
  Cᵢ of exponentially growing length, joined by short paths, with exits chosen outside a
  "bad" set of size ≤ |Cᵢ|/p + 1.
- **Prop 1.4.** For α < c/(p−1) the threshold is sharp, via subdivisions, which have δ = 2.
- **Open question (their §4).** For every α > 0 and odd k, does every sufficiently large
  **3-connected** α-expander have cycles of all residues mod k?

**Reduction (SKETCH — Lemmas 4–5 are proved; re-running Martinsson–Steiner's chain construction with entry and exit chosen among escapable vertices has not been checked line by line).** For prime k = p,
their question reduces to the following.

> (★_p) In every large 3-connected α-expander, every robust core (Lemma 3.1 of
> Martinsson–Steiner) contains a cycle of length ≢ 0 (mod p) and of length between
> 6/α + 3 and o(n).

Given (★_p), each new cycle in their chain contributes a step outside the stabiliser
(Lemma 4, entry and exit both chosen among three escapable vertices). So the sumset grows
to all of Z_p within p steps. Small-α failure then cannot come from position; it must come
from every robust core being mod-p rigid.

**Exactness for EG.** Assume (★_p) for every odd prime p ≤ A(α) + 1 and the mod-4
analogue. Primes p > A + 1 are handled for free by choosing the Friedman–Krivelevich window
to avoid multiples of p, and primes p > 1 + 1/α also by Martinsson–Steiner's Thm 1.3.
Then:
- Lemma 4 yields, for each such p, gadgets with step ≢ 0 (mod p).
- Taking h copies of a step value outside each prime, and outside 4, gives steps with gcd
  1 or 2. The coin-problem argument (Pass XV §3; Frobenius bound ≤ h²) then gives subset
  sums containing an interval of length A.
- With the M1 threading (still to be written), every even length in a linear range is
  realised. In particular there is a power-of-two cycle.

**The decisive conjecture, corrected (TARGET ★).** For every α > 0 there are n₀ and
C such that every 3-connected α-expander with bounded degree and n ≥ n₀ vertices has, in
every Martinsson–Steiner robust core, cycles of length in [C, C log n] that are ≢ 0
(mod p) for each odd prime p ≤ C, and ≢ 0 (mod 4).

**Evidence that ★ is the right target.**
- It is Martinsson–Steiner's open question (strengthened to robust cores).
- Its δ = 2 counterexamples are exactly the subdivision examples. The 1-connected cubic
  counterexample is Proposition 1, killed by 2-connectivity.
- By Fan (Corollary 3), every edge of a 2-connected δ ≥ 3 graph lies on cycles of two
  lengths differing by 1 or 2. That rules out global mod-p rigidity. What is missing is
  control of *where and how long* those cycles are, relative to a robust core.

## 5. Updated program (supersedes the M2 line of `../program/PROGRAM_2026-11-17.md`)

| ID | Statement | Status | Next step |
|---|---|---|---|
| L4 | three-escapable lemma | **PROVED** | — |
| L5 | escapability from expansion | **PROVED** | — |
| F | pocket adjusters at 2-separations (Fan) | **EXTERNAL** | use in Pillar B |
| P1 | δ ≥ 3 alone is not enough for exact lengths | **PROVED** (sketch of the expansion estimate) | write the estimate out |
| ★ | robust-core mod-p non-rigidity in 3-connected expanders | **OPEN** (Martinsson–Steiner question) | attack via Fan inside cores; see below |
| M1 | threading gadgets into the FK cycle | open, believed routine | write |
| A′ | EG and exact even lengths for 3-connected bounded-degree expanders | ⇐ ★ + M1 | — |

**Most promising attack on ★.** Fan's lemma already gives cycles of lengths differing by 1
or 2 through every edge. The gap is that it works in the whole graph, while ★ needs such
cycles inside a robust core and of bounded-log length.
- **Idea:** apply Fan to small 2-connected subgraphs H ⊆ core whose only low-degree
  vertices are two terminals. For example, take H = (ball of radius r) ∪ (a closing path),
  and use expansion to keep boundary effects to two vertices.
- **Alternative:** prove a "Fan with few defects" lemma. If a 2-connected rooted graph has
  all but O(1) non-root vertices of degree ≥ 3, are there still two u–v paths differing by
  1 or 2, perhaps of bounded length in an expander? Either version would settle ★ and,
  with M1, Pillar A′.

## Sources

- Martinsson–Steiner: https://arxiv.org/abs/2204.09107
- Fan, *Distribution of cycle lengths in graphs*, JCTB 84 (2002) 187–202 (statement
  checked as quoted in Liu–Ma): https://www.sciencedirect.com/science/article/pii/S0095895601920714
- Liu–Ma, *Cycle lengths and minimum degree of graphs*: https://arxiv.org/abs/1508.07912
- Friedman–Krivelevich: https://arxiv.org/abs/1912.11011
- Bondy–Vince, *Cycles in a graph whose lengths differ by one or two*, JGT 27 (1998)
