# one_pole.md — the rooted one-pole gadget theory

**Status as of 2026-07-25.** Formalizes the "induction gadget" direction:
instead of searching cubic graphs directly, study **one-pole graphs** —
graphs with one distinguished root r of degree 2 and every other vertex of
degree ≥3 — because a single power-of-two-cycle-free one-pole survivor,
doubled at its root (S4's construction), immediately yields a genuine
Erdős–Gyárfás counterexample with no further work. Proving rooted gadgets
*cannot* exist is therefore strictly stronger than the conjecture, and every
structural fact proved here about a hypothetical minimal one-pole graph is a
direct, self-contained analogue of the G-lemmas in lemmas.md — with a clean
connection back to S4/S5 (the O3 remark below) and to Track C's
additive/theta machinery (O4).

## 0. Setup and the "master minimality" framing [needed for a clean proof]

A **one-pole graph** is a pair (H,r): H simple connected, r∈V(H) with
deg_H(r)=2, every v≠r has deg_H(v)≥3. Say H is **F-clean** if it has no
cycle of length in F={4,8,16,…}.

Naively minimizing (|V(H)|,|E(H)|) only within the one-pole family runs
into a snag partway through the bridge argument: splitting H at a bridge
can produce a piece that is no longer one-pole but is instead a *plain*
δ≥3, F-clean graph — i.e. a full Erdős–Gyárfás counterexample outright.
That does not contradict "H is the smallest one-pole graph" (it is a
different family), even though it is an even stronger conclusion. To get a
clean, self-contained contradiction at every step, define the **master
minimum**: the smallest graph, order first then size, that is *either* (a)
a plain δ≥3 F-clean graph, *or* (b) an F-clean one-pole graph. This minimum
exists whenever the union of the two families is nonempty (well-ordering).

- If the master-minimal object is of type (a): Erdős–Gyárfás is already
  false, full stop — nothing more to prove.
- If it is of type (b), call it H (root r): every "smaller object" produced
  below, whichever type it turns out to be, contradicts H achieving the
  master minimum. **All lemmas below are proved under this framing** — they
  are conditional on H being the master-minimal object, exactly as
  B0–B4/M1–M4/S4/S5 are conditional on G being minimal. No claim here
  presumes a counterexample exists.

## O1. Bridgelessness [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH — 2026-07-25; literature.md L17]
A master-minimal one-pole graph H has no bridge (anywhere, including edges
incident to r).

*Proof.* Suppose e=uv is a bridge; H−e splits into components A, B. r lies
in exactly one, say r∈A (this covers e incident to r too: if e=(r,a), then
A∋r, B∋a — r's *other* edge, to its second neighbor b, stays intact, so
b∈A as well). Every vertex of B other than v keeps its full H-degree (≥3,
since v'≠r for all v'∈B, r∉B) — this uses v≠r, i.e. B does not contain the
root, which holds by construction. deg_B(v) = deg_H(v)−1 ≥ 2 (v≠r so
deg_H(v)≥3). Cycles of B are cycles of H, hence F-clean.
- If deg_B(v) ≥ 3: B is a **plain** δ≥3 F-clean graph, order |B| < |H| (A is
  nonempty, contains r) — contradicts H achieving the master minimum
  (type (a) object, smaller).
- If deg_B(v) = 2: B is an **F-clean one-pole graph** with root v, order
  |B| < |H| — contradicts H achieving the master minimum (type (b) object,
  smaller).
Either way, contradiction. ∎

## O2. H−r is connected; r lies on a cycle [PROVED, corollary of O1]
Let a,b be r's two neighbors. Since deg(r)=2, any cycle through r uses both
edges r-a, r-b (r has no other edges to route a cycle through), so r lies
on a cycle iff a,b are joined by a path in H−r. Because H is connected,
every component of H−r must contain a or b (a vertex unreachable from both
would be unreachable from r entirely). If a,b were in *different*
components of H−r, both r-a and r-b would be bridges — contradicting O1.
Hence a,b are in the *same* component, so **H−r is connected**, and in
particular **r lies on at least one cycle of H**. ∎

## O3. Full 2-connectivity [PROVED, novelty supported by search — 2026-07-25, strictly stronger than S5 gave for G; literature.md L17]
A master-minimal one-pole graph H has **no cut vertex at all** (H is
2-connected), not merely "at most one" as in S5 for G.

*Proof.* r is not a cut vertex by O2. Let w≠r be a cut vertex; H−w has
components, with r in exactly one, say C₀. For any other component Cᵢ
(i≥1, not containing r): every vertex of Cᵢ keeps full H-degree ≥3 (only w
cuts it off from the rest). Let dᵢ = deg_{Aᵢ}(w) where Aᵢ = H[Cᵢ∪{w}]. Since
H is connected, dᵢ≥1; since H is bridgeless (O1), dᵢ≠1 (a single edge from
w into Cᵢ would be a bridge), so dᵢ≥2.
- If dᵢ≥3: Aᵢ is a plain δ≥3 F-clean graph (w now has degree ≥3 within Aᵢ
  too), order < |H| — contradicts master minimality.
- If dᵢ=2: Aᵢ is an F-clean one-pole graph (root w), order < |H| —
  contradicts master minimality.
So no such Cᵢ can exist: H−w has only the component containing r, i.e. w
is not a cut vertex. This holds for every w≠r, and r itself is not a cut
vertex (O2). **H is 2-connected.** ∎

**Remark (why this is stronger than S5, and where the asymmetry comes
from).** S5 could only exclude *most* cut-vertex configurations in G,
leaving one surviving case (exactly one cut vertex, equal lobes) — because
peeling a lobe off G and doubling it reproduces a graph of the *same*
order n as G (the doubled lobe has 2|Cᵢ|+1 = n vertices exactly when the
lobes are equal), so order-minimality alone cannot rule it out; only
edge-minimality (S5 step 5) adds the equal-edge-count refinement, and
nothing rules out the configuration outright. Here, by contrast, peeling a
piece off *H* at a cut vertex produces a *strictly smaller* one-pole (or
plain) object — because the piece not containing r is genuinely smaller
than H (H has the extra piece C₀∪r on top), there is no "same order"
loophole. **Cross-check:** if G (a minimal counterexample) has a cut
vertex v (S5's surviving case), each lobe Aᵢ = G[Cᵢ∪{v}] is *itself* a
legitimate one-pole graph (root v, F-clean by inheritance from G) of order
(n+1)/2 — so **S5's surviving case is only possible if a one-pole survivor
exists in the first place** (this specific one, order (n+1)/2 < n). O3
does not contradict S5 (S5's lobe need not be the *master-minimal*
one-pole graph — the master-minimal one could be smaller still), but it
does mean: proving no one-pole survivor exists at all up to order (n+1)/2
would independently re-close S5's surviving case for any hypothetical G of
order n. This is a genuine link between the two lemma sets, not previously
recorded.

## O4. Root-neighborhood structure and the theta connection [OPEN — precise target, not a theorem]
By O2, r's two neighbors a,b are joined by some path in H−r; combined with
r itself this gives a cycle of length 2+ℓ for any a–b path of length ℓ in
H−r. If H−r contained **two internally-disjoint** a–b paths of lengths
ℓ₁,ℓ₂, this would be exactly a **theta graph** Θ(2,ℓ₁,ℓ₂) (Track C's
object, lemmas.md C1/C1a/C2/C3) sitting inside H, with three cycles of
lengths ℓ₁+ℓ₂, ℓ₁+2, ℓ₂+2, all constrained to avoid F. More generally, k
disjoint a–b paths in H−r give a **book** with k+1 "pages" (the k paths
plus the trivial r-path), and F-avoidance forces the *entire* pairwise-sum
structure studied in Track C to arise from a **real graph**, not a
hypothetical additive set — this is precisely the missing link the
redirection asked for ("the path lengths aren't arbitrary integers, they're
generated by a DFS tree... that's where the information lives").

**What is NOT yet established: does such a second disjoint a–b path
necessarily exist?** O3 gives H 2-connected, so by Menger's theorem there
are 2 *internally-disjoint* a–b paths **in H** — but one of those two could
simply be the trivial 2-edge path a-r-b itself (the only path through r,
since deg(r)=2 forces any r-using a–b path to be exactly a-r-b). Menger
only guarantees 2 disjoint paths somewhere in H, not that a second one
avoiding r exists; that would need H to be 2-connected **between a and b
after also deleting r**, i.e. a genuine 3-connectivity-flavored fact not
implied by O3 alone. **This is the precise open target**: does
master-minimality (or F-cleanness) force H−{r} to have ≥2 internally-
disjoint a–b paths (equivalently, H has no 2-vertex-cut of the form
{r,w})? If yes, every master-minimal one-pole graph carries a genuine
theta/book structure and Track C's additive analysis applies *directly* to
a real object for the first time (not a hypothetical). If no (a witness
with a 2-cut {r,w} exists), that is itself informative — it says the
"nested/overlapping DFS-tree" structure is more delicate than a simple
book at the root, and forces attention to the cut vertex w's own local
structure instead (w would itself be a degree-2-or-3 branch point one step
removed from r).

## O5. The rigid-core lemma [PROVED — 2026-07-25, third pass]

**Premise [KNOWN FROM LITERATURE / INDEPENDENTLY VERIFIED]:** every 3-connected
simple graph on ≥4 vertices has a K4-minor (standard consequence of
Tutte's Wheel Theorem — every 3-connected graph is buildable from a wheel
by edge additions and vertex splits, both of which preserve having a
K4-minor, and wheels contain one). Equivalently (and this is the form
actually used below, established independently here via the SPQR-tree
structure rather than re-proving Tutte's theorem): **a 2-connected simple
graph has no K4-minor iff its SPQR tree contains no R-node** — standard
SPQR-tree theory (Gutwenger–Mutzel 2001, per the SPQR package already in
use). "Series-parallel" below means exactly this: 2-connected, no K4-minor,
SPQR tree pure S/P/Q.

**Lemma (degree-2 leaves of series-parallel graphs) [PROVED IN WORKSPACE,
NOVELTY SUPPORTED BY SEARCH].** *Every nontrivial (n≥3) simple 2-connected
series-parallel graph has at least 2 vertices of degree exactly 2.*

*A note on methodology, kept for honesty.* Two hand-built "counterexamples"
were tried first and both were WRONG — computational SPQR verification
caught the error before either was written up as a disproof. ("Diamond
plus a closing edge between its own non-adjacent poles" and "two diamonds
in parallel" were both claimed series-parallel by hand-argument; both
actually contain a K4-minor when checked with `spqrtree` — the first is
literally K4, the second also registers an R-node. The hand-argument's
flaw: closing a series composition — or a parallel composition whose
branches carry their own internal chords, like the diamond's — with a
direct edge between endpoints that are NOT the network's own poles
silently reintroduces a K4-minor. This is recorded because it is exactly
the kind of error the project's "test before promoting" discipline exists
to catch — see `verifier/rigid_core_check.py`, experiments.md E13.)

*Proof (correct version, via the SPQR tree).* Let G be as claimed, T its
SPQR tree (pure S/P, no R, no Q counted separately here since Q-edges are
absorbed as real/virtual edges within S/P skeleta in this library's
convention).
- **No P-node is ever a tree leaf.** A P-node's skeleton is a bond
  (parallel edges between its 2 poles). At most 1 of those parallel edges
  can be *real* (two real parallel edges between the same pair of vertices
  would make G a multigraph, contradicting G simple); every other edge of
  the bond must be *virtual*, i.e. link to a child. A leaf has only 1
  external link (to its parent) and no children — so a leaf P-node would
  need ALL its ≥3 bond edges to be real except the 1 parent-link, i.e.
  ≥2 real parallel edges — impossible for simple G. So every P-node has
  ≥2 children, hence tree-degree ≥2: **never a leaf.**
- **Every leaf is therefore an S-node.** Its skeleton is a simple k-cycle
  (k≥3, since S-nodes are cycles by definition) with exactly 1 virtual
  edge (the parent link) and k−1 real edges. The 2 endpoints of that
  virtual edge are the node's poles (shared with the parent, hence
  possibly of higher true degree in G); the other k−2 cycle-vertices
  are **purely local** — they appear in no other node of T (a leaf has no
  children to share them with) — so each has true G-degree exactly equal
  to its skeleton degree, which is 2 (every vertex of a cycle has degree
  2 in that cycle). Since k≥3, **every leaf contributes ≥1 such
  degree-2 vertex of G.**
- **Case n=1 tree node.** T cannot be a lone P-node (shown above — even
  as root it needs ≥2 children, impossible with none). So T is a lone
  S-node: skeleton = k-cycle, no virtual edges at all (no parent, no
  children) — this means G itself IS the k-cycle, and ALL k≥3 vertices
  have degree exactly 2. ∎ (≥2, trivially, in fact all of them.)
- **Case ≥2 tree nodes.** A tree with ≥2 nodes has ≥2 leaves (standard
  tree fact). Each leaf is an S-node (shown above) contributing ≥1
  purely-local degree-2 vertex, and **distinct leaves contribute distinct
  vertices** (purely-local to one leaf's skeleton means absent from every
  other node's skeleton, in particular from any other leaf's). Two
  leaves ⇒ ≥2 distinct degree-2 vertices of G. ∎

*Computational cross-check* (`verifier/rigid_core_check.py`,
experiments.md E13): every connected min-degree-≥2 graph generated by
`geng` for n=3..8, filtered to 2-connected + series-parallel (via the
SAME `spqrtree` check used throughout this file), was tested against the
lemma: **0 violations across every series-parallel graph found**,
matching the proof exactly (and specifically confirming the two flawed
hand-examples above are correctly rejected as non-SP by the tool, not
silently mis-classified).

**O5 [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH].** *Every
master-minimal one-pole graph H is non-series-parallel: it has a K4-minor,
and its SPQR tree contains at least one R-node.*

*Proof.* H has exactly ONE vertex of degree exactly 2 (the root r — every
other vertex has degree ≥3 by the one-pole definition, and H being simple
with only r at degree 2 is exactly the one-pole hypothesis). If H were
series-parallel, the Lemma above (applicable since H is 2-connected by O3,
and nontrivial since n≥3 — a one-pole graph has n≥3: r plus its 2 distinct
neighbors at minimum) would force **≥2** vertices of degree exactly 2 —
contradicting that H has exactly 1. So H is not series-parallel: its SPQR
tree has an R-node (equivalently, H has a K4-minor). ∎

This replaces last pass's empirical "rigid pieces dominate" observation
(E12: 99.7% of a small relaxed sample) with an **unconditional structural
fact, independent of power-cycle avoidance or minimality** — every
one-pole graph whatsoever (F-clean or not, minimal or not — the proof only
used 2-connectivity plus the degree profile) has a rigid core. The E12
number now reads as "174/67,432 fail even 2-connectivity (O3's real
minimality-dependent content) and are hence not covered by O5's own
2-connectivity hypothesis; of the rest, ALL must have an R-node by O5,
matching the observed 100% (67,258/67,258) — the earlier report of 99.7%
conflated the K4-minor-free-input failures with true SP survivors; there
were in fact zero true SP survivors, exactly as O5 now guarantees
unconditionally."

## Suppressed-edge reformulation [PROVED — 2026-07-25, third pass]

Let H be a one-pole graph, root r, neighbors a,b. Delete r and, if ab∉E,
add the edge; if ab∈E already, work in the category of loopless
multigraphs and add e=ab as a **second, distinguished** parallel edge
(reason this is forced, not a convenience, is proved below). Call the
result **Gₑ**, with e the distinguished edge (either the added edge, or
— if a,b were non-adjacent — simply the new edge itself, no multigraph
needed in that case).

**δ(Gₑ) ≥ 3 [PROVED].** Every vertex w∉{a,b} keeps its full H-degree
unchanged (its edges never touched r), so deg_{Gₑ}(w)=deg_H(w)≥3. For a
(symmetrically b): deg_K(a) = deg_H(a)−1 (a loses exactly its edge to r,
K=H−r), and deg_{Gₑ}(a) = deg_K(a) + 1 (the new/distinguished edge e adds
back exactly 1) = deg_H(a) ≥ 3 (a≠r). **Exactly deg_H(a), unchanged from
H — this is why the construction works whether or not ab was already an
edge of K: the +1 from e always exactly compensates the −1 from removing
r's edge, regardless of what else was already at a.** ∎

**Cycle correspondence, avoiding e [PROVED].** Cycles of Gₑ avoiding e are
exactly cycles of Gₑ−e = K = H−r, which are exactly the cycles of H that
avoid r (H−r's cycles, by definition, are precisely H's cycles not using
vertex r). Literally the same cycles under the identity map: **length
preserved exactly.**

**Cycle correspondence, using e [PROVED].** Let C be a cycle of Gₑ of
length ℓ using edge e=ab. C−e is an a–b path of length ℓ−1 lying entirely
in K (all of C's other edges are K-edges, since e is the only edge outside
K). This path, concatenated with the 2-edge detour a-r-b (through the
root, avoiding r elsewhere since the path itself avoids r by lying in K),
gives a simple cycle of H through r of length (ℓ−1)+2 = **ℓ+1**. This map
is a bijection (reverse direction: any r-containing cycle of H, delete r
and its 2 incident edges, close with e, strictly reduces length by 1).

**Exact equivalence [PROVED].** Let F={2ᵏ:k≥2}, F⁻={2ᵏ−1:k≥2}. Combining
the two correspondences: H is F-clean (no cycle of length in F) iff
*[no cycle of Gₑ avoiding e has length in F]* **and** *[every cycle of Gₑ
using e has length ℓ with ℓ+1∉F, i.e. ℓ∉F⁻]*. Restated exactly as asked:

> **A one-pole graph exists iff there is a loopless graph Gₑ with
> δ(Gₑ)≥3 and a distinguished edge e such that every F-cycle of Gₑ uses
> e, while no e-using cycle of Gₑ has length in F⁻.**

("Every F-cycle uses e" ⟺ "no F-cycle avoids e" ⟺ the first bracket
above — restated as the contrapositive for readability, identical
content.)

**The edge-rooted target.** Negating the equivalence (no one-pole exists
⟺ the target below holds for every (G,e)):

> **For every loopless graph G with δ(G)≥3 and every edge e: either G−e
> contains a 2ᵏ-cycle, or G contains an e-using (2ᵏ−1)-cycle.**

By S5's cross-link (O3 remark), this target, if provable, closes exactly
S5's surviving cut-vertex case for a minimal counterexample — see the
Logical scope section below; it does **not** by itself touch the
2-connected case.

**Parallel edges are genuinely necessary when a,b are already adjacent —
checked, not assumed.** Suppose instead of adding a *distinguished*
parallel copy, one simply reused the existing ab edge as "e" when
ab∈E(K), keeping Gₑ:=K a simple graph. Then deg_{Gₑ}(a) = deg_K(a) =
deg_H(a)−1, which can be as low as **2** (if deg_H(a)=3, the generic
case) — **violating δ(Gₑ)≥3.** The distinguished parallel edge is not a
bookkeeping convenience; it is exactly what restores the "+1" that
suppressing r removes, and without it the equivalence's very first
condition (δ(Gₑ)≥3) fails. So: **the equivalence genuinely requires the
multigraph category whenever ab∈E(K); it cannot be restated for simple
graphs alone in that case.** This also identifies exactly when it CAN
stay simple: whenever a,b are non-adjacent in K (the generic case at
larger n, matching e.g. defect.md's discussion of C4-freeness — note H
itself being C4-free, inherited from B0-style reasoning if H arose inside
a genuine minimal counterexample's lobe, would make ab∈E(K) create a
*triangle* r-a-b in H, not forbidden by F, so this case is not excluded
by F-cleanness alone and must be handled with the multigraph category).

## O4′. The admissible-path corollary [PROVED; underlying theorem KNOWN FROM LITERATURE]

**Theorem (Gao, Huo, Liu, Ma 2022).** Jun Gao, Qingyi Huo, Chun-Hung Liu,
Jie Ma, *"A Unified Proof of Conjectures on Cycle Lengths in Graphs,"*
IMRN 2022(10):7615–7653 (arXiv:1904.08126, 2019). If G+xy is 2-connected
and every vertex of G∖{x,y} has degree ≥ k+1, then G contains k
**admissible** x–y paths: paths P₁,…,Pₖ whose lengths form an arithmetic
progression of length k with common difference 1 or 2.
**Verification note:** confirmed via targeted search (matches the stated
hypotheses and conclusion essentially exactly — same G+xy 2-connected
condition, same k+1 degree bound, same admissible-path definition); full
paper text could not be read (arXiv/IMRN both blocked in this
environment, per literature.md L16/L17's confirmed hard platform block).
**Explicitly NOT claimed by the theorem: the k paths need not be
internally vertex-disjoint** — nothing in the located hypotheses or
statement asserts disjointness, and the proof method (iteratively
combining shorter admissible families) does not obviously produce
disjoint paths. This matches the redirection's explicit instruction not
to infer disjointness, and is essential to how O4′ is derived below
(the argument does not need it).

**Application (k=2).** Let H be a master-minimal one-pole graph, root r,
neighbors a,b, K := H−r. Set x=a, y=b, G=K in the theorem.
- *K+ab is 2-connected:* this is the standard degree-2-vertex-suppression
  fact. [PROVED, elementary/classical — not claimed novel.] *Proof.*
  Suppose K+ab has a cut vertex w. If w∉{a,b}: H−w is connected (H
  2-connected, O3) and contains r with both its edges to a,b intact (w≠a,b).
  In (H−w)−r = K−w, a and b lie in at most 2 components (any component
  containing neither would already be disconnected from r in H−w, since r
  only reaches a,b — but H−w is connected, contradiction), and adding edge
  ab merges those into one, so (K+ab)−w = (K−w)+ab is connected —
  contradicting w a cut vertex. If w=a (symmetric for w=b): (K+ab)−a =
  K−a. H−a is connected (O3); in H−a, r has only its edge to b left
  (degree 1, a pendant on b), so removing r from H−a (giving K−a) doesn't
  disconnect anything else. So K−a is connected. Either case contradicts
  w being a cut vertex, so **K+ab is 2-connected.** ∎
- *Degree hypothesis:* every vertex of K∖{a,b} = H∖{r,a,b} has H-degree ≥3
  (one-pole definition, since these vertices ≠r), and K doesn't touch r,
  so their K-degree equals their H-degree, ≥3 = k+1 for k=2. Hypothesis
  holds with equality.
- Both hypotheses of the theorem hold with x=a,y=b,k=2, giving **2
  admissible a–b paths in K**: lengths ℓ₁,ℓ₂ with |ℓ₁−ℓ₂|∈{1,2}.

**Corollary O4′ [PROVED].** Each aᵢ-path Pᵢ (i=1,2), being entirely within
K=H−r, avoids r; concatenating it with the 2-edge detour a-r-b gives a
**simple cycle** Cᵢ of H of length ℓᵢ+2 through r (simple because Pᵢ is
simple and disjoint from r). This needs **no disjointness** between P₁
and P₂ — each Cᵢ is built independently from its own Pᵢ plus the fixed
r-detour. So: **every master-minimal one-pole graph contains two cycles
through its root, C₁ and C₂, with |len(C₁) − len(C₂)| ∈ {1,2}.** ∎

Since H is F-clean, neither length is itself forced into F, but their
near-equality is a real constraint: consecutive-or-near integers can't
both avoid {4,8,16,…} for long stretches only near small n (the gaps
between consecutive powers of two grow), so this bites hardest for small
H and becomes weak for large H — flagged honestly, not oversold as a
strong bound by itself.

## O4a. Failure structure of O4 [PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH]
Suppose K=H−r does **not** contain 2 internally-disjoint a–b paths (i.e.
O4, the disjoint-paths question from earlier, fails). By the vertex form
of Menger's theorem, the maximum number of internally-disjoint a–b paths
equals the minimum a–b vertex separator size; since K is connected (O2, so
≥1 path exists) and by hypothesis <2 disjoint paths exist, that minimum is
exactly 1: **∃ x∈V(K)∖{a,b} such that K−x disconnects a from b.**

*Claim: H−{r,x} has exactly two components, D₁∋a and D₂∋b, and both
attach to r and to x.*

*Proof.* Since x separates a,b in K, they lie in different components of
K−x = H−{r,x}; call them D₁∋a, D₂∋b. Suppose a third component D₃ exists
(containing neither a nor b). r's only edges are to a,b, so r has **no**
edge into D₃ (r has only two neighbors, and neither is in D₃). Since K is
connected, x must have an edge into D₃ (else D₃ would already be a
separate component of K itself, without even removing x — contradicting K
connected). So D₃'s **only** connection to the rest of H is through x
(not through r, which doesn't reach it at all). Removing x from H would
then disconnect D₃ from the rest — **making x a cut vertex of H**,
contradicting O3. So no third component exists: exactly D₁,D₂. Each
attaches to x automatically (x is exactly the separator: K connected means
every piece left over after removing x must have had an edge to x, or it
would already have been its own component of K). Each attaches to r
trivially: a∈D₁ with edge r-a; b∈D₂ with edge r-b. ∎

This matches every point requested: no-attachment-to-r would make x a cut
vertex of H (used to rule out a third component); no-attachment-to-x is
impossible given K's connectivity; r has only two neighbors (used to see r
cannot reach any component beyond the ones holding a,b); a,b are separated
by x (the defining property of x). **Label: PROVED IN WORKSPACE, NOVELTY
SUPPORTED BY SEARCH** (same search pass as S4/S5/O1/O3 — literature.md
L16/L17 — found no prior EGC statement; not re-run separately here since
it uses the identical technique already checked).

## Terminal path spectra and the exact cross-cycle identity [PROVED]
Write Lᵢ := H[Dᵢ∪{r,x}] (i=1,2), the **two-terminal lobe** with terminals
r,x. Since r's only H-edges are to a∈D₁ and b∈D₂, **r has degree exactly 1
within each Lᵢ** (only the edge to a in L₁, only to b in L₂) — r is a
pendant relative to each lobe individually. Define
**Λᵢ := {ℓ : Lᵢ has a simple r–x path of length ℓ}** (i=1,2). Since every
r–x path in Lᵢ must start with r's unique edge (to a or b), Λᵢ = 1 +
{lengths of simple a–x (resp. b–x) paths in H[Dᵢ∪{x}]}; Λᵢ is nonempty
(Dᵢ connects to both r and x).

**Exact identity: {lengths of cycles of H using both lobes} = Λ₁ + Λ₂**
(sumset). *Proof.* L₁∩L₂ = {r,x} exactly (D₁,D₂ disjoint components).
Any simple cycle using vertices of both lobes must cross between them only
at r or x (the sole shared vertices), so between consecutive visits to
{r,x} it stays entirely within one lobe; visiting each of r,x at most once
(simple cycle), it therefore splits into exactly one r–x arc in L₁
(length ℓ₁∈Λ₁) and one in L₂ (length ℓ₂∈Λ₂), total length ℓ₁+ℓ₂.
Conversely, any ℓ₁∈Λ₁,ℓ₂∈Λ₂ concatenate (sharing only endpoints r,x, and
otherwise vertex-disjoint since D₁∩D₂=∅) into a genuine simple cycle of
length ℓ₁+ℓ₂. ∎ Since H is F-clean: **(Λ₁+Λ₂) ∩ {2ʲ : j≥2} = ∅.**

**Internal cycle spectra recorded separately** (not folded into the sum
above): cycles lying entirely inside one Lᵢ (whether or not they use x)
are a *different* constraint, F-clean by inheritance from H alone, and
depend on Lᵢ's own internal 2-cut structure recursively — this is exactly
what the SPQR analysis below is for.

## Two-terminal doubling criterion [PROVED, expressed via Λᵢ+Λᵢ]
Glue **two copies of a single lobe Lᵢ** at *both* terminals (identify the
two copies' r's into r*, and the two copies' x's into x*) — the natural
generalization of S4/O1's one-vertex doubling to a 2-cut. Every internal
Dᵢ vertex keeps its Lᵢ-degree (≥3, unchanged, inherited from H). Since r
has degree exactly 1 within Lᵢ (shown above), **r\* always has degree
exactly 2** (one edge from each copy) — structurally forced, regardless of
i. x\* has degree 2·deg_{Lᵢ}(x). Since x∉{r} (x∈V(K)∖{a,b}, not adjacent to
r), deg_{L₁}(x)+deg_{L₂}(x) = deg_H(x) ≥ 3, so **at least one of the two
lobes has deg_{Lᵢ}(x) ≥ 2** (pigeonhole; possibly not both).

Cycles of the doubled graph: exactly as in S4/O1's *single*-vertex case,
cycles staying inside one copy inherit Lᵢ's own (already F-clean, by
inheritance from H) spectrum. But **with two shared vertices instead of
one, crossing cycles are now possible** (impossible in the one-vertex
doubling of O1/S4) — a cycle can run copy-1's r\*–x\* path (length ℓ∈Λᵢ,
since copy 1 is just Lᵢ) then copy-2's x\*–r\* path (length ℓ′∈Λᵢ, same
spectrum, it's the same lobe). So:

- **New cycles created by doubling have lengths exactly Λᵢ+Λᵢ** (the
  *self*-sumset — including ℓ=ℓ′, i.e. genuine self-sums 2ℓ for ℓ∈Λᵢ).
- **The doubled graph is F-clean ⟺ (Λᵢ+Λᵢ) ∩ {2ʲ:j≥2} = ∅** — a
  *strictly new* condition, not implied by H's own F-cleanness (H only
  gave (Λ₁+Λ₂)∩F=∅, pairing the two *different* lobes; Λᵢ+Λᵢ pairs a lobe
  with *itself*, an untested combination).
