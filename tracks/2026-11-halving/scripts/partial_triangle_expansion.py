#!/usr/bin/env python3
"""Exact cycle-length calculus for simultaneous triangle expansion of cubic graphs.

Only uses networkx. Supports verification and exhaustive subset search on small bases.
No assertion about the full Erdős–Gyárfás conjecture is made.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter
from dataclasses import dataclass

import networkx as nx


def check_cubic_simple(G: nx.Graph) -> None:
    if G.is_multigraph() or G.is_directed() or nx.number_of_selfloops(G):
        raise ValueError("base graph must be simple, undirected and loop-free")
    if not all(d == 3 for _, d in G.degree()):
        raise ValueError("base graph must be cubic (all degrees exactly 3)")


def triangle_expand(G: nx.Graph, expanded: set[int]) -> nx.Graph:
    """Replace each selected cubic vertex by a triangle, attaching one edge to each port."""
    check_cubic_simple(G)
    if not expanded <= set(G):
        raise ValueError("expanded vertices must belong to the graph")
    H = nx.Graph()
    port: dict[tuple[int, int], tuple] = {}
    for u in G:
        neighbors = sorted(G.neighbors(u))
        if u in expanded:
            nodes = [("t", u, i) for i in range(3)]
            H.add_edges_from(((nodes[0], nodes[1]), (nodes[1], nodes[2]), (nodes[2], nodes[0])))
            port.update({(u, v): nodes[i] for i, v in enumerate(neighbors)})
        else:
            node = ("v", u)
            H.add_node(node)
            port.update({(u, v): node for v in neighbors})
    for u, v in G.edges():
        H.add_edge(port[u, v], port[v, u])
    return H


def cycles(G: nx.Graph) -> list[tuple[int, ...]]:
    """Return the (unoriented) simple cycles, using NetworkX's Johnson-style enumerator."""
    return [tuple(c) for c in nx.simple_cycles(G) if len(c) >= 3]


def predicted_spectrum(G: nx.Graph, expanded: set[int]) -> set[int]:
    """Exact set of cycle lengths of triangle_expand(G, expanded)."""
    check_cubic_simple(G)
    lengths = {3} if expanded else set()
    for C in cycles(G):
        s = len(expanded.intersection(C))
        lengths.update(range(len(C) + s, len(C) + 2 * s + 1))
    return lengths


def forbidden_powers(order: int) -> set[int]:
    return {1 << k for k in range(2, order.bit_length()) if (1 << k) <= order}


def allowed_expansion_counts(cycle_length: int, forbidden: set[int]) -> list[int]:
    """For this base-cycle length, permitted numbers of expanded vertices."""
    return [s for s in range(cycle_length + 1)
            if not any(cycle_length + s <= p <= cycle_length + 2 * s for p in forbidden)]


@dataclass(frozen=True)
class Restriction:
    cycle: tuple[int, ...]
    mask: int
    allowed: frozenset[int]


def restrictions(G: nx.Graph, forbidden: set[int]) -> list[Restriction]:
    check_cubic_simple(G)
    nodes = list(G)
    index = {u: i for i, u in enumerate(nodes)}
    result = []
    for C in cycles(G):
        mask = sum(1 << index[u] for u in C)
        result.append(Restriction(C, mask, frozenset(allowed_expansion_counts(len(C), forbidden))))
    return result


def viable_subsets(G: nx.Graph, forbidden: set[int], required_expansions: int | None = None):
    """Yield expansion vertex subsets for which the output avoids forbidden lengths.

    Exact due to the cycle-length formula; no expanded graph construction required.
    """
    ns = list(G)
    rs = restrictions(G, forbidden)
    for mask in range(1 << len(ns)):
        count = mask.bit_count()
        if required_expansions is not None and count != required_expansions:
            continue
        if all((mask & R.mask).bit_count() in R.allowed for R in rs):
            yield {ns[i] for i in range(len(ns)) if mask >> i & 1}


def independent_has_cycle_length(G: nx.Graph, length: int) -> bool:
    """Independent DFS oracle. Never uses NetworkX's simple_cycles / formula."""
    if length > len(G) or length < 3:
        return False
    nodes = list(G)
    number = {v: i for i, v in enumerate(nodes)}
    adj = [[number[v] for v in G[u]] for u in nodes]
    n = len(nodes)
    for start in range(n):
        def dfs(u: int, seen: int, depth: int) -> bool:
            if depth == length:
                return start in adj[u]
            for w in adj[u]:
                # Canonical start: every other vertex larger than start.
                if w <= start or (seen >> w & 1):
                    continue
                if dfs(w, seen | 1 << w, depth + 1):
                    return True
            return False
        if dfs(start, 1 << start, 1):
            return True
    return False


def base_graph(name: str) -> nx.Graph:
    if name == "k4":
        G = nx.complete_graph(4)
    elif name == "prism":
        G = nx.circular_ladder_graph(3)
    elif name == "cube":
        G = nx.cubical_graph()
    elif name == "petersen":
        G = nx.petersen_graph()
    else:
        raise ValueError(f"unknown base graph {name}")
    return nx.convert_node_labels_to_integers(G)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", choices=["k4", "prism", "cube", "petersen"], default="petersen")
    ap.add_argument("--forbid", type=int, nargs="+", default=[4, 8])
    ap.add_argument("--expand", type=int, default=None, help="require exactly this many expanded vertices")
    ap.add_argument("--cross-check", action="store_true", help="build each survivor and independently verify forbidden cycles")
    args = ap.parse_args()
    G = base_graph(args.base)
    F = set(args.forbid)
    candidates = list(viable_subsets(G, F, args.expand))
    by_size = dict(sorted(Counter(map(len, candidates)).items()))
    print(f"base={args.base}, base_n={len(G)}, forbidden={sorted(F)}")
    print(f"cycle_constraints={len(restrictions(G,F))}, viable_subsets={len(candidates)}, by_expansion_size={by_size}")
    if args.cross_check:
        for S in candidates:
            H = triangle_expand(G, S)
            if any(independent_has_cycle_length(H, p) for p in F):
                raise AssertionError(f"formula disagrees with DFS for {S}")
        print(f"independent DFS: checked all {len(candidates)} survivors")
    for S in candidates[:6]:
        print(f"witness: expand={sorted(S)} order={len(G)+2*len(S)}")


if __name__ == "__main__":
    main()
