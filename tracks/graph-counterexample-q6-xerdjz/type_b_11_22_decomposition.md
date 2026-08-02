# Type B as a (1,1)-piece / (2,2)-piece pair: reconstruction, audit, and closure at n=32

## Status

Three separate claims live in this file, at three different evidence levels.
Read the labels.

1. **The reported decomposition reconstructs.** [`PROVED_IN_MARKDOWN`, modulo
   the `COMPUTATIONALLY_VERIFIED` status of F11/F12] The chat-reported Type-B
   sharpening — "a `(1,1)`-piece of order at least 13 paired with a `(2,2)`-piece
   of order at most 21" — is a correct consequence of machinery already in this
   repo. Section 2 identifies exactly what the two pieces are and Section 3
   derives both numbers by citation. Nothing had to be invented.
2. **It is substantially weaker than what the same machinery gives.**
   [`COMPUTATIONALLY_VERIFIED`, this pass] Pushing the identical argument one
   step further — a census of the `(2,2)`-piece itself rather than only of the
   bare bridge — raises **both** piece orders from `>=13` to `>=18`, hence
   `n >= 34`. Section 5.
3. **Consequence: Type B is eliminated at `n=32`.**
   [`COMPUTATIONALLY_VERIFIED`, inherits (2)] And, unlike the chat report, this
   does **not** need the cubic hypothesis. Section 6.

Claim (1) is an audit result and I am confident in it. Claims (2)–(3) are new
this pass; they rest on a finite exhaustive computation
(`verifier/type_b_22piece_series.py`, `manifests/fb22_order17_manifest.json`)
plus McKay's `ex(n;{C4,C8})` table, exactly the same dependency stack as
F9/F11/F12/FC-15. They are **not** `PROVED_IN_MARKDOWN`. See Section 8 for the
full honest-caveat list, including one order-17 sub-case that is settled by a
deletion argument rather than a direct enumeration.

**Not superseded by the R20 / diamond-exterior report.** See Section 7: that
file is about Type **C**, and its Type-B sentence is externally sourced and
explicitly not verified there. The two results touch the same 7,639-graph
extremal family but are different claims.

---

## 1. What Type B actually is

`two_cut.md` §2c, lines 195–200, verbatim:

> **Type B (t=2, xy∈E(G)).** From the "xy∈E(G)" consequence: deg_G(x)=3 or
> deg_G(y)=3; WLOG deg_G(x)=3. Then a₁+a₂+s=a₁+a₂+1=3, so **a₁+a₂=2**,
> forcing (both ≥1) **a₁=a₂=1** exactly. […] **Type B: t=2, xy∈E(G),
> a₁=a₂=1, deg_G(x)=3, q₁=q₂=3.**

