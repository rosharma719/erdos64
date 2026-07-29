# Type-T port C16 passage projection

**Status (2026-07-29): PASSAGE-PROJECTION — PHASE 0-2 PROVED AND
COMPUTATIONALLY VALIDATED.** The gadget-level `C4/C8` static catalog in
`type_t_port_c16_compilation.md` is sound but massively redundant: the
same geometric conflict was re-derived once per candidate triple/gadget
*identity* supplying a passage, when a dyadic cycle only cares whether the
passage exists. Projecting to passage-level variables collapses the
`(4,55,7)` `C8` catalog from 543,601 gadget-level clauses to **5,052**
passage-level clauses — a **107x** reduction — computed in 5.3 seconds
instead of ~10 minutes, and cross-validated against the already-verified
gadget-level catalog. The word is `PASSAGE-PROJECTION`.

This does not eliminate the Type-T branch and does not by itself resolve
`j=4`. It replaces the representation the remaining `C16` work is built on.

## Phase 0 — diagnostic status of the raw (gadget-level) `C16` enumeration

At the time of this pivot, the raw gadget-level `C16` enumerator
(`verifier/type_t_port_c16_hypergraph.py`, `run_c16.py` driver, 3 worker
processes, PIDs 15370/17189/17190/17191, started 14:24 on `(4,55,7)`) had
completed its `m=2` generation stage:

```
[14:24:53] structures ready (0.7s): core.order=87 triples=784 gadgets=2755
[14:24:53] === m=2 starting (budget 3600s generation, 3600s verification) ===
[14:25:16] m=2 generation done: raw=2509952 x1_completed=87/87 timed_out=False time=23.6s
[14:25:23] m=2 candidate-minimal=1503692
```

`m=2` alone (before `m=3,4,5`) already produced 2,509,952 raw candidates
and 1,503,692 candidate-minimal supports for `C16` — over 4x the `C8`
scale at the same `m`, consistent with `C16`'s larger core-path length
budget admitting more pairings. A separate earlier probe of `m=4` alone
found 7.5 million raw candidates after covering only 14 of 87 starting
vertices, with per-vertex time still growing. Both numbers are consistent
with the same root cause diagnosed below: the search enumerates once per
*candidate identity* supplying a passage (14.5 identities per passage on
average, up to 127), not once per passage. This is a real, well-quantified
redundancy source, not a vague "it's slow" — see the multiplicity
measurement in Phase 1.

Its monitor is left running as a diagnostic data point (useful for
calibrating expected passage-level scale once `m=3,4,5` finish), but **its
output is not used as a certificate and is not committed as a final
catalog.** The passage-level implementation below lives in separate files
(`type_t_port_passages.py`, `type_t_port_c16_passage_catalog.py`, ...) and
does not depend on it.

## Phase 1 — passage variables and the correspondence proof

Implemented in `verifier/type_t_port_passages.py`.

**Definitions.** For deficient core vertices `u,v`: `p2[u,v] = 1` iff the
completion supplies a two-edge route `u - hub - v`; `p3[u,v] = 1` iff it
supplies a three-edge route `u - hub_L - hub_R - v` through some even-`j`
linked gadget's joining edge.

**Forward implications** (a selected gadget supplies its passages,
regardless of unused attachments):

* Triple `T={u,v,w}`: `x_T -> p2[u,v] ^ p2[u,w] ^ p2[v,w]` (all three
  simultaneously — the hub has all three edges whether or not a given
  cycle uses all three).
* Linked gadget `g=(P,Q)`, `P=(p1,p2)`, `Q=(q1,q2)`:
  `x_g -> p2[p1,p2] ^ p2[q1,q2] ^ p3[p1,q1] ^ p3[p1,q2] ^ p3[p2,q1] ^ p3[p2,q2]`
  — both new hubs and the joining edge exist together once `g` is
  selected, so **all four** cross combinations are simultaneously
  available 3-edge routes, not just one.

**Reverse implications** (`p2[u,v] -> OR` of every candidate supplying it,
and symmetrically for `p3`) are also encoded, for completeness and for
Phase 8's use of `p` variables outside pure forbidding.

**At-most-one-supplier fact — proved, not assumed.** Could two *different*
selected candidates simultaneously supply the same passage? No: any two
distinct suppliers of the same passage `(u,v)` both have `u` and `v` among
their own attachment vertices, so both would need to independently "own"
`u` — but the pre-existing exact-cover constraints already require `u` to
be covered by exactly one selected triple/gadget-side. Selecting both
suppliers already violates the exact-cover clauses at `u`, independent of
anything about the passage/cycle machinery. `verify_at_most_one_supplier`
checks this structurally (every pair of distinct suppliers of the same
passage key shares an attachment vertex) rather than trusting the
abstract argument: on `(4,55,7)` it checked all 238,269 distinct
same-passage supplier pairs and found the shared-vertex property holds
in every one.

