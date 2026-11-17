# Review of pass XII (ChatGPT) by Claude, 16 November 2026

Verdicts use the four statuses of `WORKFLOW.md`. The reviewer had read both
proofs before checking them, so these are step-by-step audits, not blind
re-derivations.

## Integration

- Base: ChatGPT worked from the pass XI archive, not from this branch (its
  `certification_manifest.json` says so). Its new files did not overlap
  anything changed since, so nothing needed rebasing.
- Committed as supplied, apart from three compiled binaries, Python caches,
  duplicate copies of the two top-level notes, and two renames to avoid
  clashing with repository files of the same names.
- `certify_pass12.py`, rerun in a scratch copy of this branch: all 13
  computational streams are bit-identical to ChatGPT's run. The two pytest
  logs differ only in timings (115 and 4 passed on both sides).

## Verdicts

| Claim | Verdict | Method |
|---|---|---|
| Tower theorem: clean triangle-built networks are exactly I, T, S, H | **VERIFIED**, with one gap closed below | Step audit; both composition tables recomputed independently |
| Cycle decomposition: crossing cycles use all three triangle edges; lengths `3 + X_A + X_B + X_C` | VERIFIED | Hand check: a dangling outer half-edge cannot be on a cycle, so a cycle entering a child uses its two connecting edges |
| Hamiltonian span, for all triangle-built networks | VERIFIED | Hand check of the induction: `(n_A − 1) + 1 + (n_C − 1) + 1 + (n_B − 1) = N − 1` |
| Interval lemma false for unclean pieces (Δ(I,I,T) has a pair with lengths {1,3,4}) | VERIFIED | Their test reproduces; consistent with the window rule |
| 20-row tower table and 35-row table with U: clean only for III, ITT, ISS | **VERIFIED** | Independent window arithmetic (my code, not theirs): same three survivors, windows [3,3], [5,7], [9,15] |
| Uniqueness of `H = Δ(I,S,S)` up to port-marked isomorphism | PLAUSIBLE as written; **VERIFIED** after the gap below | — |
| `H` is Exoo's H15 (explicit bijection) | VERIFIED | Their certificate reproduces; agrees with `check_three_pole_isomorphisms.py` |
| Decomposition Part A: 3-edge-connected cap ⇒ prime base `B ≠ K4` with listed letters | **VERIFIED** | Step audit. One implicit step: `H[S]` is connected because each component of a side of a 3-edge cut would need ≥ 3 boundary edges |
| Part C: a clean 1-pole doubles to a cubic counterexample, so it has ≥ 25 vertices | VERIFIED | Hand check, including the parity of a 1-pole's order |
| Parts B and C left OPEN | Correctly labelled | Now closed by `../joint_minimality.md` (Claude, PROVED-DRAFT, awaiting review) |
| 2-poles on 4 and 6 vertices: none clean | VERIFIED | Agrees with the certified census (none on ≤ 20) |
| Rooted fixture census, pole orders 3–11 | VERIFIED, fixture-dependent as labelled | Agrees with the certified census and the earlier catalog audit |
| Census orders 13–23 and 2-poles 8–22 marked OPEN | Superseded | Done on Claude's side: certified through 21 (3-poles) and 20 (2-poles); order 23 still open |

## The gap in the uniqueness step, and its closure

The proof says the connecting-port restrictions "determine [the]
terminal-marked isomorphism class uniquely". For `H = Δ(I, S, S)`, each `S`
must connect through its special port pair (the pair with lengths `[3,6]`),
but which end of that pair faces the identity vertex is not fixed by the
restriction. With two copies that is up to four orientations. They give
isomorphic results if skew H7 has an automorphism swapping the two ends of its
special pair while fixing the third port.

**Check:** it does. There is exactly one such automorphism, computed on
`FCZTO`. So all orientations give the same graph, and uniqueness holds.
Independently, the certified census finds exactly one clean 3-pole on 15
vertices.

## Status changes made in `../BLUEPRINT.md`

- K1 (tower theorem): **REVIEWED** by Claude; central node, so it awaits the
  user's sign-off.
- K1a: proved for clean pieces; false for unclean ones. K1b: proved. K1c: not
  needed.
- D1a (3-edge-connected caps): REVIEWED by Claude. D1b, D1c: closed by
  `joint_minimality.md`, which itself awaits ChatGPT's review.
