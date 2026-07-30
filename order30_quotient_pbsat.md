# Quotient-cycle cardinality-constraint (CP-SAT) solver

## Status

[COMPUTATIONALLY VERIFIED against the exhaustive census, on 250+ quotients].
This is the "replace expansion enumeration with quotient-cycle constraints"
engineering direction — a real, working, validated tool, built and tested
this session, not a design sketch.

## What it does differently from the existing census

The existing `verifier/order30_quotient_marking_census.py` proves a
zero-survivor result by literally generating **every** `C(n,k)` marking of
**every** quotient and checking each one (vectorized, but still
combinatorial in `k`). `verifier/order30_quotient_pbsat.py` instead builds
one Boolean variable per quotient vertex and, for every quotient cycle
`(length l, vertex set V(C))`, a set of small `!=` cardinality constraints
on `e = sum_{v in V(C)} x_v` (excluding exactly the values of `e` for which
the lift interval `[l+e, l+2e]` hits a forbidden power of two), plus
`sum(x_v) == k`. An OR-Tools CP-SAT solver then searches the *marking*
space directly via constraint propagation, never materializing `C(n,k)`
candidates.

## Validation against the exhaustive census

| catalog | k | sample | CP-SAT result | time |
|---|--:|--:|---|--:|
| 16v 3-connected | 7 | 150 | 150/150 UNSAT, 0 SAT, 0 UNKNOWN | 5.2s |
| 18v 3-connected | 6 | 100 | 100/100 UNSAT, 0 SAT, 0 UNKNOWN | 5.7s |

Both match the exhaustive brute-force census exactly (which found 0
survivors on the full 2,828-quotient and 30,468-quotient catalogs
respectively) — no SAT result found where the census says none should
exist, no UNKNOWN (solver timeout/non-convergence) on any sampled instance.
This is the validation step the roadmap explicitly required before trusting
the solver prospectively.

## Why this matters: it doesn't scale with `C(n,k)`

Timing the *same* order-20 quotient at increasing `k` (holding the quotient
fixed, only varying the target mark count):

| `k` | `C(20,k)` | CP-SAT status | CP-SAT solve time |
|--:|--:|---|--:|
| 5 | 15,504 | UNSAT | 0.030s |
| 7 | 77,520 | UNSAT | 0.027s |
| 10 | 184,756 | UNSAT | 0.026s |
| 13 | 77,520 | UNSAT | 0.031s |

`C(20,k)` grows **12x** from `k=5` to `k=10`; CP-SAT's solve time is flat
(constraint count is fixed at ~1,572 regardless of `k`, since it comes from
the quotient's own cycle structure, not the target mark count). The
existing brute-force census's cost scales directly with `C(n,k)` (that's
exactly why order-20 needed sharding across 4 cores for ~50 minutes per
shard while order-16 took 20 seconds single-threaded). This is the concrete
basis for the stopping rule already adopted: **don't extend the brute-force
per-marking pipeline to order 22** (`C(22,4)` is still small, but the real
bottleneck is quotient *count* — order 22 will have on the order of several
million 2-connected cubic quotients, extrapolating the ~10-12x per-order-2
growth already seen 16→18→20 — not the per-quotient marking search).

## What's not yet done

- **Order-22+ generation and a full solver-based census.** Not attempted
  this pass — per the explicit stopping rule, this needs its own
  generation/sharding plan (quotient count alone may be too large to
  materialize as a flat `.g6.gz` file the way orders 16-20 were).
- **UNSAT-core extraction via CP-SAT's own infrastructure.** The existing
  `order30_quotient_unsat_core.py` extracts cores via greedy deletion
  against the brute-force interval test; a CP-SAT-native core (e.g. via
  `AssumptionsAreUnsat`/IIS-style extraction) would likely be faster and is
  a natural next integration, not yet built.
- **`C32` support for the order-32 ladder.** The solver's `forbidden_lengths`
  parameter already accepts `32` (see `FORBIDDEN = (4,8,16,32)` default in
  the module, currently used at `(4,8,16)` for the order-30 sectors) — untested
  against any real order-32 quotient catalog, since none exists yet.
- **Symmetry breaking.** The roadmap calls for "automorphism-aware symmetry
  breaking"; this first version has none (each quotient is solved
  independently, and no per-quotient automorphism group is computed or
  exploited). Not needed yet since even without it every tested instance
  solves in well under a second, but would matter for a much larger single
  quotient or a more constrained (larger `k`) search.
