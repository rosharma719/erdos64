# RETROSPECTIVE.md — process findings from the multi-branch Erdős #64 effort

**Written 2026-08-18 during the consolidation onto `consolidated/canonical`.**
This is a process document, not a mathematical one. It evaluates *how* the
work was done across fifteen never-merged branches (seven substantial),
using only findings that were checked against the actual branch contents
and git history. Where the received account of what happened turned out to
be wrong, the corrected version is given, because getting the process
diagnosis wrong is itself a process failure.

Nothing here changes the mathematical status: the conjecture is OPEN, and
`proof.md` is the ledger.

---

## 1. What worked

### 1.1 The label discipline — every branch that kept it caught its own errors

The rule is one line in every `plan.md`: *every assertion labeled PROVED /
COMPUTATIONALLY VERIFIED / CONJECTURAL / DISPROVED / KNOWN FROM LITERATURE;
no experimental pattern promoted to theorem without proof; failed
approaches kept with the exact obstruction.* It is the single highest-value
practice in the project, and the evidence is that **the errors it caught
were caught by the people who made them, before anything was built on
top**. Four concrete cases:

- **The additive-density formula.** "`α(H_N) = ⌊N/2⌋+1` exactly, extremal
  density exactly 1/2" was labeled PROVED after being read off `N = 2ᵏ`
  samples. Because the label carried an obligation to survive a
  smallest-counterexample search over the *general* case, that search was
  run and produced `{1,2,4,5,8,9,10} ⊂ {1..10}`, size 7 > 6. The formula
  was demoted to DISPROVED, the *valid* half (the C2 lower bound) was kept
  separately, and two downstream conclusions that had already been drawn
  from it — "the naive theta approach is dead" and "only a multiscale
  additive route remains" — were explicitly RETRACTED rather than left
  standing. Had the label been softer, the theta/additive track would have
  been abandoned on a false basis.
- **The vine charging lemma V1** ("#missing dyadic lengths ≤ D") was
  DISPROVED with an explicit witness (`n=13`, g6 `L?AB?vOLDPHa\`o`, `D=0`,
  missing `{4}`) and a violation rate (629 of 98,066 C4-free δ≥3 graphs at
  `n=10..15`), not with a vague "didn't work out".
- **The R2/S2 claim** was interrupted mid-derivation and then *audited
  rather than assumed*: T2's admissible pair need not include the shortest
  path, and the claimed length-9 object is not even simple. Refuted with
  explicit Heawood- and Balaban-derived counterexamples. The summary that
  had depended on it ("only component sharing and R2/S2 remain") was
  narrowed rather than quietly kept.
- **The literal `n ≤ 2D+3` target**, the entire motivating goal of the
  ordering-defect redirection, was DISPROVED in a single algebraic step —
  it is equivalent to `m ≤ (3n−1)/2`, contradicted unconditionally by
  `Σ(deg−3) = 2m−3n ≥ 0`. Recording it as a theorem-with-proof rather than
  as "this direction stalled" is what let the project pivot immediately to
  the `q(G)` ladder that actually worked.

The discipline also survived contact with *good* news, which is harder:
`O5` (the rigid-core K4-minor lemma) had two initially plausible hand-built
"counterexamples" that a direct SPQR computation rejected, and both were
**kept in the record as an error log** rather than deleted once the lemma
was proved.

### 1.2 Requiring ≥2 independent implementations — it caught real soundness bugs

Five distinct real errors in this project were caught by redundancy, not by
review:

1. **The hub over-materialization bug (the most serious).**
   `verify_passage_conflicts` materialized a full *supplying*
   triple/gadget — including attachments irrelevant to the claimed passage
   — and accepted a support whenever *any* cycle was found in that graph.
   That can succeed via an unintended cycle through the supplier's other,
   unclaimed edges, without ever using the passage supposedly being
   verified. **It was invisible to either algorithm's self-consistency**
   and surfaced only as a numeric disagreement between two structurally
   different implementations: 5,007 vs 5,052 verified minimal C8 supports
   on `(4,55,7)`. After the fix (materialize a minimal graph containing
   only the literally claimed passages) both agree exactly at
   **5,007 / 5,044 / 6,359**; the earlier 5,052 / 5,084 / 6,386 were each
   inflated by ~40–60 false-positive "verifications" and are retracted.
   This is the canonical case for the rule: a self-consistent implementation
   can be confidently, silently wrong.
