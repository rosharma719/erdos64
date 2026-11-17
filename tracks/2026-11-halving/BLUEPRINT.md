# Blueprint: Conjecture T and the cubic case

The dependency graph for the current programme. **This file is the single
source of truth for node statuses.** Every bundle sent to the second model
carries a copy, stamped with the commit it reflects. Workflow rules:
`WORKFLOW.md`.

**Stamp:** the commit that last changed this file (`git log -1 -- BLUEPRINT.md`).

## Status vocabulary

| Status | Meaning |
|---|---|
| `CANDIDATE` | Stated, not tested |
| `TESTED` | Survived a falsification check; the tested range is stated |
| `PROVED-DRAFT` | A complete hand proof by one author |
| `REVIEWED` | Checked by the agent that did not produce it; central nodes also need the user's sign-off |
| `FORMALIZED` | Machine-checked (none yet) |
| `COMPUTED` | One implementation |
| `CERTIFIED` | Two independent checkers agree, with manifests (exit codes, counts, stream checksums) |
| `KNOWN` | Published; cited, not re-verified here |
| `OPEN` | Not attempted or not finished |
| `OBSTRUCTED` | Attempted; the exact failing step is recorded |
| `REFUTED` | False, with a witness |

Only `REVIEWED`, `CERTIFIED` and `KNOWN` nodes may be cited without marking
the citing result conditional.

## Definitions

- **Clean k-pole:** a connected simple graph with exactly `k` vertices of
  degree 2, all others of degree 3, and no cycle whose length is a power of
  two (4, 8, 16, …).
- **Conjecture T:** the only clean 3-poles are the triangle, uniform H7, skew
  H7 and H15 (3, 7, 7, 15 vertices). Graph6: `FCptO`, `FCZTO`,
  `N?AA@AODAOP_KGGoGH?`.
- **WRP:** for every cyclically 4-edge-connected cubic `B ≠ K4`, root `r`,
  and labelling of `V(B) − r` by the letters {identity, triangle, uniform H7,
  skew H7, H15} with port orientations, some cycle of `B − r` has a lifted
  window containing a power of two.
- **Conjecture T\*:** no clean 1-pole, no clean 2-pole, and every clean
  3-pole is in T's list.

## Nodes

### Goals

| ID | Statement | Type | Depends on | Status | Evidence |
|---|---|---|---|---|---|
| G0 | Erdős–Gyárfás for all graphs of min degree ≥ 3 | AND | G1, G2 | OPEN | — |
| G1 | Erdős–Gyárfás for all cubic graphs | AND | I1, T1, L0 | OPEN | — |
| G2 | Extension from cubic to vertices of degree ≥ 4 | — | — | OPEN, not started | — |
| L0 | No counterexample of order ≤ 40; no cubic one of order ≤ 48 | — | — | KNOWN | Ducoffe–Dumitru, arXiv:2609.28594, Thm 5.1 |
| I1 | T ⇒ G1 (delete a spanning-tree leaf; use L0) | — | L0 | REVIEWED (author Claude; checked by ChatGPT and the user) | `three_port_classification.md` |
| T1 | Conjecture T | OR | R1 or R2 | OPEN | E1, E2, E3 |

### Routes to T

| ID | Statement | Type | Depends on | Status | Evidence |
|---|---|---|---|---|---|
| R1 | Decomposition route: WRP ⇒ T* ⇒ T | — | J1, W1 | **Reduced to W1**: every other node on this route is proved | `joint_minimality.md` |
| R2 | A direct obstruction to growth of clean 3-poles | — | — | OPEN, not stated | — |
| T* | T*: no clean 1-pole, no clean 2-pole, clean 3-poles = T's list | AND | — | OPEN | E1, E4 |
| I2 | T*(ii) alone ⇒ G1 (delete an edge on a cycle) | — | L0 | PROVED-DRAFT (Claude) | `joint_minimality.md` |
| J1 | WRP ⇒ T* (joint minimal counterexample over 1-, 2-, 3-poles) | AND | D1a, K2, W1 | PROVED-DRAFT (Claude); **awaiting ChatGPT's review** | `joint_minimality.md` |

