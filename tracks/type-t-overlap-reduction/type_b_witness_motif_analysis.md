# Witness motif analysis across all completed Type-B candidate databases

**Status.** Exhaustive computer-assisted enumeration and classification.
This file mines the six candidate databases that currently exist for the
order-19/20/21 Type-B bridge frontier (B19-successor layers B20, B20D2,
and the four order-40-frontier order-21 layers gap2\_e29, gap1\_e29,
gap2\_e30, gap1\_e30) for a *common structural forcing mechanism* behind
why every candidate is eliminated. It does **not** promote any all-orders
theorem. Where a claim below is a genuinely proved lemma, it is marked
**Proved** with a self-contained argument. Where a claim is a pattern
observed across the finite data but not derived, it is marked
**Empirical**. Where a natural-looking conjecture was checked and found
false, it is marked **Failed**.

Total candidates mined: 54 + 12 + 104 + 390 + 296 + 1080 = **1,936**.

## 0. Method

For every one of the 1,936 candidates, using only the graph's raw edge
list (path edges + recorded non-path edges) and independent of any
previously-recorded single witness in the existing witness JSON files:

- enumerated **all** simple 16-cycles (`networkx.simple_cycles`,
  `length_bound=16`, filtered to exact length),
- enumerated **all** simple `a`-`y` paths of length 6 and of length 14
  (`networkx.all_simple_paths`, filtered to exact length),
- as a sanity re-check, also enumerated all `C4`, `C8`, and length-2
  `a`-`y` paths (none found in any of the 1,936 candidates — see Section 1),
- for every such witness, extracted the **non-path (chord) edges** it uses,
- computed, per candidate and per witness type, the **inclusion-minimal**
  chord sets (a chord set is minimal if no other witness's chord set of the
  same type is a proper subset of it),
- canonicalized each minimal chord set under path reversal, and — for the
  gap-one families, which carry two structurally identical off-path
  vertices `z1,z2` at this layer — the additional `z1<->z2` exchange,
  taking the lexicographically-least image over the resulting symmetry
  group (2 elements for B20/B20D2/gap2 families, 4 for gap1 families),
- separately classified each chord in a minimal witness by **endpoint
  type**: `a`, `y`, `z`/`z1`/`z2` (generic "off-path"), or `p` (ordinary
  interior path vertex) — this is the classification that is actually
  comparable across candidates, since raw path positions are not.

Code: `verifier/motif_mine.py` (exhaustive enumeration + exact canonical
clustering) and `verifier/motif_classify.py` (endpoint-type
classification). Total runtime for all 1,936 candidates: 74.7s
(enumeration) + ~75s (endpoint classification, re-run of the same
enumeration).

## 1. Headline reconfirmation (stronger than what was previously claimed)

Across all 1,936 candidates, in all six families, with **zero**
exceptions:

- `C4` count = 0, `C8` count = 0, length-2 `a`-`y` path count = 0
  (re-confirms elimination-by-forbidden-subgraph never happens directly);
- every candidate has **at least one** internal `C16` witness, **at
  least one** length-6 `a`-`y` path, **and at least one** length-14
  `a`-`y` path.

This is worth stating precisely because it is stronger than the
disjunctive form of the hand theorem attempted in Section 4: the data
does not merely show "`C16` or length-6 or length-14" holds — it shows
**all three hold simultaneously, every time**, across every one of the
1,936 candidates, in every family, at every edge count and gap type
tried so far. No candidate achieves partial escape (e.g. no candidate
has a `C16` but lacks a length-14 closure path, or vice versa).

## 2. Proved lemmas (general, not candidate-specific)

These do not depend on which candidate is examined; they are arithmetic
facts about any graph containing the fixed distinguished path.

**Lemma 1 (single-chord path creation).** Let `a=p_0,p_1,...,p_L=y` be
the distinguished path (`L` edges). Let `(p_u,p_v)` be any chord with
`0<=u<v<=L`. Then this single chord creates a simple `a`-`y` path of
length exactly `L-(v-u)+1`, obtained by following the path from `a` to
`p_u`, taking the chord to `p_v`, then following the path from `p_v` to
`y`. In particular:

- this path has length 6 iff `v-u = L-5`;
- this path has length 14 iff `v-u = L-13`.

