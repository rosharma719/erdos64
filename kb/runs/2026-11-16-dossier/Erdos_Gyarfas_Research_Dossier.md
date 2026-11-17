---
title: "Erdős–Gyárfás Research Dossier"
subtitle: "Consolidated results from the previous research conversation and the November 16, 2026 continuation"
date: "November 16, 2026"
author: "Research working record"
lang: en-US
colorlinks: true
urlcolor: MidnightBlue
linkcolor: MidnightBlue
geometry: "margin=0.83in"
fontsize: 10pt
---

> **Status:** Research record, not a proof of the Erdős–Gyárfás conjecture and not a peer-reviewed manuscript. The conjecture remains open as of the stated date. This document separates internally argued theorems, finite computational observations, published results, conditional claims, and abandoned directions. It synthesizes accessible earlier notes, patches, certificates, the final prior-chat literature review, and the current continuation; it is not a verbatim reconstruction of every earlier message.

# Executive summary

The Erdős–Gyárfás conjecture asserts that every finite simple graph with minimum degree at least three contains a simple cycle of length $2^k$ for some $k\ge2$. We have explored minimal counterexamples, reductions across separators, cubic graph substitutions and lifts, three-terminal gadgets, finite enumerations, cyclically four-edge-connected cubic graphs, Hamiltonian chord interlacement, theta-necklace arithmetic, and the quantitative resilience of dyadic-cycle families.

**Most important cumulative result:** We now possess *exact* ways of transferring attainable cycle lengths across cyclic three-edge cuts, arbitrary finite edge cuts, and the edge-bridging operation. We also have a fractional cycle-packing/covering invariant that quantifies when a bridge preserves a dyadic cycle avoiding an arbitrary vertex, and a switching-polynomial description of compatible reroutings. These tools localize a credible proof obstacle: **low-resilience cubic cores in which every potential shifted-cycle and new-bridge-path repair is constrained**.

**Most important limitation:** None of these tools yet forces a dyadic cycle in every cyclically four-edge-connected cubic graph, nor does a proof for prime cubic graphs alone imply the full conjecture. Cycle-length *abundance* and arithmetic *residue coverage* do not provide absolute location at a power of two. New structural forcing is required.

**New in this continuation:** A universal upper bound on fractional resilience was proved directly:

$$
\rho(G)\le \frac{m(n-q)}{2nq},\qquad
\rho(G)\le \frac{3(n-q)}{4q}\quad\text{for cubic }G,
$$

where $q$ is the shortest dyadic cycle length. In the existing computational workspace, an order-16 generation produced 607 cubic isomorphism classes without rooted failures, and a test over **138,396 disjoint-edge bridge operations** from those 607 graphs found no rooted failures in the resulting order-18 children. This is a bounded, code-level observation, not a theorem for all order-18 prime graphs and not a proof of the conjecture.

**Research recommendation:** Pursue low-resilience *exchange or renewal* theorems for admissible edge bridging, while retaining independent compatible-switch/path-length control as the mathematically broader secondary track. Require aggressive falsification of the *rooted prime conjecture*, which is stronger than the original statement.

## Evidence taxonomy

| Label | Meaning |
|:---|:---|
| **EXTERNAL** | Theorem or numerical statement explicitly attributed to published/preprint literature; verify the cited source and its assumptions. |
| **INTERNAL PROOF** | A proof appears in the archived project notes; independently referee before claiming novelty or publication. |
| **COMPUTED** | A finite claim backed by a described program, log, certificate, or census; its precise scope and reproducibility matter. |
| **REPORTED / UNRE-AUDITED** | Prior project status quoted from an earlier dossier or discussion, without full re-execution here. |
| **CONDITIONAL** | Follows if an explicitly stated unproved hypothesis or computational completeness premise holds. |
| **OPEN / FALSIFIED** | An unresolved statement or an earlier candidate ruled out by a counterexample. |

These labels must not be conflated. In particular, finite computations should not be promoted into universal graph-theoretic claims.

# 1. Problem, notation, and global context

Define $\mathcal D(G)$ as the set of simple cycles of $G$ of lengths $4,8,16,32,\ldots$. A graph is **dyadic-free** if $\mathcal D(G)=\varnothing$. It is **root-robust** if, for every $v\in V(G)$, there exists $C\in\mathcal D(G)$ with $v\notin V(C)$. A vertex is **dyadically root-critical** if deleting it leaves no dyadic cycle. Root robustness is a stronger property than the Erdős–Gyárfás conclusion.

For a cubic graph $G$, a **cyclic three-edge cut** separates two sides each containing a cycle; **cyclically four-edge-connected** means no such nontrivial cyclic cut in the relevant 3-connected cubic setting. We refer to these as *prime* cubic graphs as a convenience, not a claim of unique decomposition developed here.