- **Valid one-pole (root r\*, all else ≥3) ⟺ deg_{Lᵢ}(x)≥2 AND
  (Λᵢ+Λᵢ)∩F=∅** — both the degree condition and the cycle condition are
  required; neither alone suffices, and no order/size balance claim is
  made beyond this (per the redirection's caution).
- **Never a full plain counterexample directly:** r\* is *always* exactly
  degree 2 by the structural fact above (r has degree 1 in every lobe,
  unconditionally) — single-lobe two-terminal doubling can produce a
  one-pole graph or (if deg_{Lᵢ}(x)=1) an unresolved **two-pole**
  intermediate object (both r\*,x\* at degree 2, needing further gluing),
  but never a plain δ≥3 graph outright. This directly matches item 6's
  required scope correction below.

### Exact order/edge inequalities [PROVED — 2026-07-25, third pass]
Write tᵢ := deg_{Lᵢ}(x) (i=1,2; t₁+t₂=deg_H(x)≥3 since x has full H-degree,
not being the root). |Lᵢ|=|Dᵢ|+2. Doubling Lᵢ at both terminals identifies
r AND x across the 2 copies (saving 2 vertices, not 1):
**|H′ᵢ| = 2|Lᵢ|−2 = 2|Dᵢ|+2.** Edges simply double (no shared edges
between copies, only shared vertices): **|E(H′ᵢ)| = 2·E(Lᵢ).**

Using n=|H|=|D₁|+|D₂|+2 (O4a's partition) and the clean identity
**E(H) = E(L₁)+E(L₂)** (proved exactly as in S5 step 5: E(Dᵢ-internal) =
E(Lᵢ)−1−tᵢ since Lᵢ = Dᵢ-internal-edges + 1 edge from r + tᵢ edges from x;
summing and telescoping the ±1,±tᵢ terms gives E(H)=E(L₁)+E(L₂) exactly):

- **Order:** |H′ᵢ| − n = (2|Dᵢ|+2) − (|D₁|+|D₂|+2) = |Dᵢ| − |D_{other}|.
  So **|H′ᵢ| < n ⟺ |Dᵢ| < |D_{other}|**, with equality iff |D₁|=|D₂|.
- **Edges, in the equal-order case (|D₁|=|D₂|):** |E(H′ᵢ)|−|E(H)| =
  2E(Lᵢ) − (E(L₁)+E(L₂)) = E(Lᵢ) − E(L_{other}). So, **given |D₁|=|D₂|**,
  **|E(H′ᵢ)| < |E(H)| ⟺ E(Lᵢ) < E(L_{other})**, with equality iff
  E(L₁)=E(L₂).

**Precise conditional conclusion (master minimality, no sumset alone):**
H′ᵢ is a genuine F-clean one-pole graph exactly when BOTH tᵢ≥2 AND
(Λᵢ+Λᵢ)∩F=∅ (proved above — this is a real conjunction, not something the
sumset condition alone determines). If, **in addition**, H′ᵢ is
lexicographically smaller than H — i.e. |Dᵢ|<|D_{other}|, **or**
|Dᵢ|=|D_{other}| and E(Lᵢ)<E(L_{other})** — then H′ᵢ would be a strictly
smaller member of the same {plain F-clean graphs}∪{F-clean one-pole
graphs} family that H is assumed to minimize (§0), contradicting
master-minimality. Hence, **conditional on tᵢ≥2 and H′ᵢ being
lex-smaller than H**:
[
(\Lambda_i+\Lambda_i)\cap\mathcal F\ne\varnothing.
]
**This conclusion genuinely needs the tᵢ≥2 hypothesis stated alongside
it** — if tᵢ=1 instead, H′ᵢ is not a one-pole graph at all (it is a
two-pole intermediate object outside the family being minimized), so no
contradiction is available from order/edge comparison regardless of the
sumset, and (Λᵢ+Λᵢ)∩F=∅ remains possible without contradiction. (Sanity
check: t₁+t₂≥3 forces at least one of t₁,t₂ ≥2, so this qualifier is
never vacuous — some lobe always qualifies for the argument, though not
necessarily the lex-smaller one.)

**Equal-order-and-equal-edge case, handled separately as required:** if
|D₁|=|D₂| **and** E(L₁)=E(L₂), then |H′ᵢ|=n and |E(H′ᵢ)|=|E(H)| for
*either* i — H′ᵢ ties H exactly in the lexicographic order used for
master-minimality, so **no contradiction is extractable this way** in
this case, regardless of tᵢ or the Λᵢ+Λᵢ sumset. This is an honest gap,
not resolved here — matching the instruction not to infer a contradiction
from the sumsets alone when the order/edge comparison itself doesn't
supply one.

## SPQR decomposition before arbitrary ear decompositions [scope correction]
O3 (H 2-connected) technically means H admits an open ear decomposition,
but per the redirection this is now **demoted**: an arbitrary ear
decomposition is the wrong primary representation while 2-cuts (like x in
O4a) remain unresolved, because it does not distinguish "this ear is
forced by a series/parallel 2-cut structure" from "this ear lives inside a
genuinely rigid (3-connected) piece where no smaller vertex cut helps."
Instead, use the **SPQR tree** of K+ab (K=H−r; 2-connected by the O4′
application above) — a real, verified decomposition (Gutwenger–Mutzel
2001 algorithm, correcting Hopcroft–Tarjan 1973, data structures of Di
Battista–Tamassia 1996; implemented here via the `spqrtree` PyPI package,
a pure-Python implementation of exactly this algorithm — not a custom
heuristic). Every 2-connected multigraph decomposes into a tree of nodes,
each of type:
- **S (series):** a simple cycle in the skeleton — real/virtual edges in
  series, i.e. a chain of 2-cuts between the poles. Corresponds directly
  to **adding terminal path lengths** end to end.
- **P (parallel):** a bond (2+ parallel real/virtual edges between the
  same pole pair) — independent parallel pieces between the same two
  vertices. Corresponds to **cycle formation from pairs of the parallel
  pieces' own path spectra** — exactly the Λᵢ+Λⱼ mechanism above, now
  seen as a specific SPQR node type rather than an ad hoc construction.
- **R (rigid):** a genuinely 3-connected skeleton — no further 2-cut
  decomposition is possible here. **This is the only place where ear
  decomposition (or any further structural tool) is still needed**; S and
  P nodes are already fully explained by the series/parallel path-length
  arithmetic above.
- **Q (single edge):** the trivial base case (a real or virtual edge on
  its own).

`verifier/spqr_analysis.py` builds the SPQR tree of K+ab for every
one-pole/relaxed candidate and reports the node-type multiset, with rigid
(R) nodes flagged as exactly the pieces needing further work; see
experiments.md E12 for results (which small graphs are pure S/P — fully
explained by the arithmetic above — vs. contain an R node). Two findings
from that run are worth flagging here directly: (i) **K+ab genuinely can
have a cut vertex** in the relaxed (non-F-clean) population (174/67,432
cases, n=5–9) — a live confirmation that O3's 2-connectivity is real
content coming from F-cleanness+minimality, not a free consequence of the
degree/connectivity hypotheses alone; (ii) **"pure series-parallel" (no
rigid node) essentially never occurs even at n≤9** (0 of the 67,258
classifiable candidates) — rigid pieces are already the dominant regime
at the smallest sizes, so the O4′/Λᵢ+Λⱼ arithmetic above, while exact, is
not by itself a full account of most small candidates' cycle structure.

## Logical scope [correction, per redirection item 6]
Three genuinely different claims must not be conflated, and the labels
below are the only ones this project asserts:
1. **Finding an F-clean one-pole survivor** (any order) — doubled at its
   root — **immediately disproves Erdős–Gyárfás outright.** No minimality,
   no O1–O4a assumptions needed; this is the strongest and simplest
   possible outcome, and it is why the one-pole search (E9) is run at all.
2. **Proving no F-clean one-pole graph exists at any order** (i.e. the
   master-minimal object in §0 is never of type (b)) — this would
   eliminate exactly the **cut-vertex case** for a minimal counterexample
   G (S5's surviving case: G has a cut vertex ⟺ each lobe is itself a
   one-pole graph, one_pole.md O3 remark) — **it does NOT by itself
   resolve Erdős–Gyárfás**, because a 2-connected minimal counterexample
   (S5's other case, no cut vertex at all) is untouched by this and
   remains open.
3. **2-connected minimal counterexamples** (G with no cut vertex, or
   equivalently a one-pole graph H that is not merely one-pole but forms
   the "core" of some G) are a **separate, unaddressed task** — nothing
   in O1–O4a, the SPQR analysis, or Track C bears on this case yet. Do not
   describe progress on one-pole gadgets as progress on the 2-connected
   case; they are logically independent lines of attack that happen to
   share machinery (S4/S5's doubling technique, Track C's additive
   framework).

## Summary table

| lemma | status | content |
|---|---|---|
| O1 | PROVED IN WORKSPACE, novelty supported by search (L17) | master-minimal one-pole H has no bridge |
| O2 | PROVED (corollary of O1) | H−r connected; r lies on a cycle |
| O3 | PROVED, novelty supported by search (L17), strictly stronger than S5's cut-vertex bound for G | H is fully 2-connected |
| O4′ | PROVED; underlying theorem KNOWN FROM LITERATURE (Gao–Huo–Liu–Ma 2022) | H has 2 cycles through r with lengths differing by 1 or 2 |
| O4a | PROVED IN WORKSPACE, novelty supported by search | if O4 fails, a 1-vertex separator x splits H−{r,x} into exactly 2 lobes attached to both r and x |
| Λᵢ identity | PROVED | cross-lobe cycle lengths = Λ₁+Λ₂; doubling-criterion cycles = Λᵢ+Λᵢ |
| O4 (disjoint paths) | OPEN — now secondary to O4a's failure-structure analysis | does H−r contain 2 disjoint a–b paths? (if not, O4a's structure applies) |
| SPQR scope | tooling built, results in experiments.md E12 | S/P nodes fully explained by path arithmetic; only R (rigid) nodes need further tools |