*Proof.* The path `a..p_u` has `u` edges, the chord contributes 1 edge,
the path `p_v..y` has `L-v` edges; total `u+1+(L-v) = L-(v-u)+1`. All
vertices used are distinct (a sub-interval of the path plus one chord
endpoint pair), so it is simple. $\blacksquare$

This lemma was checked against every single-chord minimal witness found
in the data (all such witnesses in Section 3's clustering have
`v-u=L-5` for the length-6 case and `v-u=L-13` for the length-14 case,
with `L=17` for B20/gap1 layers and `L=18` for B20D2/gap2 layers) — no
exceptions, as expected since it is an identity, not a pattern.

**Lemma 2 (single-chord cycle creation).** Under the same setup, a chord
`(p_u,p_v)` with `v-u=15` closes a simple 16-cycle using only the path
segment `p_u..p_v` plus the chord (independent of `a,y,L`, provided
`0<=u`, `v<=L`). This was observed exactly twice in the data (Section
3), both times in the `gap1_e29` family (`L=17`, so `u in {0,1}`); the
corresponding chords for `L=18` (`u in {0,1,2,3}`) never occurred as
edges in any surviving candidate of the four `L=18` families, i.e. the
lemma's hypothesis was simply never satisfied there — this is a fact
about which edges the search produced, not a failure of the lemma.

**Lemma 3 (off-path vertices are chord-only).** Every off-path vertex
(`z` in B20/gap2 layers, `z1,z2` in gap1 layers) has no path edge by
construction, so its *entire* target degree is realized by chords. In
the `E=29` layers this means the off-path vertex (or each of the two,
in gap-one) contributes exactly 3 chords (target degree 3) that are
otherwise entirely unconstrained by path-adjacency; in `E=30`'s `B3`
sub-case an off-path vertex can instead be the vertex bumped to degree
4 or 5, contributing that many chords instead. This is immediate from
the degree bookkeeping already derived in `type_b_order40_frontier.md`
and is restated here because it explains the asymmetry in Section 3.3.

## 3. Empirical structural findings

### 3.1 Chord-count of minimal witnesses (per family, per witness type)

| witness type | family | min chords | max chords |
|---|---|---|---|
| `C16` | B20 | 2 | 8 |
| `C16` | B20D2 | 2 | 6 |
| `C16` | gap2\_e29 | 2 | 8 |
| `C16` | gap2\_e30 | 2 | 8 |
| `C16` | gap1\_e29 | **1** | 9 |
| `C16` | gap1\_e30 | 2 | 9 |
| len-6 | all six families | 1 | 3-5 |
| len-14 | all six families | 1 | 5-8 |

No family has a uniform minimal-witness chord count; minimality is
achieved anywhere from 1 to 9 chords depending on the candidate. There
is **no single motif** (exact chord count, let alone exact chord
identity) that covers every candidate for any witness type. Exact
canonical (position-based) motif clustering, before falling back to
endpoint-type classification, produced 8,289 distinct `C16` motifs, 242
distinct length-6 motifs, and 4,196 distinct length-14 motifs across the
1,936 candidates — i.e. essentially no two candidates share an *exact*
minimal witness once path position is taken into account. This rules
out "a single fixed chord pattern" as the mechanism; any shared
mechanism must be stated in relative/structural terms, which is what
Section 3.2-3.3 do.

### 3.2 Endpoint-type signatures (the comparable classification)

Classifying each chord in a minimal witness by whether its endpoints are
`a`, `y`, off-path (`z`/`z1`/`z2`), or ordinary interior (`p`) collapses
the thousands of exact motifs into a much smaller, genuinely
cross-candidate-comparable set of *signatures* (chord count + sorted
type-multiset). Full tables in the underlying script output; the
dominant signatures per family and witness type are dominated by a
mixture of `p-p` (pure interior shortcuts), `a-p`/`p-y` (chords touching
a path endpoint), and `p-z`/`a-z`/`y-z` (chords touching an off-path
vertex) — no signature covers a majority of candidates in any family for
`C16`, though a handful of `p-p`-heavy signatures dominate the length-6
and length-14 cases in the gap-two and B20D2 families (which have only
one or zero off-path vertices).

