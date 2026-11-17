---
id: c-coin-gcd-parity
title: "Coin lemma, gcd reduction and odd-cycle parity gadget"
kind: claim
label: "PROVED"
topics: ["run-2026-11"]
doc_status: active
date: 2026-11-17
summary: "Values v1..vt ≤ h with gcd g, each with multiplicity M ≥ (t+1)h² + Ag, have subset sums containing every multiple of g in [t h², M v1]. Repeated pigeonhole on gadgets with steps ≢ 0 mod m drives the gcd to 1 or 2 in ≤ log2 h + 1 rounds. In a 2-connected non-bipartite graph the shortest odd cycle …"
evidence: ["kb/runs/2026-11-16-dossier/passes/20_closing_status.md#2", "kb/runs/2026-11-16-dossier/passes/20_closing_status.md#3"]
depends_on: []
---

# Coin lemma, gcd reduction and odd-cycle parity gadget

## Statement

Values v1..vt ≤ h with gcd g, each with multiplicity M ≥ (t+1)h² + Ag, have subset sums containing every multiple of g in [t h², M v1]. Repeated pigeonhole on gadgets with steps ≢ 0 mod m drives the gcd to 1 or 2 in ≤ log2 h + 1 rounds. In a 2-connected non-bipartite graph the shortest odd cycle gives an odd-step gadget.

## Evidence

- `kb/runs/2026-11-16-dossier/passes/20_closing_status.md#2`
- `kb/runs/2026-11-16-dossier/passes/20_closing_status.md#3`

## Caveats

Elementary.

## History

- 2026-11-17: created from the November 2026 run.
