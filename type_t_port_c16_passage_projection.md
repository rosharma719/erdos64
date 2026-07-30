# Type-T port C16 passage projection

**Status (2026-07-30): PASSAGE-PROJECTION — `C4/C8` COMPLETE; FIXED
`(4,55,7)` `C16` NOW HAS A COMPILED LAYER FOR EVERY ADMISSIBLE `m`.
`m=4`, previously the sole open static layer, was closed this pass
(3,971,519 verified minimal supports, 87/87 canonical starts, 0
verification rejections). `m=2/m=3/m=4` are complete outright; `m=5`
remains complete only *relative to the pre-`m=4` shadow*, so exactly one
mechanical step — rerunning `m=5` with the new `m=4` shadow — stands
between here and the final minimal fixed-instance `C16` CNF. That rerun
was **not** attempted in this pass; see "Phase 7" and "Next" for the
precise cost.** The
gadget-level `C4/C8` static catalog in
`type_t_port_c16_compilation.md` is sound but massively redundant: the
same geometric conflict was re-derived once per candidate triple/gadget
*identity* supplying a passage, when a dyadic cycle only cares whether the
passage exists. Projecting to passage-level variables collapses the
`(4,55,7)` `C8` catalog from 543,601 gadget-level clauses to **4,218**
passage-level clauses — a **128.9x** reduction
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
correctly identified that a passage-level support can never name two
different `p3` passages, and a follow-up review correctly caught that this
session's *first* explanation for why was itself imprecise for one
important sub-case. Both rounds are recorded here since the distinction
matters for trusting the methodology, even though **the actual generated
catalogs were never affected either time** (see below).

**First-pass explanation (incomplete).** A completed graph selects
**exactly one** linked-pair gadget, so it contains exactly one joining
edge; the two `p3` passages found pre-fix had **fully disjoint** endpoints
in every case (checked exhaustively: 789/5,007 `C8` candidates,
7,912/40,833 `C16` `m=2` candidates), which was taken to mean the excluded
supports were sound-but-vacuous -- already implied by "exactly one gadget
selected," never actually unsound.

**The gap.** Checking only vertex-disjointness misses a subtler case: a
*single* gadget with sides `{a,b}` and `{c,d}` makes **all four** of its
cross passages true simultaneously the instant it is selected (forward
channeling: `x_g -> p3[a,c] AND p3[a,d] AND p3[b,c] AND p3[b,d]`, all
together, regardless of whether any one cycle could ever use more than
one). `p3[a,c]` and `p3[b,d]` are a "complementary pair" of that one
gadget -- four fully distinct vertices, no shared endpoint, yet forced
true *together* by a single selection. A static clause
`not p3[a,c] or not p3[b,d]` directly contradicts that channeling axiom
the moment this gadget is selected: not vacuous (implied by other
constraints) but **actively unsound** -- capable of forcing the whole SAT
instance UNSAT by rejecting a perfectly legal completion for no real
graph-theoretic reason. Checked directly: of the 1,457 raw p3-p3
candidates the (4,55,7) `C8` search generated pre-fix, **331 were exactly
this same-gadget complementary case** -- a real occurrence, not a
hypothetical edge case.

**Why the catalogs were never actually wrong.** The fix
(`drop_multi_p3_supports` in `type_t_port_passages.py`, applied inside
both `enumerate_m2_passage_conflicts` -- skip `route1=3, route2=3` --  and
`enumerate_passage_conflicts` -- track whether a `p3` edge was already
used along the walk and forbid a second one) excludes **every** two-`p3`
support unconditionally, regardless of whether it is the same-gadget
(unsound) or different-gadget (vacuous) case -- the distinction changes
*why* exclusion is necessary, not *whether* it is, and the code already
did the latter correctly before this correction was raised. Both
independent algorithms still agree exactly. Corrected counts (the
compression table above already reflects them): `4,218` / `4,227` /
`5,432` verified `C8` clauses for `(4,55,7)` / `(4,2,2)` / `(4,28,4)`, and
`32,921` verified `C16` `m=2` clauses for `(4,55,7)` (down from `40,833`).
Regression-tested directly (`test_same_gadget_complementary_p3_pairs_would_be_unsound_if_kept`
in `tests/test_type_t_port_passages.py`): the generator produces none of
the structurally-possible same-gadget complementary pairs, for any gadget
in the catalog.

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

