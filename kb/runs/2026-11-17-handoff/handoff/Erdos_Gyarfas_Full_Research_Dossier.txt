# Erdős–Gyárfás conjecture: complete research dossier from this conversation

**Compiled:** 17 November 2026  
**Purpose:** A self-contained handoff to another mathematician or AI model. The accompanying archive contains the actual scripts, graph6 inputs, machine-readable outputs, and earlier research notes.  
**Status:** **THE FULL CONJECTURE IS NOT PROVED HERE.** The dossier records finite checks, several restricted structural propositions with arguments, some conditional computer-assisted bounds, counterexamples to *stronger auxiliary claims*, the research changes of direction, and the final unresolved proof obligation. We do not claim mathematical novelty or peer review.

---

## 0. Read this first: evidence labels and essential conclusions

- **[LITERATURE]** is a statement supported by a cited external work; it is not a new result from this chat.
- **[DERIVED]** is a mathematical argument given in the research notes. Some have short self-contained proofs here; the larger pentagon/gadget proofs have *not* been professionally refereed.
- **[COMPUTED]** is an exact bounded calculation on stated inputs. A result for a small explicit list is **not** a complete census of a wider graph family.
- **[RECHECKED 17 NOV]** means I ran the relevant archived executable or independent verification script while compiling this dossier.
- **[UNRESOLVED]** is a question we did not answer, or a result whose provenance/completeness is unverified.
- **[REFUTED AUXILIARY CLAIM]** means a stronger formulation was disproved without disproving the original Erdős–Gyárfás conjecture.

### One-paragraph status

The Erdős–Gyárfás conjecture asks whether every finite simple graph of minimum degree at least three contains a simple cycle of length 4, 8, 16, 32, ... . The work began with a planned rooted-cycle audit of the reported 251 connected cubic graphs on 28 vertices avoiding C4 and C8; the full authenticated 251-record dataset was not obtained, so no exhaustive order-28 rooted classification was performed. We implemented and independently checked rooted cycle oracles on smaller controls, quantified cycle transversals in the Coxeter graph, developed a seven-vertex three-port gadget and a cycle-length interval mechanism, derived restricted cubic structural restrictions, found a higher-degree obstruction to a proposed short-cycle theorem, and independently re-executed a finite enumeration supporting a modest edge bound for dyadic-cycle-free minimal counterexamples. The most compact exact restatement of the remaining problem is an *unproved three-terminal path-length forcing lemma*. It is equivalent to the original conjecture, not an easier theorem that has been proved. Literature checking revealed that the gadget-window method has significant precedent in 2014 and September 2026 papers.

### Best independently reproduced bounded outputs from the archived files

| Check | Result | Scope |
|---|---|---|
| C++17 exhaustive enumeration | 2,097,152 labeled graphs on 7 vertices; 163,440 C4-free 2-degenerate; maximum 9 edges; 6,615 at 9 edges | All labeled 7-vertex graphs. Recompiled and rerun for this dossier |
| 8-to-9 vertex extension check | 15,120 labeled 8-vertex extremal extensions with 11 edges; **zero** permitted 9th-vertex degree-two extensions | Exhaustive for the enumerated equality configurations; rerun |
| Independent 8-vertex candidates | `GxaGiC`, `GgqPi_`; every one of 28 possible two-neighbor extensions forms C4 or C8 | Two representatives; independent Python script rerun |
| Coxeter graph | 21 distinct C8; 609 distinct C16; minimum C8 transversal 6; minimum C16 transversal 5 | Single labeled 28-vertex graph; independent verifier rerun |
| Inflated K4 | 28 vertices, 42 edges, four C3, twelve C5, zero C4/C8, four explicit rooted C16 certificates | Single explicit construction; independent verifier rerun |
| Inflated Petersen | 70 vertices, 105 edges, ten C3, thirty C5, zero C4/C8, explicit C16 witness | Single explicit construction; independent verifier rerun |
| Line-graph construction | 165 vertices, 330 edges, 4-regular; each edge triangular; no C4 or C8 | Single explicit counterexample to *higher-degree extension*; independent verifier rerun |
| Rooted-cycle example | 18 vertices, connected cubic, 27 edges; one specified vertex lies on no dyadic cycle; C4 elsewhere | Explicit counterexample to *every-vertex rooted property*; verifier rerun |

**Independent checking is relative to implementation:** The 7-vertex C++ program enumerates every labeled input and yields checkable output, but it is not a formal proof certificate in a proof assistant. A new researcher should review its code and ideally create a second complete enumerator.

---

## 1. Statement, notation, and why this is difficult

Let `G` be finite, simple, undirected, with minimum degree `delta(G)`. Let `C_l` denote a simple cycle of length `l`, with non-induced cycles allowed. The conjecture is

> `delta(G) >= 3` implies `G` contains `C_(2^k)` for some integer `k >= 2`.

Equivalent elementary reformulation: **Every graph without any dyadic cycle is 2-degenerate**. A graph is 2-degenerate when every nonempty subgraph has a vertex of degree at most two, equivalently it admits a vertex elimination ordering in which the removed vertex has at most two neighbors remaining. If a dyadic-free graph were not 2-degenerate, one of its subgraphs would have minimum degree at least three and would contradict the conjecture, and vice versa. **This equivalence alone makes no proof progress.**

A counterexample of least order, then least edge count, has a proper-subgraph minimality condition: no proper subgraph can have minimum degree >=3, since such a subgraph would also avoid dyadic cycles. In particular every vertex-deletion is 2-degenerate. This minimality and its consequences are already present in the literature.

**External work framing the research:**

