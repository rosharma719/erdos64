# Safe-4-pole decomposition of the Type-T port completion

## Status

**Independently verified here, 2026-07-30, against every completed-graph
artifact currently in the repo.** This file records the first computational
check of a decomposition claim proposed in chat (not previously in any
branch — see `verification_status.md` cross-reference below): since every
completed `j` instance has degree sequence `(4,3^{n-1})` with `z0` the unique
degree-4 vertex, deleting `z0` always yields a **safe 4-pole** — a connected
graph whose 4 terminals (the former neighbours of `z0`) each have degree
exactly 2 and every other vertex has degree `>=3`.

## The two claims

For a safe `d`-pole capped by a new vertex `z0` joined to all `d` terminals,
every simple cycle through `z0` uses exactly two of the cap edges and a
terminal-to-terminal path in the pole; every other simple cycle lies entirely
in the pole. Hence for every `k`:

```
N_{2^k}(G) = N_{2^k}(G - z0) + sum_{{u,v} subset terminals} N_{u,v}(2^k - 2)
```
("internal cycles" + "shifted-length terminal paths", `d=4` here so 6 pairs).

Second, since each completion "passage" (a triple hub, or the two-hub-plus-edge
linked gadget) contributes exactly 2 edges of path length, and between `m`
passages on a terminal path there are `m+1` positive-length core segments, a
terminal path of length `L=2^k-2` satisfies `3m+1 <= L`, i.e.

```
m <= floor((2^k - 3) / 3)
```

For `C16` (`k=4`) this gives `m<=4` — i.e. **every 5-passage support in the
certified `m=5` layer (`type_t_port_c16_passage_projection.md`,
2,944,894 verified minimal supports) must be internal to the pole, never a
terminal path**, which is consistent with (and gives an independent
structural explanation for) why the `m=5` layer was tractable as a purely
internal enumeration.

## Verification method

`verifier/type_t_port_safe_4pole.py` loads a completed graph from any
`{parameters, completion:{edges}, best_short_cycle_counts}` JSON (the schema
used under `data/type_t_port_c16/` and `data/type_t_port_multipole/`),
confirms the unique-degree-4/4-terminal/degree-2/connected pole structure,
then independently computes both sides of the decomposition by brute-force
`networkx.simple_cycles` (internal count) and exact-length DFS path
enumeration (terminal-path count, also tagging each witness with its `m` =
number of path vertices at core-index `>= 5*2^j+7`, i.e. hub vertices).

```
python verifier/type_t_port_safe_4pole.py <completion.json...> --k 4   # C16
python verifier/type_t_port_safe_4pole.py <completion.json...> --k 3   # C8
```

## Results — every completed instance in the repo, both targets

| instance | target | internal | terminal-paths | predicted | reported | match | max `m` | bound | `m` histogram |
|---|---|--:|--:|--:|--:|:-:|--:|--:|---|
| `j4_a28_c4` (LNS best, `C16=509`) | C16 | 356 | 153 | 509 | 509 | OK | 4 | 4 | {2:76, 3:68, 4:9} |
| `j4_a28_c4` (local search) | C16 | 712 | 215 | 927 | 927 | OK | 4 | 4 | {2:75, 3:118, 4:22} |
| `j4_a2_c2` (local search) | C16 | 824 | 252 | 1076 | — | OK | 4 | 4 | {2:99, 3:140, 4:13} |
| `j4_a55_c7` (local search) | C16 | 581 | 246 | 827 | — | OK | 4 | 4 | {2:111, 3:107, 4:28} |
| `j5_a2_c2` (local search) | C16 | 1275 | 129 | 1404 | 1404 | OK | 4 | 4 | {2:40, 3:77, 4:12} |
| `j4_a28_c4` (LNS best) | C8 | 0 | 0 | 0 | 0 | OK | 0 | 1 | {} |
| `j4_a28_c4` (local search) | C8 | 0 | 0 | 0 | 0 | OK | 0 | 1 | {} |
| `j4_a2_c2` (local search) | C8 | 1 | 0 | 1 | 1 | OK | 0 | 1 | {} |
| `j4_a55_c7` (local search) | C8 | 13 | 0 | 13 | 13 | OK | 0 | 1 | {} |
| `j5_a2_c2` (local search) | C8 | 0 | 0 | 0 | 0 | OK | 0 | 1 | {} |

