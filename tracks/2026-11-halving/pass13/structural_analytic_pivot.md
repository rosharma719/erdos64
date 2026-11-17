# Pass XIII (revised): audit of the bounded-defect / expander program

**Source baseline:** user-supplied stamp `c3a61f6`, `claude/additive-reduction-brief`, PR #5.  
**Status discipline:** PROVED means a self-contained argument below; COMPUTED means two structurally independent implementations with the recorded manifests; CONDITIONAL means a named unproved assumption is used; OPEN means no proof here. No source tree, status map, or shared solver was modified.

## Executive verdict

**OPEN:** The proposed two-half program has a genuine interface gap. As stated, boundedness `F(k)` does not entail the uniform expansion hypothesis of the Friedman–Krivelevich theorem. Moreover, a non-rooted cycle-length theorem for the cubic cap of a clean pole does not certify a cycle in the pole: the cycle may use the artificial cap vertex.

**PROVED:** Two bridge-gluing reductions give useful quantitative constraints on bounded defects. **COMPUTED:** the order-six clean four-pole classification has two independently matching streams.

### Proposition 1: bridge-gluing and monotonicity of bounded defects [PROVED]

Let `P` and `Q` be clean `k`- and `l`-poles, with `k,l >=1`; join a degree-two vertex of `P` to a degree-two vertex of `Q` with one new edge. The joined graph is a clean `(k+l-2)`-pole and has `|P|+|Q|` vertices. Its new edge is a bridge, hence introduces no cycle, and its incident degree-two vertices become degree three.

Taking `Q = K3`, a clean three-pole, gives a clean `(k+1)`-pole of order `|P|+3`. Consequently, **if** a universal upper bound `N(k+1)` exists, then one exists for `k`, and the maximum sizes, when defined, satisfy `N(k+1) >= N(k)+3`.

This demonstrates that proving `F(4)` already proves `F(3)` in its existential boundedness form. The stronger conjecture T, which gives an explicit list of clean three-poles, does **not** follow from existential `F(3)` alone.

### Proposition 2: exact size in the bridge-tree subclass [PROVED]

Take `t` vertex-disjoint genuine clean three-poles of orders at most 15 and connect them according to a tree with maximum degree at most three, using different degree-two vertices for different bridge edges. The result is a clean `(t+2)`-pole, because

`k=3t-2(t-1)=t+2`.

Its order is at most `15t=15(k-2)`. Equality is attained by taking `t` copies of H15 and joining them in a path. Hence **every** possible universal upper bound on clean k-pole order must satisfy `N(k) >= 15(k-2)` for `k>=3`. In particular, `N(4) >=30`.

These bounds are for the bridge-tree subclass; they do not classify arbitrary poles.

### Proposition 3: terminal saturation [CONDITIONAL on no clean (k-2)-poles]

Suppose no clean `(k-2)`-pole exists, where `k>=3`. Let `P` be a clean `k`-pole and let `u,v` be two **nonadjacent** degree-two vertices of `P`. Then `P` contains a simple `u-v` path of length `2^j-1` for some `j>=2`.

**Proof.** If adding edge `uv` introduced no power-of-two cycle, the resulting connected simple graph would be a clean `(k-2)`-pole, contradicting the assumption. Every power-of-two cycle of `P+uv` must use the new edge, because `P` was clean; deleting that edge leaves the required `u-v` path. QED.

For k=4 the premise is the still-OPEN claim that clean 2-poles do not exist at any order. This is a directly relevant path-spectrum obstruction; it does not require the full exact even-length expander theorem.

### Structural cut calculation: what bounded defects actually provides [CONDITIONAL]

Let `P` be a clean k-pole. Let `S` induce a **connected** subgraph such that each edge crossing the cut has a distinct endpoint in `S`, none of which was an original degree-two vertex. Put `c=|delta(S)|` and let `t` original degree-two vertices lie in `S`. Then `P[S]` is a clean `(t+c)`-pole, and **if F(t+c) is known with a bound `N(t+c)`**, then

`|S| <= N(t+c) <= max_{m<=k+c} N(m)`.

The distinct-endpoint and disjointness hypotheses matter. A general four-edge cut may hit an interior vertex twice, creating degree-one vertices in the induced shore, which are excluded from the current `k`-pole definition. A more general half-edge/stub interface would handle such cuts.

