# lemmas.md — Erdős #64

Status labels: PROVED (by me, from definitions, here) / KNOWN FROM LITERATURE /
CONJECTURAL / DISPROVED. "Minimal counterexample" G = a graph minimizing
(|V|,|E|) lexicographically among all graphs with δ≥3 and **no** cycle of
length a power of two. Forbidden lengths F = {4,8,16,32,…}.

Cycle-lifting discipline: an operation is "safe" for us iff it never creates and
never length-shifts a forbidden cycle. **Vertex/edge deletion is safe** (it only
destroys cycles; surviving cycles keep their length). **Degree-2 suppression is
NOT safe** — it shifts cycle lengths by 1, breaking power-of-two-ness (see B2).

**Consolidated 2026-08-18.** Every named lemma produced across the seven
research branches appears exactly once below, at the label its originating
branch gave it. The full proofs of the core (B/M/G/S/O/C/D/I) families
follow this index unchanged; the later track lemmas are stated canonically
in the index with a pointer to the file carrying their proof, because those
proofs are long and already written out there. Cross-references to
`proof.md` sections are given throughout.

---

# Canonical lemma index, by track

## Track A — degree structure of a minimal counterexample (proof.md P2)

| id | statement | label | proof |
|---|---|---|---|
| **B0** | `G` is C4-free; `m ≤ ½(1+√(4n−3))n` | PROVED | below |
| **B1** | `G` is connected | PROVED | below |
| **B2** | 2-connectivity by degree-2 suppression | **DISPROVED as a method** — suppression shifts lengths by `ℓ−1` | below |
| **B2⁺** | which reduction collections preserve power-of-two-cycle existence | CONJECTURAL, open target | — |
| **B3 = M1** | every edge has a degree-3 endpoint; degree-≥4 vertices are independent | PROVED | below |
| **B4** | every neighbour of a degree-≥4 vertex is cubic | PROVED | below |
| **M2** | every vertex is adjacent to a degree-3 vertex | KNOWN FROM LITERATURE (Carr 2026); partial workspace re-derivation | below |
| **M3** | `n₃ ≥ (4/7)n` | PROVED (independent re-derivation of Carr) | below |
| **M4** | a regular minimal counterexample is cubic | PROVED | below |
| **G1** | `n₃ ≥ (2/3)n` | PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH | below |
| **G2** | `m ≤ 2n−3` | PROVED IN WORKSPACE, KNOWN INGREDIENTS | below |
| **G3** | `q = 2n−2−m ≥ 1`; `Σ(d−3) ≤ n−6` | PROVED IN WORKSPACE | below |
| **S1** | excess identity `Σ(deg−3) = 2m−3n` | PROVED, elementary | below |
| **S2** | extremal-layer reduction | PROVED, given McKay's `ex(n)` | below |
| **S3** | connectedness is safe for the `n ≤ 23` search | PROVED, given the `n ≤ 19` theorem | below |

## Track B — separators, one-pole gadgets, 2-cuts (proof.md P5, P7b/c, P14, P15)

| id | statement | label | proof |
|---|---|---|---|
| **S4** | a minimal counterexample has no bridge | PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH | below |
| **S5** | cut-vertex classification: exactly 2 components, `deg v = 4`, equal lobe order (so `n` odd) and equal lobe size, at most one cut vertex | PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH | below |
| **O1** | a master-minimal one-pole graph is bridgeless | PROVED | `one_pole.md` |
| **O2** | `H−r` is connected | PROVED | `one_pole.md` |
| **O3** | `H` is fully 2-connected | PROVED | `one_pole.md` |
| **O4** | `H−r` has two disjoint root-neighbour paths | **CONJECTURAL** | `one_pole.md` |
| **O4′** | `H` has two root cycles differing in length by 1 or 2 | PROVED (via Gao–Huo–Liu–Ma 2022, `k=2`) | `one_pole.md` |
| **O4a** | failure structure: a 1-vertex separator `x`, two lobes, cross-lobe cycles `= Λ₁+Λ₂`, doubling gives `Λᵢ+Λᵢ` | PROVED IN WORKSPACE | `one_pole.md` |
| **O5** | *rigid core:* every master-minimal one-pole graph has a K4-minor — unconditional, from the degree profile plus 2-connectivity alone | PROVED, COMPUTATIONALLY REPRODUCED, **two independent proofs** (SPQR leaves; partial 2-trees via Dirac 1961) | `one_pole.md`, `manuscript.md` §3 |
| **O6** | proper two-pole forcing: `Λ(P) ∩ {2ᵏ−2} ≠ ∅` when `H_P` is smaller | PROVED, conditional | `one_pole.md` |
| **O7** | no external common neighbour at a remote leaf R-node | PROVED, COMPUTATIONALLY REPRODUCED | `one_pole.md` |
| **suppressed-edge equivalence** | a one-pole graph exists iff some loopless `Gₑ` with δ≥3 has an edge `e` such that every F-cycle uses `e` and no `e`-cycle has length in `{2ᵏ−1}` | PROVED | `one_pole.md`, `manuscript.md` §3 |
| **T1** | the bridge closure is 2-connected | PROVED | `two_cut.md` |
| **T2** | endpoint admissible paths | PROVED, KNOWN FROM LITERATURE ingredient (Gao–Huo–Liu–Ma) | `two_cut.md` |
| **T3** | bridge self-forcing / minimality | PROVED | `two_cut.md` |
| **T4** | *the 2-cut trichotomy:* minimal terminal cover and the exact **Type A / Type B / Type C** classification of every 2-cut by terminal-degree profile — order-independent | PROVED | `two_cut.md` §2c, `separator_theorem_order32_gap_analysis.md` §2c |
| **T5** | replacement forcing | PROVED, IMPLEMENTATION_FIXED | `two_cut.md` |
| **T6** | direct simple copy-gadget criterion | PROVED | `two_cut.md` |
| **T7** | — | **CONJECTURAL**, gated on finding one internally clean bridge | `s6_case_tree.md` |
| **T8 / T8R / T8P / R1 / R1b / R2** | minimal Type-A gadget edge-criticality, the T8+R1 incidence rule, real R/P-edge deletion | PROVED, COMPUTATIONALLY REPRODUCED | `two_cut.md`, `verification_status.md` |
| **F12** | every two-terminal `B`, `\|V\|=12`, `d(x)=1`, `d(y)≥1`, `xy∉E`, internal degree ≥3, `B+xy` simple 2-connected ⇒ C4 or C8 | COMPUTATIONALLY VERIFIED, exhaustive, dual-detector | `f12_order12_result.md` |
| **FC-15** | as F12 but `d(x)=2`, `d(y)≥2`, `\|V\|≤15` | COMPUTATIONALLY VERIFIED, exhaustive | `fcn_order15_result.md` |
| **F13–F19** | the `d(x)=1` forbidden-`{4,8}` existence series is UNSAT contiguously through 19 | COMPUTATIONALLY VERIFIED | `fcn_satsolver_extension.md` §4.4 |
| **FC-18** | the `(2,*)`-terminal series is UNSAT through 18 | COMPUTATIONALLY VERIFIED | `fcn_satsolver_extension.md` §4.3 |
| **FC-19/20/21** | the same for 19–21 | **DISPROVED** — verified C4/C8-free `(2,2)`-terminal survivors exist | `fcn_satsolver_extension.md` |
| **monotonicity lemma** | `S`-UNSAT ⇒ `S'`-UNSAT for `S' ⊇ S` | PROVED, set containment on solution sets | `type_c_closure_order32.md` |
| **2-cut order floor** | a minimal counterexample with any 2-cut has `n ≥ 36` (Type A ≥56, Type B ≥38, Type C ≥36) | COMPUTATIONALLY VERIFIED | `order32_bounds_f19_extension.md` |
| **O32-1** | if `\|V(G)\|` is even, `G` has no cut vertex | PROVED (S5 parity) | `separator_theorem_order32_gap_analysis.md` |
| **3-connectivity corollary** | every even-order minimal counterexample with `17 ≤ n ≤ 33` is 3-connected | COMPUTATIONALLY VERIFIED — see proof.md P14 for a recorded `[17,35]` inconsistency | `three_connectivity_general_order.md` |
| **cubic 3-edge-connectivity** | a cubic minimal counterexample of even order in `[17,33]` has no edge cut of size 1 or 2 | PROVED (Whitney `κ ≤ λ ≤ δ`) | `cubic_edge_connectivity.md` |
| **V (separator-defect formulas)** | `q(G) = 2d(lobe)` for S5; `q(G) = Σd(Bᵢ) − {4,3,2}` for Type A/B/C | PROVED, COMPUTATIONALLY REPRODUCED | `defect.md` |

## Track C — contraction, Type N / Type T (proof.md Part III)

