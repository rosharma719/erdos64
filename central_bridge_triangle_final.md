# central_bridge_triangle_final.md — the (A,A) case, T3 consistency, and the final assessment

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Continues `central_bridge_triangle.md` (Parts II–V) and
`central_bridge_triangle_s5.md` (Parts VI–IX); closes out the current
task (Parts X–XIII).

## Part X: the `(A,A)` case

The interrupted analysis assumed both `\tau_x=\tau_y=A`, concretely: terminals `\{x,X_x\}`,
`\ell_x=2,\ell_x'\in\{3,4\}` (inside `B_x`, via `Y_x`); terminals
`\{y,X_y\}`, `\ell_y=2,\ell_y'\in\{3,4\}` (inside `B_y`, via `Y_y`).

**Recovery correction (2026-07-27; supersedes the path-length claims in
X.1-X.2).** `central_bridge_triangle.md` IV.2's conditional anchored-detour
lemma excludes both claimed second-path lengths. Length `3` closes against
`xX_x` to form a `C_4`; length `4`, after deleting the forced first edge
`xY_x`, leaves a length-3 `Y_x`-`X_x` path that closes against `Y_xX_x`
to form a `C_4`. More fundamentally, T2 never guaranteed that its admissible
pair contains the separately known shortest path of length 2, so the inference
to a `3` or `4` mate was invalid. The exact-two-attachment A branch remains
open with an unspecified larger admissible pair; the paragraphs below audit an
unproved pinned specialization, not residual R2/S2 paths.

### X.0. The terminal-pair relationship is fully exhausted by 2 cases, not 3 [PROVED, new]

`X_x\in T\setminus\{x\}=\{y,z_0\}`, `X_y\in T\setminus\{y\}=\{x,z_0\}`
(`z_0:=T\setminus\{x,y\}`, `central_bridge_triangle.md` Part V.1). **So
both terminal *sets* `\{x,X_x\}` and `\{y,X_y\}` are 2-element subsets
of the single 3-element set `T=\{x,y,z_0\}`.** Two distinct 2-subsets of
a 3-set always intersect in **exactly one** element (`|A\cap B|=|A|+|B|-
|A\cup B|\ge2+2-3=1`, and `=2` only if `A=B`). **So exactly one of two
things holds: the terminal sets coincide (X.1), or they share exactly
one element (X.2). A genuinely 4-distinct-terminal "crossing"
configuration (X.3) is arithmetically impossible here** — there are
only 3 candidate terminal vertices in existence (`T` itself), never
enough for 4 distinct ones.

**This is the honest answer to X.3, delivered as the task allows:
it simplifies completely away in this anchored setting**, precisely
because both admissible pairs are anchored inside the same triangle
`T`. **Scope, stated so this is not overclaimed:** this resolves
crossing only between *these two* triangle-anchored terminal sets. It
says nothing about the general crossing case flagged incomplete in
`contraction_intersections.md` V.3 for arbitrary witness-path pairs
elsewhere in `G` — that remains exactly as open as before.

### X.1. Identical terminals — `X_x=y,X_y=x` [SUPERSEDED: pinned lengths unproved]

Here `Y_x=Y_y=z_0`. `B_x`'s shortest path `R_1: x\to y` (length 2) is
`x\text{-}z_0\text{-}y` (edges `xz_0,z_0y`); `B_y`'s shortest path
`S_1: y\to x` (length 2) is `y\text{-}z_0\text{-}x` (edges `yz_0,z_0x`).
**These use the identical two edges** — `R_1` and `S_1` are the *same
path*, traversed in opposite directions, not merely the same length.
This is a genuine structural fact special to this configuration (in the
generic, non-triangle leaf-block setting, two independently-chosen
admissible pairs at the same terminal pair have no such forced
coincidence).

