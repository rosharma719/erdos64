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
