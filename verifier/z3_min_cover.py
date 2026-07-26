#!/usr/bin/env python3
"""Part III.2: minimal/near-minimal covering subset of simple-C16
hyperplanes, per base, plus a standalone exact verifier over all 3^13
assignments and a light projective-geometric structure check.

verifier/z3_certificate.py already establishes: for every one of the 4
bases, the union of {a in F3^13 : a . z_C = 0} over every simple-C16
homology vector z_C covers the ENTIRE nonzero space F3^13\\{0}, not just
the 1,545,746 C8-survivors. This file finds a small covering SUBSET
(greedy set cover -- exact minimum is NP-hard in general and not claimed
here) and produces a standalone verifier that only needs that subset, not
the full ~207-330 simple-C16 list, to certify every nonzero assignment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.z3_certificate import compact_json, enumerate_simple_c16, homology_vector  # noqa: E402
from verifier.z3_lifts import load_base  # noqa: E402


def full_digit_matrix(coords: int) -> np.ndarray:
    N = 3 ** coords
    digits = np.zeros((N, coords), dtype=np.int8)
    rem = np.arange(N, dtype=np.int64)
    for j in range(coords):
        digits[:, j] = (rem % 3).astype(np.int8)
        rem //= 3
    return digits


def greedy_min_cover(Z: np.ndarray, universe_size: int = 3**13,
                      sample_size: int = 150_000, seed: int = 20260726) -> list[int]:
    """Near-minimal set cover over F3^13 \\ {0}, found FAST by running
    greedy selection on a random sample of the space (cheap: each round is
    one (sample x candidates) dot-product matrix, not a (3^13 x candidates)
    one), then verified exactly against the FULL space afterward
    (`analyze_base` does the exact full-space check on the result). If the
    sampled cover fails to reach exact 100% on the full space, remaining
    exact-uncovered points are patched in a final exact top-up round."""
    coords = Z.shape[1]
    rng = np.random.default_rng(seed)
    sample = rng.integers(1, universe_size, size=min(sample_size, universe_size - 1), dtype=np.int64)
    sample = np.unique(sample)
    digits = np.zeros((len(sample), coords), dtype=np.int8)
    rem = sample.copy()
    for j in range(coords):
        digits[:, j] = (rem % 3).astype(np.int8)
        rem //= 3

    Zi = Z.astype(np.int32)
    all_dots = (digits.astype(np.int32) @ Zi.T) % 3  # (sample, k)
    all_covers = (all_dots == 0)  # (sample, k) boolean

    uncovered = np.ones(len(sample), dtype=bool)
    chosen: list[int] = []
    remaining = set(range(Z.shape[0]))
    while uncovered.any() and remaining:
        gains = (all_covers[uncovered][:, list(remaining)]).sum(axis=0)
        best_local = int(np.argmax(gains))
        best_gain = int(gains[best_local])
        best_idx = sorted(remaining)[best_local]
        if best_gain <= 0:
            break
        chosen.append(best_idx)
        uncovered &= ~all_covers[:, best_idx]
        remaining.discard(best_idx)

    return chosen


def exact_top_up(Z: np.ndarray, chosen: list[int]) -> list[int]:
    """Given a sample-based near cover, check the FULL exact space and
    greedily add vectors (from the full candidate list) until exact 100%
    coverage is reached, or all candidates are exhausted."""
    coords = Z.shape[1]
    digits = full_digit_matrix(coords)
    Zi = Z.astype(np.int32)
    chosen = list(chosen)

    def coverage_mask(idxs):
        if not idxs:
            return np.zeros(digits.shape[0], dtype=bool)
        sub = Zi[idxs]
        dots = (digits.astype(np.int32) @ sub.T) % 3
        m = (dots == 0).any(axis=1)
        m[0] = True
        return m

    covered = coverage_mask(chosen)
    if covered.all():
        return chosen
    remaining = [i for i in range(Z.shape[0]) if i not in chosen]
    while not covered.all() and remaining:
        uncov = ~covered
        dots = (digits[uncov].astype(np.int32) @ Zi[remaining].T) % 3
        gains = (dots == 0).sum(axis=0)
        best_local = int(np.argmax(gains))
        if gains[best_local] <= 0:
            break
        best_idx = remaining[best_local]
        chosen.append(best_idx)
        remaining.remove(best_idx)
        covered = coverage_mask(chosen)
    return chosen


def analyze_base(base_index: int) -> dict[str, Any]:
    base = load_base(base_index)
    cycles = enumerate_simple_c16(base)
    homologies = sorted(set(homology_vector(base, c) for c in cycles))
    Z = np.array(homologies, dtype=np.int8)

    chosen = greedy_min_cover(Z)
    chosen = exact_top_up(Z, chosen)
    cover_vectors = [homologies[i] for i in chosen]

    # verify the chosen subset covers the full nonzero space exactly
    coords = Z.shape[1]
    digits = full_digit_matrix(coords)
    Zc = np.array(cover_vectors, dtype=np.int32)
    dots = (digits.astype(np.int32) @ Zc.T) % 3
    covered = (dots == 0).any(axis=1)
    covered[0] = True  # zero assignment trivially satisfies every a.z=0
    full_cover_verified = bool(covered.all())

    # light projective-geometric structure check: multiplicities, and
    # whether the cover vectors' pairwise "angles" (i.e. whether any two
    # are scalar multiples -- impossible for distinct homology classes
    # unless the two 16-cycles are voltage-equivalent) coincide.
    scalar_pairs = 0
    for i in range(len(cover_vectors)):
        for j in range(i + 1, len(cover_vectors)):
            vi, vj = np.array(cover_vectors[i]), np.array(cover_vectors[j])
            if np.array_equal((vi * 2) % 3, vj) or np.array_equal((vj * 2) % 3, vi):
                scalar_pairs += 1

    return {
        "base_index": base_index,
        "total_distinct_homology_vectors": len(homologies),
        "greedy_cover_size": len(chosen),
        "cover_vectors": [list(v) for v in cover_vectors],
        "full_nonzero_space_covered_by_subset": full_cover_verified,
        "scalar_multiple_pairs_in_cover": scalar_pairs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {"schema": "erdos64-z3-min-cover-v1", "bases": []}
    for i in range(4):
        rec = analyze_base(i)
        report["bases"].append(rec)
        print(f"base {i}: {rec['total_distinct_homology_vectors']} distinct z_C -> "
              f"greedy cover size {rec['greedy_cover_size']}, "
              f"full coverage verified={rec['full_nonzero_space_covered_by_subset']}, "
              f"scalar-pair count={rec['scalar_multiple_pairs_in_cover']}")
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
