# Pass XXVI — Chord interlacement, exact cycle smoothing, and an odd-square parity obstruction

**Date:** 2026-11-16. **Objective:** Advance the Erdős–Gyárfás program using a global, scale-aware framework, and distinguish new deductions from established literature.  **Main conclusion:** A universal exact chord-smoothing model and two unconditional partial theorems, including a dyadic theorem for a nonplanar infinite family of triangle-expanded cubic graphs. The general Erdős–Gyárfás conjecture remains **OPEN**.

## Status convention

- **PROVED (hand argument):** A proof is supplied below, unrefereed.
- **COMPUTED:** The finite tests are reproduced by the included Python scripts; finite tests are not general proofs.
- **PUBLISHED:** Established literature is cited by author and link; we do not claim priority for standard chord-diagram tools.
- **OPEN:** An unsolved extension.

## 1. Universal chord-smoothing representation (PROVED; elementary cycle-space encoding)

Let `G` be a simple cubic graph with Hamiltonian cycle `C=(0,1,...,n-1,0)` where `n=2m`. The off-cycle edges form a perfect matching `M` of `m` chords. Choose a nonempty subset `S⊆M`, of size `r`, whose endpoints in circular order are `t_1<t_2<...<t_{2r}`.

Define the two **alternating boundary perfect matchings** on these endpoints:

- `Q_0={(t_1,t_2),(t_3,t_4),...,(t_{2r-1},t_{2r})}`;
- `Q_1={(t_2,t_3),(t_4,t_5),...,(t_{2r},t_1)}` with the last pairing understood cyclically.

A pair in `Q_j` is realized by the *forward arc along C* between the two selected endpoints. Let `A(S)=Σ_{j=1}^r(t_{2j}-t_{2j-1})`. The unions of the selected chord edges and the selected alternating boundary arcs give two **2-regular subgraphs** `F_0(S),F_1(S)`, with exact sizes

`|E(F_0)|=r+A(S)` and `|E(F_1)|=r+n-A(S)`.

At each selected endpoint, precisely one boundary arc and its chord meet. At other vertices, zero or two boundary edges meet. Thus each union is vertex-disjoint simple cycles. It is a **single simple cycle** iff the multigraph on the `2r` selected endpoints with edges `S ∪ Q_j` is connected (boundary paths suppressed). Conversely, every simple cycle in `G` other than `C` uses a nonempty set `S` of matching chords, and its boundary arcs necessarily alternate among the successive chord endpoints; therefore it arises from precisely such a pair `(S,j)`.

Let `τ_S` be the fixed-point-free involution pairing the selected chord endpoints and `ρ_j` the involution pairing `Q_j`. The number of components of the 2-regular multigraph `S∪Q_j` is `(# permutation cycles of τ_Sρ_j)/2`: an alternating circuit of length `2q` splits into two `q`-orbits under two-step permutation. Thus a single-cycle certificate is

`#cycles(τ_Sρ_j)=2`.

**Exact formulation:** `G` has a dyadic cycle iff either `n` is a power of two, or there exist `S,j` with `#cycles(τ_Sρ_j)=2` and `|S|+A_j(S)=2^k` for some `k≥2` (where `A_0=A` and `A_1=n-A`). This is an exact dictionary, not a proof that the certificate exists. It shows why merely adding independent chord shortcuts misses cycles: interacting chord choices can still form *one* connected circuit.

**Concrete witness.** Take `n=10` and `M={(0,2),(1,6),(3,7),(4,8),(5,9)}`. Its crossing graph is connected, hence this Hamiltonian cubic graph is 3-connected (standard chord-decomposition criterion; see Pass XXV). Disjoint-arc chord shortcuts never remove exactly 2 edges, so that limited family misses an 8-cycle. Yet `0,1,2,3,7,6,5,9,0` is an 8-cycle, using crossing chords `(3,7)` and `(5,9)`. This refutes a shortcut-only completeness claim.

## 2. Local crossing degree yields exact cycle lengths or a separator (PROVED)

For a chord `e=ab`, let `d=deg_{I_C}(e)` be its degree in the chord-intersection graph `I_C`, i.e. the number of other chords crossing `e`. Let `u` be the number of other chords with both endpoints on one open arc from `a` to `b`; let `v` count those entirely on the other arc. Every crossing chord contributes **one endpoint to each arc**, and every noncrossing chord contributes **two endpoints to one arc**. Therefore the two simple cycles using exactly `e` and one Hamiltonian arc have lengths

