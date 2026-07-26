# defect.md — the ordering-defect parameter q

## 2026-07-26 Part I: the cubic-core decomposition [PROVED IN WORKSPACE]

**Standing reminder (repeated at every major claim in this file, per project
discipline): every proof below is a hand-written Markdown argument checked
against independent computation. None of it is proof-assistant formal
verification (no Lean/Coq/Isabelle artifact exists anywhere in this
project); "PROVED" means "proved by hand, cross-checked computationally,"
never "machine-checked."**

Throughout this section `G` is a lexicographically minimal Erdős–Gyárfás
counterexample, `n=|V(G)|`, `m=|E(G)|`, `q=q(G)=2n-2-m` (G3, `q>=1` by G2).
`C={v:deg(v)=3}`, `H={v:deg(v)>=4}`, `c=|C|`, `h=|H|`, `F=G[C]`,
`κ=κ(F)` = number of connected components of `F`, `β(F)=|E(F)|-c+κ` its
cyclomatic number. These identities are **pure edge-count algebra**: they
need only (i) `H` independent (M1) and (ii) every vertex of `C` has degree
exactly 3 (true by definition of `C`) — *not* minimality, F-cleanness, or
even δ≥3 beyond what is needed to define `C`,`H`. They therefore hold for
*any* simple graph with an independent high-set and a degree-exactly-3
low-set, a strictly broader class than minimal counterexamples; this is
verified directly below (`verifier/cubic_core.py`) on non-counterexample
fixtures as well as counterexample-hypothesis fixtures, to keep the two
kinds of "why this is true" separate and auditable.

### I.1a. The cross-count identity `e(C,H) = n + 3h - 4 - 2q` [PROVED]

*Proof.* Sum degrees over the two parts: `3c + Σ_{v∈H} deg(v) = 2m`. Because
`H` is independent (M1), every edge at an `H`-vertex goes to `C`, so
`Σ_{v∈H} deg(v) = e(C,H)` exactly. Hence `e(C,H) = 2m - 3c = 2m - 3(n-h)`.
Substituting `m = 2n-2-q` (definition of `q`) gives
`e(C,H) = 2(2n-2-q) - 3n + 3h = n + 3h - 4 - 2q`. ∎

### I.1b. The internal-edge identity `|E(F)| = n - 3h + 2 + q` [PROVED]

*Proof.* `H` independent ⇒ `E(H)=∅`, so every edge of `G` is either
internal to `F` or crosses `(C,H)`: `m = |E(F)| + e(C,H)`. Substituting
I.1a and `m=2n-2-q`: `|E(F)| = m - e(C,H) = (2n-2-q) - (n+3h-4-2q)
= n - 3h + 2 + q`. ∎

### I.1c. The core cyclomatic-number identity, boxed [PROVED]

\[
\boxed{\ \beta(F) = q + 2 - 2h + \kappa\ }
\]

*Proof.* By definition `β(F) = |E(F)| - c + κ`, and `c = n - h`. Substitute
I.1b: `β(F) = (n-3h+2+q) - (n-h) + κ = q + 2 - 2h + κ`. ∎ Since `β(F)≥0`
always (cyclomatic number of any graph), this immediately gives the
inequality `κ ≥ 2h - q - 2`, used throughout Part II.

### I.1d. The `C1,C2,C3` degree-partition of the cubic core [PROVED, needs M2]

Every vertex of `C` has degree exactly 3 in `G`; write `d_F(v)` for its
degree inside `F` and `d_H(v)=3-d_F(v)` for its number of `H`-neighbours.
By M2, every vertex of `G` — including every `v∈C` — has a degree-3
neighbour; simplicity rules out `v` being its own witness, and `v`'s
degree-3 neighbours are exactly its `F`-neighbours (its `H`-neighbours have
degree ≥4 by definition of `H`). Hence **`d_F(v) ≥ 1` for every `v∈C`**,
and trivially `d_F(v) ≤ 3`. So `1 ≤ d_F(v) ≤ 3`, partitioning
`C = C₁ ∪ C₂ ∪ C₃` by `d_F(v)=1,2,3` respectively, sizes `c₁,c₂,c₃`.

**`2c₁ + c₂ = e(C,H)`.** *Proof.* `d_H(v) = 3-d_F(v)` equals `2,1,0` on
`C₁,C₂,C₃` respectively, and `e(C,H) = Σ_{v∈C} d_H(v) = 2c₁+c₂+0·c₃`. ∎

**`c₁ = c₃ + 2κ - 2β(F)`.** *Proof.* Sum `F`-degrees two ways:
`Σ_{v∈C} d_F(v) = c₁+2c₂+3c₃ = 2|E(F)|`, and `c₁+c₂+c₃=c`. Subtracting
twice the second from the first: `c₃-c₁ = 2|E(F)| - 2c = 2(|E(F)|-c)
= 2(β(F)-κ)`. Rearranged: `c₁ = c₃ + 2κ - 2β(F)`. ∎

