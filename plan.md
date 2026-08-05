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
- 2026-08-05 (INDEPENDENT CHECK of GPT's order-32-40 direct search claim —
  reimplemented from scratch, partially reproduces and exceeds it):
  - The earlier GPT report claimed an order-32 cubic graph with
    #C4=#C8=0, #C16=676 (via degree-preserving two-edge switches + exact
    cycle counters), but supplied no code, log, or graph file — recorded
    as unverified. Since the method itself (not the specific numbers) is
    well-described, built an independent from-scratch implementation
    (`external_review/order32_direct_search/local_search.py`) rather than
    trusting the claim.
  - Cycle counter validated first against the Petersen graph's known exact
    values (C3=0, C4=0, C5=12, C8=15) before trusting it on anything else.
  - First attempt (single simulated-annealing objective with an infinite
    penalty for any C4 or C8) found **zero** feasible (C4=C8=0) states in
    2,000,000+ iterations over 90s starting from a random cubic graph —
    confirming the report's own observation that a plain boolean gate from
    a random start doesn't work well; a continuous descent is needed first.
  - Redesigned as **two phases** (matching the report's own stated
    strategy): phase 1 minimizes C4+C8 as a continuous objective until it
    hits 0; phase 2 then hard-gates C4=C8=0 (rejects any move that would
    reintroduce either) and anneals to minimize C16.
  - **Result (100s total, single run): phase 1 reached C4=C8=0 in 38,453
    iterations; phase 2 reached C16=304 in the remaining 60s** — better
    than the report's claimed 676 and also better than their "471" figure
    (which they said was itself lost/unpersisted). This independently
    confirms the qualitative claim (C4/C8-free with low C16 is reachable
    by this method) and suggests their reported numbers were not
    optimized very far — 304 in under 2 minutes on a single instance, no
    tuning, no incremental cycle-delta evaluation (the perf optimization
    the report itself flagged as the "highest-value engineering step" and
    did not implement). A longer run is in progress to see how far below
    100 (their own suggested next target) this simple version can get.
  - Best graph so far is persisted to
    `external_review/order32_direct_search/best_n32_seed*.edges` with
    literal re-verification (recount C4/C8/C16 from the saved edge list,
    not trusted from the search state) before being recorded.
  - **Longer run (300s, seed=1): C16=236**, re-verified independently by
    re-reading the persisted edge file from scratch (n=32, e=48, all
    degree 3, connected, C4=0, C8=0, C16=236 recomputed cold). Still above
    the report's suggested <100 target, but a third consecutive
    independent run beating their reported figures (676, 471) with no
    tuning and no incremental cycle-delta evaluation — the report's own
    named "highest-value engineering step," not yet implemented here.
    Continuing to push this down is a legitimate, bounded next step but
    is a compute-bound search, not further hand theory — the theoretical
    thread for this branch is the girth-5/6 kernel work above, not this
    local search (which only speaks to the *general* cubic-graph
    landscape, unconstrained by the girth/triangle structure already
    established for order-30 specifically, and unconstrained to n=30
    since this is order 32).
