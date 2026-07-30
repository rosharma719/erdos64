# Order-30 triangle-quotient census: complete elimination of the 7-marking family

## Status

[COMPUTATIONALLY VERIFIED, EXHAUSTIVE]. Built from scratch this session
(searched every local and remote branch first — see cross-reference below —
found no prior artifact anywhere in the repo).

**Result: every order-30 candidate obtained by expanding 7 disjoint
triangles on a 3-connected cubic 16-vertex quotient contains a C4, C8, or
C16.** This is a complete elimination of the entire family, not a partial
search — all 2,828 quotients, all `C(16,7)=11,440` markings each, all
32,352,320 instances, zero survivors.

## Background (proposed in chat, not previously in the repo)

For a C4-free cubic graph, triangles are vertex-disjoint; contracting each
to a point gives a smaller simple cubic **quotient** `Q`. If `S` is the set
of contracted ("marked") quotient vertices, a quotient cycle of length `l`
through `e = |cycle ∩ S|` marked vertices lifts to *every* length in
`[l+e, l+2e]` (each marked vertex independently contributes 1 or 2 edges on
the lift, depending which two of its three triangle corners the cycle
enters/exits through). A marking is therefore forbidden — forces a C4, C8,
or C16 — iff `l+e <= 2^k <= l+2e` for some `2^k in {4,8,16}`, for *any*
cycle of `Q`. An order-30 graph with exactly 7 disjoint triangles quotients
to a 16-vertex cubic graph with exactly 7 marked vertices.

## Step 1 — generate and verify the 3-connected cubic 16-vertex catalog

`nauty-geng`'s `-C` flag means *bi*connected (2-connected), not
3-connected — there is no direct 3-connectivity flag — so the catalog was
built as `nauty-geng -c -C -d3 -D3 16` (all connected, biconnected, cubic
16-vertex graphs) followed by an exact `networkx.node_connectivity(G)>=3`
filter. Cross-checked against the reported sequence for every even order
4..16 (not just 16):

| n | biconnected cubic total | 3-connected | strictly 2-connected |
|--:|--:|--:|--:|
| 4 | 1 | 1 | 0 |
| 6 | 2 | 2 | 0 |
| 8 | 5 | 4 | 1 |
| 10 | 18 | 14 | 4 |
| 12 | 81 | 57 | 24 |
| 14 | 480 | 341 | 139 |
| 16 | 3,874 | **2,828** | **1,046** |

Every value reproduced exactly (nauty version `2.8.8+ds-5`, Ubuntu package;
`networkx` 3.6.1 for the connectivity filter). Catalog saved at
`data/order30_quotient_census/quotients_16v_3connected.g6.gz`
(sha256 `f02996eefdd152ff520c912efb83ef4194e4703ed41261fd47dd784d970cabe8`),
2,828 lines, one graph6 string per line.

## Step 2 — exact marking census

`verifier/order30_quotient_marking_census.py`: for each of the 2,828
quotients, enumerate every simple cycle (all length <=16, `networkx`,
avg. ~308 cycles/quotient), then for all 11,440 markings simultaneously
(vectorized `numpy` bitmask/popcount, not a per-marking Python loop) test
the interval condition against every cycle. Any marking surviving the
interval test (none did, in this run) would additionally get a **literal**
check: materialize the actual order-30 graph by triangle-expanding the 7
marked vertices (same construction independently validated earlier this
session on the Petersen graph) and run brute-force `simple_cycles`
C4/C8/C16 detection on it.

```
python verifier/order30_quotient_marking_census.py \
    data/order30_quotient_census/quotients_16v_3connected.g6.gz \
    --output data/order30_quotient_census/census_full.json
```

**Run result** (single process, 20.0 seconds, no sharding needed):

```
quotients_processed: 2828
markings_per_quotient: 11440
total_markings_checked: 32352320
total_eliminated_by_interval: 32352320
total_interval_survivors: 0
literal_survivor_count: 0
counterexample_candidates: []
```

Output saved at `data/order30_quotient_census/census_full.json`
(sha256 `888d4f7b8126140c91818e2582ab11a3eeca51598b690d08e41c366d469ffbf4`).

## Correctness cross-check

Because *every* marking was eliminated by the interval test alone (the
literal-check code path never triggered), the interval logic itself needed
independent validation before trusting a 100%-elimination result: 158
random `(quotient, marking)` pairs the interval test called "eliminated"
were separately, literally triangle-expanded and brute-force checked for
C4/C8/C16 — **0/158 mismatches**; every "eliminated" verdict corresponded to
a real forced short/dyadic cycle (sample counts e.g. `C16` in the
hundreds). This is a spot-check, not a proof the interval code is bug-free
on all 32M instances, but 158/158 agreement against an independently-coded
literal detector is strong evidence the exhaustive result is real.

## What this does and does not establish

**Establishes:** no order-30 Erdős–Gyárfás counterexample exists with
exactly 7 vertex-disjoint triangles whose contraction quotient is
3-connected. Combined with the earlier session's targeted radius-six local
search around the two strongest known order-30 near-miss basins
(`(C4,C8,C16)=(4,0,0)` and `(3,1,0)`, >160M reconnections sampled, no
survivor found, but not a completed radius-six certificate — that part was
**not** re-run or found this session and remains as previously reported,
unverified here) — this narrows, but does not close, the order-30 search.

**Does not establish:** anything about quotients that are only
2-connected (the other 1,046 sixteen-vertex quotients — the report
identified the missing edge-insertion augmentation needed to generate them
completely but did not generate or test them, and neither did this
session), quotients of other sizes (18-vertex/6-marked, 20-vertex/5-marked,
etc. per the report's table), or any order other than exactly 30. It also
only tests C4/C8/C16 specifically (sufficient for order 30, since no larger
power of two can fit as a simple cycle length on 30 vertices).

## Cross-reference

Every specific number in the pasted external report about this order-30
family (`1,2,4,14,57,341,2828`; `1,046`; the specific missing-1-at-12,
missing-5-at-14 detail; `11,440`; `32,352,320`) was independently
reproduced from scratch here and matched exactly — despite no corresponding
artifact existing anywhere in this repo's git history (all local and remote
branches checked). The full marking census the report described as not
completing in its pass **did complete here** (20 seconds, not sharded) with
a zero-survivor result.
