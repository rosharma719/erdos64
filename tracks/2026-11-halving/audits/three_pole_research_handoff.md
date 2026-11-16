> **Erratum added on commit (2026-11-16).** This audit was written by a
> separate model and is kept as written, with one correction. Its guardrail
> that Conjecture T settles only 3-connected cubic graphs is superseded: T
> implies the conjecture for **every** cubic graph, by deleting a leaf of a
> spanning tree (`../three_port_classification.md`). The order-13 to order-19
> census it asks for is recorded in `../three_pole_census_manifest.md`. The
> H15 port labels it noted are now derived from the graph6 itself
> (`../scripts/audit_clean_poles.py`).

# Erdős–Gyárfás: clean three-poles and additive windows

**Status:** audit and research handoff, 16 November 2026. The conjecture remains open. No assertion of a 21-vertex census or proof of Conjecture T is made here.

## Priority order

1. **Protect the conjecture from false positives.** Publish actual rooted graph6 representatives, distinguished terminals, cycle certificates, a complete list of capped cubic graphs traversed, and the provenance of the order-19 enumeration. Compare the claimed unique order-15 survivor with Exoo's H15 under *terminal-marked* isomorphism. A raw unrooted graph6 comparison is insufficient.
2. **Test T at order 21 by restrained computation.** Since an order-21 three-pole is obtained from an order-22 cubic graph by deleting a vertex, shard over canonical capped cubic graphs and rooted vertex-orbits, reject graphs with an unrooted dyadic cycle early, and record resumable, hash-audited shard manifests. C4/C8/C16 tests suffice for the order-21 pole; C32 is impossible. Do not use enumeration as proof unless catalog completeness and cycle-checking are audited.
3. **Prove the triangle-only tower stopping theorem by hand.** State the precise allowed elementary operations and whether `1` is an identity *vertex gadget* rather than a genuine three-degree-2 pole. Prove exhaustiveness as well as sufficiency.
4. **Prove the graph decomposition statement before calling T and WRP equivalent.** A clean three-pole might have small separators; establish a canonical quotient, that substitution of the listed components preserves terminal degrees, and that every candidate outside the list reduces to a prime rooted base not equal to K4 (or identify controlled exceptions). Prove that the cap of each pole is in the asserted class and justify each orientation.
5. **Use the existing averaged signed-width theorem as the dense-gadget case.** Focus remaining proof effort on sparse-gadget labellings and a cycle-window-chain lemma, including parity and the integer offsets. A modular counterexample defeats any claim based solely on an interval's cardinality.

## Formal corrections and guardrails

- For a **connected** cubic graph G with a root r, G-r has three degree-2 terminals and all other vertices cubic, **provided G-r is connected**. A 3-connected cubic graph satisfies this; arbitrary connected cubic graphs need not. Absence of dyadic cycles transfers to G-r.
- **Conjecture T** claims that every clean three-degree-2 connected pole is one of the stated one, two, one classes at orders 3, 7, 15. It would imply every 3-connected cubic counterexample has 4, 8, or 16 vertices. All such cubic graphs are already covered by published verification, so T would settle that class. The reduction to arbitrary cubic graphs requires separate work on vertex cuts / edge cuts.
- **WRP is a proposed structural reduction, not a proved equivalence.** In particular the classification of small poles and decomposition of all other poles into prime bases must be proved before using WRP to settle T. The root's three deleted incident edges must remain distinguishable through substitution.
- Signed window weights are additive as *real linear functionals of cycle incidence vectors*. They are **not linear maps on the binary cycle space** over F_2: symmetric difference cancels shared edges. Cycle-space averaging is legitimate when properly stated as averaging a real-valued score over its Eulerian elements and then extracting a component cycle.
- An interval `[m,M]` forces a power of two when `M >= 2m`; this is sufficient rather than necessary. For an even-only interval, check even endpoints and the relevant powers of two (>=4). A union of separately attained intervals requires overlap to claim coverage.
- The listed H7 and Exoo H15 examples do have **port-pair-specific complete integer intervals**, verified by the bundled exact path enumeration. The statement that *every* clean three-pole does is conditional on T.
- The existing averaged obstruction already gives the coarse threshold

  `3(n_identity+n_triangle) <= n_H7skew + 3 n_H7uniform + 17 n_H15`

  as a sufficient condition for a dyadic cycle on a bridgeless cubic base (independent of port orientation). Therefore Step 4 should seek a sharper local/conditioned criterion rather than restate the global count threshold. The strict reversed inequality is a necessary condition for a counterexample.

## Proven small result: no order-5 clean 3-pole

Let H have five vertices: three degree 2 and two degree 3. Write the degree-3 vertices as u,v.

If u,v are nonadjacent, each must be adjacent to all three degree-2 vertices. Thus H is K_{2,3}, which has a 4-cycle.

If u,v are adjacent, each has two neighbors among the remaining three vertices. If they have two common neighbors, the fifth vertex cannot have degree 2. Thus they have exactly one common neighbor and one different neighbor each. The two different neighbors must be adjacent to complete their degrees, giving a 4-cycle through u,v and those two vertices. Hence every candidate has a 4-cycle.

An independent brute-force check enumerates all 2^10 labeled graphs of order 5: exactly **70** graphs have degree multiset `(3,3,2,2,2)`, all containing C4.

## Independent finite audit (from previously bundled catalogs)

| Pole order | Connected cubic cap classes used | Clean terminal-marked classes |
|---:|---:|---:|
| 3 | 1 | 1 |
| 5 | 2 | 0 |
| 7 | 5 | 2 |
| 9 | 19 | 0 |
| 11 | 85 | 0 |

Catalog completeness is conditional on the accepted connected cubic census counts, as stated in the earlier repository research. Each pole is constructed by deleting *every* root from the cap catalog; poles are de-duplicated with the degree-2 terminals explicitly marked. This is an independent rerun of the earlier small-census computation, **not** an independent audit of the user's order-13/15/17/19 exhaustive claim.

The 7-vertex class representatives from the bundled catalog have path spectra `[3,6],[2,6],[2,6]` and `[2,6]` for all three port-pairs. A known Exoo 15-vertex representative has `[3,14],[3,14],[5,14]`. These spectra are verified directly from the graph's simple paths. A uniqueness claim for n=15 requires the user's survivor certificate, not supplied in this turn.

## Proof obligations for WRP

Define WRP precisely for a **rooted base** (B,r) and attachment-aware labels on B-r. Each label's ports must be matched to the three distinct neighbors of its base vertex. A cycle C avoiding r has lifted window

`[ |C| + Σ_{v∈C} a_{v,C},  |C| + Σ_{v∈C} b_{v,C} ]`.

To complete the proposed equivalence, prove:

1. The quotient/decomposition lemma for every clean pole outside the candidate list, handling 1-, 2-, and cyclic 3-edge separations and tracking the three distinguished terminals.
2. A prime quotient B that is not K4, or a separately controlled K4 tower case.
3. Completeness of the label library and its attachment orientations.
4. Absence of internal dyadic cycles and completeness of each terminal path interval.
5. Reconstruction of every rooted cycle witness as a genuine simple cycle in the pole, with no inadvertent use of the removed root.

Without (1)-(3), WRP might still be a useful **stronger standalone conjecture**, but its equivalence to T has not been established.

## Next high-value move

Prove the triangle-tower stopping lemma, then make the canonical prime-decomposition lemma the main target. In parallel, obtain a reproducible, shard-verified 21-vertex census to seek a first counterexample to T. A 21-vertex survivor would change the structural research direction immediately; an empty census is supporting evidence, not a substitute for the reduction proof.
