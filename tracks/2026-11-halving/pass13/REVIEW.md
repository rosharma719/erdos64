# Review of ChatGPT pass XIII (16 November 2026, Claude)

Files reviewed: `structural_analytic_pivot.md`, `return_report.md`, `census/`.
They were committed exactly as supplied in 15d6650.

## Verdicts

| Item | Claim | Verdict |
|---|---|---|
| Prop. 1 | Bridge gluing: F(k+1) ⇒ F(k) | **Verified.** Attach a pendant triangle by a bridge to a defect vertex. This adds one defect and creates no cycle. |
| Prop. 2 | N(k) ≥ 15(k − 2) via bridge-trees of H15 | **Verified.** A path of t copies of H15 has 15t vertices and t + 2 defects. Tight against F_lin (`../linear_defect_bound.md`). |
| Prop. 3 | Terminal saturation | **Verified as conditional.** The conclusion holds only under the stated hypothesis that every terminal is saturated. It is not a theorem about minimal counterexamples. |
| Lemma | Deleting a cap from an α-expander leaves an α/2-expander | **Verified** for caps of bounded size relative to αn. The constant is fine. |
| Critique 1 | Existential F(k) gives no uniform expansion constant | **Agree.** This is the main gap. F_lin turns it into an exact linear inequality but does not close it (a violator is only forced to be 2-edge-connected). |
| Critique 2 | Shores can repeat endpoints (degree-1 vertices) | **Agree.** Fixed by stating F_lin in terms of deficiency, which counts repeated endpoints automatically. |
| A1, S1 | Proposed analytic and isoperimetric targets | **Adopted.** S1 becomes the isoperimetric corollary of F_lin. A1 is restated at defect density ≤ 1/15. |
| 4-pole order 6 | Two classes | **Reproduced** (same stream sha 8c63b71a…), and agrees with the 4-pole census through 20. |
| C3 audit | Checker B's exit code not captured; version field held a usage line | **Correct; fixed** in `scripts/certify_pole_shard.sh`. The full census was rerun under the corrected script; see the manifests. |
| `audit_prior_manifests.py` | Flags the old manifests | **Correct.** The old manifests are replaced. |

## J1 status

ChatGPT's J1 audit was not blind: it opened the sealed proof. **J1 stays
PROVED-DRAFT.** Promoting it needs a fresh ChatGPT chat that has never seen
`joint_minimality.md` to reconstruct Steps 1–4 from the statement alone.

## New from Claude in this pass

- `../linear_defect_bound.md`: Conjecture F_lin, |V| ≤ 15(δ − 2) for
  connected clean subcubic graphs, with its consequences, tightness, leaf
  reduction, isoperimetric form, and the limitation above.
- `../four_pole_census.md`: clean 4-poles through order 20, classified.
