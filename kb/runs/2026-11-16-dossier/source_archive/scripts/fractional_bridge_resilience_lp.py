#!/usr/bin/env python3
"""Optional small-instance LP verifier for the fractional bridge-resilience theorem.

The proof is combinatorial and does not require any optimization library.  This
module uses SciPy (if installed) to solve the equivalent primal/dual LPs on
small graphs for exploratory checks.  Exact rational incidence certificates
can be produced without SciPy by bridge_family_robustness.weighted_incidence.

Enumerating all simple dyadic cycles is exponential and is inappropriate as a
large-graph proof method.  This module is intentionally a bounded verifier.
"""
from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from bridge_reduction import cycle_edges, is_dyadic
from partial_triangle_expansion import cycles


@dataclass(frozen=True)
class ResilienceLP:
    resilience: float
    dual_resilience: float
    cycle_count: int
    primal_weight: tuple[float, ...]
    vertex_cap: float
    dual_edge_weight: tuple[float, ...]
    dual_vertex_weight: tuple[float, ...]


def solve_fractional_resilience(graph: nx.Graph) -> ResilienceLP:
    """Compute rho(G) using both primal and dual linear programs.

    rho(G) = 1/2 max_{w>=0,beta<=1} (total_w - max_v weight(C containing v)).
    Dual: minimum edge weight / 2, subject to a vertex budget of 1,
    and every dyadic cycle receiving edge+vertex weight >= 1.
    """
    from scipy.optimize import linprog  # optional research dependency

    D = [tuple(C) for C in cycles(graph) if is_dyadic(len(C))]
    if not D:
        return ResilienceLP(0., 0., 0, (), 0., (), ())
    vs = tuple(graph.nodes())
    es = tuple(graph.edges())
    ev = [frozenset((u, v)) for u, v in es]
    E = [cycle_edges(C) for C in D]
    m = len(D)
    vset = [frozenset(C) for C in D]
    A = []
    b = []
    for e in ev:
        A.append([int(e in CE) for CE in E] + [0])
        b.append(1)
    for v in vs:
        A.append([int(v in CV) for CV in vset] + [-1])
        b.append(0)
    primal = linprog([-1] * m + [1], A_ub=A, b_ub=b,
                     bounds=[(0, None)] * (m+1), method='highs')
    if not primal.success:
        raise RuntimeError('primal LP failed: '+primal.message)

    # Dual: edge prices y_e, vertex prices z_v.
    # For each dyadic cycle C, sum_{e in C} y_e + sum_{v in C} z_v >= 1.
    # The vertex-price budget is sum_v z_v <= 1.
    Adual = []
    bdual = []
    for CE, CV in zip(E, vset):
        Adual.append([-int(e in CE) for e in ev] +
                     [-int(v in CV) for v in vs])
        bdual.append(-1)
    Adual.append([0] * len(es) + [1] * len(vs))
    bdual.append(1)
    dual = linprog([1] * len(es) + [0] * len(vs), A_ub=Adual,
                   b_ub=bdual, bounds=[(0, None)] * (len(es)+len(vs)),
                   method='highs')
    if not dual.success:
        raise RuntimeError('dual LP failed: '+dual.message)
    value = max(0., -primal.fun / 2)
    dual_value = max(0., dual.fun / 2)
    if abs(value-dual_value) > 1e-7:
        raise AssertionError('primal/dual gap')
    return ResilienceLP(
        value, dual_value, m, tuple(float(x) for x in primal.x[:m]),
        float(primal.x[m]),
        tuple(float(x) for x in dual.x[:len(es)]),
        tuple(float(x) for x in dual.x[len(es):]))
