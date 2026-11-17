---
id: c-handoff-rooted-on-cycle-fails
title: "Not every vertex of a connected cubic graph lies on a dyadic cycle"
kind: claim
label: "DISPROVED"
topics: ["run-2026-11-handoff"]
doc_status: active
date: 2026-11-17
summary: "The auxiliary claim 'every vertex of every connected cubic graph lies on some dyadic cycle' is false: an 18-vertex connected cubic graph (a central triangle with three bridges to five-vertex caps) has a vertex whose only cycles are triangles."
evidence: ["kb/runs/2026-11-17-handoff/handoff/Erdos_Gyarfas_Full_Research_Dossier.md#7.4", "kb/runs/2026-11-17-handoff/handoff/Original_Research_Packets/EG_shortest_path_audit.py"]
depends_on: []
---

# Not every vertex of a connected cubic graph lies on a dyadic cycle

## Statement

The auxiliary claim 'every vertex of every connected cubic graph lies on some dyadic cycle' is false: an 18-vertex connected cubic graph (a central triangle with three bridges to five-vertex caps) has a vertex whose only cycles are triangles.

## Evidence

- `kb/runs/2026-11-17-handoff/handoff/Erdos_Gyarfas_Full_Research_Dossier.md#7.4`
- `kb/runs/2026-11-17-handoff/handoff/Original_Research_Packets/EG_shortest_path_audit.py`

## Caveats

The witness has bridges and contains C4 elsewhere, so it says nothing about EG. It concerns lying *on* a dyadic cycle. The Pass XIV results (c-rooted-robustness-fails-n16, c-rooted-robustness-hard-instances) concern being *avoided by* one; the two are unrelated properties.

## History

- 2026-11-17: imported from the 17 Nov 2026 handoff.
