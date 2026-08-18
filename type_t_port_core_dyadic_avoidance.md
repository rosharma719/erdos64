# Bare-core dyadic-cycle avoidance for all j (2-adic argument)

**Status (2026-07-29): PROVED, unconditionally.** Completeness of the 35
affine forms — the gap flagged below when this file was first written — is
now closed by an independent kernel/cycle-space derivation
(`verifier/type_t_port_kernel_cycle_space.py`): **the bare core `H(j,a,c)`
avoids every dyadic cycle length, for every valid `j>=4` and every valid
`a,c`.** See "Completeness, proved" below.

This directly addresses the open precondition both the template-lifting
agent (`type_t_port_passage_templates.md`) and the C16-passage agent's
audit flagged as UNKNOWN: does the bare core `H(j,a,c)` avoid `C4,C8,C16`
(indeed every dyadic length) for *all* sufficiently large `j`, not just the
tested `j=4,5,6`?

## The affine forms

`type_t_port_completion.md` Section 1 reports the complete simple-cycle
spectrum of the bare core for `j=4,5,6` (61 cycles each, tested across "all
nine extreme/interior `(a,c)` cross-combinations" per `j`, one representative
spectrum reported per `j` since it did not vary across those 9 combinations).
Fitting each of the 35 distinct lengths at `j=5,6` (`Y=32,64`) to an affine
form `l(j) = A*2^j + B` — the two multiplicity sequences are identical in
sorted order, so the pairing is unambiguous — gives **35 forms with clean
integer `(A,B)` coefficients** (`A` in `{0,1,4,5}`), and predicting `j=4`
from those coefficients reproduces the reported `j=4` spectrum **exactly**,
including the two accidental coincidences where two different forms happen
to collide to the same integer at the smaller `Y=16` (e.g. `72` appears once
with multiplicity 4 at `j=4`, matching the *sum* of four separate
multiplicity-1 forms that are still distinct at `j=5,6`). See the
verification script output below; this 3-point exact match across integer
coefficients is very strong evidence the fit is the true underlying
structure, not a coincidence.

## The 2-adic argument (fully rigorous, no caveats)

For each of the 35 `(A,B)` pairs, is `A*2^j+B` ever a power of two, for any
`j>=4`?

* **`A=0` (5 forms, values `3,6,7,9,10`):** constant in `j`; none is a power
  of two, so none ever will be.
* **`A>0, B=0` (1 form, `A=5`):** `5*2^j` is a power of two iff `5` is; it
  isn't, so never.
* **`A>0, B!=0` (29 forms):** let `v = v_2(B)` (2-adic valuation). For
  `j > v`, `v_2(A*2^j) = j + v_2(A) > v = v_2(B)`, so
  `v_2(A*2^j+B) = v` exactly (the smaller of two different valuations). A
  positive power of two has valuation equal to its own log2, so if
  `A*2^j+B = 2^k` for some `j>v`, then `k=v`, i.e. `A*2^j+B = 2^v`, a *fixed*
  target value — but `A*2^j+B` is strictly increasing in `j` (`A>0`), so at
  most one `j` can ever hit that fixed target, and it must be a small one.
  Concretely: **only `j` in the finite range up to `v` need checking** for
  each form; every one of the 29 forms has `v_2(B) <= 3`, so the finite
  range needed is fully covered by the already-verified `j=4,5,6` (script
  below checks `j=4..max(v,6)` directly, i.e. re-derives the existing
  verification and extends the valuation argument past it).

**Result: none of the 35 forms is ever a power of two, for any `j>=4`.**
Verified computationally (exact integer arithmetic, no floating point in the
final check):

```
python3 -c "... see commit for the exact script ..."
# ALL 35 FORMS SAFE FOR ALL j>=4: True
```

## What this does and does not establish

**Established, rigorously:** *if* the 35 reported forms are the complete
list of simple-cycle lengths in the bare core for every `j>=4` (all valid
`a,c`), *then* the bare core avoids every dyadic cycle length for every
`j>=4`, not just the tested `j=4,5,6` — a genuine symbolic all-`j`
certificate, replacing what was previously only an empirical `j=4,5,6`
check.

