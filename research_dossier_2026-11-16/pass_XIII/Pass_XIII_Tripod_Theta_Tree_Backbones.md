# Pass XIII — Tripod–theta tree backbones, exact root avoidance, and a rank-two dyadic obstruction

**Date:** 16 November 2026 (continuation). **Status:** internally proved exact structural lemmas; independent small-graph certificates and finite exploratory census; the Erdős–Gyárfás conjecture, the rooted prime conjecture, and bridge-stability remain **OPEN**. **No publication-priority or novelty assertion** is made for these derivations.

## 1. Strategic change and published input

Previous passes used exact bridge predecessors, a fractional dyadic-cycle resilience LP, theta-necklace additive spectra, and Hamiltonian chord switching. The principal gap remains *forced exact dyadic lengths*. A more general geometric substrate is available from published work on decycling sets:

- Payan–Sakarovitch, strengthened by **Nedela–Seifrtová–Škoviera**, *Decycling cubic graphs*, Discrete Mathematics (2024), https://arxiv.org/abs/2309.11606 and https://www.sciencedirect.com/science/article/pii/S0012365X24001705. Every cyclically four-edge-connected cubic graph admits a **coherent decycling partition** \(V(G)=T\sqcup J\), where \(G[T]\) is an induced tree; if \(n\equiv2\pmod4\), \(J\) is independent, whereas if \(n\equiv0\pmod4\), \(G[J]\) has exactly one edge. The minimum decycling-set cardinality is \(\lceil(n+2)/4\rceil\).
- **Kingan–Kingan**, *On cyclically 4-connected cubic graphs*, AKCE International Journal of Graphs and Combinatorics (2024), https://doi.org/10.1080/09728600.2024.2333397. Prime cubic graphs are accessible using admissible edge-bridging from certain ladder bases, with the paper's stated exceptions and restrictions.

This provides an **induced-tree representation for non-Hamiltonian prime cubic graphs**, overcoming the Hamiltonicity restriction of our earlier chord machinery. We study the \(n\equiv2\pmod4\) case first, for which the connectors \(J\) are independent.

Throughout, write \(s=|J|\ge3\). Since \(G\) is cubic, \(G[T]\) a tree, and \(J\) independent, counting the \(3s\) edges from \(J\) to \(T\) gives

\[
3s=3|T|-2(|T|-1)=|T|+2,\qquad |T|=3s-2,\qquad |G|=4s-2.
\]

Each \(j\in J\) has three neighbors in \(T\), viewed as a **tripod connector**. Every choice of two neighbors \(a,b\in N(j)\) closes the unique tree path \(P_T(a,b)\) into a **one-connector fundamental cycle** of length \(d_T(a,b)+2\).

## 2. The tree-edge congestion theorem (proved)

**Theorem A.** Let \(G\) be a simple cyclically four-edge-connected cubic graph with \(G[T]\) a tree and \(J\) independent. For any tree edge \(h\in E(T)\), let \(T-h\) split into components \(A_h,B_h\), and define

\[
X_h=\{j\in J:N(j)\cap A_h\ne\varnothing\ne N(j)\cap B_h\}.
\]

Then:

1. If \(h\) is incident to a leaf of \(T\), then \(|X_h|=2\).
2. Otherwise, \(|X_h|\ge3\).
3. For every pair of distinct connectors \(j,k\in X_h\), there is a simple cycle containing exactly \(j,k\) from \(J\), **avoiding the tree edge \(h\)**. The cycles given by different pairs \(\{j,k\}\) are distinct. Hence each internal tree edge certifies at least \(\binom{|X_h|}{2}\ge3\) such two-connector cycles.

**Proof (parts 1–2).** Since each \(j\) has three tree neighbors, assign \(j\) to the component of \(T-h\) containing at least two of its neighbors. The resulting vertex bipartition of \(G\) has exactly \(1+|X_h|\) crossing edges: \(h\), plus one minority attachment from each mixed connector. Cubic 3-connectivity implies that this edge cut has size at least 3, so \(|X_h|\ge2\). If \(h\) is a leaf edge, the leaf has exactly two J-neighbors; precisely those two connectors are mixed, so equality holds. For an internal tree edge, both sides of the cut contain at least two tree vertices. A three-edge cut in a cyclically four-edge-connected cubic graph must be trivial (isolate one vertex): an acyclic component attached through three edges must be a singleton by the cubic degree sum \(3t=2(t-1)+3\). Thus \(1+|X_h|\ne3\), and \(|X_h|\ge3\).

