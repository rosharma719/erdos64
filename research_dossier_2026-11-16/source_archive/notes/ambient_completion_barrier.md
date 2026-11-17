# Pass XXV — Ambient completion: a global topological obstruction and a multiscale barrier

**Date:** 2026-11-16. **Goal:** Identify the strongest theorem supported by the literature review that constrains the proposed 'ambient connector-repair' route to Erdős–Gyárfás. This note does **not** prove the conjecture. No earlier shared solver has been modified.

## Status legend

- **PUBLISHED:** a theorem stated in the external mathematical literature.
- **PROVED:** a result with the complete argument below (not externally peer-reviewed).
- **COMPUTED:** an explicit finite sanity check by independent Python/NetworkX and C/BFS verifiers, with exit codes and identical stream checksums.
- **OPEN:** a proposed theorem not established here.

## 1. Crossing graphs measure 3-connectivity globally (PROVED; standard chord-diagram structure)

Let `G` be a simple cubic graph with a Hamiltonian cycle `C` on `n=2m` vertices. Every edge outside `C` belongs to a perfect matching `M`. Define its **chord-intersection graph** `I_C` to have one vertex per matching edge and an edge between two matching edges if their four endpoints alternate around `C`.

**Theorem 1.** `G` is 3-vertex-connected if and only if `I_C` is connected.

*Proof, forward.* Suppose `I_C` is disconnected. Choose one crossing-connected chord component `A` and a chord `f` outside it. A chord that crosses none of the chords in `A` has both endpoints in a single gap between consecutive endpoints of `A` on `C`. Here is the standard elementary argument: record, for each gap, on which side of each chord of `A` the gap lies. Gaps have distinct signatures, for otherwise the endpoints of `A` in an arc between two such gaps would be paired among themselves and would form a nonempty proper noncrossing partition of `A`, contradicting crossing-connectivity. A chord disjoint from `A` in the crossing graph has equal signatures at its two endpoints, hence they lie in one gap. Choose a gap containing both endpoints of `f`. All vertices internal to that gap are matched internally to the gap, since a matching edge leaving the gap would cross a chord of `A`. Deleting the two gap-boundary vertices disconnects its interior from the remainder of `C`, contradicting 3-connectivity.

*Proof, reverse.* If `G` has a vertex cut `{u,v}` of size at most two, the two open `u`–`v` arcs of the Hamiltonian cycle lie in distinct components of `G-{u,v}`. Hence no matching edge joins their interiors. The matching edges supported on the two sides (including any chords incident to `u` or `v`) cannot cross each other; both sides contain matching edges, so `I_C` is disconnected. A Hamiltonian graph already has no cut vertex, completing the proof.

This formulation is closely related to standard decomposability of chord diagrams. **Novelty is not claimed.**

**Two-chord length identities.** If two chords have alternating endpoints `a<b<c<d`, let the successive Hamiltonian arc lengths be `alpha=b-a`, `beta=c-b`, `gamma=d-c`, and `delta=n-(d-a)`. The two cycles using these chords have lengths

`alpha + gamma + 2` and `beta + delta + 2`,

whose sum is `n+4`. For two noncrossing chords, at least one corresponding pair-of-chords cycle also exists. A dyadic-free Hamiltonian cubic graph must avoid dyadic lengths among all such one- and two-chord circuits. This is **necessary**; it is not a sufficient condition. Cycles with three or more chords are essential in general.

## 2. No macroscopic chord-span theorem follows from 3-connectivity and fixed girth (PROVED)

**Theorem 2 (fixed-girth / bounded-span barrier).** For every fixed integer `g>=3`, there exist a constant `B(g)` and infinitely many simple **3-vertex-connected Hamiltonian cubic graphs** `X` with girth at least `g`, having a Hamiltonian cycle `C_X` such that every edge outside `C_X` has shorter cyclic span at most `B(g)` in the cyclic order `C_X`.

