# Structural results toward the Erdős–Gyárfás conjecture: separator lemmas, an ordering-defect obstruction, and a one-pole gadget theory

**Draft — 2026-07-25. Working paper, not for external circulation without review.**

**§§1–3 (S4, S5, O1–O7, the one-pole theory) are FROZEN as of the end of
the fourth redirection pass — edit only for corrections or external
expert feedback.** The project's current top priority is `two_cut.md`
(toward 3-connectivity of a minimal counterexample); a corresponding
manuscript section will be added there in a future pass, not folded into
this frozen section.

## Status of this manuscript

This is a structural note, not a resolution. The Erdős–Gyárfás conjecture
(every finite simple graph with minimum degree ≥3 contains a cycle of
length a power of two) remains **OPEN**. Every result below is either (a)
a conditional structural statement about a hypothetical minimal
counterexample or one-pole gadget — exactly the standard "if a
counterexample exists, it must look like X" form used throughout this
literature — or (b) an unconditional negative/disproof result about a
proposed invariant. No claim here asserts the conjecture is closer to
proved or disproved in the ordinary sense; the value is structural.

**Novelty wording, used consistently throughout:** *novelty supported by
the available searchable literature; full external expert verification
remains desirable.* This reflects a hard constraint of the working
environment: direct access to arXiv and every tested mirror returned
HTTP 403 at the platform/proxy level (confirmed via direct `curl` through
the egress proxy, not just the fetch tool — see literature.md L16/L17),
so no full paper body has been read for any citation below. Every
citation's applicability was checked against search-engine-returned
abstracts/snippets only. This is a genuine limitation, stated plainly
rather than hedged away.

## 0. Conventions

G always denotes a **minimal counterexample**: a graph minimizing
(|V|,|E|) lexicographically among graphs with δ≥3 and no cycle of length
in F={4,8,16,…}. H denotes a **one-pole graph**: connected, one
distinguished root r with deg(r)=2, every other vertex degree ≥3. A
one-pole graph is **F-clean** if it has no cycle of length in F. No
example of either object is known to exist — the conjecture's openness is
exactly the statement that the union of {minimal counterexamples} and
{F-clean one-pole graphs} might be empty.

## 1. Separator lemmas for a minimal counterexample

**Theorem S4 (bridgelessness).** *A minimal counterexample G has no
bridge.*

*Proof technique.* If e=uv is a bridge, G−e splits into components A∋u,
B∋v. Every vertex of one side keeps its full G-degree except the bridge
endpoint, which loses exactly 1. If that endpoint's remaining degree is
≥3, the smaller side is already a smaller δ≥3, F-clean graph, contradicting
minimality. Otherwise (remaining degree exactly 2), take two disjoint
copies of the smaller side and identify their bridge-endpoint copies into
one vertex: the glued graph has δ≥3 (the identified vertex reaches degree
4), no new cycle crosses the two copies (a simple cycle can visit the
single shared vertex at most once, so any cycle-edges at that vertex must
both belong to the same copy), and strictly fewer vertices than G —
contradicting order-minimality. Full proof: lemmas.md S4.

**Theorem S5 (cut-vertex classification).** *If v is a cut vertex of a
minimal counterexample G, then G−v has exactly two components; v has
exactly two neighbors in each (degree 4); the two lobes (component ∪ {v})
have equal order (forcing n odd) and, by edge-minimality, equal edge count
too; and G has at most one cut vertex.*

*Proof technique.* The same doubling construction as S4, applied at a cut
vertex instead of a bridge, together with a counting argument bounding how
many components can survive order-minimality (at most 2, since if k≥3
survived, some component's doubling would strictly decrease order by a
short pigeonhole sum), then a second counting pass distinguishing order
ties (forcing equal lobe order) from edge ties (forcing equal lobe edge
count, since the doubled graph would otherwise beat G on size at fixed
order). Uniqueness of the cut vertex follows by locating a second cut
vertex w inside one lobe of v and deriving a strict order shortfall.
Full proof: lemmas.md S5.

