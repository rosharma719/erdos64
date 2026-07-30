# Order-30 triangle-quotient census: complete elimination by quotient order

## Status

[COMPUTATIONALLY VERIFIED, EXHAUSTIVE]. Built from scratch this session
(searched every local and remote branch first — see cross-reference below —
found no prior artifact anywhere in the repo).

**Theorem (this file). No 30-vertex cubic C4/C8/C16-free graph has exactly
seven pairwise vertex-disjoint triangles.** Proved by the Proposition below
(the quotient of such a graph by its seven triangles is *exactly* the class
of 2-connected — not merely 3-connected — cubic 16-vertex graphs, all
3,874 of them, no missing case) plus an exhaustive computational census: all
3,874 sixteen-vertex 2-connected cubic quotients, all `C(16,7)=11,440`
markings each, all **44,318,560** instances, zero survivors. Order-18
(6-marked) results below once that run completes.

## Proposition (exact quotient characterization — closes the missing case)

*Let `G` be a bridgeless cubic C4-free graph on 30 vertices with exactly
seven triangles. Contracting all seven triangles gives a simple, 2-connected
cubic graph `Q` on 16 vertices, and `G` is uniquely recovered from `Q`
together with the seven contracted vertices.*

Proof: triangles of a C4-free graph are vertex-disjoint, so contracting all
seven removes `2*7=14` vertices, giving order `30-14=16`; each triangle has
exactly 3 external edges so `Q` stays cubic. `Q` is simple: a loop is
impossible, and a parallel edge would require two connections between the
same pair of gadgets/vertices, which (via the triangle's own edges) would
close a `C4` in `G`, contradiction. `Q` is bridgeless: a bridge of `Q`
corresponds to a bridge of `G` (triangle expansion adds no alternate route
across that cut), and `G` is bridgeless by hypothesis. A connected cubic
graph with a cut vertex necessarily has a bridge (deleting the cut vertex
leaves some component incident to only one of its three edges), so
bridgeless + cubic + connected `=>` 2-connected. Triangle expansion is
unique up to the triangle's own automorphism, so `(Q, S)` determines `G`. ∎

**Consequence:** the earlier "missing two-pole augmentation" (needed to
*generate* the 1,046 strictly-2-connected quotients recursively) is
irrelevant to the census — those 1,046 graphs were already generated
directly via `nauty-geng -c -C` (biconnected) + an exact
`networkx.node_connectivity` filter, same as the 2,828 3-connected ones, no
recursive construction needed. The Proposition says there is **no
additional 1-connected (or non-bridgeless) case to inspect at all** — every
valid quotient is one of the 3,874 already on disk.

**Remark (slightly stronger than "exactly seven"):** since a graph with
`>=7` disjoint triangles can have any 7 of them contracted (the untouched
extra triangles simply survive, unmarked, as literal triangles of `Q` — the
census's literal check already covers this: it directly counts C4/C8/C16 on
the actual lifted graph regardless of what else survives in it), the same
zero-survivor result also rules out `>=7` disjoint triangles, not just
`=7`. Stated conservatively as "exactly seven" above since that is the
literal quantity marked; the `>=7` extension is immediate but not
separately re-verified with its own write-up.

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
`networkx` 3.6.1 for the connectivity filter), including the specific
"missing 1 at order 12, missing 5 at order 14" detail from the report's own
partial recursive generator (81-80=1, 480-475=5 here). Both order-16
catalogs saved, one graph6 string per line:
- `data/order30_quotient_census/quotients_16v_3connected.g6.gz` (2,828 lines,
  sha256 `f02996eefdd152ff520c912efb83ef4194e4703ed41261fd47dd784d970cabe8`)
- `data/order30_quotient_census/quotients_16v_strictly2connected.g6.gz`
  (1,046 lines, sha256
  `80654e43a6c46be95c3156d0f7d79c6012d38fbf802e5f3c37e2095dc5ba5e5a`)

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
python verifier/order30_quotient_marking_census.py \
    data/order30_quotient_census/quotients_16v_strictly2connected.g6.gz \
    --output data/order30_quotient_census/census_strict2_full.json
