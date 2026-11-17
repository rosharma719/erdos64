# Research pass VI: rooted prime graphs, automorphism orbits, and balanced two-ear switching

**16 November 2026. Status:** proved elementary general structural lemmas; obtained a fully checkable finite theorem for Hamiltonian cubic graphs through order 16; found a concrete obstruction to a naive one-ear proof. **The rooted prime conjecture and the Erdős–Gyárfás conjecture remain open.** No novelty claim is made for the elementary lemmas.

## 1. The precise target

Call a vertex `v` **dyadically root-critical** in a graph `G` when `G-v` has no simple cycle of length `4,8,16,...`. The proposed *root-robust prime conjecture* asserts that no cyclically four-edge-connected cubic graph other than `K4` has such a vertex. This is stronger than the cubic Erdős–Gyárfás conjecture. The previous five research passes verified the assertion for the 26 non-`K4` cyclically four-edge-connected cubic isomorphism classes of orders 6–12, without a general proof.

We use **cyclically four-edge-connected cubic** to include 3-vertex-connectivity and the absence of a three-edge cut separating cyclic components. All graphs are finite, undirected, and simple.

## 2. The automorphism-orbit theorem (infinite-family reduction)

**Proposition 1 (orbit lifting).** Let `G` be any finite graph, `Γ ≤ Aut(G)` a group of automorphisms, and `O` a vertex orbit. If `C` is a simple power-of-two cycle which does not contain all vertices of `O`, then, for **every** `v∈O`, some automorphic image of `C` avoids `v`.

*Proof.* Choose `w∈O\V(C)` and an automorphism `g` with `g(w)=v`. Since `g` is a bijection and `w∉C`, the image cycle `g(C)` avoids `v` and has the same length. QED.

Consequently the set of dyadically root-critical vertices, if nonempty, is a union of whole automorphism orbits. In a **vertex-transitive** `n`-vertex graph, any **nonspanning** power-of-two cycle gives rooted robustness immediately. This turns the ordinary Erdős–Gyárfás existence assertion into its rooted version for vertex-transitive graphs of **non-power-of-two** order (because a dyadic cycle cannot span such a graph). It does not prove the unrooted existence assertion in classes where that remains open.

One published application: Burkhart (3 November 2026, arXiv:2611.05060) proves the ordinary Erdős–Gyárfás conjecture for Cayley graphs of finite nilpotent groups. The orbit lemma therefore gives the **rooted** version for every such Cayley graph of non-power-of-two order and degree at least 3. This is an implication of the published result, not a new existence theorem. A cubic Cayley graph of *odd* order is impossible, because an inverse-closed generating set of odd cardinality requires an involution.

**Proposition 2 (abelian Cayley graphs, unconditional).** Let `A` be a finite abelian group and let `G=Cay(A,S)` be a simple undirected Cayley graph with `|S|≥3`. If `|A|>4`, `G-v` contains a **4-cycle** for every vertex `v`.

*Proof.* Select `s,t∈S` with `t∉{s,s^{-1}}`, possible since `|S|≥3`. Commutativity gives the simple 4-cycle `1,s,st,t,1`. It is nonspanning when `|A|>4`. Apply Proposition 1 to the regular translation action of `A`. QED. The four-vertex complete graph `K4` is the relevant cubic exception.

These observations identify **asymmetric / small-orbit prime graphs** as the unresolved case where symmetry alone cannot settle rootedness.

## 3. What 3-connectivity really supplies

Let `G` be cubic and `C` any simple cycle. Write `δ(C)` for edges with exactly one endpoint in `V(C)` and `h(C)` for chords (edges joining vertices of `C` but not on the cycle).

**Proposition 3 (spoke identity and ear existence).**

1. `|δ(C)| = |C| - 2h(C)`.
2. If `G` is 3-edge-connected, `C` is even, and `C` is not spanning, then `|δ(C)|≥4`.
3. If `G` is 3-vertex-connected, `C` is nonspanning and `v∈C`, some simple **C-ear** (a path with endpoints on `C` and all internal vertices outside `C`) connects two vertices other than `v`. Joining this ear to the `C` arc that avoids `v` gives a root-avoiding cycle of *some* length.