**Both claims hold exactly on every one of the 10 (instance, target) checks
available** — every predicted total matches the artifact's own reported
short-cycle count where one was recorded, and `max m` never exceeds the
proved bound (and is never even close for `C8`, where the bound `m<=1`
apparently forces `m=0` in every observed case — terminal paths never appear
in the `C8` count for any of these five completions).

**Labels:** decomposition formula and the `m<=floor((2^k-3)/3)` bound —
[COMPUTATIONALLY VERIFIED] on all 10 checks above; not yet a general proof
independent of the specific `(j,a,c)` completions on disk (that direction —
"true for *every* valid completion", not just these five heuristic/LNS
survivors — is elementary given the fixed degree sequence and would follow
from the same case-free argument used for `type_t_port_core_dyadic_avoidance.md`,
but has not been written up as a standalone proof here).

## What this does and does not establish

This decomposition does **not** by itself close any open question in
`type_t_port_multipole_completion.md` (still `UNKNOWN`) or
`type_t_port_c16_passage_projection.md` (`m=4` still the sole open static
layer). What it gives: a structurally motivated split of any future `C16`
elimination argument into "kill the internal-pole `C16`s" (a fixed-rank,
`z0`-free subproblem) and "kill the six terminal-path `C16`s" (bounded to
`m<=4` passages each, i.e. within reach of the already-certified `m<=4`
static layers) — separately, rather than as one combined 2,944,894+-support
search. This matches the chat proposal's framing (safe-`d`-pole reduction of
the Type-T port family) and is now backed by a runnable, general (not
instance-specific) verifier rather than assertion.

## Appendix: pure-combinatorics claims from the same proposal

`verifier/type_t_port_repair_combinatorics.py` independently checks the
graph-independent claims proposed alongside the pole decomposition:
`M_m=(3m)!/(6^m m!)` and the `m!` hub-triple-preservation count for an
adaptive two-/three-/four-/five-block local repair search (m=2..5, exact
arithmetic); connectivity of the space of `t`-triple partitions under
two-block moves with diameter `<=2(t-1)` (verified by exhaustive BFS,
`t=3`: 280 states, diameter 3<=4; `t=4`: 15,400 states, diameter 4<=6 — both
strict, and the BFS state counts match `M_t` exactly, cross-checking the move
generator against claim 1); and the Mersenne-flavoured modular residue sets
`R_M={2^k mod M : k>=2}` for `M=31,127,255` (all match the proposed values,
e.g. `R_31={1,2,4,8,16}`, `R_31-2={30,0,2,6,14}`). All [COMPUTATIONALLY
VERIFIED]. These are generic to the proposed repair/pole-capping strategy,
not evaluated against any specific completed graph.

## Not yet implemented (open, from the same chat proposal)

The following ideas from the same proposal have **no artifact anywhere in
this repo** (checked across every local/remote branch) and were not
attempted in this pass: a period-three periodic bulk completion rule: (5*p
deficient vertices per period, `3|p` forces minimum period 3); a finite
"frontier automaton" certifying an infinite family periodic construction
modulo a bound and a modulus (the closest existing stub is
`type_t_port_passage_templates.md`'s explicitly-not-attempted Phase 7-9
sketch); and a Mersenne/odd-modulus residue certificate
(`R_M = {2^k mod M : k>=2}`) applied to this construction specifically (the
residue arithmetic itself — `R_31={1,2,4,8,16}` etc. — was checked
standalone in a scratch script, not against this graph family). These remain
the next concrete steps if the periodic/infinite-family route (rather than
the finite `j=4`/`j=5` route) is prioritized.

## Cross-reference: external report on `q(G)>=4`/`q(G)>=6`

A separately pasted report claimed `q(G)>=4` and a "provisional" `q(G)>=6`
for a minimal counterexample (unrelated defect-parameter track, not this
port-core family). Checked against the actual repo: `q(G)>=4` is real and
matches `defect_three.md`/`proof.md` P12 essentially verbatim (`h<=3` case
table, all 6 `(h,c1,c3)` rows eliminated). The `m=5` passage run the report
described as "interrupted before writing a completion artifact" in fact
completed and was certified (`status: COMPUTATIONALLY_CERTIFIED`,
`x1_completed: 87/87`, `verification_rejected: 0` in
`data/type_t_port_c16_passages/j4_a55_c7_c16_passages_m5_summary.json.gz`).
The `q(G)>=6` claim, the two order-30 near-miss graphs
(`C4=0,C8=6,C16=0`/`C4=0,C8=5,C16=335`), and the triangle-expansion census
counts have **no matching artifact anywhere** in this repo's git history
(all branches checked) and should not be treated as established.
