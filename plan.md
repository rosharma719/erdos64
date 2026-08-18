# plan.md — Erdős–Gyárfás (Erdős #64): consolidated strategy and status ledger

**Goal.** Genuinely attempt to resolve: δ(G) ≥ 3 ⇒ `G` has a cycle of length
a power of two. Pursue proof AND counterexample. Never overclaim.
**Status 2026-08: OPEN.**

**This file is the single durable status ledger for the project.** It was
reconstructed on 2026-08-18 by merging the status logs of seven divergent
research branches. Going forward there is exactly one of it — see
RETROSPECTIVE.md, rule (4).

## Ground rules (unchanged, verbatim)
- Every assertion labeled PROVED / COMPUTATIONALLY VERIFIED / CONJECTURAL /
  DISPROVED / KNOWN FROM LITERATURE.
- No experimental pattern promoted to theorem without: precise statement →
  broad independent test → smallest-counterexample search → proof.
- Failed approaches preserved with the exact obstruction that killed them.

Additional rules adopted from what actually worked (RETROSPECTIVE.md):
- Any COMPUTATIONALLY VERIFIED claim needs **two independent
  implementations**, ideally structurally different, not two runs of one.
- Any claim originating **outside the current session** — another branch,
  another sandbox, a pasted report — is CONJECTURAL until independently
  reproduced here, with artifacts. No exceptions.
- The status log below is updated **in the same session** as any dated
  result file. A result that exists only in a dated `.md` and not here is
  a process failure, not a record.

## Toolkit (verified working)
- Python 3.14 venv: networkx 3.6.1, numpy 2.5.1, OR-Tools CP-SAT, PySAT.
- nauty `geng` 2.9.3 (`-d3` min degree, `-D3` cubic, `-f` C4-free,
  `-c -C` connected/biconnected, `res/mod` sharding).
- `verifier/cycle_detect.py` — exhaustive exact power-of-two cycle
  detector, cross-validated (2,107 checks, 2 independent implementations,
  0 disagreements). The trusted oracle under every computational claim.
- `verifier/check_g6.c`, `verifier/check_c8.c`,
  `verifier/check_power_masks.c` — independent C checkers for graph6
  streams (built into `.build/` by `make`).
- `verifier/certify_shard.sh` — one certified geng shard, emitting a JSON
  manifest with command, nauty version, checker source SHA-256, raw and
  checked counts, both pipe exit codes and the stream SHA-256.
- ~250 further task-specific verifiers under `verifier/`, ~40 pytest
  regression tests under `tests/`, and frozen certificates under
  `manifests/` and `data/`.

## Certification gate (applies to every expensive run)
Record nauty version, exact command, raw + per-filter counts, per-process
exit codes, stream checksums, proof the full stream was consumed, and a
small-order cross-check against known counts; shard large searches by
`res/mod` with a manifest requiring all indices. For solver UNSAT, produce
an LRAT/DRAT (or PB) *checkable* certificate — a bare "UNSAT" line is not
accepted. CP-SAT is for discovery only unless reduced to certified CNF.
**A run that exits non-zero, or whose raw and checked counts fail to
reconcile, is not a result** (see the `n=19 pipeconf` entry: `geng_exit=143`,
`reconcile=FAIL`).

---

# The five active tracks

1. **Track A — small-order exhaustive search.** `n ≤ 11` closed; the 4-or-8
   dichotomy proved through `n=19`; the `n≤23` near-cubic layer half done
   (`n=20,22` closed, `n=21,23` unfinished).
2. **Track B — separator / connectivity.** S4, S5, the one-pole theory
   O1–O7, the 2-cut Type A/B/C trichotomy, the F/FC series, and hence
   3-connectivity at every even order in `[17,33]` plus cubic
   3-edge-connectivity there.
3. **Track C — contraction / Type-N / Type-T.** The near-power edge and
   atom-lifting lemmas, the Type N/T dichotomy, the central-bridge
   trichotomy, the pole-forcing theorem (T3 eliminated, T2 narrowed).
4. **Track D — Type-T C16 port completion.** The support-bound theorem, the
   unconditional bare-core dyadic-avoidance proof, the passage-lifting
   soundness theorem, and the passage-level conflict catalogs.
