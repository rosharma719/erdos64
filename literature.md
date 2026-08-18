# Literature — Erdős–Gyárfás conjecture (Erdős Problem #64)

**Conjecture (Erdős–Gyárfás, 1995).** Every finite simple graph with minimum
degree ≥ 3 contains a simple cycle whose length is a power of two (∈ {4,8,16,…}).
Erdős offered $100 for a proof, $50 for a counterexample (he suspected it might
be false). Status as of 2026-07: **OPEN**.

All entries below are **KNOWN FROM LITERATURE** unless I re-derive/re-verify them
here (flagged). Cross-checked against arXiv abstracts and the AMS grad blog.

## Master table

| # | Theorem / fact | Hypotheses | Conclusion | Method | Comp? | Reusable lemma/algorithm | Source | Gap / opportunity |
|---|---|---|---|---|---|---|---|---|
| L1 | Conjecture holds for planar graphs | planar, δ≥3 | ∃ 2-power cycle | structural | no | planar cycle-length forcing | Daniel & Shauger | Not the general case |
| L2 | Holds for planar claw-free graphs | planar, K₁,₃-free, δ≥3 | ∃ 2-power cycle | structural | no | claw-free local structure | Daniel & Shauger (West OPG) | — |
| L3 | Holds for K₁,ₘ-free with δ≥m+1 or Δ≥2m−1 | K₁,ₘ-free + degree cond. | ∃ 2-power cycle | structural | no | star-free ⇒ dense neighborhoods | Shauger | claw-free = m=3 case |
| L4 | Holds for 3-connected cubic planar graphs | 3-conn, cubic, planar | ∃ 2-power cycle (len 4 or 8) | structural | no | face/edge counting | Heckman & Krakovski | planarity essential |
| L5 | Holds for P₈-free graphs | no induced P₈, δ≥3 | ∃ 2-power cycle | structural | partial | induced-path branching | Gao & Shan 2022 | superseded by L7 |
| L6 | Holds for P₁₀-free graphs | no induced P₁₀, δ≥3 | ∃ 2-power cycle | structural | some | " | Hu & Shen 2024 (Discrete Math) | superseded by L7 |
| **L7** | **Holds for P₁₃-free graphs** | no induced P₁₃, δ≥3 | ∃ 2-power cycle | backtracking + **computer search** | **YES** | the induced-path search algorithm (Track E) | Hegde, Sandeep, Shashank, arXiv:2410.22842 (Oct 2024, rev Feb 2025) | Can it reach P₁₄+? Extract human lemmas? |
| L8 | Holds for diameter-2 graphs | diam(G)=2, δ≥3 | ∃ cycle of length **4 or 8** | structural | no | BFS 2-layer collision counting | arXiv:2508.19302 (Aug 2025) | Only diam 2; the 4-or-8 dichotomy is a strong local lemma |
| L9 | Holds for some Cayley graph families | specific Cayley graphs | ∃ 2-power cycle | group/structural | no | voltage/Cayley cycle lengths | Aequationes Math. 2017 | Cayley = counterexample *source* too (Track A) |
| **L10** | **Counterexample lower bound** | δ≥3, no 2-power cycle | needs **≥17 vertices** | exhaustive computer search | **YES** | canonical generation + cycle check | Royle & Markström | Re-verify (Exp) |
| **L11** | **Cubic counterexample lower bound** | cubic, no 2-power cycle | needs **≥30 vertices** | exhaustive computer search | **YES** | cubic geng + cycle check | Royle & Markström | Re-verify partially (Exp) |
| L12 | Bipartite counterexample lower bound | bipartite, δ≥3, no 2-power cyc | needs **≥30 vertices** (reported) | computer search | YES | bipartite gen | (reported; source TBC) | Confirm source |
| L13 | Markström extremal graphs | cubic, 24 vertices | only 2-power cycle length present is **16** | construction | yes | shows 4- and 8-cycles avoidable simultaneously | Markström (4 graphs; one planar = "Markström graph") | Shows how hard avoidance is; a *near*-counterexample template (Track A) |
| **L14** | **Minimal counterexample is predominantly cubic** | G minimal counterexample | see M1–M5 below | structural | no | discharging-style degree argument | **Avery Carr, arXiv:2605.22844 (May 2026)** | The current structural frontier; extend the reductions (Track B) |

