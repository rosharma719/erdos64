# Audit: "every edge lies on an odd cycle of length 2^k+1, and every
vertex has an incident edge on at least two such cycles"

## Status

[PARTIAL — nontriangle-edge part fully confirmed as already-proven
repo content; the triangle-edge part appears to be a genuine gap, not
currently closed by anything in this repo; the "two witnesses on one
edge" part is not supported by anything found here]

This claim was relayed without an external attribution this time. Applying
the same discipline used for every previous external report this session
(verify what's checkable, flag what isn't, correct overclaims explicitly
rather than silently): here is exactly what traces through and what
doesn't.

## Part 1: nontriangle edges — CONFIRMED, already proven exactly as stated

`contraction.md` Part I's near-power edge lemma (`[PROVED]`, line 119):
*for every nontriangle edge `e=uv` of `G`, `G` contains a genuine simple
cycle of length `2^k+1` through `e`.* This is unconditional, unrestricted,
and already on record — nothing new needed here. At a **Type N** cubic
vertex (independent neighbours `a,b,c`), all three incident edges are
nontriangle edges, so all three individually get their own `2^k+1`
witness — this part of the "every edge" claim, and in fact a stronger
form of the "two witnesses" claim (three separate *edges* each with a
witness, from three different neighbour pairs), was already established
and audited in `cubic32_mersenne_audit.md` Finding 2 and
`cubic34_factor_census_audit.md` Finding 2.

## Part 2: triangle edges — NOT established for all three edges; traced
through the exact mechanism and found a real gap

At a **Type T** cubic vertex `v` (triangle `{v,a,b}`, third neighbour `c`,
`vc` the unique nontriangle edge — covered by Part 1 already), the two
triangle edges `va`, `vb` are **not** nontriangle edges, so Part 1's lemma
does not apply to them directly. Two mechanisms in this repo produce
witnesses touching the triangle, and neither guarantees all three edges:

**Mechanism A — bare triangle contraction** (`contraction_atoms.md`
III.2, `[PROVED]`). Contracting the whole triangle `T={a,b,c}` (using `v`
in place of whichever letter) is unconditionally guaranteed (by
order-minimality, verified directly: III.1 shows every triangle is a
valid atom, and `contraction_atoms.md` I.3 gives the general
order-minimality argument that applies to it) to produce **some**
power-of-two cycle `D` in `G/T`, which attaches at **some** forced-distinct
pair of `T`'s three vertices — but *which* pair is a fact about the
specific graph, not something the proof gets to choose. Only the edge
**between the two attachment vertices** gets a `2^k+1` witness this way;
the other two edges of the triangle get nothing from this mechanism.

**Mechanism B — closed-neighbourhood contraction at `v`**
(`contraction_neighborhood.md` Part II, `[PROVED]`). This is the sharper,
already-worked-out version of exactly this question for a Type T vertex,
and its own stated conclusion is explicit: *"`N[v]`-contraction... forces
one of two paired-offset systems, depending only on which pair `D` happens
to attach at:* `{2^k+1, 2^k+2}` *(pair `(a,b)`) or* `{2^k+2, 2^k+3}`
*(pair `(a,c)` or `(b,c)`)."* **In the second case — which is not excluded
by anything in the file — the result is `{2^k+2, 2^k+3}`, and neither of
those is `2^k+1`.** This is the file's own honest conclusion, not a
misreading: II.2 explicitly confirms "nothing forces `D` and `D'` to be
'the same' cycle" between the two mechanisms, so Mechanism A's `D` and
Mechanism B's `D` can independently land on the unfavourable pair.

**Consequence, checked by trying to route around it.** Running the same
closed-neighbourhood analysis centred at `a` instead of `v` (both cubic
by M1 — every triangle has `>=2` cubic vertices, `contraction_atoms.md`
line 520) could in principle hit edge `vb`'s "own" favourable pair
`(v,b)`; centred at `b`, edge `va`'s pair `(v,a)`. But each of these three
independent attempts (at `v`, `a`, `b`) has its **own** independent
"unfavourable" outcome, and nothing in the repo shows the three outcomes
can't simultaneously all be unfavourable — `contraction_mixed_witness.md`
Part IV in fact proves the opposite of what would be needed to rule this
out: every one of the `{2^k+2,2^k+3}`-type combinations is
**"unconditionally safe"** (never arithmetically forced into a
contradiction), which is precisely why that file's own Part X records the
saturation/witness-system work as "neither Type N nor Type T eliminated."

**Conclusion for Part 2.** As things stand in this repo, it is **not**
established that every triangle edge lies on a `2^k+1`-length cycle — only
that *some* triangle edge does, contingent on which attachment pair a
graph-specific power-of-two cycle happens to hit, and the unfavourable
case is explicitly shown safe (not excludable by current machinery) in
`contraction_mixed_witness.md`. **This appears to be a genuine, currently
open gap, not a re-derivation of existing content** — unlike the last few
external claims audited this session (the order-32/34 "witness theorems"),
which turned out to already be proven here under different names, this
one does not.

## Part 3: "an incident edge lying on at least two such cycles" — not
found

Nothing located in `contraction.md`, `contraction_atoms.md`,
`contraction_neighborhood.md`, `contraction_mixed_witness.md`,
`contraction_intersections.md`, or `contraction_saturation.md` establishes
that any *single* edge carries two independent `2^k+1`-length witnesses
(as opposed to two different *edges*, each carrying one — the weaker,
already-proven fact from Part 1). The base near-power edge lemma
(`contraction.md` I.2–I.4) only guarantees **at least one**
power-of-two cycle exists in the relevant quotient, hence at least one
lifted witness; nothing forces a second, distinct one through the same
edge.

## What to do with this

Given Part 2 and Part 3 don't currently trace through, this claim should
**not** be used as a load-bearing input to further work (e.g. it should
not be added as a constraint to the running cubic order-32 SAT search,
and should not be cited alongside `type_c_closure_order32.md` or
`three_connectivity_general_order.md` as established). If there is a
genuinely new argument closing the Mechanism-B gap (ruling out the
`{2^k+2,2^k+3}` case, or supplying a second independent witness on some
edge), it isn't reconstructed here and would need to be supplied and
independently checked the way every other claim this session has been —
this file is not a refutation, only an honest "traced through, doesn't
yet close" report, exactly parallel to `fcn_order15_result.md`'s own
self-correction earlier this session.