5. **Track E — order-30 cubic census.** The triangle-quotient census
   (`t ≥ 4` closed), the girth-7 closure, the girth-6 `(s=0,a=0)` closure,
   the `(6,7)`-kernel theorem, and the two global theorems (chord-span,
   3-edge-cut reduction).

**Deprioritized, with the reason.** Unrestricted brute enumeration beyond
`n=11` (redundant — the extremal route is stronger and cheaper); the P₁₃
induced-path frontier (heavy compute, no extractable lemma yet);
cycle-space / F₂-dimension arguments (too weak, kept only for honesty);
Cayley-graph constructions (no near-miss has ever surfaced from them).
**Degree-driven global cycle-length theorems are formally deprioritized**
by the Track-E diagnosis: they produce *additive* length windows while the
target `{4,8,16,…}` is *multiplicative*, so at δ=3 they are near-vacuous.

---

# Priority list (as of 2026-08-18)

Ranked by (probability of genuinely new progress) × verifiability. The
status annotations matter: two items that earlier handoffs listed as top
priorities have since been overtaken by later results on other branches,
and are recorded here at their true current state rather than carried
forward stale.

### 1. Joint two-central-bridge Type-T interaction — **NOT ATTEMPTED, highest value**
`contraction_ma2_integration.md` Part X and
`contraction_separator_integration.md` Part IX both identify this as the
single highest-value remaining target across the entire six-file
contraction sequence, with the full MA2 machinery, the five-lemma
arithmetic toolkit and S5's uniqueness already available to attack it. It
requires combining the non-clean intersection machinery with two
independently chosen central bridges at a shared Type-T triangle. Only
question 5 (can both bridges name the same S5 cut vertex) has a free
partial answer. **Deferred repeatedly under time pressure; nothing blocks
it technically.**

### 2. The single Type-T yes/no question (shared internal vertex) — **CLOSED, do not re-open**
Earlier handoffs list "can `Θ_x`'s and `Θ_y`'s `P₁` branches share an
internal vertex?" as the top open item, the last unresolved question in the
whole Type-T case space. **That reduction is correct but its host row is
dead.** The question lives inside the identical-terminal row
`X_x = y, X_y = x`, and the pole-forcing theorem
(`central_bridge_triangle_pole_forcing.md`) proves the aligned pole of a
cubic Type-T vertex can never be cubic — excluding that row twice over
(`type_t_ladder_saturation.md` Theorem 1.1). T3 is eliminated outright and
T2 is narrowed to `X_x = X_y = z₀`. **Action: none. Recorded so it is not
re-attempted.** The genuine Type-T residuals are item 1 above plus the
exact-two-attachment anchored A family with unspecified larger admissible
pairs, multi-attachment A, P, single/mixed/double S, and
deletion-relative component sharing (`type_t_recovery_audit.md`).

### 3. C16 gadget completion: the `m=5` rerun and CNF assembly — mechanical, then unknown
`m=2/3/4` are complete **outright** for `(4,55,7)`; `m=5` is complete only
`COMPLETE_RELATIVE_TO` the pre-`m=4` shadow. The remaining static step is
exactly one rerun of `m=5` against the new `m=4` shadow — no new theory,
~200–260 s to regenerate the shadow plus ~900 CPU-seconds, expected to drop
≈4.8% of the 2,944,894 supports. **Then** assemble the full passage CNF
from the four layers and test the fixed completion instance. Neither step
has been started and the assembled formula's satisfiability is entirely
unknown — *a complete conflict catalog is not evidence either way about
UNSAT*. The other instances `(4,2,2)` and `(4,28,4)` lag behind `(4,55,7)`;
`tracks/type-t-c16-static-sat/`'s gadget-level `(4,28,4)` catalog is
`BOUNDED_INCOMPLETE` (still SAT).

