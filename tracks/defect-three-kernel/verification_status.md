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
| S6 Type A/B/C case tree | `PROVED_DEPENDENCIES_IN_MARKDOWN`, `OPEN_CONCLUSION`, `NOT_FORMALLY_VERIFIED` | Exact T1--T5 consequences and first unproved implication per branch in `s6_case_tree.md`. The audit proves LR is not yet the sole S6 gate. |
| LR replacement principle / LR* | `PRINCIPLE_PROVED_IN_MARKDOWN`, `EXISTENCE_TARGET_CONJECTURAL`, `NOT_FORMALLY_VERIFIED` | Spectrum-safe replacement implication is proved; existence is open for the first unseen genuine remote leaf with C4/C8-clean `R-ab`. Root-side nodes exposed by S suppression are explicitly excluded from this inference. |
| Leaf-R pattern mining | `COMPUTATIONALLY_REPRODUCED` | Existing E23/E24 only, no census rerun: 75,745 leaves, 42 exact patterns; all 72,927 genuine original remote leaves have real-edge witnesses. Of 2,818 root-side exposed orientations, 608 need one suppressed-S element in the contracted witness (15 exact patterns). |
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
| I.1a-c cubic-core identities | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | `e(C,H)`, `\|E(F)\|`, `beta(F)` identities; 0 failures across 8,171 checks (atlas, inclusion-minimal fixtures, synthetic constructions). |
| I.1d C1/C2/C3 partition | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Needs M2; checked on the M2-satisfying populations only. |
| I.2 component-incidence quotient Q | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Corrects the naive "H!=empty" exception to the precise kappa(F)>=2 requirement, with an explicit kappa=1 witness. |
| I.3 weighted-incidence cycle formula | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Single- and multi-H alternating cycle length formula, explicit disjointness/distinctness hypotheses. |
| II.0 fast property-(2) equivalent | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | O(n(n+m)) replaces O(2^n); 0 mismatches over 1,865 cross-validation graphs. |
| D1 (h=0 case) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | q=1,h=0 forces n=6 exactly; both connected cubic 6-vertex graphs contain C4. |
| D1 (general case) | `COMPUTATIONALLY_VERIFIED`, `INCOMPLETE_RANGE` | 0 counterexamples among 1,128 property-(2) graphs, n=6..12 exhaustive (two independent generation routes agree at n=6,7); n=13 (17.4M raw graphs) attempted, did not complete. Not proved in general. |
| D1C completion lemma | `DISPROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED` | Fails starting n=9 (3 witnesses); 172 further failures by n=12. |
| III.1 C16 projection classification | `COMPUTATIONALLY_REPRODUCED`, exhaustive | All 1,545,746 C8-survivors across 4 bases are Type-1 (simple base C16, trivial holonomy); 0 instances of types 2-4. |
| III.2 full-space hyperplane coverage | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, exhaustive over `3^13` per base | Union of simple-C16 hyperplanes covers ALL of `F3^13\{0}`, not just C8-survivors, for all 4 bases. |
| III.3 standalone certificate | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | 24-27-vector covering subset per base; cross-checked against 1,200 real lift reconstructions (300/base), 0 disagreements. |
| V separator-defect formulas | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | q(G)=2d(lobe) for S5 (=> q=1 excludes cut vertex); q(G)=Sum(d(Bi))-{4,3,2} for Type A/B/C; 0 failures across 2,000 synthetic checks. |
| Leaf-count identity (leaf-compression I.1) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | c1=c3+4h-2q-4; 0 failures across 1,457 checks. |
| Derived leaf graph L(G), L1-L4 (I.2) | `PROVED_IN_MARKDOWN` (L1/L2 also `COMPUTATIONALLY_REPRODUCED`), `NOT_FORMALLY_VERIFIED` | L1/L2 mechanically verified on 1,443 synthetic C4-free instances (0 failures, 833 lifted-cycle checks); L3/L4 are minimality arguments, not empirically testable (no genuine small EGC fixture exists -- all 12 order<=7 atlas fixtures already contain C4). |
| c3+2h<=2q+1 / h<=q (I.3) | `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED` | Strong form needs h>=2 (genuinely fails at h=0, checked); weak corollary h<=q holds for all h via two different mechanisms. |
| q(G)>=2 (defect-one elimination, Part II) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | h=0 forces n=6 (exhaustive geng, both graphs have C4); h=1 forces c3=2, C4 via z-a-u-b-z, verified on 74 graphs n=7..12. |
| q(G)>=3 (defect-two elimination, Part III) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | h=0 forces n=8 (cites ex(8;{C4,C8})=11<12, exhaustive geng cross-check); h=1 forces c3=4, case-split verified on 384 graphs; h=2 gives c1=c3<=1, two sub-cases (period-4 coloring; handshake-lemma lollipop pendant-path) both exhaustively verified (0 escapes across 35+ configurations). |
| Weighted-incidence formula correction | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED` | Coefficient of t corrected from t to 2t (the original was a genuine arithmetic error, self-inconsistent with its own t=1 worked example); re-verified on 3,000 synthetic constructions, 0 failures. |
| Z5 exact coverage scan (IV.2) | `COMPUTATIONALLY_VERIFIED`, exhaustive over all `5^13-1` assignments/base | Base 1: exact 100% coverage (0 uncovered), certified by the full 315-vector hyperplane list (a candidate 48-vector compression FAILED exact verification with 21,156 exceptions -- caught and corrected, not used as the certificate). Bases 0,2,3: exactly 444/72/48 uncovered (corrects the previous sampled "~0" claim for bases 0,1,3). |
| Z5 exact-lift elimination (IV.3-IV.5) | `COMPUTATIONALLY_VERIFIED`, exhaustive | All 564 uncovered assignments independently lift-constructed and exactly tested: 148 at C8, 400 at C16 (all genuine Type-3, 0 anomalies after a real projection-formula bug was caught and fixed), 16 at C32, 0 survivors. Independent NetworkX recheck agrees on all 564. F5-scalar isomorphism proved; all 4 uncovered counts divisible by 4, 0 orbit-closure exceptions across 60 sampled orbits. |
| IV.A Z5 feasibility study | `COMPUTATIONALLY_VERIFIED`, `INCOMPLETE_RANGE` (Monte Carlo estimate + exact real-lift sample, not exhaustive) | 3/4 bases exact 100% coverage (0/2,000,000 uncovered); base 2 measurable ~5x10^-7 uncovered fraction with a confirmed non-simple-projection C16 witness. 4,000 real-lift samples: 0 counterexample candidates. A 50M/5000-sample confirmatory run did not complete in budget; not used in any conclusion. |
| IV.B order-26 feasibility | `INFEASIBLE` (benchmark-based, no generation launched) | n=22 raw C4-free cubic generation did not complete in 400s; n=16/18/20 calibration (269/2,761/36,101 graphs) extrapolates to ~6 days for n=26 raw generation alone. |
| Bounded branching-kernel lemma (defect-three I) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | n=2q+4 (h=0), c3=2q (h=1), c1+c3<=2q-2 (h>=2, C4/C8-free scope); 0 failures across 13 atlas + 229,948 synthetic graphs. |
| Exact q=3 case table (defect-three II) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | Six rows derived symbolically from I.1 at q=3; cross-checked against exhaustive geng n=10-13 (C4/C8-free scoped): all 6 rows realized, 0 off-table signatures. |
| q=3, h=0/h=1 elimination (defect-three III) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | h=0 (n=10): 19/19 cubic graphs have C4/C8 (exhaustive geng). h=1 (n<=13, via branch-incidence+chain-length bounds and the P13-free theorem, L7): 2317/2317 generated graphs have C4/C8, 0 c2<=6 violations. |
| Colored degree-2 path lemma (defect-three IV) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED` (2 independent implementations), `NOT_FORMALLY_VERIFIED` | t<=2,5,8 for h=1,2,3, each tight. Direct-construction prefix-closed search and a minimal finite-state automaton (provably finite state space via saturating arc-age counters) agree exactly: 0 mismatches over 29,655 words. |
| Colored cyclic-word classification (defect-three V) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | No valid pure-cycle F-component at h=1 or h=2; exactly s=3,5 at h=3 (proved via a corollary of the linear lemma, cross-checked exhaustively to s=13). |
| h=2 elimination, both rows (defect-three VI) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | (0,2): theta pigeonhole argument + exhaustive reconstruction (6,804 theta + 304 dumbbell, 0 survivors). (1,3): kappa=2 reduces to (0,2) by citation; kappa=1's 3 enumerated topologies (general stub-matching enumerator) each give 0 survivors via backtracking. |
| h=3 elimination, both rows (defect-three VII) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | (2,0): new H-degree-feasibility argument forces t=8 exactly; exhaustive t=8 sweep gives 0 survivors; 144/144 pure-cycle-compatibility pairs incompatible. (3,1): star (kappa=1, uniquely forced) and lollipop+path (kappa=2) backtracking searches (41,958+ realizations) give 0 survivors, confirmed C4/C8-driven not degree-driven. |
| q(G)>=4 (defect-three, Part VIII) | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` | All six q=3 case-table rows eliminated (outcome 1 of the required Part VIII outcomes); q(G)=3 impossible for a minimal counterexample; |E(G)|<=2|V(G)|-6. |

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

## Global-core/Z3/S6 phase execution record

The exhaustive lift run and both full independent audits are frozen in their
checksummed manifests. The following final integrity commands were run from the
repository root on 2026-07-25/26 EDT with Python 3.14.6 and nauty 2.9.3.

| Command | Exit | Result |
|---|---:|---|
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/global_core_check.py` | 0 | 12 inclusion-minimal atlas graphs, six equality cases, zero failures. |
| `c++ -O3 -std=c++17 -Wall -Wextra -pedantic verifier/z3_lift_search.cpp -o verifier/z3_lift_search` | 0 | Warning-clean exact-engine build. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/z3_lifts.py --certify-bases` plus SHA-256 comparison | 0 | Reproduced `z3_bases_manifest.json` byte-for-byte (`352a0a...72cc`). |
| full four-shard C++ enumeration recorded in `z3_lift_run_manifest.json` | 0 | 6,377,288 nonzero assignments; 1,545,746 after C8; zero after C16. |
| `independent_z3_c4_verify.py` full audit | 0 | 6,377,288 assignments checked; zero disagreements. |
| `independent_z3_verify.py` full audit | 0 | 1,545,746 C8 survivors, 1,024 random assignments, and eight witnesses checked; zero disagreements. |
| independent SHA/row-count audit of all Z3 artifacts | 0 | 12 base files, four shard summaries, 1,545,746 survivor rows, sources, and independent manifests match. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/leaf_r_patterns.py --output manifests/leaf_r_patterns_manifest.json` | 0 | 75,745 leaves; 42 exact patterns; all 72,927 genuine original remote leaves real-edge positive. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/leaf_r_replacement_search.py --output manifests/leaf_r_replacement_small_manifest.json` | 0 | 87,004 skeletons; 1,802,018 rooted pairs; ten C4-free and zero C4/C8-free. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/test_detector.py` | 0 | Known graphs and 2,107 randomized comparisons pass with zero disagreements. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q` | 0 | 81 passed in 4.53 s; no failures, skips, or xfails. |
| `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m compileall -q .` | 0 | All Python sources compiled. |
