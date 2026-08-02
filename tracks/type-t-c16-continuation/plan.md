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
  **Integrity note:** the external `.s6` files underlying the historical
  extremal-layer degree checks are absent locally. Treat that part as
  `EXTERNAL_DATA_MISSING`, not locally reproducible, until the artifacts in
  `manifests/external_s6_manifest.json` are restored and checksummed.
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
  need no suppression at all). NOVELTY SUPPORTED BY SEARCH — two targeted
  passes (literature.md L16, L17) found no prior EGC statement of S4/S5;
  arXiv/mirror full-text access is a confirmed hard platform-level block
  in this environment (not a transient session issue), so this can never
  be upgraded past "search-supported" from here. Closest classical analog:
  Dirac 1953 (k-critical graphs have no cut vertex) — same technique,
  different theorem, no EGC application found.
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
1. **Determine whether S4/S5 are genuinely new.** DONE — literature.md L17.
   Targeted search (specific phrase combinations: "minimal counterexample"
   + connectivity/bridge/cut-vertex/block-decomposition terms; standard
   extremal-graph-theory "doubling" technique names; EG survey articles;
   Royle–Markström, Gyárfás, Daniel–Shauger, Heckman–Krakovski, Hegde–
   Sandeep–Shashank papers) found no prior EGC statement of S4/S5/O1/O3.
   Access to arXiv and every tested mirror is a **confirmed hard
   platform-level block** (verified via direct curl through the egress
   proxy, not just WebFetch) — this project can never read a full paper
   body from this environment, so "novelty supported by search" is the
   ceiling label achievable here, permanently, not just this session.
   Closest classical analog: Dirac 1953 (k-critical graphs have no cut
   vertex) — same proof technique, different theorem, no EGC application
   found; cite it as the method's origin if S4/S5/O1/O3 are written up.
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

## Third pass 2026-07-25: admissible paths, O4a failure structure, SPQR
Per external review, shifted priority from *proving* O4 to *exploiting*
admissible-path theory and classifying O4's failure mode precisely.
- **O4′ [PROVED]:** cited and verified Gao–Huo–Liu–Ma 2022 (IMRN,
  arXiv:1904.08126) — confirmed via targeted search to match the stated
  hypotheses/conclusion; full text unreadable here (platform block).
  Applying it with k=2 to K=H−r (after proving K+ab 2-connected via the
  classical degree-2-suppression fact) gives: **every master-minimal
  one-pole graph has two cycles through its root differing in length by 1
  or 2** — proved without needing the two admissible paths to be
  internally disjoint (the theorem doesn't claim that, and the
  cycle-construction doesn't need it).
- **O4a [PROVED IN WORKSPACE]:** if the 2-disjoint-paths property fails,
  Menger gives a single separator x, and H−{r,x} splits into exactly 2
  lobes attached to both r and x (else x or r would be a cut vertex,
  contradicting O2/O3).
- **Terminal path spectra Λ₁,Λ₂ [PROVED]:** exact identity
  {cross-lobe cycle lengths} = Λ₁+Λ₂; two-terminal doubling (gluing a
  single lobe to itself at both terminals) creates new cycles of length
  exactly Λᵢ+Λᵢ, giving a precise, checked (not order-balance-guessed)
  criterion for when doubling yields a valid one-pole vs. an intermediate
  two-pole object vs. an immediate cycle violation.
- **Computation (E11, E12):** extended the one-pole enumerator
  (`verifier/o4_analysis.py`) — O4 holds directly 99.9% of the time in the
  small relaxed population (n=5–9), failing only in 46/67,432 cases, all
  with small near-symmetric lobes. Added an SPQR-tree classifier
  (`verifier/spqr_analysis.py`, using `spqrtree` — later found insertion-
  order-sensitive, so new R-node claims require the definition-validated
  fallback in `verifier/brute_spqr.py`): it reports that K+ab
  can genuinely fail to be 2-connected outside the F-clean/minimal setting
  (174/67,432 — real content for O3, not a freebie), and that "pure
  series-parallel" essentially never happens even at n≤9 (0/67,258
  classifiable cases) — rigid pieces dominate already at the smallest
  sizes, so the next concrete target is cycle structure inside R-node
  skeletons, not extending the S/P arithmetic.
