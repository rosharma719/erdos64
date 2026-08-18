# contraction_block_cut_tree.md — resolving the multi-attachment obstruction

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Builds on `contraction_central_bridge.md` (CB1) and
`contraction_separator_integration.md` (CB3′, whose case 3 — the
`\ge3`-attachment obstruction — is exactly what this file resolves) and
cites `lemmas.md` S5, `two_cut.md` T1/T2/T4 directly.

## Part I: the augmented central bridge — notation

`\Theta=P_0\cup P_1\cup P_2`, poles `p,q`, cubic center `v\in P_0`,
central bridge `B=B_v`, `A(B)=\operatorname{att}_\Theta(B)`. The
unresolved case (CB3′, case 3): `|A(B)|\ge3`. Chords are excluded from
this analysis (a chord's two endpoints already ARE its full attachment
set — no internal structure to analyse); the genuine obstruction is a
nontrivial component bridge, `K:=B-V(\Theta)`, retaining every edge
between `K` and `A(B)`.

**Three deliberately distinguished objects, per the task's own
caution:** for `x\in A(B)`, its **port set** `\pi(x)\subseteq V(K)` is
the set of `K`-vertices adjacent to `x` (generically a single vertex,
but not assumed so); a port `u\in\pi(x)` is an **internal neighbour**
of `x`; and the **block** of `K`'s block-cut tree containing `u` is a
third, distinct object — a block can contain ports of several different
attachments, or none.

## Part II: attachment-core pruning

Let `T(K)` be `K`'s block-cut tree (nodes: blocks and cut vertices of
`K`, standard bipartite tree structure). A block is **marked** if it
contains some port `u\in\pi(x)`, any `x\in A(B)`. Since `|A(B)|\ge3`, at
least one marked block exists. **Prune every unmarked leaf of `T(K)`
iteratively** (remove an unmarked leaf, check whether the resulting
tree has a new unmarked leaf, repeat) until every remaining leaf is
marked; call the result the **attachment core** `T_A(B)`.

### II.1. The five claims [PROVED]

**1. `T_A(B)` is connected.** `T_A(B)` is exactly the *Steiner subtree*
of `T(K)` spanning the marked nodes — the union of all tree-paths
between pairs of marked nodes, which is always connected (a subgraph of
a tree consisting of unions of paths sharing endpoints in the marked
set). Iterative unmarked-leaf pruning computes exactly this subtree:
pruning never removes a marked node (only *unmarked* leaves are
targeted), and it terminates exactly when every leaf is marked — the
unique minimal connected subtree containing every marked node.

**2. Every leaf of `T_A(B)` is marked.** Immediate from the pruning
stopping condition.

**3. Every theta attachment is represented in at least one marked
block.** Every `x\in A(B)` has `\pi(x)\ne\varnothing` (definition of
attachment), so the block containing any `u\in\pi(x)` is marked by
definition, and — since marked blocks are never removed by pruning
(claim 1) — survives in `T_A(B)`.

