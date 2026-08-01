# FC-15: proved — a new per-bridge order bound for the (2,*)-terminal case
(see the corrected "Consequence" section below: this does NOT by itself
push Type C's overall order bound to n>=32)

## Status

[COMPUTATIONALLY VERIFIED, exhaustive, dual-detector cross-validated].
Pursued as the highest-leverage available target: `separator_theorem_
order32_gap_analysis.md`'s MISSING-2 explicitly named this as the needed
next step ("Begin MISSING-2 at `nB=8,10,12` for the `(2,2)` terminal
profile... `N=15` would be needed just to reach 32").

**Theorem (FC-15).** Every simple two-terminal graph `B` with
`|V(B)|<=15`, `d_B(x)=2`, `d_B(y)>=2`, `d_B(v)>=3` for every internal
vertex, `xy notin E(B)`, and `B+xy` 2-connected, contains a `C4` or a `C8`.

## Method

`verifier/type_c_fcn_series.py`. Search-box: `2|E(B)| >= d(x)+d(y)+3(n-2)
>= 3n-2`, so `m_min = ceil((3n-2)/2)`; combined with `ex(n;{C4,C8})`
(`literature.md` L15 table), `n` is **infeasible by pure counting alone**
(`m_min > ex(n)`, no `{C4,C8}`-free graph with this degree profile can
exist, zero search needed) at `n in {5,6,7,9,11}`. At the remaining
`n in {8,10,12,13,14,15}`, `m_min == ex(n)` exactly, pinning any instance to
an extremal `{C4,C8}`-free graph — a search space small enough to enumerate
exhaustively via `nauty-geng`.

**A real bug caught and fixed during this work**: at odd `n` the naive
"both terminals exactly degree 2" degree sequence is parity-impossible
(`2+2+3(n-2)` is odd), so the true minimum-edge degree sequence spreads its
one unit of unavoidable slack onto either `d(y)` or one internal vertex —
not necessarily giving two degree-2 vertices. An early version of this
script assumed the even-`n` shape uniformly, generated with `-D3` even at
odd `n`, and got a spurious "0 survivors" by silently filtering out every
candidate as the wrong shape rather than genuinely searching. Caught by
inspecting *why* `n=13` showed zero rooted pairs (traced actual raw
candidates by hand) before trusting the result; fixed by using the correct
degree cap (`-D4` when slack`=1`) and a general rooted-pair search over
every actual degree-2 vertex as `x` and every other vertex as `y`
(mirroring `type_a_order12_f12.py`'s pattern), not an assumed shape.

**Scale note**: `n=15` has 2,625,442 raw `-D4` candidates — too many for a
per-graph Python DFS pass. Used the independently-implemented C batch
detector (`check_power_masks.c`, already certified in the F9-F12 pipeline)
for the primary `C4`/`C8` filter, with the Python DFS detector as an
independent cross-check on every `C4`/`C8`-free survivor plus a random
2,000-graph sample of the rejects (to also catch a hypothetical
false-negative in the C detector, not just false positives).

## Result

| `n` | status | `m_min` | `ex(n)` | slack | raw | `{C4,C8}`-free | mismatches | FC survivors |
|--:|---|--:|--:|--:|--:|--:|--:|--:|
| 5,6,7,9,11 | infeasible by counting | — | — | — | — | — | — | 0 |
| 8 | searched | 11 | 11 | 0 | 1 | 0 | 0 | 0 |
| 10 | searched | 14 | 14 | 0 | 11 | 0 | 0 | 0 |
| 12 | searched | 17 | 17 | 0 | 75 | 0 | 0 | 0 |
| 13 | searched | 19 | 19 | 1 | 33,677 | 3 | 0 | 0 |
| 14 | searched | 20 | 20 | 0 | 677 | 0 | 0 | 0 |
| 15 | searched | 22 | 22 | 1 | 2,625,442 | 14 | 0 | 0 |

**Zero survivors, zero detector mismatches, at every order 5 through 15.**
The `n=13`/`n=15` `{C4,C8}`-free survivors (3 and 14 respectively) were
individually inspected: each has *too many* degree-2 vertices for any valid
`(x,y)` assignment to leave every other vertex at degree `>=3` (e.g. the
`n=13` instances have degree sequence `2,2,2,2,3,3,3,3,3,3,4,4,4` — four
degree-2 vertices, so any choice of `x,y` from among them strands at least
two more at degree 2 among the "internal" vertices, violating the `>=3`
requirement). This is the same honest "no valid shape exists" mechanism
documented for F12, not a search failure.

## Consequence: a real per-bridge bound exists now, but NOT yet "Type C forces n>=32" — corrected

**First pass at this write-up overclaimed the consequence; corrected here
before it went anywhere.** The tempting argument was: every Type-C bridge
has `a_i<3` or `b_i<3` (two_cut.md), so either the F-series (`a_i=1`) or
FC-15 (`a_i=2`) applies, both eliminating `C4`/`C8` up to order 15/13
respectively, so "every bridge has order `>=16`, forcing `n>=32`." **This
is wrong**: Type C's defining condition (`two_cut.md`, quoted directly) is
only `a_i<3 OR b_i<3` for each bridge — it does **not** exclude the
`a_i=1` sub-case. A Type-C bridge whose low-degree terminal happens to be
exactly 1 only gets the *weaker* F12-derived bound (order `>=13`), not the
FC-15 bound (order `>=16`). Combining both bridges under the weaker,
always-safe bound gives only `n >= 13+13-2 = 24` — **not an improvement
over the existing `O32-3`-style order-22 bound** by nearly as much as first
claimed, and FC-15 alone does not push Type C to `n>=32`.

**What FC-15 actually, correctly establishes**: a genuine new per-bridge
fact — *any* Type-C (or Type-B) bridge whose low-degree terminal is
exactly 2 (not 1) must have order `>=16`. This is real, novel content
(the gap analysis explicitly listed it as MISSING-2, and it did not exist
in this repo before this pass), but turning it into an improved *overall*
Type-C order bound requires an additional argument this file does **not**
supply: showing that the `a_i=1` sub-case can itself be excluded for
Type C (or handled by some other route), so that FC-15's stronger bound
applies unconditionally. That is presumably close to what the newest chat
message's Type-C reduction ("a mixed `(1,2)`-piece of odd order at most
17") is doing — a sharper, bridge-pairing argument this file does not
reconstruct or verify. **Do not cite this file for an `n>=32` Type-C
conclusion.** The honest state: FC-15 is proved; its consequence for the
overall order-32 target is a real but only *partial* per-bridge
strengthening, not a closed case.

## Updated status of the order-32 3-connectivity target

- **O32-1** (cut vertices): closed. [prior session]
- **Type A**: fully eliminated at n=32 (F12 + O32-2). [this session, prior turn]
- **Type C**: FC-15 gives a genuine new per-bridge bound (order `>=16` when
  the low-degree terminal is exactly 2) but **does not by itself improve
  the overall order bound past `n>=24`** — still open, and the "mixed
  `(1,2)`-piece" reduction reported in chat is a different, sharper
  argument not reconstructed here. [this pass: real partial progress, not closure]
- **Type B**: per the newest chat message, reportedly reduces further to a
  `(1,1)`-piece of order `>=13` paired with a `(2,2)`-piece of order
  `<=21` — **not independently verified or reconstructed here**; this
  session's FC-15 result is a different, self-contained computation
  (the base two-terminal `(2,*)` profile generally) that doesn't depend on
  that specific Type-B refinement and isn't a duplicate of it, but also
  isn't confirmed to be the same fact.
  **[RESOLVED later this session — `type_b_11_22_decomposition.md`.]** The
  reported reduction does reconstruct: the `(1,1)`-piece is the bare bridge
  `B_i` (order `>=13` by F11+F12) and the `(2,2)`-piece is its closure
  `B_i+xy` (order `<=21` by `n=n_1+n_2-2=32`). Note FC-15 itself does **not**
  apply to either — Type B always has `a_i=1`, never 2, and the closure
  contains `xy`, violating FC-15's `xy notin E(B)` hypothesis. A separate
  census (FB22-17, same method, terminal edge *present*) closes Type B at
  `n=32` outright. FC-15's `n=13,15` layers were reused there and, usefully,
  shown to be rejected by the degree-shape test alone — so FC-15's verdict at
  those orders is not an artefact of its `xy notin E` filter.

**Labels**: FC-15 is `COMPUTATIONALLY_VERIFIED`, matching F9/F11/F12's own
status tier — not `PROVED_IN_MARKDOWN`. Its consequence for Type C's
overall order bound is explicitly **not established** here (see correction
above) and should not be cited as such.