*Novelty.* Novelty supported by the available searchable literature; full
external expert verification remains desirable. The technique — split at
a cut vertex, recombine to build a smaller/contradicting instance — is a
**known historical technique**, not original to this note: it is the same
mechanism used by **G. A. Dirac, "The Structure of k-Chromatic Graphs,"
Fundamenta Mathematicae 40 (1953), 42–55**, to show chromatic-critical
graphs have no cut vertex. Dirac's theorem is for chromatic criticality,
not cycle-length avoidance, and does not carry S5's equal-order /
equal-edge-count lobe refinement (which needs lexicographic (|V|,|E|)
minimality, not order alone). No published statement of S4 or S5
themselves was located after two independent targeted search passes
(literature.md L16, L17).

## 2. The ordering-defect parameter: a negative result

Define D := 2n−2−m for a graph on n vertices, m edges. The redirection
that motivated this line of inquiry proposed a central target: *every
F-clean one-pole-doubled minimal graph satisfies n ≤ 2D+3.*

**Theorem (disproof).** *Taken literally with this D, the target is false
for every graph with δ≥3 whatsoever — no cycle-length information is
needed.* n≤2D+3 is algebraically equivalent to m≤(3n−1)/2, and the
elementary excess identity Σ(deg(v)−3)=2m−3n≥0 (minimum degree 3) forces
m≥⌈3n/2⌉>(3n−1)/2 unconditionally. Full proof and the resulting
methodological diagnosis (a pure edge-count quantity cannot bound n; any
correct relationship needs the cycle-avoidance structure): defect.md §4.

This is included in the manuscript deliberately: a clean negative result
that redirected the program away from a dead branch is exactly the kind
of finding worth recording formally, not just in a lab notebook.

## 3. The one-pole gadget theory

A single F-clean one-pole survivor, doubled at its root, is already a
full Erdős–Gyárfás counterexample — no minimality needed. The following
results describe the structure any *master-minimal* one-pole graph (the
smallest object, order then size, among {plain F-clean δ≥3 graphs} ∪
{F-clean one-pole graphs} — a framing needed because splitting a one-pole
graph at a bridge or cut vertex can land in either family) would have to
carry, if one exists.

**O1 (bridgeless), O2 (root not a cut vertex), O3 (full 2-connectivity).**
Same doubling technique as S4/S5, applied to a one-pole graph. O3 is
*strictly stronger* than S5's bound for G: peeling a piece off a one-pole
graph at any cut vertex always strictly shrinks it (no "same order"
loophole — unlike G, where doubling an equal-size lobe reproduces the
same order). Full proofs: one_pole.md O1–O3.

**O5 (rigid core, unconditional).** *Every master-minimal one-pole graph
has a K4-minor* — its SPQR tree contains at least one rigid (R) node,
regardless of F-cleanness or minimality; the fact follows purely from the
degree profile (exactly one vertex of degree 2, rest ≥3) plus
2-connectivity. Proof: every nontrivial 2-connected series-parallel graph
has ≥2 vertices of degree exactly 2 (proved here via the SPQR-tree leaf
structure — every leaf is an S-node contributing a purely-local degree-2
vertex, and a nontrivial tree has ≥2 leaves), so a one-pole graph (exactly
1 such vertex) cannot be series-parallel. Cross-checked computationally
against 304 series-parallel graphs (n=3..8, 0 violations) and against two
initially-plausible but ultimately incorrect hand-built "counterexamples"
that a direct SPQR computation caught and rejected — see one_pole.md O5
for the full account, kept deliberately as a record of the error. This
result is *independent of power-cycle avoidance*, unlike the earlier
empirical "rigid pieces dominate" observation it replaces.

**O4′ (admissible-path corollary).** *Every master-minimal one-pole graph
contains two cycles through its root whose lengths differ by 1 or 2.*
Obtained by applying, with k=2, the theorem of **Jun Gao, Qingyi Huo,
Chun-Hung Liu, Jie Ma, "A Unified Proof of Conjectures on Cycle Lengths in
Graphs," International Mathematics Research Notices 2022(10):7615–7653
(arXiv:1904.08126, 2019)**: if K+xy is 2-connected and every vertex of
K∖{x,y} has degree ≥k+1, K contains k *admissible* x–y paths (lengths
forming an arithmetic progression, common difference 1 or 2) — importantly,
**not claimed to be internally disjoint**, and the corollary here does not
need that. Verified via targeted search to match the stated hypotheses and
conclusion (full text unreadable here, per the access caveat above).
Full proof, including the classical degree-2-suppression fact that K+ab
is 2-connected: one_pole.md O4′.

