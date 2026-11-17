# Research pass X: exact boundary-linkage composition and dyadic spectral sparsity

**Date:** 16 November 2026.  **Status:** Complete elementary transfer theorem and contextual-replacement corollaries, with a separate numerical density certificate. Exact finite verification is included. This is **not** a proof of the Erdős–Gyárfás conjecture or of bridge stability, and the generic matching-state construction is standard in connectivity dynamic programming; no claim of publication-level originality is made.

## Conceptual choice

We previously had separate descriptions for triangle expansion, three-edge cuts, four-terminal square strips, and bridges of two edges. Those descriptions do not, by themselves, give a closed algebra for *all* simple cycles crossing a boundary. In particular, a cycle may use **four** edges of a four-edge cut; each side must then supply **two vertex-disjoint paths**, whose total lengths cannot generally be inferred from independent pairwise path spectra.

The right interface object is a **rooted boundary-linkage signature**. This eliminates the cubic/prime assumption from the *transfer theorem*, while leaving the genuinely hard problem of forcing rich length spectra in sufficiently connected graphs.

## Definitions

An `h`-pole consists of a finite simple undirected graph `P` and a list of `h` indexed attachment *half-edges*, each incident to a vertex `p_i` of `P`. Repeated attachment vertices are allowed, but when two poles are glued, one edge `p_i q_i` is inserted for each index `i`; for simple graphs these new edges must be pairwise distinct.

For any even subset `S` of the port indices and any perfect matching `M` of `S`, let

\[
\Lambda_P(S,M) = \left\{\sum_{\{i,j\}\in M}|R_{ij}|:\ R_{ij}\text{ are pairwise vertex-disjoint simple paths in }P\right\}.
\]

Each `R_ij` joins `p_i` to `p_j`. If `p_i=p_j`, the length-zero singleton path is permitted; this is necessary for bridges and cuts with repeated attachment vertices. The paths in a linkage are vertex-disjoint, including at their endpoints. We record only their **total** length, because a resulting cycle visits all of them exactly once.

Also retain the internal simple-cycle length set `C(P)`. For a forbidden root `r` in the pole, take the same objects computed in `P-r`. The collection `Sigma(P)=(C(P),Lambda_P)` is the boundary signature.

## Theorem 1: universal edge-cut composition

Let `G` be obtained by gluing two poles `A` and `B` along equally indexed ports, and let `C(G)` denote the set of simple-cycle lengths. Then

\[
\boxed{\begin{aligned}
C(G)= C(A)\cup C(B)\cup
\bigcup_{\substack{S\subseteq[h]\\|S|\ge2\ \mathrm{even}}}
\bigcup_{\substack{M,N\text{ matchings of }S\\M\cup N\text{ is one alternating circuit}}}
\left(|S|+\Lambda_A(S,M)+\Lambda_B(S,N)\right).
\end{aligned}}
\]

Set addition is Minkowski sum. The two matchings `M,N` are considered as matchings of edge *labels*, so for `|S|=2` their union is a single alternating **2-edge multicycle** even though they have the same underlying pair. For `|S|=4`, `M` and `N` must be different.

**Proof.** A simple cycle contained in one pole contributes to its internal spectrum. Otherwise it uses a nonzero even number `|S|` of cut edges. On each side, its portions between consecutive cut edges form pairwise vertex-disjoint simple paths, with length-zero passages permitted if consecutive cut edges meet at the same vertex. These passages pair the used cut-edge labels, yielding matchings `M,N` and total lengths from the respective `Lambda` sets. Since the original object was one simple cycle, the alternating union of the matchings has one component. The length is `|S|` (new cut edges) plus both internal totals. Conversely, any two such collections of disjoint paths with one alternating matching circuit glue to a single simple cycle, with that length. QED.

The theorem holds for **arbitrary simple graphs**, with no cubicity, planarity, connectivity, or bounded-degree condition. Root-avoidance is exact by computing the pole's signature after deleting the root. The cut size `h` is arbitrary.

### Important small-cut cases

* `h<=3`: a cycle crosses the cut exactly twice, so ordinary pairwise path spectra suffice.
* `h=4`: a cycle may cross twice **or four times**. The four-crossing term depends on vertex-disjoint **two-linkage** spectra, not just individual paths.
* `h>4`: the same formula handles 2, 4, 6, ... crossing edges without needing ad hoc cases.

## Theorem 2: contextual equivalence and dominance

If two `h`-poles have the same internal-cycle spectra and the same `Lambda(S,M)` for **all** states, then gluing either one to *any* compatible context yields exactly the same set of simple-cycle lengths. If every component of one signature is a subset of the corresponding component of the other, the first glued graph's cycle-length set is a subset of the second's.

**Proof.** Substitute the signatures in the formula of Theorem 1. Its operations are unions and Minkowski sums, both monotone in each operand. QED.

The same statement holds for rooted cycle spectra when the forbidden root is on the context side, or when the compared poles have matching root-excluded signatures.

This supplies a rigorous definition of *cycle-length-preserving gadget replacement*. It is stronger and safer than comparing only the minimum and maximum available paths.

### Explicit counterexample to endpoint-only windows

Take pole `A1` with two internally disjoint `s-t` paths of lengths **2 and 7**, and `A2` with three internally disjoint `s-t` paths of lengths **2, 3, and 7**. Both have minimum `s-t` length 2 and maximum length 7. Glue either to a second pole that is a length-3 `u-v` path, using the two cut edges `su,tv`.