**EXTERNAL, verified against contemporaneous public sources:** Ducoffe and Dumitru (2026) prove that more than two-thirds of vertices of a minimal counterexample have degree three and report verification through 40 vertices generally, 48 for cubic graphs, and 66 for bipartite graphs. Kingan and Kingan (2024) characterize cyclically four-edge-connected cubic graphs through ladder/Möbius-ladder and Petersen exceptions, and eligible edge-bridging constructions with prescribed cycle spread. Liu and Montgomery prove the conjecture under sufficiently large constant average-degree assumptions; Bucić, Gishboliner and Sudakov prove $n^{1-o(1)}$ distinct cycle lengths for Hamiltonian graphs of minimum degree at least three. None settles the cubic frontier. [References R1--R5]

A long interval of *distinct lengths* can miss a power of two: the entire integer interval $[2^k+1,2^{k+1}-1]$ does. This elementary arithmetic fact is the recurring obstruction throughout the project.

# 2. Chronological and methodological inventory

## 2.1 Early structural program: minimal counterexamples and separators

**REPORTED / UNRE-AUDITED (July 30 project brief).** In a minimal counterexample chosen first by order and then by size, the project developed an internal defect parameter

$$q(G)=2n-2-m,$$

reported an exclusion of $q\le3$ and hence $m\le2n-6$, and described degree restrictions, edge criticality, bridge exclusions, one- and two-pole terminal closures, three signature types A/B/C, and SPQR-style rigid-core constraints. These are recorded in the July brief as internal proofs, but are not re-refereed in this dossier. Some of the structural conclusions also overlap the later published Ducoffe--Dumitru framework. The underlying proofs, hypotheses, and version histories must be reviewed before using them as axioms in a new paper.

A prior claim that at most nine vertices had degree at least four was already flagged as dependent on an unverified extra inequality. The July roadmap instead retained a weaker conditional/externally-supported count. Do not silently revive the stronger claim.

**EARLY FINITE WORK (reported):** The project brief documented a complete internal minimum-degree-three census through 19 vertices, Type-A gadget eliminations at internal orders 9 and 11, attempted cyclic $\mathbb Z_3$ lifts of four 24-vertex bases, and extensive order-30 triangle-expansion sectors. Specifically, it reported 193,510 raw order-9 closures, 129,040 rooted classes and zero internally clean Type-A gadgets; it also reported 784,390,984 order-30 test instances across the six- and seven-triangle sectors, with zero survivors. The source brief regards the conclusion “any 30-vertex cubic counterexample has at most five triangles” as computationally certified **conditional on its enumerator and coverage arguments**. These counts were not re-run in the present pass and should be treated as a historical computational record, not a new independent verification.

**Important audit caveat:** Later conversation audits explicitly rejected unsupported claims of complete exhaustive results at orders 32--38. Separate order-32 defect-six and defect-seven workstreams were at various points reported as complete or partly complete, with proof-status inconsistencies. No unrestricted order-32--38 elimination is accepted in this dossier. The current published Ducoffe--Dumitru finite limits are the appropriate external benchmark.

## 2.2 Three-terminal gadgets, mixed substitutions, and triangle expansions

**INTERNAL PROOF / COMPUTED:** The November notes built exact port-pair path spectra for mixed three-terminal gadgets and a solver using convolution and interval propagation when spectra were consecutive. The archival research note records a complete small gadget classification through 11 internal vertices, a small-base census through order 10, and a six-class family of 78-vertex mixed-gadget constructions. These graphs were used to expose the limitations of short-cycle or local-window reasoning; none is a counterexample to Erdős–Gyárfás.

For one-round expansion of a vertex into a triangle, replacing a square's $t$ expanded vertices gives available lifted cycle lengths throughout $[4+t,4+2t]$. This exact formula became the basis for the later square-incidence parity theorem. For generic partial triangle expansions and cycles not entirely covered by squares, the complete cycle spectrum still requires careful accounting.

**INTERNAL PROOF:** A cycle-space averaging calculation and a path-spectrum dominance argument supplied necessary constraints, while an explicit 78-vertex family exposed an obstruction to the specific density bound under investigation. The notes explicitly did *not* convert the averaging identity into a universal Erdős–Gyárfás proof.

## 2.3 Prime decomposition and three-cut transfer (Pass IV)

**INTERNAL PROOF:** For an independent cyclic three-edge cut separating $A$ and $B$, write $I(A)$ and $I(B)$ for internal cycle-length sets, and $P_A(i,j)$ and $P_B(i,j)$ for simple terminal-to-terminal path-length sets. The *entire* cycle-length spectrum satisfies

$$
L(G)=I(A)\cup I(B)\cup\bigcup_{0\le i<j\le2}
\{2+x+y:x\in P_A(i,j),\ y\in P_B(i,j)\}.
$$

