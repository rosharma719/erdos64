#!/usr/bin/env python3
"""Part IV.2 (leaf-compression phase): EXACT (not Monte Carlo) simple-C16
constraint solving over F5^13 for the four certified 24-vertex bases.

Replaces every previously-SAMPLED conclusion (z5_lift_feasibility.py's
Monte Carlo coverage estimate) with an exact one: this script performs a
full, chunked, vectorized scan of ALL 5^13-1 = 1,220,703,124 nonzero
assignments per base against every simple-C16 homology vector (reduced
mod 5 from the same integer homology vectors already certified in
verifier/z3_certificate.py -- same canonical tree/cotree gauge, same
enumerate_simple_c16). For each assignment, "covered" means a.z_C=0 mod 5
for at least one simple-C16 vector z_C (a Type-1 lifted C16 exists with
trivial holonomy); "uncovered" assignments are recorded exactly (not
estimated) for the exact-lift follow-up in z5_exact_lift.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.z3_certificate import compact_json, enumerate_simple_c16  # noqa: E402
from verifier.z5_lift_feasibility import integer_homology_vector  # noqa: E402
from verifier.z3_lifts import load_base  # noqa: E402

P = 5
COORDS = 13
FULL_SPACE = P ** COORDS  # 1,220,703,125


def base_hyperplanes_mod5(base_index: int) -> np.ndarray:
    base = load_base(base_index)
    cycles = enumerate_simple_c16(base)
    int_vecs = [integer_homology_vector(base, c) for c in cycles]
    Z = np.array(sorted({tuple(x % P for x in v) for v in int_vecs}), dtype=np.int8)
    return Z


def exact_scan(Z: np.ndarray, chunk_size: int = 500_000,
                hyperplane_batch: int = 64,
                record_uncovered_limit: int = 2_000_000,
                start: int = 0, stop: int | None = None) -> dict[str, Any]:
    """Chunked exact scan of indices [start, stop) (default: the full
    nonzero space [1, P^COORDS)). Returns exact covered/uncovered counts
    and (up to record_uncovered_limit) the exact uncovered indices.
    Memory-bounded on TWO axes: chunk_size (points per batch) AND
    hyperplane_batch (hyperplanes per matmul), since the naive
    (chunk_size x num_hyperplanes) product matrix can otherwise reach
    many GB (e.g. 20M x 330 int16 = 13GB) and get OOM-killed."""
    stop = FULL_SPACE if stop is None else stop
    Zi = Z.astype(np.int8)
    total_covered = 0
    total_checked = 0
    uncovered_indices: list[int] = []
    t0 = time.time()

    idx = max(start, 1)  # skip the zero assignment if start==0
    while idx < stop:
        end = min(stop, idx + chunk_size)
        n = end - idx
        indices = np.arange(idx, end, dtype=np.int64)
        digits = np.zeros((n, COORDS), dtype=np.int8)
        rem = indices.copy()
        for j in range(COORDS):
            digits[:, j] = (rem % P).astype(np.int8)
            rem //= P
        covered = np.zeros(n, dtype=bool)
        digits16 = digits.astype(np.int16)
        for hb_start in range(0, Zi.shape[0], hyperplane_batch):
            hb = Zi[hb_start:hb_start + hyperplane_batch].astype(np.int16)
            dots = (digits16 @ hb.T) % P
            covered |= (dots == 0).any(axis=1)
            if covered.all():
                break
        total_checked += n
        total_covered += int(covered.sum())
        if len(uncovered_indices) < record_uncovered_limit:
            unc = indices[~covered]
            take = min(len(unc), record_uncovered_limit - len(uncovered_indices))
            uncovered_indices.extend(int(x) for x in unc[:take])
        idx = end

    elapsed = time.time() - t0
    return {
        "start": start, "stop": stop,
        "checked": total_checked,
        "covered": total_covered,
        "uncovered": total_checked - total_covered,
        "uncovered_indices_recorded": len(uncovered_indices),
        "uncovered_indices_truncated": (total_checked - total_covered) > len(uncovered_indices),
        "uncovered_indices": uncovered_indices,
        "elapsed_seconds": elapsed,
        "rate_per_second": total_checked / elapsed if elapsed > 0 else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=int, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=None)
    parser.add_argument("--chunk-size", type=int, default=20_000_000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    Z = base_hyperplanes_mod5(args.base)
    print(f"base {args.base}: {Z.shape[0]} distinct simple-C16 homology vectors mod 5")

    result = exact_scan(Z, chunk_size=args.chunk_size, start=args.start, stop=args.stop)
    print(f"checked={result['checked']} covered={result['covered']} "
          f"uncovered={result['uncovered']} elapsed={result['elapsed_seconds']:.1f}s "
          f"rate={result['rate_per_second']:.0f}/s")

    report = {"base": args.base, "num_hyperplanes": int(Z.shape[0]), "result": result}
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