- **Logical scope correction (one_pole.md, new section):** explicitly
  distinguishes (1) finding any F-clean one-pole survivor = disproves EG
  outright, (2) proving none exists = closes only S5's cut-vertex case for
  a minimal counterexample, (3) the 2-connected minimal-counterexample
  case is untouched and remains a fully separate task.

## Fourth pass 2026-07-25: rigid-core lemma, suppressed-edge equivalence, K4 skeleton
Per external direction: stop broad small-order SPQR statistics, convert
findings into exact structural formulations, begin analyzing the
unavoidable rigid core. Summary (full detail: one_pole.md, manuscript.md):
- **O5 [PROVED]:** every master-minimal one-pole graph has a K4-minor,
  unconditionally (independent of F-cleanness/minimality) — replaces the
  earlier empirical "rigid pieces dominate" (99.7%) with an exact
  structural fact. **Methodological note kept deliberately:** the first
  proof attempt used two hand-built graphs both WRONGLY believed to be
  series-parallel counterexamples to the needed lemma; a direct SPQR
  computation caught both errors before either was written up as a
  disproof (`verifier/rigid_core_check.py` keeps both as a regression
  test). Correct proof: every leaf of a nontrivial SP graph's SPQR tree is
  an S-node contributing a purely-local degree-2 vertex; ≥2 leaves ⇒ ≥2
  such vertices; a one-pole graph's degree profile (exactly 1 vertex of
  degree 2) is incompatible with this, so it can't be SP. 0 violations
  across 304 SP graphs found (n=3–8, E13).
- **Suppressed-edge reformulation [PROVED]:** deleting r and closing with
  a distinguished edge e=ab (genuinely requiring the multigraph category
  when a,b are already adjacent — checked, not assumed: without the
  duplicate edge, δ(Gₑ) can drop to 2) gives an exact equivalence between
  one-pole existence and a purely edge-rooted target over (G,e) pairs with
  δ(G)≥3. Converts the search space entirely, avoiding any special
  handling of the degree-2 root.
- **Exact lobe-doubling inequalities [PROVED]:** order comparison
  |H′ᵢ|<n ⟺ |Dᵢ|<|D_other|; at equal order, edge comparison
  |E(H′ᵢ)|<|E(H)| ⟺ E(Lᵢ)<E(L_other); the conditional conclusion
  "(Λᵢ+Λᵢ)∩F≠∅ whenever H′ᵢ is lex-smaller" is stated WITH its necessary
  tᵢ≥2 qualifier made explicit (not inferred from the sumset alone), and
  the fully-tied case (equal order AND equal edges) is recorded as a
  genuine, unresolved gap rather than glossed over.
- **Rooted SPQR signatures [PROVED, independently verified]:** series/
  parallel Σ(P) composition rules derived and cross-checked against
  brute-force enumeration on concretely assembled graphs (E15, 100% pass).
  Rigid nodes deliberately given no composition rule, per instruction —
  handled by direct analysis instead (K4 case, E16).
- **K4 skeleton [exploratory, E16]:** C4-freeness restriction derived and
  verified exhaustively (at most 4 of K4's 6 edges can be real without an
  immediate C4); bounded search over small virtual-edge spectra found
  5,525/117,649 skeleton-level F-clean configurations — explicitly flagged
  as skeleton-level only, not certified full gadgets.
- **Edge-rooted search [E14]:** 47,349 (G,e) pairs tested n=4–8, 0 full
  failures, 0 near-misses; n=9 attempted but not completed (honestly
  reported, not papered over).
- **Manuscript draft** (`manuscript.md`, new file): S4, S5, O1, O3, O4a,
  O4′, O5, the terminal-spectrum identity, and the suppressed-edge
  equivalence, with the required "novelty supported by the available
  searchable literature; full external expert verification remains
  desirable" wording and citations to Dirac 1953 and Gao–Huo–Liu–Ma 2022.

