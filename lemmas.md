# lemmas.md — Erdős #64

Status labels: PROVED (by me, from definitions, here) / KNOWN FROM LITERATURE /
CONJECTURAL / DISPROVED. "Minimal counterexample" G = a graph minimizing
(|V|,|E|) lexicographically among all graphs with δ≥3 and **no** cycle of
length a power of two. Forbidden lengths F = {4,8,16,32,…}.

Cycle-lifting discipline: an operation is "safe" for us iff it never creates and
never length-shifts a forbidden cycle. **Vertex/edge deletion is safe** (it only
destroys cycles; surviving cycles keep their length). **Degree-2 suppression is
NOT safe** — it shifts cycle lengths by 1, breaking power-of-two-ness (see B2).

---

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

## M2. Every vertex is adjacent to a degree-3 vertex  [PARTIAL]
- For deg(v)≥4: immediate from B4 (all its neighbors are degree-3). [PROVED]
- For deg(v)=3: NOT implied by B3/B4 (v is itself the degree-3 endpoint of its
  edges, so no constraint forces a degree-3 neighbor). This is the nontrivial
  case; proved by Carr 2026. [KNOWN FROM LITERATURE]

---

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

## Cross-checks
- M1, M3, M4 re-derivations were checked against Carr 2026's abstract statements
  and agree. The elementary double-counting in M3 is verifiable on any graph;
  see experiments E-struct (planned) for a computational spot-check of B3/M3 on
  edge-minimal C4∧C8-free graphs (the relaxed property for which B3 also holds).
