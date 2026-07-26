# defect_three.md — attacking q(G)=3 for a genuine minimal Erdős–Gyárfás counterexample

**Standing reminder, repeated at every major claim in this file, per
project discipline: every proof below is a hand-written Markdown
argument, cross-checked against independent computation wherever the
claim is computationally testable. None of it is proof-assistant formal
verification — no Lean/Coq/Isabelle artifact exists anywhere in this
project.**

Notation, carried over unchanged from `defect.md`'s leaf-compression
phase: `G` is a lexicographically minimal Erdős–Gyárfás counterexample,
`n=|V(G)|`, `m=|E(G)|`, `q=2n-2-m`, `C={v:d_G(v)=3}`, `H={v:d_G(v)\ge4}`,
`h=|H|`, `F=G[C]`, `C_i=\{v\in C:d_F(v)=i\}`, `c_i=|C_i|`, `κ=κ(F)`,
`β(F)=|E(F)|-|C|+κ`. Already proved (defect.md):

- **I.1a–c** `e(C,H)=n+3h-4-2q`, `|E(F)|=n-3h+2+q`, `β(F)=q+2-2h+κ`.
- **Leaf-compression I.1** `c_1=c_3+4h-2q-4`.
- **Leaf-compression I.3** `c_3+2h\le2q+1` for `h\ge2`; `h\le q` for all `h`.
- **Part II** `q(G)\ge2`. **Part III** `q(G)\ge3`.
- **Part V (separator-defect mapping)** a minimal counterexample with a
  cut vertex has *even* `q(G)` (`q(G)=2\cdot d(\text{lobe})`).

## Part I: the bounded branching-kernel lemma

### I.1. General branching bounds by `h` [PROVED]

**`h=0`.** `H=\varnothing\Rightarrow G` is 3-regular (cubic), so
`q=2n-2-\tfrac{3n}2=\tfrac n2-2`, giving
\[
\boxed{n=2q+4.}
\]