### 4. `n=21` and `n=23` near-cubic P1 layers — unfinished, cheap, certified path exists
The last two of the four one-below near-cubic cases:
`n=21, m=32` (degree sequence `4,3²⁰`) and `n=23, m=35` (`4,3²²`), both via
`geng -c -f -d3 -D4 N M:M res/mod` + `check_c8`, the identical pipeline that
certified `n=20` (36,101 graphs) and `n=22` (553,227 graphs) with 0
survivors. Their log directories contain no completion manifest. A single
C8-free survivor would DISPROVE the stronger 4-or-8 theorem (not
Erdős–Gyárfás, since C16 remains available below `n=32`).
**Prerequisite:** restore the six missing McKay `.s6` files
(`manifests/external_s6_manifest.json`) so the extremal-layer step is
locally reproducible again instead of `EXTERNAL_DATA_MISSING`.

### 5. Order-30 triangle-quotient census, `t = 0,1,2,3`
`t ≥ 4` is exhaustively closed (7,718,170,272 + 740,072,424 + 44,318,560 +
52,577,491,505 instances, zero survivors), giving "at most three
triangles". `t=3` needs the order-24 cubic quotient catalog; a generic
version of the audited `t=4` filter was mentioned externally but never
supplied, so it needs the same treatment the `t=4` filter got: hand-check
its `allowed_bits` table against the exact-interval theorem, then
cross-validate its aggregate output field-by-field against an
independently written census on real sample data, **before** spending
compute. `t = 0,1,2` follow at orders 30/28/26 and are much larger.

### 6. The `(6,7)`-kernel's C16 constraint
The `(6,7)` girth pair is bounded to at most 4 parameter classes
(`|S| ∈ {0,1,2,3}`) with a fully pinned 16-vertex kernel each
(`|V(R)|=16`, `|E(R)|=17+|S|`, `deg_R = 1^a 2^{14−2|S|−2a} 3^{a+2+2|S|}`).
The remaining step — that no admissible `(S,a,kernel)` avoids a C16 — has
no hand argument, because the C16 constraint is global in a way L1–L6 are
not. **The identified pressure point: L5's `d=3` case dies on the no-C8
hypothesis, not on girth** — the unique place in the whole reduction where
a power-of-two constraint rather than girth is load-bearing. Also open:
9 of the 10 girth-6 `(s,a)` classes, which need the skeleton builder
extended to degree-1 (leaf) positions.

### 7. Verify or refute the spectral bound `N₁₆ ≥ 53568`
Everything downstream of it in the length-16 tangle theorem is verified —
the 17-template classification bit-for-bit and by independent hand
re-derivation, Lemmas 1 and 2, and the whole 3348 → 6696 → cap-223
arithmetic. The bound itself is only *asserted* by the supplied script,
with its derivation in a companion spectral note that was never supplied.
An independent cruder Ihara bound gives ≈50,719, which changes every
headline number. The proof target's margin is **6 incidences in 6,696
(0.09%)**, with the required uniform cap below the true mean, so this is
`STRUCTURALLY FRAGILE` even if the bound holds. **Either derive it
independently or refute it; do not build on it meanwhile.**

### Standing background items
- **B2⁺** — characterize which reduction collections preserve
  power-of-two-cycle existence. The negative half (unqualified degree-2
  suppression is unsafe) is settled; the positive lemma is not.
- **Track C additive theory** — establish the actual extremal behaviour for
  both the SET (distinct sums) and MULTISET (equal-length `2ℓ`) models, and
  only then ask whether δ≥3 forces such a configuration. Do **not** infer
  graph consequences until the additive hypothesis is shown to arise.
- **`q(G) ≥ 5`** — the `q=4` case table (10 rows) and the extended colored
  path bounds `t(4)=12`, `t(5)=18` are derived and ready as *inputs*.
  Heuristic scaling says `q=4`'s worst row needs ~7–8 orders of magnitude
  more Stage-6 reconstruction than `q=3` did, so this needs a genuinely
  better method, not more compute.
- **Extending FC past FC-18** — the only lever that moves the 2-cut floor
  (Type C is binding at 36; Type A and B now have slack to 56 and 38).
- **Resolving the `[17,33]` vs `[17,35]` inconsistency** in the even-order
  3-connectivity corollary (see proof.md P14): the post-F19 floor
  `min(56,38,36)=36` appears to give `[17,35]` for free, but the file
  asserting the new floor also asserts the range is unaffected, on an
  incorrect ground. Re-derive from scratch before using either.

