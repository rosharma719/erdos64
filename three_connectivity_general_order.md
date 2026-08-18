# Generalizing beyond n=32: every even-order minimal counterexample with
17<=n<=33 is 3-connected

## Status

[COMPUTATIONALLY_VERIFIED — a direct generalization of `type_c_closure_
order32.md`, `f12_order12_result.md`, and `type_b_11_22_decomposition.md`;
no new computation, only recognizing that all the underlying per-bridge
order bounds are stated for a bridge `B_i` in isolation and never actually
used the target order `n(G)=32` anywhere except in the final arithmetic
step.]

## The observation

`type_c_closure_order32.md` proves `n(G)>=36` for any `G` (any order
whatsoever) that has a Type-C 2-cut — the `>=36` comes entirely from the
per-bridge floor `|V(Bi)|>=19` (`F19`+`FC-18`+monotonicity, itself a fact
about two-terminal graphs `B` with no reference to any ambient `G` or its
order) plus the general formula `n(G)=n1+n2-2` (`two_cut.md`, holds for
every Type-C 2-cut in every graph). **Nothing in the chain assumed
`n(G)=32`.** The same is true of the other two branches, already recorded
as such in their own source files:

- **Type A**: `f12_order12_result.md`'s own text states the general form
  directly — "`n >= 3*11+2 = 35` for **any** Type-A 2-cut" (not order-32
  specific).
- **Type B**: `type_b_11_22_decomposition.md`'s FB22-17 gives `n(G)>=34`
  for any `G` with a Type-B 2-cut (stated there as "Type B is now
  eliminated at `n=32`... in fact `n>=34`").
- **Cut vertices**: `separator_theorem_order32_gap_analysis.md`'s O32-1 is
  explicit already — "not an 'order-32' fact at all — it holds at every
  even order" (S5's parity argument: a cut vertex forces `n` odd).

## The general theorem

Every 2-cut of a 2-connected minimal counterexample is exactly Type A, B,
or C (`separator_theorem_order32_gap_analysis.md` §2c, cited already for
the order-32 case, itself order-independent — the trichotomy is by
terminal-degree profile alone). Combining the three order floors:

> **If a minimal Erdős–Gyárfás counterexample `G` has *any* 2-cut, then
> `|V(G)| >= 34`** (the minimum of 35, 34, 36 across Type A/B/C).

> **If `|V(G)|` is even, `G` has no cut vertex** (O32-1, S5's parity claim,
> unconditional on order).

**Corollary.** *Every minimal Erdős–Gyárfás counterexample `G` with `|V(G)|`
even and `17 <= |V(G)| <= 33` is 3-connected.* (The lower bound 17 is the
general, non-cubic floor already established, `literature.md` L10; the
upper bound 33 is `34-1`, i.e. the largest order still excluded from having
any 2-cut.) Concretely this covers orders `{18, 20, 22, 24, 26, 28, 30, 32}`
— eight even orders below the L10 lower bound was not previously known to
be 3-connected at any of them individually, and this is the first time any
of them besides 32 has been checked at all.

**What this does not cover.** Odd orders in `[17,33]` are not resolved
here — O32-1's cut-vertex exclusion is specific to even order (a cut vertex
forces two equal-order lobes, which forces `n` odd, so odd `n` cannot be
excluded from having a cut vertex by this argument). An odd-order minimal
counterexample in this range could in principle still have a cut vertex;
it is however still guaranteed to have no 2-cut of any type (the `>=34`
bound above is order-parity-independent), so an odd-order counterexample
in `[17,33]` is 2-connected-or-has-a-cut-vertex, with the 2-cut branch
fully closed either way.

## Why this matters, and what it doesn't establish

This is a genuine broadening of scope (structural information about eight
specific low orders that had none before), obtained for free by simply
restating already-proved per-bridge facts without the order-32 assumption
baked in early. **It does not, by itself, shrink the general lower bound
past 17**, and it does not exclude any of these orders outright — a
3-connected order-`{18,...,32}` counterexample remains logically possible
as far as this file is concerned. It is a structural constraint on any
such object, of exactly the same kind and tier as the order-32-specific
statement in `type_c_closure_order32.md`, now known to hold at every even
order in range rather than one.

**Trust tier**: identical to `type_c_closure_order32.md` — inherits the
`F19`/`FC-18` SAT-solver-UNSAT trust level, `COMPUTATIONALLY_VERIFIED`, not
proof-assistant-certified.
