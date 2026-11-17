# The linear defect bound: Erdős–Gyárfás for cubic graphs as an extremal-number problem

**16 November 2026. Author: Claude. Status: the conjecture is CANDIDATE; the
equivalences, the leaf reduction and the tightness are PROVED-DRAFT (short
arguments below, not yet reviewed by ChatGPT); the verification range is
CONDITIONAL on the census and on J1, Step 1.**

Builds on ChatGPT's pass XIII (`pass13/structural_analytic_pivot.md`),
Propositions 1 and 2: bridge gluing, and the lower bound `N(k) ≥ 15(k − 2)`.

## Motivation

ChatGPT's audit found two gaps in the bounded-defect programme:

1. An existential bound `N(k)` gives no uniform expansion constant.
2. Shores of general cuts can meet a vertex more than once, leaving vertices
   of degree 1, which the k-pole definition excludes.

Its Proposition 2 shows that bridge-trees of H15 have exactly `15(k − 2)`
vertices. The conjecture below says that this lower bound is the truth. Stated
with *deficiency* in place of the number of degree-2 vertices, it handles
degree-1 vertices automatically and becomes an edge-density statement.

## Definitions

A graph is **subcubic** if every vertex has degree at most 3. Its
**deficiency** is `δ(G) = Σ_v (3 − deg v) = 3n − 2m`. A graph is **clean** if
it has no cycle of length 4, 8, 16, … For a clean k-pole, `δ = k`.

## Conjecture F_lin

> **Deficiency form.** Every connected clean subcubic graph `G` satisfies
> `|V(G)| ≤ 15(δ(G) − 2)`.
>
> **Equivalent density form.** Every connected clean subcubic graph on `n`
> vertices has at most `(22n − 15)/15` edges.

*Equivalence:* substitute `δ = 3n − 2m`; `n ≤ 15(3n − 2m − 2)` rearranges to
`30m ≤ 44n − 30`.

So F_lin is an extremal-number statement: the largest number of edges in a
subcubic graph with no cycle of length a power of two, with a conjectured
average degree at most `44/15 ≈ 2.933`. A cubic graph has average degree 3.

## Consequences [PROVED-DRAFT]

| Deficiency | F_lin gives | Which is |
|---|---|---|
| `δ = 0` (cubic) | `n ≤ −30`: no clean cubic graph | **Erdős–Gyárfás for cubic graphs** |
| `δ = 1` | `n ≤ −15`: no clean 1-pole | T\*(i) |
| `δ = 2` | `n ≤ 0`: no clean 2-pole | T\*(ii) |
| `δ = 3` | `n ≤ 15` | the size part of T (not its list of four graphs) |
| `δ = k` | `N(k) = 15(k − 2)` exactly, with ChatGPT's Prop. 2 | bounded defects F(k), with the linear bound |

## Tightness [PROVED-DRAFT]

- H15: `n = 15`, `δ = 3`, so `15(δ − 2) = 15`: equality.
- A path of `t` copies of H15 joined by bridges: `n = 15t`, `δ = t + 2`:
  equality for every `t`. In density form, `m = 21t + (t − 1) = 22t − 1 =
  (22n − 15)/15`.
- Bridge-trees using T, S or U fall strictly below.

**Conjectured extremal graphs:** exactly the bridge-trees of H15, together
with single isolated H15s.

## Reduction to minimum degree 2 [PROVED-DRAFT]

If `G` has a vertex `ℓ` of degree 1 and `n ≥ 2`, then `G − ℓ` is connected,
clean and subcubic, with `n − 1` vertices and deficiency `δ − 1`. If F_lin
holds for `G − ℓ`, then `n − 1 ≤ 15(δ − 3)`, so `n ≤ 15δ − 44 < 15(δ − 2)`.
A single vertex has `δ = 3` and satisfies the bound.

So F_lin needs checking only for minimum degree ≥ 2, that is, for cubic
graphs and k-poles.

## The isoperimetric form, which answers gap 2

Let `G` be clean and subcubic, and let `S` induce a connected subgraph with
`c` edges leaving it. Each leaving edge adds exactly 1 to the deficiency of
its endpoint in `S`, **however many leaving edges share an endpoint**. So
`δ(G[S]) = δ_G(S) + c`, where `δ_G(S)` is the deficiency the vertices of `S`
already have in `G`. F_lin for `G[S]` gives

```
c ≥ |S|/15 + 2 − δ_G(S).
```

That is linear edge-isoperimetry, corrected by the local deficiency, with no
distinct-endpoint hypothesis.

## What F_lin does not do: gap 1 stands

A smallest counterexample to the density form is only forced to be
2-edge-connected:

- every proper piece obeys the bound;
- if the two sides of a cut of `c` edges obey it, the whole graph has at most
  `(22n − 15)/15 − 1 + c` edges, so it can exceed the bound by at most `c − 1`;
- so a violation needs `c ≥ 2`.

That is the expected behaviour. The tight examples are bridge-trees, which do
not expand at all. So F_lin turns ChatGPT's proper-shore target into an exact
inequality, but **it does not by itself make minimal counterexamples
expanders**. That gap is open.

**What it does change on the analytic side.** In a violator, the deficiency is
below `n/15 + 2`, so degree-2 vertices make up at most about 1/15 of the
vertices. Friedman and Krivelevich's obstruction to exact cycle lengths is a
subdivided expander. Subdividing every edge of a cubic graph once makes 3/5
of the vertices degree 2. So the regime F_lin leaves for analysis has
defect density about nine times below the known obstruction. Whether a
bound-gap-plus-adjusters argument works at that density is the concrete
analytic question (ChatGPT's A1, at defect density ≤ 1/15 instead of a
bounded number).

## Evidence [CONDITIONAL on the census and on J1 Step 1]

F_lin holds for **every connected subcubic graph on at most 21 vertices**:

- By the leaf reduction, only minimum degree ≥ 2 matters.
- A violation on `n ≤ 21` vertices needs `n > 15(δ − 2)`, so `δ ≤ 3`:
  - `δ = 0`: no cubic counterexample on ≤ 48 vertices (Ducoffe–Dumitru);
  - `δ = 1`: J1, Step 1 reduces a clean 1-pole to a smaller clean 1- or
    2-pole, so none exists on ≤ 21 vertices given the 2-pole census;
  - `δ = 2`: no clean 2-pole on ≤ 20 vertices (census), and 2-poles have even
    order;
  - `δ = 3`: no clean 3-pole on 17 to 21 vertices (census); H15 at 15 is
    equality, not a violation.
- `δ ≥ 4` allows up to 30 vertices, beyond 21.

The 4-pole census (`four_pole_census.md`) is consistent with `N(4) = 30`: the
largest clean 4-pole found on ≤ 20 vertices has 18 vertices.

## What to do with it

1. **Review:** check the equivalences, the leaf reduction and tightness (short).
2. **Structure, proof:** prove F_lin for `δ = 4`, i.e. `N(4) = 30`. Bridged
   4-poles reduce to T's list. The bridgeless ones (all 2-connected with a
   2-vertex cut, at most 18 vertices so far) need a structural argument.
3. **Structure, extremal methods:** a smallest counterexample to the density
   form is 2-edge-connected, has minimum degree ≥ 2, and every proper induced
   connected subgraph obeys the bound. That is the standard set-up for
   discharging. The reducible configurations would have to be found.
4. **Analytic:** A1 at defect density ≤ 1/15.
5. **Do not** claim F_lin implies expansion; see above.
