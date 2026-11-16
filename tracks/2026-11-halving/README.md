# tracks/2026-11-halving — session of 2026-11-16

Independent audit of the repository plus one new line of work. Nothing here
edits the canonical ledger files other than one status-log entry in `plan.md`.

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