---

# Status log (newest first)

**2026-08-18 — CONSOLIDATION.** Seven branches merged into
`consolidated/canonical` off `main`.
- **Branch topology established by `git merge-base`, not assumed.** Five of
  the seven are a *linear chain*: `erdos-gyarfas-handoff-l6tqlo` →
  `erdos-gyarfas-type-t-analysis-a9u4sx` → `type-t-c16-compilation-x9ts7a`
  → `codex/type-t-c16-continuation` → `claude/graph-counterexample-q6-xerdjz`,
  and that last branch had already merged `codex/type-t-overlap-reduction`
  at `c99ba8f`. Only **two** commits of content sat outside the chain
  (`codex/type-t-overlap-reduction`'s tip `f7966c1`, and the whole of
  `claude/erdos-gyarfas-conjecture-oegjjg`, which forked from `main`).
  The widely-repeated description of branches 5/6/7 as three uncoordinated
  parallel efforts is **wrong as stated**: 6 = 5 + one commit, and 7's line
  was merged into the chain. The genuine duplication was narrower and is
  reconciled here in favour of the passage-level representation.
- Docs rewritten: `proof.md`, `plan.md`, `lemmas.md`, `literature.md`,
  `README.md`; `manuscript.md` carried forward with its frozen sections and
  access caveat intact; `RETROSPECTIVE.md` added.
- Two stale top-priority items corrected: the "single Type-T yes/no
  question" (closed by pole forcing) and "C16 `m=4` is the sole missing
  layer" (`m=4` was closed 2026-07-30; only the `m=5` rerun remains).
- `logs/certify/` restored (the chain tip had dropped it); branch-1 audit
  material relocated under `tracks/`; repo hygiene (no `.pyc`, no
  `__pycache__`, no committed binaries) applied uniformly.

**2026-08-07 — length-16 tangle theorem audited (first fully substantiated
external submission).** All six supplied artifacts matched their SHA-256
manifest. The 17-template classification reproduced **bit-for-bit**
(certificate `ec060f67…`, `branch_distribution {2:10,4:7}`,
`vertex_distribution {10:2,11:3,12:6,13:3,14:3}`), and the 10 two-branch
templates plus all 17 support orders were re-derived **independently by
hand**. Lemmas 1 and 2 re-derived. An earlier own flag (that theta
configurations were omitted) was checked and **withdrawn** — 8 of the 10
two-branch templates *are* theta cores. **The load-bearing gap: `N₁₆ ≥
53568` is NOT verified** — the script asserts the formula and only checks
its arithmetic; the derivation was never supplied. Margin 0.09%.

**2026-08-06 — global methods: a diagnosis and two hand-derived theorems.**
The additive-vs-multiplicative type-mismatch diagnosis (no degree-based
global argument can close `n=30`); **Theorem A** (chord-span: every chord
of a Hamiltonian order-30 cubic counterexample has span in
`{2,4,5,6,8,9,10,11,12,13,14}`, and in `{5,9,11,13}` in the bipartite case,
reducing to a finite matching-design problem on `Z₃₀`); **Theorem B**
(3-edge-cut reduction, *not* conditional on minimality — the verified
Royle–Markström base case does the work). Also: the **(6,7)-kernel
theorem**, derived by hand from a C7 anchor, whose girth-7 degeneration
re-derives the project's earlier girth-7 kernel exactly from a different
anchor. Also audited: the Bass–Ihara high-girth theorem (**verified in
substance, vacuous at `n=30`** — the (3,9)-cage has 58 vertices) and the
contraction theorem's order-30 application (**does not follow** — needs
global minimality among all δ≥3 graphs, unavailable at order 30).

**2026-08-05 — girth-6 case `(s=0,a=0)` exhaustively closed, after catching
a real bug.** Converted a sampled sweep into true exhaustive enumeration;
the first run reported `feasible=1` on topology #12 and **was stopped and
investigated rather than reported**. Root cause: two parallel abstract
edges both assigned length 0, silently collapsed by a Python `set`, leaving
two hubs at degree 2 — an invalid non-cubic graph, not a counterexample.
Fixed with an explicit post-build degree validator. Rerun: 1,294,670
compositions across all 17 topologies, 13,074 passing the pre-filter, **0
feasible labelings**. 9 of 10 `(s,a)` classes remain. Also this week:
girth-7 branch closed and independently re-confirmed; named algebraic
families and LCF-notation constructions swept with no order-30
counterexample; an external order-32 direct-search claim independently
re-run (best local search reaches `C16=236`).

