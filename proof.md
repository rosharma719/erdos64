# proof.md — Erdős #64: current status of proof / counterexample work

**As of 2026-07-24. The conjecture is OPEN. Nothing here claims resolution.**
This file separates rigorously established progress from conjectural observations.

## Verdict so far
No proof and no counterexample. What follows is honest partial progress, each
item labeled. The two active tracks are (A) computational lower-bound/counterexample
search and (C) additive-combinatorics analysis of the theta mechanism.

## Rigorously established here (independent of literature)

### P1 [COMPUTATIONALLY VERIFIED] No counterexample on ≤ 11 vertices
Exhaustive over all connected graphs with δ≥3 (nauty `geng -c -d3`), tested by a
validated power-of-two cycle detector (two independent implementations, 0
disagreements on 2107+3377 cross-checks). n=4..10 confirmed by BOTH a Python and
a C checker with identical graph counts; n=11 (577,076,528 graphs) by the C
checker. Reproduces the lower part of Royle–Markström's ≥17 (L10) from scratch.
(n=12 brute run TERMINATED 2026-07-24 at 947M/~30e9 graphs — strategically
redundant: L10 already gives ≥17, and the McKay {C4,C8} extremal route below is a
stronger, cheaper argument. Full ≥17 by brute force is out of reach, ~50×/vtx.)

### P2 [PROVED] Minimal-counterexample structure, re-derived from definitions
Let G minimize (|V|,|E|) among δ≥3 graphs with no power-of-two cycle.
- **B0.** G is C4-free (4∈F), hence ≤ ½(1+√(4n−3))n edges (Kővári–Sós–Turán).
- **B1.** G is connected.
- **B3 = M1.** Every edge has a degree-3 endpoint ⇒ degree-≥4 vertices form an
  independent set; ≥1 degree-3 vertex exists. (Deletion-minimality.)
- **B4.** Every neighbor of a degree-≥4 vertex has degree exactly 3.
- **M3.** n₃ ≥ (4/7)n. (Double count high–low edges: 4n₊ ≤ Σ_high deg ≤ 3n₃.)
- **M4.** A regular minimal counterexample is cubic.
These independently reproduce Carr 2026 (arXiv:2605.22844) M1/M3/M4 from scratch,
confirming the literature. M2 for degree-3 vertices remains Carr's (not re-derived).

### P3 [PARTIALLY RETRACTED — 2026-07-24] Single-scale distinct-sum forcing is insufficient
**Correction.** The earlier [PROVED] version overclaimed. Precisely:
- **C2 lower bound [VALID].** The interval {2^{k-1}+1,…,2^k} (size 2^{k-1}) has no
  two *distinct* elements summing to a power of two ⇒ power-of-two-sum-free
  subsets of {1..N} reach size ≥ ⌊N/2⌋.
- **C2 sharp formula [DISPROVED].** "α(H_N)=⌊N/2⌋+1 exactly / density exactly 1/2"
  is FALSE — it was read off only from N=2^k samples (E3). Counterexample:
  {1,2,4,5,8,9,10} ⊆ {1..10} has size 7 > ⌊10/2⌋+1 = 6. Exact small-N values are
  now recorded (lemmas.md C2-upper, experiments.md E3′); true density > 1/2 for
  most N, asymptotics unresolved here.
- **C3 [VALID but NARROWED].** A book with *distinct* lengths inside one dyadic
  scale creates no power-of-two two-path cycle — supported by the valid C2 lower
  bound alone. This rules out only that one sub-mechanism.
- **RETRACTED overclaims:** "the naive theta approach is dead" and "only a
  multiscale additive route remains." Not established. The theta/additive route
  stays live; graph structure may force equal-length pairs (self-sums 2ℓ),
  multiplicities, parity/residue constraints, overlapping thetas, length
  differences, or ≥3-path cycles. **Modeling note:** path lengths form a
  *multiset*, and two equal-length paths ℓ give a cycle 2ℓ — a distinct
  constraint that the set model above ignores.

**Warning, rescoped (B2, not an "obstruction"):** *unqualified* degree-2 path
suppression shifts cycle lengths (by ℓ−1 for a length-ℓ path), so it does not
preserve power-of-two-ness. This rules out the blind textbook minor reduction,
not all reductions; seek the positive transformation lemma B2⁺ (lemmas.md).

