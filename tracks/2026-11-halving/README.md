# tracks/2026-11-halving — session of 2026-11-16

Independent audit of the repository, then a new line of work that converged on
one central conjecture. **Node statuses: `BLUEPRINT.md`. How the two models
divide the work: `WORKFLOW.md`.** Nothing here edits the canonical ledger files other
than status-log entries in `plan.md`.

## Central target: Conjecture T

> **Conjecture T.** Every connected graph with exactly three vertices of degree
> 2, all others of degree 3, and no cycle of length a power of two, is one of
> four graphs: the triangle, uniform H7, skew H7, or H15 (3, 7, 7, 15 vertices).

**T implies the Erdős–Gyárfás conjecture for every cubic graph**: delete a leaf
of a spanning tree from a cubic counterexample. Statement and proof:
`three_port_classification.md`. Plan of attack:
`research_brief_additive_reduction.md`.

### Status map

| Statement | Status | Where |
|---|---|---|
| T ⇒ Erdős–Gyárfás for all cubic graphs | **Proved** (short, uses the published order bound) | `three_port_classification.md` |
| No clean 3-pole on 5 vertices | **Proved** by hand, plus brute force | `audits/three_pole_research_handoff.md` |
| Clean 3-poles on ≤ 21 vertices are exactly the four in T | **Certified** for checkers (two independent), single generator | `three_pole_census_manifest.md` |
| No clean 2-pole on ≤ 20 vertices | **Certified** for checkers, single generator | `three_pole_census_manifest.md` |
| Pass VI Hamiltonian survivors are these poles | **Computed**, identification only, not uniqueness | `scripts/check_three_pole_isomorphisms.py` |
| Triangle-built clean 3-poles have 1, 3, 7, 15 vertices, at every size (tower theorem) | **Reviewed**: proof by ChatGPT, checked by Claude; awaits your sign-off | `tower_theorem.md`, `pass12/REVIEW.md` |
| Order 23 | **Open**; about 3.3 hours on two cores | `three_pole_census_manifest.md` |
| Decomposition, 3-edge-connected caps | **Reviewed**: ChatGPT, checked by Claude | `decomposition_lemma.md`, Part A |
| Decomposition, bridges and 2-edge cuts (joint minimality over 1-, 2-, 3-poles) | **Proved, draft** (Claude); awaits ChatGPT's review | `joint_minimality.md` |
| WRP ⇒ T* ⇒ T (T*: also no clean 1- or 2-poles) | **Proved, draft** (Claude); awaits review. If it holds, WRP is the only open step to T | `joint_minimality.md` |
| WRP for gadget-heavy labellings | **Proved** above an explicit global threshold | `cycle_space_obstruction.md` |
| WRP for identity/triangle-heavy labellings (doubling-chain lemma) | **Open**; the main conceptual gap | brief, Step 5 |
| Non-cubic graphs (vertices of degree ≥ 4) | **Not covered** by this programme | — |

"Proved" means a hand argument written in one session: not machine-checked,
not independently reviewed, novelty unchecked.

### Supporting machinery

| Role in the T programme | Notes |
|---|---|
| Exact length transfer across cuts, used by the decomposition lemma | `three_cut_prime_transfer.md` (3-edge cuts), `boundary_linkage_composition.md` (general cuts), `bridge_prime_reduction.md` (bridges) |
| Gadget windows and the dense-labelling threshold | `partial_triangle_expansion_census.md`, `mixed_gadget_research.md`, `cycle_space_obstruction.md` |
| Rooted primes, the identity-only case of WRP | `prime_pole_obstructions.md`, `root_orbit_switching.md`, `bridge_resilience_potential.md`, `square_strip_minmax.md` |
| Interval sources for the doubling-chain lemma | `switching_spectrum_necessity.md` (switches), `square_strip_minmax.md` (strips) |
| Earlier groundwork from this session | `halving_calculus.md`, `sumset_classification.md`, `richness_findings.md`, `extremal24_findings.md`, `q4_independent_check.md`, `literature_update_2026-11.md`, `expander_brief.md` |

**Known code issue.** `mixed_gadget_solver.make_gadget` writes graph6 in
node-iteration order while storing port labels by sorted order, so a stored
gadget's ports need not match its graph6. Records built from graph6 should
derive ports from the degree-2 vertices, as `audit_clean_poles.py` now does.
The solver itself is unchanged.

**Label ceiling.** Every proof in this directory is a hand argument written and
checked once in a single session. None is machine-checked or reviewed. Treat
each as `PROVED_IN_MARKDOWN`, `NOT_FORMALLY_VERIFIED`, `NOVELTY UNCHECKED`
until reproduced, per the house rule on claims from outside the current session.

## Read in this order

1. `literature_update_2026-11.md` — papers from Aug–Nov 2026 that supersede
   much of the ledger (order ≥ 41; S4, S5, G1 now published by others).
2. `q4_independent_check.md` — `q(G) ≥ 4` confirmed by a shorter route, for
   order ≥ 37.
3. `halving_calculus.md` — one definition covering the known reductions;
   Theorem A (one low-degree vertex forbidden at every scale) and Theorem B
   (the necklace condition).
4. `sumset_classification.md` — Theorem C, the integer side of Theorem B.
5. `richness_findings.md` — why rich path-length sets cannot be the route to
   3-connectivity; the doubling inequality `f(k+1) ≥ 2 f(k)`.
6. `extremal24_findings.md` — the four 24-vertex extremal graphs are triangle
   replacements of small cubic graphs; the truncation formula.
7. `expander_brief.md` — sublinear expanders, written by a subagent from
   fetched summaries; not checked by the main session.

## Negative results (kept, per the ground rules)

- Theorems B and C exclude none of the 12,255 C4-free two-pole pieces on 8–13
  vertices.
