# erdos64 — Erdős–Gyárfás conjecture (Erdős Problem #64)

Self-contained, autonomous research attempt on:

> **Conjecture (Erdős–Gyárfás, 1995).** Every finite simple graph with minimum
> degree ≥ 3 contains a simple cycle whose length is a power of two (4, 8, 16, …).

Status: **OPEN.** This folder is independent of the I(4)/intersecting-family
work in the sibling `erdos/` directory — no shared code.

## Layout
- `plan.md` — strategy, rankings, status log, failed/blocked approaches.
- `literature.md` — verified frontier (P₁₃-free, diameter-2, Carr 2026 minimal-
  counterexample structure, Royle–Markström bounds), with a master table.
- `lemmas.md` — candidate lemmas with status labels; Track-B/Track-C results.
- `experiments.md` — every run: command, params, output, interpretation.
- `verification_status.md` — theorem/experiment verification matrix, including
  explicit `NOT_FORMALLY_VERIFIED`, missing-data, and incomplete-range labels.
- `proof.md` — current rigorously-established progress vs. conjectural notes.
- `defect.md` — **arbitrary-order redirection (2026-07-25):** the
  ordering-defect parameter D, S4/S5 bridge/cut-vertex proofs summary,
  and the disproof of the literal "n≤2D+3" central target.
- `one_pole.md` — **rooted one-pole gadget theory (2026-07-25, current top
  priority):** O1–O3 prove a master-minimal one-pole graph is fully
  2-connected; **O5 proves it always has a K4-minor (unconditional rigid
  core)**; O4′ gives an admissible-path corollary (cited theorem); O4a +
  the terminal-spectrum identity give the exact failure structure and
  two-terminal doubling criterion; the suppressed-edge reformulation gives
  an exact edge-rooted equivalent search target.
- `manuscript.md` — **structural manuscript draft (2026-07-25, one-pole
  sections FROZEN):** pulls together S4, S5, O1, O3, O4a, O4′, O5, O6, O7,
  and the suppressed-edge equivalence into a single citable write-up.
- `two_cut.md` — Type A/B/C two-cut theory through T1–T6 and the exact
  remaining SPQR/replacement boundary; 3-connectivity remains conjectural.
- `s6_case_tree.md` — exact Type A/B/C dependency tree, the proved
  spectrum-safe replacement principle, its scope boundary, and the first
  unseen genuine leaf-R configuration.
- `z3_lifts.md` — normalization, completeness, implementation, and exact
  elimination statement for cyclic Z3 lifts of the four certified bases;
  Part III's algebraic compression (projection-type classification,
  full-space hyperplane coverage, compact standalone certificate) and
  Part IV's Z3-vs-Z5/order-26 feasibility comparison.
- `contraction.md` — **contraction-criticality endgame (2026-07-26):**
  the near-power edge lemma (every nontriangle edge of a minimal
  counterexample lies on a `2^k+1`-cycle), the safe-contraction
  obstruction (no safe nontriangle edge ever exists — the naive "safe
  edge" target is logically equivalent to the conjecture itself, not an
  easier sub-target), the exact `{1,3}` nontriangle-edge count at every
  cubic vertex, and one proved-forbidden clean near-power-cycle overlap
  configuration.
- `contraction_atoms.md` — **contractible-atom generalization
  (2026-07-27):** the general atom-lifting lemma (`2^k+r` for
  any connected atom `A` satisfying (H2)/(H3)), specialized to recover
  the edge lemma and to a new triangle-pair lemma (`2^k+1,2^k+2` from
  every C4-free triangle, automatically, no edge selection needed); the
  Type N/Type T local cubic-vertex dichotomy; a five-lemma arithmetic/
  gluing toolkit applied to both Type N orientation types (functional-
  digraph classification: exactly 2 isomorphism types) and to Type T,
  yielding finite exact constraint lists rather than a contradiction for
  either type; and a bridge-arithmetic chord corollary. The general
  (non-clean-overlap) case, `(a,b)`-only triangle attachment, multi-
  cubic-vertex-triangle interaction, and the separator/crossing bridge
  classification all remain explicitly open, recorded as concrete next
  steps rather than a vague list.
- `contraction_neighborhood.md` — **closed-neighborhood contraction
  (2026-07-27):** `A=N[v]` for a cubic `v` is
  always a valid atom ((H2)/(H3) automatic, and `v` itself is provably
  never a boundary attachment vertex), giving the cubic power-path
  lemma CN1 (every cubic vertex sits on a `2^k+2`-cycle) and, at Type T
  vertices, a second pair of near-power offsets `\{2^k+1,2^k+2\}` or
  `\{2^k+2,2^k+3\}` depending on the attachment pair. Establishes the
  exact relationship to the independent triangle-contraction witness
  (same internal-path content at the shared `(a,b)` pair; genuinely new
  content at `(a,c)`/`(b,c)`; exponents not assumed to coincide).
