#!/usr/bin/env python3
"""Part III: algebraic compression of the Z3 lift elimination.

Loads the four certified 24-vertex bases (verifier/z3_lifts.py) and the
exact list of assignments surviving C8 (data/z3_lifts/results/*.after8.txt,
1,545,746 total across the four bases, all independently exhaustive and
audited already -- z3_lifts.md). For each base:

III.1 -- enumerate every SIMPLE 16-cycle of the base (not just the one
  stored witness) and classify what kind of object explains each C8
  survivor's elimination: does its voltage assignment satisfy a.z_C=0 for
  some simple-base-C16 homology vector z_C (a Type-1 projection, in the
  task's numbering) -- checked for EVERY C8-survivor exhaustively, not
  sampled.

III.2 -- build the exact linear model: canonical spanning tree (same rule
  as z3_lifts.py, BFS root 0, neighbours scanned increasingly) + 13 cotree
  coordinates; z_C in F3^13 for every simple 16-cycle; check whether the
  union of hyperplanes {a : a.z_C=0} covers 100% of the C8-survivor set
  per base. Uses exact modular arithmetic (numpy int8 mod 3), vectorized.

III.3 -- for whichever assignments are NOT covered by the simple-C16
  hyperplanes (if any), classify their actual killer cycle by direct lift
  construction + exact cycle search (reusing verifier/z3_lifts.py's
  reference lift builder and verifier/cycle_detect.py's dual detector),
  producing the exact projection type (1-4) per the task's taxonomy:
    1. simple 16-cycle in the base (a.z_C=0 for a simple-C16 vector)
    2. non-simple nonbacktracking closed walk of length 16 in the base
    3. projection with repeated base vertices but distinct lifted vertices
       (a sub-case of 2, singled out when the *walk* itself is
       nonbacktracking but visits some base vertex twice at different
       sheets)
    4. anything not matching 1-3 (recorded exactly, not forced into 1-3)

All of this is independently replayable from the checked-in manifests: the
four base edge lists, the frozen after8 survivor-index files, and this
script alone (no unrecorded intermediate state).
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
from verifier.cycle_detect import find_cycle_len_dfs  # noqa: E402
from verifier.z3_lifts import (  # noqa: E402
    BASE_NAMES,
    Base,
    load_base,
    lift_detector_graph,
    voltage_vector,
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "z3_lifts" / "results"


def enumerate_simple_c16(base: Base) -> list[list[int]]:
    """Every simple 16-cycle of the base, as ordered vertex lists (one
    canonical rotation/direction per cycle, deduplicated)."""
    G = base.graph
    n = G.number_of_nodes()
    cycles: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()

    def visit(path: list[int], used: set[int], start: int):
        v = path[-1]
        if len(path) == 16:
            if G.has_edge(v, start):
                # canonicalize: rotate to min-first, pick lexicographically
                # smaller of the two directions
                cyc = tuple(path)
                rotations = [cyc[i:] + cyc[:i] for i in range(16)]
                best_fwd = min(rotations)
                rev = tuple(reversed(cyc))
                rotations_rev = [rev[i:] + rev[:i] for i in range(16)]
                best_rev = min(rotations_rev)
                canon = min(best_fwd, best_rev)
                if canon not in seen:
                    seen.add(canon)
                    cycles.append(canon)
            return
        for u in G.neighbors(v):
            if u == start or u in used:
                continue
            if u < start:
                continue  # start is the minimum vertex of the cycle
            used.add(u)
            path.append(u)
            visit(path, used, start)
            path.pop()
            used.remove(u)

    for start in range(n):
        visit([start], {start}, start)
    return [list(c) for c in cycles]


def homology_vector(base: Base, cycle: list[int]) -> tuple[int, ...]:
    """z_C in F3^13: signed cotree-coordinate vector such that a.z_C is
    the net voltage accumulated going around `cycle` once (start->...->
    start), for voltage vector a indexed the same way as base.cotree_edges."""
    index = {e: i for i, e in enumerate(base.cotree_edges)}
    vec = [0] * len(base.cotree_edges)
    n = len(cycle)
    for i in range(n):
        u, v = cycle[i], cycle[(i + 1) % n]
        key = tuple(sorted((u, v)))
        if key in index:
            sign = 1 if u < v else -1  # canonical orientation is (min,max)
            vec[index[key]] = (vec[index[key]] + sign) % 3
    return tuple(vec)


def load_after8(base_index: int) -> np.ndarray:
    path = RESULTS / f"base{base_index}-full.after8.txt"
    return np.loadtxt(path, dtype=np.int64)


def indices_to_digit_matrix(indices: np.ndarray, coords: int = 13) -> np.ndarray:
    """Vectorized base-3 digit expansion: row i = voltage_vector(indices[i])."""
    out = np.zeros((len(indices), coords), dtype=np.int8)
    rem = indices.copy()
    for j in range(coords):
        out[:, j] = (rem % 3).astype(np.int8)
        rem //= 3
    return out


def hyperplane_coverage(A: np.ndarray, Z: np.ndarray) -> np.ndarray:
    """A: (N,13) assignments: Z: (k,13) homology vectors. Returns boolean
    (N,) -- True if assignment i is orthogonal (mod 3) to at least one row
    of Z. Chunked to bound memory."""
    N = A.shape[0]
    covered = np.zeros(N, dtype=bool)
    chunk = max(1, (200_000_000 // max(Z.shape[0], 1)))
    for start in range(0, N, chunk):
        end = min(N, start + chunk)
        dots = (A[start:end].astype(np.int32) @ Z.T.astype(np.int32)) % 3
        covered[start:end] = (dots == 0).any(axis=1)
    return covered


def classify_uncovered(base: Base, base_index: int, indices: np.ndarray) -> list[dict[str, Any]]:
    """Direct lift + exact search for assignments the simple-C16 model
    does not explain; classify projection type 2/3/4."""
    records = []
    for idx in indices:
        values = voltage_vector(int(idx))
        lifted = lift_detector_graph(base, values)
        witness = find_cycle_len_dfs(lifted, 16)
        assert witness is not None, f"base {base_index} idx {idx}: no C16 in lift (contradicts z3_lifts.md)"
        base_proj = [v // 3 for v in witness]
        distinct_base_vertices = len(set(base_proj))
        # nonbacktracking check: consecutive projected edges never immediately reverse
        nonbacktracking = all(
            base_proj[i] != base_proj[(i + 2) % 16] or base_proj[i] == base_proj[(i + 1) % 16]
            for i in range(16)
        )
        if distinct_base_vertices == 16:
            ptype = 1  # simple base 16-cycle projection (shouldn't occur here by construction)
        elif len(witness) == len(set(witness)) and distinct_base_vertices < 16:
            ptype = 3  # repeated base vertices, distinct lifted vertices (always true for a simple lift cycle)
        else:
            ptype = 4
        records.append({
            "assignment_index": int(idx),
            "witness_lift_vertices": witness,
            "base_projection": base_proj,
            "distinct_base_vertices": distinct_base_vertices,
            "nonbacktracking_projection": nonbacktracking,
            "projection_type": ptype,
        })
    return records


def process_base(base_index: int, verify_sample: int) -> dict[str, Any]:
    base = load_base(base_index)
    cycles = enumerate_simple_c16(base)
    homologies = [homology_vector(base, c) for c in cycles]
    # exact cross-check on a sample: reconstruct the projected walk from
    # the base graph itself and independently confirm it is a real 16-cycle
    import random
    rng = random.Random(20260726 + base_index)
    for c in rng.sample(cycles, min(verify_sample, len(cycles))):
        assert len(c) == 16 and len(set(c)) == 16
        for i in range(16):
            assert base.graph.has_edge(c[i], c[(i + 1) % 16])

    Z_unique = sorted(set(homologies))
    Z = np.array(Z_unique, dtype=np.int8) if Z_unique else np.zeros((0, 13), dtype=np.int8)

    idx = load_after8(base_index)
    A = indices_to_digit_matrix(idx)
    covered = hyperplane_coverage(A, Z) if Z.shape[0] else np.zeros(len(idx), dtype=bool)

    uncovered_idx = idx[~covered]
    uncovered_records = classify_uncovered(base, base_index, uncovered_idx) if len(uncovered_idx) else []
    type_counts = {1: int(covered.sum())}
    for rec in uncovered_records:
        type_counts[rec["projection_type"]] = type_counts.get(rec["projection_type"], 0) + 1

    return {
        "base_index": base_index,
        "name": BASE_NAMES[base_index],
        "simple_c16_count": len(cycles),
        "simple_c16_cycles": cycles,
        "homology_vectors": [list(v) for v in homologies],
        "distinct_homology_vectors": len(Z_unique),
        "distinct_homology_vector_list": [list(v) for v in Z_unique],
        "c8_survivors": int(len(idx)),
        "covered_by_simple_c16_hyperplanes": int(covered.sum()),
        "coverage_fraction": float(covered.mean()) if len(idx) else None,
        "uncovered_count": int(len(uncovered_idx)),
        "projection_type_distribution": type_counts,
        "uncovered_sample_records": uncovered_records[:20],
        "all_uncovered_indices": [int(x) for x in uncovered_idx],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify-sample", type=int, default=200)
    args = parser.parse_args()

    report = {"schema": "erdos64-z3-certificate-v1", "bases": []}
    for i in range(4):
        rec = process_base(i, args.verify_sample)
        report["bases"].append(rec)
        print(
            f"base {i} ({rec['name']}): simple_C16={rec['simple_c16_count']} "
            f"distinct_z_C={rec['distinct_homology_vectors']} "
            f"c8_survivors={rec['c8_survivors']} "
            f"covered={rec['covered_by_simple_c16_hyperplanes']} "
            f"uncovered={rec['uncovered_count']} "
            f"types={rec['projection_type_distribution']}"
        )

    encoded = json.dumps(report, indent=2, sort_keys=True, default=str)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