*Step 1 — an explicit 3-connected base with only local chords.* For any integer `m>=4`, start with the Hamiltonian cycle `(0,1,...,2m-1,0)` and add the perfect matching

`(0,2)`, `(2j-1,2j+2)` for `1<=j<=m-2`, and `(2m-3,2m-1)`.

Every chord has shorter cyclic span at most 3. Consecutive chords cross, and no nonconsecutive chords cross; the crossing graph is the path `P_m`. Theorem 1 therefore makes every base graph `B_m` 3-connected.

*Step 2 — choose a high-girth Hamiltonian cubic cap.* **PUBLISHED** existence of 3-connected Hamiltonian cubic graphs of arbitrarily prescribed girth follows, for example, from the established asymptotic facts for random cubic graphs (high-probability Hamiltonicity and 3-connectivity together with positive limiting probability of excluding any fixed finite set of short cycles). Fix one such graph `H` of girth at least `g`, with `h` vertices, a Hamiltonian cycle `D`, and a vertex `w` on `D`.

Let `P=H-w`. Its three terminals are precisely the neighbors of `w`, each of degree two in `P`. The two neighbors of `w` used by `D` are joined by the Hamiltonian path `D-w` in `P`, of length `h-2`. Every path in `P` joining two distinct terminals has length at least `g-2`, since adding the two edges to `w` would make a cycle in `H`.

*Step 3 — replace every vertex of `B_m` by `P`.* Identify the three former incident edges with the three terminals, assigning the two base-cycle edges to the endpoints of the Hamiltonian path `D-w` and the third to the remaining terminal. Distinct gadgets are joined by one edge for each original edge of `B_m`.

**3-connectivity:** The vertex-replacement operation preserves 3-connectivity when both capped graphs are 3-connected. Indeed, removing at most two vertices from the resulting 3-sum leaves either two connected vertex-deleted shores joined by a surviving attachment edge, or all components of a shore attached to a connected opposite shore; the distinct three attachment edges cannot all be deleted by two vertices. Iteration gives 3-connectivity of `X_m`.

**Hamiltonicity:** Traverse the Hamiltonian path `D-w` in each gadget, following the edges lifted from the base Hamiltonian cycle. This visits all `h-1` vertices of each gadget exactly once and yields a Hamiltonian cycle `C_m` of length `2m(h-1)`.

**Girth:** A cycle entirely inside one gadget has length at least `g`. Otherwise it traverses exactly two of the three external edges at each visited gadget; projecting gives a simple base cycle of length `L>=3`. Every transit through a gadget has at least `g-2` internal edges, so the lifted cycle has at least `L(g-1)>=3(g-1)>=g` edges.

**Bounded chord span:** Set `t=h-1`. Each gadget occupies `t` consecutive positions along `C_m`. An edge internal to one gadget has circular span at most `t-1`. Each external edge lifted from a base chord joins gadgets separated along the base Hamiltonian cycle by at most three positions, so its span is at most `3t+(t-1)<4t`. Hence `B(g)=4(h-1)` works independent of `m`. QED.

**Corollary.** Given any fixed exponent `k`, choose `g>2^k`. The family above excludes cycles of all lengths `4,8,...,2^k`, while all non-Hamiltonian edges have span bounded independently of graph order. Thus **three-connectivity plus any fixed finite list of forbidden dyadic lengths cannot force macroscopic shortcuts along a Hamiltonian cycle**. The construction may, and likely does, contain longer dyadic cycles. No counterexample to Erdős–Gyárfás is claimed.

## 3. Connectedness may be realized by a long chain (PROVED)

**Theorem 3 (quantitative chord-intersection diameter).** Let `G=C+M` be a 3-connected Hamiltonian cubic graph with `n` vertices and every matching chord of shorter cyclic span at most `B<n/2`. Then its connected chord-intersection graph satisfies

`diam(I_C) >= n/(4B)`.

