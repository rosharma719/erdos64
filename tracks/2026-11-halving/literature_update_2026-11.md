# Literature update for erdos64 (2026-11-16)

The repo's `literature.md` stops in August 2026 and records arXiv as
unreachable. arXiv was reachable in this session. Papers below were read from
the arXiv HTML unless marked "abstract only".

## New since the repo's last update

| Paper | What it proves | Effect on the repo |
|---|---|---|
| Ducoffe, Dumitru — *Towards a more structured search for Erdős–Gyárfás counter-examples*, arXiv:2609.28594 (23 Sep 2026) | Minimal counterexample: every edge on a `2^k+1` cycle (Lemma 2.1); 2-edge-connected (Cor. 2.2); cut-vertex theorem with unique cut vertex, two components, two neighbours each, equal order and size (Thm 2.3); `m ≤ 2n−2` (Thm 3.3); ≥ 2n/3 cubic vertices (Prop. 3.4); doubling reduction on the high-degree vertices (Lemma 3.5); no `2^j`-subdivision of a min-degree-3 multigraph (Thm 3.8). Equivalent forms: one low-degree vertex allowed (Conj. 4.1, Thm 4.2); rainbow-cycle form for the bipartite case (Conj. 4.3, Thm 4.4). Computation: no counterexample of order ≤ 40, bipartite ≤ 66, cubic ≤ 48 (Thm 5.1), by SAT search, about 30 core-days. | S4, S5, G1, the near-power edge lemma and the leaf graph (defect.md I.2) are now published by others. The order-30 census, the n = 21/23 layers, and the 3-connectivity range are superseded by the order bound. |
| Garcia — *Small graphs without power-of-two cycles*, arXiv:2609.04686 (4 Sep 2026) | Every min-degree-3 graph on ≤ 23 vertices has a C4 or C8, DRAT-certified; correction to Exoo's 450-vertex construction; `f(k)` bounds. | Supersedes the repo's 4-or-8 result through 19 and its n ≤ 23 programme. |
| *A 60-Vertex Lower Bound for Cubic Bipartite Counterexamples*, arXiv:2608.02675 (2 Aug 2026) | Every cubic bipartite graph on ≤ 58 vertices has a C4, C8 or C16. Cites a public 2026 SAT computation excluding all min-degree-3 graphs through order 31. | Independent of the repo's tracks; method (incidence configurations) is new to it. |
| Burkhart — *Odd-ordered Cayley graphs satisfy Erdős–Gyárfás*, arXiv:2611.05060 (3 Nov 2026), abstract only | Conjecture holds for Cayley graphs of odd order, hence for nilpotent groups. | Relevant to the voltage-lift track. |

## Missing from the repo entirely

- Liu, Montgomery — *A solution to Erdős and Hajnal's odd cycle problem*,
  J. Amer. Math. Soc. 36 (2023), arXiv:2010.15802. Sufficiently large constant
  average degree forces a power-of-two cycle. The only known method that hits
  a multiplicatively sparse target. A separate brief covers it.

## Discrepancy to resolve

Ducoffe–Dumitru Lemma 2.1 states the `2^k+1` cycle for **every** edge. The
repo's `every_edge_witness_audit.md` says the argument goes through only for
**non-triangle** edges. One of the two is wrong or they use different
hypotheses. Not resolved here.

## What in the repo may still be unpublished

- `q(G) ≥ 4`, i.e. `m ≤ 2n − 6` (published bound: `2n − 2`). Independently
  confirmed today for order ≥ 37; see `q4_independent_check.md`.
- Pole-forcing for Type-T vertices, the atom-lifting lemma, the one-pole
  results O3 and O5, and the exact Z3/Z5 lift eliminations. None checked
  against the new papers beyond their abstracts and theorem lists.

## Priority note

The repo's proofs of S4, S5 and G1 are dated July 2026, before the September
papers, but were never posted. They cannot now be claimed as new.

## Sources

- https://arxiv.org/abs/2609.28594
- https://arxiv.org/html/2609.04686
- https://arxiv.org/html/2608.02675
- https://arxiv.org/abs/2611.05060
- https://arxiv.org/abs/2010.15802