| id | statement | label | proof |
|---|---|---|---|
| **near-power edge lemma** | every **nontriangle** edge of a minimal counterexample lies on a cycle of length `2ᵏ+1` | PROVED; mechanics COMPUTATIONALLY REPRODUCED | `contraction.md` Part I, audited in `every_edge_witness_audit.md` |
| **safe-contraction obstruction** | no nontriangle edge is ever safe; the "global safe-edge target" is equivalent to the conjecture itself | PROVED | `contraction.md` Part II |
| **cubic nontriangle-edge count** | every cubic vertex of a C4-free graph has exactly 1 or exactly 3 nontriangle incident edges | PROVED, COMPUTATIONALLY REPRODUCED | `contraction.md` Part III |
| **clean same-length merge** | two equal-length `(2ʳ+1)`-cycles sharing exactly one edge and no other vertex force a `2^{r+1}`-cycle | PROVED, verified for `L=5,9,17,33` | `contraction.md` Part IV |
| **general atom-lifting lemma** | for connected `A` with (H2) no outside vertex has 2 neighbours in `A` and (H3) `\|∂A\| ≥ 3`, every simple `a`–`b` path of length `r` in `G[A]` lifts a power-of-two cycle of `G/A` to a `2ᵏ+r`-cycle of `G` | PROVED; mechanics COMPUTATIONALLY REPRODUCED | `contraction_atoms.md` Part I |
| **triangle automatic contractibility** | every triangle of a C4-free graph satisfies (H2),(H3) automatically | PROVED, COMPUTATIONALLY REPRODUCED | `contraction_atoms.md` Part III |
| **Type N / Type T dichotomy** | exhaustive, exclusive: a cubic vertex has 0 internal edges among its neighbours (**Type N**) or exactly 1 (**Type T**, unique triangle). Global elimination of either type is explicitly NOT established | PROVED, COMPUTATIONALLY REPRODUCED | `contraction_atoms.md` Part IV |
| **Type N witness classification** | exactly 2 isomorphism types of loopless 3-element functional digraphs; the five-lemma arithmetic toolkit resolves both; **neither is eliminated** | PROVED | `contraction_atoms.md` Part V |
| **CN1, cubic power-path lemma** | for every cubic vertex some two neighbours are joined in `G−v` by a path of length `2ᵏ`, giving a `2ᵏ+2`-cycle through `v` | PROVED; the forced-distinct-attachment step is a minimality argument, not mechanically testable | `contraction_neighborhood.md` I.3–I.4 |
| **NPT arithmetic lemmas** | `2ˣ+2ʸ−1` and `2ˢ+2` are never powers of two (`x,y,s ≥ 2`); **every clean combined orbit at a Type-N vertex is unconditionally safe** | PROVED, COMPUTATIONALLY REPRODUCED | `contraction_mixed_witness.md` Part IV |
| **cell-decomposition identity** | non-crossing case: `\|P\|−\|Q\| = Σ(αᵢ−βᵢ)` over divergent cells; each divergent cell yields a cycle of length `αᵢ+βᵢ` | PROVED | `contraction_intersections.md` V.1 |
| **one-cell reduction target** | the canonical joint witness choice forces exactly one divergent cell | **DISPROVED**, smallest exact obstruction recorded | `contraction_intersections.md` V.2 |
| **crossing case** | common vertices in different relative order along the two paths | **OPEN**, explicitly unresolved | `contraction_intersections.md` V.3 |
| **CB1, central return** | the theta bridge carrying the cubic centre's third edge always has ≥2 attachments | PROVED | `contraction_central_bridge.md` I.1 |
| **CB2, one-excursion target** | — | **NOT PROVED OR DISPROVED**; a two-excursion itinerary exhibited but not certified canonical | `contraction_central_bridge.md` V.2 |
| **CB3′, block-or-separator** | the correct three-case dichotomy; ≥3 attachments is a genuinely new failure mode | PROVED | `contraction_separator_integration.md` VI.2 |
| **MA1** | multi-attachment admissible-pair lemma | PROVED, COMPUTATIONALLY REPRODUCED | `contraction_block_cut_tree.md` Part IV |
| **MA2** | the central bridge trichotomy | PROVED, COMPUTATIONALLY REPRODUCED | `contraction_block_cut_tree.md` Part V |
| **VI.5, theta saturation** | — | **OPEN**, neither proved nor disproved | `contraction_saturation.md` |
| **Lemma NE** | no two cubic triangle vertices share an external neighbour | PROVED, COMPUTATIONALLY REPRODUCED | `central_bridge_triangle.md` II.1 |
| **pole-forcing theorem** | *the aligned pole `X_x` of a cubic Type-T vertex can never be cubic* — hence **T3 eliminated, T2 narrowed to `X_x = X_y = z₀`** | PROVED, COMPUTATIONALLY REPRODUCED (gadgets `ρ_x ∈ {2,3,4,5}`) | `central_bridge_triangle_pole_forcing.md` |
| **Theorem 2.1 (divergent cells)** | complete composition classification: `k=1` + dyadic `T` FORCED; `k=1` + non-dyadic UNIVERSALLY SAFE; `k≥2` + `T=3k` UNIVERSALLY SAFE; `T=3k+1` forced; `T ≥ 3k+2` escapable but not universal | PROVED | `type_t_overlap_reduction.md` §2 |
| **alternating ladder family** | an explicit infinite colored family; no finite core list bounds the incidence structure in general | PROVED as an abstract object; **STRUCTURALLY SUPERSEDED** as a Type-T residual (its premise row is excluded by pole forcing) | `type_t_overlap_reduction.md`, `type_t_ladder_saturation.md` Thm 1.1 |
| **identical-terminal reduction** | the whole identical-terminal residual reduces to one yes/no question (do `P₁ˣ`, `P₁ʸ` share an internal vertex?) | PROVED, but **MOOT** — the host row `X_x=y, X_y=x` is excluded by pole forcing | `type_t_identical_terminal_joint_spectrum.md` |
| **R2/S2** | — | **CLAIM_REFUTED**, explicit Heawood/Balaban counterexamples | `type_t_recovery_audit.md` |
| **B19 / B20 / B20D2** | every bridge role of all 16 frozen Type-B tuples has order ≥21, so all 16 reach full-graph order ≥40 | PROVED using EXHAUSTIVE FINITE COMPUTATION | `type_b_b19.md`, `type_b_one_slack_resolution.md`, `type_b_delta2_zero_slack.md` |
| **joint two-central-bridge Type-T interaction** | — | **NOT ATTEMPTED** (top priority) | `contraction_ma2_integration.md` Part X |

## Track D — Type-T C16 port completion (proof.md Part IV)

| id | statement | label | proof |
|---|---|---|---|
| **support-bound theorem** | with `m` hub passages and `r` hubs used (`m ≤ r ≤ 2m`), a length-`L` simple cycle satisfies `L ≥ 2m + r`, hence `m ≤ ⌊L/3⌋`; and `m ≥ 2` always. So **C4 conflicts cannot exist**, **C8 conflicts have `m=2` exactly** (support size 1 or 2), **C16 conflicts have `m ∈ {2,3,4,5}`**, `v ≤ 5` | PROVED | `type_t_port_c16_compilation.md` §1.2–1.4 |
| **`m=1` screen completeness** | no candidate triple or gadget can close a dyadic cycle of *any* length by itself | PROVED | `type_t_port_c16_compilation.md` §1.3 |
| **`Φ_{4,8}` exactness** | exact-cover base clauses + C8 conflicts at `m=2` is exactly complete for `{C4,C8}`, with no CEGAR loop | PROVED | `type_t_port_c16_compilation.md` §1.5 |
| **affine dyadic-avoidance theorem** | the bare core `H(j,a,c)` avoids **every** dyadic cycle length, for **every** valid `j ≥ 4` and every valid `a,c`. 35 affine forms `A·2ʲ+B`, `A ∈ {0,1,4,5}`, killed by a 2-adic valuation argument (`v₂(B) ≤ 3` for all 29 forms with `A>0, B≠0`) | PROVED, unconditionally; form-completeness closed by an independent kernel/cycle-space derivation | `type_t_port_core_dyadic_avoidance.md` |
| **passage-support soundness (lifting) theorem** | a supported passage-based cycle candidate yields a genuine simple cycle subgraph of `G`, **regardless of any other edge of `G`** — unused attachments of supplying hubs and all other selected gadgets are irrelevant | PROVED | `type_t_port_c16_passage_projection.md` "Passage-support soundness theorem" |
| **at most one `p3` passage** | per completed graph | PROVED (after two rounds of correction, both recorded) | `type_t_port_c16_passage_projection.md` |
| **passage projection** | 128.9× (`(4,55,7)`) and 206.7× (`(4,28,4)`) compression vs. gadget-level, cross-validated | COMPUTATIONALLY VERIFIED | same |
| **C16 stage ledger `(4,55,7)`** | `m=2` (32,921), `m=3` (279,859), `m=4` (3,971,519) complete **outright**; `m=5` (2,944,894) **COMPLETE_RELATIVE_TO** the pre-`m=4` shadow | COMPUTATIONALLY VERIFIED at the stated scopes | same |
| **gadget-level `(4,28,4)` catalog** | 227,725 minimized `C4/C8` clauses, 0 C4 supports; 84,936 inclusion-minimal C16 supports | **BOUNDED_INCOMPLETE** — residual projection still SAT | `tracks/type-t-c16-static-sat/type_t_port_c16_compilation.md` |

## Track E — order-30 cubic census and girth kernels (proof.md Part VII)