**2026-08-04 — order-30 `t=4` closed.** No order-30 cubic counterexample
has exactly four disjoint triangles. The externally supplied specialized
filter was **audited before use** (hand-checked `allowed_bits` table;
field-by-field cross-validation against an independently written census on
500 real quotients; the ~340× speedup reproduced locally), then run over
the complete locally generated 7,187,627-graph order-22 biconnected catalog
(SHA-256 verified): **52,577,491,505 markings in 4m30s, zero survivors,
`complete: true`.** Combined with `t=7/6/5`, the standing bound moves from
"at most four triangles" to **"at most three"**. A separate external `t=3`
claim was logged **UNVERIFIED** (prose only, no code/data) and not used.

**2026-08-02 — `n=20` and `n=22` cubic P1 cases closed; order-38 external
bundle audited; branch landscape discovered.** Toolchain rebuilt on Linux
and the C checkers cross-validated against `cycle_detect.py` before being
trusted; certified runs gave 36,101 and 553,227 graphs with **0 C8-free
survivors** each, manifests in `logs/p1_n20_23/`. `n=21`/`n=23` started, not
finished. Platform-specific `check_c8`/`check_g6` binaries and two stray
`.pyc` files untracked. A previously presented "order-38 cubic census" with
no basis in git history was flagged as unsubstantiated; when real source
later arrived from a third sandbox it was audited rather than accepted —
the hand proofs are sound *conditional on uncited theorems*, 2 of 151
partition classes reproduced from scratch and agree, the other 149 and the
60.9M-node aggregate remain unverified. **Also: 14 further never-merged
branches discovered**, with root-level filename collisions making naive
merging unsafe; snapshots indexed rather than merged at the time.
- **A5 5-sheet lift: converges to a negative result.** All four 24-vertex
  bases hit a wall (`base0` 26 cuts; `base2`/`base3` independently
  converging to the *same* 9-cut wall; `base1` never clearing the starting
  constraint) under both random-restart and exhaustive 3-variable repair.

