#!/usr/bin/env python3
"""Exact cycle transfer for a cubic two-edge bridge addition.

Theorems are graph theoretic (no search assumption). Enumerators are for
small test cases/certificates, not scalable existence solvers.

Bridge operation: delete disjoint edges ab, cd; add vertices x, y and
edges ax, bx, xy, cy, dy.

A cycle avoiding xy is the subdivision-lift of a unique base cycle,
with length +0, +1, or +2. A cycle containing xy is specified by a
simple endpoint-to-endpoint path in G-{ab,cd}, with length +3.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Hashable, Iterable
import networkx as nx

from partial_triangle_expansion import cycles


def is_dyadic(n: int) -> bool:
    return n >= 4 and n & (n - 1) == 0


def edge(u: Hashable, v: Hashable) -> frozenset:
    return frozenset((u, v))


def cycle_edges(C: Iterable[Hashable]) -> frozenset:
    C = tuple(C)
    return frozenset(edge(C[i], C[(i + 1) % len(C)]) for i in range(len(C)))


def validate_bridge(G: nx.Graph, e: Iterable, f: Iterable) -> tuple[frozenset, frozenset]:
    e, f = frozenset(e), frozenset(f)
    if G.is_directed() or G.is_multigraph():
        raise ValueError("simple undirected graph required")
    if len(e) != 2 or len(f) != 2 or e & f:
        raise ValueError("bridge edges must be vertex-disjoint")
    if not G.has_edge(*tuple(e)) or not G.has_edge(*tuple(f)):
        raise ValueError("both bridge edges must exist")
    return e, f


def add_edge_bridge(
    G: nx.Graph, e: Iterable, f: Iterable
) -> tuple[nx.Graph, Hashable, Hashable]:
    """Return expanded graph and its two new bridge vertices."""
    e, f = validate_bridge(G, e, f)
    H = G.copy()
    H.remove_edges_from((tuple(e), tuple(f)))
    x, y = ("bridge", "x"), ("bridge", "y")
    k = 0
    while x in H or y in H:
        k += 1
        x, y = ("bridge", "x", k), ("bridge", "y", k)
    H.add_nodes_from((x, y))
    H.add_edges_from([(a, x) for a in e] + [(b, y) for b in f] + [(x, y)])
    return H, x, y


def lift_cycle(C: Iterable, e: frozenset, f: frozenset, x, y) -> tuple:
    """Subdivide a base cycle's occurrences of e/f (if any)."""
    C = tuple(C)
    out = []
    for i, u in enumerate(C):
        v = C[(i + 1) % len(C)]
        out.append(u)
        if edge(u, v) == e:
            out.append(x)
        elif edge(u, v) == f:
            out.append(y)
    return tuple(out)


def bridge_cycle_from_path(path: Iterable, x, y) -> tuple:
    """P joins one endpoint of e to one endpoint of f in G-e-f.

    Edges are those of P followed by its final endpoint -> y -> x ->
    initial endpoint. In particular |C| = |P_edges|+3.
    """
    return tuple(path) + (y, x)


@dataclass(frozen=True)
class BridgeWitness:
    kind: str                  # "lift" or "path"
    base_object: tuple         # base cycle or endpoint-to-endpoint path
    expanded_cycle: tuple
    shift: int                 # +0,+1,+2 for base cycles; +3 for paths

    @property
    def length(self) -> int:
        return len(self.expanded_cycle)


def enumerate_bridge_witnesses(G: nx.Graph, e: Iterable, f: Iterable):
    """Enumerate all cycles of bridge-expanded H, without enumerating H.

    Complexity is exponential, as is exact simple-cycle enumeration;
    used only for bounded checks. The decomposition theorem is general.
    """
    e, f = validate_bridge(G, e, f)
    H, x, y = add_edge_bridge(G, e, f)
    for C in cycles(G):
        C = tuple(C)
        s = int(e in cycle_edges(C)) + int(f in cycle_edges(C))
        W = BridgeWitness("lift", C, lift_cycle(C, e, f, x, y), s)
        assert len(W.expanded_cycle) == len(C) + s
        yield W
    B = G.copy()
    B.remove_edges_from((tuple(e), tuple(f)))
    for a in e:
        for b in f:
            for P in nx.all_simple_paths(B, a, b):
                P = tuple(P)
                W = BridgeWitness("path", P, bridge_cycle_from_path(P, x, y), 3)
                assert len(W.expanded_cycle) == len(P) + 2
                yield W


def enumerate_dyadic_root_witnesses(
    G: nx.Graph, e: Iterable, f: Iterable, root: Hashable
):
    """Exact rooted witnesses in expanded graph; no child-cycle search."""
    H, x, y = add_edge_bridge(G, e, f)
    if root not in H:
        raise ValueError("root absent from bridge-expanded graph")
    for W in enumerate_bridge_witnesses(G, e, f):
        if root not in W.expanded_cycle and is_dyadic(W.length):
            yield W


def forbidden_rooted_bridge_conditions(G, e, f, root) -> dict:
    """For a hypothetical root-critical child, enumerate forced exclusions.

    For an old root: forbid avoiding base cycles with length 2^k-s,
    where s is their usage count of the two edges; additionally forbid
    root-avoiding endpoint paths of length 2^k-3.
    For x/y: forbid only lifted cycles avoiding the corresponding
    subdivision edge (no path cycle avoids x or y).
    """
    H, x, y = add_edge_bridge(G, e, f)
    if root not in H:
        raise ValueError("root absent")
    bad = list(enumerate_dyadic_root_witnesses(G, e, f, root))
    return {
        "root": root,
        "child_root_critical": not bool(bad),
        "lift_witnesses": sum(w.kind == "lift" for w in bad),
        "path_witnesses": sum(w.kind == "path" for w in bad),
    }


def cycle_is_valid(G: nx.Graph, C: Iterable, root=None) -> bool:
    C = tuple(C)
    return (len(C) >= 3 and len(C) == len(set(C)) and
            (root is None or root not in C) and
            all(G.has_edge(C[i], C[(i + 1) % len(C)]) for i in range(len(C))))
