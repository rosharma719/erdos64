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
- `verifier/` — independently runnable code:
  - `cycle_detect.py` — exact power-of-two cycle detector (2 cross-validated impls).
  - `check_g6.c` — fast independent C checker for graph6 streams.
  - `exhaustive_lb.py` — geng-based exhaustive lower-bound reproduction.
  - `additive_study.py` — max power-of-two-sum-free set (Track C).
  - `test_detector.py` — cross-validation harness.
- `logs/`, `data/` — run outputs and artifacts.

## Environment
Python venv in `.venv` (networkx, numpy, OR-Tools CP-SAT, PySAT); nauty `geng`.
```
. .venv/bin/activate
cd verifier && python test_detector.py          # validate the detector
cc -O3 -o check_g6 check_g6.c                    # build the C checker (gitignored; rebuild per machine)
cc -O3 -o check_c8 check_c8.c                    # build the C8-survivor checker (gitignored)
geng -c -d3 10 | ./check_g6                      # exhaustive n=10 check
```
`check_g6`/`check_c8` are compiled binaries, intentionally gitignored — rebuild
them with the `cc` commands above on each machine (they are not portable
across architectures/OSes).

## Discipline
Every mathematical assertion is labeled PROVED / COMPUTATIONALLY VERIFIED /
CONJECTURAL / DISPROVED / KNOWN FROM LITERATURE. Experimental evidence is never
promoted to a theorem. Failed approaches are kept with the exact obstruction.