- 2026-08-05 (t=3 GENERATION RE-SHARDED for restart resilience; GIRTH-6
  kernel exploration started — partial, honestly incomplete, genuinely
  harder than girth-7):
  - **Practical:** confirmed the container has only 4 CPU cores, already
    fully saturated by the order-24 generation (4/4 concurrent geng
    workers) — no parallelism headroom to exploit. Re-sharded from 512-way
    to 1024-way (`order24/shards1024/`) to roughly halve the max work lost
    per restart (~254s/shard -> ~127s/shard), since restarts, not CPU
    availability, are the dominant source of waste. Old 512-way partial
    progress (24 shards) is superseded, not reused (different res/mod
    partition, not resumable across shard counts).
  - **Theory, girth-6 kernel (started, not closed):** applied the same
    method that closed girth-7 to the girth-6 case (fix a 6-cycle C,
    x_i=third neighbor of v_i, H=G-C-{x_i}, 18 vertices). Two facts
    verified by hand so far:
    - x_i are still pairwise distinct (checked all d=1,2,3: same-x cycle
      length d+2 is 3,4,5, all violate girth-6 or hit a forbidden length).
    - x_i CAN be directly adjacent when antipodal (d(i,j)=3): the two
      closing cycles both have length exactly 6 (d+3 and (6-d)+3 both = 6
      at d=3), which is girth itself and perfectly allowed — unlike
      girth-7, where x_i's were forced fully independent. This means the
      girth-6 boundary structure has an extra degree of freedom (up to 3
      possible "antipodal chords" among the 6 x_i, present or absent
      independently) that girth-7 did not have.
    - Consequently, double-attachment kernel vertices (one H-vertex
      adjacent to two x_i directly) are himself NOT forced to zero here:
      distance-1 and distance-2 double-attachments fail (lengths 5,9 and
      6,8 — a 5 violates girth, an 8 is forbidden), but **distance-3
      (antipodal) double-attachment gives cycle lengths exactly 7,7 —
      both valid.** This is the opposite of the girth-7 finding (where the
      external report's analogous "x_i,x_{i+3} viable" claim was wrong);
      here the same-shaped configuration is genuinely viable.
  - **Honest status:** girth-6 does not collapse to a single forced case
    the way girth-7 did (a=0). It has a real branching structure (chord
    count k=0..3 among antipodal pairs, plus double-attachment vertices
    tied to those same pairs) that needs full, careful case enumeration
    before any skeleton search is meaningful. This is a bigger derivation
    than girth-7 and is NOT complete — recording the verified facts now
    rather than rushing an unverified "closed" claim. Continuing this is
    the natural next theoretical step, alongside girth-5 (likely even
    larger, since n=30 is 20 vertices above the girth-5 cage vs. only 6
    above the girth-7 cage, i.e., much more freedom, probably harder, not
    easier).
- 2026-08-05 (GIRTH-7 BRANCH CLOSED — exact, verified, no computation beyond
  a tiny 11-skeleton search): see `external_review/girth7_kernel/`.
  - Built `verify_skeletons.py` to resolve the 11 candidate skeletons
    (9 theta-graph length-triples + 2 double-self-loop profiles) from the
    corrected kernel reduction below into an exact backtracking search over
    every way to assign the 7 boundary labels (2 slots each) to the 14
    skeleton positions, checking every resulting cycle against {4,8,16} and
    girth 7.
  - **Two real bugs were found and fixed in the verifier before trusting
    it**, both caught by independent cross-checks, not by inspection alone:
    (1) the first version reused the theta hub-pairwise formula's `+2`
    offset for the general boundary-excursion case, when the correct
    offset (re-derived against the report's own worked h,h'-adjacent
    example) is `+4`; (2) the self-loop "other way around" distance used
    `lA - d1` instead of the correct `(lA+1) - d1`. Both were caught by
    (a) a trivial sanity check (all-distances-huge input must be feasible —
    it was, confirming the search machinery itself was sound) and (b)
    re-deriving the formula by hand against the report's own already-
    verified d+5/7/8-9 worked example, which the buggy version failed to
    reproduce.
  - Rewrote the verifier to avoid hand formulas entirely: it builds the
    actual skeleton graph (16 nodes: 2 hubs + 14 positions) and enumerates
    every simple path between any two positions by brute-force DFS, so
    there is no distance formula left to get wrong.
  - **Cross-validated against literal 30-vertex reconstruction** (networkx,
    `literal_crosscheck.py`): built real graphs for specific (skeleton,
    labeling) pairs and confirmed with `nx.simple_cycles` that the
    abstracted model's predicted cycle lengths for a given position-pair
    exactly match the literal graph's actual cycle lengths, for both the
    same-label (d=0) and cross-label (d=1,2,3) cases. Also independently
    re-confirmed the a=0 correction (below) directly on a minimal literal
    graph: a vertex double-attached at boundary distance 3 produces cycle
    lengths {7,8} exactly as predicted — the 8 confirms the report's
    claimed-viable case is not actually viable.
  - **Result: all 11 skeletons are infeasible — no labeling avoids {4,8,16}
    and sub-girth cycles on any of them.** Combined with the corrected
    kernel reduction (a=0 forced is provably exhaustive — every order-30
    girth-7 cubic graph decomposes into one of these 11 skeletons, no
    others are possible), this eliminates girth=7 entirely: **no order-30
    cubic Erdős–Gyárfás counterexample can have girth exactly 7.**
  - Combined with the earlier girth exclusion theorem (girth ∈ {3,5,6,7}
    only), the remaining space for any order-30 cubic counterexample is
    now **girth ∈ {3, 5, 6}**.
  - Confidence framing: this is independently derived and cross-validated
    within this session (hand derivation + two independent code paths +
    literal-graph spot checks), but a result of this significance should
    still get a second, from-scratch implementation before being promoted
    to fully certain — same standard applied to the t=4 result before it
    was trusted.
- 2026-08-05 (EXTERNAL REPORT logged + independently corrected — girth-7 kernel
  reduction, theta/self-loop skeleton enumeration):
  - An external ("Codex"-labeled) report was supplied covering three claims.
    Per user instruction, treated as a working lead, not pre-verified truth;
    checked what's checkable without artifacts.
  - **Claim 1 (t=4 "finishes the order-30 search"): OVERREACH, corrected.**
    Our own certified t=4 result (see below) only closes t=4, giving "≤3
    triangles" combined with the prior t=5,6,7 closures. t≤3 remains fully
    open. Recorded as an error, not accepted.
  - **Claim 2 (order 32-40 direct cubic search, #C16=676 at order 32 with
    #C4=#C8=0): UNVERIFIED, no artifacts supplied.** The message referenced
    "Research note," "search implementation," and "persisted record graph"
    as attachments, but none actually arrived — no code, no graph file, no
    log. Recorded as an unverified claim only, per standing project
    discipline; the qualitative idea (C4/C8 easy, C16 is the hard
    constraint) is plausible but not independently checked here.
  - **Claim 3 (girth-7 kernel reduction): CHECKED BY HAND, ONE REAL ERROR
    FOUND AND CORRECTED — net result is a genuine simplification.**
    - The base kernel setup was independently re-derived and confirmed: fix
      a 7-cycle C=v0..v6, each v_i's third neighbor x_i is necessarily
      distinct from all C vertices and from every other x_j (else a cycle of
      length <7 or in {4,8} forms), and each x_i's other 2 edges must go
      into H=G-C-{x_i} (an edge to another C-vertex also forces a forbidden
      length). H has 16 vertices, 14 boundary-edge endpoints from the x_i.
    - **Error found:** the report claims a kernel vertex may have two
      boundary attachments at cyclic distance 3 (x_i, x_{i+3}). Using the
      report's own formula (H-path length ℓ joining two boundary labels at
      distance d gives cycle lengths ℓ+d+2 and ℓ+(7-d)+2) with ℓ=2 (a single
      vertex directly adjacent to both x_i, x_{i+3}): lengths are 7 and 8.
      The 8-cycle is forbidden. Checking distances 1 and 2 the same way also
      fails (sub-girth or forbidden lengths in every case). **Conclusion:
      no kernel vertex can carry two boundary attachments at all — a=0 is
      forced, not a free parameter over {0,...,7}.** (The final |V(H)|=16,
      |E(H)|=17 headline numbers happen to be a=-invariant, so they still
      hold; only the "range of cases" claim was wrong.)
    - This simplifies rather than kills the reduction: with a=0, exactly 14
      kernel vertices carry one boundary edge, 2 carry none (cubic hubs).
      Suppressing all degree-2 vertices, the abstract skeleton is either (i)
      a theta graph — 3 internally-disjoint paths between the 2 hubs, or
      (ii) two hub self-loops joined by a connecting path.
    - **Theta-graph case, hand-enumerated:** path lengths (ℓ1,ℓ2,ℓ3),
      ℓ1+ℓ2+ℓ3=14, each pairwise hub-to-hub cycle (length 16-ℓk for the
      excluded path k) must avoid {4,8,16} and be ≥7, giving ℓk∈{1..9}\{8}.
      Exhaustive hand enumeration of a≤b≤c summing to 14 in that set yields
      exactly 9 surviving triples: (1,4,9), (1,6,7), (2,3,9), (2,5,7),
      (2,6,6), (3,4,7), (3,5,6), (4,4,6), (4,5,5).
    - **Double-self-loop case, hand-enumerated:** loop lengths ℓA,ℓB need
      ℓA+1, ℓB+1 ≥7 and ∉{8,16} (so ℓA,ℓB≥6, ≠7), connecting path
      ℓAB=14-ℓA-ℓB≥0. Only 2 profiles survive (up to hub symmetry):
      (ℓA,ℓB,ℓAB)=(6,6,2) and (6,8,0).
    - **Net: the entire girth-7 order-30 branch reduces to exactly 11
      candidate skeletons.** Remaining work: assign the 7 boundary labels
      (2 slots each of 14 positions) to each skeleton and check every
      resulting cycle (including same-label pairs, which give a separate
      direct cycle of length ℓ+2, needing ℓ≥5 and ℓ∉{6,14} — also derived
      and confirmed by hand here) against the {4,8,16}/girth-7 exclusion.
      This labeling-feasibility check is well-defined but combinatorially
      intricate enough (14 positions, 7-label assignment, two cycle-length
      formulas depending on position AND label) that it should be resolved
      with a short targeted script rather than further hand tracing — this
      would be a tiny computation (11 skeletons) compared to any census run
      so far, not a re-opening of large-scale search.
  - **New rigorous theorem, zero computation.** For a cubic graph on exactly
    n=30 vertices, girth is bounded by the standard (3,g)-cage table (Petersen
    g=5/n=10, Heawood g=6/n=14, McGee g=7/n=24, Tutte–Coxeter g=8/n=30
    (**unique** (3,8)-cage), next cage g=9/n=58). Two exclusions follow with no
    search: (a) girth=4 trivially satisfies E–G (shortest cycle is itself a
    power of 2); (b) girth=8 is impossible for a counterexample because n=30 is
    exactly the (3,8)-cage number and the cage is unique, so the only girth-8
    cubic graph on 30 vertices is Tutte–Coxeter itself, which contains an
    8-cycle by definition of girth. girth≥9 is impossible outright (needs ≥58
    vertices). **Conclusion: any order-30 cubic E–G counterexample has girth
    ∈ {3, 5, 6, 7}.**
  - **Maps exactly onto the existing t-decomposition.** girth=3 ⟺ t≥1 (a
    triangle exists) — the branch the triangle-quotient program already
    covers (t=4..7 closed, t=3 running). girth∈{5,6,7} ⟺ t=0, fully
    triangle-free — a branch the triangle-quotient theorem *cannot* address at
    all (nothing to contract). This branch has zero coverage from any tool
    built so far.
  - **Computational-ceiling finding for the t-branch.** Quotient order is
    30−2t, so it *grows* as t shrinks: t=4→order22 (7.19M, done), t=3→order24
    (~127M, in progress, ~18x growth matching the empirical 20→22 ratio),
    t=2→order26 extrapolates to ~2.2–2.4B, t=1→order28 extrapolates to
    ~40B+ — almost certainly months of generation alone on this hardware, i.e.
    the triangle-quotient chain likely cannot reach t=1 in practice even if
    t=3 and t=2 both close cleanly.
  - **Reframing.** The triangle-quotient program was never going to resolve
    the full order-30 cubic question by itself — it only ever had reach into
    the girth=3 branch, and even there it likely stalls before t=1. The
    untouched girth∈{5,6,7} branch is a structurally different problem
    (needs algebraic/voltage-lift constructions, à la the earlier A5-lift
    work, or a girth-filtered generation — much cheaper than full cubic
    generation since girth≥5 is a strong restriction, not full geng). Within
    that branch, **girth=7 is the highest-leverage entry point**: only 6
    vertices above the McGee cage (24), vs. 20 above Petersen for girth 5, so
    it plausibly has by far the smallest population and is most tractable to
    attack first (analytically or with a cheap targeted search) once t=3
    closes.
  - No claim here has been computationally re-verified in this session beyond
    citing the standard, extremely well-documented cage table; flagging this
    explicitly per project discipline even though cage numbers/uniqueness are
    textbook facts, not external claims.
- 2026-08-04 (t=3 EXTERNAL CLAIM — unverified, recorded for tracking only):
  - A separate external (GPT) session reported closing the order-30 t=3 case
    by a different method than our own catalog census: contract the 3
    triangles, classify the marker-induced subgraph `Q[S]` into its 3
    possible forest types (`3K1`, `K2+K1`, `P3` — **this specific fact
    independently checked**: a forest on 3 vertices has exactly 3
    isomorphism types by edge count 0/1/2, consistent with our own
    already-derived and verified theorem that `Q[S]` must be a forest), then
    exhaustively search finite cubic-pseudograph kernels after deleting
    markers and suppressing degree-2 paths, across 12 exact shared-attachment
    patterns.
  - **Status: UNVERIFIED.** No source code, logs, or data were supplied —
    only a prose description and a boxed conclusion. Per this project's own
    discipline (every claim must be checked before being trusted, see the
    order-38/A5-lift/t=4 audits above, all of which required actual
    artifacts before any compute or belief was extended), this is recorded
    as an external claim only, not a result. If actual source/data
    materializes, it gets the same independent-audit treatment as
    everything else in `external_review/`.
  - **This does not need to be taken on faith either way**: our own
    independent, already-in-progress exhaustive order-24 catalog + t=3
    filter (below) will settle the same question definitively, with full
    certification, regardless of whether this external claim holds up.
- 2026-08-04 (order-30 t=4 CLOSED — real, certified, exhaustive result):
  - **THEOREM (COMPUTATIONALLY VERIFIED): no order-30 cubic Erdős–Gyárfás
    counterexample has exactly four disjoint triangles.** An externally
    supplied (Codex) specialized filter implementing the same exact
    triangle-quotient interval theorem already independently derived and
    verified this session was itself independently audited before use: its
    `allowed_bits` table checked by hand against the theorem's printed
    table, and its aggregate output on a 500-quotient sample cross-validated
    *exactly* (every field) against our own independently-written
    `order30_quotient_marking_census.py` on the same real data. The
    ~340x measured speedup (0.057s vs 19.5s for 500 quotients, confirmed on
    our own hardware, not taken on faith) then let the complete real
    7,187,627-graph order-22 biconnected catalog (generated this session via
    `nauty-geng -c -C -d3 -D3 22`, SHA-256 verified) be checked exhaustively
    in 4m30s wall clock: all 52,577,491,505 four-vertex markings
    (7,187,627 × C(22,4), exact), zero survivors, zero literal/theorem
    mismatches, `complete: true`. Full writeup and certification fields:
    `external_review/t4_intersection_filter/AUDIT.md`.
  - **Combined with the prior session's exhaustive t=7/6/5 closures**
    (`tracks/graph-counterexample-q6-xerdjz/order30_quotient_census.md`,
    orders 16/18/20, ~8.5B instances, zero survivors) and the `>=t`
    corollary there, this **strengthens the standing bound from "at most 4
    triangles" to "at most 3 triangles"** for any hypothetical order-30
    cubic counterexample.
  - Superseded this session's own slower, still-running approach (Python
    marking census + connectivity split on partial data) — the new filter
    needs only plain connectivity (already guaranteed by `nauty-geng -c -C`),
    not the 3-connected/strictly-2-connected split, so that split work is no
    longer necessary for this specific census and was stopped.
  - **Next open target: t=3** (order-24 cubic quotients). A generic version
    of the same filter was mentioned but not supplied/audited this session;
    per the project's own discipline, it needs the same independent audit
    (theorem/table cross-check + small-sample cross-validation against an
    independent implementation) before being trusted with real compute.
    t=0,1,2 also remain open.
