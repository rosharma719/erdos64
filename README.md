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
  attachment-rich leaves (2026-07-27, current top priority):** the
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
