# Zero-slack `delta=2` Type-B bridges: exact reduction and B20D2

**Status.** Hand-written reduction plus exhaustive computer-assisted finite
certificates. Family I and the 29-edge layer are eliminated by direct reuse
of existing certificates (`data/type_b_slack_family_i_certificate.json`,
`data/type_b_one_slack_extremal_certificate.json`) with zero new
computation. Family II is eliminated by a fresh exhaustive computation,
cross-validated by two independently coded generators whose canonical
candidate sets agree exactly, plus a third independent networkx verifier.
No proof-assistant formalization exists.

## 1. Why this case is genuinely different from the delta=1 (B20) case

The frozen tuple family `Pi=(rho,s,t,u,delta,epsilon)`
(`type_b_realizability.md`) gives `B1` forced terminal spectrum
`S1={2,ell,ell+delta}` and `B2` forced spectrum
`S2={2^rho,2^s+1,m,m+epsilon}`, with `ell=2^t+1`, `m=2^u+1`. For `t=u=4`,
`ell=m=17`. When `delta=1` (or `epsilon=1`), the longest required path has
length 18, one less than the bridge's minimum order of 19 — this is the
"one-slack" geometry B19/B20 already resolved. When `delta=2` (or
`epsilon=2`), the longest required path has length **19**, exactly equal
to a 20-vertex bridge's vertex count minus 1: **zero slack**. The required
path is Hamiltonian in `B`, with no off-path vertex at all — a materially
different geometry from B20's Family II (which had exactly one off-path
vertex `z`).

## 2. Setup for a minimum-order `delta=2` bridge

Let `B` be a bridge role whose longest required length is 19 (i.e.
`delta=2` for `B1`, or `epsilon=2` for `B2`), with `|V(B)|=20`. Terminals
`x,y`; `a` is `x`'s unique neighbour (`d_B(x)=1`); the required length-19
path is Hamiltonian in `B`, so deleting `x` leaves a Hamiltonian `a-y` path
in `R=B-x`, which therefore has exactly 19 vertices and is connected,
matching `p_0=a,\ldots,p_{18}=y` with **no off-path vertex**. This claim
(Hamiltonicity of the length-19 path in a 20-vertex bridge) is immediate
from vertex-count arithmetic (a length-19 path has 20 vertices, `|V(B)|=20`
exactly) rather than assumed.

**Degree bounds, generic across both bridge roles (no `rho,s` dependence).**
Exactly as in B19's dependency table (`type_b_b19.md`), which the priority
audit (`type_b_tuple_priority_audit.md`) already established never
references `rho` or `s`:

- The 17 vertices `p_1,\ldots,p_{17}` are internal to `B`, unaffected by
  deleting `x`, so `d_R(p_i)>=3` (ambient minimum degree three).
- `a=p_0` is internal to `B` too (ambient degree `>=3`), loses only edge
  `xa` when forming `R`, so `d_R(a)>=2`.
- `d_R(y)>=2`: for the `B1` role (`delta=2`), `S1` always contains `2`
  (independent of `delta`), forcing a direct `a-y` edge in `B`/`R`, plus
  the Hamiltonian path's own distinct last edge into `y` — two distinct
  edges. For the `B2` role (`epsilon=2`), the two internally disjoint
  theta suffixes enter `y` through distinct neighbours — again two
  distinct edges. Neither mechanism depends on the specific suffix
  lengths (`2^rho-1`, `2^s`) or on `epsilon`, only on the structural fact
  that a theta bridge has two branches.

Hence, exactly as in B19:

\[
 2|E(R)|\ge17\cdot3+2\cdot2=55, \qquad |E(R)|\ge28.
\]

Since `R` is `C4/C8`-free (subgraph of the ambient counterexample) and
`ex(19;{C4,C8})=29`, `|E(R)| in {28,29}`.

## 3. Degree classification at 28 edges

Degree sum `56`, excess over the minimum-`55` sum is exactly `1`,
distributed as a single non-negative unit exactly as in the B20 excess
argument (`type_b_one_slack_resolution.md` Section 1) — no vertex can
reach degree 5 without forcing a negative excess elsewhere. Two cases:

- **Family I-A**: `d(a)=2, d(y)=3`, all 17 internal vertices at 3. Degree
  sequence `2,3^18`.
- **Family I-Y**: `d(a)=3, d(y)=2`, same degree sequence `2,3^18` (labels
  swapped).
- **Family II**: `d(a)=d(y)=2`, exactly one internal vertex `p_j`
  (`1<=j<=17`) at degree 4, the rest at 3. Degree sequence `2^2,3^16,4`.

Unlike B20's Family II, there is **no off-path vertex** here: the degree-4
role is one of the 17 *on-path* internal vertices, giving exactly 17 role
cases (not 17 = 16 internal + 1 off-path as in B20 — here it is 17 = 17
on-path internal vertices exactly, a different count that happens to
coincide numerically).

## 4. Family I (both labelings): eliminated by direct reuse, zero new computation

