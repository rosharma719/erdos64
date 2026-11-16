# Research brief: reducing the power-of-two target to an additive one

**16 November 2026.** A plan, not a result. Written for whoever does the next
round of work, human or model. Builds on `three_port_classification.md` and
passes IV–XI in this directory.

## The bridge

If the achievable cycle lengths include every integer in `[x, 2x]`, one of
them is a power of two. If they include every even integer in `[x, 2x]` with
`x` even, the same holds, because powers of two from 4 up are even. So the
multiplicative target can be replaced by an additive one: **find a full
interval of lengths spanning a factor of 2.**

When a cycle passes through pieces whose port path lengths are intervals
`[a_v, b_v]`, its achievable lengths form one interval, and the factor-2
condition is the linear inequality

```
sum over the cycle of (b_v − 2 a_v − 1) ≥ 0.
```

That sum is additive along a cycle and over vertex-disjoint unions of
cycles. It is **not** linear over the binary cycle space: a symmetric
difference cancels shared edges. The averaging argument of
`cycle_space_obstruction.md` is still valid, because it averages this
real-valued score over the even subgraphs and then extracts one component
cycle.

**Caveats.** The condition is sufficient, not necessary: `[17, 32]` fails it
but contains 32. Full intervals also fail at small orders: the Petersen graph
with a vertex deleted has cycle lengths 5, 6, 8, 9 and no factor-2 interval,
yet it has 8-cycles. So the reduction is asymptotic. Small cases are covered by
the published verification (cubic through 48 vertices).

## Step 1. Classify the clean three-port pieces

*Clean 3-pole*: connected, three degree-2 vertices, all others degree 3, no
power-of-two cycle. Deleting a leaf of a spanning tree from a connected cubic
counterexample gives one.

- **Conjecture T.** The only clean 3-poles are the triangle, the two H7
  gadgets and H15.
- **Evidence.** Exhaustive census through 19 vertices
  (`three_pole_census_manifest.md`); `N = 5` by hand proof; complete at every
  size for triangle-built pieces (`three_port_classification.md`).
- **Why it matters.** **T alone implies the conjecture for every cubic
  graph** (proof in `three_port_classification.md`). WRP below is one proposed
  route to T, not a prerequisite. T also means every relevant piece has
  interval path lengths, which the additive calculus needs.
- **Task.** Extend the enumeration to 21, 23, 25 vertices in shards. Run the
  analogous counts for two-port and four-port pieces (no clean two-port piece
  on 8–13 vertices).
- **Stop rule.** A clean 3-pole outside the list refutes T. If its path
  lengths are not intervals, it is the first piece carrying multiplicative
  structure: study it before anything else.

## Step 2. Prove the tower theorem by hand

The template for everything after it. Triangle-built clean pieces have 1, 3,
7, 15 vertices and none beyond. Mechanism: the shortest port path grows by 1
or 2 per level while the longest becomes `N − 1` and doubles, so the triangle
cycle's window reaches a factor of 2 at the 31-vertex step.

- **Deliverable.** A human proof that the triangle closure is exactly
  `{1, 3, 7, 15}`, written to generalize to other bases.

## Step 3. Reduce to prime graphs

Split along cyclic 3-edge cuts; treat 2-edge cuts and bridges separately.
**If the decomposition lemma below holds**, a smallest clean 3-pole outside
the list is a prime cubic graph `B` with a vertex deleted and listed gadgets
substituted at its other vertices. T would then reduce to:

> **WRP.** For every prime cubic `B ≠ K4`, every root `r`, and every labelling
> of the other vertices by the five letters (identity, triangle, uniform H7,
> skew H7, H15, with port orientations), some cycle of `B − r` has a window
> containing a power of two.

Every window is an interval `[ℓ + Σ a_v, ℓ + Σ b_v]`, so all the data is
additive; only the final check is not. WRP with the identity letter only is
the root-robust prime conjecture of pass V.

- **Deliverable.** The decomposition lemma, with bridges, 2-edge cuts and
  cyclic 3-edge cuts, tracking the three ports and every gadget orientation.
  Only then does WRP imply T. Without it, WRP is a stronger standalone
  conjecture.
- **Not yet proved:** the decomposition lemma itself, and therefore any
  equivalence between T and WRP.

## Step 4. Labellings with many large gadgets

The 7- and 15-vertex letters have positive factor-2 weight. Averaging over the
cycle space (`cycle_space_obstruction.md`) already proves WRP on any
bridgeless base when

```
3 (n_identity + n_triangle) ≤ n_H7skew + 3 n_H7uniform + 17 n_H15.
```

- **Deliverable.** A **sharper** criterion than this existing global count:
  edge-conditioned or local versions, and windows that chain together. Do not
  restate the threshold.

## Step 5. Labellings with mostly identities and triangles

The conceptual jump. Identity and triangle letters each contribute −1, so no
single window reaches a factor of 2. This is the only place multiplicative
structure survives, and it is where all known extremal constructions live.

- **Target: doubling-chain lemma.** In a prime cubic `B` of order at least
  `n₀`, with a root `r` and any identity/triangle labelling, there are cycles
  `C_1, …, C_s` avoiding `r` whose windows overlap in sequence and together
  cover `[x, 2x]` (or its even part). Each overlap is a linear inequality.
- **Sources of intervals.** Independent switches with complete increment
  sequences (pass XI's switching polynomial); square strips, whose path
  lengths are step-2 intervals (pass IX); triangles, which are switches of
  increment 1; ear exchanges.
- **Tools.** Subset sums of increments (complete sequences; long arithmetic
  progressions in subset sums); Lyngsie–Merker on residues of cycle lengths to
  control the gcd. Parity needs no special handling, since step-2 intervals
  still hit powers of two.
- **Stop rule.** Test each candidate lemma on all prime graphs up to about 20
  vertices, then on the Markström, Exoo and 450-vertex constructions. A family
  of primes with sparse rooted spectra at every scale kills the lemma, and
  would be the first ingredient of a counterexample.

## Where computation belongs

Only to extend the Step 1 classification, find the smallest counterexample to
a proposed lemma in Steps 4 and 5, and check certificates. Direct search for
counterexamples to the conjecture is out of scope.