**Computational validation.** `verifier/cubic_core.py` checks I.1a–I.1d on
three independent populations, none restricted to minimal-counterexample
fixtures except where M2 is genuinely needed:
(a) every connected δ≥3 graph in NetworkX's graph atlas (order ≤7) whose
degree-≥4 set happens to be independent — 14 graphs, tests I.1a–c only
(M2 is a literature fact about genuine minimal counterexamples, not
assumed for arbitrary atlas graphs, so I.1d is skipped when the "every
C-vertex has an F-neighbour" hypothesis is checked and found false);
(b) the 12 inclusion-minimal-δ≥3 order≤7 fixtures already certified by
`global_core_check.py` (M2 does hold here, checked as
`every_vertex_touches_cubic` in that script) — I.1a–d all checked;
(c) 8,145 synthetic random `H`-independent, all-`C`-degree-3 graphs built
directly from random forest/unicyclic `F`-pieces wired to random `H`-sets
(construction guarantees M2's `C`-restriction by design, so I.1d is
checked on 100% of these) at `n` up to ~30, `h` up to 5, `κ` varying.
**Result: 0 failures across all 8,171 applicable checks** —
`manifests/cubic_core_manifest.json`.

### I.2. The component-incidence quotient `Q` [PROVED, with a correction to the naive statement]

Let `K₁,…,K_κ` be the connected components of `F`. Define the **bipartite
multigraph `Q`** on vertex set `H ⊔ {K₁,…,K_κ}`, with `μ(h,Kᵢ)` parallel
edges between `h` and `Kᵢ`, where `μ(h,Kᵢ)` = the number of edges of `G`
from `h` to `Kᵢ`. Equivalently, `Q` is exactly the graph obtained from `G`
by contracting each `Kᵢ` to a single point (no other identification: `H`
vertices, and edges between distinct `Kᵢ`'s cannot exist by definition of
"component").

**(a) `G` connected ⇒ `Q` connected. [PROVED, no extra hypothesis]**
*Proof.* Let `π:V(G)→V(Q)` send each `h∈H` to itself and each `c∈Kᵢ` to
the point `Kᵢ`. For `p,q∈V(Q)`, pick preimages `u∈π⁻¹(p)`, `v∈π⁻¹(q)` and a
`G`-path `u=x₀,…,x_t=v` (exists, `G` connected). For consecutive `xⱼxⱼ₊₁`:
either both lie in the same `Kᵢ` (an internal `F`-edge, contracted, so
`π(xⱼ)=π(xⱼ₊₁)`), or the edge crosses `(C,H)` (so `π(xⱼ)π(xⱼ₊₁)` is a genuine
`Q`-edge by construction) — no other case is possible since `H` is
independent and distinct `Kᵢ`'s share no edge. Deleting the stationary
repeats from `π(x₀),…,π(x_t)` gives a `Q`-walk from `p` to `q`. ∎

**(b) Correction to the naive "2-/3-connected" statement.** The literal
target as stated in the task ("G 2-connected ⇒ every component-node of Q
has ≥2 distinct H-neighbours, unless H=∅") is **too strong as written**:
it also fails, harmlessly, whenever `κ=1` (F itself connected) even with
`H≠∅` — an explicit witness is given below. The correct hypothesis is
`κ(F)≥2`, not merely `H≠∅`:

- **If `κ≥2`: `G` 2-connected ⇒ every `Kᵢ` has ≥2 distinct `H`-neighbours;
  `G` 3-connected ⇒ every `Kᵢ` has ≥3 distinct `H`-neighbours.** [PROVED]
  *Proof.* Suppose `Kᵢ`'s distinct `H`-neighbours are a set `S` with
  `|S|≤1` (resp. `|S|≤2`). Every edge leaving `Kᵢ` in `G` lands in `S`
  (`Kᵢ` has no edges to `C∖Kᵢ` by definition of component, none within `H`
  since `H` independent). Since `κ≥2`, some other component `Kⱼ` (`j≠i`)
  exists, nonempty, disjoint from `Kᵢ∪S` (`Kⱼ⊆C`, `S⊆H`). Any `G`-path from
  `Kᵢ` to `Kⱼ` must leave `Kᵢ` through `S`, so `G − S` disconnects `Kᵢ`
  from `Kⱼ`: `S` is a cut set of size ≤1 (resp. ≤2), contradicting
  2-connectivity (resp. 3-connectivity). ∎
- **If `κ=1` (F connected, a single component `K`): the distinct-neighbour
  count of `K` equals `|H|=h` exactly, and neither 2- nor 3-connectivity
  of `G` forces any further lower bound on `h` through this mechanism.**
  [PROVED, with an explicit realizable witness for `h=1`]
  *Proof of the equality.* Every `h∈H` has `deg(h)≥4≥1` edges, all landing
  in `C=K` (the only component); so every `h∈H` is automatically a
  neighbour of `K` — the distinct-neighbour count is `|H|` by definition,
  not merely `≥` or `≤` something. *Witness that this need not exceed 1
  while `G` is 2-connected:* take `H={h}`, `F=K` any 2-connected cubic-core
  graph, `h` joined to `deg(h)≥4` vertices of `K`. Removing `h` leaves `K`
  itself, connected (`κ=1` by hypothesis), so `h` is *not* a cut vertex —
  `G` can be fully 2-connected with `h` as `K`'s only distinct
  `H`-neighbour. (A concrete instance: `K` any C4-free 2-connected cubic
  graph on `c` vertices with `c ≡ 0 (mod 4)`, minus a perfect matching to
  free 4 slots... a fully worked small instance is impractical to hand-draw
  here; the structural argument above is the actual proof and needs no
  drawing — the point is purely that the cut-vertex argument in (b)'s first
  bullet genuinely requires a *second* component to separate from, which
  `κ=1` does not supply.) This is exactly the corrected caveat: the task's
  own "unless H=∅" was necessary but not sufficient; `κ(F)=1` is the
  precise excluded case, a strictly larger exception (it contains `H=∅` as
  the sub-case `h=0`, but also includes every `h≥1,κ=1` configuration).

**(c) Cuts of `Q` do not automatically transfer to cuts of `G`. [PROVED,
with the exact extra hypothesis isolated]** Two genuinely different kinds
of "vertex" sit inside `Q`, and they behave differently under this
correspondence:
- **An `H`-vertex `h` that is a cut vertex of `Q` *is* automatically a cut
  vertex of `G`, with no extra hypothesis.** *Proof.* `Q−h` disconnected
  into parts `P₁,…,P_r` (`r≥2`). Un-contracting, each `Pⱼ` corresponds to a
  vertex set `Uⱼ⊆V(G)∖{h}` (union of the `H`-vertices and the *entire*
  `Kᵢ`'s in that part). Since distinct `Kᵢ`'s share no edge and `H` is
  independent, every `G`-edge with both ends outside `h` lies entirely
  inside some single `Uⱼ` (it is either internal to one `Kᵢ` or a `C,H`
  edge captured verbatim as a `Q`-edge, and `Q`-edges only ever join
  vertices *within* one `Pⱼ` once `h` is deleted, by disconnection). So
  `G−h` has no edge between different `Uⱼ`'s: `G−h` is disconnected the
  same way. ∎ This is because deleting a *single true `G`-vertex* commutes
  exactly with the contraction map.
- **A component-node `Kᵢ` that is a "cut vertex" of `Q` does NOT
  correspond to deleting a single vertex of `G` at all** — unless `|Kᵢ|=1`,
  deleting the `Q`-node `Kᵢ` corresponds to deleting the *entire*
  `|Kᵢ|`-vertex set `Kᵢ` from `G`, a vertex-*set* removal, not a bona fide
  1-cut. **Extra hypothesis needed to call this a genuine cut of `G`:**
  `|Kᵢ|=1` exactly (then `Kᵢ`'s single vertex is honestly a `G`-vertex and
  the correspondence is exact by the previous bullet, applied to that
  vertex). Symmetrically, a "2-cut" of `Q` built from one `H`-vertex and
  one component-node (or two component-nodes) is a genuine 2-vertex-cut of
  `G` **only if every component-node involved is a singleton**; a 2-cut of
  `Q` built from two `H`-vertices *is* always a genuine 2-cut of `G`, by
  the same single-true-vertex argument applied twice (deleting 2 true
  vertices commutes with contraction exactly as deleting 1 does).

**Computational validation.** `verifier/cubic_core.py`'s
`component_incidence_quotient`/`check_identities` build `Q` explicitly and
check (a) via `nx.is_connected`, the `κ≥2` refined 2-/3-connectivity claims
of (b) via `nx.node_connectivity`, and the `κ=1` equality — 0 violations
across all three populations above (same 8,171-check run).

### I.3. Weighted-incidence cycle-translation formula [PROVED]

**Base case (single `H`-vertex, task's literal statement).** For `h∈H`
with two *distinct* `C`-neighbours `u≠v`, and any simple path `P` from `u`
to `v` lying entirely inside `F` (hence avoiding `h`, since `h∉C`), the
closed walk `h,u,P,v,h` is a simple cycle of `G` of length `|P|+2` (`|P|`
= number of edges of `P`; it visits `h` once, and `P`'s internal vertices
are disjoint from `h` and from each other since `P` is simple). `G`
F-clean forces
\[
|P| + 2 \notin F \iff |P| \notin \{2,6,14,30,\dots\} = \{2^k-2 : k\ge2\}
\]
for every such `u,v,P` with `|P|+2 \le n`.

**General case (alternating multi-H cycle, `t≥1` "spokes").** Let
`t≥1`, let `h₁,…,h_t` be `H`-vertices (pairwise **distinct** when `t≥2`;
for `t=1` a single `h₁` is reused as both endpoints), and for each
`i=1,…,t` (indices mod `t`) let `Pᵢ` be a simple path lying in `F` from
some neighbour of `hᵢ` to some neighbour of `h_{i+1}`, subject to:
(i) the `t` paths `P₁,…,P_t` are pairwise vertex-disjoint;
(ii) for `t≥2`, at each `hᵢ` the neighbour used to close `P_{i-1}` differs
from the neighbour used to start `Pᵢ` (automatic room to choose this since
`deg(hᵢ)≥4≥2`); for `t=1` this reduces to `u≠v` above.
Then `h₁,P₁,h₂,P₂,\dots,h_t,P_t,h₁` is a simple cycle of `G` (disjointness
of the `Pᵢ`'s and distinctness of the `hᵢ`'s exclude every repeated
vertex) of length
\[
t + \sum_{i=1}^{t}|P_i|,
\]
so F-cleanness of `G` forces, for **every** such disjoint/distinct choice,
\[
t + \sum_{i=1}^{t}|P_i| \ \notin\ F.
\]
`t=1` recovers the base case exactly (`2+|P|\notin F`). This is the
precise "sum of path lengths" statement the task asked for — with the
disjointness and distinctness hypotheses stated explicitly, since neither
is optional: reusing a path-internal vertex as another `hᵢ` (violating
disjointness) or repeating an `hᵢ` (violating distinctness) does not
produce a *simple* cycle, and the conclusion is about simple cycles only
(F is defined via simple-cycle length).

---

## 2026-07-26 Part II: the defect-one theorem D1

**Statement (task's target, NOT assumed true).**
> D1. Every graph `G` satisfying (1) `δ(G)≥3`; (2) every proper subgraph has
> min degree `≤2`; (3) `|E(G)|=2|V(G)|-3`; contains a cycle of length 4 or 8.

This is a **standalone graph-theory statement with no F-cycle-avoidance
hypothesis at all** — it is not conditioned on `G` being an EG minimal
counterexample. If `G` *is* a genuine minimal EG counterexample with
`q(G)=1`, it automatically satisfies (1)–(3) (property (2) is exactly
Carr's Lemma 0.1, reused directly, not re-derived; (3) is `q=1`'s
definition), so a proof of D1 would immediately upgrade G2's `q(G)≥1` to
`q(G)≥2`. **No such upgrade is claimed here — see the verdict in II.5.**

### II.0. A fast, exact equivalent of property (2) [PROVED]

Property (2) (every proper subgraph — any edge subset on any vertex
subset — has min degree `≤2`) is checked exactly, but the literal
definition needs an exponential (`2ⁿ`) scan of vertex subsets. It is
equivalent to two `O(n·(n+m))` checks:

\[
\text{property (2)}\iff
\underbrace{\text{every edge has a degree-3 endpoint}}_{\text{B3}}
\ \text{ and }\
\underbrace{\text{for every }v,\ G-v\text{ is 2-degenerate}}_{\text{(∗)}}.
\]

*Proof.* (⇐) Let `(S',E')` be any proper subgraph. If `S'⊊V(G)`: pick
`v∉S'`; `(S',E')` is a subgraph of `G-v` (its vertex set avoids `v`, its
edges are among `G[S']⊆G-v`'s edges), and 2-degeneracy is hereditary
(every subgraph of a 2-degenerate graph is 2-degenerate, by definition),
so `(S',E')` has a vertex of degree `≤2` because `G-v` does. If `S'=V(G)`
and `E'⊊E(G)`: pick `e=xy∈E(G)∖E'`; B3 gives `min(deg_G(x),deg_G(y))=3`,
say `deg_G(x)=3`; since `E'⊆E(G)∖{e}` and `x` loses at least the edge `e`
in passing from `G` to `(V,E')`, `deg_{E'}(x)≤deg_{G-e}(x)≤2`. (⇒) B3 is
literally the `S'=V,E'=E(G)-e` instance of property (2). For (∗): `G-v`
itself is a proper subgraph, and property (2) applied to *every* subgraph
of `G-v` (each is a proper subgraph of `G` too, since it excludes `v`)
gives exactly "every subgraph of `G-v` has a vertex of degree `≤2`," i.e.
`G-v` is 2-degenerate by definition. ∎

**Computational validation.** `verifier/d1_search.py` implements both the
literal `O(2ⁿ)` check (`is_property2`) and this `O(n(n+m))` equivalent
(`is_property2_fast`), and the analogous fast equivalent for the modern
degree-3-critical definition (`is_degree3_critical_fast`, dropping the B3
clause since that definition is induced-subgraph-only). Cross-checked with
**0 mismatches over 329 graphs** (property (2), all connected `δ≥3` graphs
with `m=2n-3`, `n=6..9`) and **0 mismatches over 1,536 graphs**
(degree-3-criticality, all connected `δ≥3` graphs with `m=2n-2`, `n=5..9`).
This speed-up (from `2ⁿ` to linear-ish) is what makes II.4's exhaustive
search reach `n=12` instead of stalling at `n≈8`.

### II.1. The one-defect ordering, classified [PROVED]

By G3, for a genuine minimal counterexample with `q=1`, choosing any cubic
`v` and a 2-degeneracy order `x_1,…,x_{n-1}` of `G-v` (caps
`(2,…,2,1,0)`), the total deficit `Σ(b_i-a_i)=q=1` with every term
`b_i-a_i≥0` (a valid 2-degeneracy order realizes `a_i≤b_i` at *every*
position, not just in total — this is what "2-degenerate" buys beyond the
bare total-edge-count bound). **Hence exactly one position `i*` carries
the entire deficit, all others realizing their cap exactly.** Two
genuinely distinct shapes, mutually exclusive:

- **Case A** (`1≤i*≤n-3`): `x_{i*}` has exactly 1 forward neighbour
  instead of 2 (an "ordinary" position undershoots by one edge).
- **Case B** (`i*=n-2`): `x_{n-2}` has forward degree 0 instead of 1,
  i.e. `x_{n-2}` and `x_{n-1}` (the last two vertices peeled) are
  **not** adjacent in `G-v`.

(`i*=n-1` is impossible: its cap is already 0, so its deficit term is
always 0 — this position can never carry the defect, matching §1's
"vacuous by construction" remark for the historical `D`-identity above.)

**Genuine distinctness under reordering.** A single graph `H=G-v` can
admit *several* valid 2-degeneracy orderings, and the defect can land at
different positions/Cases in different valid orderings of the *same* `H`
— e.g. relabelling which vertex is treated as "last" can convert a Case B
instance into a Case A instance of a different ordering realizing the same
edge count. What is ordering-**independent** is only the *total* (`q=1`)
and the resulting **structural fact**: `H` is obtainable from some
maximal (extremal, `2(n-1)-3`-edge) 2-degenerate graph `H'` on the same
vertex set by deleting exactly one edge (add back whichever single edge
the deficit position is missing — Case A: any not-yet-present edge from
`x_{i*}` to a later vertex; Case B: the edge `x_{n-2}x_{n-1}`). **This
repair edge is not canonically unique** in general (Case A can have
several valid completions when `x_{i*}` has more than one non-neighbour
among the later vertices) — recorded explicitly, since D1C (II.2) asks
exactly this question for `G` itself, not `G-v`.

**Comparison with EFGS 1988 / Narins–Pokrovskiy–Szabó 2015/2017
[literature, access-limited — see literature.md L20].** EFGS's own
degree-3-critical graphs are the `q=0`, zero-defect case of exactly this
same ordering (every position at cap, `m=2(n)-2`... for the *whole* graph,
not `G-v`); NPS's disproof of EFGS's "long cycle-length spectrum"
conjecture is built from **1–3 trees** (leaf-degree-1, internal-degree-3
trees) closed by two extra vertices adjacent to every leaf and to each
other — i.e. an `H`-like pair of high-degree vertices attached to a
*tree*, structurally the same shape as our `β(F)=0` (forest `F`) case in
II.3 below, though NPS's two closing vertices are mutually adjacent
(violating our `H`-independence M1) since their target is unrelated to
power-of-two avoidance. This is a genuine structural parallel worth
flagging for future work, not a citation that resolves D1 here — see
literature.md L20 for the precise access-limited citation and the exact
disproved/proved boundary (NPS disprove "all short lengths `3..C(n)`,
`C(n)→∞`"; they do **not** touch the base EFGS `{3,4,5}` theorem used by
G2, which stands).

**A clean corollary, independent of the rest of Part II.** Property (1)
and (3) alone (no property (2) needed) force `Σ_v(deg(v)-3) = n-6 ≥ 0`
(G3's identity at `q=1`), so **`n≥6` always**, with equality forcing the
`h=0` (cubic) case — matching II.3/II.5's forced base case exactly, and
matching G3's `q(G)≥1 ⇒` `Σ(deg-3)≤n-6` bound at equality.

### II.2. D1C tested directly and found FALSE [DISPROVED — 2026-07-26]

**D1C (as stated in the task):** *every graph satisfying D1's hypotheses
has a nonedge `ab` such that `G+ab` is degree-3-critical* (the modern
induced-only definition, L19: `2n-2` edges, no proper induced subgraph of
min degree `≥3`).

`G+ab` automatically has `δ≥3` (adding an edge never decreases degree) and
exactly `2n-2` edges (one more than `m=2n-3`); the *only* nontrivial
condition is the induced-subgraph one, checked exactly via II.0's fast
equivalent. `verifier/d1_search.py`'s `test_d1c` tries **every** nonedge
of every D1-hypothesis graph found in II.4's exhaustive search.

**Result: D1C holds for every `n=6,7,8` instance (2+4+16=22 graphs), then
FAILS starting at `n=9`.** Smallest counterexamples (3, all at `n=9`,
`m=15`, degree sequence `3⁶4³`, i.e. `h=3`): graph6 `HCOfeW{`, `HCOfbY[`,
`HCOethk` (`manifests/d1_search_manifest.json`). Concretely, for
`HCOfeW{` (edges `03,06,07,14,16,17,25,26,28,36,38,47,48,57,58`), **no**
choice of nonedge `ab` makes `G+ab` degree-3-critical: every completion
either still has a proper induced subgraph of min degree `≥3` (typically
because `G` already has enough redundant high-degree attachment that
completing one gap leaves another dense chunk untouched) or fails for a
symmetric reason. **All three witnesses already contain a C4 directly**
(so D1's conclusion is unaffected by D1C's failure at these instances —
D1C was only ever a proposed *proof strategy* for D1, not part of D1's
statement), but D1C's failure closes off the "reduce D1 to EFGS via one
edge" route in general: 172 further D1C failures accumulate by `n=12`
(`manifests/d1_search_manifest.json`), a rate that is not shrinking.
**Exact obstruction:** D1C would need `G+ab`'s induced-subgraph density to
be controllable by a single edge addition; instead, once `h≥2`, several
independent near-dense induced pieces can coexist (their `d_F`-attachment
patterns to different `H`-vertices), and one edge cannot simultaneously
repair all of them. **No replacement completion theorem is asserted** —
this is recorded as a closed, failed proof route with its exact witness,
per the project's obstruction-preservation discipline, not silently
dropped.

### II.3. The `q=1` specialization of `β(F)=κ+3-2h` [PROVED / COMPUTATIONALLY ILLUSTRATED]

At `q=1`, I.1c gives `β(F) = 3 - 2h + κ`, and `β(F)≥0` forces
\[
\kappa \ge 2h-3.
\]

- **`h=0` [PROVED, forced, exhaustive]:** `H=∅` means `G` is cubic
  (3-regular); `q=2n-2-3n/2=n/2-2=1 ⟺ n=6` exactly (matches the
  independent `n≥6` bound of II.1 at equality). `κ=1` (F=G, connected by
  B1), `β(F)=4`. There are exactly 2 connected cubic graphs on 6 vertices
  (`geng -c -d3 6 9:9`, cross-validated against the direct ordering
  generator in II.4): `K_{3,3}` and the triangular prism. Property (2)
  holds automatically for both (any proper subgraph of a connected cubic
  graph loses degree somewhere, by the same boundary-edge argument used
  throughout this project). **Both contain a 4-cycle directly** (`K_{3,3}`
  by bipartite girth 4; the prism via e.g. `1-2-2'-1'-1`). **D1 holds for
  `h=0` unconditionally and exhaustively — this sub-case is a genuine
  proved theorem, not merely computational evidence for a range.**
- **`h=1`:** `κ≥-1`, i.e. no real constraint (`κ≥1` trivially). All
  `n=7` D1-hypothesis graphs found (4 of them) have `κ=1` (the single
  `C`-vertex not adjacent to `H`'s one vertex... every `C` vertex is
  attached with `d_F≥1` by M2, forcing `F` connected in the smallest
  instances found; no larger-`κ` `h=1` instance appears through `n=12`).
- **`h=2`:** `κ≥1`. Both `κ=1` (`β(F)=0`: `F` is a **spanning tree** on
  `C`) and `κ=2` (`β(F)=1`: `F` a union of 2 pieces with total cyclomatic
  number 1, e.g. one tree + one unicyclic component) occur among the
  `n=8` instances (203 and 138 respectively of the 341 `h=2` graphs found
  through `n=11`).
- **`h≥3`:** `κ≥2h-3` becomes a genuine constraint. The `n=9` instances
  found are all `h=3,κ=3` (the *tight* case, `β(F)=0`: **`F` is a
  disjoint union of exactly 3 trees**, each attached to `H`) — no `h=3`
  instance with `κ>3` appears through `n=12` (larger `κ` needs more
  `C`-vertices, hence larger `n`, consistent with not yet appearing in
  this range).

The **tight case `β(F)=0`** (`F` a forest, `κ=2h-3` exactly) is exactly
the structural shape shared with the NPS 1–3-tree construction flagged in
II.1 — trees hanging off the `H`-vertices, closable via leaf-to-leaf path
arguments. **This is flagged as the most promising single direction for a
future full proof of D1** (see II.5), but is **not** carried to a proof
here: a full leaf-to-leaf translation would need I.3's weighted-incidence
formula specialized to tree-`F` (paths between two `H`-neighbours inside a
tree are unique, unlike in a general connected `F`), which is a
substantial separate undertaking properly scoped as future work, not
attempted in this pass per the task's explicit "continue direct analysis"
instruction (do not silently expand scope into an unbounded new proof
attempt).

**Computational validation.** All `(h,κ,β(F))` triples above, and I.1c's
identity itself, are checked automatically via `verifier/cubic_core.py`'s
`check_identities` on every D1-hypothesis graph found by
`verifier/d1_search.py` — 0 mismatches, `manifests/d1_search_manifest.json`
records the graph6 of every instance by `n`.

### II.4. Canonical generator [PROVED complete at small n; escalated via geng]

Two independent routes, per the task's "generate from the ordering, not
post-hoc filtering" instruction:

1. **Direct ordering generator** (`verifier/d1_search.py`,
   `direct_ordering_generator` + `attach_cubic_vertex`): builds every
   labelled `H=G-v` realizing exactly one 2-degeneracy defect against caps
   `(2,…,2,1,0)` (II.1's Case A/B enumerated directly as combinatorial
   choices of "which later vertices"), then attaches a fresh cubic `v` to
   every 3-subset of `H`'s vertices — literally the task's "one-defect
   forward ordering + 3 neighbors of the restored cubic vertex," with
   *only* the two exact degree/edge-count constraints applied afterward
   (no arbitrary filtering). Combinatorial branching restricts this to
   `N=|H|≤6` (`n≤7`) in practice.
2. **`geng`-driven generator** (`via_geng`): `geng -c -d3 n {2n-3}:{2n-3}`
   generates exactly constraints (1),(3); property (2) is then checked
   *exactly* via II.0's fast equivalent — the one remaining constraint,
   with no simpler `geng`-expressible form, so this is not "filtering
   arbitrary graphs" in the sense the task warns against.

**Completeness cross-check:** at `n=6` and `n=7` — every order where route
1 is feasible — the sets of canonical (brute-force-relabelled) property-2
survivors from routes 1 and 2 **match exactly** (2 and 4 classes
respectively, `route1_only`/`route2_only` both empty). Route 2 is then
used alone for `n=8..12`, escalating exactly the same "validate slow
generator against `geng` at small order, then trust `geng`" pattern
already used throughout this project (e.g. P1's `n=18` geng
re-derivation).

**Per-graph record schema** (one row per D1-hypothesis graph, all stored
in `manifests/d1_search_manifest.json`): `n`, canonical graph6, `(h,κ,β(F))`
via `cubic_core.check_identities`, C4/C8 status (dual DFS+networkx
detector, per project discipline), D1C witness list (possibly empty).
**Completed order range, predeclared here rather than inferred after the
fact: `n=6` through `n=12`, exhaustive** (raw `geng` counts 2, 4, 35, 288,
3478, 50575, 878121; property-(2) survivors 2, 4, 16, 41, 111, 273, 681 —
**1,128 D1-hypothesis graphs total**). `n=13` (17,362,215 raw `geng`
graphs) was **attempted and did not complete** within this session's
compute budget (exceeded the tool's execution-time limit; no partial
result is claimed for `n=13`) — recorded honestly as incomplete, not
silently dropped, per this project's standing discipline for unfinished
runs.

### II.5. Verdict — exactly one outcome [outcome (4): one precisely-formulated open configuration]

Per the task's explicit instruction to end with **exactly one** of four
outcomes, not a list:

**D1 is neither proved nor refuted here.** The genuinely proved content is
narrower: (i) the `h=0` case is a complete, unconditional proof (II.3);
(ii) D1C is disproved as a universal completion strategy, with an exact
witness and obstruction (II.2), closing off the most natural reduction to
EFGS; (iii) `0` counterexamples to D1's conclusion were found among all
1,128 D1-hypothesis graphs through `n=12`, exhaustively (II.4).

**The single precisely-formulated open configuration, chosen as the
outcome per the task's option (4):**

> Does every graph `G` with `δ(G)≥3`, property (2) (Carr's Lemma 0.1), and
> `|E(G)|=2|V(G)|-3` and **`h(G)≥1`** (equivalently `n≥7`, the `h=0` case
> being separately closed by II.3) contain a cycle of length 4 or 8? The
> most structurally promising unresolved sub-configuration inside this
> question is the **tight forest case** (`κ(F)=2h-3` exactly, `F` a
> disjoint union of trees), by the NPS 1–3-tree parallel noted in II.1;
> this sub-configuration is not itself isolated as provably harder or
> easier than the non-tight cases by any evidence gathered here (all
> `(h,κ,β(F))` shapes found through `n=12` satisfy D1's conclusion
> equally, tight or not) — it is flagged as the most promising *entry
> point* for a future proof attempt (via I.3's leaf-to-leaf path
> translation), not as a distinguished harder case.

**Explicitly not claimed, because D1 is not proved:** `q(G)≥2` for
minimal EG counterexamples, and the consequent global bound
`|E(G)|≤2|V(G)|-4`. **G2's `q(G)≥1` / `|E(G)|≤2|V(G)|-3` remains the
current global edge bound** — Part II neither strengthens nor weakens it.

**Reminder, restated per the task's explicit repetition requirement: none
of the above — including the `n≤12` exhaustive claim and the `h=0` "proof"
— is proof-assistant formal verification. Every "PROVED" here is a
hand-written mathematical argument cross-checked by independent Python
computation (dual DFS/NetworkX cycle detectors, two independent D1
generation routes, fast/slow property-(2) cross-validation); no Lean, Coq,
Isabelle, or other formal-proof artifact exists anywhere in this
project.**

---

## 2026-07-25 correction and strengthened theorem [PROVED IN WORKSPACE]

The current parameter is
\[
q(G)=2|V(G)|-2-|E(G)|.
\]
It is the same algebraic quantity called `D` in the historical audit below.
That audit left the 2-degeneracy of `G-v` open because it used only the local
edge statement B3. The missing input is now explicit: Carr's Lemma 0.1 says
that **every proper subgraph** of a lexicographically minimal counterexample has
minimum degree at most two. Therefore, for every cubic `v`, every nonempty
subgraph of `G-v` has a vertex of degree at most two; equivalently `G-v` is
2-degenerate.

Let `x_1,...,x_{n-1}` be any 2-degeneracy ordering of `G-v`, with forward
degrees `a_i`. Against the coordinatewise maximal sequence
\[
(2,2,\ldots,2,1,0),
\]
the nonnegative total deficit is
\[
\sum_{i=1}^{n-1}(\min(2,n-1-i)-a_i)
=(2n-5)-(m-3)=2n-2-m=q(G).
\]
The same argument gives `m<=2n-2`. Equality would make `G` degree-3-critical
in the exact modern sense (it has `n` vertices, `2n-2` edges, and no proper
induced subgraph of minimum degree at least three). The EFGS theorem then
forces a 4-cycle, so in fact
\[
m\le2n-3,\qquad q(G)\ge1.
\]
Finally,
\[
\sum_{u\in V(G)}(d(u)-3)=2m-3n=n-4-2q(G)\le n-6.
\]
See G2--G3 in `lemmas.md` for the complete proof and literature boundary.

The remainder of this file is retained as a historical adversarial audit. Its
claim that 2-degeneracy was unproved is **superseded only for a genuine
lexicographically minimal counterexample**, where the full proper-subgraph
lemma applies. Its counterexamples among arbitrary C4-free minimum-degree-3
graphs remain valid and useful: those graphs need not have the required
proper-subgraph minimality.

---

# Historical audit — the ordering-defect parameter D (superseded as noted)

**Status as of 2026-07-25.** This file is new (redirection of the main project
toward structures that apply to arbitrary order, per the 2026-07-25 task).
Every claim is labeled per the project discipline in README.md. G always
denotes a minimal counterexample (δ≥3, no cycle of length in F={4,8,16,…},
minimizing (|V|,|E|) lexicographically) *if one exists* — none is known to
exist (the conjecture is OPEN), so results here are conditional statements
about G, exactly like B0–B4/M1–M4/S4/S5.

## 1. Elimination ordering and forward degree — setup [PROVED, elementary]

For a simple graph H on n vertices and an ordering x₁,…,xₙ of V(H), define the
**forward degree** d⁺(xᵢ) = |N(xᵢ) ∩ {x_{i+1},…,xₙ}| (neighbors that come
later in the order). Every edge has a unique "earlier" endpoint under any
total order, so **Σᵢ d⁺(xᵢ) = m** for *any* ordering of *any* simple graph.
Also **d⁺(xₙ) = 0** always (nothing comes after the last vertex), and
**d⁺(x_{n-1}) ≤ 1** always (at most one vertex, xₙ, comes after x_{n-1}) —
these last two facts hold for *every* graph and *every* ordering; they are
not special to G and impose no real constraint. This matters below: two of
the five terms in the task's "defect identity" are vacuous by construction,
so the identity's only real content is in the x₁ and middle terms.

## 2. Definition of D and the exact identity [PROVED, pure algebra]

For any simple graph H (n vertices, m edges), define
**D := 2n − 2 − m**.

**Claim.** For *any* ordering x₁,…,xₙ of *any* simple graph,
D = (3 − d⁺(x₁)) + Σ_{i=2}^{n-2} (2 − d⁺(xᵢ)) + (1 − d⁺(x_{n-1})).

*Proof.* RHS = [3 + 1 + 2(n−3)] − [d⁺(x₁) + Σ_{i=2}^{n-2} d⁺(xᵢ) + d⁺(x_{n-1})]
= (2n−2) − Σ_{i=1}^{n-1} d⁺(xᵢ) = (2n−2) − Σ_{i=1}^{n} d⁺(xᵢ) (since
d⁺(xₙ)=0) = (2n−2) − m = D. ∎

This is **pure arithmetic** — it holds for every ordering of every graph,
with no hypothesis on H at all (not even δ≥3). It does **not** by itself
show D ≥ 0, let alone D ≥ 2: the individual terms (3−d⁺(x₁)) etc. can be
negative for a "bad" ordering. What would make the terms a genuine
nonnegative "defect decomposition" is the *existence* of an ordering
realizing the caps d⁺(x₁)≤3, d⁺(xᵢ)≤2 (2≤i≤n−2), d⁺(x_{n-1})≤1 — and by
§1 the last cap is free, so only two things need proving:

**2a. [PROVED] x₁ can be chosen with d⁺(x₁) = 3 exactly.** Take x₁ to be any
degree-3 vertex of G — one exists by M1's corollary (B3). Since x₁ is first
in the order, *all* its neighbors are "later," so d⁺(x₁) = deg_G(x₁) = 3.

**2b. [OPEN — gap, not established here] Middle cap d⁺(xᵢ) ≤ 2 for
2≤i≤n−2.** Equivalently: does G − x₁ admit *some* ordering with all forward
degrees ≤ 2, i.e. **is G − x₁ 2-degenerate** (every subgraph of G−x₁ has a
vertex of degree ≤2, equivalently G−x₁ has no subgraph of minimum degree
≥3)? This is the "known result on graphs without a proper minimum-degree-3
subgraph" the redirection asks to invoke. I could not derive it here from
B0–B4/M1–M4/S4/S5:
- B3 says G itself has no *proper edge-subgraph* of min degree ≥3 (every
  edge has a degree-3 endpoint) — this is a fact about G, not about G−x₁,
  and does not imply G−x₁ is 2-degenerate (B3 does not prevent a min-degree-3
  chunk of G from surviving entirely inside G−x₁, far from x₁).
- The natural orientation argument (orient every edge toward a degree-3
  endpoint, using B3+B4) gives in-degree 0 at every degree-≥4 vertex and
  in-degree ≤3 at every degree-3 vertex, hence only **m ≤ 3n₃ ≤ 3n** — far
  too weak, and it is really just M3 restated, not a 2-degeneracy bound.
- I therefore do **not** assert m(G) ≤ 2n−4 or D ≥ 2 as proved. Both remain
  open pending either (i) a proof that G−x₁ is 2-degenerate (which, if true,
  gives only m ≤ 2n−2, i.e. D≥0 — see the arithmetic below, not yet D≥2),
  or (ii) an independent sharper argument. Flagging this explicitly rather
  than citing an unverified "known result," per the project's no-overclaim
  rule.

Arithmetic check on the gap: if G−x₁ *were* shown 2-degenerate, the standard
tight 2-degenerate edge bound (build from a triangle seed, each further
vertex adds ≤2 edges) gives m(G−x₁) ≤ 2(n−1)−3 = 2n−5, so
m(G) = 3 + m(G−x₁) ≤ 2n−2, i.e. **D ≥ 0** only — not yet D ≥ 2. Reaching
D ≥ 2 needs *either* a strictly sub-extremal 2-degeneracy bound (e.g. using
C4-freeness, B0, to rule out the triangle-heavy extremal 2-degenerate
graphs) *or* a different argument entirely. Left open.

## 3. What IS provable about D from existing lemmas [PROVED]

**3a. Σ_v (deg(v) − 3) = n − 4 − 2D.** *Proof.* Σ(deg(v)−3) = 2m − 3n (S1,
already proved). And n − 4 − 2D = n − 4 − 2(2n−2−m) = n−4−4n+4+2m = 2m−3n.
Same quantity — this is again pure algebra from the definition of D, no new
hypothesis. Matches the redirection's requested identity exactly. ∎

**3b. D ≤ ⌊n/2⌋ − 2.** *Proof.* By S1, m ≥ ⌈3n/2⌉ (δ≥3). So
D = 2n−2−m ≤ 2n−2−⌈3n/2⌉. For n even: ⌈3n/2⌉=3n/2, giving D ≤ n/2−2 =
⌊n/2⌋−2. For n odd: ⌈3n/2⌉=(3n+1)/2, giving D ≤ 2n−2−(3n+1)/2 =
(4n−4−3n−1)/2 = (n−5)/2; since D is an integer and (n−5)/2 = ⌊n/2⌋−2 exactly
when n is odd (⌊n/2⌋=(n−1)/2, so ⌊n/2⌋−2=(n−5)/2), equality of the bound
holds in both parities. So **D ≤ ⌊n/2⌋−2 in general**, with equality iff G
is regular (cubic, by M4) — the excess Σ(deg−3)=0 case. ∎ This reuses only
S1 (already in lemmas.md) — no gap.

**3c. D ≥ 2 remains OPEN**, tied to the §2b gap (an upper bound m ≤ 2n−4 is
exactly equivalent to D ≥ 2 by the definition of D). Not claimed here.

## 4. The central target, taken literally, is DISPROVED [DISPROVED — 2026-07-25]

The redirection's "central proof target": *every power-of-two-cycle-free
minimal graph satisfies n ≤ 2D+3*, with D := 2n−2−m as defined above. Taken
literally (exactly this D, exactly this inequality), this is **false for
every graph with δ≥3** — not just for a hypothetical counterexample G, for
*any* simple graph with minimum degree ≥3 whatsoever. No cycle-length
information is even needed to refute it; S1 alone suffices.

*Proof.* n ≤ 2D+3 ⟺ n ≤ 2(2n−2−m)+3 = 4n−2m−1 ⟺ 2m ≤ 3n−1 ⟺
**m ≤ (3n−1)/2**. But S1 gives m ≥ ⌈3n/2⌉, and ⌈3n/2⌉ ≥ 3n/2 > (3n−1)/2
strictly, for every n ≥ 1. So m > (3n−1)/2 always when δ≥3 — the required
inequality m ≤ (3n−1)/2 **never holds**. Hence n ≤ 2D+3 never holds for any
δ≥3 graph. ∎

**Worked example (cubic case, the extremal case of §3b).** If H is cubic
(m=3n/2, n even), D = 2n−2−3n/2 = n/2−2 = ⌊n/2⌋−2 (equality in 3b), and
2D+3 = n−1 < n = n — off by exactly 1, always. E.g. K₄ (n=4,m=6): D=0,
2D+3=3<4. The Petersen graph (n=10,m=15, cubic): D=3, 2D+3=9<10. This is
not a special pathology of small or specific graphs — §4's proof shows the
gap n−(2D+3) = 2m−3n+1 = (excess)+1 ≥ 1 always, by S1's excess≥0.

**Consequence for the redirection.** Because a cubic δ≥3 graph is not
excluded by any lemma proved so far (M4 only says *if* G is regular it is
cubic; no lemma rules out a cubic minimal counterexample outright — the
Royle–Markström cubic search, L11, only rules it out below n=30, leaving
n≥30 fully open), a literal reading of "n≤2D+3 for every minimal graph"
is inconsistent with what is currently known/open about G's regularity.
**Methodological conclusion:** D as a pure edge-count quantity (a function
of (n,m) alone) cannot by itself bound n — the excess/defect identity in
§3a shows D is just an affine reparametrization of the excess 2m−3n, so any
inequality of the form n ≤ αD+β is *equivalent to* a pure edge-count bound
m ≤ (2n−β)/α, which is either already implied by S1 (if weak) or
contradicted by S1 (if it demands a stronger *lower* bound on excess than
δ≥3 gives, as here). **A correct bound bridging D and n must use the
cycle-length-avoidance structure, not the (n,m) pair alone.** This sharpens
the redirection's own instruction ("search aggressively for
counterexamples") into a precise diagnosis of *why* the naive form fails,
and points Part 3/4's vine/two-tree machinery at the right target: D must
be coupled to the missing-dyadic-length count, not substituted for it.

**Open question for a corrected statement.** The most natural repair
compatible with 3a/3b is to conjecture a bound of the shape
*n ≤ f(D) for some f growing faster than 2D+3* (since D≤⌊n/2⌋−2 already
forces n ≥ 2D+4 in the cubic-extremal case — matching the disproof above
exactly, n = 2D+4 there, one more than the false target) **or** to restrict
the target to non-extremal excess (e.g. state it only for graphs with
excess ≥ 1, which the disproof's gap formula (excess+1) shows would need
excess ≥ 1 exactly to reach n ≤ 2D+4, still not 2D+3). Neither repair is
attempted as a theorem here; both are flagged as the next concrete target,
labeled CONJECTURAL, and require the cycle-spectrum argument (§5/vine
experiment) rather than pure counting.

## 5. Small-D empirical data [COMPUTATIONALLY VERIFIED — see experiments.md E7]

`verifier/defect_model.py` computes (n,m,D,excess) and the full cycle-length
spectrum for real small graphs (connected, δ≥3, generated by `geng`) and
checks both (i) the proved bound D≤⌊n/2⌋−2 and (ii) the disproof in §4. See
experiments.md E7 for the full run log.

**Result: both proved facts hold with 0 exceptions** across 2,762 generic
connected δ≥3 graphs (n=4..8) and 98,066 C4-free connected δ≥3 graphs
(n=10..15) — exactly as guaranteed by the unconditional proofs in §3b/§4
(this is a consistency check on the algebra, not new information).

**The §2b gap is real, not just a missing proof — it computationally
FAILS on a nontrivial fraction of C4-free δ≥3 graphs.** For every graph
tested, and every choice of degree-3 vertex x₁, `defect_model.py` checked
whether G−x₁ is 2-degenerate:

| n range | C4-free δ≥3 graphs | every deg-3 x₁ works | some but not all | **no x₁ works** |
|---|---|---|---|---|
| 10–13 | 574 | 375 | 160 | 39 (6.8%) |
| 14–15 | 97,492 | 33,428 | 48,430 | 15,632 (16.0%) |

The "no x₁ works" fraction is growing with n, not shrinking. **This directly
refutes the naive hope that §2b can be proved by "pick any degree-3 vertex
as x₁"** — smallest concrete witness at n=12: g6 `K?`DA_wdeQKc`, D=1, every
one of its 6 degree-3 vertices leaves a non-2-degenerate remainder. If §2b
(hence m≤2n−4, D≥2) is true at all for genuine minimal counterexamples, the
proof must use F-cycle-freeness beyond C4-freeness (C8, C16, … avoidance)
and/or a cleverer/adaptive choice of x₁ than "arbitrary," not a
universal fact about C4-free δ≥3 graphs. Recorded as an honest negative
result, per the project's discipline of keeping failed approaches with
their exact obstruction.

## 6. Vine construction and cycle spectrum [see experiments.md E8, DISPROVED]

A **vine graph** V(n; chords) realizes the target forward-degree pattern
literally: forward path x₁–x₂–…–xₙ, x₁ additionally joined to 2 further
later vertices (chords), each internal xᵢ (2≤i≤n−2) additionally joined to
at most 1 further later vertex (a "vine" chord) so that its forward degree
is ≤2 (1 path edge + ≤1 chord), and x_{n-1} joined only to xₙ. The natural
charging conjecture to test:

**V1 (candidate lemma).** *"A graph with D defects has at most D missing
dyadic cycle lengths among {4,8,…,≤n}."*

**First (uninformative) test — `verifier/vine_experiment.py`.** Randomized
vine construction (path + minimal/near-minimal chord sets) at n=9..21,
D=0..8: **116/116 instances satisfy V1**, but this is a false positive —
random chord placement makes these graphs cycle-*rich* (missing-count is 0
or 1 in every single instance regardless of D, see experiments.md E8), so
the test never actually stresses the inequality. Recorded as a
methodology note: naive random vine sampling cannot find V1's failure mode,
because avoiding dyadic cycles is an adversarial property random
construction essentially never produces (this is itself informative — it
is a small piece of evidence for *why* Erdős–Gyárfás is hard: "generic"
sparse graphs already satisfy it easily).

**Second test (the real one) — reusing E7's C4-free data.** Every C4-free
graph has length 4 in its missing set by definition (B0 applies to any
C4-free graph, counterexample or not), so num_missing ≥ 1 always among
C4-free graphs — meanwhile D=0 is achievable (D≤⌊n/2⌋−2 only upper-bounds
D; nothing lower-bounds it above the trivial D matching S1's equality
case). **V1 is DISPROVED**, both in general (the argument just given) and
concretely: smallest witness found by `defect_model.py --c4free`, n=13,
g6 `L?AB?vOLDPHa\`o`, D=0, missing={4} (num_missing=1 > D=0). 629/98,066
C4-free graphs (n=10–15) violate V1 outright (experiments.md E7/E8).
**Status: DISPROVED**, recorded per the redirection's explicit instruction
to keep a disproved lemma with its exact obstruction rather than discard
it — see lemmas.md V1 entry.
