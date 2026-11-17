# Clean k-pole census: what was run, and what was not

**Scope.** Every connected simple graph on `N` vertices with degrees 2 and 3
only, no 4-cycle, and exactly `k` vertices of degree 2, for `k = 3` and
`k = 2`. Each is tested for cycles of length 8 and 16 (32 cannot occur for
`N ≤ 31`). A graph passing every test is a **clean k-pole**.

## Method (certified, 16 November 2026)

Each row was produced by `scripts/certify_pole_shard.sh N E RES MOD OUTDIR LABEL`:

```
geng -c -f -d2 -D3 N E:E RES/MOD
```

`-c` connected, `-f` no 4-cycle, `-d2 -D3` degrees 2 to 3. With `E` edges the
degree sum fixes the number of degree-2 vertices at `3N − 2E`, so
`E = (3N − 3)/2` for 3-poles and `E = (3N − 2)/2` for 2-poles.

The stream is SHA-256 checksummed and fed simultaneously to two independent
checkers:

- **A:** `scripts/cycle_check.c` (DFS, written for the audit of 16 November);
  reports graphs with no power-of-two cycle up to `N`.
- **B:** `verifier/check_power_masks.c` (the repo's own checker); reports
  C4/C8/C16 presence masks.

A shard passes only if `geng`, `tee` and checker A exit 0; `geng`'s own count,
A's count and B's count are equal; no 4-cycle was seen; and A and B report the
same number of clean graphs. **Every shard below passed.** One JSON manifest per
shard is in `census/`: command, nauty version string, checker source
checksums, start and end times, exit codes, the three counts, stream checksum,
and checksum of the clean-graph list.

Tools: nauty `geng` 2.8.8 (built from the pynauty 2.8.8.1 source
distribution); two cores.

**Limit.** The checkers are independent, but the generator is not: every row
relies on `geng` alone for completeness. An independent generator is
blueprint node E5.

## Clean 3-poles

| N | E | graphs | clean (A = B) | shards | stream SHA-256 (first 12) |
|---:|---:|---:|---:|---:|---|
| 7 | 9 | 2 | **2** | 1 | `59c3c4b15892` |
| 9 | 12 | 10 | 0 | 1 | `87ab765d5d98` |
| 11 | 15 | 57 | 0 | 1 | `9b393fe016fb` |
| 13 | 18 | 525 | 0 | 1 | `3af9724eb023` |
| 15 | 21 | 5,775 | **1** | 1 | `347109554f82` |
| 17 | 24 | 75,524 | 0 | 1 | `8027631d456a` |
| 19 | 27 | 1,124,269 | 0 | 1 | `ac1a3fb23646` |
| 21 | 30 | 18,580,327 | 0 | 2 | `f45cde2101c1`, `3f16c4038f9f` |

The order-21 run took about 12 minutes of wall time on two cores.

The three clean graphs are in `scripts/clean_three_poles_n_le_21.g6`. The
certified run's clean-graph lists are byte-identical to that file. They are
uniform H7 and skew H7 (`N = 7`) and H15 (`N = 15`); see
`three_port_classification.md`.

**Small orders.** `N = 3` is the triangle. `N = 5`: no clean 3-pole (hand
proof and brute force over all 70 candidates,
`audits/three_pole_research_handoff.md`).

**What this establishes** [CERTIFIED for checkers, single generator]. The
clean 3-poles on at most 21 vertices are exactly the triangle, uniform H7,
skew H7 and H15. Uniqueness at 7 and 15 vertices rests on this census, not on
the pass VI Hamiltonian cross-check, which only identifies the rooted
survivors of that census with these poles.

## Clean 2-poles

| N | E | graphs | clean (A = B) | stream SHA-256 (first 12) |
|---:|---:|---:|---:|---|
| 4 | 5 | 0 | 0 | (empty stream) |
| 6 | 8 | 0 | 0 | (empty stream) |
| 8 | 11 | 1 | 0 | `a65560dd95e0` |
| 10 | 14 | 11 | 0 | `81186ae869d0` |
| 12 | 17 | 75 | 0 | `4c87d661cd8b` |
| 14 | 20 | 677 | 0 | `6680cd96c041` |
| 16 | 23 | 7,639 | 0 | `c0eef0e333fc` |
| 18 | 26 | 101,546 | 0 | `708cb05b6d8a` |
| 20 | 29 | 1,533,261 | 0 | `19f7c62c2766` |

**What this establishes** [CERTIFIED for checkers, single generator]. There is
no clean 2-pole on at most 20 vertices. This bears on case D1b of the
decomposition lemma (`BLUEPRINT.md`) but cannot close it: that case needs an
argument for every size.

## Not run

| Run | Estimated cost | Why it matters |
|---|---|---|
| 3-poles, `N = 23` | about 3.3 hours of wall time on two cores (about 16 times the order-21 run) | The cheapest test that could refute T |
| 2-poles, `N = 22` | about 20 minutes on two cores | Extends E4 |

An earlier order-21 attempt, started before this method existed and stopped by
request, produced no result and is superseded by the certified row above.

## Reproduce

```sh
export PATH=/path/to/nauty:$PATH
O=census_out
for N in 7 9 11 13 15 17 19; do scripts/certify_pole_shard.sh $N $(( (3*N-3)/2 )) 0 1 $O three; done
scripts/certify_pole_shard.sh 21 30 0 2 $O three & scripts/certify_pole_shard.sh 21 30 1 2 $O three & wait
for N in 4 6 8 10 12 14 16 18 20; do scripts/certify_pole_shard.sh $N $(( (3*N-2)/2 )) 0 1 $O two; done
python3 scripts/identify_three_poles.py scripts/clean_three_poles_n_le_21.g6
python3 scripts/check_three_pole_isomorphisms.py
```
