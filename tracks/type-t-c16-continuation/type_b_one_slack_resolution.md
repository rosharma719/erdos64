# One-slack `Pi0` bridges: resolving the 28-edge remainder layer

**Status.** This file extends `type_b_one_slack.md` Section 4. Both Family
I (`2,3^18`) and Family II (`2^2,3^16,4`) are now fully eliminated by
exhaustive computation. Family I is cross-checked by four independent
detectors; Family II by two independently coded exhaustive generators (a
C backtracking slot-matching search and an independent PySAT model) whose
canonical candidate sets agree exactly (identical SHA-256), plus a third
independent networkx-based witness verifier. Theorem B20 is proved at the
end of this file. No proof-assistant formalization exists for any part of
this file.

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
(`verifier/type_b_slack_family_filter.py` stage 2) is never reached
because no candidate survives the cycle-freeness filter.

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

## 3. Family II (`2^2,3^16,4`): the exact slot-matching model

Unlike Family I, this degree profile cannot be produced directly by
`nauty-geng`, which only supports global min/max degree bounds, not exact
per-degree vertex counts. The natural box `-d2 -D4 19 28:28` also contains
every other admissible-looking-but-irrelevant profile with degree deviations
summing to `-1` (e.g. three degree-2 and two degree-4 vertices), which
Section 1 above rules out but `geng` cannot be told to skip. A single-
threaded full generation of this box did not complete in a 5-minute trial,
and inspection of the first 8.28 million graphs generated (before being
intentionally stopped) contained zero matches for the exact `2^2,3^16,4`
profile — not evidence of absence, only a sign the relevant region of
`geng`'s canonical generation order had not yet been reached. This broad,
degree-sequence-agnostic search was abandoned in favor of an exact model
built directly from the required structure.

**The exact model.** `R` contains the fixed 18-vertex path
`p_0 p_1 ... p_17` (`p_0=a`, `p_17=y`) contributing 17 edges, plus the
off-path vertex `z`. Since `|E(R)|=28`, exactly **11** non-path edges
remain to be placed. By the excess argument of Section 1, exactly one
vertex carries a `+1` degree excess (degree 4) beyond the base pattern
`a=y=2`, all sixteen other path-internal vertices `=3`, `z=3`. That
degree-4 role is either one of `p_1,...,p_16` (16 cases) or `z` itself (1
case): **17 role cases** in total. For role `p_j`: the deficit vector
(additional degree needed beyond path degree) is `a=1, y=1, p_j=2`, the
other 15 internal vertices `=1` each, `z=3`; total deficit `22 = 2*11`.
For role `z`: `a=1, y=1`, all 16 internal vertices `=1` each, `z=4`; total
deficit `22` again. No edge is excluded a priori beyond the 17 fixed path
edges and loops — every other pair among the 19 vertices is an eligible
non-path candidate (154 of them), and any exclusion is discovered by the
search itself (via the incremental C4/C8 check), not assumed upfront.

## 4. Direct slot-matching generator (`verifier/type_b_slack_path_search.c -generate-all`)

For each of the 17 roles, a backtracking search over the 154 candidate
edges (include/exclude branching, in a fixed lexicographic order) selects
exactly 11 edges matching the role's deficit vector. Two feasibility
prunes are applied at every step: a vertex with zero remaining deficit can
never receive another edge, and a branch is abandoned once fewer
candidate edges remain than some vertex's outstanding deficit requires.

**Cycle pruning (edge-local, C4/C8 only).** Adding edge `uv` creates a
`k`-cycle exactly when the graph built so far already contains a simple
`u`-`v` path of length `k-1`. This is safe to check incrementally because
cycles are monotone under edge addition: once a graph is known to contain
no forbidden cycle through the newest edge, no earlier or later edge
choice can retroactively remove that cycle, and any completed graph's
full cycle set is exactly the union of what each edge contributed at its
own insertion. The search rejects an edge if the graph so far already has
a simple `u`-`v` path of length 3 (would create `C4`) or length 7 (would
create `C8`). It does **not** prune on length 15 (`C16`) during the
search; every completed 11-edge graph is independently re-checked for
`C4`, `C8`, and `C16` after the fact using the same `has_cycle_len`
routine already used (and unit-tested) for Family I.