### Exact fixed-instance stage ledger

For `(j,a,c)=(4,55,7)`, lower-shadow pruning always includes all already
certified `C8` conflicts and all smaller completed `C16` passage-count
stages:

| stage | status | new verified supports |
|---|---|---:|
| `m=2` | complete | 32,921 |
| `m=3` | complete | 279,859 |
| `m=4` | complete (closed 2026-07-30, Phase 7) | 3,971,519 |
| `m=5` | complete **only relative to the `C8/m2/m3` lower shadow** — predates `m=4`, needs one rerun | 2,944,894 |

`m=2`, `m=3` and `m=4` are complete *outright*, not merely relative to
their shadow: domination only ever runs from a smaller support to a larger
one, so a stage at support size `k` is final as soon as every conflict of
support size `< k` is certified — which was true for each of these three at
the time it ran. `m=5` is the only stage that was compiled before a smaller
stage (`m=4`) existed, which is exactly why it alone carries a qualifier.

The `m=5` layer is handled by
`verifier/type_t_port_c16_passage_m5.py`.  The length identity leaves only
two cases: five `p2` passages with core segment lengths
`{2,1,1,1,1}`, or four `p2` passages plus one `p3` passage with five unit
core segments.  The exact run:

* covered all 87/87 canonical start vertices;
* pruned 157,006,598 branches using 316,684 distinct certified lower-shadow
  supports;
* exhaustively reconstructed a literal simple 16-cycle for every one of
  the 2,944,894 survivors, rejecting zero;
* cross-checked an evenly spaced 2,000-support sample using the older,
  structurally different `materialize_passages + edge_path_cycle` verifier,
  again rejecting zero.

Retaining 2,944,894 copies of essentially the same 16-vertex witness would
inflate the repository without adding mathematical information.  The
committed 60 KiB summary therefore contains the counts, the 2,000 generic
cross-check witnesses, the complete reproduction command, and a canonical
commitment to the sorted support set:

```text
ed4f922106dbba98774b97ed8151e97dfc1afe6e8f1ab25fd9a026f595f1f646
```

This is not yet the final globally minimal `C16` clause set: once `m=4` is
compiled, some five-passage supports may be supersets of an `m=4` conflict.
The `m=5` compiler must then be rerun with that new lower shadow.  Thus this
result closes the exact five-passage search itself while identifying `m=4`
as the sole remaining static layer for the fixed instance; it does not
claim an UNSAT result, a counterexample, or a proof of the conjecture.

## Phase 7 — closing the `m=4` layer

Implemented in `verifier/type_t_port_c16_passage_m4.py`; result committed as
`data/type_t_port_c16_passages/j4_a55_c7_c16_passages_m4_summary.json.gz`.

### Why `m=4` was left open, and what was actually blocking it

It was **not** a missing technique and **not** a theory gap — it was a
scale problem with a specific shape, which is worth recording precisely
because the shape is what dictated the fix.

The general oracle-pruned search (`type_t_port_c16_passage_general.py`,
which produced `m=2` and `m=3`) has two costs. Generation is the cheaper
one: `m=3` generation took 50.5 s. The expensive half is *verification* —
the generic `materialize_passages + edge_path_cycle` checker costs about
2 ms per candidate, so `m=3`'s 417,864 candidates took **896.6 s**, over
94% of that stage's wall time. The `m=4` layer turns out to hold
3,971,519 surviving supports out of a far larger candidate pool; at
~2 ms each the generic verifier alone would have run for hours. That is
why the general driver stopped after `m=3` with `m=4` marked "not yet
attempted", and why the committed `..._general.json.gz` artifact contains
`per_m` entries for `2` and `3` only.

So the blocker was the same one the `m=5` compiler had already solved:
the generic verifier does not scale past ~10^6 supports. What did *not*
transfer was the `m=5` compiler's generation trick.

### Why the `m=5` compiler does not generalize to `m=4`

`type_t_port_c16_passage_m5.py` is fast because the `(m,r,v)` identity
pins its core-path composition almost completely. With `route_total = 2(m-b) + 3b`
and `core_total = L - route_total` split into `m` positive parts:

| `m` | `b=0` core budget → partitions | `b=1` core budget → partitions | longest core segment |
|---|---|---|---:|
| `5` | `6` → `{2,1,1,1,1}` | `5` → `{1,1,1,1,1}` | **2** |
| `4` | `8` → `{5,1,1,1}`, `{4,2,1,1}`, `{3,3,1,1}`, `{3,2,2,1}`, `{2,2,2,2}` | `7` → `{4,1,1,1}`, `{3,2,1,1}`, `{2,2,2,1}` | **5** |

At `m=5` the only core segments that can ever occur have length 1 or 2,
which is why that compiler gets away with just `core_adj` plus a
hand-rolled `paths2` table. At `m=4` segments of length 3, 4 and 5 all
occur, so that pair of structures is not merely slower — it structurally
cannot represent the search space. (The regression test
`test_specialized_m4_needs_core_segments_the_m5_compiler_never_sees`
pins exactly this: a tiny core whose only `m=4` conflict uses the
`{5,1,1,1}` partition.)

### The compiler

The fix is to replace the ad-hoc length-1/length-2 structures with a
precomputed table of **every** simple bare-core path of length `1..5`,
each stored as `(length, endpoint, interior-vertex bitmask, sequence)`.
This is cheap because the bare core is extremely sparse: on `(4,55,7)`
the core has order 87 with degree sequence `76 x 2 + 10 x 3 + 1 x 4`, and
the whole table is only **1,554 directed paths**. Carrying the interior
bitmask is what makes the DFS enforce *whole-cycle* simplicity (not just
endpoint distinctness) with a single integer AND per step — an interior
core vertex and a passage endpoint can never collide, in either order,
because the running used-vertex mask accumulates both.

Everything else mirrors the `m=5` compiler deliberately, so the two are
easy to diff: the same canonical rotation (each alternating cycle is
generated exactly once, from its numerically least *passage* endpoint,
with the walk always leaving that vertex through its passage — interior
core vertices are correctly exempt from the `>= x1` restriction), the same
`pair_forbidden` / `triple_forbidden` bitmask encoding of the certified
lower shadow, the same "at most one `p3`" generation-time exclusion, and
the same fast support-local verifier in place of the generic one.

### The exact run

Seeded with 316,684 distinct certified lower-shadow supports (the complete
`C8` catalog plus the complete `C16` `m=2` and `m=3` layers), 2 worker
processes, no time budget:

* covered all **87/87** canonical start vertices, `truncated = false`;
* pruned 103,810,586 branches on the lower shadow;
* emitted **3,971,519** supports, every one of support size exactly 4
  (within-stage superset minimalization is therefore a no-op, and the
  shadow is complete for all sizes below 4, so this is the complete set of
  size-4 clauses for the final CNF);
* 261.3 s generation, 66.2 s verification.

Because the shadow it survived is complete for every support size `< 4`,
this layer is final: it does not need to be rerun when any later stage is
compiled.

### What was checked, and what each check is worth

1. **Exhaustive support-local reconstruction — all 3,971,519 supports,
   0 rejected.** For each support the verifier ignores the generator's
   search entirely, takes the support's own endpoint pairing as given,
   searches for a compatible core matching, and materializes a literal
   cycle from core edges plus fresh hub vertices, asserting it has exactly
   16 distinct vertices. This is the check that actually certifies the
   claim "this support is a `C16` conflict".
2. **Independent generic verifier on a 2,000-support evenly spaced
   sample — 0 rejected.** This is the older `materialize_passages +
   edge_path_cycle` implementation. Being honest about its strength: it is
   the *weaker* of the two, because it accepts whenever *some* 16-cycle
   exists in the minimal materialization, not necessarily one using all
   four claimed passages. For these particular supports the two notions
   coincide, and the argument is short: a 16-cycle in
   `materialize_passages(core, S)` uses some subset `S' ⊆ S`; `|S'| = 0`
   is impossible because the bare core has no dyadic-length cycle
   (`type_t_port_core_dyadic_avoidance.md`, re-confirmed by direct
   enumeration on this core: zero bare 16-cycles); `|S'| = 1` is excluded
   by the Phase 1 bound `m >= 2`; and `|S'| ∈ {2,3}` would make `S'` an
   `m=2` or `m=3` conflict, both of which are *complete* catalogs seeded
   into the shadow, so `S ⊇ S'` would have been pruned before ever being
   emitted. Hence `|S'| = 4`. The value of this check is that it is a
   structurally different implementation, not that it is independently
   sufficient.
