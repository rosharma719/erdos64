# Type-T port passage-level symbolic templates

**Status (2026-07-29): TEMPLATE_CONJECTURE.** This picks up
`type_t_port_c16_passage_projection.md` where it stopped: the passage-level
`C8`/`C16`(`m=2`) conflict catalogs are now themselves quotiented by the
translation/reflection symmetry the branch structure obviously has. The
headline result: **the "same-mode" (non-anchor-crossing) fraction of both
catalogs collapses to a handful of universal, `j`-independent symbolic
templates (6 for `C8`, 22 for `C16` `m=2`), derived from first principles
and independently verified by construction at fresh `j=4` and `j=5`
coordinates. The "crossing" (anchor-junction) fraction does NOT collapse —
hundreds to thousands of instance-specific templates, a genuine negative
result.** Net assessment at the end of this file.

**Corrected-catalog note.** This file uses the catalogs *after* commit
`8617422` ("Exclude structurally-vacuous two-p3-passage supports"),
identified via external mathematical review mid-session: a completed graph
selects **exactly one** linked-pair gadget ever, hence has **exactly one**
`hub_L`-`hub_R` joining edge in existence, so two *different* `p3` passages
can never coexist in one simple cycle (both would need to traverse that
single edge). Corrected clause counts: `C8` `4,218`/`4,227`/`5,432` (was
`5,007`/`5,044`/`6,359`) for `(4,55,7)`/`(4,2,2)`/`(4,28,4)`; `C16` `m=2`
`32,921` (was `40,833`) for `(4,55,7)`. This is now encoded directly in the
first-principles derivation (`enumerate_bulk_shapes` /
`enumerate_same_mode_abstract_shapes` exclude `route1==route2==3`), not
just filtered post hoc.

## Phase 0 — coordinate audit (`verifier/type_t_port_coordinates.py`)

`build_core(j,a,c)` already bakes a full symbolic addressing scheme into
its vertex *labels*: 13 fixed anchors (`ANCHORS`, including `u_x`/`u_y`,
which are anchors *and* deficient — degree-2 "bridge" vertices sitting
directly between `r_x`/`s_x` resp. `r_y`/`s_y`, bypassing the 7-edge
`A_middle`/`C_middle` path) and 19 named subdivided paths between them
(`PATH_SPEC`), with every internal vertex literally labeled
`f"{path}:{index}"`.

**Formalized and PROVED**, checked exhaustively (not sampled) on all three
`j=4` catalog instances plus one fresh `j=5` instance
(`build_core(5,40,10)`):

* `parse_label` / `label_of` round-trip every label.
* `path_length(path,j,a,c)` matches the materialized path length for all
  19 paths.
* `symbolic_adjacent(u,v,j,a,c)` — "same named path, index differs by
  1" — reproduces materialized bare-core adjacency **exactly** for every
  `O(n^2)` ordered pair of distinct labels, not just for real edges.
* `distance_to_nearest_anchor` matches true BFS shortest-path distance to
  the nearest of the 13 anchors, for every vertex. This is provable
  directly from the construction, not just checked: every path-internal
  vertex has degree exactly 2 with both neighbors on the *same* path (no
  other `add_path` call ever names that vertex), so leaving it toward one
  end must pass through that end's anchor before reaching anything else.
* The 13-anchor/19-path **skeleton topology never changes with `j`** —
  only 4 of the 19 length formulas (`A_left=a-1`, `A_right=4Y-8-a`,
  `C_left=c-1`, `C_right=Y-8-c`) depend on `Y`/`a`/`c`; the other 15 are
  fixed integer constants (`GROWING_PATHS`/`PATH_SPEC`).
* `A_left + A_right = 4Y-9` and `C_left + C_right = Y-9` **identically**,
  for every valid `(j,a)` resp. `(j,c)` — only the *split* between the two
  varies with `a`/`c`. This is the load-bearing fact behind Phase 6.

Run: `PYTHONPATH=verifier .venv/bin/python verifier/type_t_port_coordinates.py`.

## Phase 1 — symbolic passage features (`verifier/type_t_port_passage_templates.py`)