**Every pairwise combination is blocked from the clean shortcut.** `x`'s
only edge into `B_x` is `e_x=x\text{-}z_0`, so *every* `x`-`y` path
inside `B_x` (in particular `R_2`, length `\ell_x'`) passes through
`z_0`. Symmetrically every `y`-`x` path inside `B_y` (`S_1=R_1` and
`S_2`) passes through `z_0`. **So `R_1,R_2,S_2` all share the vertex
`z_0`** — none of the pairwise unions is internally disjoint, so
neither Lemma D nor `contraction_separator_integration.md` VII.1's
clean `\ell+\ell'`-union shortcut applies to any pair drawn from this
set. Historically this paragraph proposed applying the A-output theta
arithmetic with `\ell_x=\ell_y=2`. That application is withdrawn: those
length-2 paths need not belong to T2's admissible pairs. A surviving
identical-terminal A/A case requires new, unpinned admissible-pair data before
the overlap machinery can be applied.

### X.2. One common terminal — the other three `(X_x,X_y)` rows [SUPERSEDED: pinned lengths unproved]

Take the representative case `X_x=X_y=z_0` (`Y_x=y,Y_y=x`; the other two
rows, `X_x=y,X_y=z_0` and `X_x=z_0,X_y=x`, are symmetric relabellings).
Common terminal `z_0`. `R`-family: `x\to z_0`, `R_1` (length 2, via `y`:
`x\text{-}y\text{-}z_0`) or `R_2` (length `\ell_x'\in\{3,4\}`, inside
`B_x`). `S`-family: `y\to z_0`, `S_1` (length 2, via `x`:
`y\text{-}x\text{-}z_0`) or `S_2` (length `\ell_y'\in\{3,4\}`).

**Four candidate combinations, as the task requires, classified
exactly:**

- **`R_1` with `S_1`.** Both use the edge `xy`, in opposite directions,
  then diverge (`R_1` continues `y\text{-}z_0`, `S_1}` continues
  `x\text{-}z_0`). Their union is exactly `\{xy,yz_0,xz_0\}=T` itself —
  **no new information, exactly the same "no new information" finding
  `contraction_atoms.md` III.2 already recorded for the bare triangle
  atom.**
- **`R_1` with `S_2`.** `R_1=x\text{-}y\text{-}z_0` already uses `y` as
  an internal vertex — but `S_2` *starts* at `y`. **Blocked**: the
  natural "close via edge `xy`" combination would need `R_1` (or a
  matching piece of it) to avoid `y`, which it cannot, since `y` is
  `R_1`'s own second vertex. Not a clean combination.
- **`R_2` with `S_1`.** Symmetric obstruction: `S_1=y\text{-}x\text{-}
  z_0` uses `x` internally, while `R_2` starts at `x`. **Blocked** for
  the identical reason.
- **`R_2` with `S_2` (corrected).** Both paths have a forced shared edge:
  every `R_2` starts `x\text{-}y`, and every `S_2` starts
  `y\text{-}x`.  Hence the former `1+\ell_x'+\ell_y'` object repeats
  `x,y,xy` and is not a simple cycle.  More decisively, neither path can
  exist: the anchored-detour lemma above produces a `C_4` from either one
  separately.  With symbolic length `4`, cubicity would force
  `R_2=x-y-y'-r-z_0` and `S_2=y-x-x'-s-z_0`; the literal cycles
  `y-y'-r-z_0-y` and `x-x'-s-z_0-x` expose the contradiction.

**Corrected outcome for Part X.** **The committed R2/S2 candidate is
refuted; anchored `(A,A)` is not eliminated.** X.0 still fully resolves
the terminal-relationship question (only X.1/X.2 occur, X.3 is
vacuous in this anchored setting — the task's own flagged target,
answered), but X.1/X.2's concrete path list was never obtained. A surviving
anchored A/A row must use unspecified larger admissible pairs. See
`type_t_recovery_audit.md` for the recovered definitions, explicit inference
counterexample, independent checks, and corrected residual table.

