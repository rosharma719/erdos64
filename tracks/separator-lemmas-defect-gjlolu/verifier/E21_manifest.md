# E21 canonical manifest — reconciling the 318 vs 547 discrepancy

**Purpose.** An external audit reproduced 318 (matching the pre-tie-fix
number) and flagged that 547 (post-tie-fix) was reported without a clear
account of which model each number belongs to. This file is the single
source of truth going forward; `experiments.md` E21 links here instead of
restating both numbers loosely.

## Exact provenance

- Commit at time of this manifest: `5b6e940803a66f753633c9b30e5481486e34ccd3`
- Script: `verifier/three_bridge_search.py`
- Function: `abstract_search()`, calling `candidate_lambdas()` then
  `check_T5_consistency_with_ties()` (current/canonical) or the removed
  `check_T5_consistency(tri, perm)` (historical, strict-permutation only —
  no longer present in the script; reconstructed here for the record).
- Command: `python3 verifier/three_bridge_search.py`
- Input universe: `candidate_lambdas(max_len=6, universe=range(1,9))` —
  all subsets of {1,...,8} of size 2 or 3 passing T2 (contains 2 values
  differing by 1 or 2).
- **Input spectra checksum:** 65 candidate Λ sets, SHA-256 of
  `repr(sorted(tuple(sorted(l)) for l in lambdas))` =
  `863b3b38527d17854cf46c3eacefdafe8e68eab99488e5e1d45f4533824e31f`
  (reproducible via the one-liner in this file's git history / by
  re-running `candidate_lambdas()` directly).

## Two models, precisely distinguished

Both numbers are **correct counts of two different things**. Neither is
an error; the earlier presentation didn't distinguish them clearly
enough, which is the actual defect being fixed here.

### Model 1 (historical, strict-permutation T5 check) — **318**

For each pairwise-cross-compatible Λ-triple, T5's maximality corollary
was checked by requiring **some strict total order** (c,e)-permutation
of the 3 bridges under which every self-sum-clean bridge sits at the
*unique* maximal position. A strict permutation can only place ONE index
at the maximal slot, so this model **structurally cannot accept** any
triple with ≥2 simultaneously self-sum-clean bridges — it treats a tie
as unrepresentable, not as consistent.

### Model 2 (current/canonical, ties-aware T5 check) — **547**

T5's actual mathematical content (two_cut.md §4b) only requires each
self-sum-clean bridge to be **weakly** maximal (≥ every other bridge,
ties allowed) — a strict total order is not required by the theorem.
Model 2 checks this correctly: any subset of self-sum-clean bridges can
always be made mutually consistent by setting their (c,e) equal at the
maximum, so the check is (correctly) always satisfiable once pairwise
cross-compatibility already holds.

### Exact reconciliation (recomputed and verified here)

Filters applied, in order, to the 65×65×65 (with repetition,
unordered) = C(65+2,3) = 46,690 raw Λ-triples:

1. **Pairwise cross-compatibility filter**: (Λᵢ+Λⱼ)∩F=∅ for all 3 pairs
   i<j (this alone leaves **547** triples — this is Model 2's exact
   count, since Model 2's T5 check never rejects anything beyond this
   filter).
2. **Model 1's additional T5 filter** (strict-permutation, no ties):
   removes every triple with ≥2 self-sum-clean bridges.

| # self-sum-clean bridges in the triple | count (after filter 1) | kept by Model 1 (strict) | kept by Model 2 (ties) |
|---|---|---|---|
| 0 | 77 | 77 | 77 |
| 1 | 241 | 241 | 241 |
| 2 | 203 | **0** | 203 |
| 3 | 26 | **0** | 26 |
| **Total** | **547** | **318** | **547** |

547 − 318 = 229 = 203 + 26, exactly the triples Model 1's strict
permutation could not represent. **No arithmetic error occurred in
either run** — the two scripts (before and after the tie fix) were
computing the closed-form counts of two different, precisely-stated
predicates over the same 547-triple base set. Verified by direct
recomputation on 2026-07-25 (both the historical strict check and the
current ties-aware check re-implemented side by side and run against the
same candidate set; see the reconciliation script output preserved in
this manifest's construction — reproducible via the commands above).

## What this number does NOT establish (repeated for emphasis)

Neither 318 nor 547 nor any subdivision above says anything about
**realizability** — whether any actual two-terminal graph B realizes a
Λ-spectrum in this abstract search space while also satisfying T1
(B+xy 2-connected), internal min-degree-3, and internal F-cleanness. Per
two_cut.md §7, this is *provably* insufficient on its own (the infinite
Λ₁=Λ₂=Λ₃={m,m+1} family survives every filter here for infinitely many
m). The realizable count from the bridge-signature library remains 0
through n=7, and is a completely separate, non-vacuous measurement (see
`verification_status.md` and experiments.md E19).
