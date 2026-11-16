# Clean 3-pole census: what was run, and what was not

**Scope.** Every connected simple graph with exactly three vertices of degree 2,
all others of degree 3, and no 4-cycle, on `N` vertices. Each is tested for
cycles of length 8 and 16 (and 32 where `N ≥ 32`, which does not arise here).
A graph passing every test is a *clean 3-pole*.

**Tools.** nauty `geng` 2.8.8 (built from the pynauty 2.8.8.1 source
distribution) and `scripts/cycle_check.c` (independent DFS checker written for
the audit of 16 November 2026). One core.

**Command, for each odd `N`, with `E = (3N − 3)/2`:**

```sh
geng -q -c -f -d2 -D3 N E:E | ./cycle_check 2> clean_N.g6
```

`-c` connected, `-f` no 4-cycle, `-d2 -D3` degrees 2 to 3. With `E` edges the
degree sum forces exactly three degree-2 vertices.

## Completed runs

| N | E | graphs generated | no C4, no C8 | clean | time |
|---:|---:|---:|---:|---:|---:|
| 7 | 9 | 2 | 2 | 2 | < 1 s |
| 9 | 12 | 10 | 0 | 0 | < 1 s |
| 11 | 15 | 57 | 0 | 0 | < 1 s |
| 13 | 18 | 525 | 0 | 0 | < 1 s |
| 15 | 21 | 5,775 | 1 | 1 | < 1 s |
| 17 | 24 | 75,524 | 6 | 0 | 3 s |
| 19 | 27 | 1,124,269 | 38 | 0 | 51 s |

The "graphs generated" column is the number of graphs `cycle_check` read.
`geng` exit codes and stream checksums were not recorded, so these runs fall
short of the repo's certification gate (`plan.md`); rerun with
`verifier/certify_shard.sh`-style manifests before relying on them. The clean graphs are in
`scripts/clean_three_poles_n_le_19.g6`, one per line, in order of `N`.

**Small orders not covered by `geng` here.** `N = 3` is the triangle. `N = 5`
has no clean 3-pole: hand proof and a labelled brute-force check of all 70
candidates in `audits/three_pole_research_handoff.md`
(`scripts/audit_clean_poles.py`).

**What the completed runs establish** [COMPUTED]. The clean 3-poles on at most
19 vertices are exactly the triangle, uniform H7, skew H7 and H15. Uniqueness
at 15 vertices is this census's claim, conditional on `geng` being complete for
the stated class. It is **not** established by the Hamiltonian cross-check,
which only identifies the rooted survivors of pass VI with these poles.

**Not independently reproduced.** Orders 13 to 19 have one run, with one
generator and one checker. Orders 3 to 11 agree with the separate
catalog-based audit in `scripts/clean_pole_small_audit.json`.

## Unfinished: N = 21

`geng -q -c -f -d2 -D3 21 30:30 i/2` was started in two shards and stopped
by request before completion. **No count and no survivor list is recorded.**
The order-21 question is open.

Estimated cost: about 15 times the order-19 run, so roughly 13 core-minutes,
from the growth between orders 17 and 19.

## Reproduce

```sh
cc -O3 -o cycle_check scripts/cycle_check.c
for N in 7 9 11 13 15 17 19; do E=$(( (3*N-3)/2 )); geng -q -c -f -d2 -D3 $N $E:$E | ./cycle_check 2> clean_$N.g6; done
cat clean_7.g6 clean_15.g6 | diff - scripts/clean_three_poles_n_le_19.g6
python3 scripts/identify_three_poles.py scripts/clean_three_poles_n_le_19.g6
python3 scripts/check_three_pole_isomorphisms.py
```