**Proof (part 3, exact XOR formula).** For each \(j\in X_h\), choose a neighbor on each side of \(h\), and denote their tree path by \(P_j\). Its fundamental cycle \(C_j\) consists of \(P_j\) and the two edges incident to \(j\). For distinct \(j,k\), paths \(P_j,P_k\) intersect in a nonempty path \(Q\) containing \(h\), since simple paths in a tree have connected intersection. The symmetric difference \(C_j\triangle C_k\) is a **single simple cycle**, using just \(j,k\) among the connectors and avoiding \(Q\)'s edges. It has exact length

\[
\boxed{|C_j\triangle C_k|=|P_j|+|P_k|-2|Q|+4.}
\]

Different connector pairs give different cycles. QED.

**Aggregate congestion corollary.** If \(\ell\) is the number of leaves of \(T\), then, writing \(S_j\) for the minimum subtree of \(T\) spanning \(N(j)\),

\[
\boxed{\sum_{j\in J}|E(S_j)|=\sum_{h\in E(T)}|X_h|\ge3(|T|-1)-\ell.}
\]

This converts cyclic four-connectivity into an exact **threefold internal-edge cover by tripods**, strengthening the twofold cover that mere 3-edge connectivity gives. It supplies topological switching opportunities on every internal tree edge, but the theorem gives no dyadic-length guarantee.

## 3. All roots admit cycles using at most two connectors (proved)

**Theorem B.** Let \(G\) be any simple cubic graph admitting an induced-tree partition \(V(G)=T\sqcup J\), with \(J\) independent and \(|J|\ge3\). For every vertex \(r\in V(G)\), **some simple cycle avoiding \(r\)** contains at most two vertices of \(J\).

**Proof.** If \(r\in J\), choose any other connector \(j\) and its fundamental cycle. If \(r\in T\) and \(\deg_T(r)\le2\), then at most \(3-\deg_T(r)\le2\) connectors neighbor \(r\), so choose \(j\) not adjacent to \(r\). Its three neighbors lie in at most two components of \(T-r\); two lie in the same component. Their fundamental cycle avoids \(r\).

For \(r\in T\) with \(\deg_T(r)=3\), let \(B_1,B_2,B_3\) be the components of \(T-r\). If some connector has two neighbors in one \(B_i\), its fundamental cycle avoids \(r\). Otherwise each connector has exactly one neighbor in **each** \(B_i\). Choose two distinct connectors \(j,k\) and two branches \(B_p,B_q\). Join their respective attachment points by the unique paths inside \(B_p\) and \(B_q\). Together with the four connector edges, these form one simple cycle avoiding \(r\) and using only \(j,k\). QED.

**Important:** The conclusion concerns cycles of *arbitrary* lengths. It does **not** establish a power-of-two cycle. The two-connector restriction is a new precise structural target for our additive methods, not an Erdős–Gyárfás result.

## 4. The exceptional root normal form: three trees and a theta pencil (proved)

**Theorem C (exact one-connector obstruction).** Let \(r\in T\) have tree degree three. There is no **one-connector** cycle avoiding \(r\) if and only if **every connector \(j\in J\) has exactly one neighbor in each** of the three branches \(B_1,B_2,B_3\) of \(T-r\).

If this occurs, each branch has exactly \(s-1\) tree vertices, and for **any** two distinct connectors \(j,k\) the subgraph consisting of their three branch routes is a theta graph. Let \(a_i(j)\) denote the unique neighbor of \(j\) in \(B_i\) and define three tree pseudometrics on the connector labels,

\[
d_i(j,k)=d_{B_i}\big(a_i(j),a_i(k)\big),\qquad i=1,2,3.
\]

The three simple **two-connector** cycle lengths associated with \(j,k\) are exactly

\[
\boxed{4+d_1(j,k)+d_2(j,k),\quad
       4+d_1(j,k)+d_3(j,k),\quad
       4+d_2(j,k)+d_3(j,k).}
\]

**Proof.** A one-connector fundamental cycle avoids \(r\) exactly when its two chosen tree neighbors lie in the same branch; hence the characterization. Each branch \(B_i\) is a tree connected to \(r\) by one edge. Cubic degree summation gives \(|E(B_i,J)|=3|B_i|-2(|B_i|-1)-1=|B_i|+1\). Every \(j\) meets each \(B_i\) exactly once, so \(|E(B_i,J)|=s\), and \(|B_i|=s-1\).

