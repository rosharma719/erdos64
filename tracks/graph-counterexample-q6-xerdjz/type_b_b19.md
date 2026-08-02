# The local 19-vertex bridge obstruction

**B19 [HAND-WRITTEN REDUCTION + PREVIOUS EXHAUSTIVE FINITE
CERTIFICATE].** Neither bridge role of the smallest tuple

\[
 \Pi_0=(2,2,4,4,1,1)
\]

can be realized by a 19-vertex bridge in a Type-B counterexample. This is a
local bridge theorem: the partner bridge and the total order are irrelevant.
The reduction is a hand-written proof; the two order-18 remainder layers were
eliminated by the computer-assisted exhaustive finite certificate already
frozen in `manifests/type_b_equality_order_manifest.json`. There is no
proof-assistant formalization.

## Dependency audit

Let `B` be either bridge role, with terminals `x,y`, and suppose `|V(B)|=19`.
The unique neighbour of `x` in `B` is denoted by `z` and `R=B-x`.

| property of the 19-vertex bridge | local bridge hypothesis used | global Type-B/counterexample hypothesis used | order-36 equality used | partner used |
|---|---|---|---|---|
| `d_B(x)=1` and unique gateway `z` | exact Type-B terminal profile | none | no | no |
| required length-18 `x-y` path | `18` belongs to the frozen forced spectrum in both bridge roles | none | no | no |
| that path is Hamiltonian in `B` | simple path uses 19 vertices and `|V(B)|=19` | none | no | no |
| `R` is connected on 18 vertices | delete the first edge `xz` from the Hamiltonian path | none | no | no |
| sixteen ordinary vertices of `R` have degree at least 3 | they are internal vertices of `B` not incident with deleted `xz` | ambient minimum degree three plus bridge separation | no | no |
| `d_R(z)>=2` | `z` is internal and loses only `xz` | ambient minimum degree three | no | no |
| `d_R(y)>=2` in the first role | forced edge `zy` and the distinct last edge of the Hamiltonian suffix | none | no | no |
| `d_R(y)>=2` in the second role | internally disjoint length-3/4 theta suffixes enter `y` through distinct neighbours | none | no | no |
| `|E(R)|>=26` | preceding local degree bounds | none | no | no |
| `R` has no `C4` or `C8` | subgraph inheritance | the ambient graph is power-cycle-free | no | no |
| `|E(R)|<=27` | none | known extremal value `ex(18;{C4,C8})=27` | no | no |
| 26 edges are impossible | exact degree sequence `3^16,2^2` | previous exhaustive 101,546-graph certificate | no | no |
| 27 edges are impossible | at most two degree-two vertices | complete checksummed 570-graph extremal certificate | no | no |

The phrases “ambient” and “global” in the table supply only properties inherited
by a single bridge: minimum degree of its internal vertices and absence of
power cycles. No cross-spectrum sum, partner spectrum, full-graph size, or
equality between bridge orders occurs.

## Proof of B19

The length-18 required path is Hamiltonian. Since `d_B(x)=1`, it starts with
`xz`, and deleting `x` leaves a Hamiltonian `z-y` path in `R`. Thus `R` is
connected and has order 18.

Besides `z`, exactly sixteen vertices of `R` are internal vertices unaffected
by deletion and have degree at least three. The table proves that `z` and `y`
each have degree at least two. Therefore

\[
 2|E(R)|\ge16\cdot3+2\cdot2=52,
 \qquad |E(R)|\ge26.
\]

As a subgraph of the ambient counterexample, `R` has neither a `C4` nor a
`C8`. The known extremal value gives `|E(R)|<=27`. The prior certificate
exhausts both remaining sizes: all 101,546 connected C4-free 26-edge graphs
with forced degree sequence `3^16,2^2` contain a C8, while every one of the 570
extremal 27-edge C4/C8-free graphs has at least three degree-two vertices.
Both contradict the derived properties of `R`. This proves B19 for either
bridge role.

## Global corollaries

Every `Pi0` Type-B realization must now satisfy

\[
 |V(B_1)|\ge20,\qquad |V(B_2)|\ge20,
\]

and therefore

\[
 |V(G)|=|V(B_1)|+|V(B_2)|-2\ge38.
\]

Order 36 is excluded by the previous theorem. Order 37 is excluded separately:
the integer equation `|V(B_1)|+|V(B_2)|-2=37`, together with the original
19-vertex lower bound, forces bridge orders `(19,20)` up to exchange, and B19
excludes the 19-vertex bridge.

This promotion adds no new computation and makes no claim about 20-vertex
bridges. It identifies order 38, with bridge orders `(20,20)`, as the next
case.

B19 proved locally and the global lower bound raised to 38
