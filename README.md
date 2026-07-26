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
- `two_cut.md` — **current top priority (2026-07-25):** toward proving a
  lexicographically minimal counterexample is 3-connected (kept
  CONJECTURAL). T1–T3, the global bridge-spectrum identity, and a
  balanced 2-cut census (S5-analogue) are proved for the 2-connected
  case.
- `s6_case_tree.md` — exact Type A/B/C dependency tree, the proved
  spectrum-safe replacement principle, its scope boundary, and the first
  unseen genuine leaf-R configuration.
- `z3_lifts.md` — normalization, completeness, implementation, and exact
  elimination statement for cyclic Z3 lifts of the four certified bases.
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
  - `z3_lift_search.cpp` / `independent_z3_verify.py` — exhaustive staged
    cyclic-lift engine and independent full-survivor audit.
- `manifests/` — canonical run and external-artifact provenance records.
- `logs/`, `data/` — run outputs and artifacts.

## Environment
Python venv in `.venv` (networkx, numpy, OR-Tools CP-SAT, PySAT); nauty
`geng`; `spqrtree` (pure-Python Gutwenger–Mutzel SPQR-tree algorithm, used
by `verifier/spqr_analysis.py`).
```
. .venv/bin/activate
cd verifier && python test_detector.py          # validate the detector
cc -O3 -o check_g6 check_g6.c                    # build the C checker
geng -c -d3 10 | ./check_g6                      # exhaustive n=10 check
```

## Discipline
Every mathematical assertion is labeled PROVED / COMPUTATIONALLY VERIFIED /
CONJECTURAL / DISPROVED / KNOWN FROM LITERATURE. Experimental evidence is never
promoted to a theorem. Failed approaches are kept with the exact obstruction.