1. Markström (2004), *Extremal graphs for some problems on cycles in graphs*, reports 4, 23, and 251 connected cubic C4/C8-free graphs at orders 24, 26, and 28, respectively. The count was cited as background, not independently reproduced.
2. Hegde, Sandeep, Shashank (2025 version, arXiv:2410.22842) prove the conjecture for graphs with no induced P13; they also show that P12-free graphs of minimum degree three have C4 or C8. Any counterexample has an induced P13. This corrected an earlier focus on the weaker P10-free result (Hu and Shen).
3. Ducoffe and Dumitru (arXiv:2609.28594, September 2026) prove a minimal counterexample is 2-edge-connected, has `|E| <= 2n-2`, has more than two-thirds cubic vertices, and has every edge on some C_(2^k+1). Their paper reports computational verification through orders 40 (general), 48 (cubic), and 66 (bipartite). These bounds are their reported results; the full searches were not rerun here.
4. Daniel Garcia (arXiv:2609.04686, September 2026) reports certified C4/C8-free minimum-degree-three lower bounds through 23 vertices, a correction to Exoo's construction, and an existing exact gadget-window calculus that includes a symmetric seven-vertex gadget with port path lengths 2 through 6. This substantially limits the novelty of our gadget method.
5. Julius Tranquilli (arXiv:2608.02675) reports a certified cubic-bipartite result through 58 vertices.
6. Avery Carr (arXiv:2605.22844) proved a 4/7 lower bound on the proportion of degree-three vertices in a minimal counterexample, subsequently strengthened by Ducoffe–Dumitru.
7. Nowbandegani et al. (2014), *On the Erdős–Gyárfás conjecture in claw-free graphs*, already employ related local path-expansion reasoning for cubic claw-free graphs.

These references and exact links appear in section 13.

---

## 2. Research stage I: proposed 251-graph order-28 rooted census

### 2.1 Objective

The initially targeted claim was stronger than Erdős–Gyárfás. For each connected cubic graph `G` of order 28 with no C4 or C8, and each vertex `v`, ask whether there is a C16 *avoiding `v`*. A further proposed restriction focused on 3-vertex-connected and cyclically four-edge-connected cubic graphs, called the “prime” class in internal notes.

The **251** is a reported number of graphs, **not** the number that we obtained or processed. The complete graph6 file containing all 251 nonisomorphic graphs was not retrieved or independently generated. Consequently:

- **No exhaustive rooted result for the 251 was established.**
- No claim that zero, some, or all of the 251 are cyclically four-edge-connected was established.
- No claim that all possible roots in the 251 have an avoiding C16 was established.

### 2.2 Exact rooted C16 algorithm

`EG28_Rooted_Audit_Packet.zip` contains `verify_g6.py`. A simple C16 exists exactly when some endpoints have **two internally vertex-disjoint simple length-eight paths** between them. The meet-in-the-middle (MITM) algorithm enumerates length-eight paths, groups by endpoints, and tests interior intersections using bitmasks. The packet also uses an independently implemented bounded DFS as an oracle for each positive/negative test on controls. A positive answer is backed by a literal vertex-list cycle, verified edge-by-edge.

The intended census command is:

```bash
python verify_g6.py complete_28_C4_C8_free.g6 --expect-count 251 --strict --output order28_results.json
```

The `complete_28_C4_C8_free.g6` input was **never obtained**. Even providing a file of 251 lines would not alone certify that it contained the complete nonisomorphic family; provenance and an independent generator/count or canonical checks would still be necessary.

### 2.3 Exact control calculations

The six controls comprised K4, Petersen, and four 24-vertex C4/C8-free near-miss graphs (provided as graph6, not regenerated from scratch). On 64 test rooted C16 queries, the separate MITM and bounded-DFS oracles agreed. The four 24-vertex controls each have a C16 avoiding any individual vertex, but none is cyclically four-edge-connected. The 24-vertex family’s completeness comes from the cited census, not our own census.

All 96 single vertex-to-triangle expansions (`4 controls × 24 vertices`) were also checked. None remains simultaneously C4-free and C8-free: 12 gained only C4, 36 gained only C8, and 48 gained both. This only rules out a particular local growth operation from those four starts; it does not classify order 26 or 28.

### 2.4 Correction to “prime” / cyclic connectivity classification

An early classifier incorrectly **required triangle-freeness by definition** in addition to 3-connectivity and absence of cyclic edge cuts of size <=3. The standard cyclically four-edge-connected condition does not include triangle-freeness. K4 is 3-connected and cyclically four-edge-connected (under the standard nontrivial cyclic-cut definition), but all its 4-cycles use all four vertices. It disproves the unqualified statement that every root of every cyclically four-edge-connected cubic graph can be avoided by a dyadic cycle. This does **not** disprove the original Erdős–Gyárfás conjecture.

For a *connected cubic graph with at least six vertices*, a triangle gives a cyclic three-edge cut, so it cannot occur in a cyclically four-edge-connected example. This observation justifies triangle-freeness as a **derived property in that restricted setting**. The corrected code removes the definitional triangle-free filter. The six-control results became: K4 prime/root-critical; Petersen prime/root-robust (it has C8); four 24-vertex C4/C8-free graphs neither prime nor rooted-critical.

### 2.5 Why the census was deprioritized

The underlying conjecture is unrooted and general minimum-degree-three; the stronger rooted prime conjecture could fail for reasons unrelated to the general question. Once it was clear that the complete 251 graph inputs were unavailable, repeating small rooted calculations offered diminishing returns. We preserved the code as a falsification harness for stronger lemmas and shifted to structural forcing.

---

## 3. Research stage II: exact cycle transversals

For fixed `l`, let `H_l(G)` be the hypergraph whose hyperedges are vertex sets of all simple l-cycles in `G`. Define the transversal number `tau_l(G)` as the smallest vertex set meeting every l-cycle. If `tau_l >= 2`, every single vertex can be avoided by some l-cycle; if `tau_l >= s+1`, every vertex set of size at most s can be avoided by some l-cycle.

