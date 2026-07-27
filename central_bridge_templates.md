# central_bridge_templates.md — normalized single-bridge output templates

**Standing reminder, per project discipline.** Nothing here is a new
theorem — this file normalizes, without paraphrase, the exact proved
formulas from `contraction_block_cut_tree.md` and `contraction_leaf_blocks.md`
into one reference table, so the Type T joint analysis
(`central_bridge_triangle.md`) can cite them precisely. Nothing here is
proof-assistant formal verification.

## A — admissible-pair output

*Source: `contraction_block_cut_tree.md` IV.2–IV.3 (MA1), `contraction_leaf_blocks.md`
Part VI.*

- **Attachments:** `x,y\in A(B)`.
- **Bridge-path lengths:** `\ell,\ \ell+\delta`, `\delta\in\{1,2\}`
  (exact quote: *"Two simple `x\to y` paths `Q_1,Q_2`, `|Q_2|-|Q_1|
  \in\{1,2\}`, both lying inside `B`"* — MA1).
- **Every simple theta `x`-`y` route length** (VI.1, exact quotes):
  - same branch: **three routes** — `d_y-d_x`; `d_x+2+(M-d_y)`;
    `d_x+N+(M-d_y)`.
  - different branches: **four routes** (six if `pq\in E(G)`) —
    `d_x+d_y`; `(M-d_x)+(N-d_y)`; `d_x+2+(N-d_y)`; `(M-d_x)+2+d_y`; and,
    only if `pq\in E(G)`: `d_x+1+(N-d_y)`; `(M-d_x)+1+d_y`.
  - one attachment a pole: reduces to the same-branch case at `d_x=0`;
    both attachments poles: `\Theta`'s own spectrum, `2,M,N`, and `1` if
    `pq\in E(G)`.
- **Resulting cycle lengths, every route `d_i`:** `\ell+d_i` and
  `\ell+\delta+d_i` (exact quote, VI, opening line).
- **Exact surviving arithmetic condition (VI.2, quoted in full):**
  \[
  \ell+d_i\ne2^t\quad\text{and}\quad\ell+d_i\ne2^t-\delta\qquad(\text{all
  valid }t).
  \]
  `\delta=1`: excludes `\ell+d_i\in\{2^t-1,2^t\}`. `\delta=2`: excludes
  `\ell+d_i\in\{2^t-2,2^t\}`. **"No contradiction is forced by this
  arithmetic alone... the required outcome is this exact finite
  template family, not a false elimination claim"** — quoted exactly,
  not paraphrased as "safe."

## P — shared-port output

*Source: `contraction_leaf_blocks.md` VII.1, resolved precisely below
per the task's own instruction, since the prior compressed report left
this direction ambiguous.*

- **Shared internal port:** `u=\phi(x)=\phi(y)`, `x\ne y\in X_L\subseteq
  A(B)`.
- **Length-two bridge path:** `x{-}u{-}y` (exact quote: *"the bridge
  contains the length-2 path `x{-}u{-}y`"*).
- **Every theta `x`-`y` route** `d_i`: identical census to the A
  template above (VI.1), now applied to this specific `x,y` pair.
- **The precise role of `2^m-2`, stated without shorthand:** combining
  the length-2 bridge path with a theta route `d_i` gives a cycle of
  length `2+d_i` (a *direct*, single cycle — not a paired-offset
  system like A's `\ell,\ell+\delta`). **`2^m-2` is the forbidden route
  length**: the configuration is an *immediate contradiction* — an
  actual power-of-two cycle of `G` — **exactly when `d_i=2^m-2` for some
  `m\ge2`** (`d_i\in\{2,6,14,30,62,\dots\}`), because then
  `2+d_i=2+(2^m-2)=2^m` directly. It is **not** an equivalence with
  anything else, and it is **not** itself a surviving/safe length —
  reaching it is the failure mode. **The surviving (non-contradictory)
  condition is the negation**: every available theta `x`-`y` route
  length must satisfy `d_i\ne2^m-2` for all `m`, for the shared-port
  configuration to remain consistent with `G`'s F-cleanness (exact
  quote: *"retained as the exact shared-port template: every theta
  `x`-`y` route length must avoid `2^m-2`, for all `m`"*).

## S — S5 output

*Source: `contraction_block_cut_tree.md` III.1–III.2.*

- **Cut vertex:** `z` (proved to be a cut vertex of `G`, III.1: *"So
  `G-z` disconnects `V(L)\setminus\{z\}` from everything else: `z` is a
  cut vertex of `G`"*).
- **Degree four:** `\deg_G(z)=4` exactly (S5, cited).
- **The two lobes:** `G_1` (`=L`'s closure, `V(L)\cup\{z\}`), `G_2`
  (everything else).
- **Equality of lobe order:** `|G_1|=|G_2|` (S5, cited exactly).
- **Equality of lobe size:** `|E(G_1)|=|E(G_2)|` (S5, cited exactly).
- **Lobe containing the canonical theta:** `G_2`, entirely (exact
  quote: *"The other lobe `G_2` contains `\Theta` in its entirety"*).
- **Lobe containing the attachment-free leaf block:** `G_1` (`=L`
  itself, exactly).
- **Exact itinerary of the external-edge witness through `z`:** **not
  forced to pass through `z` at all**, in general (exact quote,
  `contraction_ma2_integration.md` Part IX: *"the third-edge witness
  `W_v`... need **not** pass through `z` at all in general... unless
  its chosen route happens to pass through `L` specifically (not
  forced)... No claim that `W_v` traverses `z` is made or needed"*).
  **This is recorded exactly as previously proved — not strengthened
  and not weakened here.**

## Summary: the three named outputs, exactly as established

Every central bridge (whether from a single-attachment-2 clean case,
cited directly to T1/T2, or from MA2's trichotomy) resolves to exactly
one of:

1. **A** — an admissible theta-attachment path pair, arithmetic
   template as above (open, finite, no contradiction).
2. **P** — a shared-port length-two path, arithmetic template as above
   (open, finite, no contradiction; `2^m-2` is the *forbidden* route
   length, not a safe one).
3. **S** — the precise S5 lobe-equality configuration, as above (open,
   one exact highly-constrained configuration, not a contradiction).

No new claim is made in this file beyond organizing these three exactly
as proved.