`ℓ_1=d+2+2u,       ℓ_2=d+2+2v,       u+v=m-1-d`.

In particular, if both `u` and `v` are positive, the chord sets represented by `u` and `v` lie on opposite sides of `e` and **no chord in one set crosses a chord in the other**. Hence `I_C-N[e]` is disconnected, where `N[e]` is the closed neighborhood of `e` in `I_C`.

**Separator–cycle dichotomy:** For any chord `e` of degree `d`, either `G` contains a cycle of length `d+2` using only `e` plus `C`, or the closed neighborhood `N[e]` separates `I_C` into two nonempty groups of chord vertices. Thus, in a dyadic-free `G`, every chord of degree `2^k-2` (for `k≥2`) must have such a separating neighborhood.

This is **one-way**: the separator condition is necessary for an obstruction, not sufficient.

### Consequence: cycle interlacement forces squares (PROVED)

Suppose `I_C` itself is a cycle `C_m`, `m≥3`. Then every chord has `d=2`. Removing the chord and its two neighbors from `I_C` leaves either no vertices (`m=3`) or a connected path (`m≥4`). Therefore `u=0` or `v=0` for every chord, and one arc has length `3` edges. **Every chord belongs to a 4-cycle**, so `G` has at least `m` distinct squares. This includes odd `m`, for which `I_C` is nonbipartite and `G` is nonplanar (in a planar Hamiltonian embedding the non-crossing chords inside and outside `C` would 2-color `I_C`).

For comparison, if `I_C` is a tree then an independent geometric reduction shows `G` is built from `K_4` by repeatedly replacing one vertex with a triangle. Indeed draw the chords as curves with generic pairwise crossings. Because the crossing graph is a tree, the diagram of chord arcs is a plane tree with `m-1` four-valent internal crossings and `2m` boundary leaves. A crossing incident to at least three leaves exists by counting; those three leaves are consecutive on the boundary, with the endpoints of a leaf chord flanking an endpoint of its unique crossing neighbor. Removing that chord contracts a triangle in `G`; the remaining crossing diagram is again a tree. Induction ends at two crossing chords and `K_4`. Insertion of the triangle preserves the two Hamiltonian color-pair cycles, showing these graphs are Kotzig graphs. This is a structurally useful class but stays **planar**, already covered by Heckman–Krakovski (2013), so it is not the main new frontier.

## 3. Odd-square parity preservation under one-round triangle expansion (PROVED)

Let `H` be any finite simple cubic graph, and let `𝒬` be a collection of an **odd number** of distinct 4-cycles such that **every vertex occurs in an even number of cycles in 𝒬**. Select an arbitrary vertex subset `X`. **Expand each vertex in X exactly once** into a triangle, attaching its original three incident edges to three distinct vertices of the triangle. Denote the resulting cubic graph by `H_X`.

**Theorem:** `H_X` has a 4-cycle or an 8-cycle, for *every* choice of `X` and every attachment order.

*Proof.* Fix any square `Q` of `H`, and put `t=|V(Q)∩X|`, `0≤t≤4`. For each expanded vertex on `Q`, the two used external edges can be connected through its replacement triangle either by its direct side (increasing the lifted length by 1) or by the other two sides (increasing it by 2). The choices are independent and yield **all** lifted simple-cycle lengths in the integer interval `[4+t,4+2t]`. If `t=0`, a 4-cycle survives. If `t≥2`, this interval contains 8. Hence absence of both 4 and 8 would require `|Q∩X|=1` for **every** `Q∈𝒬`. Summing over `𝒬`,

`|𝒬| = Σ_{Q∈𝒬}|Q∩X| = Σ_{v∈X} #(Q∈𝒬 containing v)`.

The left side is odd and the right side is even, a contradiction. QED.

**Linear-algebraic form:** If `A` is the square-by-vertex incidence matrix over `GF(2)`, then any one-round expansion avoiding 4 and 8 would require `A x = 1`. An **odd** left-null vector `y` with `y^T A=0` and `y^T 1=1` gives a contradiction. Thus any cubic base graph whose 4-cycle incidence matrix excludes the all-ones vector from its column space has the one-round robustness property. This is a broad **certificate**, not restricted to chord graphs.

### Application: infinite nonplanar family (PROVED)