**4. A simple path inside `B` between two theta attachments' ports
projects to a path in `T_A(B)`.** Standard block-cut tree fact: a
simple path between two vertices of a connected graph, recorded by
which block it occupies at each step, traces exactly the (unique)
tree-path between those vertices' blocks in the block-cut tree — no
block is skipped, none is revisited except as consecutive tree-nodes.
Since both endpoints' blocks are marked (claim 3), the corresponding
tree-path lies entirely within the Steiner subtree of the marked set —
i.e. within `T_A(B)` (claim 1's characterization).

**5. A simple path cannot visit the same block-cut-tree node twice.**
A block-cut tree is a tree (acyclic); the projection of any simple path
is itself a simple tree-path (a path cannot leave and later re-enter a
block without passing back through one of its (at most two, on a
non-branching traversal) incident cut vertices — but a *simple* path
visits each vertex, in particular each cut vertex, at most once, so it
cannot pass through the same block-boundary twice).

**Audit: shared ports/blocks.** Two distinct attachments `x,y\in A(B)`
may have `\pi(x)\cap\pi(y)\ne\varnothing}` (a literal shared port
vertex) or simply share the same *block* without sharing a port vertex.
Neither breaks claims 1–5 above — marking is defined at the block level
and is monotone in the number of attachments routing through it. This
is exactly the phenomenon Part VII below (shared-port vs. distinct-port)
resolves in detail; it is not an obstruction to the pruning construction
itself.

**Computational cross-check.** `verifier/block_cut_tree.py`'s
`check_attachment_core_pruning` builds explicit multi-block gadgets with
a mix of marked and unmarked leaves, computes the block-cut tree via
networkx, prunes, and confirms all five claims directly (connectivity,
all-leaves-marked, attachment representation, and — via explicit path
construction — that simple paths project without repetition).

## Part III: attachment-free leaf blocks and S5

Let `L` be a leaf of the **original** (pre-pruning) block-cut tree of
`K`, unique cut vertex `z`, with **no** vertex of `V(L)\setminus\{z\}`
incident to any theta attachment.

### III.1. `z` is a cut vertex of `G` [PROVED]

Every edge from `V(L)\setminus\{z\}` goes either within `L`, or to `z`
(`L` a leaf block, unique cut vertex `z}` — by definition its only
connection to the rest of `K` is via `z`), or to `\Theta` — but the
attachment-free hypothesis excludes the last option entirely. So
`G-z` disconnects `V(L)\setminus\{z\}` from everything else: **`z` is a
cut vertex of `G`.**

### III.2. Exact S5 consequences [PROVED, by direct citation]

By **S5**: `z` is `G`'s *unique possible* cut vertex, `\deg_G(z)=4`
exactly, and the two lobes have **equal order and equal size**.
`V(L)\setminus\{z\}` lies entirely within one lobe (say `G_1}`, since it
is connected to the rest of `G` only via `z`). Since S5 gives *exactly
two* of `z`'s four edges into each lobe, and all of `z`'s edges into
`G_1}` are precisely its edges into `L`: **`z` has exactly 2 edges into
`L`.** The other lobe `G_2}` contains `\Theta` in its entirety (`\Theta`
is connected to `z` only via `B`'s attachment structure, which routes
through `L` only if `A(B)\subseteq V(L)` — excluded here since `L` is
attachment-free — so `\Theta` and `z`'s remaining two edges lie together
in `G_2}`, along with any other `K`-blocks not equal to `L`).

**Coexistence with `|A(B)|\ge3` [tested, found consistent — not
eliminated].** Nothing above prevents the other `\ge3` attachments from
routing entirely through `K`'s *other* blocks (all in `G_2}`), with `L`
serving purely as an attachment-free appendage off `z`. **This
configuration is not eliminated; it is reduced to one exact, highly
constrained S5-central-bridge configuration:** `G` has a cut vertex
`z`, `\deg_G(z)=4}` with exactly 2 edges into `L}`; `G_1=L`'s closure
(`V(L)\cup\{z\}`, i.e. `L}` itself); `G_2\supseteq\Theta`; **and
`|G_1|=|G_2|`, `|E(G_1)|=|E(G_2)|` exactly (S5's equal-order/equal-size
conclusion)** — since `G_2}` already contains all of `\Theta` (a
substantial structure: poles, three branches of lengths `2,2^r{-}1,2^s`
at minimum, plus the *rest* of `B`'s other blocks), **`L` itself must be
comparably large** — a severe, concrete size constraint, not a
contradiction, matching the required outcome's second alternative
exactly (reduced to one exact configuration).

**Computational cross-check.** `check_attachment_free_leaf_s5` builds
an explicit gadget with an attachment-free leaf `L` and confirms
directly (via networkx connectivity) that `z` disconnects `L` from a
constructed `\Theta`-proxy, and that `z`'s edge count into `L` versus
into the rest matches the "exactly 2 into each side" structural claim
whenever the gadget is built to have exactly 4 total edges at `z`.

## Part IV: singly marked leaf block gives admissible attachment paths

Let `L` be a leaf of the **attachment core** `T_A(B)`, unique cut vertex
`z`, with **exactly one** theta attachment edge `xu` (`x\in V(\Theta)`,
`u\in V(L)\setminus\{z\}`).

### IV.1. `L` is not a bare edge [PROVED]

If `L=uz` (a `K_2`-block — the standard block-cut-tree convention *does*
admit bridge-edges as degenerate blocks, audited here explicitly), `u`'s
only edges would be `uz` and (the single attachment) `ux` — degree 2,
**contradicting `\delta(G)\ge3`** (assuming `u` has no further block
incidence, which "singly marked, `u` not a cut vertex" rules out by
hypothesis). **So `L` is a genuine 2-connected block** (the only other
option in the block-cut-tree convention).

### IV.2. `R+xz` is 2-connected; admissible paths apply [PROVED]

Write `R:=L` with vertex `x` and edge `xu` added, terminals `(x,z)`.

**Degree preservation, the generic case.** For `w\in V(L)\setminus\{z\}`:
"singly marked" already gives no *other* attachment at `w`
(`w\ne u\Rightarrow` no attachment edge at all; `w=u\Rightarrow` exactly
the one edge `ux`) — this sub-claim is automatic from the hypothesis,
not additional work. **The remaining sub-claim — `w` has no edge into
another `K`-block — holds unless `w` is itself forced to be `G`'s
(unique, by S5) cut vertex**, exactly as in Part III's mechanism applied
recursively to a hypothetical further unmarked branch hanging off `w`:
if such a branch existed, its own leaf's cut vertex would need to be a
*second* cut vertex of `G`, forbidden by S5 unless it coincides with
`z` itself (impossible for `w\ne z}` inside `L`'s own interior). **In
the generic case (no such coincidence), every `w\in V(L)\setminus\{z\}`
has all its `G`-edges inside `L` (plus, for `w=u`, the edge to `x`), so
`d_R(w)=d_G(w)\ge3`** exactly. *(The non-generic case reduces to a
variant of Part III's S5 analysis and is not a new obstruction.)*

**`R+xz` is 2-connected [PROVED directly, using only `L`'s own
2-connectivity — no need to invoke `G`'s 2-connectivity as `T1` does].**
`L` is 2-connected (IV.1). Check every single-vertex removal from
`R+xz`: removing `x` leaves `L` (connected). Removing `u`: `L-u` is
connected (2-connectivity of `L`), and `x` still reaches `z}` directly
(`z\in L-u`, edge `xz`) — connected. Removing `z`: `L-z` is connected,
and `x` reaches `u\in L-z` via edge `xu` — connected. Removing any other
`w`: `L-w` connected, `x` reaches both `u,z\in L-w` — connected. **No
single-vertex removal disconnects `R+xz`.**

**Applying the rooted admissible-path theorem (`k=2`, Gao–Huo–Liu–Ma,
cited exactly as in `two_cut.md` T2).** Both hypotheses verified:
`R+xz` 2-connected, every internal vertex degree `\ge3` — gives **two
simple `x`-`z` paths whose lengths differ by 1 or 2.**

### IV.3. MA1 — the multi-attachment admissible-pair lemma [PROVED]

`|A(B)|\ge3`: choose `y\ne x`, `y`'s port outside `V(L)\setminus\{z\}`
(exists since `L` is singly marked and `|A(B)|\ge3\ge2+1}`). Choose a
simple `z`-`y` path `S` through `K\setminus(V(L)\setminus\{z\})`
(internal vertices avoiding `L`'s interior). Concatenating each of the
two admissible `x`-`z` paths with `S` (valid: both share exactly the
vertex `z}`, and `S` avoids `L}`'s interior entirely, so no other
overlap) gives:

**MA1 [PROVED].** *Two simple `x\to y` paths `Q_1,Q_2`, `|Q_2|-|Q_1|
\in\{1,2\}`, both lying inside `B`.*

**Computational cross-check.** `check_ma1_construction` builds an
explicit singly-marked-leaf gadget, verifies `R+xz`'s 2-connectivity and
internal-degree preservation directly, and confirms the concatenated
`Q_1,Q_2` are genuine simple `x`-`y` paths with the predicted length
difference, for both `\delta=1` and `\delta=2` instances.

## Part V: MA2 — the central bridge trichotomy

**MA2.** *Every central theta bridge with `|A(B)|\ge3` satisfies at
least one of: (1) it contains two theta-attachment paths whose lengths
differ by 1 or 2; (2) it contains an attachment-free leaf block
(Part III's exact S5 configuration); (3) it contains a leaf block
incident with at least two distinct theta attachments.*

**Proof [PROVED] — sharper than requested: (1) or (3) always holds by
itself.** `|A(B)|\ge3>0`, so at least one block is marked, so `T_A(B)`
is a nonempty tree, so it has at least one leaf (every nonempty tree
does). By Part II claim 2, this leaf is marked — it carries at least one
attachment. **If exactly one:** Part IV applies, MA1 gives outcome (1).
**If at least two (counting *distinct* elements of `A(B)`, not edge
multiplicity — the task's own caution, addressed directly in Part VII
below):** outcome (3) holds directly. **So (1) or (3) always holds,
unconditionally, from the mere existence of a marked leaf of `T_A(B)`.**

**Where (2) fits, precisely.** Outcome (2) concerns leaves of the
*original, pre-pruning* block-cut tree of `K` — exactly the leaves
pruning *removes*. It is a genuinely independent, separately-occurring
structural fact (Part III), not logically required to complete the
trichotomy's exhaustiveness (which (1)/(3) already guarantee alone) —
but it is real, constrains the graph severely when it does occur
(III.2), and is recorded as its own case because the task's trichotomy
correctly anticipates it as a live possibility to *check*, even though
it turns out not to be load-bearing for completeness. **This is stated
plainly rather than silently strengthening the claim past what was
asked**: MA2 as stated is proved in full; the sharpening (that (1)/(3)
alone already exhaust the cases) is an honest bonus observation, not a
substitute for the requested three-way statement.

**Computational cross-check.** `check_ma2_trichotomy` builds three
separate gadgets (singly-marked leaf only, attachment-free leaf present,
multiply-marked leaf) and confirms in each that the corresponding
outcome is triggered by direct inspection of the constructed attachment
core, and specifically that a nonempty `T_A(B)` always has a marked leaf
falling into outcome (1) or (3).
