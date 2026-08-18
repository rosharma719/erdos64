#!/usr/bin/env python3
"""INDEPENDENT CP-SAT re-implementation of the FC-N / F-N existence question.

This is deliberately a *second, separate* implementation of the same decision
problem that `verifier/fcn_sat_existence.py` solves with PySAT/CDCL, written to
share no encoding code with it:

  * different engine            -- OR-Tools CP-SAT instead of a CDCL SAT solver
  * different degree encoding   -- native integer linear constraints
                                   (`sum(row) == d`) instead of sequential-
                                   counter cardinality clauses
  * different C4 encoding       -- "at most one common neighbour" via reified
                                   AND variables and `AddAtMostOne`, instead of
                                   one explicit 4-literal clause per 4-cycle
  * different symmetry breaking -- degree-monotone ordering of the
                                   interchangeable vertex block, instead of
                                   lex-maximal adjacency serialisation
  * different cycle enumeration -- `networkx.simple_cycles` instead of the
                                   hand-written rooted DFS

Only the CEGAR *idea* (lazily block each 8-cycle found in a candidate) is
shared, because that is the mathematical content, not an implementation detail.

If both implementations report UNSAT for the same (n, d_x), that is a genuine
dual-implementation cross-check of the kind this project already applies to its
C4/C8 detectors -- a bug would have to be present in both, in two different
solver engines with two different encodings of every constraint.

Usage:
    python verifier/fcn_cpsat_existence.py --n 16 --dx 2 --time-limit 1800
    python verifier/fcn_cpsat_existence.py --sweep 13 18 --dx 2 --time-limit 1800
"""

from __future__ import annotations

import argparse
import itertools
import json
import time

import networkx as nx
from ortools.sat.python import cp_model


def build_model(n: int, dx: int, symbreak: bool = True):
    """Returns (model, edge_var_dict)."""
    m = cp_model.CpModel()
    e = {}
    for i, j in itertools.combinations(range(n), 2):
        e[(i, j)] = m.NewBoolVar(f"e_{i}_{j}")

    def E(a, b):
        return e[(a, b)] if a < b else e[(b, a)]

    x, y = 0, 1

    # xy absent
    m.Add(E(x, y) == 0)

    # degrees, as native integer linear constraints.  No upper bound on any
    # degree and no bound on the total edge count: the degree-sequence shape is
    # left entirely free (this is the trap that fcn_order15_result.md documents).
    for v in range(n):
        row = sum(E(v, w) for w in range(n) if w != v)
        if v == x:
            m.Add(row == dx)
        elif v == y:
            m.Add(row >= dx)
        else:
            m.Add(row >= 3)

    # C4-freeness as "every vertex pair has at most one common neighbour",
    # via reified conjunctions -- a different encoding from the clause-per-
    # 4-cycle form used by the PySAT implementation.
    for a, b in itertools.combinations(range(n), 2):
        commons = []
        for w in range(n):
            if w == a or w == b:
                continue
            t = m.NewBoolVar(f"cn_{a}_{b}_{w}")
            m.AddBoolAnd([E(a, w), E(b, w)]).OnlyEnforceIf(t)
            m.AddBoolOr([E(a, w).Not(), E(b, w).Not()]).OnlyEnforceIf(t.Not())
            commons.append(t)
        m.AddAtMostOne(commons)

    # Symmetry breaking: the vertices {2,...,n-1} carry identical constraints,
    # so we may require their degrees to be non-increasing.  This is a
    # different (and weaker) canonical form than the PySAT implementation's
    # lex-maximal adjacency serialisation -- intentionally so, since agreeing
    # under two different symmetry breaks is stronger evidence than agreeing
    # under the same one.
    if symbreak:
        degs = []
        for v in range(2, n):
            d = m.NewIntVar(0, n - 1, f"deg_{v}")
            m.Add(d == sum(E(v, w) for w in range(n) if w != v))
            degs.append(d)
        for a, b in zip(degs, degs[1:]):
            m.Add(a >= b)

    return m, e


