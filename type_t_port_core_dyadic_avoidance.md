# Bare-core dyadic-cycle avoidance for all j (2-adic argument)

**Status (2026-07-29): PROVED for the 35 reported affine forms, given
completeness; completeness itself is CERTIFIED for j=4,5,6 (matching the
repository's existing scope) and PLAUSIBLE-BUT-NOT-YET-FORMALLY-PROVED for
general j, pending the kernel/cycle-space argument delegated below.**

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

**Not yet independently re-derived here:** the completeness claim itself.
The repository's existing computation checked exactly `j=4,5,6` (27 cores:
9 `(a,c)` combinations per `j`) and found 61 cycles / 35 forms in every one,
which is why the spectrum could be fit with no `a,c`-dependence at all in
the affine coefficients — plausible because a full traverse of the growing
branches has `a`/`c`-independent length (`A_left+A_right=4Y-9`,
`C_left+C_right=Y-9`, the `a`/`c` terms cancel), suggesting every one of the
61 cycles either avoids a growing branch entirely or traverses it in full,
never partially — but this session has not independently verified that no
*36th* form appears at some untested `j` or `(a,c)`.

**Why completeness should be provable, not just observed:** the core has
cyclomatic rank exactly 7 (`type_t_port_completion.md` Section 1: `m0-n0+1=7`,
independently reconfirmed by `verifier/type_t_port_coordinates.py`'s kernel
audit), so its binary cycle space has exactly `2^7=128` elements, all
determined by a **13-anchor, 19-edge kernel multigraph whose topology never
changes with `j`, `a`, or `c`** (only 4 of the 19 edge/path lengths do). A
subset of kernel edges is a valid simple cycle exactly when it is one in
this fixed abstract multigraph — a purely topological question, answerable
once from the kernel alone, independent of `j`/`a`/`c` entirely. If that
classification yields exactly 35 realizable affine forms (some kernel edges
carry a `j`-dependent length, some don't), that already *is* the completeness
proof: not "checked at three values of `j`" but "true for every value of
`j`, `a`, `c` by construction." Formalizing this (build the kernel + cycle
space, enumerate the up to 127 nonzero vectors, classify each) is delegated
as a follow-on task, since it is exactly the machinery already partly built
by `verifier/type_t_port_coordinates.py` and can reuse it directly.

## Strategic consequence, conditional on completeness

If completeness is confirmed, this closes the open precondition for an
externally-proposed "bounded-rank/finite-horizon completion theorem" (a
lopsided-Lovász-Local-Lemma argument, relayed into this session and
independently audited by the template-lifting agent for its *other*
precondition — bounded max degree, which is already PROVED): the bare core
would avoid every dyadic length for every `j>=4`, which is exactly the
missing ingredient that theorem needs to conclude that **no fixed finite
set of forbidden cycle lengths (in particular `{4,8,16}`) can be forced by
every sufficiently large exact-cover completion of this family** — i.e. an
all-`j` proof via a fixed short-cycle catalog would be structurally
impossible for this specific construction, not just empirically hard. This
would mean the strategic pivot both prior agents already leaned toward
(deprioritize fixed-template global forcing; look at growing-length
obstructions or explicit periodic-completion constructions instead) is not
just prudent but *necessary* for this family. This conclusion is
conditional on (a) the completeness claim above and (b) the external LLL
argument's own proof holding up under independent scrutiny — neither is
treated as settled by this file alone.