| id | statement | label | proof |
|---|---|---|---|
| **exact quotient characterization** | contracting all `t` triangles of a bridgeless cubic C4-free 30-vertex graph gives a simple **2-connected** (not merely 3-connected) cubic quotient on `30−2t` vertices, and `G` is uniquely recovered | PROVED | `order30_quotient_census.md` |
| **exact-interval lemma** | each contracted triangle contributes an independently choosable 1-or-2-edge detour, so quotient cycle lengths lift to an **exact**, not merely bounded, interval | PROVED, hand-verified against the trusted detector (0 mismatches, 251 markings, 6 graphs) | `order30_quotient_census.md`, `tracks/order30-census/` |
| **`≥t` corollary** | closing quotient order `30−2t` closes every `t' ≥ t` standalone | PROVED | `order30_quotient_census.md` |
| **triangle-count theorem** | a 30-vertex cubic counterexample, if one exists, has **at most three** pairwise disjoint triangles | COMPUTATIONALLY VERIFIED, EXHAUSTIVE (`t=7,6,5,4` closed) | `order30_quotient_census.md`, `tracks/order30-census/t4_intersection_filter/AUDIT.md` |
| **girth-7 kernel** | `\|V(R)\|=16`, `\|E(R)\|=17`, `deg_R = 2¹⁴3²`; the girth-7 branch is closed at order 30 | PROVED, independently re-derived twice | `tracks/order30-census/girth7_kernel/` |
| **girth-6 `(s=0,a=0)`** | exhaustively eliminated: 17 topologies × 1,294,670 compositions, 13,074 passing the pre-filter, **0 feasible labelings** | COMPUTATIONALLY VERIFIED, EXHAUSTIVE (after a real degree-collapse bug was caught and fixed) | `tracks/order30-census/girth6_kernel/exhaustive_s0a0.py` |
| **(6,7)-kernel theorem** | L1 (C chordless), L2 (`\|R\|=16`), L3 (W-edges only at distance 3, forming a single 7-cycle `H₃`), L4 (`S` a matching, `\|S\| ≤ 3`), L5 (doubled R-attachments only at distance 2), L6; counting theorem `deg_R = 1^a 2^{14−2\|S\|−2a} 3^{a+2+2\|S\|}`, `\|V(R)\|=16`, `\|E(R)\|=17+\|S\|`, `a ≤ 7−\|S\|`. Girth-7 degeneration (`S=∅`, `a=0`) reproduces the girth-7 kernel exactly | PROVED, hand-derived; **does NOT close (6,7)** | plan.md status log 2026-08-06 |
| **Theorem A (chord-span)** | in a Hamiltonian order-30 cubic counterexample every chord has span in `{2,4,5,6,8,9,10,11,12,13,14}`; bipartite case `{5,9,11,13}`; no antipodal chord | PROVED; **requires Hamiltonicity** | plan.md status log 2026-08-06 |
| **Theorem B (3-edge-cut reduction)** | a nontrivial 3-edge-cut forces both contracted sides to thread their entire power-of-two spectrum through one degree-3 vertex — **not conditional on minimality**, the verified Royle–Markström base case does the work | PROVED | plan.md status log 2026-08-06 |
| **additive/multiplicative diagnosis** | degree-driven global cycle-length theorems produce additive length windows; `{4,8,16,…}` is multiplicative, so at δ=3 they are near-vacuous — no degree-based global argument can close `n=30` | DIAGNOSIS, explicitly **not a theorem** | plan.md status log 2026-08-06 |

## Track F — additive / theta (proof.md P3, Part VIII)

| id | statement | label | proof |
|---|---|---|---|
| **C1** | "forced power-of-two sum" | CONJECTURAL, target | below |
| **C1a** | elementary necessary condition on a single theta | PROVED | below |
| **C2 lower** | `{2^{k−1}+1,…,2^k}` is power-of-two-sum-free, so `α ≥ ⌊N/2⌋` | PROVED | below |
| **C2-upper** | `α(H_N) = ⌊N/2⌋+1`, density exactly 1/2 | **DISPROVED** — witness `{1,2,4,5,8,9,10} ⊂ {1..10}` | below |
| **C3** | single-scale distinct-length pairwise sums are insufficient | PROVED, narrowed | below |
| **D-def / D-identity** | `D := 2n−2−m`; `Σ(deg−3) = n−4−2D` | PROVED, pure algebra | below |
| **D-upper** | `D ≤ ⌊n/2⌋−2` | PROVED from S1 | below |
| **D-lower** | `D ≥ 2` | **OPEN — gap** (witness route fails on 6.8–16.0% of C4-free δ≥3 graphs) | below |
| **Central-target** | `n ≤ 2D+3` | **DISPROVED** unconditionally for every δ≥3 graph | below |
| **V1 (vine charging)** | #missing dyadic lengths `≤ D` | **DISPROVED** — witness `n=13`, `D=0`, missing `{4}` | below |

## Track G — the defect ladder (proof.md P8–P13)

| id | statement | label | proof |
|---|---|---|---|
| **I.1a–c** | `e(C,H)`, `\|E(F)\|`, `β(F)` cubic-core identities | PROVED, COMPUTATIONALLY REPRODUCED | below |
| **I.1d** | the `C1/C2/C3` degree partition | PROVED, needs M2 | below |
| **I.2** | component-incidence quotient `Q`, with the `κ(F) ≥ 2` correction | PROVED | below |
| **I.3** | weighted-incidence cycle formula (coefficient corrected `t → 2t`) | PROVED, corrected | below |
| **II.0** | fast `O(n(n+m))` equivalent of property (2) | PROVED | below |
| **leaf-count identity** | `c1 = c3 + 4h − 2q − 4` | PROVED, pure algebra | below |
| **L1–L4 (derived leaf graph)** | `L(G)` is simple, cycle-lifting, power-cycle-clean, 2-degenerate | PROVED (L1/L2 also mechanically verified; L3/L4 are minimality arguments, not empirically testable) | below |
| **h ≤ q** | weak corollary of `c3+2h ≤ 2q+1` | PROVED, scope precise | below |
| **D1** | δ≥3 + property (2) + `m=2n−3` ⇒ C4 or C8? | **OPEN**, neither proved nor refuted | below |
| **D1C** | proposed nonedge-completion lemma | **DISPROVED** from `n=9` | below |
| **q(G) ≥ 2 / ≥ 3 / ≥ 4** | `\|E\| ≤ 2\|V\|−4 / −5 / −6` | PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH | below, `defect.md`, `defect_three.md` |
| **bounded branching-kernel lemma** | `n=2q+4` (`h=0`), `c3=2q` (`h=1`), `c1+c3 ≤ 2q−2` (`h≥2`) | PROVED, COMPUTATIONALLY REPRODUCED | `defect_three.md` |
| **colored degree-2 path lemma** | `t ≤ 2,5,8` for `h=1,2,3` (each tight); extended to `t(4)=12`, `t(5)=18` | PROVED, **two independent implementations**, 0 mismatches over 29,655 words | `defect_three.md`, `defect_q_ge6_audit.md` |
| **colored cyclic-word classification** | no valid pure-cycle F-component at `h=1,2`; exactly `s=3,5` at `h=3` | PROVED, cross-checked exhaustively to `s=13` | `defect_three.md` |
| **q(G) ≥ 5, q(G) ≥ 6** | — | **NOT_ESTABLISHED** (externally claimed, zero matching artifacts) | `defect_q_ge6_audit.md` |

---

# Full proofs of the core families


## B0. Definition sanity  [PROVED]
G a counterexample ⇒ G has no 4-cycle. (4 ∈ F.) So **every counterexample is
C4-free**, hence (Kővári–Sós–Turán) has ≤ ½(1+√(4n−3))·n edges. It may still
contain triangles and C5,C6,C7. Girth ∈ {3,5,6,7,…}, never 4.

## B1. Connected  [PROVED]
A minimal counterexample is connected. *Proof.* A component C has δ(C)=δ within
C ≥3 (components are degree-closed) and its cycles are cycles of G, so C has no
forbidden cycle. If G were disconnected, a component is a strictly smaller
counterexample. ∎

## B2. 2-connectivity — NOT proved here; obstruction recorded  [CONJECTURAL]
Claimed in the literature. My attempted proof fails at a precise point, which is
itself informative:
- Take an endblock B with unique cut vertex v. Every non-cut vertex u∈B has all
  its edges inside B, so deg_B(u)=deg_G(u)≥3. No block is a bridge (a bridge
  endpoint would have degree 1 < 3). So B is 2-connected, deg_B(v)≥2.
- If deg_B(v)≥3: B has δ≥3, is C4/…-free (subgraph), and |B|<|G| ⇒ smaller
  counterexample. Contradiction. **So deg_B(v)=2.**
- deg_B(v)=2 with B-neighbors a,b: the natural reduction is to *suppress* v
  (delete v, add edge ab). **This is unsafe:** every cycle through a-v-b (length
  ℓ) becomes a cycle through edge ab (length ℓ−1). A power-of-two cycle can be
  created or destroyed by the ±1 shift, so B-suppressed is not a valid
  counterexample and minimality gives no contradiction.
**Warning, not an "obstruction" (rescoped 2026-07-24):** what is actually
established is narrow — *unqualified* suppression of a degree-2 path changes
lifted cycle lengths (a length-ℓ path replacing an edge shifts every cycle
through it by ℓ−1) and so does not preserve power-of-two-ness. This does **not**
prove that no reduction works; it only rules out the textbook length-preserving
minor argument used blindly. Positive replacement lemma to seek (target B2⁺):
characterize exactly how each cycle length transforms when a length-ℓ path
replaces an edge (every cycle through the edge → +（ℓ−1), cycles avoiding it
unchanged), and find conditions on a *collection* of such reductions under which
the existence / non-existence of power-of-two cycles is preserved. 2-connectivity
must then come from a deletion-only argument or from B2⁺, not asserted here.

