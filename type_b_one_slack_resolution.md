# One-slack `Pi0` bridges: resolving the 28-edge remainder layer

**Status.** This file extends `type_b_one_slack.md` Section 4. Family I
(`2,3^18`) is now fully eliminated by exhaustive computation, cross-checked
by four independent detectors. Family II (`2^2,3^16,4`) is **still under
active exhaustive search**; no elimination or survival claim is made for it
yet. No proof-assistant formalization exists for any part of this file.

## 1. Why only two degree sequences are possible

Restated precisely: in `R` (19 vertices, `|E(R)|=28`), the seventeen
"ordinary internal" vertices (the sixteen true path-internal vertices plus
`z`) have degree `>=3`, and the two path endpoints `a,y` have degree `>=2`.
Summing the lower bounds gives `17*3+2*2=55`. The actual degree sum is
`2*28=56`, an excess of exactly `1` over the sum of lower bounds.

Since every vertex's excess over its own lower bound is a non-negative
integer, and these excesses must sum to exactly `1`, **exactly one vertex**
carries the entire excess and every other vertex sits exactly at its lower
bound. Two cases:

- The excess lands on one of the seventeen internal vertices (degree
  `3->4`): `a=2, y=2`, sixteen internal vertices at `3`, one internal vertex
  at `4`. Degree sequence `2^2,3^16,4` (**Family II**).
- The excess lands on `a` or `y` (degree `2->3`): the other endpoint stays
  at `2`, all seventeen internal vertices stay at `3`. Degree sequence
  `2,3^18` (**Family I**).

No vertex can reach degree `5` or higher: that would require excess `>=2`
on one vertex, forcing negative excess (a violation of a stated lower
bound) somewhere else to keep the sum at `1`. This is a complete case
analysis, not a heuristic one.

## 2. Family I (`2,3^18`): fully eliminated

**Generation.** All connected, 4-cycle-free graphs on 19 vertices with 28
edges and degree bounds `[2,3]` were enumerated with `nauty-geng`:

```text
nauty-geng -c -f -d2 -D3 19 28:28
```

Because every degree lies in `{2,3}` and the edge count is fixed at 28,
the degree sequence `2k+3(19-k)=56` forces `k=1`: this box's degree
sequence is automatically exactly `2,3^18`, with no further filtering
needed. This produced **86,047** non-isomorphic graphs in 27 seconds,
stored at `data/type_b_slack_family_i_n19e28.g6` (SHA-256
`cd9d2477eae69bd427ece21f33668bd27896d90722158fcda18f7381c281507b`).

**Result.** Every one of the 86,047 candidates contains an 8-cycle. Zero
survive C4/C8/C16-freeness. Since a valid embedding requires `R` to be
C4/C8/C16-free (Section 1 of `type_b_one_slack.md`), Family I is
eliminated outright — the Hamiltonian-path/off-path-vertex geometry check
(Section 4 below) is never reached because no candidate survives the
cycle-freeness filter.

**Four independent cross-checks, all in agreement:**

| detector | language/library | result |
|---|---|---|
| DFS backtracking (`verifier/cycle_detect.py`) | Python | 86,047/86,047 contain C8 |
| `networkx.simple_cycles` (`verifier/cycle_detect.py`) | Python/networkx | 86,047/86,047 contain C8, 0 disagreements with DFS |
| SAT cycle-position encoding (`verifier/type_b_slack_path_sat.py`) | Python/pysat (Glucose3) | agrees with DFS+networkx on 100 random-graph trials x {C4,C8} (0 disagreements) |
| from-scratch DFS (`verifier/type_b_slack_path_search.c`) | C | 86,047/86,047 contain C8, 0 malformed, 0 degree mismatches |

The C implementation was unit-tested independently before use: correctly
flags `K4` (has C4), correctly flags an 8-cycle graph (has C8), and
correctly reports a path graph as a survivor (contains no C4/C8/C16 at
all) — see the manifest for the exact commands.

**Conclusion:** Family I is eliminated by an exhaustive, four-way
cross-validated computation. No further geometric argument is needed for
this branch.

## 3. Family II (`2^2,3^16,4`): search in progress, unresolved

Unlike Family I, this degree profile cannot be produced directly by
`nauty-geng`, which only supports global min/max degree bounds, not exact
per-degree vertex counts. The natural box `-d2 -D4 19 28:28` also contains
every other admissible-looking-but-irrelevant profile with degree deviations
summing to `-1` (e.g. three degree-2 and two degree-4 vertices), which
Section 1 above rules out but `geng` cannot be told to skip. A single-
threaded full generation of this box did not complete in a 5-minute trial
(consistent with the earlier abandoned attempt recorded in
`type_b_one_slack.md`), and inspection of the first 8.28 million graphs
generated (before being intentionally stopped) contained **zero** matches
for the exact `2^2,3^16,4` profile — this is *not* evidence of absence, only
a sign the relevant region of `geng`'s canonical generation order had not
yet been reached.

**Current approach.** The box is sharded four ways using `geng`'s native
`res/mod` partitioning and streamed through a fast graph6 degree-profile
filter (`verifier/type_b_slack_degree_filter.py`) that discards
non-matching graphs without ever storing them, so only true
`2^2,3^16,4` candidates hit disk. Each shard runs with a 90-minute budget.

**No claim is made about this layer until the search completes and its
survivors (if any) pass the same four-detector C4/C8/C16 check and the
Hamiltonian-path/off-path-vertex geometry check from Section 4 of
`type_b_one_slack.md`.** This file will be updated with that result.

## 4. What is explicitly NOT yet claimed

- `|V(G)| >= 40` is **not** claimed. That requires both families
  eliminated and theorem B20 proved; neither has happened.
- Family II is **not** claimed eliminated, nor is a survivor claimed
  found. The search is incomplete.
- No proof-assistant formalization exists for any result in this file.
