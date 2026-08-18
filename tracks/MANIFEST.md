# tracks/ — provenance and layout of the consolidation

**Consolidated 2026-08-18 onto `consolidated/canonical`, branched from
`main`.** This file records where every branch's work went, and why the
layout is what it is. **No original branch was deleted; all fifteen remain
on `origin` with full commit history.**

## The actual branch topology

Established with `git merge-base`, not inferred from prose. The seven
substantial branches are **not** seven parallel attempts:

```
main (9fb2756, "init")
 │
 ├── claude/erdos-gyarfas-conjecture-oegjjg      a35358c  2026-08-07   46 commits
 │      (genuinely independent — forked directly from main)
 │
 └── claude/erdos-gyarfas-handoff-l6tqlo         7a3c1f7  2026-07-27   78
      └── claude/erdos-gyarfas-type-t-analysis-a9u4sx  3ba40fc 2026-07-28   94
           └── claude/type-t-c16-compilation-x9ts7a    666f54a 2026-07-29  120
                └── codex/type-t-c16-continuation      d3b1034 2026-07-29  121
                     └── claude/graph-counterexample-q6-xerdjz b64444c 2026-08-02 160
                            ▲
                            └── merged codex/type-t-overlap-reduction at c99ba8f
                                (that branch's tip f7966c1, 2026-07-29, 104 commits,
                                 has exactly ONE commit not in the chain)
```

Consequences that matter for anyone reading a handoff document:

- `claude/graph-counterexample-q6-xerdjz` is a **strict descendant** of four
  of the other six. Fast-forwarding to it carries branches 2, 3, 5 and 6
  entirely, plus 103 of `codex/type-t-overlap-reduction`'s 104 commits.
- `codex/type-t-c16-continuation` = `claude/type-t-c16-compilation-x9ts7a`
  **plus one commit** ("Certify Type-T C16 five-passage layer"). They are
  sequential, not parallel.
- Therefore the frequently repeated description of the three Type-T/C16
  branches as *three uncoordinated parallel efforts on the same problem* is
  **wrong as stated**. The genuine duplication is narrower: the
  `codex/type-t-overlap-reduction` line and the
  `type-t-c16-compilation` line did fork at `f8a11e0` and did independently
  build overlapping C4/C8/C16 conflict catalogs under **identical
  filenames**, but the fork was later merged back, and the residue is one
  commit. That residue is preserved here, renamed, in
  `tracks/type-t-c16-static-sat/`.
- Two branches' work was genuinely outside the chain and is folded in here:
  `codex/type-t-overlap-reduction`'s tip, and the whole of
  `claude/erdos-gyarfas-conjecture-oegjjg`.

## Where the code lives, and why the root layout was kept

The chain's ~250 verifiers, ~40 tests, and all `data/`, `manifests/` and
`logs/` artifacts stay in the repository root layout (`verifier/`, `data/`,
`manifests/`, `tests/`). **That is deliberate.** The collision hazard flagged
by the earlier snapshot manifest was real *between* unmerged branches, but
inside the chain it was already resolved by linear history — there are no
duplicate filenames there. Relocating those files into thematic
subdirectories would break path references in ~90 markdown files, the
`Makefile`, and every test, while resolving zero actual collisions.

`tracks/` therefore holds exactly the material that could **not** live in
the root layout without a genuine name collision or a genuine provenance
question. Use this table to find a theme:

| theme | where it lives | key entry points |
|---|---|---|
| **Type-T C16 port completion** (passage-level, most advanced) | root | `type_t_port_c16_passage_projection.md`, `type_t_port_c16_compilation.md`, `type_t_port_core_dyadic_avoidance.md`, `verifier/type_t_port_*.py`, `data/type_t_port_c16_passages/` |
| **Type-T C16, gadget-level static SAT** (parallel, `BOUNDED_INCOMPLETE`) | `tracks/type-t-c16-static-sat/` | its own `type_t_port_c16_compilation.md` |
| **Global structure / separators / 2-cuts** | root | `two_cut.md`, `separator_theorem_order32_gap_analysis.md`, `three_connectivity_general_order.md`, `cubic_edge_connectivity.md`, `fcn_satsolver_extension.md`, `f12_order12_result.md` |
| **One-pole gadget theory** | root | `one_pole.md`, `manuscript.md` §3, `verifier/one_pole_*.py`, `verifier/spqr_*.py` |
| **Contraction / Type N / Type T** | root | `contraction*.md`, `central_bridge_triangle*.md`, `type_t_*.md` |
| **Defect ladder `q(G) ≥ 4`** | root | `defect.md`, `defect_three.md`, `verifier/defect_*.py`, `verifier/kernel_*.py` |
| **Z3 / Z5 voltage lifts** | root | `z3_lifts.md`, `verifier/z3_*.py`, `verifier/z5_*.py`, `data/z3_lifts/` |
| **Order-30 triangle-quotient census** | root **and** `tracks/order30-census/` | `order30_quotient_census.md` (root, the census itself); `tracks/order30-census/t4_intersection_filter/` (the audited `t=4` filter and its complete run logs), `girth6_kernel/`, `girth7_kernel/` |
| **Small-order exhaustive search** | root + `logs/` | `verifier/certify_shard.sh`, `verifier/check_*.c`, `logs/certify/`, `logs/p1_n20_23/` |
| **Audits of externally supplied claims** | `tracks/external-audits/` | `verification_log_2026-08-06.md`, `order38_bundle/AUDIT.md`, `a5_lift_probe/AUDIT.md` |

## `tracks/` contents

### `tracks/type-t-c16-static-sat/`
Source: `codex/type-t-overlap-reduction` at `f7966c1` (2026-07-29), the one
commit of that branch not contained in the chain.

A **gadget-level** static short-cycle compilation for the fixed
representative `(j,a,c) = (4,28,4)`: a complete exact `C4/C8` layer (579
relevant core paths, 286,011 literal C8s, 227,725 minimized clauses — 371
unary, 227,354 binary — and **zero** C4 supports), plus a universal-gadget
AllSAT projection of every simple 16-cycle yielding **84,936**
inclusion-minimal C16 supports (569 unary / 24,252 / 29,172 / 16,497 /
14,446 by support size).

**Its own label: `BOUNDED_INCOMPLETE`.** The residual projection is still
SAT, so the C16 catalog is explicitly incomplete; the file claims no
obstruction theorem and no counterexample.

**Why it is here rather than in the root.** Four of its paths collide by
name with different content in the chain:
`type_t_port_c16_compilation.md`, `verifier/type_t_port_c16_hypergraph.py`,
`verifier/type_t_port_short_conflicts.py`, and
`manifests/type_t_port_c16_manifest.json`.

**How it relates to the root version.** The root (passage-level) work
supersedes the *representation* — projecting to passage variables gives a
206.7× clause reduction on this very instance — and reaches materially
further on `(4,55,7)` (`m=2/3/4` complete outright). It does **not**
reproduce this instance's gadget-level data, and the support-bound theorem
that both lines rest on was established first on the
`type-t-c16-compilation` line. Kept as a distinct sub-track for that
reason, not merged into it.

### `tracks/order30-census/`
Source: `claude/erdos-gyarfas-conjecture-oegjjg`, `external_review/`.

- `t4_intersection_filter/` — the specialized order-30 `t=4` triangle-marking
  filter (`src/t{2,3,4}_intersection_filter.cpp`, `derive_t3_table.py`), its
  audit (`AUDIT.md`, `T3_AUDIT.md`), and **the complete run logs and
  aggregate for the exhaustive `t=4` census** (`results/t4_full_intersection/`:
  219 per-shard log/time pairs, `input.sha256`, `aggregate.json`). This is
  the certification for `proof.md` O30-2's `t=4` row
  (52,577,491,505 markings, zero survivors, `complete: true`).
  The filter was **audited before being trusted**: hand-check of its
  `allowed_bits` table against the independently derived exact-interval
  theorem, plus field-by-field cross-validation of its aggregate output on
  500 real quotients against an independently written Python census.