The proof uses the fact that a cycle crosses a three-edge cut in either zero or two edges. This is an exact identity, including for gapped path sets.

For a nonempty finite set $S$ of attainable path lengths, define the certified interval score

$$\omega(S)=\max_{[a,b]\cap\mathbb Z\subseteq S}(b-2a-1),\qquad
\Phi(A)=\sum_{0\le i<j\le2}\omega(P_A(i,j)).$$

The project proved the sufficient test $\Phi(A)+\Phi(B)\ge0\Rightarrow\mathcal D(G)\ne\varnothing$. This cannot be reversed, and the invariant is blind to parity-gapped spectra. A later note proved that the old $\Phi$ can be arbitrarily negative in the high-girth bipartite setting, *if* appropriate prime families exist, so a universal nonnegative prime lower bound is implausible.

**OPEN:** A usable 3-cut induction requires rooted or terminal-path information from the capped components. A dyadic cycle passing through an artificial cap vertex need not survive re-gluing. A theorem for prime cubic graphs, by itself, is insufficient for arbitrary cubic graphs.

## 2.4 Rooted prime graphs and two-ear switching (Passes V--VI)

**INTERNAL PROOF:** If a group of automorphisms has vertex orbit $O$ and a dyadic cycle omits at least one vertex of $O$, an automorphic copy avoids each specified vertex of $O$. For vertex-transitive graphs of non-power-of-two order, an existing dyadic cycle is necessarily nonspanning and hence establishes root robustness. This transports published existence results for certain Cayley families but does not create their existence proof.

For a cubic cycle $C$, with $h(C)$ chords and $\delta(C)$ edges leaving its vertex set, the spoke identity is $|\delta(C)|=|C|-2h(C)$. Three-vertex-connectivity guarantees some external $C$-ear avoiding a designated vertex, but does not guarantee the correct length.

**COMPUTED / INTERNAL PROOF:** A Petersen graph certificate demonstrates that no single-ear dyadic root-avoiding rerouting works in one natural rooted setup, although a *two-ear* balanced switch does. The Hamiltonian-matching reduction gave a bounded computational theorem for cyclically four-connected Hamiltonian cubic graphs through 16 vertices. At orders 6, 8, 10 and 12, all 26 non-$K_4$ prime classes in that record were root-robust. The larger order-16 census in the continuation is discussed separately below.

## 2.5 Edge bridging: a four-predecessor theorem (Pass VII)

Let $e=ab$ and $f=cd$ be vertex-disjoint edges of $G$. Delete $e,f$, add $x,y$, and insert $ax,bx,xy,cy,dy$. Write the resulting cubic graph as $B(G;e,f)$.

**INTERNAL PROOF (exact bijection):** Every child cycle avoiding $xy$ is a parent cycle with its used selected edges subdivided; its new length is $|C|+1_{e\in C}+1_{f\in C}$. Every child cycle containing $xy$ corresponds to a simple path in $G-\{e,f\}$ between one endpoint of $e$ and one endpoint of $f$ and has length $|P|+3$.

Thus, for a target $Q=2^k$, exactly four predecessor length types can generate a dyadic child cycle:

| Parent structure | Required parent length |
|:---|---:|
| Parent cycle using neither $e$ nor $f$ | $Q$ |
| Parent cycle using precisely one selected edge | $Q-1$ |
| Parent cycle using both selected edges | $Q-2$ |
| Endpoint-to-endpoint path in $G-\{e,f\}$ | $Q-3$ |

Root restrictions are inherited by the parent cycle/path; the *new roots* $x$ and $y$ can only be avoided by cycles of the first, subdivision-only type. This sharpens the prospective induction but also creates a hard obstruction: all applicable predecessor configurations must be excluded in a hypothetical root-critical child.

**FALSIFIED SIMPLIFICATIONS:** The project exhibits a prime 14-vertex child in which *only a new bridge path* repairs a particular root, and a complementary prime example where root-avoiding dyadic cycles arise from shifted parent cycles but no bridge-path dyadic repair exists. Neither one-sided mechanism is universal.

## 2.6 Fractional dyadic-cycle resilience (Pass VIII)

For nonzero weights $w_C\ge0$ on $C\in\mathcal D(G)$, set

$$W=\sum_Cw_C,\qquad \alpha=\max_v\sum_{C\ni v}w_C,
\qquad \beta=\max_e\sum_{C\ni e}w_C,$$

and define

$$\rho(G)=\sup_{w\ne0}\frac{W-\alpha}{2\beta},$$

with $\rho(G)=0$ if the graph has no dyadic cycles.

**INTERNAL PROOF:** $\rho(G)>0$ if and only if $G$ is root-robust. Under one bridge,

$$\boxed{\rho(B(G;e,f))\ge\max(0,\rho(G)-1)}.$$

