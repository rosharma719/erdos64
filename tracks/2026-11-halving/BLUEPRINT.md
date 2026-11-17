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
- **WRP:** for every prime cubic `B ≠ K4`, root `r`, and labelling of
  `V(B) − r` by the letters {identity, triangle, uniform H7, skew H7, H15} with
  port orientations, some cycle of `B − r` has a lifted window containing a
  power of two.

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
| R1 | Decomposition route: D1 ∧ W1 ∧ K1 ⇒ T | AND | D1, W1, K1 | OPEN | brief, Step 3 |
| R2 | A direct obstruction to growth of clean 3-poles | — | — | OPEN, not stated | — |

### Tower theorem

| ID | Statement | Type | Depends on | Status | Owner |
|---|---|---|---|---|---|
| K1 | Clean triangle-built 3-poles have exactly 1, 3, 7, 15 vertices | AND | K1a, K1b, K1c | COMPUTED (signature level); proof OPEN | ChatGPT, pass XII |
| K1a | Interval lemma: port-pair path sets of clean triangle-built poles are integer intervals | — | — | CANDIDATE | ChatGPT |
| K1b | Span lemma: the longest port-pair path has length N − 1 | — | — | CANDIDATE | ChatGPT |
| K1c | Short-path growth: A(N) ≤ α log₂ N + β, constants to be found | — | — | CANDIDATE | ChatGPT |

### Decomposition lemma

| ID | Statement | Type | Depends on | Status | Owner |
|---|---|---|---|---|---|
| D1 | A smallest clean 3-pole outside T's list is a prime cubic graph minus a root, with T-list gadgets substituted | AND | D1a–D1d | OPEN | ChatGPT, pass XII |
| D1a | Case: cyclic 3-edge cuts of the capped graph | — | X1 | OPEN | ChatGPT |
| D1b | Case: 2-edge cuts (the far side is a clean 2-pole) | — | E4 | OPEN; E4 covers 2-poles ≤ 20 vertices | ChatGPT |
| D1c | Case: bridges (the far side is a clean 1-pole; doubling gives a min-degree-3 counterexample) | — | L0 | OPEN | ChatGPT |
| D1d | Lifting rule for cycles and paths through substituted gadgets | — | X1, X2 | OPEN | ChatGPT |
| X1 | Exact length transfer across cyclic 3-edge cuts | — | — | PROVED-DRAFT (pass IV) | `three_cut_prime_transfer.md` |
| X2 | Exact length transfer across general edge cuts | — | — | PROVED-DRAFT (pass X) | `boundary_linkage_composition.md` |

### WRP

| ID | Statement | Type | Depends on | Status | Evidence |
|---|---|---|---|---|---|
| W1 | WRP | AND | W1a, W1b | OPEN | — |
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
| E5 | Independent generator (not nauty) agrees through 15 vertices | OPEN | ChatGPT, pass XII |

### Novelty

| ID | Statement | Status |
|---|---|---|
| N1 | Garcia (arXiv:2609.04686, Prop. 6.2) already classifies three-port gadgets free of C4 and C8 on 5, 7, 9 vertices (exactly H7 and H7′ at 7), and on 11 only with attachments pairwise at distance ≥ 3. E1 beyond 9 vertices, uniqueness of H15, Conjecture T and I1 were not found in the literature | Search of 16 Nov 2026 (arXiv full text of Garcia; web search); not exhaustive |
| N2 | Garcia conjectures that a two-attachment gadget with no internal power-of-two cycle has max S ≥ 2 min S. E4 says no such gadget (in our 2-pole sense) exists on ≤ 20 vertices | Relation to Garcia's definition of two-attachment gadget not yet checked |

## Highest-value open nodes

1. **K1** (tower proof): template for every route to T.
2. **D1** (decomposition): turns T into a statement about prime graphs.
3. **E1 at 23 vertices**: the cheapest test that could refute T (about 3.3
   hours of wall time on two cores).