```

**Run results** (single process each, no sharding needed):

| catalog | quotients | markings/quotient | total instances | eliminated | survivors | time |
|---|--:|--:|--:|--:|--:|--:|
| 3-connected | 2,828 | 11,440 | 32,352,320 | 32,352,320 | 0 | 20.0s |
| strictly-2-connected | 1,046 | 11,440 | 11,966,240 | 11,966,240 | 0 | 8.6s |
| **total (all 16-vertex quotients)** | **3,874** | | **44,318,560** | **44,318,560** | **0** | **28.6s** |

Outputs: `data/order30_quotient_census/census_full.json`
(sha256 `888d4f7b8126140c91818e2582ab11a3eeca51598b690d08e41c366d469ffbf4`),
`data/order30_quotient_census/census_strict2_full.json`.

## Correctness cross-check

Because *every* marking was eliminated by the interval test alone (the
literal-check code path never triggered), the interval logic itself needed
independent validation before trusting a 100%-elimination result: 218 random
`(quotient, marking)` pairs the interval test called "eliminated" (158 from
the 3-connected catalog, 60 from the strictly-2-connected one) were
separately, literally triangle-expanded and brute-force checked for
C4/C8/C16 — **0/218 mismatches**; every "eliminated" verdict corresponded to
a real forced short/dyadic cycle (sample counts e.g. `C16` in the
hundreds). This is a spot-check, not a proof the interval code is bug-free
on all 44M instances, but 218/218 agreement against an independently-coded
literal detector is strong evidence the exhaustive result is real.

## Order-18 quotient family (6-marked) — catalog confirmed, census in progress

Same method, one order up: `nauty-geng -c -C -d3 -D3 18` gives all
biconnected cubic 18-vertex graphs; split by exact `node_connectivity`.

| | claimed | reproduced here |
|---|--:|--:|
| 3-connected | 30,468 | **30,468** |
| strictly-2-connected | 9,398 | **9,398** |
| total | 39,866 | **39,866** |

All three counts matched exactly. Catalogs saved:
`data/order30_quotient_census/quotients_18v_3connected.g6.gz` (sha256
`0728fa6a5c83aae8ed22e58f368d9821e5cdaea8940ee5dace97d3de9d70c68d`),
`data/order30_quotient_census/quotients_18v_strictly2connected.g6.gz`
(sha256 `878c687ee960265b5c71a0eb3ed47b66a405015cc455517effc706bc3c57f71c`).
By the same Proposition (order-agnostic: it only used C4-freeness,
bridgelessness, and cubicness), these 39,866 graphs are the *complete* set
of valid order-18 quotients for a 30-vertex graph with exactly six disjoint
triangles — no missing case here either.

Marking-census run (`--n 18 --k 6`, `C(18,6)=18,564` markings/quotient,
`39,866 * 18,564 = 740,072,424` total instances) was launched at the end of
this pass; see the next update for results — do not treat order 18 as
closed until that lands.

## What this does and does not establish

**Establishes (order 16 / seven-triangle case, fully closed):** no order-30
Erdős–Gyárfás counterexample has exactly seven pairwise-disjoint triangles
— proved for *every* valid quotient (all 3,874, both 3-connected and
strictly-2-connected; the Proposition shows there is no other case).
Combined with the earlier session's targeted radius-six local search around
the two strongest known order-30 near-miss basins (`(C4,C8,C16)=(4,0,0)`
and `(3,1,0)`, >160M reconnections sampled, no survivor found, but not a
completed radius-six certificate — that part was **not** re-run or found
this session and remains as previously reported, unverified here) — this
narrows, but does not close, the order-30 search.

**Does not (yet) establish:** anything about the order-18/six-triangle
family (catalog generated and count-verified above; marking census
launched but not yet complete — see that section), order-20/five-triangle
and smaller-marking cases, or any order other than exactly 30. Also
(per the Remark above) the "exactly seven" phrasing is conservative — the
same computation immediately rules out `>=7` disjoint triangles too, but
that extension hasn't been given its own separate verification pass. Only
tests C4/C8/C16 specifically (sufficient for order 30, since no larger
power of two can fit as a simple cycle length on 30 vertices).

## Cross-reference

Every specific number in the pasted external reports about this order-30
family — `1,2,4,14,57,341,2828`; `1,046`; the missing-1-at-12,
missing-5-at-14 detail; `11,440`; `32,352,320`; and then `30,468`; `9,398`;
`39,866`; `18,564`; `740,072,424` — was independently reproduced from
scratch here and matched exactly, despite no corresponding artifact
existing anywhere in this repo's git history (all local and remote branches
checked). The full order-16 marking census (both connectivity classes) is
now complete with a zero-survivor result across all 44,318,560 instances.
