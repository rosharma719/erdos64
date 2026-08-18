# Order-30 cubic t=4 census — closed, zero survivors (COMPUTATIONALLY VERIFIED)

**Source:** externally supplied (Codex) C++ filter (`t4_intersection_filter.cpp`)
implementing the same exact triangle-quotient interval theorem already in use
in this project's own `order30_quotient_marking_census.py`, claimed to be
24-42x faster via a specialized allowed-intersection bitmask table and a
high-yield cycle-length processing order. Independently audited and then run
to completion on the real, already-generated 7,187,627-graph order-22
biconnected catalog.

## Independent verification performed before trusting this for real compute

1. **Theorem cross-check.** The supplied `triangle_quotient_intersection_theorem.md`
   states exactly the same exact-interval theorem I independently derived and
   hand-verified earlier this session (each of the `e` marked vertices on a
   quotient cycle independently contributes a 1-or-2-edge detour on
   expansion, so cycle lengths lift to the *exact* interval `[L+e, L+2e]`,
   not merely a bound) — confirmed against our trusted `cycle_detect.py` on
   251 markings across 6 small graphs (K4, K33, Petersen, triangular prism),
   0 mismatches, prior to this handoff.
2. **allowed_bits() table cross-check.** The C++ filter's per-length allowed-`e`
   bitmask table (used to prune candidate markings) matches the theorem
   document's printed table exactly (checked by hand, length by length).
3. **Independent cross-validation on real data.** Ran our own
   `order30_quotient_marking_census.py` (a completely independent Python
   implementation of the same theorem, written and validated earlier this
   session, before this handoff existed) on the same 500-quotient sample
   drawn from our actual catalog. Results agreed exactly:
   `total_markings_checked=3,657,500`, `total_eliminated=3,657,500`,
   `0 survivors` — matching the C++ filter's `initial_markings=3,657,500`,
   `final_markings=0` on the identical input, byte for byte in every
   aggregate field. Two independently-written implementations (different
   language, different cycle-enumeration order, different data structures)
   agreeing exactly is strong evidence of correctness.
4. **Speed confirmed genuine, not fabricated.** 500 quotients: 0.057s (C++)
   vs 19.5s (our Python) — real ~340x speedup, in the same ballpark as (and
   exceeding) the claimed 24-42x, measured independently on our own hardware
   and our own real catalog data, not taken from the supplied benchmark
   numbers.

## The complete run

```
./src/run_t4_catalog_intersection.sh \
  .../order22/quotients_22v_all.g6 results/t4_full_intersection 100000 4
```

against the real, previously-generated (this session, via `nauty-geng -c -C
-d3 -D3 22`) catalog of all 7,187,627 biconnected cubic 22-vertex graphs.

**Result** (`results/t4_full_intersection/aggregate.json`):

| field | value |
|---|---|
| input SHA-256 | `ede3aee56297a18e5c9ba994e19e4314491235223c5953f7b0284f45a8c187b7` (verified against the actual catalog file on disk) |
| input lines | 7,187,627 |
| lines processed | 7,187,627 (`complete: true`) |
| cubic order-22, connected | 7,187,627 / 7,187,627 |
| initial markings | 52,577,491,505 (= 7,187,627 × C(22,4) = 7,187,627 × 7,315, exact) |
| candidate intersection tests | 158,383,876,992 |
| final markings (post-filter survivors) | **0** |
| literal checks performed | 0 (none needed — no quotient had any surviving marking) |
| literal/theorem mismatches | **0** |
| counterexamples found | **0** |
| wall time | 1,065.5s aggregate across 4 parallel chunks (4m30s wall clock) |

Every one of the 72 chunk results carries its own input hash and exit
status; the aggregator requires `lines == input_lines` and
`literal_mismatch == 0` to mark the run `complete` — both satisfied.

## What this proves

**No order-30 cubic Erdős–Gyárfás counterexample has exactly four disjoint
triangles.** Combined with the already-established (prior session,
`order30_quotient_census.md`) exhaustive closures of the t=7, t=6, and t=5
cases (orders 16/18/20 quotients, ~8.5B instances, zero survivors) and the
project's `>=t` corollary (closing t=k rules out every t>=k, since a
counterexample with more triangles than the closed case would already have
been caught at a smaller marked set — see that file's exact argument), this
result **strengthens the standing bound from "at most 4 triangles" to "at
most 3 triangles."**

## What remains open

The t=0, 1, 2, 3 cases (quotient orders 30, 28, 26, 24 respectively) are not
addressed by this run and remain open. t=3 (order-24 quotients) is the
immediate next target; per the same supplied material, a generic version of
this filter (`triangle_quotient_intersection_filter.cpp`) is designed for
this but was NOT included in what was verified this session — it would need
the same independent audit (theorem cross-check, allowed-table check,
small-sample cross-validation against an independent implementation) before
being trusted with real compute, exactly as done here for t=4.

The large `random_cubic_g6*` sampling results in the supplied material
(claiming "1,000,000 connected cubic graphs" sampled and filtered) are
**not** exhaustive nonisomorphic catalogs (acknowledged as such in the
source material itself: "a uniform labeled sample, not a nonisomorphic
census") and are not treated as part of this certified result — only the
complete, hash-verified, full catalog run above is.
