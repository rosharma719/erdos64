# Erdős–Gyárfás research, Run 8: girth-cycle overlap and scale escalation

Date: 17 November 2026. This document is standalone and the proof claims are independent of the computational searches. The code is evidence for finite claims and adversarial testing, not a proof of the full conjecture.

## Goal and prior work

The Erdős–Gyárfás conjecture says every finite graph with minimum degree at least three has a simple cycle whose length is a power of two. It remains open. Ducoffe–Dumitru (2026, arXiv:2609.28594, Lemma 2.1) prove that in a smallest hypothetical counterexample every edge belongs to a cycle of length `2^j+1`. This run asks whether those *near-dyadic* cycles must intersect in a way that forces a dyadic cycle. Earlier work established interval-forcing gadgets, a bounded 2-degenerate edge bound, and a three-terminal reformulation, but not the full conjecture.

## 1. General girth-cycle intersection lemma (proved)

Let `g=2h+1` be odd, and let G have girth at least g. If two distinct g-cycles share an edge, their intersection is a single path of length `t`, with `1 <= t <= h`.

Proof: Any two distinct simple x-y paths of length at most h would yield a cycle of length at most 2h < g. Hence any x-y path of length at most h is unique. Given two common vertices x,y on two g-cycles, the short x-y arcs in both cycles have length at most h and therefore coincide. Hence all shared vertices and edges form one common path, unless the cycles are identical. If the path had length >h, its endpoints would also be joined along the complementary C arc of length <h, which must belong to the other cycle, forcing equality. Thus t<=h. (The path case can equivalently be checked by taking a shortest gap between components of the intersection.)

The union of two such cycles contains a third simple cycle of length `2(g-t)`. If additionally `G` has no `C_{2g-2}`, then t cannot equal 1. Thus any two distinct g-cycles sharing an edge must share a path of length `2 <= t <= h`.

For `g=2^k+1`, the excluded `2g-2` is exactly `2^{k+1}`.

## 2. Scale-escalation theorem (proved)

**Theorem.** Let `g=2^k+1` with k>=2, and let G have girth g but no cycle of length `2g-2`. Suppose distinct g-cycles C,D share a path `P=v_0,v_1,...,v_t` with t>=2. If every internal vertex `v_i` has degree exactly three, then at least one such vertex has a third incident edge (outside P) that belongs to no g-cycle.

Proof: Assume every internal off-path edge e_i belongs to some g-cycle F_i. Since v_i is cubic and F_i uses e_i, it also uses exactly one of the two P edges incident to v_i. By the intersection lemma, F_i must share at least two consecutive P edges with *both* C and D; otherwise it would meet one of them in only one edge and force a forbidden `C_{2g-2}`. Since C,D diverge at both endpoints of P, F_i must follow P for at least two edges towards its chosen direction.

Write R if F_i leaves v_i towards v_{i+1}, and L if it leaves towards v_{i-1}. Necessarily F_1 chooses R and F_{t-1} chooses L. For t=2 these are incompatible at the same internal vertex, contradiction. For t>=3, among positions 1,...,t-1 there are adjacent positions i,i+1 with directions R,L. Their cycles F_i and F_{i+1} share the edge v_i v_{i+1}. At v_i the first cycle uses e_i while the second continues left on P; at v_{i+1} the first continues right on P while the second uses e_{i+1}. Hence they have no other common edge incident to their shared edge. By the intersection lemma their entire intersection is a single edge, producing a `C_{2g-2}`. Contradiction.

**Corollary for a smallest hypothetical counterexample.** If G is cubic, has girth `g=2^k+1`, and avoids all dyadic cycles, each such overlap path forces an edge lying on some longer `C_{2^j+1}` with `j>k`, via Ducoffe–Dumitru's edge-saturation lemma. Girth excludes the smaller scales and the theorem excludes scale k.

**Mixed-degree variant.** If internal vertices have degree >=3, every overlap path P has either an internal degree>=4 vertex or a degree-3 internal vertex whose third edge lies on no g-cycle.

**Counting corollary.** Let `nu_g` be the maximum size of a family of pairwise internally vertex-disjoint common paths of length >=2 between distinct g-cycles. Let `D_g` be the number of edges not lying on any g-cycle, and `H` the number of vertices of degree at least four. For a graph of minimum degree >=3, girth g odd >=5, and no `C_{2g-2}`:

`nu_g <= 2*D_g + H`.

Indeed, each path must be charged to one internal high-degree vertex or the off-path edge of an internal cubic vertex. Disjointness of interiors prevents reusing the high-degree vertex and an edge can be charged by at most two endpoints. For cubic G, `D_g >= ceil(nu_g/2)`. This is an explicit bridge between near-dyadic overlaps and edge counts. It is not yet a contradiction, because nu_g is not known to be large enough.

## 3. Global odd-girth forcing theorem (proved)

**Theorem.** For every odd g>=5, any cubic graph of girth g in which every edge lies on a g-cycle contains a cycle of length `2g-2`.

Proof: Assume no `C_{2g-2}`. Take a g-cycle C and any vertex v of C. Its unique third edge e is outside C. By the edge-cover assumption e is in a distinct g-cycle D. At v, D uses e and one of the two edges of C. Thus C,D share an edge, and by the intersection lemma they share a path of length at least 2. All internal vertices of the path are cubic, and their off-path edges are covered by g-cycles. This contradicts the scale-escalation theorem. QED.

In particular, if `g=2^k+1` (k>=2), then a cubic graph of girth g with all edges on near-dyadic g-cycles has a `C_{2^{k+1}}`. This is a genuine bounded-structure proof for a subclass of cubic graphs, **not** a proof of Erdős–Gyárfás. A smallest hypothetical counterexample may have edges with near-dyadic witnesses at several different scales, may have non-near-dyadic girth, and need not be cubic.

Originality note: edge-girth-regular and girth-regular cubic graphs have an extensive literature (e.g. arXiv:1802.01881; *Edge-girth-regular graphs*, JCTA 2018). The statements here are established by the supplied proof; research priority is not asserted.

## 4. Exact C9-pair census (computer checked twice)

Fix C=(0,1,...,8) and anchor the common edge (0,1). Represent the second C9 by its 8-edge 1-to-0 path with seven distinct intermediate vertices, each either one of 2..8 or a fresh vertex. Fresh vertices are assigned canonical consecutive labels. This enumerates precisely:

`sum_{r=0}^7 choose(7,r) * P(7,r) = 130922` labeled path assignments, before identifying isomorphisms. We reject the identical cycle, degree>3, and any C4, C8, C16. We check every input with two independent cycle oracles: an incremental exact-path search and a direct complete static cycle DFS. Every accepted input is also checked with NetworkX's independent simple-cycle enumerator.

- **151** assignments give distinct C9 cycles whose union is subcubic and contains no C4, C8 or C16.
- Only **9** also have girth at least 9. Their shared path lengths are 2 (2 assignments), 3 (3), 4 (4).
- These are counts of **labeled local embeddings**, not nonisomorphic cubic graphs or a complete graph census.

For a fixed g=9 cycle, two distinct g-cycles sharing one edge with no further shared vertices would create C16. In a graph of girth9, every shared edge must be part of a shared path of length 2, 3 or 4.

## 5. Two near-dyadic ears sharing a spoke (67 patterns, 27 valid)

Fix C9 with cyclic vertices 0..8. Attach two external paths from root0 ending at distinct vertices b,c from {2,...,7}. Each external path joins root to target with length `9 - distance_C(0,target)` and the paths share an initial prefix of length s>=1, branching into internally disjoint tails. Every graph constructed is a subdivision of K4, hence has exactly seven simple cycles. The seven cycle lengths have independent closed forms in `research_run8.py` (`ear_algebra`) and agree with a NetworkX full simple-cycle enumeration for **all 67 possible parameter triples (b,c,s)**.

There are **27** cases with girth >=9 and no C16. Thus two or even more C9 witnesses can overlap without forcing a dyadic cycle.

**Antipodal-fork obstruction (analytic, all odd scales).** For g=2h+1, choose the two antipodal vertices b,c at C-distance h from root a, which are adjacent along C. If g-cycle ears of length h+1 from a to b and c share a prefix of length s>=1 and are disjoint after branching, then their two tails plus edge bc make a cycle of length `2h+3-2s`. Girth g forces s=1; the complementary b-c arc of C instead gives a cycle of length `4h=2g-2`. Consequently, in a graph of girth g with no C_{2g-2}, this pair of near-girth witnesses cannot both exist. The finite g9 test finds no valid (b,c)=(4,5).