*Proof.* The vertices of `C` have total degree `3|C|`. Exactly `2(|C|+h(C))` of this degree belongs to edges with both endpoints on `C`, giving (1). For an even cycle the cut size in (1) is even, and 3-edge-connectivity forces it to be at least three, proving (2). For (3), each connected component of `G-V(C)` has at least three distinct neighbors on `C`: otherwise deleting at most two attachment vertices separates it, contradicting 3-connectivity. Choose two such neighbors different from `v` and connect their external neighbors through that component. The resulting `C`-ear and the arc on `C` not containing `v` form the desired root-avoiding cycle. QED.

The exact difficulty is **length**, not topological rerouting. This proof does not assert that the new cycle is dyadic.

## 4. Two-ear switching and its exact length equation

Suppose `C` is a dyadic cycle through a root `v`, and `D` is a simple cycle avoiding `v` **which shares at least one vertex with `C`**. In a cubic graph, the edges of `D` outside `C` decompose into disjoint **C-ears**: every vertex of `C` has only one incident edge not belonging to `C`, so a segment of `D` off `C` cannot visit another `C` vertex internally.

Let the ears be `P_1,...,P_r`. Since `D` consists of its retained `C` edges together with its exterior ears, we have the *exact switching equation*

`|D| = |C| - |E(C)\E(D)| + Σ_i |E(P_i)|`.

The strongest local mechanism is **balanced switching**: if the total ear length equals the number of deleted `C` edges, then `|D|=|C|`, and `D` is dyadic because `C` is. An analogous condition for a different dyadic target is `Σ_i |E(P_i)| - |E(C)\E(D)| = 2^j-2^k` when `|C|=2^k`.

**One ear does not suffice, even on the Petersen graph.** With NetworkX's standard Petersen labeling, take

- root `v=0`;
- through-root 8-cycle `C=(0,1,2,3,4,9,7,5)`;
- avoiding 8-cycle `D=(1,2,3,8,5,7,9,6)`;
- two exterior ears `3-8-5` and `9-6-1`.

The switch deletes four `C` edges and adds four ear edges, giving another 8-cycle. All **12** 8-cycles through root `0` were examined, and none permits a single-ear dyadic rerouting omitting `0`. By vertex-transitivity, the same holds at every root. Nevertheless, the Petersen graph is root-robust. **Any proof strategy premised on universally successful single-ear switching is false.**

**Finite sanity check.** For all `26` non-`K4` prime cubic classes on 6, 8, 10, and 12 vertices, the minimum number of ears needed to find a dyadic cycle avoiding the root from *some* dyadic cycle through that root was:

| Prime graph order | Roots certified with 1 ear | Roots requiring 2 ears | Total roots |
|:---:|---:|---:|---:|
| 6 | 6 | 0 | 6 |
| 8 | 16 | 0 | 16 |
| 10 | 40 | 10 | 50 |
| 12 | 212 | 4 | 216 |
| **Total** | **274** | **14** | **288** |

These are finite observations, not proof that two ears always suffice. The 10 order-10 two-ear cases are the roots of the Petersen graph.

## 5. A finite theorem: rooted Hamiltonian cubic primes through 16 vertices

**Theorem 4 (computer-assisted, completely bounded).** Let `G` be a simple **Hamiltonian** cubic graph on at most `16` vertices. If `G` is cyclically four-edge-connected and `G≠K4`, then **for every vertex `v`, `G-v` contains a simple cycle of length 4 or 8**.

*Proof (exact finite matching reduction).* Fix an arbitrary root `v=0` and label the vertices around a Hamiltonian cycle `C=(0,1,...,n-1)`. Since `G` is cubic, the other `n/2` edges form a perfect matching `M` disjoint from the edges of `C`. If `G-0` has no dyadic cycle, any matching edge `{i,j}` with `1≤i<j≤n-1` must satisfy `j-i ≠ 2^k-1` for `k≥2`, since that chord together with `C[i:j+1]` gives a root-avoiding cycle of length `2^k`. For `n≤16`, the only possible root-avoiding dyadic lengths are 4 and 8. Enumerate all matchings satisfying the necessary chord-distance restrictions and test `G-0` for 4-cycles and 8-cycles. This is exhaustive because every Hamiltonian cubic graph with a chosen root admits such a labeling.

