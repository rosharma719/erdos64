---
id: three-cut-prime-transfer
title: "Structural pass IV: cyclic three-edge cuts as exact cycle-spectrum interfaces"
kind: track-note
topics: ["tracks", "2026-11-halving"]
doc_status: active
date: 2026-11-16
summary: "Research note · November 16, 2026. Follow-up to cycle_space_obstruction.md."
---

# Structural pass IV: cyclic three-edge cuts as exact cycle-spectrum interfaces

**Research note · November 16, 2026.** Follow-up to `cycle_space_obstruction.md`.

## 0. What is established already, and what this pass adds

A decomposition of 2-connected cubic graphs into cyclically 4-edge-connected factors along 2- and 3-edge cuts is established graph theory. In particular, the uniqueness (up to isomorphism and ordering) of the decomposition factors is proved in *Perfect-matching covers of cubic graphs with colouring defect 3* (Theorem 5.2 of the accessible preprint). Related treatments use the 3-sum of cubic graphs; see also *Decycling cubic graphs* (2024). We are **not** claiming a new prime decomposition theorem.

This pass applies that structural decomposition to the Erdős–Gyárfás problem. Its exact interface identity, a dyadic-gap condition, and an orientation-independent signed-width obstruction are proved below. We have **not established novelty** of these interface lemmas; similar path-spectrum considerations appear in Garcia's 2026 gadget window calculus (arXiv:2609.04686). Unlike that gadget catalog, the interface lemmas apply to **arbitrary** three-terminal sides of an independent cyclic 3-edge cut.

The main question is now specific: **must some cyclic 3-cut of a nonprime cubic graph have two complementary sides whose terminal path spectra force a dyadic crossing cycle?** If so, induction could reduce the problem to cyclically 4-edge-connected cores, but **a prime-case theorem alone is insufficient**. A putative counterexample without such a cut would need to violate the interface criterion at every 3-cut.

## 1. Exact transfer across a 3-edge cut

Let `G` be a finite simple cubic graph, with three pairwise independent edges

```
              e_i = a_i -- b_i     (i=0,1,2)
```

whose deletion separates `G` into connected components `A` and `B`, each containing at least one cycle, with `a_i in A`, `b_i in B`. Such an independent cyclic 3-cut exists automatically at every cyclic 3-edge cut of a **3-edge-connected cubic graph**: if two cut edges met at a vertex, moving that vertex to the other side would expose a cut of size two, contradicting 3-edge connectivity.

Define `I(A)` as the set of lengths of *simple cycles entirely contained in A*, and `P_A(i,j)` as the set of lengths of *simple paths in A* from `a_i` to `a_j`, measured in internal edges. Similarly for `B`.

**Exact cut-transfer theorem.** The set `L(G)` of simple cycle lengths in `G` equals

```
    I(A) union I(B)
        union (union_{0 <= i < j <= 2}
               {2 + x + y : x in P_A(i,j), y in P_B(i,j)}).
```

*Proof.* Every cycle uses an even number of edges in any cut. With just three cut edges, it uses zero or two. In the first case the entire cycle is internal to a side. In the second case the cycle consists of a simple terminal-to-terminal path on each side, joined by exactly two cut edges. Conversely, any such pair of paths has disjoint interiors (different sides) and their union with the two cut edges is a simple cycle. QED.

No interval assumption is needed. This is an exact *interface* reduction, rather than a finite base-graph census. The full terminal spectra may be expensive to compute; a mathematically certified *subset* of a spectrum is always sufficient for a **positive** obstruction, though not for proving avoidance.

## 2. Gap condition, without averaging

When both pair spectra are complete integer intervals, say `P_A(i,j)=[a_A,b_A]` and `P_B(i,j)=[a_B,b_B]`, the crossing lengths for that pair form the complete integer interval

```
    [m,M] = [2+a_A+a_B, 2+b_A+b_B].
```

For an all-power-of-two-avoiding `G`, every pair's crossing interval must lie *strictly between consecutive powers of two*: for some integer `k` it is entirely in `(2^k, 2^(k+1))`. Equivalently, no `2^t` lies in `[m,M]`.

In particular, `M>=2m` guarantees a power-of-two cycle. This simple sufficient bound often misses dyadic cycles in narrower intervals, e.g. the two triangle poles obtained from the 3-sum of two `K4` graphs have crossing interval `[4,6]`, which contains 4 although `M<2m`.

## 3. A three-terminal deficiency invariant valid with gaps

Full path sets may be highly non-interval in prime cores. We should **not** assume they are intervals without proof.

For a nonempty finite integer set `S`, define its *certified interval score*

```
    omega(S) = max {b - 2a - 1 : [a,b] intersection Z is a subset of S}.
```

The maximum can be computed just from maximal consecutive runs in `S`: for each run `[a,b]`, its score is `b-2a-1`; a shorter subinterval in the same run cannot improve the score. Thus the invariant only uses a block of lengths that really occurs. It is defined even for isolated available lengths.

For a three-terminal side `A`, put

```
    Phi(A) = sum_{0<=i<j<=2} omega(P_A(i,j)).
```

**Cut-deficiency theorem (sufficient orientation-free obstruction).** If

```
                          Phi(A) + Phi(B) >= 0,
```

then `G` contains a simple power-of-two cycle. The inequality is independent of how the three ports are matched, because a port permutation merely permutes the three unordered terminal pairs.

*Proof.* Choose a maximizing contained interval `[a_A,b_A]` for each `P_A(i,j)` and similarly `[a_B,b_B]`. For a fixed pair, the corresponding cross interval `[m,M]` is fully realizable. The identity

```
   M - 2m = (b_A-2a_A-1) + (b_B-2a_B-1)
```

