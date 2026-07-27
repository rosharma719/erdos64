# central_bridge_triangle_s5.md — S5 cases at a Type T triangle

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Continues `central_bridge_triangle.md` Parts II–V; uses
`central_bridge_templates.md`'s frozen A/P/S outputs by citation.
`lemmas.md`'s S5 is cited, not reopened, throughout — exactly the
restriction `contraction_ma2_integration.md` Part IX already imposed on
a single central bridge, now applied to a *pair*.

Fix two distinct cubic vertices `x,y\in T`, `z_0:=T\setminus\{x,y\}` the
third (cubic or in `H`). Each of `\tau_x,\tau_y\in\{A,P,S\}` is the
per-vertex MA2 output of `central_bridge_triangle.md` Part IV.2.

## Part VI: the S5 cases

### VI.1. Both `\tau_x=\tau_y=S` [PROVED, one exact configuration]

If `B_x` hits CB3′ case 2, its own attachment-free leaf `L\subset B_x`
has a cut-attachment vertex `z_x`; symmetrically `B_y` gives `L'\subset
B_y` with cut-attachment `z_y`. Both `z_x,z_y` are genuine cut vertices
of `G` (`contraction_block_cut_tree.md` Part III, quoted in
`central_bridge_templates.md`'s **S** output). **By S5 (`lemmas.md`:
*at most one cut vertex*), if both are genuine cut vertices of the same
graph `G`, they must be the same vertex: `z_x=z_y=:z`.** This is a free
consequence of uniqueness, not an assumption.

**The lobe distribution is forced, not merely restated [PROVED, new].**
`z` gives the one `(G_1,G_2)` partition of `G` (`G_1=`the relevant leaf's
closure, `G_2=`everything else, `|G_1|=|G_2|`, S5). **Assume the generic
case `z\notin T`** (the degenerate case `z\in T` is flagged separately
below, not resolved here).

