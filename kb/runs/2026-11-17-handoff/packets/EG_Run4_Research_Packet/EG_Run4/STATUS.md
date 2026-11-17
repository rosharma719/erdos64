# Erdős–Gyárfás continuation, 2026-11-17

## Data availability
The local archive has four 24-vertex C4/C8-free graphs, not the complete 251 28-vertex records. GitHub raw retrieval fails DNS in the container. The repository `chriss1245/erdos-gyarfas-cubic-frontier` publicly lists graph6 collections for orders 24 and 26 but not a complete order-28 dataset. No exhaustive 28-vertex classification is claimed.

## Independently verified computation
`verify_g6.py` on `controls.g6` reports six controls, four C4/C8-free, zero cyclically-4-edge-connected among the four, and K4 rooted-critical. The Coxeter graph is cubic, cyclically 4-edge-connected, has C8, and is rooted-robust. The Coxeter graph is not a member of the target C4/C8-free class.

`transversal.py` independently enumerates undirected cycles as oriented canonical vertex sequences, finding exactly 21 C8 and 609 C16 in the Coxeter graph. It exhaustively computes C8 transversal number 6 with witness (0,1,3,6,9,14), C16 transversal number 5 with witness (0,1,3,9,15), and combined C8/C16 transversal number 6. `independent_transversal.py` uses an independent stack-based DFS with bitmasks and independently verifies the C8 and C16 counts and their transversal lower bounds and witnesses. (Combined transversal follows from C8 family inclusion and the C8 witness hitting all C16.)

## Sourced literature
Markström (2004) gives 4,23,251 C4/C8-free cubic graphs at orders 24,26,28, according to `oaustegard/experiments` research note and `chriss1245/erdos-gyarfas-cubic-frontier` README. The latter claims an exhaustive unrooted cubic bound through 40. The former claims Markström's archived search through 52; this is not yet independently authenticated from original logs, and priority should remain unresolved. Tranquilli (2026, arXiv:2608.02675) claims a certificate-backed cubic bipartite bound through 58. Garcia (2026, arXiv:2609.04686) reports a certified general minimum-degree-3 bound through 23 and correction of Exoo's construction. Carr (2026, arXiv:2605.22844) proves minimum counterexamples have >=4/7 cubic vertices.

## Bounded observation
Assuming the published counts and the independently reported fact that all 4 order-24 and 23 order-26 C4/C8-free graphs have triangles, there are no cyclically 4-edge-connected cubic graphs with no C4/C8 on <=26 vertices. For n>=6 a triangle in a connected cubic graph gives a cyclic 3-edge cut, because the complement contains a cycle (the external edges are at most 3, and a cubic graph on >=3 remaining vertices cannot be a forest). K4 is an exceptional small-order case, but it has C4. This bounded statement is conditional on the completeness of the sourced census, not a new standalone exhaustive enumeration.

## Next
Acquire all 251 28-vertex graph6 records and an independent canonical completeness certificate. Then use `verify_g6.py --expect-count 251 --strict` and compare with a separately implemented cycle oracle and edge-cut classifier. A full unrooted bound does not imply rootedness.