`data/type_b_slack_family_i_certificate.json` is the record of
`nauty-geng -c -f -d2 -D3 19 28:28`: the complete set of 86,047 connected,
`C4`-free, 19-vertex, 28-edge graphs with degree sequence `2,3^18`
(automatic from the `[2,3]` degree box at exactly 28 edges). Every one of
them contains a `C8`. This is a pure statement about abstract graphs with
a given vertex count, edge count, and degree sequence — it says nothing
about any path embedding, off-path vertex, or one-slack/zero-slack
structure. Since Family I-A and Family I-Y both have this exact abstract
degree sequence, **the existing certificate applies verbatim: both are
eliminated with no new graph generation.**

## 5. The 29-edge layer: eliminated by direct reuse, zero new computation

`data/type_b_one_slack_extremal_certificate.json` records McKay's complete
extremal census of 304 connected, `C4/C8`-free, 19-vertex, 29-edge graphs
(`data/c48_n19e29.s6`): every one has at least 3 degree-two vertices. This
is likewise a pure abstract-graph statement, independent of any path
structure. In the zero-slack `delta=2` case, exactly as in the one-slack
case, only `a,y` can possibly be degree-2 (all 17 internal vertices are
forced to degree `>=3`), so an eligible `R` needs at most 2 degree-two
vertices. Since all 304 extremal graphs have at least 3, **the existing
certificate applies verbatim: the 29-edge layer is eliminated with no new
computation.**

## 6. Family II: exact slot-matching model

10 non-path edges remain (`28-18=10`, since the spanning path itself has
18 edges). For degree-4 role `p_j`: deficits are `a:1, y:1, p_j:2`, all
other 16 internal vertices `:1` each. Total deficit `1+1+2+16=20=2*10`.
Candidate edges: all 153 non-path pairs among the 19 vertices (`C(19,2)-18
= 171-18=153`). No edge is excluded a priori beyond the 18 fixed path
edges and loops.

## 7. Direct slot-matching generator (`verifier/type_b_delta2_slot_search.c -generate-all`)

Backtracking search over the 153 candidates for each of the 17 roles,
include/exclude branching, with the same feasibility prunes as B20's
generator (zero-deficit vertices can never receive an edge; branches with
insufficient remaining candidates are abandoned) and the same edge-local
incremental `C4/C8` pruning rule (reject an edge if the graph so far
already has a simple path of length 3 or 7 between its endpoints; `C16` is
checked post-hoc, not pruned incrementally). The `has_cycle_len` routine
was freshly written for this file (not `#include`d from
`verifier/type_b_slack_path_search.c`) and independently unit-tested
before use: `-selftest` confirms `K4` has a `C4`, an 8-cycle graph has a
`C8` and no `C4`, and a path graph has neither — guarding directly against
the interrupted-session's previously-recorded vacuous-detector bug
pattern (start vertex marked visited *and* required unvisited at closure).

**Result:** 12 total labeled candidates across all 17 roles:

| role | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| solutions | 0 | 0 | 1 | 0 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 0 |

Symmetric under path reversal (`p_i<->p_18-i`, role `j<->18-j`): role 9 is
the unique self-paired role (count 2); every other pair (1,17), (2,16),
(3,15), (4,14), (5,13), (6,12), (7,11), (8,10) agrees exactly — again an
unplanned internal consistency check. Total DFS nodes: 12,004,454 (2.3
seconds).

**All 12 candidates independently re-checked positive for all three of:**
an internal `C16`, a simple length-6 `a`-`y` path (closure `C8`), and a
simple length-14 `a`-`y` path (closure `C16`). Zero have a `C4`, `C8`
directly, or a length-2 `a`-`y` path (closure `C4`) — 0/12, consistent
with the incremental pruning.

## 8. The terminal-closing offset (audited, unchanged formula)

Identical mechanism to B20 Section 5: the full graph contains edges `xa`
and `xy`; a simple `a`-`y` path of length `r` in `R` closes to a cycle of
length `r+2` through `x-a...y-x`. `r=2` gives `C4`, `r=6` gives `C8`,
`r=14` gives `C16`. All three lengths were explicitly checked (not just
6 and 14); zero candidates have the length-2 path, all 12 have both the
length-6 and length-14 paths.

## 9. Independent SAT generator (`verifier/type_b_delta2_slot_sat.py`)

Independently coded: one boolean variable per candidate edge,
exact-cardinality constraints (PySAT `CardEnc.equals`) per vertex deficit
plus a total-of-10 constraint, and a CEGAR loop against
`verifier/cycle_detect.py`'s DFS detector (not the C file's) for `C4/C8`.
Shares only the mathematical definition of the path/deficits/candidate
universe with the direct generator; imports neither its recursion, its
cycle detector, nor its output.

**Result:** 12 total solutions, matching the direct generator's per-role
counts exactly (`0,0,1,0,1,1,1,1,2,1,1,1,1,0,1,0,0`). Total wall time
1m45s.

## 10. Canonical-set comparison

Canonicalizing under path reversal (`p_i<->p_18-i`, role mapped
accordingly) collapses the 12 labeled solutions from each generator to
**6** canonical classes. The two generators' canonical sets are identical:

```text
C direct generator:  labeled=12  canonical=6
SAT generator:       labeled=12  canonical=6
C canonical multiset SHA-256:   7486f2ee4d8c3707e790816e15c7df5d67ec83dabed1096e8c7b5cf78110cf4c
SAT canonical multiset SHA-256: 7486f2ee4d8c3707e790816e15c7df5d67ec83dabed1096e8c7b5cf78110cf4c
only_in_C: 0   only_in_SAT: 0
SETS AGREE: True
```

## 11. Third-method independent verification

`verifier/type_b_delta2_independent.py` (networkx-only, calling neither
generator's internal functions) re-derives from the 12 saved candidate
records alone: vertex/edge counts, connectivity, exact degree sequence,
presence of the full spanning path, the claimed degree-4 role, `C4`,
`C8`, `C16`, and all three closing-path witnesses (lengths 2, 6, 14). All
12 pass every structural check and all 12 are independently confirmed
eliminated. A further manual spot re-verification (outside all three
tools) confirmed the recorded `C16` witness and both length-6/length-14
path witnesses are valid simple paths/cycles on all 12 records.

## 12. Theorem B20D2

**B20D2.** No eligible 20-vertex Type-B bridge with frozen admissible gap
2 exists.

*Proof.* Let `B` be a bridge role with longest required path length 19
(`delta=2` for `B1`, or `epsilon=2` for `B2`) and `|V(B)|=20`. By Section
2, `R=B-x` has 19 vertices spanned entirely by the required path (no
off-path vertex), with `d_R(a),d_R(y)>=2` and all 17 remaining vertices at
degree `>=3` — derived using only generic bridge/ambient facts, never
`rho` or `s`. By Section 2's edge-count argument, `|E(R)| in {28,29}`. The
29-edge layer is eliminated by direct reuse of the existing 304-graph
McKay extremal certificate (Section 5). At 28 edges, the only possible
degree sequences are `2,3^18` (Family I, both labelings) and `2^2,3^16,4`
(Family II). Family I is eliminated by direct reuse of the existing
86,047-graph certificate (Section 4). Family II is eliminated by an
exhaustive computation (Sections 6-11): all 12 candidates (agreeing
exactly between two independently coded generators, confirmed by a third
independent verifier) contain an internal `C16` and force a closure `C8`
and closure `C16`. Hence no 19-vertex `R` — and so no 20-vertex bridge
role with admissible gap 2 — satisfies the necessary conditions. `square`

**This proof never uses `rho`, `s`, the partner bridge, cross-spectrum
compatibility, or equality of the two bridge orders** — matching the
task's stated constraints for a genuinely local, role-generic theorem.

## 13. Global tuple corollary

Combining B19+B20 (which raise a role with gap 1 from 20 to 21) with
B20D2 (which raises a role with gap 2 from 20 to 21), **every bridge role
of every frozen tuple in `type_b_realizability.md`'s first-16 entries
(the only ones with original bound `<=40`) now has `|V(role)|>=21`**,
since every such role has gap either 1 (covered by B19/B20) or 2 (covered
by B20D2):

| rank | `(delta,epsilon)` | orig `nG` | after B19+B20 only | after B20D2 too |
|---:|---|---:|---:|---:|
| 1-4 | `(1,1)` | 36 | 40 | 40 |
| 5,6,8,9,10,11,14,15 | mixed | 37 | 39 | **40** |
| 7,12,13,16 | `(2,2)` | 38 | 38 | **40** |

\[
 |V(G)|=|V(B_1)|+|V(B_2)|-2\ge21+21-2=40 \quad\text{for every one of the 16 tuples.}
\]

**Every frozen irreducible paired-spectrum tuple with original bound
`<=40` has full-graph order at least 40.** Ranks 17-20 (and beyond,
`t` or `u`=5) already had original bound `>=52`, unaffected and
irrelevant to this comparison.

**Scope, stated precisely.** This is a lower bound for the frozen Type-B
tuple family in `type_b_realizability.md` — the one explicit infinite
family isolated in prior phases, not a classification of every possible
Type-B spectrum (that file's own completeness-scope caveat, Section 1,
still applies). It is not automatically a global Erdos-Gyarfas
counterexample-order lower bound unless every Type-B configuration is
proved to reduce to this family, which is not claimed here.

## 14. What is explicitly claimed and what is not

- **Claimed:** B20D2 is proved, using only generic (rho,s-independent)
  bridge facts. Family I and the 29-edge layer reuse existing certificates
  verbatim with zero new computation; Family II is eliminated by a fresh,
  cross-validated exhaustive computation (two independent generators
  agreeing exactly, a third independent verifier).
- **Claimed:** every one of the 16 frozen tuples with original bound
  `<=40` now has full-graph order `>=40`.
- **Not claimed:** any classification of Type-B configurations beyond the
  frozen tuple family; any proof-assistant formalization; any statement
  about ranks 17+ (already far above 40, unaffected).
