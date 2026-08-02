# contraction_intersections.md — decomposing non-clean witness intersections

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Builds on `contraction_atoms.md` and
`contraction_mixed_witness.md`, which stopped at "clean" (internally
disjoint) witness overlaps and left the general case explicitly open.
This file resolves that general case as far as it honestly goes.

## Part V: non-clean path intersections

### V.1. Exact cell decomposition [PROVED, for the non-crossing case; general crossing case deferred to V.3]

Let `P,Q` be two simple `s`–`t` paths. Write `M=V(P)\cap V(Q)`
(`s,t\in M` always). **Assume for this subsection that `M`'s vertices
occur in the *same relative order* along both `P` and `Q`** (the
*non-crossing* hypothesis; V.3 below is exactly where this can fail and
must be handled separately). Under this hypothesis, list `M` in that
common order `s=m_0,m_1,\dots,m_k=t`. Between consecutive landmarks
`m_i,m_{i+1}`, `P` has a sub-path of length `\alpha_i` and `Q` has one
of length `\beta_i`, and — by maximality of consecutive common
vertices — **neither sub-path contains any other vertex of `M`, nor
(automatically, since `M` is defined as *all* shared vertices) any
other vertex of the other path at all.**

**Each cell is one of exactly two kinds [PROVED, exhaustive].**
- **Common component:** `P`'s and `Q`'s sub-paths between `m_i,m_{i+1}`
  are the *identical* sequence of edges (`\alpha_i=\beta_i`, same
  route). No cycle arises from retracing an identical path; this cell
  contributes to `|P|,|Q|` equally and is excluded from cycle-generating
  consideration.
- **Divergent cell:** the two sub-paths are genuinely different routes
  (whether or not `\alpha_i=\beta_i` numerically). Since neither
  sub-path meets the other outside its own two endpoints
  (maximality of `M`, above), **the two sub-paths share only `m_i,m_{i+1}`
  — they combine (Lemma D) into a genuine simple cycle of length
  `\alpha_i+\beta_i`.**

**The exact identity [PROVED].**
\[
|P|-|Q|=\sum_{i=0}^{k-1}(\alpha_i-\beta_i)
=\sum_{i\text{ divergent}}(\alpha_i-\beta_i)
\]
(common-component cells contribute `\alpha_i-\beta_i=0` identically, so
excluding them from the sum changes nothing — this is the precise sense
in which "common segments [are] removed from both totals": not that the
identity requires it, but that doing so does not affect it and isolates
the cycle-generating content). **Every divergent cell yields a simple
cycle of length `\alpha_i+\beta_i`; common-component cells yield no
cycle at all** — a distinction the task's phrasing elides and this file
makes explicit, since conflating them would misstate which cells are
actually cycle-generating.

**Computational cross-check.** `verifier/intersection_diagrams.py`'s
`check_cell_decomposition` builds explicit multi-cell gadgets (mixed
common/divergent cells, non-crossing by construction) and verifies the
identity and every divergent cell's cycle length directly.

### V.2. The one-cell reduction target — tested, and found FALSE [DISPROVED, smallest exact obstruction given]

**Claim tested:** *under the joint canonical witness choice
(`contraction_mixed_witness.md` III.2), two same-endpoint witnesses
always reduce to exactly one divergence-reconvergence cell.*

**This is false, and the canonical-choice criteria do not by
themselves prevent the counterexample.** The canonical choice minimizes
(3) total shared-edge count and (4) shared-*component* count — both of
which a genuine multi-cell configuration can already satisfy at their
minimum (zero shared edges, zero common components) while still having
`\ge2` **divergent** cells, because minimizing shared edges/components
says nothing about how many *distinct* intermediate vertices the two
paths happen to cross. **Smallest exact obstruction:** two `s`–`t`
paths sharing exactly one intermediate vertex `m` and no edges, with
cell data `(\alpha_1,\beta_1)=(2,3)` and `(\alpha_2,\beta_2)=(3,2)` —
`0` shared edges, `0` common components (already minimal on criteria
3–4), yet **2** divergent cells, each yielding a 5-cycle (`\alpha_i+
\beta_i=5`, safely non-forbidden, so this obstruction is not itself
excluded by C4/C8-freeness — a genuine realizable structural
possibility, not merely a numeric curiosity). `|P|=5=|Q|`, illustrating
that even *equal total length* does not imply a single clean cell.

