# The order-40 frontier: gap-two and gap-one, E=29 and E=30

**Status.** Hand-written reduction plus exhaustive computer-assisted
finite certificates. Extends `type_b_order40_frontier.md`, which derived
the normalized geometries and role tables used here. No proof-assistant
formalization exists. This file makes results explicit per layer, kept
separate from any eventual global consequence (per the established
convention in `type_b_delta2_zero_slack.md`).

**Cross-validation status, stated precisely, per layer:**

| layer | direct C generator | independent PySAT | independent networkx | status |
|---|---|---|---|---|
| gap-two, `E=29` | complete | complete, exact match | complete, 0 discrepancies | **fully cross-validated** |
| gap-one, `E=29` | complete | complete, exact match | complete, 0 discrepancies | **fully cross-validated** |
| gap-two, `E=30` | complete | complete, exact match | complete, 0 discrepancies | **fully cross-validated** |
| gap-one, `E=30` | complete | **in progress** (one configuration is a slow SAT instance) | complete, 0 discrepancies | **direct+independent-verifier confirmed; SAT cross-check pending, to be finalized in a follow-up commit** |

No theorem is promoted on the gap-one `E=30` result until its SAT
cross-check completes and either matches or is reconciled. The direct
generator's result for that layer is, on its own, an exhaustive,
self-tested, and independently networkx-verified computation — it is
not asserted with the same confidence tier as the three fully
triple-cross-validated layers until SAT agreement is confirmed.

## 1. Gap-two, `E=29` (row G2-29)

**Model:** 20 vertices, 19-vertex spanning path `p_0..p_18` (18 edges,
`a=p_0`, `y=p_18`), one off-path vertex `z` (index 19). Unique degree
sequence `2^2,3^18` (Section 3 of the frontier doc, `q=0`). 11 non-path
edges. Candidate universe: 172 non-path pairs.

**Direct generator** (`verifier/type_b_order40_gap2_e29.c`, self-tested
via `-selftest` before use): **104** candidates, 8,402,595 DFS nodes,
2.56 seconds.

**Independent PySAT generator** (`verifier/type_b_order40_slot_sat.py`,
exact-cardinality constraints, CEGAR against `cycle_detect.py`'s DFS, no
shared code with the C file): **104** candidates, 24.38 seconds.

**Canonical comparison** (path-reversal symmetry `p_i<->p_18-i`, `z`
fixed): both generators give **52** canonical classes; identical SHA-256
`3850450f0198ce3ef959ef999631524dfc4bfc28934f549d13d0119f42d8cc71`;
`only_in_C=0`, `only_in_SAT=0`.

**Independent networkx verifier**
(`verifier/type_b_order40_independent.py`): all 104 structurally
consistent, all 104 eliminated.

**Result: all 104 candidates contain an internal `C16`, zero contain a
`C4`/`C8` directly or a length-2 `a`-`y` closure path, all 104 have both
a length-6 closure path (`C8`) and a length-14 closure path (`C16`).**

Explicit witness (candidate 0):

```text
degrees: 2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3  (a=vertex0=2, y=vertex18=2, all else 3)
internal C16 subset of R: 0-1-2-3-4-5-6-7-8-9-10-11-12-14-13-19-0
Q_{a,y} length 6:  0-1-2-3-4-17-18   => closure a-x-y gives x-0-1-2-3-4-17-18-x, 6+2=8 edges (C8)
Q_{a,y} length 14: 0-1-2-3-4-5-6-7-8-9-10-15-16-17-18 => closure gives 14+2=16 edges (C16)
```

## 2. Gap-one, `E=29` (row G1-29)

**Model:** 20 vertices, 18-vertex spanning path `p_0..p_17` (17 edges,
`a=p_0`, `y=p_17`), two off-path vertices `z1,z2` (indices 18,19). Unique
degree sequence `2^2,3^18`. 12 non-path edges. Candidate universe: 173
non-path pairs, including the `z1-z2` pair (not excluded a priori).

**Direct generator** (`verifier/type_b_order40_gap1_e29.c`, self-tested):
**390** candidates, 35,483,733 DFS nodes, 9.66 seconds.

**Independent PySAT generator:** **390** candidates, 74.56 seconds.

**Canonical comparison** (path reversal `p_i<->p_17-i` combined with the
`z1<->z2` exchange, since both off-path vertices carry identical
deficits at this layer — 4 total symmetry variants checked, minimum
taken): both generators give **103** canonical classes; identical
SHA-256 `c15d44eea0137b058106f52fe472fede2df4663ca4e4d796daccf037ababf25b`;
`only_in_C=0`, `only_in_SAT=0`.

**Independent networkx verifier:** all 390 structurally consistent, all
390 eliminated.

**Result: all 390 candidates contain an internal `C16`, zero contain a
`C4`/`C8` directly or a length-2 closure path, all 390 have both a
length-6 and length-14 closure path.**

## 3. Gap-two, `E=30` (rows G2-30-A1/A2/B1/B2/B3)

