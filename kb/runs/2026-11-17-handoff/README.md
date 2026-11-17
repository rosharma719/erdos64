---
id: run-2026-11-handoff-readme
title: "17 November 2026 handoff — index and cross-references"
kind: run
topics: ["run-2026-11-handoff"]
doc_status: active
date: 2026-11-17
summary: "Entry point for the imported handoff dossier: what it contains, how its evidence tags map to repository labels, registered claims and open problems, and cross-references to existing results (q(G) ≥ 4, Pass XIV rooted results, gadget-window precedent)."
---

# 17 November 2026 handoff (imported)

A research handoff from a separate conversation, imported verbatim on 17 November 2026.
**It does not prove the conjecture**, and says so.

## Contents

| Path | What |
|---|---|
| `handoff/` | Verbatim bundle. `Erdos_Gyarfas_Full_Research_Dossier.md` is the preferred format (identical `.txt`, 21-page `.pdf`). `SHA256SUMS.txt` verified on import (all OK). The separately uploaded PDF is byte-identical to the one here. |
| `handoff/Original_Research_Packets/` | Eight original packets, as zips, plus `EG_shortest_proof_route.md` and `EG_shortest_path_audit.py`. |
| `packets/` | Extracted copies of the eight zips, for direct reading. No compiled binaries; excluded from pytest collection. |

## Evidence tags → repository labels

| Handoff tag | Repository label used in claim files |
|---|---|
| [LITERATURE] | KNOWN FROM LITERATURE |
| [DERIVED] (not refereed) | SKETCH |
| [DERIVED], short argument given in full | PROVED (as reported) |
| [COMPUTED] / [RECHECKED 17 NOV] | COMPUTATIONALLY VERIFIED (as reported by the handoff's author; **not re-run on import**) |
| [UNRESOLVED] | OPEN |
| [REFUTED AUXILIARY CLAIM] | DISPROVED (for the auxiliary claim only) |

## Registered in the claim registry

- `q-three-terminal-forcing-lemma` (OPEN): the handoff's endpoint. Equivalent to EG; the
  proof of equivalence is short and reproduced in §7.2 of the dossier.
- `c-handoff-c4c8-edge-bound` (COMPUTATIONALLY VERIFIED + PROVED, as reported): if
  n ≥ 10, δ ≥ 3, there is no C₄ or C₈, and no proper subgraph has minimum degree 3, then
  |E| ≤ 2n − 5.
- `c-handoff-short-cycle-edge-cover` (SKETCH): a cubic graph in which every edge lies on a
  C₃ or C₅ contains a C₄ or C₈.
- `c-handoff-saturated-triangle-bound` (SKETCH): 8t < n for t disjoint saturated
  T-gadgets in a bridgeless cubic dyadic-free graph.
- `c-handoff-coxeter-transversals` (COMPUTATIONALLY VERIFIED): the Coxeter graph has 21
  C₈ and 609 C₁₆; minimum C₈ transversal 6; minimum C₁₆ transversal 5.
- `c-handoff-rooted-on-cycle-fails` (DISPROVED auxiliary claim): an 18-vertex connected
  cubic graph has a vertex lying on no dyadic cycle.
- `q-order28-rooted-census` (OPEN): the 251-graph order-28 dataset was never obtained.

## Cross-references to existing results (read before citing)

1. **Edge bound versus q(G) ≥ 4.**
   - `kb/core/proof.md` P9–P12 records q(G) = 2n − 2 − m ≥ 4, i.e. m ≤ 2n − 6, for a
     *minimal counterexample* (PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH).
   - The handoff's |E| ≤ 2n − 5 has a different hypothesis: only C₄ and C₈ are forbidden,
     and the graph need only be δ ≥ 3 with no proper δ ≥ 3 subgraph. It is not directly
     comparable.
   - But for minimal counterexamples the repository's bound is stronger. The handoff's
     claim to improve on Ducoffe–Dumitru's 2n − 2 should be read with that in mind.
2. **Two different "rooted" properties.**
   - The handoff refutes *"every vertex lies **on** a dyadic cycle"*, using a graph with
     bridges.
   - Pass XIV (`c-rooted-robustness-fails-n16`) concerns *"every vertex is **avoided** by a
     dyadic cycle"*, in 3-connected cubic graphs.
   - The two results are independent and do not conflict.
3. **Gadget windows.** The handoff notes precedent for its three-port gadget and
   window method in Salehi Nowbandegani et al. (2014) and Garcia (arXiv:2609.04686, Sep
   2026, the symmetric H7′ gadget). Compare also the Π-gadget and Fan pocket adjusters of
   Passes XVI–XX, which are path-anchored rather than vertex-substituted.
4. **Coxeter transversals.** These complement the 24-vertex near-miss transversal data in
   the 16 November dossier (§4.2).
5. **Edge-cover claim.** The cubic short-cycle edge-cover claim interacts with the
   pentagon/triangle structure of the order-30 census (`kb/notes/finite-frontier/`).

## Literature added by the handoff (not verified on import)

- Narins–Pokrovskiy–Szabó, *Degree-critical graphs with a missing cycle length*,
  arXiv:1408.5289.
- Di Braccio et al., *Leaf-to-leaf paths and cycles in degree-critical graphs*,
  arXiv:2504.11656.
- Salehi Nowbandegani–Esfandiari–Shirdareh Haghighi–Bibak, *On the EG conjecture in
  claw-free graphs* (2014).
- Computational cubic census repository: github.com/chriss1245/erdos-gyarfas-cubic-frontier
  (reported order-40 result).
- Independent research note: github.com/oaustegard/experiments, erdos-gyarfas/note.html.
- Earlier Zenodo claimed proof, record 22019344. Not accepted as validated, by the
  handoff or by us.
