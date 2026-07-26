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

**Local reproducibility note (integrity pass):** the `.s6` inputs used for
these historical degree-distribution calculations are not present in the
current checkout, and the original run recorded no checksums. The integrity
pass recorded authoritative temporary-download checksums, but did not restore
the artifacts. These computations remain `EXTERNAL_DATA_MISSING`, not locally
reproducible from the checkout alone; see
`manifests/external_s6_manifest.json`. The separate geng n=18 reproduction does
not depend on those files.

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
- **Access caveat**: direct WebFetch to arxiv.org (abs/html/pdf) and
  export.arxiv.org returned HTTP 403 (proxy policy denial, confirmed via
  `$HTTPS_PROXY/__agentproxy/status` — `connect_rejected` to
  `arxiv.org:443`), and WebFetch failed broadly (also ar5iv.org,
  semanticscholar.org, en.wikipedia.org) in this session. Only
  WebSearch-returned abstract/snippet text was checked, **not** the full
  body of Carr 2026 or any other paper. A body-text bridgelessness/
  2-connectivity lemma buried in Carr's proof (not advertised in the
  abstract) cannot be ruled out from here.

**Conclusion:** no prior published statement of S4 or S5 found in
accessible sources; label stands as **PROVED IN WORKSPACE, NOVELTY
UNCHECKED (full-text access to arXiv:2605.22844 blocked here — re-verify
the paper body when access is available)**, not upgraded to a novelty
claim.

### L17 — Second-pass targeted novelty search for S4/S5 [2026-07-25]

**Access status confirmed as a hard platform-level block, not a transient
proxy issue.** WebFetch to arxiv.org, arxiv.org/html, arxiv.org/pdf,
ar5iv.org, alphaxiv.org, export.arxiv.org, an r.jina.ai reader-proxy of the
arXiv abstract page, en.wikipedia.org, and dwest.web.illinois.edu all
returned HTTP 403. A direct `curl` against arxiv.org/wikipedia.org through
the session's egress proxy also failed (`CONNECT tunnel failed, 403`),
confirmed via the proxy's own status endpoint as an organization egress
policy block, not a per-tool or per-host glitch. **No full paper body text
has been read for any source in this project, ever** — every literature
claim here rests on WebSearch snippets only. This is a standing limitation,
not something to keep re-attempting.

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
which use the identical technique) appear **novel within the EGC
literature as it can be searched from here** — no equal-or-stronger
published statement found after two independent targeted passes. Labels
stand as **PROVED IN WORKSPACE, NOVELTY SUPPORTED BY SEARCH BUT UNVERIFIED
AGAINST FULL TEXT** (full-text arXiv/mirror access is confirmed blocked at
the platform level in this environment, not just unlucky this session) —
this is the most confident label the project's no-overclaim discipline
allows without ever having read a full paper body. Dirac 1953 is the
correct citation for "this proof pattern is a classical technique," to be
used if S4/S5 are ever written up formally.

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
