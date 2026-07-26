#!/usr/bin/env python3
"""Part IV.A: algebraic-feasibility study for cyclic Z5 lifts of the same
four certified 24-vertex bases.

Does NOT enumerate all 5^13 = 1,220,703,125 assignments (explicitly
forbidden by the task). Instead:

1. Reduces every simple-C16 homology vector (already enumerated exactly
   over F3 in verifier/z3_certificate.py) mod 5 instead of mod 3, using
   the SAME canonical tree/cotree gauge (the homology vector's INTEGER
   signed-count representation is modulus-independent; only the final
   reduction changes).
2. Estimates the coverage fraction of the resulting F5^13 hyperplane union
   via Monte Carlo sampling (a random sample well below 5^13, with an
   explicit standard-error estimate) -- NOT full enumeration.
3. Directly samples exact lifts (real 120-vertex graphs, independent DFS/
   NetworkX dual detector) among assignments the linear model does NOT
   cover, testing C4/C8/C16/C32/C64 to see whether the "algebraic
   survivors" are actually killed by some other mechanism (a longer
   simple cycle, a non-simple projection, etc.) or might be genuine
   counterexample candidates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cycle_detect import has_cycle_len_dfs  # noqa: E402
from verifier.z3_certificate import enumerate_simple_c16  # noqa: E402
from verifier.z3_lifts import Base, load_base  # noqa: E402


def integer_homology_vector(base: Base, cycle: list[int]) -> tuple[int, ...]:
    """Signed integer (not yet reduced) cotree-coordinate vector -- exact
    over Z, so it can be reduced mod ANY prime afterward without
    recomputation."""
    index = {e: i for i, e in enumerate(base.cotree_edges)}
    vec = [0] * len(base.cotree_edges)
    n = len(cycle)
    for i in range(n):
        u, v = cycle[i], cycle[(i + 1) % n]
        key = tuple(sorted((u, v)))
        if key in index:
            sign = 1 if u < v else -1
            vec[index[key]] += sign
    return tuple(vec)


def lift_graph_mod_p(base: Base, values: list[int], p: int) -> dict[int, set[int]]:
    voltage = {edge: 0 for edge in base.tree_edges}
    voltage.update(zip(base.cotree_edges, values))
    lifted: dict[int, set[int]] = {v: set() for v in range(p * base.graph.number_of_nodes())}
    for u, v in base.edges:
        a = voltage[(u, v)]
        for sheet in range(p):
            left = p * u + sheet
            right = p * v + (sheet + a) % p
            lifted[left].add(right)
            lifted[right].add(left)
    return lifted


def monte_carlo_coverage(Z_mod5: np.ndarray, coords: int, p: int, n_samples: int, seed: int,
                          chunk_size: int = 2_000_000) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    Zi = Z_mod5.astype(np.int32)
    total_checked = 0
    total_covered = 0
    uncovered_examples: list[list[int]] = []
    remaining = n_samples
    while remaining > 0:
        take = min(chunk_size, remaining)
        remaining -= take
        A = rng.integers(0, p, size=(take, coords), dtype=np.int32)
        all_zero = (A == 0).all(axis=1)
        A = A[~all_zero]
        if len(A) == 0:
            continue
        dots = (A @ Zi.T) % p
        covered = (dots == 0).any(axis=1)
        total_checked += len(A)
        total_covered += int(covered.sum())
        if len(uncovered_examples) < 50:
            for row in A[~covered][:50 - len(uncovered_examples)]:
                uncovered_examples.append(row.tolist())

    frac = total_covered / total_checked if total_checked else 0.0
    stderr = float(np.sqrt(frac * (1 - frac) / total_checked)) if total_checked > 0 else 0.0
    return {
        "samples": int(total_checked),
        "covered_fraction_estimate": frac,
        "stderr": stderr,
        "estimated_total_covered": frac * (p ** coords - 1),
        "estimated_total_uncovered": (1 - frac) * (p ** coords - 1),
        "uncovered_sample_assignments": uncovered_examples,
    }


def exact_lift_sample_test(base: Base, base_index: int, p: int, coords: int,
                            n_samples: int, seed: int) -> dict[str, Any]:
    """Build real p-sheeted lifts for random assignments and test C4/C8/
    C16 with the dual detector (cheap, checked on every sample);
    C32/C64 (expensive on a 120-vertex graph) are checked ONLY for the
    rare/hopefully-empty survivors of C4+C8+C16 -- staged exactly the way
    the original exhaustive Z3 engine was staged, for the same reason
    (avoid exponential blowup on cases already resolved by a cheaper
    stage)."""
    rng = random.Random(seed)
    early_lengths = (4, 8, 16)
    results = {L: 0 for L in (4, 8, 16, 32, 64)}
    survivors_c4_c8_c16 = []
    for _ in range(n_samples):
        values = [rng.randrange(p) for _ in range(coords)]
        if all(v == 0 for v in values):
            continue
        lifted = lift_graph_mod_p(base, values, p)
        any_hit = False
        for L in early_lengths:
            d = has_cycle_len_dfs(lifted, L)
            if d:
                results[L] += 1
                any_hit = True
        if not any_hit:
            survivors_c4_c8_c16.append(values)

    counterexample_candidates = []
    for values in survivors_c4_c8_c16:
        lifted = lift_graph_mod_p(base, values, p)
        d32 = has_cycle_len_dfs(lifted, 32)
        if d32:
            results[32] += 1
            continue
        d64 = has_cycle_len_dfs(lifted, 64)
        if d64:
            results[64] += 1
            continue
        counterexample_candidates.append(values)

    return {
        "samples": n_samples,
        "hit_counts": results,
        "c4_c8_c16_survivor_count": len(survivors_c4_c8_c16),
        "counterexample_candidates_found": len(counterexample_candidates),
        "counterexample_candidates": counterexample_candidates[:5],
    }


def analyze_base(base_index: int, p: int, mc_samples: int, lift_samples: int, seed: int) -> dict[str, Any]:
    base = load_base(base_index)
    cycles = enumerate_simple_c16(base)
    int_vecs = [integer_homology_vector(base, c) for c in cycles]
    coords = len(int_vecs[0])
    Z_mod_p = np.array([[x % p for x in v] for v in int_vecs], dtype=np.int32)
    Z_mod_p_unique = np.unique(Z_mod_p, axis=0)

    mc = monte_carlo_coverage(Z_mod_p_unique, coords, p, mc_samples, seed)
    exact = exact_lift_sample_test(base, base_index, p, coords, lift_samples, seed + 1)

    return {
        "base_index": base_index,
        "p": p,
        "simple_c16_count": len(cycles),
        "distinct_homology_vectors_mod_p": int(Z_mod_p_unique.shape[0]),
        "monte_carlo": mc,
        "exact_lift_sample": exact,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=5)
    parser.add_argument("--mc-samples", type=int, default=20_000_000)
    parser.add_argument("--lift-samples", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=20260726)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report: dict[str, Any] = {"schema": "erdos64-z5-lift-feasibility-v1", "p": args.p, "bases": []}
    for i in range(4):
        rec = analyze_base(i, args.p, args.mc_samples, args.lift_samples, args.seed + 1000 * i)
        report["bases"].append(rec)
        mc = rec["monte_carlo"]
        ex = rec["exact_lift_sample"]
        print(f"base {i}: p={args.p} simple_C16={rec['simple_c16_count']} "
              f"distinct_z_C_mod_p={rec['distinct_homology_vectors_mod_p']} "
              f"MC_covered_frac={mc['covered_fraction_estimate']:.4f}+-{mc['stderr']:.4f} "
              f"est_uncovered={mc['estimated_total_uncovered']:.0f} "
              f"exact_lift_hits(c4,c8,c16,c32,c64)={ex['hit_counts']} "
              f"counterexample_candidates={ex['counterexample_candidates_found']}")

    encoded = json.dumps(report, indent=2, sort_keys=True, default=str)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
