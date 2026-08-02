#!/usr/bin/env python3
"""Shared enumerator (defect-three phase, Parts VI.2/VII): every
connected multigraph (self-loops and parallel edges allowed, since both
correspond to legitimate F-realizations after suppression) on a small
labelled vertex set with a PRESCRIBED degree sequence, up to
isomorphism.

Method: stub/configuration-model enumeration -- build the multiset of
degree-stubs, enumerate every perfect matching of the stubs into edges
(a standard, exhaustive, finite procedure for small degree sums), keep
only the CONNECTED results, then deduplicate up to graph isomorphism
(using networkx's VF2, exact -- not a hash-based heuristic) so the
enumeration "is intended as an all-orders finite certificate" per the
task's own phrasing: completeness follows from exhausting every
matching of a finite stub multiset, not from a search cutoff.
"""
from __future__ import annotations

import itertools
from typing import Any

import networkx as nx


def _all_matchings(stubs: list[int]) -> list[list[tuple[int, int]]]:
    if not stubs:
        return [[]]
    first, rest = stubs[0], stubs[1:]
    out = []
    for i, other in enumerate(rest):
        edge = (first, other)
        remaining = rest[:i] + rest[i + 1:]
        for sub in _all_matchings(remaining):
            out.append([edge] + sub)
    return out


def enumerate_kernels(degree_seq: dict[str, int]) -> list[nx.MultiGraph]:
    """degree_seq: vertex-name -> required degree. Returns one
    representative MultiGraph per isomorphism class among all CONNECTED
    multigraphs realizing exactly this degree sequence."""
    stubs: list[int] = []
    names: list[str] = []
    for name, deg in degree_seq.items():
        for _ in range(deg):
            stubs.append(len(names))
            names.append(name)
    assert sum(degree_seq.values()) % 2 == 0, "degree sum must be even"

    seen_reps: list[nx.MultiGraph] = []
    for matching in _all_matchings(list(range(len(stubs)))):
        G = nx.MultiGraph()
        G.add_nodes_from(degree_seq.keys())
        for a, b in matching:
            G.add_edge(names[a], names[b])
        if not nx.is_connected(G):
            continue
        is_new = True
        for rep in seen_reps:
            if nx.is_isomorphic(G, rep):
                is_new = False
                break
        if is_new:
            seen_reps.append(G)
    return seen_reps


def describe(G: nx.MultiGraph) -> dict[str, Any]:
    loops = sum(1 for u, v in G.edges() if u == v)
    return {
        "nodes": sorted(G.nodes()),
        "edges": sorted((u, v) for u, v in G.edges()),
        "num_self_loops": loops,
        "degree": {n: G.degree(n) for n in G.nodes()},
    }


if __name__ == "__main__":
    # smoke test matching VI.1's already hand-derived theta/dumbbell pair
    reps = enumerate_kernels({"u": 3, "w": 3})
    print(f"deg(u)=deg(w)=3 kernels: {len(reps)} isomorphism classes")
    for r in reps:
        print(describe(r))
