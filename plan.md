# plan.md — Erdős–Gyárfás (Erdős #64) autonomous attack

**Goal.** Genuinely attempt to resolve: δ(G)≥3 ⇒ G has a cycle of length a power
of two. Pursue proof AND counterexample. Never overclaim. Status 2026-07: OPEN.

## Toolkit (verified working)
- Python 3.14 venv: networkx 3.6.1, numpy 2.5.1, OR-Tools CP-SAT, PySAT.
- nauty `geng` (canonical graph generation, incl. `-d3` min-degree, `-D3` cubic).
- `verifier/cycle_detect.py`: exhaustive exact power-of-two cycle detector,
  **cross-validated** (2107 checks, 2 independent impls, 0 disagreements). This
  is the trusted oracle underlying every computational claim.

## Ground rules
- Every assertion labeled PROVED / COMPUTATIONALLY VERIFIED / CONJECTURAL /
  DISPROVED / KNOWN FROM LITERATURE.
- No experimental pattern promoted to theorem without: precise statement →
  broad independent test → smallest-counterexample search → proof.
- Failed approaches preserved with the exact obstruction that killed them.

## Five proof mechanisms
1. **P₁₃-free extension (Track E).** Push the induced-path search to P₁₄-free,
   or extract a human structural dichotomy from its search tree.
2. **Theta / additive path-length lemma (Track C).** A theta subgraph (paths
   a,b,c between two vertices) yields cycles a+b, a+c, b+c. Seek: "any path
   system forced by δ≥3 contains two lengths summing to a power of two."
3. **BFS-layer collision recurrence (Track D).** Exact recurrence on layer
   sizes; show avoiding all 2-power cycles forces unbounded growth. (The
   diameter-2 → {4,8} result L8 is the 2-layer instance.)
4. **Discharging / reducible configurations (Track B).** Re-derive & extend
   Carr 2026 (M1–M4); find a finite reducible-configuration set.
5. **Cycle-space / F₂ dimension.** m−n+1 ≥ n/2 independent cycles for δ≥3;
   try to force a controlled-length simple cycle. (Weak — noted for honesty.)

## Five counterexample mechanisms
1. **SAT/CP-SAT direct search** with symmetry breaking + lazy forbidden-cycle
   clauses. Doubles as independent lower-bound reproduction (UNSAT ⇒ none exists).
2. **Cubic enumeration** (`geng -d3 -D3`) + detector; hunt near-misses à la
   Markström (only length-16 present).
3. **Graph lifts / voltage graphs / covers** — control cycle lengths via
   voltage sums; push girth up and lengths off powers of two.
4. **Cayley graphs** — pick group + generators so relation/word lengths dodge
   {4,8,16,…}.
5. **Local surgery on Markström-type extremal graphs** (only 16-cycles remain);
   try to destroy the 16-cycles without creating 4/8/32 or dropping below δ3.

## Priority order (Phase V — revised 2026-07-24 after external correction)
The old "brute ≤ n=12 then CP-SAT sweep n=13..16" objective is **withdrawn** as
strategically redundant (L10 already gives ≥17; L15 gives a stronger, cheaper
argument). New ranking by (probability of *genuinely new* progress) × verifiability:

- **P1 — Sharp small-order 4-or-8 theorem.** Resolve whether every δ≥3 graph on
  ≤23 vertices contains C4 or C8. **Done through n=19** (L15: n≤17 strict from ex(n)
  < ⌈3n/2⌉; n=18,19 all extremal graphs δ=2; n=18 also re-derived by exhaustive
  geng). **n=20..23:** McKay's exact extremal table already covers these
  (ex=31,33,34,36). The extremal (top) layer is ALREADY CLEARED — all extremal
  graphs at n=20..23 have δ=2 (verified from `.s6` files), which also disposes of
  every excess-2/excess-3 degree sequence. The ONLY remaining search is the
  one-below near-cubic layer, 4 cases:
    1. n=20, m=30, cubic 3²⁰
    2. n=22, m=33, cubic 3²²
    3. n=21, m=32, one deg-4 (4,3²⁰)
    4. n=23, m=35, one deg-4 (4,3²²)
  Method (validated at n=18: 2761 graphs, 0 C8-free survivors, detectors agree):
  `geng -c -f -d3 -D<maxdeg> N M:M res/mod` (−c connected [safe: n≤19 theorem makes
  every component a smaller δ≥3 {C4,C8}-free graph; −f = C4-free, confirmed by geng
  −help], filter degree sequence, reject any C8). A single C8-free survivor at
  n≤23 DISPROVES the stronger theorem — save it immediately in g6+s6+edgelist.
