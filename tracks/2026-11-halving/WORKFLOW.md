# Workflow: Claude and ChatGPT on Conjecture T

Two models with different tools, used as independent checkers of each other.
The user carries files between them, so each pass is **one round trip**.
Node statuses live in `BLUEPRINT.md`.

## Who does what

| | Claude (repo session) | ChatGPT |
|---|---|---|
| Tools | Repo and GitHub; nauty `geng`; C compiler; drat-trim; arXiv and web access; persistent workspace | Python and C++ sandbox; no repo access; no nauty; files only via the user |
| Produces | Large enumerations with certificates; literature and novelty checks; the blueprint; integration and commits | Long proofs and case analyses; falsification of candidate lemmas; independent small implementations |
| Checks | ChatGPT's proofs (blind re-derivation of short ones, step-by-step audit of long ones); reruns its computations with separate tools | Claude's proofs, completeness arguments and census methods |

- **Only Claude writes to the repo.** ChatGPT's results enter as claims from
  outside the session (repo house rule) until reviewed.
- **Strategy is shared.** Either model may propose a change of plan. Changes
  enter the blueprint only through Claude, with the reason recorded. Switching
  routes at an OR node needs the user's decision.

## One pass

1. **Plan (Claude).** Update `BLUEPRINT.md`. Choose 2–4 contracts: one main
   proof, one cheap decisive test, one audit of Claude's latest claims. Build
   one zip and one message the user can paste.
2. **Work in parallel.** ChatGPT works its contracts. Claude runs the heavy
   computation for the same pass.
3. **Return (ChatGPT).** One zip: changed or new files against the stamped
   commit, one return report per contract, and verdicts on Claude's claims.
4. **Integrate (Claude).** Apply on a branch, run its tests, check each claim,
   update statuses, commit, push.
5. **Decide (user).** Approve `REVIEWED` on central nodes (T1, I1, K1, D1, W1);
   choose a new route when a node is `REFUTED` or `OBSTRUCTED`.

## Rules

- **Two-model review.** A node reaches `REVIEWED` only after the agent that
  did not produce it has checked it. Short central proofs are re-derived blind,
  from the statement alone. `CERTIFIED` computations need two independent
  implementations that agree, with manifests.
- **Self-contained bundles.** Definitions inline; every file a contract needs
  is in the zip; the blueprint stamp names the commit. ChatGPT cannot look
  anything up in the repo.
- **Every contract names the node it moves and the decision it informs.** No
  computation without a hypothesis it can kill.
- **Red-team pass every few passes.** Each agent tries to break the other's
  top node. Run a literature check before any novelty claim.
- **Never upgrade a label silently.** Report the statement as proved, word for
  word, and how it differs from what was asked.

## Contract template (outbound)

```
Node:            <ID from BLUEPRINT.md>
Decision:        <what changes in the plan depending on the outcome>
Definitions:     <inline>
May use:         <node IDs, with statuses; anything not REVIEWED/CERTIFIED/KNOWN makes the result conditional>
Target:          <exact statement>
Deliverable:     <proof | counterexample search | implementation | audit>
Budget:          <rough effort>
Kill criterion:  <when to stop and report instead>
```

## Return report template (inbound)

```
Node:              <ID>
Proposed status:   <from the vocabulary>
Statement proved:  <verbatim>
Diff from target:  <hypotheses added or dropped; conclusion weakened or strengthened>
Artifacts:         <path, sha256> for each file
Tests:             <command and result>
If not finished:   breaking step (verbatim); smallest counterexample; strengthening that would make the step go through
Harvested:         <new CANDIDATE lemmas, each with an exact statement>
Audit verdicts:    <for each Claude claim in the bundle: VERIFIED | REFUTED | UNVERIFIED | PLAUSIBLE, with method>
```

The audit verdicts reuse the four statuses of
`tracks/external-audits/verification_log_2026-08-06.md`.
