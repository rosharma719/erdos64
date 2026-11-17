# Joint minimality: WRP implies Conjecture T

**16 November 2026. Status: PROVED-DRAFT (author: Claude). Not yet reviewed by
ChatGPT; a blind re-derivation is requested in pass XIII.** It builds on Part A
of `decomposition_lemma.md` (ChatGPT, pass XII, reviewed by Claude).

## The point

`decomposition_lemma.md` reduces a smallest clean 3-pole outside T's list to
WRP only when its capped graph is 3-edge-connected. Its bridge and 2-edge-cut
cases were left open, because the far side of such a cut is a clean 1-pole or
2-pole, objects T says nothing about.

**Fix: take the minimal counterexample over 1-, 2- and 3-poles at once.** Then
the far side of a bridge or 2-edge cut is a *smaller* counterexample of another
kind, which minimality forbids. The open cases disappear.

## Definitions

A **clean k-pole** is a connected simple graph with exactly `k` vertices of
degree 2, all others of degree 3, and no cycle of length 4, 8, 16, …

Let `L = {T, S, U, H}`: the triangle, skew H7, uniform H7 and H15.

> **Conjecture T\*.** (i) There is no clean 1-pole. (ii) There is no clean
> 2-pole. (iii) Every clean 3-pole is in `L`.

(iii) is Conjecture T. **WRP** is as stated in `decomposition_lemma.md`, Part D
(letters `I, T, S, U, H`).

## Theorem

**WRP ⇒ T\*.** In particular WRP ⇒ T ⇒ Erdős–Gyárfás for all cubic graphs.

## Proof

Suppose T\* fails. Among all clean 1-, 2- and 3-poles that violate it (any
1-pole, any 2-pole, any 3-pole outside `L`), choose one, `P`, of smallest
order.

### Step 1: `P` is not a 1-pole

Let `r` be its degree-2 vertex, with neighbours `a ≠ b`. In `P − r`, the
vertices `a` and `b` have degree 2 and all others degree 3, and every cycle is
a cycle of `P`.

- If `P − r` is connected, it is a clean 2-pole on fewer vertices.
- Otherwise every component contains `a` or `b`, since `P` is connected. The
  component containing `a` (and not `b`) is a clean 1-pole on fewer vertices.

Either way minimality fails.

### Step 2: `P` is not a 2-pole

Let `u, w` be its degree-2 vertices.

**Case `u ≁ w`.** Let `a, b` be the neighbours of `u`. Neither is `w`, so both
have degree 3 in `P`. In `P − u`, the vertices `a, b, w` have degree 2 and all
others degree 3.

- If `P − u` is disconnected, each component contains `a` or `b`, and has one
  or two degree-2 vertices: a smaller clean 1-pole or 2-pole. Contradiction.
- If `P − u` is connected, it is a smaller clean 3-pole, so `P − u = X ∈ L`
  with ports `a, b, w`. The cycles of `P` through `u` have lengths
  `2 + P_X(a, b)`, where `P_X(a, b)` is the set of `a`–`b` path lengths in `X`.
  For every `X ∈ L` and every port pair this set contains a power of two:

  | X | port-pair path sets | plus 2 | contains |
  |---|---|---|---|
  | T | [1,2] | [3,4] | 4 |
  | S | [2,6], [2,6], [3,6] | [4,8], [4,8], [5,8] | 4 or 8 |
  | U | [2,6] ×3 | [4,8] | 4, 8 |
  | H | [3,14], [3,14], [5,14] | [5,16], [5,16], [7,16] | 8, 16 |

  So `P` is not clean. Contradiction.

**Case `u ~ w`.** Let `a` be the other neighbour of `u` and `b` the other
neighbour of `w`.

- If `a ≠ b`: in `P − {u, w}` the vertices `a, b` have degree 2 and all others
  degree 3. It is a smaller clean 2-pole if connected; otherwise each component
  is a smaller clean 1-pole. Contradiction.
- If `a = b`: `a u w` is a triangle, and `a` has one further neighbour `c`.
  `P − {u, w, a}` is connected, because every path from it to the triangle
  passes through `c`. In it `c` has degree 2 and all others degree 3, so it is
  a smaller clean 1-pole. It is nonempty, because `c` has degree 3 in `P`.
  Contradiction.

### Step 3: the cap of `P` is 3-edge-connected

Now `P` is a 3-pole outside `L`. Let `H = P + v`, where `v` is joined to the
three degree-2 vertices; `H` is cubic and connected. For an edge cut `δ(S)` of
`H` with `v ∉ S`, the graph `H[S]` lies inside `P`, so its cycles are cycles of
`P`. Also `S ≠ V(P)`, because `δ(V(P)) = δ({v})` has three edges.

- **No bridge.** If `δ(S) = {e}`, then `H[S]` is connected, its endpoint of `e`
  has degree 2, and all others degree 3: a smaller clean 1-pole.
- **No 2-edge cut.** Let `δ(S) = {e, f}`, with `H` bridgeless.
  - If `e, f` have distinct endpoints `x, y` in `S`, then `H[S]` is connected,
    since a component with at most one boundary edge would give a bridge. So
    `H[S]` is a smaller clean 2-pole.
  - If they share an endpoint `x`, then `x` has one neighbour in `S`, so
    `δ(S − x)` is a single edge: a bridge. `S − x` is nonempty, because `x`
    has degree 3. Excluded above.

Hence `H` is 3-edge-connected.

### Step 4: reduction to WRP

Apply Part A of `decomposition_lemma.md` to `P`. Each nontrivial cyclic 3-edge
cut away from `v` has a far side that is a smaller clean 3-pole, hence in `L`
by minimality of `P` within T\*. Contracting all of them gives a cyclically
4-edge-connected cubic base `B` with root `v`, and `P` is `B − v` with letters
from `{I, T, S, U, H}` substituted. `B ≠ K4` by the 35-case table
(`tower_theorem.md`). WRP then gives a cycle of `B − v` whose lifted window
contains a power of two. That is a power-of-two cycle in `P`, a contradiction. ∎

## Consequences

1. **The decomposition route is complete.** On route R1 the only open node is
   now **WRP itself**.
2. **Conjecture T\*(ii) alone also implies the cubic conjecture.** In a
   connected cubic counterexample, delete an edge lying on a cycle. The rest is
   connected, its two endpoints have degree 2, and it has no power-of-two cycle:
   a clean 2-pole. T\*(ii) is a statement with an empty list.
3. **Evidence for T\*.**
   - (ii): no clean 2-pole on ≤ 20 vertices (certified census).
   - (iii): T's list is complete through 21 vertices (certified census).
   - (i): Step 1 turns a clean 1-pole on `N` vertices into a clean 1-pole or
     2-pole on fewer, so the 2-pole census leaves no clean 1-pole on ≤ 21
     vertices. Doubling a clean 1-pole by an edge gives a cubic counterexample,
     so the published bound for cubic graphs through 48 vertices independently
     excludes clean 1-poles on ≤ 24 vertices.

## What to check

- Every "smaller" claim: each piece is a proper subgraph of `P`, so it has
  fewer vertices.
- Connectivity in every case, especially the `a = b` case of Step 2.
- Step 4 uses Part A unchanged, with `L` including `U`.
- The cap test in Step 2 uses only the four port-pair profiles, which the
  tower verifiers and `identify_three_poles.py` both reproduce.
