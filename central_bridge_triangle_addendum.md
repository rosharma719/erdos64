# central_bridge_triangle_addendum.md — two sharpenings after the Part XIII close

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. `central_bridge_triangle_final.md` Part XIII already
closed the Type-T joint-triangle sequence (outcome 4: every case reduces
to the frozen A/P/S templates, concretely instantiated, neither Type N
nor Type T eliminated). This file does not reopen that assessment or
add a new part number to the closed sequence — it records two narrow,
independently-checked sharpenings of specific claims inside
`central_bridge_triangle_s5.md` VI.1 and `central_bridge_triangle_final.md`
Part X.2, found while independently re-deriving the same ground. Neither
changes the sequence's overall outcome.

## 1. `central_bridge_triangle_s5.md` VI.1: `L=L'` is forced, not merely unresolved

VI.1 proves (generic case, `z\notin T`) that both attachment-free leaves
`L,L'` (for two cubic triangle vertices `x,y` both landing in the **S**
output, sharing the same cut vertex `z` by S5's uniqueness) lie in the
same lobe `G_1`, then states: *"Whether `L=L'`. Not forced either way by
the argument above: both are sub-blocks of the single lobe `G_1`, but
nothing here identifies them as the same block."*

**This is an understatement of what is already proved.** `central_bridge_templates.md`'s
own **S** output (transcribing `contraction_block_cut_tree.md` III.2
verbatim) does not merely place `L` *inside* `G_1` — it *defines* `G_1`
**as** `L`'s closure: *"The two lobes: `G_1` (`=L`'s closure, `V(L)\cup
\{z\}`)."* `G_1` is not some larger lobe that happens to contain the
sub-block `L`; **`G_1` *is* `L\cup\{z\}`, exactly, by the S output's own
definition.**

**Corollary [PROVED, new].** Given `z_x=z_y=z` (VI.1's own free
consequence of S5 claim 5) and `G-z`'s two components `C_1,C_2` (S5
claim 1, one global fact about `G`, not two independent instances): `x`'s
analysis defines `G_1^{(x)}:=L\cup\{z\}` and shows `T\subseteq G_2^{(x)}`;
since `L,V(L)\setminus\{z\}` cannot be a *proper subset* of `C_1` or
`C_2` (it is disconnected from everything else by removing only `z`, and
`G-z` has *exactly* two components, so `V(L)\setminus\{z\}` must coincide
with one of them entirely, not merely sit inside it), `G_1^{(x)}` is
**exactly** one of `\{C_1,C_2\}` — and since `T\subseteq G_2^{(x)}`, that
one is `C_1` (the component not containing `T`, given the two-component
split is fixed by `z` alone, independent of which vertex's analysis
names it). The identical argument for `y` gives `G_1^{(y)}=C_1` too,
since `T\subseteq G_2^{(y)}` forces the same exclusion. **So
`L=G_1^{(x)}\setminus\{z\}=C_1\setminus\{z\}=G_1^{(y)}\setminus\{z\}=L'`
exactly — the two leaves are the same connected piece of `G`, not merely
two (possibly different) sub-blocks of the same lobe.**

**Why this does not change VI.1's own required outcome.** VI.1's stated
result was already "one exact double-S configuration, not a
contradiction" — this sharpening pins down the configuration further
(identifying `L` and `L'` as literally the same object) without
producing a contradiction either; it is a strictly sharper instance of
the same non-eliminating outcome, not a different one.

**Computational cross-check.** `verifier/central_bridge_triangle_addendum.py`'s
`check_l_equals_lprime` builds an explicit gadget with a single cut
vertex `z`, confirms via `networkx.connected_components` that `G-z` has
exactly two components, and confirms both vertices' independently-
computed "leaf side" identify the *same* component — not merely two
components on the same "side."

## 2. `central_bridge_triangle_final.md` Part X.2: the bridge-spectrum identity pins `\ell_x'=4`

