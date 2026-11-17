# Erdős–Gyárfás proof program: short-cycle coverage and interval forcing

Date: 2026-11-17. All graphs finite, simple, undirected. A cubic graph is 3-regular.

**Status**: The statements labeled PROVED below have complete arguments. The computer results are cross-checked but not exhaustive for arbitrary order. No proof of the full Erdős–Gyárfás conjecture is claimed, and no literature-priority claim is made.

## 1. Literature context (sources)

1. Hegde–Sandeep–Shashank, *Erdős-Gyárfás conjecture on graphs without long induced paths*, arXiv:2410.22842 (2024/2025), https://arxiv.org/abs/2410.22842 : every P13-free graph of minimum degree at least 3 satisfies Erdős–Gyárfás; P12-free such graphs have C4 or C8.
2. Ducoffe–Dumitru, *Towards a more structured search for Erdős-Gyárfás counter-examples*, arXiv:2609.28594 (2026), https://arxiv.org/html/2609.28594 : any smallest counterexample is 2-edge-connected, has > 2/3 cubic vertices and at most 2n-2 edges; every edge belongs to some cycle of length 2^k+1 (k>=1); SAT-modulo-symmetry reports all general graphs through 40 vertices and cubic graphs through 48.
3. Di Braccio–Katsamaktsis–Ma–Malekshahian–Zhao, *Leaf-to-leaf paths and cycles in degree-critical graphs*, arXiv:2504.11656v2 (2026), https://arxiv.org/html/2504.11656 : distinct cycle length bounds for a **special** degree-3-critical class with 2n-2 edges. Its special definition must not be conflated with minimal subgraph of minimum degree 3.
4. Related pentagon-cluster literature exists (e.g. *Structural analysis of cubic graphs based on 5-cycle clusters*, 2022, https://ceur-ws.org/Vol-3226/paper25.pdf). Exact priority of the claims in this note has **not** been established.

## 2. PROVED: pentagon overlap lemma

**Lemma A.** If G is cubic, has girth at least 5, and contains no C8, then two distinct C5s are either vertex-disjoint or intersect in exactly a path with two edges (three vertices). Moreover, each vertex lies on at most two C5s, and each C5 intersects at most one other C5.

**Proof of overlap classification.** Let C,D be distinct 5-cycles sharing a vertex. At any shared vertex, their two 2-element sets of incident cycle edges overlap because that vertex has degree 3; thus C,D share an edge, so they share at least two vertices. Each C5 is induced (a chord would create a triangle). If C and D shared four vertices, their shared edges among the four old vertices would form a 3-edge path in C; replacing the complementary length-2 C-path by the 2-edge detour of D yields a 4-cycle. If they shared five vertices, inducedness forces C=D. Thus they share two or three vertices. If two, their unique shared edge has two remaining internally disjoint 4-edge paths, yielding C8. Since C8 is forbidden, they share exactly three vertices. The third vertex must be adjacent in both cycles to an endpoint of the shared edge, again because cubic degree forces an incident shared edge, so the common edges form a two-edge path. (A shared third vertex separated from the shared edge would force a fourth common vertex.)

**At most two cycles through a vertex.** Suppose three distinct pentagons pass through v, with incident edges va,vb,vc. If two use the same pair, say va,vb, their paths must diverge at a and at b, because overlap of three edges would contradict the classification. Any third pentagon using the same pair would repeat a continuation at a and share three consecutive edges; any third using a different pair, say va,vc, would need to extend the common edge va at a in the two distinct directions prescribed by the first pair, impossible. Otherwise the three pentagons use the three different pairs (va,vb),(vb,vc),(vc,va). The overlap classification forces them to share a continuation beyond b, beyond c, and beyond a, respectively. Let those continuation vertices be x,y,z. Each of the three 5-cycles has the form z-a-v-b-x-z, x-b-v-c-y-x, y-c-v-a-z-y. Then x,y,z form a triangle, contrary to girth >=5. Therefore at most two pentagons pass through v.

**At most one partner.** If C met two distinct other C5s D,E, each would intersect C in 3 vertices. Two 3-subsets of a 5-set overlap, giving a vertex on three distinct C5s, impossible. Hence at most one partner. QED.

**Five-port decomposition.** The subgraph U consisting of every edge of every C5 has connected components of only these types:

- A single C5: 5 vertices, 5 edges, and exactly five one-edge external ports (each internal degree is 2).
- A theta graph with three internally disjoint branch-to-branch paths of lengths 2,3,3, obtained from two C5s sharing a length-two path: 7 vertices, 8 edges, and exactly five one-edge external ports (its two branch vertices have internal degree 3).

Girth >=5 rules out additional edges joining ports *within* one component: any such edge closes a cycle of length 3 or 4 inside either component. Edges joining different components are allowed.

## 3. PROVED: short-cycle edge-cover theorem

**Theorem B.** Every cubic graph all of whose edges belong to a triangle or a 5-cycle contains a 4-cycle or an 8-cycle.

Equivalently, every cubic graph without C4 or C8 has an edge belonging to neither a triangle nor a pentagon.

**Proof.** Suppose G has no C4 or C8, and every edge lies on C3 or C5.

**Case 1: G triangle-free.** Then girth >=5 and every edge lies on C5. At every vertex, its three incident edges need at least two distinct C5s to cover them, since a single C5 uses only two. By Lemma A, at most two C5s pass through each vertex, so exactly two pass through each vertex. Fix a C5 C. The other pentagons meeting C partition its five vertices into disjoint groups of three (each intersecting pentagon shares precisely a two-edge path with C, and no vertex lies on three pentagons). This is impossible because 3 does not divide 5. Contradiction.

**Case 2: G contains a triangle abc.** Because C4 is absent, triangles are pairwise vertex-disjoint. Let x,y,z be the respective third neighbors of a,b,c. They are distinct and pairwise nonadjacent: equality gives two triangles sharing an edge (hence C4), while an edge xy would give the C4 x-a-b-y-x. The three edges ax,by,cz lie on no triangle; hence each must lie on some C5.

Every such pentagon through ax uses exactly one triangle edge, ab or ac. It must use at least one, as a has neighbors b,c,x. If it used two, it would be x-a-b-c-z-x (or its symmetric equivalent), forcing the forbidden edge xz and therefore C4. Thus every pentagon covering triangle-boundary edges has form x-a-b-y-u-x or its symmetric variant; u is a common neighbor of the external vertices x,y.

To cover ax,by,cz, choose pentagons C_ab and C_bc corresponding to two different pairs of boundary edges (relabel a,b,c if necessary). These are x-a-b-y-u-x and y-b-c-z-u'-y. If u != u', the cycles have exactly the one edge by in common, so their remaining length-four paths form a C8. Hence u=u'=w. The vertices a,b,c,x,y,z,w form the **seven-vertex three-port gadget** T: abc is a triangle, w is adjacent to x,y,z, and a-x,b-y,c-z are matching edges. The four vertices a,b,c,w have all their cubic neighbors inside T; x,y,z each have exactly one edge to the outside.

For any two distinct ports of T, there exist internally simple paths inside T of lengths 2,3,5. For example, between x and y they are x-w-y (2), x-a-b-y (3), and x-a-c-z-w-y (5). If an external simple path of length 1,2,or 3 joined x,y while avoiding internal vertices of T, it would form a C4 (use internal length 3 or 2) or C8 (use internal length 5), respectively. By symmetry no two ports admit such an external path.

Now take the unique edge xt leaving port x and T. It cannot belong to a triangle, since its other two neighbors a,w are already saturated internally and not adjacent. If it belonged to a C5, the C5 would exit T through xt and re-enter T through another port y or z. The exterior segment would have length at most 3 because any internal port-to-port segment has length at least 2. This contradicts the preceding paragraph. Thus xt lies on neither C3 nor C5, contrary to our covering hypothesis. QED.

**Corollary (conditional on a minimal cubic counterexample).** Ducoffe–Dumitru's edge saturation lemma requires every edge of such a counterexample to lie on a C_{2^k+1}. By Theorem B, at least one edge has no witness at k=1 (C3) or k=2 (C5), so its shortest near-dyadic witness is C9 or longer. This is a restriction, not a contradiction.

## 4. PROVED: dyadic forcing by terminal path spectra

Let T be the seven-vertex gadget from Case 2, with ports x,y,z. Direct enumeration (or inspection) shows that for **each unordered pair of distinct ports** there is a simple internal path of **every length 2,3,4,5,6**. Consider a finite simple cubic base graph H. Replace every base vertex by a disjoint copy of T and assign its three incident edges to the three ports bijectively. Call the inflated cubic graph F(H).

**Theorem C.** F(H) contains C_{2^k} for some k>=2. In fact, if H contains a q-cycle (q>=3), F(H) contains a cycle of every length in [3q,7q]. In addition F(H) is C4-free and C8-free.

**Proof.** For each of the q vertices of a fixed base cycle, independently select an internal port-to-port path of length any integer from 2 to 6. Use the q external matching edges between gadgets. The resulting lifted closed walk is a simple cycle because the base cycle visits each gadget once; its length ranges over all integers q+[2q,6q]=[3q,7q]. The smallest power of two >= 3q is < 6q <= 7q, so one of these lengths is a power of two. Any cycle of F(H) either lies in a single gadget or projects to a simple base cycle (a simple cycle cannot traverse a three-port gadget twice). Single gadgets have no C4 or C8; a projected cycle has at least 3 external edges and at least 2 internal edges per visited gadget, hence length >=9. QED.

This is a **genuine interval-forcing mechanism** on a restricted but infinite class, rather than merely a cycle length transfer identity. It does not prove that every cubic graph is of this form or contains enough such gadgets.

## 5. Independently checked examples and certificates

`gadget_forcing.py` constructs F(K4) and F(Petersen) from literal graph edge lists and emits four independently rooted C16 witnesses for F(K4). `independent_verify.py` re-reads the emitted edge lists and uses NetworkX's bounded-cycle enumeration to verify C3/C4/C5/C8 counts and the C16 certificates; no construction-module imports are made by the verifier.

| Base H | Order F(H) | Edges | C3 | C5 | C4 | C8 | Uncovered by C3 or C5 | C16 certificate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| K4 | 28 | 42 | 4 | 12 | 0 | 0 | 6 | 4 certificates, each avoids one entire 7-vertex gadget |
| Petersen | 70 | 105 | 10 | 30 | 0 | 0 | 15 | 1 certificate |

F(K4) is an explicitly constructed 28-vertex cubic graph avoiding C4 and C8. It should belong to the reported 251-graph order-28 family **if** that published census is exhaustive. The complete 251-record dataset was **not** used or independently audited here.

K4-base adjacency SHA-256 (sorted adjacency lines): `2fb66d723de3a652a842ccb6762f27d35319370a11aab6829630bf6bef9258cb`.

Verification includes an independent finite enumeration of all admissible unions of two and three C5s through a fixed root (`pentagon_local_exhaust.py`). All six canonical two-C5 configurations overlap on exactly a two-edge path; no admissible triple is found. The argument in Lemma A is an independent paper proof.

`theorem_checks.py` independently tests all 3 cubic atlas graphs (n<=7), Petersen, dodecahedron, triangular prism, and 180 pseudorandom connected or disconnected 3-regular samples across n=10..20. These are **falsification checks**, not an exhaustive cubic census.

To reproduce from this directory:

```bash
python pentagon_local_exhaust.py
python gadget_forcing.py
python independent_verify.py
python theorem_checks.py
```

The code uses Python 3 and NetworkX for independent verification (not for gadget generation). Machine-readable edge lists and certificates are in this packet.

## 6. Proof strategy after this result

1. **Exploit overlapping near-dyadic cycles.** In any smallest counterexample, each edge lies on C_{2^k+1} for some k. Two cycles of length 2^k+1 with a single common edge and otherwise disjoint form a C_{2^{k+1}}. For k=2 and cubic girth>=5, short girth forces a rigid pentagon packing; for k>=3, allowed overlaps have multiple lengths, so the same counting obstruction does not immediately generalize.
2. **Seek rich path-spectrum substructures forced by saturation, rather than postulated as gadgets.** The seven-vertex T shows that terminal path spectra can force *entire intervals of lengths*, which unavoidably hit powers of two whenever the interval grows by factor >=2. The missing theorem is a global structural mechanism guaranteeing enough independent reroutings in an arbitrary minimum-degree-three graph.
3. **Handle high-degree vertices:** the proved edge-cover theorem is cubic-only, while hypothetical smallest counterexamples may include degree>=4 vertices despite the known >2/3 cubic fraction.

**Open:** Does a finite collection of near-dyadic cycle-overlap motifs and bounded-width reroutings cover every minimal 3-core? Can one force a factor-two interval of cycle lengths without assuming a special gadget? Nothing here establishes either assertion.

## 7. PROVED: a reducible interaction-forest obstruction in cubic counterexamples

Call a triangle **saturated** if each of its three incident edges leaving the triangle belongs to a C5. In a cubic graph with no C4 or C8, Section 3 proves that every saturated triangle sits in a seven-vertex gadget T with three ports. Its center and triangle vertices are saturated (full cubic degree inside T), and each port has exactly one edge leaving T.

**Lemma D (disjointness of saturated gadgets).** In a cubic C4,C8-free graph, two distinct saturated-triangle gadgets are vertex-disjoint.

**Proof.** Distinct triangles are vertex-disjoint: two triangles meeting at a vertex in a cubic graph share an edge and form a C4. Every center w of a saturated gadget is triangle-free (its three port neighbors are pairwise nonadjacent, since any pair would create C4 with the original triangle). Every port x is triangle-free as well (its neighbors a,w are not adjacent, and each a,w has all other incident edges already fixed). A gadget of a distinct triangle can thus only overlap in its center or ports. If centers coincide, their three port sets coincide as well because a center has degree 3. There are then two distinct triangles a-b-c-a and a'-b'-c'-a' connected respectively to the same ports x,y,z, which in turn are adjacent to the common center w. The eight vertices along x-a-b-y-b'-c'-z-w-x make a C8, contradiction. A center of the first gadget cannot be a port of the second, because then a triangle vertex of the second gadget would have to be a port of the first (all center neighbors are ports), contradicting the fact that ports are triangle-free. Finally, a port cannot be shared by two gadgets with distinct centers and triangles: it would have at least four distinct neighbors (the two centers and two triangle vertices). QED.

Define the **saturated-triangle interaction multigraph** Q by placing a vertex for each saturated gadget and an edge between two vertices whenever a port of one gadget is directly connected by an edge to a port of the other. Any self-edge (a direct edge joining two ports of the same gadget) creates a C4 using the internal port-to-port path of length 3. Any parallel pair of gadget-joining edges creates a C8: use one 3-edge internal path between the two used ports of each gadget together with the two join edges, total 3+3+2=8. Thus Q is simple in a C4,C8-free graph.

**Theorem D (interaction forest).** If G is cubic and contains no cycle of power-of-two length, then the saturated-triangle interaction graph Q is a forest. In particular, if t>=1 saturated gadgets are present in c connected components of Q, at least t+2c of their three-port external edges lead to vertices outside all saturated gadgets.

**Proof.** In a hypothetical counterexample, C4 and C8 are absent, so Q is simple and gadgets are disjoint. If Q contained a cycle of q>=3 gadgets, the edges of this Q-cycle and the independently selected internal port-to-port paths of lengths 2,3,4,5,6 would produce *every* cycle length in [3q,7q] in G, including a power of two by Theorem C. Thus Q has no cycles. Since a forest on t vertices with c components has t-c edges, the number of port stubs not used by gadget-to-gadget edges is 3t-2(t-c)=t+2c. These stubs lead outside every saturated gadget. QED.

**Stronger metric version (path-spectrum forcing).** Let q>=3 vertex-disjoint seven-vertex gadgets be arranged in a ring, connected through distinct ports by pairwise internally vertex-disjoint paths whose internal vertices lie outside all chosen gadgets, with *total* connector length B. Then G contains cycles of every length in [B+2q,B+6q]. In particular, if B<=2q, at least one of those lengths is a power of two because B+6q >= 2(B+2q). This is an actual forbidden *global configuration* in a counterexample, applicable even when adjacent gadgets have connectors of length two rather than direct port edges.

**Computational checks.** `saturated_triangle_quotient.py` independently detects saturated triangles by enumerating C5s, reconstructs their gadgets, checks disjointness, and builds Q. On F(K4), Q=K4 (4 gadgets, 6 edges, triangles); on F(Petersen), Q=Petersen (10 gadgets, 15 edges, cycles). These graphs contain explicitly certified C16s as predicted. No claim is made that a hypothetical general counterexample necessarily has any saturated triangle.