After $t$ successive bridges, $\rho(G_t)\ge\max(0,\rho(G_0)-t)$. A hand-checkable sufficient condition is $W>\alpha+2t\beta$. The proof discards parent dyadic cycles touching either selected edge and retains the surviving weighted family intact.

An exact LP dual expresses $2\rho(G)$ as the minimum $\sum_e y_e$ subject to nonnegative $y_e,z_v$, total $\sum_vz_v\le1$, and

$$\sum_{e\in C}y_e+\sum_{v\in C}z_v\ge1\quad\text{for every dyadic }C.$$

Thus the invariant measures an *edge fractional cover after allowing one unit of free vertex-cover weight*. This is a useful structural translation, though the LP itself may be a standard instance of packing/covering duality.

**INTERNAL PROOF:** For a prism or Möbius ladder with $2k$ vertices, a family of $k$ peripheral squares has $W=k$, $\alpha=2$, $\beta\le2$, yielding $\rho\ge(k-2)/4$. Consequently, after $t$ arbitrary bridges, root robustness is maintained whenever $k>4t+2$. Small one-bridge exceptions were handled by a finite check. That result gives a genuine infinite-family theorem, independent of finding every cycle.

**COMPUTED COUNTEREXAMPLES:** Three-vertex-connectivity alone does not make root robustness bridge-stable; the triangular prism has a bridged, still 3-connected child with a root-critical vertex. Even in the prime setting, $\rho$ is not monotonically increasing under bridging: the archive reports a prime cube bridge taking $\rho$ from $3/4$ to $1/2$.

## 2.7 Square strips, exact boundary signatures, and switches (Passes IX--XI)

**INTERNAL PROOF:** The square-strip work converted distinguished 4-cycles into a rooted blocker packing/covering problem, studied how the square family transforms under bridge operations, and gave a four-terminal transfer identity for an open strip. This is a useful specialized refinement of the resilience method; it does not overcome arbitrary high-girth cubic graphs, where no squares exist.

**INTERNAL PROOF:** The general boundary-linkage theorem encodes a graph split across an edge cut by lengths of internally vertex-disjoint paths realizing each feasible boundary pairing, together with internal cycle information. Matching compatible pairing states and summing path lengths gives every crossing cycle. Contextual equivalence requires richer data than a single endpoint window; the notes show elementary examples distinguishing signatures with superficially similar interval bounds. Exact complete lossless signatures can require growing state complexity.

**INTERNAL PROOF:** If a path or cycle has genuinely independent bypasses with signed length increments $d_1,\ldots,d_t$, its constructed length spectrum contains $L+\sum_{i\in I}d_i$ for each subset $I$. The generating Laurent polynomial

$$F(z)=z^L\prod_{i=1}^t(1+z^{d_i})$$

counts cycles within that *specific switching family*. Root constraints can be enforced by fixing switch choices. A positive dyadic coefficient certifies existence; failure of one polynomial is not a graph-wide absence certificate. A Petersen certificate has choices of lengths $6,9,5,8$, with an 8-cycle obtained only by combining two signed changes.

**FALSIFIED:** A strict requirement that every prime cubic root admit two *positive* independent bypasses satisfying the complete subset-sum criterion is false in the Petersen graph. A separate subcubic example has wide endpoint-length range but no power-of-two cycle. Modularity and switch compatibility matter as much as nominal range.

# 3. November passes XXIII--XXVI: why scale is the barrier

## 3.1 Theta-necklace cancellation (Pass XXIII)

The published Lyngsie--Merker theta$(i)$ block provides four attachment routes of lengths

$$R_j(x,y)=B_j+xX_j+yY_j-2ixy,\qquad x,y\in\{0,1\}.$$

The mixed second difference is exactly $-2i$. **INTERNAL PROOF:** For two disjoint blocks with equal $Y$ increments, exchanging route choices produces two simple cycles differing by exactly $2i$; no equality of the $X$ increments is needed. Repeating disjoint pairs supplies an arithmetic progression of attainable *absolute* lengths $L,L+2i,\ldots,L+2im$, but only when the baseline, width and residue actually hit a power of two.

A modular-to-exact audit also isolated a common invalid inference: realizing the correct residue of a power of two modulo the odd part of a modulus does not imply a dyadic residue modulo the full modulus. Nor does modular attainment imply an exact length without a bounded length interval and sufficiently large modulus.

## 3.2 Subset-sum collisions and a no-go necklace (Pass XXIV)

**INTERNAL PROOF:** More generally, two distinct subsets of $Y_1,\ldots,Y_N$ with equal sums yield a $2i$ difference in cycle lengths. The pigeonhole condition $2^N>1+\sum|Y_j|$ guarantees such a collision. Partitioning blocks into disjoint groups yields multiple independent switches and an exact progression in increments of $2i$.

