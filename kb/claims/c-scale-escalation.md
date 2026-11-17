---
id: c-scale-escalation
title: "Scale escalation: overlaps of near-dyadic girth cycles force an uncovered edge"
kind: claim
label: "PROVED"
topics: ["run-2026-11-handoff", "near-dyadic"]
doc_status: active
date: 2026-11-17
summary: "Let g = 2^k + 1 (k ≥ 2) and let G have girth g and no C_{2g−2}. If two distinct g-cycles share a path P of t ≥ 2 edges whose internal vertices all have degree 3, then some internal vertex has its third edge on no g-cycle. In a smallest counterexample of girth g that edge must lie on some C_{2^j+1…"
evidence: ["kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#2", "kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/scale_stdout.txt"]
depends_on: ["c-girth-cycle-intersection"]
---

# Scale escalation: overlaps of near-dyadic girth cycles force an uncovered edge

## Statement

Let g = 2^k + 1 (k ≥ 2) and let G have girth g and no C_{2g−2}. If two distinct g-cycles share a path P of t ≥ 2 edges whose internal vertices all have degree 3, then some internal vertex has its third edge on no g-cycle. In a smallest counterexample of girth g that edge must lie on some C_{2^j+1} with j > k (by Ducoffe–Dumitru's edge-saturation lemma).

## Evidence

- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#2`
- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/scale_stdout.txt`

## Caveats

Proof (direction-choice argument) read and checked on import; not refereed. The exhaustive local search (t = 2: 0 third witnesses; t = 3: 4; t = 4: 3) confirms that the theorem asserts *some*, not *every*, internal edge is uncovered. Requires girth exactly near-dyadic and cubic internal vertices; a mixed-degree variant allows a degree-≥4 internal vertex instead.

## History

- 2026-11-17: imported from Run 8 (near-dyadic research packet); proof read on import.
