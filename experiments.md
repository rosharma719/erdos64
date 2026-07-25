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