### L14 detail (Carr 2026) — minimal-counterexample structure

A **minimal counterexample** = graph of minimum order, then size, with δ≥3 and no
power-of-two cycle. Carr proves:

- **M1.** The vertices of degree ≥4 form an **independent set** (no two adjacent),
  and there is a nonempty set of degree-exactly-3 vertices.
- **M2.** **Every** vertex is adjacent to a vertex of degree exactly 3.
- **M3.** At least **4/7** of the vertices have degree exactly 3.
- **M4.** Every **regular** minimal counterexample must be **cubic** (3-regular).

These are the "known starting points" the task listed; all are now sourced to
Carr 2026 (M1–M4) and Royle–Markström (L10–L11). I re-derive the easy ones in
`lemmas.md` (Track B) rather than merely citing.

### L15 — McKay {C4,C8}-free extremal data ⇒ 4-or-8 theorem through n=19 [values source-verified 2026-07-25]

Source: B. McKay, "Combinatorial Data — Extremal Graphs"
(users.cecs.anu.edu.au/~bdm/data/extremal.html). The `.s6` file names encode
ex(n;{C4,C8}) directly (`c48_nN eE.s6` ⇒ ex(N)=E); read off from the page's own
links (authoritative, not a summarizer). ⌈3n/2⌉ = min edges of any δ≥3 graph.

| n  | 4 | 5 | 6 | 7 | 8 | 9 |10 |11 |12 |13 |14 |15 |16 |17 | 18 | 19 |
|----|---|---|---|---|---|---|---|---|---|---|---|---|---|---|----|----|
| ex | 4 | 6 | 7 | 9 |11 |12 |14 |15 |17 |19 |20 |22 |23 |25 | 27 | 29 |
|⌈3n/2⌉| 6 | 8 | 9 |11 |12 |14 |15 |17 |18 |20 |21 |23 |24 |26 | 27 | 29 |
| ex<⌈3n/2⌉? | ✓|✓|✓|✓|✓|✓|✓|✓|✓|✓|✓|✓|✓|✓| = | = |

For **n=4..17 the inequality is strict** (ex < ⌈3n/2⌉), so a δ≥3 graph already has
more edges than any {C4,C8}-free graph on n vertices ⇒ **no δ≥3 {C4,C8}-free graph
exists**, no case analysis needed. For **n=18,19 it is equality**, so a δ≥3
{C4,C8}-free graph would have to be *extremal* (exactly ⌈3n/2⌉ edges) and near-
regular (n=18 ⇒ Σdeg=54 ⇒ 3-regular; n=19 ⇒ Σdeg=58 ⇒ one deg-4, rest deg-3).
Inspecting the extremal files settles these:
- n=18: 570 extremal graphs, **all min-deg 2** (0 cubic) ⇒ none is δ≥3.
- n=19: 304 extremal graphs, **all min-deg 2** (0 with δ≥3).

**Local reproducibility note (updated Type-B one-slack pass):** the order-18
and order-19 `.s6` inputs are now present and match their authoritative
checksums; order 18 is also independently regenerated in the Type-B
equality-order audit. The order 16,17,20--23 inputs remain absent. See
`manifests/external_s6_manifest.json` for per-file status. The separate cubic
geng n=18 reproduction does not depend on the restored file.

**THEOREM (4-or-8 through n=19).** Every graph with δ≥3 on at most 19 vertices
contains a C4 or a C8.
- [PROVED FROM PUBLIC EXTREMAL DATA] — the ex(n) values above are McKay's.
- [COMPUTATIONALLY VERIFIED] — I processed the extremal `.s6` files (min-deg dist
  computed for every graph, n=16..19) AND independently re-derived n=18 by exhaustive
  geng: all 2761 connected cubic C4-free graphs on 18 vertices contain a C8 (0
  survivors, DFS/nx detectors agree). n=19 geng re-derivation: see experiments E5.
- [NOVELTY UNCHECKED] — do NOT call this a new literature result until a targeted
  search confirms no prior published statement. It may be folklore / implicit in
  the extremal tables.

