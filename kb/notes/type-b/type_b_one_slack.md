# One-slack `Pi0` bridges: exact reduction and open layer

**Status.** This file gives a hand-written one-slack reduction and a
computer-assisted exhaustive elimination of the extremal edge layer. It does
not classify the remaining near-extremal layer, so it is not a complete
20-vertex bridge census. No proof-assistant formalization exists.

## 1. Geometry forced at bridge order 20

Let `B` be either `Pi0` bridge role with `|V(B)|=20`. Let `x,y` be its
terminals, `a` the unique neighbour of `x`, and `P` a required length-18
`x-y` path. Since `P` has 19 vertices, there is exactly one vertex `z` of `B`
outside `P`. This statement does not claim that `z` avoids the other required
paths; it may lie on any of them.

Put `R=B-x`. The path `P-x` has length 17 and covers 18 vertices of the
19-vertex graph `R`; `z` is its unique off-path vertex. The closure `B+xy` is
2-connected, so deleting `x` leaves `R` connected. The endpoints of the
distinguished path are `a,y`.

The vertex `z` is internal, hence all of its neighbours lie on `P-x` and
`|N_R(z)|>=3`. If the distinguished path is

\[
 p_0p_1\cdots p_{17},
\]

then two attachments `zp_i,zp_j` create a cycle of length `|i-j|+2`.
Consequently attachment distances 2, 6, and 14 are forbidden by C4, C8, and
C16. A chord `p_ip_j` creates a cycle of length `|i-j|+1`, so chord distances
3, 7, and 15 are forbidden. These are necessary single-edge conditions, not a
complete multi-chord classification.

## 2. Exact degree and size range

In `R`, the seventeen ordinary internal vertices have degree at least three.
The gateway `a` loses `xa` and has degree at least two. The same local path
arguments as B19 give `d_R(y)>=2`. Thus

\[
 2|E(R)|\ge17\cdot3+2\cdot2=55,
 \qquad |E(R)|\ge28.
\]

Since `R` is C4/C8-free and `ex(19;{C4,C8})=29`, only 28 and 29 edges are
possible.

| `|E(R)|` | possible graph-level degree sequences under the lower bounds | degree-two vertices | status |
|---:|---|---:|---|
| 28 | `2,3^18` or `2^2,3^16,4` | 1 or 2 | unresolved near-extremal layer |
| 29 | `2,3^17,5`; `2,3^16,4^2`; `2^2,3^16,6`; `2^2,3^15,4,5`; or `2^2,3^14,4^3` (the no-degree-two case would be `3^18,4`) | at most 2 | eliminated below |

Each bridge has `|E(B)|=|E(R)|+1`, so a full order-38 pair would have between

\[
 (28+1)+(28+1)+1=59
\]

and

\[
 (29+1)+(29+1)+1=61
\]

edges. This is much sharper than the global upper bound 70. T9B is not used in
this range calculation.

## 3. The 29-edge layer

McKay's complete order-19 extremal input
`data/c48_n19e29.s6` contains 304 nonisomorphic C4/C8-free graphs and has
SHA-256

```text
bf81b89b826ae3153c7497addb26025796b982a52a5e39210754f15620226562
```

A fresh exact audit gives:

| degree-two vertices | 3 | 4 | 5 | 6 | 7 | 8 |
|---:|---:|---:|---:|---:|---:|---:|
| graphs | 9 | 61 | 122 | 92 | 19 | 1 |

Every extremal graph has at least three degree-two vertices, contradicting the
one-slack bound of at most two. Two C4 detectors and two C8 detectors agree on
all 304 records. Hence the entire 29-edge layer is eliminated.

## 4. Exact unresolved computation

The sole remaining graph layer is:

```text
connected simple graphs on 19 vertices,
28 edges,
degree sequence 2,3^18 or 2^2,3^16,4,
C4/C8-free,
with distinguished endpoint roles and the required paths still to filter.
```

A broad command

```text
geng -c -q -f -d2 -D4 19 28:28 | .build/check_c8
```

was attempted for about six minutes and stopped without completion. It is not
used as evidence and supplies no absence claim. A complete run should filter
the two exact degree sequences as early as possible, preserve every survivor,
then test C16, distinguished paths, full terminal spectra, closure
2-connectivity, and T9B. No order-38 pairing claim is made yet.