## B3. Every edge has a degree-3 endpoint  ⇔  M1  [PROVED]
In a minimal counterexample, every edge is incident to a vertex of degree exactly
3. *Proof.* Let e=uw. Deletion is safe, so G−e has no forbidden cycle. If both
deg(u),deg(w)≥4, then δ(G−e)≥3 still, so G−e is a counterexample on the same
vertex set with fewer edges — contradicting lex-minimality. Hence min(deg u,deg
w)=3. ∎
**Corollary M1 [PROVED]:** the vertices of degree ≥4 form an **independent set**
(any edge between two would violate B3). And there is ≥1 degree-3 vertex (G has
an edge; its degree-3 endpoint). This is exactly Carr 2026's M1, re-derived.

## B4. Neighborhoods of high-degree vertices  [PROVED]
If deg(v)≥4 then **every** neighbor of v has degree exactly 3. *Proof.* Edge vw,
v has degree ≥4, so by B3 the degree-3 endpoint must be w. ∎

## M3. At least 4/7 of vertices have degree 3  [PROVED — independent re-derivation]
Let n₃ = #{deg 3}, n₊ = #{deg ≥4}, n = n₃+n₊. By B4 all neighbors of high
vertices are degree-3, so the number of high–low edges is exactly Σ_{v:deg≥4}
deg(v) ≥ 4·n₊. Each degree-3 vertex meets ≤3 such edges, so that same count is
≤ 3·n₃. Hence **4 n₊ ≤ 3 n₃**, giving n₊ ≤ ¾ n₃ and n ≤ (7/4) n₃, i.e.
**n₃ ≥ (4/7) n**. ∎ (Matches Carr 2026 M3 exactly, derived from scratch.)

## M4. A regular minimal counterexample is cubic  [PROVED]
If G is r-regular, r≥4 ⇒ no degree-3 vertex, contradicting B3's corollary
(degree-3 set nonempty). δ≥3 rules out r<3. So r=3. ∎

## M2. Every vertex is adjacent to a degree-3 vertex  [KNOWN FROM LITERATURE;
## partial workspace re-derivation]
- For deg(v)≥4: immediate from B4 (all its neighbors are degree-3). [PROVED]
- For deg(v)=3: NOT implied by B3/B4 (v is itself the degree-3 endpoint of its
  edges, so no constraint forces a degree-3 neighbor). This is the nontrivial
  case; proved by Carr 2026. [KNOWN FROM LITERATURE]

## G1. At least two-thirds of the vertices are cubic  [PROVED IN WORKSPACE;
## immediate but apparently unpublished strengthening of Carr 2026]
Let
\[
C=\{v:d_G(v)=3\},\qquad H=\{v:d_G(v)\ge4\}.
\]
By M2, each vertex of `C` has a neighbor in `C`. Because it has degree three,
it therefore has at most two neighbors in `H`, and hence
\[
e(C,H)\le 2|C|.
\]
By M1, `H` is independent. Thus every edge incident with a vertex of `H`
goes to `C`, and
\[
e(C,H)=\sum_{h\in H}d_G(h)\ge4|H|.
\]
Consequently `4|H| <= 2|C|`, so `|C| >= 2|H|`. Since
`|V(G)|=|C|+|H|`,
\[
\boxed{|C|\ge \frac23|V(G)|}.
\]

**Audit.** The application of M2 to a cubic vertex is legitimate: M2 says
that *every* vertex has a degree-three neighbor, not merely that every high
vertex does. Simplicity rules out the vertex itself serving as that neighbor.
The equality for `e(C,H)` uses both the independence of `H` and the partition
`V(G)=C union H`, which follows from `delta(G)>=3`.

Carr's Theorem 0.1 instead bounds `e(C,H)` above by `3|C|` and obtains `4/7`.
The full Carr paper and targeted searches for this `2/3` statement and its
double count revealed no earlier occurrence. The deliberately conservative
status is therefore **immediate but apparently unpublished strengthening**,
not a claim of priority; see `literature.md` L18.

## G2. Global edge bound  [PROVED IN WORKSPACE]
Write `n=|V(G)|` and `m=|E(G)|`, and choose any `v in C`. Every nonempty
subgraph of `G-v` is a proper subgraph of `G`, so Carr's Lemma 0.1 gives it a
vertex of degree at most two. This is exactly the hereditary definition that
`G-v` is 2-degenerate. A 2-degenerate simple graph on `N>=2` vertices has at
most
\[
2(N-2)+1=2N-3
\]
edges: repeatedly remove a vertex of degree at most two and read the removals
as a forward-degree ordering, whose caps are `2,...,2,1,0`. Taking `N=n-1`
and using `d_G(v)=3` gives
\[
m-3=|E(G-v)|\le2(n-1)-3,
\]
and hence `m<=2n-2`.

Suppose equality holds. Then `G` has `n` vertices and `2n-2` edges. Moreover
Carr's Lemma 0.1 says more than is required here: *every* proper subgraph has
minimum degree at most two, so in particular no proper **induced** subgraph has
minimum degree at least three. This is the modern literature definition of a
degree-3-critical graph. Erdős--Faudree--Gyárfás--Schelp proved that every
such graph on at least five vertices has cycles of lengths 3, 4, and 5. The
hypothetical `G` has order at least five and is `C4`-free, a contradiction.
Therefore
\[
\boxed{|E(G)|\le2|V(G)|-3}.
\]

This is degree-criticality, not chromatic-criticality or edge-chromatic
criticality. The ingredients are Carr's proper-subgraph lemma, the standard
2-degenerate edge bound, and the classical EFGS theorem; see `literature.md`
L19.

## G3. Nonnegative ordering defect  [PROVED IN WORKSPACE]
Define
\[
q(G)=2|V(G)|-2-|E(G)|.
\]
G2 gives `q(G)>=1`. Fix any cubic vertex `v` and let
`x_1,...,x_{n-1}` be a 2-degeneracy ordering of `G-v`. Put
`a_i=|N(x_i) intersect {x_{i+1},...,x_{n-1}}|`. Then
\[
a_i\le b_i:=\min(2,n-1-i),\qquad
(b_1,...,b_{n-1})=(2,...,2,1,0).
\]
Every edge of `G-v` is counted once by the forward degrees, so
\[
\sum_i(b_i-a_i)
=(2(n-1)-3)-(m-3)=2n-2-m=q(G).
\]
Thus `q` is the total of nonnegative local deficits from the maximal
2-degenerate sequence, for every choice of cubic `v` and every such peeling
order. Also
\[
\sum_{u\in V(G)}(d_G(u)-3)=2m-3n
=n-4-2q(G)\le n-6.
\]
No classification of the `q=1` case is asserted.

---

## S4. Bridgelessness  [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH — 2026-07-25; see literature.md L17]
A minimal counterexample G has no bridge.

*Proof.* Suppose e = uv is a bridge. G−e has exactly two components; let A be
the one containing u, B the one containing v (so A∪B = V(G), A∩B = ∅,
u∈A, v∈B). Every vertex of A other than u keeps its full G-degree inside A
(none of its edges left A, since only e crosses the cut), so deg_A(w) =
deg_G(w) ≥ 3 for w∈A∖{u}; and deg_A(u) = deg_G(u) − 1 ≥ 2 (u loses only e).
Symmetrically for B and v. Also every cycle of A is a cycle of G (A is an
induced subgraph on a vertex-disjoint piece), so since G has no F-cycle
(F = {4,8,16,…}), neither does A; likewise B.

**Case 1: deg_A(u) ≥ 3 (equivalently deg_G(u) ≥ 4), or symmetrically
deg_B(v) ≥ 3.** Then A itself already has δ(A) ≥ 3 and no F-cycle, and
|A| ≤ n−|B| ≤ n−1 < n (B is nonempty, it contains v) — so A is a smaller
δ≥3, F-cycle-free graph, contradicting the order-minimality of G. (Same
argument with B if deg_B(v) ≥ 3.)

**Case 2: deg_A(u) = deg_B(v) = 2 exactly** (i.e. deg_G(u) = deg_G(v) = 3).
Take two disjoint copies A, A′ of A and identify their copies of u into a
single vertex u* (edges are not merged, only the vertex). Call the result
A**. Then:
- *δ(A**) ≥ 3.* Every vertex of A** other than u* is an unidentified copy of
  some w∈A∖{u}, degree unchanged at deg_A(w) ≥ 3. The vertex u* has the 2
  edges from copy A plus the 2 edges from copy A′, degree exactly 4 ≥ 3.
- *No new cycles cross the two copies.* u* is the only vertex shared by the
  two copies; a simple cycle visits u* at most once, so the (at most) two
  cycle-edges incident to u* both come from the same copy — if one came from
  each copy, the cycle would have to travel from a vertex of copy A (≠u*) to
  a vertex of copy A′ (≠u*) without revisiting u*, impossible since the two
  copies share no other vertex or edge. Hence every simple cycle of A**
  lies entirely inside one copy, so it is (a copy of) a cycle of A — already
  known to avoid F. **No F-cycle in A**.**
- *Fewer vertices.* |A**| = 2|A| − 1. Writing n = |A|+|B| (B nonempty, so
  |B| ≥ 1), and using |A| ≤ n − 1 (B nonempty): if |A| ≤ |B| then
  2|A| − 1 ≤ |A| + |B| − 1 = n − 1 < n. If instead |A| > |B|, apply the
  identical construction to B (B is in Case 2 as well, deg_B(v)=2) to get
  B** with |B**| = 2|B| − 1 < |A| + |B| = n (since |B| < |A| ⇒
  2|B| < |A|+|B| = n, so 2|B|−1 < n − 1 < n). Either way, doubling the
  no-larger side of the bridge produces an order-smaller δ≥3, F-cycle-free
  graph — contradicting order-minimality of G.

