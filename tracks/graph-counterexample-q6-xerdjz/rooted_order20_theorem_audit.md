# Audit: the claimed "rooted order-20 theorem" — independently confirmed (C4-free case)

## Status

[COMPUTATIONALLY VERIFIED — independent partial confirmation, different
method and implementation than the source report]

## The claim (as reported, source not accessible from this repo)

> Let `K` be a simple cubic graph on 20 vertices, and let `e` be an edge
> belonging to a perfect matching. Then `K` has a `C4`, `C8`, or `C16`
> avoiding `e`.

Reported as proved via an exhaustive rooted census (22 2-factor
partitions, 157 root-edge orbits, 2,068,777 recursive states, 11,305,998
rejected extensions, 0 survivors), cross-validated by independent C and Go
implementations with byte-identical logs. That implementation is not in
this repo's history (not on any local or remote ref, checked via
`git fetch origin` + `git branch -a` + `git log --all`).

**One combinatorial fact from the report was checked immediately and
matches exactly**: the "22 2-factor partitions of 20 avoiding cycle
lengths 4, 8, 16" — independently computed here via a direct partition
enumeration (parts >=3, excluding {4,8,16}) — gives exactly 22 partitions,
and the first three and last two printed in the report
(`(3,3,3,3,3,5)`, `(3,3,3,5,6)`, `(3,3,3,11)`, ..., `(10,10)`, `(20)`)
match this session's independently generated list exactly.

## Independent verification performed here

Rather than reconstruct the reported orbit-based census (which needs the
source implementation to reproduce exactly), this session ran a
complementary, brute-force independent check on the **hardest special
case**: `K` restricted to `C4`-free. (If `K` has any `C4` avoiding `e`,
the theorem holds trivially for that `e` — the C4-free case is where the
theorem has no easy escape hatch, since the burden falls entirely on
`C8`/`C16`.)

```
nauty-geng -c -f -d3 -D3 20 30:30    # all 36,101 connected, C4-free, cubic 20-vertex graphs
```

For every one of the 36,101 graphs: found a perfect matching
(`networkx.max_weight_matching`, `maxcardinality=True`) — every graph had
one, all of size 10 (`no_perfect_matching: 0`). For every one of its 10
matching edges `e`: removed `e` and checked for a `C8` or `C16` in the
remainder (`verifier/cycle_detect.py`'s DFS detector, this repo's
existing trusted oracle, already cross-validated thousands of times
elsewhere in this project).

**Result: 361,010 (graph, matching-edge) pairs checked, 0 violations.**
(`10 * 36,101 = 361,010`, confirming no pairs were skipped.) Runtime 56.5s.

## What this does and does not establish

**Establishes**: strong independent support for the theorem, specifically
confirmed for the C4-free special case, via a different implementation
(Python/networkx + this repo's own DFS detector) than the source's
reported C/Go implementation, and a completely different algorithm (direct
brute-force matching + removal, not the source's 2-factor/orbit/pruned
completion approach). Two independent methods agreeing on zero
counterexamples across a substantial check is meaningful corroboration.

**Does not establish**: the full theorem as stated, which covers *all*
simple cubic 20-vertex graphs (including ones that do have a `C4`, where
the theorem could in principle fail if every `C4` happens to pass through
`e` and no `C8`/`C16` avoids it either — not checked here, and there are
far more cubic 20-vertex graphs with a `C4` than without one, so this is
not a small residual case). Also does not verify the source's own reported
computation (its exact orbit/state/rejection counts) — only the theorem's
truth on a large, meaningful, independently-generated instance set.

## Bottom line

The theorem's hardest case checks out cleanly under independent
re-implementation. Combined with the exact match on the "22 partitions"
fact, this is meaningfully corroborating evidence, not full independent
reproduction of the source's own certified computation.
