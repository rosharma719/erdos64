# A cubic minimal counterexample of even order in [17,33] has no 2-edge-cut
(new lemma — the edge-connectivity side of the separator program is
untouched territory until now)

## Status

[PROVED — a direct, elementary consequence of Whitney's standard
vertex/edge-connectivity inequality applied to the already-established
vertex-3-connectivity result. No new computation.]

`separator_theorem_order32_gap_analysis.md`'s own summary table (line 427)
flags this area explicitly: *"Cubic / cyclically 4-edge-connected variant |
Not started | Only S4 exists. No 2-edge-cut or 3-edge-cut lemma anywhere
in the repo."* This file supplies the 2-edge-cut case for the orders
already covered by `three_connectivity_general_order.md`.

## The lemma

**Theorem.** *Let `G` be a cubic (3-regular) minimal Erdős–Gyárfás
counterexample with `|V(G)|` even and `17<=|V(G)|<=33`. Then `G` has no
edge-cut of size `1` or `2` — i.e. `G` is 3-edge-connected.*

*Proof.* Write `κ(G)` for vertex-connectivity and `λ(G)` for
edge-connectivity. **Whitney's inequality** (standard, 1932): for any
finite simple graph, `κ(G) <= λ(G) <= δ(G)`. This holds because (a) any
minimum edge-cut can be turned into a vertex separator of size no larger
than itself by taking one endpoint from each cut edge on the smaller
side (giving `κ<=λ`, with the usual caveat for complete graphs, moot
here since `G` is far from complete at these orders and degrees), and
(b) the set of edges incident to any single vertex is itself an edge-cut
of size `deg(v)`, so the minimum edge-cut is at most the minimum degree
(`λ<=δ`). Both directions are textbook and not re-derived here.

`three_connectivity_general_order.md` already establishes `κ(G)>=3` for
every `G` in scope (no 2-cut, no cut vertex — i.e. `G` is 3-connected).
Separately, `δ(G)<=3` trivially: `G` is cubic, so `δ(G)=3` exactly.
Chaining: `3 <= κ(G) <= λ(G) <= δ(G) = 3`, forcing **`κ(G)=λ(G)=δ(G)=3`
exactly**. In particular `λ(G)=3`: the minimum edge-cut has size exactly
3, so no edge-cut of size 1 (a bridge) or 2 exists. ∎

## Why this is genuinely new, not a restatement

`lemmas.md`'s **S4** (cited throughout this project as already
establishing "bridgelessness") only rules out edge-cuts of size 1
directly, via a different, graph-theoretic argument specific to the
power-of-two-cycle structure (not via vertex-connectivity at all — S4
predates and does not depend on the 2-cut program in `two_cut.md`). The
**size-2** case was, per the gap-analysis table quoted above, genuinely
absent from this repo before now. This file closes it for free, as a
one-line corollary of work already done for an unrelated reason (the
vertex-separator program), rather than via new structural argument about
edge-cuts themselves.

## Honest scope

- **Cubic hypothesis is load-bearing here** (unlike
  `three_connectivity_general_order.md`, which is general). The `κ<=λ<=δ`
  chain only pins `λ` exactly when `δ` also equals the already-known
  lower bound on `κ`; for a non-cubic minimal counterexample (some
  vertices of degree `>=4`), this argument only gives `λ(G)>=3` (still
  useful — no bridge, no 2-edge-cut — but doesn't pin `λ` exactly, since
  `δ(G)` could then exceed 3).
- **Does not reach cyclic edge-connectivity.** Ordinary 3-edge-connectivity
  (no small edge-cut of *any* kind) is weaker than *cyclic* 4-edge-
  connectivity (no small edge-cut where *both* sides retain a cycle) —
  the latter is the property most useful for cubic-graph structural
  theory (snark theory, Petersen-minor arguments, etc.) and is **not**
  established here. This file supplies exactly what its title says: no
  2-edge-cut, nothing about 3-edge-cuts or cyclic connectivity, both
  still open exactly as the gap-analysis table recorded.
- **Order range inherited exactly** from
  `three_connectivity_general_order.md`: even orders in `[17,33]`
  (unaffected by `order32_bounds_f19_extension.md`'s Type A/B
  strengthening, since that file didn't move the binding `[17,33]` range
  either — Type C stayed at `36`).

## Computational sanity check

Not separately run — this is a one-step logical consequence of two
already-verified facts (Whitney's inequality is textbook; `κ(G)>=3` is
`three_connectivity_general_order.md`'s own COMPUTATIONALLY_VERIFIED
result), so there is nothing new to computationally cross-check beyond
what those two ingredients already carry. Flagged honestly rather than
padded with a redundant script.