Let `I_C=C_m` with odd `m≥5`. By Section 2 every chord has a unique length-three arc on `C`, yielding a square `Q_e`. This gives exactly `m` squares. Every vertex occurs in **exactly two** of these squares:

- each vertex belongs to the square of its own matching chord;
- there are `4m` total vertex incidences among `2m` vertices, so the average multiplicity is two;
- no vertex can belong to *two further* squares as an internal vertex of their three-edge arcs, since those two chords and the vertex's own matching chord would then be pairwise crossing, forming a triangle in `I_C`, contrary to `I_C=C_m` with `m≥5`.

Thus every vertex occurs twice. Since `m` is odd, the square-parity theorem applies. **Every one-round triangle expansion of such an odd-cycle-core contains a 4- or 8-cycle.** These are generally nonplanar, 3-connected cubic graphs, and arbitrary subsets of original vertices may be expanded.

For `m=3`, the core is `K_{3,3}`. In a standard six-vertex Hamiltonian labeling, the three squares with vertex sets `{0,1,2,3}`, `{0,1,4,5}`, `{2,3,4,5}` are odd in number and cover every vertex twice. The same conclusion applies.

This proves Erdős–Gyárfás for an infinite nonplanar family beyond the planar cubic theorem. **It is a special-family result and does not solve the general problem.**

## 4. Evidence / reproducibility (COMPUTED)

`check_chord_smoothing.py` (stdlib only) tested 11,460 complete chord diagrams with 3–6 chords for the arc degree and separator identities; 343 interlacement-tree diagrams for the two Hamiltonian color-pair cycles; 7 cycle-interlacement diagrams for the span-three consequence; and 328 simple cubic Hamiltonian diagrams (orders ≤10) for an independent comparison between the smoothing spectrum and direct simple-cycle DFS. All checks passed.

`check_square_parity.py` checked odd crossing-cycle cores of lengths `m=3,5,7,9`, including all choices of expanded original vertices. The 5/7/9-core checks covered 1,024 / 16,384 / 262,144 subsets respectively; all have an explicit odd family of squares covering each vertex twice.

These checks corroborate the hand proofs and are not themselves general proofs.

## 5. Research priority and boundaries

The **largest remaining useful question** is to extend the incidence/parity certificate beyond one-round expansions and the `4→8` jump. For a base cycle of dyadic length `q=2^k` with `t` expanded vertices, a single round produces all lengths `[q+t,q+2t]`. If `t≥q/2`, this reaches `2q`. Avoiding both `q` and `2q` requires a nontrivial integer constraint on how expansion sites hit a family of q-cycles; for `q=4`, it simplifies to `t=1`, which is precisely why the mod-2 argument works. For larger `q` there are multiple allowed hit counts, so a new **multiscale incidence/discrepancy theorem** is needed.

For general 3-connected Hamiltonian cubic graphs, the matching-smoothing model is exact and subsumes both independent shortcut and crossing interactions. A promising next target is a structural result converting a separator decomposition of `I_C` into a *compatible family of alternating matchings* whose weights straddle a dyadic threshold. The odd-square theorem is a concrete first instance of a topological choice system plus an arithmetic impossibility certificate.

**Limits:** One-round triangle expansion is essential to Theorem 3 as stated. No claim of closure under arbitrary repeated expansions is made. The tree crossing class is planar and is not a new Erdős–Gyárfás case. No claim of priority over chord-diagram or Kotzig-graph folklore is made without specialist review.

## Literature

- Heckman & Krakovski (2013), *Erdős–Gyárfás Conjecture for Cubic Planar Graphs*, Electron. J. Combin., https://doi.org/10.37236/3252.
- Bucić, Gishboliner & Sudakov (2022), *Cycles of many lengths in Hamiltonian graphs*, Forum of Mathematics, Sigma 10:e70, https://doi.org/10.1017/fms.2022.42.
- Traldi (2011), *Binary nullity, Euler circuits and interlace polynomials*, Eur. J. Combin., https://doi.org/10.1016/j.ejc.2011.02.004.
- Circle graph chord-representation and split decomposition: https://doi.org/10.1007/s00453-024-01216-5.
- Ducoffe & Dumitru (2026), *Towards a more structured search for Erdős–Gyárfás counter-examples*, https://arxiv.org/abs/2609.28594.
- Lyngsie & Merker (2021), *Cycle lengths modulo k in large 3-connected cubic graphs*, https://doi.org/10.19086/aic.18971.
