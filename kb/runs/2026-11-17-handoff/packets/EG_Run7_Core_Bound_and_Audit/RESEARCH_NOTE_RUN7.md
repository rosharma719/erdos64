# Erdős–Gyárfás: a bounded reduction theorem from C4/C8-free 2-degenerate graphs

17 November 2026. All graphs finite and simple; cycles are not required to be induced. This note does **not** prove the Erdős–Gyárfás conjecture. This is an incremental, partly computer-assisted bound, not a claim of discovery priority.

## 1. Background and pre-existing work

Ducoffe–Dumitru (arXiv:2609.28594, 2026) show that a smallest counterexample G has no proper subgraph of minimum degree >=3, has at most 2n-2 edges, and has at least 2n/3+1 degree-three vertices. Their Lemma 3.5 builds a 2-degenerate auxiliary graph M on the high-degree vertices, with one edge per cubic vertex having two high-degree neighbors, and proves M has **no power-of-two cycle**. Their computational search claims to check the full conjecture through order 40. Hegde–Sandeep–Shashank (arXiv:2410.22842) prove the induced-P13-free case.

Garcia's September 2026 paper (arXiv:2609.04686) develops a gadget path-window calculus including the seven-vertex symmetric H7' with the same 2..6 terminal path spectrum as the gadget from previous runs. The older 2014 Nowbandegani–Esfandiari–Haghighi–Bibak work likewise uses independent cycle detours in cubic claw-free graphs. Hence the earlier interval forcing argument is not a compelling originality claim.

## 2. Exact finite lemma (computationally assisted)

**Finite lemma.** Every 2-degenerate graph F on eight vertices containing no C4 or C8 has at most 11 edges. Up to isomorphism there are exactly two such graphs with 11 edges, with graph6 labels `GxaGiC` and `GgqPi_`. In both graphs, adding a ninth vertex adjacent to any two distinct original vertices produces a C4 or a C8.

**Complete enumeration protocol, independent of graph atlases.** `verify_complete_7.cpp` enumerates **all 2^21 = 2,097,152 labeled simple seven-vertex graphs**, using the fixed list of 21 possible edges. It checks C4 absence with pairwise common-neighbor intersections and 2-degeneracy by iterative removal of vertices of current degree <=2. Exactly 163,440 labeled graphs pass; their maximum edge count is nine (6,615 eligible labeled graphs have nine edges). Therefore a 2-degenerate C4-free eight-vertex graph has at most 11 edges: remove a vertex of degree <=2 and use the seven-vertex bound. To test equality, for every eligible nine-edge seven-vertex graph and every pair of its vertices, attach an eighth degree-two vertex; adding this vertex creates a C4 iff its endpoints have an old common neighbor, and a C8 iff an old simple path of length six joins them. The C++ run finds **15,120 labeled eight-vertex extremal extensions** satisfying both prohibitions. For each, the code checks every possible pair of old vertices: every degree-two ninth-vertex attachment creates a C4 or C8. Count of permissible ninth-vertex extensions: **zero**. The 15,120 are labeled extensions with a distinguished eighth vertex, not non-isomorphic graphs. The program has no dependencies other than a C++17 compiler. The independent Python/NetworkX atlas audit yields two isomorphism classes and checks the representatives by a separate DFS.

The classification is exhaustive at the level of **labeled seven-vertex input graphs** without relying on any graph-isomorphism enumeration. The proof of the finite result depends on the correctness of the small standalone C++ implementation, which can be independently reimplemented/audited. It is not a formally verified theorem prover certificate.

## 3. Bounded theorem (rigorous subject to finite lemma)

**Theorem.** If F is a 2-degenerate graph with no C4 and no C8 and N>=9 vertices, then

    |E(F)| <= 2N - 6.

**Proof.** The n=9 case follows by removing a vertex x of degree at most 2. The eight-vertex remainder has at most 11 edges by the finite lemma. If x has degree at most one, the total has at most 12=2(9)-6 edges. If x has degree two and the total had 13 or more edges, the eight-vertex remainder would have exactly 11 edges. By the classification in the finite lemma, reinserting x would create a C4 or C8, contradiction. Hence the n=9 case holds. For N>9 remove any vertex of degree at most two and apply induction: 2(N-1)-6+2=2N-6. QED.