- **P2 — Search-space characterization.** Subsumed into P1 above (the extremal-
  layer characterization is done from McKay's data; test min degree and C16 on any
  P1 survivor). If P1 finds a survivor, check whether it also avoids C16 (only then
  is it E–G-relevant, and only for the eventual n≥32 regime).
- **P3 — Cubic frontier.** Reproduce the cubic ≥30 bound (L11) below 30 with a
  certified incremental generator; then probe order ≥30.
- **P4 — Correct additive theory.** Establish the *actual* extremal behavior for
  both the SET (distinct sums) and MULTISET (equal-length 2ℓ) models; only then
  ask whether δ≥3 forces such a configuration. Do NOT infer graph consequences
  until the additive hypothesis is shown to arise in δ≥3 graphs.
- **P5 — Structural novelty.** Find one restriction on minimal counterexamples
  strictly stronger than Carr's independent-set / domination / (4/7) results
  (e.g. the positive path-replacement lemma B2⁺).

**Certification gate (applies to every expensive run):** record nauty version,
exact command, raw + per-filter counts, per-process exit codes, stream checksums,
proof the full stream was consumed, and a small-order cross-check vs. known
counts; shard large searches by `res/mod` with a manifest requiring all indices.
For solver UNSAT, produce an LRAT/DRAT (or PB) *checkable* certificate — a bare
"UNSAT" line is not accepted. Investigate OR-Tools CP-SAT LRAT proof output; if it
can't certify the model, translate to CNF/PB and use a proof-producing solver.

Deprioritized: unrestricted brute enumeration (redundant), E (P₁₃ frontier, heavy
compute), cycle-space (too weak), lifts/Cayley (only if P1–P3 surface near-misses).

## Redirection 2026-07-25: structures for arbitrary order
The project now also carries a second track alongside P1–P5: results that
apply to *arbitrary* n rather than small fixed n. New/updated files:
`lemmas.md` (S4, S5, ordering-defect lemma summaries), `defect.md` (new —
the ordering-defect parameter D, full derivation), `verifier/defect_model.py`,
`verifier/vine_experiment.py`, `verifier/one_pole_search.py` +
`one_pole_verify.py`. Summary of this pass (see defect.md/lemmas.md for
full proofs):
- **S4 (bridgelessness)** and **S5 (cut-vertex classification)**: PROVED IN
  WORKSPACE from B0–B4/M1–M4 by a "doubling" construction (glue two copies
  of a low-attachment lobe at the shared vertex) — strictly refines the old
  stalled B2 2-connectivity attempt (which tried unsafe suppression; S4/S5
  need no suppression at all). NOVELTY UNCHECKED — see literature.md L16
  (arXiv full-text access blocked in this session; Carr 2026's *abstract*
  has no connectivity content).