- `girth6_kernel/` — `exhaustive_s0a0.py` (the complete, non-sampled
  enumeration that closes girth-6 case `(s=0,a=0)`), `sweep_s0a0.py`,
  `verify_s0a0.py`, `enumerate_degseq.py`. The exhaustive script carries the
  post-build degree validator added after a real bug (two parallel
  length-0 edges collapsing in a Python `set`, leaving two hubs at degree 2)
  produced a spurious `feasible=1`.
- `girth7_kernel/` — `verify_skeletons.py`, `literal_crosscheck.py`.
- `order30_quotient_sanity.py`, `split_shard.py`, `split_by_connectivity.py`,
  `run_geng_waves.sh` — catalog generation and sharding helpers.

### `tracks/external-audits/`
Source: `claude/erdos-gyarfas-conjecture-oegjjg`, `external_review/`.
Every item here is an audit of a claim that arrived from **outside** the
session that audited it. **None of them is a result of this project**; they
are recorded so the claims are not silently re-imported.

- `verification_log_2026-08-06.md` — the claim-by-claim log, in the format
  *claim → status → method → note* with statuses VERIFIED / REFUTED /
  UNVERIFIED / PLAUSIBLE. This is the format worth reusing. It contains the
  three findings that most affect the current frontier: the Bass–Ihara
  high-girth theorem is **correct but vacuous at `n=30`** (the (3,9)-cage
  has 58 vertices); the contraction theorem's order-30 application **does
  not follow** (it needs global minimality among all δ≥3 graphs, and the
  quotient carries a degree-4 vertex so only the `≥17` bound applies); and
  the length-16 tangle theorem's 17-template classification is **reproduced
  bit-for-bit and re-derived by hand** while its load-bearing spectral bound
  `N₁₆ ≥ 53568` is **not verified at all**.
- `order38_bundle/` — audit of a separately supplied (third-sandbox)
  order-38 census claim. `AUDIT.md`, the three hand-proof notes, the C++
  sources and two skeleton data files. Outcome: proofs sound *conditional on
  uncited external theorems*; the shared cycle-detection primitive
  cross-validates against `cycle_detect.py` with 0 disagreements; **2 of 151
  partition classes reproduced from scratch and agree**; the other 149 and
  the 60.9M-node aggregate remain **unverified** (the data files were never
  supplied).
- `a5_lift_probe/` — the A5 5-sheet permutation-lift probe over all four
  24-vertex bases, with an independent Python reimplementation of the
  solver's tree/cotree bookkeeping verified byte-for-byte against the
  compiled solver. Convergent negative evidence (`base2`/`base3`
  independently hitting the *same* 9-cut wall).
- `order32_direct_search/`, `order40_probe/`, `algebraic_constructions/`,
  `s5_lift_check/` — independent re-runs and spot-checks of further
  externally reported searches.

## What was deliberately not carried forward

- **The 14 branch snapshots** that
  `claude/erdos-gyarfas-conjecture-oegjjg` had archived under its own
  `tracks/<branch-name>/` (≈3,300 files). They are byte-copies of branches
  that still exist on `origin` with full history; duplicating them inside a
  branch whose whole purpose is to supersede them would be pure redundancy.
  This manifest replaces that index.
- **Compiled binaries and Python bytecode** — `.pyc`, `__pycache__/`,
  `verifier/check_g6`, `verifier/check_c8`, and the audit tracks' C++
  binaries. All are rebuilt from committed source (`make`, or `cc -O3`);
  `.gitignore` covers every relocated path. This applies the hygiene pass
  both lines had already adopted.
- **Branch-specific `README.md` / `plan.md` / `proof.md` / `lemmas.md`
  variants.** Superseded by the single consolidated set at the repository
  root, which merges their content rather than picking one.