This inequality does not follow from minimality alone. F(t+c) is an additional global hypothesis and may involve a **larger** number of defects than the `k` under investigation. An existential function `N` need not be linear. Inverting this bound need not give `|delta(S)| >= alpha |S|` with a fixed `alpha>0`. A quantitative uniform *proper-shore* isoperimetric bound (and a careful handling of repeated boundary incidences) is the actual structural target.

### Expansion after deleting the cap vertex [PROVED]

If `H` is an alpha-vertex-expander and `H-v` is connected, then `H-v` is an `(alpha/2)`-vertex-expander. For any nonempty `S subset V(H-v)` of size at most `|V(H-v)|/2`, its external neighborhood in `H-v` has size at least `alpha|S|-1`. If `|S| >=2/alpha`, this is at least `(alpha/2)|S|`. For smaller `S`, connectedness yields at least one external neighbor, and `1 >=(alpha/2)|S|`.

However, the three neighbors of the cap vertex have degree **two** after deletion. The candidate analytic theorem assuming minimum degree at least three does not apply to `H-v`. A theorem allowing a bounded number of degree-two defects, or one that guarantees the desired cycle avoids any specified root, is needed.

## The analytic half: strongest honest formulation

**KNOWN:** Friedman–Krivelevich (2021) prove that an alpha-vertex-expander on `n` vertices has a cycle in each interval `[ell,ell+A(alpha)]` for `ell` from `C(alpha)log n` through `c(alpha)n`. It is a bounded-gap statement, not an exact-length statement. **KNOWN:** their general subdivision example creates low-degree vertices and shows the dependence of A on alpha is necessary. It is not a classification of all possible exact-length obstructions.

**OPEN:** The proposed theorem that every even length in `[C log n, c n]` occurs for every sufficiently large alpha-expander of minimum degree at least three was not located among the searched sources. A proof is not supplied here. It is stronger than needed for Erdős–Gyárfás, and even if proved, does not directly handle the three degree-two vertices in `H-v`.

**PROPOSED C2 replacement (OPEN):** At a fixed alpha and defect budget k, prove that every sufficiently large connected alpha-vertex-expander with at most k degree-two vertices (all others degree at least three) contains at least one cycle of power-of-two length in `[C log n,c n]`. A stronger, optional target is a whole interval of even lengths. This is naturally compatible with clean 3-poles and avoids the root-avoidance oversight.

**Alternative stronger analytic mechanism (OPEN):** For a power `q=2^j` in the Friedman–Krivelevich scale, find a cycle within A(alpha) edges of q and a disjoint/compatible system of reroutings that changes its length to exactly q. Only bounded correction near one power is needed; producing all even lengths is a separate and stronger problem.

## Four-pole base case [PROVED independently by a short classification, COMPUTED by two checkers]

At order four, every vertex of a 4-pole has degree two, so the only connected possibility is `C4`, forbidden. Thus no clean 4-pole has order four.

At order six, there are exactly two unlabelled clean four-poles:

1. Two triangles joined by a single bridge, with internal cycle-length set `{3}`.
2. A six-cycle with a chord joining two vertices at distance two along the cycle, with internal cycle-length set `{3,5,6}`. This second graph is bridgeless and is an exception to a pure bridge-tree description.

To see completeness by hand, let `u,v` be the two degree-three vertices. If they are nonadjacent, they share at least two of the remaining four neighbors, creating a four-cycle. Hence `u,v` are adjacent. They have either zero, one, or two common degree-two neighbors. Two shared neighbors create a four-cycle. Zero shared neighbors force two disjoint triangles joined by `uv`, once four-cycles are excluded. One shared neighbor forces the chorded six-cycle. Both examples avoid 4- and 8-cycles.

A NetworkX Graph Atlas filter and an independent C labeled-graph bit-mask enumerator output the same complete class stream with SHA-256
`8c63b71acea99bd00f48c013354e6395e9a2b46eda2763bee2db80c9f480d3d3`.
Both exit 0. There are two unlabelled classes and 450 labeled graphs in total. See `census/four_pole_manifest.json`. This check is **not** a census beyond order six.

## C1 independent audit of joint-minimality (sealed file opened during initial bundle inspection)

**Protocol exception:** the sealed proof was read before a blind derivation. This is a line-by-line independent audit, **not** the requested blind review. Do not advance J1's blueprint status on the basis of this check alone.