The exact resulting counts are:

| n | Permitted matchings after single-chord rule | Containing root-free C4 | Additional containing root-free C8 | Root-critical survivors |
|---:|---:|---:|---:|---:|
| 4 | 1 | 0 | 0 | 1 (`K4`) |
| 6 | 1 | 1 | 0 | 0 |
| 8 | 14 | 9 | 0 | 5 |
| 10 | 80 | 50 | 30 | 0 |
| 12 | 768 | 524 | 244 | 0 |
| 14 | 8,817 | 5,925 | 2,892 | 0 |
| 16 | 123,472 | 82,460 | 41,009 | 3 |

All five order-8 survivors have nontrivial cyclic three-edge cuts (two unrooted graph classes). All three order-16 survivors are isomorphic and have nontrivial cyclic three-edge cuts. For example, the first order-16 survivor has matching edges

`(0,5),(1,13),(2,4),(3,7),(6,8),(9,11),(10,15),(12,14)`.

Deleting the edges `(0,15),(1,13),(8,9)` splits it into cyclic components on 9 and 7 vertices. Each survivor therefore violates the **prime** hypothesis. `K4` is the unique permitted prime exception. This proves the theorem. QED.

**Verification discipline.** The same order-16 counts were reproduced by a separate C++ matching enumerator with a distinct cycle-detection procedure. Explicit survivor matching lists, graph6 strings, root-critical vertices, and cyclic-three-cut witnesses are stored in `root_switching_certificates.json`. Unit tests independently construct each graph and verify each cut and rooted status. The theorem makes no claim about non-Hamiltonian cubic graphs on 16 vertices or Hamiltonian graphs above 16 vertices.

## 6. Where the conceptual work should go

The next proof target should be a **two-ear balancing or power-crossing lemma**, not a larger catalog:

> For a cyclically four-edge-connected cubic `G`, a root `v`, and a dyadic cycle through `v`, find conditions on two appropriately placed internally disjoint ears which force a dyadic root-avoiding cycle. Analyze whether cyclic connectivity, parity, and the three terminal-pair path spectra suffice to force those conditions.

The Petersen graph shows that *two* ears are genuinely necessary. The 16-vertex classification shows that Hamiltonian chord patterns which defeat both 4- and 8-cycle switching correspond to decomposable graphs at that order. The open step is to turn **indecomposability into a length relation**; neither result yet proves such a relation in general.

This is potentially an infinite-family structural argument. The 16-vertex enumeration is best treated as a finite falsification/regression check on proposed lemmas, not as the main research activity.

## Reproduce

```sh
python -m pytest -q tracks/2026-11-halving/scripts/test_root_orbit_switching.py
python -m pytest -q tracks/2026-11-halving/scripts/test_*.py
python tracks/2026-11-halving/scripts/rooted_hamiltonian_matching.py 16
c++ -O2 -std=c++17 tracks/2026-11-halving/scripts/rooted_hamiltonian_census.cpp -o /tmp/root_census
/tmp/root_census 16
```

**Related literature (not a novelty claim):**

- Heckman and Krakovski, *Erdős–Gyárfás Conjecture for Cubic Planar Graphs*, EJC 20(2), 2013, https://doi.org/10.37236/3252 . The result concerns existence of a dyadic cycle, not avoidance of a prescribed vertex.
- Burkhart, *Odd-ordered Cayley graphs satisfy Erdős–Gyárfás*, 2026, https://arxiv.org/abs/2611.05060 . Contains the finite nilpotent Cayley corollary used above.
- Lo, *A note on cycles in cyclically 4-edge-connected cubic planar graphs*, 2026, https://arxiv.org/abs/2605.03786 . Related vertex-avoiding results concern line graphs, not the proposed rooted cubic statement.
