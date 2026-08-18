# Type C is eliminated at n=32 — the order-32 3-connectivity target is complete

## Status

[COMPUTATIONALLY_VERIFIED — a pure logical (monotonicity) argument applied
to two already-computed, already-merged SAT results (`fcn_satsolver_extension.md`
§4.3-4.4: `F19` and `FC-18`). No new computation was run for this file; the
content is the argument connecting existing numbers to the Type-C order
bound, which `fcn_order15_result.md` and `fcn_satsolver_extension.md` both
explicitly flagged as *not yet done*.]

## The monotonicity observation

If a graph-existence predicate with forbidden-cycle set `S` is UNSAT (no
graph satisfies it), then the same predicate with any **larger** forbidden
set `S' ⊇ S` is also UNSAT. *Proof.* Any graph satisfying the `S'`-version
also avoids every length in `S` (since `S ⊆ S'`), hence would also satisfy
the `S`-version — so a solution to `S'` would produce a solution to `S`.
`S`-UNSAT means no such solution exists, so no `S'`-solution can exist
either. This needs no computation; it is set-containment on solution sets.

**Consequence, applied directly:** `fcn_satsolver_extension.md` §4.4 proved
`F13` through `F19` (`d_B(x)=1`, forbidden `{4,8}`) all UNSAT, contiguously,
with no gap. By monotonicity, **`F13`-`F19` are therefore also UNSAT for
forbidden `{4,8,16}`** — the set actually required by the application
(a genuine bridge of a minimal counterexample must avoid every power-of-two
cycle length that fits in its own order; for `n<=19` that set is exactly
`{4,8,16}`, since `32>19`). Combined with the pre-existing `F9`-`F12`
(`f12_order12_result.md`, itself only needing `{4,8}` since `n<=12<16`
cannot contain a `C16` at all), **every order from the applicable floor
through 19 is UNSAT for the real, application-relevant forbidden set**:

> **Every simple two-terminal graph `B` with `d_B(x)=1`, `d_B(y)>=1`,
> internal min-degree `>=3`, `xy notin E(B)`, `B+xy` 2-connected, and
> `|V(B)|<=19`, contains a `C4`, `C8`, or `C16`.**

i.e. **any such bridge that is genuinely free of all relevant power-of-two
cycles has order `>=20`.**

Likewise, `fcn_satsolver_extension.md` §4.3 directly computed (no
monotonicity needed — `C16` was in the forbidden set from the start) `FC-16`,
`FC-17`, `FC-18` (`d_B(x)=2`, forbidden `{4,8,16}`) all UNSAT, contiguous
with `fcn_order15_result.md`'s pre-existing `FC-5`-`FC-15` (also
automatically valid for `{4,8,16}` by the same `n<=15<16` argument as above).
So:

> **Every simple two-terminal graph `B` with `d_B(x)=2`, `d_B(y)>=2`,
> internal min-degree `>=3`, `xy notin E(B)`, `B+xy` 2-connected, and
> `|V(B)|<=18`, contains a `C4`, `C8`, or `C16`.**

i.e. **any such bridge that is genuinely free of all relevant power-of-two
cycles has order `>=19`.**

**Neither of these needs the currently-running `n=19,20,21` background jobs**
(`p2_n19`/`p2_n20`/`p2_n21` in `fcn_satsolver_extension.md`'s companion
processes) — those jobs are chasing the exact frontier of `FC-19`/`FC-20`/
`FC-21`, which is not needed for what follows.

## Applying this to Type C

`two_cut.md`'s exact Type-C definition (quoted, line 208): 2 bridges `B1,B2`,
`xy notin E(G)`, `a1+a2>=3`, `b1+b2>=3`, and **for each bridge `i`
individually, `ai<3` or `bi<3`** (neither bridge alone reaches both terminal
degrees `>=3`). Since `ai,bi>=1` always for a nontrivial bridge (`two_cut.md`
§1, cited already in `f12_order12_result.md`/`fcn_order15_result.md`),
`ai<3` means `ai in {1,2}` exactly — the same exact hypothesis space F/FC
were built for.