**A complete local obstruction to a too-strong claim.** At b=3,c=6,s=3, the graph is the uniform 3-subdivision of K4: 16 vertices, degree 2 or 3, girth9, exactly four C9s and three C12s, no C4/C8/C16. Every edge belongs to **exactly two C9s**. Thus even simultaneous near-dyadic edge coverage and abundant pairwise overlap do not force a dyadic cycle without minimum degree three.

More generally, for every odd k>=3, let `m=(2^k+1)/3`. The uniform m-subdivision of K4 is 2-connected and subcubic, has girth `3m=2^k+1`, and all cycles have length `3m` or `4m`, neither dyadic. Every edge belongs to two C_{2^k+1}'s. Its degree-three proportion is `2/(3m-1)`; the long corridors have degree two. This explicitly identifies the degree-three requirement as essential.

## 6. An infinite obstruction to replacing minimum degree with average degree (exact)

The graph6 string `GxaGiC` represents a simple 8-vertex graph with exactly 11 edges, no C4 or C8, and **every edge on a C3 or C5**. The program gives a cycle-edge certificate for each of the 11 edges.

Take t copies and identify their vertices labeled 0 to one common vertex. Result:

- `n=7t+1` vertices and `e=11t` edges;
- all simple cycles stay in one 8-vertex block, hence no C4,C8,C16 or any other dyadic cycle;
- every edge still lies on a triangle or pentagon;
- average degree `22t/(7t+1)>3` for every integer t>=4.

At t=4 this is an explicit connected 29-vertex, 44-edge example, average degree 88/29=3.03448..., checked by full simple-cycle enumeration and edge witnesses. **It is not an Erdős–Gyárfás counterexample**: it has many degree-two vertices, and is not 2-connected. It shows that average degree above three **plus near-dyadic edge-saturation** does not suffice; minimum degree and the minimal counterexample's connectivity restrictions really matter.

## 7. Computational test of the local scale-escalation theorem

`scale_escalation_check.py` builds two C9s sharing a path of t edges, t=2,3,4, and exhaustively searches for a third C9 through the new external edge at vertex1, canonicalizing all fresh vertices, maintaining degree<=3, girth>=9 and excluding C16.

| Shared path t | Search states | Admissible extensions at vertex1 |
|---|---:|---:|
| 2 | 27 | 0 |
| 3 | 43 | 4 |
| 4 | 41 | 3 |

All 7 positive extensions at t=3,4 were separately checked by NetworkX exhaustive simple-cycle enumeration. This confirms why the theorem for t>=3 guarantees *some* un-covered internal off-edge, not that *each* such edge is uncovered.

## 8. What remains open; research order

1. **Near-dyadic intersection forcing:** Prove that overlap paths occur with enough internally disjoint coverage in any smallest counterexample and bootstrap the scale-defect inequality. The current theorem requires odd girth equal to a near-dyadic length; removing that assumption is a central obstacle.
2. **Edge counts:** Combine `nu_g <= 2D_g+H` with minimal-counterexample restrictions `H < n/3` and the previously checked weak `|E(G)|<=2n-5`. Neither bound currently produces a contradiction in predominantly cubic graphs.
3. **Gadgets:** Use explicit K4-subdivision obstructions as tests for any claimed local forcing; account for the third edge at every degree-three corridor vertex.
4. **Multiscale:** Develop a recurrence for the numbers of edges whose shortest near-dyadic witness scale is k, hopefully forcing an impossible growth beyond `log_2 n`.
5. **SAT/exact search:** Test sharply formulated lemmas against high-girth cubic data and finite patch embeddings, without treating finite search as an exhaustive proof of the general conjecture.

## Sources

- G. Ducoffe and B. Dumitru, *Towards a more structured search for Erdős-Gyárfás counter-examples* (2026), Lemma 2.1 and structural bounds: https://arxiv.org/html/2609.28594
- *Edge-girth-regular graphs* (2018): https://www.sciencedirect.com/science/article/pii/S0195669818300787
- *Girth-regular graphs* (2018): https://arxiv.org/abs/1802.01881
- D. Garcia, *Small graphs without power-of-two cycles* (2026), gadget window calculus: https://arxiv.org/abs/2609.04686

**Status:** a rigorous restricted forcing theorem, a rigorous local scale-escalation theorem, an overlap-packing/defect inequality, exact finite certificates, and an infinite counterexample to an overstrong average-degree route. The full Erdős–Gyárfás conjecture remains open.
