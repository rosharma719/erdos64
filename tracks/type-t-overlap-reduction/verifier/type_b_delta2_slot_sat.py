#!/usr/bin/env python3
"""Independent SAT-based generator for the zero-slack delta=2 Type-B bridge
remainder layer (see type_b_delta2_zero_slack.md).

Deliberately independent of verifier/type_b_delta2_slot_search.c: shares
only the mathematical definition of the fixed 19-vertex path (p_0=a,
p_18=y), the per-role degree-deficit vector, and the candidate-edge
universe. Does not import that file's recursion, its incremental
cycle-pruning routine, or its output as a starting population.

Model: one boolean variable per allowed non-path edge (153 of them). Exact
cardinality constraints per vertex deficit plus a total-of-10 constraint.
CEGAR loop against verifier/cycle_detect.py's independent DFS detector
(not the C file's) for C4/C8-freeness.
"""

from __future__ import annotations

from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose3
from pysat.formula import IDPool

from cycle_detect import find_cycle_len_dfs, from_edges

D2_NV = 19  # vertices 0..18, all on the path (no off-path vertex)
D2_PATH_EDGES = [(i, i + 1) for i in range(18)]


def d2_candidate_edges():
    path_set = set(D2_PATH_EDGES)
    edges = []
    for u in range(D2_NV):
        for v in range(u + 1, D2_NV):
            if (u, v) in path_set:
                continue
            edges.append((u, v))
    return edges


def d2_deficits(role: int):
    """role in 1..17: p_role carries the +1 excess (degree 4). a=p0, y=p18
    always need exactly 1 additional edge; all other internal vertices need
    exactly 1 except the role vertex, which needs 2."""
    deficit = {v: 1 for v in range(D2_NV)}
    deficit[role] = 2
    return deficit


def d2_search_role(role: int):
    edges = d2_candidate_edges()
    deficit = d2_deficits(role)
    pool = IDPool()
    edge_var = {e: pool.id(("e", e)) for e in edges}

    incident = {v: [] for v in range(D2_NV)}
    for e in edges:
        incident[e[0]].append(edge_var[e])
        incident[e[1]].append(edge_var[e])

    base_clauses = []
    for v in range(D2_NV):
        base_clauses += CardEnc.equals(
            lits=incident[v], bound=deficit[v], vpool=pool,
            encoding=EncType.seqcounter
        ).clauses

    total_edge_vars = list(edge_var.values())
    base_clauses += CardEnc.equals(
        lits=total_edge_vars, bound=10, vpool=pool, encoding=EncType.seqcounter
    ).clauses

    solutions = []
    with Glucose3(bootstrap_with=base_clauses) as solver:
        while solver.solve():
            model = set(solver.get_model())
            chosen = [e for e in edges if edge_var[e] in model]
            assert len(chosen) == 10

            g = from_edges(D2_NV, D2_PATH_EDGES + chosen)
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

    return solutions


if __name__ == "__main__":
    import sys
    import time

    all_results = {}
    for role in range(1, 18):
        t0 = time.time()
        sols = d2_search_role(role)
        all_results[str(role)] = [sorted(list(e) for e in s) for s in sols]
        print(f"role={role} solutions={len(sols)} time={time.time()-t0:.2f}s", flush=True)
    total = sum(len(v) for v in all_results.values())
    print("total:", total)

    if len(sys.argv) > 1:
        import json
        with open(sys.argv[1], "w") as f:
            json.dump(all_results, f, indent=2)
