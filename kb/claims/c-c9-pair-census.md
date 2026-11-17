---
id: c-c9-pair-census
title: "Local census of two 9-cycles sharing an edge"
kind: claim
label: "COMPUTATIONALLY VERIFIED"
topics: ["run-2026-11-handoff", "near-dyadic"]
doc_status: active
date: 2026-11-17
summary: "Of 130,922 labelled placements of a second C9 through a fixed edge of a C9, 151 give a subcubic union with no C4, C8, C16; 9 of those also have girth ≥ 9, with shared paths of length 2 (2 cases), 3 (3), 4 (4). Of 67 two-ear (K4-subdivision) patterns, 27 have girth ≥ 9 and no C16."
evidence: ["kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#4", "kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/run8_stdout.txt", "kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/verified_results.json"]
depends_on: []
---

# Local census of two 9-cycles sharing an edge

## Statement

Of 130,922 labelled placements of a second C9 through a fixed edge of a C9, 151 give a subcubic union with no C4, C8, C16; 9 of those also have girth ≥ 9, with shared paths of length 2 (2 cases), 3 (3), 4 (4). Of 67 two-ear (K4-subdivision) patterns, 27 have girth ≥ 9 and no C16.

## Evidence

- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#4`
- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/run8_stdout.txt`
- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/verified_results.json`

## Caveats

As reported in the packet (two independent cycle oracles plus NetworkX); not re-run on import. Counts are labelled local embeddings, not isomorphism classes.

## History

- 2026-11-17: imported from Run 8 (near-dyadic research packet); proof read on import.
