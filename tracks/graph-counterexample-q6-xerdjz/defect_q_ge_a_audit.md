# Audit: is `q(G) >= a` (`a` = number of high-degree vertices) proven here?

## Answer: yes, already proven — cross-reference note

An external strategy document (pasted 2026-07-30) used the bound
`q(G)>=a` (writing `A` for the independent high-degree-vertex set, `a=|A|`)
to derive `|A|<=9` at `n=32` from `n=a+s+2q+4`, then flagged that
inequality as "not part of the presently summarized proved package,"
recommending the weaker fallback `|A|<=10` (from the two-thirds-cubic
theorem `G1`) until audited. This file is that audit.

**Finding: `q(G)>=a` is already proven**, in `defect.md`'s leaf-compression
Part I, stated as `h<=q` (the project's variable name for the high-degree
set is `H`/`h`, not `A`/`a` — same object, different letter, which is why a
literal grep for "`q>=a`" or "`n=a+s+2q+4`" found nothing on the first
pass). See `defect.md`:

> **Weak corollary, all `h` [PROVED].** ... `h<=q` ... holds for every
> `h>=0`, but by two different mechanisms: a trivial corollary of G2 at
> `h in {0,1}`, and a genuine consequence of the leaf-graph 2-degeneracy
> bound at `h>=2`.

**Proof sketch** (full detail in `defect.md`'s leaf-compression Part I):
build the derived leaf graph `L(G)` on vertex set `H` (one edge per
degree-3 "leaf" vertex with exactly two `H`-neighbours); `L1` proves `L` is
simple with `|E(L)|=c_1` exactly (a C4-freeness argument: two leaves
sharing the same `H`-neighbour pair would close a literal `C4` in `G`);
`L4` proves `L` is 2-degenerate (else a smaller counterexample would exist,
contradicting order-minimality), giving the standard bound
`|E(L)|<=2h-3` for `h>=2`; combined with the pure-algebra identity
`c_1=c_3+4h-2q-4` (`I.1`) and `c_3>=0`, this forces `h<=q`. For `h in{0,1}`
it follows trivially from the already-proven `q(G)>=1` (`G2`). This lemma
is already load-bearing elsewhere in the repo — it's the exact tool that
lets `P9` (`q>=2`) dispose of the `h>=2` case "immediately," leaving only
`h=0,1` to check by hand (see `proof.md`).

**Status labels** (as recorded in `defect.md`/`verification_status.md`):
the algebraic identity and the `L1`/`L2` mechanical facts are
computationally cross-validated (1,457 and 1,443+833 checks respectively,
0 failures); the `L4` 2-degeneracy step is a pure minimality argument, not
independently testable on real data (no small genuine counterexample
exists to test it on — same honest limitation as `S4`/`S5`/`G2` itself,
which this project has always stated plainly rather than hidden).

## Consequence: the stronger `n=32` bound is valid

With `q>=a` in hand, `n=a+s+2q+4 >= a+s+2a+4 = 3a+s+4 >= 3a+4` (`s>=0`).
At `n=32`: `32>=3a+4 => a<=28/3=9.33... => a<=9`.

**So `|A|<=9` (the original, stronger bound) is correct, not the
conservative `|A|<=10` fallback the roadmap suggested pending audit.** The
roadmap's caution was reasonable to raise given the claim wasn't easy to
locate on a first pass, but the audit resolves in favor of the original
number.
