# Bridge spectrum and star-closure lemmas

## 1. Exact bridge-spectrum correspondence

Let `H` be a finite simple graph and let `e=ab` and `f=cd` be distinct edges. Form `G=B(H;e,f)` by deleting `e,f`, introducing new vertices `x,y`, and adding

`ax, bx, xy, cy, dy`.

Thus `G` is obtained from `H` by bridging `e` and `f`.

### Theorem 1 (bridge-spectrum theorem)

The simple cycles of `G` are exactly the following.

1. **Cycles avoiding `xy`.** For every simple cycle `C` of `H`, replace each occurrence of `e` and `f` by its two-edge subdivided route. The resulting cycle has length

   `|C| + |E(C) ∩ {e,f}|`.

2. **Cycles using `xy`.** Choose one endpoint of `e`, one endpoint of `f`, and a simple path `P` between them in `H-{e,f}`. Adding the three gadget edges from the first endpoint to `x`, across `xy`, and from `y` to the second endpoint gives a simple cycle of length

   `|P|+3`.

These correspondences are bijective.

### Proof

Let `C'` be a simple cycle of `G`.

If `xy` is absent from `C'`, then whenever `C'` contains `x`, it must use both `ax` and `bx`; replacing `a-x-b` by `ab` preserves simplicity. The same applies to `y`. This yields a unique simple cycle `C` of `H`, and each replaced edge decreases the length by one.

If `xy` is present, the cycle uses exactly one of `ax,bx` and exactly one of `cy,dy`. Deleting `x,y` and those three gadget edges leaves a simple path in `H-{e,f}` between the selected endpoints. The converse constructions are immediate. □

### Corollary 1.1 (exact dyadic sterility conditions)

`G` has no power-of-two cycle if and only if all four conditions hold in `H`:

1. no cycle of length `2^k` avoids both `e,f`;
2. no cycle of length `2^k-1` uses exactly one of `e,f`;
3. no cycle of length `2^k-2` uses both `e,f`;
4. no cross-endpoint path in `H-{e,f}` has length `2^k-3`.

This is an equivalence, rather than only a necessary condition.

### Corollary 1.2 (spread strengthening for a C4-free bridge)

If `G=B(H;e,f)` is `C4`-free and `H` is 2-connected, then the cycle spread of `e,f` is at least `(2,2)`.

Indeed, a cross-endpoint path of length one in `H-{e,f}` would produce a four-cycle through `xy` in `G`.

Combined with the Wormald–Kingan unbridging theorem, every cyclically 4-connected cubic counterexample other than the standard base graphs has a smaller cyclically 4-connected cubic predecessor and a bridged edge pair of cycle spread at least `(2,2)` satisfying all four sterility conditions above. This is the exact induction target for the cyclically 4-connected cubic case.

---

## 2. Star closure at an independent neighborhood

Let `G` be a globally minimal counterexample. Let `v` have degree at least three and suppose `N(v)` is independent.

For each `x in N(v)`, form

`H_x = G-v + {xy : y in N(v)\{x}}`.

Because vertices of degree at least four form an independent set in a minimal counterexample, every neighbor of a high-degree `v` is cubic. After deleting `v`, every such neighbor has degree two. The added star restores every leaf to degree three and raises the center above degree three. Thus `delta(H_x)>=3`, and `H_x` has smaller order.

### Theorem 2 (star-closure Mersenne saturation)

For every `x in N(v)`, there is some `y in N(v)\{x}` and a simple `x-y` path in `G-v` of length `2^k-1`. Equivalently, every incident edge `vx` lies on a cycle of length `2^k+1`.

### Proof

Minimality forces a power-of-two cycle `C` in `H_x`.

- `C` cannot use zero added star edges, since it would already occur in `G`.
- A simple cycle can use at most two star edges, because all added edges meet `x`.
- If it uses two, they occur as a two-edge subpath `y-x-z`. Replacing that subpath by `y-v-z` gives a simple cycle of the same power-of-two length in `G`, impossible.

Therefore `C` uses exactly one added edge `xy`. Removing it leaves an `x-y` path in `G-v` of length `2^k-1`; inserting `x-v-y` gives a cycle of length `2^k+1` containing `vx`. □

### Consequences

1. At every vertex with independent neighborhood, all incident edges are Mersenne-witnessed.
2. For such a vertex `v`, define a witness graph on `N(v)` by joining `x` to one partner `y` supplied by `H_x`. This witness graph has minimum degree at least one, and each edge carries a label `k` and an external path of length `2^k-1` in `G-v`.
3. If two adjacent witness edges have the same label and their external paths meet only at their common endpoint, their union with the two-edge route through `v` gives a cycle of length `2^(k+1)`. Hence equal-label adjacent witnesses must reintersect.

The remaining high-degree problem is therefore a labeled reintersection problem, parallel to the forked-theta obstruction already obtained at cubic triangles.
