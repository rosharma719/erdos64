# Research pass VIII: fractional dyadic-cycle resilience under edge bridging

**16 November 2026.** Status: a proved, general quantitative bridge-survival theorem; an exact linear-programming dual; an infinite-family result for arbitrarily many bridge operations on large prism/Möbius-ladder bases; finite verification of the small one-bridge exceptions; and explicit counterexamples to two tempting stronger statements. **The full prime bridge-stability conjecture and the Erdős–Gyárfás conjecture remain open.** These elementary incidence and LP arguments have not been established as new in the broader literature.

## 1. Why revisit bridge repair?

The exact decomposition in `bridge_prime_reduction.md` expresses dyadic cycles in the child in four classes: parent cycles of lengths `q`, `q-1`, or `q-2`, with the prescribed use of the bridged edges, and paths of length `q-3` closed across the new bridge. A claim that connectivity automatically creates the fourth class is **false** (explicit prime example below). A different mechanism should control the cases where an old dyadic cycle can survive untouched.

The global idea is to keep **a weighted family of dyadic cycles**, rather than committing to one cycle. One bridge can damage only two *original edges*. A family with low incidence at every edge and vertex cannot be entirely destroyed or concentrated through one vertex.

## 2. The fractional resilience potential

Let `D(G)` denote the set of all simple cycles of lengths `4,8,16,32,...` in a finite graph `G`. For any nonzero nonnegative weights `w_C` on these cycles, set

```
W(w)     = sum_{C in D(G)} w_C
alpha(w) = max_{v in V(G)} sum_{C containing v} w_C
beta(w)  = max_{e in E(G)} sum_{C containing e} w_C.
```

Since every cycle uses at least one edge, `beta(w)>0`. Define

\[
\boxed{\rho(G)=\sup_{w\geq0,\ w\ne0}\frac{W(w)-\alpha(w)}{2\beta(w)}}
\]

and define `rho(G)=0` if `G` contains no dyadic cycle. `rho` is finite: `4W<=sum_e sum_{C containing e} w_C<=|E(G)| beta`. Also `0<=alpha<=W`, so `rho>=0`.

**Theorem 1 (exact rooted criterion).** `rho(G)>0` **if and only if** every vertex `v` can be avoided by some dyadic cycle.

*Proof.* If a vertex `v` lies on every dyadic cycle, then `alpha(w)=W(w)` for every choice of weights, so `rho=0`. Conversely, if every vertex is avoided by at least one dyadic cycle, put positive weight on every dyadic cycle. Each vertex omits some positive weight, so `alpha<W`, whence `rho>0`. QED.

**Theorem 2 (one-step bridge inequality).** If `B=B(G;e,f)` is obtained by bridging any two vertex-disjoint edges, then

\[
\boxed{\rho(B)\geq\max\{0,\rho(G)-1\}.}
\]

*Proof.* For any weights on parent dyadic cycles, discard cycles that use either `e` or `f`. All other cycles remain **identical** dyadic cycles in the child, avoiding both new subdivision vertices. Their total weight is at least `W-2 beta`. Their maximum vertex and edge incidence is at most `alpha` and `beta` respectively. If `(W-alpha)/(2 beta)>1`, then the retained family has strictly positive weight margin, and its ratio satisfies

