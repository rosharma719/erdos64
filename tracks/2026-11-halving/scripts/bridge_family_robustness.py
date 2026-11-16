#!/usr/bin/env python3
"""Structural dyadic-cycle survival under arbitrary sequences of I-extensions.

The mathematical certificate is a weighted family of *original* dyadic cycles.
A bridge only subdivides two edges, so original cycles that avoid every
subdivided edge persist with exactly their original length.  This supplies a
uniform bound on the bridge depth required to lose root-avoiding dyadic cycles.

All claims about unbounded graph families follow from incidence counting;
search is used only for the exceptional small ladders and the Petersen base.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations
from typing import Hashable, Iterable

import networkx as nx

from bridge_reduction import add_edge_bridge, cycle_edges, edge, is_dyadic


def cubic_ladder(k: int, *, mobius: bool = False) -> nx.Graph:
    """Return prism Q_{2k} or Möbius ladder V_{2k}, k>=4.

    Nodes 0..k-1 are upper rim, k..2k-1 lower rim, with k rungs.
    Möbius closing edges cross the rims rather than connecting within them.
    """
    if k < 4:
        raise ValueError('require k>=4')
    G = nx.Graph()
    G.add_nodes_from(range(2*k))
    G.add_edges_from((i, i+k) for i in range(k))
    for i in range(k-1):
        G.add_edge(i, i+1)
        G.add_edge(i+k, i+k+1)
    if mobius:
        G.add_edge(k-1, k)
        G.add_edge(2*k-1, 0)
    else:
        G.add_edge(k-1, 0)
        G.add_edge(2*k-1, k)
    assert all(d == 3 for _, d in G.degree())
    return G


def ladder_square_family(k: int, *, mobius: bool = False) -> tuple[tuple[int, ...], ...]:
    """k peripheral 4-cycles, each vertex in 2, each edge in at most 2."""
    if k < 4:
        raise ValueError('require k>=4')
    squares = [(i, i+1, i+1+k, i+k) for i in range(k-1)]
    squares.append((k-1, k, 0, 2*k-1) if mobius
                   else (k-1, 0, k, 2*k-1))
    G = cubic_ladder(k, mobius=mobius)
    assert all(all(G.has_edge(c[j], c[(j+1) % 4]) for j in range(4))
               for c in squares)
    return tuple(squares)


def incidence_counts(cycles: Iterable[Iterable]) -> tuple[Counter, Counter]:
    """Vertex and edge incidences of a specified family of simple cycles."""
    vc, ec = Counter(), Counter()
    for C in cycles:
        C = tuple(C)
        if len(set(C)) != len(C) or len(C) < 3:
            raise ValueError('only simple cycles are allowed')
        vc.update(C)
        ec.update(cycle_edges(C))
    return vc, ec


def weighted_incidence(
    cycles: Iterable[Iterable],
    weights: Iterable[Fraction | int],
) -> tuple[Fraction, Fraction, Fraction]:
    """Return (total weight, max vertex incidence, max edge incidence).

    Fraction gives an exact rational certificate, avoiding numerical tolerance.
    No graph enumeration or assumption about base connectivity is required.
    """
    cs = [tuple(C) for C in cycles]
    ws = [Fraction(w) for w in weights]
    if len(cs) != len(ws) or not cs or any(w < 0 for w in ws):
        raise ValueError('need matching nonnegative cycle weights')
    vc, ec = Counter(), Counter()
    for C, w in zip(cs, ws):
        if len(set(C)) != len(C) or len(C) < 3:
            raise ValueError('only simple cycles are allowed')
        for v in C:
            vc[v] += w
        for e in cycle_edges(C):
            ec[e] += w
    return sum(ws, Fraction(0)), max(vc.values(), default=Fraction(0)), max(ec.values(), default=Fraction(0))


def guaranteed_root_robust_after_bridges(
    cycles: Iterable[Iterable], weights: Iterable[Fraction | int], steps: int
) -> bool:
    """Sufficient survival certificate: W > alpha + 2*steps*beta."""
    if steps < 0:
        raise ValueError('steps must be nonnegative')
    W, alpha, beta = weighted_incidence(cycles, weights)
    return W > alpha + 2 * steps * beta


def bridge_sequence(G: nx.Graph, pairs: Iterable[tuple[Iterable, Iterable]]) -> nx.Graph:
    """Apply an arbitrary valid sequence of I-extensions to a copy of G."""
    result = G.copy()
    for e, f in pairs:
        result, _, _ = add_edge_bridge(result, e, f)
    return result


def surviving_original_cycle(
    child: nx.Graph, original_family: Iterable[Iterable], root: Hashable
) -> tuple | None:
    """Find a rooted dyadic witness using untouched *original* edges only."""
    if root not in child:
        raise ValueError('root must be in child')
    for C in original_family:
        C = tuple(C)
        if root in C or not is_dyadic(len(C)):
            continue
        if all(child.has_edge(C[j], C[(j+1) % len(C)]) for j in range(len(C))):
            return C
    return None


def square_survival_depth(k: int) -> int:
    """Largest s guaranteed by the k-squares certificate, including s=0.

    k > 4s + 2, so s <= floor((k-3)/4).
    """
    if k < 4:
        raise ValueError('require k>=4')
    return (k - 3) // 4


def disjoint_edge_pairs(G: nx.Graph):
    return ((e, f) for e, f in combinations(G.edges(), 2) if not set(e) & set(f))