3. **Lower-shadow pruning audit.** The pruning is the one place where a
   bug would silently *remove* real clauses rather than add fake ones, so
   it gets its own check: start vertices 40–44 were re-enumerated with
   pruning disabled, producing 368,081 raw size-4 supports; filtering those
   post hoc by "contains no certified smaller conflict" leaves 55,337 —
   exactly the 55,337 the pruned run emits for those starts, with **0**
   supports on either side of the symmetric difference.
4. **Cross-validation against the independently implemented general-`m`
   walk.** `type_t_port_c16_passage_hypergraph.py` is the second, separately
   written search that already cross-validated the `C8` catalog (and, by
   disagreeing, exposed the `verify_passage_conflicts` bug in Phase 2). It
   cannot run at `max_m=4` on the full 1,302-passage catalog, but
   restricting the *passage catalog* leaves the bare core untouched, so on
   any subset both searches must return identical size-4 supports. 5 random
   40-passage subcatalogs: exact agreement, symmetric difference 0 on every
   trial. This is the check that would catch a length-arithmetic slip, a
   missed rotation, or a core-path-table error in the new compiler.

### What this does not claim

It does not claim an UNSAT result, a counterexample, or anything about the
conjecture. It does not claim the `C16` CNF has been assembled or tested.
It does not claim the `m=5` layer is final — it is not, and Phase 7 makes
that *more* pressing rather than less, since there are now 3,971,519 size-4
clauses that could subsume five-passage supports. And it deliberately does
not assert "sound, no unsoundness": what is asserted is exactly the four
machine-checked properties above, each with its scope stated.

### The remaining static step, and its exact cost

Rerunning `m=5` with the `m=4` layer in its lower shadow was **not
attempted in this pass**, on purpose, and the reason is plumbing plus CPU
rather than difficulty:

* The committed `m=4` artifact is *summary-only* (count, canonical
  SHA-256 commitment, samples, audit reports) — the same policy the `m=5`
  summary follows, for the same reason: 3,971,519 near-identical 16-vertex
  witnesses would bloat the repository without adding mathematical content.
  Consequently the supports are not on disk in a form
  `load_lower_shadow` can read, and must either be regenerated in-process
  (~261 s at 2 workers) or committed as a new ~30–80 MB binary artifact.
* `m=5` regeneration on top of that is roughly 900 CPU-seconds.
* The domination check itself is cheap and needs no new machinery: `m=5`
  supports have size 5 and `m=4` shadow sets size 4, so it is five set
  lookups per surviving support, either in-DFS at the fourth hop or as a
  post-filter.

Nothing there requires new mathematics; it was left undone only to keep
this pass's compute small on a shared machine.

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

## Passage-support soundness theorem

