# Erdős–Gyárfás proof program: matching-amplified flexibility and its limits

17 November 2026. All graphs finite, simple, undirected unless indicated.

**Status:** No proof of the full Erdős–Gyárfás conjecture is claimed. The mathematical statements below have proofs. The computational data checks explicit examples only, and the literature priority of the derived lemmas has not been established.

## Definitions

A *saturated triangle* in a cubic graph G is a triangle abc whose three edges leaving {a,b,c} all lie in pentagons. In a cubic graph with no C4 and C8, the local overlap argument in the previous packet establishes that each such triangle belongs to a seven-vertex **T gadget**: a triangle abc, a center w, three ports x,y,z, and edges abc (triangle), a-x,b-y,c-z,w-x,w-y,w-z. Every port has one additional external edge; the other four vertices have all cubic neighbors inside. A single T has, for each pair of distinct ports, internally simple paths of lengths exactly 2,3,4,5,6. Distinct saturated T's are vertex-disjoint if G is C4,C8-free; see the previous packet's structural proof.

## Theorem 1: Weighted-cycle lifting

Let H be a cubic graph (or a cubic multigraph with no loops or parallel edges on the selected cycle). Let S be any set of vertices, and construct G by replacing each v in S by a T gadget, attaching its three incident edges bijectively to the gadget's ports. For every simple cycle C of H of length L, with r=|V(C)∩S|, G contains a simple cycle of each integer length from L+2r to L+6r inclusive.

**Proof.** For each ordinary vertex of C, traverse the same vertex as in H. For a marked vertex, route between the two ports selected by the cycle through a T-internal path of any length 2 through 6. The two connector edges replace the original two cycle edges, increasing the resulting length by 2 through 6 at each marked vertex. Choices at distinct marked vertices are vertex-disjoint. All sums of r independent integer contributions 2..6 occur, giving exactly the interval [L+2r,L+6r]. QED.

**Forcing corollary.** If 2r>=L, this interval contains a power of two, because L+6r>=2(L+2r) and every interval [a,2a] contains a power of two.

## Theorem 2: Perfect matching amplifies the flexibility density

Let H be a **bridgeless cubic graph with N vertices** and S⊆V(H). If |S|>=N/2, the partially inflated G contains a power-of-two cycle.

**Proof.** By Petersen's perfect matching theorem, H has a perfect matching M. Since H is cubic, deleting M leaves a 2-factor, a disjoint union of cycles C_1,...,C_j covering every vertex. If every such cycle contained fewer than half marked vertices, summing would give |S|<N/2. Therefore some C_i contains r>=|C_i|/2 marked vertices. Theorem 1 forces a dyadic cycle. QED.

This applies to *all bridgeless cubic bases*, not just Hamiltonian or vertex-transitive bases. It is a theorem for a restricted infinite family and is not a reduction of the full Erdős–Gyárfás conjecture.

## Theorem 3: Density obstruction in hypothetical cubic counterexamples

Let G be a **bridgeless cubic graph with no power-of-two cycles**, with n vertices, and let t be its number of saturated triangles. Then

    8t < n.

**Proof.** As G has no C4 or C8, each saturated triangle gives a T gadget, and these are vertex-disjoint (previous packet). Contract all T gadgets, each to one vertex, to obtain H. There are N=n−6t vertices, of which t are marked. We verify H is simple cubic:

- A port-to-port edge inside the same T would close a C4 with the length-3 internal port-to-port path.
- Two edges between two T gadgets would close a C8 using a 3-edge internal port-to-port path in each gadget and the two connector edges.
- Two ports of one T connected to the same ordinary vertex would close a C4 using the 2-edge internal path through the center.

Consequently no loops or parallel edges arise upon contraction and each contracted gadget vertex has degree three. Contracting connected subgraphs cannot make an original non-bridge external edge into a bridge, so H is bridgeless. If 2t>=N, Theorem 2 would supply a dyadic cycle in G. Thus 2t<N=n−6t, or 8t<n. QED.

**Interpretation.** A smallest counterexample *if cubic* is bridgeless as a smallest **general** counterexample by Ducoffe–Dumitru (2026). It could therefore contain at most floor((n−1)/8) saturated triangles. This theorem says nothing quantitative about unsaturated triangles and is not enough to prove their nonexistence.

## Theorem 4: Quantitative scarcity of pentagon-covered edges

If G is triangle-free, cubic, has n vertices, and has no C4 and no C8, at least 5n/14 of its edges belong to **no 5-cycle**.