Both cases contradict minimality of G, so G has no bridge. ∎

*Remark.* This is exactly the "one-pole doubling" construction used
operationally in Part 5 below: a bridge endpoint of degree 2 inside its own
side is precisely a one-pole graph (root degree 2, else δ≥3) whose gluing
would refute the conjecture, so S4 says such a one-pole graph can never be
"F-cycle-free" if a genuine minimal counterexample existed with that bridge —
equivalently, **the one-pole search of Part 5 is a direct independent test of
S4's contrapositive**: any F-cycle-free one-pole survivor found by search,
doubled at its root, is by itself already a valid smaller-order candidate
counterexample (it does not even need to originate from splitting a larger
G) — see Part 5.

## S5. Cut-vertex classification  [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH — 2026-07-25; see literature.md L17]
Let v be a cut vertex of a minimal counterexample G. Then:
1. G−v has **exactly two** components.
2. v has **exactly two** neighbors in each of the two components (so
   deg_G(v) = 4).
3. The two lobes (component ∪ {v}) have **equal order**: (n+1)/2 each (in
   particular n is odd whenever G has a cut vertex).
4. Edge-minimality forces the two lobes to have **equal edge counts** too.
5. G has **at most one** cut vertex.

*Setup.* Let G−v have components C₁,…,C_k (k≥2 by definition of cut
vertex). No vertex of Cᵢ is adjacent to a vertex of Cⱼ (i≠j) — all their
G-edges stay inside Cᵢ∪{v}. Let Aᵢ = G[Cᵢ∪{v}] (the *lobe* through v), and
let dᵢ = deg_{Aᵢ}(v) = the number of edges from v into Cᵢ = the number of
distinct neighbors of v in Cᵢ (simple graph). Σdᵢ = deg_G(v) ≥ 3. Every
vertex w∈Cᵢ keeps its full G-degree inside Aᵢ (its edges all stay in
Cᵢ∪{v}), so δ(Aᵢ∖{v}-part) ≥ 3 automatically; only v's degree in Aᵢ can be
below 3. Cycles of Aᵢ are cycles of G, hence F-free.