2. **The girth-6 degree-collapse bug.** An exhaustive run reported
   `feasible=1` on hub topology #12 — a would-be counterexample. It was
   **stopped and investigated instead of reported**. Root cause: topology
   #12 has two parallel abstract edges between hubs 0 and 5, both assigned
   length 0; the adjacency was stored as a Python `set`, which silently
   collapsed the duplicate, leaving two hubs at degree 2. Not a
   counterexample — an invalid non-cubic graph passing an unguarded filter.
   Fixed with an explicit post-build degree validator applied *before* any
   cycle or labeling check, then rerun completely (1,294,670 compositions,
   0 feasible labelings).
3. **The weighted-incidence arithmetic error** (`t` → `2t` coefficient),
   found while deriving `q(G) ≥ 3`; the original was self-inconsistent with
   its own `t=1` worked example. Re-verified on 3,000 synthetic
   constructions after the fix.
4. **The Z5 48-vector compression failure.** A sample-derived compressed
   certificate was put through exact verification and **failed** with
   21,156 exceptions. The full 315-vector list was used instead, and the
   failure was recorded rather than the compression quietly dropped.
5. **A projection-formula bug** in the Z5 exact-lift resolution, caught
   during the independent NetworkX recheck of all 564 uncovered
   assignments.

Note the pattern in every case: the second implementation was
**structurally different** (a different algorithm, a different language, or
an independent library's primitives), not a second run or a refactor. Two
implementations sharing an assumption catch nothing. The strongest instances
in this repository use four detectors (Python DFS, networkx, a from-scratch
C implementation, and a SAT cycle-position encoding — the 86,047-graph
Type-B family) or two independently coded generators whose canonical outputs
must agree by **matching SHA-256** (the Type-B slot-matching families).

### 1.3 Using existing public extremal data instead of re-deriving

The 4-or-8 dichotomy through `n=19` — a statement *strictly stronger* than
Erdős–Gyárfás in that range — came almost free from McKay's published
`ex(n;{C4,C8})` table. For `n ≤ 17` the values are strictly below `⌈3n/2⌉`,
so no δ≥3 graph can be `{C4,C8}`-free at all, with **no case analysis**; at
`n=18,19` there is equality, so it reduces to checking min-degree on 570 and
304 extremal graphs. Compare the alternative that was being pursued: a brute
geng ladder that was killed at `n=12` after 947M of ~30 billion graphs,
growing roughly 50× per vertex, with `n=17` unreachable.

The lesson is not "look things up" but something sharper: **reformulating
the target into the shape of an existing published dataset converted an
unreachable computation into a table lookup plus 874 min-degree checks.**
The same move powered `type_b_equality_order.md` (McKay's checksummed
570-graph file eliminating a whole order layer) and Theorem B at order 30
(Royle–Markström's verified cubic `≥30` bound doing the work that
minimality would otherwise have to do, which is why Theorem B is *not*
conditional on minimality).

### 1.4 Treating claims from outside the current session as unverified

This one repeatedly paid for itself, and it should be an explicit house
rule. Every claim that arrived from another session, another sandbox, or a
pasted report was treated as CONJECTURAL until independently reproduced.
Concretely, that policy caught:

- **A vacuous theorem presented as progress.** The Bass–Ihara high-girth
  bound is *correct* — it was re-derived from scratch, independently
  confirming that for girth > r every closed non-backtracking walk of
  length `2r` traces a simple `2r`-cycle. But its hypothesis is girth ≥ 9,
  and **the (3,9)-cage has 58 vertices**, so no cubic 30-vertex graph
  satisfies it. Its advertised consequence at `n=30` is empty. Accepting it
  would have added nothing while creating the impression that order 30 was
  closing in.
- **An invalid application of a valid theorem.** The contraction theorem
  ("every edge lies on a `2ᵏ+1`-cycle") is correct step by step. Its claimed
  order-30 application is not: the quotient carries a degree-4 vertex, so it
  needs `G` globally minimal among *all* δ≥3 graphs, where only the `≥17`
  bound applies — not the cubic `≥30` bound. A follow-up round "fixed" a
  *different* problem (universal vs. existential quantifier) and left this
  objection untouched. Only an independent check of the hypothesis, not of
  the proof, finds this class of error.
- **A load-bearing number that was never derived.** In the length-16 tangle
  theorem — the first external submission whose artifacts actually arrived
  and matched their SHA-256 manifest — the 17-template classification
  reproduced **bit-for-bit** and was then re-derived **by hand**, entry for
  entry. But reading the reduction script line by line showed it merely
  *asserts* the spectral bound formula and checks that it evaluates to
  `1553220/29`. The derivation lives in a companion note that was never
  supplied. An independent cruder Ihara bound gives ≈50,719 instead of
  53,568, which changes every headline number. **Everything downstream of
  `N₁₆ ≥ 53568` is verified; the bound itself is not.**
- **An unjustified "linear defect growth" theorem** (`n ≤ 15q−17`), whose
  §§1–2 turned out to merely reconstruct this repository's own already-proved
  `h ≤ q`, with the genuinely new core lemma unverified — and which cites a
  branch (`codex/dyadic-passage-leap`) that exists in no local or remote ref.
- **A "provisional `q(G) ≥ 6`"** with elaborate counts (17,010 one-hub `q=5`
  configurations, 146 two-hub core classes, 17,969 three-hub cores) for
  which an audit against every ref's full history found **zero matching
  artifacts** — no file, no verifier, no manifest, no data, no commit.
  Meanwhile every `q=4` mention in the repository is an explicit statement
  that it was never attempted.
- **A fabricated order-38 census**, originally presented with broken
  reference links, an unverifiable checksum and a citation to a
  "Wormald–Kingan" theorem, with zero backing files. When real source later
  arrived from an inaccessible third sandbox, it was audited rather than
  accepted: **2 of 151** partition classes were reproduced from scratch and
  agree; the other 149 and the 60.9M-node aggregate remain unverified
  because the data files were never supplied.

The format that worked is worth copying verbatim:
`tracks/external-audits/verification_log_2026-08-06.md`, a table of
*claim → status → method → note* with exactly four statuses — **VERIFIED**
(checked myself, holds), **REFUTED** (checked myself, false), **UNVERIFIED**
(no code or data supplied, not cheaply checkable), **PLAUSIBLE**
(setup/reasoning sound, specific numbers unchecked). Note that VERIFIED and
REFUTED both require the auditor to have done work; "sounds right" maps to
PLAUSIBLE, and "no artifacts" maps to UNVERIFIED, never to acceptance.

Equally important, and easy to lose: the policy was applied **without
hostility and without paralysis**. The `t=4` order-30 filter was externally
supplied and *was* used — after its `allowed_bits` table was hand-checked
against the independently derived exact-interval theorem, its aggregate
output was cross-validated field by field against an independently written
census on 500 real quotients, and its claimed ~340× speedup was reproduced
locally. That audit cost a few hours and unlocked a 52.6-billion-marking
exhaustive closure in 4m30s.

### 1.5 Honest retraction culture

Disproved and superseded claims were kept in the record **with their exact
obstruction**, not deleted. `proof.md` Part VIII is a register of thirteen
of them. This matters in three specific ways that showed up in practice:

- The *valid residue* of a retracted result is usually salvageable, and you
  can only salvage it if you wrote down precisely what failed. The C2 lower
  bound survived the additive-density retraction; the narrowed C3 survived
  with it.
- Retracted numbers stay retracted. The inflated 5,052/5,084/6,386 passage
  counts are explicitly listed as superseded, so a later reader who finds
  them in an old file knows they are dead.
- A recorded dead end prevents a re-attempt. The `n ≤ 2D+3` disproof, the
  one-cell reduction disproof (with its smallest exact obstruction: 0
  shared edges, 0 common components, 2 divergent cells, both safe), and the
  FC-19/20/21 falsity each stop a future session from spending days on a
  known-dead target.

The best single instance is the **alternating ladder self-correction**: an
explicit infinite family was built to prove that no finite core list bounds
the incidence structure, and then the same line of work went back, found
that the family's premise (the identical-terminal row `X_x=y, X_y=x`) was
already excluded by an *ancestor commit's* pole-forcing theorem, and
downgraded its own result from "live Type-T residual" to "valid abstract
object, not a residual" — while keeping the mathematics. That is the
behaviour to reward.

---

## 2. What did not work

### 2.1 Duplicated effort — real, but much smaller than everyone believed

**This item's premise needed correcting, and the correction is itself the
finding.** The received account across several handoffs was that three
branches independently spent ~100 commits each duplicating the same
Type-T/C16 gadget-completion work with zero coordination. `git merge-base`
says otherwise:

| claim | reality |
|---|---|
| three uncoordinated parallel efforts | five of the seven branches form a **linear chain**; `codex/type-t-c16-continuation` = `claude/type-t-c16-compilation-x9ts7a` **+ one commit** |
| `codex/type-t-overlap-reduction` is a ~103-commit parallel line | it is `f8a11e0` **+ one commit**; the other 103 are the shared chain |
| the three lines were never reconciled | the chain tip `claude/graph-counterexample-q6-xerdjz` contains all of branches 2, 3, 5, 6 and 103 of branch 7's 104 commits |

So the **genuine** duplication is: at commit `f8a11e0` two lines took the
same handoff task; one added a single commit of gadget-level static
compilation on instance `(4,28,4)`, the other added ~17 commits that proved
the support-bound theorem and then pivoted to a passage-level projection
reaching `(4,55,7)` `m=2/3/4` complete. Roughly **1 commit of wasted
parallel work against 17 of productive work**, plus four identically-named
files with different content
(`type_t_port_c16_compilation.md`,
`verifier/type_t_port_c16_hypergraph.py`,
`verifier/type_t_port_short_conflicts.py`,
`manifests/type_t_port_c16_manifest.json`).

That is not nothing, but the **larger cost was the belief, not the
duplication**. Because the topology was never established, one branch's
README warned at length against merging (accurate when written, largely
obsolete once the chain absorbed the work), and another branch spent an
entire session building read-only snapshots of all fourteen branches
(≈3,300 files) purely to make them browsable — a consolidation effort that
this consolidation supersedes and that would have been unnecessary given a
five-minute `git merge-base` sweep.

A second, smaller instance is unambiguous: `verifier/certify_shard.sh` was
"fixed for a hardcoded Mac path" on the independent branch, while the chain
had already replaced the same script with a strictly more portable version
(`#!/usr/bin/env bash`, a `sha256sum`-or-`shasum` fallback, an argument-count
check, and a `make`-built `.build/check_c8`). Two sessions fixed the same
defect; only one fix survives.

**Diagnosis.** The failure was not "people duplicated work"; it was that
**nobody ran `git merge-base` before deciding what was duplicated.** Branch
topology is cheap to measure and expensive to guess.

### 2.2 The recurring overclaim has one specific shape: inducting a general formula from a special or small sample

Every overclaim in this project's history reduces to the same anti-pattern.
Naming it precisely is more useful than "be careful":

> **The `N = 2ᵏ` trap.** A quantity is sampled on a structurally special
> subsequence — powers of two, small orders, one instance, the extreme
> `(a,c)` corners — the pattern is clean, and the clean pattern is written
> down as a general formula.

Instances, all verified:

- `α(H_N) = ⌊N/2⌋+1` was read off `N = 2ᵏ` only. False at `N=10`.
- The bare-core cycle spectrum was reported for `j = 4,5,6` and for "all
  nine extreme/interior `(a,c)` cross-combinations" per `j`. Fitting 35
  affine forms to three points is *suggestive*, not a theorem — and the
  branch that did it said so, flagging form-completeness as an open gap and
  later closing it with an **independent kernel/cycle-space derivation**.
  That is the correct handling of the same trap, and it is why C16-2 is
  labeled PROVED rather than "verified for tested `j`".
- The Z5 48-vector compressed certificate was derived from a sample and
  failed exact verification with 21,156 exceptions.
- The claimed "`≈0` coverage" for Z5 bases 0, 1, 3 came from Monte Carlo and
  was simply **wrong** — the exact computation found 444, 0 and 48
  uncovered assignments.

**The check to run, every time:** before promoting a sampled pattern, ask
what is special about the sample (is it powers of two? the smallest cases?
one instance? the extreme parameter corners?) and then search deliberately
*off* that structure for the smallest counterexample. If the general
statement cannot be proved, keep the label at COMPUTATIONALLY VERIFIED with
the tested range stated explicitly — `INCOMPLETE_RANGE`,
`COMPLETE_RELATIVE_TO`, `BOUNDED_INCOMPLETE` all exist for exactly this and
were used well.

### 2.3 "Novelty supported by search" can never be upgraded here — a tooling gap, not a math gap

arXiv and every tested mirror return **HTTP 403 at the platform/proxy
level**, confirmed by direct `curl` through the egress proxy and not merely
by the fetch tool. Consequently **no full paper body was read for any
citation in this project**, with a single exception (Carr's four-page
preprint, obtained in full HTML — which is precisely why G1's audit is the
strongest one on record).

Everything downstream inherits that ceiling: S4, S5, G1, the `q(G)` ladder
and the one-pole theory are all capped at `NOVELTY SUPPORTED BY SEARCH`,
meaning only *"two targeted passes over abstracts and snippets found no
prior statement"*. Three of the load-bearing external theorems —
Gao–Huo–Liu–Ma's admissible-path theorem (used in O4′, T2, MA1, CB3′),
Dirac 1961 (used in O5's second proof) and Dirac 1953 — were matched to
their hypotheses from **abstracts and snippets only**.

This is a **tooling gap, and it should be treated as an action item, not as
a permanent property of the results.** Concretely:

- **Action:** obtain real literature access (institutional proxy, an
  allow-listed arXiv route, or a human collaborator who can fetch PDFs) and
  then re-audit L16–L24 in one pass. Several labels would likely move in
  one direction or the other, and one of them — the Gao–Huo–Liu–Ma
  hypotheses — is load-bearing for four separate lemmas.
- **Meanwhile:** where "supported by search" overstates what was actually
  done, say so. The 4-or-8 dichotomy through `n=19` already does this
  correctly with `NOVELTY UNCHECKED` ("may be implicit in the extremal
  tables"). That is the honest default when the search was not actually
  targeted and exhaustive.

### 2.4 The `plan.md` status log went stale while the work continued

This is the most easily fixed failure and it did real damage to
navigability. Verified: on `claude/graph-counterexample-q6-xerdjz`, the
**"Status log (newest first)" section's newest entry is dated 2026-07-25**,
while that branch's commits run through **2026-08-02** and include some of
the project's strongest results — F12, FC-15, the F13–F19 SAT series, the
Type-C closure, the even-order 3-connectivity corollary, cubic
3-edge-connectivity, the entire order-30 quotient census, the C16 `m=4`
closure, and five external-claim audits. **None of them appears in the
canonical log.** They exist only in ~40 scattered dated `.md` files and in
commit messages.

`verification_status.md` has the same problem one layer down: its execution
records stop at 2026-07-27, so the matrix does not cover the branch's own
last week of work.

The consequences were concrete and cost this consolidation real time:

- Two "current top priorities" propagated into handoffs **after they had
  been overtaken**: the "single Type-T yes/no question" (closed by the
  pole-forcing theorem — its host row `X_x=y, X_y=x` is excluded twice
  over) and "C16 `m=4` is the sole missing static layer" (`m=4` was closed
  on 2026-07-30; only the `m=5` rerun remains).
- An independent branch's session had to *discover* the other fourteen
  branches by inspection, because no log recorded that they existed.
- One file's own title (`order32_bounds_f19_extension.md`, "extending
  3-connectivity to every even order in [17,35]") contradicts its own
  closing prose ("the range `[17,33]` is unaffected"), on an incorrect
  ground — the kind of drift a same-session log entry forces you to notice.

**Rule:** the status log is updated **in the same session** as any dated
result file. No exceptions. A result that exists only in a dated `.md` and
not in the log is a process failure, not a record. If that feels like
overhead, note that it is three lines against a file that took a day to
produce.

---

## 3. What to codify going forward

1. **Keep the label discipline verbatim.** Every assertion labeled PROVED /
   COMPUTATIONALLY VERIFIED / CONJECTURAL / DISPROVED / KNOWN FROM
   LITERATURE. No experimental pattern promoted to theorem without proof.
   Failed approaches kept with the exact obstruction. Scope qualifiers
   (`INCOMPLETE_RANGE`, `COMPLETE_RELATIVE_TO`, `BOUNDED_INCOMPLETE`,
   `NOT_FORMALLY_VERIFIED`, `EXTERNAL_DATA_MISSING`) are part of the label
   and are never dropped when a result is quoted elsewhere.
2. **Two independent implementations for any COMPUTATIONALLY VERIFIED
   claim.** Structurally different — a different algorithm, language, or
   library — not two runs or a refactor. They must be compared on
   *numbers*, and any disagreement is investigated to root cause before
   either result is used. This rule is what caught the hub
   over-materialization bug, which no amount of reading would have found.
3. **Before starting a new structural sub-thread, search this repository's
   own history and status log first.** Run `git merge-base` across the
   relevant refs and `git log --all -S<symbol>` for the machinery you are
   about to build. Establishing topology takes minutes; guessing it cost
   this project a wasted duplicate commit, a redundant script fix, an
   unnecessary 3,300-file snapshot exercise, and two stale top priorities.
4. **Maintain exactly ONE `plan.md` status log as the durable ledger.** No
   more branch forks of it. If a branch must exist, it appends to the same
   log and merges back promptly; a long-lived branch with its own divergent
   ledger is how fourteen unmerged research lines happened.
5. **Any claim from outside the current session is CONJECTURAL until
   independently reproduced here, with artifacts.** Another branch, another
   sandbox, a pasted report, a prior session — all the same. Reproduction
   means checking the *hypotheses* as well as the proof (the contraction
   theorem was valid and its application was not) and reading load-bearing
   scripts line by line (the spectral bound was asserted, not derived). Use
   the *claim → status → method → note* table with statuses
   VERIFIED / REFUTED / UNVERIFIED / PLAUSIBLE. Auditing is not rejection:
   audit, then use what survives.
6. **Label arXiv-blocked novelty honestly.** Use `NOVELTY UNCHECKED — no
   literature access` wherever "supported by search" would overstate what
   was actually done, and reserve `NOVELTY SUPPORTED BY SEARCH` for claims
   that really did get two targeted passes. Record the access block as an
   open action item, not as a standing caveat.

Two further rules the work earned but never wrote down:

7. **Reformulate before you compute.** The biggest wins in this project came
   from changing the shape of the question — into McKay's extremal tables
   (unreachable brute force → a table lookup plus 874 min-degree checks),
   into passage-level variables (a 128.9×–206.7× clause reduction), into
   the triangle-quotient (order-30 graphs → order-16/18/20/22 quotients).
   The biggest sinks came from scaling the original formulation up.
8. **Never commit build products.** No `.pyc`, no `__pycache__`, no
   compiled binaries. Platform-specific `check_c8`/`check_g6` binaries
   caused repeated Mac/Linux churn until they were untracked; the hygiene
   test in `tests/test_repository_hygiene.py` now enforces this, including
   local-agent state directories.

---

## 4. The honest current frontier

The conjecture is open and nothing in this repository is close to closing
it; what exists is a conditional structure theory for a hypothetical
minimal counterexample, plus certified exhaustive eliminations in several
finite ranges. The live work, in priority order, is: **(1)** the joint
two-central-bridge Type-T interaction, never attempted despite being named
the highest-value target across an entire six-file sequence, with all the
machinery (MA2's trichotomy, the five-lemma arithmetic toolkit, S5's
uniqueness) already in place; **(2)** finishing the Type-T C16 catalog —
one mechanical `m=5` rerun against the now-complete `m=4` shadow, then
assembling the four-layer passage CNF, whose satisfiability is *entirely
unknown* (a complete conflict catalog is not evidence either way about
UNSAT); **(3)** the two unfinished near-cubic small-order layers `n=21`
(`4,3²⁰`) and `n=23` (`4,3²²`), cheap on the same certified pipeline that
closed `n=20` and `n=22` with zero survivors, once the six missing McKay
`.s6` files are restored; **(4)** the order-30 triangle-quotient census at
`t = 0,1,2,3`, where `t ≥ 4` is exhaustively closed and `t=3` needs the
order-24 catalog plus the same pre-use audit the `t=4` filter received;
**(5)** the `(6,7)`-kernel's C16 constraint, bounded to four parameter
classes with a fully pinned 16-vertex kernel each, whose identified
pressure point is that L5's `d=3` case dies on the no-C8 hypothesis rather
than on girth; **(6)** independently deriving — or refuting — the spectral
bound `N₁₆ ≥ 53568`, on which everything else in the length-16 tangle
theorem is already verified and which carries a 0.09% margin; and **(7)**
`q(G) ≥ 5`, whose case tables and path bounds are derived and ready but
which needs a genuinely better method, since the worst `q=4` row scales
roughly seven to eight orders of magnitude beyond `q=3`. Two items that
earlier handoffs listed near the top — the "single Type-T yes/no question"
and "C16 `m=4`" — are closed, and are recorded in `plan.md` as closed
precisely so they are not attempted again.