**Proof.** By the pentagon overlap lemma from the previous packet, the subgraph U of edges lying on C5 has components of two types: a single pentagon (5 vertices, 5 edges) or two pentagons sharing a length-2 path (7 vertices, 8 edges). Let p5,p7 count the two types and n0 count vertices not in U. Then n=n0+5p5+7p7. G has 3n/2 edges, whereas U has 5p5+8p7 edges. Hence the number of edges not belonging to any C5 is

    u = (3n0+5p5+5p7)/2,

and

    u - (5n/14) = (8n0+5p5)/7 >=0.

QED.

In a minimal counterexample that is triangle-free and cubic, the edge-saturation theorem of Ducoffe–Dumitru therefore forces at least 5n/14 edges to have their **shortest** (2^k+1)-cycle witness at length at least nine. This counts edges, not distinct witnesses.

## Falsification: the short-cycle edge-cover theorem does NOT extend to arbitrary minimum degree >=3

There is an explicit 165-vertex 4-regular graph A with:

* no 4-cycle,
* no 8-cycle,
* every edge on a triangle.

Construction: Start with the Petersen graph P, select the mod-11 edge voltages listed in `high_degree_obstruction.json`, and build the corresponding 11-fold cyclic lift B. Every simple cycle in P of length 5,6,7,8 has nonzero total oriented voltage modulo 11, and P has girth five. Thus B has girth >=9 (any shorter lift cycle would project to a reduced closed walk of length <=8 in P; such a walk must project to a simple cycle because P has girth five). B has 110 vertices, cubic. Let A=L(B), its line graph. A has 165 vertices and is 4-regular. Every edge of A lies in a triangle formed by the three B-edges incident to some B-vertex. If A contained a cycle of length 4 or 8, the corresponding 4 or 8 distinct edges of B could not form a forest: the line graph of any subcubic forest is a block graph with maximal cliques of size <=3, so has no simple cycle of length >=4. Thus these edges would include a cycle in B of length <=8, contradicting girth(B)>=9. QED.

The code separately reads the complete 330-edge certificate, independently checks degrees, every-edge-in-triangle, and the absence of C4/C8 with exact bounded DFS. This is a *counterexample to the proposed high-degree extension of the local theorem*, not to Erdős–Gyárfás. In fact A has other dyadic cycle lengths.

## Reproduction

Python 3 with `networkx` installed for the construction only:

    python weighted_gadget_theorem.py
    python independent_verify.py
    python high_degree_obstruction.py
    python verify_high_degree.py

`independent_verify.py` and `verify_high_degree.py` use only the Python standard library and do not import the constructors. Generated edge lists and JSON certificates are in this folder.

- All 16 marked subsets of K4 and six marked subsets of the Petersen graph were checked, producing 22 literal dyadic cycle certificates.
- The fully inflated K4 (28 vertices) and Petersen (70 vertices) examples were independently shown to contain C16 and avoid C4 and C8.
- The 165-vertex 4-regular graph's full edge list has SHA-256 `17e911bc7240f37b5d055c75a94ac2abbad57179721512a61c61a05687cb20e8`.

## Strategic conclusion

Theorem 2 converts independent reroutings on a 2-factor into a dyadic cycle, which is a clean *global forcing* mechanism. Theorem 3 provides a quantitative restriction for a hypothetical cubic counterexample. Theorem 4 forces many edges to have long near-dyadic witnesses in the triangle-free cubic case. The explicit 4-regular construction demonstrates why the short-cycle cover method cannot be naively extended from cubic to all minimum-degree-3 graphs.

**Critical missing step:** Prove that every hypothetical smallest counterexample supplies sufficiently many independent reroutings at *some scale*, or find a reduction that handles the high-degree vertices and the triangle-free, long-girth case. No present result establishes this. The local and counting results alone are insufficient for a full proof.

## Sources

- Ducoffe and Dumitru (2026), arXiv:2609.28594: https://arxiv.org/html/2609.28594 (minimal counterexamples, edge cycle saturation and 2-edge connectivity).
- Hegde, Sandeep, Shashank (2025), arXiv:2410.22842: https://arxiv.org/html/2410.22842 (induced P13 restriction).
- Petersen's perfect matching theorem, e.g. MIT lecture notes: https://math.mit.edu/~goemans/18438S12/lec4.pdf.
- Earlier internal seven-vertex gadget and pentagon-overlap proofs are in `EG_Proof_Route_Short_Cycle_Theorem.zip`; do not interpret this note as an independent discovery-priority claim for those statements.