**O4a (failure-structure lemma) and the terminal-spectrum identity.** If
the root's two neighbors a,b are NOT joined by 2 internally-disjoint paths
in K=H−r, Menger's theorem gives a single separator x, and H−{r,x} splits
into exactly two lobes, each attached to both r and x (else r or x would
be a cut vertex, contradicting O2/O3). Writing Λᵢ for lobe Lᵢ's r–x
terminal-path-length spectrum: **{cross-lobe cycle lengths of H} =
Λ₁+Λ₂** exactly, and doubling a single lobe at both terminals creates new
cycles of length exactly **Λᵢ+Λᵢ**. The exact order/edge inequalities
governing when this doubling contradicts master-minimality (distinguishing
the equal-order and equal-order-and-equal-edge cases explicitly, per the
requirement not to infer a contradiction from the sumsets alone) are
proved in one_pole.md's "Exact order/edge inequalities" section.

**The suppressed-edge equivalence.** Deleting r and adding a distinguished
edge e=ab (a second parallel edge, in the multigraph category, if ab was
already present — proved to be genuinely necessary, not a convenience,
whenever a,b are already adjacent, since otherwise δ(Gₑ)≥3 can fail) gives
a graph Gₑ with δ(Gₑ)≥3 exactly, and an exact bijective, length-shifting
correspondence between H's cycles and Gₑ's cycles (avoiding e: same
length; using e: length ℓ ↔ H-cycle of length ℓ+1). This yields:

> **A one-pole graph exists iff there is a loopless graph Gₑ with δ≥3 and
> a distinguished edge e such that every F-cycle uses e, while no
> e-using cycle has length in F⁻ = {2ᵏ−1 : k≥2}.**

Equivalently, the **edge-rooted target**: for every loopless G with δ≥3
and every edge e, either G−e contains a 2ᵏ-cycle or G contains an e-using
(2ᵏ−1)-cycle — true for every (G,e) exactly when no one-pole graph
exists. Full derivation: one_pole.md, "Suppressed-edge reformulation."

## 3b. Hardening pass — O5's second proof, the corrected edge category, and forcing lemmas at remote rigid pieces

**O5, second independent proof.** The SPQR-based proof of O5 is retained,
with its exact convention stated precisely (Q-nodes suppressed except in
the fully degenerate single-edge case; no two same-type nodes are ever
tree-adjacent — a theorem about the canonical/reduced SPQR tree, not an
assumption). A second, convention-independent proof is added via **partial
2-trees**: a simple series-parallel graph is a partial 2-tree (standard
treewidth theory); complete it, on the same vertex set, to an actual
2-tree; every 2-tree with n≥4 is chordal and non-complete, so **Dirac's
theorem on chordal graphs** (G. A. Dirac, "On rigid circuit graphs,"
Abh. Math. Sem. Univ. Hamburg 25 (1961), 71–76) gives ≥2 non-adjacent
simplicial vertices, each forced to have degree exactly 2 (since 2-trees
have no K4 and every vertex has degree ≥2); 2-connectivity of the original
graph then sandwiches these same vertices to degree exactly 2 there too.
Both proofs were cross-checked computationally against each other and
against the two flawed hand-examples from the earlier pass (which,
independently, both register treewidth 3 — genuinely not partial 2-trees,
agreeing with their SPQR-based rejection via a completely different
algorithm).

**The suppressed-edge category, corrected.** Gₑ lands exactly in the
category of loopless multigraphs with at most one parallel pair, located
exactly at the distinguished edge's own endpoints — never a broader
relaxation. The two cases (root neighbors adjacent or not in K) are
handled separately, and subdividing the distinguished edge is confirmed,
case by case, to always recover a simple graph (namely H itself).

**O6 (proper two-pole forcing).** For any proper connected subgraph P of
H with terminals x,y (internal degree ≥3, terminal degree ≥2 at x,y),
attaching a fresh root to both terminals gives a valid one-pole graph
H_P; every cycle of H_P is exhaustively either an internal cycle of P
(automatically F-clean, inherited from H) or a root cycle of length ℓ+2
for ℓ∈Λ(P). So whenever H_P is lexicographically smaller than H,
Λ(P)∩{2ᵏ−2:k≥2}≠∅ — proved with the tied/non-smaller cases handled
explicitly (no contradiction is extractable there).

