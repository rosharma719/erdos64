# Structural pass V: parity-resolved spectra and rooted prime obstructions

**Research note, 16 November 2026.** This pass tests the proposed program of lower-bounding the three-terminal score `Phi` on cyclically 4-edge-connected cubic components. It finds a fundamental defect in the score for bipartite components, repairs part of that defect with parity-resolved spectra, and isolates a sharper obstruction involving dyadic cycles that avoid the attachment vertex. **The conjecture remains open. Novelty of these lemmas has not been established.**

## 1. Why the old score is unsuitable for a universal lower bound

Recall a three-terminal pole `P` with terminals `t_0,t_1,t_2`, and let `S_ij` denote the lengths (in edges) of simple paths connecting `t_i,t_j`. The earlier score was

`omega(S)=max { b-2a-1 : [a,b]∩Z is contained in S }`, and `Phi(P)=sum_(i<j) omega(S_ij)`.

**Proposition 1 (parity blind spot).** If `H` is a simple **3-connected** cubic bipartite graph of girth `g` and `v` is any vertex, then `P=H-v`, with the three neighbors of `v` as terminals, satisfies

`Phi(P) <= -3(g-1)`.

**Proof.** The three neighbors of `v` lie in the same bipartition class. Thus every terminal-to-terminal path in `H-v` has even edge length, so any *integer-consecutive* interval contained in its spectrum is a singleton `[a,a]`. Closing that path with its two incident edges at `v` makes a cycle of length `a+2` in `H`; hence `a>=g-2`. Its score is `a-2a-1=-a-1<=1-g`. Sum over the three terminal pairs. QED.

This proposition gives an *upper* bound, growing more negative with girth. It invalidates any attempt to obtain a nonnegative lower bound by assuming the old `Phi` detects broad terminal-path spectra on every prime. It does **not** itself prove unbounded negative `Phi` over prime graphs; that further assertion would require an existence theorem for prime bipartite cubic graphs of arbitrarily large girth.

Concrete computed examples (all use the pole obtained by deleting any vertex):

| Capped cubic graph | `Phi` | Even-stride score `Phi_2` |
| --- | ---: | ---: |
| `K_{3,3}` | -9 | -3 |
| Cube | -9 | +3 |
| Heawood | -15 | +9 |

The difference reflects *certified realizable path lengths*, not a numerical heuristic.

## 2. A parity-resolved two-sided obstruction

For a nonempty integer path spectrum `S`, choose a parity `e ∈ {0,1}` and let `[a,b]_2={a,a+2,...,b}`, where all elements have parity `e`. Define

`omega_e(S)=max {b-2a-1 : [a,b]_2 ⊆ S, a≡b≡e mod 2}`

when there is at least one such path. Put `Phi_e(P)=sum_(i<j) omega_e(S_ij)` when the three terms exist.

**Proposition 2 (parity-resolved cut obstruction).** Consider a cubic graph formed by joining two three-terminal poles `A,B` with an independent three-edge cut. If, for either parity `e`, `Phi_e(A)` and `Phi_e(B)` are defined and

`Phi_e(A)+Phi_e(B) >= 0`,

then the glued graph has a power-of-two cycle, regardless of the terminal matching.

**Proof.** For each terminal pair select a step-two interval `[a_A,b_A]_2` and `[a_B,b_B]_2` attaining the two scores. Matching a pair on one side to a pair on the other yields all even crossing-cycle lengths in `[m,M]_2`, where `m=2+a_A+a_B` and `M=2+b_A+b_B`. Since both path lengths have parity `e`, `m` is even. Algebra gives

`M-2m=(b_A-2a_A-1)+(b_B-2a_B-1)`.

The sum of these expressions over all three matched pairs is `Phi_e(A)+Phi_e(B)`. It is unchanged by the matching, so some matched pair has `M>=2m`. Every interval `[m,2m]` with `m>=4` contains a power of two, and that power is even, so it belongs to the certified step-two interval. The corresponding two paths joined by two cut edges form the desired simple cycle. QED.

This extends the previous sufficient width score and is especially useful when both capped factors are bipartite (then all terminal path lengths are even). It remains a **sufficient** obstruction, not a characterization; for example, two `K_{3,3}` poles have aggregate score `-6`, yet their crossing cycles include length 8. The exact union-of-sumsets transfer from pass IV remains definitive where complete spectra are available.

**Small explicit contrast.** Gluing a `K_{3,3}-v` pole to a cube-minus-vertex pole has old aggregate score `-18` and new even-stride aggregate score `0`. Proposition 2 guarantees a crossing 8-cycle in all six attachment orientations, independently verified by constructed cycles.

## 3. The attachment-vertex obstruction is stronger than a width bound

Let `G` have a cyclic three-edge cut with pole `A`; cap `A` by one new cubic vertex `x` to form `H_A`.

**Proposition 3 (root obstruction).** If `G` has no power-of-two cycle, then every power-of-two cycle of `H_A` contains the cap `x`.

**Proof.** A simple cycle of `H_A` avoiding `x` lies entirely in `A`, hence would be a cycle of `G`. QED.

If `G` is chosen as a **minimum-order cubic counterexample** to the Erdős–Gyárfás conjecture, the capped factor `H_A` is a smaller cubic graph, so by minimality it contains a power-of-two cycle. Proposition 3 then says the cap must hit **all** such cycles. The symmetric statement applies to `B`.

