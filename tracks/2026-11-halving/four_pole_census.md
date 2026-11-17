# Clean 4-poles through 20 vertices (16 November 2026)

**Author:** Claude. Census CERTIFIED for checkers, single generator (method
and manifests: `three_pole_census_manifest.md`, `census/`). Classification
COMPUTED (`scripts/classify_four_poles.py`, one implementation).

A clean 4-pole is a connected graph with exactly four vertices of degree 2,
all others of degree 3, and no cycle of length 4, 8, 16, … Its order is even.
Command: `geng -c -f -d2 -D3 N E:E` with `E = (3N − 4)/2`.

## Counts

| N | graphs (no C4) | clean | joined by a bridge | bridgeless |
|---:|---:|---:|---:|---:|
| 6 | 2 | 2 | 1 (T–T) | 1 |
| 8 | 6 | 2 | 0 | 2 |
| 10 | 37 | 4 | 3 (S–T ×2, T–U) | 1 |
| 12 | 300 | 2 | 0 | 2 |
| 14 | 3,138 | 15 | 6 (S–S ×3, S–U ×2, U–U) | 9 |
| 16 | 39,904 | 18 | 0 | 18 |
| 18 | 583,717 | 5 | 2 (H–T ×2) | 3 |
| 20 | 9,551,674 | **0** | 0 | 0 |

Order 6 agrees with ChatGPT's independent classification (two classes: two
triangles joined by a bridge, and a six-cycle with a chord at distance two).

## What the classification shows

1. **Every clean 4-pole with a bridge is two clean 3-poles from T's list joined
   by that bridge**, and every such pairing occurs, with the multiplicities the
   port symmetries predict. For example, S has two kinds of port and H has two,
   so S–S occurs 3 ways and H–T 2 ways. This matches ChatGPT's bridge-gluing
   Proposition 1 exactly.
2. **The bridgeless ones are all 2-connected but not 3-connected** (vertex
   connectivity exactly 2). The smallest is the 6-cycle with a distance-two
   chord, a theta graph with paths of lengths 1, 2 and 4. None of them becomes
   a T-list pole when one port is suppressed, except one at order 8 that
   suppresses to uniform H7.
3. **The bridgeless family stops**: 36 graphs at orders 6–18 and none at 20.

## Consequences for the conjectures

- Consistent with `N(4) = 30`, the linear defect bound at `δ = 4`
  (`linear_defect_bound.md`). The bridge-joined pairs predicted at 22 (S–H,
  U–H) and 30 (H–H) are beyond this census.
- The tree-of-towers picture is right for the bridged part, but bridgeless
  sporadic pieces exist. A classification of clean k-poles must include them.

## Not run

- Order 22: about 150 million graphs, roughly 85 core-minutes. Restricting to
  bridgeless graphs (`geng -C`) barely helps: 9.30 million versus 9.55 million
  at order 20.
- Orders 24–30, needed to confirm `N(4) = 30` exactly.
