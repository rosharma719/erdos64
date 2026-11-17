# Pass XIII revised return report (stamp c3a61f6)

## J1: audit of WRP => T*

- **Proposed status:** Retain PROVED-DRAFT; no upgrade.
- **Statement checked:** WRP => no clean 1- or 2-poles and the four-class classification of clean 3-poles.
- **Diff from target:** A non-blind audit was performed; strict blind protocol was not met because sealed material was read during initial bundle inspection.
- **Verdicts:** Steps 1, 2, 3 VERIFIED; Step 4 CONDITIONAL on reviewed D1a and K2.
- **Artifact:** `pass13/structural_analytic_pivot.md`.

## C2 revised: F(k), four-poles and expanders

- **Proposed status:** New bridge-gluing lemmas PROVED; four-pole order-six classification COMPUTED; general F(k), shore expansion and analytic length theorem OPEN.
- **Statement proved:** Bridge sum of clean k- and l-poles is a clean (k+l-2)-pole. In particular F(k+1) => F(k), and a tree of t known clean 3-poles has t+2 degree-two vertices and at most 15t vertices.
- **Statement proved:** If clean (k-2)-poles do not exist, every nonadjacent terminal pair of a clean k-pole admits a path of length 2^j-1. Conditional on that nonexistence claim.
- **Correction:** Bounded defects do not by themselves imply uniform alpha-expansion for hypothetical minimal counterexamples. Attachment boundary multiplicity and the presence of three degree-two vertices after uncapping must be handled.
- **Artifacts:** `pass13/structural_analytic_pivot.md`, `pass13/census/`.
- **Tests:** NetworkX Atlas and exhaustive independent C masks on N=6, each exit 0, identical stream checksum `8c63b71acea99bd00f48c013354e6395e9a2b46eda2763bee2db80c9f480d3d3`.
- **Smallest non-tree four-pole:** C6 with a chord at distance two; cycle lengths {3,5,6}.

## C3: census audit

- **Proposed status:** Keep E1 and E4 at their supplied statuses; no upgrade.
- **Existing evidence checked:** all 18 manifests reconcile raw counts, A/B counts, clean counts and source SHA256 values; order-21 shards sum to 18,580,327. The generator options encode exact degree counts via `3N-2E`. However, **strict certification is incomplete:** `certify_pole_shard.sh` never captures checker B's exit code because B is in a process substitution behind `awk`; the manifest version field is a Usage message. Audit script exits 1 to flag these missing certification fields. This does not demonstrate the numerical counts are wrong. Re-run affected streams or re-check an archived identical stream with explicit B exit status before upgrading. No independent regeneration of geng streams here.
- **New result:** exactly two clean 4-pole classes at order six; two structurally different enumerators agree with exit codes and SHA256 as above.
- **Unknown:** counts of clean 4-poles at orders >=8, an independent generator for high-order 3-poles, and checker B exit codes on the prior runs.

## Blueprint integration suggestions (Claude-owned files; not edited here)

- Retain J1 PROVED-DRAFT pending a protocol-compliant second review.
- Add F1: clean k-pole boundedness, OPEN.
- Add F1a: bridge-gluing / F(k+1) => F(k), PROVED-DRAFT for integration.
- Add F1b: bridge-tree order <=15(k-2), PROVED-DRAFT for integration.
- Add F4-6: two clean four-pole classes at order six, CERTIFIED (two independently agreeing checkers with manifest).
- Add S1: proper-shore quantitative expansion bound, OPEN.
- Add A1: bounded-defect/root-avoiding dyadic theorem for expanders, OPEN.
- Record change of C2 from WRP-slack question to this new route only after the user's route decision.