**O7 (no external common neighbor).** Applied to a remote leaf R-node's
pertinent graph P_R (terminal degree ≥2 and internal min degree ≥3 both
proved automatically from 3-connectivity of the R-node skeleton): if O6's
hypothesis holds, P_R's forced terminal path of length 2ᵏ−2 combines with
any external common neighbor of the two poles into a forbidden 2ᵏ-cycle —
contradiction. Translated into the parent skeleton: the virtual edge for
such a leaf cannot sit in a triangle whose other two edges are both real.

**Empirical status of the one-R-node target.** Applying O7 to the earlier
K4 census (5,525 skeleton-clean configurations) leaves 4,717 survivors in
4 orbits under K4's automorphism group. A direct search of the relaxed
one-pole population for ≥2-R-node candidates found 118/2,464 (n=5–8), 0
F-clean, but **26 with a leaf R-node satisfying every currently proved
local condition (O6+O7) while the whole graph remains non-F-clean** —
smallest example n=8, g6 `GCQVRw`. Per instruction, "every master-minimal
one-pole has exactly one R-node" is **explicitly not conjectured** at
this stage: O6+O7 are demonstrated empirically insufficient on their own,
and the additional condition needed remains unidentified.

## 4. Logical scope — what each result does and does not imply

Recorded explicitly to prevent the three outcomes below from being
conflated in future work (one_pole.md, "Logical scope" section):
1. **Finding any F-clean one-pole survivor** (any order), doubled at its
   root, disproves Erdős–Gyárfás outright — no minimality needed.
2. **Proving no F-clean one-pole graph exists at any order** eliminates
   exactly S5's cut-vertex surviving case for a minimal counterexample —
   it does **not** resolve the conjecture, since the 2-connected minimal
   counterexample case is untouched.
3. **The 2-connected minimal-counterexample case** is a separate,
   unaddressed task; nothing in this manuscript bears on it directly.

## 5. Computational support

Every non-trivial claim above that has a computational component is
backed by an independently runnable script in `verifier/` with results
logged in `experiments.md` (E7–E16): the defect-parameter disproof (E7),
the vine-lemma disproof (E8), the one-pole exhaustive search with a
dual-detector independent verifier (E9), the O4/O4a computational test
(E11), a real SPQR-tree classifier using the published Gutwenger–Mutzel
algorithm rather than a custom heuristic (E12), the rigid-core lemma
cross-check including the regression test on the two flawed hand-examples
(E13), the edge-rooted (G,e) search (E14), independently-verified SPQR
composition-rule tests against brute-force ground truth (E15), and the K4
rigid-skeleton search (E16).

## References

- G. A. Dirac, "The Structure of k-Chromatic Graphs," Fundamenta
  Mathematicae 40 (1953), 42–55. [Historical technique: cut-vertex
  splitting and recombination in a critical-graph minimality argument.]
- G. A. Dirac, "On rigid circuit graphs," Abhandlungen aus dem
  Mathematischen Seminar der Universität Hamburg 25 (1961), 71–76.
  [Chordal graphs have ≥2 non-adjacent simplicial vertices unless
  complete — used for O5's second, convention-independent proof via
  2-trees.]
- Jun Gao, Qingyi Huo, Chun-Hung Liu, Jie Ma, "A Unified Proof of
  Conjectures on Cycle Lengths in Graphs," International Mathematics
  Research Notices 2022(10):7615–7653; arXiv:1904.08126 (2019).
  [Admissible-path theorem, applied here with k=2.]
- Avery Carr, "Every Minimal Counterexample to the Erdős–Gyárfás
  Conjecture is Predominantly Cubic," arXiv:2605.22844 (2026). [M1–M4,
  re-derived independently in lemmas.md; no connectivity content found in
  its abstract per literature.md L16/L17.]
- C. Gutwenger, P. Mutzel, "A Linear Time Implementation of SPQR-Trees,"
  2001 (algorithm underlying the `spqrtree` package used throughout §3's
  computational checks); corrections to J. E. Hopcroft, R. E. Tarjan,
  "Dividing a Graph into Triconnected Components," 1973; data structures
  of G. Di Battista, R. Tamassia, "On-Line Planarity Testing," 1996.
- See literature.md for the full master table (L1–L17) of prior results
  on the Erdős–Gyárfás conjecture and the exact record of what could and
  could not be verified against full text in this environment.