- **Defect parameter D := 2n−2−m**: the requested identity and
  Σ(deg−3)=n−4−2D are pure algebra (PROVED). D≤⌊n/2⌋−2 is PROVED from S1.
  D≥2 (⇔ m≤2n−4) is an **open gap** — the natural route ("G−x₁ is
  2-degenerate") is not implied by current lemmas and fails on 6.8–16.0% of
  C4-free δ≥3 graphs computationally (growing with n — see experiments.md
  E7). **The literal central target "n≤2D+3" is DISPROVED outright** — it
  is equivalent to m≤(3n−1)/2, which contradicts S1 unconditionally for
  every δ≥3 graph (not just hypothetical counterexamples); see defect.md §4
  for the exact gap formula and a methodological diagnosis (a pure
  (n,m)-based bound can never work; the real content must come from the
  cycle-avoidance structure).
- **Vine charging lemma V1** ("#missing dyadic lengths ≤ D"): DISPROVED,
  smallest witness n=13 D=0 missing={4} (experiments.md E8).
- **One-pole search** (Part 5): implemented + independent verifier
  (`one_pole_search.py`/`one_pole_verify.py`, cross-checked DFS vs nx
  detectors on both H and its doubled graph). Initial run n=5..9 exhaustive
  (67,432 one-pole candidates, 0 survivors); n=10 in progress — see
  experiments.md E9.
- **P13→lemma-extraction redirection (Part 6)**: no local implementation of
  the P13-free search exists in this repo (L7/Track E cites an external
  paper, Hegde–Sandeep–Shashank, whose code is not reproduced here) — a
  literal "convert the P13 computation" is not possible without first
  re-implementing their search, which is out of scope for this pass. Scoped
  down honestly to applying the same methodology (canonical state
  memoization, proof-DAG of failed completions, minimal impossible states)
  to a search we do control locally — see `verifier/state_search_proto.py`
  and experiments.md E10 for the prototype and its (small, local) findings.

## Reprioritization 2026-07-25 (second pass, post external review)
External review of the redirection pass above reframed priorities. Adopted
in full:
1. **Determine whether S4/S5 are genuinely new.** Targeted literature
   search launched (specific phrase combinations: "minimal counterexample"
   + connectivity/bridge/cut-vertex/block-decomposition terms; standard
   extremal-graph-theory "doubling" technique names; EG survey articles;
   Royle–Markström, Gyárfás, Daniel–Shauger, Heckman–Krakovski, Hegde–
   Sandeep–Shashank papers). Result appended to literature.md L17 when the
   search completes.
2. **Develop the rooted one-pole theory** — now the top computational/
   structural priority, above cubic search. New file `one_pole.md`: a
   "master minimality" framing (smallest object that is either a plain
   δ≥3 F-clean graph or an F-clean one-pole graph) makes the doubling
   argument fully rigorous. Result: **O1 (bridgeless), O2 (H−r connected),
   O3 (H fully 2-connected — strictly stronger than S5 gave for G)** all
   PROVED; **O4 (root-neighborhood theta/book structure)** stated as a
   precise open target with the exact Menger-theorem obstruction recorded
   (2-connectivity of H doesn't by itself give 2 disjoint root-neighbor
   paths avoiding r — that needs ruling out a 2-cut {r,w}). Direct
   cross-link found back to S5: a cut vertex's lobe in G is *itself* a
   one-pole graph, so S5's surviving case (one cut vertex, equal lobes)
   presupposes a one-pole survivor exists.
3. **Ear decomposition / cycle-space** — now well-defined thanks to O3 (H
   2-connected ⇒ has an open ear decomposition). Flagged as the next
   structural direction (one_pole.md §5) but not developed yet.
4. **Computation only to test structural conjectures**, not to push raw
   vertex bounds. The n=10 one-pole exhaustive push is deprioritized under
   this rule (it was pure bound-pushing); resume it only if O4 or the ear
   direction produces a specific small-case conjecture worth testing.

## Status log (newest first)
- 2026-07-25 (correction pass 2, pre-n20-search): tightened the McKay-table
  framing and set up the n=20..23 search.
  - Read ex(n;{C4,C8}) for n=4..23 straight off McKay's file names: strict below
    ⌈3n/2⌉ for n≤17, equality at 18,19, and **exceeds** for n=20..23
    (ex=31,33,34,36). n=20..23 ARE in McKay's table — no regeneration needed.
  - Verified extremal counts (94,12,13644,3257) and that **all** n=20..23 extremal
    graphs have δ=2 ⇒ top edge-layer cleared, incl. all excess-2/3 degree
    sequences. Remaining search = 4 one-below near-cubic cases (P1).
  - **4-or-8 theorem through n=19** finalized with labels: PROVED FROM PUBLIC
    EXTREMAL DATA + COMPUTATIONALLY VERIFIED + NOVELTY UNCHECKED. n=18 also
    re-derived by exhaustive geng (2761 graphs, 0 C8-free, detectors agree).
  - Architecture validated at n=18 (`geng -c -f -d3 -D3` + degree filter + C8
    reject); confirmed `geng -f` = C4-free from geng −help. n=19 re-derivation
    running. Excess identity Σ(deg−3)=2m−3n used to enumerate degree sequences.
  - Certification requirements restated: DRAT/LRAT for any UNSAT; CP-SAT for
    discovery only unless reduced to certified CNF.
- 2026-07-24 (correction pass, external review): Paused compute, fixed two errors.
  - **Killed** the running `geng -c -d3 12` job (947M/~30e9, strategically
    redundant). Cancelled the planned n=13..16 CP-SAT sweep as a frontier target.
  - **P3 partially RETRACTED.** The exact formula "α(H_N)=⌊N/2⌋+1, density 1/2"
    is DISPROVED (witness {1,2,4,5,8,9,10}⊂{1..10}, size 7 > 6); it was inferred
    only from N=2^k samples (E3 sampling trap). VALID: the C2 lower bound and the
    narrowed C3 (single-scale distinct sums insufficient). RETRACTED: "naive theta
    dead" / "only multiscale remains." Added set-vs-multiset modeling distinction.
    True α sequence recorded (experiments E3′) for OEIS lookup.
  - **L15 added & VERIFIED:** McKay ex(n;{C4,C8})=23,25,27,29 (n=16..19) vs
    ⌈3n/2⌉ ⇒ no δ≥3 {C4,C8}-free graph for n=16,17. Downloaded McKay's extremal g6
    and confirmed ALL extremal graphs at n=18 (570) and n=19 (304) have min-degree
    2 ⇒ **the 4-or-8 dichotomy holds through n=19** (proven, not just E–G). New
    finite target: extend to n≤23 (sharp; 24-vertex cubic {C4,C8}-free known).
  - **B2 rescoped** from "obstruction" to a warning + positive-lemma target B2⁺.
  - **P2 (Carr re-derivation) relabelled** KNOWN FROM LITERATURE + INDEPENDENTLY
    RE-DERIVED; it is validation, not new progress.
  - Priorities replaced (P1–P5 above); certification gate added.
- 2026-07-24 (session 1): Substantial progress persisted across proof.md/
  lemmas.md/experiments.md.
  - Detector built + cross-validated (0 disagreements, 2 impls, 5484 checks). ✓
  - **P1:** reproduced "no counterexample ≤ 11 vertices" exhaustively (n=11 =
    577M graphs, 0 ctx; two independent checkers agree through n=10). n=12 in bg.
  - **P2:** re-derived minimal-ctx structure M1/M3/M4 + B0/B1/B3/B4 from scratch
    (match Carr 2026). Recorded B2 obstruction: degree-2 suppression is UNSAFE.
  - **P3:** additive study — α(H_N)=⌊N/2⌋+1, density 1/2 ⇒ Lemmas C2/C3: the
    pairwise-sum/theta mechanism CANNOT force a 2-power cycle in a bounded length
    range. Naive theta proof family FALSIFIED (kept).
  - NEXT: (a) finish n=12; (b) CP-SAT E4 for n=13..16 via UNSAT + C4-free bound;
    (c) cubic E2; (d) test multi-scale path forcing (only additive route left).

## Completed / failed (kept)
- **DISPROVED (P3 exact formula):** "α(H_N)=⌊N/2⌋+1, extremal density exactly 1/2"
  — FALSE off powers of two; a sampling artifact. See experiments E3′, lemmas
  C2-upper. The *valid* residue: C2 lower bound (interval {2^{k-1}+1..2^k} is
  sum-free) and the narrowed C3 (a single-scale, distinct-length book can't force
  a 2-power two-path cycle). RETRACTED: "naive theta dead / only multiscale left."
  The additive/theta route stays live (multiset self-sums, multiplicities, parity,
  differences, ≥3-path cycles all untouched).
- **WARNING, not blocked (B2):** *unqualified* degree-2 suppression shifts cycle
  lengths (by ℓ−1), so blind textbook minor reduction is unsafe — but this does
  not kill all reductions. Open target B2⁺: characterize which reduction
  collections preserve 2-power-cycle existence/non-existence.
- **METHOD LESSON (kept):** a pattern true on a special subsequence (here N=2^k)
  is NOT a theorem. Every "PROVED" from computation must survive a smallest-
  counterexample search over the *general* case before promotion — the failure
  that produced the P3 error.
