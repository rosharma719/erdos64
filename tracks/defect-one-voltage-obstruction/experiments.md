# experiments.md — Erdős #64

Every experiment: command, params, output, interpretation, and a status label.
Newest at bottom of each section.

## E0. Detector construction & cross-validation  [COMPUTATIONALLY VERIFIED]
- `verifier/cycle_detect.py`: exact power-of-two cycle detector. Two independent
  existence routines: `has_cycle_len_dfs` (my backtracking, rooted at min vertex)
  and `has_cycle_len_nx` (networkx `simple_cycles(length_bound=L)`).
- `verifier/test_detector.py`: known graphs (K4→4, K3,3→4, Petersen→8 [girth 5,
  no C4, has C8], C7→none) + 400 random graphs.
- **Result:** 2107 (graph,L) existence checks, **0 disagreements**; every DFS
  witness structurally re-verified as a genuine simple L-cycle. Detector trusted.
- `verifier/check_g6.c`: independent C bitmask checker (no-C4 via common-neighbor
  popcount; no-C8/C16 via DFS). Validated against the Python detector: 3377
  random checks 0 mismatches, and identical graph counts/verdicts on the geng
  streams below.

## E1. Exhaustive counterexample search (reproduce L10: ctx ≥17 vertices)
Method: `geng -c -d3 n` (all connected graphs, min degree ≥3) piped to the
checker. Minimal counterexample is connected, so this finds the smallest
counterexample order. For n≤15 forbidden lengths are {4,8}; for n=16 add {16}.

| n | connected δ≥3 graphs | counterexamples | tool | time |
|---|---|---|---|---|
| 4 | 1 | 0 | py | 0s |
| 5 | 3 | 0 | py | 0s |
| 6 | 19 | 0 | py | 0s |
| 7 | 150 | 0 | py | 0s |
| 8 | 2,589 | 0 | py & C | 0s |
| 9 | 84,242 | 0 | py & C | 0.6s / 0s |
| 10 | 5,203,110 | 0 | py & C | 52s / 3s |
| 11 | 577,076,528 | 0 | C | ~7 min |
| 12 | **PARTIAL: 947,155,260 of ~30e9** | 0 (in partial) | C | killed (exit 144, CPU contention) |

**Interpretation so far [COMPUTATIONALLY VERIFIED]:** No counterexample on ≤11
vertices — independently reproduced by two methods (Python + C) with identical
graph counts through n=10, and 577M graphs at n=11 with the C checker. This
reproduces the lower portion of Royle–Markström's ≥17 bound from scratch (I have
independently re-verified n ≤ 11). **n=12 is NOT complete** (partial 947M/~30e9,
killed under CPU contention); do NOT claim n=12. Brute force past n=11 is the
wrong tool — pivot to CP-SAT UNSAT (E4), which prunes instead of enumerating, and
exploit C4-freeness. Full ≥17 by brute enumeration is infeasible here (~50×/vtx).
Reaching n=16 by brute force is likely infeasible here (graph count grows ~50×/
vertex); plan: push brute to ~n=12, then use C4-free edge bounds (Kővári–Sós–
Turán: C4-free ⇒ ≤ ½(1+√(4n−3))n edges) via `geng n mine:maxe` and/or CP-SAT to
go higher, reporting the exact boundary honestly.

## E2. (pending) Cubic exhaustive (reproduce L11: cubic ctx ≥30)
Plan: `geng -c -d3 -D3 n` (connected cubic) for even n, up to feasible order.

## E3. Track C — additive path-length study  [FLAWED SAMPLING — superseded by E3′]
`verifier/additive_study.py`: exact max independent set of H_N =
({1..N}, i~j iff i+j is a power of two). **Original sample (POWERS OF TWO ONLY):**

| N | α(H_N) | α/N | optimal |
|---|---|---|---|
| 8 | 5 | .625 | yes |
| 16 | 9 | .562 | yes |
| 32 | 17 | .531 | yes |
| 64 | 33 | .516 | yes |
| 128 | 65 | .508 | yes |
| 256 | 129 | .504 | yes |
| 512 | 257 | .502 | yes |

**METHODOLOGICAL ERROR (found 2026-07-24).** Every sampled N is a power of two —
the *one* subsequence where α=N/2+1 holds. Generalizing to "α(H_N)=⌊N/2⌋+1
exactly / density → 1/2" was never tested off powers of two, and is FALSE.
This is the sampling trap that let a false claim reach [PROVED]. See E3′.

## E3′. Corrected additive study — exact α(H_N), all N ≤ 32  [COMPUTATIONALLY VERIFIED]
Exact maximum independent set (networkx max-clique on the complement), **distinct-
summands** model, run 2026-07-24:

| N  | 1 2 3 4 | 5 6 7 8 | 9 10 11 12 | 13 14 15 16 | 17 18 19 20 | 21 22 23 24 | 25 26 27 28 | 29 30 31 32 |
|----|---------|---------|------------|-------------|-------------|-------------|-------------|-------------|
| α  | 1 2 2 3 | 4 4 4 5 | 6 7 7 7    | 8 8 8 9     | 10 11 11 12 | 13 13 13 13 | 14 15 15 15 | 16 16 16 17 |
| formula ⌊N/2⌋+1 | 1 2 2 3 | 3 4 4 5 | 5 6 6 7 | 7 8 8 9 | 9 10 10 11 | 11 12 12 13 | 13 14 14 15 | 15 16 16 17 |

Formula matches ONLY at N=2^k (and a few coincidences); exceeded whenever N is not
a power of two. Refutation witness: **{1,2,4,5,8,9,10} ⊆ {1..10}**, size 7, zero
distinct pairs summing to 2^k (verified), vs. formula's 6. True density > 1/2 for
most N (7/10, 11/18, 13/21); exact asymptotics OPEN — look up the reliable
sequence `1,2,2,3,4,4,4,5,6,7,7,7,8,8,8,9,10,11,11,12,13,13,13,13,14,15,15,15,16,16,16,17`
in OEIS interactively (oeis.org was Cloudflare-blocked to scripted fetch here).

**Two models to keep separate (see lemmas.md C2-upper):**
- *set / distinct summands* — the table above (a+b, a≠b).
- *multiset / equal lengths allowed* — two paths of length ℓ give cycle 2ℓ,
  forbidden iff ℓ is a power of two. A book/theta is a multiset, so the graph-
  relevant extremal function is the multiset one, NOT the table above. Recompute
  before any graph inference.