**2026-08-02 — two free lemmas.** F19 strengthens Type A to `n ≥ 56` and
Type B to `n ≥ 38` (Type C's 36 remains binding); cubic 3-edge-connectivity
at every even order in `[17,33]` follows from Whitney's inequality plus the
already-proved vertex 3-connectivity — closing a gap the project's own
gap-analysis table had flagged as untouched.

**2026-08-01 — 3-connectivity generalized, and three external claims
audited.** The order-32 3-connectivity target completed (Type C closed via
monotonicity on F19/FC-18), then generalized: **every even-order minimal
counterexample with `17 ≤ n ≤ 33` is 3-connected**, obtained for free by
noticing the per-bridge bounds never used `n=32`. FC-N SAT extension
merged: FC-18 true, **FC-19/20/21 FALSE** (verified C4/C8-free `(2,2)`
survivors), F19 true. Type B closed at `n=32` via the `(1,1)/(2,2)`
decomposition. Audits: the cubic order-32 "Mersenne" census (its "new"
theorem is not new), the order-34 factor census, the "linear defect growth"
theorem `n ≤ 15q−17` (its §§1–2 merely reconstruct this repo's own `h ≤ q`;
the new core lemma unverified), and the rooted order-20 theorem
(corroborated). The "every edge has a `2ᵏ+1` witness" claim was audited
down to **nontriangle edges only**.

**2026-07-30 — the order-30 census, the F-series, and the C16 `m=4`
layer.** Order-16/18/20 quotient families closed (44,318,560 / 740,072,424
/ 7,718,170,272 markings, zero survivors), with the `≥t` corollary
formalized so each closure stands alone. **F12** proved (Type A eliminated
at `n=32`); **FC-15** proved. **C16 `m=4` closed for `(4,55,7)`:
3,971,519 verified minimal supports, 87/87 canonical starts, 0 verification
rejections** — so `m=4` was *not* the missing layer after this date; only
the `m=5` rerun is, and its subsumption was measured at ≈4.8%.
**The externally claimed "provisional `q(G) ≥ 6`" was audited and found
unfounded** — zero matching artifacts in any local or remote ref. `q=4`/`q=5`
case tables and path bounds were derived as *prerequisites only*.

**2026-07-29 — Type-T C16 static compilation and the passage-level pivot.**
The support-bound theorem proved (`L ≥ 2m+r`, `m ≤ ⌊L/3⌋`, `m ≥ 2`: C4
conflicts impossible, C8 exactly `m=2`, C16 `m ∈ {2,3,4,5}`), making
`Φ_{4,8}` exactly complete with no CEGAR loop. Gadget-level catalogs
compiled, then projected to **passage-level** variables (128.9× and 206.7×
compression), with the passage-support soundness (lifting) theorem proved.
`m=2`, `m=3` and the specialized `m=5` layer certified.
**A real soundness bug was caught only by disagreement between two
structurally different implementations** (5,007 vs 5,052 verified minimal
C8 supports): `verify_passage_conflicts` over-materialized the supplying
gadget and accepted supports via unclaimed edges. Fixed; both
implementations now agree exactly at 5,007/5,044/6,359; the earlier
5,052/5,084/6,386 are retracted. Separately, the **bare-core dyadic
avoidance proof** was completed unconditionally for all `j ≥ 4` via a
2-adic argument on 35 affine length-forms, with completeness closed by an
independent kernel/cycle-space derivation.

**2026-07-28 — Type-T overlap reduction, then self-correction.**
Theorem 2.1 proved: the exact arithmetic classification of divergent-cell
decompositions (`k=1` + dyadic `T` FORCED; `k=1` + non-dyadic and `k≥2`
with `T=3k` UNIVERSALLY SAFE; `T=3k+1` forced; `T ≥ 3k+2` escapable but not
universal). An explicit infinite **alternating ladder** family was built,
showing no finite core list bounds the incidence structure in general —
and then **self-corrected**: the ladder's premise (the identical-terminal
row `X_x=y, X_y=x`) was already excluded by an ancestor commit's
pole-forcing theorem, so it is a valid abstract object but **not** a live
Type-T residual. The identical-terminal residual's reduction to "one
yes/no question" is likewise correct but moot. The 87,167-row sweep remains
valid.

**2026-07-27/28 — pole forcing, Type-B realizability, and the R2/S2
refutation.** **Pole-forcing theorem:** the aligned pole of a cubic Type-T
vertex can never be cubic ⇒ **T3 eliminated outright, T2 narrowed to
`X_x = X_y = z₀`**. Type-B: B19, B20 and B20D2 proved, so all 16 frozen
tuples reach order ≥40 — with two independently coded generators agreeing
by matching SHA-256 and a third independent verifier eliminating every
candidate. The interrupted **R2/S2 claim was audited and refuted** (T2's
admissible pair need not include the shortest path), with explicit
Heawood/Balaban counterexamples; the earlier "only component sharing and
R2/S2 remain" summary was too narrow and is withdrawn.

**2026-07-26/27 — the defect ladder and the exact Z5 completion.**
`q(G) ≥ 2` → `q(G) ≥ 3` → **`q(G) ≥ 4`, `|E| ≤ 2|V|−6`**, via the derived
leaf graph, the leaf-count identity `c1 = c3 + 4h − 2q − 4`, the bounded
branching-kernel lemma and the colored degree-2 path lemma (`t ≤ 2,5,8`,
two independent implementations, 0 mismatches over 29,655 words). A real
arithmetic error (`t → 2t`) in the weighted-incidence formula was caught
and fixed mid-derivation. **Z5 completed exactly**: all 4,882,812,496
nonzero assignments over four certified bases, base 1 at exact 100%
coverage via its full 315-vector list (a 48-vector compression attempt
FAILED with 21,156 exceptions and is recorded as a failure), bases 0/2/3
with exactly 444/72/48 uncovered assignments, all 564 resolved, **zero
survivors**. All earlier sampled Z5 numbers superseded — the sampled
"≈0 coverage" claim for bases 0,1,3 was **wrong**.