- `contraction_mixed_witness.md` — **mixed power/near-power path systems
  at a Type N vertex (2026-07-27):** derives, by
  orbit-counting (not labelled enumeration), exactly four combined
  endpoint orbits (T1, T2a, T2b, T2c) for the joint nontriangle-edge and
  closed-neighbourhood witnesses at a Type N vertex, then resolves the
  exact cycle-length arithmetic of every clean configuration in all four
  orbits — the NPT theta (T1, T2b), a 4-branch fan (T2a), and
  vertex-hub/closed-triangle merges (T2c, which has no direct theta).
  **Every single combination is unconditionally safe for every exponent
  choice** (two new arithmetic lemmas proved for this pass); the clean
  local system alone never forces a contradiction at a Type N vertex,
  motivating the shift to theta-saturation as the next target.
- `contraction_intersections.md` — **decomposing non-clean witness
  intersections (2026-07-27):** proves the exact
  cell-decomposition identity for two same-endpoint paths in the
  non-crossing case (`|P|-|Q|=\sum` over divergent cells, each yielding
  a genuine cycle `\alpha_i+\beta_i`; common-component cells yield no
  cycle); tests and **disproves** the "canonical witnesses always give
  one cell" target with an explicit smallest obstruction (0 shared
  edges/components, still 2 divergent cells); classifies three
  non-crossing intersection-diagram types exactly. The crossing case is
  left explicitly open — uncrossing is named as the applicable
  technique, but its hypotheses are not verified to hold here, and no
  crossing instance is claimed resolved.
- `contraction_saturation.md` — **theta-bridge saturation and the Type
  T system (2026-07-27):** defines theta bridges
  precisely and reduces single-branch-pair bridges to the existing
  near-power-cycle chord machinery; proves a genuine new connection to
  **S5** (at most one theta-internal vertex, out of `\ge6` and growing,
  can be saturated by a single-attachment bridge without creating a
  second cut vertex, which S5 already forbids) — a real quantitative
  narrowing, not a full saturation proof. Derives the complete 3-formula
  same-branch and 4-formula cross-branch bridge arithmetic (VI.3/VI.4,
  new). Extends the NPT-theta safety mechanism to Type T vertices
  (VII.2). Honestly reports what is NOT resolved: VI.5's saturation
  target, VII.3's multi-cubic-vertex-triangle interaction (the
  highest-value remaining Type T question), and V.3's crossing case —
  each named as a precise next step, with no `q=4` census, defect
  bound, or voltage search substituted for genuine progress.
- `contraction_central_bridge.md` — **the central-bridge lemma and
  topological-K4 reduction (2026-07-27):** CB1
  (PROVED, by direct citation of S5): the theta bridge carrying the
  cubic center's third edge can *never* be single-attachment, since
  `v`'s own degree (3) already contradicts S5's forced degree-4 for any
  cut vertex — sharper than the prior session's general "at most one"
  bound. Splits the return location into endpoint-return (an exact
  normal form, no contradiction) and interior-return, which is PROVED to
  form a genuine topological-`K_4` subdivision with an exact seven-cycle
  table — three of the seven collapse immediately to already-proved
  safe lemmas (Lemma E, Lemma F, and simple parity), leaving four
  genuine open `(\ell,d)`-dependent conditions recorded as a compact
  theorem table. Establishes the first-excursion containment fact and
  a one-directional length bound relating the canonical return path to
  the third-edge witness; tests the "one-excursion" target (CB2) and
  finds it structurally unsupported (a genuine two-excursion
  configuration is exhibited, though not certified canonical/minimal),
  the correct honest replacement for last phase's disproved "one-cell"
  claim.
- `contraction_separator_integration.md` — **separators, admissible
  paths, and Type T integration (2026-07-27):**
  refines the task's proposed CB3 into **CB3′**, the sharper correct
  dichotomy: a clean 2-attachment central bridge reduces, by direct
  citation, to `two_cut.md`'s already-proved T1 (2-connectivity) and T2
  (two admissible paths, via Gao–Huo–Liu–Ma) with no new proof needed;
  the failure modes are exactly an S5 cut vertex, or — the genuinely new
  case the original formulation missed — `\ge3` theta attachments,
  which causes real internal-degree loss when restricted to 2 terminals
  and cannot be misfiled under Type A/B/C (a 2-terminal classification).
  Derives the paired topological-`K_4` union arithmetic from T2's two
  admissible paths (always safe at offset 1; excludes `\ell=2^j-1`
  exactly at offset 2). Proves a sharp `pq`-edge consequence via direct
  citation of T4 (if `pq\in E(G)`, some theta bridge must be
  cross-branch) and maps the no-cross-branch case exactly onto Type A's
  already-recorded dependency chain in `s6_case_tree.md`. Honestly
  reports the joint two-central-bridge Type T analysis (this file's own
  highest-value target) as not attempted.