**CRITICAL NEGATIVE THEOREM (internal proof):** For arbitrarily large $N$, one can build a connected subcubic theta necklace with $N$ theta blocks, equal local increments, and no dyadic cycle. Its internal block cycles have lengths 6, 7, and 11, while all cycles traversing the ring can be placed strictly between consecutive powers of two by lengthening connectors. Such graphs have degree-two vertices, so they are not counterexamples to Erdős–Gyárfás. They demonstrate that arbitrary amounts of *local* flexibility need not reach the *absolute* dyadic scale. The surrounding cubic completion is indispensable.

Two independent code paths in the archived Pass XXIV checks agreed on finite necklace fixtures, including 120- and 250-vertex examples; those fixtures validate the formulas, not the general conjecture.

## 3.3 Hamiltonian interlacement barrier (Pass XXV)

For a cubic Hamiltonian graph $G=C+M$, define $I_C$ by connecting matching chords whose endpoints alternate on $C$.

**INTERNAL PROOF (classical structural fact):** $G$ is 3-vertex-connected if and only if the chord interlacement graph $I_C$ is connected. The archive constructs infinite 3-connected Hamiltonian cubic graphs of arbitrarily prescribed fixed girth and uniformly bounded chord span relative to the chosen Hamiltonian cycle. Hence neither three-connectivity nor the exclusion of any *fixed* finite set of dyadic cycle lengths forces macroscopic Hamiltonian shortcuts.

The construction rules out a previous conjectured “large chord span must appear” proof mechanism. It leaves open whether a bounded-span class eventually contains a *larger* power-of-two cycle.

## 3.4 Chord smoothing, separator identities, and odd-square parity (Pass XXVI)

**INTERNAL PROOF:** A Hamiltonian chord subset can be analyzed via a permutation/circuit-smoothing representation, giving an exact dictionary for when the smoothing is one simple cycle of a prescribed length. This is more complete than choosing disjoint shortcut arcs, because interacting chords are essential.

For a chord of intersection degree $d$, the two fundamental cycle lengths are $d+2+2u$ and $d+2+2v$, where $u,v$ count noncrossing chords nested on the two sides. Unless one of $u,v$ vanishes, the closed neighborhood of that chord separates $I_C$. In particular, when $I_C$ is a cycle, every matching chord belongs to a 4-cycle.

**INTERNAL PROOF, odd-square theorem:** If a cubic graph contains an odd number of distinct squares such that every vertex belongs to an even number of those squares, *every one-round triangle expansion at an arbitrary set of vertices* contains a 4- or an 8-cycle. If the expanded set meets each square $Q$ in $t$, the lifted lengths fill $[4+t,4+2t]$; avoiding 4 and 8 requires $t=1$. Summing over an odd square family contradicts even vertex incidence. This yields an infinite class of nonplanar examples, including odd-cycle chord-interlacement cores under one round of triangle expansions.

The theorem has genuine infinite-family content, but is silent on high-girth cubic graphs and arbitrary repeated expansions. Specialist novelty review remains necessary.

# 4. New continuation: resilience ceiling and bridge census

## 4.1 Universal resilience ceiling (current-chat internal proof)

**THEOREM.** Let $G$ have $n$ vertices and $m$ edges, and let $q$ be its shortest dyadic cycle length. Then

$$\boxed{\rho(G)\le\frac{m(n-q)}{2nq}}.$$

If $G$ is cubic, $m=3n/2$, so

$$\boxed{\rho(G)\le\frac{3(n-q)}{4q}}.$$

**Proof.** Take any nonzero nonnegative weights $w_C$ on dyadic cycles. Every weighted cycle has at least $q$ vertices and $q$ edges. Double-count vertex and edge incidences:

$$n\alpha\ge qW,\qquad m\beta\ge qW.$$

Therefore,

$$\frac{W-\alpha}{2\beta}\le
\frac{W(1-q/n)}{2qW/m}
=\frac{m(n-q)}{2nq}.$$

Take the supremum. $\square$

**Consequence.** In a cubic graph, the sufficient bridge certificate $\rho>1$ can occur only when $n>7q/3$. For $n=24$ and $q=16$, $\rho\le3/8$. The certificate can therefore fail even in very root-robust graphs rich in dyadic cycles; the low-resilience regime is large and structurally important. This is a bound on this *specific proof certificate*, not a proof that any bridge destroys root robustness.

## 4.2 Published 24-vertex near-misses tested in the continuation

**COMPUTED:** Four 24-vertex cubic near-misses originally associated with Markström, each avoiding 4- and 8-cycles while containing 16-cycles, were tested for rooted dyadic-cycle coverage. The continuation reported no root-critical vertex among the four, with $\rho=3/8$ for one graph and $\rho=1/3$ for the other three. A fresh run of the finite-cycle/LP verifier gave 315, 330, 207, and 228 dyadic cycles respectively, with the first graph attaining the universal $3/8$ ceiling. The verifier uses exact 4/8/16 cycle enumeration plus a SciPy linear program; it is computational corroboration rather than a symbolic proof of the LP optimum. The universal $3/8$ ceiling itself is proved without computation.