**Corollary 1.** Suppose G has minimum degree >=3, no C4 or C8, and no proper induced subgraph of minimum degree >=3. If n=|V(G)|>=10, then

    |E(G)| <= 2n - 5.

**Proof.** G has a degree-three vertex v, since otherwise deletion of any vertex preserves minimum degree >=3. The graph G-v has no proper 3-core, so it is 2-degenerate; it is C4,C8-free and has n-1>=9 vertices. Apply the theorem to get |E(G)|-3 <=2(n-1)-6, as claimed. QED.

**Corollary 2.** Conditional on Ducoffe–Dumitru's minimal-counterexample theorem and its verified order-40 frontier, a smallest counterexample to Erdős–Gyárfás on n vertices would have at least

    ceil(2n/3 + 2)

vertices of degree exactly three.

**Proof.** Let h be the number of degree>=4 vertices and ell=n-h the number of degree-three vertices. The cited paper proves every cubic vertex has at most two high-degree neighbors, each high-degree vertex has >=4 cubic neighbors, and constructs a 2-degenerate auxiliary graph M on h vertices with |E(M)| equal to the number ell_2 of cubic vertices with two high-degree neighbors; moreover M has no dyadic cycle, hence no C4 or C8. If h>=9, apply the bounded theorem to M: ell_2 <=2h-6. If ell_i counts cubic vertices with i high-degree neighbors, 4h <=ell_1+2ell_2, so ell>=ell_1+ell_2>=4h-ell_2>=2h+6. Thus 3ell>=2n+6. If h<=8, the published order-40 verification implies n>=41, so ell=n-h>=n-8>=(2n+6)/3 (already valid for n>=30). QED.

This sharpens the published lower bound by just **one degree-three vertex**, and does not resolve even the cubic case. We have not established whether an equivalent strengthening is already known.

## 4. Limits and next experiment

- The improved linear edge bound is still far above the cubic edge count of 3n/2 for large n, so it does not reduce the general conjecture to cubic graphs.
- A C4,C8-free 2-degenerate graph on eight vertices can attain 11 edges. The enumerated maximizers are locally saturated with respect to adding a new degree-2 vertex, but other nine-vertex examples of the permitted maximum (12 edges) *are* extendable. No growing edge deficit follows from repeating the order-eight analysis.
- Graphs of arbitrarily large girth and minimum degree three exist, so no fixed finite inventory of triangle/pentagon gadgets can by itself cover the full problem.
- For additional conceptual progress, study attainable simple a-b path lengths in a C4,C8,...-free 2-degenerate graph as a vertex of degree two is added. The exact rule: adding x with neighbors a,b creates a C_{2^k} **iff** the old graph contains a simple a-b path of length 2^k-2. The hope is to use these forced forbidden path lengths to prove a structural theorem about minimal 3-core build orders, rather than relying on one fixed seven-vertex gadget.

## 5. Reproduce

Requires a C++17 compiler for the standalone exhaustive search; NetworkX 3.x for an independent cross-check:

    g++ -O3 -std=c++17 verify_complete_7.cpp -o verify_complete_7
    ./verify_complete_7
    python bounds_audit.py
    python independent_bounds_verify.py

The C++ program independently enumerates all labeled seven-vertex graphs. `bounds_audit.py` outputs `eight_vertex_certificate.json` with the two graph6/edge-list representatives and atlas cross-checks. The second Python script does not import the first script's DFS or adjacency-mask logic; it verifies the two reported representatives with its own cycle enumeration. The finite classification, not the induction, is the computational dependency.

Sources:
- Guillaume Ducoffe and Bogdan Dumitru (2026): https://arxiv.org/html/2609.28594
- Daniel Garcia (2026): https://arxiv.org/html/2609.04686
- A. S. Hegde, R. B. Sandeep, P. Shashank (2025): https://arxiv.org/html/2410.22842
- P. Salehi Nowbandegani, H. Esfandiari, M. H. Shirdareh Haghighi, K. Bibak (2014): https://www.dmgt.uz.zgora.pl/publish/pdf.php?doi=1732