### P4 [THEOREM — 3 labels below] 4-or-8 dichotomy through n=19
**Every graph with δ≥3 on ≤19 vertices contains a C4 or a C8.** (Strictly stronger
than Erdős–Gyárfás through n=19.) Proof: for n≤17, ex(n;{C4,C8}) < ⌈3n/2⌉ (McKay),
so a δ≥3 graph has too many edges to be {C4,C8}-free; for n=18,19 equality holds
and every extremal {C4,C8}-free graph has min-degree 2 (checked over all 570 + 304
of them), so none is δ≥3. Labels:
- [PROVED FROM PUBLIC EXTREMAL DATA] the ex(n) values are McKay's.
- [COMPUTATIONALLY VERIFIED] min-deg computed for every extremal graph n=16..19;
  n=18 independently re-derived by exhaustive geng (2761 cubic C4-free graphs, 0
  C8-free, DFS/nx agree). n=19 geng re-derivation running (E5c).
- [NOVELTY UNCHECKED] not to be called new until a literature search finds no
  prior statement — may be implicit in the extremal tables. See literature L15.

**Extension status (n=20..23).** ex(n) now *exceeds* ⌈3n/2⌉, so the top edge layer
is not forced to δ=2 — but a direct check of McKay's extremal files shows all
n=20..23 extremal graphs have δ=2, clearing the top layer (incl. all excess-2/3
degree sequences). Remaining: 4 one-below near-cubic cases (n=20 m=30 cubic; n=22
m=33 cubic; n=21 m=32 4,3²⁰; n=23 m=35 4,3²²) — a geng search, validated at n=18.
A single C8-free δ≥3 survivor at n≤23 would DISPROVE the stronger theorem (but not
E–G, since C16 remains available below n=32). See plan P1 / experiments E6.

## Conjectural / directional (NOT proved)
- Whether δ≥3 forces a u–v path system spanning ≥2 dyadic scales (would revive an
  additive route). Open.
- Whether the P₁₃-free search (L7) extends or yields an extractable human lemma.
- 2-connectivity of a minimal counterexample (claimed in literature; my
  deletion-only re-derivation is incomplete — see B2).

### P5 [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH] Bridgelessness + cut-vertex classification (2026-07-25 redirection)
**S4.** A minimal counterexample has no bridge. **S5.** If v is a cut
vertex, G−v has exactly two components, v has exactly 2 neighbors in each
(degree 4), the two lobes have equal order (n odd) and equal edge count,
and G has at most one cut vertex. Both proved from B0–B4/M1–M4 by a
degree-preserving "doubling" construction (glue two copies of a lobe at
their shared low-attachment vertex) — see lemmas.md S4/S5, defect.md §1
remark. This supersedes the stalled B2 attempt (unsafe suppression); no
suppression is needed. Literature check (L16, L17 — two targeted passes):
no prior statement found in accessible sources. arXiv/mirror full-text
access is confirmed blocked at the platform level (direct curl through
the egress proxy also 403s, not just WebFetch), so this label cannot be
upgraded past "novelty supported by search" from this environment, ever.
Closest classical analog: Dirac 1953 (k-critical graphs have no cut
vertex) — same technique, no EGC application found.

### P6 [mixed — see defect.md] Ordering-defect parameter D
D := 2n−2−m. The requested identity and Σ(deg−3)=n−4−2D are
[PROVED, pure algebra]. D≤⌊n/2⌋−2 is [PROVED from S1]. D≥2 (⇔m≤2n−4) is
**[OPEN — gap]**: not implied by current lemmas, and the natural witness
route fails computationally on 6.8–16.0% of C4-free δ≥3 graphs (growing
with n). The literal central target "n≤2D+3" is **[DISPROVED]**
unconditionally for every δ≥3 graph (equivalent to m≤(3n−1)/2, contradicted
by S1) — see defect.md §4 for the full proof and diagnosis. The vine
charging lemma V1 ("#missing dyadic lengths ≤ D") is **[DISPROVED]**,
witness n=13 D=0 missing={4}. Full detail: defect.md (new file).

