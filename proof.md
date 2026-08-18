# proof.md — Erdős #64: consolidated status of proof / counterexample work

**Consolidated 2026-08-18 from seven research branches. The conjecture is
OPEN. Nothing here claims resolution.** This file separates rigorously
established progress from conjectural observations. Every assertion carries
a label.

> **Conjecture (Erdős–Gyárfás, 1995).** Every finite simple graph with
> minimum degree ≥ 3 contains a simple cycle whose length is a power of two.

Throughout, `F = {4, 8, 16, 32, …}`, a graph is **F-clean** if it has no
cycle of length in `F`, and `G` denotes a **minimal counterexample**: a
graph minimizing `(|V|,|E|)` lexicographically among δ≥3 F-clean graphs.
`q(G) := 2n − 2 − m` is the ordering defect. No F-clean δ≥3 graph is known
to exist at any order; every "structure of `G`" statement below is
conditional on that hypothetical object.

## Verdict

No proof and no counterexample. What follows is honest partial progress.
The five live tracks are (A) small-order exhaustive search, (B) the
separator / connectivity program for a minimal counterexample, (C) the
contraction / Type-N–Type-T local program, (D) the Type-T C16 port
completion, and (E) the order-30 cubic census.

## Labels used in this file

The base repository's five labels are used verbatim and are never widened:

- **PROVED** — a complete human-readable mathematical proof exists in this
  repository. It is *not* machine-checked; see `verification_status.md`,
  which tags every such item `NOT_FORMALLY_VERIFIED`. No Lean/Coq/Isabelle
  development exists anywhere in this repository.
- **COMPUTATIONALLY VERIFIED** — established by an exhaustive, certified
  computation whose command, counts, exit codes and checksums are recorded.
- **CONJECTURAL** — stated, not established.
- **DISPROVED** — refuted, with the exact witness or obstruction recorded.
- **KNOWN FROM LITERATURE** — cited, with the exact source.

Branch-specific qualifiers are carried forward **unchanged**, never
upgraded. In particular `NOVELTY SUPPORTED BY SEARCH`,
`NOVELTY UNCHECKED`, `BOUNDED_INCOMPLETE`, `INCOMPLETE_RANGE`,
`COMPLETE_RELATIVE_TO`, `NOT_ESTABLISHED`, `CLAIM_REFUTED` and
`PROVED_IN_MARKDOWN` appear exactly where their originating branch put
them. `verification_status.md` is the full row-by-row matrix; this file is
the narrative summary.

---

# Part I — Structure of a minimal counterexample

### P1 [COMPUTATIONALLY VERIFIED] No counterexample on ≤ 11 vertices
Exhaustive over all connected δ≥3 graphs (nauty `geng -c -d3`), tested by a
validated power-of-two cycle detector (two independent implementations, 0
disagreements on 2107+3377 cross-checks). n=4..10 confirmed by BOTH a Python
and a C checker with identical graph counts; n=11 (577,076,528 graphs) by
the C checker. Reproduces the lower part of Royle–Markström's ≥17 (L10)
from scratch. The n=12 brute run was TERMINATED 2026-07-24 at
947M/~30e9 graphs as strategically redundant; `INCOMPLETE_RANGE` beyond 11.

### P2 [PROVED] Minimal-counterexample degree structure, re-derived
- **B0.** `G` is C4-free (4∈F), hence `m ≤ ½(1+√(4n−3))n` (Kővári–Sós–Turán).
- **B1.** `G` is connected.
- **B3 = M1.** Every edge has a degree-3 endpoint ⇒ degree-≥4 vertices form
  an independent set; ≥1 degree-3 vertex exists. (Deletion-minimality.)