### 3.1 Four 24-vertex near-misses

Archived exact undirected-cycle counts and transversal sizes:

| Control | Number of C16 | Min C16s avoiding one vertex | Max C16s avoiding one vertex | `tau_16` | Number of minimum transversals |
|---|---:|---:|---:|---:|---:|
| #1 | 315 | 83 | 131 | 3 | 61 |
| #2 | 330 | 74 | 135 | 2 | 3 |
| #3 | 207 | 49 | 84 | 2 | 2 |
| #4 | 228 | 43 | 93 | 2 | 9 |

These are four supplied graphs, not all C4/C8-free cubic graphs. Their triangle content makes them irrelevant as direct prime counterexamples.

### 3.2 Coxeter graph (28 vertices)

Using the graph6 labeling archived in `EG_Run3_Coxeter_Transversal.zip` and `EG_Run4_Research_Packet.zip`:

- Distinct C8: **21**. Minimum hitting-set size `tau_8 = 6`. Example: `{0,1,3,6,9,14}`.
- Distinct C16: **609**. Minimum hitting-set size `tau_16 = 5`. Example: `{0,1,3,9,15}`.
- Minimum transversal meeting every C8 **or** C16: **6**; the displayed C8 witness also hits every C16.
- **[RECHECKED 17 NOV]** `independent_transversal.py` reproduced the 21 and 609 distinct vertex sets and minimum transversals 6 and 5.

The Coxeter graph contains C8, so it is **outside** the 251 C4/C8-free target. Its value is as a test for stronger multiple-root cycle-avoidance claims.

### 3.3 General elementary observation (not a new discovery)

If a vertex-transitive graph on `n` vertices has a cycle of length `l`, then for any fixed set `S` of vertices with `|S| * l < n`, some automorphic image of that cycle avoids `S`. Proof: a uniformly random automorphism of the cycle has expected intersection `|S|*l/n < 1`, so some image has zero intersection. On Coxeter this guarantees avoidance of sets of size at most 3 for C8, while enumeration improves it to 5. This elementary observation was not claimed as original.

---

## 4. Research stage III: pentagons and the seven-vertex gadget

### 4.1 Local pentagon-overlap lemma (derived in an archived mathematical argument)

In a **cubic graph of girth at least five with no C8**, the research note argues:

- Two distinct 5-cycles are vertex-disjoint or intersect in precisely a common path of length two (three vertices).
- A vertex belongs to at most two 5-cycles.
- A 5-cycle meets at most one other 5-cycle.
- The union of all edges on 5-cycles has components that are either isolated pentagons (5 vertices, 5 edges) or two pentagons sharing a two-edge path (a theta graph with 7 vertices and 8 edges).

Sketch: Two pentagons meeting at one edge and otherwise disjoint create a C8 by taking their two length-four complementary paths. Overlaps of greater size create a C4 or identical cycles. Cubic degrees constrain triples of pentagons at a vertex, and the remaining possible arrangement forces a triangle, forbidden by girth five. Full local case argument and finite overlap checks appear in `EG_Proof_Route_Short_Cycle_Theorem.zip` (`RESEARCH_NOTE.md` and `pentagon_local_exhaust.py`). **The mathematical proof has not received external referee review.**

### 4.2 Short-cycle edge-cover theorem (derived)

**Claim with proof in archived note:** If a cubic graph has every edge on a triangle or pentagon, it contains a C4 or C8. Equivalently, a cubic graph avoiding C4 and C8 has at least one edge lying on neither C3 nor C5.

**Triangle-free case.** If every edge is covered by a pentagon, then at each cubic vertex at least two pentagons are needed, while the overlap lemma permits at most two. A fixed pentagon’s five vertices would have to be partitioned into disjoint overlapping groups of three by its partner pentagons, an impossibility (`3` does not divide `5`).

**Triangle-containing case.** With no C4, triangles are disjoint. If all three edges leaving a triangle are on pentagons, two such pentagons must force a seven-vertex subgraph with three ports (below), or yield a C8. A remaining external port edge can lie on neither a triangle nor a pentagon because an external return path of length <=3 to another port would create C4 or C8. That contradicts complete C3/C5 edge coverage.

The proof is specific to cubic graphs. It has not been extended to minimum degree three without an upper-degree restriction. The script `theorem_checks.py` used 180 randomized small cubic falsification cases plus named controls; those tests are supplemental, not a proof of all cubic cases.

### 4.3 Three-port gadget T

Seven vertices `a,b,c,w,x,y,z` with the edges:

```text
a-b, b-c, c-a,
a-x, b-y, c-z,
w-x, w-y, w-z
```

The ports are `x,y,z`. The four vertices `a,b,c,w` have degree three within T; the three ports each have degree two internally and exactly one external attachment in a cubic host.

For every unordered pair of distinct ports, there are internally simple paths of **each length 2, 3, 4, 5, 6**. For instance, from `x` to `y`:

```text
length 2: x-w-y
length 3: x-a-b-y
length 4: x-a-c-b-y
length 5: x-a-c-z-w-y
length 6: x-a-b-c-z-w-y
```

**Novelty warning:** Garcia’s 2026 paper already studies a symmetric seven-vertex vertex-replacement gadget `H7'` with the same port path-length spectrum, as part of a more general window calculus. Similar expandable-cycle arguments appear in 2014 claw-free work. We do not claim to have invented this technique.

### 4.4 Ring/path-window forcing theorem (direct argument)

Suppose `q >= 3` vertex-disjoint T gadgets are encountered cyclically, with pairwise internally vertex-disjoint connector paths whose total edge length is `B`, using two different ports in each gadget and no internal connector vertex in another chosen gadget. Each gadget traversal can independently have length 2 through 6; therefore the host graph has simple cycles of **every integer length** in:

