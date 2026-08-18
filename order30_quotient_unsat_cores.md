# UNSAT-core mining: compressing the order-16 census into recurring obstructions

## Status

[COMPUTATIONALLY VERIFIED on a 600-quotient sample]. Prototype for the
proposed "quotient-cycle UNSAT-core mining" direction — not a new
computation, a compression of what `order30_quotient_census.md` already
exhaustively proved.

## Method

`verifier/order30_quotient_unsat_core.py`: for a quotient `Q` and marking
size `k`, the full cycle list is already known to be "UNSAT" — no `k`-subset
of `V(Q)` avoids every cycle's forbidden lift interval (that's exactly what
the order-16/18 census proved, one marking at a time). This extracts a
much smaller **irreducible** subset via greedy deletion: repeatedly try
dropping a cycle (longest first), keep it dropped if the remaining set is
*still* UNSAT over all `C(n,k)` markings (checked with the same vectorized
interval test as the main census, so this is exact, not heuristic pruning —
every claimed core really is independently UNSAT on its own, re-verified by
the same machinery that proved the full census).

## Result (600 random quotients, order-16 3-connected catalog, k=7)

- Core sizes range **3–11** (mean 5.77) — out of ~250–360 cycles per
  quotient. A ~50x average compression from "every cycle of Q" down to a
  handful that already force elimination on their own.
- 182 distinct length-signatures across 600 quotients — **not** a single
  universal obstruction, but a real head-heavy distribution, not a flat
  one:

| length signature | count / 600 | share |
|---|--:|--:|
| `4,4,6` | 49 | 8.2% |
| `4,4,4,4` | 38 | 6.3% |
| `3,4,4,5,5,5` | 32 | 5.3% |
| `4,4,4,5` | 24 | 4.0% |
| `4,4,4,4,4` | 20 | 3.3% |

Top 5 signatures alone cover 163/600 (27%) of quotients. Full histogram
and top-20 signatures with example graph6 strings in
`data/order30_quotient_census/unsat_cores_16v_3connected.json`.

## Interpretation

Four of the top 5 signatures are made **entirely of short cycles (3–6)**,
dominated by 4-cycles — consistent with the earlier-established fact that
quotient `C4`s are maximally restrictive (exactly one marked vertex allowed,
per the interval rule `[4+e,4+2e]` hitting 4 unless `e=1`, hitting 8 unless
`e<2`). A cluster of ~4 quotient-`C4`s sharing overlapping vertex sets is
apparently often, by itself, enough to make no 7-marking possible — before
any of the ~250+ longer cycles are even needed.

**This is evidence for, not yet a proof of, a genuine human lemma**: something
like "a 16-vertex cubic quotient with `>=4` (or some small number of)
pairwise-overlapping short cycles in a specific configuration cannot be
7-marked safely, and every quotient in the catalog has such a
configuration" would explain the whole family's elimination structurally,
rather than by exhaustive search. Not established here — the 182 distinct
signatures show the *exact* pattern varies quotient to quotient; extracting
the actual shared combinatorial structure (not just the length multiset)
across the top clusters is the next step, not yet done.

## Honest scope

- Sample of 600 out of 2,828 3-connected order-16 quotients (not
  exhaustive — a full-catalog run would take a few more minutes and is a
  natural follow-up, not done in this pass since the sample already shows
  the qualitative picture: small, non-monolithic cores).
- Strictly-2-connected order-16, and either order-18 catalog, not yet
  cored — worth doing given the near-miss analysis already found a
  connectivity-class asymmetry (`order30_near_miss_classification.md`).
- The greedy-deletion order (longest cycles dropped first) biases toward
  *short*-cycle-heavy cores; a different deletion order could in principle
  find different (not necessarily smaller) irreducible cores for the same
  quotient — "a minimal core" was found, not verified to be *the* smallest
  possible one (minimum hitting set / MUS is NP-hard in general; greedy
  deletion gives *a* minimal, i.e. locally-irreducible, core, not
  necessarily *the* minimum one).