**Computational cross-check, implemented.**
`verifier/central_bridge_triangle_final.py` brute-forces all 4 rows of
`central_bridge_triangle.md` V.1, confirming the terminal *sets*
`\{x,X_x\},\{y,X_y\}` always coincide or share exactly one element,
never four distinct vertices — an exhaustive check over the only 4
possible configurations, not a sampled search.

## Part XI: T3 consistency across all three vertices

For T3 (`a,b,c` all cubic), every pairwise analysis above (Parts
IV–X, for `(a,b)`, `(a,c)`, `(b,c)`) must remain simultaneously
consistent when the third vertex's own data is added.

- **S5 uniqueness.** If any *two* of the three pairwise analyses
  independently reach the S5 outcome, VI.1's argument applies verbatim
  (it never used which two vertices) — **all pairs reaching S5 must
  name the same cut vertex `z`**, and (if `z\notin T`) `T` sits entirely
  in one lobe regardless of which pair is examined, so there is no
  three-way inconsistency to derive: the lobe distribution is the same
  fact, viewed from any of the (up to 3) pairs.
- **Parity/equality constraints.** Each cubic vertex `x\in\{a,b,c\}`
  independently gets `X_x\in T\setminus\{x\}` (Part V.1's table, one
  choice per vertex, `2^3=8` joint combinations of
  `(X_a,X_b,X_c)\in\{b,c\}\times\{a,c\}\times\{a,b\}`). **No pairwise
  analysis above constrains a *third* vertex's own `X`-choice** — each
  `X_x` is a property of `x`'s own canonical witness (`central_bridge_triangle.md`
  IV, V.1's definitional choice), independent of the other two vertices'
  choices. **So all 8 joint combinations remain consistent** — this is
  not a gap, it is the correct scope: nothing forces `X_a,X_b,X_c` to
  align beyond what each pairwise table already records.
- **Component-sharing transitivity.** If `B_a,B_b` share a component
  (Part V.2's possibility (2)) and `B_b,B_c` also share a component,
  **transitivity would require `B_a,B_c}` to share the same component
  too** — but Part V.2 left possibility (2) open (not shown to occur or
  to be excluded in general), so this transitivity question is
  **conditionally open**: *if* two of the three pairwise-shared-
  component facts hold, the third is forced by ordinary set-theoretic
  transitivity of "same connected component," not by any new graph
  argument — recorded as a free consequence, not a new theorem.
- **Attachment-order consistency.** Each vertex's shortest path
  (`\ell_x=2`) routes through `Y_x`, a *specific* one of the other two
  triangle vertices — consistent across all three simultaneously exactly
  when the `(X_a,X_b,X_c)` triple is fixed (no additional constraint
  beyond X.0/V.1's per-pair table, checked once per pair, not per
  triple).
- **Common-path constraints.** `Q` (`central_bridge_triangle.md` Part
  III) attaches at **one** pair `\{u,v\}\subset T` per power-of-two cycle
  of `G/T` — a given `D` names one specific pair, so at most one of the
  three pairwise analyses is "the `Q`-carrying pair" for that particular
  `D`; `G/T` may have several such `D`'s, potentially naming different
  pairs, each independently subject to Part III's own orbit
  classification (all three pairs equivalent in T3, III.1).

**Required outcome for Part XI.** **No inconsistency is found or
expected** — T3's three pairwise analyses combine freely, since (per the
audit above) none of the six required consistency checks the task lists
actually constrains one pair's data using another pair's, beyond the
ordinary transitivity of shared components (itself conditional, not
forced). This is the honest, complete answer: **T3 is consistent, not
because a hard three-way argument was resolved, but because the
pairwise machinery never created a cross-pair dependency to be
inconsistent about.**

## Part XII: computation strategy, confirmed

