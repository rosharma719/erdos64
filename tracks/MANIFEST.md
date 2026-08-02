# Track manifest — consolidated branch provenance

This repository accumulated **14 independent, never-merged research branches**
(plus `main`, a single-commit bootstrap, and this branch's own direct-enumeration
work) attacking the Erdős–Gyárfás conjecture from different angles. All 14 share
only the single `init` commit as common ancestor — they are parallel attempts,
not a sequence, and were never reconciled. Several branches even independently
produced files with identical names and different content while working on
overlapping sub-problems (see `graph-counterexample-q6-xerdjz`'s own README,
which flags this for `type-t-c16-compilation-x9ts7a` vs `type-t-overlap-reduction`).

**What happened here:** each subdirectory below is a full snapshot of one
branch's tree at its head commit, taken via `git archive`, so the content is
browsable in one place without juggling checkouts. **Nothing was deleted or
rewritten** — every original branch still exists at the SHA listed below on
`origin`, with its full incremental commit history intact, and can be
`git log`/`git diff`'d independently at any time. This manifest is the index;
it does not merge or resolve conflicts between tracks, because these are
genuinely divergent research directions (not a single narrative that can be
flattened) and forcing a line-level merge of e.g. 14 different `plan.md`
files would destroy information, not consolidate it.

Discipline note: every track follows the same PROVED / CONJECTURAL /
NOT_FORMALLY_VERIFIED / DISPROVED labeling convention as this branch's own
`plan.md`. Read each track's claims at the label it gives itself.

## Tracks

| Directory | Source branch | Head commit | Date | Commits vs. main |
|---|---|---|---|---|
| `erdos-gyarfas-handoff-l6tqlo` | `claude/erdos-gyarfas-handoff-l6tqlo` | `7a3c1f7` | 2026-07-27 | 77 |
| `erdos-gyarfas-type-t-analysis-a9u4sx` | `claude/erdos-gyarfas-type-t-analysis-a9u4sx` | `3ba40fc` | 2026-07-28 | 93 |
| `graph-counterexample-q6-xerdjz` | `claude/graph-counterexample-q6-xerdjz` | `b64444c` | 2026-08-02 | 159 |
| `separator-lemmas-defect-gjlolu` | `claude/separator-lemmas-defect-gjlolu` | `a273253` | 2026-07-26 | 10 |
| `type-t-c16-compilation-x9ts7a` | `claude/type-t-c16-compilation-x9ts7a` | `666f54a` | 2026-07-29 | 119 |
| `defect-one-voltage-obstruction` | `codex/defect-one-voltage-obstruction` | `0125b5a` | 2026-07-26 | 25 |
| `defect-three-kernel` | `codex/defect-three-kernel` | `e6050b7` | 2026-07-26 | 50 |
| `e21-integrity` | `codex/e21-integrity` | `330054f` | 2026-07-25 | 10 |
| `global-core-z3-lifts` | `codex/global-core-z3-lifts` | `a5af13d` | 2026-07-26 | 19 |
| `leaf-compression-z5-exact` | `codex/leaf-compression-z5-exact` | `473ce76` | 2026-07-26 | 41 |
| `t8-gadget-search` | `codex/t8-gadget-search` | `f284371` | 2026-07-25 | 12 |
| `type-a-extremal-spqr` | `codex/type-a-extremal-spqr` | `bb3a06b` | 2026-07-25 | 14 |
| `type-t-c16-continuation` | `codex/type-t-c16-continuation` | `d3b1034` | 2026-07-29 | 120 |
| `type-t-overlap-reduction` | `codex/type-t-overlap-reduction` | `f7966c1` | 2026-07-29 | 103 |

Plus this branch's own root-level work (`plan.md`, `proof.md`, `lemmas.md`,
`experiments.md`, `literature.md`, `verifier/`, `logs/`): direct exhaustive
enumeration (n≤19 proved, n=20/22 cubic newly extended this session — see
root `plan.md` status log), and `external_review/order38_bundle/`: an
independent audit of a separately-supplied (non-git, third-sandbox) order-38
census claim.

## What each track attacks (one line each, from commit history — see each
track's own `plan.md`/`README.md` for the real detail)

- **graph-counterexample-q6-xerdjz** — deepest and most recent track (159
  commits, through 2026-08-02). Type A/B/C two-cut structure theory, cubic
  order-32/34 factor census audits, contraction-criticality endgame
  (near-power-cycle witnesses), F12/F19 lemmas, cubic 3-edge-connectivity via
  Whitney's inequality. Contains `data/order30_quotient_census/` with
  `near_miss_*.json` candidate graphs and `.g6.gz` quotient census files —
  the most direct existing resource for a counterexample hunt.
- **type-t-c16-compilation-x9ts7a** / **type-t-c16-continuation** /
  **type-t-overlap-reduction** — three independently-developed attempts at
  the same handoff task (minimum-cubic Type-T port completion / C16 passage
  compilation), diverging after a shared ancestor commit. Not reconciled
  with each other (see graph-counterexample-q6's own warning).
- **erdos-gyarfas-type-t-analysis-a9u4sx** / **erdos-gyarfas-handoff-l6tqlo**
  — Type-T vertex structure (aligned poles, joint four-path spectrum,
  bridge theorems).
- **separator-lemmas-defect-gjlolu** / **e21-integrity** — separator lemmas,
  the "defect" parameter, E21 order-count reconciliation.
- **defect-one-voltage-obstruction** — voltage-graph/lift obstructions tied
  to the defect parameter.
- **defect-three-kernel** — resolves a "defect-three" case, q(G)≥4 result.
- **global-core-z3-lifts** / **leaf-compression-z5-exact** — cyclic Z3/Z5
  lift searches over certified base graphs.
- **t8-gadget-search** / **type-a-extremal-spqr** — Type-A copy-gadget
  search, SPQR-tree obstruction classification.

## Non-destructive by design

The original 14 branches remain on `origin` untouched. If/when the user wants
to actually delete the stale branches (a real cleanup step, and a genuinely
destructive one — commits become unreachable once the branch ref is gone),
that should be a deliberate, explicit decision, not a side effect of this
consolidation.
