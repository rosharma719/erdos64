# Realizability of the irreducible Type-B family

**Status.** This phase combines hand-written proofs, explicit finite graph
certificates, a computer-assisted fixed-template UNSAT certificate checked by
two unrelated solvers, and an exhaustive finite Balaban 2-switch audit. It is
not an exhaustive search over all path embeddings or orders, does not prove
ICF, and is not proof-assistant formal verification. No Lean, Coq, Isabelle,
or comparable formalization exists.

The exact command is
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/type_b_realizability.py
--certificate data/type_b_pi0_fixed_template_certificate.json`.
`manifests/type_b_realizability_manifest.json` freezes source, input, output,
and stdout checksums, dependency versions, independent checks, and the precise
completed range. The literal certificate is
`data/type_b_pi0_fixed_template_certificate.json`.

The input theorem package is `type_b_compatibility.md`. We do not repeat its
abstract arithmetic classification; the question here is whether its one
named infinite family can be realized by actual bridges.

## 1. The family, frozen exactly

Define

\[
 \Pi=(\rho,s,t,u,\delta,\varepsilon)
\]

with

\[
 \rho,s\ge2,\qquad \delta,\varepsilon\in\{1,2\},\qquad
 t,u>\max\{\rho,s,3\}.
\]

Put

\[
 \ell=2^t+1,\qquad m=2^u+1
\]

and define the forced terminal spectra

\[
 S_1(\Pi)=\{2,\ell,\ell+\delta\},
\]

\[
 S_2(\Pi)=\{2^\rho,2^s+1,m,m+\varepsilon\}.
\]

`verifier/type_b_realizability.py` implements this definition as
`forced_spectra(Pi)`. Its `is_abstractly_compatible(Pi)` checks:

\[
 (S_1+\{1\})\cap\mathcal F=\varnothing,
 \quad (S_2+\{1\})\cap\mathcal F=\varnothing,
 \quad (S_1+S_2)\cap\mathcal F=\varnothing,
\]

as well as the forced internal lengths

\[
 \ell,\quad\ell+\delta,\quad2^\rho+2^s-1.
\]

For clarity, the complete guaranteed list is frozen here rather than hidden
behind the function name:

| source | guaranteed lengths |
|---|---|
| internal `B1` | `ell`, `ell+delta` |
| internal `B2` | `2^rho+2^s-1` |
| edge plus `S1` | `3`, `ell+1`, `ell+delta+1` |
| edge plus `S2` | `2^rho+1`, `2^s+2`, `m+1`, `m+epsilon+1` |
| shortest `B1` path plus `S2` | `2^rho+2`, `2^s+3`, `m+2`, `m+epsilon+2` |
| long `B1` pair plus theta pair | `ell+2^rho`, `ell+delta+2^rho`, `ell+2^s+1`, `ell+delta+2^s+1` |
| the two long admissible pairs across the cut | `ell+m`, `ell+m+epsilon`, `ell+delta+m`, `ell+delta+m+epsilon` |

Thus the four gap subfamilies have offsets from `ell+m` equal to
`(0,1,1,2)`, `(0,1,2,3)`, `(0,1,2,3)`, and `(0,2,2,4)` for
`(delta,epsilon)=(1,1),(1,2),(2,1),(2,2)`, respectively. They are four
indexed subfamilies of this one parameterized schema.

The excluded small exponent cases are unchanged: for
`2^t+2^u+2+q`, `0<=q<=4`, the only power hits up to interchanging `t,u` are

\[
 (q;t,u)=(0;2,1),(2;1,1),(2;3,2),(4;3,1).
\]

The inequalities above force `t,u>=4`, so none occurs.

**Completeness scope [PROVED BY DEFINITION AND AUDIT].** This parameterization
is exactly the one explicit infinite family isolated in the previous phase.
That phase did not classify every abstractly compatible spectrum, and this
file does not retroactively claim it did. No second infinite family was named
there. Thus `Pi` is complete relative to the prior stopping object, not a
classification of all possible Type-B spectra.

## 2. First twenty targets

Tuples are ordered by maximum required terminal-path length, sum of required
lengths, the order lower bound below, exponent tuple, then gap tuple. The
first twenty are:

| rank | `(rho,s,t,u;delta,epsilon)` | `S1` | `S2` | `(n1,n2;nG)` lower bound |
|---:|---|---|---|---|
| 1 | `(2,2,4,4;1,1)` | `2,17,18` | `4,5,17,18` | `(19,19;36)` |
| 2 | `(2,3,4,4;1,1)` | `2,17,18` | `4,9,17,18` | `(19,19;36)` |
| 3 | `(3,2,4,4;1,1)` | `2,17,18` | `5,8,17,18` | `(19,19;36)` |
| 4 | `(3,3,4,4;1,1)` | `2,17,18` | `8,9,17,18` | `(19,19;36)` |
| 5 | `(2,2,4,4;1,2)` | `2,17,18` | `4,5,17,19` | `(19,20;37)` |
| 6 | `(2,2,4,4;2,1)` | `2,17,19` | `4,5,17,18` | `(20,19;37)` |
| 7 | `(2,2,4,4;2,2)` | `2,17,19` | `4,5,17,19` | `(20,20;38)` |
| 8 | `(2,3,4,4;1,2)` | `2,17,18` | `4,9,17,19` | `(19,20;37)` |
| 9 | `(2,3,4,4;2,1)` | `2,17,19` | `4,9,17,18` | `(20,19;37)` |
| 10 | `(3,2,4,4;1,2)` | `2,17,18` | `5,8,17,19` | `(19,20;37)` |
| 11 | `(3,2,4,4;2,1)` | `2,17,19` | `5,8,17,18` | `(20,19;37)` |
| 12 | `(2,3,4,4;2,2)` | `2,17,19` | `4,9,17,19` | `(20,20;38)` |
| 13 | `(3,2,4,4;2,2)` | `2,17,19` | `5,8,17,19` | `(20,20;38)` |
| 14 | `(3,3,4,4;1,2)` | `2,17,18` | `8,9,17,19` | `(19,20;37)` |
| 15 | `(3,3,4,4;2,1)` | `2,17,19` | `8,9,17,18` | `(20,19;37)` |
| 16 | `(3,3,4,4;2,2)` | `2,17,19` | `8,9,17,19` | `(20,20;38)` |
| 17 | `(2,2,4,5;1,1)` | `2,17,18` | `4,5,33,34` | `(19,35;52)` |
| 18 | `(2,2,5,4;1,1)` | `2,33,34` | `4,5,17,18` | `(35,19;52)` |
| 19 | `(2,2,4,5;2,1)` | `2,17,19` | `4,5,33,34` | `(20,35;53)` |
| 20 | `(2,2,5,4;1,2)` | `2,33,34` | `4,5,17,19` | `(35,20;53)` |

The certificate stores the complete keys and all bounds. The enumerated box
contains more than twenty tuples below the first omitted dyadic scale, so this
is an exact prefix, not a sampled list.

## 3. Rigorous order and size bounds

For `B_1`, the path of length `ell+delta` alone gives

\[
 |V(B_1)|\ge \ell+\delta+1.
\]

This already accounts for maximum possible overlap: no simple path of that
length can use fewer vertices. The forced gateway prefix and the length-two
path do not weaken it.

For `B_2`, the longest required path gives `m+epsilon+1`. Independently, the
two theta suffixes have lengths `2^rho-1` and `2^s`, are internally disjoint,
and form a cycle of length `2^rho+2^s-1`; adding the gateway vertex `x` gives

\[
 |V(B_2)|\ge\max\{m+\varepsilon+1,2^\rho+2^s\}.
\]

Every bridge has degree one at `x`, positive degree at `y`, and all internal
degrees at least three. Hence for `n_i=|V(B_i)|`,

\[
 |E(B_i)|\ge\left\lceil\frac{3n_i-4}{2}\right\rceil.
\]

Consequently

\[
 |V(G)|\ge n_1+n_2-2,
 \qquad
 |E(G)|\ge
 \left\lceil\frac{3n_1-4}{2}\right\rceil+
 \left\lceil\frac{3n_2-4}{2}\right\rceil+1.
\]

For the smallest tuple this is `|V(G)|>=36`, `|E(G)|>=55`. The completed
global computation in `proof.md` covers all graphs only through order 11,
and the proved `C4/C8` theorem only through order 19. The Type-A bridge search
through bridge order 11 is a different rooted class. None covers order 36 or
the present Type-B family.

## 4. Path-union optimization at the first dyadic scale

For `t=u=4`, explicit path systems attain the vertex lower bounds for both
gaps. The certificate records every vertex sequence and edge.

- `delta=1`: `B_1` has paths `2,17,18` on 19 vertices.
- `delta=2`: `B_1` has paths `2,17,19` on 20 vertices.
- `epsilon=1`: `B_2` has paths `4,5,17,18` on 19 vertices.
- `epsilon=2`: `B_2` has paths `4,5,17,19` on 20 vertices.

Two independent exact detectors find no `C4`, `C8`, or `C16` in any union.
The longest-path lower bound plus these literal witnesses proves optimality
at the canonical-path-union level. This is stronger than a bounded absence
calculation: overlap really can pack every required path at the trivial order
bound without yet creating a forbidden internal cycle.

The missing constraint is degree saturation. For the smallest gap-one
systems the `B_1` union has internal degree deficit 13 and the `B_2` union
deficit 12, so at least 7 and 6 additional edges, respectively, are required.
Those edges must be chords, ears, or larger pertinent expansions. This is the
first exact realizability mechanism: path packing succeeds, while saturating
its degree-two segments is the obstruction.

## 5. Fixed-template paired saturation certificate

The first constructive solver fixes one optimal embedding for

\[
 \Pi_0=(2,2,4,4,1,1)
\]

at bridge orders `(19,19)` and full order 36. It then ranges over **every**
possible additional edge within either bridge, with no cross edges, retaining
`xy`, the exact gateway edges, all required paths, the Type-B degree-one
profile at `x`, and Lemma NA at the second gateway.

The solver deliberately omits closure 2-connectivity and T9B: this enlarges
the candidate set. Therefore UNSAT in the relaxed model remains a valid
nonrealizability certificate for this fixed embedding.

The exact run has:

| quantity | value |
|---|---:|
| full order | 36 |
| optional/fixed edge variables | 340 |
| hard possible-`C4` constraints | 23,256 |
| learned literal `C8` witnesses | 138 |
| OR-Tools final status | `INFEASIBLE` |
| independent CNF variables | 1,998 |
| independent CNF clauses | 26,318 |
| PySAT Glucose3 result | `UNSAT` |

Every learned clause is the negation of the eight literal edges of an actual
simple `C8` returned by the exact DFS detector and confirmed during CEGAR.
After OR-Tools reaches infeasibility, a separately constructed CNF uses a
different sequential-cardinality encoding and the unrelated Glucose3 solver;
it independently returns UNSAT.

**Exact conclusion [COMPUTER-ASSISTED FINITE CERTIFICATE].** This one optimal
path embedding cannot be completed even to a minimum-degree-three `C4/C8`-free
graph. It is not a proof for other optimal embeddings, the other first twenty
tuples, or higher orders. No fixed-order UNSAT generalization is made.

## 6. Canonical paths, ears, and the Balaban mechanism

The Balaban admissible paths `11,13` share their gateway prefix through vertex
6. Their symmetric difference is a `C10`, not the canonical `C16`. Thus the
`C16` is neither their one divergence cell nor their symmetric-difference
component.

There are exactly 3,298 internal `C16`s. NetworkX enumeration and a separate
elementary exact DFS enumeration agree cycle-for-cycle after canonicalization;
the certificate retains every literal cycle and its edge/vertex intersection
counts with both admissible paths. All 3,298 avoid the two added gateway
vertices and lie in the Balaban rigid host core; 672 are vertex-disjoint from
both recorded paths. So the fixture has many independent internal failures,
not only the selected witness below.

The exact `C16` decomposes instead as:

- a rigid-core ear
  `3-32-31-22-23-62`, of length 5; and
- a route already in the union of the recorded paths,
  `3-4-5-6-7-8-27-28-69-0-61-62`, of length 11.

Their interiors are disjoint and `5+11=16`. This is an instance of the
elementary ear-closure lemma: an `a`-edge ear and an internally disjoint
`(2^k-a)`-edge route force a `C_{2^k}`. Its SPQR location is the
3-connected Balaban R-core.

The proposed formula involving a pair `(2^t+1,2^t+3)` is not supported by
this fixture: `11,13` equal `2^3+3,2^3+5`. The correct extracted mechanism is
the `5+11` ear closure, not a theorem about every pair of that proposed form.

### Exhaustive witness-preserving 2-switch audit

There are five canonical-`C16` edges outside both recorded admissible paths.
The verifier exhausts every simple degree-preserving 2-switch that removes one
of those edges, removes no edge of either required path, and retains closure
2-connectivity. Exactly 826 structural mutations occur:

| first failure | mutations |
|---|---:|
| `C4` | 135 |
| `C8` | 316 |
| `C16` | 375 |
| clean through 16 | 0 |

Every failure record contains its literal cycle witness, checked directly
against the mutated graph. This is an exhaustive finite certificate for that
precise 2-switch class, not a theorem about ear rerouting, lifts, vertex
splits, or other mutations.

## 7. ICF and SPQR status

ICF remains conjectural. The present evidence proves neither that every
realization has a power cycle nor that every long admissible pair creates the
Balaban ear. The optimal path unions show why a one-cell theorem cannot work:
required paths can overlap enough to remain internally clean at minimum
order. The fixed-template UNSAT result shows that adding degree-saturating
edges can force short power cycles, but only for one embedding.

Relative to the canonical path union, the remaining SPQR question is now
precise: can degree deficits be supplied by ears or pertinent expansions
whose endpoint-route sums all avoid powers of two? T9B forces real R/P edges
to meet internal cubic vertices, but does not decide these ear endpoint
lengths. The Balaban `5+11` pattern is one exact R-node answer; it is not yet a
finite traversal classification.

No full counterexample, fully realizable isolated bridge, or compatible
paired obstruction was found. The unresolved object is no longer an abstract
spectrum: it is degree-three saturation of an optimal, internally clean
canonical path union while preserving all full spectra.

**one exact unresolved realizability mechanism**