### P7b [PROVED, novelty unchecked] One-pole gadget structure (2026-07-25, second redirection pass)
New file one_pole.md, "master minimality" framing (smallest object that is
either a plain δ≥3 F-clean graph or an F-clean one-pole graph — this
resolves a snag where naive one-pole-only minimality can't handle a bridge
split producing a plain graph). Result: **O1 (bridgeless), O2 (H−r
connected), O3 (H fully 2-connected)** — O3 is strictly stronger than S5's
"at most one cut vertex" for G, because peeling a piece off a one-pole
graph always strictly shrinks it (no same-order loophole). Cross-link to
S5: a cut vertex's lobe in G is itself a one-pole graph, so S5's surviving
case presupposes a one-pole survivor exists. **O4** (does H−r contain 2
disjoint root-neighbor paths, forcing a genuine theta/book structure onto
Track C's additive machinery) is the precise next open target, with the
exact Menger-theorem obstruction recorded. This is now the top structural
priority per the reprioritization in plan.md.

### P7c [PROVED / mixed] Admissible paths, O4a failure structure, SPQR (2026-07-25, third redirection pass)
Cited and verified Gao–Huo–Liu–Ma 2022 (IMRN, arXiv:1904.08126) and applied
it (k=2, after proving K+ab 2-connected via classical degree-2
suppression) to get **O4′ [PROVED]:** every master-minimal one-pole graph
has 2 cycles through its root differing in length by 1 or 2 — without
needing path disjointness. **O4a [PROVED IN WORKSPACE]:** if 2 disjoint
root-neighbor paths don't exist, Menger gives a 1-vertex separator x
splitting H−{r,x} into exactly 2 lobes attached to both r,x. Exact
terminal-path-spectrum identity (cross-lobe cycles = Λ₁+Λ₂) and a
two-terminal doubling criterion (new cycles from doubling one lobe =
Λᵢ+Λᵢ) both proved. Computation: O4 holds directly 99.9% of the time in a
small relaxed population (E11); a real SPQR-tree classifier (`spqrtree`
package, Gutwenger–Mutzel algorithm) shows K+ab's 2-connectivity is
genuine content of O3 (fails 174/67,432 times outside the F-clean/minimal
setting) and that rigid (non-series-parallel) pieces already dominate at
n≤9 (E12). Full detail and the logical-scope correction (finding a
survivor vs. eliminating the cut-vertex case vs. the untouched
2-connected case) in one_pole.md.

### P7 [COMPUTATIONALLY VERIFIED, in progress] One-pole search (task Part 5)
Rooted graphs with one degree-2 root, rest δ≥3, searched for power-of-two-
cycle-freeness (a survivor doubles into a direct counterexample via S4's
construction). n=5..9 exhaustive: 67,432 candidates, 0 survivors. n=10
launched; independent verifier (`one_pole_verify.py`, dual-detector +
explicit doubled-graph recheck) ready for any future survivor. See
experiments.md E9.

## Next concrete steps (revised 2026-07-24 — see plan.md for full priority order)
The unrestricted brute-force ladder (n=12) and the n=13..16 CP-SAT sweep are
**cancelled** as strategically redundant. New target: the *stronger* 4-or-8
dichotomy via extremal generation, not all connected δ≥3 graphs.
1. **P1 (sharp small order).** Verify McKay's ex(n,{C4,C8}) for n=16..19 against
   ⌈3n/2⌉ (16,17: strict ⇒ no δ≥3 graph; 18,19: equality ⇒ inspect min degree of
   the extremal graphs). Then push toward n≤23 (24-vertex cubic C4/C8-free graph
   is known ⇒ 23 is the sharp endpoint). Prefer extremal / edge-bounded `geng`.
2. **Certification.** Any exhaustive/UNSAT claim needs a manifest (nauty version,
   exact command, raw + per-filter counts, exit codes, checksums, small-order
   cross-check) and, for solver UNSAT, an LRAT/DRAT checkable proof — not a bare
   "UNSAT" line.
3. **Track C (still live).** Test whether δ≥3 forces a multi-scale OR
   repeated-length path system (the additive route was NOT killed). Track
   distinct-sum vs. equal-length (2ℓ) constraints separately.
4. **B2⁺.** Derive the positive path-replacement cycle-length transformation lemma.
5. Spot-check B3/M3 on edge-minimal C4∧C8-free graphs (E-struct).
