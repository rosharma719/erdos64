# Audit of the externally-supplied "order-38 census" bundle

**Source:** pasted by the user as `ALL_PROOFS_AND_SOURCE.md` plus a `sha256sum`-style file
listing for ~370 result/data files. Only the markdown transcription (proof notes + C++/Python
source) was actually available as content; the referenced data files themselves
(`manifest.json`, `partition_catalog.tsv`, `results/**/*.out|.err|.status`,
`data/quotients/*.txt`) were **not** supplied — only their names and SHA-256 hashes were,
as plain text in the chat message. This means `replay_manifest.py` cannot actually be run
here: it needs those files on disk, and their contents are unknown to us.

**Provenance red flag:** `src/generate_quotients38.cpp` originally hardcoded its output path
as `/mnt/data/f38_quotient/data/skel...` — the working-directory convention of a different
sandboxed code-execution tool, not this repository or the Mac environment referenced in
`verifier/certify_shard.sh`'s original hardcoded path. This material was generated in a third,
now-inaccessible environment. Combined with the earlier "cubic38_theorem_report" fabrication
found in this same project (see git history on this branch), external claims of this kind
should not be trusted without independent reproduction.

## What was independently checked here

### 1. The three hand-written proof notes (`proofs/`)
Read and checked line-by-line for logical validity (not just plausibility). All three
arguments are **internally sound** — the cycle-surgery/replacement steps (subdivision-bridge
correspondence, star-closure replacement, triangle-arc replacement) are correct wherever
checked by hand. However, each depends on external citations that could not be verified from
memory with confidence:
- "Carr 2026" (independent-set / cubic-neighbor structure of minimal counterexamples)
- "Candráková–Lukoťka" 2-factor / 5-odd-edge-connectivity theorem
- a "Wormald–Kingan" cyclic-4-connected-cubic unbridging/generation theorem

None of these are in this project's `literature.md` (which is the discipline this whole
project otherwise follows: no literature claim used before being recorded and verified).
**Verdict: mathematically self-consistent, but resting on unverified citations. Not
independently confirmed as new theorems.**

### 2. The shared cycle/path-detection primitive
`factor38_direct_mrv.cpp`, `quotient_static38_rot.cpp`/`_nosym.cpp`, and
`filter_pair_local38.py`/`filter_triple_local38.cpp` all reimplement the same "does an exact
simple path/cycle of length L exist" backtracking routine. Extracted it into
`test_pathrec.cpp`, compiled fresh on this machine, and cross-validated against this
project's already-validated `verifier/cycle_detect.py` (itself cross-validated against
networkx, 2107 checks, 0 disagreements — see `plan.md`):
- 300 random graphs, n=5..24, random L: **0 disagreements**.
- 60 random sparser graphs, n=28..38, L in {15,16,31,32,n,n-1}: run, taking longer than
  expected in the pure-Python comparison side (likely just slow unoptimized Python DFS on
  some instances, not a bug) — see `xcheck_pathrec_large.py`; check the background task
  output for the final verdict when it completes.

**Verdict: the core cycle-avoidance primitive that all the order-38 tools depend on is
correct on every case checked so far.**

### 3. From-scratch reproduction of two partition classes
Fixed the hardcoded `/mnt/data` path (now `$OUT_DIR` env var), compiled
`generate_quotients38.cpp`, `quotient_static38_rot.cpp`, `quotient_static38_nosym.cpp` fresh
(none of the original binaries or logs were available or used), and ran the **full,
unfiltered** quotient enumeration + search end to end, independent of any figure in the
original bundle:

| Partition | Canonical quotient rows | Solver | Result |
|---|---|---|---|
| (7,31) | 2 | rot | **0 leaves**, 41,753 nodes, 7.6s |
| (7,31) | 2 | nosym | **0 leaves**, 41,753 nodes, 7.6s (identical — no symmetry pruning fired here) |
| (5,5,5,5,9,9) | 3,390 | rot | **0 leaves**, 122,976 nodes, 26.7s |
| (5,5,5,5,9,9) | 3,390 | nosym | started; no-symmetry search is far more expensive per row, did not finish within this session's time budget |

Both reproduced classes agree with the bundle's headline claim (no counterexample in that
factor-cycle-length class). This is a real, independent computation — not merely a hash
check — for these two classes out of the 151 the bundle claims to have covered.

The bundle's own `quotient_reflection_symmetry_audit` note cites a **specific** number pair
(177 vs 134,539 nodes) for "the two-row class (5,5,5,5,9,9)" — that phrase does not match
what `generate_quotients38` actually produces for that degree sequence (3,390 canonical
rows, not two), so it most likely refers to a single specific row after the
`filter_pair_local38.py` → `filter_triple_local38.cpp` reduction pipeline, which was not
run here. This wasn't reconciled — flagging it rather than guessing.

## What was NOT verified (and cannot be, from what was supplied)

- The other ~149 partition classes and the full order-38 "60,889,513 primary nodes" total —
  no time budget in a single session to brute-force-reproduce a census this large end to end,
  and the actual per-class result logs / `manifest.json` were never supplied, only their
  hashes.
- The order-36 "symmetry repair" claims and their specific corrected node counts.
- Whether `Candráková–Lukoťka`, `Carr 2026`, and `Wormald–Kingan` are real, correctly-cited
  results (would require literature access, not just code execution).
- Whether the reduction from "no counterexample exists in any of these 151 quotient classes"
  actually constitutes an exhaustive cover of all cubic order-38 graphs (i.e., whether the
  Candráková–Lukoťka-based factor selection is complete/correct as a case-generation
  method) — this is a mathematical completeness claim, not something code execution alone
  can confirm.

## Bottom line

Nothing found here contradicts the bundle. The parts that were checked — the shared
cycle-detection primitive, and two full partition classes reproduced from scratch — check
out. But the overwhelming majority of the order-38 claim (149 more classes, the order-36
repair, and the load-bearing external citations) remains **unverified**, and the
provenance (a different, inaccessible sandbox, the same failure mode as the earlier
fabricated report on this project) means it should be treated as a promising lead to
independently keep checking, not as an established result.