### Tower theorem

| ID | Statement | Type | Depends on | Status | Evidence |
|---|---|---|---|---|---|
| K1 | Clean triangle-built networks are exactly I, T, S, H (orders 1, 3, 7, 15) | — | K1a, K1b | **REVIEWED** (author ChatGPT; checked by Claude; signed off by the user, 16 Nov) | `tower_theorem.md`, `pass12/REVIEW.md` |
| K1a | Interval lemma, for clean triangle-built pieces | — | — | PROVED-DRAFT inside K1; **false for unclean pieces** (witness Δ(I,I,T)) | `tower_theorem.md` |
| K1b | Hamiltonian span: longest port-pair path has length N − 1, for all triangle-built pieces | — | — | REVIEWED | `tower_theorem.md` |
| K1c | Short-path growth bound | — | — | Not needed (superseded by the finite table) | — |
| K2 | K4 root with letters I, T, S, U, H: clean only for III, ITT, ISS | — | K1 | REVIEWED (author ChatGPT; table recomputed by Claude) | `tower_theorem.md` |

### Decomposition lemma

| ID | Statement | Type | Depends on | Status | Evidence |
|---|---|---|---|---|---|
| D1 | A smallest counterexample to T* is a prime cubic base `B ≠ K4` minus a root, with letters substituted | AND | D1a–D1d | PROVED-DRAFT via J1 | `joint_minimality.md` |
| D1a | Case: 3-edge-connected caps (cyclic 3-cut contraction; `B ≠ K4`) | — | X1, K2 | **REVIEWED** (author ChatGPT; checked by Claude) | `decomposition_lemma.md`, Part A |
| D1b | Case: 2-edge cuts | — | J1 | Closed by joint minimality (PROVED-DRAFT, Claude) | `joint_minimality.md`, Step 3 |
| D1c | Case: bridges | — | J1 | Closed by joint minimality (PROVED-DRAFT, Claude). ChatGPT's Part C also gives ≥ 25 vertices independently (REVIEWED) | `joint_minimality.md`, `decomposition_lemma.md` Part C |
| D1d | Lifting rule for cycles through substituted letters | — | X1 | REVIEWED (Part A, "exact lifting") | `decomposition_lemma.md` |
| X1 | Exact length transfer across cyclic 3-edge cuts | — | — | PROVED-DRAFT (pass IV) | `three_cut_prime_transfer.md` |
| X2 | Exact length transfer across general edge cuts | — | — | PROVED-DRAFT (pass X) | `boundary_linkage_composition.md` |

### WRP

| ID | Statement | Type | Depends on | Status | Evidence |
|---|---|---|---|---|---|
| W1 | WRP (letters I, T, S, U, H; statement in `decomposition_lemma.md` Part D) | AND | W1a, W1b | OPEN; **the only open node on route R1** | — |
| W1a | WRP when `3(n_I + n_T) ≤ n_H7skew + 3 n_H7unif + 17 n_H15` | — | — | PROVED-DRAFT (cycle-space averaging) | `cycle_space_obstruction.md` |
| W1b | WRP for identity/triangle-heavy labellings (doubling-chain lemma) | — | W1c | OPEN; main conceptual gap | brief, Step 5 |
| W1c | Root-robust prime conjecture (identity letters only) | — | — | TESTED: primes ≤ 12 vertices; Hamiltonian ≤ 16 | `prime_pole_obstructions.md`, `root_orbit_switching.md` |

### Evidence for T

