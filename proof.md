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