*Step 1: dᵢ ≥ 2 for every i.* If dᵢ = 1 for some i, that single edge from v
into Cᵢ is a bridge of G — contradicting S4. dᵢ = 0 is impossible (Cᵢ would
be disconnected from v, contradicting v a cut vertex with Cᵢ one of the
components hanging off it — Cᵢ is connected to v by definition of "the
components of G−v", i.e. dᵢ≥1 always). So dᵢ ≥ 2.

*Step 2: dᵢ = 2 for every i (not ≥3).* If dᵢ ≥ 3 for some i, then Aᵢ already
has δ(Aᵢ) ≥ 3 (v included) with no F-cycle, and |Aᵢ| = |Cᵢ|+1 ≤ n − 1 < n
(some other Cⱼ, j≠i, is nonempty since k≥2) — a smaller counterexample,
contradiction. So dᵢ = 2 for all i, giving deg_G(v) = Σdᵢ = 2k — v has exactly 2 neighbors
in each component (claim 2's first half); the "degree 4" half of claim 2
follows once k=2 is established next.

*Step 3 (⇒ claim 1, k=2): at most two components survive minimality.*
Suppose k ≥ 3. Double lobe Aᵢ at v exactly as in S4 Case 2: two disjoint
copies of Aᵢ glued at the shared vertex v (now degree 4 in the glued graph:
2+2 edges). The identical argument as S4 shows the glued graph Aᵢ* has
δ ≥ 3, no F-cycle (any cycle through v uses two same-copy edges at v, since
the copies share only v), and order 2|Aᵢ|+1 = 2|Cᵢ|+1 (v is not doubled,
|Aᵢ| = |Cᵢ|+1, glued order = 2(|Cᵢ|+1) − 1 = 2|Cᵢ|+1). This contradicts
order-minimality whenever 2|Cᵢ|+1 < n, i.e. |Cᵢ| < n − |Cᵢ| − 1 =
Σ_{ℓ≠i}|Cℓ|. If this failed for **every** i (no valid contradiction
anywhere), then |Cᵢ| ≥ Σ_{ℓ≠i}|Cℓ| for all i, i.e. 2|Cᵢ| ≥ Σ_ℓ|Cℓ| = n−1
for all i; summing over the k components gives k(n−1) ≤ 2Σᵢ|Cᵢ| = 2(n−1),
so k ≤ 2 — contradicting k ≥ 3. Hence some i gives a genuine order
contradiction, so **k ≥ 3 is impossible: G−v has exactly two components.**
∎(1) Combined with Step 2, deg_G(v) = 2·2 = 4 with 2 neighbors in each
component. ∎(2)

*Step 4 (⇒ claim 3, equal order): the two lobes have equal order.* With
k=2, write C₁,C₂, |C₁|+|C₂| = n−1. Doubling the smaller lobe Aᵢ (order
2|Cᵢ|+1) gives an order contradiction unless 2|Cᵢ|+1 ≥ n for **both** i=1,2
simultaneously, i.e. |C₁| ≥ (n−1)/2 and |C₂| ≥ (n−1)/2; since
|C₁|+|C₂|=n−1 this forces equality **|C₁| = |C₂| = (n−1)/2** (any strict
inequality on one side would force the reverse strict deficit on the other,
contradicting both bounds holding at once). In particular n−1 is even, so
**n is odd**. Both lobes have order (n−1)/2 + 1 = (n+1)/2. ∎(3)

*Step 5 (⇒ claim 4, equal edge counts): edge-minimality among order-n
counterexamples.* G minimizes size (edge count) among all δ≥3, F-cycle-free
graphs on its own vertex order n (lexicographic minimality, order first).
With |C₁|=|C₂|, doubling either lobe now preserves order exactly:
|Aᵢ*| = 2|Cᵢ|+1 = n for i=1,2. Count edges: |E(Aᵢ)| = (internal edges of
Cᵢ) + dᵢ = (internal edges of Cᵢ) + 2, so internal(Cᵢ) = |E(Aᵢ)|−2, and
|E(G)| = internal(C₁)+internal(C₂)+d₁+d₂ = (|E(A₁)|−2)+(|E(A₂)|−2)+2+2 =
|E(A₁)|+|E(A₂)|. Doubling gives |E(Aᵢ*)| = 2|E(Aᵢ)| (the two copies share
no edge, only the vertex v). So |E(A₁*)| = 2|E(A₁)| compares to
|E(G)| = |E(A₁)|+|E(A₂)|: |E(A₁*)| < |E(G)| ⟺ |E(A₁)| < |E(A₂)|. If
|E(A₁)| ≠ |E(A₂)|, doubling the lobe with fewer edges yields a same-order,
strictly-fewer-edges δ≥3 F-cycle-free graph, contradicting the size part of
G's lexicographic minimality. Hence **|E(A₁)| = |E(A₂)|.** ∎(4)

*Step 6 (⇒ claim 5, at most one cut vertex).* Suppose v, w are two distinct
cut vertices of G. By Steps 1–4 (applied to v), G−v has exactly two
components C₁,C₂ each of order (n−1)/2, and w ≠ v lies in one of them, say
w∈C₁. Consider G−w: by the same theorem applied to w, G−w has exactly two
components D₁,D₂, each of order (n−1)/2 (n is odd, consistent, since the
same n is used). v ≠ w, so v∈D₁ or v∈D₂; say v∈D₁.

Now locate C₂ inside {D₁,D₂}. Every vertex of C₂ has all its G-edges
inside C₂∪{v} (v is a cut vertex separating C₁ from C₂), and w∉C₂ (w∈C₁,
C₁∩C₂=∅), so no vertex of C₂ is adjacent to w. Hence C₂ is untouched by
deleting w: G[C₂] is still connected (it was a component of G−v, so
connected already) and still attached to v via its unchanged edges to v.
So C₂∪{v} is connected in G−w and contains v, forcing **C₂∪{v} ⊆ D₁**
(D₁ = the component of G−w containing v). Consequently D₂, being disjoint
from D₁, satisfies **D₂ ⊆ C₁∖{w}** (the only vertices not in C₂∪{v}∪{w}
are C₁∖{w}). Therefore |D₂| ≤ |C₁| − 1 = (n−1)/2 − 1 = (n−3)/2.

But Step 4 applied to w requires |D₂| = (n−1)/2 exactly. Since
(n−3)/2 < (n−1)/2 strictly, this is a contradiction. Hence **G cannot have
two distinct cut vertices: at most one exists.** ∎(5) ∎

**Corollaries recorded for reuse.**
- If G has a cut vertex, n is odd and both lobes have exactly (n+1)/2
  vertices and (n−1)/2−|E| ... i.e. equal size **and** equal edge count —
  the two lobes are combinatorially indistinguishable in (order,size),
  though not necessarily isomorphic.
- G has **at most one** cut vertex ⇒ if 2-connectivity fails at all, it
  fails at a single unique articulation point with the block structure
  "two blocks glued at one vertex" is *not* forced beyond that single
  split — S5 says nothing about whether each lobe Aᵢ∖{...} is itself
  2-connected; it could in principle contain further bridgeless-but-not-
  biconnected structure only via *that same single* v (a second cut vertex
  anywhere, even nested inside one lobe, is exactly excluded by Step 6,
  since the argument only used that v,w are both cut vertices of G, with
  no assumption on where w sits beyond w≠v).
- Together with S4, **G is either 2-connected, or is exactly two blocks of
  equal order/size sharing a single degree-4 cut vertex.** This is strictly
  more refined than the "2-connected" claim recorded as CONJECTURAL/
  attempted in B2 above — B2's stalled suppression argument is superseded:
  the *doubling* construction (not suppression) is what carries S4/S5
  through, and it needs no length-shifting reduction at all.
- **Provenance note (literature.md L17):** the split-at-a-cut-vertex-and-
  recombine-to-violate-minimality *technique* is classical in critical-
  graph theory — closest named analog is Dirac's theorem that k-chromatic-
  critical graphs have no cut vertex (G. A. Dirac, Fund. Math. 40 (1953),
  42–55) — but no source found applies it to Erdős–Gyárfás, and Dirac's
  version lacks S5's equal-order/equal-edge-count lobe refinement (which
  needs lexicographic (|V|,|E|) minimality, not |V|-only). Cite Dirac 1953
  as the method's origin if S4/S5 are written up formally.

## Search-space lemmas (small-order 4-or-8 dichotomy)

### S1. Excess identity  [PROVED — elementary]
For a graph with n vertices, m edges, Σ_v deg(v)=2m, so **Σ_v(deg(v)−3) = 2m−3n**.
A δ≥3 graph therefore has m ≥ ⌈3n/2⌉, with equality iff it is 3-regular (n even)
or has exactly one degree-4 vertex and the rest degree 3 (n odd). The "excess"
2m−3n bounds the total surplus degree, giving a finite list of degree sequences at
each (n,m): excess 0 ⇒ cubic; excess 1 ⇒ 4,3^{n−1}; excess 2 ⇒ {5,3^{n−1}} or
{4²,3^{n−2}}; excess 3 ⇒ {6,3^{n−1}}, {5,4,3^{n−2}}, or {4³,3^{n−3}}.

### S2. Extremal-layer reduction  [PROVED, given McKay's ex(n)]
A δ≥3 {C4,C8}-free graph on n vertices has ⌈3n/2⌉ ≤ m ≤ ex(n;{C4,C8}). Hence:
- ex(n) < ⌈3n/2⌉ ⇒ none exists (n≤17, done).
- ex(n) = ⌈3n/2⌉ ⇒ any such graph is *extremal*; check the extremal file's min
  degree (n=18,19: all δ=2 ⇒ none exists).
- ex(n) > ⌈3n/2⌉ ⇒ it lies in edge layers [⌈3n/2⌉, ex(n)]; the top layer m=ex is
  exactly the extremal file (check its min degree), lower layers need generation.
Corollary: since all n=20..23 extremal graphs have δ=2, only the one-below layer
(m = ⌈3n/2⌉ for n=20,22; m = ⌈3n/2⌉ for n=21,23) remains — 4 near-cubic cases.
See literature L15/L15b, plan P1.

### S3. Connectedness is safe for the n≤23 search  [PROVED, given the n≤19 theorem]
When searching n=20..23, restrict to connected graphs. If a δ≥3 {C4,C8}-free
counterexample were disconnected, each component would be a δ≥3 {C4,C8}-free graph
on <20 ≤ 19 vertices — impossible by the n≤19 theorem (P4/L15). So a
disconnected counterexample cannot exist; `geng -c` loses nothing. ∎

## Additive / theta lemmas (Track C) — under construction
Notation: a **theta** Θ(a,b,c) = two vertices joined by three internally
disjoint paths of edge-lengths a,b,c (a,b,c≥1, at most one equal to 1). Its three
cycles have lengths a+b, a+c, b+c.

### C1 (target). "Forced power-of-two sum."
Seek the strongest true statement of the form: *any theta (or path system)
that δ≥3 forces must have two path-lengths summing to an element of F.* Status:
under computational investigation (experiments E3). Not yet a lemma.

### C1a (elementary necessary condition on a single theta) [PROVED]
Θ(a,b,c) avoids all of F in its three 2-cycles iff none of a+b, a+c, b+c ∈ F.
This alone does not force an F-sum (a=b=c=1 → sums 2,2,2 ∉ F; a=b=c=3 → 6,6,6).
So a single theta is NOT enough; forcing (if any) needs **many** paths.

### C2 (lower bound: a single dyadic interval is power-of-two-sum-free) [PROVED — valid half]
For every k, the interval S_k = {2^{k-1}+1, …, 2^k} (size 2^{k-1}) has **no two
distinct elements summing to a power of two**. *Proof.* Distinct a,b∈S_k give
a+b ∈ (2^k, 2^{k+1}); the only power of two in that open-closed range is 2^{k+1},
and the largest distinct sum is (2^k−1)+2^k = 2^{k+1}−1 < 2^{k+1}. ∎
Consequently the maximum size of a power-of-two-sum-free subset of {1,…,N} is
**≥ ⌊N/2⌋**. This lower bound is correct and is all that C3 below actually needs.

### C2-upper (the claimed sharp formula) [DISPROVED — 2026-07-24]
The previously asserted matching upper bound "α(H_N)=⌊N/2⌋+1 exactly, density
exactly 1/2" is **FALSE**. It was inferred from experiment E3, which sampled
**only** N=2^k (8,16,…,512) — the one subsequence where α does equal N/2+1 — and
was never tested at a non-power-of-two. Exact recomputation (E3′, exact MIS over
N=1..32) gives, for the **distinct-summands** model:
`α = 1,2,2,3,4,4,4,5,6,7,7,7,8,8,8,9,10,11,11,12,13,13,13,13,14,15,15,15,16,16,16,17`.
Explicit refutation: **{1,2,4,5,8,9,10} ⊆ {1,…,10}** has size **7** with no two
distinct elements summing to a power of two, vs. the formula's ⌊10/2⌋+1 = 6.
The formula holds **only** at N=2^k. The true extremal density is **> 1/2** for
most N (e.g. 7/10, 11/18, 13/21) and its exact asymptotics are **NOT established
here** — to be looked up in OEIS from the reliable sequence above (OEIS was
Cloudflare-blocked to automated fetch on 2026-07-24; do it interactively).

**Modeling ambiguity (must be resolved before any graph inference):** a book/theta
can contain two paths of the *same* length ℓ, giving a cycle of length 2ℓ, which
is forbidden iff ℓ is itself a power of two. So the additive object is a
**multiset**, not a set, and the sum operation includes ℓ+ℓ. The old example
"{32,…,64}" is invalid under repeats (32+32=64 is forbidden; and 32=2^5 is itself
a power of two so cannot be repeated). The clean sum-free interval is
{2^{k-1}+1,…,2^k}, which contains no power of two below its endpoint. Distinct-
length vs. equal-length pair sums are genuinely different constraints and must be
tracked separately (see experiments E3′).

### C3 (single-scale distinct-length pairwise sums are insufficient) [PROVED — narrowed]
The one thing the *valid* half of C2 supports: a book of internally-disjoint u–v
paths with **distinct** lengths all inside one dyadic interval (2^{k-1}, 2^k]
realizes **no** power-of-two cycle among its two-path cycles. Hence *this
particular sub-mechanism* — distinct pairwise sums confined to a single bounded
scale — cannot force the conclusion, no matter how many paths.
**What this does NOT establish (correction of prior overclaim):**
- It does **not** show "the naive theta approach is dead" in general, nor that
  "only a multiscale additive route remains." Those are **RETRACTED**.
- Graph structure may still force multiplicities, equal-length pairs (self-sums),
  parity/residue patterns, overlapping thetas, length *differences*, or ≥3-path
  cycles — none of which this narrow single-scale distinct-sum analysis touches.
The honest residual statement: single-scale distinct-length pairwise forcing is
insufficient; whether δ≥3 forces a *multi-scale* or *repeated-length* path system
is open (Track C, still live). [Track C sub-obstruction — kept, scope corrected.]

## One-pole gadget lemmas (redirection 2026-07-25) — see one_pole.md for full detail
O1–O3 [PROVED, novelty unchecked]: a master-minimal one-pole graph
(root r deg 2, else δ≥3, F-clean) has no bridge, H−r is connected, and H
is **fully 2-connected** (no cut vertex at all) — strictly stronger than
S5 could establish for G itself, because peeling a piece off a one-pole
graph always shrinks it (no "same order" loophole the way doubling equal
cut-vertex lobes of G does). O4 [OPEN, precise target]: whether H−r
contains 2 internally-disjoint root-neighbor paths, which would force a
genuine theta/book structure and connect directly to Track C's additive
lemmas on a real (not hypothetical) object. See one_pole.md for full
proofs and the cross-link back to S5 (a cut vertex's lobe in G is itself a
one-pole graph).

## Z3 lift elimination, algebraically compressed (2026-07-26 pass) — see z3_lifts.md Part III for full detail

Every one of the 1,545,746 C8-survivor voltage assignments across the 4
certified order-24 bases is eliminated by a **Type-1** projection (a
simple base 16-cycle with trivial holonomy) -- exhaustively verified, 0
instances of the other 3 projection types. Stronger: the union of
simple-C16 hyperplanes covers the **entire** nonzero `F3^13` space per
base (not just C8-survivors), reducible to a 24-27-vector covering subset
per base (down from 207-330 distinct homology vectors), independently
verified against real lift reconstruction (300 random cross-checks per
base, 0 disagreements). `verifier/z3_certificate.py`,
`verifier/z3_min_cover.py`, `verifier/z3_standalone_verifier.py`.

## Exact Z5-lift completion (2026-07-27 pass) — see z3_lifts.md Part IV (completed exactly) for full detail

**Replaces every sampled Z5 conclusion with an exact one.** Full exact
(non-sampled) scan of all `4x1,220,703,124=4,882,812,496` nonzero cyclic
Z5-voltage assignments across the 4 certified order-24 bases against the
mod-5 simple-C16 hyperplanes: base 1 has EXACT 100% coverage (0
uncovered -- a genuine UNSAT/hyperplane-cover result, certified by the
full 315-vector hyperplane list; a candidate 48-vector *compression* of
this, found via the same sample-then-verify method that worked for Z3,
FAILED exact verification with 21,156 exceptions -- caught and corrected,
not silently patched, the same sampling-trap shape already caught once
this session); bases 0, 2, 3 have exactly 444, 72, 48 uncovered assignments
respectively (corrects the previous phase's sampled "~0 for bases
0,1,3" claim, which undershot -- an exact scan of just the first 1M
sequential indices for base 0 alone already found 124 uncovered).
Proved the F5^x scalar-multiplication isomorphism (fibre relabelling
(v,i)->(v,lambda*i)) and confirmed every uncovered count is divisible by
4 with 0 orbit-closure exceptions across 60 sampled orbits. Every one of
the 564 uncovered assignments was independently lift-constructed and
exactly tested (staged C4/C8/C16/C32/C64): 148 killed at C8, 400 at C16
(all genuine non-simple Type-3 projections, 0 anomalies after fixing a
real vertex-projection bug caught during testing), 16 at C32, **0
survivors**. Independent NetworkX recheck agrees on all 564.
**Conclusion (exact): no connected cyclic Z5-lift of these four bases is
an Erdos-Gyarfas counterexample.**

## Next voltage-cover search selection (2026-07-26 pass) — see z3_lifts.md Part IV for full detail

**IV.A (Z5 lifts of the same 4 bases) SELECTED over IV.B (Z3 lifts of
order-26 bases).** IV.B fails the feasibility gate directly: order-22
C4-free cubic generation did not complete in 400s; extrapolated order-26
raw generation alone needs ~6 days (geometric-mean growth x11.58/count,
x18.07/time per +2 vertices, calibrated at n=16,18,20). IV.A evidence
(2,000,000 Monte Carlo samples/base + 1,000 real 120-vertex lift
samples/base): 3 of 4 bases show exact 100% simple-C16 hyperplane
coverage over `F5^13`; base 2 shows a genuine, measurable ~5x10^-7
uncovered fraction (a real qualitative difference from Z3's exact 100%
coverage), with a confirmed real-lift witness (no C4/C8, genuine C16 via
a non-simple projection). 0 counterexample candidates found. A larger
50M-sample confirmatory run did not complete in budget; not used in any
conclusion.

## q(G)>=4 for genuine minimal counterexamples (2026-07-27 defect-three pass) — see defect_three.md for full detail

**Theorem [PROVED IN WORKSPACE, novelty supported by search]:** no
minimal Erdos-Gyarfas counterexample has `q(G)=3`. Since `q=3` is odd,
the separator-defect mapping (even `q` for any cut-vertex counterexample)
forces `G` 2-connected. `h<=q=3` and the leaf-count identity/strong
inequality pin the case table to exactly 6 `(h,c1,c3)` rows over
`h in {0,1,2,3}`, all eliminated:
- `h=0` (n=10): 4-or-8 dichotomy (n<=19, P4/L15) + independent geng
  certificate, 19/19 cubic graphs on 10 vertices confirmed.
- `h=1` (c1=0,c3=6): branch-incidence + chain-length bounds force
  n<=13, then the P13-free theorem (L7) applies exactly within its
  hypotheses; independently verified via exhaustive geng at n=11,12,13
  filtered to the forced signature (2317 graphs, 0 escapes).
- `h=2`, (c1,c3)=(0,2): Part V's elimination of pure-cycle F-components
  at h=2 forces kappa(F)=1 directly, pinning the kernel to a theta or
  dumbbell shape (elementary degree parity); the all-subdivided theta
  falls to a 2-line pigeonhole argument, everything else (one-direct-
  edge theta, every dumbbell) to exhaustive reconstruction (6,804+304
  realizations, 0 survivors).
- `h=2`, (c1,c3)=(1,3): the kappa=2 split reduces algebraically to the
  already-eliminated (0,2) kernel (a lollipop component's cyclomatic
  number is forced to 1 for any internal length); the kappa=1 split's
  kernel topology is enumerated exhaustively (a general stub-matching
  multigraph enumerator, not assumed) into exactly 3 non-isomorphic
  shapes, each eliminated by backtracking reconstruction.
- `h=3`, (c1,c3)=(2,0): a new H-degree-feasibility argument (every
  H-vertex needs G-degree>=4, forcing the lone path component's
  internal-C2 count to be exactly 8, the same value the colored-path
  lemma already caps it at) combined with an exhaustive t=8 sweep (0
  valid colourings) eliminates this row; a 144-pair pure-cycle-
  compatibility check confirms no Part V pure cycle can rescue it.
- `h=3`, (c1,c3)=(3,1): the kappa=1 split's kernel is uniquely forced
  (elementary tree structure) to be the star K_{1,3}; kappa=2 splits
  into a lollipop (cyclomatic number 1, same identity as above) plus a
  bare path. Backtracking search over both topologies (41,958+
  realizations) finds 0 survivors, confirmed via a hard C4/C8
  violation in every case (never H-degree infeasibility, so no
  pure-cycle addition could rescue any configuration).

New machinery introduced this phase and reused throughout: the bounded
branching-kernel lemma (kernel vertex count bounded by q after
suppressing degree-2 chains); the colored degree-2 path lemma (exact
bounds t<=2,5,8 for h=1,2,3, proved by two independent implementations
-- a prefix-closed direct-construction search and a minimal finite-
state automaton with a proved-finite saturating-counter state space);
the colored cyclic-word classification (h=1,2: no valid pure-cycle
component; h=3: exactly s=3,5, closed via a corollary of the linear
lemma); and a general stub-matching topological-kernel enumerator
(exhaustively lists every multigraph realizing a prescribed degree
sequence up to isomorphism, validated by rediscovering the theta/
dumbbell pair independently before being trusted on new cases).

**Conclusion: `q(G)>=4`, hence `|E(G)|<=2|V(G)|-6`** -- strictly
improves the previous `q(G)>=3` result.

## q(G)>=3 for genuine minimal counterexamples (2026-07-27 pass) — see defect.md Leaf-compression Part III for full detail

**Theorem [PROVED IN WORKSPACE, novelty supported by search]:** no
minimal Erdos-Gyarfas counterexample has `q(G)=2`. `h<=q=2` restricts to
`h in {0,1,2}`, all three eliminated:
- `h=0`: forces `n=8`; cites `ex(8;{C4,C8})=11 < 12` (McKay data, P4/L15,
  already established) to force C4 or C8, cross-checked by exhaustive
  geng (5 graphs, all confirmed).
- `h=1`: forces `c3=4`; a genuine CASE SPLIT (not one mechanism) --
  either some C3 vertex has >=2 C2-neighbours (direct C4 via
  z-a-u-b-z) or every C3 vertex has <=1 (hence F[C3] has min-degree>=2
  on 4 vertices, forcing C4 via an exhaustively-checked 4-vertex lemma).
  Verified on 384 property-(2) graphs, n=8..12: 0 in neither branch.
- `h=2`: `c1=c3<=1` from the leaf-graph inequality. `c1=c3=0`: F is a
  union of cycles; C4-freeness forces a period-4 a/b coloring, forcing
  cycle length divisible by 4 (else forced C4 immediately); L=4,8 give
  the F-cycle itself as the forbidden cycle; L>=12 gives an explicit C8
  via 2 arcs + a,b. `c1=c3=1`: handshake-lemma parity forces the unique
  leaf x and unique C3-vertex y into the same F-component, which is a
  cycle+pendant-path (lollipop, independently confirmed the ONLY such
  shape via atlas enumeration); 3 sub-cases on pendant length t=1,2,>=3
  each force a C4 (all exhaustively coloring-checked, 0 escapes across
  35 configurations).

**Conclusion: `q(G)>=3`, hence `|E(G)|<=2|V(G)|-5`** -- strictly
improves the previous q(G)>=2 result. **Errata:** caught and fixed an
arithmetic error in the previous phase's general weighted-incidence
formula (coefficient of t was t, corrected to 2t) while deriving this
result -- see defect.md's I.3 correction note.

## q(G)>=2 for genuine minimal counterexamples (2026-07-27 pass) — see defect.md Leaf-compression Part II for full detail

**Theorem [PROVED IN WORKSPACE, novelty supported by search]:** no
lexicographically minimal Erdos-Gyarfas counterexample has `q(G)=1`.
Narrower than the previous phase's abstract D1 (which used property (2)
alone, not genuine F-cleanness) -- D1 itself remains open, not
re-attempted here. `h>=2` excluded immediately by `h<=q`. `h=0` forces
`n=6`; both connected cubic 6-vertex graphs (via the 2-regular
complement: C6 or 2*C3) contain a C4, cross-checked by exhaustive geng
(exactly 2 graphs). `h=1` forces `c1=0` (needs 2 distinct H-neighbours,
impossible with |H|=1) hence `c3=2` (from the leaf-count identity); the
two C3 vertices force a C4 through the unique H-vertex via
`z-a-u-b-z`. Exhaustively verified on 74 h=1,q=1 property-(2) graphs
(n=7..12, same range as the prior D1 search), 0 algebra/mechanism
failures. **Conclusion: `q(G)>=2`, hence `|E(G)|<=2|V(G)|-4`** --
strictly improves G2's `q(G)>=1`/`m<=2n-3`.

