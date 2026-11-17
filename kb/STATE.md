---
id: state-of-knowledge
title: "State of knowledge — read this first"
kind: guide
topics: ["guide"]
doc_status: active
date: 2026-11-17
summary: "Curated one-page state of the Erdős–Gyárfás project: the conjecture, verified frontier, what this repository has established (with labels), the November 2026 expander program, open problems, dead ends, and where to look next."
---

# State of knowledge (last curated 2026-11-17)

> **Conjecture (Erdős–Gyárfás 1995; Erdős Problems #64).** Every finite simple graph with
> minimum degree ≥ 3 contains a cycle whose length is a power of two.
>
> **Status: OPEN.** Nothing in this repository proves or disproves it.

This page is curated by hand. When you add a result, update the relevant bullet and
point to the claim file. The exhaustive, generated list of documents is
[`INDEX.md`](INDEX.md). Machine-readable metadata is in [`index.json`](index.json).

## 1. Label vocabulary

These are the labels used everywhere. They come verbatim from `kb/core/proof.md`; never
upgrade one without evidence.

| Label | Meaning |
|---|---|
| **PROVED** | Complete human-readable proof in this repo; not machine-checked. |
| **COMPUTATIONALLY VERIFIED** | Exhaustive or certified computation, with command and counts recorded. |
| **KNOWN FROM LITERATURE** | Cited, with the exact source. |
| **SKETCH** | Argument outlined; some steps not written. |
| **CONJECTURAL** | Stated, not established. |
| **OPEN** | Open problem. |
| **DISPROVED** | Refuted, with a witness. |

Legacy files also carry qualifiers such as `NOVELTY SUPPORTED BY SEARCH`,
`BOUNDED_INCOMPLETE`, `INCOMPLETE_RANGE` and `PROVED_IN_MARKDOWN`. They are kept
unchanged; see `kb/core/verification_status.md`.

## 2. Verified frontier (external, 2026)

Detail and verification levels are in `kb/runs/2026-11-16-dossier/LITERATURE_REVIEW.md`.

- **No counterexample, by order:**
  - all graphs ≤ 40 vertices, cubic ≤ 48, bipartite ≤ 66 (Ducoffe–Dumitru,
    arXiv:2609.28594);
  - an independent unrefereed campaign reports cubic ≤ 48 (frontier ≥ 50) and
    bipartite ≤ 56;
  - cubic bipartite ≤ 58, by certified computation (Tranquilli, arXiv:2608.02675).
- **Minimal counterexamples** are 2-edge-connected and almost biconnected; more than 2/3
  of their vertices have degree 3; every regular one is cubic (Carr, arXiv:2605.22844).
- **Proved classes:**
  - 3-connected cubic planar graphs (Heckman–Krakovski);
  - claw-free graphs; P₈-, P₁₀- and P₁₃-free graphs; diameter 2;
  - odd-order Cayley graphs (Burkhart, arXiv:2611.05060);
  - sufficiently large constant average degree (Liu–Montgomery).
- **Near-misses** (unrefereed constructions):
  - smallest cubic graph with no C₄, C₈, C₁₆ has between 50 and 82 vertices;
  - a 370-vertex cubic graph avoids C₄–C₃₂;
  - a 26,550-vertex cubic graph avoids C₄–C₆₄.
- **Expert view:** Montgomery's 2026 survey (arXiv:2607.26049) says a proof "would
  require very substantial new ideas".

## 3. Established in this repository, July–October 2026 (see `kb/core/proof.md`)

Headline items, with their labels exactly as in `proof.md`:

- **Part I — structure of a minimal counterexample**
  - P1 [COMPUTATIONALLY VERIFIED] no counterexample on ≤ 11 vertices.
  - P2 [PROVED] degree structure.
  - P9–P12 [PROVED IN WORKSPACE] q(G) = 2n − 2 − m ≥ 4.
- **Part II — separators**
  - P5 S4/S5 separator lemmas.
  - P7 one-pole gadget theory O1–O7.
  - P14 [PROVED / COMPUTATIONALLY VERIFIED] the 2-cut trichotomy and F-series.
  - P15 [PROVED] cubic 3-edge-connectivity in range.
- **Part III — contraction / Type-N–Type-T local program;** Type-B realizability. Notes
  under `kb/notes/{contraction,central-bridge,type-b,type-t}/`.
- **Part IV — Type-T C16 port completion**
  - C16-1 to C16-3 [PROVED].
  - C16-4 [COMPUTATIONALLY VERIFIED].
  - C16-6 [BOUNDED_INCOMPLETE].
- **Parts V–VII — finite and algebraic**
  - P11 [COMPUTATIONALLY VERIFIED] Z₃/Z₅ lifts.
  - P4 4-or-8 dichotomy through n = 19.
  - P17 [COMPUTATIONALLY VERIFIED] cubic layers n = 20 and 22.
  - Order-30 triangle-quotient census O30-1 to O30-4.
- **Part VIII — disproved or retracted** (kept on purpose):
  - the sharp additive-density formula;
  - the target n ≤ 2D + 3;
  - the vine charging lemma V1;
  - D1C;
  - the one-cell reduction;
  - FC-19/20/21;
  - inflated passage-conflict counts.
- **Part IX:** external claims audited and **not** established, including broad order
  32–38 eliminations.

## 4. November 2026 run (`kb/runs/2026-11-16-dossier/`)

One claim file each in `kb/claims/`:

- `c-growth-reformulation` [PROVED] — EG ⟺ f(k) ≥ 2^(k+1). The smallest open finite band
  is k = 5: graphs on 41–63 vertices avoiding C₄–C₃₂; for cubic graphs, 50–62.
- `c-rooted-robustness-fails-n16` [COMPUTATIONALLY VERIFIED]
- `c-rooted-robustness-hard-instances` [COMPUTATIONALLY VERIFIED]
- `c-three-cut-rooted-gluing` [PROVED] — rooted 3-cut gluing works except at triangle and
  7-vertex sides, which are genuine obstructions.
- **The expander pillar.** Program: exact cycle lengths in 2-connected bounded-degree
  expanders with δ ≥ 3.
  - `c-delta3-induced-cycle-adjuster` [PROVED]
  - `c-fan-pocket-adjusters` [PROVED; relies on Fan 2002 via secondary quote]
  - `c-three-escapable-lemma` [PROVED]
  - `c-short-nonzero-residue-cycles` [PROVED, needs refereeing]
  - `c-anchoring-nesting` [PROVED]
  - `c-pi-gadget` [PROVED]
  - `c-coin-gcd-parity` [PROVED]
  - `c-rigid-pocket-example` [SKETCH] — δ ≥ 3 alone is insufficient; connectivity is
    needed.
  - ⇒ `c-conditional-expander-theorem` [CONJECTURAL]: conditional on the open items
    below. **Even if completed it is not EG.**
- `c-resilience-ceiling` [PROVED] — from the uploaded dossier.

## 5. Open problems (one file each in `kb/open/`)

| id | One line |
|---|---|
| `q-mod4-bipartite-pockets` | The only genuinely mathematical gap left in the expander pillar. |
| `q-robust-linkage` | Turn single-vertex robustness into selections from large sets. |
| `q-fk-threading-constants` | Recheck Friedman–Krivelevich with the threading modifications. |
| `q-subcase-t` | Tiny certificate cycles in G3. |
| `q-lyngsie-merker-check` | Could their 2-connected cubic counterexamples be expanders? |
| `q-verify-fan-cor31` | Read Fan (2002) in the original. |
| `q-pillar-b-nonexpanding` | Graphs with no large expanding piece: **not started**. |
| `q-cubic-4-8-16-free-50-62` | The decisive finite computation (SAT scale). |
| `q-martinsson-steiner` | External open question that our program would partly settle. |
| `q-rooted-prime-conjecture` | From the dossier; survives all tests. |

## 6. Dead ends (do not re-try without a new idea)

- **Small-order enumeration below the published frontier** (≤ 40 general, ≤ 48 cubic).
- **New rooted censuses.** Rooted robustness for 3-connected cubic graphs is false at
  n = 16.
- **Ad hoc gadget passes** without a growth or absorption argument.
- **The "pattern on N = 2ᵏ" inference.** It is the most repeated failure mode
  (`kb/core/RETROSPECTIVE.md`).
- **Unqualified degree-2 suppression.** It shifts cycle lengths.
- **Interval or residue coverage alone.** It never locates an exact power of two
  (dossier §5).

## 7. Where to look next

1. `kb/open/q-mod4-bipartite-pockets.md`, then the robust-linkage write-up. This
   completes the expander pillar.
2. `q-cubic-4-8-16-free-50-62`, on external compute.
3. Pillar B, which needs a new idea for non-expanding minimal counterexamples.