**Claim: every Type-C bridge `Bi` has `|V(Bi)| >= 19`.**

*Proof.* By definition, `ai<3` or `bi<3` for bridge `i`. Two (non-exclusive)
cases:

- **The low-degree terminal has degree exactly 1** (either `ai=1` or
  `bi=1`, possibly relabelled so that terminal is called `x` in the F-series
  sense). The F-series hypothesis on the *other* terminal is only
  `d_B(y)>=1`, which holds automatically (`§1`'s `ai,bi>=1` fact) —
  **no additional condition on the other terminal's degree is needed**. By
  the boxed F-series result above, `|V(Bi)|>=20 >= 19`.
- **The low-degree terminal has degree exactly 2, and this is the only
  low-degree terminal** (i.e. `ai=2` and `bi>=2`, or symmetrically), so the
  degree-1 case above does not apply to either terminal. The FC-series
  hypothesis `d_B(y)>=2` is then satisfied by the other terminal directly
  (`bi>=2` by assumption in this case). By the boxed FC-series result above,
  `|V(Bi)|>=19`.

These two cases are exhaustive: `ai<3` forces `ai in {1,2}`, and similarly
for `bi`; if either equals 1, the first case applies (regardless of the
other terminal's value, since F-series imposes no lower bound beyond the
universal `>=1`); otherwise both low-degree terminals (whichever of `ai,bi`
is `<3`) equal exactly 2, and the second case applies. In both cases
`|V(Bi)| >= 19`. ∎

## The order-32 consequence

`two_cut.md` (line 1125, "Type C ... `n(G) = n1+n2-2`", already `[PROVED]`
in this repo, no new derivation needed here):

```
n(G) = |V(B1)| + |V(B2)| - 2 >= 19 + 19 - 2 = 36.
```

**`n(G)=32 < 36` is impossible under Type C.** No Type-C 2-cut can exist in
an order-32 minimal counterexample.

## Consolidated status of the order-32 3-connectivity target

| case | status | source |
|---|---|---|
| O32-1 (cut vertices) | eliminated | `separator_theorem_order32_gap_analysis.md`, free |
| Type A | eliminated at `n=32` | F12 + O32-2 (`f12_order12_result.md`) |
| Type B | eliminated at `n=32` (in fact `n>=34`) | FB22-17 census (`type_b_11_22_decomposition.md`) |
| Type C | **eliminated at `n=32`** (in fact `n>=36`) | **this file**, via `F19`+`FC-18` + monotonicity |

**All four cases are now closed.** Modulo the tiers already attached to each
input (`F12`/`FC-15`/`F19`/`FC-18` are `COMPUTATIONALLY_VERIFIED` — SAT-solver
UNSAT verdicts trusted per `fcn_satsolver_extension.md` §7's stated
mitigations, not proof-assistant-certified; `type_b_11_22_decomposition.md`'s
FB22-17 census carries the same tier), this establishes:

> **Every order-32 minimal Erdős–Gyárfás counterexample (if one exists) is
> 3-connected.**

**What this is not.** This is not a proof that no order-32 counterexample
exists — only that *if* one exists, it has no 2-cut and no cut vertex, i.e.
it is 3-connected. It also does not extend automatically to other orders:
the specific bound `n(G)>=36` for Type C, `>=34` for Type B, and Type A's
elimination are all order-32-specific consequences of combining these
per-bridge floors with `n(G)=32` exactly; a different target order would
need the same argument re-run against its own value.

**Honest caveat on trust level, stated plainly.** The load-bearing new facts
here (`F13`-`F19` and `FC-16`-`FC-18`) are CDCL SAT-solver UNSAT verdicts,
not hand proofs and not machine-checked in a proof assistant. They are
validated the way `fcn_satsolver_extension.md` describes (exact agreement
with brute-force ground truth through `n=9` including 23 genuine SAT
witnesses; exact replay of the previously-established `F9`-`F12`/`FC-5`-`FC-15`
results; independent CP-SAT re-implementation) — real, substantive
validation, but not a certificate. This file inherits that trust level
exactly, and should be read at the same tier as `F12` and `FC-15` themselves,
not as a hand-verified theorem.
