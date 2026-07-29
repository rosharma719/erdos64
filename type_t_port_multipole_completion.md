# Type-T port cores: minimum cubic multipole completion

## Status

This run establishes the minimum-order normal form, exhaustively computes the
single-hub compatibility hypergraphs, and implements the requested unlabelled
exact-cover/cycle-cut formulation.  It does **not** close the minimum cubic
multipole class: all three bounded `j=4` exact runs ended `UNKNOWN`, and no
power-of-two-cycle-free completion was found.  The strongest survivors are
`C4,C8`-free but contain many `C16`s.

The distinction is important.  The retained frontier CNFs contain every cut
learned so far, but their satisfiability is unresolved; they are continuation
points, not UNSAT certificates.

## Minimum-order normal form

Let `D` be the intrinsic set of degree-two vertices of the expanded core.
Every vertex of `D` needs one new incidence, and

```text
|D| = 5*2^j - 4.
```

Suppose `t` new vertices are introduced, every new vertex has degree three,
and `e` edges have both endpoints among the new vertices.  The new vertices
receive `|D|` incidences from the core and `2e` incidences from internal edges.
Summing their degrees proves

```text
3t = |D| + 2e.                                      (1)
```

This is a theorem about the minimum-order all-new-vertices-cubic completion
class.  It is not a classification of every possible added-vertex completion.

Modulo three, `2^j` is `(-1)^j`.  Hence `|D|` is zero modulo three for odd `j`
and one modulo three for even `j`.  Minimizing `t` in (1), equivalently using
the least nonnegative admissible `e`, gives:

* odd `j`: `e=0`, `t=|D|/3`; every new vertex has three core neighbours, so
  `D` is partitioned into triples;
* even `j`: `e=1`, `t=(|D|+2)/3`; the endpoints of the unique new-new edge
  each have two core neighbours, while every other new vertex has three.

Thus `j=4` has 24 triple hubs and two linked double hubs (`t=26`, order 113),
while `j=5` has 52 triple hubs and no new-new edge (`t=52`, order 219).

## Single-hub compatibility

A hub gives a length-two route between any two attachments.  For every pair
of deficient vertices the verifier enumerates every simple core path at
lengths `2^k-2`; the pair is safe exactly when none exists.  For the opposite
sides of the linked `j=4` gadget it analogously enumerates paths at lengths
`2^k-3`, because that route has length three.

Allowed triples are triangles of the resulting safe-pair graph.  Maximum safe
attachment size is computed exactly.  Contrary to the proposed strengthening,
safe sets of size four do exist; a core-only-neighbour hub is therefore not
forced to have degree at most three by this test.

| `(j,a,c)` | safe pairs | allowed triples | triple degree min--max | maximum safe set | linked gadgets | local cover |
|---|---:|---:|---:|---:|---:|---|
| `(4,2,2)` | 652 | 925 | 6--99 | 6 | 3,037 | SAT |
| `(4,28,4)` | 776 | 1,225 | 13--101 | 5 | 4,371 | SAT |
| `(4,55,7)` | 623 | 784 | 5--81 | 5 | 2,755 | SAT |
| `(5,2,2)` | 6,193 | 79,185 | 498--2,536 | 11 | not applicable | SAT |

Each safe-pair graph is connected.  PySAT finds an exact cover in all four
cases.  Single-worker CP-SAT independently returns `OPTIMAL` for the three
`j=4` covers; its 30-second `j=5` confirmation ends `UNKNOWN`, while the
explicit PySAT `j=5` cover remains a directly checkable witness.  Consequently
there is no single-hub, component, or elementary Hall obstruction in these
instances.

## Exact-cover and cycle-cut model

There is one primary Boolean variable per allowed triple, not per labelled
hub.  For even `j` there is additionally one variable per locally safe
unordered pair of linked attachment pairs.  Exact-one constraints cover every
deficient vertex, and exactly one linked gadget is selected for `j=4`.