For fixed \(j,k\), the route \(j-a_i(j)-P_{B_i}(a_i(j),a_i(k))-a_i(k)-k\) has length \(d_i(j,k)+2\). The three routes have disjoint interiors because the \(B_i\) are disjoint. Any two routes form a simple cycle, with the displayed lengths. Conversely **every cycle avoiding \(r\) and containing exactly two connectors** must use exactly two branches and is one of these theta cycles. Thus there are precisely \(3\binom{s}{2}\) distinct two-connector root-avoiding cycles, whose length multiset is explicitly determined by the three tree metrics. QED.

**Research consequence.** In this normal form, rank-two dyadic forcing becomes a **three-tree simultaneous distance-sum problem**. For target \(q=2^k\), the relevant equations are \(d_p(j,k)+d_q(j,k)=q-4\). Higher-rank cycles correspond to compatible linkages among three or more connectors. This is a concrete extension of our theta-necklace/cycle-switching program beyond Hamiltonian graphs.

## 5. Sharp prime obstructions to a rank-two *dyadic* theorem

### Petersen (10 vertices)

Take graph6 `IkE?ISqJ?`, root \(r=0\), and \(J=\{7,8,9\}\). The tree has three branches of two vertices. Every pair of connectors has branch-distance vector equal to a permutation of \((0,1,1)\). Thus all its root-avoiding two-connector cycles have length \(5\) or \(6\), and no root-avoiding one-connector cycle exists. Nevertheless,

`3-4-7-6-5-9-2-8-3`

is a simple **8-cycle** avoiding root 0. It contains **all three** connectors. The graph is the Petersen graph and is cyclically four-edge-connected.

### A 14-vertex cyclically four-connected cubic obstruction

Take graph6 `MHEIGC@AM?AD_CGO_`, root \(r=9\), and \(J=\{0,1,3,7\}\). The tree is induced, \(J\) independent, and the three branches at the root each have three vertices. The six unordered connector pairs give the following complete distance/length data:

| Connector pair | Distances \((d_1,d_2,d_3)\) | Three two-connector cycle lengths |
|---|---|---|
| 0,1 | 2,1,0 | 7,6,5 |
| 0,3 | 2,1,1 | 7,7,6 |
| 0,7 | 1,1,2 | 6,7,7 |
| 1,3 | 0,2,1 | 6,5,7 |
| 1,7 | 1,0,2 | 5,7,6 |
| 3,7 | 1,2,1 | 7,6,7 |

Hence **no root-avoiding 4- or 8-cycle uses one or two connectors** in this coherent partition. But

`0-5-6-1-2-3-11-10-0`

is a simple root-avoiding **8-cycle** using exactly three connectors (0,1,3).

The independent certificate checker verifies: all 14 vertices have degree three; node connectivity is three; all 14 three-edge cuts are trivial; the listed tree and branch attachments; every entry in the metric table; and every edge and distinct vertex of the explicit 8-cycle. No claim that the *graph* requires three connectors for **every alternative decycling partition** is made. The necessity of three is relative to the displayed partition.

**Falsified candidate.** “For every coherent partition and every root in a cyclically four-connected cubic graph, a dyadic cycle avoiding that root can be found using at most two connectors” is **false already at orders 10 and 14**. This is why proving only rank-two theta lengths cannot settle rooted Erdős–Gyárfás in general.

## 6. Exact parity-state transfer under bridging (proved)

These transformations connect our new tree model to the old four-predecessor bridge calculus. A *TT* edge has both ends in the induced tree, *TJ* joins tree to connector, and *JJ* joins two connectors.

**Theorem D (explicit partition updates).** Suppose a cubic graph \(G\) admits a coherent decycling partition \(T\sqcup J\).

