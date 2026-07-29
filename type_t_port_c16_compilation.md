# Type-T port cores: static short-cycle compilation

## Status

For the fixed representative `(j,a,c)=(4,28,4)`, the complete static
`C4/C8` layer has been compiled and independently checked.  The `C16`
compiler replaces completion-by-completion cycle discovery with an AllSAT
projection of every simple 16-cycle in a universal gadget graph.  The current
bounded run has compiled 84,936 inclusion-minimal `C16` supports, but the
residual projection is still SAT and the catalog is therefore explicitly
marked incomplete.  This report does not claim an obstruction theorem or a
counterexample.

## Passage reduction and support bound

Contract a traversal through a new hub to a weighted passage.  Core edges
have weight one.  A passage through an ordinary hub, or through one side of
the linked gadget, has weight two.  A passage using the edge between the two
linked hubs has weight three.

Every two consecutive hub passages in a simple cycle are separated by at
least one core edge.  Thus a `C16` with `p` hub passages satisfies

```text
16 >= 2p + p,
```

and hence `p <= 5`.  An ordinary gadget can occur in only one passage.  The
linked gadget can occur in one same-side passage, one cross passage, or two
vertex-disjoint same-side passages, but still contributes only one selected
gadget variable.  Consequently every `C16` conflict has support size at most
five.  This proves the finite support bound used by the projection encoding.

The fixed core itself has no `C4`, `C8`, or `C16`; the compiler refuses to
construct a nonempty-support catalog if this premise fails.

## Exact `C4/C8` layer

The short-conflict compiler exhausts all simple core paths that can occur
between one or two hub passages.  Three passages require at least nine edges,
so a `C4` or `C8` uses at most two passages.  It handles both passages through
the same linked gadget as a unary support and otherwise enforces exact-cover
co-selectability.

For `(4,28,4)` it enumerates 579 relevant core paths and 286,011 literal
`C8`s.  There are no `C4` supports.  After inclusion minimization, the static
short layer contains 227,725 clauses: 371 unary and 227,354 binary.  Every one
of the 9,157 retained `C8` cuts from the earlier CEGAR run is covered, and the
saved `C4/C8`-free completion violates none of the static clauses.

Therefore models of

```text
Phi_4,8 = exact cover + all compiled C4/C8 conflicts
```

are exactly the minimum cubic completions of this core with no `C4` or `C8`.

## Universal `C16` projection

The universal graph contains the 87 core vertices, one hub for each of 1,225
allowed triples, and two hubs for each of 4,371 linked gadgets: 10,054
vertices and 25,623 edges in total.  Sixteen position blocks encode a simple
cycle.  Gadget projection variables are exact: a variable is true exactly
when one of its hub vertices occurs on the cycle.  The encoding also imposes:

* pairwise-disjoint attachment sets;
* at most one linked gadget;
* the support bound of five;
* all 227,725 `C4/C8` conflicts; and
* a canonical least-deficient-vertex position to remove rotations.

A second set of gadget variables carries the complete exact-cover CNF and all
of `Phi_4,8`, with every cycle-used gadget forced selected.  Thus the
production projection enumerates only supports that extend to an actual
`C4/C8`-free exact cover.  This removes irrelevant structural cycles without
weakening completeness for the target completion space.

Each SAT model emits the clause negating its projected gadget support, and
that support is blocked before the next model.  Previously discovered CEGAR
supports may seed the run, but they do not weaken completeness: every seed is
re-materialized and independently checked, and final completeness requires
the residual universal-cycle formula itself to be UNSAT.

One-gadget supports receive a separate exhaustive check over all 5,596
gadgets.  Exactly 608 linked gadgets create a `C16` alone; 39 are already
forbidden by `Phi_4,8`, leaving 569 minimal unary `C16` clauses.  No ordinary
triple is a unary `C16` support.

The current merged bounded catalog has this distribution:

| support size | minimal supports |
|---:|---:|
| 1 | 569 |
| 2 | 24,252 |
| 3 | 29,172 |
| 4 | 16,497 |
| 5 | 14,446 |
| **total** | **84,936** |

These clauses are all sound, but the catalog is not yet complete.

## Static solve and interpretation

The current static formula has 31,049 variables and 389,020 clauses:

| layer | clauses |
|---|---:|
| exact-cover base | 76,359 |
| complete `C4/C8` conflicts | 227,725 |
| current `C16` conflicts | 84,936 |

CaDiCaL and Lingeling both return SAT.  Independent reconstruction finds
`C16`, `C32`, and `C64` witnesses in that completion, so it is only a witness
that the bounded catalog has not reached exhaustion.  It is not a
`C16`-free completion.

MaxSAT is deliberately deferred until the `C16` catalog is complete.  On an
incomplete catalog, optimum zero merely reproduces the same missing-support
phenomenon and is not the requested invariant.

## Independent verification

The checker expanded all 84,936 stored supports into ordinary graphs and
found a fresh 16-cycle for each using the edge-plus-simple-path detector.  For
a catalog marked complete, it additionally rebuilds the positional
projection, blocks all short and `C16` supports, and requires a fresh
Lingeling run to return UNSAT.
Thus support soundness and projection exhaustion are checked separately.

## Reproduction

```bash
PYTHONPATH=verifier python verifier/type_t_port_short_conflicts.py \
  --j 4 --a 28 --c 4 \
  --output data/type_t_port_c16/j4_a28_c4_short_conflicts.json.gz

PYTHONPATH=verifier python verifier/type_t_port_c16_hypergraph.py \
  --j 4 --a 28 --c 4 --length 16 --seed-unary \
  --forbid-catalog data/type_t_port_c16/j4_a28_c4_short_conflicts.json.gz \
  --seed-cegar data/type_t_port_multipole/j4_a28_c4_exact.json.gz \
  --output data/type_t_port_c16/j4_a28_c4_c16_hypergraph.json.gz

PYTHONPATH=verifier python verifier/type_t_port_c16_static_sat.py \
  --j 4 --a 28 --c 4 \
  --short-catalog data/type_t_port_c16/j4_a28_c4_short_conflicts.json.gz \
  --c16-catalog data/type_t_port_c16/j4_a28_c4_c16_hypergraph.json.gz \
  --output data/type_t_port_c16/j4_a28_c4_static_sat.json

PYTHONPATH=verifier python verifier/type_t_port_c16_check.py \
  --j 4 --a 28 --c 4 \
  --short-catalog data/type_t_port_c16/j4_a28_c4_short_conflicts.json.gz \
  --c16-catalog data/type_t_port_c16/j4_a28_c4_c16_hypergraph.json.gz
```

The `complete` field in the `C16` catalog is the machine-readable boundary:
only `true`, backed by residual projection UNSAT, licenses the full static
claim.