- `T` is 2-connected (a triangle); removing the single vertex `z\notin T`
  cannot separate any two vertices of `T`. **So all of `T` lies in one
  lobe.** WLOG that lobe is called `G_2` (matching the convention that
  `\Theta_x` always lies in the lobe *not* containing its own
  attachment-free leaf, quoted verbatim in `central_bridge_templates.md`'s
  **S** output: *"The other lobe `G_2` contains `\Theta` in its
  entirety"*).
- Since `x\in T\subseteq G_2` and `x\in V(\Theta_x)`, and `\Theta_x`
  always sits in the lobe *not* containing `L` (its own leaf), **`L`
  must be in `G_1`** — consistent with `T,x\in G_2`.
- Since `y\in T\subseteq G_2` as well, the identical argument applied to
  `B_y`'s own analysis forces `\Theta_y\subseteq G_2` too, and hence
  **`L'` must also be in `G_1`**.

**So the two abstractly possible lobe distributions — `L,L'` on the
same side, or on opposite sides of `z` — collapse to exactly one:
`L,L'` are *forced onto the same lobe* `G_1`, while `T`, `\Theta_x`,
`\Theta_y`, and (per the single-bridge fact) every other block of both
central bridges' block-cut trees sit in `G_2`.** This is not a
contradiction — it is the required "one exact double-S5 configuration,"
sharper than either single-vertex analysis alone, since it pins the
*relative* position of the two leaves, not just each one's position
relative to its own theta.

**Recovery/addendum correction: `L=L'`.** The argument above originally stopped
at the common lobe. `central_bridge_triangle_addendum.md` observes that the S
output defines that lobe as the attachment-free component's closure itself.
Since both analyses use the same cut vertex and the same component of `G-z`
opposite `T`, their leaves are literally the same connected component, not two
unidentified sub-blocks.

**The excluded degenerate case, honestly flagged.** If `z\in T` (i.e.
`z\in\{x,y,z_0\}`), the "triangle can't be split" argument above does not
apply directly (the cut vertex is itself a triangle vertex) and a
separate analysis would be needed. **Not resolved in this pass** —
recorded as a precise, narrow open item, not folded silently into the
generic case above.

**Computational cross-check, implemented.**
`verifier/central_bridge_triangle_s5.py` constructs a double-S5 gadget with a
shared cut vertex and confirms via `networkx.articulation_points` and connected
components that the triangle and leaf occupy the two forced lobes. The sharper
literal equality `L=L'` is checked separately by the addendum verifier.

### VI.2. One `\tau=S`, the other `\in\{A,P\}` [PROVED where stated]

Say `\tau_x=S` (cut vertex `z`, lobes `G_1,G_2` as above, `T\subseteq
G_2` by the identical argument, `z\notin T` generic case), `\tau_y\in
\{A,P\}` (`B_y` is CB3′ case 1, no cut vertex of its own).

**"`B_y` crosses lobes without using `z`" is vacuous, not a contradiction
to derive.** `z` is *by definition* the unique vertex separating `G_1`
from `G_2` (S5's cut-vertex property). Any connected subgraph (`B_y` is
connected) touching both lobes **must** contain `z` — there is no other
route between the lobes. So this sub-case simply does not occur; nothing
is eliminated because nothing of this shape can exist. Recorded exactly
this way rather than manufacturing a contradiction from a vacuous
premise.

**The genuine dichotomy: does `B_y` touch `z` at all?**

- **`B_y` does not touch `z`** (the generic case: `B_y` stays entirely
  inside `G_2`, disjoint from `L`). **Then `B_y`'s A/P arithmetic is
  completely unaffected by `x`'s S5 outcome** — it proceeds exactly as
  `central_bridge_templates.md`'s frozen templates describe, with no new
  term introduced by `z`. This is the default, and nothing here rules
  it out or forces it — it is simply the case requiring no further
  translation.
- **`B_y` touches `z`** (some `\ell_y`/`\ell_y'`-path, or a shared-port
  route, passes through `z`). `z` has degree exactly 4 (S5), with
  exactly 2 edges into `L`/`G_1` and 2 into `G_2` (quoted fact,
  `central_bridge_templates.md`'s **S** output). A path of `B_y`
  entirely within `G_2` can thread through `z` using only its 2
  `G_2`-side edges, contributing no new length term beyond what the
  existing route census already allows (`z` is then just an ordinary
  degree-`\ge3` internal vertex on that route). **Only if the path
  genuinely detours into `L`** (using one of `z`'s 2 `L`-side edges and
  returning) does new arithmetic appear, and its exact length
  contribution depends on `L`'s internal structure — precisely the same
  information gap `contraction_ma2_integration.md` Part IX already
  flagged for a single bridge (*"would require knowing `L`'s own internal
  cycle spectrum... not established in this phase"*). **Not resolved
  here, for the same honest reason.**

**Required outcome, delivered honestly.** Neither the mixed `S`/`A` nor
`S`/`P` combination is eliminated. What is proved: the vacuous
"crosses-without-`z`" case cannot occur at all (so there is nothing to
eliminate there); the generic non-touching case leaves `\tau_y`'s
arithmetic completely untouched; the touching-`z`-and-detouring-into-`L`
case is the one genuinely open item, requiring `L`'s internal cycle
spectrum, exactly as already flagged upstream — **preserved as one
exact mixed-S5 template**, not a false elimination.

**Computational cross-check, planned.** A gadget realizing `B_y`
entirely within `G_2` (confirming no arithmetic change) and, separately,
a gadget where a `B_y` path is forced through `z`'s two `G_2`-side edges
without entering `L` (confirming it contributes no new term beyond the
existing route census), both via explicit path construction.

## Part VII: the non-S5 case matrix, set up precisely

Fix `x,y\in T` cubic, `\tau_x,\tau_y\in\{A,P\}` (Part VI's S5 case
excluded). Every combination has these ingredients available, all
already established, none independent of the others:

- **`Q`**: the shared triangle-contraction outside arc
  (`central_bridge_triangle.md` Part III), giving `2^k+1,2^k+2` at
  *some* attachment pair `\{u,v\}\subset T` — which pair depends on
  which power-of-two cycle of `G/T` is being lifted, not fixed in
  advance.
- **External-edge witnesses** `x',y'`: each cubic triangle vertex's own
  nontriangle edge, already absorbed into `\Theta_x,\Theta_y}` (`P_1`
  branch, `contraction_saturation.md` VII.2) — not a separate witness
  to add again.
- **Closed-neighbourhood power paths**: CN1 (`contraction_neighborhood.md`
  Part II) puts *every* cubic vertex, `x` and `y` included, on its own
  `2^k+2` cycle via `N[x]`/`N[y]` — already the source of `\Theta_x`'s
  own `P_2` branch (`Q_{X_x,x'}`, `contraction_saturation.md` VII.2), so
  again not independent new content, but worth naming explicitly since
  the task requires it be recorded rather than silently absorbed.
- **The A/P bridge paths and theta routes**: `central_bridge_templates.md`'s
  frozen templates, instantiated per vertex. The formerly concrete
  instantiation `\ell_x=2,\ell_x'\in\{3,4\}` was not licensed by T2;
  surviving A data remain symbolic.

**Scoping fact, corrected by the interrupted-session recovery.** When
`\operatorname{att}(B_x)` is exactly `\{x,X_x\}`, Part IV.2 gives the
length-2 path `x-Y_x-X_x`. The original text also asserted a second path of
length 3 or 4, but that inference was invalid: T2 supplies some admissible
pair, not necessarily one containing the length-2 path. The conditional
anchored-detour lemma excludes lengths 3 and 4, but **exact-two-attachment A
remains possible with an unspecified larger admissible pair**. Its complete
guaranteed cycle table and infinite safe family are now recorded in
`type_t_exact_two_a.md`. P and S still
require further attachment structure. The pinned `(A,A)` and pinned side of
`(A,P)` analysed below are historical, unproved specializations.

## Part VIII: the `(P,P)` case

Both `x,y` require a further attachment beyond their own `\{x,X_x\}`,
`\{y,X_y\}` pairs (Part VII's scoping fact) — call the extra attachments
`x_1,x_2\in A(B_x)` sharing port `u_x` (symmetrically `y_1,y_2,u_y` for
`B_y`), per `central_bridge_templates.md`'s **P** output, applied
independently at each vertex. **Its arithmetic, applied independently at
each vertex, is exactly the frozen template**: cycles `2+d_i^x` at `x`
(`d_i^x` a theta-`x_1`-`x_2` route in `\Theta_x`), `2+d_i^y` at `y`,
each requiring `d_i^x,d_i^y\ne2^m-2` for consistency.

**What genuinely combines, and what does not.** `Q` (Part VII) attaches
at some pair `\{u,v\}\subset T`; if `\{u,v\}=\{x,y\}` itself (a
realizable orbit case, `central_bridge_triangle.md` III.1), `Q`'s
`2^k+1,2^k+2` are cycles through `x,y` directly, **independent of the
shared-port data at either vertex** (`Q` lives outside `T` entirely,
while the shared ports `u_x,u_y` are attachment structure *inside* each
`B_x,B_y`) — so no new combined arithmetic beyond the two already-cited
families (Part III's `Q` pair, each vertex's own shared-port template)
is produced by juxtaposition alone, **unless `u_x` or `u_y` coincides
with a vertex of `Q}` itself**, which this file has no way to pin down
without first resolving the open geometry flagged in Part VII.

**Required outcome, honestly delivered.** `(P,P)` is **not eliminated**,
and is **not reducible further than the two independent frozen
templates plus `Q`'s independent pair** — this is the least
characterized of the three non-S5 combinations, precisely because `P`
itself already requires geometry this sequence has not pinned down at a
single triangle vertex (Part VII's scoping fact). Recorded as open,
rather than forcing a combined arithmetic condition from an
underdetermined configuration.

## Part IX: the `(A,P)` case

The formerly analysed anchored `\tau_x=A` path list
(`\ell_x=2,\ell_x'\in\{3,4\}`, terminals `\{x,X_x\}`) is invalid: the
short mate was never supplied by T2 and would force a C4 if present.
Exact-two-attachment A and multi-attachment A can both survive, but their
admissible-pair lengths are not pinned by Part IV.2.
Let `\tau_y=P` have shared port `u_y` and terminals
`y_1,y_2\in A(B_y)`, with extra attachment as in Part VIII.

**Correct symbolic endpoint relationship.** The terminal sets
`\{x,X_x\}` and `\{y_1,y_2\}` still live on different theta systems and
may coincide, meet once, or be disjoint according to the unresolved P
attachment geometry. If they coincide, A contributes its symbolic pair
`\ell_x+d_i,\ell_x+\delta_x+d_i`, while P contributes `2+d_i`; no term
may be replaced by a pinned `\ell_x=2`. One-common/disjoint/crossing cases
still require the generic path-intersection toolkit, after the P ports are
located. This classification is conditional and no A/P combination is
eliminated.

**Corrected outcome.** The same-pair, concretely pinned A/P calculation is
withdrawn because its A path list was unproved. Exact-two-attachment and
multi-attachment A/P families remain open with underdetermined admissible-pair
lengths; no paired `\ell_x=2` arithmetic may be carried into them.
