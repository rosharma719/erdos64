#!/usr/bin/env python3
"""Structural obstructions for three-terminal cubic components.

The algorithms that enumerate paths / cuts below are SMALL-ORDER validators.
The parity-resolved and root-critical implications themselves are general.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Hashable

import networkx as nx

from three_cut_transfer import PoleSignature, is_dyadic

PAIRS = ((0, 1), (0, 2), (1, 2))


def stride_two_runs(lengths: frozenset[int] | set[int], parity: int) -> tuple[tuple[int, int], ...]:
    """Return maximal certified step-two runs of selected parity."""
    if parity not in (0, 1):
        raise ValueError('parity must be 0 or 1')
    values = sorted(n for n in lengths if n % 2 == parity)
    if not values:
        return ()
    runs = []
    start = end = values[0]
    for n in values[1:]:
        if n == end + 2:
            end = n
        else:
            runs.append((start, end))
            start = end = n
    runs.append((start, end))
    return tuple(runs)


def even_stride_score(signature: PoleSignature, parity: int = 0) -> int | None:
    """Sum max(b-2a-1) for certified parity-specific length bands.

    Returns None when some terminal pair has no paths of this parity. The
    score is a SUFFICIENT criterion only when paired with a matching-parity
    component; it is not an estimate of graph girth or a complete invariant.
    """
    weights = []
    for i, j in PAIRS:
        runs = stride_two_runs(signature.paths(i, j), parity)
        if not runs:
            return None
        weights.append(max(b - 2*a - 1 for a, b in runs))
    return sum(weights)


@dataclass(frozen=True)
class ParityCutCertificate:
    terminal_pair: tuple[int, int]
    parity: int
    first_length: int
    last_length: int
    dyadic_length: int
    interval_a: tuple[int, int]
    interval_b: tuple[int, int]


def parity_cut_certificate(A: PoleSignature, B: PoleSignature,
                           parity: int = 0, *, use_mean: bool = False) -> ParityCutCertificate | None:
    """Certify an even dyadic crossing cycle from exact step-two subintervals.

    Both terminal paths use the same parity, so their sum plus two cut edges
    is even. The pair must attain *all* lengths in the certified stride-two
    runs, including the dyadic witness. This proof needs no full spectrum.

    use_mean=True restricts to the orientation-independent aggregate bound
    Phi_parity(A)+Phi_parity(B)>=0 and its maximizing pair runs.
    """
    if parity not in (0, 1):
        raise ValueError('parity must be 0 or 1')
    if use_mean:
        a, b = even_stride_score(A, parity), even_stride_score(B, parity)
        if a is None or b is None or a + b < 0:
            return None
    for i, j in PAIRS:
        runs_a = stride_two_runs(A.paths(i, j), parity)
        runs_b = stride_two_runs(B.paths(i, j), parity)
        if use_mean and runs_a and runs_b:
            runs_a = (max(runs_a, key=lambda z: z[1] - 2*z[0] - 1),)
            runs_b = (max(runs_b, key=lambda z: z[1] - 2*z[0] - 1),)
        for a0, a1 in runs_a:
            for b0, b1 in runs_b:
                lo, hi = 2 + a0 + b0, 2 + a1 + b1
                if lo % 2:  # defensive; equal-parity paths always make even cycles
                    raise AssertionError('crossing lengths must be even')
                p = 1 << (max(4, lo) - 1).bit_length()
                if p <= hi and is_dyadic(p):
                    return ParityCutCertificate((i, j), parity, lo, hi, p,
                                                (a0, a1), (b0, b1))
    if use_mean:
        raise AssertionError('nonnegative aggregate score must force a pair')
    return None


def triangle_leaf_crossing_witness(pole: PoleSignature) -> tuple[tuple[int, int], int, int] | None:
    """If a triangle pole is glued at a cyclic 3-cut, find a dyadic crossing.

    A capped K4 pole has path spectrum {1,2} at every terminal pair, hence
    the other side must omit each 2**k-3 and 2**k-4 to avoid a dyadic cycle.
    Return (port pair, path length on other side, resulting cycle length).
    """
    for i, j in PAIRS:
        for length in sorted(pole.paths(i, j)):
            for delta in (3, 4):
                cycle_length = length + delta
                if is_dyadic(cycle_length):
                    return ((i, j), length, cycle_length)
    return None


def dyadic_cycle_avoiding_vertex(graph: nx.Graph, avoided: Hashable) -> tuple[Hashable, ...] | None:
    """Find ONE simple dyadic cycle after deleting a vertex.

    Intended for small finite examples/census validation, not a scalable
    solver. Canonical-start DFS avoids duplicate rotations of a cycle.
    """
    if avoided not in graph:
        raise ValueError('avoided vertex not in graph')
    vertices = [v for v in graph if v != avoided]
    rank = {v: i for i, v in enumerate(vertices)}
    adjacency = {v: set(graph.neighbors(v)) - {avoided} for v in vertices}

    for target in (1 << k for k in range(2, len(vertices).bit_length() + 1)):
        if target > len(vertices):
            break
        for start in vertices:
            selected = [start]
            selected_set = {start}

            def dfs(u: Hashable) -> tuple[Hashable, ...] | None:
                if len(selected) == target:
                    return tuple(selected) if start in adjacency[u] else None
                for w in adjacency[u]:
                    if rank[w] <= rank[start] or w in selected_set:
                        continue
                    selected.append(w)
                    selected_set.add(w)
                    witness = dfs(w)
                    if witness is not None:
                        return witness
                    selected.pop()
                    selected_set.remove(w)
                return None

            witness = dfs(start)
            if witness is not None:
                return witness
    return None


def verify_dyadic_cycle(graph: nx.Graph, cycle: tuple[Hashable, ...],
                        avoided: Hashable | None = None) -> bool:
    """Small independent checker for an explicit witness."""
    return (is_dyadic(len(cycle)) and len(set(cycle)) == len(cycle)
            and (avoided is None or avoided not in cycle)
            and all(graph.has_edge(cycle[k], cycle[(k+1) % len(cycle)])
                    for k in range(len(cycle))))


def is_cyclically_four_edge_connected_cubic(graph: nx.Graph) -> bool:
    """Reference small-order test; exhaustively scans triples of cut edges.

    Cyclically 4-edge-connected means 3-connected and no edge cut of size 3
    with cycles on both sides. Suitable for the <=12-order reference catalog.
    """
    if not nx.is_connected(graph) or any(graph.degree(v) != 3 for v in graph):
        return False
    if nx.node_connectivity(graph) < 3:
        return False
    edges = tuple(graph.edges())
    for triple in combinations(edges, 3):
        h = graph.copy()
        h.remove_edges_from(triple)
        components = list(nx.connected_components(h))
        if len(components) != 2:
            continue
        if all(graph.subgraph(nodes).number_of_edges() >= len(nodes) for nodes in components):
            return False
    return True


def root_robustness_violations(graph: nx.Graph) -> tuple[Hashable, ...]:
    """Roots v for which the graph minus v has no dyadic cycle.

    A factor attached across ONE cyclic 3-cut must have this property at its
    cap vertex if the final graph avoids all dyadic cycles.
    """
    return tuple(v for v in graph if dyadic_cycle_avoiding_vertex(graph, v) is None)
