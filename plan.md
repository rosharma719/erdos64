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

## Status log (newest first)
- 2026-08-02 (branch consolidation + n=20/22 P1 results + order-38 external audit):
  - **P1 progress: n=20 and n=22 cubic cases CLOSED.** Rebuilt the toolchain
    (nauty `geng`, both C checkers) on this session's Linux environment
    (previous work was Mac-only; `certify_shard.sh` had a hardcoded Mac path,
    now fixed to a relative lookup). Cross-validated the rebuilt C checkers
    against `cycle_detect.py` before trusting them (n=10/n=12 C4-free
    streams, 0 disagreements). Ran the certified `geng -c -f -d3 -D3` +
    `check_c8` pipeline for both remaining cubic P1 cases: **n=20** (36,101
    connected cubic C4-free graphs, `c4_seen=0` sanity, raw==checked
    reconciled, **0 C8-free survivors**) and **n=22** (553,227 graphs, same
    all-clear). Logs/manifests in `logs/p1_n20_23/`. n=21/n=23 (one degree-4
    vertex, `-D4`) not yet run.
  - Also untracked the committed platform-specific `check_c8`/`check_g6`
    binaries (source of repeated Mac/Linux churn) — rebuild locally via `cc`
    per the README; and dropped two accidentally-committed `.pyc` files.
  - **Flagged and audited an external fabrication.** A prior conversation
    turn presented an elaborate "order-38 cubic census" result (minimal
    counterexample ≥40 vertices) with no basis in this repo's actual git
    history (one commit at the time) — broken reference links, an
    unverifiable checksum, and citations to a "Wormald–Kingan" theorem and
    specific node/leaf counts with zero backing files. Treated as
    unsubstantiated. When the user separately supplied real transcribed
    source + proof notes for what appears to be that same order-38 line of
    work (evidently produced in a *third*, inaccessible sandbox — hardcoded
    `/mnt/data/...` paths), did an independent audit rather than accept it:
    see `external_review/order38_bundle/AUDIT.md`. Summary: the 3 hand-proof
    notes are logically sound conditional on uncited external theorems
    (Carr 2026, Candráková–Lukoťka, "Wormald–Kingan"); the shared
    cycle-detection primitive cross-validates against `cycle_detect.py` with
    0 disagreements; two full partition classes ((7,31) and the complete
    unfiltered (5,5,5,5,9,9), both `rot` and `nosym` solver variants) were
    reproduced completely from scratch and agree (0 leaves). The other 149
    of 151 claimed partition classes and the aggregate 60.9M-node total
    remain unverified — the underlying result/manifest data files were never
    supplied, only source code and a hash listing.
  - **Discovered 14 more branches with substantial independent prior work**
    on this conjecture (`claude/*` and `codex/*`, 10–159 commits each,
    sharing only the single `init` commit with `main` and this branch —
    never merged). Root-level filename collisions make naive merging unsafe
    (flagged by one branch's own README). Consolidated full snapshots into
    `tracks/<branch-name>/` with `tracks/MANIFEST.md` indexing provenance
    (source branch, head SHA, date); original branches left untouched on
    `origin`. This branch's own P1–P5 priorities above predate that
    discovery and should be read alongside the much deeper Type A/B/C/T
    structural work in `tracks/graph-counterexample-q6-xerdjz/` and related
    tracks before further prioritization.
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
