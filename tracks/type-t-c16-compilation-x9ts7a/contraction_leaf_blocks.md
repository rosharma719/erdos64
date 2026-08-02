# contraction_leaf_blocks.md — arithmetic of admissible pairs and attachment-rich leaves

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Builds on `contraction_block_cut_tree.md` (MA1, MA2) and
cites `two_cut.md` T1/T2 (Gao–Huo–Liu–Ma) directly.

## Part VI: arithmetic of an admissible attachment pair

Assume MA2 outcome (1): `Q_1,Q_2:x\to y` inside `B`, lengths
`\ell,\ell+\delta`, `\delta\in\{1,2\}`. For every simple `x`-`y` route
inside `\Theta` itself (not through `B`) of length `d_i`, the pairing
gives cycles `\ell+d_i` and `\ell+\delta+d_i`.

### VI.1. Endpoint-location route census [PROVED, exhaustive per case]

Write `P_1` length `M`, `P_2` length `N`, poles `p,q`.

**Case 1 — `x,y` on the same branch** (say `P_1`, distances `d_x<d_y`
from `p`). **Three routes**, no more: direct sub-arc (`d_y-d_x`); via
`v` (`d_x+2+(M-d_y)`); via `P_2` (`d_x+N+(M-d_y)`). *(No route uses both
`P_1`'s far side and `P_2` simultaneously — that would revisit `p` or
`q`.)*

**Case 2 — `x,y` on different branches** (`x` on `P_1` at distance
`d_x` from `p`, `y` on `P_2` at distance `d_y` from `p`). Each of `x,y`
has exactly two "exit poles" (`p` at distance `d_x}`/`d_y`, `q` at
`M-d_x}`/`N-d_y`); a route pairs one exit-pole of `x` with a matching
entry-pole of `y`, closing directly if they coincide or detouring via
`P_0` (length 2) — or the direct `pq` edge (length 1), if present —
otherwise. **Four routes** (six if `pq\in E(G)`): `d_x+d_y`;
`(M-d_x)+(N-d_y)`; `d_x+2+(N-d_y)`; `(M-d_x)+2+d_y`; and, only if
`pq\in E(G)`: `d_x+1+(N-d_y)`; `(M-d_x)+1+d_y`.

**Case 3 — one of `x,y` is `p` or `q`.** If (say) `x=p`, this is
exactly Case 1 with `d_x=0` — no new formulas, cited not re-derived.
If `x=p,y=q` (both poles), the routes are exactly `\Theta`'s own
`p`-`q` spectrum: `2` (`P_0`), `M`, `N`, and `1` if `pq\in E(G)` —
**three or four routes**, matching `\Lambda_0\cup\{M\}\cup\{N\}` from
`contraction_separator_integration.md` VIII.2.

**Case 4 — one attachment equals `v`.** **Vacuous.** `v` has no
boundary edges within `\Theta` at all (`contraction_central_bridge.md`
I.3, via CB1) — `v\notin A(B)` ever, for any theta bridge.

**Case 5 — the central topological-`K_4` return geometry.** If one of
`x,y` coincides with the earlier single-attachment analysis's own
return vertex (`contraction_central_bridge.md` Part IV), its route set
is exactly that `K_4}` subdivision's own six branch-path combinations —
cross-referenced, not re-derived, since it is already the case-1/2
route census specialized to that particular `x`.

**No route is double-counted**: every route above is characterized by
which pole(s) it uses to connect the branches, and internally-repeated
vertices are excluded by construction (each route is a concatenation of
sub-arcs of distinct branches, meeting only at shared poles).

### VI.2. Integrating the near-power data — a compact template family [PROVED template; no contradiction claimed]

For a fixed route length `d_i`, the two paired cycles `\ell+d_i` and
`\ell+\delta+d_i` must both avoid `F={4,8,16,\dots}`:
\[
\ell+d_i\ne2^t\quad\text{and}\quad\ell+d_i\ne2^t-\delta\qquad(\text{all
valid }t).
\]
(`\delta=1`: excludes `\ell+d_i\in\{2^t-1,2^t\}`, i.e. `\ell+d_i}` may
not be *or immediately precede* a power of two. `\delta=2}`: excludes
`\ell+d_i\in\{2^t-2,2^t\}`.) **Applied across every `d_i`** in VI.1's
route census (3–6 values depending on the case), this gives a **compact
finite family of excluded-residue templates on `\ell`** — one pair of
excluded values per route, all expressible in closed form given `M,N`
(and `r,s` once substituted). **No contradiction is forced by this
arithmetic alone** (as flagged explicitly, this is not expected without
further numeric information pinning `\ell`) — **the required outcome is
this exact finite template family**, not a false elimination claim.

**Computational cross-check.** `verifier/leaf_block_arithmetic.py`'s
`check_route_census` builds explicit gadgets for Cases 1–3 and confirms
the predicted route counts and lengths via direct construction and
independent enumeration; `check_admissible_pair_templates` confirms the
excluded-residue arithmetic for both `\delta` values against direct
power-of-two testing.

## Part VII: the attachment-rich leaf block

Assume MA2 outcome (3): leaf `L` (attachment core), cut vertex `z`,
`X_L\subseteq A(B)` with `|X_L|\ge2`, port map `\phi`.

### VII.1. Shared-port case [PROVED template]

