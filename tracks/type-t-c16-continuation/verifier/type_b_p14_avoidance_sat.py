#!/usr/bin/env python3
"""
Witness-AVOIDANCE models (not witness enumeration): for a given fixed path +
degree-deficit system, ask directly "does a completion exist that avoids C4,
C8, AND a forbidden a-y path length (e.g. 14)?" via CEGAR against a fresh,
from-scratch backtracking a-y path detector (independent of motif_mine.py and
of networkx).

This is the priority follow-up requested after `type_b_witness_motif_analysis.md`:
that file only ever enumerated *witnesses* inside the (already fully known)
C4/C8-avoiding completion set. This script instead builds the completion set
under the STRONGER constraint set {no C4, no C8, no forbidden-length a-y path}
directly via CEGAR blocking, and separately supports relaxed geometries (extra
off-path vertex, extra path vertex) to test whether the forcing persists.

Independent of verifier/type_b_order40_slot_sat.py's `search()`: re-implements
its own a-y path detector rather than importing motif_mine.py's networkx-based
one, though it reuses the same PySAT cardinality-constraint pattern (that
pattern itself is just "exact degree per vertex", not part of what's being
independently verified here -- the a-y path detector is the new part).
"""
from __future__ import annotations
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Glucose3
from pysat.formula import IDPool

from cycle_detect import find_cycle_len_dfs, from_edges


def find_ay_path_len_dfs(g, a, y, L):
    """Fresh backtracking search for a simple a-y path of exactly L edges.
    Independent implementation (does not call networkx or motif_mine.py)."""
    path = [a]
    visited = {a}

    def dfs(u, depth):
        if depth == L:
            return list(path) if u == y else None
        for w in g[u]:
            if w in visited:
                continue
            path.append(w)
            visited.add(w)
            res = dfs(w, depth + 1)
            if res is not None:
                return res
            path.pop()
            visited.discard(w)
        return None

    return dfs(a, 0)


def candidate_edges(nv, path_edges):
    path_set = set(path_edges)
    edges = []
    for u in range(nv):
        for v in range(u + 1, nv):
            if (u, v) in path_set:
                continue
            edges.append((u, v))
    return edges


def search_avoid(nv, path_edges, deficits, total_non_path_edges, a, y,
                  forbidden_lengths=(14,), max_solutions=1, verbose=False):
    """CEGAR search for a completion satisfying exact degree deficits while
    avoiding C4, C8, and every length in forbidden_lengths (simple a-y paths).

    Returns (solutions, n_blocked) where solutions is a list of surviving
    edge-sets (empty if the model is UNSAT -- i.e. every valid completion was
    blocked for containing C4, C8, or a forbidden-length a-y path) and
    n_blocked is how many distinct completions were visited and blocked.
    Stops early once max_solutions survivors are found (default 1: we only
    need to know whether the model is SAT or UNSAT, and one witness suffices
    if SAT)."""
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
    n_blocked = 0
    with Glucose3(bootstrap_with=base_clauses) as solver:
        while solver.solve():
            model = set(solver.get_model())
            chosen = [e for e in edges if edge_var[e] in model]
            assert len(chosen) == total_non_path_edges

            g = from_edges(nv, path_edges + chosen)
            c4 = find_cycle_len_dfs(g, 4)
            c8 = None if c4 is not None else find_cycle_len_dfs(g, 8)
            forbidden_path = None
            if c4 is None and c8 is None:
                for L in forbidden_lengths:
                    p = find_ay_path_len_dfs(g, a, y, L)
                    if p is not None:
                        forbidden_path = p
                        break

            if c4 is None and c8 is None and forbidden_path is None:
                solutions.append(sorted(chosen))
                if verbose:
                    print("  SURVIVOR found:", sorted(chosen))
                solver.add_clause([-edge_var[e] for e in chosen])
                if len(solutions) >= max_solutions:
                    break
                continue

            n_blocked += 1
            if c4 is not None:
                witness = c4
            elif c8 is not None:
                witness = c8
            else:
                witness = forbidden_path
            cyclic = witness is c4 or witness is c8
            witness_edges = []
            rng = len(witness) if cyclic else len(witness) - 1
            for i in range(rng):
                uu, vv = witness[i], witness[(i + 1) % len(witness)]
                key = (uu, vv) if uu < vv else (vv, uu)
                if key in edge_var:
                    witness_edges.append(key)
            solver.add_clause([-edge_var[e] for e in witness_edges])

    return solutions, n_blocked


