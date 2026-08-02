#!/usr/bin/env python3
"""Generic independent SAT slot-matching generator for the order-40
frontier (order-21 bridge remainders, both gap types, all edge-count
layers). See type_b_order40_frontier.md.

Deliberately independent of the C generators in this directory: shares
only the mathematical definition of a fixed path, a per-vertex degree
deficit dict, and the total-non-path-edge target. Does not import any C
file's recursion, cycle detector, or output.

Parametrized so the same code serves every layer (gap-1/gap-2, E=29/30/31)
rather than being rewritten per layer.
"""

from __future__ import annotations

from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose3
from pysat.formula import IDPool

from cycle_detect import find_cycle_len_dfs, from_edges


def candidate_edges(nv: int, path_edges: list):
    path_set = set(path_edges)
    edges = []
    for u in range(nv):
        for v in range(u + 1, nv):
            if (u, v) in path_set:
                continue
            edges.append((u, v))
    return edges


def search(nv: int, path_edges: list, deficits: dict, total_non_path_edges: int,
           max_solutions=None):
    """Enumerate every C4/C8-free completion matching the exact deficits.
    deficits: dict vertex -> required additional degree beyond path degree.
    Returns a list of solutions, each a sorted list of chosen non-path edges."""
    edges = candidate_edges(nv, path_edges)
    pool = IDPool()
    edge_var = {e: pool.id(("e", e)) for e in edges}

    incident = {v: [] for v in range(nv)}
    for e in edges:
        incident[e[0]].append(edge_var[e])
        incident[e[1]].append(edge_var[e])

    base_clauses = []
    for v in range(nv):
        bound = deficits.get(v, 0)
        if incident[v]:
            base_clauses += CardEnc.equals(
                lits=incident[v], bound=bound, vpool=pool,
                encoding=EncType.seqcounter
            ).clauses
        elif bound != 0:
            base_clauses.append([])

    total_edge_vars = list(edge_var.values())
    base_clauses += CardEnc.equals(
        lits=total_edge_vars, bound=total_non_path_edges, vpool=pool,
        encoding=EncType.seqcounter
    ).clauses

    solutions = []
    with Glucose3(bootstrap_with=base_clauses) as solver:
        while solver.solve():
            model = set(solver.get_model())
            chosen = [e for e in edges if edge_var[e] in model]
            assert len(chosen) == total_non_path_edges

            g = from_edges(nv, path_edges + chosen)
            c4 = find_cycle_len_dfs(g, 4)
            c8 = None if c4 is not None else find_cycle_len_dfs(g, 8)

            if c4 is None and c8 is None:
                solutions.append(sorted(chosen))
                solver.add_clause([-edge_var[e] for e in chosen])
            else:
                witness = c4 if c4 is not None else c8
                witness_edges = []
                for i in range(len(witness)):
                    a, b = witness[i], witness[(i + 1) % len(witness)]
                    key = (a, b) if a < b else (b, a)
                    if key in edge_var:
                        witness_edges.append(key)
                solver.add_clause([-edge_var[e] for e in witness_edges])

            if max_solutions is not None and len(solutions) >= max_solutions:
                break

    return solutions


def gap2_e29_deficits():
    """19-vertex path p0..p18 (18 edges) + z=vertex19. a=p0, y=p18."""
    nv = 20
    path_edges = [(i, i + 1) for i in range(18)]
    deficit = {v: 1 for v in range(19)}
    deficit[19] = 3
    return nv, path_edges, deficit, 11


def gap1_e29_deficits():
    """18-vertex path p0..p17 (17 edges) + z1,z2=vertices18,19. a=p0, y=p17."""
    nv = 20
    path_edges = [(i, i + 1) for i in range(17)]
    deficit = {v: 1 for v in range(18)}
    deficit[18] = 3
    deficit[19] = 3
    return nv, path_edges, deficit, 12


if __name__ == "__main__":
    import sys
    import time
    import json

    nv, path_edges, deficit, total = gap2_e29_deficits()
    t0 = time.time()
    sols = search(nv, path_edges, deficit, total)
    print(f"gap2_e29: solutions={len(sols)} time={time.time()-t0:.2f}s")
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w") as f:
            json.dump([sorted(list(e) for e in s) for s in sols], f, indent=2)