**2026-07-25 — separators, one-pole theory, and two disproofs.**
**S4** (bridgelessness) and **S5** (cut-vertex classification) proved by the
doubling construction, superseding the stalled B2 suppression attempt.
One-pole theory O1–O3 (full 2-connectivity), **O5** (unconditional K4-minor
rigid core, two independent proofs, with two flawed hand-examples kept as
an error log), O4′ (via Gao–Huo–Liu–Ma), O4a, O6, O7, and the
suppressed-edge equivalence. **Disproved:** the literal `n ≤ 2D+3` central
target (unconditionally false for every δ≥3 graph) and the vine charging
lemma V1 (witness `n=13`, `D=0`, missing `{4}`). `D ≥ 2` recorded as an
**open gap**, with its natural witness route failing on 6.8–16.0% of
C4-free δ≥3 graphs.

**2026-07-24/25 — small-order results and the first correction pass.**
`n ≤ 11` closed exhaustively (577,076,528 graphs at `n=11`, 0
counterexamples). Minimal-counterexample structure B0/B1/B3/B4 + M1/M3/M4
re-derived from scratch, matching Carr 2026. **L15 added and verified:**
McKay's `ex(n;{C4,C8})` data gives the **4-or-8 dichotomy through `n=19`**,
strictly stronger than Erdős–Gyárfás in that range. The `n=12` brute-force
job was killed as strategically redundant and the `n=13..16` CP-SAT sweep
cancelled.
- **The additive-density formula was RETRACTED.** `α(H_N) = ⌊N/2⌋+1` /
  density exactly 1/2 is FALSE (witness `{1,2,4,5,8,9,10} ⊂ {1..10}`, size
  7 > 6); it had been induced from `N = 2ᵏ` samples only. The valid residue
  (the C2 lower bound and the narrowed C3) was kept; the overclaims
  ("naive theta is dead", "only multiscale remains") were withdrawn.
- **B2 rescoped** from "obstruction" to a warning plus the positive target
  B2⁺. **P2 relabelled** KNOWN FROM LITERATURE + INDEPENDENTLY RE-DERIVED —
  validation, not new progress.

---

# Completed / failed, kept with the exact obstruction

Full register in `proof.md` Part VIII. Summary of the ones that changed the
project's direction:

- **DISPROVED — the sharp additive-density formula.** A sampling artifact
  read off `N = 2ᵏ` only. **METHOD LESSON, kept:** a pattern true on a
  special subsequence is not a theorem; every computationally derived
  "PROVED" must survive a smallest-counterexample search over the general
  case before promotion. This exact anti-pattern — *inducting a general
  formula from a special or small sample* — is the project's most repeated
  failure mode and is now an explicit checklist item.
- **DISPROVED — `n ≤ 2D+3`** and **the vine lemma V1.** Both killed the
  ordering-defect program's original central target; the surviving
  `q(G) ≥ 4` ladder came from a different route entirely.
- **DISPROVED — the one-cell reduction target**, with the smallest exact
  obstruction recorded (0 shared edges, 0 common components, 2 divergent
  cells, both safe).
- **DISPROVED — FC-19/20/21** for forbidden `{4,8}`, with explicit
  survivors. This is what fixes Type C at 36 rather than higher.
- **CLAIM_REFUTED — R2/S2**, refuted by explicit Heawood/Balaban
  counterexamples rather than quietly dropped.
- **STRUCTURALLY SUPERSEDED — the alternating-ladder Type-T residual**, and
  with it the "single remaining Type-T yes/no question": correct
  mathematics, dead premise.
- **WARNING, not blocked — B2.** Unqualified degree-2 suppression shifts
  cycle lengths by `ℓ−1`. Blind textbook minor reduction is unsafe; not all
  reductions are.
- **NOT_ESTABLISHED — `q(G) ≥ 5`/`≥ 6`**, the "linear defect growth"
  theorem, the cubic order-32/34 factor censuses, and 149 of 151 order-38
  partition classes. All externally supplied, none reproducible here.
