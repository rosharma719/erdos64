# central_bridge_triangle_pole_forcing.md — the theta-chord case is forced whenever the pole is cubic, eliminating T3

**Status.** Hand-written proof, independently cross-checked by an
explicit NetworkX construction. Not proof-assistant formal verification.
No literature-novelty claim is made.

**Scope.** This file is independent of, and does not reopen, the
recovery audit's R2/S2 correction (`type_t_recovery_audit.md`,
`central_bridge_triangle_addendum.md` §2) — it does not touch
exact-two-attachment A's arithmetic at all. It instead resolves
`type_t_recovery_audit.md`'s own **"theta-chord case IV.1(ii)"** row
(`central_bridge_triangle.md` IV.1's case (ii), listed there as
genuinely open: *"exact placement of `Y_x` on the near-power/power
branch and resulting route arithmetic"*), by showing that case is not
merely possible but **forced** whenever the aligned pole `X_x` is
cubic, and that it **always** produces a forbidden power-of-two cycle.
This eliminates T3 outright and narrows every other residual family in
the recovery audit's table (exact-two-attachment A, multi-attachment
A, P, single/mixed S, double S) to the one place they can still occur:
T2, with the aligned pole fixed to the (necessarily unique) non-cubic
triangle vertex.

## 1. Setup, recalled exactly, not re-derived

For cubic `x\in T` with mates `\{p,q\}=T\setminus\{x\}`
(`central_bridge_triangle.md` Part IV): `X_x\in\{p,q\}` is whichever
mate the canonical `xx'`-edge witness exits through; `Y_x:=T\setminus
\{x,X_x\}`; `\Theta_x` has poles `\{X_x,x'\}`, branches `P_0=X_x{-}
x{-}x'` (length 2), `P_1:x'\to X_x` (length `2^{\rho_x}-1`, the
`xx'`-edge witness, avoiding `x`), `P_2:X_x\to x'` (length
`2^{s_x}`, the `N[x]`-witness `Q_{X_x,x'}`, avoiding `x`). `e_x=x{-}
Y_x` carries central bridge `B_x`. IV.1 distinguishes case (i)
(`Y_x\notin V(\Theta_x)`, `e_x` a genuine bridge) from case (ii)
(`Y_x\in V(\Theta_x)`, `e_x` a chord) and calls (i) "the generic one
used below" without checking whether (ii) can be avoided.

## 2. `P_2` avoids `Y_x`; a cubic `X_x`'s own degree pins `P_1`'s neighbour exactly [PROVED]

`P_2=Q_{X_x,x'}` is the outside arc of the `N[x]`-contraction lift
(`contraction_neighborhood.md` Part II, `contraction_saturation.md`
VII.2). By the atom-lifting lemma's own mechanism
(`contraction_atoms.md` Part I, atom `A=N[x]=\{x,X_x,Y_x,x'\}`), the
outside arc of any quotient cycle lies entirely outside `A` except at
its two attachment vertices — here `X_x,x'` — so `P_2` avoids every
other vertex of `A`, **in particular `Y_x`**. This is automatic from
what "outside arc" already means; it is not a new hypothesis.

Write `X_x'` for **the pole `X_x`'s own external neighbour**; this is
distinct notation from `x'`, the external neighbour of the original cubic
vertex `x` and the other theta pole.  **If `X_x` is cubic**, its three edges
are exactly `\{X_xx,X_xY_x,X_xX_x'\}` (`X_x`'s own fixed Type-T structure:
two triangle edges and its own external edge). `P_0` already uses the edge
`X_x{-}x`.
`P_1,P_2` are theta branches of length `\ge3` each (`\rho_x,s_x\ge2`),
so — by the standard definition of a theta graph used throughout this
project — each needs its own, distinct edge from `X_x` into its interior.
`X_x`'s only two remaining edges are `X_xY_x` and `X_xX_x'`. Since `P_2`
**cannot** use `Y_x` (above), its first edge at `X_x` must be `X_xX_x'`,
and **`P_1`'s edge from `X_x` must be `X_xY_x`** — the only option left.
This does not assert that `X_x'=x'`; the two external-neighbour symbols have
different owners.

**Corollary [PROVED].** *Whenever `X_x` is cubic, `Y_x` is adjacent to
`X_x` on `P_1` — `central_bridge_triangle.md` IV.1's case (ii) is
forced, not merely possible.*

## 3. The forced chord creates an immediate power-of-two cycle [PROVED]

Under the forcing above: the chord `e_x=x{-}Y_x` exists (case ii).
Trace the route `x\to Y_x` via `P_0` then `P_1`: `x` to `x'` (`P_0`'s
other edge, length 1), then along `P_1` from `x'` up to (but not
including) its final edge — i.e. up to `Y_x`, since `Y_x` is `P_1`'s
own vertex adjacent to `X_x` — length `(2^{\rho_x}-1)-1=2^{\rho_x}-2`.
Total route length `1+(2^{\rho_x}-2)=2^{\rho_x}-1`. This route is
simple (`x`, `x'`, `P_1`'s own internal vertices, `Y_x` all pairwise
distinct — `x` is the theta centre on `P_0`, not on `P_1`).

