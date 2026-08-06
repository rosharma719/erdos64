# Verification report — "girth pair (6,9) closed" report, 2026-08-06

Standard format going forward for these external report pastes: claim →
status → method → note. Statuses: **VERIFIED** (checked myself, holds),
**REFUTED** (checked myself, false), **UNVERIFIED** (no code/data supplied,
not cheaply checkable), **PLAUSIBLE** (setup/reasoning sound, specific
numbers unchecked).

| # | Claim | Status | Method | Note |
|---|---|---|---|---|
| 1 | Two antipodal chords (any 2 of the 3 pairs) force a C8 | **VERIFIED** | Built all 3 literal 12-vertex configurations (6-cycle + both chords), ran exact `networkx.simple_cycles` | All 3 pairs give exactly one C8 each (plus five C6's, one C10). Confirms `s≤1`. |
| 2 | Doubled attachment (kernel vertex adjacent to both antipodal x's) forces two C7's | **VERIFIED** | Built all 3 literal configurations, exact cycle check | Matches this session's own earlier independent derivation of the same fact, now doubly confirmed. |
| 3 | "Previous roadmap invalidly used the girth-7 theorem to exclude 7-cycles inside the girth-6 branch" | **N/A to this session** | Searched `plan.md` for any such claim | No match — this session's own girth-6 work never made that inference. The underlying math point (girth=7 theorem assumes no cycle <7 anywhere; a girth-6 graph can still contain a 7-cycle) is correct regardless of who erred. |
| 4 | Girth pair (6,9): 516 kernel topologies (312 connected + 204 disconnected across m=3..9), zero survivors, SHA256 certificate | **UNVERIFIED** | No code, data, or certificate contents supplied (same placeholder-artifact pattern as prior reports) | Methodology (delete shortest odd 9-cycle + its 9 external neighbors, classify the resulting 12-vertex kernel, arc-length constraints avoiding {<6, 7, 8, 16}) is structurally sound and consistent with this session's own kernel technique applied to a different anchor cycle. Not dismissed, not trusted. |
| 5 | "Independent individualization-refinement generator" reproduced counts 135,136,40,1,0 | **UNVERIFIED**, internally consistent | Cross-checked against their own table | Matches their stated connected-kernel column (m=7,6,5,4 and one of 8/9) exactly, but this is a self-reported cross-check, not one performed by this session. |
| 6 | Bipartite sub-case: "every simple cubic bipartite graph on ≤58 vertices contains C4, C8, or C16" (external citation) | **CHECKING NOW** (order-30 case only) | `nauty-geng -c -C -b -t -f -p -d3 -D3 30 45:45` — generating the actual order-30 bipartite-girth≥6 population directly rather than trusting the cited bound | Running in background; the "58 vertices" figure is suspiciously identical to the unrelated (3,9)-cage number from this session's earlier girth-exclusion theorem, which raises (not confirms) suspicion of a conflation. Result to follow. |
| 7 | Reduction: girth-6 branch collapses entirely to the (6,7) girth-pair case | **CONDITIONALLY VERIFIED** | Follows deductively from #1 (VERIFIED) + #2 (VERIFIED) + #4 (UNVERIFIED) + #6 (CHECKING) | The logic chain is sound *given* #4 and #6 hold. Two of four supporting pillars are independently confirmed; two are not yet. Not promoted to a session-verified theorem until #4/#6 status resolves. |
| 8 | Proposed next theorem (C6/C7 intersection classification by shared-path length k) | Forward-looking proposal, not a result | — | Reasonable structural idea (θ(3,3,4) case correctly identified as matching the doubled-attachment structure), not evaluated further this round. |