## Completeness, proved (`verifier/type_t_port_kernel_cycle_space.py`)

The repository's existing computation checked exactly `j=4,5,6` (27 cores:
9 `(a,c)` combinations per `j`) and found 61 cycles / 35 forms in every one,
with no `a,c`-dependence in the affine coefficients observed. That alone
would only be strong evidence, not a proof, that no 36th form appears at
some untested `j` or `(a,c)`. This session closed the gap with an
independent, purely topological derivation:

`build_core` always wires the same 13 anchor vertices via the same 19
named subdivided paths; only 4 of the 19 path *lengths* depend on
`j`/`a`/`c` — the topology never changes. Two anchors, `u_x` and `u_y`, are
themselves degree-2 pass-through points (confirmed directly against a built
core: `verify_u_bridge_suppression`); suppressing them merges their two
incident length-1 paths each into one length-2 kernel edge, giving the true
**kernel multigraph: 11 vertices, 17 edges, cyclomatic rank exactly 7**
(`17-11+1=7`, matching the documented `m0-n0+1=7` exactly).

**Reconciling 13 anchors / 19 paths with 11 kernel vertices / 17 kernel
edges** (`verify_degree_distribution_reconciliation`,
`cross_validate_kernel_topology` — the latter re-derives the kernel a
*second*, fully independent way, by raw degree computation and generic
degree-2-chain suppression directly on a materialized `build_core` graph,
with no reference to the hand-transcribed `KERNEL_EDGES` table or to
`coordinates.py::PATH_SPEC`, and checks it agrees exactly — vertex set, edge
endpoints, *and* numeric lengths — with the hand-transcribed kernel across 9
distinct `(j,a,c)` instances spanning `j=4,5,6` with extreme and interior
`a,c`):

* Of the 13 named anchors, exactly one (`z0`) has degree 4 and ten have
  degree 3 — these 11 are exactly the kernel vertices, and
  `sum(d(v)-2) = (4-2)*1 + (3-2)*10 = 12`, matching the documented value
  exactly. The remaining two anchors, `u_x` and `u_y`, have degree 2 — they
  are not branch points at all, just named waypoints, so they belong inside
  the documented `n2=5Y-4` count (along with every ordinary path-internal
  vertex) rather than being one of the 11 kernel vertices.
* Suppressing `u_x` merges its two incident paths (`u_x_r_x`, `u_x_s_x`,
  each length 1) into a single length-2 kernel edge between `r_x` and `s_x`
  — running in parallel with the already-direct length-7 `A_middle` kernel
  edge between the same two vertices (likewise `u_y` merges `u_y_r_y` +
  `u_y_s_y` into a length-2 edge parallel to `C_middle`). That is exactly
  **2 of the 19 named paths becoming parallel companions of 2 others**, so
  19 paths collapse to 17 kernel edges — not 18 — consistent with the rank
  formula `E = V - 1 + r = 11 - 1 + 7 = 17` exactly (not merely `<=18`).

**Why the `a`/`c`-cancellation is forced by the kernel topology, not merely
observed** (proved once here, from the fixed kernel alone — this is the
formal version of task item 6, not an appeal to the 61-cycle enumeration
that also happens to confirm it): `r_x` and `s_x` each have kernel-degree
exactly 3, with incident edges `{A_left, A_middle, u_x_bridge}` at `r_x` and
`{A_middle, u_x_bridge, A_right}` at `s_x` — i.e. `A_left` is `r_x`'s *only*
connection away from the `r_x`-`s_x` pair, and `A_right` is `s_x`'s only
connection away from it (`A_middle`/`u_x_bridge` are the two parallel edges
directly between `r_x` and `s_x`). In any simple cycle, `r_x` (if used at
all) has support-degree exactly 2. Suppose a cycle uses `A_left`: `r_x`'s
second used edge must be `A_middle` or `u_x_bridge` (its only other
options), so the cycle continues into `s_x`. At `s_x`, one edge (whichever
of `A_middle`/`u_x_bridge` was just used) is already spent; `s_x` needs
exactly one more from its remaining two options — *the other*
`r_x`-`s_x` parallel edge, or `A_right`. Choosing the other parallel edge
would add a *second* `r_x`-`s_x` edge back at `r_x` — but `r_x` already has
its two allowed slots filled (`A_left` + the first parallel edge), so a
third edge there is forbidden for a simple cycle. That option is therefore
excluded, forcing `s_x`'s second edge to be `A_right`. Hence **`A_left` used
implies `A_right` used**, and by the symmetric argument (starting from
`A_right`) the converse holds too — so every simple cycle uses `A_left` and
`A_right` together or neither, and since `length(A_left)+length(A_right) =
(a-1)+(4Y-8-a) = 4Y-9` is itself `a`-free, the `a`-dependence cancels
identically, for every simple cycle, by this topological argument alone
(not by inspecting all 61 cycles case-by-case). The identical argument with
`r_y`, `s_y`, `C_left`, `C_right`, `u_y_bridge` (also all kernel-degree 3)
gives the matching `c`-cancellation
(`length(C_left)+length(C_right) = (c-1)+(Y-8-c) = Y-9`).