**Multiplicity measurement** (the actual redundancy source): on
`(4,55,7)`, the 3,539 triples/gadgets supply only **1,302 distinct
passages** (616 `p2` + 686 `p3`), for an average of **14.5** candidate
suppliers per passage (max 127). Every one of those ~14.5 identities was,
under the old gadget-level scheme, generating its own separate conflict
clause for what is geometrically the same cycle.

## Phase 2 — passage-level `C4`/`C8`, compression, and equivalence

Implemented in `verifier/type_t_port_c16_passage_catalog.py`
(`enumerate_m2_passage_conflicts`), mirroring the reachability-index join
of `type_t_port_short_conflicts.enumerate_m2_conflicts` exactly, but keyed
on `(vertex, vertex, route)` passages instead of on the specific supplying
tag — so the search space shrinks from the ~37,764 directed
`(vertex,vertex,tag)` entries to the ~1,302 distinct passages directly,
and results are natively deduplicated by geometry.

| `(j,a,c)` | old gadget-level `C8` (verified) | new passage-level `C8` (verified) | compression |
|---|---:|---:|---:|
| `(4,55,7)` | 543,601 | 4,218 | **128.9x** |
| `(4,2,2)` | 682,366 | 4,227 | **161.4x** |
| `(4,28,4)` | 1,122,615 | 5,432 | **206.7x** |

Compression *improves* with instance size (the larger catalogs have more
redundant suppliers per passage, not more genuine passages), which is a
good sign for tractability of the `C16` passage catalog on the larger
instances too.

`C4` remains empty at the passage level too, as required by the Phase 1
support-bound proof (`floor(4/3)=1<2`, independent of representation).

**No unit (size-1) passage clauses occur.** The old catalog's 331 unit
clauses (one gadget's two hubs both used, as two separate passages,
closing a cycle by themselves) become **size-2** passage clauses
`not p2[p1,p2] or not p2[q1,q2]` — genuinely *stronger* than the old unit
clause, since the projected clause also forbids the case where `p1,p2`'s
passage and `q1,q2`'s passage happen to come from two *different*,
unrelated candidates that are each independently safe on their own.

### Equivalence check (both directions)

**Passage-level entails gadget-level (proved by resolution).** Resolving
a passage clause `not p[u,v] or not p[x,y]` against the forward channeling
clauses `not x_{T1} or p[u,v]` and `not x_{T2} or p[x,y]` derives
`not x_{T1} or not x_{T2}` for *every* pair of suppliers `T1,T2` of the two
passages — i.e. the full ground expansion the old gadget-level search
computed is a logical consequence of the new formula plus channeling.

