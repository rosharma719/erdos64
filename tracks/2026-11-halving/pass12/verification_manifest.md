# Pass XII — independent verification manifest

**Overall status: COMPUTED (limited cases only); OPEN (requested high orders).** This is not the requested completed order-13–23 or order-8–22 census. The remote branch, its raw survivor files, `geng`, and its verifier/sharding scripts were unavailable in this execution environment. No missing count is inferred or fabricated.

## Fresh dual implementation evidence (COMPUTED)

- **Tower:** A NetworkX full simple-path/cycle enumerator and an independent C adjacency-bitmask DFS agree on seven actual graph certificates (identity; clean 3, both clean 7-poles, clean 15; unclean 5, 9) and 20 symbolic tower triple rows plus 35 `K4` extension rows. The finite classification is proved independently in `tower_theorem.md`.
- **Cubic fixture deletions:** `small_pole_census.py` generates each connected rooted pole of orders 3, 5, 7, 9, 11 from the earlier saved cubic-graph class catalogs (cap orders 4,6,8,10,12). The Python verifier computes cycle spectra with NetworkX; a separate C verifier computes them using bit-mask DFS. Each checker validates the input degrees and both streams match exactly. This is **conditional on those fixture catalogs being complete**; it is not a fresh `geng` verification of the source catalog.
- **2-poles at orders 4 and 6:** One checker uses the independent NetworkX unlabelled graph atlas; another uses exhaustive labeled adjacency bitmasks, degree filtering and canonicalization under degree-class-preserving vertex permutations. Their outputs agree exactly. No clean two-poles were found.

### Rooted pole records from the existing cubic fixtures

| Pole order | Connected rooted deletions checked | Clean rooted deletions | Status |
|---:|---:|---:|---|
| 3 | 4 | 4 | COMPUTED (fixture-dependent) |
| 5 | 12 | 0 | COMPUTED (fixture-dependent) |
| 7 | 40 | 4 | COMPUTED (fixture-dependent) |
| 9 | 188 | 0 | COMPUTED (fixture-dependent) |
| 11 | 1012 | 0 | COMPUTED (fixture-dependent) |
| 13 | — | — | OPEN: not run/certified |
| 15 | — | — | OPEN: not run/certified; prior claimed survivor not rechecked |
| 17 | — | — | OPEN: not run/certified |
| 19 | — | — | OPEN: not run/certified |
| 21 | — | — | OPEN: `geng` shards not run |
| 23 | — | — | OPEN: `geng` shards not run |

The clean rooted count is a **record count**, not the number of terminal-marked isomorphism classes. Source completeness and isomorphism-class counts require separate certification.

### Two-poles

| 2-pole order | Connected unlabelled candidate classes | Clean classes | Status |
|---:|---:|---:|---|
| 4 | 1 | 0 | COMPUTED, independent atlas and C generators |
| 6 | 4 | 0 | COMPUTED, independent atlas and C generators |
| 8, 10, 12, 14, 16, 18, 20, 22 | — | — | OPEN: `geng` not available; no claim |

**No counterexample to Conjecture T was found in the verified cases.** This is an observation limited to the explicitly checked inputs.

## Machine-readable certification

`verifier/certification_manifest.json` records command-level exit codes, SHA-256 of each input/output stream, source hashes, matching stream comparison, and baseline-suite result. Regenerate with:

```
cd tracks/2026-11-halving/pass12/verifier
python certify_pass12.py
```

The Python and C streams are maintained separately, including checksums even when identical. This meets the two-checker protocol **for the explicitly executed calculations only**.

## What a complete requested census still requires

**OPEN:** Checkout branch `claude/additive-reduction-brief`, inspect PR #5 and `tracks/2026-11-halving/README.md`, run the repository's actual `verifier/certify_shard.sh` with `geng` and `verifier/check_power_masks.c`. Record every `geng` exit code, every ordered shard stream checksum, edge/degree/connectedness verification, and the independent checker result. Cover 3-pole orders 13–23 (equivalently caps 14–24), and all even 2-pole orders through 22. Each outside-list survivor must be recorded first, with graph6, its degree-derived terminals, path spectra, and internal cycle lengths. The sources available for this pass contain no such new survivor.