- No graph half of a 24-vertex `{4,8}`-free graph can be `{4}`-free with min
  degree 3 (counting), and none of the four is bipartite. Halving does not
  explain the jump from 10 to 24.

## Scripts (`scripts/`)

| file | what it does | needs |
|---|---|---|
| `q4_check.py` | longest clean coloured paths and cyclic words for 1–3 hubs | Python |
| `sumset_check.py` | tests Theorem C on all sets of ≤ 4 integers from 1..14 | Python |
| `cycle_check.c` | independent power-of-two cycle checker for graph6 streams | cc, nauty `geng` |
| `poles.c`, `pieces_analyze.py` | pole-path length sets of small two-pole pieces | cc, `geng`, Python |
| `extremal24.py` | invariants of the four 24-vertex graphs; writes `extremal24_edges.json` | networkx |
| `quotient24.py`, `truncation_check.py` | triangle quotients; truncation formula check | run `extremal24.py` first |

Reproduced in the same session with `cycle_check.c`: order 10 (5,203,110
graphs, 0 survivors), cubic C4-free order 18 (2,761, 0 without a C8) and
order 20 (36,101, 0). The stored DRAT certificate re-verified with drat-trim.

## Known issues found on `main`, not fixed here

- `proof.md` Part VIII and `lemmas.md` "D-lower" still list `D ≥ 2` as open
  while Part I proves `q ≥ 4`; `D` and `q` are the same quantity.
- `make test` fails at collection: `tracks/type-t-c16-static-sat/tests`
  imports a root module of the same name.
- With the floors 56/38/36, the even-order 3-connectivity range should read
  `[17,35]` (now moot given order ≥ 41).

## Research passes added 2026-11-16 (later the same day)

Supplied as a patch after pull request #2 was merged. **These were not written
or reviewed by the audit session above, and their tests were not run when they
were committed.** Each note states its own status; none claims a proof of the
conjecture. Treat every result as CONJECTURAL until reproduced, per the house
rule on claims from outside the current session.

| note | pass | scripts |
|---|---|---|
| `partial_triangle_expansion_census.md` | partial triangle expansion | `partial_triangle_expansion.py`, `census_small_bases.py`, `derive_cubic_12_catalog.py` |
| `mixed_gadget_research.md` | mixed three-port gadgets, 78-vertex family | `mixed_gadget_solver.py`, `mixed_gadget_census.py`, `exoo78_family.py`, `exoo78_witness.py` |
| `cycle_space_obstruction.md` | cycle-space averaging | `cycle_space_obstruction.py` |
| `three_cut_prime_transfer.md` | IV: cyclic three-edge cuts | `three_cut_transfer.py` |
| `prime_pole_obstructions.md` | V: parity-resolved spectra | `prime_pole_obstructions.py` |
| `root_orbit_switching.md` | VI: rooted prime graphs, two-ear switching | `root_orbit_switching.py`, `rooted_hamiltonian_matching.py`, `rooted_hamiltonian_census.cpp` |
| `bridge_prime_reduction.md` | VII: bridge transfer | `bridge_reduction.py` |
| `bridge_resilience_potential.md` | VIII: fractional resilience | `bridge_family_robustness.py`, `fractional_bridge_resilience_lp.py` |
| `square_strip_minmax.md` | IX: square strips | `square_strip_obstruction.py` |
| `boundary_linkage_composition.md` | X: boundary-linkage composition | `boundary_linkage.py` |
| `switching_spectrum_necessity.md` | XI: spectral isolation, switch amplification | `spectral_switching.py` |

Each script has a matching `test_*.py`. To run them:
`python -m pytest -q tracks/2026-11-halving/scripts`. One test compiles
`rooted_hamiltonian_census.cpp` with the local C++ compiler.

## Three-port classification and the additive-reduction brief (2026-11-16, evening)

- `three_port_classification.md` — every clean 3-pole (three degree-2 vertices,
  rest degree 3, no power-of-two cycle) through 21 vertices (certified 16 Nov): only the two H7
  gadgets and H15, plus the triangle. Triangle-built clean pieces stop at 15
  vertices at every size. Matches all pass VI Hamiltonian survivors. States
  Conjecture T. Also corrects an earlier conversational remark about
  Ducoffe–Dumitru's low-degree question.
- `research_brief_additive_reduction.md` — the plan: replace "hit a power of
  two" by "cover a factor-2 interval", reduce to prime graphs labelled by the
  five gadget letters (WRP), then attack dense and sparse labellings.
- Scripts: `triangle_closure.py`, `identify_three_poles.py`; data:
  `clean_three_poles_n_le_21.g6`.

## Corrections and audit (2026-11-16, late evening)

- Brief and classification corrected: T settles **all** cubic graphs; WRP is a
  route to T conditional on the decomposition lemma; the width score is
  additive over disjoint cycles, not linear over the binary cycle space; Step 4
  must sharpen the existing threshold.
- Added `three_pole_census_manifest.md`, `audits/three_pole_research_handoff.md`
  (a separate model's audit, with an erratum), `scripts/audit_clean_poles.py`
  and its output `scripts/clean_pole_small_audit.json`, and
  `scripts/check_three_pole_isomorphisms.py`.

## Pass XII (2026-11-16, night)

- ChatGPT's results, committed as supplied: `tower_theorem.md`,
  `decomposition_lemma.md`, and `pass12/` (verifiers, streams, certification
  manifest, its own status notes).
- Claude's review: `pass12/REVIEW.md`. Its certification rerun matches bit for
  bit; one gap in the tower proof's uniqueness step is closed there.
- Claude's addition: `joint_minimality.md`, closing the bridge and 2-edge-cut
  cases and giving WRP ⇒ T*.