So there are exactly two nontrivial bridges `B_1,B_2`, the edge `xy` is a
*separate* trivial bridge belonging to neither (`two_cut.md` §1 lines 26–27;
`type_b_compatibility.md` line 42: "The edge `xy` is not an edge of either
nontrivial bridge"), and

```
a_1 = a_2 = 1          (deg of x inside each bridge)
b_1, b_2 >= 1          (two_cut.md §1, lines 30-34)
deg_G(y) = b_1+b_2+1   (type_b_compatibility.md lines 38-40 — need NOT be 3)
```

**The cubic hypothesis.** The chat report scopes itself to "a cubic order-32
counterexample". That matters here and only here: `G` cubic forces
`deg_G(y)=3`, hence `b_1=b_2=1`, hence both bridges have terminal-degree
profile `(a_i,b_i)=(1,1)`. This repo does **not** prove a minimal
counterexample is cubic — `lemmas.md` M4 proves only that a *regular* minimal
counterexample is cubic, and G1 only that at least two-thirds of the vertices
are cubic. So "cubic" is an added hypothesis, correctly flagged as such by the
report's own phrasing. (Section 6 shows the final conclusion does not need it.)

## 2. Identifying the two "pieces" — the one real interpretive question

The task brief asked whether `(1,1)` and `(2,2)` refer to the original bridges
or to some finer internal (SPQR-style) decomposition. **Neither piece requires
any sub-decomposition.** Both are the two original bridges; the two labels are
the *same two objects drawn with and without the terminal edge*:

| name | object | `d(x)` | `d(y)` | is `xy` an edge? |
|---|---|---:|---:|---|
| `(1,1)`-piece | the bare bridge `B_i` | `a_i = 1` | `b_i = 1` (cubic) | no |
| `(2,2)`-piece | the **closed** piece `J_i := B_i + xy` | `a_i+1 = 2` | `b_i+1 = 2` (cubic) | yes |

`J_i` is exactly the induced subgraph `G[C_i ∪ {x,y}]`, where `C_i` is the
`i`-th component of `G−{x,y}`. Everything needed about it is already proved:

* `d_{J_i}(x) = a_i+1 = 2` and `d_{J_i}(y) = b_i+1 >= 2` — `two_cut.md` §2c, §1.
* `d_{J_i}(v) = deg_G(v) >= 3` for internal `v` — the argument in `two_cut.md`
  T2's proof, lines 73–77 ("every internal vertex `z∈Cᵢ` has all its `G`-edges
  inside `Bᵢ`, so `deg_{Bᵢ}(z)=deg_G(z)>=3`"). Under cubic `G` this is `= 3`.
* `J_i` is 2-connected — `two_cut.md` **T1**, lines 36–63, verbatim "`Bᵢ+xy`
  (add the edge if absent) is 2-connected".
* `J_i` is simple — `xy ∉ E(B_i)` by the trivial-bridge convention above.
* **`J_i` is `F`-clean** (no `C4`, `C8`, `C16`, `C32`). `J_i ⊆ G` as a
  subgraph, so every cycle of `J_i` is a cycle of `G`. Concretely,
  `two_cut.md` §2 lines 106–111 records internal cycles as inherited, and the
  cycles of `J_i` through `xy` are `xy ∪ P` for `P` an `x`–`y` path in `B_i`,
  which is a genuine cycle of `G` because `xy ∈ E(G)` (Type B).

So `(1,1)`-piece and `(2,2)`-piece are **not** two structurally different
objects. They are `B_i` and `B_i+xy`. The naming is useful anyway, and for a
non-obvious reason — see Section 4.

**Order bookkeeping.** `|V(J_i)| = |V(B_i)| = n_i` (adding an edge adds no
vertex), and `two_cut.md` §26 line 1120 gives, for Type B,

```
n(G) = n_1 + n_2 - 2 .
```

## 3. Reconstructing "order >= 13" and "order <= 21" [PROVED, by citation]

**Order >= 13.** This is exactly the F-series bound, applied to a Type-B
bridge, in precisely the way `separator_theorem_order32_gap_analysis.md`'s
O32-2 applies it to a Type-A bridge. `B_i` satisfies F11/F12's hypotheses
verbatim: `d_{B_i}(x)=a_i=1`, `d_{B_i}(y)=b_i>=1`, `xy ∉ E(B_i)`,
`d_{B_i}(v)>=3` internally, `B_i+xy` simple and 2-connected. So:

* F9/F11 (`two_cut.md` §20): `|V(B_i)| <= 11` ⇒ `B_i` has a `C4` or `C8`.
* F12 (`f12_order12_result.md`, Theorem F12): `|V(B_i)| = 12` ⇒ same.

`B_i ⊆ G` and `4,8 ∈ F`, so `B_i` has neither. Hence **`n_i >= 13`.** This is
verbatim O32-3's argument (`separator_theorem_order32_gap_analysis.md` lines
205–212, "Identical to O32-2. Type B has `a₁=a₂=1` (§2c) and the edge `xy`
belongs to neither nontrivial bridge […] so `xy∉E(Bᵢ)` and F11's hypotheses
hold verbatim"), with F11's `12` upgraded to F12's `13`.

**Order <= 21.** Pure arithmetic from `n = n_1+n_2-2 = 32`, i.e. `n_1+n_2 = 34`:

```
n_2 = 34 - n_1 <= 34 - 13 = 21 .
```

**Verdict on the reported claim: correct, and fully reconstructible.** Both
numbers follow from F12 + `two_cut.md` §2c + §26. Two honest footnotes:

* The bound is **symmetric**, and the report's asymmetric phrasing slightly
  undersells it. `a_1=a_2=1`, so F12 applies to *both* bridges; the true
  statement is `13 <= n_1, n_2 <= 21` for both. Labelling one piece "`(1,1)`"
  and the other "`(2,2)`" is a presentational choice about which bridge gets
  drawn with the terminal edge, not a structural asymmetry.
* `n >= 13+13-2 = 24` is the corresponding overall bound — already an
  improvement on the `n >= 22` recorded as O32-3, and exactly the number
  `fcn_order15_result.md` reached for Type C by the same route.

**FC-15 does not apply here, and this is worth stating explicitly.** FC-15
(`fcn_order15_result.md`) requires `d_B(x)=2` *and* `xy ∉ E(B)`. A Type-B
bridge always has `a_i=1`, never 2, so FC-15 never applies to `B_i`; and the
closed piece `J_i` does have `d(x)=2` but *contains* `xy`, so it fails FC-15's
other hypothesis. FC-15 is genuinely orthogonal to Type B. Anyone tempted to
cite it for a Type-B order bound should not.

## 4. Why the `(2,2)` framing is not cosmetic [the load-bearing observation]

Restating the bridge as its closure buys exactly one edge, and that one edge
is worth a lot, because it moves the piece from a slack-1 counting regime into
a slack-0 one.

For the bare bridge `B` of order `n` with `d(x)=d(y)=1`:

```
2|E(B)| >= 1 + 1 + 3(n-2) = 3n-4,   so  m_min(B) = ceil((3n-4)/2)
```

For the closed piece `J = B+xy` of the same order `n`:

```
2|E(J)| >= 2 + 2 + 3(n-2) = 3n-2,   so  m_min(J) = m_min(B) + 1
```

and `J` is still `{C4,C8}`-free, so `m_min(J) <= ex(n;{C4,C8})` too. That
extra `+1` closes the gap to the extremal bound at every order in range:

| `n` | `ex(n;{C4,C8})` | `m_min(B)` | headroom for `B` | `m_min(J)` | headroom for `J` |
|--:|--:|--:|--:|--:|--:|
| 13 | 19 | 18 | 1 | **19** | **0** |
| 14 | 20 | 19 | 1 | **20** | **0** |
| 15 | 22 | 21 | 1 | **22** | **0** |
| 16 | 23 | 22 | 1 | **23** | **0** |
| 17 | 25 | 24 | 1 | **25** | **0** |
| 18 | 27 | 25 | 2 | 26 | 1 |
| 19 | 29 | 27 | 2 | 28 | 1 |
| 20 | 31 | 28 | 3 | 29 | 2 |
| 21 | 33 | 30 | 3 | 31 | 2 |

(`ex` values from `literature.md` L15/L15b, McKay's extremal data.)

Headroom 0 means `|E(J)|` is **pinned to `ex(n)` exactly**, which in turn pins
the whole degree sequence — precisely the regime in which FC-15's method
works ("`m_min == ex(n)` exactly, pinning any instance to an extremal
`{C4,C8}`-free graph", `fcn_order15_result.md` line 24). A census of the
`(1,1)`-piece at these orders has headroom 1 and is a strictly harder search
than a census of the `(2,2)`-piece at the same order. That is the entire
practical content of the `(2,2)` reformulation, and it is why the reported
sharpening is a genuinely good idea rather than a relabelling.

## 5. Doing the census: FB22-17 [COMPUTATIONALLY_VERIFIED, this pass]

> **Theorem (FB22-17).** Every simple graph `J` with `|V(J)| <= 17` carrying
> two adjacent distinguished vertices `x,y` such that `d_J(x)=2`,
> `d_J(y)>=2`, `d_J(v)>=3` for every `v ∉ {x,y}`, and `J` 2-connected,
> contains a `C4` or a `C8`.

Script `verifier/type_b_22piece_series.py`; manifest
`manifests/fb22_order17_manifest.json`; per-order report
`data/fb22_series_report.json`.

Method, mirroring `type_c_fcn_series.py` exactly. For each `n`, compute
`m_min = ceil((3n-2)/2)` and compare with `ex(n;{C4,C8})`. If
`m_min > ex(n)`, the order is impossible by counting with no search at all.
Otherwise `m_min == ex(n)`, `m` is pinned, and the degree sequence is pinned
to within one unit of slack, giving an exact `nauty-geng` degree cap.
Detection is the certified C batch detector `verifier/check_power_masks.c`
(bit 0 = `C4`, bit 1 = `C8`, bit 2 = `C16`), cross-checked against an
independently written Python DFS on every `{C4,C8}`-free survivor *plus* a
500-graph random sample of the rejects at every order.

| `n` | verdict | `m` | `ex(n)` | slack | cap | raw | `{C4,C8}`-free | shape-admissible | detector mismatches | survivors |
|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 3,4,5,6,7,9,11 | infeasible by counting | — | — | — | — | — | — | — | — | 0 |
| 8 | searched | 11 | 11 | 0 | `-D3` | 1 | 0 | 0 | 0 | 0 |
| 10 | searched | 14 | 14 | 0 | `-D3` | 11 | 0 | 0 | 0 | 0 |
| 12 | searched | 17 | 17 | 0 | `-D3` | 75 | 0 | 0 | 0 | 0 |
| 13 | searched | 19 | 19 | 1 | `-D4` | 33,677 | 3 | **0** | 0 | 0 |
| 14 | searched | 20 | 20 | 0 | `-D3` | 677 | 0 | 0 | 0 | 0 |
| 15 | searched | 22 | 22 | 1 | `-D4` | 2,625,442 | 14 | **0** | 0 | 0 |
| 16 | searched | 23 | 23 | 0 | `-D3` | 7,639 | **0** | 0 | 0 | 0 |
| 17 (sub-case A) | searched | 25 | 25 | 1 | `-D3` | 6,314 | **0** | 0 | 0 | 0 |
| 17 (sub-case B) | by deletion, §5.2 | 25 | 25 | 1 | — | — | — | — | — | 0 |

**Zero survivors at every order, zero detector disagreements.**

### 5.1 Cross-validation

* Raw counts at `n = 8,10,12,13,14,15` are `1, 11, 75, 33677, 677, 2625442`
  — reproducing `fcn_order15_result.md`'s independently-obtained table
  (lines 55–60) **exactly**. The two scripts were written separately; the
  agreement is a real check on the generation box.
* The raw count at `n=16` is **7,639**, reproducing
  `diamond_exterior_r20_closure.md`'s count for the identical `geng` command
  (line 38) exactly.
* `geng -f` was verified to mean "`C4`-free" by control: at `n=10, m=14`,
  102 of 113 graphs contain a `C4` without `-f`, and 0 of 11 do with `-f`.
* At `n=13` and `n=15` the `{C4,C8}`-free graphs that survive (3 and 14) are
  rejected by a filter that never looks at `xy`-adjacency at all: **no**
  assignment of `(x,y)` with `d(x)=2, d(y)>=2` leaves every other vertex at
  degree `>=3` (their degree sequences carry four or five degree-2 vertices).
  This matters because it shows FC-15's zero-survivor verdict at those orders
  was **not** an artefact of its `xy ∉ E` filter — the `xy`-present variant
  needed here is empty for the same reason. (In `type_c_fcn_series.py`'s
  `rooted_pair_survivors`, the degree-shape test at line 90 precedes the
  `xy`-adjacency test at line 92; this pass confirms the shape test alone
  already empties the set.)

### 5.2 Order 17, sub-case B, settled by terminal deletion

At `n=17`, `m=25=ex(17)` and the slack is 1, so `d(y) ∈ {2,3}`
(`2 + d(y) + Σ_internal = 50` with `Σ_internal >= 45` forces `d(y) <= 3`).

* **Sub-case A, `d(y)=3`:** all internal degrees are exactly 3, so the degree
  sequence is `2,3^16` and `-D3` suffices. Searched directly above: 6,314 raw
  graphs, **0** `{C4,C8}`-free.
* **Sub-case B, `d(y)=2`:** the degree sequence is `2,2,4,3^14`, needing
  `-D4`. The `-D4` box at `n=17` is far too large to enumerate cheaply, so it
  is settled instead by deleting the terminals. Let `x'` be `x`'s neighbour
  other than `y`, and `y'` be `y`'s neighbour other than `x`. Then `x' ≠ y'`
  (otherwise `x'` is a cut vertex of `J` separating `{x,y}` from the other 14
  vertices, contradicting T1), and `x'` is not adjacent to `y` (whose only
  neighbours are `x,y'`), so `H := J − {x,y}` loses exactly the three edges
  `xy, xx', yy'`. Hence `H` has 15 vertices and 22 edges; it is connected
  (it is `G[C_i]`, a component of `G−{x,y}`) and `{C4,C8}`-free (`H ⊆ G`);
  and its degree sequence is `2,3^14` (if the degree-4 vertex is `x'` or `y'`)
  or `2,2,4,3^12` (otherwise) — in both cases min degree 2, max degree 4.
  The `n=15` layer of the same census enumerates **every** such graph
  (`geng -c -f -d2 -D4 15 22:22`, 2,625,442 raw, complete), and its 14
  `{C4,C8}`-free members have degree sequences
  `[2,2,2,2,3^8,4,4,4]` (×10) and `[2,2,2,2,2,3^6,4,4,4,4]` (×4).
  **Neither target sequence occurs**, so sub-case B is impossible. ∎
  (Verified programmatically by `check_order_17_subcase_B` in the script.
  Note this sub-case does not depend on `ex(15)` at all — the `n=15`
  enumeration at the exact `(n,m,degree-range)` is complete on its own terms.)

## 6. Consequence: Type B is eliminated at n = 32

Apply FB22-17 to **both** closed pieces. Both qualify: `a_1=a_2=1` gives
`d_{J_i}(x)=2` for `i=1,2`, `b_i>=1` gives `d_{J_i}(y)>=2`, internal degrees
are `>=3`, `xy ∈ E(J_i)`, and each `J_i` is 2-connected (T1) and
`{C4,C8}`-free (`J_i ⊆ G`). Therefore

```
n_1 >= 18   and   n_2 >= 18 ,
n(G) = n_1 + n_2 - 2 >= 18 + 18 - 2 = 34  >  32 .
```

**So no Type-B 2-cut exists in a minimal counterexample of order 32.**

Three things to note about the shape of this conclusion.

* **The cubic hypothesis is not needed.** FB22-17 only assumes `d(y) >= 2`,
  and Type B gives that unconditionally from `b_i >= 1`. Cubicity was needed
  to make the piece literally a "`(2,2)`-piece"; it is not needed for the
  bound. (Under cubic there is an extra, independent kill: all internal
  degrees are exactly 3, so `2|E(J_i)| = 3n_i - 2` must be even, forcing
  `n_i` **even** — which by itself rules out every odd order and would make
  the orders 13, 15, 17 layers unnecessary.)
* **It supersedes O32-3.** `separator_theorem_order32_gap_analysis.md` line
  207 records the best available Type-B order bound as `n >= 22`, and line 214
  as "Type B is not eliminated at order 32 by any order bound currently
  available". With F12 that becomes `n >= 24`; with FB22-17 it becomes
  `n >= 34`, and the case closes. `f12_order12_result.md` line 91's status
  line ("Type B: order bound only reaches `n>=22` (`O32-3`) […] still open,
  needs new machinery") should be updated.
* **It does not touch Type C.** Type C has `xy ∉ E(G)`, so there is no
  terminal edge to close a bridge with, and the `(2,2)` trick is unavailable
  in that form. Type C remains open here (see Section 7).

The reported "`(1,1)`-piece of order at least 13 paired with a `(2,2)`-piece
of order at most 21" is therefore **true but vacuously so at `n=32`**: the
interval `[13,21]` is correct as far as F12 goes, but no piece of order
`<= 17` exists at all, and two pieces of order `>= 18` cannot fit in 32
vertices.

## 7. Relation to the R20 / diamond-exterior report

`diamond_exterior_r20_closure.md` verifies that
`nauty-geng -c -f -d2 -D3 16 23:23` (7,639 graphs) has zero `C4`/`C8`/`C16`-free
members, in service of an externally-reported **Type-C** claim. That is
*literally the same generation command* as this file's `n=16` layer, and the
raw count agrees exactly — a useful independent cross-check in both
directions. The results are nevertheless different claims:

* That file needs `C4`/`C8`/**`C16`**-freeness; this one gets 0 survivors from
  `C4`/`C8`-freeness alone (a strictly weaker filter), so the `n=16` layer here
  does not depend on the `C16` detector at all.
* That file's conclusion is scoped to fully-cubic **Type C** and, by its own
  §"Scope caveat", rests on an un-reconstructed reduction living in a source
  session's files that are not in this repo.
* Its Type-B content is a single reported sentence, explicitly **not**
  verified there.

So this file is **not** duplicated effort: it independently establishes the
Type-B half from this repo's own `two_cut.md`/`type_b_*.md` machinery, with no
reliance on any external session's reduction.

## 8. Honest caveats

* **Label.** FB22-17 is `COMPUTATIONALLY_VERIFIED`, exactly like F9/F11/F12
  and FC-15 — not `PROVED_IN_MARKDOWN`. The Type-B elimination at `n=32`
  inherits that status. Nothing here is proof-assistant formalised.
* **Dependence on `ex(n;{C4,C8})`.** The upper bound `m <= ex(n)` comes from
  McKay's extremal data via `literature.md` L15/L15b and is load-bearing: if
  any `ex(n)` for `n <= 17` were larger than tabulated, there would be
  unsearched edge counts. This is the same dependency the entire F-series
  already carries; it is not a new exposure, but it is not zero either.
  (`literature.md` line 70 notes the order-16, 17 and 20–23 `.s6` inputs are
  absent locally, so those `ex` values are used from the table, not
  re-derived here.)
* **Order-17 sub-case B is an argument, not an enumeration.** §5.2 replaces a
  `-D4` enumeration at `n=17` with a deletion argument plus the `n=15` layer.
  The argument is short and I believe it is right, but it is the one place in
  the chain where a reader must check reasoning rather than a count. A direct
  `geng -c -f -d2 -D4 17 25:25` census would remove the caveat; it was not run
  (the box is very large, on the order of `10^8` by extrapolation from
  `n=15`'s 2.6M).
* **`Λ`-side constraints were not used.** `two_cut.md` §2 lines 113–118 give
  `Λ_i ∩ {2^k−1} = ∅` for Type B, and `type_b_compatibility.md` lines 116–118
  give the full triple `(Λ_1+{1}), (Λ_2+{1}), (Λ_1+Λ_2)` cleanliness. None of
  that was needed; the order bound alone sufficed. If anyone wants to push
  FB22 past 17 (see below), those constraints are available and unused.
* **What was *not* reconstructed.** The chat message's Type-C half ("a mixed
  `(1,2)`-piece of odd order at most 17") is outside this file's scope and is
  neither confirmed nor contradicted here.
* **Standing assumptions.** `G` 2-connected (discharged at even order by
  `separator_theorem_order32_gap_analysis.md` O32-1) and lexicographically
  minimal, as throughout `two_cut.md`.

## 9. If you want to go further: the exact next computation

FB22-17 is what is needed for `n=32`, and it is done. For the record, the
next layers, with the same feasibility analysis this session did for FC-15:

| `n` | `m` range (`m_min : ex`) | slack at `m_min` | degree sequences to cover | cap | expected difficulty |
|--:|---|--:|---|---|---|
| 18 | 26 : 27 | 0 at 26, 2 at 27 | `2,2,3^16` (m=26); `2,2,4,4,3^14` / `2,2,5,3^15` / `2,3,4,3^15` / `2,4,3^16` (m=27) | `-D5` | the first order where `m` is **not** pinned; both layers needed |
| 19 | 28 : 29 | 1 at 28, 3 at 29 | many | `-D6` | materially harder |
| 20 | 29 : 31 | 0 at 29 | `2,2,3^18` at m=29; two further layers | `-D7` | hard |

Reaching `n=18` would give `n >= 2·19−2 = 36` for Type B, which is *not*
needed for the order-32 target but would matter for an order-34 or order-36
attack. Note the `n=18, m=27` layer is where the search stops being pinned and
the `Λ`-side constraints from §8 become worth switching on.

Two cheaper follow-ups that would strengthen what is here rather than extend it:

1. Run `geng -c -f -d2 -D4 17 25:25` directly to convert §5.2's deletion
   argument into a plain census. Pure hygiene; expected to be a long but
   finite run.
2. Re-derive `ex(16)`, `ex(17)` locally (the `.s6` inputs are absent per
   `literature.md` line 70) to remove the last unre-derived numeric input in
   the chain.

---

## Reproduction

```
python verifier/type_b_22piece_series.py          # full series through n=17
python verifier/type_b_22piece_series.py 14       # cheap subset, seconds
```

Artifacts: `manifests/fb22_order17_manifest.json` (SHA-256 of the script, the
detector source, and every raw `geng` stream, plus per-layer counts) and
`data/fb22_series_report.json` (per-order machine-readable result including
the degree sequences of every `{C4,C8}`-free graph found).