\[
\frac{W'-\alpha'}{2\beta'}\geq
\frac{W-2\beta-\alpha}{2\beta}=
\frac{W-\alpha}{2\beta}-1.
\]

Here the ratio inequality is valid because the numerator is positive and `beta'<=beta`. For a parent ratio at most 1 the claimed lower bound is zero and follows from nonnegativity. Take the supremum over parent weights, allowing an arbitrarily close approximation. QED.

**Corollary (arbitrary depth).** For any sequence of `t` edge bridges, with no restrictions on the intermediate graphs,

\[
\boxed{\rho(G_t)\geq\max\{0,\rho(G_0)-t\}.}
\]

Therefore `rho(G_0)>t` implies that `G_t` remains rooted dyadic-cycle robust. Equivalently, **only the low-resilience region** `0<rho(G)<=1` needs a genuine shifted-cycle or bridge-path repair argument for one step. This formulation does not claim that one of those repairs always exists.

### Weighted cycle-family version

The proof also yields a direct, hand-checkable sufficient certificate. For *any* chosen finite family of original dyadic cycles and nonnegative weights,

\[
\boxed{W>\alpha+2t\beta\ \Longrightarrow\ G_t\text{ is root robust}.}
\]

This is valid without enumerating all cycles in the graph. It depends only on the supplied family and its vertex/edge incidences. A hypothetical root-critical descendant requires `W<=alpha+2t beta` for **every** family and weight choice on its ancestor.

## 3. The exact LP dual: an edge/vertex fractional cover

Normalize edge capacity to `beta<=1`. Write `a` for the maximum vertex load. Standard finite-dimensional LP duality gives

\[
2\rho(G)=\max_{w_C,a\ge0}\left(\sum_C w_C-a\right)
\]

subject to

\[
\sum_{C\ni e}w_C\le1\quad(\forall e),\qquad
\sum_{C\ni v}w_C\le a\quad(\forall v).
\]

The dual is

\[
\boxed{2\rho(G)=\min\sum_e y_e}
\]

where `y_e,z_v>=0`, with

\[
\sum_v z_v\le1,\qquad
\sum_{e\in C}y_e+\sum_{v\in C}z_v\ge1
\quad(\forall C\in\mathcal D(G)).
\]

Thus `rho` is **half the smallest fractional edge weight needed to cover every dyadic cycle when up to one unit of vertex-cover weight is free**. If one vertex meets every dyadic cycle, putting vertex weight 1 there yields `rho=0`, consistent with Theorem 1.

The optional SciPy checker `fractional_bridge_resilience_lp.py` solves both LPs independently on bounded graphs, and tests equality of optimal values. For larger graphs one should supply short weighted cycle families as witnesses instead of enumerating `D(G)`.

## 4. An infinite-family theorem with explicit bridge depth

Let `Q_{2k}` be the cubic prism on `2k` vertices and `V_{2k}` the Möbius ladder, for `k>=4`. Each has `k` distinguished peripheral 4-cycles `S_0,...,S_{k-1}`. Every vertex belongs to exactly two of them; every edge belongs to at most two.

Assign each `S_i` unit weight. Then `W=k`, `alpha=2`, `beta=2`, giving

\[
\rho(Q_{2k}),\rho(V_{2k})\ge(k-2)/4.
\]

**Theorem 3 (ladder-descendant theorem).** *Every graph obtained from either `Q_{2k}` or `V_{2k}` through any sequence of `t` bridge additions contains a 4-cycle avoiding every prescribed vertex whenever*

\[
\boxed{k>4t+2.}
\]

This is proved for **all k and t**, without cycle searches or assumptions on the bridge choices. A root-critical descendant from these bases must have bridge depth at least `ceil((k-2)/4)`; a descendant with no 4-cycles at all requires at least `ceil(k/4)` bridges to destroy this distinguished square family.

For `t=1`, the proof covers `k>=7`. A finite check of every pair of disjoint edges and every old/new root resolves `k=4,5,6` for both families. Thus **every one-step bridge child of any prism or Möbius ladder with k>=4 is root robust**. Independently, all 75 bridge pairs of the Petersen graph also passed the rooted checks, as did all 3 bridge pairs of `K4` (yielding `K_{3,3}`).

| Base | Bridges checked | Roots checked per child | Result |
|---|---:|---:|---|
| `Q8`, `V8` | 42 each | 10 | all root robust |
| `Q10`, `V10` | 75 each | 12 | all root robust |
| `Q12`, `V12` | 117 each | 14 | all root robust |
| Petersen | 75 | 12 | all root robust |
| `K4` | 3 | 6 | all root robust |

These are enumerations of **edge pairs**, not isomorphism class counts. The full finite census tests 546 bridge pairs and 6,834 rooted child instances, using both a fixed-length DFS oracle and a separate NetworkX directed simple-cycle oracle for the ladder and Petersen cases. The proofs for arbitrarily large k and arbitrary t do not rely on these finite checks.

## 5. Two essential counterexamples and a nonmonotone potential

### A. Three-vertex connectivity alone is insufficient

The six-vertex triangular prism (graph6 `E{Sw`) is **root robust**: every vertex can be avoided by one of its three squares. Bridge `e={0,1}`, `f={2,5}`. The new 8-vertex cubic graph is still **3-vertex-connected**, but its old vertex `2` lies on *every* dyadic cycle, i.e., it is root critical. An independent enumeration of all 4- and 8-cycles of the child confirms this.

Both parent and child have cyclic three-edge cuts. Thus the cyclically four-edge-connected assumption in the prime bridge program is substantive; even 3-vertex-connectivity does not suffice. Certificate: `nonprime_bridge_failure_certificate.json`.

### B. Newly bridged paths are not guaranteed as the repair mechanism

The prime 12-vertex cubic graph encoded by graph6 `KKbA?Wo?x_@P` is root robust. Bridge `e={2,8}`, `f={4,11}`, and choose old root `r=7`. The resulting 14-vertex graph is also cyclically four-edge-connected and root robust. However **no root-avoiding dyadic child cycle uses the new bridge edge `xy`**.

Instead a parent 7-cycle `0-3-8-9-6-11-4-0`, using just `f`, lifts to an 8-cycle avoiding root `7`. All other root-free dyadic child cycles in this instance likewise arise from +1 shifted parent 7-cycles. Independent complete child cycle enumeration verifies the absence of any root-free dyadic cycle through `xy`. Certificate: `shift_only_bridge_certificate.json`.

The preceding research pass has the complementary 14-vertex prime example where **only a new bridge path** gives the rooted dyadic witness. Therefore a proof that keeps only shifted parent cycles or only new bridge paths cannot work.

### C. Resilience is not monotone under prime bridging

A prime bridge of the 8-vertex cube across `{0,1}` and `{2,6}` decreases `rho` from `3/4` to `1/2`. Both graphs remain root robust. The general one-sided bound `rho(child)>=rho(parent)-1` is the correct unconditional statement; monotonicity is false, even within the cyclically four-edge-connected class.

## 6. Where the genuine proof problem remains

The high-resilience part of bridge stability is settled by Theorem 2:

> Every bridge with parent `rho>1` preserves root robustness, for arbitrary finite graphs.

The only remaining case for the **proposed prime bridge-stability induction** is:

> If `G` and the result of an admissible bridge are cyclically four-edge-connected cubic graphs, and `0<rho(G)<=1`, must one of the exact `q`, `q-1`, `q-2`, `q-3` predecessor mechanisms force `rho(child)>0`?

This is **not proved**. The two counterexamples distinguish the shifted-cycle and path mechanisms and show why both must be retained. A promising next conceptual task is to prove a **low-resilience renewal lemma** from the LP dual: a small fractional edge/vertex cover of dyadic parent cycles may force complementary detour paths across the two bridged edges under cyclic four-edge-connectivity. That would turn the bridge transfer rule into a usable induction rather than an enumeration problem.

Kingan & Kingan (2024) give the relevant structural characterization of cyclically four-edge-connected cubic graphs: https://doi.org/10.1080/09728600.2024.2333397 . The Erdős–Gyárfás conjecture itself is still open, and no novelty claim is made for the incidence/LP formulation without a broader literature comparison.

## 7. Reproduction

```
python -m pytest -q tracks/2026-11-halving/scripts/
```

Files:

- `bridge_family_robustness.py` — exact rational weighted incidence certificates and arbitrary-depth square-family witness extraction.
- `fractional_bridge_resilience_lp.py` — optional SciPy primal/dual LP checker on small graphs.
- `test_bridge_family_robustness.py` — structural incidence, finite bridge checks, new/old roots, and explicit counterexamples.
- `test_fractional_bridge_resilience_lp.py` — optional LP strong-duality and nonmonotonicity checks.
- `shift_only_bridge_certificate.json` and `nonprime_bridge_failure_certificate.json` — minimal reproducible labeled examples.
