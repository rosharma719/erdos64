---
id: c-handoff-c4c8-edge-bound
title: "Edge bound |E| ≤ 2n − 5 for 3-critical C4/C8-free graphs"
kind: claim
label: "COMPUTATIONALLY VERIFIED"
topics: ["run-2026-11-handoff"]
doc_status: active
date: 2026-11-17
summary: "Every 2-degenerate C4/C8-free graph on N ≥ 9 vertices has at most 2N − 6 edges (finite 8-vertex saturation lemma, by exhaustive enumeration of 2^21 labelled 7-vertex graphs, plus induction). Hence a graph with n ≥ 10, δ ≥ 3, no C4, no C8 and no proper subgraph of minimum degree 3 has at most 2n −…"
evidence: ["kb/runs/2026-11-17-handoff/handoff/Erdos_Gyarfas_Full_Research_Dossier.md#6", "kb/runs/2026-11-17-handoff/packets/EG_Run7_Core_Bound_and_Audit/verify_complete_7.cpp", "kb/runs/2026-11-17-handoff/packets/EG_Run7_Core_Bound_and_Audit/RESEARCH_NOTE_RUN7.md"]
depends_on: []
---

# Edge bound |E| ≤ 2n − 5 for 3-critical C4/C8-free graphs

## Statement

Every 2-degenerate C4/C8-free graph on N ≥ 9 vertices has at most 2N − 6 edges (finite 8-vertex saturation lemma, by exhaustive enumeration of 2^21 labelled 7-vertex graphs, plus induction). Hence a graph with n ≥ 10, δ ≥ 3, no C4, no C8 and no proper subgraph of minimum degree 3 has at most 2n − 5 edges.

## Evidence

- `kb/runs/2026-11-17-handoff/handoff/Erdos_Gyarfas_Full_Research_Dossier.md#6`
- `kb/runs/2026-11-17-handoff/packets/EG_Run7_Core_Bound_and_Audit/verify_complete_7.cpp`
- `kb/runs/2026-11-17-handoff/packets/EG_Run7_Core_Bound_and_Audit/RESEARCH_NOTE_RUN7.md`

## Caveats

As reported by the handoff, which recompiled and reran the enumeration itself; not re-run on import. The handoff notes there is no second, independently implemented complete enumeration. For minimal EG counterexamples the repository already records m ≤ 2n − 6 (q(G) ≥ 4, kb/core/proof.md P9–P12) under a different hypothesis; see the run README cross-reference 1.

## History

- 2026-11-17: imported from the 17 Nov 2026 handoff.