## Derived leaf graph L(G) (2026-07-27 pass) — see defect.md Leaf-compression Part I for full detail

### I.1 (new). Leaf-count identity [PROVED, pure algebra]
`c1 = c3 + 4h - 2q - 4`, by substituting `beta(F)=q+2-2h+kappa` into
`c1=c3+2*kappa-2*beta(F)` (kappa cancels exactly). 0 failures across
1,457 checks.

### I.2 (new). Derived leaf graph L(G) [PROVED / MECHANICALLY VERIFIED]
Multigraph on H: every `x in C1` (exactly 2 distinct H-neighbours `a_x,
b_x`) contributes edge `a_x b_x` labelled `x`. **L1** (simplicity): a
label collision would give a C4 in G, impossible for F-clean G. **L2**
(cycle lifting): an r-cycle of L lifts to a genuine simple 2r-cycle of G
(every sub-claim -- distinct vertices/labels, no overlap, edge existence
-- checked explicitly). **L3**: L has no power-of-two cycle (else G
would). **L4**: L is 2-degenerate (else a smaller counterexample would
exist) -- a minimality argument, not empirically testable, same status
as S4/S5/O1/O3/G2. Edge bound `c1<=2h-3` for `h>=2`; `h=0,1` handled
directly (c1=0 forced by |H| too small, not by degeneracy counting).
0 mismatches: L1 (0 collisions across 1,443 synthetic C4-free instances,
matching the C4-freeness precondition exactly), L2 (0 failures across
833 lifted-cycle reconstructions). **No genuine small EG counterexample
fixture exists to test L1/L2 "for real"** -- all 12 order<=7
inclusion-minimal-delta>=3 atlas fixtures already contain a C4.