```text
[B + 2q, B + 6q]
```

If `B <= 2q`, the interval ends at least twice as far as it starts; any interval `[m,2m]` contains a power of two. Thus such a dense ring of flexible gadgets forces a dyadic cycle.

For a cubic base graph `H`, replacing every vertex by T yields `F(H)`. A base cycle of length `q` lifts to every length in `[3q,7q]`. In particular it forces at least one dyadic cycle. With only selected vertices replaced, a base cycle of length `L` containing `r` replaced vertices yields all lengths

```text
[L + 2r, L + 6r].
```

Therefore `2r >= L` forces a power-of-two cycle. The **critical unknown** is whether arbitrary minimal counterexamples must possess enough such adjustable vertices, or an alternative source of flexibility. Nothing established this globally.

### 4.5 Explicit constructions and finite checks

Replacing all four vertices of K4 with T gives a 28-vertex cubic C4/C8-free graph; replacing all ten vertices of Petersen gives a 70-vertex cubic C4/C8-free graph. `gadget_forcing.py` emits edges and cycles; `independent_verify.py` reads independently and checks them. **[RECHECKED 17 NOV]**:

| Graph | Vertices | Edges | C3 | C5 | C4 | C8 | Edges not on C3/C5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| F(K4) | 28 | 42 | 4 | 12 | 0 | 0 | 6 |
| F(Petersen) | 70 | 105 | 10 | 30 | 0 | 0 | 15 |

The 28-vertex construction comes with four C16 certificates, each avoiding all seven vertices of a selected gadget. A sample C16 in the package's numbering:

```text
13, 9, 7, 8, 12, 19, 15, 14, 16, 20, 27, 23, 21, 25, 24, 26
```

The 28-vertex construction is a concrete member of the *property-defined* C4/C8-free cubic class. It has **not** been matched to a verified member of an authenticated 251-record census.

---

## 5. Research stage IV: structural restrictions on hypothetical cubic counterexamples

These results depend on the gadget/pentagon structural lemmas above and are **conditional restrictions**, not proofs that minimal counterexamples contain these gadgets.

### 5.1 Saturated-triangle interaction forest

A triangle in a cubic C4/C8-free graph is called **saturated** when its three edges leaving the triangle all lie on 5-cycles. The pentagon argument yields an embedded T gadget around it. In the archived proof, distinct saturated T gadgets are disjoint; loops or double edges between their ports produce C4 or C8. Construct an interaction graph `Q`: one vertex per saturated gadget, with an edge when two gadgets' ports have a direct external edge between them.

**Claim:** In a dyadic-cycle-free cubic graph, `Q` is a forest. A cycle of q gadgets would lift to all cycle lengths `[3q,7q]` and hence a dyadic cycle. With `t` saturated gadgets and `c` components, the forest has `t-c` edges, leaving exactly `3t - 2(t-c) = t+2c` unused port stubs that lead outside the gadget system.

This forbids cyclic *dense* interaction patterns. It says nothing if a hypothetical counterexample has no saturated triangles.

### 5.2 Perfect matching amplification and the `t < n/8` bound

**[DERIVED]** Let H be a **bridgeless cubic** base graph with N vertices. Replace a set S of its vertices by T gadgets. By Petersen’s perfect matching theorem, H has a perfect matching. Removing it gives a 2-factor (disjoint cycles covering all vertices). If `|S| >= N/2`, one of those cycles contains at least half marked vertices, so the weighted window theorem forces a dyadic cycle.

In a hypothetical *bridgeless cubic* dyadic-free G of order n with t disjoint saturated T gadgets, contracting the gadgets gives a bridgeless cubic base H of order `N = n-6t`. Since the inflated graph is presumed dyadic-free, one must have `2t < N`, hence

```text
8t < n.
```

No such density lower bound on t was obtained. In particular, a triangle-free cubic graph has t=0 and automatically satisfies this bound.

### 5.3 Pentagon-uncovered-edge density in triangle-free cubic graphs

**[DERIVED]** In a triangle-free cubic graph of order n with no C4 or C8, let `p5` count isolated-pentagon components of the union of pentagon edges, `p7` count seven-vertex paired-pentagon components, and `n0` count vertices in no pentagon. Then

```text
n = n0 + 5p5 + 7p7,
number of edges on pentagons = 5p5 + 8p7,
u = number of edges on no pentagon = (3n0 + 5p5 + 5p7)/2,
u - (5n/14) = (8n0 + 5p5)/7 >= 0.
```

Hence **at least `5n/14` edges are on no C5**. If such a graph were a smallest *general* counterexample, Ducoffe–Dumitru’s edge-saturation result would require each uncovered edge to lie on some C9, C17, C33, ... . This is an obstruction to *short* near-dyadic coverage, but it gives no contradiction.

### 5.4 Why local forcing cannot be naively generalized to higher degrees

We built a **165-vertex, 330-edge, 4-regular graph** in which every edge belongs to a triangle, but no C4 or C8 exists. Construction: take a specified 11-fold cyclic voltage lift of the Petersen graph with girth at least nine, then form its line graph. The voltage assignment and complete 330-edge list are in `EG_Run6_Flexibility_and_Obstruction.zip`.

**[RECHECKED 17 NOV]** `verify_high_degree.py` independently verified 165 vertices, 330 edges, degree four at every vertex, every edge on a triangle, and absence of C4/C8. This explicitly refutes the obvious statement “every graph of minimum degree at least three with every edge on a triangle or pentagon contains C4 or C8.” It **does not** refute Erdős–Gyárfás: the graph has other dyadic cycles.

### 5.5 Exhaustive sample family of partially inflated graphs

