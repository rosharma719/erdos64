# F19 also strengthens Type A and Type B directly — extending 3-connectivity
to every even order in [17,35]

## Status

[COMPUTATIONALLY_VERIFIED — free arithmetic consequence of `F19`
(`fcn_satsolver_extension.md`, already merged) applied to bridges that were
previously only given the weaker `F12` bound. No new computation.]

## The observation

`type_c_closure_order32.md` used `F19` (extended by monotonicity to forbid
`{4,8,16}`, giving every `d_B(x)=1` two-terminal graph order `>=20`) for
Type C. It did not occur to re-examine Type A and Type B with the same
upgrade, even though both of their bridges satisfy the F-series hypothesis
**exactly**, with no compromise:

- **Type A** (`two_cut.md` §2c): three bridges `B1,B2,B3`, **all** with
  `a_i=1` exactly (`a_1=a_2=a_3=1`, the defining condition). `f12_order12_
  result.md` used `F12` (order `>=13`) to get `n(G)>=3*13-4=35`.
- **Type B** (`type_b_11_22_decomposition.md` §1, §3): two bridges, **both**
  with `a_i=1` exactly. Section 3 used `F12` on the bare bridge to get
  order `>=13` per bridge, `n(G)>=13+13-2=24`, then switched to a dedicated
  census of the *closed* piece `B_i+xy` (FB22-17) to reach `n(G)>=34`
  because `F12` alone wasn't strong enough to beat that census.

**Both bridges' bare form (`a_i=1`, `xy notin E(B_i)`) is exactly what
`F19` was proved for.** Swapping `F12`'s order-13 floor for `F19`'s
order-20 floor (`fcn_satsolver_extension.md` §4.4 + the monotonicity
argument in `type_c_closure_order32.md`, which applies identically here —
nothing about it was Type-C-specific) gives, by the same arithmetic these
files already use:

```
Type A:  n(G) >= 3*20 - 4 = 56
Type B:  n(G) >= 20 + 20 - 2 = 38   (bare-bridge route; beats the
                                      dedicated FB22-17 census's 34
                                      outright, with less machinery)
```

**Type C is unaffected** (`type_c_closure_order32.md` already used `F19`
for its `a_i=1` sub-case; its binding constraint is `FC-18`'s weaker
order-19 floor for the `a_i=2` sub-case, which `F19` doesn't touch).

## Updated table

| case | previous bound | new bound | binding ingredient |
|---|--:|--:|---|
| Type A | `n>=35` | **`n>=56`** | `F19` (was `F12`) |
| Type B | `n>=34` | **`n>=38`** | `F19` on the bare bridge (was FB22-17 census) |
| Type C | `n>=36` | `n>=36` (unchanged) | `F19` + `FC-18` (already optimal) |
| cut vertex | excluded at every even `n` | unchanged | O32-1 |

**New overall floor for any 2-cut: `min(56,38,36) = 36`** (Type C remains
the binding case). This number is unchanged from `type_c_closure_order32.md`
and `three_connectivity_general_order.md`'s prior statement — **but it's
worth recording explicitly that Type A and Type B are not merely "also
closed," they now have enormous slack (56 and 38) relative to Type C's 36**,
which matters if `FC` is ever extended further (see below).

## Consequence: no change to the order-32 conclusion, but the general
corollary's arithmetic should cite the stronger numbers

`type_c_closure_order32.md`'s order-32 result and `three_connectivity_
general_order.md`'s "every even order in `[17,33]`" corollary both used
`min(35,34,36)=34` as the floor for "2-cut requires `n>=34`" — call this
`floor_old`. **With Type A and B strengthened, the relevant `min` for
those two specific files doesn't change** (`36` was already the binding
value via Type C, and Type C is untouched) — so no correction is needed
there.

**What *does* change: if `FC` is ever extended past `FC-18`,** Type C's own
bound moves, and *at that point* Type A/B's new slack (56, 38) means Type C
alone determines the new floor all the way up to `n(G)=56` — i.e. **Type A
and Type B will never again be the bottleneck** unless `FC` is pushed past
`F19`'s own order-20 equivalent. Concretely: if a future `FC-n` result ever
reaches `n=37` (order `>=38`, matching Type B's new floor) or `n=54`
(order `>=56`, matching Type A's), those cases would start to matter again;
anything below that, Type C alone (via further `FC` progress) is what
should be chased next, not Type A/B.

## Honest scope note

This file changes no headline conclusion — the order-32 target was already
closed, and the general corollary's stated range `[17,33]` is unaffected
(Type C's `36` was always the binding constraint, and it's untouched here).
Its value is (a) recording the stronger, now-available Type A/B numbers so
they're not silently stale relative to `F19`, and (b) clarifying that all
future effort on extending the "even order 3-connectivity" range past 33
should go toward extending `FC` (Type C's bottleneck), not Type A/B, which
now have very wide margins.
