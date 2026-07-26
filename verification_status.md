# Verification status

> **The project has reproducible computations and human-readable mathematical proofs. It does not currently have proof-assistant-level formal verification.**

No Lean, Coq, Isabelle, or comparable machine-checked development exists in
this repository. `PROVED_IN_MARKDOWN` means a human-readable proof is present;
it must not be paraphrased as formally verified.

| Item | Status | Scope and evidence |
|---|---|---|
| Two-thirds cubic lemma (G1) | `PROVED_IN_MARKDOWN`, `NOVELTY_SUPPORTED_BY_SEARCH`, `NOT_FORMALLY_VERIFIED` | Carr's two proved local facts sharpen his `4/7` count to `2/3`; full preprint and targeted search audited in L18. |
| Edge bound `m<=2n-3` (G2) | `PROVED_IN_MARKDOWN`, `KNOWN_INGREDIENTS`, `NOT_FORMALLY_VERIFIED` | `G-v` is 2-degenerate; equality is degree-3-critical and EFGS forces a C4. |
| Defect framework (G3) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | `q>=1`, exact forward-degree deficit identity, and degree-excess bound; small inclusion-minimal graphs checked adversarially. |
| Four 24-vertex lift bases | `SOURCE_CERTIFIED`, `COMPUTATIONALLY_REPRODUCED` | Hegde--Sandeep--Shashank `special-graphs` at frozen commit; graph6/sparse6/edge checksums, automorphisms, rank, and two-detector C4/C8/C16 certificates in `z3_bases_manifest.json`. |
| Normalized cyclic Z3 framework | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Exact 13-coordinate gauge normalization and connectivity proof; Python fixtures cover zero and nonzero lifts; C++ staged exact engine covers 4/8/16/32/64. |
| Cyclic Z3 lift enumeration | `COMPUTATIONAL_ELIMINATION`, `INDEPENDENTLY_REPRODUCED` | All 6,377,288 nonzero assignments: 1,545,746 survive C8 and zero survive C16. Python checked every post-C4 and post-C8 survivor, 1,024 random assignments, and every stored witness with zero disagreements. Scope is only these four bases. |
| S4 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Bridgelessness proof in `lemmas.md`; novelty supported by limited search. |
| S5 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Cut-vertex classification in `lemmas.md`; novelty supported by limited search. |
| O1 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Master-minimal one-pole graph is bridgeless. |
| O2 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Root deletion is connected; corollary of O1. |
| O3 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Full 2-connectivity. |
| O4 | `CONJECTURAL`, `NOT_FORMALLY_VERIFIED` | Disjoint root-neighbor paths remain open; O4a describes failure and O4′ is a literature-based admissible-path corollary. |
| O5 | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Rigid-core/K4-minor lemma; 304 series-parallel cases checked. |
| O6 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Conditional proper two-pole forcing. |
| O7 | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Conditional no-external-common-neighbor lemma; E17/E18 are supporting computations. |
| T1 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Bridge closure is 2-connected. |
| T2 | `PROVED_IN_MARKDOWN`, `KNOWN_FROM_LITERATURE`, `NOT_FORMALLY_VERIFIED` | Endpoint admissible paths, using Gao–Huo–Liu–Ma. |
| T3 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Bridge self-forcing/minimality lemma. |
| T4 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Minimal terminal cover and exact Type A/B/C classification. |
| T5 | `PROVED_IN_MARKDOWN`, `IMPLEMENTATION_FIXED`, `NOT_FORMALLY_VERIFIED` | Replacement forcing; Type A/B filtering now precedes cross-spectrum checks. |
| T6 | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Direct simple copy-gadget criterion; terminal edge must be absent from B. |
| T8 | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Minimal Type-A gadget edge-criticality; deletion monotonicity and exact degree cases have adversarial fixtures. |
| R1/R1b | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `IMPLEMENTATION_FIXED`, `NOT_FORMALLY_VERIFIED` | Real R-skeleton edge deletion and expansion preservation. Zero violations across 64,596 validated R-real edge instances; invalid package R labels are rejected. |
| T8R | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | T8+R1 incidence rule; 25,914 critical incidences and 38,682 nonminimality certificates in relaxed fixtures. |
| R2/T8P | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Real P-edge deletion and tight-degree corollary; zero violations on 388 atlas and 3,498 relaxed-closure P-edge instances. |
| S/P leaf classification | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Exact finite S-leaf forms and impossibility of original P-leaves; zero classification violations across 5,212 relaxed closures. |
| Rigid-leaf dichotomy | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Proved for minimal rigid-forced gadgets after terminal-S suppression. Relaxed failures document why tightness and self-sum cleanliness are necessary. |
| E0 detector cross-check | `COMPUTATIONALLY_REPRODUCED` | 2,107 Python checks and independent C/Python checks reproduced without disagreement. |
| E1 order 10 | `COMPUTATIONALLY_REPRODUCED` | Python and C checked 5,203,110 connected minimum-degree-3 graphs; zero survivors. |
| E1 order 11 | `COMPUTATIONALLY_REPRODUCED` | C checked 577,076,528 graphs; zero survivors. |
| E1 order 12+ | `INCOMPLETE_RANGE` | Order 12 was partial; no claim beyond order 11 is locally certified by E1. |
| E5(a) McKay files | `EXTERNAL_DATA_MISSING` | Historical results retained, but eight `.s6` files are absent; see `manifests/external_s6_manifest.json`. |
| E5(b) order-18 cubic check | `COMPUTATIONALLY_REPRODUCED` | 2,761 C4-free cubic graphs; zero C8-free survivors. |
| E6 n=20–23 near-cubic layers | `INCOMPLETE_RANGE` | Not launched/completed. |
| E9 one-pole search | `COMPUTATIONALLY_REPRODUCED`, `INCOMPLETE_RANGE` | 67,432 candidates through n=9; n=10 unfinished. |
| E14 edge-rooted search | `COMPUTATIONALLY_REPRODUCED`, `INCOMPLETE_RANGE` | 47,349 pairs through n=8; n=9 unfinished. |
| E16/E17 K4 census | `COMPUTATIONALLY_REPRODUCED`, `IMPLEMENTATION_FIXED` | 117,649 assignments, 5,525 clean, 4,717 after O7; census now executes once. |
| E19 bridge signatures | `COMPUTATIONALLY_REPRODUCED`, `INCOMPLETE_RANGE`, `IMPLEMENTATION_FIXED` | Empty through n=7; n=8 unfinished. Direct terminal edge is rejected and C_F is named as dyadic-only. |
| E20 bridge compatibility | `IMPLEMENTATION_FIXED` | Exact Type A/B/C search; real n≤7 run is vacuous, while synthetic tests exercise every path nonvacuously. |
| E21 abstract reconciliation | `COMPUTATIONALLY_REPRODUCED`, `IMPLEMENTATION_FIXED` | Old strict count 318; corrected tied count 547; exact 229-gap regression. Abstract conditions are insufficient; neither count is evidence toward the conjecture. |
| E22 bridge closure | `COMPUTATIONALLY_REPRODUCED`, `INCOMPLETE_RANGE` | 5,212 candidates through n=8. Its broader range stops there; E23b separately completes the targeted Type-A order-9 census. |
| Bridge order 9 | `COMPUTATIONALLY_REPRODUCED` | Complete 1/1 residue: 193,510 closures, 129,040 rooted oriented classes, zero internally clean bridges. |
| Compact Type-A order 9 | `COMPUTATIONALLY_REPRODUCED` | All 33 exact `{C4,C8}`-free extremal graphs and 2,376 ordered terminal choices checked twice; zero Type-A choices. |
| Direct Type-A order 10 | `COMPUTATIONALLY_REPRODUCED` | Complete m=13,14 C4-free layers: 57+216 raw, 4+12 C8-free, zero degree-1 roots. |
| Exact Type-A order 11 | `COMPUTATIONALLY_REPRODUCED` | All 245 exact extremal graphs and 26,950 ordered terminal choices checked twice; zero Type-A choices. |
| Type-A finite bound through 11 | `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Every structural Type-A bridge through order 11 has C4 or C8; identical-copy T6 constructions therefore have order at least 32. |
| Three-copy lift verification | `COMPUTATIONALLY_REPRODUCED` | All 129,040 lifts directly checked for C4/C8/C16 by Python and independent C detectors; zero survivors and 129,040 equivalence agreements. |
| Order-9 SPQR obstruction support | `COMPUTATIONALLY_REPRODUCED` | Existing E23 artifact mined without regeneration: 98,990 R-local, 29,581 P-created, 469 multi-node shortest witnesses. |
| T7 | `CONJECTURAL` | T7 remains gated on finding at least one internally clean bridge. |

## Integrity-pass execution record

All commands below were run from the repository root on 2026-07-25/26 EDT
with Python 3.14.6 in `.venv`.

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q` | 0 | 19 passed in 3.01 s; no failures or skips. |
| `.venv/bin/python -m compileall -q .` | 0 | All Python sources compiled. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/test_detector.py` | 0 | Known graphs pass; 2,107 randomized `(graph,L)` comparisons, zero disagreements. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/three_bridge_search.py` | 0 | E21: 318 old, 547 corrected, exact delta 229. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/bridge_signature.py --nmin 3 --nmax 7` | 0 | E19: 19,845 terminal pairs, empty qualifying library. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/bridge_compatibility.py --nmin 3 --nmax 7` | 0 | E20: typed real-data run empty/vacuous; all paths covered by synthetic tests. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/spqr_k4_skeleton.py` | 0 | One 117,649-assignment census; 5,525 clean and 4,717 O7 survivors. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/linkage_data.py` | 0 | All seven identity fixtures pass. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/bridge_closure_search.py --nmin 5 --nmax 8` | 0 | E22: all 5,212 candidates processed. |

E5(a) was not rerun: its eight external McKay `.s6` inputs are absent from
the checkout. Their authoritative URLs, line counts, and SHA-256 checksums
are recorded in `manifests/external_s6_manifest.json`; the local status of
each remains `MISSING`.

## T8/order-9 execution record

The following final integrity checks were run from the repository root on
2026-07-25 EDT with Python 3.14.6. The definitive order-9 run itself is
recorded in `manifests/E23_order9_manifest.json`: it completed exit 0 in one
complete residue, and both independent detector batches completed exit 0.

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q` | 0 | 35 passed in 5.24 s; no failures, skips, or xfails. |
| `.venv/bin/python -m compileall -q .` | 0 | All Python sources compiled. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/gadget_criticality.py --nmin 5 --nmax 8` | 0 | 5,212 closures and 64,596 real R-edges; zero R1 violations; 25,914 T8R incidences and 38,682 noncritical deletion certificates. |
| `cc -O3 -std=c11 -Wall -Wextra -pedantic verifier/check_power_masks.c ...` | 0 | Warning-clean compile; C4 and empty synthetic records returned the expected masks 1 and 0. |
| `gzip -t data/E23_order9_candidates.jsonl.gz` | 0 | Complete compressed artifact passes integrity check. |
| `shasum -a 256 data/E23_order9_candidates.jsonl.gz` | 0 | `9f530d95918406bec166cc3e09fa5edf0d7b8f8ff58613b9ffae83c85851e446`, matching the manifest. |
| streamed JSONL field/count audit with `jq` and `awk` | 0 | 129,040 records; 4,214 SP-eligible; 124,826 rigid-forced; zero internal/lift-clean; 129,040 equivalence agreements; zero Python/C mask disagreements. |

## Extremal/SPQR phase execution record

All commands were run from the repository root on 2026-07-25 EDT with
Python 3.14.6 and nauty 2.9.3.

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/type_a_extremal_check.py --output manifests/E24_extremal_manifest.json` | 0 | 33 order-9 and 245 order-11 extremal graphs; 29,326 ordered terminal choices; zero survivors and zero checker disagreements. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/type_a_order10_direct.py --run ...` | 0 | Complete m=13,14 plans; 57+216 raw C4-free, 4+12 C8-free, zero degree-1 roots. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/spqr_extremal_audit.py ...` | 0 | R2, S/P leaves, and scoped rigid-leaf audit complete; zero in-scope failures. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/order9_spqr_obstructions.py --workers 8 ...` | 0 | Reused 129,040 E23 records; completed in 328.044 s without graph generation. |
| independent streamed E24d JSONL audit with `jq` and `awk` | 0 | Exact class/support/leaf totals reproduced; zero malformed records. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q` | 0 | 45 passed in 7.65 s; no failures, skips, or xfails. |
| `.venv/bin/python -m compileall -q .` | 0 | All Python sources compiled. |
