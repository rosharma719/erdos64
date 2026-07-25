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

## 5. Connection to ear decomposition [next direction, not developed here]
O3 (H 2-connected) means H admits an **open ear decomposition**: a
starting cycle C₀ plus a sequence of ears (paths with both endpoints on
the graph built so far, internally disjoint from it) whose union is H.
Every ear of length ℓ added to an existing cycle/path structure creates
new cycles by combining ℓ with existing distances between the ear's
endpoints — formally analogous to O4's theta mechanism, but iterated
across the whole ear sequence rather than a single root split. This is
recorded as the natural next computational/structural target (build small
2-connected F-clean-attempt graphs via explicit ear sequences and track
which ear lengths are forced/forbidden at each step) but is **not**
attempted here — flagged per the redirection's point 4 (use computation to
test structural conjectures, not to push raw vertex bounds).

## Summary table

| lemma | status | content |
|---|---|---|
| O1 | PROVED IN WORKSPACE, novelty supported by search (L17) | master-minimal one-pole H has no bridge |
| O2 | PROVED (corollary of O1) | H−r connected; r lies on a cycle |
| O3 | PROVED, novelty supported by search (L17), strictly stronger than S5's cut-vertex bound for G | H is fully 2-connected |
| O4 | OPEN — precise target stated | does H−r contain 2 disjoint a–b paths (⇔ a real theta/book, feeding Track C)? |
| §5 | direction, not developed | ear decomposition of H, forced/forbidden ear lengths |