### 3.3 The off-path vertex acts as a near-universal `C16`-closing hub

This is the most striking and reproducible pattern found. For each
candidate, checked whether *every* minimal `C16` witness uses at least
one off-path-vertex-touching chord ("all"), whether *at least one* does
("any"), and whether a minimal `C16` witness exists using **only**
interior-to-interior (`p-p`, plus possibly `a`/`y`) chords, with no
off-path vertex at all ("pure path-only witness exists"):

| family | n | all minimal `C16` witnesses touch off-path vertex | at least one does | pure path-only `C16` witness exists |
|---|---|---|---|---|
| B20 | 54 | 12 | **54/54** | 22 |
| B20D2 (no off-path vertex) | 12 | n/a | n/a | 12/12 (trivial) |
| gap2\_e29 | 104 | 0 | **104/104** | 40 |
| gap2\_e30 | 296 | 0 | **296/296** | 188 |
| gap1\_e29 | 390 | 162 | **388/390** | 18 |
| gap1\_e30 | 1080 | 444 | **1080/1080** | 184 |

In every family that has an off-path vertex, **at least one minimal
`C16` witness touches it in essentially every candidate** — 100% in
four of five such families, and 388/390 (99.5%) in the fifth
(`gap1_e29`; the 2 exceptions are candidates whose only minimal `C16`
witnesses are pure interior chords). This is consistent with, and
explained qualitatively by, Lemma 3: the off-path vertex's chords are
the least constrained by path-adjacency (no path edges "using up" two of
its slots), so any completion is structurally biased toward routing
long-range connections through it, and the internal `C16` — which by
construction must traverse a large fraction of the 19-20 vertex graph —
disproportionately relies on that flexibility.

This pattern is markedly **weaker** for the length-6 and length-14
closure paths (Section 3.4's "pure `p-p` witness exists" fractions are
much higher there, reaching 100% for length-14 in `gap2_e30` and
`gap1_e30`), which makes sense: those are single arcs, not full cycles,
so they have more freedom to avoid the off-path vertex by staying on
one long interior run plus a single shortcut chord (Lemma 1).

### 3.4 Off-path-vertex dependence, length-6 and length-14 closures

| witness | family | n | some minimal witness touches off-path vertex | pure path-only witness exists |
|---|---|---|---|---|
| len-6 | B20 | 54 | 32 | 28 |
| len-6 | gap2\_e29 | 104 | 60 | 52 |
| len-6 | gap2\_e30 | 296 | 144 | 224 |
| len-6 | gap1\_e29 | 390 | 336 | 128 |
| len-6 | gap1\_e30 | 1080 | 852 | 596 |
| len-14 | B20 | 54 | 54 | 54 |
| len-14 | gap2\_e29 | 104 | 104 | 102 |
| len-14 | gap2\_e30 | 296 | 290 | **296/296** |
| len-14 | gap1\_e29 | 390 | 388 | 316 |
| len-14 | gap1\_e30 | 1080 | 1080 | **1080/1080** |

Both types of dependence on the off-path vertex (usage vs. avoidance)
coexist in most families — most candidates have minimal witnesses of
*both* kinds (with and without the off-path vertex), which is why "some
touches" and "pure path-only exists" both run high simultaneously in
several rows. This says the off-path vertex is heavily used *when
available as a shortcut*, but is not logically *required* for the
length-6/length-14 closures the way it is (near-universally) for the
internal `C16`.

## 4. Attempted hand theorem

**Target statement (as specified):** "Every completion of the specified
path-degree system avoiding `C4` and `C8` contains `C16` or an `a`-`y`
path of length 6 or 14."

**What is established:** This statement is **true on all 1,936 examined
candidates** (Section 1) — in fact the stronger conjunctive form (all
three witnesses present, every time) holds. Lemma 1 gives a fully
general, proved arithmetic mechanism for *when a single chord alone*
produces a length-6 or length-14 closure. Lemma 3 plus Section 3.3's
near-universal off-path-hub pattern gives a plausible qualitative
mechanism for why the `C16` in particular tends to be forced. But:

**What is not established:** no proof was found, or is claimed, that
this statement holds for *every* graph satisfying the path-degree
system (only for the finite, exhaustively-generated candidate sets on
hand, at the specific orders/edge-counts examined). Two concrete
obstacles to a full proof, identified while attempting one:

1. There is no single motif or fixed small chord count that works
   uniformly (Section 3.1) — a hand proof would need a case analysis at
   least as fine as "how many of the 19-20 path/off-path vertices attach
   directly to the off-path hub," and the data shows this varies
   candidate-to-candidate (from the `E=29` degree bookkeeping in Lemma
   3, the hub always claims exactly 3 slots at `E=29`, but *which* 3
   path positions is not determined by degree counting alone — it's a
   further combinatorial choice that the `C4`/`C8`-avoidance constraint
   narrows down only after the fact).
2. The near-universality of the `C16`-hub dependency (Section 3.3) has
   two exceptions in `gap1_e29` (388/390, not 390/390) — a genuine
   all-orders lemma cannot be built directly on top of a "usually but
   not always" sub-pattern without separately handling the exceptional
   cases, which was not attempted here.

**Conclusion:** the disjunctive hand theorem is an accurate description
of every candidate examined, backed by a proved arithmetic identity
(Lemma 1) covering the single-chord case and a strong (not fully
universal) structural tendency (Section 3.3) for the `C16` case, but it
is **not proved** in general and is not claimed as an all-orders result.

## 5. Failed candidate lemmas (checked and refuted by the data)

- *"Every minimal `C16` witness uses exactly 2 chords."* False — chord
  counts of minimal `C16` witnesses range up to 9 (`gap1_e29`,
  `gap1_e30`).
- *"Minimal length-6/length-14 witnesses never touch the off-path
  vertex."* False — Section 3.4 shows the majority of candidates in most
  families have at least one off-path-vertex-touching minimal witness of
  each type.
- *"Every candidate has a single-chord (chord-count-1) length-6 closure
  path."* False — this holds for only 30-100% of candidates depending on
  family (e.g. 116/390 = 30% in `gap1_e29`, vs. 12/12 = 100% in
  `B20D2`); most families require 2+ chords for a large fraction of
  their candidates.
- *"Every minimal `C16` witness touches the off-path vertex" (as a
  strict universal, not near-universal, claim).* False — refuted by
  exactly 2 candidates in `gap1_e29` (Section 3.3) and by the 18/54,
  40/104, 188/296, 184/1080 "pure path-only witness exists" counts in
  the other four off-path families (those counts are about *existence*
  of a path-only witness *alongside* others, not a refutation by
  themselves, but the strict-universal reading of the claim is still
  false because of the `gap1_e29` exceptions).
- *"A single-chord `C16` witness (span-15 chord, Lemma 2) occurs in every
  family."* False — observed only in `gap1_e29` (`L=17`); never in the
  four `L=18` families, because the corresponding span-15 edges simply
  never appeared in any of those families' surviving candidates.

## 6. What is explicitly claimed and what is not

- **Claimed (exhaustive, re-derived from raw edge lists, not reused from
  prior single-witness records):** all 1,936 candidates across all six
  families have zero `C4`, zero `C8`, zero length-2 `a`-`y` path, and at
  least one each of internal `C16`, length-6 `a`-`y` path, length-14
  `a`-`y` path (Section 1).
- **Claimed (proved, general arithmetic facts, independent of any
  candidate):** Lemmas 1-3 (Section 2).
- **Claimed (empirical, finite-data pattern, not proved in general):**
  the off-path-vertex-hub dependency for `C16` closures (Section 3.3),
  the chord-count and endpoint-type distributions (Sections 3.1-3.2 and
  3.4).
- **Not claimed:** any all-orders theorem; any proof that the hand
  theorem in Section 4 holds beyond the 1,936 examined candidates; any
  claim about `E=31` or higher edge counts (out of scope for this file).

## 7. Files

- `verifier/motif_mine.py` — loads all six candidate databases,
  exhaustively enumerates `C16`/length-6/length-14 witnesses per
  candidate, computes inclusion-minimal chord sets, and canonicalizes
  them under path-reversal (+ `z1<->z2`) symmetry.
- `verifier/motif_classify.py` — reuses `motif_mine.py`'s enumeration and
  additionally classifies each minimal witness's chords by endpoint type
  (`a`/`y`/off-path/interior), producing the tables in Sections 3.2-3.4.