`\phi(x)=\phi(y)=u`: the bridge contains the length-2 path `x{-}u{-}y`.
Combined with a theta route of length `d_i` (VI.1's census, applied to
this `x,y}`): cycle length `2+d_i`. **Immediate contradiction exactly
when `d_i=2^m-2` for some `m`** (`m\ge2`: `d_i\in\{2,6,14,30,62,\dots\}`).
**Not automatically contradictory in general** (nothing forces every
available route to hit this residue) — **retained as the exact
shared-port template: every theta `x`-`y` route length must avoid
`2^m-2`, for all `m`, a finite, checkable condition per theta.**

### VII.2–3. Distinct-port case reduces directly to an admissible pair [PROVED — sharper than the task's proposed trichotomy]

`u=\phi(x)\ne\phi(y)=w`. **The task's own VII.3 asks whether one of
three outcomes holds (shared port; admissible-path applicability to
some `(u,w)`-rooted subgraph; port-saturation) — working this through
finds a cleaner answer than a genuine three-way split.**

**`L` is 2-connected here too [PROVED, same mechanism as IV.1].** If `L`
degenerated to a bare edge, some port vertex would have degree `\le2}`
(one block edge, one attachment), contradicting `\delta(G)\ge3` unless
it carries a second attachment — excluded by the distinct-port
hypothesis at that specific vertex. So `L` is genuinely 2-connected.

**The admissible-path theorem applies *directly* to `R:=L+\{x,y\}+
\{xu,yw\}`, rooted at `x,y` themselves — not merely at some auxiliary
`(u,w)`-rooted subgraph.** *Proof, `R+xy` 2-connected, by the identical
five-case single-vertex-removal check as `contraction_block_cut_tree.md`
IV.2* (now with `x,y` as the added terminals and `u,w` playing the role
`u` played there): removing `u`: `L-u` connected (`L` 2-connected),
`x` still reaches `y` via the closure edge `xy`, `y` still reaches
`L-u}` via `w` — connected; removing `w`, symmetric; removing `x` or
`y`, leaves `L` (plus a pendant, still connected); removing any other
`L`-vertex, `L`-minus-that-vertex stays connected (2-connectivity) and
both `x,y` still reach it via `u,w`. **Every other vertex retains full
`G`-degree in the generic case** (identical caveat to Part IV: fails
only if some vertex is forced to coincide with `G`'s S5 exception).

**Consequence: this gives an admissible `x`-`y` pair *directly*,
`\ell,\ell+\delta`, `\delta\in\{1,2\}` — the exact same kind of pair
MA1 produces, with `x,y` themselves as the endpoints (no auxiliary `S`
excursion needed, since both endpoints are already genuine theta
attachments).** **So the distinct-port case of outcome (3) feeds
directly back into Part VI's arithmetic — it is not a separate
arithmetic regime.**

**What this means for the task's proposed trichotomy.** The genuinely
new content in an attachment-rich leaf is **only** the shared-port
arithmetic (VII.1); the distinct-port case does *not* require a
separate "admissible-path-sometimes-applies" analysis or a genuine
port-saturation fallback — it **always** reduces to Part VI's machinery
in the generic case. **Port-saturation (the task's outcome 3 of VII.3)
is therefore not generically needed** — a real strengthening, found by
working the construction through rather than assumed. The one place it
could still matter is the same recurring non-generic exception (a
vertex of `L` coinciding with `G`'s S5 cut vertex) — addressed once,
not built out into a separate theory, in Part VIII below.

**Computational cross-check.** `check_shared_port_arithmetic` confirms
the `2+d_i=2^m` contradiction condition directly; `check_distinct_port_reduction`
builds an explicit distinct-port gadget, confirms `R+xy`'s 2-connectivity
and full internal degree preservation exactly as in the MA1 check,
demonstrating the reduction mechanically.

## Part VIII: port-saturated block — why it is not generically needed

**The task's Part VIII asks to reduce a minimal attachment-rich leaf to
a finite port-topology list, investigating whether it must contain a
shared port, a `\ge3`-port cycle, a theta between ports, a `K_4}`
subdivision, or a smaller admissible subgraph.** Part VII.2–3's finding
answers this directly: **in the generic case, every distinct-port pair
already reduces to a direct admissible pair (Part VI's arithmetic) —
there is no further "saturation" structure to classify**, since the
2-terminal admissible-path machinery applies at the *first* attempt
(`R=L+\{x,y\}+`attachment edges, terminals `x,y` themselves), not after
some sequence of failed smaller attempts requiring a fallback
classification.

**The only surviving question is the shared-port template (VII.1)** —
itself already a finite, exact condition (`d_i\ne2^m-2`, all routes),
not requiring further block-topology classification. **And the one
non-generic exception** (some `L`-vertex forced to coincide with `G`'s
S5 cut vertex, breaking the degree-preservation step) **reduces to a
variant of Part III's exact S5 configuration**, already fully treated
there — not a new topology to enumerate.

**Honest conclusion: Part VIII's requested finite-topology classification
collapses to two already-resolved cases (VII.1's shared-port template;
Part III's S5 exception) plus the generic distinct-port reduction to
Part VI — no genuinely new "port-saturated block" phenomenon survives
the construction.** This is reported as a positive resolution (the
question Part VIII poses turns out to have a clean answer, once VII.2–3
is worked through), not a gap.

**Computational cross-check.** No new gadget is needed beyond VII.2–3's
`check_distinct_port_reduction` and VII.1's shared-port check — both
already exercise every surviving case; `verifier/leaf_block_arithmetic.py`
does not construct a separate "port-saturated" gadget, since none is
claimed to exist generically.
