# Order-30 cubic t=3 census — filter built and validated, catalog generation in progress

## Why this filter is hand-built, not imported

The externally-supplied material referenced a generic
`triangle_quotient_intersection_filter.cpp` for t=1..6, but only its theorem
writeup (`triangle_quotient_intersection_theorem.md`) was actually supplied
in any upload — the source file itself never arrived. Rather than wait or
guess at unavailable code, `src/t3_intersection_filter.cpp` was built by
adapting the already-audited, already-proven-correct `t4_intersection_filter.cpp`
(quotient order 22→24, marks 4→3, C(22,4)=7315→C(24,3)=2024 candidates,
triangle-expansion vertex bookkeeping adjusted accordingly).

## Deriving and validating the t=3 allowed-intersection table

The allowed-`e` table is not copied from anywhere. It was derived from the
same theorem statement already independently verified this session
(`[L+e, L+2e]` avoids `{4,8,16}`, plus the L=3/e=0 strengthening: an
unmarked quotient triangle is always an extra triangle beyond the exactly-t
marked ones). Before trusting this derivation for t=3, **the same derivation
method was run for t=4 and checked against the externally-supplied,
already-audited t=4 table — exact match at all 14 lengths, 0 mismatches**
(see the derivation script's own self-check). Only after that validation was
the method trusted to produce the t=3 table.

Derived t=3 table (`allowed_bits` in the source):

| L | allowed e |
|---:|:---|
| 3 | 2 |
| 4 | 1 |
| 5 | 0, 1 |
| 6 | 0, 3 |
| 7 | 0, 2, 3 |
| 8 | 1, 2, 3 |
| 9 | 0, 1, 2, 3 |
| 10 | 0, 1, 2 |
| 11 | 0, 1, 2 |
| 12 | 0, 1 |
| 13 | 0, 1 |
| 14 | 0, 3 |
| 15 | 0, 2, 3 |
| 16 | 1, 2, 3 |

(Identical to the t=4 table with every occurrence of `e=4` removed — expected,
since the per-length interval computation doesn't depend on t except through
the maximum possible `e`, which is capped at `min(L, t)`.)

## Cross-validation before trusting real compute

Compiled and ran on 500 real order-24 quotients (`nauty-geng -c -C -d3 -D3 24`,
first 500 canonical-order lines) against an independent Python
implementation (`order30_quotient_marking_census.py --n 24 --k 3`, the same
already-validated script used for the t=4 cross-check). Results agreed
exactly: `1,012,000` markings checked (`500 * C(24,3)`), all eliminated, 0
survivors, on both implementations. Measured speed: 0.0084s (C++) vs 25.9s
(Python) on identical input.

## Status

Order-24 catalog generation (`nauty-geng -c -C -d3 -D3 24`) launched and
running. Order-22 (7,187,627 graphs) took ~78 minutes; order-24 is expected
to be substantially larger (the 20→22 step was ~14.4x), so this generation
is expected to take considerably longer — realistically many hours. The
exhaustive t=3 census will run once generation completes, using the same
resumable, hash-manifested runner pattern as the t=4 run.
