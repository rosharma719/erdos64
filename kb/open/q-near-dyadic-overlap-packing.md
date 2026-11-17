---
id: q-near-dyadic-overlap-packing
title: "Global overlap packing: force enough near-dyadic overlaps in a minimal counterexample"
kind: open-problem
label: "OPEN"
topics: ["run-2026-11-handoff", "near-dyadic"]
doc_status: active
date: 2026-11-17
summary: "Show that a smallest counterexample must contain enough internally disjoint overlap paths of near-dyadic girth cycles (or an analogue without the girth hypothesis) that the forced scale escalations (c-scale-escalation, c-overlap-packing-inequality) cannot all be accommodated, e.g. via a recurrenc…"
evidence: ["kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#8"]
depends_on: ["c-scale-escalation", "c-overlap-packing-inequality"]
---

# Global overlap packing: force enough near-dyadic overlaps in a minimal counterexample

## Question

Show that a smallest counterexample must contain enough internally disjoint overlap paths of near-dyadic girth cycles (or an analogue without the girth hypothesis) that the forced scale escalations (c-scale-escalation, c-overlap-packing-inequality) cannot all be accommodated, e.g. via a recurrence on the number of edges whose shortest near-dyadic witness has scale k.

## Evidence

- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#8`

## Caveats

The current theorems need odd girth exactly 2^k + 1 and cubic overlap interiors; removing the girth assumption is the central obstacle. Obstructions to test against: c-k4-subdivision-near-dyadic-obstruction, c-average-degree-near-dyadic-obstruction.

## History

- 2026-11-17: imported from Run 8 (near-dyadic research packet); proof read on import.