- `contraction_block_cut_tree.md` — **resolving the multi-attachment
  obstruction via block-cut trees (2026-07-27):**
  builds the attachment core `T_A(B)` (minimal subtree of `B`'s
  block-cut tree spanning every marked block) and proves its five basic
  properties; proves the attachment-free-leaf case reduces to one exact
  S5 configuration (`z` cut vertex, exactly 2 of its 4 edges into the
  leaf, equal-order/equal-size lobes forcing the leaf to be as large as
  the rest of the graph); proves MA1 (a singly-marked leaf, once shown
  not to be a bare edge, gives a genuine 2-connected `R+xz` with full
  internal degree, licensing the admissible-path theorem and extending
  its two paths through a second attachment). Proves **MA2**, the
  central-bridge trichotomy — and sharpens it in the proving: outcomes
  (1) or (3) alone already exhaust every case, from the mere existence
  of a marked leaf in the (always-nonempty) attachment core; outcome (2)
  is real but not needed for completeness, stated honestly rather than
  silently dropped or overclaimed as load-bearing.
- `contraction_leaf_blocks.md` — **arithmetic of admissible pairs and
  attachment-rich leaves (2026-07-27):** the
  endpoint-location route census (three routes same-branch; four-to-six
  different-branch; the theta's own `p`-`q` spectrum when both
  attachments are poles) feeds a compact finite excluded-residue
  template family — no contradiction claimed, as expected. Resolves
  MA2's outcome (3) further: the shared-port sub-case gives an exact
  arithmetic template (`2^m-2}`); the distinct-port sub-case is proved
  to reduce **directly** to the same admissible-pair mechanism as
  outcome (1) — with `x,y` themselves as the admissible-path theorem's
  terminals, no auxiliary construction needed — meaning Part VIII's
  proposed "port-saturated block" classification **is not generically
  necessary**, a genuine simplification found by working the
  construction through rather than assumed.
- `contraction_ma2_integration.md` — **S5 integration, Type T setup,
  and final assessment (2026-07-27):** integrates
  the central-bridge-induced S5 configuration precisely (which lobe
  holds `\Theta`, which holds the attachment-free leaf, exact lobe
  signatures) without reopening `lemmas.md`'s general cut-vertex
  program; sets up the joint two-central-bridge Type T interaction's
  five priority questions with MA2's full machinery now available,
  honestly reporting none resolved — the single most consequential open
  target across this entire six-file contraction-phase sequence.
  Closes with: MA2 proved, every one of its three outcomes reduced to
  an exact named obstruction (an admissible-pair arithmetic template, a
  shared-port arithmetic template, or one precise S5 lobe-equality
  configuration) — neither Type N nor Type T eliminated.
- `central_bridge_templates.md` — **frozen A/P/S single-bridge output
  templates (2026-07-27):** normalizes, without paraphrase, the exact
  proved formulas from `contraction_block_cut_tree.md`/
  `contraction_leaf_blocks.md` into one reference table (admissible-pair
  A, shared-port P, S5 S), resolving precisely the P output's `2^m-2`
  role left ambiguous by a prior compressed report: it is the
  *forbidden* route length (an immediate contradiction when reached),
  not an equivalence or a safe value.
- `central_bridge_triangle.md` — **Type T triangle: paired central
  bridges (2026-07-27):** classifies T2 (two
  cubic triangle vertices)/T3 (three), proves no two cubic triangle
  vertices ever share an external neighbour (Lemma NE, a direct C4-forcing
  argument), records the triangle-contraction attachment-pair symmetry
  orbits (T2: `\{a,b\}` inequivalent to `\{a,c\}`/`\{b,c\}`; T3: all
  equivalent). The main new finding: each cubic triangle vertex's own
  central bridge `B_x` attaches directly at `\{x,X_x\}` (`X_x` a pole of
  its own canonical theta `\Theta_x`) via the triangle's own edges alone
  — no S5 argument needed — and contains an isolated shortest path of
  length 2. The recovery audit shows that path is not pinned into T2's
  admissible pair; either claimed length-3/4 mate would force a `C_4`.
  The exact-two-A continuation gives the full larger-pair cycle table and
  an infinite safe arithmetic family, so the case remains open. Classifies the four
  `(X_x,X_y)` configurations between two triangle vertices exactly, and
  honestly resolves 3 of the task's 6 component-sharing possibilities
  from local data alone, leaving the rest open (external-structure
  dependent) rather than forcing a false resolution.
- `central_bridge_triangle_s5.md` — **S5 and shared-port cases at a Type
  T triangle (2026-07-27):** Part VI.1 proves that
  if two cubic triangle vertices' central bridges both independently hit
  the S5 outcome, their cut vertices must coincide (S5's own
  uniqueness) — and, new here, that the two attachment-free leaves are
  then *forced onto the same lobe* (never opposite lobes), since the
  triangle itself cannot be split by a cut vertex outside it. Part VI.2
  shows the "crosses lobes without using z" alternative is vacuous by
  the cut-vertex definition itself, and isolates the one genuinely open
  sub-case (a bridge path detouring through the leaf side) as needing
  the same unresolved internal-cycle-spectrum information already
  flagged upstream. Sets up the non-S5 `(A,A)/(A,P)/(P,P)` matrix (Part
  VII), now correcting the pinned A path lengths. Exact-two-attachment A
  remains with an unspecified larger admissible pair; `P` and `S` require
  structure beyond `\{x,X_x\}`, while `(P,P)` remains open
  honestly rather than forced to a false arithmetic conclusion; `(A,P)`
  (Part IX) is resolved concretely in its same-terminal-pair sub-case.