This "4-or-8" form is *stronger* than Erdős–Gyárfás through n=19 (E–G needs any
2-power cycle, and C16 exists for n≥16). Sharp endpoint is **n=24**: a 24-vertex
cubic {C4,C8}-free graph is known (Markström, L13; only 2-power cycle length is 16).

### L15b — the n=20..23 layers still open [data source-verified 2026-07-25]

Here ex(n) **exceeds** ⌈3n/2⌉, so a δ≥3 {C4,C8}-free graph is *not* forced to be
extremal — it can live in the extremal layer OR one below. Candidate edge ranges
(⌈3n/2⌉ : ex):

| n | ⌈3n/2⌉ : ex | # extremal graphs (all δ=2, verified) |
|---|-------------|----------------------------------------|
| 20 | 30 : 31 | 94    |
| 21 | 32 : 33 | 12    |
| 22 | 33 : 34 | 13644 |
| 23 | 35 : 36 | 3257  |

**Top layer already cleared (2026-07-25):** the extremal file at each n is the
complete set of {C4,C8}-free graphs at the max edge count; I checked all four —
every extremal graph has min-deg 2, so no δ≥3 graph exists at m=ex. This disposes
of *all* excess-2 and excess-3 degree sequences (they only occur at m=ex). The
**only remaining search** is the one-below near-cubic layer:

| case | n | m | degree seq | excess 2m−3n |
|------|---|---|-----------|-----|
| 1 | 20 | 30 | 3²⁰ (cubic)  | 0 |
| 2 | 22 | 33 | 3²² (cubic)  | 0 |
| 3 | 21 | 32 | 4,3²⁰        | 1 |
| 4 | 23 | 35 | 4,3²²        | 1 |

The extremal layer is known exactly; the unresolved computational task is to
examine the extremal and one-below-extremal layers compatible with δ≥3 — and the
extremal (top) layer is now done, leaving cases 1–4. See plan.md P1 / experiments E6.

### L16 — Novelty check on S4 (bridgelessness) / S5 (cut-vertex classification)
[checked 2026-07-25; WebFetch to arxiv.org blocked by proxy policy — see caveat]

Searched for prior publication of S4/S5 (lemmas.md) before labeling them
"PROVED IN WORKSPACE, NOVELTY UNCHECKED":
- **Carr 2026 (arXiv:2605.22844, "Predominantly Cubic")**: abstract text
  (retrieved via WebSearch snippets, consistent across 3 independent
  queries) covers only M1 (deg≥4 independent set), M2 (every vertex
  adjacent to a degree-3 vertex), M3 (≥4/7 degree-3 density) — **no mention
  of bridgelessness, 2-edge-connectivity, 2-connectivity, or cut-vertex
  structure**. No stronger/equal claim to S4/S5 found in the abstract.
- Broader search found no published bridge/cut-vertex classification
  specific to Erdős–Gyárfás. "Minimal counterexample is 2-connected" is
  confirmed as classical folklore *technique* in other minimal-
  counterexample settings (cycle double cover, flow-critical graphs,
  coloring), but via a different mechanism (recombine colorings/covers on
  each side) than S4/S5's degree-preserving doubling construction — a
  spiritual analogue, not a prior instance of this exact argument.
  Neither the equal-lobe-order, degree-4-cut-vertex, nor at-most-one-
  cut-vertex refinements (S5 claims 2–5) were found anywhere.
- arXiv:2410.22842 (P13-free) and arXiv:2508.19302 (diameter-2, also Carr)
  abstracts: no connectivity content found.
- **Access caveat for this historical pass**: direct WebFetch returned HTTP
  403, so only search-returned abstract/snippet text was checked at this
  stage. L18 later obtained Carr's full text, but did not redo the targeted
  S4/S5 search against every candidate source.

**Conclusion:** no prior published statement of S4 or S5 was found in the
sources accessible to that pass. L17 records the follow-up assessment; this
is not upgraded to a priority claim.

### L17 — Second-pass targeted novelty search for S4/S5 [2026-07-25]