## 4.3 Order-16 class generation and rooted census

**COMPUTED, local workspace:** A graph constructor began with the two 8-vertex cyclically four-connected ladder classes, added the 10-vertex prism, Möbius ladder, and Petersen graph, then generated disjoint-edge bridges with graph isomorphism deduplication based on trace fingerprints and exact NetworkX isomorphism tests. The resulting counts and rooted results in `prime_census.log` are:

| Vertices | Distinct generated classes | Classes with root-critical vertex |
|---:|---:|---:|
| 8 | 2 | 0 |
| 10 | 5 | 0 |
| 12 | 18 | 0 |
| 14 | 84 | 0 |
| 16 | 607 | 0 |

These counts agree with the earlier project's small prime-class census and with the expected construction counts, but the local script is a research enumerator, not a separately published enumeration certificate. Its completeness for the asserted graph class rests on the bridge characterization and faithful application of its hypotheses.

## 4.4 Order-18 bridge-child scan: exactly what was tested

**COMPUTED, local workspace:** The file `bridge18.log` records a completed scan from the 607 order-16 graphs. For each pair of vertex-disjoint edges, the program constructs the 18-vertex bridged child. It first checks whether *untouched* parent dyadic cycles already avoid each candidate root; only exceptional root cases trigger a fresh fixed-length DFS for 4-, 8- or 16-cycles.

| Quantity | Recorded result |
|:---|---:|
| Parent graphs | 607 |
| Disjoint-edge bridge pairs examined | **138,396** |
| Bridge operations requiring at least one root repair | **5,137** |
| Exceptional root/bridge instances | **6,508** |
| Repairs found using a 4-cycle | 2,821 |
| Repairs found using an 8-cycle | 3,687 |
| Root-critical child instances found | **0** |

Of the 6,508 exceptional root/bridge instances, a separate classification log assigns 6,456 to cases admitting both a new-bridge-path and shifted-parent-cycle repair, 24 to shifted-cycle-only repairs, and 28 to path-only repairs. The classification is relative to the program's enumerated witness types; it is not a universal theorem. An independent NetworkX directed-cycle check was **re-run successfully** on 80 randomly sampled children. That independent sample is much smaller than the full census.

**Scope caution:** These are bridge operations from the generated order-16 collection, not a formally established exhaustive list of all cyclically four-connected 18-vertex graph isomorphism classes. The Kingan--Kingan characterization has named exceptions and cycle-spread conditions, and those must be reconciled explicitly with this constructor before promoting the result to a complete order-18 theorem. Even a complete finite theorem at 18 vertices would fall short of the external 48-vertex cubic existence frontier; the distinctive contribution here is rootedness, which is stronger.

# 5. What has been refuted or superseded

1. **Universal positive bound for the old $\Phi$ score:** parity-gapped terminal spectra in bipartite prime-like components make the score strongly negative. The invariant remains only a sufficient local test.
2. **Every repair is a bridge path:** false by explicit prime shifted-cycle-only examples.
3. **Every repair is a shifted parent cycle:** false by explicit prime path-only examples.
4. **Three-vertex-connectivity implies rooted bridge stability:** false for a bridged triangular prism.
5. **Fractional resilience increases under prime bridging:** false; it can decrease.
6. **One external ear always repairs a rooted dyadic cycle:** false on the Petersen graph.
7. **Positive independent increments with complete subset-sum sequence always exist:** false for the stated strict Petersen ear model.
8. **Large numbers of attainable lengths, broad endpoint windows, modular coverage, or many local theta switches alone force a dyadic cycle:** false as general arguments; exact scale and residue alignment are necessary.
9. **High girth plus three-connectivity forces macroscopic Hamiltonian chord spans:** false by the bounded-span replacement family.
10. **The proposed 2026 Zenodo proof resolves Erdős–Gyárfás:** rejected/withdrawn after defects and an acknowledged reduction with unresolved cases; no published solution is accepted here.
11. **Exhaustive computational elimination at orders 32--38:** previous repository audit did not support the broad claims; they must not be reused as established evidence.

A failed approach may still contribute reusable identities and certificates. Its negative result is an important research output in its own right.

# 6. Strategic comparison and open problems

## 6.1 Primary: low-resilience exchange/renewal under eligible bridging

**OPEN TARGET.** Let $G$ be a root-robust cyclically four-edge-connected cubic graph and $B(G;e,f)$ an admissible prime bridge. In the difficult region $0<\rho(G)\le1$, can cyclic connectivity force one of the four predecessor configurations for *every* old or new root? Even stronger, is the rooted prime conjecture true at all orders?