| ID | Statement | Status | Evidence |
|---|---|---|---|
| E1 | Clean 3-poles on ≤ 21 vertices are exactly T's four | CERTIFIED for checkers (two independent), single generator (nauty `geng`); 18,580,327 graphs at order 21 | `three_pole_census_manifest.md`, `census/` |
| E2 | No clean 3-pole on 5 vertices | REVIEWED (author ChatGPT; checked by Claude) | `audits/three_pole_research_handoff.md` |
| E3 | Pass VI Hamiltonian survivors delete to T's poles (identification, not uniqueness) | COMPUTED | `scripts/check_three_pole_isomorphisms.py` |
| E4 | No clean 2-pole on ≤ 20 vertices | CERTIFIED for checkers, single generator | `three_pole_census_manifest.md`, `census/` |
| E6 | Clean 4-poles on ≤ 20 vertices: 48 in all (orders 6–18, none at 20). Every bridged one is two T-list poles joined by a bridge; 36 are bridgeless, all with vertex connectivity 2 | CERTIFIED for checkers, single generator; classification COMPUTED | `four_pole_census.md`, `scripts/classify_four_poles.py` |
| E5 | Independent generator (not nauty) agrees through 15 vertices | PARTIAL: ChatGPT's own generator covers 2-poles on 4 and 6 vertices; its 3-pole check (orders 3–11) uses saved cubic catalogs, not its own generator | `pass12/verification_manifest.md` |

### Bounded-defect programme (pass XIII)

| ID | Statement | Status | Evidence |
|---|---|---|---|
| F(k) | Clean k-poles have bounded order N(k) | OPEN (k ≥ 3); F(1), F(2) are T\*(i),(ii) | `pass13/structural_analytic_pivot.md` |
| F1 | F(k+1) ⇒ F(k) (bridge gluing) | REVIEWED (author ChatGPT; checked by Claude) | `pass13/REVIEW.md` |
| F2 | N(k) ≥ 15(k − 2) (bridge-trees of H15) | REVIEWED (author ChatGPT; checked by Claude) | `pass13/REVIEW.md` |
| F_lin | Every connected clean subcubic graph has \|V\| ≤ 15(δ − 2), δ = deficiency; equivalently m ≤ (22n − 15)/15 | CANDIDATE (author Claude). Implies cubic EG, T\*(i),(ii), the size part of T, and N(k) = 15(k − 2). Holds on ≤ 21 vertices, conditional on E1, E4 and J1 Step 1 | `linear_defect_bound.md` |
| S1 | Proper-shore isoperimetry | Reduced to F_lin (corollary: c ≥ \|S\|/15 + 2 − δ_G(S)) | `linear_defect_bound.md` |
| A1 | Dyadic cycle in min-degree-3 expanders with few defects | OPEN; now targeted at defect density ≤ 1/15 | `pass13/structural_analytic_pivot.md`, `linear_defect_bound.md` |
| X3 | F_lin's minimal violators are expanders | OPEN. The gluing argument forces only 2-edge-connectivity; the extremal graphs (bridge-trees) are not expanders, so expansion would need a new idea | `linear_defect_bound.md` |

### Novelty

| ID | Statement | Status |
|---|---|---|
| N1 | Garcia (arXiv:2609.04686, Prop. 6.2) already classifies three-port gadgets free of C4 and C8 on 5, 7, 9 vertices (exactly H7 and H7′ at 7), and on 11 only with attachments pairwise at distance ≥ 3. E1 beyond 9 vertices, uniqueness of H15, Conjecture T and I1 were not found in the literature | Search of 16 Nov 2026 (arXiv full text of Garcia; web search); not exhaustive |
| N2 | Garcia conjectures that a two-attachment gadget with no internal power-of-two cycle has max S ≥ 2 min S. E4 says no such gadget (in our 2-pole sense) exists on ≤ 20 vertices | Relation to Garcia's definition of two-attachment gadget not yet checked |

## Highest-value open nodes

1. **W1 (WRP)**: now the only open step between the census evidence and
   Conjecture T. Split as W1a (gadget-heavy, proved above a threshold) and W1b
   (identity/triangle-heavy, the doubling-chain lemma).
2. **F_lin at δ = 4** (N(4) = 30): a structural proof for the bridgeless,
   2-connected 4-poles; then a discharging attack on the general density form.
3. **J1 review**: a *fresh* ChatGPT chat's blind re-derivation (the pass XIII
   audit was not blind) of `joint_minimality.md`.
4. **E1 at 23 vertices**: the cheapest test that could refute T (about 3.3
   hours of wall time on two cores).