The Run6 packet enumerates all 16 marked subsets of K4 and six selected marked subsets of Petersen, with 22 literal dyadic-cycle witnesses, plus separate verification of the generated graph edges. This supports the path-window theorem on examples; it is not an exhaustive test over all cubic host graphs.

---

## 6. Research stage V: improved bounded edge-count lemma

This is the strongest *computer-assisted general bound* developed in the conversation. It is an incremental improvement to a published edge estimate, not remotely a proof of Erdős–Gyárfás.

### 6.1 Finite seven/eight-vertex calculation

`EG_Run7_Core_Bound_and_Audit.zip` contains `verify_complete_7.cpp`, `independent_bounds_verify.py`, graph6 certificates, and the proof note. Its standalone C++17 enumeration considers **all `2^21 = 2,097,152` labeled simple graphs** on seven fixed vertices, checks C4-freeness and 2-degeneracy, and finds:

```text
enumerated=2097152
eligible_C4free_2deg_7=163440
max_edges_7=9
eligible_edges9=6615
labelled_8vertex_11edge_extremals=15120
degree2_extensions_without_C4_C8=0
```

The 15,120 count refers to **labeled eight-vertex extensions with a distinguished last vertex**, not 15,120 isomorphism classes. The separate Python verifier checks the two reported eight-vertex graph6 representatives (`GxaGiC`, `GgqPi_`), each having 11 edges, and every one of 28 two-neighbor ninth-vertex attachments. The archived independent atlas-based check reports two eight-vertex isomorphism classes.

**[RECHECKED 17 NOV]** I recompiled `verify_complete_7.cpp` with `g++ -O3 -std=c++17` and reran it. Its complete output is identical to that above. I also reran `independent_bounds_verify.py`, confirming both representative checks. This is strong bounded evidence, conditional on program correctness and the classification proof; it is not an independently implemented second complete enumeration of the 2,097,152 seven-vertex graphs.

### 6.2 Finite lemma and induction

**Finite lemma:** Every 2-degenerate C4/C8-free graph on eight vertices has at most 11 edges. Every one with 11 edges is **saturated against adding a degree-two ninth vertex**, in the sense that attaching the new vertex to any two distinct existing vertices creates C4 or C8.

**Proof of the `N>=9` theorem (conditional on the finite lemma):** For a 2-degenerate C4/C8-free graph F on nine vertices, remove a vertex x of degree at most two. The eight-vertex remainder has at most 11 edges. If `d(x)<=1`, F has at most 12 edges. If `d(x)=2`, an F with 13 edges would have an eight-vertex 11-edge remainder and would violate the finite lemma's saturation property. Thus order nine has at most 12 edges. For larger N, repeatedly remove a vertex of degree at most two and use induction, adding back at most two edges each time. Therefore

```text
N >= 9, F 2-degenerate, C4/C8-free  ==>  |E(F)| <= 2N - 6.
```

**Corollary:** A graph G of order n>=10 with minimum degree three, no C4/C8, and no *proper* subgraph of minimum degree three has

```text
|E(G)| <= 2n - 5.
```

Choose a degree-three vertex v (one must exist by minimality). Then G-v is 2-degenerate, has n-1>=9 vertices, and no C4/C8, hence `|E(G)|-3 <= 2(n-1)-6`.

This improves the earlier `2n-2` general estimate reported in Ducoffe–Dumitru *for a smallest counterexample*. We have not established whether the exact `2n-5` bound is previously known elsewhere.

### 6.3 Conditional degree-three count improvement

Using the auxiliary simple, 2-degenerate graph M on high-degree vertices from Ducoffe–Dumitru Lemma 3.5, and assuming their reported verified general frontier through order 40, the Run7 proof derives

```text
number of degree-3 vertices >= ceil(2n/3 + 2)
```

for a hypothetical smallest counterexample of order n. The source establishes at least `2n/3+1`, so the derived integer lower bound increases the requirement by one vertex relative to the cited theorem. The argument splits into `h>=9` high-degree vertices, where the new bound `|E(M)|<=2h-6` applies, and `h<=8`, where `n>=41` makes the inequality automatic. The improvement is small and supplies no cubic reduction.

**Limit:** `2n-5` is still far above the edge count `3n/2` of a cubic graph when n is large; it cannot itself force a contradiction. The 8-vertex saturation cannot be repeatedly iterated to grow a further edge deficit without additional structure.

### 6.4 Reproduction

```bash
cd EG_Run7_Core_Bound_and_Audit
g++ -O3 -std=c++17 verify_complete_7.cpp -o verify_complete_7
./verify_complete_7
python independent_bounds_verify.py
```

A complete independently coded exhaustive enumeration of all 2^21 inputs would strengthen the computational certification further. The two Python representative checks are not that full second enumeration.

---

## 7. Research stage VI: equivalent three-terminal path-length problem

### 7.1 Exact unproved target

Let H be a finite simple **2-degenerate** graph with three distinct terminals `a,b,c`, with:

1. Every vertex outside `{a,b,c}` of degree at least three.
2. Each terminal of degree at least two.
3. No cycle of length `2^k`, for any `k>=2`.

**Three-terminal path forcing lemma (UNPROVED):** Some pair from `{a,b,c}` is joined by a simple path of length `2^k - 2` for some `k>=2`.

This has the right arithmetic. Add a new vertex v adjacent to all three terminals. A simple path of length `2^k-2` between two terminals closes with the two edges through v to form a cycle of length exactly `2^k`.

### 7.2 Why this lemma is logically equivalent to the original conjecture

