# Verification status

> **The project has reproducible computations and human-readable mathematical proofs. It does not currently have proof-assistant-level formal verification.**

No Lean, Coq, Isabelle, or comparable machine-checked development exists in
this repository. `PROVED_IN_MARKDOWN` means a human-readable proof is present;
it must not be paraphrased as formally verified.

| Item | Status | Scope and evidence |
|---|---|---|
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
| E22 bridge closure | `COMPUTATIONALLY_REPRODUCED`, `INCOMPLETE_RANGE` | 5,212 candidates through n=8; n=9+ unfinished. |
| Bridge order 9 | `INCOMPLETE_RANGE` | Generator and verification pipeline are the next step of the current phase; no completed-range claim yet. |
| Three-copy lift verification | `INCOMPLETE_RANGE` | Direct dual-detector census pending the complete order-nine rooted population. |
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
