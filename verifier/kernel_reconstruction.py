#!/usr/bin/env python3
"""Part VI/VII shared infrastructure (defect-three phase): reconstruct a
small topological kernel (a multigraph on the C1/C3 vertices, edges
replaced by direct edges or colored C2-paths) as an actual graph and
test it for C4/C8 directly.

CORRECTNESS OF THE PRUNING STRATEGY (why restricting candidate path
colorings to those already valid in Part IV's per-path sense loses no
real solution): deleting vertices/edges from a graph cannot CREATE a
new cycle, only remove one. So if the full joint reconstruction is
C4/C8-free, then deleting every OTHER branch from a shared kernel
vertex leaves a single u--path--w subgraph (with u,w now pendant/
degree-1 at that end) that must ALSO be C4/C8-free -- and a pendant
kernel vertex with no H-attachment cannot itself be part of any cycle,
so this reduced subgraph has EXACTLY the same C4/C8 status as Part IV's
bare colored path. Hence any jointly-valid reconstruction's branch
colorings are individually valid in Part IV's sense, and restricting
candidates to Part IV's (small, already-enumerated) valid-word lists
prunes the search without losing any genuine survivor. This does NOT
apply to a self-loop branch (both ends at the SAME kernel vertex): a
self-loop's isolated subgraph is a genuine cycle through that vertex,
not a bare path, so self-loops get their own (separately implemented,
separately justified) candidate generator below.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.colored_path_search import has_forbidden_cycle as path_forbidden  # noqa: E402


def all_valid_path_words(h: int, max_len: int) -> dict[int, list[tuple[int, ...]]]:
    """Every colouring of every length 0..max_len whose BARE open path
    (Part IV's setup) has no C4/C8. Small (Part IV proved max_len need
    never exceed 2,5,8 for h=1,2,3 to capture every survivor)."""
    by_len: dict[int, list[tuple[int, ...]]] = {0: [()]}
    frontier = [()]
    length = 0
    while frontier and length < max_len:
        nxt = []
        for word in frontier:
            for c in range(h):
                cand = word + (c,)
                bad, _ = path_forbidden(cand, h)
                if not bad:
                    nxt.append(cand)
        length += 1
        by_len[length] = nxt
        frontier = nxt
    return by_len


def all_valid_loop_words(h: int, max_s: int) -> dict[int, list[tuple[int, ...]]]:
    """Every colouring of a self-loop of length s (s colored C2 vertices
    x_1..x_s forming a cycle u-x_1-...-x_s-u through ONE uncoloured
    pass-through vertex u, u itself not attached to H) with no C4/C8,
    checked by DIRECT construction (no automaton/prefix shortcut is
    claimed here -- exhaustive brute force per s, since s stays small)."""
    by_s: dict[int, list[tuple[int, ...]]] = {}
    for s in range(2, max_s + 1):
        survivors = []
        for coloring in itertools.product(range(h), repeat=s):
            G = nx.Graph()
            G.add_node("u")
            G.add_nodes_from(f"p{i}" for i in range(s))
            G.add_nodes_from(f"H{c}" for c in range(h))
            G.add_edge("u", "p0")
            G.add_edge("u", f"p{s - 1}")
            for i in range(s - 1):
                G.add_edge(f"p{i}", f"p{i + 1}")
            for i, c in enumerate(coloring):
                G.add_edge(f"p{i}", f"H{c}")
            relabel = {v: i for i, v in enumerate(sorted(G, key=str))}
            g = from_edges(G.number_of_nodes(), [(relabel[a], relabel[b]) for a, b in G.edges()])
            c4 = has_cycle_len_dfs(g, 4)
            c8 = has_cycle_len_dfs(g, 8)
            assert c4 == has_cycle_len_nx(g, 4) and c8 == has_cycle_len_nx(g, 8)
            if not (c4 or c8):
                survivors.append(coloring)
        by_s[s] = survivors
    return by_s


def build_kernel_graph(
    branches: list[tuple[str, str, tuple[int, ...]]], h: int,
    c1_vertices: tuple[str, ...] = (),
) -> nx.Graph:
    """branches: list of (endpoint_u, endpoint_w, coloring) -- coloring
    is the tuple of colours for the internal C2 vertices of that branch
    (empty tuple = a direct edge). Kernel endpoint names repeat across
    branches to share vertices (e.g. theta: 3 branches with the same
    (u,w) pair; dumbbell: 2 self-loop branches plus 1 bridge).

    c1_vertices: kernel vertices that are themselves C1 (F-degree 1,
    hence needing 2 DISTINCT direct H-edges of their own -- to ALL h
    colours when h=2, since "2 distinct out of 2" exhausts every
    colour). These are genuinely different from the C2 path vertices
    (which get exactly 1 H-edge each): a C1 kernel vertex both
    participates in exactly one F-branch AND independently touches
    every H-vertex directly."""
    G = nx.Graph()
    G.add_nodes_from({b[0] for b in branches} | {b[1] for b in branches})
    G.add_nodes_from(f"H{c}" for c in range(h))
    for idx, (u, w, coloring) in enumerate(branches):
        if not coloring:
            G.add_edge(u, w)
            continue
        prev = u
        for i, c in enumerate(coloring):
            node = f"b{idx}_p{i}"
            G.add_edge(prev, node)
            G.add_edge(node, f"H{c}")
            prev = node
        G.add_edge(prev, w)
    for v in c1_vertices:
        for c in range(h):
            G.add_edge(v, f"H{c}")
    return G


def check_c4_c8(G: nx.Graph) -> tuple[bool, bool]:
    relabel = {v: i for i, v in enumerate(sorted(G, key=str))}
    g = from_edges(G.number_of_nodes(), [(relabel[a], relabel[b]) for a, b in G.edges()])
    c4 = has_cycle_len_dfs(g, 4)
    c8 = has_cycle_len_dfs(g, 8)
    assert c4 == has_cycle_len_nx(g, 4) and c8 == has_cycle_len_nx(g, 8)
    return c4, c8
