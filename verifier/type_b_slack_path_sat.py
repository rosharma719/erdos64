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