def cycles_of_length(G: nx.Graph, L: int) -> list[list[int]]:
    return [c for c in nx.simple_cycles(G, length_bound=L) if len(c) == L]


def solve(n: int, dx: int, time_limit: float = 1800.0, symbreak: bool = True,
          workers: int = 1, verbose: bool = False) -> dict:
    t0 = time.time()
    m, e = build_model(n, dx, symbreak=symbreak)

    def E(a, b):
        return e[(a, b)] if a < b else e[(b, a)]

    iterations = 0
    blocked = 0
    status = "TIMEOUT"
    witness = None

    while True:
        remaining = time_limit - (time.time() - t0)
        if remaining <= 0:
            status = "TIMEOUT"
            break
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = remaining
        solver.parameters.num_search_workers = workers
        st = solver.Solve(m)
        iterations += 1

        if st == cp_model.INFEASIBLE:
            status = "UNSAT"
            break
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            status = "TIMEOUT"
            break

        edges = [(i, j) for (i, j) in e if solver.Value(e[(i, j)])]
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges)

        if cycles_of_length(G, 4):
            return {"status": "BUG", "n": n, "dx": dx,
                    "detail": "eager C4 encoding violated", "edges": edges}

        c8s = cycles_of_length(G, 8)
        if c8s:
            for cyc in c8s:
                k = len(cyc)
                m.AddBoolOr([E(cyc[i], cyc[(i + 1) % k]).Not() for i in range(k)])
                blocked += 1
            if verbose and iterations % 100 == 0:
                print(f"    iter {iterations}: blocked {blocked} C8s, "
                      f"{time.time() - t0:.1f}s", flush=True)
            continue

        # C4- and C8-free candidate: check the remaining side conditions.
        closure = G.copy()
        closure.add_edge(0, 1)
        if nx.is_biconnected(closure):
            status = "SAT"
            witness = sorted(edges)
            break
        # not 2-connected -> lazy cut clause (valid for every genuine solution)
        added = False
        for c in range(n):
            h = closure.copy()
            h.remove_node(c)
            if not nx.is_connected(h):
                comps = list(nx.connected_components(h))
                S, T = set(comps[0]), set(h.nodes()) - set(comps[0])
                if (0 in S and 1 in T) or (0 in T and 1 in S):
                    continue
                m.AddBoolOr([E(a, b) for a in S for b in T])
                added = True
        if not added:
            present = set(edges)
            m.AddBoolOr([(e[k].Not() if k in present else e[k]) for k in e])

    return {"engine": "ortools-cpsat", "status": status, "n": n, "dx": dx,
            "symbreak": symbreak, "iterations": iterations,
            "c8_clauses": blocked, "witness_edges": witness,
            "elapsed_seconds": round(time.time() - t0, 2)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int)
    ap.add_argument("--sweep", nargs=2, type=int, metavar=("FROM", "TO"))
    ap.add_argument("--dx", type=int, default=2, choices=(1, 2))
    ap.add_argument("--time-limit", type=float, default=1800.0)
    ap.add_argument("--no-symbreak", action="store_true")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    ns = range(args.sweep[0], args.sweep[1] + 1) if args.sweep else [args.n]
    print(f"{'n':>4} {'status':>8} {'iters':>8} {'C8cl':>9} {'secs':>10}")
    for n in ns:
        r = solve(n, args.dx, time_limit=args.time_limit,
                  symbreak=not args.no_symbreak, workers=args.workers,
                  verbose=args.verbose)
        print(f"{n:>4} {r['status']:>8} {r['iterations']:>8} "
              f"{r['c8_clauses']:>9} {r['elapsed_seconds']:>10.2f}", flush=True)
        if r["status"] in ("SAT", "BUG"):
            print(json.dumps(r, indent=2, default=str))


if __name__ == "__main__":
    main()