- If \(J\) is independent and two vertex-disjoint **TT** edges are bridged, put one subdivision vertex into \(T'\), the other into \(J'\). Then \(J'\) is independent and \(G'[T']\) is a forest with **exactly two trees**.
- If \(J\) is independent and at least one of the two bridged edges is **TJ**, assign one subdivision vertex to \(T'\) and one to \(J'\), choosing the latter on a TJ edge. Then \(G'[T']\) is a **tree** and \(G'[J']\) has **exactly one edge**.
- If \(G[J]\) has exactly one edge **JJ** and that edge is one of the two bridged edges, assign **both** subdivision vertices to \(T'\). Then \(G'[T']\) is a **tree** and \(J\) is **independent** in the child.

**Proof.** Inspect only the changed edges: subdividing a TT edge with a T vertex preserves tree connectivity; a T subdivision on a TJ edge creates a new tree leaf; a J subdivision on a TT edge deletes one tree edge and leaves two tree components; a J subdivision on a TJ edge joins one old J endpoint and creates the unique JJ edge; subdividing the unique JJ edge by a T vertex deletes the sole JJ edge and attaches a new tree leaf through the other new subdivision vertex. The bridge edge joins the two new vertices, and in every case the induced subgraph and connector-edge counts have the claimed structure. QED.

These are **sufficient update rules for specified bridge types**. They do not assert that all admissible bridges preserve one fixed coherent partition locally, or that the dyadic-cycle property follows from these transitions. Bridging two TT edges is particularly interesting: the natural induced-tree state becomes the *two-forest alternative* from the earlier Payan–Sakarovitch theorem, making the need for a structural pivot explicit.

## 7. Finite checks and scope

The scripts in this pass check these statements by two independent styles: constructive graph/path/XOR assertions, and exact graph6 certificates checked against graph connectivity and explicit cycles. A separate search over all coherent decycling partitions minimized, for each graph, the **largest minimum connector count** needed to find a dyadic cycle avoiding a prescribed root.

| Graph order | Generated prime cubic classes | Best rank 1 | Best rank 2 | Best rank 3 |
|---:|---:|---:|---:|---:|
| 8 | 2 | 0 | 2 | 0 |
| 10 | 5 | 4 | 0 | 1 (Petersen) |
| 12 | 18 | 14 | 4 | 0 |
| 14 | 84 | 70 | 14 | 0 |
| 16 | 607 | 551 | 56 | 0 |

“Best rank \(t\)” means **some coherent partition** permits, for **every root**, a root-avoiding dyadic cycle using at most \(t\) connectors, but no coherent partition permits the same with \(t-1\). Counts are based on the previous bridge-generated class list plus new exhaustive partition scans; the order-16 generation is not independently certified beyond the previous tests. In particular, the graph-specific 14-vertex obstruction above does admit an *alternative* coherent partition with lower dyadic rank. The table does **not** establish that fixed low rank suffices in unbounded graph order.

Additional structural regression: a parametrized family of cubic three-arm graphs of orders 10, 14, 18, 22, and 26 was tested. Every tree edge satisfied Theorem A, and the constructive Theorem B produced a root-avoiding cycle with at most two connectors for every root. These are sample tests of the formulas, not evidence of an unproved dyadic forcing lemma.

A randomized search of 20,000 slot-permutation configurations for each of orders 26, 30, and 34 found **no** graph avoiding both 4- and 8-cycles. This is only a negative randomized search. Published small-order enumeration already explains why the order-26 search was extremely unlikely to find such an example: all 23 connected cubic order-26 graphs avoiding both lengths reportedly contain triangles, whereas the three-arm family is triangle-free. See https://github.com/oaustegard/experiments/blob/main/erdos-gyarfas/note.html (external, not independently reproduced here).

## 8. Research decision and next proof target

**The exact topological part of a low-rank switching theorem is now available** for every prime cubic graph of order \(2\pmod4\): two-connector root-avoiding cycles exist, and internal tree edges are spanned by at least three interacting tripods. Its failure to force powers of two is illustrated by a fully explicit prime 14-vertex graph.

A better next objective is a **metric-array dispersion or renewal theorem**:

> Identify global structural conditions, stronger than the three-edge-cut congestion inequalities, under which the combined spectra of one-, two-, and three-connector cycles must hit a power of two at a scale tied to the tree size. The theorem should be compatible with Petersen and the displayed 14-vertex rank-two obstruction; a rank-two-only universal forcing statement is already false.

The three-tree pseudometrics \(d_1,d_2,d_3\) give an unusually concrete test-bed for additive combinatorics, including triangle inequalities, degree capacities, and simultaneous path incompatibility. Our existing exact bridge-transfer and fractional-resilience work should remain as the inductive skeleton, with tree-partition **state changes** replacing ad hoc chord gadgets. The \(n\equiv0\pmod4\) near-independent case will require tracking a single connector-to-connector edge or two-forest state.

**No proof of Erdős–Gyárfás or the rooted prime conjecture is claimed.** All universal assertions above are self-contained elementary derivations whose novelty would need targeted review beyond the cited structural antecedents.

## Reproduction

```bash
python pass13_tree_backbone.py
python pass13_prime_certificate.py
python pass13_prime14_audit.py
python pass13_prime14_optim.py
python pass13_prime16_optim.py
python decycling_exhaustive.py
```

Primary artifact: `Pass_XIII_Tripod_Theta_Tree_Backbones.md`.
