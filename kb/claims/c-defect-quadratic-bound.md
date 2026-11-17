---
id: c-defect-quadratic-bound
title: "Minimal counterexamples satisfy n ≤ (3q² + 7q − 4)/2, hence q ≥ 5 (m ≤ 2n − 7)"
kind: claim
label: "SKETCH"
topics: ["defect", "2026-11-halving"]
doc_status: active
date: 2026-11-17
summary: "For a minimal counterexample with q = 2n − 2 − m ≥ 2, t(h) and K(h) are finite and n ≤ (3q² + 7q − 4)/2, so m ≤ 2n − √(2n/3) + O(1). With Garcia's lower bound n ≥ 24 this gives q ≥ 4 (m ≤ 2n − 6); with Ducoffe–Dumitru's n ≥ 41 it gives q ≥ 5 (m ≤ 2n − 7)."
evidence: ["kb/open/assets/2026-11-17-defect-quadratic-bound-screenshot.jpg", "kb/open/q-defect-growth-via-t-and-k.md", "tracks/2026-11-halving/q4_independent_check.md"]
depends_on: ["q4-independent-check", "q-defect-growth-via-t-and-k"]
---

# Minimal counterexamples satisfy n ≤ (3q² + 7q − 4)/2, hence q ≥ 5 (m ≤ 2n − 7)

## Statement

For a minimal counterexample with q = 2n − 2 − m ≥ 2, t(h) and K(h) are finite and n ≤ (3q² + 7q − 4)/2, so m ≤ 2n − √(2n/3) + O(1). With Garcia's lower bound n ≥ 24 this gives q ≥ 4 (m ≤ 2n − 6); with Ducoffe–Dumitru's n ≥ 41 it gives q ≥ 5 (m ≤ 2n − 7).

## Evidence

- `kb/open/assets/2026-11-17-defect-quadratic-bound-screenshot.jpg`
- `kb/open/q-defect-growth-via-t-and-k.md`
- `tracks/2026-11-halving/q4_independent_check.md`

## Caveats

Reported by another session (screenshot). The hand argument is not yet written in this repo, hence SKETCH; upgrade to PROVED when the write-up is added. **Computer check of the key lemma: PASSED** (recorded on the user's instruction, 17 Nov 2026; no log in the repo). The corollary arithmetic was rechecked on import: q = 3 gives n ≤ 22 < 24 and q = 4 gives n ≤ 36 < 41. If confirmed, q ≥ 5 strengthens the repo's q ≥ 4 (kb/core/proof.md P9–P12); compare the unsupported 'provisional q ≥ 6' (kb/notes/defect/defect_q_ge6_audit.md) and the unverified linear claim n ≤ 15q − 17 (kb/notes/defect/linear_defect_growth_audit.md).

## History

- 2026-11-17: created from a screenshot of another session's answer; computer check recorded as passed per user instruction.
