---
id: c-average-degree-near-dyadic-obstruction
title: "Average degree > 3 plus near-dyadic edge saturation does not force a dyadic cycle"
kind: claim
label: "PROVED"
topics: ["run-2026-11-handoff", "near-dyadic"]
doc_status: active
date: 2026-11-17
summary: "Gluing t ≥ 4 copies of the 8-vertex, 11-edge graph GxaGiC (no C4/C8, every edge on a C3 or C5) at one vertex gives a graph with average degree 22t/(7t+1) > 3, every edge on a C3 or C5, and no dyadic cycle."
evidence: ["kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#6", "kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/near_dyad_8vertex_block.g6", "kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/near_dyad_glued29.g6"]
depends_on: []
---

# Average degree > 3 plus near-dyadic edge saturation does not force a dyadic cycle

## Statement

Gluing t ≥ 4 copies of the 8-vertex, 11-edge graph GxaGiC (no C4/C8, every edge on a C3 or C5) at one vertex gives a graph with average degree 22t/(7t+1) > 3, every edge on a C3 or C5, and no dyadic cycle.

## Evidence

- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#6`
- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/near_dyad_8vertex_block.g6`
- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/near_dyad_glued29.g6`

## Caveats

Elementary (all cycles lie in a block) plus packet certificate for t = 4 (29 vertices, 44 edges). Has degree-2 vertices and cut vertices; not an EG counterexample.

## History

- 2026-11-17: imported from Run 8 (near-dyadic research packet); proof read on import.