## Fifth pass 2026-07-25: hardened O5, corrected edge category, O6/O7, K4 refiltering
Per external direction: do not extend the order-8 edge-rooted search;
use master minimality to constrain proper two-terminal pieces instead.
Full detail: one_pole.md, manuscript.md.
- **O5 hardened**: exact SPQR convention stated (Q-nodes suppressed except
  the degenerate single-edge case; no two same-type nodes ever tree-
  adjacent — confirmed by direct testing, not assumed). Added a SECOND,
  convention-independent proof via partial 2-trees + Dirac's 1961 chordal-
  graph theorem (≥2 non-adjacent simplicial vertices unless complete),
  sandwiched to exact degree 2 in G via 2-connectivity. Both proofs
  cross-checked against each other (networkx treewidth decomposition vs
  spqrtree) and against the earlier flawed hand-examples (both
  independently confirmed treewidth 3, i.e. genuinely not partial
  2-trees) — kept as permanent regression tests.
- **Suppressed-edge category corrected**: stated precisely as loopless
  multigraphs with at most one parallel pair, located exactly at the
  distinguished edge's endpoints; the 2 cases (adjacent/nonadjacent root
  neighbors) handled separately; subdividing the distinguished edge
  confirmed (case by case, not assumed) to always recover a simple graph.
