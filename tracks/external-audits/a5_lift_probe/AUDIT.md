# A5-permutation-lift counterexample attempt — audit and independent extension

**Source:** externally supplied (Codex) C++ tools (`a5_breakout_solver_v2.cpp`,
`a5_point_repair_k3.cpp`, `s5_parity_breakout.cpp`) plus a hand-derived
16-cut constraint file, reporting a serious but ultimately rejected
120-vertex cubic candidate (a 5-sheeted A5-permutation lift of the 24-vertex
Markström near-counterexample) — rejected because the literal graph
contained a C8.

## What this is

A voltage-graph / permutation-lift construction: take a 24-vertex cubic
base graph B with no C4/C8 and only C16 present (a known near-miss to the
conjecture, per this project's own `literature.md` L13), assign each
"cotree" edge (13 of them, after fixing a spanning tree) a permutation from
A5 (60 even permutations of 5 points), and lift to a 120-vertex graph (5
sheets per base vertex). A base cycle of length L whose monodromy is a
5-cycle lifts to a single 5L-cycle instead of five separate L-cycles — the
standard mechanism for eliminating a specific cycle length via a lift. This
is a real, legitimate technique (listed as counterexample mechanism #3 in
this project's own `plan.md`), not fabricated.

## Independent verification performed

- Confirmed `base0_markstroem` (and the three siblings `base1/2/3_hss`,
  also referenced in the report as "the four 24-vertex near-misses") are
  genuinely cubic, C4-free, C8-free, C16-present, using our own trusted
  `cycle_detect.py` — independent of anything in the upload.
- Wrote `lift_lib.py`, an independent from-scratch Python reimplementation
  of the C++ solver's spanning-tree/cotree bookkeeping and lift
  construction, and verified it reproduces the *exact* cotree edge list and
  ordering the compiled C++ solver uses internally, for every base tested
  (not assumed — checked byte-for-byte against actual solver output each
  time).
- Every "clean" or "violation" verdict in this investigation was checked
  against our own trusted `cycle_detect.py` on the literally materialized
  120-vertex graph — never taken from the constraint solver's own internal
  bookkeeping.

## What was found

The manual (Codex) process was reactive: solve, find one bad cycle in the
literal lift, hand-derive one cut, repeat. `auto_repair.py` automates and
extends this: solve → audit the *entire* literal lift for every forbidden
length 4/8/16/32/64 in one pass → derive and add a cut for *every*
violation found → warm-start and re-solve. When pure random-restart local
search exhausted (4 independent seeds, up to 900s each), an exhaustive
3-variable repair (`a5_point_repair_k3`: all C(13,3)=286 variable triples ×
60³ value combinations ≈ 62M checks per attempt) was tried as an automatic
fallback.

Result across all four available base graphs:

| base | outcome |
|---|---|
| `base0_markstroem` | wall at **26 cuts** — both random-restart and exhaustive k3-repair failed |
| `base1_hss` | could not satisfy even the *initial* constraint (monodromy of every simple base 16-cycle must be a 5-cycle) — 4×900s random restarts, no k3-repair possible (no near-solution to repair from) |
| `base2_hss` | wall at **9 cuts** — k3-repair broke through one earlier 7-cut wall, but a second wall at 9 cuts resisted both methods |
| `base3_hss` | wall at **9 cuts** — same signature as base2, both methods exhausted |

Two independent bases (`base2_hss`, `base3_hss`) converged to the exact
same wall depth (9 cuts) via completely independent random search paths.
Combined with the Codex report's own independently-discovered wall at 16
cuts on `base0_markstroem` (a different specific stuck point, but the same
qualitative failure mode), this is convergent evidence — not a fluke of one
run — that the 5-sheet A5-lift of these four specific near-miss bases is
very likely either infeasible or well beyond what local-search + bounded
exhaustive repair can find.

## What would be needed to go further

None of this rules out a counterexample via voltage lifts in general —
only via this exact combination (these 4 bases, A5, 5 sheets, these two
search techniques). Genuinely new leverage would need one of:
- A complete (not reactive) constraint derivation — proactively enumerating
  *all* base closed walks of length ≤8 (tractable: ≤3^8 per vertex) rather
  than discovering them one violation at a time. Attempted in reasoning
  but not implemented this session; nontrivial because avoiding a lift
  cycle requires more than "monodromy doesn't fix a point" once
  non-simple base walks and sheet-collision conditions are considered.
- A real SAT/CP-SAT/ILP formulation instead of local search, which could
  exhaustively resolve or refute feasibility of the full constraint system
  rather than getting stuck in local-search plateaus.
- A larger group (S5, A6, S6, ...) or more sheets, trading a larger search
  space for more degrees of freedom — the `s5_parity_breakout.cpp` tool
  from the same upload was tried by Codex and also did not reach
  feasibility (12 violated constraints on the Markström base, 4 on a
  second base, per the original report).
- A different base graph outside this specific 4-graph family.

None of these were pursued further this session given the convergent
negative signal and the availability of a more rigorous, exhaustive
alternative (the order-30 triangle-quotient census, still running).
