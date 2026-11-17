---
id: c-odd-girth-edge-cover-forcing
title: "Cubic graphs of odd girth g with every edge on a g-cycle contain C_{2g−2}"
kind: claim
label: "PROVED"
topics: ["run-2026-11-handoff", "near-dyadic"]
doc_status: active
date: 2026-11-17
summary: "For every odd g ≥ 5, a cubic graph of girth g in which every edge lies on a g-cycle contains a cycle of length 2g − 2. In particular, for g = 2^k + 1 such a graph contains C_{2^{k+1}}."
evidence: ["kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#3"]
depends_on: ["c-scale-escalation"]
---

# Cubic graphs of odd girth g with every edge on a g-cycle contain C_{2g−2}

## Statement

For every odd g ≥ 5, a cubic graph of girth g in which every edge lies on a g-cycle contains a cycle of length 2g − 2. In particular, for g = 2^k + 1 such a graph contains C_{2^{k+1}}.

## Evidence

- `kb/runs/2026-11-17-handoff/run8/EG_NearDyadic_Run8/RESEARCH_NOTE.md#3`

## Caveats

Proof from c-scale-escalation, read on import; not refereed. Covers only a subclass of cubic graphs (girth exactly g, all edges covered at that scale). Related literature on edge-girth-regular cubic graphs (arXiv:1802.01881; Edge-girth-regular graphs, 2018) not yet checked for priority. Compare the g = 3/5 statement c-handoff-short-cycle-edge-cover.

## History

- 2026-11-17: imported from Run 8 (near-dyadic research packet); proof read on import.
