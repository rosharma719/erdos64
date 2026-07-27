#!/usr/bin/env python3
"""Independent SAT-based cross-check for the one-slack 28-edge remainder
layer (type_b_one_slack.md, Section 4).

This is algorithmically independent of verifier/cycle_detect.py (DFS
backtracking + networkx simple_cycles): it encodes "does concrete graph G
contain a simple cycle of length exactly L" as a CNF instance (position
variables x[v][i] = "vertex v occupies position i of the L-cycle") and asks
a SAT solver, rather than searching paths directly.

Also encodes Hamiltonian-path-with-fixed-endpoint existence as CNF, to
cross-check verifier/type_b_slack_family_filter.py's stage 2 DFS search.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Glucose3

Graph = Dict[int, Set[int]]


def sat_cycle_len_exists(g: Graph, n: int, L: int) -> bool:
    """SAT encoding: does g contain a simple cycle of length exactly L?"""
    pool = IDPool()
    var = lambda v, i: pool.id(("pos", v, i))

    with Glucose3(bootstrap_with=[]) as solver:
        clauses: List[List[int]] = []

        # exactly one vertex per position
        for i in range(L):
            lits = [var(v, i) for v in range(n)]
            clauses += CardEnc.equals(lits=lits, bound=1, vpool=pool,
                                       encoding=EncType.seqcounter).clauses

        # each vertex used at most once across positions
        for v in range(n):
            lits = [var(v, i) for i in range(L)]
            clauses += CardEnc.atmost(lits=lits, bound=1, vpool=pool,
                                       encoding=EncType.seqcounter).clauses

        # adjacency along consecutive cycle positions
        for i in range(L):
            j = (i + 1) % L
            for v in range(n):
                for w in range(n):
                    if v == w:
                        continue
                    if w not in g[v]:
                        clauses.append([-var(v, i), -var(w, j)])

        # symmetry break: position 0 is the minimum vertex used
        # (fix vertex 0 to be eligible at position 0 only if it can occur at all;
        # simplest safe symmetry break: forbid vertex 0 from any position != 0)
        for i in range(1, L):
            clauses.append([-var(0, i)])

        for clause in clauses:
            solver.add_clause(clause)
        return solver.solve()


def sat_ham_path_from(g: Graph, vertices: List[int], start: int) -> bool:
    """SAT encoding: does the induced subgraph on `vertices` have a
    Hamiltonian path starting at `start`?"""
    m = len(vertices)
    index_of = {v: idx for idx, v in enumerate(vertices)}
    pool = IDPool()
    var = lambda v, i: pool.id(("hp", v, i))

    with Glucose3(bootstrap_with=[]) as solver:
        clauses: List[List[int]] = []

        for i in range(m):
            lits = [var(v, i) for v in vertices]
            clauses += CardEnc.equals(lits=lits, bound=1, vpool=pool,
                                       encoding=EncType.seqcounter).clauses

        for v in vertices:
            lits = [var(v, i) for i in range(m)]
            clauses += CardEnc.equals(lits=lits, bound=1, vpool=pool,
                                       encoding=EncType.seqcounter).clauses

        clauses.append([var(start, 0)])

        for i in range(m - 1):
            for v in vertices:
                for w in vertices:
                    if v == w:
                        continue
                    if w not in g[v]:
                        clauses.append([-var(v, i), -var(w, i + 1)])

        for clause in clauses:
            solver.add_clause(clause)
        return solver.solve()



# =============================================================================
# Independent SAT-based generator for the Family II (2^2,3^16,4) layer.
#
# This is deliberately independent of verifier/type_b_slack_path_search.c's
# generator: it does not import that file's recursion, its incremental
# cycle-pruning routine, or its output as a candidate population. It shares
# only the mathematical definition of the fixed path (vertices 0..17),
# off-path vertex z (vertex 18), the per-role degree-deficit vector, and the
# set of allowed non-path candidate edges.
#
# Model: one boolean variable per allowed non-path edge. Degree constraints
# are exact-cardinality constraints (CardEnc.equals) forcing each vertex's
# total additional degree (beyond its fixed path degree) to match the
# required deficit for the given role. C4/C8-freeness is enforced by a
# CEGAR loop: solve for a degree-feasible model, check the induced graph for
# a C4 or C8 with verifier/cycle_detect.py's independent DFS detector (not
# the C file's), and if one is found, add a blocking clause forbidding that
# exact set of chosen candidate edges from recurring, then resolve. This
# repeats until UNSAT (all C4/C8-free completions for this role have been
# enumerated).
# =============================================================================

from cycle_detect import find_cycle_len_dfs as _cd_find_cycle_len_dfs
from cycle_detect import from_edges as _cd_from_edges

SAT_NV = 19       # vertices 0..17 = path, 18 = z
SAT_PATH_EDGES = [(i, i + 1) for i in range(17)]


def sat_family_ii_candidate_edges():
    """All vertex pairs on 0..18 except the 17 fixed path edges."""
    path_set = set(SAT_PATH_EDGES)
    edges = []
    for u in range(SAT_NV):
        for v in range(u + 1, SAT_NV):
            if (u, v) in path_set:
                continue
            edges.append((u, v))
    return edges


def sat_family_ii_deficits(role):
    """role: 1..16 means p_role carries the +1 excess (degree 4);
    role == 'z' means z carries it. Mirrors type_b_one_slack_resolution.md
    Section 1, derived independently here (not imported from the C file)."""
    deficit = {v: 0 for v in range(SAT_NV)}
    deficit[0] = 1   # a = p0
    deficit[17] = 1  # y = p17
    for i in range(1, 17):
        deficit[i] = 1
    deficit[18] = 3  # z
    if role == "z":
        deficit[18] = 4
    else:
        deficit[role] = 2
    return deficit


def sat_family_ii_search_role(role, max_solutions=None):
    """Enumerate every C4/C8-free completion for the given role. Returns a
    list of solutions, each a sorted list of the 11 chosen candidate edges."""
    edges = sat_family_ii_candidate_edges()
    deficit = sat_family_ii_deficits(role)
    pool = IDPool()
    edge_var = {e: pool.id(("e", e)) for e in edges}

    incident = {v: [] for v in range(SAT_NV)}
    for e in edges:
        incident[e[0]].append(edge_var[e])
        incident[e[1]].append(edge_var[e])

    base_clauses: List[List[int]] = []
    for v in range(SAT_NV):
        if incident[v]:
            base_clauses += CardEnc.equals(
                lits=incident[v], bound=deficit[v], vpool=pool,
                encoding=EncType.seqcounter
            ).clauses
        elif deficit[v] != 0:
            base_clauses.append([])  # unsatisfiable: no incident edges but nonzero deficit

    total_edge_vars = list(edge_var.values())
    base_clauses += CardEnc.equals(
        lits=total_edge_vars, bound=11, vpool=pool, encoding=EncType.seqcounter
    ).clauses

    solutions = []
    with Glucose3(bootstrap_with=base_clauses) as solver:
        while solver.solve():
            model = set(solver.get_model())
            chosen = [e for e in edges if edge_var[e] in model]
            assert len(chosen) == 11

            g = _cd_from_edges(SAT_NV, SAT_PATH_EDGES + chosen)
            c4 = _cd_find_cycle_len_dfs(g, 4)
            c8 = None if c4 is not None else _cd_find_cycle_len_dfs(g, 8)

            if c4 is None and c8 is None:
                solutions.append(sorted(chosen))
                # block this exact solution to move on to the next distinct one
                solver.add_clause([-edge_var[e] for e in chosen])
            else:
                witness = c4 if c4 is not None else c8
                witness_edges = []
                for i in range(len(witness)):
                    a, b = witness[i], witness[(i + 1) % len(witness)]
                    key = (a, b) if a < b else (b, a)
                    if key in edge_var:
                        witness_edges.append(key)
                # block: at least one candidate edge of this witness cycle
                # must be absent (forbids this exact violating combination)
                solver.add_clause([-edge_var[e] for e in witness_edges])

            if max_solutions is not None and len(solutions) >= max_solutions:
                break

    return solutions


if __name__ == "__main__":
    # smoke test: an 8-cycle graph on 8 vertices must satisfy sat_cycle_len_exists(_, 8, 8)
    n = 8
    g = {v: set() for v in range(n)}
    for v in range(n):
        g[v].add((v + 1) % n)
        g[(v + 1) % n].add(v)
    assert sat_cycle_len_exists(g, n, 8) is True
    assert sat_cycle_len_exists(g, n, 4) is False
    print("smoke test passed")
