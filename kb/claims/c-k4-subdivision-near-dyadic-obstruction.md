---
id: c-k4-subdivision-near-dyadic-obstruction
title: "Degree 3 is essential: subdivided K4 has all edges on two near-dyadic cycles and no dyadic cycle"
kind: claim
label: "PROVED"
topics: ["run-2026-11-handoff", "near-dyadic"]
doc_status: active
date: 2026-11-17
summary: "For odd k ≥ 3 and m = (2^k + 1)/3, the uniform m-subdivision of K4 is 2-connected, has girth 2^k + 1, all cycles of length 3m or 4m (none dyadic), and every edge on exactly two C_{2^k+1}. For k = 3 (m = 3): 16 vertices, four C9 and three C12."
evidence: ["kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#5", "kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/K4_three_subdivision.g6"]
depends_on: []
---

# Degree 3 is essential: subdivided K4 has all edges on two near-dyadic cycles and no dyadic cycle

## Statement

For odd k ≥ 3 and m = (2^k + 1)/3, the uniform m-subdivision of K4 is 2-connected, has girth 2^k + 1, all cycles of length 3m or 4m (none dyadic), and every edge on exactly two C_{2^k+1}. For k = 3 (m = 3): 16 vertices, four C9 and three C12.

## Evidence

- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#5`
- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/K4_three_subdivision.g6`

## Caveats

Elementary (K4 has four triangles and three 4-cycles); the k = 3 case was also checked by full cycle enumeration in the packet. It has degree-2 vertices, so it is not an EG counterexample; it shows near-dyadic coverage without minimum degree 3 forces nothing.

## History

- 2026-11-17: imported from Run 8 (near-dyadic research packet); proof read on import.