* `A1` creates cycles of lengths 7, 9 and 12, hence **no dyadic cycle**.
* `A2` also creates an **8-cycle** using its length-3 path and the other pole's length-3 path plus the two cut edges.

Consequently, *endpoint windows* alone cannot decide whether a dyadic cycle survives gluing, even for two-terminal poles. Both cases have independent exact-graph tests.

## Theorem 3: additive-density forcing and the counterexample obstruction

Fix any compatible state `(S,M,N)` from Theorem 1 and let `X=Lambda_A(S,M)`, `Y=Lambda_B(S,N)`. Set `t=2^k-|S|` and take **any finite nonempty integer window** `W` (including a single parity class or other arithmetic progression).

Then

\[
\boxed{|X\cap W|+|Y\cap(t-W)|>|W|\quad\Longrightarrow\quad 2^k\in C(G).}
\]

**Proof.** Reflection `w -> t-w` is a bijection from `W` to `t-W`. Since the two occupied subsets have total size greater than `|W|`, their reflected positions intersect. Thus some `x in X cap W` has `t-x in Y`, and `|S|+x+(t-x)=2^k` is a cycle length by Theorem 1. QED.

The strict inequality is sharp for arbitrary integer sets: at equality the occupied reflected positions may be complementary and no target sum need occur.

**Necessary condition for a counterexample.** If a graph has no power-of-two cycle, then for **every** edge cut, every compatible matching state, every target `2^k`, and every finite `W`,

\[
\boxed{|X\cap W|+|Y\cap(2^k-|S|-W)|\le |W|.}
\]

This is an exact *spectral sparsity obstruction* on all graph components. It is particularly useful when structural arguments supply **lower bounds on the number of distinct path/linkage lengths** in an arithmetic progression. Unlike width-only scores, it remains valid for bipartite components whose path lengths occur at spacing two.

## Recovering all bridge transfer cases from one four-pole

Let a parent graph have disjoint edges `ab,cd`. Remove those edges to get pole `A` with ports `a,b,c,d`. Let pole `B` consist of an edge `xy` with ports `x,x,y,y`, respectively. Gluing creates exactly the usual edge bridge.

The only possible boundary patterns produce:

| Boundary state | Length in bridged graph | Interpretation in parent |
|---|---|---|
| Entirely in `A` | `L` | Old cycle using neither edge |
| Two edges across cut, both ports at `x` or `y` | `L+2` | Parent cycle using exactly one deleted edge has length `L+1` |
| Two edges across cut, one port at each | `L+3` | New bridge-edge cycle from an old endpoint-to-endpoint path of length `L` |
| Four edges across cut | `L+4` | Parent cycle using both deleted edges has length `L+2`; `A` supplies *two vertex-disjoint paths* |

For a target dyadic length `q`, these four classes demand respectively `L=q`, `q-2`, `q-3`, `q-4`. These are equivalent to the previously described parent-cycle lengths `q`, `q-1`, `q-2` and parent endpoint path length `q-3`.

Deleting a new root `x` leaves only bridge-free paths on the `y` side, and the same signature formula gives the exact new-root condition without a separate proof. This shows that the earlier bridge- and cut-specific tools are manifestations of one operation.

## Validation and scope

The companion script `boundary_linkage.py` is an exact **small-instance oracle**, not a scalable solver: it enumerates simple paths and collections of vertex-disjoint paths. Tests independently enumerate all simple cycles in the glued graph using NetworkX and compare length sets. Included:

* The four-edge-cut cube and root-forbidden variants.
* A four-terminal construction where the only 8-cycle across the cut uses **all four cut edges**, revealing the missing two-linkage term.
* Arbitrary cuts with repeated endpoints, including a bridged `K4` and every possible old/new root.
* Random cubic-graph cuts, random small pole compositions, and the theta-pole endpoint-width counterexample.
* Integer and parity-window density certificates, including randomized implication checks.

The proof does not depend on the tests. The tests only guard the formal implementation.

## What remains, and how to aim at a genuine breakthrough

The transfer algebra is exact but cannot **force** a rich signature for a graph with minimum degree three. This is the true missing theorem; merely counting states or running SAT does not supply it.

**Proposed frontier: a linkage-spectrum expansion theorem.** Seek a structural condition implied by cyclic four-edge-connectivity (or a weaker condition available for minimal general counterexamples) that produces, at a suitable cut and compatible pairing, enough *distinct total linkage lengths* in a common parity window to violate the spectral sparsity inequality above.

This would immediately imply a power-of-two cycle and would automatically apply both to bridges and to three-/four-edge cut compositions. An initial proof target is a near-balanced two-linkage density lemma in a cyclically four-edge-connected cubic graph with a prescribed root. Any such lemma must be tested against the known 24- and 78-vertex sparse-cycle constructions before considering it credible.

**Literature positioning.** Boundary matching states and linkage-based dynamic programming appear in prior connectivity algorithms, for example Nederlof–Pilipczuk–Swennenhuis–Węgrzycki (2023, *SIAM J. Discrete Math.*), and Kingan–Kingan (2024) use edge bridging for cyclically four-edge-connected cubic graphs. The contribution of this research pass is a precise synthesis tailored to **simple-cycle length spectra and dyadic additive obstructions**; originality beyond that synthesis has not been established.