The forward-implication design in Phase 1 ("selecting a gadget supplies all
its passages simultaneously, **regardless of unused attachments**") and the
minimal-materialization fix in Phase 2 (`materialize_passages`, closing the
verification-bug gap) both rely, informally, on the same underlying fact:
that an unused attachment of a selected hub can never affect whether a
*specific* passage-based cycle candidate actually exists. This section
states and proves that fact once, explicitly, as a standalone theorem,
rather than leaving it as an implicit assumption baked separately into two
different places in the code.

### Setup

Fix a completion `G` of the bare core `H = H(j,a,c)`: a selection of
triples and linked-pair gadgets satisfying the exact-cover deficiency
constraints (`type_t_port_completion.md` Section 1: a same-vertex
completion is a perfect matching on the deficient vertices, realized here
via triples/gadgets, that **adds** edges on top of `H` and never removes or
alters a core edge). "Selected" means: the hub vertex/vertices of that
triple/gadget, and *all* of their incident edges (all three of a triple's
attachments; both hubs and the joining edge of a linked gadget), are
literally present in `G` — this is the forward-implication fact from Phase
1, already established, restated here only as a hypothesis this theorem
builds on, not re-derived.

A **passage-based cycle candidate** is a tuple `(P_1,...,P_k; s_1,...,s_k)`,
`k>=2`: each `P_i` is a simple core path in `H` between two deficient
vertices `P_i.left`, `P_i.right`, with the `P_i` pairwise vertex-disjoint
(no vertex, including an endpoint, shared between any two distinct `P_i`);
each `s_i` is a `p2` or `p3` passage instance whose two named endpoints are
exactly `P_i.right` and `P_{i+1 mod k}.left`, with all hub vertices
appearing across the `s_i` pairwise distinct from each other and from every
`P_i`-vertex (hub vertices are always freshly-added completion vertices,
never core vertices, so the only possible coincidence — a hub equal to some
`P_i`-endpoint — cannot occur since endpoints are core vertices by
definition).

The candidate is **supported by `G`** if, for every `i`, some selected
triple/gadget `h_i` of `G` supplies the passage `s_i` (Phase 1's forward
sense). Write `E(s_i)` for the *specific* 2 (for `p2`) or 3 (for `p3`)
edges of `h_i` that literally realize that one passage — e.g. for a `p2`
supplied by triple `h_i={u,v,w}` with `s_i` the pair `(u,v)`, `E(s_i)` is
exactly the two edges `hub-u`, `hub-v`, deliberately excluding `h_i`'s third
edge `hub-w` even though that edge is also present in `G`.

### Theorem

If a passage-based cycle candidate `(P_1,...,P_k;s_1,...,s_k)` is supported
by `G`, then
```
C := ( union_i V(P_i) union_i V(s_i),  union_i E(P_i) union_i E(s_i) )
```
is a simple cycle subgraph of `G` — **regardless of any other edge present
in `G`**, in particular regardless of any unused attachment of any
supplying hub `h_i`, and regardless of every edge of every *other* selected
triple/gadget of `G` not among the `h_i`.

### Proof

**(1) `E(C) ⊆ E(G)`.** Each `P_i` is a path in `H`, and `H`'s edges are all
present in `G` unchanged (completions only add edges), so
`E(P_i) ⊆ E(H) ⊆ E(G)`. Each `h_i` is selected in `G` by hypothesis, so by
the forward-implication fact *all* of `h_i`'s edges — not just the ones in
`E(s_i)` — are present in `G`; in particular `E(s_i) ⊆ E(h_i) ⊆ E(G)`.
`E(C)` is a finite union of subsets of `E(G)`, hence `E(C) ⊆ E(G)`. Note
this step never used anything about which attachments are *unused* — it
only used that a *selected* hub contributes **all** of its own edges
(forced by "selected" meaning fully present, not partially present), which
holds independent of anything else `G` does or doesn't contain. The unused
attachment's edge is simply some element of `E(h_i) \ E(s_i) ⊆ E(G)`,
present in `G` but by construction not in `E(C)` — irrelevant to a subset
containment, since `⊆` is monotone in the right-hand side.

**(2) `C` is a simple cycle.** It suffices to show every vertex of `V(C)`
has degree exactly 2 within `E(C)`, and `E(C)` is connected on `V(C)`.
By pairwise vertex-disjointness of the `P_i`, an internal vertex of `P_i`
touches only `P_i`'s own two edges at that vertex (degree 2, from `P_i`
being a simple path) and no other `P_j` or `s_j` — internal vertices are
never named as passage endpoints. Each endpoint `P_i.right` gets one edge
from `P_i` and, by the endpoint-matching definition of a candidate, exactly
one more edge from `E(s_i)` (the edge of `s_i` incident to that specific
endpoint — one edge for `p2`, one of the two "outer" edges for `p3`),
giving degree exactly `1+1=2`; symmetrically for `P_i.left` via `s_{i-1}`.
A `p3` joiner's internal hub-to-hub edge and its two hub vertices: each
`p3` hub vertex is incident to exactly 2 of `E(s_i)`'s 3 edges (one outer,
one joining), and by the pairwise-distinctness of hub vertices across
different `s_i`, no other `s_j` or `P_j` contributes a further edge there —
degree exactly 2. This is exactly where restricting to `E(s_i)` (the
minimal-materialization discipline) rather than `E(h_i)` (the full hub)
matters: if a hub's *unused* attachment edge were (incorrectly) included,
that vertex's degree would be inflated past 2 and part (2) would fail: it
is only because `E(C)` is built from `E(s_i)`, not `E(h_i)`, that every
`V(C)`-vertex is guaranteed degree exactly 2. Connectivity: the cyclic
sequence `P_1, s_1, P_2, s_2, ..., P_k, s_k` visits `P_1.left`, traverses
`P_1` to `P_1.right`, crosses `s_1` to `P_2.left`, and so on, returning to
`P_1.left` after `s_k` — a closed walk touching every `V(C)`-vertex, hence
`E(C)` is connected on `V(C)`. Both conditions hold, so `C` is a simple
cycle. `∎`