*Note on the interrupted-session narrative.* An earlier account of this
project (never found in this repository's history) described a
`has_cycle_len` bug where the start vertex was marked visited and the
closing step also required it unvisited, making detection vacuous. No
such implementation exists anywhere in this repository's git history; the
`has_cycle_len` used throughout (Family I and here) was written fresh and
unit-tested against `K4`, an 8-cycle, and a path graph (Section 2 of this
file's certificate) before being trusted. The warning is recorded here
only because the task instructions asked for it, not because the bug was
actually inherited.

**Result.** The generator found **54** total labeled candidates across
all 17 roles (not "72" — no prior count exists in this repository to
match or hide a discrepancy against):

| role | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| solutions | 0 | 0 | 3 | 1 | 4 | 4 | 5 | 8 | 8 | 5 | 4 | 4 | 1 | 3 | 0 | 0 | 4 |

The counts are exactly symmetric under path reversal (`p_j <-> p_17-j`,
`a<->y`, `z` fixed) — role `j` and role `17-j` always agree (e.g. role 3
and role 14 both give 3; role 8 and role 9 both give 8) — a strong,
unplanned internal consistency check, since the search for each role runs
completely independently and this symmetry was never hard-coded.
Total DFS nodes: 41,923,888 (about 7.75 seconds).

**Every one of the 54 candidates independently re-checked positive for
all three of:**

- an internal `C16` (found by the same `has_cycle_len` routine, not
  pruned incrementally),
- a simple length-6 `a`-`y` path (closing to a `C8` — see Section 5),
- a simple length-14 `a`-`y` path (closing to a `C16` — see Section 5).

Zero candidates contain a `C4` or `C8` directly (as guaranteed by the
incremental pruning; the redundant post-hoc check confirms this on all 54,
serving as a self-consistency check on the pruning logic).

## 5. The terminal-closing offset, audited

The restored full Type-B graph contains edges `xa` and `xy` (`x`'s only
neighbour is `a`; `xy` is the terminal edge). A simple `a`-`y` path `Q` of
length `r` inside `R` produces the simple cycle `x-a + Q + y-x` of length
`r+2` (**two** edges close the cycle, not one): `r=6` gives a `C8`,
`r=14` gives a `C16`. This is the offset the task instructions asked to be
audited against an "edge-plus-one" error; the implementation searches for
paths of length exactly 6 and exactly 14 (not 7 and 15), matching `r+2`
correctly. All 54 candidates have both such paths (see
`data/type_b_slack_family_ii_witnesses.json` for explicit vertex
sequences), so the closure-cycle argument eliminates them independent of
the internal-`C16` argument above.

## 6. Independent SAT generator (`verifier/type_b_slack_path_sat.py`)

A second, independently coded generator: one boolean variable per
candidate edge, exact-cardinality constraints (PySAT `CardEnc.equals`) for
every vertex's required additional degree, and a CEGAR loop — solve for a
degree-feasible model, check the induced graph for a `C4`/`C8` using
`verifier/cycle_detect.py`'s DFS detector (not the C file's), add a
blocking clause over the witnessed candidate edges if one is found, and
resolve. This shares only the mathematical definition of the path, the
per-role deficit vectors, and the candidate-edge universe with the direct
generator — it imports neither its recursion nor its pruning code nor its
output as a starting population.

**Result:** 54 total solutions, matching the direct generator's per-role
counts exactly (0,0,3,1,4,4,5,8,8,5,4,4,1,3,0,0,4). Total wall time 3m33s.

## 7. Canonical-set comparison

Canonicalizing under the path-reversal symmetry (`p_i <-> p_17-i`, `a<->y`,
`z` fixed, degree-4 role mapped accordingly) collapses the 54 labeled
solutions from each generator to **27** canonical classes. The two
generators' canonical sets are identical:

```text
C direct generator:  labeled=54  canonical=27
SAT generator:       labeled=54  canonical=27
C canonical multiset SHA-256:   31a373da1a9d22ffeb260dc8a0ec99b83390287855dd9c1f6ca6ab4ac454be8c
SAT canonical multiset SHA-256: 31a373da1a9d22ffeb260dc8a0ec99b83390287855dd9c1f6ca6ab4ac454be8c
only_in_C: 0   only_in_SAT: 0
SETS AGREE: True
```

## 8. Third-method independent verification

`verifier/type_b_slack_independent.py` (networkx-only, calling neither
generator's internal functions) re-derives, from the 54 saved candidate
records alone: vertex/edge counts, connectivity, the exact degree
sequence, presence of the fixed path, the claimed degree-4 role, `C4`,
`C8`, `C16`, and both closing-path witnesses. All 54 pass every
structural check and all 54 are independently confirmed eliminated
(`data/type_b_slack_family_ii_witnesses.json`,
`all_have_c16 = all_have_ay_len6 = all_have_ay_len14 = true`). A further
manual spot re-verification (outside all three tools, directly against
the raw edge lists with a fresh networkx script) confirmed the recorded
`C16` witness and both `a`-`y` path witnesses are valid on all 54 records.

## 9. Family II conclusion

Both Family I and Family II of the 28-edge remainder layer are eliminated
by exhaustive, cross-validated computation. No candidate in either family
admits a valid embedding: Family I fails `C8`-freeness outright; every
Family II candidate fails on three independent grounds at once (internal
`C16`, closure `C8` via a length-6 `a`-`y` path, and closure `C16` via a
length-14 `a`-`y` path).

## 10. Theorem B20

**B20.** No eligible 20-vertex `Pi0` bridge exists.

*Proof.* Let `B` be either `Pi0` bridge role with `|V(B)|=20`, terminals
`x,y`, gateway `a`, remainder `R=B-x` (19 vertices, `|E(R)|=28` by Section
2 of `type_b_one_slack.md`). By the excess-counting argument (Section 1
above), `R`'s degree sequence is exactly `2,3^18` (Family I) or
`2^2,3^16,4` (Family II); no other sequence is arithmetically possible
under the established lower bounds. Family I is eliminated (Section 2);
every one of its 86,047 exhaustively-generated candidates contains a `C8`.
Family II is eliminated (Sections 3-8); every one of its 54
exhaustively-generated candidates (agreeing exactly between two
independently coded generators, further confirmed by a third independent
verifier) contains an internal `C16` and forces both a closure `C8` and a
closure `C16` through the terminal-closing argument of Section 5. Hence no
19-vertex `R` — and so no 20-vertex bridge `B` — satisfies the necessary
conditions for either `Pi0` role. `square`

**Consequence.** Since B19 already established `|V(B)| != 19` for either
bridge role (`type_b_b19.md`), and B20 now establishes `|V(B)| != 20`,
every `Pi0`-eligible bridge has `|V(B)| >= 21`. For a full graph built from
two such bridges sharing terminals `x,y`:

\[
 |V(G)| = |V(B_1)| + |V(B_2)| - 2 \ge 21+21-2 = 40.
\]

This raises the lower bound for a `Pi0`-realizing Type-B configuration to
`|V(G)| >= 40`, stated narrowly: it applies to configurations that reduce
to the `Pi0` tuple `(2,2,4,4,1,1)` under the established bridge-reduction
machinery. It is not claimed here that every Type-B configuration reduces
to `Pi0`, nor that `|V(G)|>=40` holds for Type-B in general — that broader
claim is outside the scope of this file. No proof-assistant formalization
exists for B19, B20, or this consequence.

## 11. What is explicitly claimed and what is not

- **Claimed:** Family I and Family II of the 28-edge one-slack remainder
  layer are both exhaustively eliminated, cross-validated as described
  above. B20 is proved. `|V(G)| >= 40` holds narrowly for `Pi0`-reducing
  Type-B configurations.
- **Not claimed:** that all Type-B configurations reduce to `Pi0`; any
  proof-assistant formalization; that the broad (non-degree-restricted)
  `nauty-geng` search of Section 3 completed (it did not — it was
  abandoned in favor of the exact model, and is not required once the two
  exact generators agree).