**Status of the conclusion:** the VALID lower-bound half of C2 still supports the
narrow C3 (single-scale distinct sums insufficient). The "naive theta approach is
dead / only multiscale remains" conclusion is RETRACTED. See lemmas.md, proof.md.

## E5. McKay extremal-file min-degree check + geng architecture validation  [COMPUTATIONALLY VERIFIED]
Software: nauty geng (built-in; `geng -f` = 4-cycle-free, `-d/-D` = min/max degree,
confirmed via `geng -help`), Python 3.14 venv networkx 3.6.1, trusted detector
`verifier/cycle_detect.py` (has_cycle_len_dfs / has_cycle_len_nx).

**(a) Extremal-file min-degree (downloaded `c48_nNeE.s6` from McKay).** For every
non-isomorphic {C4,C8}-free extremal graph, min-degree distribution:

**Current artifact status:** the eight `.s6` inputs are absent from this
checkout and their checksums were not recorded by the original run. The
integrity pass recorded checksums from temporary authoritative downloads in
`manifests/external_s6_manifest.json`, but did not restore the artifacts. The
historical results below remain `EXTERNAL_DATA_MISSING` and are **not currently
locally reproducible from this checkout alone**.

| n | e=ex | #graphs | min-deg distribution | #(δ≥3) |
|---|------|---------|----------------------|--------|
| 16 | 23 | 9473  | {1:1858, 2:7615} | 0 |
| 17 | 25 | 2580  | {2:2580}         | 0 |
| 18 | 27 | 570   | {2:570}          | 0 |
| 19 | 29 | 304   | {2:304}          | 0 |
| 20 | 31 | 94    | {2:94}           | 0 |
| 21 | 33 | 12    | {2:12}           | 0 |
| 22 | 34 | 13644 | {1:224, 2:13420} | 0 |
| 23 | 36 | 3257  | {2:3257}         | 0 |

Counts match McKay's page exactly. **Every** extremal graph has δ≤2 ⇒ the top edge
layer contains no δ≥3 graph at any n=16..23.

**(b) geng re-derivation, n=18 (independent of the extremal files):**
`geng -c -f -d3 -D3 18 | c8filter.py <cubic-degseq> --xcheck`
→ `total=2761 seqmatch=2761 C8free_survivors=0 detector_disagreements=0`.
All 2761 connected cubic C4-free graphs on 18 vertices contain a C8; DFS and nx
detectors agree on all 2761. Validates: (i) geng −f gives C4-free, (ii) the C8
reject filter, (iii) reproduces the extremal-file conclusion for n=18 from scratch.

**(c) geng re-derivation, n=19** (`geng -c -f -d3 -D4 19 29:29`, filter deg seq
4,3¹⁸, reject C8): RUNNING (higher volume; extremal file already proved 0 δ≥3).
Result recorded on completion.

## E6. (READY — not yet launched) n=20..23 one-below-extremal search
Top layer cleared by E5(a). Remaining 4 cases (see literature L15b / plan P1),
run order: (1) n=20 m=30 cubic; (2) n=22 m=33 cubic; (3) n=21 m=32 (4,3²⁰);
(4) n=23 m=35 (4,3²²). Command template (shard by `res/mod`):
`geng -c -f -d3 -D<maxdeg> N M:M res/mod | c8filter.py <degseq> [--save=...]`.
Per case record: exact command + geng version, shard manifest (all res/mod present),
raw generated count, degree-seq survivors, C8-free survivors, checksums, all exit
codes, independent rerun/checker comparison. **Any C8-free survivor disproves the
stronger 4-or-8 theorem** — save in g6+s6+edgelist immediately (c8filter `--save`).

## E4. (pending) CP-SAT counterexample model — DISCOVERY ONLY. For a certified
UNSAT: reduce to CNF (edge vars, exact degree-seq constraints, C4- and C8-exclusion
clauses, sound symmetry-breaking), run a proof-producing SAT solver, and check the
DRAT/LRAT certificate independently. A CP-SAT "UNSAT" status line is NOT a proof.
## E-global. Global-core adversarial atlas check (2026-07-25)
[COMPUTATIONALLY REPRODUCED; validation, not proof]

`verifier/global_core_check.py` exhausts `networkx.graph_atlas_g()` and selects
the connected graphs through order seven for which every proper subgraph has
minimum degree at most two. It found 12 such graphs. On all 12 it checked:

- the high-degree set is independent and every vertex touches a cubic vertex;
- `3|C|>=2n`;
- deletion of **every** cubic vertex leaves a 2-degenerate graph;
- `m<=2n-2` and the exact forward-deficit identity equals `q=2n-2-m`;
- every equality case `m=2n-2` has a C4;
- conditionally on C4-freeness, `m<=2n-3`, `q>=1`, and
  `sum(d-3)<=n-6`.

Counts: 12 selected, 6 equality cases, 0 C4-free cases, 0 failures. The C4-free
implications are therefore logically checked but vacuous in this very small
range; the equality boundary is exercised nonvacuously. Adversarial fixtures
also verify that `K4` realizes equality and contains a C4, `K5` is rejected as
nonminimal, and a nonempty 3-core is rejected by the 2-degeneracy peeler.