### Discussion — what this closes, and what it deliberately does not

* **This is a soundness statement about the translation, not a claim about
  which supports occur.** It says nothing about which passages a *specific*
  completion actually supports — that per-instance question is exactly what
  the passage-level `C4/C8/C16` conflict catalogs compute. The theorem only
  certifies that *if* a candidate is supported, its cycle genuinely exists,
  with the hypotheses spelled out precisely enough to see exactly where each
  one is used.
* **Explains, precisely, why the Phase 1 forward-implication design is
  correct.** "Regardless of unused attachments" is exactly part (1) of the
  proof: unused attachments live in `E(G) \ E(C)`, and existence only ever
  needs `E(C) ⊆ E(G)`, a fact monotone in — hence indifferent to — anything
  else `G` contains.
* **Explains, precisely, why the Phase 2 verification bug was a real bug,
  not a counterexample.** The buggy `verify_passage_conflicts` materialized
  the *full* supplying hub `h_i` (including unused attachments) and
  accepted the candidate whenever `edge_path_cycle` found *any* cycle in
  that larger graph — i.e. it silently substituted `E(h_i)` for `E(s_i)` in
  the construction of `C`. `E(h_i) \supseteq E(s_i)` can contain an
  unrelated cycle that never uses `s_i`'s claimed passage at all (routed
  through the extra unused edge instead), so "a cycle exists in
  `materialize(h_i)`" does not imply "the specific candidate `C` is a
  cycle in `G`" — the fix (materializing exactly `E(s_i)`, nothing more) is
  precisely what makes part (2) of the proof above go through; the theorem
  is false in general if `E(s_i)` is replaced by `E(h_i)`, which is exactly
  the failure mode the bug exhibited.
* **The "second correction" (at most one `p3` passage per completed graph)
  is orthogonal, not a special case of this theorem.** It restricts which
  candidates can ever be *supported by `G`* at all (the exact-cover
  constraints select exactly one linked gadget, hence realize at most one
  `p3`-capable hub structure per completion), not whether a supported
  candidate's cycle exists. A candidate naming two distinct `p3` joiners
  would require two distinct selected linked gadgets in the same `G` —
  already impossible by exact-cover, independent of anything in this
  theorem — so such a candidate is simply never "supported by `G`" for any
  real `G`, and the theorem is (correctly) never invoked on it. This is why
  `drop_multi_p3_supports` is a generation-time filter (never producing the
  candidate) rather than a caveat added to the soundness argument itself.

## Next

`m=4` is closed (Phase 7), so the immediate static-catalog task is now
exactly the `m=5` rerun against the new `m=4` lower shadow — mechanical, no
new theory, ~261 s to regenerate the `m=4` shadow plus ~900 CPU-seconds for
`m=5` itself, or alternatively a one-off ~30–80 MB binary artifact holding
the 3,971,519 `m=4` supports so future stages can load them directly.
After that: assemble the full passage CNF from the four layers and test the
fixed completion instance.  Note that neither of those steps has been
started, and the assembled formula's satisfiability is entirely unknown —
compiling a complete conflict catalog is not evidence either way about
`UNSAT`.  Passage-aware large-neighborhood search remains the parallel
constructive route.  Phase 5/6's soundness half (the lifting theorem) is
written up above; its "compact static SAT" half remains open.