**Model:** same 20-vertex, 19-vertex-path structure as Section 1, but
`q=2`: five sub-cases from the integer partitions of 2 (frontier doc
Section 3), 210 total role configurations (`A1`: 2, `A2`: 18, `B1`: 1,
`B2`: 36, `B3`: 153). 12 non-path edges in every sub-case.

**Direct generator** (`verifier/type_b_order40_gap2_e30.c -generate-all`
internally loops all 210 configurations): **296** total candidates,
1,330,749,623 DFS nodes, 7m02s.

**A striking, uniform structural finding, independently reproduced by
both generators:** sub-cases `A1`, `A2`, `B1` (fully cubic `3^20`), and
`B2` each yield **zero** candidates at all — not merely zero survivors
after cycle-freeness filtering, but zero completions satisfying their
degree deficits while avoiding `C4`/`C8` at all, for every one of their
57 combined role configurations (`2+18+1+36`). **Only sub-case `B3`**
(two distinct ordinary vertices each bumped to degree 4, giving
`2^2,3^16,4^2`) produces any candidates: all 296, across its 153 role
configurations.

**Independent PySAT generator:** **296** total candidates, matching the
same sub-case breakdown (`A1=A2=B1=B2=0`, all 296 from `B3`), 100m28s.

**Canonical comparison:** both generators give **148** canonical
classes; identical SHA-256
`489a89bd65c292bcb7f7d5f118831365f49398689baa3b9cbcbab6102d49eede`;
`only_in_C=0`, `only_in_SAT=0`.

**Independent networkx verifier:** all 296 structurally consistent
(including re-deriving the degree sequence `2^2,3^16,4^2` from the raw
edge list, matching what the generators intended), all 296 eliminated.

**Result: all 296 candidates contain an internal `C16`, zero contain a
`C4`/`C8` directly or a length-2 closure path, all 296 have both a
length-6 and length-14 closure path.**

## 4. Gap-one, `E=30` (rows G1-30-A1/A2/B1/B2/B3)

**Model:** 20-vertex, 18-vertex-path structure (Section 2's geometry)
with `q=2`, same five sub-cases, 210 role configurations, 13 non-path
edges.

**Direct generator** (`verifier/type_b_order40_gap1_e30.c -generate-all`):
**1080** total candidates, 5,425,098,514 DFS nodes, 28m18s (run to full
completion after an initial 15-minute timeout on the first attempt
covered only 127/210 configurations — rerun with a 50-minute budget to
completion, not left partial).

**The identical structural finding as gap-two:** sub-cases `A1`, `A2`,
`B1` (fully cubic), and `B2` again yield **zero** candidates across all
57 combined configurations. **Only `B3`** yields candidates: all 1080,
across its 153 configurations.

**Independent networkx verifier:** all 1080 structurally consistent
(degree sequence `2^2,3^16,4^2` confirmed on every record), all 1080
eliminated: all contain an internal `C16`, zero contain a `C4`/`C8`
directly or a length-2 closure path, all 1080 have both a length-6 and
length-14 closure path.

**Independent PySAT generator:** in progress. As of this commit, 48/210
configurations complete, all agreeing with the direct generator so far
(zero solutions on every `A1`/`A2`/`B1`/partial-`B2` configuration
checked, matching the C generator's zero result on those same
configurations exactly). One `B2` configuration is proving to be a slow
CEGAR instance; the sweep continues in the background and will be
finalized (full canonical comparison against the direct generator's
1080/153 result) in a follow-up commit. **No theorem is promoted on this
layer's Family-II-analogue result until that comparison completes.**

## 5. Manual spot-verification, all four completed layers

Independent of all three generation/verification tools, a direct
one-off script re-checked every recorded `C16` witness, length-6
closure-path witness, and length-14 closure-path witness against the
raw edge lists for all four layers:

```text
gap2_e29: checked 104, failures 0
gap1_e29: checked 390, failures 0
gap2_e30: checked 296, failures 0
gap1_e30: checked 1080, failures 0
```

## 6. What is explicitly claimed and what is not

- **Claimed (fully cross-validated, three independent methods):** the
  `E=29` layer is empty for both gap types (104+390=494 candidates, all
  eliminated). The `E=30` layer is empty for gap-two (296 candidates,
  all eliminated), with the striking uniform finding that only the
  `2^2,3^16,4^2` degree sequence is even combinatorially realizable at
  this edge count under the fixed-path constraint.
- **Claimed (direct generator + independent networkx verifier, SAT
  pending):** the `E=30` layer is empty for gap-one (1080 candidates,
  all eliminated), with the same uniform-B3-only finding.
- **Not yet claimed:** any conclusion about `E=31` or higher (deferred,
  per `type_b_order40_frontier.md` Section 3's staged plan); any
  theorem statement combining these layers into "no order-21 bridge
  exists" (that requires resolving `E=31` too, and finalizing the
  gap-one `E=30` SAT cross-check); the exact value of
  `ex(20;{C4,C8})` (still unverified, per the frontier doc's Section 0).
