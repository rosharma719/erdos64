# P14-avoidance models: does length-14 forcing survive under slack?

**Status.** Computer-assisted exhaustive/CEGAR search, hand-derived
reduction lemma. Follows on from `type_b_witness_motif_analysis.md`,
which found that the "small common motif" route does not explain the
elimination mechanism (thousands of exact minimal witnesses, no
uniform chord count). This file takes the strategic pivot suggested
after that result: instead of cataloguing witnesses inside the known
`C4`/`C8`-avoiding completion set, it builds **avoidance models** that
directly ask whether a completion can exist which avoids `C4`, `C8`,
**and** a length-14 `a`-`y` path simultaneously — and tests whether
that avoidance stays impossible as slack (off-path vertices, path
length, degree) is deliberately increased. No proof-assistant
formalization exists. **No all-orders theorem is claimed anywhere in
this file.**

## 0. Why length-14 first

Per Lemma 1 of `type_b_witness_motif_analysis.md`, a single chord
`(p_u,p_v)` creates a length-14 `a`-`y` path iff `v-u = L-13` (`L` = the
path's edge count). This makes length-14 avoidance the most local,
tractable target of the three witness types: length-6 avoidance
involves more/larger chord combinations in the data, and the
single-chord `C16` mechanism (Lemma 2) appeared in only one of six
families. Per the explicit instruction motivating this file, `C16` and
length-6 avoidance are deliberately deferred until the length-14
picture is understood.

## 1. The avoidance model

**Model `M14`:** given a fixed distinguished path, a per-vertex degree
deficit (additional degree beyond the path edges), and a total
non-path-edge count, does a simple-graph completion exist that (a)
matches every degree deficit exactly, (b) contains no `C4`, no `C8`,
and (c) contains no simple `a`-`y` path of length 14?

**Method** (`verifier/type_b_p14_avoidance_sat.py`): CEGAR over a PySAT
cardinality encoding (`CardEnc.equals` per vertex for exact degree,
plus one global cardinality constraint for the total edge count —
identical encoding style to `verifier/type_b_order40_slot_sat.py`).
Each time the solver proposes a completion, it is checked, via a
**freshly written, from-scratch backtracking detector**
(`find_ay_path_len_dfs`, independent of `motif_mine.py`'s networkx-based
enumeration and of the C generators' recursive search), for `C4`, `C8`,
and a length-14 `a`-`y` path. If any is found, the witness's edges are
blocked and the solver retries. If the solver ever proposes a
completion with none of the three, that is a **survivor** — a
counterexample to "`M14` is unsatisfiable" for that geometry. If the
solver instead returns UNSAT (every completion has been visited and
blocked), that is an independent, from-scratch confirmation that no
completion avoids all three simultaneously.

This is deliberately not a re-use of the prior exhaustive enumeration:
the earlier work (C generators + `motif_mine.py`) generated the full
`C4`/`C8`-avoiding completion set and then checked, post-hoc, whether
each one happened to contain a length-14 path. Here the solver is asked
directly "produce a completion that avoids all three," with no access
to the previously-recorded fact that all known completions contain
one.

## 2. Baseline confirmation (E=29, both gap types)

| geometry | vertices | edges | forbidden | result | completions blocked | time |
|---|---|---|---|---|---|---|
| gap2\_e29 (1 off-path vertex, `L=18`) | 20 | 11 | length-14 | **UNSAT** | 18,682 | 25.6s |
| gap1\_e29 (2 off-path vertices, `L=17`) | 20 | 12 | length-14 | **UNSAT** | 31,338 | 80.5s |

Both baseline `E=29` layers are independently reconfirmed
unsatisfiable: no completion of the exact degree system, avoiding
`C4`/`C8`, escapes having a length-14 `a`-`y` path. This matches
(rather than merely repeats) the prior full-census finding, now via a
structurally different search method.

`E=30`'s `M14` confirmation was **not** re-run via this CEGAR method for
either gap type — a 153-role-configuration sweep at this search cost
(comparable per-configuration cost to the baseline runs above, so
plausibly hours of wall time) was judged not to be worth the marginal
evidence, since `E=30` is already covered by a complete, exhaustive
census from three independently-cross-validated methods (the direct C
generator, an independent PySAT generator, and an independent networkx
verifier — all agreeing that all 296 gap-two and 1080 gap-one `E=30`
candidates contain a length-14 closure path; see
`type_b_order40_generators.md` and `type_b_witness_motif_analysis.md`
Section 1). This is flagged honestly as a **deferred** confirmation,
not a completed one — the `E=30` claim currently rests on the earlier
complete-census evidence, not on a fresh CEGAR run.

## 3. Relaxation experiments: does slack break the forcing?

Three relaxations of the gap-two `E=29` baseline were tested, each
adding exactly one unit of structural slack relative to the baseline
(order 20, `L=18`, 1 off-path vertex at degree 3):

| relaxation | vertices | path length `L` | off-path vertices (degrees) | edges | result | completions blocked | time |
|---|---|---|---|---|---|---|---|
| baseline | 20 | 18 | 1 (degree 3) | 11 | UNSAT | 18,682 | 25.6s |
| **1. extra off-path vertex** | 21 | 18 (unchanged) | 2 (degrees 3, 4 — forced by parity) | 13 | **UNSAT** | 37,362 | 107.9s |
| **2. extra path vertex** | 21 | 19 | 1 (degree 4 — forced by parity) | 12 | **UNSAT** | 23,678 | 42.2s |
| **3. extra off-path vertex, order 22** | 22 | 19 | 2 (degrees 3, 3 — parity now permits both at 3) | 13 | **UNSAT** | 58,750 | 325.6s |

**All three relaxations are UNSAT.** Adding one more off-path vertex,
one more path vertex, or both together (at a fully symmetric order-22
geometry where both off-path vertices sit at degree 3) never creates a
completion escaping the length-14 path. This directly answers the
question the pivot flagged as mattering most: length-14 avoidance did
**not** become satisfiable under any of the three slack increases
tried. The number of completions the solver had to visit and block
before exhausting the space grows with each relaxation (18,682 ->
37,362 / 23,678 -> 58,750), consistent with a genuinely larger search
space each time — this is not a case of the relaxed models being
trivially small or degenerate.

**Important scope caveat:** four data points (baseline plus three
relaxations, all starting from the same gap-two `E=29` base, all still
within order 20-22, all still respecting the `S1`/`S2` tuple's
degree/edge bookkeeping) is *not* evidence of an all-orders pattern —
it is evidence that the forcing is not a knife-edge artifact of the
single most-constrained layer. Whether it persists at, say, order 30 or
40 is not addressed by anything in this file, and no such claim is
made.

## 4. A proved structural reduction (Lemma 4)

**Lemma 4 (forced hub-matching decomposition, `E=29` layers).** In every
`E=29` geometry examined (gap-two: 1 off-path vertex of degree 3;
gap-one: 2 off-path vertices of degree 3 each), every vertex on the
distinguished path — including `a` and `y` — has degree deficit exactly
1 (needs exactly one non-path edge), while every off-path vertex has
deficit equal to its full target degree (3, since it has no path edges
at all). Consequently, **every** valid completion decomposes uniquely
into:

- a set of edges from each off-path vertex to distinct path vertices,
  exactly saturating that off-path vertex's degree (3 choices of path
  vertex per off-path vertex in gap-two; a joint choice of 6 path
  vertices, possibly overlapping, across the two off-path vertices in
  gap-one — or a direct `z1`-`z2` edge using up one slot from each);
- a **perfect matching** on the path vertices *not* chosen as an
  off-path neighbor (each such vertex still has deficit exactly 1, and
  no off-path vertex remains available to it), using chords entirely
  among path vertices.

*Proof.* Immediate from the target degree sequences already derived in
`type_b_order40_frontier.md` (Section 2): path vertices always carry
deficit exactly 1 at `E=29`, off-path vertices carry deficit equal to
their full degree target (no path edges to offset it). A vertex with
deficit 1 receives exactly one non-path edge; summing over all
deficit-1 path vertices not adjacent to an off-path vertex forces a
perfect matching (every one of them has exactly one remaining chord,
and none of them can still reach an already-saturated off-path vertex,
so their sole chord goes to another such vertex). $\blacksquare$

This is a genuine simplification: for gap-two `E=29`, every one of the
104 candidates is exactly "3 path vertices chosen to attach to `z`,
paired with a perfect matching on the other 16," and finding whether
some choice avoids `C4`,`C8`, and a length-14 path is a much smaller
combinatorial question than the raw 11-edge slot search. **What this
lemma does not do** is complete a hand proof that every such
hub+matching choice is forced into a length-14 path — that step (a
case analysis over which 3 vertices attach to the hub and over the
matching's edge-span multiset) was attempted but not completed; see
Section 5.

## 5. Attempted hand proof (incomplete — explicitly not claimed)

Using Lemma 4's reduction plus Lemma 1's chord-span identity, the
natural next step is: show that for *any* choice of 3 hub-attachment
vertices and *any* `C4`/`C8`-avoiding perfect matching on the remaining
16, either a single matching edge already has span `L-13` (giving a
length-14 path directly by Lemma 1), or some short combination of 2-3
matching edges plus possibly a hub edge produces one. This was
attempted directly but **not completed**: the case analysis branches on
which 3 (of 19) vertices are chosen as hub-adjacent and on the spans of
the resulting 8-edge matching, and no argument was found (in the time
budgeted for this file) that rules out every combination without
itself amounting to the same case enumeration the CEGAR search already
performs. This is stated plainly as an open, unproved step, not
papered over.

## 6. Correction: justifying (and scoping) the path-reversal symmetry

The prior motif analysis canonicalized minimal witnesses under path
reversal (`p_i <-> p_{L-i}`, which swaps the labels `a<->y`) to avoid
over-counting motif classes. This needs an explicit justification,
which was missing before:

**What reversal justifiably does.** Within a *single fixed layer* (one
specific assignment of degree deficits to `a`, `y`, and the other
vertices — e.g. gap-two `E=29`, where `a` and `y` both carry deficit
exactly 1), reversal is a genuine **automorphism of the combinatorial
completion-counting problem**: the degree-deficit dict, the `C4`/`C8`
forbidden-subgraph constraints, and the total edge count are all
invariant under simultaneously relabeling `p_i -> p_{L-i}` (which sends
`a` to `y`'s position and vice versa). Since `a` and `y` always carry
*identical* deficits in every layer examined here (both terminals stay
at deficit 1 in `E=29`; in `E=30`'s `A1` sub-case, "bump `a`" and "bump
`y`" are generated as two separate, genuinely mirror-image role
configurations, not folded together prematurely), reversal correctly
identifies completions that are the same object up to a relabeling that
preserves every constraint used in the search — so it cannot
under-count real solutions or conflate two combinatorially distinct
ones for the *purpose of counting canonical classes within one layer*.

**What reversal does NOT justify.** `type_b_order40_frontier.md`
explicitly calls `a` "the gateway — `x`'s unique neighbour, losing edge
`xa`" in the full (undeleted) bridge `B`, while `y`'s forced-degree-2
justification comes from a different mechanism (`S1`'s constant `2`,
or `B2`'s two-branch theta-suffix structure). That is, `a` and `y` are
**not** asserted to be symmetric roles in the underlying Type-B
tuple/bridge semantics — they may correspond to different tuple
parameters (e.g. `ℓ` vs `m`, or `δ` vs `ε`) in the parent realizability
problem. Reversal is therefore a valid **counting symmetry of the
fixed-degree combinatorial search performed at each layer**, not a
claimed symmetry of the full Type-B bridge realizability semantics; a
"reversed" witness should not be read as asserting anything about a
swapped tuple. This distinction affects only the *reported number of
motif classes* in the prior file, not the existence claims (Section 1
there) or anything in this file, since every avoidance-model result
above is a direct SAT/UNSAT answer on the original (non-canonicalized)
completion set.

## 7. What is explicitly claimed and what is not

- **Claimed (independent, from-scratch CEGAR confirmation):** the
  gap-two and gap-one `E=29` layers are both `M14`-unsatisfiable — no
  completion avoids `C4`, `C8`, and a length-14 `a`-`y` path
  simultaneously (Section 2).
- **Claimed (new relaxation results):** this unsatisfiability survives
  three successive slack increases on the gap-two `E=29` baseline
  (Section 3): one extra off-path vertex (order 21), one extra path
  vertex (order 21), and both together at a fully symmetric order-22
  geometry. All three relaxations are `M14`-unsatisfiable.
- **Claimed (proved, general):** the hub+matching decomposition, Lemma
  4 (Section 4).
- **Not claimed:** a hand proof that `M14` is unsatisfiable in general
  (Section 5, explicitly incomplete); any all-orders theorem; any
  conclusion about orders beyond the ones directly tested (20-22); a
  fresh CEGAR-based `M14` confirmation for `E=30` (deferred, Section
  2); anything about `C16` or length-6 avoidance (`M16`/`M6`,
  deliberately not started per the stated priority order).

## 8. Files

- `verifier/type_b_p14_avoidance_sat.py` — the avoidance-model CEGAR
  search (`search_avoid`), its independent `a`-`y` path detector
  (`find_ay_path_len_dfs`), and the baseline + relaxation geometry
  definitions used above.