Reproduction:
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q tests/test_global_core_check.py`
and `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python verifier/global_core_check.py`.

## E25. Exhaustive normalized cyclic Z3 lifts (2026-07-25)
[COMPUTATIONAL ELIMINATION; independently reproduced]

The four certified 24-vertex cubic `{C4,C8}`-free, `C16`-positive bases have
cycle rank 13. `verifier/z3_lift_search.cpp` exhaustively tested every nonzero
normalized Z3 assignment, `4(3^13-1)=6,377,288`, without symmetry quotienting.
The exact stage counts are:

| base | C4 survivors | C8 survivors | C16 survivors | C32 | C64 |
|---:|---:|---:|---:|---:|---:|
| 0 | 1,594,322 | 54,458 | 0 | 0 | 0 |
| 1 | 1,594,322 | 570,806 | 0 | 0 | 0 |
| 2 | 1,594,322 | 750,140 | 0 | 0 | 0 |
| 3 | 1,594,322 | 170,342 | 0 | 0 | 0 |

The independent Python detector checked every one of the 6,377,288 post-C4
assignments and every one of the 1,545,746 post-C8 assignments, plus 1,024
deterministic random assignments and all eight stored witnesses: zero
disagreements. See `manifests/z3_lift_run_manifest.json` for checksums and
`z3_lifts.md` for the normalization and exactness proofs.

Conclusion, with exact scope: no connected cyclic Z3-lift of these four
specific bases is an Erdős--Gyárfás counterexample.

## E26. Leaf-R pattern and smallest-case replacement audit (2026-07-25)
[COMPUTATIONALLY REPRODUCED; diagnostic evidence, not proof of LR]

`verifier/leaf_r_patterns.py` streamed the checksummed E23/E24 artifacts in
their preserved common order; it generated no graph and recomputed no SPQR
tree. The 75,745 leaf records split as follows:

| orientation / witness | records |
|---|---:|
| genuine original remote R-leaf, real-edge C4/C8 | 72,927 |
| root-side R exposed after terminal-S suppression | 2,818 |
| exposed root-side records still having a real-edge C4/C8 | 2,210 |
| exposed root-side records needing the suppressed-S element in a contracted C4 | 608 |

The canonical dihedral word records pole/internal status, B-degree 3/higher,
and real/converted-suppressed-S edges. Exactly 42 nonempty equivalence classes
cover all records by definition; the 608 warning records occupy 15 exact and
seven coarse classes (562 rigid-forced and 46 SP-eligible). They are not LR
counterexamples because that R-node is not an original leaf in the pertinent
orientation and its suppressed side can contain the artificial closure edge
`xy`.

Independently, `verifier/leaf_r_replacement_search.py` ran
`geng -q -c -d3 n` for every `4<=n<=9` and tested all parent edges. Among
87,004 connected minimum-degree-three skeletons and 1,802,018 edge-rooted
pairs, ten parent deletions are C4-free and all ten contain C8. Hence every
unexpanded genuine leaf-R pertinent graph through skeleton order nine meets
LR* alternative 1; no clean case reaches the replacement test. This search is
a superset check for 3-connected R-skeletons, not an SPQR census or a proof at
arbitrary order. Reproducible records are
`manifests/leaf_r_patterns_manifest.json` and
`manifests/leaf_r_replacement_small_manifest.json`.

## E-struct. (planned) computational spot-check of B3/M3 on edge-minimal
C4∧C8-free graphs (validates the deletion-minimality reduction on real graphs).
## E2. (pending) Cubic exhaustive `geng -c -d3 -D3` (reproduce L11 cubic ≥30).

## E7. Defect-parameter data (redirection 2026-07-25)  [COMPUTATIONALLY VERIFIED]
`verifier/defect_model.py`: for every connected δ≥3 graph in a size range
(via `geng -c -d3 [-f]`), computes D=2n−2−m, checks the proved bound
D≤⌊n/2⌋−2 (defect.md §3b) and the disproof of the literal "n≤2D+3" target
(defect.md §4), and tests whether G−x₁ is 2-degenerate for every degree-3
vertex x₁ (defect.md §2b, the open gap toward m≤2n−4).

Commands: `python3 verifier/defect_model.py --nmin 4 --nmax 8` (generic
δ≥3) and `python3 verifier/defect_model.py --nmin 10 --nmax 15 --c4free`
(C4-free δ≥3, via `-f`, matching B0's hypothesis on G).

| run | n range | graphs | D≤⌊n/2⌋−2 violations | n≤2D+3 held (would refute §4) | every deg-3 x₁ 2-degenerate | some only | none work |
|---|---|---|---|---|---|---|---|
| generic | 4–8 | 2,762 | 0 | 0 | 111 | 60 | 2,133 |
| C4-free | 10–13 | 574 | 0 | 0 | 375 | 160 | 39 |
| C4-free | 14–15 | 97,492 | 0 | 0 | 33,428 | 48,430 | 15,632 |

**Interpretation.** Both proved facts (§3b, §4) hold with zero exceptions
on 100,828 graphs total, exactly as their unconditional proofs require —
consistency check, not new content. The 2-degeneracy check is genuinely
informative: the fraction of C4-free δ≥3 graphs where **no** degree-3
vertex gives a 2-degenerate remainder grows from 6.8% (n=10–13) to 16.0%
(n=14–15), so "G−x₁ is 2-degenerate for the right x₁" is not free — see
defect.md §5 for the smallest concrete witness (n=12, g6 `K?`DA_wdeQKc`).

## E8. Vine-graph cycle-spectrum experiment (redirection 2026-07-25)  [DISPROVED]
Candidate lemma V1: "a graph with D defects has ≤ D missing dyadic cycle
lengths among {4,8,…,≤n}" (defect.md §6).

**Pass 1 — `verifier/vine_experiment.py`** (`python3 verifier/vine_experiment.py`):
randomized path+chord "vine" construction, n=9..21, D=0..8 via 0–3 excess
chords on top of a minimal degree-3-completing chord set. 116 valid
instances generated; **0 violations** — but every instance has
num_missing∈{0,1} regardless of D, so this never tests the inequality's
real content (random chords make cycle-rich graphs). Kept as a documented
negative-methodology result, not evidence for V1.

**Pass 2 — reusing E7's exhaustive C4-free data** (the informative test):
every C4-free δ≥3 graph has 4 ∈ missing by definition, while D=0 occurs
(nothing forces D>0). `defect_model.py`'s C4-free run (n=10–15, 98,066
graphs) flags every (n,g6) with num_missing(spectrum) > D:
- **629 / 98,066 violate V1.**
- Smallest witness: **n=13, g6 `L?AB?vOLDPHa\`o`, D=0, missing=[4]**
  (1 > 0). Reproduce: `python3 verifier/defect_model.py --nmin 10 --nmax 15
  --c4free` (prints "smallest V1 violation" in the summary).

**Verdict: V1 is DISPROVED**, both by explicit small witness and by a
general argument (C4-freeness forces num_missing≥1 independent of D, and
D=0 is achievable). See lemmas.md V1, defect.md §6.

