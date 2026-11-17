---
id: run-2026-11-readme
title: "November 2026 research run — index"
kind: run
topics: ["run-2026-11"]
doc_status: active
date: 2026-11-17
summary: "Entry point for the 16–17 November run: reading order, layout, and the open-items list."
---

# Research dossier, 16–17 November 2026

The record of the November research run on the Erdős–Gyárfás conjecture (open).
**Nothing here proves or disproves the conjecture.** Every note labels its claims as
PROVED, EXTERNAL, COMPUTED, SKETCH or OPEN.

## Start here

1. `program/STRATEGY_2026-11-17.md`
   - Why disproof looks unlikely (the growth reformulation);
   - where rooted gluing breaks;
   - the program in outline.
2. `passes/20_closing_status.md` — the current status of the expander pillar: what is
   proved and what is open.
3. `LITERATURE_REVIEW.md` — every external result used, with its verification level.

## Layout

| Path | Contents |
|---|---|
| `Erdos_Gyarfas_Research_Dossier.{md,pdf}` | Consolidated dossier of 16 Nov: Passes I–XII, the resilience ceiling, the order-16/18 census |
| `source_archive/` | Notes, scripts, logs and historic material behind the dossier (checksums in `SHA256SUMS.txt`) |
| `program/STRATEGY_2026-11-17.md` | Strategic assessment and literature-driven program |
| `program/PROGRAM_2026-11-17.md` | Milestones, dependencies, probabilities (M2 line superseded by Pass XVI) |
| `passes/13_tripod_theta_tree_backbones/` | Pass XIII packet: induced-tree backbones, rank-two obstruction (with scripts) |
| `passes/14_rooted_stress_test/` | Pass XIV: rooted robustness on all 3-connected cubic graphs ≤ 16 and on external hard graphs. Contains C checker, generator, catalogs, logs. |
| `passes/15_pillar_A_attempt.md` | FK construction read in full; exactness reduces to adjuster attachment |
| `passes/16_crux_sharpening.md` | δ ≥ 3 alone is insufficient; Fan pocket adjusters; three-escapable lemma; crux = Martinsson–Steiner question |
| `passes/17_short_nonzero_residue.md` | **Theorem:** short nonzero-residue cycles in 2-connected δ ≥ 3 expanders, any α. Constant-specials reduction. |
| `passes/18_robust_specials.md` | Anchoring and nesting lemmas (few rigid candidates); free-entry gadgets; chain sketch |
| `passes/19_threading_and_gaps.md` | M1 threading design; G2 outline; mod 4 reduced |
| `passes/20_closing_status.md` | Π-gadget lemma, coin lemma, parity lemma, G3 for odd primes; open list |
| `LITERATURE_REVIEW.md` | Literature review with verification levels and novelty positioning |

## Open items (as of Pass XX)

1. **G1′:** mod-4 rigidity in bipartite cores whose pockets all have ≥ 3 attachments.
2. Robust linkage of *specific* vertices in weak expanders. Rewrite as selections from
   large sets.
3. M1: recheck the FK constants with the removed set and the new root choices.
4. Subcase T of G3 (tiny certificate cycles).
5. Check the conditional expander theorem against Lyngsie–Merker's 2-connected cubic
   examples.
6. Verify Fan (2002) Cor. 3.1 in the original.
7. Pillar B, graphs with no large expanding piece: not started.