- **B4.** Every neighbor of a degree-≥4 vertex has degree exactly 3.
- **M3.** `n₃ ≥ (4/7)n` (Carr's original double count).
- **G1.** `n₃ ≥ (2/3)n`. [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH]
  M2 applied also to cubic vertices improves the high–low upper bound from
  `3n₃` to `2n₃`. Audited against Carr's full preprint text (L18).
- **G2.** `m ≤ 2n−3`. [PROVED IN WORKSPACE, KNOWN INGREDIENTS] Delete a
  cubic vertex; the remainder is 2-degenerate. Equality at `2n−2` would be
  degree-3-critical and hence contain a C4 (EFGS).
- **G3.** `q = 2n−2−m ≥ 1` is the exact nonnegative deficit of a
  2-degeneracy ordering of `G−v`; hence `Σ(d−3) ≤ n−6`.
- **M4.** A regular minimal counterexample is cubic.

B0/B1/B3/B4/M3/M4 independently reproduce Carr 2026 (arXiv:2605.22844)
M1/M3/M4 from scratch — validation, not new progress. M2 for degree-3
vertices remains Carr's (not re-derived). Full proofs and novelty audits:
`lemmas.md` B0–G3, `literature.md` L18–L19.

### P8 [mixed — see `defect.md` Part II] Defect-one theorem D1
D1 ("does δ≥3 + Carr's property (2) + `m=2n−3` force a C4/C8, for *any*
such graph?") is **neither proved nor refuted**.
**[PROVED]** `h=0` forces `n=6` exactly; both graphs (K₃,₃, prism) contain
a C4. **[DISPROVED]** D1C (a proposed nonedge-completion lemma) fails
starting `n=9` (3 witnesses; 172 further failures by `n=12`).
**[COMPUTATIONALLY VERIFIED, INCOMPLETE_RANGE]** 0 counterexamples to D1
among 1,128 property-(2) graphs, `n=6..12` exhaustive, two independent
generation routes agreeing exactly at `n=6,7`; `n=13` (17.4M raw graphs)
attempted, did not complete.

### P9–P12 [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH] q(G) ≥ 4
A single ladder of results, each strictly extending the previous one, all
proved through the **derived leaf graph** `L(G)` and the leaf-count
identity `c1 = c3 + 4h − 2q − 4` with `h ≤ q` (`defect.md` leaf-compression
Part I; `lemmas.md` I.1–I.3):

- **P9. `q(G) ≥ 2`, `|E| ≤ 2|V|−4`.** `h=0` forces `n=6`; `h=1` forces
  `c3=2`, giving a direct C4 (`z–a–u–b–z`), verified exhaustively on 74
  graphs `n=7..12`. Strictly improves G2.
- **P10. `q(G) ≥ 3`, `|E| ≤ 2|V|−5`.** All three `h∈{0,1,2}` cases
  eliminated (`h=0`⇒`n=8`; `h=1`⇒`c3=4`, verified on 384 graphs; `h=2`
  ⇒`c1=c3≤1`, a period-4 cycle-coloring argument and a handshake-lemma
  lollipop pendant-path argument). A real arithmetic error in the previous
  phase's weighted-incidence cycle formula (coefficient `t → 2t`) was
  caught and fixed while deriving this; re-verified on 3,000 synthetic
  constructions.
- **P12. `q(G) ≥ 4`, `|E| ≤ 2|V|−6`.** All six `(h,c1,c3)` rows of the
  exact `q=3` case table eliminated. `q=3` is odd, so the separator-defect
  mapping (P5/S5) forces `G` 2-connected. New machinery: the bounded
  branching-kernel lemma; the exact colored degree-2 path lemma
  (`t ≤ 2,5,8` for `h=1,2,3`, **two independent implementations**, 0
  mismatches over 29,655 words); the colored cyclic-word classification;
  a general stub-matching topological-kernel enumerator.
  Full detail: `defect_three.md`.

**Deduplication note.** `q(G) ≥ 4` appears verbatim in the `proof.md` of
both `claude/erdos-gyarfas-handoff-l6tqlo` and
`claude/graph-counterexample-q6-xerdjz`. These are **not** two independent
derivations: git ancestry shows the latter is a strict descendant of the
former, so it inherited the result rather than re-deriving it. Stated once
here, credited to the single derivation in `defect_three.md`.

### P13 [DERIVED + COMPUTATIONALLY VERIFIED] q=4 / q=5 prerequisites only
Not progress on the theorem — **inputs only**. Exact `(h,c1,c3)` case
tables at `q=4` (10 rows) and `q=5` (14 rows), derived symbolically and
reproducing the documented `q=1,2,3` tables (2/4/6 rows) exactly; the
colored degree-2 path bound extended to `t(4)=12`, `t(5)=18` by the same
two independent implementations. Heuristic scaling: `q=4`'s worst row needs
~7–8 orders of magnitude more Stage-6 reconstruction than `q=3`.
See `defect_q_ge6_audit.md`.

---

# Part II — The separator / connectivity program

### P5 [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH] S4, S5
**S4 (bridgelessness).** A minimal counterexample has no bridge.
**S5 (cut-vertex classification).** If `v` is a cut vertex of `G`, then
`G−v` has exactly two components; `v` has exactly two neighbors in each
(so `deg v = 4`); the two lobes have equal order (forcing `n` odd) and
equal edge count; and `G` has at most one cut vertex.

Both proved from B0–B4/M1–M4 by a degree-preserving **doubling**
construction (glue two copies of a lobe at their shared low-attachment
vertex). This supersedes the stalled B2 attempt (unsafe suppression); no
suppression is needed. Two targeted literature passes (L16, L17) found no
prior statement; the closest classical analog is Dirac 1953 (k-critical
graphs have no cut vertex) — same technique, different theorem.
**Label ceiling, permanent from this environment:** arXiv and every tested
mirror return HTTP 403 at the platform level (confirmed by direct `curl`
through the egress proxy, not only the fetch tool), so `NOVELTY SUPPORTED
BY SEARCH` can never be upgraded from here. See RETROSPECTIVE.md — this is
a tooling gap, not a mathematical one.

### P7b/P7c [PROVED / mixed] One-pole gadget theory O1–O7
A **one-pole graph** `H` is connected with one distinguished root `r` of
degree 2 and every other vertex of degree ≥3. A single F-clean one-pole
survivor, doubled at its root, is already a full counterexample — no
minimality needed. Under *master minimality* (smallest object, order then
size, among {plain F-clean δ≥3 graphs} ∪ {F-clean one-pole graphs}):

- **O1 [PROVED]** `H` is bridgeless. **O2 [PROVED]** `H−r` is connected.
  **O3 [PROVED]** `H` is fully 2-connected — strictly stronger than S5's
  "at most one cut vertex" for `G`, because peeling a piece off a one-pole
  graph always strictly shrinks it.
- **O4 [CONJECTURAL]** — whether `H−r` contains two disjoint
  root-neighbour paths remains open.
- **O4′ [PROVED, KNOWN FROM LITERATURE ingredient]** Every master-minimal
  one-pole graph has two cycles through its root differing in length by 1
  or 2. Obtained by applying Gao–Huo–Liu–Ma 2022 with `k=2`, after proving
  `K+ab` 2-connected by classical degree-2 suppression. Path disjointness
  is **not** needed and **not** claimed.
- **O4a [PROVED IN WORKSPACE]** If two disjoint root-neighbour paths do
  not exist, Menger gives a 1-vertex separator `x` splitting `H−{r,x}` into
  exactly two lobes attached to both `r` and `x`. Exact terminal-spectrum
  identity: cross-lobe cycle lengths `= Λ₁+Λ₂`; doubling one lobe creates
  new cycles of length exactly `Λᵢ+Λᵢ`.
- **O5 [PROVED, COMPUTATIONALLY REPRODUCED]** *Rigid core, unconditional.*
  Every master-minimal one-pole graph has a K4-minor — its SPQR tree
  contains at least one rigid (R) node — from the degree profile plus
  2-connectivity alone, independent of F-cleanness. Two independent
  proofs: an SPQR-leaf argument, and a partial-2-tree argument via Dirac
  1961 on chordal graphs. Cross-checked against 304 series-parallel graphs
  (0 violations) and against two initially plausible hand-built
  "counterexamples" that a direct SPQR computation rejected — kept in the
  record as an error log.
- **O6 [PROVED]** Proper two-pole forcing: for a proper connected subgraph
  `P` with terminals `x,y`, if `H_P` is lexicographically smaller than `H`
  then `Λ(P) ∩ {2ᵏ−2} ≠ ∅`.
- **O7 [PROVED, COMPUTATIONALLY REPRODUCED]** No external common
  neighbour: a remote leaf R-node's virtual edge cannot sit in a triangle
  whose other two edges are both real.
- **Suppressed-edge equivalence [PROVED].** A one-pole graph exists iff
  there is a loopless `Gₑ` with δ≥3 and a distinguished edge `e` such that
  every F-cycle uses `e` while no `e`-using cycle has length in
  `F⁻ = {2ᵏ−1}`.
- **Empirical status of "exactly one R-node": explicitly NOT conjectured.**
  O6+O7 leave 4,717 of 5,525 K4 skeleton-clean configurations, and 26
  relaxed one-pole graphs satisfy every proved local condition while
  remaining non-F-clean (smallest `n=8`, g6 `GCQVRw`).

Full detail: `one_pole.md`, `manuscript.md` §3.

### P14 [PROVED / COMPUTATIONALLY VERIFIED] The 2-cut trichotomy and the F-series
For a 2-connected minimal counterexample, every 2-cut is exactly **Type A,
B or C** by terminal-degree profile (`two_cut.md` §2c,
`separator_theorem_order32_gap_analysis.md` §2c) — the trichotomy is
order-independent. Per-bridge order floors, each a statement about a
two-terminal graph `B` in isolation with no reference to any ambient `G`:

| result | statement | label |
|---|---|---|
| **F12** | every two-terminal `B` with `\|V(B)\|=12`, `d_B(x)=1`, `d_B(y)≥1`, `xy∉E(B)`, internal degree ≥3, `B+xy` simple 2-connected, contains a C4 or C8 | COMPUTATIONALLY VERIFIED, exhaustive, dual-detector |
| **FC-15** | same with `d_B(x)=2`, `d_B(y)≥2`, `\|V(B)\|≤15` | COMPUTATIONALLY VERIFIED, exhaustive, dual-detector |
| **F13–F19** | the `d_B(x)=1`, forbidden `{4,8}` series is UNSAT contiguously through 19 | COMPUTATIONALLY VERIFIED (SAT graph-existence) |
| **FC-18** | the `(2,*)`-terminal series is UNSAT through 18 | COMPUTATIONALLY VERIFIED |
| **FC-19/20/21** | **FALSE** for forbidden `{4,8}` — verified C4/C8-free `(2,2)`-terminal survivors exist | DISPROVED |

By monotonicity (any UNSAT with forbidden set `S` stays UNSAT for `S' ⊇ S`),
F13–F19 also hold for `{4,8,16}`. Combining the resulting per-bridge floors
with `n(G) = n₁+n₂−2`:

- **Type A** `n ≥ 56`, **Type B** `n ≥ 38`, **Type C** `n ≥ 36`
  (`order32_bounds_f19_extension.md`; Type C is binding).
- **[COMPUTATIONALLY VERIFIED]** *If a minimal counterexample has any
  2-cut, then `|V(G)| ≥ 36`.*
- **[PROVED, O32-1]** If `|V(G)|` is even, `G` has no cut vertex (S5's
  parity argument: a cut vertex forces two equal-order lobes, hence odd `n`).

> **Corollary [COMPUTATIONALLY VERIFIED].** *Every minimal Erdős–Gyárfás
> counterexample of even order `n` with `17 ≤ n ≤ 33` is 3-connected.*
> Covers `n ∈ {18,20,22,24,26,28,30,32}`.

**Recorded inconsistency, deliberately not resolved here.**
`three_connectivity_general_order.md` states the range `[17,33]` using the
pre-F19 floor `min(35,34,36)=34`. `order32_bounds_f19_extension.md`'s title
and table give the post-F19 floor `min(56,38,36)=36`, which would extend
the corollary to `[17,35]`, but that same file's prose then asserts the
range is "unaffected" on the (incorrect) ground that 36 was already
binding. The `[17,33]` form is implied under either reading and is what is
asserted above; **`[17,35]` is a plausible free strengthening that has NOT
been independently re-derived here and must be checked before use.**

Odd orders in `[17,33]` are **not** resolved: the 2-cut branch is closed
for them too (the `≥36` floor is parity-independent), but the cut-vertex
branch is not.

### P15 [PROVED] Cubic 3-edge-connectivity in the same range
*Let `G` be a cubic minimal counterexample with `|V(G)|` even and
`17 ≤ |V(G)| ≤ 33`. Then `G` has no edge cut of size 1 or 2.*
Immediate from Whitney's inequality `κ ≤ λ ≤ δ` together with P14's
`κ(G) ≥ 3` and `δ(G)=3`, forcing `κ=λ=δ=3`. S4 gave only the size-1 case,
by a different argument; the size-2 case was previously absent from this
project (flagged as missing in
`separator_theorem_order32_gap_analysis.md`). See `cubic_edge_connectivity.md`.

---

# Part III — The contraction / Type-N–Type-T local program

Established by contracting a vertex set `A` of a minimal counterexample and
lifting the quotient's forced power-of-two cycle back. All items below are
`PROVED_IN_MARKDOWN`; the mechanical parts are `COMPUTATIONALLY REPRODUCED`
on fixtures, while the "same-side is impossible" steps are minimality
arguments about a hypothetical object and are *not* independently testable
(same status as S4/S5). Full detail in `contraction*.md`.

- **Near-power edge lemma [PROVED].** Every nontriangle edge of a minimal
  counterexample lies on a cycle of length `2ᵏ+1`. Cross-checked on 34
  fixtures, 249 nontriangle edges, 35,357 lifted cycles, 0 failures.
  **Audit correction:** the stronger reading "every edge has a `2ᵏ+1`
  witness" traces through only for **nontriangle** edges
  (`every_edge_witness_audit.md`).
- **General atom-lifting lemma [PROVED].** Generalizes the above to any
  connected `A` with (H2) no outside vertex having 2 neighbours in `A` and
  (H3) `|∂A| ≥ 3`.
- **Safe-contraction obstruction [PROVED].** No nontriangle edge of a
  minimal counterexample is ever safe; the proposed "global safe-edge
  target" is logically equivalent to the conjecture itself, **not** an
  easier sub-target.
- **Type N / Type T dichotomy [PROVED].** Every cubic vertex of a C4-free
  graph has exactly 1 or exactly 3 nontriangle incident edges, never 0 or
  2 — equivalently, 0 internal edges among its three neighbours (**Type N**)
  or exactly 1 (**Type T**, with a unique triangle). The global target
  "neither type occurs in a minimal counterexample" is explicitly **NOT**
  established.
- **Type N witness system [PROVED, no contradiction].** Exactly 2
  isomorphism types of loopless 3-element functional digraphs; a five-lemma
  arithmetic toolkit applied to both. Neither orientation type is
  eliminated. The four combined endpoint orbits at a Type-N vertex are
  **unconditionally safe for every exponent choice** — the clean local
  system alone never produces a contradiction.
- **Cell-decomposition identity, non-crossing case [PROVED].** For two
  same-endpoint simple paths with common vertices in the same relative
  order, `|P|−|Q| = Σ(αᵢ−βᵢ)` over divergent cells, each divergent cell
  yielding a cycle of length `αᵢ+βᵢ`.
- **One-cell reduction target [DISPROVED].** The canonical joint witness
  choice does not force exactly one divergence–reconvergence cell; smallest
  exact obstruction has 0 shared edges, 0 common components and 2 divergent
  cells, both safe 5-cycles.
- **Crossing case [OPEN].** Common vertices in different relative order
  along the two paths is explicitly NOT resolved.
- **CB1 (central return) [PROVED]**, endpoint-return normal form
  [PROVED], topological-K4 reduction for interior return [PROVED,
  exhaustive per instance], MA1/MA2 (multi-attachment admissible-pair
  lemma, central bridge trichotomy) [PROVED].
- **Theta-saturation target VI.5 [OPEN]** — substantial partial progress
  (the S5-grounded "at most one saturated theta-internal vertex" bound),
  neither proved nor disproved.
- **CB2, the one-excursion target [NOT PROVED OR DISPROVED]** — a
  structurally valid two-excursion itinerary is exhibited but explicitly
  not certified as canonical.

### Type-T triangle results

- **Lemma NE [PROVED].** No two cubic triangle vertices share an external
  neighbour (else a C4).
- **Pole-forcing theorem [PROVED, COMPUTATIONALLY REPRODUCED].** *The
  aligned pole `X_x` of a cubic Type-T vertex `x` can never be cubic.* If
  `X_x` were cubic its three edges are pinned; `P_2` must avoid `Y_x`, so
  `P_1` is forced through `Y_x`, and the chord `e_x = x–Y_x` closes a simple
  cycle of length exactly `2^{ρ_x}`. Verified on explicit gadgets for
  `ρ_x ∈ {2,3,4,5}`. **Consequence: T3 is eliminated outright, and T2 is
  narrowed to `X_x = X_y = z₀`, the unique non-cubic triangle vertex.**
- **Theorem 2.1 (complete composition classification) [PROVED].** For two
  actual simple paths with divergent colored edge totals `m,n`, `T=m+n`,
  and a noncrossing symmetric-difference decomposition into `k` divergent
  cells with `aᵢ+bᵢ ≥ 3`: `k=1` with `T` dyadic is FORCED; `k=1` with `T`
  not dyadic is UNIVERSALLY SAFE; `k≥2` with `T=3k` is UNIVERSALLY SAFE;
  `T=3k+1` is forced; `T ≥ 3k+2` is escapable but not universal.
  (`type_t_overlap_reduction.md` §2.)
- **The alternating ladder family [PROVED as an abstract object;
  STRUCTURALLY SUPERSEDED as a Type-T residual].** An explicit infinite
  colored family showing no finite core list bounds the incidence
  structure in general. Its premise is the identical-terminal row
  `X_x=y, X_y=x`, which the pole-forcing theorem already excludes
  (both assumed poles are cubic). Recorded as a genuine self-correction:
  the family is real, its Type-T application is not
  (`type_t_ladder_saturation.md` Theorem 1.1).
- **The "single unresolved Type-T yes/no question" is CLOSED, not open.**
  `type_t_identical_terminal_joint_spectrum.md` reduced the entire
  identical-terminal residual to one question: can `Θ_x`'s and `Θ_y`'s
  `P₁` branches share an internal vertex? That reduction is correct, but
  the row it lives in (`X_x=y, X_y=x`) is eliminated by the pole-forcing
  theorem, so the question is moot as a Type-T residual. **Any handoff
  that still lists it as the top open item is out of date.**
- **R2/S2 [CLAIM_REFUTED].** An earlier pinned R2/S2 claim was never
  obtained: T2's admissible pair need not include the shortest path. If
  the claimed length-4 paths are assumed, cubic incidence forces two C4s;
  the proposed length-9 object repeats vertices and is not simple.
  Refuted by explicit Heawood- and Balaban-derived counterexamples
  (`type_t_recovery_audit.md`).
- **Joint two-central-bridge Type-T interaction [NOT ATTEMPTED].**
  Identified across the whole six-file contraction sequence as the single
  highest-value remaining target (`contraction_ma2_integration.md` Part X,
  `contraction_separator_integration.md` Part IX). Deliberately deferred
  rather than attempted under time pressure.

### Type-B realizability

- **[PROVED, EXHAUSTIVE FINITE COMPUTATION] B19/B20/B20D2.** Every bridge
  role of all 16 frozen Type-B tuples with original bound ≤40 has order
  ≥21, so **all 16 reach full-graph order ≥40**. Stated narrowly for the
  frozen tuple family, not as a general Type-B or global bound.
  Certificates: 86,047 exact-degree-box candidates all containing a C8
  (four independent detectors: Python DFS, networkx, a from-scratch C
  implementation, and a SAT cycle-position encoding); 54 and 12 slot-matched
  candidates from **two independently coded generators** (C backtracking,
  PySAT) whose canonical sets agree by matching SHA-256, each eliminated by
  a third independent networkx verifier.
- **[NOT RESOLVED] ICF** and the general Type-B realizability question
  remain open.

---

# Part IV — Type-T C16 port completion

The minimum cubic Type-T port completion problem: given a fixed bare core
`H(j,a,c)`, can it be completed to a cubic graph with no C4, C8 or C16?
All three bounded `j=4` exact CEGAR runs returned `UNKNOWN` — **no
counterexample and no UNSAT certificate**. The static compilation program
below replaces ad hoc CEGAR cuts.

### C16-1 [PROVED] Support-bound theorem (the foundation of the whole track)
Contract each traversal through a new hub to a weighted passage. For a
simple cycle of length `L` with `m` hub passages and `r` hubs used
(`m ≤ r ≤ 2m`):
```
L = route_total + core_total ≥ (m + r) + m = 2m + r,   hence   m ≤ ⌊L/3⌋.
```
Combined with the proved fact that no candidate triple or gadget can close
a dyadic cycle by itself (so `m ≥ 2` always, for **every** dyadic `L`):

- **C4 (`L=4`): no admissible `m` — C4 conflicts cannot exist** beyond the
  base local-safety screen.
- **C8 (`L=8`): `m = 2` exactly**, support size 1 or 2, never larger.
- **C16 (`L=16`): `m ∈ {2,3,4,5}`**, variable-count `v ≤ 5`; unit `C16`
  cuts are combinatorially possible and must be searched for.

Consequently `Φ_{4,8} =` exact-cover base clauses `+` C8 conflicts at `m=2`
is **exactly complete** for `{C4,C8}` with no CEGAR loop.

### C16-2 [PROVED, unconditional] Bare-core dyadic avoidance for all j
*The bare core `H(j,a,c)` avoids every dyadic cycle length, for every valid
`j ≥ 4` and every valid `a,c`.* The 61-cycle spectrum fits 35 affine forms
`ℓ(j) = A·2ʲ + B` with integer `A ∈ {0,1,4,5}`; a 2-adic valuation argument
(`A=0` constants; `A>0,B=0`; and for `A>0,B≠0`, `v₂(A·2ʲ+B)=v₂(B)` once
`j > v₂(B)`, with every form having `v₂(B) ≤ 3`) shows none is ever a power
of two. Completeness of the 35 forms — the one gap when this was first
written — was subsequently closed by an independent kernel/cycle-space
derivation (`verifier/type_t_port_kernel_cycle_space.py`).
This closes the precondition both the template-lifting and C16-passage
lines had flagged UNKNOWN. See `type_t_port_core_dyadic_avoidance.md`.

### C16-3 [PROVED] Passage-support soundness (lifting) theorem
If a passage-based cycle candidate `(P₁,…,P_k; s₁,…,s_k)` is supported by
`G`, then `C = (⋃V(Pᵢ) ∪ ⋃V(sᵢ), ⋃E(Pᵢ) ∪ ⋃E(sᵢ))` is a **simple cycle
subgraph of `G`, regardless of any other edge of `G`** — in particular
regardless of unused attachments of any supplying hub and of every edge of
every other selected triple/gadget. This is what licenses reasoning at
passage level rather than gadget level.

### C16-4 [COMPUTATIONALLY VERIFIED] Passage-level projection and catalogs
Projecting gadget-level conflicts to passage-level variables collapses the
C8 catalog by **128.9×** for `(4,55,7)` (543,601 → 4,218 clauses) and
**206.7×** for `(4,28,4)` (1,122,615 → 5,432), cross-validated against the
already-verified gadget-level catalog.

Exact fixed-instance C16 stage ledger for `(j,a,c) = (4,55,7)`:

| stage | status | verified minimal supports |
|---|---|---:|
| `m=2` | complete outright | 32,921 |
| `m=3` | complete outright | 279,859 |
| `m=4` | complete outright (closed 2026-07-30) | 3,971,519 |
| `m=5` | **COMPLETE_RELATIVE_TO the `C8/m2/m3` lower shadow** — predates `m=4`, needs one rerun | 2,944,894 |

The `m=5` run covered all 87/87 canonical start vertices, pruned
157,006,598 branches against 316,684 certified lower-shadow supports,
reconstructed a literal simple 16-cycle for every one of the 2,944,894
survivors (rejecting zero), and cross-checked a 2,000-support sample with a
structurally different verifier (again rejecting zero). A measured estimate
says the rerun against the `m=4` shadow will drop ≈4.8% of them.

**What this does not claim.** The four layers have **not** been assembled
into a full passage CNF, and the assembled formula's satisfiability is
entirely unknown. *Compiling a complete conflict catalog is not evidence
either way about UNSAT.* The Type-T branch is not eliminated by anything
in Part IV.

### C16-5 [COMPUTATIONALLY VERIFIED] A real soundness bug, caught by redundancy
`verify_passage_conflicts` materialized a full *supplying* triple/gadget —
including attachments irrelevant to the claimed passage — and accepted a
support whenever any cycle was found in that graph, which can succeed via
an unintended cycle through the supplier's other, unclaimed edges. It was
invisible to either algorithm's self-consistency and surfaced **only** as a
disagreement between two structurally different implementations
(5,007 vs 5,052 verified minimal C8 supports on `(4,55,7)`). Fixed by
materializing a minimal graph containing only the literally claimed
passages; after the fix both implementations agree exactly at
**5,007 / 5,044 / 6,359** supports for `(4,55,7)/(4,2,2)/(4,28,4)`. The
previously reported 5,052/5,084/6,386 were each inflated by ~40–60
false-positive verifications and are **retracted**.

### C16-6 [BOUNDED_INCOMPLETE] The parallel gadget-level static SAT line
`tracks/type-t-c16-static-sat/` carries the one commit of
`codex/type-t-overlap-reduction` not contained in the main chain: a
gadget-level static compilation of instance `(4,28,4)` — complete exact
`C4/C8` layer (579 core paths, 286,011 literal C8s, 227,725 minimized
clauses, 0 C4 supports) and a merged bounded C16 catalog of **84,936**
inclusion-minimal supports (569 unary / 24,252 / 29,172 / 16,497 / 14,446
by support size). Its residual projection is **still SAT**, so the catalog
is explicitly **incomplete** and claims no obstruction theorem and no
counterexample. Its exact-cover multipole SAT runs end `UNKNOWN`, not
UNSAT, on the representative cores; all 324 ordinary `j=4` completions were
closed with no valid completion. Kept as a separate sub-track: the main
chain's passage-level representation supersedes the *representation*, but
this instance's data is not reproduced there.

---

# Part V — Voltage graphs and cyclic lifts

### P11 [COMPUTATIONALLY VERIFIED, exact and exhaustive] Z3 and Z5 lifts
Base graphs: four **source-certified** 24-vertex bases (Markström and three
Hegde–Sandeep–Shashank graphs at a frozen commit), each independently
confirmed C4/C8-free with C16 present; graph6/sparse6/edge checksums,
automorphisms, rank and two-detector certificates frozen in
`manifests/z3_bases_manifest.json`.

- **Z3, exhaustive.** All `6,377,288` nonzero assignments: 1,545,746
  survive C8, **zero** survive C16. Independently reproduced: a full
  C4 audit over all 6,377,288 assignments and a full audit of all 1,545,746
  C8 survivors, both with zero disagreements. All 1,545,746 C8 survivors
  are Type-1 (simple base C16, trivial holonomy); 0 instances of types 2–4.
- **Z5, exhaustive.** All `4 × 1,220,703,124 = 4,882,812,496` nonzero
  assignments checked exactly. Base 1 has exact 100% simple-C16-hyperplane
  coverage, certified by its **full 315-vector list** — a sample-based
  48-vector compression **FAILED** exact verification (21,156 exceptions)
  and is recorded as a failure, not used as a certificate. Bases 0, 2, 3
  have exactly 444, 72, 48 hyperplane-uncovered assignments; all 564 were
  independently lift-constructed and exactly resolved (148 at C8, 400 at
  C16, 16 at C32) — **zero survivors**. An independent NetworkX recheck
  agrees on all 564; a real projection-formula bug was caught and fixed en
  route.
- **[SUPERSEDED]** Every earlier *sampled* Monte-Carlo Z5 number is
  superseded, not supplemented; in particular its "≈0 coverage" claim for
  bases 0, 1, 3 was **wrong** (undershot).
- **Scope.** These eliminations are about *these four bases only*.

### P16 [COMPUTATIONALLY VERIFIED, negative] The A5 5-sheet lift construction
An externally supplied A5-permutation-lift attempt (24-vertex base → 120
vertices, reactively patching one bad cycle at a time) was rejected for
containing a C8, then automated and extended with an independent Python
reimplementation of the solver's tree/cotree bookkeeping (verified
byte-for-byte against the compiled solver). Across all four 24-vertex
bases, both random-restart search and exhaustive 3-variable repair hit a
wall (`base0`: 26 cuts; `base2` and `base3` independently converged to the
*same* 9-cut wall; `base1` could not clear even the starting constraint).
**Convergent negative evidence across four independent bases** that this
specific construction is exhausted — evidence, not a theorem.
See `tracks/external-audits/a5_lift_probe/AUDIT.md`.

---

# Part VI — Small-order exhaustive results

### P4 [THEOREM — three labels] 4-or-8 dichotomy through n = 19
**Every graph with δ≥3 on ≤19 vertices contains a C4 or a C8.** (Strictly
stronger than Erdős–Gyárfás through `n=19`.) For `n ≤ 17`,
`ex(n;{C4,C8}) < ⌈3n/2⌉` (McKay), so a δ≥3 graph has too many edges to be
`{C4,C8}`-free; for `n=18,19` equality holds and every extremal
`{C4,C8}`-free graph has min-degree 2 (checked over all 570 + 304).
- [PROVED FROM PUBLIC EXTREMAL DATA] the `ex(n)` values are McKay's.
- [COMPUTATIONALLY VERIFIED] min-degree computed for every extremal graph
  `n=16..19`; `n=18` independently re-derived by exhaustive geng (2,761
  cubic C4-free graphs, 0 C8-free, DFS/nx agree).
- [NOVELTY UNCHECKED] — may be implicit in the extremal tables. See L15.
- **[EXTERNAL_DATA_MISSING]** six of the eight McKay `.s6` inputs are
  absent locally; only the order-18 and order-19 files are restored with
  authoritative checksums (`manifests/external_s6_manifest.json`). Treat the
  `n=20..23` extremal-layer degree check as not locally reproducible until
  those artifacts return.

### P17 [COMPUTATIONALLY VERIFIED, certified] The n = 20 and n = 22 cubic layers
The remaining `n ≤ 23` search is the one-below near-cubic layer, four cases.
Two are now closed, with full certification manifests in `logs/p1_n20_23/`:

| case | command | raw = checked | c4_seen | C8-free survivors | exits | reconcile |
|---|---|---:|---:|---:|---|---|
| `n=20, m=30`, cubic | `geng -c -f -d3 -D3 20 30:30 0/1` | 36,101 | 0 | **0** | 0/0 | OK |
| `n=22, m=33`, cubic | `geng -c -f -d3 -D3 22 33:33 0/1` | 553,227 | 0 | **0** | 0/0 | OK |

Both manifests carry the exact command, nauty version string, checker source
SHA-256, stream SHA-256 and both pipe exit codes. The C checkers were
rebuilt and cross-validated against `cycle_detect.py` on n=10/n=12 C4-free
streams (0 disagreements) *before* being trusted.

**[INCOMPLETE_RANGE]** `n=21, m=32` (`4,3²⁰`) and `n=23, m=35` (`4,3²²`)
were started and **not** completed — their log directories contain no
`.json` manifest and no completion record. The `n=19` `pipeconf` run
likewise recorded `geng_exit=143` (SIGTERM) and `reconcile=FAIL`; it is
**not** a certified completion.

A single C8-free δ≥3 survivor at `n ≤ 23` would DISPROVE the stronger
4-or-8 theorem (but not Erdős–Gyárfás, since C16 remains available below
`n=32`).

---

# Part VII — The order-30 cubic program

### O30-1 [PROVED] Exact quotient characterization
*Let `G` be a bridgeless cubic C4-free graph on 30 vertices with exactly
`t` triangles. Contracting all `t` triangles gives a simple, 2-connected
(not merely 3-connected) cubic quotient `Q` on `30−2t` vertices, and `G` is
uniquely recovered from `Q` plus the `t` contracted vertices.* Closes the
case that a 3-connected-only census would have missed.

### O30-2 [COMPUTATIONALLY VERIFIED, EXHAUSTIVE] The triangle-quotient census
Together with the `≥t` corollary (each closure is a standalone consequence
of its own order's census):

| triangles `t` | quotient order | quotients | markings / quotient | total instances | survivors |
|--:|--:|--:|--:|--:|--:|
| 7 | 16 | 3,874 | 11,440 | 44,318,560 | **0** |
| 6 | 18 | 39,866 | 18,564 | 740,072,424 | **0** |
| 5 | 20 | 497,818 | 15,504 | 7,718,170,272 | **0** |
| 4 | 22 | 7,187,627 | 7,315 | 52,577,491,505 | **0** |

> **Theorem [COMPUTATIONALLY VERIFIED].** *A 30-vertex cubic
> Erdős–Gyárfás counterexample, if one exists, has at most **three**
> pairwise vertex-disjoint triangles.*

The `t=4` closure used an externally supplied specialized filter that was
**audited before use, not on trust**: its `allowed_bits` table was checked
by hand against the independently derived exact-interval theorem, and its
aggregate output on a 500-quotient sample was cross-validated field-by-field
against an independently written Python census on the same real data; the
claimed ~340× speedup was reproduced on local hardware. The complete
7,187,627-graph order-22 biconnected catalog was generated locally
(`nauty-geng -c -C -d3 -D3 22`, SHA-256 verified) and checked exhaustively
in 4m30s with `complete: true`, zero literal/theorem mismatches.
Artifacts: `tracks/order30-census/t4_intersection_filter/`,
`order30_quotient_census.md`.

**[OPEN]** `t = 0, 1, 2, 3`. An external claim of closing `t=3` by a
different method was recorded as **UNVERIFIED** (prose and a boxed
conclusion only, no code, logs or data) and is not used.

### O30-3 [PROVED] Girth-based reductions at order 30
- **Girth-7 branch: closed** (exact, verified, independently converged
  with a second external derivation after correcting it).
- **Girth-6, case `(s=0, a=0)`: exhaustively closed.** All 17 hub
  topologies × 1,294,670 compositions checked completely (not sampled),
  13,074 passing the internal-cycle pre-filter, **zero feasible labelings**.
  A first run reported `feasible=1` on topology #12; it was **stopped and
  investigated instead of reported**, and traced to a real bug — two
  parallel abstract edges both assigned length 0 collapsed in a Python
  `set`, leaving two hubs at degree 2. Fixed with an explicit post-build
  degree validator applied before any cycle or labeling check.
  **9 of the 10 `(s,a)` classes remain open** (any with antipodal chords or
  doubled-attachment vertices); the skeleton builder needs degree-1 (leaf)
  support, not yet implemented.
- **The (6,7)-kernel theorem [PROVED, hand-derived].** For `G` cubic,
  `n=30`, girth 6, containing a C7, with no C8 and no C16: L1 (C is
  chordless), L2 (the seven `wᵢ` are distinct, so `|R|=16`), L3 (W-edges
  only at distance 3, forming a single 7-cycle `H₃`), L4 (`S` is a matching
  in `H₃`, so `|S| ≤ 3`), L5 (doubled R-attachments only at distance 2),
  L6. Counting theorem:
  ```
  deg_R = 1^a 2^(14−2|S|−2a) 3^(a+2+2|S|),  |V(R)| = 16,  |E(R)| = 17+|S|,
  with |S| ≤ 3 and a ≤ 7−|S|.
  ```
  **Internal consistency check:** re-running L1–L6 under girth 7 forces
  `S = ∅` and `a = 0`, giving `|V(R)|=16`, `|E(R)|=17`, `deg_R = 2¹⁴3²` —
  **exactly the girth-7 kernel this project established earlier, re-derived
  from a different anchor.** The new framework strictly contains the old
  theorem as its degenerate case.
  **Honest scope:** bounds `(6,7)` to at most 4 parameter classes with a
  fully pinned 16-vertex kernel each. It does **not** close `(6,7)`. The
  remaining step — no admissible `(S,a,kernel)` avoids a C16 — has no hand
  argument; **L5's `d=3` case dies specifically on the no-C8 hypothesis,
  not on girth**, which is the unique load-bearing power-of-two constraint
  in the whole reduction and therefore the pressure point any completion
  must exploit.

### O30-4 [PROVED] Two global theorems orthogonal to the girth split
- **Theorem A (chord-span).** Let `G` be cubic on 30 vertices, Hamiltonian
  with Hamilton cycle `v₀…v₂₉`; the other 15 edges form a perfect matching
  of chords. A chord `{vᵢ,v_j}` with `d=|i−j|`, span `a=min(d,30−d)` splits
  `H` into cycles of lengths `d+1` and `31−d`, so avoiding `{4,8,16}` forces
  `d ∉ {3,7,15,23,27}`: **every chord has span in
  `{2,4,5,6,8,9,10,11,12,13,14}`**; no chord is antipodal. In the bipartite
  case every span is odd, intersecting to **span ∈ {5,9,11,13}** — fifteen
  chords, four permitted spans. Pair constraints reduce the case to a finite
  matching-design problem on `Z₃₀`. **Limitation:** needs Hamiltonicity;
  non-Hamiltonian cubic graphs on 30 vertices exist. The ear-decomposition
  generalization survives without Hamiltonicity but loses the matching
  structure.
- **Theorem B (3-edge-cut reduction).** If an order-30 cubic counterexample
  has a nontrivial 3-edge-cut splitting it into `G₁,G₂`, contract `G₂` to a
  vertex `z`: `G₁'` is cubic on fewer than 30 vertices, so by
  Royle–Markström it has a power-of-two cycle, which must pass through `z`;
  symmetrically for `G₂'`. Cycles through `z` use exactly 2 of the 3 cut
  edges, so **both contracted sides must thread their entire power-of-two
  cycle spectrum through a single degree-3 vertex simultaneously.**
  **Unlike the generic minimal-counterexample version this is not
  conditional on minimality** — the verified base case does the work. This
  is the clean route to assuming cyclic 4-edge-connectivity at `n=30`.

### O30-5 [DIAGNOSIS, not a theorem] Why global machinery fails at δ=3
Bondy–Vince, Gao–Huo–Liu–Ma and Liu–Ma are all degree-driven; at δ=3 they
degenerate to "an even cycle exists". The structural reason is a **type
mismatch: that machinery produces ADDITIVE windows of cycle lengths, while
the target set `{4,8,16,…}` is MULTIPLICATIVE with doubling gaps.** At
`n=30` an additive guarantee would need width ≥8 to land on a power of two;
degree 3 buys width 2. **Actionable consequence:** no degree-based global
argument can close `n=30`; any proof must exploit the sporadic arithmetic
of `{4,8,16}` against `n=30` specifically. This is a diagnosis, not a
theorem, and it correctly predicts that the problem keeps devolving into
case analysis.

---

# Part VIII — DISPROVED, RETRACTED, and failed approaches (kept)

Preserved with the exact obstruction, per the project's ground rules.

- **[DISPROVED] The sharp additive-density formula.**
  "`α(H_N) = ⌊N/2⌋+1` exactly / extremal density exactly 1/2" is FALSE.
  Witness: `{1,2,4,5,8,9,10} ⊆ {1..10}` has size 7 > 6. It had been read
  off only from `N = 2ᵏ` samples. **The valid residue:** the C2 lower bound
  (the interval `{2^{k−1}+1,…,2^k}` is power-of-two-sum-free, so
  `α ≥ ⌊N/2⌋`) and the narrowed C3 (a single-scale distinct-length book
  cannot force a power-of-two two-path cycle).
- **[RETRACTED] "The naive theta approach is dead" / "only a multiscale
  additive route remains."** Not established. The theta/additive route
  stays live: equal-length pairs (self-sums `2ℓ`), multiplicities,
  parity/residue constraints, overlapping thetas, length differences and
  ≥3-path cycles are all untouched. **Modeling note:** path lengths form a
  *multiset*; the set model above ignores the `2ℓ` constraint.
- **[WARNING, rescoped — B2, not an obstruction]** *Unqualified* degree-2
  path suppression shifts cycle lengths (by `ℓ−1` for a length-`ℓ` path),
  so it does not preserve power-of-two-ness. This rules out the blind
  textbook minor reduction, **not** all reductions. Open target **B2⁺**:
  characterize which reduction collections preserve power-of-two-cycle
  existence.
- **[DISPROVED] The literal central target `n ≤ 2D+3`** (`D := 2n−2−m`).
  False for *every* δ≥3 graph, no cycle information needed: it is
  equivalent to `m ≤ (3n−1)/2`, contradicted unconditionally by the excess
  identity `Σ(deg−3) = 2m−3n ≥ 0`.
- **[DISPROVED] The vine charging lemma V1** ("#missing dyadic lengths
  ≤ D"). Witness: `n=13`, `D=0`, missing `= {4}`.
- **[OPEN — gap] `D ≥ 2` (⇔ `m ≤ 2n−4`)** is not implied by current
  lemmas; the natural witness route fails on 6.8–16.0% of C4-free δ≥3
  graphs, and the failure rate grows with `n`.
- **[DISPROVED] D1C**, the proposed nonedge-completion lemma — fails from
  `n=9`.
- **[DISPROVED] The one-cell reduction target** — see Part III.
- **[DISPROVED] FC-19/20/21** — false for forbidden `{4,8}`, with verified
  C4/C8-free `(2,2)`-terminal survivors.
- **[CLAIM_REFUTED] R2/S2** — see Part III.
- **[STRUCTURALLY SUPERSEDED] The alternating-ladder Type-T residual** —
  see Part III; the family is real, its Type-T premise is excluded.
- **[SUPERSEDED] All sampled Monte-Carlo Z5 numbers** — see Part V.
- **[RETRACTED] The inflated passage-conflict counts** 5,052/5,084/6,386 —
  see C16-5.
- **[METHOD LESSON, kept]** A pattern true on a special subsequence (here
  `N = 2ᵏ`) is NOT a theorem. This is the failure that produced the
  additive-density error, and it is the single most repeated failure mode
  in this project. See RETROSPECTIVE.md.

---

# Part IX — External / other-session claims audited and NOT established

Recorded so nobody re-imports them. All were treated as CONJECTURAL until
independently reproduced; none reproduced.

- **`q(G) ≥ 5` and `q(G) ≥ 6` — `NOT_ESTABLISHED`.** An externally pasted
  report claimed a "provisional `q(G) ≥ 6`" (17,010 one-hub `q=5`
  configurations, 146 two-hub core classes, 17,969 three-hub cores).
  Audited against every local and remote ref's full history: **zero
  matching artifacts** — no case-analysis file, no verifier, no manifest,
  no data, no commit. Every `q=4` mention in the repository is an explicit
  statement that it was **not** attempted. **Do not cite.**
  (`defect_q_ge6_audit.md`.)
- **The "linear defect growth" theorem `n ≤ 15q−17` — PARTIAL AUDIT, core
  lemma NOT verified.** Cites a branch `codex/dyadic-passage-leap` that
  exists in no local or remote ref. Its §§1–2 exactly reconstruct this
  repository's own already-audited `h ≤ q` result; the genuinely new core
  lemma is unverified. (`linear_defect_growth_audit.md`.)
- **The cubic order-32 "factor census" + "Mersenne closure witness" and the
  cubic order-34 factor census — PARTIAL AUDIT.** Cite commits absent from
  every ref. The partition/orbit counts are exact (a strong positive
  signal), but the "new" structural theorem is **not new**.
  (`cubic32_mersenne_audit.md`, `cubic34_factor_census_audit.md`.)
- **An "order-38 cubic census" (minimal counterexample ≥40) — originally
  presented with broken references, an unverifiable checksum and citations
  to a "Wormald–Kingan" theorem with zero backing files.** When real
  transcribed source later arrived (from an inaccessible third sandbox,
  hardcoded `/mnt/data/...` paths) it was audited rather than accepted: the
  three hand-proof notes are logically sound **conditional on uncited
  external theorems**; the shared cycle-detection primitive cross-validates
  against `cycle_detect.py` with 0 disagreements; **2 of 151** claimed
  partition classes were reproduced completely from scratch and agree (0
  leaves). The other 149 classes and the aggregate 60.9M-node total remain
  **unverified** — the result/manifest data files were never supplied.
  (`tracks/external-audits/order38_bundle/AUDIT.md`.)
- **The Bass–Ihara high-girth theorem — VERIFIED in substance, but its
  advertised consequence is VACUOUS at `n=30`.** The closed form was
  re-derived from scratch via Ihara (independently confirming that for
  girth > r every closed non-backtracking walk of length `2r` traces a
  simple `2r`-cycle, since every non-simple topology has minimum length
  `2g ≥ 2r+2`). But its hypothesis is girth ≥ 9 and **the (3,9)-cage has 58
  vertices**, so no cubic 30-vertex graph satisfies it. Genuine value is
  confined to `58 ≤ n ≤ 131`.
- **The contraction theorem's application at order 30 — DOES NOT FOLLOW.**
  The theorem itself is correct (verified step by step), but it requires
  `G` **globally** minimal among all δ≥3 graphs, because the quotient has a
  degree-4 vertex and so only the general `≥17` bound applies to it — not
  the cubic `≥30` bound. An order-30 cubic counterexample is not known to
  be globally minimal. A later correction fixed a *different* problem
  (universal vs. existential quantifier) and left this objection untouched.
- **The length-16 tangle theorem — first fully substantiated external
  submission; combinatorial core VERIFIED, spectral bound NOT.** All six
  supplied artifacts matched their SHA-256 manifest. The **17-template
  classification reproduced bit-for-bit**, including certificate SHA-256
  `ec060f67e159ed3ab52e7057eec6bb9fd2d49b102028886b36812aab6afe2743`,
  `branch_distribution {2:10, 4:7}` and
  `vertex_distribution {10:2,11:3,12:6,13:3,14:3}`; the 10 two-branch
  templates and all 17 support orders were **re-derived independently by
  hand**, entry for entry, and Lemmas 1 and 2 re-derived.
  **But `N₁₆ ≥ 53568` itself is `NOT VERIFIED` and is the load-bearing
  gap:** the reduction script merely *asserts* the formula
  `lower = (2^r+1+c)² − (c²−2c+2^{r+1}−1)·n` with `c=(n+2^r+1)/(n−1)` and
  checks that it evaluates to `1553220/29`; the derivation lives in a
  "companion spectral note" that **was not supplied**. An independent
  cruder Ihara bound gives ≈50,719, which would change every headline
  number. Everything *downstream* of `N₁₆ ≥ 53568` is verified; the bound
  itself is not. The proof target's margin is **6 incidences out of 6,696
  (0.09%)**, with the required uniform cap sitting below the true mean —
  `STRUCTURALLY FRAGILE`.

---

# Conjectural / directional (NOT proved)

- Whether δ≥3 forces a `u`–`v` path system spanning ≥2 dyadic scales
  (would revive an additive route). Open.
- Whether the P₁₃-free search (L7) extends or yields an extractable human
  lemma. Open.
- **T7** remains gated on finding at least one internally clean bridge.
- **O4** (two disjoint root-neighbour paths in `H−r`). Open.
- **CB2**, the one-excursion target. Neither proved nor disproved.
- **VI.5**, theta saturation. Open.
- The crossing case of the intersection-diagram classification. Open.
- Whether the assembled four-layer passage CNF for `(4,55,7)` is SAT or
  UNSAT. Entirely unknown.

# Where to look next

See `plan.md`'s priority list. The short version: the joint two-central-
bridge Type-T interaction (never attempted, repeatedly identified as the
highest-value target), the `m=5` C16 rerun and CNF assembly, the two
unfinished `n=21/23` near-cubic layers, the order-30 `t ≤ 3` census, the
`(6,7)`-kernel's C16 constraint, and an independent derivation of — or a
refutation of — the `N₁₆ ≥ 53568` spectral bound.
