# Pass XII — status log and follow-on plan

## 2026-11-16: Pass XII local audit

- **PROVED:** All clean triangle-built networks are I, T, S, or H15 (identity as virtual 3-port). `tower_theorem.md` gives the all-order argument. The uniform H7 does not generate additional clean `K4`-root compositions.
- **PROVED:** A minimal clean 3-pole with a three-edge-connected cubic cap admits a root-preserving prime reduction; if the base is `K4`, it is already among the classified small poles.
- **OPEN:** 1-/2-edge cuts in arbitrary caps; hence full T-to-WRP reduction.
- **COMPUTED:** Independent Python and C verification for the tower profiles and the 20+35 composition tables, and fixture-based small-root checks. The actual `geng` order-13–23 and two-pole order-8–22 searches remain unrun.
- **COMPUTED:** Full *accessible pass-XI package* suite ran with exit 0 and 115 passing tests. No shared solver source was modified.

## Immediate branch-side actions (OPEN)

1. Checkout `claude/additive-reduction-brief` and read the actual PR #5; merge this additive directory and theorem notes; append the above status changes to `tracks/2026-11-halving/README.md` and its existing `plan.md` status log in the **same commit**.
2. Run the repository-supplied `geng`/`certify_shard.sh` jobs for 3-pole orders 13,15,17,19,21,23 and two-poles through 22. Retain per-shard generator and checker exits and stream SHA-256 values. Stop immediately on any verified outside-list survivor.
3. Investigate the one-/two-pole 1-/2-edge-cut cases of `decomposition_lemma.md`; do not declare WRP ⇒ T before these close.
4. Do not begin the identity/triangle-heavy doubling-chain lemma yet; exact WRP reduction is unfinished.

**Branch access:** unavailable in this run (GitHub host DNS not resolvable and GitHub connection uninstalled). The files in this workspace are staging artifacts, not a commit on the requested branch.