- `central_bridge_triangle_final.md` — **the (A,A) case, T3
  consistency, and the final assessment (2026-07-27, current top
  priority):** proves (Part X.0) that the terminal pairs `\{x,X_x\}` and
  `\{y,X_y\}` of any two triangle-anchored admissible pairs are always
  2-subsets of the same 3-element triangle, hence always either
  identical or share exactly one element — **the crossing case (X.3),
  flagged incomplete in the prior path-cell work, is arithmetically
  impossible in this anchored setting, resolved rather than left open.**
  Classifies the identical-terminal (X.1) and one-common-terminal (X.2)
  sub-cases exactly. The recovery audit supersedes their survivor status:
  the former `1+\ell_x'+\ell_y'` object repeats `x,y,xy`, and either
  anchored detour alone already forces a `C_4`. Part
  XI confirms T3's three pairwise analyses combine without any
  three-way inconsistency. The historical close selected **outcome 4** — every
  case was reduced to the frozen A/P/S templates — but the current corrected
  outcome refutes the interrupted R2/S2 claim and restores the unpinned
  exact-two-attachment A survivor. Multi-attachment A/P/S, chord,
  S5-incidence, and component-sharing cases also remain; neither
  Type N nor Type T is eliminated.
- `central_bridge_triangle_addendum.md` — **two sharpenings after the
  Part XIII close (2026-07-27):** does not reopen the closed sequence or
  add a new part number; records two narrow corrections found while
  independently re-deriving the same ground. (1) `central_bridge_triangle_s5.md`
  VI.1's double-S case: since `central_bridge_templates.md`'s **S**
  output *defines* `G_1` as `L`'s closure exactly (not merely a lobe
  containing `L`), the two attachment-free leaves are not just "on the
  same side" but **the same connected component of `G`**, sharper than
  VI.1's own "not forced either way." (2) `central_bridge_triangle_final.md`
  Part X.2's `\ell_x'\in\{3,4\}`: the original addendum excluded `3`;
  the recovery supplies the missed triangle-edge closure and excludes `4`
  too. The old conditional `4\in\Lambda_x => \rho_x\ne2` is vacuous in
  this anchored setting.
- `type_t_recovery_audit.md` — forensic state recovery, exact R2/S2
  definitions, theorem dependency graph, degree/simplicity audit, independent
  symbolic and NetworkX checks, an explicit T2-inference counterexample, and
  the corrected residual Type-T table.
- `type_t_exact_two_a.md` — continues with the highest-priority residual A
  case. Separates the generic pole-to-pole A template from the actual
  triangle gateway, proves the complete guaranteed cycle table with offsets
  `0,1,2^rho,2^s+1`, classifies its infinite arithmetic complement, audits
  Heawood/Balaban counterexamples and overlap cells, and explains why the
  scoped T8/SPQR results do not yet give a rooted replacement.
- `type_t_identical_terminal_joint_spectrum.md` — audits commit `3ba40fc`
  and corrects its existential/universal overlap quantifiers: the same-theta
  pairs are fixed safe, while all four cross-theta pair types have both safe
  and failing abstract incidences. It withdraws the invalid reduction to one
  `P_1^x`/`P_1^y` coincidence. These are now explicitly conditional abstract
  statements: the identical-terminal pole row was already eliminated by
  `central_bridge_triangle_pole_forcing.md`.
- `type_t_overlap_reduction.md` — builds the rooted four-color weighted
  incidence core, proves the exact FORCED/ESCAPABLE/UNIVERSALLY-SAFE
  classification for every valid cell count, records the exact hypotheses a
  splice must preserve, and isolates a scalable alternating-ladder family as
  an abstract colored graph. Structurally superseded: the ladder is not a live
  Type-T residual because its `X_x=y,X_y=x` premise uses cubic aligned poles.
- `type_t_ladder_saturation.md` — closes the proposed saturation target at its
  prerequisite: pole forcing leaves only `X_x=X_y=z_0`, so the
  identical-terminal ladder has zero initial/accepting states. It retains the
  abstract arithmetic, corrects the smallest ladder parameter to
  `L_{3,2,5}`, proves the generic two-attachment lower bound for off-core
  components and exact single-ear spectrum formula, and explains why neither
  ears nor `Q` can rescue the eliminated pole row.
- `central_bridge_triangle_pole_forcing.md` — resolves
  `type_t_recovery_audit.md`'s own "theta-chord case IV.1(ii)" row
  (there listed as open): a degree-counting argument shows a cubic
  Type-T vertex's aligned theta pole `X_x` can never itself be cubic —
  its fixed 3-edge budget (already committed to `P_0`, plus the
  `N[x]`-witness `P_2`'s established avoidance of `Y_x`) forces `Y_x`
  onto `P_1`, adjacent to `X_x`; the resulting chord `e_x`, closed
  against the `P_0`/`P_1` route, is then a genuine simple cycle of
  length exactly `2^{\rho_x}` — always a forbidden power of two. Since
  every T3 vertex's two triangle-mates are both cubic, **T3 is
  eliminated outright**; T2 is narrowed to exactly one pole assignment
  (both cubic vertices' poles equal to the shared non-cubic vertex) —
  the other three rows of `central_bridge_triangle.md` V.1's table are
  eliminated by the identical mechanism. Independent of, and does not
  touch, `type_t_recovery_audit.md`'s own R2/S2 correction — every
  other residual family there (exact-two-attachment A, multi-attachment
  A, P, single/mixed S, double S) survives exactly as catalogued,
  narrowed to this one pole assignment.
- `type_b_compatibility.md` — pivots to the complete Type-B cut: records the
  exact T3/T4/T5 scopes, proves the five-category cycle decomposition,
  reconstructs the asymmetric triangle-anchored spectra, gives an infinite
  mutually compatible forced-core family, and proves T9B paired replacement
  criticality plus its stronger real R/P-edge consequence. It isolates an
  exact paired-spectrum family without claiming graph realizability or a
  finite SPQR reduction.
- `type_b_realizability.md` — freezes that exact family and its first twenty
  targets, proves sharp canonical path-union and degree bounds, gives a
  two-solver UNSAT certificate for one fixed minimum-order paired embedding,
  enumerates all 3,298 Balaban `C16`s, and exhausts 826 witness-preserving
  degree-preserving 2-switches. The remaining claim is explicitly one
  degree-saturation/ear realizability mechanism, not ICF or a bounded-family
  elimination.
- `type_b_equality_order.md` — closes the minimum-order embedding gap for the
  smallest tuple. Deleting the degree-one bridge terminal reduces every
  possible 19-vertex bridge, independently of path overlap, to an 18-vertex
  `{C4,C8}`-free graph with 26 or 27 edges and at most two degree-two
  vertices. Exhaustive local generation eliminates the 26-edge layer; the
  complete checksummed 570-graph McKay extremal layer eliminates 27 edges.
  Thus `Pi0` has no realization at order 36.
- `type_b_b19.md` — promotes that result to the local bridge theorem B19 after
  an explicit dependency audit: neither `Pi0` bridge role can have order 19,
  independently of its partner. Consequently both bridges have order at least
  20, the full graph has order at least 38, and order 37 is eliminated by the
  impossible mixed `(19,20)` bridge sizes.
- `type_b_one_slack.md` — derives the exact 20-vertex bridge reduction: after
  deleting `x`, the 19-vertex remainder has one vertex off a distinguished
  18-vertex path, 28 or 29 edges, and at most two degree-two vertices. The
  complete 304-graph extremal layer eliminates 29 edges; the exact 28-edge
  degree-sequence layer remains explicitly incomplete.
- `verifier/` — independently runnable code:
  - `cycle_detect.py` — exact power-of-two cycle detector (2 cross-validated impls).
  - `check_g6.c` — fast independent C checker for graph6 streams.
  - `exhaustive_lb.py` — geng-based exhaustive lower-bound reproduction.
  - `additive_study.py` — max power-of-two-sum-free set (Track C).
  - `test_detector.py` — cross-validation harness.
  - `defect_model.py` — computes D and cycle spectra on real small graphs.
  - `vine_experiment.py` — vine-graph construction and V1 lemma test.
  - `one_pole_search.py` / `one_pole_verify.py` — one-pole counterexample
    search (Part 5) with an independent dual-detector verifier.
  - `state_search_proto.py` — canonical-state / proof-DAG search prototype
    (Part 6, scoped to the one-pole search — see experiments.md E10).
  - `o4_analysis.py` — O4/O4a failure-structure and terminal-path-spectrum
    analysis (see experiments.md E11).
  - `spqr_analysis.py` — historical SPQR-tree classification of the
    two-terminal root-neighbor structure; new R-node claims require the
    structural validator/fallback documented in `two_cut.md` §17.
  - `rigid_core_check.py` — O5's rigid-core lemma: exhaustive check plus a
    regression test on two flawed hand-examples (see experiments.md E13).
  - `edge_rooted_search.py` — direct (G,e) search per the suppressed-edge
    equivalence (see experiments.md E14).
  - `spqr_signature.py` — series/parallel Σ(P) composition rules,
    independently verified against brute-force enumeration (E15).
  - `spqr_k4_skeleton.py` — K4 rigid-skeleton triangle/quadrilateral
    spectrum analysis and reducible-configuration search (E16, E17).
  - `multi_r_search.py` — one-R-node target search (E18).
  - `bridge_signature.py` — terminal-edge-free two-terminal signatures,
    with Λ(B) and the explicitly dyadic internal-cycle spectrum C_F(B) (E19).
  - `bridge_compatibility.py` — exact Type A/B/C search with T5-before-cross
    filtering and independent re-verification of realizable candidates (E20).
  - `three_bridge_search.py` — proves T2/T4/T5/pairwise-compatibility are
    jointly insufficient to exclude Type A abstractly (infinite
    equal-signature family); regression-only abstract search (E21).
  - `linkage_data.py` — the symmetric-difference identity
    |P|+|Q|=2ω(P,Q)+Σ(cycle lengths), independently verified (E22).
  - `bridge_closure_search.py` — generates bridge closures J=B+xy (reusing
    the one-pole search structure), computes Λ(B)/h(B)/𝒟(B)/SPQR, ranks
    near-gadgets by h(B) (E22).
  - `gadget_criticality.py` — executable T8/R1/T8R audits and validated
    reduced-SPQR records for Type-A closure candidates (E23a).
  - `brute_spqr.py` — definition-first exhaustive split-pair decomposition
    for n≤9, used when the external SPQR package fails structural validation.
  - `type_a_order9_search.py` / `check_power_masks.c` — manifest-driven
    rooted order-9 closure census and independent direct three-copy detector
    (E23b).
  - `type_a_extremal_check.py` — independent terminal-choice checks on the
    exact order-9 and order-11 McKay–Afzaly extremal files (E24a).
  - `type_a_order10_direct.py` — manifest-frozen direct Type-A search in the
    only possible clean order-10 edge layers, m=13,14 (E24b).
  - `spqr_extremal_audit.py` — R2 and exact S/P/rigid-leaf adversarial census
    over the graph atlas and relaxed closures (E24c).
  - `order9_spqr_obstructions.py` — shortest forbidden-cycle projection and
    leaf-R structural dataset mined from the existing E23 artifact (E24d).
  - `leaf_r_patterns.py` — exact dihedral witness-pattern mining over the
    preserved E23/E24 records, including original-vs-suppression-exposed leaf
    orientation.
  - `leaf_r_replacement_search.py` — targeted edge-rooted R-skeleton audit
    through order nine; not a new SPQR census.
  - `z3_lift_search.cpp` / `independent_z3_verify.py` /
    `independent_z3_c4_verify.py` — exhaustive staged cyclic-lift engine and
    the independent full-survivor / full-C4-stage audits.
  - `z3_lifts.py` — reference Z3 lift construction, base certification, and
    voltage/assignment-index helpers reused throughout Part III/IV.
  - `global_core_check.py` — 2-degeneracy peeling order, inclusion-minimal-
    delta>=3 atlas certification, reused by `cubic_core.py`/`d1_search.py`.
  - `survivor_analyze.py` — standalone diagnostic for any future 4-or-8
    survivor (degree sequence, C4/C8/C16 status, girth, diameter, |Aut|,
    full cycle spectrum); part of the survivor-handling protocol, not tied
    to a specific experiment.
  - `cubic_core.py` — cubic-core decomposition identities (C/H/F/beta(F),
    the component-incidence quotient Q), validated on 3 independent
    populations (defect.md Part I).
  - `d1_search.py` — defect-one theorem D1: fast property-(2) equivalent,
    two independent D1-hypothesis generators (direct ordering + geng),
    D1C completion-lemma test (defect.md Part II).
  - `z3_certificate.py` — exhaustive simple-C16 projection-type
    classification and full-nonzero-space hyperplane coverage per base
    (z3_lifts.md Part III.1-III.2).
  - `z3_min_cover.py` — near-minimal covering-subset search (greedy set
    cover) for the simple-C16 hyperplanes (z3_lifts.md Part III.2).
  - `z3_standalone_verifier.py` — self-contained certificate checker using
    only the covering subset, cross-validated against real lift
    reconstruction (z3_lifts.md Part III.3).
  - `z5_lift_feasibility.py` — algebraic-feasibility study for cyclic Z5
    lifts of the same four bases, Monte Carlo coverage estimate plus
    real-lift sampling, no full `5^13` enumeration (z3_lifts.md Part IV.A).
  - `separator_defect_map.py` — q(G) formulas for the S5 cut-vertex and
    Type A/B/C 2-cut cases in terms of piece defects, validated on
    synthetic constructions (two_cut.md §26, Part V).
  - `contraction_lift.py` — mechanical cross-check of the near-power edge
    lemma's contraction/lifting arithmetic, the cubic-vertex `{1,3}`
    nontriangle-edge count, and the clean same-length merge lemma
    (contraction.md Parts I, III, IV); does not and cannot test claims
    that presuppose a minimal counterexample exists.
  - `atom_lift.py` — mechanical cross-check of the general atom-lifting
    lemma, the triangle-pair lemma, the Type N/T dichotomy plus triangle
    uniqueness, the functional-digraph orbit classification, the
    five-lemma arithmetic/gluing toolkit, and the bridge-arithmetic chord
    corollary (contraction_atoms.md Parts I, III-V, VII.1); kept separate
    from `contraction_lift.py`, whose prior audit it does not touch.
  - `neighborhood_lift.py` — mechanical cross-check of closed-
    neighborhood contraction, the cubic power-path lemma CN1 and its
    r=2 closure, and the Type T offset comparison between the triangle
    atom and the closed-neighborhood atom (contraction_neighborhood.md
    Parts I-II); kept separate from `contraction_lift.py`/`atom_lift.py`,
    neither of which it touches.
  - `mixed_witness.py` — mechanical cross-check of the four combined
    endpoint orbits at a Type N vertex, the NPT-theta/fan/vertex-hub
    arithmetic, and two new arithmetic lemmas (contraction_mixed_witness.md);
    kept separate from the three prior contraction verifiers, none of
    which it touches.
  - `intersection_diagrams.py` — mechanical cross-check of the
    non-crossing cell-decomposition identity, the explicit smallest
    counterexample to the one-cell reduction target, and the three
    resolved non-crossing intersection-diagram types
    (contraction_intersections.md Part V); kept separate from the four
    prior contraction verifiers, none of which it touches; deliberately
    builds no gadget for the still-open crossing case.
  - `theta_saturation.py` — mechanical cross-check of the same-branch
    and cross-branch theta-bridge arithmetic and the internal-vertex-
    count growth used in the S5 cut-vertex saturation argument
    (contraction_saturation.md Part VI); kept separate from the five
    prior contraction verifiers, none of which it touches; deliberately
    builds no gadget for the unresolved saturation target itself.
  - `central_bridge.py` — mechanical cross-check of CB1, the
    endpoint-return cycle list, the topological-K4 construction with a
    full independent simple-cycle enumeration confirming exactly seven
    cycles, the NPT substitution table (1,500 parameter tuples), the
    first-excursion containment fact, and a structural (explicitly
    non-canonical) two-excursion CB2 instance (contraction_central_bridge.md
    Parts I-V); kept separate from the six prior contraction verifiers,
    none of which it touches.
  - `separator_integration.py` — mechanical cross-check of CB3′'s three
    exact cases (clean 2-attachment 2-connectivity/degree preservation;
    the >=3-attachment internal-degree-loss phenomenon) and the paired
    topological-K4 union arithmetic (contraction_separator_integration.md
    Parts VI-VII); kept separate from the seven prior contraction
    verifiers, none of which it touches; does not re-derive S5/T1/T2,
    all cited by name.
  - `block_cut_tree.py` — mechanical cross-check of attachment-core
    pruning (via networkx's own biconnected-components/articulation-
    points routines, independent of this project's code), the
    attachment-free-leaf S5 consequence, the MA1 construction, and the
    MA2 trichotomy (contraction_block_cut_tree.md Parts I-V); kept
    separate from the eight prior contraction verifiers, none of which
    it touches.
  - `leaf_block_arithmetic.py` — mechanical cross-check of the
    endpoint-location route census (via networkx.all_simple_paths,
    fully independent enumeration), the admissible-pair excluded-
    residue templates, the shared-port arithmetic, and the
    distinct-port-to-admissible-pair reduction (contraction_leaf_blocks.md
    Parts VI-VIII); kept separate from the nine prior contraction
    verifiers, none of which it touches.
  - `central_bridge_triangle.py` — mechanical cross-check that the
    shared-external-neighbour configuration (`a'=b'`) genuinely forces a
    4-cycle on an explicit gadget, and that a triangle-anchored central
    bridge `B_x` (built with an explicit NPT theta `\Theta_x` and a
    bridge component attached via the triangle's own edges) has
    attachment set exactly `\{x,X_x\}` with shortest `x`-`X_x` path
    length exactly 2; its former length-4 supporting fixture is now correctly
    identified as a negative fixture containing the forced `C_4`
    (central_bridge_triangle.md Parts II, IV); kept separate from the ten
    prior contraction verifiers, none of which it touches.
  - `central_bridge_triangle_s5.py` — mechanical cross-check that on an
    explicit double-S5 gadget (two central bridges sharing one forced
    cut vertex `z` of degree exactly 4), the triangle is forced entirely
    into one lobe of `G-z` and the attachment-free leaf into the other,
    never opposite lobes (central_bridge_triangle_s5.md Part VI.1); kept
    separate from the eleven prior contraction verifiers, none of which
    it touches.
  - `central_bridge_triangle_final.py` — exhaustive check (all 4
    `(X_x,X_y)` configurations) that two triangle-anchored admissible-
    pair terminal sets always coincide or share exactly one element,
    never four distinct vertices — the crossing case is arithmetically
    impossible in this setting (central_bridge_triangle_final.md Part
    X.0); kept separate from the twelve prior contraction verifiers,
    none of which it touches.
  - `central_bridge_triangle_addendum.py` — mechanical cross-check of
    both sharpenings: an explicit double-S gadget confirming both
    vertices' "leaf-side" computation identifies the identical
    component, not merely components on the same side; and two gadgets
    confirming both length-3 and length-4 anchored detours close into a
    literal `C_4`; retains the older length-4/`\rho_x` sum only as a
    conditional arithmetic check (central_bridge_triangle_addendum.md);
    kept separate from the thirteen prior contraction verifiers, none of
    which it touches.
  - `type_t_r2_s2_audit.py` — definition-first symbolic incidence and an
    independent NetworkX joint two-theta realization of the recovered R2/S2
    candidate; verifies the forced `C_4`s and that the claimed length-9 object
    is not simple, plus a Heawood-based regression showing T2's admissible pair
    need not contain the shortest terminal path.
  - `type_t_exact_two_a.py` — checks the corrected exact-two-attachment A
    cycle table and infinite safe family, the generic pole-to-pole comparison,
    complete Heawood hypothesis failures, a C4/C8-free Balaban-derived rooted
    counterexample to local anchoring, and irreducible two-cell overlap
    patterns for both admissible offsets.
  - `type_t_cell_decompositions.py` — independently brute-forces every valid
    simple-graph cell decomposition through path totals 10, then checks all
    four cross-theta length types, exponents 2 through 12, and every permitted
    cell count against the symbolic classification; saves the smallest mixed
    and S/S counterexamples to the former universal claims.
  - `type_t_ladder_states.py` — independently enumerates all four T2 pole
    rows, confirms that only the one-common-terminal `(z_0,z_0)` row survives,
    and checks the abstract even-cell ladder formulas without calling them a
    graph realization.
  - `type_t_ladder_saturation_sat.py` — two independent prerequisite-CNF
    checks (complete assignment enumeration and elementary DPLL) prove the
    identical-terminal requirements inconsistent with pole forcing before
    any saturation or `Q` variable is created.
  - `central_bridge_triangle_pole_forcing.py` — mechanical cross-check
    of the degree-forcing argument (a cubic `X_x` has exactly one spare
    edge once `P_2` is required to avoid `Y_x`, forcing `Y_x` onto
    `P_1`); the resulting forced simple cycle of length exactly
    `2^{\rho_x}` (`\rho_x\in\{2,3,4,5\}`); and that rows 1–3 of the
    `(X_x,X_y)` table each force this cycle while the last row (built
    with a genuinely non-cubic shared pole, degree 6) does not
    (central_bridge_triangle_pole_forcing.md); independent of
    `verifier/type_t_r2_s2_audit.py`, neither touches the other.
  - `type_b_compatibility.py` — independently checks the five Type-B cycle
    categories, deletion monotonicity, the exact asymmetric gateway mapping,
    all four paired-offset patterns and a 1,600-row finite regression of the
    infinite forced-core family, plus the explicit Balaban C16 witness and
    its intersections with the length-11/13 paths.
  - `type_b_realizability.py` — checks the frozen family and exact first-20
    prefix; constructs sharp minimum-order path unions; runs deterministic
    CP-SAT C8-CEGAR and an independently encoded Glucose3 UNSAT check for one
    fixed order-36 paired template; independently enumerates every Balaban
    C16; and exhausts a precisely scoped class of 826 path-preserving
    degree-preserving 2-switches.
  - `type_b_equality_order.py` — verifies the overlap-independent E36
    reduction; regenerates all 101,546 possible 26-edge remainders twice with
    unrelated C8 detectors; checks McKay's 570 order-18 extremal graphs and a
    fresh degree audit; and certifies that neither edge layer contains a bridge
    remainder with the necessary degree pattern.
  - `type_b_one_slack_setup.py` — verifies all 304 order-19, 29-edge McKay
    extremal graphs with two C4/two C8 routes, recomputes their degree-two
    distribution, and certifies that the extremal one-slack remainder layer is
    empty without claiming anything about the unresolved 28-edge layer.
- `manifests/` — canonical run and external-artifact provenance records.
- `logs/`, `data/` — run outputs and artifacts.

## Environment

Python 3.14.6 is recorded in `.python-version`; direct runtime and development
dependencies are pinned in `requirements.txt` and `requirements-dev.txt`.
The exhaustive generators additionally require nauty 2.9.3 (`geng`, `labelg`,
and `countg`). Native verification binaries are build products and belong in
`.build/`, never under `verifier/`.

```bash
make setup                         # create .venv and install pinned dependencies
make check                         # build checkers, parse Python, run all tests
geng -c -d3 10 | .build/check_g6  # example exhaustive stream
```

`make clean` removes only disposable build and test caches. Checksummed files
under `data/`, `logs/`, and `manifests/` are research certificates and are not
cleaned automatically. Frozen manifests may retain execution-time paths for
provenance; they are records, not current setup instructions. The test suite
also rejects newly tracked bytecode, local-agent state, and native binaries.

## Discipline
Every mathematical assertion is labeled PROVED / COMPUTATIONALLY VERIFIED /
CONJECTURAL / DISPROVED / KNOWN FROM LITERATURE. Experimental evidence is never
promoted to a theorem. Failed approaches are kept with the exact obstruction.
