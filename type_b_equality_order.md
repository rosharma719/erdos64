# Minimum-order realizability of the smallest Type-B tuple

**Result.** The smallest tuple

\[
 \Pi_0=(2,2,4,4,1,1)
\]

has no Type-B realization at its minimum possible full order 36. The reduction
to two finite order-18 edge layers is a hand-written proof. Exhaustion of those
layers is a computer-assisted exhaustive finite computation, independently
generated and checked as described below. This is not proof-assistant formal
verification. It does not exclude order 37 or any larger order.

This argument supersedes the need to repeat the prior fixed-template solve. It
does not assume that template, a one-cell path intersection, a canonical
Balaban witness, T9B, or any conjectural SPQR property.

## 1. Exact path data and equality conditions

Write the cut terminals as `x,y`. In each Type-B bridge, `x` has bridge degree
one; call its unique neighbour `z_i`. Every required terminal path therefore
starts with `xz_i`.

| bridge | required `x-y` path lengths | suffix data after deleting `x` |
|---|---|---|
| `B1` | `2,17,18` | `z_1-y` lengths `1,16,17`; the length-1 suffix is `z_1y` |
| `B2` | `4,5,17,18` | `z_2-y` lengths `3,4,16,17`; the length-3/4 theta suffixes are internally disjoint |

The precise equality audit is:

| inequality | reason | slack | equality condition | path consequence |
|---|---|---|---|---|
| `n_i >= 19` | a simple length-18 path uses 19 vertices | `sigma_i=n_i-19` | `sigma_i=0` | the length-18 path is Hamiltonian in `B_i` |
| `n_G=n_1+n_2-2 >= 36` | bridge interiors are disjoint and only `x,y` are shared | `sigma_1+sigma_2` | both slacks zero | both bridges have order 19 |
| `|V(H_i)|=18` for `H_i=B_i-x` | delete the unique degree-one terminal | none at equality | automatic | the Hamiltonian path loses `xz_i` and becomes a Hamiltonian `z_i-y` path |
| `2|E(H_i)| >= 16*3+2*2=52` | sixteen non-gateway internal vertices retain degree at least 3; `z_i,y` have degree at least 2 | `tau_i=2|E(H_i)|-52` | `tau_i=0` | degree sequence `3^16,2^2` |
| `|E(H_i)| <= ex(18;{C4,C8})=27` | McKay's certified extremal value | `eta_i=27-|E(H_i)|` | `eta_i in {0,1}` | only the 26- and 27-edge layers can occur |

The degree claim at `z_i` is immediate: it is internal in `B_i`, so it has
degree at least three and loses only `xz_i`. For `B1`, `y` is incident with
`z_1y` and with the distinct last edge of the Hamiltonian suffix. For `B2`,
the internally disjoint length-3 and length-4 theta suffixes enter `y` through
distinct neighbours. Hence `d_{H_i}(y)>=2` in both cases.

This accounts for every possible path overlap. Shared prefixes, shared
suffixes, divergence cells, repeated segment incidences, and extra branch
vertices cannot change the Hamiltonicity or degree calculation. They therefore
do not create another equality case outside the two edge layers.

## 2. E36: finite equality reduction

**E36 [HAND-WRITTEN PROOF].** If a Type-B realization of `Pi0` has order 36,
then for each bridge the graph `H_i=B_i-x` is a connected simple graph with:

- order 18;
- size 26 or 27;
- no `C4` or `C8`;
- sixteen vertices of degree at least three;
- at most two vertices of degree two and no lower degree.

Conversely, every required-path topology extendable to a valid order-36 bridge
must occur inside one of these `H_i`. Thus exhausting the two `H` layers
exhausts all embeddings at once. Finiteness is mathematical: there are only
`2^153` labeled simple graphs on 18 vertices, and the fixed order, two fixed
edge counts, degree conditions, and terminal roles define a finite subset.
Program termination is not used as the finiteness proof.

The literal family of naked path unions is nonempty—the earlier certificate
contains examples—and is not being declared empty. The family of equality
path unions **extendable to a bridge satisfying the proved degree and cycle
conditions** is what E36 classifies. The layer exhaustion below proves that
extendable family empty before weighted-topology enumeration is needed.

## 3. Exhausting 26 edges

At 26 edges the degree-sum inequality is equality, so the degree sequence is
exactly `3^16,2^2`. The command

```text
geng -c -q -f -d2 -D3 18 26:26
```

generates precisely all connected simple C4-free graphs in that layer. It
produces 101,546 graphs. Every one contains a C8. The audit regenerates the
entire stream twice: once for the repository's rooted exact DFS detector and
once for NetworkX's unrelated `simple_cycles` implementation. Both runs see
the same 101,546 graph6 records, the same stream checksum, and zero C8-free
graphs.

This is an exhaustive finite computation. No absence inference is made beyond
the stated order, edge count, connectivity, and degree sequence.

## 4. Exhausting 27 edges

The authoritative input `data/c48_n18e27.s6` is McKay's complete list of all
570 extremal `{C4,C8}`-free graphs at order 18 and size 27. Its SHA-256 is

```text
c21bfccdc139f3abac60141b886423fb4daa88dc05fa084715a012dd04460359
```

The exact number of degree-two vertices has distribution:

| degree-two vertices | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| graphs | 18 | 103 | 220 | 187 | 39 | 2 | 1 |

Every graph has at least three degree-two vertices, whereas E36 permits at
most two. Hence this layer has zero candidate remainders.

The file is canonicalized with nauty and audited independently of the original
degree calculation. Exact DFS/common-neighbour C4 checks and exact
DFS/NetworkX C8 checks agree on all 570 graphs, and a fresh NetworkX degree
pass produces the displayed histogram. A local sharded `geng -D5`
regeneration was attempted for roughly ten minutes but not completed; it
produced no final shard and is not used in the conclusion. Completeness of the
27-edge layer is therefore the existing public McKay extremal-data result,
while every property used here is locally recomputed from the restored,
checksummed input.

## 5. Size equality and saturation

The old general bound `|E(G)|>=55` need not be equality at order 36. The
26-edge remainder layer is impossible, so a hypothetical order-36 realization
would require both remainders to have 27 edges. Since each bridge adds its one
edge `xz_i` and the full graph adds `xy`, it would have exactly

\[
 27+1+27+1+1=57
\]

edges. Thus the proposed 55-edge perfect-matching saturation case never
arises. The contradiction already occurs before completion edges, terminal
spectrum expansion, closure 2-connectivity, T9B protection types, C16, or C32
need to be tested. Adding those conditions can only shrink the empty set.

## 6. Scope and reproducibility

The certificate and manifest record the exact inputs, generator commands,
canonical set checks, source and output hashes, versions, and completed range:

- `verifier/type_b_equality_order.py`;
- `data/type_b_equality_order_certificate.json`;
- `manifests/type_b_equality_order_manifest.json`.

The conclusion is narrow: `Pi0` is eliminated only at full order 36. No
one-vertex-slack family is started here, and no later tuple is examined.

a proof that no realization of \(\Pi_0\) exists at order 36