**If the terminal lemma holds:** Suppose the original conjecture is false and take a counterexample G minimal by order and then edge count. A degree-three vertex v exists (otherwise deleting any vertex preserves minimum degree three). The graph H=G-v has all nonterminal degrees at least three and the three neighbors `a,b,c` of v each have at least two remaining neighbors. Every nonempty subgraph of H has degree <=2 somewhere, by minimality of G; hence H is 2-degenerate. It has no dyadic cycle. The lemma yields a terminal path of length `2^k-2`; adjoining v closes a dyadic cycle in G, contradiction.

**If the original conjecture holds:** Take any H satisfying the terminal hypotheses but containing no required path. Adjoin v joined to a,b,c. Every vertex of the augmented graph has degree at least three. Cycles avoiding v were already cycles of H (and so none are dyadic), while a dyadic cycle using v would require exactly one of the forbidden terminal paths. Thus the augmented graph would refute Erdős–Gyárfás. Contradiction.

Therefore the terminal lemma and the full conjecture are **equivalent**. This is a clean proof target, but the equivalence **does not lower the difficulty** or provide the needed path-spectrum forcing theorem. No one in this chat proved the lemma.

### 7.3 Limitation: deletion of a vertex from any connected cubic graph

For **every connected cubic graph**, deleting any vertex automatically leaves a 2-degenerate graph. If an induced subgraph of G-v had minimum degree three, since G was cubic every one of its vertices would retain all three G-neighbors within that subgraph, giving a proper connected component of G, impossible. Therefore the three-terminal formulation already contains the entire connected cubic difficulty. We must extract new arithmetic information from simple terminal-path lengths rather than relying on degeneracy alone.

### 7.4 A falsified rooted shortcut

The note `EG_shortest_path_audit.py` constructs a connected **18-vertex cubic graph** with a designated root on only a triangle. It consists of a central triangle with three bridges leading to identical five-vertex cubic-completion caps (each derived from K5 by deleting `(0,1),(0,2),(3,4)` and attaching at the unique degree-two vertex). Thus every cycle through the specified central root has length exactly three. The graph has C4 elsewhere, and hence is not a counterexample to Erdős–Gyárfás.

**[RECHECKED 17 NOV]** The script reports 18 vertices, 27 edges, connected cubic, all root-cycle lengths `[3]`, G-root 2-degenerate, and a C4 elsewhere. This refutes the proposed shortcut “every vertex of every connected cubic graph lies on some dyadic cycle”.

### 7.5 Other shortcuts rejected

- **Forcing any sufficiently large *number* of distinct cycle lengths** is inadequate: an arbitrary large set of attainable lengths can omit every power of two. Exact arithmetic control is essential.
- **An induced P13** is necessary in a counterexample by the cited theorem, but its existence alone does not specify where third incident edges reconnect or guarantee the required path lengths.
- **Triangle/pentagon gadget inventories** cannot cover all high-girth cubic graphs. High-girth regular graphs exist without any such local motifs.
- **A purely cubic proof** is not automatically a proof for all minimum-degree-three graphs. Hypothetical minimal counterexamples may contain degree four or higher; their majority being cubic does not eliminate the minority.
- **Parity must be respected:** in a bipartite graph, all paths between a fixed pair of vertices have a fixed parity. A universal full consecutive interval of terminal path lengths cannot hold in that setting. Any global path-spectrum theorem must allow parity-restricted progressions or combine different pairs.
- **Unrestricted prime rooted conjecture** was already refuted by K4; strengthened rooted claims should carry explicit size, girth, and connectivity hypotheses.
- **Gadget window calculus** has pre-existing published or posted versions; an extension must prove that flexibility is *forced* in general, not merely verify that flexibility works when present.

---

## 8. Earlier inherited ideas that did not become proof progress

The initial context preceding the present research packets included 3-cut cycle transfer identities, bridge predecessor tables, boundary signatures, and switching-polynomial bookkeeping. Those track how existing cycle lengths change across a decomposition but do not themselves force a length that is a power of two. Parent-to-child induction required parent cycles of particular nearby lengths (for instance Q, Q-1, Q-2, or a path of length Q-3), whereas an inductive hypothesis merely guaranteeing one dyadic cycle does not supply those stronger antecedents. The decision was to stop reporting exact bookkeeping as substantive advancement toward the full conjecture. No complete proof resulted from that line.

These inherited ideas are mentioned for continuity; the full prior scratchpad and dossier from previous conversations are **not** included among the supplied files here, so this section is a recap of the available conversational record rather than a full reconstruction of all prior experiments.

---

## 9. Proven, computational, sourced, and open: precise separation

### 9.1 Mathematical facts proved directly in this dossier or by short arguments

- Degeneracy formulation equivalent to Erdős–Gyárfás.
- Exact two-length-eight-path characterization of a C16.
- Exact relation between a three-terminal path of length `2^k-2` and a dyadic cycle through an added common neighbor.
- Equivalence of the **unproved** terminal forcing lemma to the original conjecture.
- Vertex-transitive automorphism average/avoidance bound `|S|*l<n`.
- Weighted cycle-window arithmetic `[L+2r, L+6r]` **for a graph already given as a suitable T-gadget expansion**.
- 2-factor/Petersen-theorem deduction that at least half marked gadgets in a bridgeless cubic base forces a dyadic cycle.
- Induction from the stated finite 8-vertex saturation lemma to `|E(F)|<=2N-6`.
- 18-vertex explicit rooted-cycle failure, as a graph-theoretic constructed counterexample verified by code.

### 9.2 Additional derived restrictions with mathematical arguments in archived notes (not independently refereed)

- Local pentagon-overlap classification under girth >=5, cubicity, and no C8.
- Cubic short-cycle edge-cover proposition: C3/C5 edge coverage forces C4 or C8.
- Disjointness of saturated-triangle gadgets, their interaction-forest obstruction, and `8t<n` in bridgeless cubic dyadic-free graphs.
- Triangle-free cubic C4/C8-free pentagon-uncovered-edge lower bound `5n/14`.
- Auxiliary degree-three vertex count improvement conditional on the finite lemma, Ducoffe–Dumitru Lemma 3.5, and the published search frontier.