`type_t_port_kernel_cycle_space.py` builds this kernel directly from
`build_core`'s topology (no numeric fitting anywhere in the module), picks
a spanning tree, constructs its 7 fundamental cycles, and enumerates all
`2^7=128` binary cycle-space vectors. For each nonzero vector it decides —
from the *kernel's* abstract topology alone (connected edge-support, every
included vertex has degree exactly 2), a question with no dependence on
`j`/`a`/`c` whatsoever — whether it is a genuine simple cycle, and if so
computes that cycle's length **symbolically** as
`(const, Y_coef, a_coef, c_coef)` by summing the constituent kernel edges'
symbolic lengths (no plugging in of numbers at any point).

**Result:**
* **Exactly 61 valid simple cycles** — matching the documented count
  exactly, now derived rather than observed.
* **Every one of the 61 has `a_coef=0` and `c_coef=0`** — proving, not
  merely observing at 9 sampled `(a,c)` pairs, that every cycle's length is
  a pure function of `Y` alone (the `a`/`c` contributions from `A_left`/
  `A_right` resp. `C_left`/`C_right` always cancel exactly).
* The resulting 35 distinct `(Y_coef, const)` pairs, **with multiplicities**,
  are **exactly** the 35 forms independently fit from the `j=4,5,6` spectra
  in `type_t_port_core_affine_dyadic_check.py` — literal set equality, zero
  mismatches, checked by `self_test()` (also a pytest-covered regression:
  `tests/test_type_t_port_kernel_cycle_space.py`).

Because the kernel topology and the cycle-space classification are both
independent of `j`/`a`/`c` by construction (not sampled at finitely many
values), this **is** the completeness proof, not further evidence for it:
the 35 forms are the complete simple-cycle spectrum of `H(j,a,c)` for every
valid `j>=4` and every valid `a,c`, not just the tested combinations.

**Putting it together:** the 2-adic argument above (none of the 35 forms is
ever a power of two, for any `j>=4`) plus this completeness proof gives,
unconditionally: **`H(j,a,c)` contains no cycle of dyadic length, for every
valid `j>=4` and every valid `a,c`.**

## Strategic consequence

This closes the open precondition for an externally-proposed
"bounded-rank/finite-horizon completion theorem" (a lopsided-Lovász-Local-
Lemma argument, relayed into this session and independently audited by the
template-lifting agent for its *other* precondition — bounded max degree,
already PROVED there). With both preconditions now established, that
theorem concludes: **no fixed finite set of forbidden cycle lengths (in
particular `{4,8,16}`) can be forced by every sufficiently large exact-cover
completion of this family** — an all-`j` proof via a fixed short-cycle
catalog is structurally impossible for this specific construction, not just
empirically hard. This makes the strategic pivot both prior agents already
leaned toward — deprioritize fixed-template global forcing; look at
growing-length obstructions or explicit periodic-completion constructions
instead — not just prudent but *necessary* for this family, conditional
only on the external LLL argument's own proof holding up under further
scrutiny (that proof itself, as pure probability theory, has not been
independently re-derived in this repository).
