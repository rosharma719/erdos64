# central_bridge_triangle_addendum.md — two sharpenings after the Part XIII close

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. `central_bridge_triangle_final.md` Part XIII originally
closed the Type-T joint-triangle sequence under outcome 4. The recovery audit
corrects that assessment: the pinned A paths were not obtained, so
exact-two-attachment A returns to the residual table and neither Type N nor
Type T is eliminated. This file adds no new part number to the historical
sequence; it records two narrow, independently checked corrections to claims in
`central_bridge_triangle_s5.md` VI.1 and `central_bridge_triangle_final.md`
Part X.2, found while independently re-deriving the same ground.

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

## 2. `central_bridge_triangle_final.md` Part X.2: neither claimed short detour survives

Part X (citing `central_bridge_triangle.md` IV.2) left
`\ell_x'\in\{3,4\}` symbolic throughout the `(A,A)` analysis. The first
version of this addendum correctly excluded `3` but incorrectly retained `4`.
The interrupted-session recovery (`type_t_recovery_audit.md`) found the
missing triangle-edge closure: **both values force a `C_4`**, so the pinned
`{2,3/4}` path claim does not survive.

**Setup, restated exactly.** Under IV.2's own hypothesis
(`\operatorname{att}(B_x)=\{x,X_x\}` exactly), `\{x,X_x\}` is a genuine
2-cut of `G` (`two_cut.md` VI.1, cited via
`contraction_separator_integration.md` VI.1), with `B_x` one of its
bridges, spectrum `\Lambda_x:=\{\text{lengths of simple }x\text{-}X_x
\text{ paths in }B_x\}\supseteq\{2\}` (IV.2's isolated shortest path,
not an admissible-path label). **Two
further bridges at the same cut are already implicit in `\Theta_x`
itself**: the trivial edge-bridge `B_0` (the direct `P_0` edge
`xX_x\in E(G)`, `\Lambda_0=\{1\}`, `two_cut.md` §2's own "trivial
bridge" convention), and `B'`, the component of `G-\{x,X_x\}` containing
`x'` (i.e. `x'` plus the interiors of `P_1,P_2`, which meet only at
`x'`): `\Lambda_{B'}\supseteq\{2^{\rho_x},2^{s_x}+1\}` (the two guaranteed
routes through `x'` via `P_1` or `P_2`; other off-theta structure may enlarge
the bridge spectrum).

**`(\Lambda_0+\Lambda_x)\cap F=\varnothing`** is exactly `two_cut.md`
§2's own "trivial bridge" corollary: `\Lambda_x\cap\{2^k-1:k\ge2\}=
\varnothing`. **So `3\notin\Lambda_x`, unconditionally** (3 is a literal
`C_4` combining the length-3 detour with the direct `P_0` edge).

For `\ell_x'=4`, use information internal to `B_x` that the bridge-spectrum
comparison discarded. Every `x`-`X_x` path in `B_x` starts with `xY_x`.
Deleting that edge from the length-4 path leaves a simple length-3
`Y_x`-`X_x` path. The triangle edge `Y_xX_x` closes it into a literal
`C_4`. Hence **`4\notin\Lambda_x` as well**, under this anchored setup.

The old arithmetic implication `4\in\Lambda_x\Rightarrow\rho_x\ne2` is
still a correct conditional application of the cross-bridge identity, but it
is vacuous here: its antecedent cannot occur. It must not be reported as a
surviving Type-T restriction.

**Scope, stated precisely.** The length-3 exclusion uses `two_cut.md`'s
bridge-spectrum identity; the length-4 exclusion uses only the forced prefix
and the other triangle edge. Together they eliminate the claimed paths before any
R2/S2 internal-disjointness or component-sharing question arises.

**Upstream correction.** The exact-two-attachment A branch itself is not
eliminated. T2 guarantees some pair of path lengths differing by 1 or 2; it
does not guarantee that the separately known shortest path of length 2 is in
that pair. Thus the surviving spectrum may contain `2` together with a larger
admissible pair. The R2/S2 labels and every calculation based on their claimed
lengths are unavailable, not a proof that the bridge has no admissible pair.

**Computational cross-check.** `verifier/central_bridge_triangle_addendum.py`'s
`check_lambda_x_excludes_three` and the recovery verifier's independent
symbolic/NetworkX checks confirm the two distinct `C_4` closures. The older
length-4/`\rho_x` arithmetic fixture is retained only as a check of that
conditional sum, not as evidence that a length-4 anchored detour is valid.

## 3. Status, honestly scoped

Type T remains not eliminated. The committed anchored R2/S2 candidate is
refuted: its path lengths were not supplied by T2, and hypothetical paths of
those lengths force `C_4`s. Exact-two-attachment A remains a survivor with an
unspecified larger admissible pair. See `type_t_recovery_audit.md` for the
corrected residual table and explicit theorem-inference regression.