**Historical access note.** During L17, direct fetches to arXiv and its
mirrors returned platform-level HTTP 403 responses, so that pass relied on
search metadata and snippets. This is not a current blanket limitation: the
later L18 and L19 audits obtained and read Carr's full HTML text and the EFGS
paper PDF through the web research tool. L17's S4/S5 assessment remains
limited to its targeted metadata search; the stronger literature claims in
L18/L19 use the full texts named there.

**Targeted search results (specific phrase combinations: "minimal
counterexample" × connectivity/bridge/cut-vertex/block-decomposition;
extremal/critical-graph-theory "doubling" technique names; EG survey
articles; Royle–Markström, Gyárfás, Daniel–Shauger, Heckman–Krakovski,
Hegde–Sandeep–Shashank):**
- **S4 (bridgelessness):** no source found asserting this for EGC minimal
  counterexamples, in any paper or survey snippet searched. Heckman–
  Krakovski (Electron. J. Combin. 20(2) #P7, 2013) prove EGC for
  "3-connected cubic **planar**" graphs — but 3-connectivity there is a
  *hypothesis restricting the class studied*, not a derived property of a
  minimal counterexample; not the same claim.
- **S5 (cut-vertex classification):** no EGC-specific source found. Closest
  classical analog identified: **Dirac's theorem** (G. A. Dirac, "The
  Structure of k-Chromatic Graphs," Fund. Math. 40 (1953), 42–55) — k-
  critical (chromatic-critical) graphs have no cut vertex, with a refined
  gluing lemma for 2-vertex cuts. Same *proof pattern* (split at a cut
  vertex, recombine lobes to violate minimality), applied to chromatic
  criticality rather than cycle-length avoidance, and without S5's specific
  equal-order/equal-edge-count lobe refinement (which follows from
  lexicographic (|V|,|E|) minimality, not |V|-only). This is folklore
  technique, appropriately citable as the origin of the *method*, not a
  prior instance of S4/S5 themselves.

**Conclusion:** S4 and S5 (and by the same search, O1/O3 in one_pole.md,
which use the identical technique) appear **novel within the EGC literature
covered by those searches** — no equal-or-stronger published statement was
found after two targeted passes. Labels stand as **PROVED IN WORKSPACE,
NOVELTY SUPPORTED BY SEARCH BUT UNVERIFIED AGAINST THE FULL TEXT OF EVERY
POSSIBLE SOURCE**. Dirac 1953 is the correct citation for "this proof pattern
is a classical technique," to be used if S4/S5 are ever written up formally.

### L18 — Two-thirds cubic strengthening [audited 2026-07-25]

Carr's full four-page preprint (arXiv:2605.22844) was read, not merely its
abstract. Corollary 0.1 proves both inputs used here: every vertex is adjacent
to a degree-three vertex, and the degree-at-least-four vertices are independent.
In Theorem 0.1 Carr then uses the upper bound `e(C,H)<=3|C|`, obtaining
`|C|>=4|V|/7`. Applying Corollary 0.1 to the vertices of `C` themselves shows
that each has at least one neighbor in `C`, sharpening the same line to
`e(C,H)<=2|C|` and hence `|C|>=2|V|/3`.

Targeted searches used the exact fractions, the phrases "predominantly cubic"
and "degree exactly 3", the Carr title, and minimal-counterexample terminology.
They found Carr's `4/7` theorem and unrelated `2/3` graph results, but no prior
statement of this sharpening. Status: **PROVED IN WORKSPACE; IMMEDIATE BUT
APPARENTLY UNPUBLISHED STRENGTHENING**. This is deliberately not a priority or
novelty claim.

### L19 — Degree-3-critical boundary and the edge bound [literature + workspace]

The modern definition is documented by Narins--Pokrovskiy--Szabó (2015) and
Di Braccio--Katsamaktsis--Ma--Malekshahian--Zhao (2025/2026): an `n`-vertex
graph with `2n-2` edges and no proper induced subgraph of minimum degree at
least three. Narins et al. explicitly explain that the 1988 paper's phrase
"proper subgraph" is interpreted as "proper induced subgraph" for this class.
They also record the theorem of Erdős--Faudree--Gyárfás--Schelp that every
degree-3-critical graph on `n>=5` contains cycles of lengths 3, 4, and 5.

Combining this classical theorem with Carr's proper-subgraph lemma and the
standard extremal edge count for a 2-degenerate graph yields the workspace
bound `m<=2n-3` (G2 in `lemmas.md`). Targeted searches found the ingredients
but no prior EGC-specific statement of this exact bound. Status:
**PROVED IN WORKSPACE FROM KNOWN LITERATURE INGREDIENTS; APPARENTLY UNPUBLISHED
AS AN EGC MINIMAL-COUNTEREXAMPLE COROLLARY**. The associated `q` identity is
elementary bookkeeping, not treated as a novelty claim.

### L20 — EFGS 1988 vs. Narins–Pokrovskiy–Szabó 2017: proved vs. disproved boundary [2026-07-26, access-limited]

Direct fetch of arXiv:1408.5289 (and its Springer/mirror pages) returned
HTTP 403 in this environment — the same confirmed hard platform-level
block recorded in L16/L17; this pass relies on WebSearch-returned
abstracts/snippets from three independent queries, cross-checked against
each other for consistency, not full text.

**What is proved (stands, used by G2 unmodified):** Erdős, Faudree,
Gyárfás, Schelp (1988) prove every degree-3-critical graph (n vertices,
`2n-2` edges, no proper induced subgraph of min degree `≥3`) on `n≥5`
vertices contains cycles of length 3, 4, and 5.

**What EFGS 1988 additionally *conjectured* (separate from the above) and
what NPS 2017 (Combinatorica 37, 495–519) *disprove*:** EFGS conjectured
every degree-3-critical graph has cycles of **all** lengths
`3,4,5,…,C(n)` for some `C(n)→∞`. Narins–Pokrovskiy–Szabó disprove this:
they construct arbitrarily large degree-3-critical graphs with **no cycle
of length 23** (not length 4 — the base `{3,4,5}` theorem is untouched),
via **1–3 trees** (every vertex degree 1 or 3) with no two leaves at
distance 20, closed by two extra vertices adjacent to every leaf and to
each other. They also characterize all `n`-vertex, `2n-2`-edge graphs with
no proper subgraph of minimum degree 3, and pose several weaker
conjectures about degree-3-critical cycle-length spectra and 1–3-tree
leaf-to-leaf path lengths — later work (arXiv:2504.11656,
Di Braccio–Katsamaktsis–Ma–Malekshahian–Zhao) resolves several of these,
proving `Ω(log n)` distinct cycle lengths and settling a leaf-to-leaf
path-diversity conjecture in strong form.

**Relevance to D1 (defect.md Part II):** the base `{3,4,5}` theorem
(unaffected by the disproof) is exactly what G2 uses and remains valid.
The 1–3-tree construction is structurally close to the `β(F)=0` (`F` a
forest) tight case identified in defect.md II.3, flagged there as the most
promising entry point for a future D1 proof attempt — NOT claimed as
resolving D1 here, since NPS's own two closing vertices are mutually
adjacent (violating this project's `H`-independence M1) and their target
(arbitrary cycle-length diversity) is a different question from "must
contain length 4 or 8 specifically." Status: **KNOWN FROM LITERATURE
(search-supported only, full text inaccessible from this environment —
same permanent limitation as L16/L17)**; no priority or novelty claim is
made about any connection drawn here between NPS's construction and the
`β(F)=0` case, which is original observation, not a literature claim.

### L21 — Novelty check on the voltage-graph/lift methodology (Part III/IV) [2026-07-26]

Targeted search ("Erdos-Gyarfas voltage graph", "graph lift cycle avoidance
cubic", "cyclic Z_p lift power of two cycle") found substantial general
voltage-graph/graph-cover literature (LDPC-code cycle-distribution
analysis, cage constructions via voltage graphs, pseudo-Loupekine snarks
as Zm lifts, isomorphism criteria for abelian-group voltage assignments)
but **no prior application of voltage-graph lifts to Erdős–Gyárfás
counterexample search specifically**. Status: **novelty supported by
search only** (same permanent access-limited ceiling as L16/L17/L20 — no
arXiv full text reachable from this environment); not a priority claim.
The general technique (cyclic lifts, voltage assignments, holonomy) is of
course long-classical (Gross–Tucker); what is not found elsewhere is its
application to systematically eliminate candidate EGC counterexamples
from a fixed small set of extremal near-miss bases, or the algebraic
compression technique of III.2/III.3 (reducing an exhaustive lift search
to a small covering set of cycle-space hyperplanes).

### L22 — Novelty check on q(G)>=2 / the leaf-graph theorem [2026-07-27]

Targeted search ("Erdos-Gyarfas minimal counterexample defect one",
"q=1", "2n-3 edges", "cubic-core high degree vertices") found Carr 2026's
M1-M4, Royle-Markstrom's order bounds, and general survey material --
**no prior statement of a "defect"/`q` parameter, the cubic-core
decomposition (C,H,F,beta(F)), the derived leaf graph L(G), or any
q(G)>=2-type bound** for Erdos-Gyarfas minimal counterexamples. Since `q`
and the cubic-core decomposition are this project's own constructions
(introduced in the 2026-07-26 pass, not found in any external source
across this project's entire literature audit L1-L21), this negative
result is unsurprising and is recorded conservatively, at the same
"novelty supported by search, full external verification desirable"
ceiling used throughout this project (S4, S5, G1, G2) -- not a priority
claim.

### L23 — Defect-three (q=3) literature audit [2026-07-26]

**Carr 2026 (M1–M4, L14/L18).** No content beyond what L18 already
extracted (independence of `H`, `e(C,H)<=2|C|`) is used or needed by the
defect-three phase; nothing in Carr's four pages addresses `q`,
branching kernels, or colored-path structure (these remain this
project's own constructions, per L22).

**The P13-free theorem (Hegde–Sandeep–Shashank, L7).** Used exactly
once, precisely within its stated hypotheses: `defect_three.md` Part
III.2's `h=1` elimination shows `n<=13` and that `G` cannot itself equal
a `P_{13}` (a path has degree-1 endpoints, contradicting `δ(G)\ge3`),
so `G` is `P_{13}`-free at every reachable order — the theorem's
hypothesis is met exactly, not stretched.

**Choi–Chu–Kim–Park, arXiv:2605.02731 (May 2026), "Existence of cycles
of length divisible by 3 or 4."** Located via targeted search; **direct
fetch of both the abstract page and the HTML mirror returned HTTP 403**
(the same permanent access-limited ceiling recorded at L16/L17/L20/L21
— this project has never obtained full-text access to an arXiv page
returning this error). Per the search-engine-returned abstract text
only: for `k\in\{3,4\}`, every graph with minimum degree `\ge2` and at
most `k-2` vertices of degree 2 has a cycle of length divisible by `k`,
and the authors characterize the exceptional graphs at the boundary.
**Read literally, the `k=4` case bounds the degree-2-vertex count by
`k-2=2`, not `3`** — the task's own phrasing ("min-degree-2-with-
`\le3`-degree-2-vertices characterization") does not exactly match the
abstract snippet found here; this discrepancy is recorded rather than
silently resolved, since the primary source could not be read. **This
theorem is NOT used anywhere in this project's `q=3` elimination**
(Parts I–VIII above), consistent with the task's explicit warning: "a
cycle length divisible by four is not automatically a power-of-two
cycle" — none of this project's forbidden-cycle checks (C4, C8, C16)
would be satisfied merely by *divisibility* by 4 (e.g. a C12 is
divisible by 4 but is not itself forbidden by Erdős–Gyárfás). Recorded
for completeness only; no reliance, no novelty claim either way.

**Classical subcubic suppression / topological-kernel results.** The
"kernel suppression" operation used throughout Parts I, VI, VII
(replacing maximal degree-2 paths by single edges to expose a
multigraph on the odd-degree vertices) is standard, classical graph
theory — sometimes called the *topological reduction* or
*homeomorphic reduction* of a graph, going back to Whitney-era
structural graph theory (subdivisions, topological minors). No specific
citation is claimed as novel; this project's contribution is the
application (bounding kernel size by `q`, then exhaustively enumerating
and reconstructing kernels under the colored-path/cycle constraints),
not the suppression operation itself.

**Overall novelty posture, consistent with L21/L22.** The q=3
elimination (bounded branching-kernel lemma, the exact case table, the
colored-path/cycle lemmas and their finite-state-automaton/stub-
matching computational machinery, and the full kappa=1/kappa=2
topological-kernel enumerations for both `h=2` rows and both `h=3`
rows) is, like the leaf-graph/q>=2/q>=3 results before it, **this
project's own construction**, built on Carr's M1/M2 and the classical
`P_{13}`-free citation but not found stated anywhere in the literature
searched across L1–L23. Recorded at the same **novelty supported by
search only, full external verification desirable** ceiling used
throughout — not a priority claim.

### L24 — Cited external theorems actually used in proofs [consolidated 2026-08-18]

Three published results are load-bearing in this project's own arguments
and were previously recorded only inside `manuscript.md`'s reference list
rather than in this master file. They are added here so that no proof
depends on a citation that lives outside `literature.md`.

**(a) Gao, Huo, Liu, Ma 2022 — the admissible-path theorem.**
Jun Gao, Qingyi Huo, Chun-Hung Liu, Jie Ma, "A Unified Proof of Conjectures
on Cycle Lengths in Graphs," *International Mathematics Research Notices*
2022(10):7615–7653; arXiv:1904.08126 (2019).
*Statement used (k = 2):* if `K + xy` is 2-connected and every vertex of
`K \ {x,y}` has degree ≥ `k+1`, then `K` contains `k` **admissible** `x`–`y`
paths — lengths forming an arithmetic progression with common difference 1
or 2. **Important:** the paths are **not** claimed internally disjoint, and
none of this project's applications needs them to be.
*Where used:* **O4′** (`one_pole.md`, `manuscript.md` §3), **T2**
(`two_cut.md`), and by citation in **MA1** (`contraction_block_cut_tree.md`
Part IV) and **CB3′** (`contraction_separator_integration.md` VI.2).
*Verification status:* `HYPOTHESES MATCHED VIA SEARCH-RETURNED
ABSTRACT/SNIPPET ONLY`. The full text was never readable in this
environment (see the access note below). The statement's hypotheses and
conclusion were checked against search-returned material and against the
2-connectivity fact (`K+ab` 2-connected via classical degree-2 suppression)
that this project proves separately.

**(b) Dirac 1953 — the historical cut-vertex technique.**
G. A. Dirac, "The Structure of k-Chromatic Graphs," *Fundamenta
Mathematicae* 40 (1953), 42–55.
*Relevance:* this is the closest classical analog to **S4/S5** — the same
mechanism (split at a cut vertex, recombine to build a smaller contradicting
instance), used there to show chromatic-critical graphs have no cut vertex.
It is a **different theorem**, and it does not carry S5's equal-order /
equal-edge-count lobe refinement, which needs lexicographic `(|V|,|E|)`
minimality rather than order alone. Recorded explicitly so that S4/S5's
*technique* is not presented as original — only their statements are, and
those only at the `NOVELTY SUPPORTED BY SEARCH` ceiling.

**(c) Dirac 1961 — chordal graphs, used in O5's second proof.**
G. A. Dirac, "On rigid circuit graphs," *Abhandlungen aus dem Mathematischen
Seminar der Universität Hamburg* 25 (1961), 71–76.
*Statement used:* a chordal graph that is not complete has ≥2 non-adjacent
simplicial vertices.
*Where used:* the second, **convention-independent** proof of **O5** (the
rigid-core / K4-minor lemma) via partial 2-trees — complete a
series-parallel graph to a 2-tree, which is chordal and non-complete, and
sandwich the two simplicial vertices to degree exactly 2. This proof exists
precisely so that O5 does not rest on any SPQR-tree normalization
convention; the two proofs were cross-checked computationally against each
other and against two flawed hand-examples that both algorithms reject
(independently: the examples register treewidth 3, so they are genuinely
not partial 2-trees).

**Supporting algorithmic citations** (used by the computational side, not
by any proof): C. Gutwenger, P. Mutzel, "A Linear Time Implementation of
SPQR-Trees" (2001), correcting J. E. Hopcroft, R. E. Tarjan, "Dividing a
Graph into Triconnected Components" (1973), with data structures from
G. Di Battista, R. Tamassia, "On-Line Planarity Testing" (1996) — the
algorithm behind the `spqrtree` package used throughout the one-pole work.
Also **Whitney 1932** (`κ ≤ λ ≤ δ`), used in `cubic_edge_connectivity.md`,
and the **Alon–Hoory–Linial irregular Moore bound**, used in the audit of
the length-16 tangle theorem's Lemma 2.

### Access limitation — a tooling gap, restated because it caps every novelty label

Direct access to arXiv and to every tested mirror returns **HTTP 403 at the
platform/proxy level**, confirmed by direct `curl` through the egress proxy
and not merely by the fetch tool (L16, L17). **No full paper body has been
read for any citation above.** Consequences, stated plainly rather than
hedged:

1. Every "novelty" label in this repository is capped at
   **NOVELTY SUPPORTED BY SEARCH** and can never be upgraded from this
   environment. It means "two targeted search passes over
   abstracts/snippets found no prior statement" — nothing stronger.
2. Where even that is an overstatement, the label used is
   **NOVELTY UNCHECKED** (e.g. the 4-or-8 dichotomy through `n=19`, which
   may well be implicit in the extremal tables).
3. This is a **tooling gap, not a mathematical one**, and the correct
   response is to obtain real literature access — not to keep restating the
   ceiling. It is an action item in RETROSPECTIVE.md, not a permanent
   condition of the project.
4. The one exception on record: Carr's four-page preprint
   (arXiv:2605.22844) *was* obtained in full HTML and read (L18), which is
   why G1's audit is stronger than the rest.

## Verified vs. to-verify (my independent checks — see experiments.md)

- L10 (≥17): I reproduce exhaustively as far as compute allows via `geng` +
  my validated detector; status recorded in experiments.md.
- L11 (cubic ≥30): reproduce for cubic graphs up to the feasible order.
- M1–M4: re-derive the connectivity/degree reductions from scratch in lemmas.md.

## Sources
- AMS grad blog, "The Erdős–Gyárfás Conjecture" (overview, bounds, Markström graphs).
- arXiv:2410.22842 — Hegde, Sandeep, Shashank, "Erdős–Gyárfás conjecture on graphs without long induced paths" (P₁₃-free).
- arXiv:2508.19302 — "Cycles of Length 4 or 8 in Graphs with Diameter 2 and Minimum Degree at Least 3."
- arXiv:2605.22844 — Avery Carr, "Every Minimal Counterexample to the Erdős–Gyárfás Conjecture is Predominantly Cubic."
- D. West, Open Problems Graph Theory (2powcyc): Daniel–Shauger, Shauger K₁,ₘ-free.
- ScienceDirect/Discrete Math (Hu & Shen, P₁₀-free 2024; Gao & Shan, P₈-free 2022).
- MathWorld "Markström Graph."
- arXiv:2605.02731 — Choi, Chu, Kim, Park, "Existence of cycles of length divisible by 3 or 4" (abstract snippet only; full text inaccessible, see L23).
- arXiv:1904.08126 / IMRN 2022(10):7615–7653 — Gao, Huo, Liu, Ma, "A Unified Proof of Conjectures on Cycle Lengths in Graphs" (admissible-path theorem, applied with k=2 in O4′ and T2; see L24a).
- G. A. Dirac, "The Structure of k-Chromatic Graphs," Fundamenta Mathematicae 40 (1953), 42–55 (the historical cut-vertex split-and-recombine technique behind S4/S5; see L24b).
- G. A. Dirac, "On rigid circuit graphs," Abh. Math. Sem. Univ. Hamburg 25 (1961), 71–76 (chordal graphs have ≥2 non-adjacent simplicial vertices; O5's second proof; see L24c).
- C. Gutwenger, P. Mutzel, "A Linear Time Implementation of SPQR-Trees" (2001); J. E. Hopcroft, R. E. Tarjan, "Dividing a Graph into Triconnected Components" (1973); G. Di Battista, R. Tamassia, "On-Line Planarity Testing" (1996) — the `spqrtree` algorithm stack.
- H. Whitney, "Congruent graphs and the connectivity of graphs" (1932) — κ ≤ λ ≤ δ, used in `cubic_edge_connectivity.md`.
- N. Alon, S. Hoory, N. Linial, "The Moore bound for irregular graphs" (2002) — used in the length-16 tangle audit.