- **O6 [PROVED]**: any proper 2-terminal piece P of H (internal degree≥3,
  terminal degree≥2), closed with a fresh root, has an exhaustive cycle
  classification (internal-to-P, automatically safe by inheritance from
  H's F-cleanness, or root cycles of length ℓ+2); whenever the closure is
  lex-smaller than H, this forces Λ(P)∩{2^k−2}≠∅ — tied/non-smaller cases
  handled explicitly, no contradiction claimed there.
- **O7 [PROVED, conditional on O6's hypothesis]**: a remote leaf R-node's
  2 poles can have no common neighbor outside its own territory (else an
  external length-2 path plus O6's forced length-(2^k−2) path would give
  a forbidden 2^k-cycle). Translates to: the parent virtual edge for such
  a leaf can't sit in a triangle with both other edges real.
- **K4 census refiltered**: O7 applied to the 5,525 skeleton-clean
  configurations from the previous pass, 4,717 (85.4%) survive, collapsing
  to 4 orbits under K4's automorphism group.
- **One-R-node target tested, explicitly NOT conjectured** per
  instruction: 118/2,464 relaxed one-pole candidates (n=5–8) have ≥2
  R-nodes, 0 F-clean (expected); but 26/118 have a leaf R-node satisfying
  every currently-proved local condition (O6+O7) while the whole graph
  remains non-F-clean — smallest example n=8, g6 GCQVRw, where the
  obstruction is a 4-cycle unrelated to that leaf's own root-cycle
  mechanism entirely. Diagnosed honestly: O6+O7 are demonstrably
  insufficient alone; the missing condition is unidentified.

## Sixth pass 2026-07-25: redirect to 3-connectivity; freeze one-pole work
Per explicit instruction: `one_pole.md` and manuscript.md's one-pole
sections are **FROZEN** except for corrections/external feedback. New
top-priority target, in new file `two_cut.md`: *every lexicographically
minimal counterexample is 3-connected* (kept CONJECTURAL). Scoped
honestly: this works in the case G is already 2-connected (S5's
non-cut-vertex surviving case / one_pole.md's "logical scope" item 3),
not a claim that 2-connectivity is now unconditionally established.
Summary (full detail: two_cut.md):
- **T1 [PROVED]**: every nontrivial xy-bridge Bᵢ has Bᵢ+xy 2-connected —
  same doubling/case-check technique as S4/S5/O1/O3, now for a 2-cut in
  G itself.
- **T2 [PROVED, citing Gao–Huo–Liu–Ma]**: every Λᵢ contains 2 values
  differing by 1 or 2 — the internal-degree-3 hypothesis is now automatic
  from G's own δ≥3 (simpler than the one-pole case).
- **Global bridge-spectrum identity [PROVED]**: (Λᵢ+Λⱼ)∩F=∅ for i≠j
  (cross-bridge cycles), internal cycles safe by inheritance, and the
  Mersenne-style corollary Λᵢ∩{2^k−1}=∅ when xy∈E(G).
- **T3 [PROVED]**: the qᵢ-fold gluing construction and its exact
  order/edge parameters; qᵢ=1 impossible by minimality; tied/non-smaller
  cases handled explicitly (no contradiction claimed there).
- **Balanced 2-cut census [PROVED where forced, honestly incomplete
  where not]**: at most 3 bridges can simultaneously evade T3's order
  part; the k=3-all-q=3 and k=2-both-q=2 cases are pinned down exactly
  (the latter directly analogous to S5's equal-lobe result: xy∉E(G),
  e₁=e₂ exactly); mixed/partial-evasion cases are recorded as genuinely
  open, not forced into a false unique classification.
- **Bridge-signature library + compatibility search built** (E19, E20)
  but **empty through n=7** — investigated directly (a natural small
  candidate fails via an internal C4), matching the project's broader
  small-order pattern. n=8 attempted, did not complete; not claimed.
- **§7 candidate-cause clustering recorded, target kept CONJECTURAL** —
  no finite exclusion theorem established.
- K4 census **not extended** this pass, per instruction (retained as
  supporting data only).

## Seventh pass 2026-07-25: T4, exact bridge-count classification, T5, corrected balanced census
Per instruction: add subfamily-minimality consequences before extending
the bridge-signature enumeration. Full detail: two_cut.md.
- **T4 [PROVED]**: no proper sub-selection of {bridges}∪{xy edge if
  present} reaches degree ≥3 at both terminals — omitting a bridge
  breaks order-minimality, omitting just the edge (keeping all bridges)
  breaks edge-minimality given the order tie.
- **Exact classification [PROVED]**: a pairwise argument (for t≥3, every
  pair must share aᵢ=aⱼ=1 or bᵢ=bⱼ=1) extends to a common-coordinate
  lemma for all t≥3 bridges simultaneously, and a NEW argument shows
  t≥4 is impossible outright (any 3-subfamily of a common-coordinate
  ≥4-bridge set violates T4 directly) — **every 2-cut has exactly 2 or 3
  nontrivial bridges**, sharpened into exactly Type A (t=3, xy∉E(G),
  a₁=a₂=a₃=1, deg_G(x)=3, q=3,3,3), Type B (t=2, xy∈E(G), a₁=a₂=1,
  deg_G(x)=3, q=3,3), or Type C (t=2, xy∉E(G), neither bridge reaches
  both terminal degrees ≥3, q∈{2,3}).
- **Correction to the fifth pass**: the "k=3 fully-evading" balanced
  case was stated with only an edge INEQUALITY (2eᵢ≥eⱼ+eₖ); this was an
  incomplete derivation — the same inequality, applied to all 3
  simultaneously and ordered, forces e₁=e₂=e₃ EXACTLY (a short ordering
  argument: the smallest value's inequality combined with the trivial
  reverse bound forces equality throughout). Both S5-analogue balanced
  cases (k=2 both q=2, and k=3 all q=3) are now fully pinned equal-
  signature configurations, not one exact and one merely constrained.
- **T5 [PROVED, both versions]**: replacing 2 bridges with 2 copies of
  one of them (dropping the other, three-bridge case) or retaining the
  shared edge (two-bridge-plus-edge case) reduces the whole lex
  comparison to just the doubled bridge's own (c,e) vs. the dropped
  bridge's (c,e) — the third bridge's signature cancels out entirely.
  Corollary: a self-sum-clean bridge is always lex-maximal; if ALL
  bridges in a triple/pair are self-sum-clean, their signatures are
  forced identical — an independent re-derivation of the corrected
  balanced-case conclusion above via a completely different construction.
- **Compatibility search refactored** to the 3 exact types only (no
  arbitrary signature cliques), with T5 applied before cross-spectrum
  checks; new targeted Type-A abstract+realizable search
  (`verifier/three_bridge_search.py`): the historical strict-order model
  reported 318 abstract triples, but this count was incomplete because
  the model could not encode ties. The corrected tied-signature count is
  547; the restored 229 are exactly the triples with at least two
  self-sum-clean bridges. Both counts are regression-only, not evidence
  toward exclusion. 0 realizable is inherited from the empty n≤7 bridge
  library and is therefore vacuous, not evidence of nonexistence.
- **Main target reprioritized**: excluding Type A (three-bridge 2-cuts)
  specifically, ahead of the full 3-connectivity target — kept
  CONJECTURAL, no exclusion theorem claimed.

## Eighth pass 2026-07-25: abstract insufficiency proved, T6 copy-gadget, linkage data
Per instruction: stop investing in unrestricted abstract signature
triples; replace with a direct two-terminal counterexample-gadget
program. Full detail: two_cut.md §7-15.
- **Abstract insufficiency [PROVED]**: an explicit infinite family
  (Λ₁=Λ₂=Λ₃={m,m+1}, valid for 1,979/1,999 tested m) satisfies T2, every
  pairwise cross-compatibility check, and (trivially, once ties are
  modeled correctly) T5's maximality corollary. `three_bridge_search.py`
  corrected: the old strict-permutation T5 check is replaced with a
  ties-aware one (always trivially consistent — the finding itself, kept
  as an explicit checkable confirmation, not silently dropped) and a new
  function verifies the infinite family directly. Abstract survivor
  counts are retired as a route to the three-bridge exclusion.
- **E21 integrity reconciliation**: old strict-order count 318; corrected
  tied-signature count 547; exact delta 229 = 203 exactly-two-clean + 26
  three-clean triples. Regression tests preserve equal and partially tied
  cases. Neither count bears on realizability or resolves a conjectural
  case.
- **T6 [PROVED]**: a standalone, unconditional copy-gadget criterion — no
  minimal-G context needed. Any two-terminal B satisfying 5 structural
  conditions (q(B)∈{2,3}, internal degree≥3, B itself F-clean, B+xy
  2-connected, (Λ(B)+Λ(B))∩F=∅, plus the necessary xy∉E(B) for
  simplicity, made explicit), glued q(B)-fold at both terminals, is a
  genuine Erdős–Gyárfás counterexample outright. Type-A case (d_B(x)=1)
  forces q(B)=3 — a single such B resolves the whole conjecture.
- **Focused conjecture stated [CONJECTURAL]**: every structurally-valid
  Type-A bridge has a dyadic self-sum — proving it closes the balanced
  three-identical-bridge route; disproving it (via T6) ends the project.
- **Linkage data [PROVED]**: the disjoint-pair spectrum 𝒟(B) is always
  dyadic-clean (its cycles are genuine B-cycles); every dyadic self-sum
  witness must therefore involve overlapping paths; the exact
  symmetric-difference identity |P|+|Q|=2ω(P,Q)+Σ(cycle lengths)
  proved and independently verified two ways (E22, 7/7 tests pass).
- **Type-A canonical form [PROVED]**: Λ(B)=1+M(B) (M(B) = path spectrum
  of B minus its degree-1 terminal), reducing the self-sum condition to
  (M(B)+M(B))∩{2^k−2}=∅ on a one-smaller graph.
- **Generator + ranking built**: `bridge_closure_search.py` reuses the
  frozen one-pole search structure directly (x at degree 2 = a one-pole
  root); 5,212 candidates through n=8, 0 internally-clean yet (matches
  the established small-order pattern, not evidence of nonexistence).
  h(B) ranking implemented per the specified priority order; no h(B)=0
  or h(B)=1 qualifying candidate found this pass.
- **T7 (minimum-overlap reduction)**: stated precisely, neither proved
  nor refuted — no genuine witness pair yet exists to test it against.

## Ninth pass 2026-07-25: T8/R1 criticality and complete Type-A order-9 census
Per instruction: prove the deletion rules first, then exhaust exactly bridge
order 9 and directly verify every three-copy lift. Full detail: two_cut.md
§§16–19 and experiments.md E23a/E23b.
- **T8 [PROVED]**: both cleanliness conditions are monotone under edge
  deletion. Minimality therefore makes every bridge edge degree-critical,
  terminal-critical, or closure-2-connectivity-critical, with the exact
  endpoint cases recorded in two_cut.md §16.
- **R1/R1b [PROVED]**: deleting a real edge from a 3-connected R-skeleton
  preserves 2-connectivity, and substituting closed two-terminal expansions
  preserves it. A definition-first SPQR implementation was added after
  adversarial fixtures exposed insertion-order-sensitive false R labels in
  `spqrtree==0.1.2`; it validates all 538 biconnected graph-atlas graphs.
- **T8R [PROVED]**: a real B-edge in an R-skeleton must meet x, an internal
  degree-3 vertex, or y when d_B(y)=1. The relaxed n≤8 audit contains 64,596
  genuine R-real edge instances, with zero R1 failures.
- **Structural split [PROVED]**: d_B(y)=1 is SP-eligible; d_B(y)≥2 has exactly
  one degree-2 closure vertex and is rigid-forced by the partial-2-tree lemma.
- **Order-9 census [COMPUTATIONALLY VERIFIED]**: complete nauty residue 0/1,
  193,510 raw closures, 134,204 degree-filtered rootings, and 129,040 rooted
  oriented isomorphism classes. The split is 4,214 SP-eligible versus 124,826
  rigid-forced; even the SP-eligible population has no actually series-parallel
  closure at this order.
- **Three-copy lifts [COMPUTATIONALLY VERIFIED]**: independent Python and C
  detectors agree on C4/C8/C16 for all 129,040 bridges and all lifts. Every
  bridge already contains C4 or C8, so there are zero internally clean bridges,
  zero survivors, no defined minimum h(B), and no empirical instance on which
  to develop T7. The run manifest and complete per-candidate compressed records
  are preserved under `manifests/` and `data/`.

## Tenth pass 2026-07-25: extremal compression, order 10–11, and SPQR leaves
Per instruction, replace unrestricted closure growth with exact `{C4,C8}`-
free edge layers and finish the P/S/R leaf consequences of T8.
- **Finite Type-A theorem [COMPUTATIONALLY VERIFIED]**: the existing E22/E23
  certificates prove every structural Type-A bridge through order 9 contains
  C4 or C8. The identical-three-copy T6 construction therefore starts at
  order 26, without implying any general Erdős–Gyárfás lower bound.
- **Extremal compression [COMPUTATIONALLY VERIFIED]**: restored the exact
  McKay–Afzaly order-9 (33 graphs, ex=12) and order-11 (245 graphs, ex=15)
  files. Two independent checkers found zero valid ordered terminal choices.
- **Direct order 10 [COMPUTATIONALLY VERIFIED]**: only m=13,14 are possible
  for a clean Type-A bridge. Exact C4-free generation produced 57 and 216
  graphs; 4 and 12 respectively survive C8, but none has a degree-1 root.
  Combined with order 11, the identical-copy floor strengthens to order 32.
- **R2/T8P [PROVED]**: a real P-element is deletable because at least two
  closed-2-connected expansions remain in parallel. Zero failures occur on
  388 atlas P-edges and 3,498 relaxed-closure instances.
- **S/P leaves [PROVED]**: leaf S real edges form a path whose internal
  vertices are exactly x, y, or both in four finite terminal-local forms;
  no remote/larger S leaf and no original P leaf is possible.
- **Rigid-leaf dichotomy [PROVED WITH CORRECTED SCOPE]**: after suppressing
  the x-triangle in a minimal rigid-forced gadget, the core is one R-node or
  has only R leaves. The relaxed audit found why self-sum cleanliness is
  essential: 35 R/P-tight pseudo-failures all expose a length-2 terminal path
  and hence the forbidden self-sum 2+2=4.
- **Order-9 support mining [COMPUTATIONALLY VERIFIED]**: reused, never
  regenerated, all 129,040 E23 records. Canonical shortest witnesses split as
  98,990 one-R-local, 29,581 two-P-expansion, 469 multi-node, and zero S/root-
  local. A later orientation audit refines the 75,745-record leaf-R statement:
  all 72,927 genuine original remote leaves contain a real-edge C4/C8; 608
  root-side nodes exposed only after terminal-S suppression are clean on real
  R-edges, and their contracted C4 uses the suppressed-S element. Those 608
  are closure-orientation warnings, not counterexamples to the remote-leaf LR
  target (see `s6_case_tree.md`).

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
