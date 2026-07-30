# F12: proved — Type A is entirely eliminated at order 32

## Status

[COMPUTATIONALLY VERIFIED, exhaustive, dual-detector cross-validated].
Identified as the single highest-value cheap follow-up in
`separator_theorem_order32_gap_analysis.md` (MISSING-1); run and closed
this session.

**Theorem (F12).** Every simple two-terminal graph `B` with `|V(B)|=12`,
`d_B(x)=1`, `d_B(y)>=1`, `xy not in E(B)`, `d_B(v)>=3` for every
`v notin {x,y}`, and `B+xy` simple and 2-connected, contains a `C4` or a
`C8`.

## Method

`verifier/type_a_order12_f12.py`, adapted directly from the certified
order-9/10/11 F-series pipeline (`type_a_order9_search.py`,
`type_a_order10_direct.py`): `nauty-geng -c -f -d1 -D{3 or 5} 12 {16 or
17}:{16 or 17}` (connected, `C4`-free at generation time via `-f`, min
degree >=1), independent dual detection of `C4`/`C8` (Python DFS-based
`cycle_detect` vs. a from-scratch C implementation, asserted to agree on
every one of the 16,412 raw graphs — 0 disagreements), rooted-pair
enumeration over every actual degree-1 vertex as candidate `x` and every
other vertex as candidate `y`, filtered for internal-degree->=3,
`xy`-absence, and 2-connectivity of the closure `B+xy`, then canonical
deduplication via `nauty-labelg` with a fixed root-coloured partition.
Full manifest with SHA-256 checksums for every input/output stream at
`manifests/F12_order12_manifest.json` (`status: COMPLETE`, every generator/
detector/labelg exit code `0`).

**Search box** (re-derived independently, matches the gap analysis exactly):
`2|E(B)| >= d(x)+d(y)+3(n-2) >= 1+1+30 = 32`, so `|E(B)|>=16`; the
`{C4,C8}`-free extremal bound `ex(12;{C4,C8})=17` (`literature.md` L15
table) caps it from above, giving exactly `m in {16,17}`.

## Result

| `m` | raw C4-free graphs | also C8-free | with an actual degree-1 vertex | F12 survivors |
|--:|--:|--:|--:|--:|
| 16 | 465 | 2 | **0** | 0 |
| 17 | 15,947 | 62 | **0** | 0 |

**Zero survivors at both layers.** Combined with the (`degree-1 x, edge
absent, internal degree>=3`) rooted-pair enumeration finding nothing to
enumerate in the first place, F12 holds.

**Honest note on the mechanism.** Every `{C4,C8}`-free graph on 12 vertices
with 16 or 17 edges turns out to have **minimum degree >= 2** — none of the
64 (`2+62`) `{C4,C8}`-free candidates at either edge count has *any*
degree-1 vertex at all. So F12 is established because the hypothesis
`d_B(x)=1` combined with `{C4,C8}`-freeness and this edge count is
**never simultaneously satisfiable** at order 12, not because a degree-1
vertex is shown to force a cycle through some clever argument. This is a
real, complete, correct proof of F12 as stated (the theorem is a universal
statement over an empty-when-C4/C8-free-required set, which is exactly how
universally-quantified statements over vacuous domains work) — flagged
explicitly rather than left implicit, matching this project's discipline.
It is also intuitively unsurprising: near the extremal edge bound, a
pendant vertex "wastes" edge budget relative to what a `{C4,C8}`-free graph
can otherwise pack in, so extremal/near-extremal instances tend to have no
low-degree vertices.

## Consequence: Type A eliminated entirely at n=32 (not just constrained)

`separator_theorem_order32_gap_analysis.md`'s **O32-2** used **F11**
(orders `<=11` always have `C4`/`C8`) to show every nontrivial bridge of a
Type-A 2-cut has order `>=12` (`c_i>=10`), forcing `n>=32` for any Type-A
2-cut, with equality pinning every bridge to order *exactly* 12.

**F12 closes exactly that remaining case.** Order-12 bridges *also* always
contain a `C4` or `C8` (by F12 itself), so the true bridge-order floor is
`>=13` (`c_i>=11`), giving

```
n >= 3*11 + 2 = 35
```

for any Type-A 2-cut — strictly greater than 32. **Consequently, at
`n=32` exactly, no Type-A 2-cut can exist at all**: the case that O32-2
left as "the unique surviving configuration" (three order-12 bridges,
`e_i in {16,17}`, max degree `<=5`) is now impossible, because F12 shows no
such order-12 bridge is `{C4,C8}`-free in the first place.

## Updated status of the order-32 3-connectivity target

Per `separator_theorem_order32_gap_analysis.md`'s Part 3 (missing lemmas):

- **O32-1** (cut vertices): free, no external premise needed. [done, prior session]
- **Type A**: **now fully eliminated at n=32**, via O32-2 + F12. [done, this pass]
- **Type B**: order bound only reaches `n>=22` (`O32-3`), not `n>=32` —
  **still open**, needs new machinery (a Type-B replacement/order lemma
  reaching 32, not currently in the repo).
- **Type C**: **no order bound exists at all** (F9/F11/F12 require
  `d_B(x)=1`; Type C only guarantees `min(a_i,b_i)<=2`, entirely outside
  the F-series' scope) — **still open**, needs a new `d_B(x)=2` F-series
  (named `FC-N` in the gap analysis, MISSING-2).

So "every order-32 minimal counterexample is 3-connected" now reduces to
exactly two remaining cases (Type B, Type C) instead of three — a genuine,
if partial, narrowing of the target, achieved with a few seconds of
computation once the exact search box was correctly identified.

**Labels** (matching F9/F11's own status exactly): F12 is
`COMPUTATIONALLY_VERIFIED`, not `PROVED_IN_MARKDOWN` — O32-2 and this
Type-A elimination inherit that status.