- Step 1 (minimal clean 1-pole): **VERIFIED**. Deleting the only degree-two vertex yields a smaller clean 2-pole if connected, otherwise a smaller clean 1-pole component.
- Step 2 (minimal clean 2-pole): **VERIFIED**. The nonadjacent-terminal case reduces to a smaller clean 3-pole, and every known 3-pole has a terminal pair path length `2^j-2`, so reattaching the deleted vertex produces a dyadic cycle. Adjacent-terminal subcases reduce to smaller clean 1- or 2-poles.
- Step 3 (cap has no 1- or 2-edge cuts): **VERIFIED**. A two-edge cut with both ends on one vertex induces a bridge upon removing that vertex from the shore; distinct endpoints give a smaller clean 2-pole.
- Step 4: **CONDITIONAL** on the previously REVIEWED cyclic 3-cut decomposition (D1a) and the K4 substitution table (K2); the reduction uses both. No counterexample to the step found here.
- Overall `WRP => T*`: **PROVED-DRAFT remains unchanged**, pending protocol-compliant review/sign-off under project rules.

## Revised Pass XIII priorities

1. **C1:** preserve independent review of J1; a truly blind audit must be performed by a reviewer that has not opened the sealed proof.
2. **C2a (structural, small decisive task):** classify clean four-poles; begin with the two order-six types, distinguish bridge-tree and 2-edge-connected families, and test whether attaching small pieces can be iterated while keeping exactly four defects.
3. **C2b (structural, substantive):** formulate *proper-shore* boundedness for half-edge boundary components, with a quantitative expansion profile. Do not infer linear expansion from existential F(k).
4. **C2c (analytic):** seek a dyadic-length theorem for expanders with at most three degree-two vertices, or a root-avoiding version for cubic caps. The bounded-gap + bounded-adjuster route is a weaker sufficient target than all even lengths.
5. **C3:** the existing 18 shard manifests reconcile all generated counts and checker-source hashes, but the current certification shell script does **not record or check checker B's exit code**: B runs in a process substitution behind `awk`, outside `PIPESTATUS`. The `nauty_geng` field contains a Usage message, not a version. The script needs a corrected exit-status capture and future reruns before the strict per-checker-exit certification contract can be met. Independent generator completeness for 21 remains unverified here. This pass adds the independently certified order-six 4-pole check.

## Existing census method: detailed audit [PARTIALLY VERIFIED]

I inspected all 18 supplied `census/*.json` files and the actual `certify_pole_shard.sh`, `cycle_check.c` and `verifier/check_power_masks.c` sources. All 18 manifests record matching `raw_count`, `checker_A_count`, and `checker_B_count`; matching clean counts; `geng_exit=tee_exit=checker_A_exit=0`; valid degree arithmetic; and source SHA256 values matching the copies in the bundle. The order-21 shard counts add to `18,580,327` as reported.

**REFUTED (strict certification assertion):** The script claims to require both checker exit codes to be zero. In fact the B checker is started in a process substitution, piped to `awk`, and its exit status is neither captured nor checked. No manifest has a `checker_B_exit` field. Thus there is independent count agreement but not the explicitly required B exit-code certificate. The `nauty_geng` field is the output of `geng -h | head -1`, and in these manifests it is a `Usage:` line rather than a version identifier. A correction should capture and wait for checker B's PID (or run both checkers sequentially on a saved stream) and record a `geng` binary SHA256 or verified release identifier.

The audit utility `census/audit_prior_manifests.py` exits 1 under the strict contract: all 18 counts and source hashes pass, missing B exit and version are flagged. This is a **method audit**, not a rerun of the original `geng` streams.

## What remains OPEN

- F(k) for any unbounded value of k (except logical implications above).
- All clean 4-pole classes beyond order six.
- Uniform quantitative proper-shore isoperimetry or a theorem showing it follows from joint minimality.
- The exact or bounded-correction dyadic expander theorem at minimum degree three with bounded defects.
- A deduction of the general Erdős–Gyárfás conjecture from the proposed two-half loop.

## Relevant literature

- Friedman and Krivelevich, *Cycle lengths in expanding graphs*, Combinatorica 41 (2021), arXiv:1912.11011.
- Martinsson and Steiner, *Cycle lengths modulo k in expanders*, European Journal of Combinatorics 109 (2023), arXiv:2204.09107.
- Liu and Montgomery's sublinear-expander / adjuster theorems, as surveyed in the 2026 ICM chapter *Recent Progress in Graph Theory Using Expansion*.