- 2026-08-02 (continued session: A5-lift audit + order-30 census extension):
  - **A5-permutation-lift counterexample attempt: audited and extended, converges
    to a negative result.** An externally-supplied (Codex) attempt lifted the
    24-vertex Markström near-counterexample through A5 (5 sheets, 120 vertices),
    reactively patching one bad cycle at a time; rejected for containing a C8.
    Automated and extended this (`external_review/a5_lift_probe/`): wrote an
    independent Python reimplementation of the solver's tree/cotree bookkeeping
    (verified byte-for-byte against the compiled solver's actual behavior),
    then a loop that audits the *entire* literal lift for every forbidden
    length in one pass, derives cuts for all violations, and falls back to
    exhaustive 3-variable repair when local search stalls. Tested against all
    four available 24-vertex near-miss bases (`base0_markstroem`,
    `base1/2/3_hss`, all independently confirmed C4/C8-free with C16 present):
    every one hit a wall where both random-restart search and exhaustive
    k3-repair failed (`base0`: 26 cuts; `base2` and `base3`: independently
    converged to the *same* 9-cut wall; `base1`: couldn't clear even the
    starting constraint). Convergent evidence across 4 independent bases that
    this specific construction (5-sheet A5 lift of these bases, via local
    search) is very likely exhausted, not unlucky. Full writeup:
    `external_review/a5_lift_probe/AUDIT.md`.
  - **Order-30 cubic triangle-quotient census (t=4 case) in progress.** Per
    `tracks/graph-counterexample-q6-xerdjz/order30_quotient_census.md`, orders
    16/18/20 (7/6/5-triangle cases) are exhaustively closed with zero survivors
    (~8.5B instances); by the ">=t" corollary, any order-30 cubic
    counterexample has at most 4 triangles, and t=0..4 remain open. Hand-verified
    the underlying exact-interval lemma (each triangle contributes an
    independently-choosable 1-or-2-edge detour, so cycle lengths lift to an
    *exact*, not merely bounded, interval) against our trusted detector (0
    mismatches on 251 markings across 6 test graphs). Generated the order-22
    catalog for t=4 (7,187,627 biconnected cubic 22-vertex graphs, matching a
    from-scratch geng run) and started the 3-connected/strictly-2-connected
    split (`external_review/split_shard.py`, sharded); marking census
    (C(22,4)=7,315 instances/quotient) to follow once the split completes.
  - Also resumed the two still-open P1 near-cubic cases (n=21, n=23) in the
    background.
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
