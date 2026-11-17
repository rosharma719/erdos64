# Erdős–Gyárfás: exact 16-cycle transversal audit

Date: 2026-11-17. Scope: the four previously supplied 24-vertex connected cubic C4/C8-free control graphs, in `controls.g6` (lines 3–6).

For a graph G, let H16(G) be the hypergraph of vertex sets of simple 16-cycles, and let tau16(G) be its minimum vertex transversal size. This is a bounded diagnostic, not a theorem about all cubic graphs or a new proof of Erdős–Gyárfás.

## Exact results

| Control graph (1-based within four) | C16 cycles | Min C16 avoiding a vertex | Max C16 avoiding a vertex | tau16 | Number of minimum hitting sets |
|---|---:|---:|---:|---:|---:|
| 1 | 315 | 83 | 131 | 3 | 61 |
| 2 | 330 | 74 | 135 | 2 | 3 |
| 3 | 207 | 49 | 84 | 2 | 2 |
| 4 | 228 | 43 | 93 | 2 | 9 |

The script enumerates each undirected 16-cycle exactly once, by requiring its smallest-labeled vertex to be the starting point and canonicalizing the two orientations. It enumerates all candidate vertex sets of sizes 1, 2, 3, and (if necessary) 4 to obtain exact transversal numbers.

An independently written meet-in-the-middle 16-cycle existence oracle from the preceding audit was also run on every vertex of every control graph and found no root-critical vertices (96 tests). This independently corroborates the positivity of the root-avoiding counts, but not the exact cycle counts or transversal numbers.

## Interpretation

Every vertex is avoidable by at least 43 distinct 16-cycles in each of the four controls, yet three of the four graphs have a pair of vertices meeting every 16-cycle. Therefore rooted robustness alone does not imply a strong two-vertex-avoidance property, even among these near-misses.

These four controls contain triangles and hence fail cyclic four-edge-connectivity; no conclusion about the prime cubic class follows.

## Run

```
python cyclecount.py
```

Requires Python 3 and NetworkX. The first two rows in `controls.g6` are Petersen and K4 controls and are intentionally skipped.

## External provenance

Zackary Loevseth's public repository reports an independently audited 251-class census for order 28 but the public audit summary is not the graph6 dataset. Until the full graph6 records are obtained and their completeness checked, we cannot assert any order-28 rooted classification.

Sources:
- https://github.com/ZackaryLoevseth/Erd-s-Problem-64/blob/main/reports/data-and-significance-review.md
- https://github.com/chriss1245/erdos-gyarfas-cubic-frontier
