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
