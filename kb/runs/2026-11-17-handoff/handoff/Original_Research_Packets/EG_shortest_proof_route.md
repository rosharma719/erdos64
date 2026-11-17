# Erdős–Gyárfás: shortest defensible proof route (17 November 2026)

## Conclusion
The conjecture is **not proved** by the current research. The most efficient remaining test is a dyadic terminal-path theorem. It is an exact equivalence, not a newly proved reduction in difficulty. Until someone supplies an independent mechanism proving it, a full-proof claim would be unsound.

## Exact bottleneck

Let `H` be a finite simple 2-degenerate graph, with three distinct terminals `a,b,c`. Assume:
1. all vertices outside `{a,b,c}` have degree at least three;
2. each terminal has degree at least two;
3. `H` contains no cycle of length `2^k`, `k>=2`.

**Required terminal lemma (OPEN):** One of the three terminal pairs is joined by a *simple* path of length `2^k-2` for some integer `k>=2`.

Why this would prove the full conjecture: if a counterexample `G` exists, choose one of minimum order. It has a vertex `v` of degree exactly 3 (otherwise deleting a vertex gives a smaller counterexample). Deleting `v` gives `H` with terminals its three neighbors. `H` is 2-degenerate, because a nonempty subgraph of `H` with minimum degree >=3 would itself be a smaller counterexample. The terminal lemma would give a power-of-two cycle through `v`, contradiction. Conversely, if the terminal lemma fails, adjoining a new vertex to all three terminals creates a graph of minimum degree >=3 with no dyadic cycle. Thus **the lemma is mathematically equivalent to the full conjecture**. It describes the precise gap; it does not close it.

## Audited bounded result

The archived `verify_complete_7.cpp` was recompiled and rerun from scratch on 17 November 2026. It examined all `2^21=2,097,152` labeled graphs on 7 vertices. Its outputs were:

- C4-free 2-degenerate labeled 7-graphs: 163,440.
- Maximum edges among them: 9.
- Labeled C4/C8-free 8-vertex extremal degree-2 extensions: 15,120.
- Valid degree-2 extensions of those extremal graphs to order 9: 0.

An independent cycle enumerator again checked the two reported 8-vertex isomorphism-class representatives. Subject to correctness of the exhaustive small program, induction establishes: every C4/C8-free 2-degenerate graph on `N>=9` vertices has at most `2N-6` edges. For a smallest Erdős–Gyárfás counterexample `G` with `n>=10`, `|E(G)|<=2n-5`. This bound is incremental and much too weak to prove the conjecture.

## Exact root obstruction

The accompanying `EG_shortest_path_audit.py` constructs a connected **18-vertex cubic graph**: take a triangle and attach, by bridges, a copy of `K5` minus edges `(0,1),(0,2),(3,4)` at each of its three vertices, attaching each bridge to the unique degree-two vertex of that cap. Every cycle through any of the three triangle vertices is the triangle itself. Thus the superficially attractive assertion that *every vertex of a connected cubic graph belongs to a dyadic cycle* is **false**, and the graph is no counterexample to Erdős–Gyárfás because it has 4-cycles in the caps. The program exactly enumerates cycle lengths through the chosen root and verifies degrees, connectivity, and 2-degeneracy on vertex deletion.

## Why the earlier routes were stopped

- Gadget/window calculus had already been developed in Daniel Garcia's September 2026 preprint, so more gadget substitutions would be primarily incremental.
- For *every* connected cubic graph, deletion of any vertex automatically leaves a 2-degenerate graph; this does not provide a special restriction on hypothetical cubic counterexamples.
- The 2015 work of Narins–Pokrovskiy–Szabó gives degree-critical graphs with missing cycle length 23; the 2026 Di Braccio et al. work guarantees many distinct lengths, but counting distinct lengths alone does not force an exact power of two.
- Parity matters. In bipartite graphs, all paths between fixed terminals have the same parity, so universal consecutive-integer path windows are unavailable. Any credible global forcing mechanism must handle parity-restricted spectra.

## Highest-priority next *proof* step

Find a **strictly stronger, independently provable structural hypothesis** on dyadic-free 3-terminal graphs, for example a decomposition theorem forcing an explicit **arithmetic progression of admissible terminal path lengths** long enough to contain `2^k-2`, with parity taken into account. A proposed hypothesis must be falsified against bridgeless cubic high-girth graphs and verified against the known gadget counterexamples before attempting induction. Without such a theorem, no short proof route is established.

## Source links

- Ducoffe–Dumitru (2026), structural restrictions and computational frontiers: https://arxiv.org/html/2609.28594
- Garcia (2026), dyadic window calculus: https://arxiv.org/html/2609.04686
- Hegde–Sandeep–Shashank (2025), induced-P13-free graphs: https://arxiv.org/html/2410.22842
- Narins–Pokrovskiy–Szabó (2015), degree-critical graphs missing a fixed cycle length: https://arxiv.org/abs/1408.5289
- Di Braccio et al. (2026), leaf-to-leaf paths and cycle length multiplicity: https://link.springer.com/article/10.1007/s00493-026-00205-2
