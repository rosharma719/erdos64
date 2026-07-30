# defect_q_ge6_audit.md — audit of the claimed "provisional q(G)>=6"

**Standing reminder, per project discipline: every proof referenced below
is a hand-written Markdown argument cross-checked by independent
computation. None of it is proof-assistant formal verification — no
Lean/Coq/Isabelle artifact exists anywhere in this project.**

## Verdict

\[
\boxed{q(G)\ge6\ \text{is NOT established. Neither is } q(G)\ge5.}
\]

The established frontier is unchanged:
\[
\boxed{q(G)\ge4,\qquad |E(G)|\le2|V(G)|-6}
\]
(`defect_three.md` Part VIII, `verification_status.md` row "q(G)>=4
(defect-three, Part VIII)"), proved by eliminating all six `(h,c1,c3)`
rows of the exact `q=3` case table.

An externally-pasted report circulated in an earlier session claimed a
"provisional `q(G)>=6`", said to rest on "17,010 exact configurations in
the one-hub `q=5` case, 146 two-hub core classes, 17,969 three-hub cores,
and all remaining four- and five-hub configurations." **No artifact
matching any part of that claim exists in this repository.** This audit
re-confirms, independently, the same conclusion an earlier audit reached
(recorded at `type_t_port_safe_4pole.md`, "Cross-reference: external
report on `q(G)>=4`/`q(G)>=6`").

## What was searched, and what was found

Searched across the full branch content and **all** local and remote
refs' history (`git log --all`):

| probe | result |
|---|---|
| filenames ever in history matching `defect_(four\|five\|4\|5)`, `q4`, `q5`, `q_ge` | **none, on any ref, at any commit** |
| commit subjects mentioning `q=4`, `q=5`, `q>=5`, `q>=6`, "defect four/five" | **none** |
| content grep for `q>=5`, `q>=6`, `q=4`, `q=5` elimination claims | only *forward references* and explicit **non-**attempt notes (below) |
| content grep for the report's vocabulary ("one-hub", "two-hub", "three-hub", 17,010 / 146 / 17,969) | **no match anywhere** |
| `verification_status.md` | last defect row is `q(G)>=4`; **nothing beyond** |
| `manifests/` (74 manifests) | defect manifests stop at `kernel_h3_c1c3_31` / `defect_three_table` — all `q=3` |
| `verifier/` | defect verifiers stop at `kernel_h3_*.py`, `q3_table_check.py` — all `q=3` |

Every `q=4` mention in the repository is an explicit statement that it
was **not** attempted, e.g. `defect_three.md` Part X's own stop point:

> "`q=3` is fully resolved (eliminated). This phase does **not** begin
> `q=4` […] — all explicitly out of scope for this phase."

and similar deliberate non-attempt notes in `contraction_atoms.md`
(Part VIII), `contraction_saturation.md`, `contraction_ma2_integration.md`,
`central_bridge_triangle_pole_forcing.md`, and `README.md`.

**Conclusion: there is no evidence that any `q=4` or `q=5` elimination
work was ever performed in this repository.** The `q(G)>=6` claim should
continue to be treated as unverified and must not be cited.

## The `q=3` elimination methodology — a concrete template

This is what a `q=4` attack would have to reproduce at larger scale. The
pipeline (`defect_three.md`) has six stages.

**Stage 1 — bound `h`, then derive the exact case table (Part II.1).**
From the already-proved leaf-compression relations:
- `h <= q` (unconditional), so `h ∈ {0,…,q}` — this is a *derivation*,
  not a search;
- `h=0`: `G` is cubic, `n = 2q+4`, `c1=0`, `c3=n`;
- `h=1`: `c1=0` is forced (a `C1`-vertex needs two **distinct**
  `H`-neighbours), so the leaf-count identity gives `c3 = 2q`;
- `h>=2`: the leaf-count identity `c1 = c3 + 4h - 2q - 4` with `c1>=0`,
  plus the strong inequality `c3 + 2h <= 2q + 1`, pins `c3` to a short
  interval.

At `q=3` this yields **exactly six** `(h,c1,c3)` rows. Every subsequent
stage exists to kill rows.

**Stage 2 — kill the small-order rows by citation (Part III).**
- `h=0` gives `n = 2q+4 = 10`, and P4 ("every `δ>=3` graph on `n<=19`
  vertices contains a C4 or C8", `proof.md`) closes it outright.
- `h=1` needs a genuine argument: branch-incidence (`<=1` `C2`-neighbour
  per `C3`-vertex), chain-length (`<=2` internal `C2` per kernel chain),
  and no kernel self-loops together bound `c2 <= 2q`, hence
  `n <= 1 + 2q + 2q = 4q+1`. At `q=3` that is `n<=13`, exactly where the
  `P_13`-free theorem (L7) applies.

**Stage 3 — the colored degree-2 path lemma (Part IV).** A maximal
degree-2 path of `C2`-vertices, each with a unique `H`-neighbour
`χ(i)`, admits a C4/C8-avoiding coloring only up to a hard maximum
length `t(h)`. Proved `t = 2, 5, 8` for `h = 1, 2, 3`, each tight, by
**two implementations independent by construction**: a prefix-closed
BFS over explicitly built graphs, and a minimal finite-state automaton
whose state space is finite *by construction* (a 6-window plus
arc-age counters saturating at 4). Completeness comes from
prefix-closure, not from a cutoff.

**Stage 4 — the colored cycle components (Part V).** Pure-`C2`
components are cycles; deleting one wraparound edge reduces them to
Stage 3's linear setting, so the same `t(h)` ceiling applies. Result:
no valid pure-cycle component at `h=1,2`; exactly `s ∈ {3,5}` at `h=3`.

**Stage 5 — kernel suppression, then enumerate topologies.** Contract
every maximal `C2`-path to a single edge. The result is a multigraph on
the `c1+c3` kernel vertices with degrees inherited exactly (1 for `C1`,
3 for `C3`). Parity (handshake, per component) restricts how the kernel
vertices split across `F`-components; `verifier/kernel_topology_enum.py`
then enumerates **every** connected multigraph with the given degree
sequence by exhausting a finite stub-matching set, deduplicated by VF2
isomorphism — complete because the matching set is finite, not because
a search terminated.

**Stage 6 — reconstruct and test, exhaustively.** Every kernel edge is
re-expanded into a direct edge or a colored path drawn from Stage 3's
already-proved-complete valid-word lists; a backtracking search discards
a partial assignment the instant a C4/C8 appears (sound by subgraph
monotonicity — completing the remaining edges can only add cycles).
`0 survivors` in every case closes the row.

Stages 3–6 are *computer-assisted finite certificates*: each is an
exhaustive procedure over a provably bounded space. Stages 1–2 and
several row arguments (the theta pigeonhole, the lollipop `β=1`
identity, the `H`-degree feasibility argument) are hand proofs.

## How much harder is `q=4`? — quantitative assessment

All numbers below are produced by `verifier/defect_q4_prerequisites.py`,
which **first reproduces every corresponding `q<=3` PROVED baseline** and
refuses to report if any baseline fails.

### Growth driver 1: number of case-table rows

| `q` | rows | max kernel vertices (`h>=2`) | max kernel edges |
|---|---|---|---|
| 1 | 2 | 0 | 0 |
| 2 | 4 | 2 | 1 |
| 3 | **6** | 4 | 5 |
| 4 | **10** | 6 | 8 |
| 5 | **14** | 8 | 11 |

The `q=1,2,3` counts reproduce the documented tables in `defect.md`
Part II/III and `defect_three.md` II.1 exactly. Row growth alone is mild
(6 → 10 → 14).

### Growth driver 2: the colored-path ceiling `t(h)`

`q=4` admits `h=4`, and `q=5` admits `h=5` — values Part IV never
covered. Extending Part IV's own two implementations (see below):

| `h` | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| `t(h)` | 2 | 5 | 8 | **12** | **18** |
| valid colored words | 2 | 18 | 258 | **5,588** | **370,170** |

`h=1,2,3` are the PROVED values, reproduced exactly (including the word
totals, which match the level sums in
`manifests/colored_path_search_manifest.json`). **`h=4` and `h=5` are new
here and are `COMPUTATIONALLY VERIFIED` only** — see the labels section.

The word count is the per-kernel-edge branching factor in Stage 6. It
grows **~22x** from `h=3` to `h=4` and **~66x** from `h=4` to `h=5`.

### Growth driver 3: the Stage-6 search space

Naive realization count for a row `= (valid words at that h)^(kernel edges)`:

| `q` | worst row | kernel edges | branching | naive realizations |
|---|---|---|---|---|
| 3 | `h=3, (3,1)` | 3 | 258 | `1.7e7` |
| 4 | `h=4, (5,1)` | 4 | 5,588 | `9.8e14` |
| 5 | `h=5, (7,1)` | 5 | 370,170 | `7.0e27` |

At `q=3` the actual backtracking explored `41,958` realizations for the
worst row — roughly a 400x prune against the `1.7e7` naive figure. **Even
granting the same pruning ratio, `q=4`'s worst row leaves ~`2.4e12`
realizations, and `q=5`'s ~`1.7e25`.**

**Assessment.** `q=4` is *not* a "run the same scripts on bigger inputs"
task. The case-table growth (6 → 10 rows) is mild and the kernel topology
counts stay small (the `q=4` degree sequences enumerate to 5, 3, 2, 1, …
connected shapes, comparable to `q=3`'s 2 and 3). The barrier is
**Stage 6**: roughly **seven to eight orders of magnitude** more
reconstruction work than `q=3`, driven almost entirely by the `h=4`
branching factor of 5,588 valid colored words. Closing `q=4` by direct
extension of the existing method would need at least one genuinely new
structural lemma that prunes before reconstruction — the role played at
`q=3` by the `H`-degree feasibility argument (Part VII.1–2), which
collapsed an entire row to the single length `t=8` before any search ran.
`q=5` is a further ~13 orders of magnitude beyond `q=4` and is not
plausibly reachable by this route at all without a different idea.

### One genuine simplification found

At `q=4`, **two of the ten rows are already closed by existing proved
results**, with no new work:
- `h=0`: `n = 2q+4 = 12 <= 19`, so P4 applies directly.
- `h=1`: Stage 2's chain of bounds never uses the value of `q` — it uses
  only `h=1` and C4-freeness — so it gives `n <= 4q+1 = 17 <= 19`, and P4
  applies again. (At `q=3` this bound is the documented `n<=13`.)

So the genuinely open part of `q=4` is the **eight rows with
`h ∈ {2,3,4}`**. Note this simplification does **not** persist: at `q=5`,
`h=1` gives only `n <= 21 > 19`, so P4 no longer suffices there.

**Label:** this two-row observation is `DERIVED_IN_THIS_AUDIT` — it
follows by inspection from the `q`-independence of `defect_three.md`
III.2's argument together with P4, but it has **not** been independently
re-verified computationally, and it eliminates two rows of `q=4`, not
`q=4` itself.

## What this audit added

`verifier/defect_q4_prerequisites.py` (+
`manifests/defect_q4_prerequisites_manifest.json`) computes, and
self-checks against PROVED baselines:
1. the exact `(h,c1,c3)` case tables for `q=4` (10 rows) and `q=5`
   (14 rows), reproducing `q=1,2,3` exactly;
2. the colored-path bound extended to `t(4)=12` and `t(5)=18`, by the
   two independent implementations of Part IV, which agree;
3. the valid-word branching factors above.

The `h=4`/`h=5` path search uses a color-symmetry reduction (restrict to
words whose first color occurrences appear in increasing order). This is
sound: permuting `H`-colors is a graph isomorphism of the realized graph,
every word has a canonical representative of the same length, and every
prefix of a canonical word is canonical — so the canonical set is still
prefix-closed and Part IV's emptiness argument applies verbatim. The
reduction reproduces `t=2,5,8` and the exact witness `a,a,b,b,a`
documented at `h=2`.

**These are prerequisites, not progress on the theorem.** They do not
eliminate any `q=4` row beyond the two noted above.

## Rigor labels

| claim | label |
|---|---|
| `q(G)>=4`, `\|E\|<=2\|V\|-6` | `PROVED_IN_MARKDOWN`, `COMPUTATIONALLY_REPRODUCED`, `NOT_FORMALLY_VERIFIED` (pre-existing) |
| `q(G)>=5` | **`NOT_ESTABLISHED`** — no argument, no artifact, never attempted |
| `q(G)>=6` | **`NOT_ESTABLISHED`** — external claim, zero matching artifacts; do not cite |
| `q=4`/`q=5` case tables (10/14 rows) | `DERIVED` from PROVED relations (pure algebra) + `COMPUTATIONALLY_VERIFIED` (reproduces `q=1,2,3`) |
| colored-path `t(4)=12`, `t(5)=18` | `COMPUTATIONALLY_VERIFIED` (two independent implementations agree; baselines reproduced), `NOT_PROVED_BY_HAND` |
| valid-word counts at `h=4,5` | `COMPUTATIONALLY_VERIFIED` (the `h<=3` totals reproduce the PROVED search exactly) |
| `q=4` rows `h=0,1` fall to P4 | `DERIVED_IN_THIS_AUDIT`, `NOT_INDEPENDENTLY_REVERIFIED` |
| search-space growth estimates | `HEURISTIC` — order-of-magnitude only; assumes `q=3`'s pruning ratio carries over, which is not proved |
| anything about `q=4` being *impossible* | **no such claim is made here** |
