# Pass XII: universal resilience ceiling and additional rooted census

Date: November 16, 2026. Status: internally proved inequality; finite computations with logged outputs; no proof of the full Erdős–Gyárfás conjecture or rooted prime conjecture.

## Bound
For a graph with n vertices, m edges, and shortest power-of-two cycle length q, let rho(G) be the fractional resilience defined in `bridge_resilience_potential.md`. Then

rho(G) <= m(n-q)/(2nq).

For cubic graphs this becomes rho(G) <= 3(n-q)/(4q). If rho(G)>1, then n>7q/3 necessarily.

Proof: For any nonnegative nonzero cycle weights of total W, every dyadic cycle has at least q edges and vertices, so n alpha >= qW and m beta >= qW by double counting vertex and edge incidences. Consequently (W-alpha)/(2beta) <= m(n-q)/(2nq). Take the supremum.

This can make the rho>1 bridge-survival certificate inapplicable even in graphs with many dyadic cycles; it does not imply a bridge destroys the rooted property.

## LP verification
`python resilience_lp_verify.py` re-run successfully with these results:

| Graph | n | q | dyadic cycles | computed rho | bound |
|:---|---:|---:|---:|---:|---:|
| K4 | 4 | 4 | 3 | 0 | 0 |
| cube | 8 | 4 | 12 | .75 | .75 |
| Petersen | 10 | 8 | 15 | .1875 | .1875 |
| K3,3 | 6 | 4 | 9 | .375 | .375 |
| Heawood | 14 | 8 | 21 | .5625 | .5625 |
| dodecahedron | 20 | 8 | 120 | 1.125 | 1.125 |
| 24-vertex near-miss #1 | 24 | 16 | 315 | .375 | .375 |
| 24-vertex near-miss #2 | 24 | 16 | 330 | .3333333 | .375 |
| 24-vertex near-miss #3 | 24 | 16 | 207 | .3333333 | .375 |
| 24-vertex near-miss #4 | 24 | 16 | 228 | .3333333 | .375 |

The exact graph6 strings for the last four samples are embedded in `check24.py` and `edge_transversals.py`. This is a numerical LP computation, not a formal proof of each optimum.

## Bounded class generation
From the continuation's `prime_census.log`, 2, 5, 18, 84 and 607 distinct generated cubic graph classes were found on 8, 10, 12, 14, and 16 vertices, respectively. In all generated graphs, every vertex was avoided by a 4-, 8- or 16-cycle as applicable. The class construction relies on repeated edge bridging and isomorphism deduplication.

## Order-18 bridge-child check
The completed `bridge18.log` records all 138,396 pairs of disjoint edges from the 607 order-16 graphs; it checks 6,508 exceptional root/bridge instances where untouched parent cycles are insufficient. All were repaired (2,821 via 4-cycles and 3,687 via 8-cycles), zero failures found.

`repair_classification.log` classifies 6,456 exceptional instances as admitting both path and shifted-cycle witnesses, 24 shifted-only, and 28 path-only. `independent_validation.py` was re-run and agreed with a second NetworkX directed simple-cycle oracle on 80 randomly selected bridge children.

This is not claimed as an exhaustive n=18 isomorphism-class census. Complete coverage and source-code correctness have not received independent mathematical certification. Published external cubic non-rooted verification already reaches 48 vertices, while rooted avoidance is a stronger target.

## Next problem
A low-resilience exchange theorem under eligible prime bridging remains open. A universal rooted prime statement may also be false; prioritize larger-cubic and high-girth falsification tests.