The exact dual indicates a possible route: a low fractional edge-plus-vertex cover of dyadic parent cycles may force alternative near-dyadic endpoint paths or a shifted cycle under the no-small-cyclic-cut hypothesis. However, no theorem currently derives a useful detour from such a fractional cover. The project should seek a genuine **low-resilience exchange lemma** and try to falsify it on snarks, large-girth primes, and the 24-vertex near-misses before building an induction around it.

The induction need not require every eligible bridge to preserve root robustness. An *existential unbridging* that chooses a favorable predecessor at each step might suffice, depending on a precise invariant and the Kingan--Kingan construction.

## 6.2 Secondary: compatibility, scale, and exact correction

**OPEN TARGET.** Prove that a nontrivial class of sparse, highly connected graphs supports enough compatible reroutings to create a dyadic coefficient in some rooted switching polynomial, or a sequence of overlapping exact length windows that necessarily crosses a power-of-two boundary. The key issue is a *graph-theoretic source* of switches with useful absolute scale and parity, rather than the elementary subset-sum algebra after the switches have been found.

This program builds on Lyngsie--Merker's theta/wiggly-necklace infrastructure, the multiscale path constructions of Bucić--Gishboliner--Sudakov, and the exact-length correction machinery of Liu--Montgomery. It could yield valuable theorems even without fully resolving Erdős–Gyárfás.

## 6.3 Tertiary: separator induction and falsification

The precise 3-cut transfer remains necessary for carrying a prime theorem to nonprime cubic graphs; one must control cycles through artificial cap vertices. For noncubic minimal counterexamples, the general defect/high-degree reductions remain incomplete. In parallel, exact boundary signatures should continue testing graph substitutions and lifts for actual dyadic-free counterexamples; the conjecture may be false.

## 6.4 Decision gates for the next pass

- **Root robustness stress test:** Check large known prime/snark/high-girth cubic instances for a root-critical vertex. A single counterexample invalidates the proposed rooted induction target, though the original conjecture may remain true.
- **Bridge completeness audit:** Prove that the order-16 generation matches precisely the intended prime class; include all Kingan--Kingan exceptions when interpreting order-18 scans; re-run independent oracle checks on a defined statistically and structurally meaningful sample.
- **Low-resilience mechanism:** Formulate a falsifiable exchange lemma quantified over selected bridge pairs and roots. Require a proof of the implication from connectivity/fractional cover to the appropriate predecessor length, not a definition restating the desired dyadic cycle.
- **Literature novelty check:** Compare the resulting lemma with cycle-length packing, chord diagram/interlace polynomials, fractional packing-covering duality, and established graph minors/ear decomposition techniques.
- **Publication threshold:** Claim a substantial advance only for a new infinite graph class outside stronger known coverage, a genuinely useful structural reduction, or a theorem creating a reusable forcing mechanism.

# 7. Known literature and external benchmarks

The references below are ordinary research citations for checking scope and novelty. They do not retroactively validate every internal proof.

- **[R1]** Ducoffe, G. & Dumitru, B. (2026), *Towards a more structured search for Erdős–Gyárfás counter-examples*. https://arxiv.org/abs/2609.28594 . External minimal-counterexample restrictions and finite verification limits.
- **[R2]** Kingan, R. J. & Kingan, S. R. (2024), *On cyclically 4-connected cubic graphs*, AKCE International Journal of Graphs and Combinatorics. https://doi.org/10.1080/09728600.2024.2333397 . Structural bridging characterization.
- **[R3]** Bucić, M., Gishboliner, L. & Sudakov, B. (2022), *Cycles of many lengths in Hamiltonian graphs*, Forum of Mathematics, Sigma 10:e70. https://doi.org/10.1017/fms.2022.42 . Nearly linear count of distinct lengths.
- **[R4]** Liu, H. & Montgomery, R. (2023), *A solution to Erdős and Hajnal's odd cycle problem*. https://arxiv.org/abs/2010.15802 . Expansion and long even-cycle intervals under sufficient average degree.
- **[R5]** Lyngsie, K. S. & Merker, M. (2021), *Cycle lengths modulo k in large 3-connected cubic graphs*, Advances in Combinatorics. https://doi.org/10.19086/aic.18971 . Modular length and theta-necklace methods.
- **[R6]** Heckman, C. & Krakovski, B. (2013), *Erdős–Gyárfás Conjecture for Cubic Planar Graphs*, Electronic Journal of Combinatorics. https://doi.org/10.37236/3252 . Cubic planar case.
- **[R7]** Garcia (2026), *Small graphs without power-of-two cycles*. https://arxiv.org/abs/2609.04686 . Finite constructions and replacement/window calculus.
- **[R8]** Burkhart, M. C. (2026), *Odd-Ordered Cayley Graphs Satisfy Erdős–Gyárfás*. https://arxiv.org/abs/2611.05060 . Cayley graph results and finite nilpotent corollary.
- **[R9]** Friedman, J. & Krivelevich, M., *Cycle lengths in expanding graphs*. See discussion and reference trail in the archived final literature review; precise publication metadata should be checked prior to use.
- **[R10]** Traldi, L. (2011), *Binary nullity, Euler circuits and interlace polynomials*. https://doi.org/10.1016/j.ejc.2011.02.004 . Chord/circuit algebra context.

