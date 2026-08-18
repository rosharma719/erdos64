# contraction_ma2_integration.md — S5 integration, Type T setup, and final assessment

**Standing reminder, per project discipline.** Every proof below is a
hand-written Markdown argument, cross-checked computationally wherever
the claim is unconditional. Nothing here is proof-assistant formal
verification. Closes out the multi-attachment resolution phase started
in `contraction_block_cut_tree.md` and `contraction_leaf_blocks.md`.

## Part IX: the S5 outcome, integrated (not re-derived)

**Restricted exactly to the central-bridge-induced configuration —
`lemmas.md`'s original cut-vertex program is not reopened.** From
`contraction_block_cut_tree.md` Part III: `z` is `G`'s unique cut
vertex, `\deg_G(z)=4`, exactly 2 edges into the attachment-free leaf
`L`, lobes `G_1=L`'s closure, `G_2\supseteq\Theta`, `|G_1|=|G_2|`,
`|E(G_1)|=|E(G_2)|`.

**Recorded precisely, as required:**
- **Lobe containing `\Theta`:** `G_2`, entirely (`\Theta` connects to `z`
  only through `K`'s other blocks, never through the attachment-free
  `L`, by definition of "attachment-free").
- **Lobe containing the attachment-free leaf:** `G_1=L`'s closure,
  exactly.
- **Remaining central-bridge attachments:** since `|A(B)|\ge3` and `L`
  contributes none (attachment-free), **all `\ge3` attachments lie in
  `K`'s *other* blocks — which are in `G_2`, alongside `\Theta`.**
- **Near-power witness traversal of `z`:** the third-edge witness `W_v`
  (`contraction_central_bridge.md` Part V) need **not** pass through
  `z` at all in general — its first excursion lies in `B_v` (proved
  there), and unless its chosen route happens to pass through `L`
  specifically (not forced, since the other `\ge3` attachments and
  `\Theta` are all reachable without touching `L`), `z` plays no role in
  `W_v`'s itinerary. **No claim that `W_v` traverses `z`** is made or
  needed.
- **Exact lobe signatures:** `G_1` = `L\cup\{z\}` with `z`'s 2 edges
  into `L`; `G_2` = everything else, `|G_1|=|G_2|`, `|E(G_1)|=|E(G_2)|`
  (S5, cited).

**Testing contraction/replacement for a smaller counterexample.**
S5's *own* proof technique is doubling a lobe at the cut vertex
(`lemmas.md` S5, Step 3). The equal-order/equal-size structure here is
*exactly* the setup that technique needs — but carrying it out would
require knowing `L`'s own internal cycle spectrum well enough to certify
that a doubled copy of `L` (glued to itself at `z`, forming a new
graph replacing `G_2`) introduces no forbidden cycle — precisely the
kind of fact this phase has not established about `L`'s internal
structure (only its *external* degree/2-connectivity properties, via
`contraction_block_cut_tree.md` Part III). **This specific replacement
test is not carried out here** — recorded as the precise next step,
distinct from (and not requiring) reopening S5's own general proof.

**Computational cross-check.** No new gadget beyond `block_cut_tree.py`'s
`check_attachment_free_leaf_s5`, which already confirms the lobe
edge-count split this Part restates; no further computation is added.

## Part X: Type T interaction — set up with MA2 available, not resolved

**MA2 is now available as a generic tool; the joint two-central-bridge
analysis at a shared Type T triangle is set up precisely, consuming
MA2 rather than duplicating its proof — but is not completed this
pass, exactly as flagged in `contraction_separator_integration.md`
Part IX as this sequence's single highest-value remaining target.**