**Closing this route with the chord `e_x` gives a simple cycle of
length**
\[
\boxed{(2^{\rho_x}-1)+1=2^{\rho_x}}
\]
**— a power of two, for every `\rho_x\ge2`, unconditionally.**

**Theorem (pole-forcing elimination) [PROVED].** *A cubic Type-T
triangle vertex `x`'s aligned pole `X_x` can never be cubic. If it
were, the forced chord `e_x` together with the `P_0`-`P_1` route
closes into a simple `2^{\rho_x}`-cycle, contradicting `G`'s
`F`-cleanness. Hence `X_x` must be the (necessarily unique) non-cubic
triangle vertex.*

**Computational cross-check.** `verifier/central_bridge_triangle_pole_forcing.py`
builds the complete gadget (triangle, both externals, full
`P_0/P_1/P_2` branches with `Y_x` placed exactly where the forcing
argument puts it — as `P_1`'s own vertex adjacent to `X_x`) and
confirms, via both a hand-rolled and a `networkx` cycle checker, a
genuine simple cycle of length exactly `2^{\rho_x}` for
`\rho_x\in\{2,3,4,5\}` — 0 mismatches.

## 4. Consequence: T3 is eliminated; T2's residual families are confined to one pole assignment [PROVED]

**T3.** Every cubic vertex `x\in T` has both triangle-mates cubic. `X_x`
must be one of them, so `X_x` is always cubic — **contradicting §3 for
every choice of `x`. T3 cannot occur in a minimal counterexample: it is
eliminated outright.**

**T2** (`x,y` cubic, `z_0` the unique non-cubic vertex). `X_x\in\{y,
z_0\}`; `X_x=y` is cubic, excluded by §3, so `X_x=z_0` is forced.
Symmetrically `X_y=z_0`. **This is exactly the last row of
`central_bridge_triangle.md` Part V.1's table (`X_x=X_y=z_0`) — rows
1–3 (every row where `X_x` or `X_y` equals the *other* cubic vertex)
are eliminated by the identical argument.**

**Scope correction to the residual table, stated precisely.**
`type_t_recovery_audit.md`'s residual-family table lists the
theta-chord case as a live, open row and treats the other rows (exact-
two-attachment A, multi-attachment A, P, single/mixed S, double S) as
occurring "either" in T2 or T3. §2–3 above supersede this: **the
theta-chord row is not open — it never survives** (its only possible
trigger, a cubic `X_x`, is now excluded). **Every other row's own
"either" is narrowed to T2 only, with the aligned pole of *every*
cubic vertex under study fixed to `z_0`.** None of those rows'
own arithmetic changes — `\Lambda_x\supseteq\{2\}`, the two exclusions
`3,4\notin\Lambda_x` (`central_bridge_triangle_addendum.md` §2), the
`L=L'` double-S argument, the P/multi-attachment templates — all go
through exactly as proved, now correctly scoped to this one pole
assignment rather than left open across four.

**Computational cross-check.** `check_rows_1_2_3_impossible` confirms,
via the same forced-cycle gadget, that rows 1–3 each produce a literal
`2^{\rho}`-cycle (using whichever forced-cubic pole applies), while
`check_row_4_no_forced_cycle` confirms the last row (both poles built
with degree `\ge4`) produces no such forced cycle.

## 5. What this does not resolve

No claim is made about `B_x`'s or `B_y`'s further internal structure,
component sharing, or the still-open items `type_t_recovery_audit.md`
Section 7 already lists (deletion-relative component equality, P's
extra-attachment geometry, mixed-S leaf detours, the `z\in T`
degenerate S5 case). Those all remain exactly as open as recorded
there, now understood to apply only to T2's one surviving pole
assignment.

## 6. Honest stopping-condition assessment

**T3 is eliminated outright**, by an unconditional degree-forcing
argument, not a conjectural narrowing. **T2 survives**, restricted to
exactly one pole assignment (`X_x=X_y=z_0`) rather than four; within
it, every residual family already catalogued in
`type_t_recovery_audit.md` remains open exactly as recorded there. This
is closest to the task's outcome **"T3 eliminated, T2 configuration(s)
remain"** — not full Type-T elimination, and not a restatement of the
already-catalogued residual families, but a genuine narrowing of which
configurations can occur at all.

**Named next steps.** The residual families of `type_t_recovery_audit.md`
Section 7, now scoped to `X_x=X_y=z_0` only: deletion-relative
component sharing, P's extra-attachment geometry, multi-attachment A's
terminal/overlap geometry, mixed-S leaf-detour internal spectrum, the
double-S incidence question, and the `z\in T` degenerate S5 case.

## 7. Limited computation, honestly scoped

**No `q=4` census, no broad graph regeneration.** Computation is
limited to `verifier/central_bridge_triangle_pole_forcing.py`: the raw
degree-counting fact (§2), the forced power-of-two cycle for
`\rho_x\in\{2,3,4,5\}` (§3), and the row 1–3-vs-4 confirmation (§4). All
are small, explicit, hand-specified gadgets.