# ---------------------------------------------------------------------------
# Baseline geometries (identical degree systems to the existing E=29 layers)
# ---------------------------------------------------------------------------

def gap2_e29_geometry():
    nv = 20
    path_edges = [(i, i + 1) for i in range(18)]
    deficit = {v: 1 for v in range(19)}
    deficit[19] = 3
    return nv, path_edges, deficit, 11, 0, 18


def gap1_e29_geometry():
    nv = 20
    path_edges = [(i, i + 1) for i in range(17)]
    deficit = {v: 1 for v in range(18)}
    deficit[18] = 3
    deficit[19] = 3
    return nv, path_edges, deficit, 12, 0, 17


# ---------------------------------------------------------------------------
# Relaxation 1: one EXTRA off-path vertex added to the gap2 geometry (same
# path length 18, now TWO off-path vertices instead of one; total order 21).
# Parity forces one of the two off-path vertices to degree 4 (both must be
# >=3 for a valid delta>=3 remainder; 3+3 with the existing 19 path-demand
# units is odd, so the smallest valid fix is one vertex at degree 4).
# ---------------------------------------------------------------------------

def gap2_e29_extra_z_geometry():
    nv = 21
    path_edges = [(i, i + 1) for i in range(18)]
    deficit = {v: 1 for v in range(19)}
    deficit[19] = 3
    deficit[20] = 4
    total_non_path_edges = (19 + 3 + 4) // 2
    return nv, path_edges, deficit, total_non_path_edges, 0, 18


# ---------------------------------------------------------------------------
# Relaxation 2: one EXTRA distinguished-path vertex (path length 18 -> 19),
# single off-path vertex, same total order 21. Parity forces the off-path
# vertex to degree 4 (19 path-demand units [now 1(a)+1(y)+18 interior=20,
# wait recompute] -- see geometry function for exact bookkeeping).
# ---------------------------------------------------------------------------

def gap2_e29_extra_path_geometry():
    nv = 21
    path_edges = [(i, i + 1) for i in range(19)]  # a=0..y=19, 20 path vertices
    deficit = {v: 1 for v in range(20)}
    deficit[20] = 4
    total_non_path_edges = (20 + 4) // 2
    return nv, path_edges, deficit, total_non_path_edges, 0, 19


if __name__ == "__main__":
    import sys

    experiments = [
        ("gap2_e29 (baseline, M14)", gap2_e29_geometry, (14,)),
        ("gap1_e29 (baseline, M14)", gap1_e29_geometry, (14,)),
        ("gap2_e29 + extra off-path vertex (relaxation 1, M14)", gap2_e29_extra_z_geometry, (14,)),
        ("gap2_e29 + extra path vertex (relaxation 2, M14)", gap2_e29_extra_path_geometry, (14,)),
    ]

    only = sys.argv[1] if len(sys.argv) > 1 else None

    for name, geom_fn, forbidden in experiments:
        if only is not None and only not in name:
            continue
        nv, path_edges, deficit, total, a, y = geom_fn()
        t0 = time.time()
        sols, n_blocked = search_avoid(nv, path_edges, deficit, total, a, y,
                                        forbidden_lengths=forbidden, max_solutions=5)
        dt = time.time() - t0
        status = "SAT (survivor found!)" if sols else "UNSAT (every completion blocked)"
        print(f"[{name}] nv={nv} edges={total} forbidden={forbidden} "
              f"-> {status}  n_blocked={n_blocked}  n_survivors_found={len(sols)}  time={dt:.2f}s")
        if sols:
            print("   survivor edges (non-path):", sols[0])