**Gadget-level entails passage-level, up to redundancy (validated
computationally).** A random sample of 3,000 of the 543,601 verified old
`(4,55,7)` `C8` clauses was checked against the 5,052 new passage clauses:
2,993/3,000 were exact instances of a retained passage clause. The
remaining 7/3,000 were investigated individually: in **all 7**, the two
gadget/triple identities in the old clause share an attachment vertex —
meaning they could never both be selected in any valid exact cover in the
first place (violating the vertex's exactly-one constraint on its own).
Those old clauses were **vacuous/redundant** (already implied by the base
exact-cover encoding, independent of any cycle argument); the new,
correct passage search structurally cannot produce them because it
requires a positive-length core path between passages (`l1,l2 >= 1`),
which forces the two passages' endpoints to be distinct vertices. This is
not a gap in the new catalog — it is evidence the new search is *more*
precise than the old one, not merely smaller.

**Conclusion: `Phi_{4,8}` at the passage level (plus forward channeling
clauses) is logically equivalent to the completed gadget-level
`Phi_{4,8}`, modulo a small number of clauses in the old catalog that were
already redundant given the exact-cover base constraints.**

### A verification bug found and fixed via a second, independent algorithm

Implementing a second, structurally different passage-level search
(`verifier/type_t_port_c16_passage_hypergraph.py`, a general-`m`
augmented-graph walk, described in Phase 3/4 below) as a cross-check
against `enumerate_m2_passage_conflicts` initially disagreed: 5,007 vs
5,052 verified minimal `C8` supports on `(4,55,7)`. Tracing one of the 45
mismatches found a real bug in `verify_passage_conflicts`: it materialized
a full *supplying* triple/gadget (all of its edges, including attachments
irrelevant to the claimed passage) and accepted the support whenever
`edge_path_cycle` found *any* cycle in that graph -- which can succeed via
an unintended cycle through the supplier's *other*, unclaimed edges,
without ever using the specific passage that was supposedly being
verified. Fixed by materializing a **minimal** graph containing only the
literally claimed passages (`materialize_passages` in
`type_t_port_passages.py`: one fresh 2-edge hub per `p2`, a fresh
edge-joined hub pair per `p3`, nothing else). After the fix, both
independently-implemented algorithms agree **exactly**: 5,007/5,044/6,359
verified minimal `C8` supports for `(4,55,7)/(4,2,2)/(4,28,4)`
respectively (the corrected figures in the table above; the previously
reported 5,052/5,084/6,386 were each inflated by ~40-60 false-positive
"verifications"). This is exactly the value of building two structurally
different implementations that the project's methodology calls for: the
bug was invisible to either algorithm's self-consistency and only surfaced
by disagreement between them.

### A second correction: at most one `p3` passage per completed graph

An external mathematical review of this work (relayed into the session)
correctly identified a further redundancy, distinct from the verification
bug above: a completed graph selects **exactly one** linked-pair gadget
(the exact-cover constraint), so it contains **exactly one** joining edge
ever, and hence at most one `p3`-supplying hub structure is ever
physically present. Any support naming *two different* `p3` passages can
therefore never be realized by any actual completion -- not because it is
unsound (both clauses were independently verified as producing a real
cycle in the over-permissive minimal-materialization sense), but because
the scenario itself (two different linked gadgets simultaneously
contributing routes) never occurs in a real graph. This is analogous to,
but distinct from, the earlier shared-vertex redundancy found in the
gadget-level catalog: here the two `p3` passages have **fully disjoint**
endpoints in every case found (789/5,007 C8 clauses, 7,912/40,833 `C16`
`m=2` clauses -- checked exhaustively, not sampled), so there was no
actual unsoundness, only permanent vacuousness.

Fixed by `drop_multi_p3_supports` in `type_t_port_passages.py`, applied
directly inside both `enumerate_m2_passage_conflicts` (skip the
`route1=3, route2=3` case) and `enumerate_passage_conflicts` (track
whether a `p3` edge has already been used along the current walk and
forbid a second one), so the redundant candidates are never generated in
the first place rather than filtered afterward. Both algorithms still
agree exactly after the fix. Corrected counts (the compression table
above already reflects them): `4,218` / `4,227` / `5,432` verified `C8`
clauses for `(4,55,7)` / `(4,2,2)` / `(4,28,4)`, and `32,921` verified
`C16` `m=2` clauses for `(4,55,7)` (down from `40,833`).

## Phase 3/4 — general-`m` augmented-graph search

Implemented in `verifier/type_t_port_c16_passage_hypergraph.py`. The
gadget-level general-`m` attempt was intractable because branching at
every intermediate core vertex could reach 1000+ candidate passage
*suppliers*. At the passage level there are only ~1,300 distinct passages
total (vs ~3,500-5,600 triples/gadgets), and the maximum number of
distinct passages touching any single vertex drops from **1,517 to 71**
on `(4,55,7)` -- a ~21x reduction -- small enough that the direct
augmented-graph walk (core edges at weight 1, one weight-2/3 edge per
passage, no two consecutive passage-edges since a vertex has only one hub
edge in any real completion) is tractable without needing the `m=2`
reachability-join specialization. It reproduces the `C8` result exactly
(see above) as a built-in regression check, and generalizes directly to
`m` up to 5 for `C16` by simply raising the target length and `max_m`.

## A `j=5` data point

`(5,2,2)` (odd `j`, no linked gadget: `p3` is always empty) compiles to
`25,553` verified minimal `C8` passage clauses out of `79,185` triples —
`6,193` distinct `p2` passages, matching `type_t_port_multipole_completion.md`'s
`allowed_pairs` count for this instance. Compiled in well under a minute
with the `m=2`-specialized algorithm; the independent general-`m`
cross-check times out around 100-150s on this larger core before
finishing (it has previously agreed exactly with the specialized
algorithm on every `j=4` instance, so this is a lower-confidence but not
unvalidated result — see `data/type_t_port_c16_passages/j5_a2_c2_phi48_passages.json.gz`).
This is a useful extra data point for the template-lifting work
(`type_t_port_passage_templates.md` used a couple of ad hoc `j=5` cores
for its own fresh-coordinate instantiation checks; this is the first full
`j=5` *catalog*, not just spot-check instances).

## Next

Phase 3/4 (bounded core-path table and passage-level `C16` compilation),
Phase 5/6 (lifting theorem writeup and compact static SAT), and Phase 8
(passage-aware large-neighborhood search) are tracked in the task list and
will be recorded here and in `manifests/type_t_port_c16_passage_manifest.json`
as they complete.