For every SAT model the verifier materializes the ordinary graph, checks
simplicity, connectedness, order, and minimum degree, and searches
shortest-first for `C4,C8,C16,C32,C64` (and `C128` at order 219).  A witnessed
cycle yields the clause negating precisely the selected unlabelled gadgets
used by that cycle.  This clause is sound because those same gadgets and core
edges recreate the literal cycle in every extension.

An independent checker rebuilds each gadget set and finds the claimed cycle
as an edge plus a simple path, a different search organization from the CEGAR
enumerator.  It checked every retained cut, not merely samples.

| `j=4` core | exact models | learned cuts | shortest `C8` models | shortest `C16` models | cumulative seconds | result |
|---|---:|---:|---:|---:|---:|---|
| `(2,2)` | 691 | 9,169 | 680 | 11 | 301.10 | UNKNOWN |
| `(28,4)` | 2,092 | 49,018 | 2,019 | 73 | 301.21 | UNKNOWN |
| `(55,7)` | 8 | 105 | 8 | 0 | 180.01 | UNKNOWN |

The cut supports have sizes one through five.  Unit cuts occur (7, 15, and 1,
respectively), proving that some locally pair-compatible linked gadgets are
globally invalid by themselves.  Most cuts use two to four hubs, so the first
visible obstruction layer is bounded hub interaction, but the current CNFs do
not prove that this layer excludes every exact cover.

## Local-exchange near misses

Randomized exact covers were followed by exact-cover-preserving exchanges of
two to four triple hubs.  Every reported zero was independently rechecked on
the materialized graph.

| core | steps | `C4` | `C8` | `C16` | interpretation |
|---|---:|---:|---:|---:|---|
| `j4_a2_c2` | 200,000 | 0 | 1 | not counted | one-eight-cycle near miss |
| `j4_a28_c4` | 200,000 | 0 | 0 | 927 | short-cycle-free through 8 |
| `j4_a55_c7` | 200,000 | 0 | 13 | not counted | bounded heuristic result |
| `j5_a2_c2` | 88 | 0 | 0 | 1,404 | short-cycle-free through 8 |

The `j=5` graph has order 219, is connected and simple, and has minimum degree
three.  Independent witnesses confirm cycles of lengths 16, 32, 64, and 128,
so it is a strong near miss rather than a counterexample.

## What the run proves and does not prove

It proves the minimum-order normal form and the reported finite compatibility
data.  It also proves that local exact covers exist, that safe attachment sets
can exceed size three, and that every retained cycle-cut clause is sound.

It does not prove any of the three `j=4` instances UNSAT, does not prove a
universal bounded-hub theorem, and does not produce a counterexample.  The
next useful computation is continuation from the retained frontier clauses,
preferably with the `C4,C8`-free partitions supplied as SAT phases, followed by
focused `C16` cut generation.  Repeating the raw compatibility screen would
add little.

## Reproduction

```bash
PYTHONPATH=verifier python verifier/type_t_port_triples.py \
  --j 4 --a 2 --c 2 --include-catalog

PYTHONPATH=verifier python verifier/type_t_port_multipole_check.py \
  data/type_t_port_multipole/j4_a2_c2_exact.json.gz

PYTHONPATH=verifier python verifier/type_t_port_multipole_check.py \
  data/type_t_port_multipole/j5_a2_c2_local.json
```

To continue an exact frontier without replaying learned models:

```bash
PYTHONPATH=verifier python verifier/type_t_port_multipole_sat.py \
  --j 4 --a 28 --c 4 --max-seconds 300 --cycle-limit 2000 \
  --resume data/type_t_port_multipole/j4_a28_c4_exact.json.gz \
  --phase-completion data/type_t_port_multipole/j4_a28_c4_local.json \
  --output /tmp/j4_a28_c4_next.json.gz --cnf /tmp/j4_a28_c4_next.cnf.gz
```

`Q` is not used anywhere in the construction or independent verification.