### I.3 (new). Defect/high-degree inequality [PROVED, scope precise]
Strong form `c3+2h<=2q+1` holds **only for h>=2** (genuinely fails at
h=0, checked directly -- not a near-miss). Weak corollary `h<=q` holds
for ALL h>=0, but via two different mechanisms: trivial from the
already-proved q(G)>=1 (G2) at h in {0,1}, genuine leaf-graph consequence
at h>=2.

## Cubic-core decomposition (2026-07-26 pass) — see defect.md Part I for full detail

### I.1a-c. Cross-count/internal-edge/beta(F) identities [PROVED, pure algebra]
`e(C,H)=n+3h-4-2q`, `|E(F)|=n-3h+2+q`, and boxed
`beta(F)=q+2-2h+kappa`, from `H` independent (M1) + every `C`-vertex having
degree exactly 3. No minimality hypothesis needed beyond M1's independence.

### I.1d. C1/C2/C3 degree partition [PROVED, needs M2]
`1<=d_F(v)<=3` for `v in C` (from M2: every `C`-vertex has a `C`-neighbour).
`2c1+c2=e(C,H)`; `c1=c3+2*kappa-2*beta(F)`.

### I.2. Component-incidence quotient Q [PROVED, with a correction]
`G` connected => `Q` connected (contraction argument, unconditional).
**Corrected statement:** "G 2-/3-connected => every component-node has
>=2/3 distinct H-neighbours" needs `kappa(F)>=2` explicitly, not merely
`H!=empty` as informally stated in the task -- `kappa(F)=1` is a genuine
exception even when `H` is nonempty (the unique component's distinct-
neighbour count is exactly `h`, which 2-/3-connectivity does not bound
further). A "cut" of `Q` transfers to a genuine cut of `G` exactly when
every node involved is either an `H`-vertex or a singleton component.

### I.3. Weighted-incidence cycle formula [PROVED, corrected 2026-07-27]
Single-H base case: `|P|+2 notin F` for any F-path P between 2 distinct
C-neighbours of one H-vertex. General alternating cycle through `t`
distinct H-vertices with `t` pairwise-disjoint connecting F-paths:
`2t + sum|P_i| notin F` (corrected coefficient of `t`; the original
`t + sum|P_i|` was an arithmetic error, caught while reusing the formula
in the leaf-compression phase's Part III.3.a -- see defect.md's inline
correction note for the vertex-count re-derivation and t=1/t=2 checks).

**Computational validation (`verifier/cubic_core.py`):** 0 failures across
8,171 checks over 3 independent populations (14 atlas graphs, 12
inclusion-minimal-delta>=3 fixtures, 8,145 synthetic constructions) —
`manifests/cubic_core_manifest.json`.

## Defect-one theorem D1 (2026-07-26 pass) — see defect.md Part II for full detail

D1: does every graph with delta>=3, property(2) (Carr Lemma 0.1), and
`m=2n-3` contain a C4 or C8? **Verdict: outcome (4) -- one precisely
formulated open configuration**, not proved, not refuted:
- `h=0` case: [PROVED, forced, exhaustive] `q=1,h=0` forces `n=6` exactly;
  both connected cubic 6-vertex graphs (K_{3,3}, triangular prism) satisfy
  property(2) automatically and contain C4.
- D1C ("exists nonedge ab with G+ab degree-3-critical"): [DISPROVED],
  fails starting n=9 (3 witnesses, g6 `HCOfeW{`/`HCOfbY[`/`HCOethk`), 172
  further failures by n=12. Closes the "reduce to EFGS via 1 edge" route.
- Exhaustive computational search n=6..12 (1,128 property-(2) graphs, two
  independently cross-validated generation routes): 0 counterexamples to
  D1's conclusion. n=13 (17.4M raw graphs) attempted, did not complete.
- Open configuration: h>=1 case of D1 (h=0 separately closed); the
  `beta(F)=0` tight-forest case is flagged as the most promising entry
  point (parallel to Narins-Pokrovskiy-Szabo's 1-3-tree construction,
  literature.md L20) but NOT isolated as harder by any evidence gathered.
- **q(G)>=2 / |E(G)|<=2|V(G)|-4 is NOT claimed** (D1 not proved); G2's
  q(G)>=1 remains the current global bound.

### II.0. Fast equivalent of property (2) [PROVED]
property(2) <=> [B3: every edge has a degree-3 endpoint] AND [for every v,
G-v is 2-degenerate]. Reduces an O(2^n) check to O(n(n+m)); 0 mismatches
against the literal exponential check over 1,865 cross-validation graphs.

## Ordering-defect lemmas (redirection 2026-07-25) — see defect.md for full detail

### D-def, D-identity  [PROVED, pure algebra]
D := 2n−2−m for a graph with n vertices, m edges. For any vertex ordering
with forward degrees d⁺(xᵢ), D = (3−d⁺(x₁)) + Σ_{i=2}^{n-2}(2−d⁺(xᵢ)) +
(1−d⁺(x_{n-1})), and Σ_v(deg(v)−3) = n−4−2D. Both are unconditional
algebraic identities (no δ≥3 hypothesis needed for the identities
themselves). See defect.md §2, §3a.

### D-upper [PROVED from S1]
D ≤ ⌊n/2⌋−2 for any δ≥3 graph, with equality iff regular (cubic, by M4).
Direct consequence of S1 (m≥⌈3n/2⌉). See defect.md §3b.

### D-lower [OPEN — gap]
D ≥ 2 (equivalently m ≤ 2n−4) is **not established** here. The natural
route (G−x₁ is 2-degenerate for a degree-3 vertex x₁) is not implied by
B0–B4/M1–M4/S4/S5, and fails computationally for a growing fraction of
C4-free δ≥3 graphs (6.8% at n=10–13, 16.0% at n=14–15 have NO working x₁ —
experiments.md E7). See defect.md §2b, §5.

### Central-target [DISPROVED — 2026-07-25]
"n ≤ 2D+3 for every power-of-two-cycle-free minimal graph," read literally
with D:=2n−2−m, is **false for every δ≥3 graph** (not conditional on
counterexample existence): equivalent to m≤(3n−1)/2, contradicted
unconditionally by S1. Cubic graphs give the exact gap n−(2D+3)=1 always.
See defect.md §4 for the full proof and the methodological diagnosis (D as
a pure (n,m)-function cannot bound n; any correct bound needs the
cycle-avoidance structure, not edge-counting alone).

### V1 (vine charging lemma)  [DISPROVED — 2026-07-25]
"A graph with D defects has ≤ D missing dyadic cycle lengths among
{4,8,…,≤n}." False in general (C4-freeness forces ≥1 missing length
independent of D, and D=0 is achievable) and concretely: n=13, g6
`L?AB?vOLDPHa\`o`, D=0, missing={4}; 629/98,066 C4-free δ≥3 graphs
(n=10–15) violate it. See defect.md §6, experiments.md E8.

## Cross-checks
- M1, M3, M4 re-derivations were checked against Carr 2026's abstract statements
  and agree. The elementary double-counting in M3 is verifiable on any graph;
  see experiments E-struct (planned) for a computational spot-check of B3/M3 on
  edge-minimal C4∧C8-free graphs (the relaxed property for which B3 also holds).
