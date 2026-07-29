# Type-T port C16 compilation

**Status (2026-07-29): PHASE 0/1 PROVED; PHASE 2 IN PROGRESS.** This picks up
the minimum cubic multipole completion (`type_t_port_multipole_completion.md`)
where it stopped: all three bounded `j=4` exact CEGAR runs are `UNKNOWN`, no
counterexample and no UNSAT certificate exist, and the dominant residual
obstruction is `C16`. This file compiles the static short-cycle conflict
system in place of further ad hoc CEGAR cuts.

The Type-T branch is not eliminated by anything below. This is one explicit
minimum cubic completion family within the shared-port residual.

## Phase 0 — audit of the existing formulation

### 1. Semantics of a triple variable

A triple `t=(u,v,w)` (`u<v<w`, deficient core vertices) is a Boolean variable
introduced once per element of `allowed_triples(deficient, pairs)`
(`verifier/type_t_port_triples.py`). `allowed_triples` enumerates triangles of
the *same-hub safe-pair graph*: `(u,v,w)` is emitted iff all three of
`(u,v),(u,w),(v,w)` are safe pairs, i.e. none of them is in `same_bad`, the
route-length-2 incompatibility map from `path_incompatibilities`. Each triple
corresponds to exactly one new degree-three hub vertex with three core edges,
one to each of `u,v,w`. There is exactly one variable per 3-subset; the
construction never emits two variables for the same 3-subset.

### 2. Semantics of a linked-gadget variable

For even `j`, a linked gadget is an unordered pair of safe pairs
`(P,Q)`, `P=(p1,p2)`, `Q=(q1,q2)`, `P<Q`, produced by `linked_gadgets`. It
represents **two** new hub vertices (`hub_L` attached to `p1,p2`; `hub_R`
attached to `q1,q2`) joined by **one** new hub-hub edge `hub_L-hub_R`, all
controlled by a **single** Boolean variable. `hub_L` and `hub_R` each have
degree three: two core edges plus the shared hub-hub edge. A gadget is
admitted only when `P`,`Q` are each already safe pairs (checked earlier, when
they were added to the same-hub safe-pair graph) **and** every cross pair
`(p_i,q_j)` is safe at route-length 3 (`cross_bad`, from
`path_incompatibilities(core, route_length=3, ...)`), because the natural
route across the joining edge has length three (`p_i - hub_L - hub_R - q_j`).

### 3. Materialization

`materialize()` in `verifier/type_t_port_multipole_sat.py` is deterministic
and injective: it allocates one fresh vertex per selected triple (edges to
its 3 attachments) and, if a gadget is selected, two fresh vertices `hub_L`,
`hub_R` (edges to `p1,p2` and `q1,q2` respectively, plus the edge
`hub_L-hub_R`). `hub_variable[hub_L] = hub_variable[hub_R] = gadget_var[gadget]`
— both hub vertices map back to the *same* Boolean variable.

### 4. Can two variables represent the same ordinary edge set?

No. Triples are indexed by unique 3-subsets of deficient vertices, so no two
triple variables materialize the same three edges. Gadgets are indexed by
unique unordered pairs of *distinct* safe pairs (`first < second` in
`linked_gadgets`, and `pairs` themselves are distinct 2-subsets), so no two
gadget variables materialize the same four attachment edges. A triple and a
gadget can never coincide because a triple emits three edges from **one**
new vertex while a gadget emits four edges from **two** new vertices plus a
fifth hub-hub edge; the materialized subgraphs are structurally different
(one new vertex of degree 3 vs. two new vertices of degree 3 joined by an
edge). Hence the map from selected variables to ordinary edge sets is
injective, and a cut clause naming a variable set is unambiguous.

### 5. How current cycle cuts map cycles to gadget-variable supports

