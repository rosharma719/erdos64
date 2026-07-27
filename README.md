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
- `contraction_atoms.md` — **contractible-atom generalization (2026-07-27,
  current top priority):** the general atom-lifting lemma (`2^k+r` for
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