Part X (citing `central_bridge_triangle.md` IV.2) leaves `\ell_x'\in\{3,4\}`
symbolic throughout the `(A,A)` analysis (X.1, X.2's `R_2,S_2` candidate
cycle `1+\ell_x'+\ell_y'\in\{7,8,9\}`). **`\ell_x'=3` can be excluded
outright, and `\ell_x'=4` forces a condition on `\rho_x` — both by direct
citation of machinery already on record, not by new arithmetic.**

**Setup, restated exactly.** Under IV.2's own hypothesis
(`\operatorname{att}(B_x)=\{x,X_x\}` exactly), `\{x,X_x\}` is a genuine
2-cut of `G` (`two_cut.md` VI.1, cited via
`contraction_separator_integration.md` VI.1), with `B_x` one of its
bridges, spectrum `\Lambda_x:=\{\text{lengths of simple }x\text{-}X_x
\text{ paths in }B_x\}\supseteq\{2\}` (IV.2's own `\ell_x=2`). **Two
further bridges at the same cut are already implicit in `\Theta_x`
itself**: the trivial edge-bridge `B_0` (the direct `P_0` edge
`xX_x\in E(G)`, `\Lambda_0=\{1\}`, `two_cut.md` §2's own "trivial
bridge" convention), and `B'`, the component of `G-\{x,X_x\}` containing
`x'` (i.e. `x'` plus the interiors of `P_1,P_2`, which meet only at
`x'`): `\Lambda_{B'}=\{2^{\rho_x},2^{s_x}+1\}` exactly (the two routes
through `x'` via `P_1` or `P_2`).

**`(\Lambda_0+\Lambda_x)\cap F=\varnothing`** is exactly `two_cut.md`
§2's own "trivial bridge" corollary: `\Lambda_x\cap\{2^k-1:k\ge2\}=
\varnothing`. **So `3\notin\Lambda_x`, unconditionally** (3 is a literal
`C_4` combining the length-3 detour with the direct `P_0` edge) — pinning
IV.2's `\ell_x'\in\{3,4\}` down to `\ell_x'=4` whenever a second element
of `\Lambda_x` beyond `2` is realized at all.

**`(\Lambda_x+\Lambda_{B'})\cap F=\varnothing`**, applied to `4\in
\Lambda_x`: `4+2^{\rho_x}\notin F` is required. This fails **exactly
when `\rho_x=2`** (`4+4=8\in F`): for `\rho_x>2`,
`4+2^{\rho_x}=4(2^{\rho_x-2}+1)`, with `2^{\rho_x-2}+1` odd and `>1`,
never a power of two. **So: whenever IV.2's hypothesis holds and
`\ell_x'=4` (the only surviving option), `\rho_x\ne2` is forced** — the
`xx'`-edge witness's exponent can never take its minimum value.

**Scope, stated precisely.** This uses `two_cut.md`'s bridge-spectrum
identity `(\Lambda_i+\Lambda_j)\cap F=\varnothing` (`i\ne j`, cited, not
re-derived), applied to the three bridges `B_0,B_x,B'` at cut
`\{x,X_x\}` — a direct instantiation of already-proved machinery to this
specific triangle-anchored setting, not a new theorem about `two_cut.md`
itself. It sharpens `\ell_x'`'s two-element dichotomy to one value and
adds one new exponent-exclusion; it does not resolve Part X.2's own
open item (whether `R_2,S_2` are internally clean) or change Part
XIII's outcome-4 assessment.

**Computational cross-check.** `verifier/central_bridge_triangle_addendum.py`'s
`check_lambda_x_excludes_three` and `check_lambda_x_four_excludes_rho_two`
build explicit gadgets realizing a length-3 detour (confirmed to close
into a literal `C_4` against the direct edge) and a length-4 detour
combined with `\rho_x=2` (confirmed to close into a literal `C_8`, and
safe at `\rho_x=3`), matching the arithmetic above exactly.

## 3. Status, honestly scoped

Neither sharpening changes `central_bridge_triangle_final.md` Part
XIII's stopping-condition assessment: **Type T remains not eliminated,
outcome 4 remains the accurate match.** Both are narrow corrections/
extensions found by independently re-deriving the same double-S and
admissible-pair ground via a different (bridge-spectrum-identity-based)
route, recorded here rather than silently left as a discrepancy between
files.