## E9. One-pole search (redirection 2026-07-25, task Part 5)  [COMPUTATIONALLY VERIFIED]
`verifier/one_pole_search.py`: generate connected min-degree≥2 graphs
(`geng -c -d2 n`), filter to "exactly one degree-2 vertex (root), all
others ≥3," check the full dyadic cycle spectrum with the validated DFS
detector. `verifier/one_pole_verify.py`: independent re-check of any
survivor with the nx-based detector (cross-validated in E0) on BOTH the
raw candidate and its doubled graph (S4's construction), plus an explicit
min-degree recheck of the doubled graph.

Command: `python3 verifier/one_pole_search.py --nmin 5 --nmax N`.

| n | connected min-deg≥2 graphs | one-pole candidates | survivors |
|---|---|---|---|
| 5 | 11 | 2 | 0 |
| 6 | 61 | 12 | 0 |
| 7 | 507 | 143 | 0 |
| 8 | 7,442 | 2,307 | 0 |
| 9 | 197,772 | 64,968 | 0 |
| 10 | (see below) | | |

n=5..9: **67,432 one-pole candidates checked, 0 survivors** (no candidate
avoids all of {4,8}; n=9 is below 16 so C16 is not yet in play). This is
COMPUTATIONALLY VERIFIED evidence only for n in the tested range, not a
bound for larger n — matches the honesty discipline used for E1.

**n=10: attempted, NOT completed in this environment.** `geng -c -d2 10`
generates enough graphs (min-deg≥2 count grows ~20-27x per vertex in this
range, so n=10 is plausibly >1e8) that the run did not finish within a
600s budget (the process was still at ~99% CPU after 6+ minutes when this
report was written; the current implementation also buffers the entire
geng stream into memory via `subprocess.run(capture_output=True)` before
processing a single line, which is the wrong strategy at this size). **Do
NOT claim n=10 exhaustive.** Fix needed before attempting it: stream
`geng` via `Popen` + line-by-line iteration instead of capturing all
output at once, and/or shard by `res/mod` as already practiced elsewhere
in this project (plan.md certification gate). Left as the next concrete
step rather than papered over.

## E10. Canonical-state / proof-DAG prototype (redirection 2026-07-25, task Part 6)  [COMPUTATIONALLY VERIFIED — prototype only]
**Scoping note:** no local P13-free search exists in this repo (L7/Track E
cites an external paper whose code is not reproduced here); reimplementing
it is out of scope for this pass. `verifier/state_search_proto.py` applies
the requested *methodology* (canonical-ish state memoization, a proof DAG
of failed completions, minimal-impossible-state extraction, cause
classification) to the one-pole incremental-construction search instead —
a search this project actually controls. State signatures use an
INEXPENSIVE APPROXIMATE canonical key (degree sequence + realized dyadic
cycle-length multiset), not full nauty canonicalization — recorded
honestly in the module docstring; this only risks redundant work, never
unsoundness, since a state is marked "dead" only after every successor
(isomorphism-collapsed or not) is exhausted, and a hard node-budget abort
(not silent truncation) prevents budget cutoffs from being mislabeled as
genuine impossibility.

Runs (both completed without hitting the node budget, i.e. genuinely
exhaustive within the stated max-n/deg-cap scope):
- `--max-n 6 --deg-cap 4`: 216 nodes visited, 27 dead states, 0 survivors.
- `--max-n 8 --deg-cap 4`: 1,227 nodes visited, 80 dead states, 0
  survivors.

**Extracted candidate reducible configurations (deliverable for task Part
6):** every dead state found at this scale is dead purely because the
degree-cap=4 / max-n bound was exhausted before reaching a valid one-pole
completion (cause classifier never reported "contains forbidden L-cycle"
in these two runs — the search never got large enough to hit a C4/C8
before running out of room). The **minimal impossible state is trivial**:
the empty 1-vertex root state itself, under deg-cap 4 and max-n 6 or 8, has
no completion — i.e. **the bound, not cycle-avoidance, is the obstruction
at this scale**. This is itself an honest, useful negative finding: it
means the interesting "forbidden-cycle-caused" dead states only start
appearing once deg-cap/max-n are large enough to reach length-4 or length-8
cycles at all, which the current prototype's scope does not yet reach — a
concrete next step (raise deg-cap to accommodate degree-≥4 vertices per
M1, and max-n past 8) rather than a claimed reducible-configuration set.
No cycle-caused impossible configuration was extracted at this scale;
reported as the honest (negative) Part-6 result, not padded into a false
positive.

## E11. O4/O4a computational test (redirection 2026-07-25, second pass, task Part 4)  [COMPUTATIONALLY VERIFIED]
`verifier/o4_analysis.py`: for every one-pole candidate (relaxed
population -- root r degree 2, else delta>=3, connected, cycles of any
length allowed, i.e. NOT required F-clean -- this is exactly what tells
us whether O4 needs F-cleanness/minimality or follows from
degree+connectivity alone), checks local vertex-connectivity of a,b in
K=H-r (does O4 -- 2 disjoint a-b paths -- hold directly?), and if not,
runs the full O4a analysis (minimum separator x, the two lobes, terminal
path spectra Lambda_1,Lambda_2, cross/self-sum dyadic hits).

Command: `python3 verifier/o4_analysis.py --nmin 5 --nmax 9 --path-cap 9`

| n range | one-pole candidates (relaxed) | O4 holds directly | O4 fails (needs O4a) |
|---|---|---|---|
| 5-9 | 67,432 | 67,386 (99.9%) | 46 (0.1%) |

**O4 (2 disjoint a-b paths) holds directly for the overwhelming majority
of small relaxed one-pole graphs -- it is close to "generic" behavior, not
a delicate minimality-dependent fact, at least at this size.** The rare
failures cluster at n=8-9 (smallest witness n=8, g6 GCQrUo); every
failure example found has small, near-symmetric lobes (|D1|,|D2| in {3,4}),
consistent with the failure mode being "the graph is barely big enough to
have 2 vertices >=3 outside {r,a,b} at all," not a subtle obstruction.

**Representative terminal spectra (>=10, satisfying task Part 4 item 5):**
all 10+ O4-failure witnesses at n=8-9 were recorded with their
Lambda_1,Lambda_2 (see raw run output); e.g. n=8 g6 GCQrUo: Lambda1=
Lambda2=[3,4], cross-sum hits dyadic {8}, both self-sums hit dyadic {8} --
meaning doubling EITHER lobe at both terminals would immediately create an
8-cycle (self-sum 4+4=8, since 4 is in Lambda_i), so neither lobe survives
the two-terminal doubling criterion here (one_pole.md's Lambda_i+Lambda_i
condition), consistent with 0 one-pole survivors found anywhere so far.
n=9 g6 H?`bcrn: Lambda1=[2,3,4,5], Lambda2=[2,3,4], cross-sum hits {4,8},
both self-sums hit {4,8} -- same conclusion, more severely (even the
CROSS-lobe combination, which is guaranteed safe by H's own F-cleanness in
a genuine survivor, hits dyadic here -- confirming this particular relaxed
graph is NOT itself F-clean, as expected since we did not filter for
F-cleanness in this pass).

## E12. SPQR-based classification (redirection 2026-07-25, task Part 5)  [COMPUTATIONALLY VERIFIED]
`verifier/spqr_analysis.py`: uses the `spqrtree` PyPI package (pure-Python
implementation of the Gutwenger-Mutzel 2001 SPQR-tree algorithm -- a real
published algorithm, not a custom heuristic) to decompose K+ab (K=H-r) for
every relaxed one-pole candidate and classify node types (S=series,
P=parallel, R=rigid, Q=edge).

Command: `python3 verifier/spqr_analysis.py --nmin 5 --nmax 9`

| n range | candidates | K+ab has a cut vertex (SPQR inapplicable) | pure series-parallel (no R), of the rest | contains >=1 rigid node, of the rest |
|---|---|---|---|---|
| 5-9 | 67,432 | 174 (0.3%) | 0 (0.0%) | 67,258 (99.7%) |

Node-type totals across all classified candidates: R=69,686, S=6,083,
P=5,482.

**Two findings, both informative:**
1. **"K+ab has a cut vertex" occurs 174 times in the relaxed population --
   this is O3's real content, not a free structural fact.** one_pole.md's
   O3 proof (H fully 2-connected) is conditional on H being master-minimal
   AND F-clean; the 174 counterexamples here confirm that without that
   hypothesis, a one-pole graph's K+ab genuinely can have a cut vertex
   (SPQR requires 2-connected input, so these were skipped, not silently
   misclassified). Smallest witness: n=7, g6 FQhVo.
2. **At this small size, essentially every one-pole candidate's SPQR tree
   contains at least one rigid (R) node -- "pure series-parallel" (fully
   explained by the Lambda_i+Lambda_j path arithmetic alone) essentially
   never happens for n<=9.** Smallest example overall: n=5, g6 DV{, a
   single bare R node (K+ab is already minimally 3-connected, no 2-cut at
   all). This means, per one_pole.md's SPQR scoping section, that
   rigid-piece analysis (the "only place ear decomposition is still
   needed") is already the dominant regime even at the smallest sizes --
   the series/parallel path-arithmetic alone will not suffice for most
   candidates; the next concrete target is understanding cycle structure
   INSIDE R-node skeletons, not extending the S/P arithmetic further.

## E13. Rigid-core lemma verification (redirection 2026-07-25, third pass, task Part 1)  [PROVED + COMPUTATIONALLY CROSS-CHECKED]
`verifier/rigid_core_check.py`: regression-checks the two flawed hand-built
"counterexamples" from the first attempt at O5 (both are rejected as
non-series-parallel, confirming the SPQR computation catches the earlier
hand-reasoning error -- see one_pole.md O5 for the full account), then
exhaustively tests "every nontrivial 2-connected series-parallel graph has
>=2 degree-2 vertices" against every 2-connected graph `geng` can generate
for n=3..8.

Command: `python3 verifier/rigid_core_check.py --nmin 3 --nmax 8`

| n range | 2-connected graphs | series-parallel (no R node) | violations |
|---|---|---|---|
| 3-8 | 7,661 | 304 | 0 |

**0 violations across all 304 series-parallel graphs found** -- matches
the proof in one_pole.md exactly (proof via SPQR-tree leaf structure: every
leaf of a nontrivial SP graph's SPQR tree is an S-node contributing >=1
purely-local degree-2 vertex, and a tree with >=2 nodes has >=2 leaves).

## E14. Edge-rooted (G,e) search (redirection 2026-07-25, third pass, task Part 6)  [COMPUTATIONALLY VERIFIED]
`verifier/edge_rooted_search.py`: direct search over (G,e) pairs (G
connected delta>=3 from `geng`, e any edge) testing the suppressed-edge
equivalence's 2 conditions (G-e has no 2^k-cycle; no e-using cycle has
length 2^k-1) -- a full failure of both is exactly a one-pole survivor
after subdividing e (one_pole.md's suppressed-edge reformulation).

Command: `python3 verifier/edge_rooted_search.py --nmin 4 --nmax 8`

| n range | (G,e) pairs tested | full failures (one-pole survivors) | near-misses (dist<=1 to nearest 2^k-1) |
|---|---|---|---|
| 4-8 | 47,349 | 0 | 0 |

n=9 (84,242 connected delta>=3 graphs) attempted, **NOT completed**
(per-edge SPQR + path enumeration is too slow at this size within the
budget used here -- terminated after ~115s, no partial data trusted).
Do NOT claim n=9. The forbidden-minus-one set only starts containing
values beyond {3} at n>=7 (2^3-1=7), so near-miss data is genuinely thin
at this scale; n=9-10 (reaching 2^4-1=15) is the natural next target with
a faster implementation (streaming geng, caching SPQR per graph instead
of per edge).

## E15. SPQR composition-rule verification (redirection 2026-07-25, third pass, task Part 4)  [PROVED + INDEPENDENTLY VERIFIED]
`verifier/spqr_signature.py`: implements the series/parallel Sigma(P)
composition rules (one_pole.md's rooted-SPQR-signature section) and
cross-checks them against brute-force exhaustive path/cycle enumeration
on the concretely assembled graph, for a battery of series compositions
(path lengths 1-3 x 1-3) and parallel compositions (2-4 branches, lengths
1-4). **All tests passed exactly** (`python3 verifier/spqr_signature.py`
-> "ALL composition-rule tests PASSED").

## E16. K4 rigid-skeleton search (redirection 2026-07-25, third pass, task Part 5)  [COMPUTATIONALLY VERIFIED, exploratory]
`verifier/spqr_k4_skeleton.py`: derives the C4-freeness restriction on
K4's 6 edges (at most 4 of 6 can be real without some quadrilateral being
entirely real -- an immediate C4; verified exhaustively over all 2^6
real/virtual patterns), then runs a bounded search over small candidate
virtual-edge spectra ({2},{3},{2,3},{3,4},{2,4},{5}) for all 7^6=117,649
edge-assignment combinations.

| total configs | forced C4 | forced other dyadic (8,16,...) | skeleton-level F-clean |
|---|---|---|---|
| 117,649 | 10,945 | 101,179 | 5,525 (4.7%) |

Smallest skeleton-clean example found: edges (1,2),(1,3),(1,4) real,
(2,3)->{3}, (2,4)->{5}, (3,4)->{5}, giving cycle spectrum {5,7,10,12,13}
(no dyadic hits). **This is a skeleton-level result only** -- it does not
certify a full one-pole survivor (each virtual edge's spectrum must still
be realized by an actual gadget with its own F-clean internal cycles, not
tracked at this level). Reported as a candidate direction, not a proved
reducible configuration.

## E17. O7-filtered K4 census (redirection 2026-07-25, fourth pass, task Part 6)  [COMPUTATIONALLY VERIFIED]
`verifier/spqr_k4_skeleton.py` (extended): applies O7's triangle
restriction to the 5,525 skeleton-clean K4 configurations from E16.
**Modeling caveat, stated explicitly:** the original E16 search only
tracked each edge's spectrum, not which SPQR node TYPE a virtual edge's
child actually is; this refiltering treats every virtual edge as
representing a remote-leaf-R-child (the natural reading given the
section's focus on rigid pieces), not a mix of S/P/R child types. A more
refined refiltering that distinguishes child type is future work.

Command: `python3 verifier/spqr_k4_skeleton.py` (O7 section runs after
the main search).

| input (E16 skeleton-clean) | O7 survivors | distinct edge patterns | orbits under K4 automorphism |
|---|---|---|---|
| 5,525 | 4,717 (85.4%) | 14 | 4 |

The 4 orbit representatives (#real edges = 3,2,1,0) are listed in
one_pole.md's "O7-filtered K4 census" section.

## E18. One-R-node target search (redirection 2026-07-25, fourth pass, task Part 7)  [COMPUTATIONALLY VERIFIED]
`verifier/multi_r_search.py`: searches the relaxed one-pole population for
candidates with ≥2 R-nodes in the SPQR tree of K+ab, checks O6/O7 on
every leaf R-node found.

Command: `python3 verifier/multi_r_search.py --nmin 5 --nmax 8`

| n range | one-pole candidates | ≥2 R-nodes | F-clean among them | leaf passes O6+O7 fully | leaf fails O7 (ext. common neighbor) |
|---|---|---|---|---|---|
| 5-8 | 2,464 | 118 (4.8%) | 0 | 26 | 108 |

**No F-clean multi-R-node survivor found (expected).** The key finding:
**26/118 relaxed multi-R candidates have a leaf R-node satisfying every
currently-proved local condition (O6's hypotheses + O7's conclusion)
while the overall graph is still not F-clean** — smallest example: n=8,
g6 `GCQVRw`, root 2, leaf R-node poles (7,0) with lex_smaller=True and
O7_holds=True, yet the whole graph has a forbidden 4-cycle unrelated to
that leaf's own root-cycle mechanism. **Diagnosis:** O6/O7 only constrain
cycles running through one specific leaf's own poles; they say nothing
about cycles elsewhere in the graph. Per the explicit instruction not to
label "exactly one R-node" a conjecture prematurely: **it is not labeled
here** — the data shows O6+O7 are demonstrably insufficient on their own
(26 counterexamples to "O6+O7 at every leaf implies F-clean"), and the
"additional condition" that would close the gap is not yet identified.
Recorded as the honest open state, not papered over with a false
conjecture.

## E19. Bridge-signature library (redirection 2026-07-25, fifth pass, task Part 5)  [COMPUTATIONALLY VERIFIED, empty at this scale]
`verifier/bridge_signature.py`: enumerates two-terminal graphs B
(terminals x,y) satisfying T1's exact hypothesis (xy absent from B and
modeled separately, B+xy 2-connected, internal min degree >=3, internal
cycles F-clean). The complete path spectrum Λ(B) and the explicitly named
**dyadic internal-cycle spectrum** C_F(B)=C(B)∩F are computed by two
independent methods and cross-checked. C_F is not described as the full
cycle spectrum.

Command: `python3 verifier/bridge_signature.py --nmin 3 --nmax 7`

| n range | (graph,x,y) candidates checked | qualifying bridges | distinct signatures |
|---|---|---|---|
| 3-7 | 19,845 | 0 | 0 |

**0 qualifying bridges found through n=7.** Investigated directly: a
natural small candidate (x, y, 3 internal vertices forming a triangle,
each internal vertex getting one extra edge to x or y) passes T1's
2-connectivity requirement and the degree requirement, but contains an
internal C4 (verified: vertices x,v1,v3,v2 form a 4-cycle) — an explicit
illustration of why the library is empty this small, not just an
unexplained gap. n=8 attempted, did not complete in the time budget used
(O(n^2) candidate pairs x expensive per-pair 2-connectivity + full path
enumeration). **Do not claim n=8.** Matches the project's broader pattern
that avoiding even a single C4 is already restrictive at small n
(consistent with B0/M1/L15-style small-order results elsewhere).

## E20. Bridge compatibility search (redirection 2026-07-25, fifth pass, task Part 6)  [COMPUTATIONALLY VERIFIED, empty at this scale — consistent with E19]
`verifier/bridge_compatibility.py`: builds on E19's library and now searches
**only** T4's exact Type A/B/C families. Types A/B apply T5 before the
pairwise cross-spectrum check; Type C enforces its exact no-edge terminal
coverage conditions. Every candidate record includes the bridge type,
terminal degree profile, (cᵢ,eᵢ), self-sum/internal cleanliness, T5,
cross-compatibility, and abstract/graph-realizable status. Accepted graph-
realizable candidates are independently rechecked with both detectors.

Command: `python3 verifier/bridge_compatibility.py --nmin 3 --nmax 7`

With E19's library empty at this order range, there is nothing to search
over — 0 typed candidates and 0 assembled graphs. **This is vacuous and
not a separate negative result.** Nonvacuous synthetic regression fixtures
exercise valid and rejected Type A/B/C paths, including equal and partially
tied T5 cases, even when the real library is empty. The graph-realizable
pipeline remains ready for a nonempty library.

## E21. Abstract additive conditions proved insufficient (redirection 2026-07-25, seventh pass, corrects the sixth-pass entry)  [PROVED + COMPUTATIONALLY VERIFIED]
**Correction to the sixth-pass E21 entry.** The earlier "tie modeling
limitation" caveat undersold what's actually true: two_cut.md §7 now
**proves** (not just notes as a gap) that T2+T4+T5+pairwise
cross-compatibility are jointly insufficient to exclude Type A
abstractly, via an explicit infinite family. `verifier/
three_bridge_search.py` is corrected accordingly: the old strict-permutation
check is retained under an explicitly historical model name solely to
reproduce 318, while `check_T5_consistency_with_ties` supplies the corrected
semantics (always satisfiable abstractly once ties are allowed). A new
`verify_infinite_equal_signature_family` function directly checks the
Λ₁=Λ₂=Λ₃={m,m+1} family.

Command: `python3 verifier/three_bridge_search.py`

**Infinite family, verified directly:** 1,979 of the first 1,999 integers
m give Λ₁=Λ₂=Λ₃={m,m+1} with (Λᵢ+Λⱼ)∩F=∅ for every i,j (including
self-sums) — e.g. m=5,6,9,10,11. This alone proves the insufficiency
claim; no search is needed to establish it.

| stage/model | count | interpretation |
|---|---:|---|
| size-2/3 subsets of {1,…,8} | 84 | deterministic generated input |
| spectra passing T2 | 65 | input to triple enumeration |
| triples with replacement | 47,905 | before cross-spectrum filtering |
| pairwise cross-compatible | 547 | abstract additive survivors |
| old strict-order model | 318 | **incomplete historical model**; ties were unrepresentable |
| corrected tied-signature model | 547 | current regression count |
| newly represented | 229 | exactly 203 with two clean bridges + 26 with three clean bridges |
| graph-realizable | 0 | vacuous consequence of E19's empty n≤7 library |

The direct set-difference regression proves that the 229 restored triples
are **exactly** the cross-compatible triples with at least two self-sum-clean
bridges, i.e. precisely the cases that need a partial or three-way maximum
tie and therefore could not be represented by the old strict permutation.
Canonical provenance is recorded in `manifests/E21_manifest.json`.

Both 318 and 547 are **regression data only**. The first is an incomplete
model count; the second is the corrected abstract count. Neither is evidence
toward resolving Erdős–Gyárfás or excluding Type A. Likewise, “0 realizable”
is explicitly vacuous at this range because the real bridge library is empty.

**Recorded conclusion, per instruction:** abstract additive conditions
are insufficient; the remaining problem is realizability by degree-
constrained two-terminal graphs. The project's live search is now
`verifier/bridge_closure_search.py` (E22), not this script.

## E22. Bridge-closure generation, linkage-data identity, and near-gadget ranking (redirection 2026-07-25, seventh pass, task Parts 4, 6-8)  [PROVED + COMPUTATIONALLY VERIFIED]

**Symmetric-difference identity** (`verifier/linkage_data.py`,
two_cut.md §11): |P|+|Q| = 2ω(P,Q) + Σ(cycle lengths in the edge-disjoint
decomposition of the symmetric difference), verified via two independent
computations (direct edge-set arithmetic for ω, greedy cycle-peeling for
the decomposition) on a battery of 7 hand-built path pairs (disjoint,
overlapping, identical, diverge-immediately cases). Command:
`python3 verifier/linkage_data.py` → "ALL IDENTITY TESTS PASSED".

**Bridge-closure generation** (`verifier/bridge_closure_search.py`,
two_cut.md §13): generates J=B+xy by reusing the (frozen) one-pole search
structure directly — x at degree exactly 2 is precisely a one-pole root,
relaxed to allow d_J(y)≥2 rather than ≥3. Deletes the distinguished edge
to recover B; computes Λ(B), h(B), the disjoint-pair spectrum 𝒟(B),
minimum witness overlap, and SPQR type, cross-checked via the dual-
detector discipline used since E0.

Command: `python3 verifier/bridge_closure_search.py --nmin 5 --nmax 8`

| n range | (J,x,y) candidates | distinct edge-rooted B | Type-A (d_B(x)=1) | internally-clean Type-A |
|---|---|---|---|---|
| 5-8 | 5,212 | 5,212 | 5,212 (100%) | 0 |

**Every candidate at this scale has d_B(x)=1 automatically** (deleting
one of a degree-2 vertex's two edges always leaves degree 1 — this is
structural, not a search artifact). **0 internally-clean candidates** —
matches the established small-order pattern (B0/M1/L15-style; also
directly confirmed here on a live example: g6 `DV{`, x=1, y=3, has
Λ(B)=[2,3,4], h(B)=2, but internal_clean=False). h(B) distribution among
internally-clean candidates is therefore empty at this scale — **not
evidence of nonexistence**, consistent with every other search in this
project reaching n≤8 or n≤9. No h(B)=0 gadget found (would have triggered
immediate escalation per protocol). No h(B)=1 candidate qualifies either
(internal cleanliness gates first). At the E22 pass, n=9+ was not attempted —
generation cost scales the same as the earlier one-pole search (E9),
already documented as slow past n≈9 without a streaming rewrite.
The later streaming E23b census completes the targeted Type-A order-9 case;
E22's broader implementation remains a completed-range n≤8 experiment.

**T7 (minimum-overlap reduction target, two_cut.md §14): neither proved
nor refuted.** The generator has not yet produced a genuine (internally-
clean, dyadic-self-sum-witnessing) Type-A candidate to test T7 against.
Recorded as open, with the exact target statement preserved for when one
appears.

## E23a. T8/R1/T8R structural audit (2026-07-25) [PROVED + COMPUTATIONALLY VERIFIED]

`verifier/gadget_criticality.py` makes T8's edge-deletion monotonicity and
the R1/T8R conclusions executable. `verifier/brute_spqr.py` independently
decomposes the small graphs by exhaustive split pairs and rejects any alleged
R-skeleton that is not actually simple and 3-connected. Full proofs are in
two_cut.md §§16–18.

Command:
`python verifier/gadget_criticality.py --nmin 5 --nmax 8`

| relaxed rooted closures | real R-skeleton B-edges | R1 violations | T8R degree-critical | noncritical deletion certificates |
|---:|---:|---:|---:|---:|
| 5,212 | 64,596 | 0 | 25,914 | 38,682 |

The last column is expected on relaxed, nonminimal fixtures: R1 preserves
closure 2-connectivity and the edge preserves every degree condition, so T8
certifies that such a fixture cannot be a minimal gadget.

**SPQR implementation adversary.** The installed `spqrtree==0.1.2` initially
reported two apparent R1 failures, both rootings of graph6 `GCpbeo` at the
same edge 3–6. Its alleged R-skeleton had connectivity 2 and a degree-2
vertex, violating the definition of R. A valid decomposition places 3–6 in
an S-node. Graph6 `FCZv_` gives a second regression: the package leaves a
crossing separator unsplit for every tested insertion ordering, while the
definition-first decomposition is the reduced R–R–S path. The new validator
and fallback prevent either package artifact from entering R1, T8R, or the
order-nine statistics. The fallback validates all 538 biconnected graphs in
NetworkX's graph atlas.

## E23b. Complete bridge-order-9 Type-A census (2026-07-25) [COMPUTATIONALLY VERIFIED]

Here bridge order means |V(B)|=9, so every three-copy lift has
3(9−2)+2=23 vertices. The degree sum bound
1+1+7·3=23 and parity give |E(B)|≥12, hence |E(J)|≥13. Conversely
d_J(x)=2 gives |E(J)|≤C(8,2)+2=30.

Installed generator: nauty 2.9.3. Its help identifies `-C` as biconnected
generation. The complete one-residue plan was frozen in
`manifests/E23_order9_manifest.json` before the definitive run.

Commands:

- `geng -C -d2 9 13:30 0/1`
- `labelg -q -fabzzzzzzz` after relabeling x=0,y=1; singleton `a` and `b`
  cells preserve orientation and prevent exchanging terminal roles.
- `python verifier/type_a_order9_search.py --run --manifest manifests/E23_order9_manifest.json --workers 8`

| stage | count |
|---|---:|
| raw unlabeled biconnected closures J | 193,510 |
| oriented incident edges from degree-2 x | 345,020 |
| Type-A degree-filtered rootings | 134,204 |
| rooted oriented isomorphism classes | 129,040 |
| SP-eligible (d_B(y)=1) | 4,214 |
| rigid-forced (d_B(y)≥2) | 124,826 |
| internally {4,8}-cycle-free B | **0** |
| power-cycle-free 23-vertex lifts | **0** |
| direct lift-equivalence agreements | 129,040 / 129,040 |

All 4,214 SP-eligible closures nevertheless contain a validated R-node;
none is actually series-parallel at order 9. Across both classes the reduced
trees contain 136,088 R-nodes: 122,126 candidates have one, 6,780 have two,
and 134 have three. Every rigid-forced record preserves each R-skeleton's
real edges, T8R annotations, and complete skeleton-vertex degree profile.

**Direct three-copy verification.** Every B and every 23-vertex G_B was
tested independently by Python's exact DFS detector and
`verifier/check_power_masks.c`. Both evaluated C4, C8, and C16 separately,
without short-circuiting after a shorter hit, and agreed on every mask.
Every lift is simple, connected, has minimum degree at least 3, and has order
23. The three-copy equivalence holds in all 129,040 records. There is no
survivor/counterexample.

**Internal-cycle obstruction is universal at this order.** Of the bridges,
5,980 contain C4 but no C8, one contains C8 but no C4, and 123,059 contain
both. Because none passes internal cleanliness, h(B) is not computed for any
candidate, respecting the cleanliness gate. The minimum positive h is
uninstantiated—not zero—and the T7 overlap program remains empirically
uninstantiated.

The complete 12,795,230-byte compressed record set is
`data/E23_order9_candidates.jsonl.gz`, SHA-256
`9f530d95918406bec166cc3e09fa5edf0d7b8f8ff58613b9ffae83c85851e446`.
The manifest records all generator/detector stream checksums and exit codes.

## E24a. Compact order-9/order-11 extremal certificates (2026-07-25) [COMPUTATIONALLY VERIFIED]

The authoritative McKay–Afzaly `{C4,C8}` table and sparse6 files were restored
from `https://users.cecs.anu.edu.au/~bdm/data/extremal.html`:

| n | ex(n,{C4,C8}) | records | SHA-256 | ordered (x,y) choices | survivors |
|---:|---:|---:|---|---:|---:|
| 9 | 12 | 33 | `ab93fb789a63defcb189f69f6e7f8a3bcac1057c77837dfd20211d644416ca98` | 2,376 | 0 |
| 11 | 15 | 245 | `fa5c5158ad641d1f2124feea75255e8077144fcdaeb7b051cd45f32470bbe0f2` | 26,950 | 0 |

Both the cycle conditions and every terminal choice were checked twice, using
NetworkX and direct connectivity after every vertex deletion. The exact
provenance record is `manifests/E24_extremal_manifest.json`.

## E24b. Direct order-10 Type-A edge layers (2026-07-25) [COMPUTATIONALLY VERIFIED]

The Type-A degree sum gives m≥13, while the exact Turán value is 14. The
complete manifest was frozen before running these direct-B commands:

- `geng -c -f -d1 -D3 10 13:13 0/1`
- `geng -c -f -d1 -D5 10 14:14 0/1`

The `-f` meaning was confirmed from installed nauty 2.9.3 help. The degree
caps are exact consequences of the 26 lower-bound degree sum: no excess at
m=13 and only two excess units at m=14.

| m | raw C4-free B | C8-free | degree-1 x pairs | rooted Type-A classes | internally clean | self-sum clean | lift survivors |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 13 | 57 | 4 | 0 | 0 | 0 | 0 | 0 |
| 14 | 216 | 12 | 0 | 0 | 0 | 0 | 0 |

Python and independent C masks agree on all 273 generated graphs. No lift
exists to test after the degree-1 filter, so the zero lift batches are
correctly recorded as vacuous rather than positive evidence from a detector.

## E24c. R2 and SPQR leaf adversarial audit (2026-07-25) [PROVED + COMPUTATIONALLY VERIFIED]

R2 has zero failures on 388 real P-edges in the 538 biconnected graph-atlas
graphs and 3,498/3,498 real P-edge instances in 5,212 relaxed closures. A
synthetic three-element P-bond exercises the direct parallel-union proof.
There are zero original P-leaves and zero invalid S-leaves.

The audit also prevented an overclaim: simply pruning the terminal S-leaf
exposes 2,872 P core-leaves in relaxed nonminimal fixtures. Even R/P tightness
alone leaves 35; all have self-sum hit 4. With the exact rigid-forced,
tight-edge, and self-sum-clean hypotheses used by the proof, both applicable
fixtures satisfy the R-leaf dichotomy and there are zero failures.

## E24d. Existing order-9 obstruction-support census (2026-07-25) [COMPUTATIONALLY VERIFIED]

No graph generation was run. The checksummed E23 gzip was streamed through
`verifier/order9_spqr_obstructions.py` using eight workers in 328.044 seconds.
The 129,040 output records occupy 3,456,437 compressed bytes with SHA-256
`e6723280ec82e02f125730958279e219b61d5939ecd8b8dba8cce1732684ca0e`.

Shortest-cycle support counts are: 98,990 contained in one R-node, 29,581
created by two P expansions, 469 genuinely multi-node, and zero S-cycle or
root-local cases. Among the 411 R/P-tight candidates the corresponding counts
are 307, 70, and 34. The leaf-R dataset contains 75,745 transformed core
orientations; all contain a contracted C4 or C8 and 6,325 have a tight-degree
cover of every real B-edge. E26 separates genuine original remote leaves from
root-side nodes exposed by terminal-S suppression.