**What this means for later work.** "Assume the canonical witnesses are
clean (one cell)" is **not** licensed by the canonical choice alone; it
is a genuinely separate hypothesis that must be checked or additionally
justified case by case, not inferred from minimal overlap. The earlier
"clean case" results in `contraction_atoms.md`/`contraction_mixed_witness.md`
remain correct as conditional statements ("if clean, then...") — this
finding shows that conditional cannot be silently upgraded to
unconditional via the canonical choice.

**On replacement.** *Could one divergent cell replace the whole witness
and improve the canonical tuple?* Only if a genuine alternative simple
`m_i`–`m_{i+1}` witness realizing the *same* role (feeding into the same
power-of-two-cycle argument) actually exists in `G` with a smaller
exponent — this is not automatic; the cell-decomposition identity alone
supplies no such replacement, it only describes the existing witnesses'
structure. **No replacement is claimed or constructed here.**

**Computational cross-check.** `check_one_cell_target_false` builds the
smallest obstruction above as an explicit gadget, confirms `0` shared
edges/components while exposing exactly 2 divergent cells, and confirms
both cell-cycle lengths (`5,5`) are realized and non-forbidden.

### V.3. Different-endpoint intersections among `\{a,b,c\}` [framework given; full uncrossing not carried out]

For the three terminals `a,b,c` (as they arise from `P_a,P_b,P_c,Q_{pq}`
collectively), pairs of witnesses may share **different** endpoints
(e.g. `P_a:a\to b` and `P_c:c\to a` share only `a`, already handled by
Lemma C in the clean case) or overlap in more complex ways when *not*
clean. The relevant configurations, named but not all resolved:

- **Common prefix/suffix:** two witnesses agree on an initial or final
  sub-path from a shared endpoint before diverging — a direct instance
  of V.1's common-component cell, at one end only.
- **One path entering and leaving another:** a witness `R` touches
  another witness `R'` at two points `u,v\in V(R')` without endpoint
  coincidence, effectively inserting a "detour cell" into `R'` — same
  divergent-cell mechanics as V.1, applied to a sub-segment rather than
  the whole path.
- **Crossing orders:** `V(R)\cap V(R')` occurs in *different* relative
  order along `R` versus `R'` — **V.1's non-crossing hypothesis fails
  here**, and the clean cell decomposition does not directly apply.
  Standard **uncrossing** (swapping the two paths' tails at a crossing
  point to produce two new same-total-length paths with a strictly
  smaller crossing number) is the standard technique from extremal/
  planar graph theory for this situation, but it requires either
  planarity or a degree/connectivity argument justifying that the
  swapped tails remain valid simple paths respecting `G`'s actual
  incidences — **this project does not currently have such an
  argument for this setting, and none is constructed here.**
- **Multiple common components:** more than one common-component cell
  interleaved with divergent cells — mechanically just V.1's identity
  applied with more terms; no new phenomenon, only more bookkeeping.

**Honest stopping point for V.3.** The non-crossing cases (common
prefix/suffix, enter-and-leave) reduce cleanly to V.1's divergent-cell
mechanics and are resolved by the same identity. **The crossing case is
not resolved**: uncrossing is named as the standard applicable
technique, but its hypotheses are not verified to hold in this
project's setting, and no crossing instance is eliminated or classified
here. This is recorded as the precise open continuation, not attempted
speculatively — Part V therefore ends with a **finite set of named
path-intersection diagram types**, fully resolved for three of the four
(common-component, divergent-cell, and their combinations), open for the
fourth (crossing), matching the instruction to end with diagram types
rather than an order-bounded graph census, while not overclaiming the
crossing case as solved.

**Computational cross-check.** `check_intersection_diagram_types`
builds one explicit gadget per named non-crossing diagram type (common
prefix, common suffix, enter-and-leave) and confirms the cell
decomposition and resulting cycle lengths in each; no gadget is built
for the crossing case, consistent with it being left open rather than
falsely validated.