Every `m=2` conflict's witness cycle (`{"support": [[kind,[u,v]], ...],
"witness": [...]}`) decodes deterministically into two alternating
core-path runs and two hub-passage runs (`split_witness` / cyclic-wraparound
handling, cross-checked against `support` on **every** clause in all four
catalogs — `13,877` `C8` clauses + `32,921` `C16` `m=2` clauses, zero
mismatches). Each core-path run is classified `same` (stays on one named
path — the only bulk-eligible shape) or `cross` (touches >=1 anchor mid-run,
spanning >=2 named paths). Each endpoint gets a symbolic tag: `anchor` (one
of the 13), `bulk` (path-internal, distance `>12` from *both* bounding
anchors — the proved `C16` total-core-path-length bound), or `near`
(path-internal, distance `<=12`, with an explicit offset).

Re-deriving the `A_middle`/`C_middle` note from the task setup: because
`A_middle`/`C_middle` have fixed length 7 and `B_right`/`D_right` fixed
length 3, **no vertex on those four fixed-length paths can ever be `bulk`**
(max internal distance to nearest anchor is 3 or 1) — every deficient
vertex on them is necessarily a boundary vertex. Bulk vertices can only
occur on the four growing branches (`A_left`, `A_right`, `C_left`,
`C_right`), and only once that branch's length exceeds 24.

## Phase 2 — quotient the `C8` catalog

Two independent quotient layers, both applied via a single symmetry group
(`canonicalize_cyclic`: rotate-by-2 + reflect, order 4 — the natural
symmetry of an `m=2` witness's "which passage is first / which reading
direction"):

* **Raw (offset-preserving) templates** — collapses only rotation/reflection.
  `569`/`617`→ now `449`/`480`/`5,331` templates for `4,218`/`4,227`/`5,432`
  clauses (`(55,7)`/`(2,2)`/`(28,4)`). Of these, `3`/`3`/`1` are
  **raw-bulk** (all 4 endpoints `>12` from every anchor, both core paths
  `same`) — `189`/`189`/`1` clauses. The compression here is modest and
  instance-dependent, exactly the ratio at which a branch happens to have
  deep-bulk room in that particular `(a,c)`.

* **Abstracted (branch-name-wildcarded, offset-dropped) templates** — the
  translation-quotient proper. `55`/`59`/`197` total abstract templates.
  Splitting by whether either core path crosses an anchor:

| `(j,a,c)` | clauses | same-mode clauses | same-mode abstract templates | crossing clauses | crossing abstract templates |
|---|---:|---:|---:|---:|---:|
| `(4,55,7)` | 4,218 | 3,672 (87%) | **6** | 546 (13%) | 49 |
| `(4,2,2)` | 4,227 | 3,665 (87%) | **6** | 562 (13%) | 53 |
| `(4,28,4)` | 5,432 | 3,896 (72%) | **6** | 1,536 (28%) | 191 |

The **6 same-mode abstract templates are literally identical (set
equality) across all three instances** — a robust, `j=4`-parameter-choice-
independent finding. The crossing templates are **not** shared well:
`|T_{55,7} ∩ T_{2,2}|=21` (of 49/53), `|T_{55,7} ∩ T_{28,4}|=39` (of
49/191), `|T_{2,2} ∩ T_{28,4}|=48` (of 53/191), union over all three `=206`.

## Phase 3 — first-principles derivation, cross-checked for completeness

`enumerate_same_mode_abstract_shapes(target_length)` derives the same-mode
template set **without reading any catalog**: exhaustively case-splits
`route1,route2 in {2,3}` (`p2`/`p3`), **excluding `route1==route2==3`**
(structurally vacuous — see the correction note above; a global exact-cover
fact, not derivable from cycle-length arithmetic alone, which is why it is
encoded as an explicit exclusion rather than falling out of the arithmetic),
`l1,l2 >= 1` summing to `target_length - route1 - route2`, and two branch
arrangements (same-branch / cross-branch), all quotiented by the identical
`canonicalize_cyclic` symmetry used on real data.

**For `target_length=8`: exactly 6 templates** — three arithmetically
distinct `(route1,l1,route2,l2)` compositions (`{2,1,2,3}`/`{2,3,2,1}`
merge; `{2,2,2,2}`; `{2,1,3,2}`/`{2,2,3,1}`/`{3,1,2,2}`/`{3,2,2,1}` merge)
× {same-branch, cross-branch}.

**Completeness, PROVED not just clustered**:
`set(enumerate_same_mode_abstract_shapes(8)) == union of realized
same-mode abstract keys across all three corrected j=4 catalogs` — literal
Python set equality, checked directly (not by re-implementing a parallel
notion of "same").

**Genuineness, COMPUTATIONALLY_CERTIFIED**: every one of the 6 templates
independently instantiated at *fresh* coordinates (not drawn from any
catalog) via `instantiate_same_branch`/`instantiate_cross_branch`, both in
a `j=4` instance and a fresh `j=5` instance (`build_core(5,64,16)`,
`build_core(5,30,4)` for cross-branch), and verified with
`materialize_passages` + `edge_path_cycle` (the project's own trusted
minimal-materialization method, not a re-implementation) — `64/64` checks
passed once branch-length availability was accounted for.

## Phase 4 — the `C16` `m=2` catalog (32,921 clauses)

Same machinery, `target_length=16`, one available instance `(4,55,7)`.

| | clauses | abstract templates |
|---|---:|---:|
| total | 32,921 | 3,269 |
| same-mode | 5,292 (16%) | **21** (of 22 derived) |
| crossing | 27,629 (84%) | 3,248 |

`enumerate_same_mode_abstract_shapes(16)` derives **22** templates
(`route1,route2 in {2,3}` minus `{3,3}`, `l1,l2>=1` summing to
`16-route1-route2 <= 12`, × {same-branch, cross-branch}); **21 are
realized** in the one available instance (the missing one is data
sparsity, not incompleteness — `realized ⊆ derived` is exact, i.e.
soundness holds unconditionally and completeness holds up to sampling).

**The crossing/junction fraction dominates `C16` `m=2` far more than `C8`**
(84% vs 13-28%) — expected, since `C16`'s core-path budget (up to 12) gives
far more room to wander through multiple named paths before closing, and
does **not** collapse (3,248 templates for 27,629 clauses, essentially no
multiplicity).

## Phase 5 — incremental ingestion design

`decode_general_witness` / `build_cyclic_tokens` / `canonicalize_cyclic_general`
generalize the `m=2`-specific pipeline to arbitrary `m` (dihedral symmetry
of order `2m` instead of the fixed order-4 group). **Regression-tested**:
`general_conflict_keys` reproduces the specialized `m=2` pipeline's raw and
abstract keys **exactly** on all `46,798` real conflicts across the four
corrected catalogs (0 mismatches) — the sibling agent's `m=3,4,5` output
can be folded in later by writing one more decoder (`m` core/hub run pairs
instead of 2) and reusing every downstream function (`vertex_tag`,
`core_path_descriptor`, `wildcard_branch_names`, clustering) unmodified.
Branch-name wildcarding for `m>2` is explicitly flagged as a Phase-7+
extension, not yet implemented (only `m=2` currently produces an
`abstract_key`).

## Phase 6 — lifting theorem

**Restriction (PROVED by construction)**: `enumerate_same_mode_abstract_shapes(L)`
takes only `L` as input — never `j`, `a`, or `c` — so the same-mode
template set for a fixed length is *identical* for every instance. Any
catalog at any `j`, decoded through the identical parameter-free pipeline,
can only land on one of these keys. A `j>=5` instance's same-mode conflicts
therefore restrict to the `j=4` template set by construction, not by
sampling.

**Embedding threshold (derived, not assumed-periodic)**: using
`A_left+A_right=4Y-9`/`C_left+C_right=Y-9`, the worst-case `a`/`c` (the one
balancing the family's two branches as evenly as possible) gives
`max(branch1,branch2) = ceil(budget/2)`. A same-branch shape with core-path
lengths `l1,l2` needs branch length `>= 27+l1+l2` to be *bulk-classified*
(translation-free — genuinely far from every anchor, matching the `is_bulk`
flag used in Phase 2). Solving for the minimal `j` guaranteeing the *full*
bulk-classified same-branch template set embeds for **every** valid `a`/`c`
(not just the tested instances):

| | `C8` (max `l1+l2=4`) | `C16 m=2` (max `l1+l2=12`) |
|---|---:|---:|
| A-family min `j` | **5** | **5** |
| C-family min `j` | **7** | **7** |

The C-family needs substantially larger `j` because its total growing
budget (`Y-9`) is 4x smaller than the A-family's (`4Y-9`) at the same `j` —
this is why **none** of the three tested `j=4` instances has *any*
C-family bulk vertex at all, and stress-tested directly:
`stress_test_same_branch` at `j=4,5,6,7` for both families confirms the
derived thresholds exactly (`C_family: all_ok` first becomes `True` at
`j=6` in the constructed stress instance, `j=7` is the *guaranteed-for-
every-c* threshold — the stress instance's specific `c` happened to clear
the bar one `j` early, which is expected since the threshold is a
worst-case-over-`c` guarantee, not a per-instance one).

**A separate, much weaker "mere existence" threshold** (`length >=
l1+l2+3`, no anchor-clearance requirement) explains why the *same* 6/22
same-mode template sets were already found complete even in the `(28,4)`
instance, whose growing branches never reach the deep-bulk (`>12`) regime
at all — same-mode template existence needs only that the branch has *any*
room for the raw coordinates, not that they land far from anchors.

**Scope clarification (important, added after a mid-session external
review raised a related question — see below).** This proves the *same
finite conflict-clause template set* continues to arise as valid, sound
constraints once `j` clears the derived threshold — a structural fact
about which clauses exist. It does **not** claim (and does not need) that
the overall exact-cover SAT instance is forced UNSAT for large `j`; that is
a distinct, harder, global combinatorial question, and is not in conflict
with this result (a growing number of local conflict clauses is fully
compatible with the whole system remaining satisfiable).

### A mid-session external-review note (audited, not accepted on faith)

An external mathematical review raised a "finite-horizon hub-completion
lemma" (random-partition + lopsided-Lovász-Local-Lemma argument that, for
graphs like this family, *some* completion avoiding any fixed finite
forbidden-length set exists for all sufficiently large `n`) and asked
whether it undercuts this file's lifting goal. Audited directly against
this repository:

* **Precondition — bounded max degree, independent of `j`: PROVED.**
  Checked exhaustively on all three `j=4` instances (max degree `4`) and
  provable directly from the construction: the 13-anchor/19-path skeleton
  topology never changes with `j` (Phase 0), so every anchor's degree is a
  fixed count of incident named paths and every subdivision vertex has
  degree 2, for every `j`.
* **Precondition — bare core `H(j,a,c)` avoids `C4,C8,C16` for all
  sufficiently large `j`: UNKNOWN**, matching `type_t_port_completion.md`'s
  own existing "PARAMETRIC FAMILY OPEN" status (checked computationally
  for `j=4,5,6` only, not proved for all `j`). Not resolved here for lack
  of remaining time; one relevant structural fact established in passing:
  a bare-core cycle that traverses an entire growing branch end-to-end
  (`A_left` then `A_right`, or `C_left` then `C_right`) has length
  *independent of `a`/`c`* (the `-a`/`+a` terms cancel: `(a-1)+(4Y-8-a) =
  4Y-9`), while a cycle using only one growing branch partially *does*
  depend on the specific `a`/`c` chosen — so whether a dyadic bare-core
  cycle is avoidable is a genuine per-`(a,c)`-choice question, not
  automatic for all parameter choices.
* **This file's Phase 6 result is not threatened either way** — see the
  scope clarification above: it is about template recurrence, not SAT/UNSAT
  of the whole system, so it does not depend on resolving the open
  precondition.

## Phase 7-9 — transfer automaton

**Not attempted** (stretch goal, explicitly optional per the task; Phases
0-6 consumed the available time, plus a mid-session audit of an externally
raised question). Starting point for a future session: state = unfinished
same-mode/crossing passage obligations within core-distance 12 of the
current cut along the 13-anchor skeleton; transitions = the 19 named paths
with their length formulas (15 fixed constants, 4 growing); the Phase 0
coordinate module and Phase 2-4 template catalogs
(`data/type_t_port_templates/*.json.gz`) are the direct inputs this would
consume without re-deriving anything.

## Headline numbers (as requested)

* **`C8`: 6 genuinely distinct symbolic templates** explain the same-mode
  fraction (81% of the corrected 13,877-clause union across three `j=4`
  instances) — PROVED complete, COMPUTATIONALLY_CERTIFIED genuine, and
  PROVED to lift to every `j` clearing a derived, family-specific threshold
  (`j>=5` A-family, `j>=7` C-family). The remaining 19% (crossing/junction)
  needs **49-191 instance-specific templates**, poorly shared across
  instances (21-48 of 49-191 pairwise overlap) — does not collapse.
* **`C16` `m=2`: 22 templates** (21 realized in the one available instance)
  explain only 16% of the 32,921-clause catalog; the dominant 84%
  (crossing) needs **3,248 templates**, essentially no multiplicity —
  does not collapse, and is proportionally *worse* than `C8`'s crossing
  fraction, not better.
* **Net assessment**: the compression trend from gadget-level →
  passage-level (107-207x) does **not** continue cleanly into a full
  symbolic-template collapse. The same-mode substructure is a clean,
  provable, `j`-lifting-ready partial result (small, stable, derivable from
  first principles). The crossing/junction substructure — which *dominates*
  by clause count at `C16`'s scale — genuinely does not collapse with the
  symmetry available here, and would need much harder, anchor-by-anchor
  case analysis to template at all. This is a real, valuable negative
  result for the crossing fraction, and a real, valuable positive result
  for the same-mode fraction; taken together, they argue for
  **deprioritizing a full all-`j` proof via template counting** for this
  completion family, while keeping the same-mode result as a genuinely
  useful, reusable structural fact.

## Deliverables

* `verifier/type_t_port_coordinates.py` — Phase 0 coordinate module + self-test.
* `verifier/type_t_port_passage_templates.py` — Phase 1-5 feature extraction,
  clustering, first-principles derivation, general-`m` infrastructure.
* `verifier/type_t_port_template_lift_check.py` — Phase 6 threshold
  derivation + stress tests.
* `verifier/export_templates.py` — writes
  `data/type_t_port_templates/c8_templates.json.gz` and
  `data/type_t_port_templates/c16_m2_templates.json.gz`.
* `manifests/type_t_port_template_manifest.json` — machine-readable summary.
