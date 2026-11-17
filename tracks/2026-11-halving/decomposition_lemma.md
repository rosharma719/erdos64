# Pass XII — Capped-pole decomposition audit

## Scope and status

- **PROVED (restricted):** The cyclic-three-edge-cut decomposition and transfer lemma below, assuming the capped graph is three-edge-connected.
- **OPEN:** The full decomposition lemma for an arbitrary clean 3-pole.
- **CONDITIONAL:** WRP rules out minimal clean 3-poles with three-edge-connected caps, by the restricted lemma and the tower theorem.
- **OPEN:** The reduction through one- and two-edge cuts, so the implication `WRP ⇒ T` remains unproved.

## Setup

Let `P` be a clean 3-pole (connected simple graph with exactly three degree-2 vertices and all others degree 3; no power-of-two cycle). Let `H=P+v` be the cubic cap obtained by adding a new vertex `v` adjacent to the three degree-2 vertices. The cap itself may contain power-of-two cycles through `v` and is **not** asserted clean. Keep all three ports distinct; derive their identities from the internal degree-2 vertices, not any stale graph6 numbering.

Suppose `P` has the **smallest** order among the clean 3-poles outside `{T,S,U,H15}`. Every proper clean 3-pole subpiece is consequently one of the four listed types.

## A: Cyclic three-edge cuts (PROVED under three-edge connectivity)

Assume `H` is three-edge-connected. Consider a nontrivial cyclic 3-edge cut `δ(S)` with `v∉S`. The three cut edges have pairwise distinct endpoints on `S` (and on its complement). To see this, if two cut edges shared `x∈S`, then the remaining edge incident to `x` would run inside `S`. The cut separating `S\{x}` from the rest would have size at most two, contradicting three-edge connectivity; the same argument applies on the other side. Nontrivial means both sides have at least two vertices, so the one-vertex exception is inapplicable.

Therefore `H[S]` is a connected graph with exactly three degree-2 terminals and all other vertices degree 3. Its cycles lie in `P`, so `H[S]` is clean. If `S` is proper, `H[S]` has fewer vertices than `P` and must be one of `T,S,U,H15` by minimality. Contract `S` to a single cubic vertex, remembering the three cut-edge attachments as a port orientation. Connectivity of all cuts of size at least three survives contraction. Repeat, always choosing a nontrivial cyclic cut away from the root, and interpreting already-contracted vertices as their recorded three-terminal substitutions. Their preimages in the original `P` remain proper clean 3-poles and thus belong to the list.

The process terminates because each contraction strictly reduces the order. Its rooted quotient `B` has no nontrivial cyclic 3-edge cut, is three-edge-connected and cubic, and retains the cap root `v`. It is cyclically four-edge-connected in the usual sense. The original `P` is obtained by replacing vertices of `B−v` by the recorded clean pieces or identities, each with a specified bijection between its three ports and the three incident base edges.

**PROVED — The quotient is not `K4`.** If `B=K4`, then `B−v` is a triangle with its three vertices replaced by pieces in `{I,T,S,U,H15}`. The 35-case extension of the tower interval table (proved in `tower_theorem.md`) says the only clean resulting poles are `T,S,H15`; none is a minimal outside pole. This contradiction excludes `K4`.

**PROVED — Exact lifting.** For a simple base cycle `C` avoiding `v`, let `X_u(i,j)` be the internal simple-path length set of the piece substituted at `u`, between the two ports corresponding to the two base edges used by `C`. Every choice of those paths yields a simple lifted cycle in `P`, since pieces are vertex disjoint and `C` visits each base vertex at most once. Its length set is exactly

`|C| + Σ_{u∈C} X_u(i_u,j_u)`.

All four listed clean gadgets and the identity have complete intervals for every terminal pair. Consequently every base cycle has a lifted interval with the indicated sum of endpoints. An attained power of two contradicts cleanness of `P`.

## B: Cuts of size two (OPEN)

For a 2-edge cut away from `v` with distinct endpoints on the away side, the away side is a **clean 2-pole**, with two degree-2 vertices and all others degree 3. Classifying or excluding such objects is a different problem. If the two boundary edges share an endpoint `x` on that side, the away side contains an internal degree-1 vertex `x`, and a smaller bridge-cut case must be handled first; it cannot be called a 2-pole in the stated definition.

**COMPUTED (dual implementation):** No clean connected 2-pole on 4 or 6 vertices; counts of all unlabelled connected candidate graphs are respectively 1 and 4. This does not settle the open 2-pole obstruction, nor does it independently certify the user's previous claims about orders 8–12. A 2-pole has even order by the degree sum `(3N−2)/2`.

**OPEN:** Whether *any* clean 2-pole exists, and how the decomposition changes if one does. The requested exhaustive `geng` range through order 22 was not available in this environment.

## C: Bridges / one-poles (OPEN)

For a bridge separating a component `Q` away from `v`, `Q` is a connected **clean 1-pole**: exactly one internal degree-2 vertex at the boundary and all other vertices degree 3. Joining two disjoint copies of `Q` by an edge between their degree-2 vertices makes a connected cubic graph of order `2|Q|`, and the joining edge is a bridge. Every cycle lies entirely inside one copy of `Q`; hence this new cubic graph has no power-of-two cycle.

**CONDITIONAL on published verification of all cubic graphs through order 48:** `2|Q|>48`; because `|Q|` is odd (from `(3|Q|−1)/2` integral), `|Q|≥25`. This excludes only small one-poles; it does not prove the absence of all one-poles, and relying on the full cubic conjecture here would be circular.

## D: The precise WRP and what follows

**OPEN — WRP (prime-base window-root property):** For every cyclically four-edge-connected cubic base `B≠K4`, every root `r`, and every assignment to each vertex of `B−r` of one of `I,T,S,U,H15` together with a bijection of its three ports to its incident base edges, some simple cycle `C⊆B−r` has a lifted interval containing a power of two.

**PROVED (logical implication):** `WRP` plus the **hypothesis that the capped graph of a minimal counterexample to T is three-edge-connected** implies no such minimal counterexample exists, by parts A and D. More precisely, WRP excludes the minimal outside pole **whenever its cap is three-edge-connected**.

**OPEN:** `WRP ⇒ T` in general, because a minimal outside pole may have a cap with a bridge or 2-edge cut. The classifications or length-forcing conditions needed for those cases have not been established. It is therefore unjustified to mark T equivalent to WRP.

**PROVED independently:** If T were established, then every connected cubic counterexample would yield a clean three-pole by deleting a leaf of a spanning tree. This limits its order to 4,8,16, which are already in the verified small-cubic range. This implication does not depend on WRP or the cap-decomposition lemma.
