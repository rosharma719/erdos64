#!/usr/bin/env python3
"""Quotient-cycle cardinality-constraint (pseudo-Boolean/CP-SAT) solver for
the order-30 triangle-quotient census -- the "replace expansion enumeration
with quotient-cycle constraints" direction.

For a cubic quotient Q and target mark count k: one Boolean variable x_v per
vertex. For every simple cycle C of Q (length l, vertex set V(C)), let
e = sum_{v in V(C)} x_v. The expansion of a marking realizes every lifted
cycle length in [l+e, l+2e] (proved elsewhere, independently cross-checked
0/218+ mismatches in order30_quotient_census.md/order30_near_miss_classification.md).
So a marking is feasible only if, for every cycle, e avoids every value that
would put a forbidden power of two (4, 8, 16 at order 30; also 32 if the
quotient order + 2*mark_count = 32) inside that interval. This is a small
integer-domain constraint per cycle, not a subset-enumeration -- the whole
point is to let a CP-SAT/PB solver search the *marking* space directly
instead of the caller enumerating all C(n,k) markings up front.

This is meant to be validated (--validate) against the exhaustive
brute-force census before being trusted prospectively at orders where
C(n,k) is too large to enumerate directly (order 22 and up).

Usage:
    # single quotient, decide SAT/UNSAT for a given (n,k):
    python verifier/order30_quotient_pbsat.py solve --graph6 <g6> --k 7

    # validate against the already-exhaustive order-16/18/20 catalogs:
    python verifier/order30_quotient_pbsat.py validate \
        data/order30_quotient_census/quotients_16v_3connected.g6.gz --n 16 --k 7 --sample 200
"""

from __future__ import annotations

import argparse
import gzip
import time
from pathlib import Path

import networkx as nx
from ortools.sat.python import cp_model

FORBIDDEN = (4, 8, 16, 32)


def load_catalog(path: Path) -> list[str]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as f:
        return [line.strip() for line in f if line.strip()]


def enumerate_cycles(graph: nx.Graph) -> list[tuple[list[int], int]]:
    out = []
    for cyc in nx.simple_cycles(graph, length_bound=graph.number_of_nodes()):
        out.append((cyc, len(cyc)))
    return out


def forbidden_e_values(length: int, max_e: int, forbidden_lengths: tuple[int, ...]) -> set[int]:
    """e values (0..max_e) for which [length+e, length+2e] hits a forbidden
    power of two."""
    bad = set()
    for e in range(0, max_e + 1):
        lo, hi = length + e, length + 2 * e
        if any(lo <= f <= hi for f in forbidden_lengths):
            bad.add(e)
    return bad


def build_and_solve(graph: nx.Graph, k: int, forbidden_lengths: tuple[int, ...] = (4, 8, 16),
                     time_limit_s: float = 30.0) -> tuple[str, list[int] | None, dict]:
    """Returns (status, marking_or_None, stats). status in
    {"SAT","UNSAT","UNKNOWN"}."""
    model = cp_model.CpModel()
    n = graph.number_of_nodes()
    nodes = sorted(graph.nodes())
    x = {v: model.NewBoolVar(f"x{v}") for v in nodes}

    cycles = enumerate_cycles(graph)
    n_constraints = 0
    for cyc, length in cycles:
        max_e = len(cyc)
        bad_e = forbidden_e_values(length, max_e, forbidden_lengths)
        if not bad_e:
            continue
        e_expr = sum(x[v] for v in cyc)
        for bad in bad_e:
            model.Add(e_expr != bad)
            n_constraints += 1

    model.Add(sum(x[v] for v in nodes) == k)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_search_workers = 1
    t0 = time.time()
    status = solver.Solve(model)
    elapsed = time.time() - t0

    stats = {"cycles": len(cycles), "cardinality_constraints": n_constraints, "elapsed_seconds": elapsed}
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        marking = [v for v in nodes if solver.Value(x[v])]
        return "SAT", marking, stats
    if status == cp_model.INFEASIBLE:
        return "UNSAT", None, stats
    return "UNKNOWN", None, stats


def cmd_solve(args: argparse.Namespace) -> None:
    graph = nx.from_graph6_bytes(args.graph6.encode())
    status, marking, stats = build_and_solve(graph, args.k, time_limit_s=args.time_limit)
    print(f"status={status} marking={marking}")
    print(stats)


def cmd_validate(args: argparse.Namespace) -> None:
    import math
    import random

    g6s = load_catalog(args.catalog)
    random.seed(args.seed)
    sample = g6s if len(g6s) <= args.sample else random.sample(g6s, args.sample)

    t0 = time.time()
    n_sat, n_unsat, n_unknown = 0, 0, 0
    mismatches = []
    for i, g6 in enumerate(sample):
        graph = nx.from_graph6_bytes(g6.encode())
        status, marking, stats = build_and_solve(graph, args.k, time_limit_s=args.time_limit)
        if status == "SAT":
            n_sat += 1
            # cross-check: literally verify this marking really is clean
            print(f"  !!! SAT found (unexpected if this catalog is fully eliminated): {g6} marked={marking}")
            mismatches.append({"graph6": g6, "marking": marking, "status": status})
        elif status == "UNSAT":
            n_unsat += 1
        else:
            n_unknown += 1
            mismatches.append({"graph6": g6, "status": status})
        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{len(sample)}: SAT={n_sat} UNSAT={n_unsat} UNKNOWN={n_unknown} "
                  f"elapsed={time.time() - t0:.1f}s", flush=True)

    print(f"\nDONE: {len(sample)} quotients, SAT={n_sat} UNSAT={n_unsat} UNKNOWN={n_unknown}, "
          f"elapsed={time.time() - t0:.1f}s")
    print(f"Expected (per exhaustive brute-force census): all UNSAT, 0 SAT, 0 UNKNOWN.")
    print(f"Match: {'YES' if n_sat == 0 and n_unknown == 0 else 'NO -- MISMATCH, investigate'}")
    if mismatches:
        print("Mismatches:", mismatches[:10])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_solve = sub.add_parser("solve")
    p_solve.add_argument("--graph6", required=True)
    p_solve.add_argument("--k", type=int, required=True)
    p_solve.add_argument("--time-limit", type=float, default=30.0)
    p_solve.set_defaults(func=cmd_solve)

    p_val = sub.add_parser("validate")
    p_val.add_argument("catalog", type=Path)
    p_val.add_argument("--n", type=int, required=True)
    p_val.add_argument("--k", type=int, required=True)
    p_val.add_argument("--sample", type=int, default=200)
    p_val.add_argument("--seed", type=int, default=0)
    p_val.add_argument("--time-limit", type=float, default=30.0)
    p_val.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
