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
- `manuscript.md` — **structural manuscript draft (2026-07-25):** pulls
  together S4, S5, O1, O3, O4a, O4′, O5, and the suppressed-edge
  equivalence into a single citable write-up with full novelty/reference
  bookkeeping.
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
  - `spqr_analysis.py` — SPQR-tree classification of the two-terminal
    root-neighbor structure, via the verified `spqrtree` package (see
    experiments.md E12).
  - `rigid_core_check.py` — O5's rigid-core lemma: exhaustive check plus a
    regression test on two flawed hand-examples (see experiments.md E13).
  - `edge_rooted_search.py` — direct (G,e) search per the suppressed-edge
    equivalence (see experiments.md E14).
  - `spqr_signature.py` — series/parallel Σ(P) composition rules,
    independently verified against brute-force enumeration (E15).
  - `spqr_k4_skeleton.py` — K4 rigid-skeleton triangle/quadrilateral
    spectrum analysis and reducible-configuration search (E16).
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