In `exact_search` (`type_t_port_multipole_sat.py`), for a rejected model the
code enumerates ordinary simple cycles of the shortest violated dyadic length
in the *materialized* graph, then for each cycle computes
`variables = sorted({hub_variable[vertex] for vertex in cycle if vertex in hub_variable})`
and emits `not(v1) or ... or not(vk)`. This already **deduplicates** by
Boolean variable, not by hub vertex: if a cycle visits both `hub_L` and
`hub_R` of the same gadget, the support has size 1 for that gadget, not 2.
This is the mechanism behind the "unit cuts" reported in
`type_t_port_multipole_completion.md` (7, 15, 1 unit cuts for the three
`j=4` cores) — Phase 1 below explains exactly when they arise and proves
they cannot occur for `C4` or `C8` from a single gadget alone (they require
`m=2` hub-passages, so a unit cut needs both hubs of *one* gadget used as two
separate passages, never one gadget by itself in a single passage).

### 6. Does every selected gadget have a unique canonical representation?

Yes, for the reasons in (4): triples are literal 3-subsets, gadgets are
literal unordered pairs of 2-subsets with a fixed `first < second` order, and
the two families are mutually exclusive. No ambiguity remains to correct
before compiling conflicts.

## Phase 1 — support bounds

### 1.1 Hub-passage anatomy

Fix a simple cycle `C` in a materialized completion. `C` alternates between
**hub passages** (maximal runs of `C` lying in the new vertices) and **core
paths** (maximal runs of `C` lying in `G0`, the bare core). Because every
deficient core vertex is covered by exactly one triple or one side of exactly
one gadget (the exact-one constraint), two hub passages can never share a
boundary vertex, so every core path between consecutive hub passages has
length `>= 1`. This reproduces the alternating-path decomposition of
`type_t_port_completion_obstruction.md` Section 2, now for hubs rather than
matching edges.

A simple cycle visits each vertex at most once, so it uses each new hub
vertex at most once. Every new hub vertex has degree exactly 3, so a hub
passage through it uses exactly 2 of its 3 incident edges. Case analysis on
the hub type:

* **Triple hub.** All three incident edges are core edges (to `u,v,w`). A
  passage uses 2 of the 3, contributing **route length 2** and consuming
  **1 hub, 1 Boolean variable**.