shows that if this pair's two scores sum nonnegatively, then a power of two is realizable. Summing the three pair scores and applying the hypothesis ensures at least one of the three pairs has nonnegative sum. QED.

**Necessary condition for a hypothetical counterexample:** Every independent cyclic 3-edge cut in a cubic counterexample must satisfy `Phi(A)+Phi(B)<0`. This is a universal *restriction*, not a proof that a counterexample cannot have such a cut. The condition does not require every simple path length to lie in a single interval.

For *complete* interval spectra the score specializes to `b-2a-1`, matching the earlier cycle-width score. For gapped spectra, using a maximally certified subinterval prevents the false inference that missing path lengths are realizable.

## 4. Small exact examples that explain the distinction

### 4.1 Two capped triangles (the triangular prism)

Deleting a vertex from `K4` leaves a triangle with three ports; every pair has path spectrum `{1,2}`. Gluing two such poles by any matching yields a triangular prism. The crossing interval is `[4,6]`, so an explicit 4-cycle exists. However each pair's width score is `2-2(1)-1 = -1`, and `Phi(A)+Phi(B)=-6` is negative. The sufficient width test is inconclusive; the **exact** gap test detects 4. This matters because we should not treat a failed width certificate as a candidate counterexample.

### 4.2 Gluing two asymmetric seven-vertex H7 poles

The skew `H7` pole's three terminal-pair path sets have interval scores `(-1,+1,+1)` in some order, so `Phi(H7)=+1`. Two skew `H7` poles have sum `+2` under **every** port permutation; their 3-sum necessarily contains a dyadic cycle. All six matchings were independently checked at the graph level, and explicit simple-cycle witnesses were constructed.

This orientation-independent conclusion is about an **infinite pattern of permissible attachments**, not a claim that the seven-vertex gadget or its use is new. It illustrates how a local invariant can rule out a family before doing any graph cycle enumeration.

### 4.3 Genuine gaps

For illustrative *abstract signatures* with path sets `{2,3,4,5,6,10}` and `{2,3,4,5,6,20}` at each pair, the full sets have gaps. Nevertheless each contains `[2,6]` with width score `+1`, so the cut-deficiency criterion forces an 8-cycle across any matching. These are synthetic signatures used to test the arithmetic, **not** a claim that a cubic three-pole with those exact three spectra exists.

## 5. What the prime-core reduction actually requires

For a 3-edge-connected cubic graph, repeated splitting at nontrivial cyclic 3-edge cuts and *capping* each component with a new degree-three vertex yields smaller cubic factors. Iterating terminates; the established decomposition theorem gives cyclically 4-edge-connected factors. The whole original graph can be reconstructed by inverse 3-sums.

**Crucial logical caveat.** If a capped factor contains a dyadic cycle *through the artificial cap vertex*, that cycle need not survive when the cap is replaced by the opposing pole. Therefore a proof for all prime cubic factors, taken on its own, does **not** solve the problem for all cubic graphs. An induction must use a **rooted theorem controlling terminal path spectra** (or another invariant preserved by 3-sums).

This suggests a concrete high-level program:

1. Establish a quantitative lower bound on `Phi(P)` or on dyadic-gap coverage for a **cyclically 4-edge-connected capped prime** with a deleted vertex. The lower bound should follow from connectivity/structural arguments (e.g., path switching, cycle space, or ear structure), rather than a small catalog.
2. Prove a compositional rule for lower bounds on *certified* path intervals when a prime factor is enlarged by 3-sums. For negative or non-interval cases, retain exact attainable length sets until a safe contiguous subinterval can be proved.
3. Combine the bounds with `Phi(A)+Phi(B)<0` for every hypothetical dyadic-free cut. Only after step 1 yields a quantitative conjecture should we use SAT/finite search to probe exceptions or boundary cases.

This work is **restricted to cubic graphs and independent 3-cuts**. A separate argument is required to handle bridges, 2-edge cuts, general 2-connected graphs with different interfaces, and the general minimum-degree-at-least-three problem.

## 6. Reproducibility

Implementation: `scripts/three_cut_transfer.py`. Tests: `scripts/test_three_cut_transfer.py`.

- `split_independent_cyclic_three_cut(G, cut)` validates a *specified* cut and returns the two poles. It does not enumerate arbitrary base graphs.
- `pole_signature` is a deliberately exhaustive small-graph **reference verifier** that computes all internal simple cycles and port-to-port simple paths. Do not call it a polynomial-time algorithm for large prime cores.
- `cycle_lengths_from_signatures` gives the exact spectrum predicted by the interface theorem; differential tests independently compare it to simple-cycle enumeration in the joined graph.
- `cut_subinterval_mean_obstruction` and `cut_subinterval_width_obstruction` use *contained* intervals and remain sound with spectrum gaps.
- `dyadic_cut_cycle_witness` constructs and verifies an actual simple power-of-two cycle in the joined graph.
- The tests include two `K4` factors, Petersen + `K4` under all six matchings, two Petersen factors, and skew `H7` + skew `H7` under all six matchings, plus input rejection and synthetic gapped signatures.

```bash
python -m pytest -q tracks/2026-11-halving/scripts/test_three_cut_transfer.py
```

### References to verify / cite

- *Perfect-matching covers of cubic graphs with colouring defect 3*, decomposition via 2-/3-sums, Theorem 5.2 (2023 preprint): https://www.researchgate.net/publication/372749836_Perfect-matching_covers_of_cubic_graphs_with_colouring_defect_3
- *Decycling cubic graphs*, 2024, on canonical 3-connected cubic decompositions: https://www.sciencedirect.com/science/article/pii/S0012365X24001705
- Daniel Garcia, *Small graphs without power-of-two cycles*, arXiv:2609.04686 (2026), exact window calculus for vertex-replacement gadgets: https://arxiv.org/abs/2609.04686