# 8. Source map and reproducibility index

The companion source archive preserves the materials underlying this synthesis. The key names are:

| Source in archive | Main contents |
|:---|:---|
| `past_chat_final_review.txt` | Final uploaded prior-conversation literature assessment. |
| `july_project_brief.pdf` | July 30 chronological theorem/computation history, with older status. |
| `erdos64-research-eleven-passes.patch` | November patch snapshot with source notes, code, tests, graph6 catalogs, JSON certificates. |
| `notes/bridge_prime_reduction.md` | Exact bridge-cycle transfer and root conditions. |
| `notes/bridge_resilience_potential.md` | Fractional resilience theorem, dual LP, ladder descendants and counterexamples. |
| `notes/three_cut_prime_transfer.md` | Exact three-cut composition and certified-width sufficient test. |
| `notes/boundary_linkage_composition.md` | General edge-cut boundary signatures. |
| `notes/switching_spectrum_necessity.md` | Independent switches, rooted polynomial and Petersen obstruction. |
| `notes/theta_subset_sum_and_scale_obstruction.md` | Exact theta cancellation, subset-sum switches and long dyadic-free subcubic necklaces. |
| `notes/ambient_completion_barrier.md` | Global chord-interlacement and bounded-span counterexample. |
| `notes/interlacement_parity_frontier.md` | Exact chord smoothing, separator dichotomy and odd-square theorem. |
| `continuation/prime_census.log` | Generated order-8--16 class counts and rooted checks. |
| `continuation/bridge18.log` | Completed 138,396 bridge-child scan and finite root-repair counts. |
| `continuation/repair_classification.log` | Counts of shifted-only, path-only, and joint repairs. |
| `continuation/*.py` | Scripts used in the interrupted pass, including the resilience LP bound tests and bridge scans. |

The archived source code can be executed in a suitable Python environment with NetworkX, NumPy, SciPy, and pytest, subject to the exact dependencies and versions of the earlier workspace. Some archived patch tests have not been re-executed in the present response. The `.patch` snapshot includes precompiled Python cache files, which are unnecessary for verification; the companion zip omits them when storing extracted sources.

# 9. Consolidated status ledger

| Question or result | Present status | What is needed next |
|:---|:---|:---|
| Original Erdős–Gyárfás conjecture | **OPEN** | A global existence proof or a counterexample. |
| Minimal-counterexample two-thirds cubic proportion | **EXTERNAL** | Use the published statement with precise assumptions. |
| Exact 3-cut and bridge cycle formulas | **INTERNAL PROOF** | Literature novelty audit; compose into forcing lemmas. |
| General boundary-linkage calculus | **INTERNAL PROOF** | Find compact sufficient invariants. |
| Fractional resilience and bridge survival | **INTERNAL PROOF** | Low-resilience renewal theorem. |
| Universal resilience ceiling | **CURRENT-CHAT INTERNAL PROOF** | Referee for novelty and usefulness. |
| Odd-square one-round expansion theorem | **INTERNAL PROOF** | Extend to broader families / repeated expansions. |
| Theta exact cancellation | **INTERNAL PROOF** | Force absolute scale and alignment in cubic completion. |
| Arbitrarily long dyadic-free subcubic theta necklaces | **INTERNAL PROOF** | Exploit missing degree-three connections in ambient graph. |
| Rooted prime conjecture | **OPEN** | Test larger primes and attempt structural proof. |
| Order-16 generated prime-cubic rooted census | **COMPUTED** | Audit completeness/cycle oracle independently. |
| Order-18 bridge-child rooted scan | **COMPUTED** | Establish coverage of all eligible classes, add independent certificates. |
| Claimed general order-32--38 eliminations | **NOT ACCEPTED** | Rebuild a replayable complete certificate before citing. |
| Universal low-resilience exchange theorem | **OPEN** | Falsifiable formulation and proof or explicit counterexample. |

---

**Bottom line.** This research has produced a coherent vocabulary and several exact transfer/obstruction results, with credible finite tests. The strongest potential lies in proving a theorem that converts cubic connectivity and low cycle-family resilience into an exact dyadic-length repair. The present record deliberately stops short of asserting that such a theorem, or the original conjecture, has been proved.