These should be independently examined line-by-line before a research-paper claim is made. In particular, **priority searches and external referee checks were not completed**.

### 9.3 Exact computations with explicitly bounded scope

- Six rooted controls, including four 24-vertex graphs; 64 initial MITM-vs-DFS comparisons and subsequent control checks; 96 triangle-expansion trials.
- Four 24-vertex C16 cycle/transversal counts.
- Coxeter C8/C16 exact cycle counts, transversals, and witnesses.
- Inflated K4/Petersen explicit cycle checks and 22 marked-graph witnesses.
- 165-vertex 4-regular obstruction to the *higher-degree short-cycle coverage statement*.
- 2,097,152-case labeled 7-vertex enumeration and exhaustive 8-to-9 extension check.
- 18-vertex connected cubic rooted counterexample to the **unrestricted per-vertex** assertion.

### 9.4 Unresolved

1. The entire Erdős–Gyárfás conjecture.
2. The equivalent three-terminal path forcing lemma.
3. A theorem forcing suitable path-length spectra or enough independent reroutings in every minimal 3-core, including high-girth cubic and mixed-degree cases.
4. A complete authenticated 251-item 28-vertex C4/C8-free cubic dataset and exhaustive rooted/prime classification.
5. Whether the restricted structural lemmas and the finite edge-bound refinements are original, or already subsumed in prior literature.
6. Mathematical peer review of the more elaborate pentagon and gadget disjointness proofs, and independent reimplementation of the entire seven-vertex exhaustive enumeration.

---

## 10. Which direction emerged as the shortest defensible route?

**Target:** Prove the three-terminal forcing lemma in §7.1, or an independently strong structural theorem implying it. That is a *precise endpoint*, not a demonstrated shortcut. The likely missing ingredient is a **multiscale arithmetic path-spectrum theorem**: in a dyadic-free 2-degenerate graph whose nonterminal vertices already have degree >=3, some pair of the three terminals must have a simple path of length `2^k-2`. Conditions must work even when terminal path parity is constrained, in high-girth cubic graphs, and in minimal cores with some high-degree vertices.

A credible new proof attempt should first state a strictly stronger hypothesis that can be established independently (for example, a specified arithmetic progression of terminal path lengths or a reducible local configuration forced globally), then test it on the explicit obstruction families and current finite datasets. Merely asserting the equivalent terminal lemma again does not advance a proof.

**Why the research stopped:** Neither a universal path-spectrum theorem nor a globally forced adjustable-gadget structure was established. Presenting the local interval machinery, the small edge improvement, or the terminal equivalence as a full proof would overstate the work. There is no completed solution to submit.

---

## 11. Reproducibility: exact files and commands

The separate file `Erdos_Gyarfas_Research_And_Certificates.zip` packages this complete dossier and the original packet ZIPs intact. They are kept as original artifacts to preserve source code, graph6 strings, JSON, and version-specific notes. Extract any individual run packet before using its commands.

| Original file | Contents / role |
|---|---|
| `EG28_Rooted_Audit_Packet.zip` | Rooted 28-vertex test harness; six controls; independent MITM/DFS oracles; triangle expansions; **no 251 dataset** |
| `EG28_Cycle_Transversal_Audit.zip` | Exact C16 enumeration/transversal data for four 24-vertex controls |
| `EG_Run2_Corrected_Rooted_Audit.zip` | Removes mistaken triangle-free condition from cyclic edge-connectivity classifier |
| `EG_Run3_Coxeter_Transversal.zip` | Coxeter C8 cycle enumeration, C8 transversal six, verification scripts |
| `EG_Run4_Research_Packet.zip` | Coxeter C16 transversal five, combined transversal six, independent check |
| `EG_Proof_Route_Short_Cycle_Theorem.zip` | Pentagon-overlap reasoning, T gadget, local exhaustive cases, inflated K4/Petersen and certificates |
| `EG_Run6_Flexibility_and_Obstruction.zip` | Weighted windows, perfect-matching amplification, 165-vertex 4-regular obstruction, 22 certificates |
| `EG_Run7_Core_Bound_and_Audit.zip` | Complete 7-vertex enumerator, eight-vertex finite lemma, `2N-6` induction, degree-count derivation |
| `EG_shortest_proof_route.md` | Final proof target, decisions, references and limitations |
| `EG_shortest_path_audit.py` | Explicit 18-vertex connected cubic rooted counterexample to a stronger claim |

### Quick rerun of the best bounded certificate

```bash
unzip EG_Run7_Core_Bound_and_Audit.zip -d Run7
cd Run7
g++ -O3 -std=c++17 verify_complete_7.cpp -o verify_complete_7
./verify_complete_7
python independent_bounds_verify.py
```

### Coxeter cross-check

```bash
unzip EG_Run4_Research_Packet.zip -d Run4
cd Run4/EG_Run4
python independent_transversal.py
```

### Explicit constructed graphs and higher-degree obstruction

```bash
unzip EG_Proof_Route_Short_Cycle_Theorem.zip -d Gadget
cd Gadget
python independent_verify.py
cd ..
unzip EG_Run6_Flexibility_and_Obstruction.zip -d Run6
cd Run6
python verify_high_degree.py
```

### Rooted counterexample

```bash
python EG_shortest_path_audit.py
```

### Notes on full 28-vertex graph generation

No complete 251-record graph6 file is provided in any archived packet. The existence of a `--expect-count 251` checker flag is **not** evidence that the family was generated. No exhaustive rooted claim should be made on the basis of these artifacts alone.

---