Call `(H,v)` *dyadically root-critical* if `H-v` contains no simple cycle whose length is a power of two. Proposition 3 gives a precise necessary condition for cubic counterexamples with cyclic three-edge cuts. It also explains why proving the conjecture for a capped factor does not, on its own, prove it for its 3-sum.

### Prime-factor direction

Consider the stronger statement:

> **Root-robust prime conjecture (research question).** If `H≠K4` is cyclically 4-edge-connected and cubic, then for **every** vertex `v`, `H-v` contains a power-of-two cycle.

This is *not proved* and is logically stronger than the cubic Erdős–Gyárfás conjecture. `K4` is a necessary exception: its 4-cycles use all four vertices. A leaf prime factor in a cyclic-three-cut decomposition has only one artificial cap. Therefore, **conditional on the root-robust prime conjecture**, every leaf prime factor of a cubic counterexample admitting such a decomposition must be `K4`. This does **not** eliminate internal non-`K4` factors, whose cycles can pass through several cap vertices.

A finite falsification check over the previously certified catalogs gives:

| Order of capped cubic graph | Cyclically 4-edge-connected isomorphism classes | Root-critical classes |
| --- | ---: | ---: |
| 4 | 1 | 1 (`K4`) |
| 6 | 1 | 0 |
| 8 | 2 | 0 |
| 10 | 5 | 0 |
| 12 | 18 | 0 |

Thus 26 of the 27 prime classes at orders 4–12 are root-robust. Every vertex has an explicit dyadic-cycle witness avoiding it. The exhaustive finite check does *not* establish the conjecture beyond this range. Two order-8 **nonprime** cubic graphs have root-critical vertices, confirming that primeness is essential even for such a small sample.

A separate exploratory sample of 506 order-14 cubic representatives found no root-critical vertex. This sample **is incomplete** relative to the 509 published isomorphism classes; no complete order-14 classification is claimed here.

**Published context:** Heckman and Krakovski (2013) already proved the ordinary Erdős–Gyárfás conjecture for 3-connected cubic planar graphs. Their theorem does *not* state the stronger root-robust version. Consequently, if we pursue this direction, nonplanar prime graphs and vertex-avoiding cycles are the substantive frontier, not reproving the known planar result.

## 4. A sharper exact rule for triangle-leaf factors

For the pole obtained from `K4` by deleting a vertex, the three terminal-pair path spectra are exactly `{1,2}`. Hence joining this triangular pole to `P` produces, for every terminal pair and every path length `s∈S_ij(P)`, crossing cycles of lengths `s+3` and `s+4`.

**Proposition 4 (triangle-leaf gap rule).** If a cubic graph with such a triangle side contains no power-of-two cycle, then for every pair of terminals in its other side `P`,

`S_ij(P) ∩ {2^k-3, 2^k-4 : k>=2} = ∅`.

The statement is exact for crossing cycles; its proof is the transfer identity from pass IV with the triangle's `{1,2}` path spectrum. Combined with Proposition 3, it says that a smaller capped factor can have a dyadic cycle only through the attachment vertex, while its corresponding terminal path spectra must avoid the two immediately preceding offsets. This is a concrete **rooted spectrum-gap** problem, more sharply targeted than seeking a uniform positive `Phi` bound.

## 5. Suggested structural route, not a search escalation

1. **Prove or falsify root-robustness for cyclically 4-edge-connected prime cubic graphs.** A promising lemma would show that a dyadic cycle through `v` can be rerouted to avoid `v`, perhaps using cyclic edge-connectivity and two-path switching. The order-12 census is a sanity check, not a substitute for such a proof.
2. **Use the triangle-leaf gap rule when all decomposition leaves are `K4`.** Show that a root-critical non-`K4` core cannot simultaneously omit both offsets before every relevant power of two, potentially using local theta-subgraphs or the parity-resolved spectrum rather than counting all paths.
3. **Keep the exact transfer identity as the final verifier.** Only invoke SAT or finite cycle search to disprove a carefully formulated candidate lemma or independently certify short exceptional cases.

None of these statements proves a reduction from arbitrary minimum-degree-3 graphs to cubic ones. The work applies to simple cubic graphs and their independent cyclic three-edge cuts.

## 6. Reproducing the bounded checks

Implementation: `scripts/prime_pole_obstructions.py`. Tests: `scripts/test_prime_pole_obstructions.py`. They use the previously included n=8/10/12 cubic catalogs and NetworkX. The reference `dyadic_cycle_avoiding_vertex` uses small-graph DFS and returns an actual cycle; it is not intended as a polynomial-time theorem prover.

```sh
python -m pytest -q tracks/2026-11-halving/scripts/test_prime_pole_obstructions.py
python -m pytest -q tracks/2026-11-halving/scripts/test_*.py
```

**Literature to compare before making a novelty claim:**

- Heckman and Krakovski, *Erdős–Gyárfás Conjecture for Cubic Planar Graphs*, Electronic Journal of Combinatorics 20(2), 2013. https://doi.org/10.37236/3252
- Garcia, *Small graphs without power-of-two cycles*, 2026, arXiv:2609.04686. https://arxiv.org/abs/2609.04686
- Ducoffe and Dumitru, *Towards a more structured search for Erdős–Gyárfás counter-examples*, 2026, arXiv:2609.28594. https://arxiv.org/abs/2609.28594