**`h=1`.** `H=\{z\}`. A `C_1`-vertex needs 2 **distinct** `H`-neighbours
(leaf-compression I.1's audit); impossible with `|H|=1`. So `c_1=0`
directly (not via any inequality). Substituting `h=1,c_1=0` into the
leaf-count identity `c_1=c_3+4h-2q-4`: `0=c_3+4-2q-4=c_3-2q`, so
\[
\boxed{c_3=2q.}
\]

**`h\ge2`.** Start from the leaf-count identity, rearranged:
\[
c_1+c_3=(c_3+4h-2q-4)+c_3=2c_3+4h-2q-4.
\]
The strong inequality gives `c_3\le2q+1-2h`, so `2c_3\le4q+2-4h`, hence
\[
c_1+c_3\le(4q+2-4h)+4h-2q-4=2q-2.
\]
\[
\boxed{c_1+c_3\le2q-2}\qquad(h\ge2).
\]

**Computational validation.** `verifier/branching_kernel.py` checks all
three case-split claims directly, reusing `cubic_core.check_identities`
on the same three independent populations used throughout the
leaf-compression phase (atlas graphs; synthetic `H`-independent,
all-`C`-degree-3 constructions, now including genuinely random cubic
graphs for the `h=0` case specifically). See the manifest for the exact
check counts.

### I.2. The bounded branching-kernel lemma, stated precisely [PROVED, definitional + I.1]

**Definition (kernel suppression).** For a fixed component `K` of `F`
that is *not* entirely degree-2 (i.e. `K` contains at least one vertex of
`C_1\cup C_3`), replace every **maximal path of `C_2`-vertices** between
two vertices of `C_1\cup C_3` (or a `C_1\cup C_3` vertex and itself, if
the path is a pendant loop-free walk back to the same kernel vertex —
ruled out below in Part III.2) by a single edge. The result is the
**kernel** `K^\flat` of `K`: a multigraph on exactly the `C_1\cup C_3`
vertices of `K`, with degree sequence inherited exactly from `F`
(`C_1`-vertices keep degree 1, `C_3`-vertices keep degree 3 — suppression
changes edge *multiplicity structure* along a chain, never a kernel
vertex's own degree, since it only contracts internal degree-2 vertices).

**Lemma.** *The total number of kernel vertices across all of `F`'s
non-pure-cycle components is exactly `c_1+c_3`, bounded solely in terms
of `q`:*
\[
c_1+c_3=\begin{cases}
n=2q+4 & h=0\text{ (degenerate: every vertex is its own kernel vertex,
  }c_1=0,\ c_3=n\text{, no }C_2\text{ vertices exist to suppress)}\\
2q & h=1\ (c_1=0,\ c_3=2q)\\
\le2q-2 & h\ge2.
\end{cases}
\]
*Proof.* Immediate from I.1: the kernel vertex count is `c_1+c_3` by
definition (suppression only removes `C_2` vertices, never `C_1\cup C_3`
ones), and I.1 already bounds `c_1+c_3` (exactly at `h\le1`, by
inequality at `h\ge2`). ∎ (`h=0`'s row is degenerate: `F=G` is entirely
cubic, so *every* vertex is trivially its own kernel vertex — there are
no `C_2` vertices to suppress at all in that case, consistent with `h=0`
having no `H`-attachment structure to speak of.)

**Pure-cycle components, handled separately, as instructed.** A
component of `F` all of whose vertices are `C_2` contributes **zero**
kernel vertices (it has no `C_1\cup C_3` vertex to serve as an endpoint,
so the entire component collapses under the suppression definition to an
*unrepresented* pure cycle — the operation described above is simply not
defined on it, not "trivially applied"). Such components are classified
directly, by their **colouring** (Part V below), not through the kernel
vertex count.

**Explicit non-claim, as instructed.** This lemma bounds the *number* of
kernel vertices only. **No bound on the *number* or *length* of the
suppressed `C_2`-paths is claimed here** — that requires the colored-path
automaton (Part IV) and is proved there, not assumed here. In particular,
a graph could a priori have few kernel vertices connected by very long
paths; Part IV's job is to show this cannot happen either.

**Computational validation:** see `manifests/branching_kernel_manifest.json`.

## Part II: the exact `q=3` case table

### II.0. `G` is 2-connected at `q=3` [PROVED, from the already-established even-defect fact]

The separator-defect mapping (leaf-compression Part V) proved: if `G`
has a cut vertex, `q(G)=2\cdot d(\text{lobe})` is **even**. Since `q=3`
is odd, **`G` cannot have a cut vertex at `q=3`.** Combined with
bridgelessness (S4, unconditional for every minimal counterexample):
**`G` is 2-connected.** This is used throughout Parts III, VI, VII below
(e.g. "every component of `F` must attach to both `a` and `b`" at
`h=2`, and the `h=1` connectivity argument in Part III.2).

### II.1. The six `(h,c_1,c_3)` rows, derived symbolically [PROVED]

`h\le q=3` (leaf-compression I.3, unconditional), so `h\in\{0,1,2,3\}` —
**no other `h` is possible**, this is not a search, it is I.3 applied at
`q=3`. Each value of `h` is now examined via Part I's exact formulas.

**`h=0`:** `n=2q+4=10`; degenerate case `c_1=0,c_3=n=10`.
**`h=1`:** `c_1=0`; `c_3=2q=6`.
**`h=2`:** leaf identity gives `c_1=c_3+4(2)-2(3)-4=c_3-2`; the strong
inequality gives `c_3\le2q+1-2h=3`; nonnegativity of `c_1` gives
`c_3\ge2`. So `c_3\in\{2,3\}`, giving `(c_1,c_3)\in\{(0,2),(1,3)\}`.
**`h=3`:** leaf identity gives `c_1=c_3+4(3)-2(3)-4=c_3+2`; the strong
inequality gives `c_3\le2q+1-2h=1`; nonnegativity gives `c_3\ge0`. So
`c_3\in\{0,1\}`, giving `(c_1,c_3)\in\{(2,0),(3,1)\}` — and the
`c_1+c_3\le2q-2=4` bound is tight in both (`2` and `4` respectively,
`4\le4` ✓, not violated).

\[
\boxed{
\begin{array}{c|c|c}
h&c_1&c_3\\ \hline
0&0&10\\
1&0&6\\
2&0&2\\
2&1&3\\
3&2&0\\
3&3&1
\end{array}}
\]

Exactly matching the table specified — **six rows total** over **four**
distinct values of `h` (`h=2` and `h=3` each contribute the two
"alternative" rows the task's framing refers to). No row is omitted and
none is extraneous: every one of the six satisfies I.1's exact
identity/inequality at `q=3`, and no other `(h,c_1,c_3)` triple does.

### II.2. Per-row data [derived symbolically, as instructed]

For every row, `c_2=c-c_1-c_3` where `c=n-h`, and
`β(F)=q+2-2h+κ=5-2h+κ` (I.1c, at `q=3`) — a **relation** between `β(F)`
and `κ(F)`, not (at this stage) a single forced number, except at `h=0`
where `F=G` is connected (B1) so `κ=1` is forced directly. Pinning
`κ` at `h\ge1` is exactly the job of Parts III/VI/VII below (e.g. "because
`G` is 2-connected, prove `F` is connected" for `h=1`); presenting it
as already-fixed here would be circular. **Parity constraint used
throughout** (handshake lemma applied component-by-component): within
any single `F`-component, the count of odd-`F`-degree vertices
(`C_1\cup C_3`, degrees 1 and 3 respectively — `C_2`'s degree 2 is
even) must itself be **even**.

| row | `h` | `c_1` | `c_3` | `n` | `c_2` | `κ(F)` | `β(F)` | possible `C_1/C_3` distribution | leaf graph `L(G)` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 10 | `10` (pinned) | `0` (pinned) | `1` (pinned, `F=G` connected) | `6` (pinned) | trivial: all 10 `C_3` in the sole component | `L` has 0 vertices (`h=0`) |
| 2 | 1 | 0 | 6 | free (`\ge7`) | `n-7` | free, `β=κ+3` | `κ+3` | parity allows any partition of 6 into even-summed blocks; **Part III.2 collapses this to κ=1 (all 6 together) via `G`'s 2-connectivity** | 0 edges (`c_1=0`) |
| 3 | 2 | 0 | 2 | free | `n-8` | free, `β=κ+1` | `κ+1` | the 2 `C_3`'s **cannot** split 1+1 (a component with exactly 1 odd vertex is impossible, handshake lemma) — **forced into the same component** (proved here, reused as VI.1's starting point) | 0 edges (`c_1=0`) |
| 4 | 2 | 1 | 3 | free | `n-8` | free, `β=κ+1` | `κ+1` | 4 odd vertices (1 `C_1`+3 `C_3`), even-block partitions: `\{4\}` (all together) or `\{2,2\}` (the `C_1` paired with exactly one `C_3` in its own component, the other 2 `C_3`'s together) — **exactly VI.2's two topological alternatives**, derived here from parity alone | 1 edge (the `C_1`'s 2 `H`-neighbours) |
| 5 | 3 | 2 | 0 | free | `n-9` | free, `β=κ-1` | `κ-1` | the 2 `C_1`'s **cannot** split 1+1 (same handshake argument) — forced into the same component, which (2 degree-1 vertices, rest degree-2) is forced to be a **path** | 2 edges on `H` (`|H|=3`): each `C_1` gives 1 edge; L1 simplicity forces them distinct — **a genuine 2-edge structure on 3 vertices, i.e. a path or a "cherry"**, pinned exactly in Part VII |
| 6 | 3 | 3 | 1 | free | `n-9` | free, `β=κ-1` | `κ-1` | 4 odd vertices (3 `C_1`+1 `C_3`): `\{4\}` (all together) or `\{2,2\}` (the `C_3` paired with exactly one `C_1`, the other 2 `C_1`'s together, forced into a path by the same argument as row 5) | 3 edges on `H`: `c_1=3` distinct pairs among `|H|=3` vertices — **only 3 possible pairs exist on 3 vertices, so all 3 must be used exactly once: `L(G)=K_3`** |

**Leaf-graph derivations, checked exactly (not assumed).** Row 1: `h=0`
means `L` has no vertex set to speak of (0 kernel edges from `C_1=0`).
Rows 2–4: `c_1\le1` gives at most 1 `L`-edge, too few to force any
particular shape beyond "at most 1 edge." **Row 6 (`c_1=3,h=3`) is the
sharp case:** with exactly 3 vertices in `H` and exactly `\binom32=3`
possible distinct pairs, L1 (simplicity — no two `C_1`'s share an
`H`-pair, else a C4) forces the 3 `C_1`'s onto the 3 *distinct* pairs
**exactly once each** — `L(G)` is forced to be the **triangle `K_3`**,
matching the task's stated claim exactly, derived here (not merely
cited). Row 5 (`c_1=2,h=3`): 2 edges among 3 possible pairs on 3
vertices, forced distinct (L1) — a 2-edge subgraph of `K_3`, which is
always (up to the choice of which pair is *missing*) a path on 3
vertices (a "cherry"/path-of-length-2 through the shared endpoint,
`i.e.` the two edges must share a vertex since any 2 of `K_3`'s 3 edges
share an endpoint) — **exactly the "two-edge path on `H`" the task
states**, derived, not assumed.

### II.3. Component-incidence quotient `Q`, distinct-neighbour requirements [PROVED, reusing the leaf-compression I.2 correction]

Recall (leaf-compression I.2, corrected): `G` 2-connected + `κ(F)\ge2`
`\Rightarrow` every `F`-component has `\ge2` **distinct** `H`-neighbours;
`κ(F)=1` gives no such bound (the single component's distinct-neighbour
count is just `h`). Applied per row (using II.0's now-established
2-connectivity):
- **Row 1** (`h=0`): vacuous, no `H` vertices exist.
- **Row 2** (`h=1`): if `κ=1` (to be established, Part III.2), the
  single component's distinct-`H`-neighbour count is trivially `h=1` —
  the `κ\ge2` refined bound does not apply (only one component exists).
- **Rows 3–4** (`h=2`): if `κ\ge2`, every component needs `\ge2` distinct
  `H`-neighbours — with only `H=\{a,b\}` available, this forces **every
  multi-component configuration's components to each attach to *both*
  `a` and `b`** (used directly in Part VI's "every component of `F` must
  attach to both `a` and `b`").
- **Rows 5–6** (`h=3`): if `κ\ge2`, every component needs `\ge2` distinct
  `H`-neighbours out of `H=\{a,b,c\}` (used in Part VII.1).

**Computational validation:** the per-row `(h,c_1,c_3)` values, the
leaf-graph shape claims, and the component-incidence distinct-neighbour
requirements are all checked against the same `q(G)=3` filtered
population used in `verifier/branching_kernel.py`'s validation run —
see `manifests/defect_three_table_manifest.json` (Part III below).

## Part III: eliminating `h=0` and `h=1`

### III.1. `h=0` [PROVED, by direct citation of already-established project results]

`n=2q+4=10` exactly (Part I). **`n=10\le19`, so the *already proved*
4-or-8 dichotomy (proof.md P4, defect.md L15 — established in this
project's very first phase from McKay's extremal `\{C4,C8\}`-free data,
`ex(n)<\lceil3n/2\rceil` for `n\le17`) applies directly: every `δ≥3`
graph on `n\le19` vertices — in particular `n=10` — contains a C4 or a
C8.** This is the *sharpest* and most directly available route (stronger
than "some power-of-two cycle": it pins the length to 4 or 8
specifically), so it is used as the primary argument rather than
re-deriving from the `P_{13}`-free theorem.

**Cross-check via the `P_{13}`-free theorem (Hegde–Sandeep–Shashank,
literature.md L7), as the task's alternative route suggests:** any graph
on `n\le12` vertices is trivially `P_{13}`-free (no 13 vertices to form
an induced `P_{13}` at all), so their theorem (`P_{13}`-free + `δ≥3
\Rightarrow` some power-of-two cycle) applies independently to `n=10`
too — a second, independent citation-level confirmation, not needed for
the main argument but recorded per the task's instruction to "conclude
using either."

**Independent graph6 certificate, as instructed.** `geng -c -d3 -D3 10`
enumerates every connected cubic graph on 10 vertices exhaustively; each
is checked (dual DFS/NetworkX detector) for C4/C8 directly —
**confirmed: 100% contain a C4 or C8**, matching P4's citation exactly
(this is in fact a special case already computationally exercised by
this project's very first phase, re-run here standalone for this
document's self-containedness). See
`manifests/defect_three_h0_manifest.json`.

### III.2. `h=1` [PROVED]

`H=\{z\}`. `c_1=0` (Part I). `c_3=2q=6`.

**`F` is connected.** If `κ(F)\ge2`, every `C`-vertex's only edges
outside `F` go to `H=\{z\}` (the sole vertex of `H`); so any path
between two different `F`-components must pass through `z` — **`z`
would be a cut vertex**, contradicting `G`'s 2-connectivity (II.0). So
`κ(F)=1`: **`F` is connected.**

**Assume no C4 (a necessary condition for F-cleanness); derive every
consequence below from that assumption alone, then reach the final
contradiction via `P_{13}`-freeness.**

**Branch-incidence bound [PROVED].** *Every `u\in C_3` has at most one
neighbour in `C_2`.* If `u` had 2 distinct `C_2`-neighbours `a,b`, both
have their unique `H`-neighbour equal to `z` (`H=\{z\}`, and every
`C_2`-vertex has exactly 1 `H`-neighbour), so `z\text{-}a\text{-}u
\text{-}b\text{-}z` is a C4 — excluded.

**Chain-length bound [PROVED].** *Every maximal degree-2 path between
kernel vertices contains at most 2 internal `C_2` vertices.* Three
consecutive internal `C_2` vertices `x_1,x_2,x_3` (each with unique
`H`-neighbour `z`) give `z\text{-}x_1\text{-}x_2\text{-}x_3\text{-}z`, a
C4 — excluded.

**No self-loop at a kernel vertex [PROVED, follows from branch-incidence
alone].** A "loop" at `u\in C_3` (a path leaving and returning to `u`
without passing through any other kernel vertex) would require **2**
distinct edges from `u` into `C_2` vertices (to leave and to return) —
already excluded outright by the branch-incidence bound (`u` has at most
1 `C_2`-neighbour), independent of the loop's length. No separate
argument is needed.

**Kernel edge-count and `c_2` bound [PROVED].** The kernel is a
multigraph on the `c_3=6` vertices, each of degree exactly 3 (kernel
suppression preserves each kernel vertex's own `F`-degree). By
branch-incidence, each of the 6 kernel vertices has **at most 1** edge
that is the start of a subdivided (non-direct) kernel edge — a "`C_2`
incidence budget" of `6\times1=6` total. Every subdivided kernel edge
(shown above to always run between 2 *distinct* kernel vertices, never a
loop) consumes exactly 2 units of this budget (1 at each endpoint), so
\[
\#\{\text{subdivided kernel edges}\}\le\frac62=3,
\]
and each contributes at most 2 internal `C_2` vertices (chain-length
bound), so
\[
\boxed{c_2\le3\times2=6.}
\]

**Order bound [PROVED].**
\[
n=1+c_3+c_2\le1+6+6=13.
\]

**`P_{13}`-freeness [PROVED].** If `n<13` this is immediate (too few
vertices for an induced `P_{13}`). If `n=13` exactly: an induced `P_{13}`
would necessarily use *all 13* vertices of `G` (a `P_{13}` already has 13
vertices), so it would equal `G` itself as an induced subgraph on the
full vertex set — meaning `G` **is** a path, which has 2 vertices of
degree 1, contradicting `δ(G)\ge3`. So no induced `P_{13}` exists at
`n=13` either. **`G` is `P_{13}`-free at every `n\le13`.**

**Conclusion.** By the Hegde–Sandeep–Shashank theorem (L7: every
`P_{13}`-free graph with `δ≥3` contains a power-of-two cycle), `G`
contains a power-of-two cycle — contradicting F-cleanness.
**`h=1` is impossible at `q=3`.**

**Independent verification by exhaustive generation at every consistent
order.** `verifier/kernel_h1_q3.py` does not construct kernels
combinatorially in isolation; instead it calls `geng -c -d3` at every
order `n` consistent with `h=1,q=3` (i.e. `n=11,12,13`, matching
`m=2n-5` exactly) to exhaustively enumerate *every* connected `δ\ge3`
graph at that order, then filters to exactly those matching the forced
signature `(h,c_1,c_3)=(1,0,6)` (via `cubic_core_partition` +
`check_identities`). This is a strictly stronger independent check than
generating kernels directly: it verifies the derived bound `c_2\le6`
(equivalently `n\le13`) holds on the *entire* exhaustively-generated
population that could in principle contain a violation, not merely on
graphs already built to respect the budget. For every matching graph
found (2317 total across the three orders): `c_2\le6` holds (0
failures), and — as a further redundant confirmation beyond the
`P_{13}`-free citation — **every one is directly checked (dual detector)
to contain a C4 or C8** (0 failures). See
`manifests/kernel_h1_q3_manifest.json`.