## 12. Source and provenance caution

The chronology matters:

- Early in this chat a newer repository’s **through-40 cubic** claim was described as potentially the frontier. Later literature showed a historical Markström **through-52** unpublished/archived search may underlie the `f(4)>=54` bound; this was not independently authenticated from Markström’s complete raw logs. Still later the Ducoffe–Dumitru September paper explicitly reported **through 48 cubic** and **through 40 general**. Do not claim historical priority without reconciling the older 52 computation and what exact cycle exclusions each result tested.
- The 251 count has multiple secondary corroborations, but the exact 251 graphs were not acquired here.
- The 2026 external preprints include computer-assisted claims, which were verified at the level of their published abstracts/theorem statements in this dossier, not by rerunning their full SAT/DRAT searches.
- The restricted gadget path spectrum of 2...6 appears explicitly in Garcia, so the key length-window mechanism is not a verified original discovery from this conversation.
- A 2026 Zenodo upload claimed a complete proof, but an earlier review in the conversation considered the claim unsupported; we did not validate a full proof from it. Do not present that upload as a settled resolution.
- The user requested conceptual progress and a possible full proof; the research work attained useful checkable subresults, but its **central global forcing step was never proved**.

---

## 13. External literature and links (checked during compilation)

These are direct, upload-friendly URLs. They can be pasted into a follow-up research prompt. **Claims attributed to authors are not claimed as our discoveries.**

1. G. Ducoffe and B. Dumitru, *Towards a more structured search for Erdős–Gyárfás counter-examples* (2026), arXiv:2609.28594. Primary paper with 2-edge connectivity, edge-saturation, degree counts, doubling auxiliary graph, computation: https://arxiv.org/html/2609.28594
2. D. Garcia, *Small graphs without power-of-two cycles: a lower bound of 24, a correction to a construction of Exoo, and explicit bounds for f(k)* (2026), arXiv:2609.04686. Includes symmetric `H7'` path-window gadget: https://arxiv.org/html/2609.04686
3. A. S. Hegde, R. B. Sandeep, P. Shashank, *Erdős–Gyárfás conjecture on graphs without long induced paths* (2025 version), arXiv:2410.22842: https://arxiv.org/html/2410.22842
4. J. Tranquilli, *A 60-Vertex Lower Bound for Cubic Bipartite Counterexamples to the Erdős–Gyárfás Conjecture* (2026), arXiv:2608.02675: https://arxiv.org/abs/2608.02675
5. A. Carr, *Every Minimal Counterexample to the Erdős–Gyárfás Conjecture is Predominantly Cubic* (2026), arXiv:2605.22844: https://arxiv.org/abs/2605.22844
6. K. Markström, *Extremal graphs for some problems on cycles in graphs* (2004), cited primary PDF: https://citeseerx.ist.psu.edu/document?doi=27733b5bbe1c33ff70addf950e622f0330c1938e&repid=rep1&type=pdf
7. P. Salehi Nowbandegani, H. Esfandiari, M. H. Shirdareh Haghighi, K. Bibak, *On the Erdős–Gyárfás conjecture in claw-free graphs* (2014): https://www.dmgt.uz.zgora.pl/publish/article.php?doi=1732
8. C. C. Heckman and R. Krakovski, *Erdős–Gyárfás conjecture for cubic planar graphs* (2013): https://www.combinatorics.org/ojs/index.php/eljc/article/view/v20i2p7
9. Computational cubic census repository (40-order reported result, data and SAT files): https://github.com/chriss1245/erdos-gyarfas-cubic-frontier
10. Independent research note summarizing Markström’s census and historical through-52 claim: https://github.com/oaustegard/experiments/blob/main/erdos-gyarfas/note.html
11. Hegde–Sandeep–Shashank implementation for induced-path results: https://github.com/rbsandeep/Erdos-Gyarfas
12. S. Narins, A. Pokrovskiy, E. Szabó, *Degree-critical graphs with a missing cycle length* (2015): https://arxiv.org/abs/1408.5289
13. Di Braccio et al., *Leaf-to-leaf paths and cycles in degree-critical graphs* (2026): https://arxiv.org/html/2504.11656
14. Wolfram MathWorld summary: https://mathworld.wolfram.com/Erdos-GyarfasConjecture.html
15. Earlier Zenodo claimed proof (not accepted here as validated): https://zenodo.org/records/22019344

---

## 14. One-paragraph handoff prompt for a new model

> I am investigating the open Erdős–Gyárfás conjecture that every graph of minimum degree at least three contains a simple cycle of power-of-two length. Read this dossier and the accompanying source-code/certificate archive. Treat prior numerical results as exact **only for their stated input families**; the full 251-graph order-28 census was never obtained. Independently review the claimed cubic pentagon/gadget lemmas and the standalone 2^21-case 7-vertex enumeration before citing them as theorems. Ducoffe–Dumitru (arXiv:2609.28594) already provide minimal-counterexample structure and edge-saturation; Garcia (arXiv:2609.04686) already provides 7-vertex gadget window calculus. The most concise unproved bottleneck is: if H is 2-degenerate, has three terminals of degree at least two, all other vertices degree at least three, and no dyadic cycle, must there be a simple terminal-to-terminal path of length 2^k-2? This statement is logically equivalent to the original conjecture. Find a genuinely stronger, independently provable structural lemma implying it, or rigorously falsify an overly strong intermediate statement. Handle high-girth cubic graphs, mixed degrees, and parity. Do not claim a full proof without closing the global forcing step.

---

**Bottom line:** We established a reproducible research trail and some bounded/conditional results. We did **not** solve Erdős–Gyárfás. The central barrier is proving a forcing mechanism for exact dyadic path/cycle lengths in every minimal 3-core, rather than demonstrating flexible cycles in special constructions.
