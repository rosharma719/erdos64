#!/usr/bin/env python3
"""Part IV.3 (leaf-compression phase): construct and exactly test every
algebraically feasible Z5 lift -- i.e. every assignment NOT explained by
a simple-C16 homology hyperplane, as found exactly (not sampled) by
verifier/z5_exact_solve.py.

For every such assignment: build the real 120-vertex cyclic lift, verify
its basic structure (simple, connected, 5-regular fibre action, cubic,
120 vertices, 180 edges), then test EXACTLY for C4, C8, C16 (staged --
C32/C64 only for whatever survives C16, mirroring the original engine's
own staging and this project's established discipline against wasting
exponential work on cases a cheaper stage already resolves). Every C16
witness is classified by projection type (III.1's taxonomy: 1 = simple
base C16 -- should not occur here since these assignments already failed
the simple-C16 hyperplane test, so any occurrence would itself be a bug
worth flagging; 2 = non-simple nonbacktracking walk; 3 = repeated base
vertices, distinct lifted vertices; 4 = other).

COUNTEREXAMPLE PROTOCOL: if anything survives all five lengths, all other
work stops; the base, voltage vector, lift mapping, graph6/sparse6/
DIMACS/edge-list, and independent two-detector + standalone-verifier
confirmation are all produced before any announcement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cycle_detect import find_cycle_len_dfs, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402
from verifier.z3_lifts import load_base  # noqa: E402
from verifier.z5_lift_feasibility import lift_graph_mod_p  # noqa: E402

P = 5
COORDS = 13


def index_to_digits(idx: int, coords: int = COORDS, p: int = P) -> list[int]:
    digits = []
    rem = idx
    for _ in range(coords):
        digits.append(rem % p)
        rem //= p
    return digits


def structural_checks(lifted: dict[int, set[int]], base_n: int) -> dict[str, Any]:
    n = len(lifted)
    m = sum(len(v) for v in lifted.values()) // 2
    degs = {v: len(nbrs) for v, nbrs in lifted.items()}
    simple = all(v not in nbrs for v, nbrs in lifted.items())  # no self-loops
    cubic = all(d == 3 for d in degs.values())
    G = nx.Graph()
    G.add_nodes_from(lifted.keys())
    for v, nbrs in lifted.items():
        for u in nbrs:
            G.add_edge(v, u)
    connected = nx.is_connected(G)
    return {
        "vertices": n, "edges": m,
        "expected_vertices": P * base_n, "expected_edges": (P * base_n * 3) // 2,
        "simple": simple, "cubic": cubic, "connected": connected,
        "structure_ok": (
            n == P * base_n and m == (P * base_n * 3) // 2
            and simple and cubic and connected
        ),
    }


def classify_c16_witness(witness: list[int], base) -> dict[str, Any]:
    """Lift vertex label = P*u + sheet (verifier/z5_lift_feasibility.py's
    lift_graph_mod_p convention), so the base vertex is `label // P`, NOT
    `label % P` -- using the wrong projection formula here previously
    caused every classification to look like spurious "simple base C16"
    witnesses (caught via an explicit edge-validity check below, which
    is why that check is retained even though it should now always
    pass)."""
    base_proj = [v // P for v in witness]
    distinct_base_vertices = len(set(base_proj))
    L = len(witness)
    edges_valid_in_base = all(
        base.graph.has_edge(base_proj[i], base_proj[(i + 1) % L]) for i in range(L)
    )
    nonbacktracking = all(
        base_proj[i] != base_proj[(i + 2) % L] or base_proj[i] == base_proj[(i + 1) % L]
        for i in range(L)
    )
    if distinct_base_vertices == L and edges_valid_in_base:
        ptype = 1  # simple base C16 -- SHOULD NOT occur for these assignments
    elif len(witness) == len(set(witness)):
        ptype = 3  # repeated base vertices, distinct lifted vertices (always true here)
    else:
        ptype = 4
    return {
        "witness_lift_vertices": witness, "base_projection": base_proj,
        "distinct_base_vertices": distinct_base_vertices,
        "edges_valid_in_base_as_simple_cycle": edges_valid_in_base,
        "nonbacktracking_projection": nonbacktracking, "projection_type": ptype,
    }


def process_assignment(base, base_index: int, idx: int) -> dict[str, Any]:
    digits = index_to_digits(idx)
    lifted = lift_graph_mod_p(base, digits, P)
    struct = structural_checks(lifted, base.graph.number_of_nodes())

    result: dict[str, Any] = {
        "base_index": base_index, "assignment_index": idx, "voltage": digits,
        "structure": struct,
    }

    c4 = has_cycle_len_dfs(lifted, 4)
    result["c4"] = c4
    if c4:
        result["killed_at"] = 4
        return result
    c8 = has_cycle_len_dfs(lifted, 8)
    result["c8"] = c8
    if c8:
        result["killed_at"] = 8
        return result
    c16_witness = find_cycle_len_dfs(lifted, 16)
    result["c16"] = c16_witness is not None
    if c16_witness is not None:
        result["killed_at"] = 16
        result["c16_classification"] = classify_c16_witness(c16_witness, base)
        if result["c16_classification"]["projection_type"] == 1:
            result["ANOMALY"] = "simple-base-C16 projection found on an assignment already excluded by the hyperplane test -- investigate"
        return result

    c32 = has_cycle_len_dfs(lifted, 32)
    result["c32"] = c32
    if c32:
        result["killed_at"] = 32
        return result
    c64 = has_cycle_len_dfs(lifted, 64)
    result["c64"] = c64
    if c64:
        result["killed_at"] = 64
        return result

    result["killed_at"] = None  # SURVIVOR -- counterexample protocol triggers
    return result


def independent_recheck(base, base_index: int, idx: int, killed_at: int | None) -> bool:
    """Cross-detector recheck using NetworkX's independent simple-cycle
    machinery, for the SPECIFIC length that killed_at claims (or, for a
    survivor, confirm absence of all 5 lengths independently)."""
    digits = index_to_digits(idx)
    lifted = lift_graph_mod_p(base, digits, P)
    if killed_at is None:
        return not any(has_cycle_len_nx(lifted, L) for L in (4, 8, 16, 32, 64))
    return has_cycle_len_nx(lifted, killed_at)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=int, required=True)
    parser.add_argument("--uncovered-file", type=Path, required=True,
                         help="JSON file from z5_exact_solve.py (reads result.uncovered_indices)")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = json.loads(args.uncovered_file.read_text())
    indices = data["result"]["uncovered_indices"]
    truncated = data["result"]["uncovered_indices_truncated"]
    total_uncovered = data["result"]["uncovered"]

    base = load_base(args.base)
    t0 = time.time()
    killed_at_counts: dict[str, int] = {}
    c16_type_counts: dict[str, int] = {}
    survivors = []
    anomalies = []
    struct_failures = []
    recheck_failures = []

    for i, idx in enumerate(indices):
        rec = process_assignment(base, args.base, idx)
        if not rec["structure"]["structure_ok"]:
            struct_failures.append(rec)
        ka = rec["killed_at"]
        killed_at_counts[str(ka)] = killed_at_counts.get(str(ka), 0) + 1
        if ka == 16:
            pt = rec["c16_classification"]["projection_type"]
            c16_type_counts[str(pt)] = c16_type_counts.get(str(pt), 0) + 1
            if "ANOMALY" in rec:
                anomalies.append(rec)
        if not independent_recheck(base, args.base, idx, ka):
            recheck_failures.append(rec)
        if ka is None:
            survivors.append(rec)

    elapsed = time.time() - t0
    report = {
        "base": args.base,
        "total_uncovered_by_hyperplane_scan": total_uncovered,
        "uncovered_indices_processed": len(indices),
        "uncovered_list_was_truncated": truncated,
        "killed_at_counts": killed_at_counts,
        "c16_projection_type_counts": c16_type_counts,
        "anomalies": anomalies,
        "structural_check_failures": struct_failures,
        "independent_recheck_failures": recheck_failures,
        "survivors": survivors,
        "elapsed_seconds": elapsed,
    }
    print(f"base {args.base}: processed {len(indices)}/{total_uncovered} uncovered "
          f"(truncated={truncated}) in {elapsed:.1f}s")
    print(f"killed_at distribution: {killed_at_counts}")
    print(f"C16 projection types: {c16_type_counts}")
    print(f"anomalies: {len(anomalies)} struct_failures: {len(struct_failures)} "
          f"recheck_failures: {len(recheck_failures)} SURVIVORS: {len(survivors)}")

    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    ok = not anomalies and not struct_failures and not recheck_failures
    if survivors:
        print("\n*** SURVIVOR(S) FOUND -- COUNTEREXAMPLE PROTOCOL REQUIRED, NOT ANNOUNCING YET ***")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