For each cubic triangle vertex `v_i`, MA2 (applied to its own theta
`\Theta_{v_i}` and central bridge `B_{v_i}`) gives, independently: an
admissible pair (outcome 1, feeding `contraction_leaf_blocks.md` Part
VI's arithmetic), an S5 configuration (outcome 2, Part IX above), or an
attachment-rich leaf reducing to the shared-port template or a further
admissible pair (outcome 3, `contraction_leaf_blocks.md` Part VII). The
five priority questions, restated with the exact machinery now
available to answer them:

1. **Can both central bridges have attachment-rich leaf blocks?**
   Nothing established rules this out — no obstruction from any single-
   vertex MA2 application alone.
2. **Can the two blocks be the same block?** Requires knowing whether
   `\Theta_{v_1}` and `\Theta_{v_2}` (generally *different* theta
   systems, each built around its own cubic center) can share enough
   structure for `B_{v_1}`, `B_{v_2}` to coincide as literal subgraphs
   — not established either way.
3. **Do their attachment sets interlace on the corresponding theta
   systems?** A genuinely new intersection question, of exactly the
   `contraction_intersections.md` flavour but for *two* independently
   canonical bridges rather than two witness paths at one vertex — the
   existing cell-decomposition toolkit is the right starting point, not
   yet applied here.
4. **Does one bridge's admissible pair force a power cycle with the
   other vertex's triangle-pair witness?** This is exactly the kind of
   cross-witness arithmetic `contraction_atoms.md`/`contraction_mixed_witness.md`'s
   five-lemma toolkit was built for — applying it to an MA1-produced
   admissible pair against a triangle-pair witness (`contraction_atoms.md`
   III.2) is a concrete, well-specified next computation, not attempted
   here.
5. **Can both bridges produce the same S5 cut vertex?** By S5's own
   uniqueness, if both central-bridge analyses independently land in
   outcome 2, they **must** name the *same* `z` (there is only one
   cut vertex in all of `G`) — a clean, free consequence worth
   recording, though it does not by itself resolve whether outcome 2 is
   reachable from *both* vertices simultaneously in the first place.

**Honestly not completed.** Each question above is answered only to the
extent that MA2's machinery mechanically applies; none is resolved to a
definite yes/no. This remains the correct next target for a future
pass, now with the full MA2 apparatus available to attack it.

## Part XI: computation limits, honestly scoped

**No `q=4` census, no broad graph regeneration, no mining of the
order-9/defect-`q` populations.** All computation across this file and
its two companions (`contraction_block_cut_tree.md`,
`contraction_leaf_blocks.md`) was limited to exactly the permitted list:
block-cut-tree/attachment-core validation (`block_cut_tree.py`);
synthetic MA1/MA2 tests (same file); exact route-census enumeration in
one leaf block (`leaf_block_arithmetic.py`); shared-port/distinct-port
arithmetic (same file). No small-counterexample search against a
port-clean-pair target was needed, since Part VII/VIII's construction
resolved that question directly rather than requiring a search. No
existing project artifact was mined — the `data/`/`manifests/`
artifacts remain from the structurally unrelated defect-three phase, as
noted in every prior file of this sequence.

## Part XII: honest stopping-condition assessment

**Outcome 2 is the precise match: proof of MA2, and a reduction of the
attachment-rich branch to essentially one exact obstruction family.**

- **MA2 is proved** (`contraction_block_cut_tree.md` Part V), and
  sharpened in the proving (outcomes 1/3 alone already exhaust every
  case from the attachment core's mere existence).
- **Outcome 1 (admissible pair) is *not* eliminated** — reduced to a
  compact finite arithmetic template family (`contraction_leaf_blocks.md`
  VI.2), no contradiction forced, exactly as the task's own framing
  anticipated ("do not expect pure arithmetic to eliminate every
  tuple").
- **Outcome 3 (attachment-rich) is *not* eliminated, but is reduced
  further than requested:** its distinct-port sub-case collapses
  directly into outcome 1's *same* arithmetic (not a separate regime),
  leaving **only the shared-port template** as genuinely new content —
  a single, exact, checkable arithmetic obstruction (`d_i=2^m-2}`).
- **Outcome 2 (S5 configuration) is *not* eliminated**, reduced to one
  exact, highly constrained lobe-equality configuration
  (`contraction_block_cut_tree.md` III.2, restated precisely in Part IX
  above).

**So: MA2 proved; every one of its three outcomes survives, but each is
reduced to an exact, named, finite obstruction — an admissible-pair
arithmetic template, a shared-port arithmetic template, or one precise
S5 lobe-equality configuration — with no genuinely open "port-saturated"
or unresolved-topology case remaining.** This is not outcome 1 (no
admissible-pair elimination is claimed), not outcome 3/4 (no full
elimination of attachment-rich leaves or a single irreducible
port-saturated block, since none is shown irreducible — the reduction
eliminates the *category* rather than producing one hard example), not
outcome 5 (the S5 case is one exact configuration, not a further
reduction of the *whole* central bridge), and **not outcomes 6/7** —
**neither Type N nor Type T is eliminated this pass.**

**Concrete named next steps, not a vague list:** (1) Part IX's lobe-
replacement test, requiring `L`'s own internal cycle spectrum; (2) Part
X's five joint Type T questions, now fully set up with MA2's machinery
available but not yet executed; (3) `contraction_separator_integration.md`
VIII.2's still-open full determination of `\Lambda_0`, needed to close
the separator-outcome mapping completely. Across this entire six-file
contraction-phase sequence (`contraction.md` through this file), the
single most consequential open target remains the same one identified
several phases ago and reaffirmed here: **the joint two-central-bridge
interaction at a shared Type T triangle (Part X).**
