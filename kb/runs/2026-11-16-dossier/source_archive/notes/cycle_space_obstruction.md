# Structural jump: cycle-space averaging and constructive dyadic witnesses

**Research note, 2026-11-16.** Continuation of `mixed_gadget_research.md`.

**Objective.** Replace finite base-graph enumerations by structural obstructions that apply to **every** cubic base graph, irrespective of size. Gadget path-length intervals were already established by Garcia's window lemma (arXiv:2609.04686, §3); the arguments here use those intervals to derive a weighted cycle-space certificate. The resulting inequality has been independently checked by code, but **originality in the broader graph-theory literature has not been established**. It does not resolve the Erdős–Gyárfás conjecture.

## 1. From a cycle spectrum to a signed cycle weight

Let `B` be a finite simple cubic base, and replace each vertex `v` by a three-port gadget. At each unordered pair `q` of ports, assume the set of simple internal path lengths is the **complete integer interval** `[a_v(q), b_v(q)]`. Internal cycles in every gadget are assumed to avoid powers of two if we want to study constructions that avoid all such cycles.

For a simple base cycle `C`, let `q_v(C)` denote the port pair traversed at `v`. The exact cycle-lifting interval (Garcia's window calculus) is

```
m(C) = |C| + sum_{v in C} a_v(q_v(C))
M(C) = |C| + sum_{v in C} b_v(q_v(C)).
```

Define the **width score** of a vertex traversal and of a base cycle as

```
w_v(q) = b_v(q) - 2 a_v(q) - 1
W(C)   = sum_{v in C} w_v(q_v(C)) = M(C) - 2 m(C).
```

**Width lemma.** If `W(C) >= 0`, the expanded graph contains a simple cycle of power-of-two length.

*Proof.* `m(C) >= 3`, since every simple base cycle has at least three edges. The least power of two `p >= m(C)` satisfies `p < 2m(C)` except when `m(C)` is itself a power of two, in which case `p=m(C)`. Thus `W(C)>=0` implies `m(C) <= p <= M(C)`. The interval path spectra guarantee that the choice of internal path lengths can realize `p` exactly. Their paths occur in disjoint gadgets, so the lift is simple. QED.

This is a *sufficient* obstruction, not an equivalence: a lifted interval `[17,32]` has `W<0` but still contains the dyadic length 32.

## 2. Cycle-space averaging theorem

The binary cycle space `Z_1(B; F_2)` consists of all edge subsets with even degree at every vertex. Since `B` is cubic, every even subgraph is a **vertex-disjoint union of simple cycles**. For any even subgraph `F`, define `W(F)` as the sum of the local traversal weights at degree-two vertices (zero at unused vertices). Therefore `W(F)` is the sum of `W(C)` over its components.

**Theorem (cycle-space mean obstruction).** If the average of `W(F)` over all even subgraphs `F` is nonnegative, there exists a simple cycle `C` with `W(C)>=0`. Hence every gadget expansion with interval path spectra satisfying this condition has a power-of-two cycle.

*Proof.* The empty even subgraph has weight zero. If all simple cycles had strictly negative weight, every nonempty even subgraph would have negative weight. Since a cubic graph contains cycles, the average over the cycle space would then be strictly negative. Contradiction. Apply the width lemma. QED.

For **bridgeless** cubic `B`, each vertex sees four equiprobable local configurations in a uniformly random even subgraph: unused, or any one of its three two-edge pairs. To see this, the restriction of the cycle space to the three incident edges is a linear subspace of the even-parity triples. Every incident edge lies on a cycle because it is not a bridge, so this restriction has dimension two and equals `{000,011,101,110}`.

Consequently,

```
4 E_F[ W(F) ] = sum_{v in V(B)} sum_{q among 3 port pairs} w_v(q).
```

This formula is **independent of the topology and size of the bridgeless cubic base**. It depends only on the gadget types, not their port orientations.

### Explicit density obstruction for the current library

| Gadget | Three traversal scores `w_v(q)` | Sum |
|---|---|---:|
| Identity | `-1, -1, -1` | -3 |
| Triangle `T3` | `-1, -1, -1` | -3 |
| Seven-vertex skew `H7` | `-1, +1, +1` | +1 |
| Seven-vertex uniform `H7` | `+1, +1, +1` | +3 |
| Exoo `H15` | `+3, +7, +7` | +17 |

Write the gadget counts as `(n_I, n_T, n_S, n_U, n_15)`. On any bridgeless cubic base, if

```
     -3(n_I+n_T) + n_S + 3 n_U + 17 n_15 >= 0,
```

the expansion **must** contain a cycle whose length is a power of two. Therefore any putative all-power-avoiding expansion in this gadget family must satisfy

```
     3(n_I+n_T) > n_S + 3 n_U + 17 n_15.
```

Corollary: **Every full skew-H7 expansion of every bridgeless cubic base has a power-of-two cycle**, without any order bound or search. With only skew H7 and identity/triangle choices, at least *strictly more than one quarter* of base vertices must be left as identity or triangle gadgets to evade this particular sufficient criterion. For H15, the dilution requirement is stronger.

For cubic graphs **with bridges**, the uniform-four-local-states formula is false at a vertex incident to a bridge; however the general cycle-space mean theorem remains valid, and the software computes each exact affine local distribution from a cycle basis, so it covers that case as well.

## 3. Localized extension: conditioning on an edge

A negative global mean does not preclude a positive mean in a **restricted affine subspace**. If `e` is any nonbridge edge, condition on even subgraphs containing `e` and compute

```
     E[ W(F) | e in F ].
```

If this conditional mean is nonnegative, some such nonempty even subgraph has `W(F)>=0`, yielding a dyadic simple cycle. This is a **strictly stronger certificate procedure** than the global mean test; unlike SAT, it still requires only linear algebra over the base cycle space.

To compute the conditional expectation without enumeration, take an F2 basis of fundamental cycles, solve the single parity equation `e in F`, represent the conditioned space as an affine offset plus independent even-subgraph directions, and project that affine space onto the four possible local states at each vertex. Each local projection has size 1, 2, or 4; exact expectations have denominator dividing four. A method of **conditional expectations** fixes the remaining cycle-basis coefficients one by one without decreasing the mean. It produces an actual even subgraph with nonnegative score, then an actual simple cycle with nonnegative score.

*Tiny example.* On `K4`, take the gadget choices (by vertices `0,1,2,3`): `identity, H7_uniform, H7_skew:012, triangle`. The unconditional score has `4E[W]=-2` and cannot certify anything. Conditioning on the base edge `(2,3)` gives `E[W | (2,3) in F]=0`, producing the triangle base cycle `(1,2,3)` with lifted interval `[8,17]`. The program returns an explicit 8-cycle in the expanded graph. Thus the localized criterion genuinely adds explanatory power beyond a global density threshold.

## 4. Reinterpreting the 78-vertex family

The six previously reconstructed 78-vertex classes each contain **eleven H7-skew gadgets and one identity**, on a 12-vertex bridgeless cubic base. The global signed-width sum is

```
     11 * (+1) + 1 * (-3) = +8,
```

so `4 E[W]=8` and `E[W]=2>0`. In particular, *every orientation* of eleven skew H7 gadgets and one identity on **any bridgeless cubic 12-vertex base** forces some power-of-two cycle, regardless of whether the expansion avoids 4, 8, and 16.

The deterministic polynomial-time witness extractor proves the following for all six archived class representatives:

| Class | Base cycle order | Lift interval | Certified power |
|---:|---:|---:|---:|
| 1 | 10 | `[29,64]` | 32 |
| 2 | 9 | `[29,63]` | 32 |
| 3 | 9 | `[27,63]` | 32 |
| 4 | 9 | `[27,63]` | 32 |
| 5 | 10 | `[29,64]` | 32 |
| 6 | 10 | `[28,64]` | 32 |

The certificates contain actual expanded-graph vertex sequences and verify consecutive edges, simplicity, and lengths. The result explains the observed 32-cycles **without graph-level cycle enumeration**; the prior exhaustive checks only corroborate the constructed witnesses.

## 5. Second structural reduction: path-spectrum dominance

A useful general observation: suppose two gadgets `A,B` have the same three external attachment slots. Each has no internally forbidden cycle. If their pairwise internal path sets satisfy

```
     Paths_A(i,j) ⊆ Paths_B(i,j)   for every two distinct slots i,j,
```

then replacing `B` with `A` cannot create a forbidden lifted cycle length. Every lifted cycle length through `A` was already realizable through `B`; gadget-internal cycles remain safe.

For the forbidden set of **all powers of two >=4**, the skew H7 gadget dominates the uniform H7 gadget: its path sets are `[3,6], [2,6], [2,6]`, compared with `[2,6]` for all three uniform pairs. The extra internal 7-cycle of the skew H7 is allowed. Therefore **the uniform H7 gadget can be removed entirely from existence searches for power-of-two-avoiding expansions**, without changing feasibility. This statement is independent of the base graph's size.

## 6. Limits and next structural targets

- The theorem requires *contiguous* port-pair path spectra. For non-interval gadgets, `M>=2m` alone does not guarantee a realizable dyadic length. A rigorous extension would replace interval width with certified additive-combinatorial coverage of Minkowski sums.
- The global inequality is a one-sided obstruction. A negative mean does not guarantee a valid expansion; the edge-conditioned test can still certify some such cases.
- These results constrain **three-port vertex-replacement families**. They do **not** prove that arbitrary cubic graphs decompose into these gadgets, let alone settle all minimum-degree-three graphs.
- The next genuine conceptual target should be a *multi-cut/prime-core* theorem: use cycle-space constraints across cyclic three-edge cuts, and identify what must be proved for cyclically four-edge-connected cubic cores. Enlarging a gadget catalog and running SAT should follow a structural reduction, not precede it.
- Any novelty claim needs a targeted literature review. Garcia's 2026 window calculus and counting obstruction should be cited as antecedents; the cycle-space argument is presented here as a self-contained derived lemma, without asserting priority.

## Reproduce

With the prior mixed-gadget continuation applied, run:

```bash
python tracks/2026-11-halving/scripts/cycle_space_obstruction.py
python -m pytest -q tracks/2026-11-halving/scripts/test_cycle_space_obstruction.py
```

`cycle_space_obstruction.py` operates on a binary cycle basis, not a cycle list. The proof-generating routine returns an explicit base cycle, its attainable lift interval, a power of two in the interval, and a simple expanded-graph cycle of that exact length.