* **Linked-gadget hub, single-hub passage.** `hub_L` has two core edges (to
  `p1,p2`) and one hub-hub edge (to `hub_R`). If `C` uses `hub_L`'s two core
  edges and *not* the hub-hub edge, this is a passage of **route length 2**,
  consuming **1 hub** (just `hub_L`), **1 Boolean variable** (the gadget's).
  Symmetrically for `hub_R` alone.
* **Linked-gadget hub, cross passage.** If `C` uses the hub-hub edge, it must
  use exactly one core edge at `hub_L` and one at `hub_R` (each hub still
  contributes exactly 2 of its 3 edges to the cycle), so `C` passes through
  `hub_L` and `hub_R` together as **one passage** of **route length 3**
  (`p_i - hub_L - hub_R - q_j`), consuming **2 hubs** but only **1 Boolean
  variable**.
* **Linked-gadget, both hubs, two separate passages.** `hub_L` and `hub_R`
  can *each independently* take the "single-hub passage" case above, at two
  different, non-adjacent points of the cyclic order, without ever using the
  hub-hub edge. This consumes **2 hubs, 2 passages, but only 1 Boolean
  variable** (both hubs still resolve to the same `gadget_var`). This is the
  mechanism that produces unit cuts when `m=2` (Section 1.3).

No other case exists: a hub-hub edge forces its two endpoints into one
combined passage; without it, each linked hub is an independent route-2
passage exactly like a triple hub restricted to 2 of 3 slots (except it only
*has* 2 slots).

### 1.2 The `(m, r, v)` identity

Let `m` = number of hub passages in `C`, `r` = number of **distinct new hub
vertices** used, `v` = number of **distinct Boolean variables** used
(`v <= m`, the quantity that actually indexes a conflict clause literal set).
Let `x` = number of cross passages among the `m` (route length 3, 2 hubs
each); the remaining `m - x` passages are route-length-2, 1 hub each. Then

```
r = (m - x) * 1 + x * 2 = m + x
route_total = (m - x) * 2 + x * 3 = 2m + x = m + r
```

Every core path has length `>= 1` and there are exactly `m` of them (cyclic
alternation with `m` passages), so `core_total >= m`. Hence for cycle length
`L`:

```
L = route_total + core_total >= (m + r) + m = 2m + r.      (*)
```

Also `0 <= x <= m` gives `m <= r <= 2m`, i.e. `m >= r/2` (using `x <= m`,
i.e. `r = m + x <= 2m`) and `m <= r` (using `x >= 0`).

**Bound on `m` (and hence on `v`, since `v <= m`).** Since `r >= m`,
`(*)` gives `L >= 2m + m = 3m`, i.e.

```
m <= floor(L/3),   v <= m <= floor(L/3).
```

For `L=4`: `m <= 1`. For `L=8`: `m <= 2`. For `L=16`: `m <= 5` — this
reproduces and generalizes the requested bound `16 >= 3r` for the
all-ordinary-triple case (there `x=0`, so `r=m`, and the general bound
specializes exactly to `16 >= 3r`, `r <= 5`).

**Bound on `r` alone** (allowing cross passages) is looser: minimizing `m`
for fixed `r` uses `m = ceil(r/2)` (pack `r` hubs into as few, cross-heavy,
passages as possible), and `(*)` gives `L >= 2*ceil(r/2) + r`, i.e.
`r <= floor(L/2)` (even `L`). For `L=16` this allows `r` up to 8 if every
passage is a cross passage, strictly more than the 5 ordinary hubs of the
literal statement — this is why the two quantities must be kept distinct, as
required: **`r` (hubs) can exceed `v` (variables) can exceed neither can
exceed `floor(L/2)` resp. `floor(L/3)`, and they coincide only when no cross
passages and no doubled gadgets are used.**

### 1.3 The `m=1` screen is already complete, for every dyadic length

`path_incompatibilities(core, route_length, completion_order)` computes,
for **every** power-of-two length up to `completion_order` (so certainly
`4,8,16,...`), the forbidden core-path length `length - route_length` and
records every core pair realizing it. `allowed_triples` only keeps triples
all of whose 3 sub-pairs are absent from this `route_length=2` map;
`linked_gadgets` only keeps gadgets whose cross pairs are absent from the
`route_length=3` map. **Consequently no candidate triple or gadget can, by
itself, close a dyadic cycle of *any* length via a single hub passage** —
the `m=1` case is excluded uniformly, not just for `C16`. This proves the
requested completeness claim, and it strengthens it: it holds for every
`L in {4,8,16,32,64,...}` up to the completion order, not only `L=16`.

### 1.4 Corollaries: `m >= 2` always, hence per-length classification

Combining 1.2 and 1.3: every dyadic-cycle conflict has `2 <= m <= floor(L/3)`.

* **`C4` (`L=4`):** `floor(4/3)=1`, but `m>=2` is required. **No `m` value is
  admissible: `C4` conflicts cannot exist beyond the base local-safety
  screen.** Every completion drawn from `allowed_triples` and locally-safe
  `linked_gadgets` is automatically `C4`-free — no additional clause is
  needed for `C4`. This matches the data: `best_cycle_counts["4"] == 0` in
  all four recorded instances (`(2,2)`, `(28,4)`, `(55,7)`, `j=5 (2,2)`),
  and 320-324 of 324 j=4 same-vertex-completion classes needed no `C4` cut
  either (`type_t_port_completion_j4.md` Section 3).
* **`C8` (`L=8`):** `floor(8/3)=2`, so `m=2` exactly. `x in {0,1,2}` gives
  `r in {2,3,4}`, `route_total in {4,5,6}`, `core_total in {4,3,2}` split
  into 2 positive parts. `v = m - d` where `d in {0,1}` is 1 exactly when
  both passages are the two single-hub passages of *one* gadget (the unit-cut
  case); otherwise `v=2`. **So every `C8` conflict has support size 1 or 2,
  never larger**, and no `C4` term can appear in it.
* **`C16` (`L=16`):** `m in {2,3,4,5}`. `v <= 5`, matching the "at most five
  hubs" statement in the handoff, now proved with an exact variable-count
  interpretation (`v`, not `r`) and shown to also bound the case with linked
  gadgets. Minimum `v` is 1, achieved e.g. at `m=2,d=1` (a single gadget
  used twice, 12 units of slack to distribute across the two core paths) —
  so unit `C16` cuts are combinatorially possible and must be searched for,
  not assumed absent.

### 1.5 What this buys Phase 2

Because `C4` contributes nothing beyond the existing local screen, and `C8`
requires exactly `m=2`, the static formula

```
Phi_{4,8} = (exact-cover base clauses) + {C8 conflict clauses at m=2}
```

is **exactly** the existing exact-cover encoding (`build_exact_cover_cnf`)
plus a *bounded, 2-hub-passage* conflict search — no arbitrary-depth CEGAR
loop is needed to be complete for `C4,C8`. This is implemented and verified
in `verifier/type_t_port_short_conflicts.py` (Phase 2 below).

## Phase 2 — status

Implemented in `verifier/type_t_port_short_conflicts.py` as
`enumerate_m2_conflicts`, specialized to the (proved) exactly-`m=2` case
that covers both `C4` (vacuously empty) and `C8`. The naive approach —
build an augmented graph with one weighted "virtual" edge per candidate hub
passage and run a live weighted-DFS cycle search — is intractable: some
core vertices are endpoints of 1000+ candidate passages (from the `~3500`
triples/gadgets in a `j=4` catalog), so branching at every intermediate
core vertex blows up. The working algorithm instead precomputes, once, a
bare-core reachability index `reach[v][l]` (vertices reachable from `v` by
a simple core path of length exactly `l`) and uses the undirected symmetry
`y2 reaches x1 at length l2  <=>  y2 in reach[x1][l2]` to turn the search
for a valid `(x1,y1)-(x2,y2)` join into two small-set lookups plus one
`O(1)` dict probe into `(endpoint, endpoint, route-length) -> variable`
(`build_pair_index`), never scanning a vertex's full passage list. Every
raw candidate is then **independently** re-verified by materializing
exactly its named hubs and locating the cycle with `edge_path_cycle`
(edge plus an exact-length simple path avoiding it — a differently
organized detector, reused unmodified from `verifier/type_t_port_multipole_check.py`);
candidates the fast filter proposes but that don't materialize into a real
cycle are dropped, not treated as errors.

| `(j,a,c)` | catalog (triples+gadgets) | `C4` | `C8` raw / minimal / verified | status |
|---|---:|---:|---|---|
| `(4,55,7)` | 784+2755=3539 | 0 (matches the proof) | 801,129 / 571,761 / 543,601 (331 unit, 543,270 pair) | `COMPUTATIONALLY_CERTIFIED` |
| `(4,2,2)` | 925+3037=3962 | pending | pending | running |
| `(4,28,4)` | 1225+4371=5596 | pending | pending | running |

The `(4,55,7)` `C4` result is a genuine independent cross-check of the
Phase 1 proof (`m>=2` required, `floor(4/3)=1`), not just a restatement of
it — the search machinery was run and correctly found nothing. The `C8`
scale is large (`543,601` verified minimal conflict clauses for the
smallest of the three instances) but this is the complete, exact static
catalog for that instance, not a CEGAR sample: `Phi_{4,8}` for `(4,55,7)`
is the existing exact-cover encoding plus these clauses, and every model
of it is provably `C4,C8`-free (every possible 2-hub-passage conflict was
enumerated and independently verified) and every `C4,C8`-free completion
is provably a model of it (Phase 1 proves no other conflict shape is
possible). See `manifests/type_t_port_c16_manifest.json` and
`data/type_t_port_c16/j4_a55_c7_phi48.json.gz` for the full record.

Never inferring an all-`j` theorem from `j=4`, never calling a timed-out
run `UNSAT`, and never calling a `C4,C8,C16`-free completion a
counterexample before every power-of-two cycle through its order is
independently excluded.

## Phase 3 onward

Not yet attempted in this file. The `C16` hypergraph (`m in {2,3,4,5}`),
static `Phi_{4,8,16}` solve, and any obstruction/theorem extraction remain
open and are tracked in `manifests/type_t_port_c16_manifest.json` with
status `UNKNOWN`/`BOUNDED_INCOMPLETE` until computed.