**No new graph populations were generated this pass** — every gadget
above is a small, explicit, hand-specified construction (the
shared-external-neighbour 4-cycle gadget, the triangle-theta-bridge
gadget, the double-S5 lobe gadget), each testing one precise structural
or arithmetic claim, none a search or census. **Permitted computation
used**: finite orbit-table enumeration (X.0's 4-row exhaustion,
`central_bridge_triangle.md` V.1's `(X_x,X_y)` table), path/attachment
diagram verification (`networkx.all_simple_paths`,
`node_connected_component`, `articulation_points`), and historical symbolic
arithmetic (the now-superseded `\ell_x'\in\{3,4\}` and
`1+\ell_x'+\ell_y'\in\{7,8,9\}` candidates were closed-form, not searched).
**No existing project
artifact was mined** — consistent with every prior file in this
sequence. **No exponential Diophantine equality was newly solved this
pass** (the frozen `2^m-2`/excluded-residue templates from
`central_bridge_templates.md` are cited, not re-derived); the one new
symbolic quantity, `1+\ell_x'+\ell_y'`, is a small closed enumeration
(`\ell_x',\ell_y'\in\{3,4\}`), not an open Diophantine search.

## Part XIII: honest stopping-condition assessment

**Historical assessment, corrected by the recovery audit.** The original
match was outcome 4, but its pinned A/A specialization used T2 incorrectly.
The current outcome is: **the interrupted R2/S2 claim is refuted by an
explicit theorem-hypothesis configuration.** Exact-two-attachment A remains
open with unspecified larger admissible pairs; multi-attachment A, P, S,
chord, and component-sharing cases also remain as listed in
`type_t_recovery_audit.md`.

- **Type T is not eliminated**, and **no single T2 or T3 configuration
  is isolated as the unique survivor** — ruling out outcomes 1–3.
- **X.0 is the one clean, unconditional new theorem of this pass**:
  the terminal-pair relationship between any two triangle-anchored
  admissible pairs is *always* identical-terminal or one-common-terminal
  — **the crossing case (outcome 5's "anchored crossing-path diagram")
  is not an open diagram to exhibit, because it does not exist in this
  setting.** So **outcome 5 does not apply** — there is no crossing
  diagram to name, anchored or otherwise, because X.0 proves none can
  arise here.
- **No double-S5 configuration is the unique survivor either** — VI.1
  gives one precise lobe distribution, but it is not shown to be forced
  (only shown to be the *only* one of two abstractly-possible
  distributions that can occur) — so **outcome 6 does not apply**
  precisely, though VI.1 is the closest single fact to it.
- **The MA2/A/P/S templates are not shown to fail to combine** — every
  combination examined (VIII, IX, X.1, X.2) was expressed in the frozen
  templates. The one concrete arithmetic candidate
  (`1+\ell_x'+\ell_y'`) was subsequently shown not to be a simple cycle, and
  the claimed short paths are conditionally excluded.
- **The original outcome 4 reduction remains useful only for the genuinely
  multi-attachment/P/S survivors**: T2's `\{a,b\}`-vs-`\{a,c\}/\{b,c\}`
  orbit split, T3's single orbit, the four `(X_x,X_y)` rows, the
  double-S5 lobe-forcing fact, the vacuous crossing-case elimination
  (X.0), and the `(A,A)/(A,P)/(P,P)` matrix all resolve to **one
  finite, named joint obstruction family**: the frozen A/P/S templates
  (`central_bridge_templates.md`), instantiated concretely at
  triangle vertices, combined via the triangle's own edges. The inference
  from shortest length `2` to a `3/4` mate is removed. Component sharing remains
  open, as do the additional residual families itemized in the recovery
  audit; the R2/S2 internal-cleanliness question is closed as based on an
  impossible premise.

**Neither Type N nor Type T is eliminated this pass.** The concrete
named next steps are the residual families in `type_t_recovery_audit.md`,
led by deletion-relative component sharing and the double-S incidence problem
— not another generic central-bridge lemma, a `q=4` census, or more
voltage/defect work.

**Computational cross-check, implemented.** The exhaustive
`check_terminal_pair_exhaustion` result for X.0 is recorded in
`manifests/central_bridge_triangle_final_manifest.json` with its environment
and checksums.