*Proof.* Give each chord its shorter closed arc of length at most `B` on `C`. For crossing chords these two arcs must intersect, so any endpoint of one lies at circular distance at most `2B` from any endpoint of the other. Let `e` and `f` be the matching chords incident to opposite vertices of `C`. Along a crossing-graph path from `e` to `f`, circular distance between chosen endpoints can advance by at most `2B` per step. But the endpoints are `n/2` positions apart. Hence each such path has at least `n/(4B)` edges. QED.

Thus the connectivity forced in the bounded-span examples is **longitudinal**. It can organize into a crossing chain of diameter linear in graph order, rather than one shortcut spanning a positive proportion of the Hamiltonian cycle.

## 4. Explicit independent finite checks (COMPUTED)

Use `generate_fixtures.py` to construct the graphs from the 14-vertex Heawood graph (girth 6, 3-connected and Hamiltonian). Explicit fixtures have 104 and 156 vertices. A Python/NetworkX verifier and an independent C implementation using adjacency matrices, BFS girth, and exhaustive 1-/2-vertex deletion tests each check cubic degrees, 3-connectivity, girth, Hamiltonian cycle, and maximum chord span. They agree exactly:

- order 104, edges 156, connectivity 3, girth 6, chord span 39;
- order 156, edges 234, connectivity 3, girth 6, chord span 39.

For reproducibility, the `verification_manifest.md` records both exit codes and the matching entire SHA-256 output-stream hashes. This computation only illustrates the theorem; the all-order theorem is proved independently.

## 5. Research implications and exact open target

**OPEN.** A defensible positive replacement for the failed 'ambient shortcuts must be macroscopic' conjecture is a **bounded-span amplification theorem**:

> For every fixed `B`, does there exist `N(B)` such that every 3-connected Hamiltonian cubic graph of order at least `N(B)`, whose chords all have cyclic span at most `B`, has a power-of-two cycle?

An edge-avoiding version would be stronger. A proof would settle an infinite, highly nontrivial bounded-cyclic-bandwidth class and would provide a route to the **local-propagation** branch of a global argument. No proof or counterexample is known here. The construction in Theorem 2 does not contradict this proposed theorem: it only excludes a *fixed initial list* of dyadic cycle lengths.

The complementary branch requires long-range connectors. The revised high-level dichotomy is now: **many local crossings propagate length freedom over multiple scales, or sufficiently long connectors permit alternative global routes.** The previous theta-necklace arithmetic handles only the first step of propagation; absolute scale alignment remains open.

For a non-Hamiltonian 3-connected cubic graph, Tutte's induced nonseparating-cycle theorem and Lyngsie–Merker's theta-chain decomposition remain the most credible way to generate an analogous scaffold, but this extension also remains open.

**Strategic conclusion:** In the Erdős–Gyárfás setting, progress requires a scale-adaptive argument that uses *all* forbidden dyadic lengths up to a growing target or combines local chord interactions across a long chain. Connectivity and finite local exclusions cannot independently supply the missing length scale.

## Literature

- Lyngsie and Merker, *Cycle Lengths Modulo k in Large 3-connected Cubic Graphs*, Advances in Combinatorics (2021), https://doi.org/10.19086/aic.18971.
- Sachs' high-girth regular Hamiltonian graph existence is discussed in He–Luo–Xu, *Graphs and hypergraphs of prescribed girth and degrees with restricted cycles*, Discrete Mathematics (2026), https://doi.org/10.1016/j.disc.2025.114879.
- A convenient explicit statement that 3-connected Hamiltonian cubic graphs have arbitrarily prescribed girth appears in *On cycle lengths in claw-free graphs with com...*, available at https://home.zcu.cz/~ryjacek/publications/files/067.pdf (Fact 4, using standard random regular graph results).
- Thomassen, *Chords in longest cycles in 3-connected graphs*, JCTB (2026), https://doi.org/10.1016/j.jctb.2026.03.001, is relevant to the non-Hamiltonian extension, though it does not control chord span.
- Ducoffe and Dumitru, *Towards a more structured search for Erdős–Gyárfás counter-examples*, 2026, https://arxiv.org/abs/2609.28594.
