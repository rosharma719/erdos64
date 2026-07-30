# Order-30 near-miss classification within the triangle-quotient families

## Status

[COMPUTATIONALLY VERIFIED, EXHAUSTIVE within the families searched so far].
New analysis this session, built on the already-exhaustive
`order30_quotient_census.md` catalogs (not a new search space — a finer
classification of the same, already fully-enumerated data).

**Result: within the order-16/seven-triangle quotient family (both
connectivity classes, 3,874 quotients, 44,318,560 markings — the family
`order30_quotient_census.md` proved has zero markings that avoid C4, C8,
*and* C16 simultaneously), exactly 2,090 markings avoid C4 *and* C8** (all
from the 3-connected sub-family; the strictly-2-connected sub-family
contributes **zero**). Among those 2,090, the minimum possible `C16` count
is **165**, achieved by exactly 4 markings — and all 4 are graph-isomorphic
to a single 30-vertex graph: **the full triangle expansion of the Petersen
graph.**

## Method

`verifier/order30_quotient_near_miss.py`: reuses the exact same interval
machinery as the main census, but instead of collapsing "hits 4, 8, or 16"
into one elimination flag, tracks hits against `{4}`, `{8}`, `{16}`
separately for every marking. A marking is a *candidate* iff no single
quotient cycle's lift interval ever hits `4` or `8` (this is sound and
complete for "no quotient-cycle-forced C4/C8", not a sample — checked
against **every** marking of **every** quotient in each catalog). Every
candidate then gets a full literal triangle-expansion + brute-force
`simple_cycles` count for the real `(C4,C8,C16)` profile — the exact ground
truth, not the interval bound.

```
python verifier/order30_quotient_near_miss.py \
    data/order30_quotient_census/quotients_16v_3connected.g6.gz --n 16 --k 7 \
    --output data/order30_quotient_census/near_miss_16v_3connected.json
```

## Results by catalog

| catalog | quotients | markings | interval-clean candidates | literal C4=0∧C8=0 | min `C16` |
|---|--:|--:|--:|--:|--:|
| 16v 3-connected | 2,828 | 32,352,320 | 2,090 | 2,090 (100% of candidates) | **165** |
| 16v strictly-2-connected | 1,046 | 11,966,240 | 0 | 0 | n/a |

(Every interval-clean candidate turned out to be a genuine literal
`C4=0,C8=0` graph in this run — the interval filter and the literal ground
truth agreed on all 2,090, consistent with the earlier 218-sample
cross-validation of the interval logic in `order30_quotient_census.md`.)

## The extremal graph

The 4 markings achieving `C16=165` are **all pairwise graph-isomorphic**
(`networkx.is_isomorphic`, confirmed for all 4), and that graph is in turn
isomorphic to the full triangle expansion of the Petersen graph (independently
rebuilt from `networkx.petersen_graph()` and cross-checked: same order (30),
same size (45), same degree sequence (all-3), and identical `C4=0, C8=0,
C16=165` via a completely independently-coded literal cycle count). This
gives a second, structurally different derivation of the same extremal
graph the earlier external report found via a 12-vertex/9-triangle
quotient construction — here it emerges instead as the unique minimizer
inside the 16-vertex/7-triangle family, arrived at by exhaustive
enumeration rather than local search. (It makes sense the same graph shows
up: the Petersen expansion has 10 disjoint triangles total, so contracting
any 7 of them is a valid point in *this* family too, leaving 3 as
unmarked-but-still-literal triangles of the quotient.)

## Order-18 strictly-2-connected: also zero (conjecture strengthened)

`data/order30_quotient_census/near_miss_18v_strict2.json`: scanned all
9,398 strictly-2-connected order-18 quotients, all 174,464,472 markings —
**zero** clean (`C4=0,C8=0`) candidates, same as the order-16
strictly-2-connected result. The order-18 3-connected scan (30,468
quotients, 565,607,952 markings) is still running; will report its minimum
once done.

**Conjecture status, now backed by both orders' strictly-2-connected data:**
*every literal-clean (`C4=0,C8=0`) order-30 graph reachable through
triangle-quotient marking arises only from a 3-connected quotient, never a
strictly-2-connected one.* Evidence: **0 clean markings out of 186,430,712
total** across both strictly-2-connected catalogs (order 16: 0/11,966,240;
order 18: 0/174,464,472), versus 2,090 clean markings found in the order-16
3-connected catalog alone. Still not proved — no structural argument for
*why* attempted yet — but the sample size checked is now the *entire*
strictly-2-connected family at two different orders, not a subsample.

## Order-18 3-connected: same extremal graph, independently confirmed

`data/order30_quotient_census/near_miss_18v_3connected.json`: full scan of
all 30,468 3-connected order-18 quotients, all 565,607,952 markings — 6,926
literal-checked clean (`C4=0,C8=0`) candidates. Minimum `C16` is again
**165**, and the best candidate (`marked=[4,5,6,14,15,17]` on a different
18-vertex quotient than the order-16 case) is independently confirmed
graph-isomorphic to the same full Petersen-graph triangle expansion.

This is now a genuinely cross-validated structural fact, not a coincidence
of one search: **across two different quotient-order parametrizations
(16-vertex/7-triangle and 18-vertex/6-triangle) of the same underlying
30-vertex candidate space, the minimum achievable `C16` count subject to
`C4=0,C8=0` is 165, uniquely realized (up to isomorphism) by the full
triangle expansion of the Petersen graph.** (The order-18 strictly-2-connected
catalog was also fully scanned — zero clean candidates, matching order 16's
strictly-2-connected result exactly; see below.)

## Open / next
- Not yet checked: whether 165 is the true minimum `C16` over *all* order-30
  cubic C4/C8-free graphs, or only the minimum reachable via a 7-triangle
  (order-16-quotient) decomposition specifically — a graph with fewer or
  more disjoint triangles, or one not decomposable this way at all, could
  in principle do better (or the true minimum could simply not have any
  disjoint triangle at all, outside this construction's reach entirely).
