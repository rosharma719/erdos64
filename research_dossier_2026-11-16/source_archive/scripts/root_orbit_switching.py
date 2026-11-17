#!/usr/bin/env python3
"""Rooted dyadic cycles: automorphism-orbit and single-ear certificates.

The mathematical lemmas work for all finite simple graphs. The graph
algorithms here are deliberately SMALL-ORDER certificate constructors.
They never infer an unobserved cycle or assert that the open conjecture holds.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

import networkx as nx

from prime_pole_obstructions import verify_dyadic_cycle


def is_dyadic_length(n: int) -> bool:
    return n >= 4 and (n & (n - 1)) == 0


def verify_cycle(G: nx.Graph, C: tuple[Hashable, ...]) -> bool:
    return (len(C) >= 3 and len(C) == len(set(C))
            and all(G.has_edge(C[i], C[(i+1) % len(C)]) for i in range(len(C))))


def automorphism_orbits(G: nx.Graph) -> tuple[frozenset, ...]:
    """Compute vertex orbits by colored-vertex isomorphism (small graphs).

    H_w and H_v are copies of G with exactly one vertex marked. They are
    isomorphic iff some automorphism takes w to v. Avoids enumerating the
    full automorphism group (which may be factorially large).
    """
    if G.is_directed() or G.is_multigraph():
        raise ValueError('simple undirected graph required')
    orbits = []
    remaining = set(G)
    while remaining:
        w = next(iter(remaining))
        A = G.copy()
        nx.set_node_attributes(A, {v: int(v == w) for v in A}, '_marked')
        orbit = set()
        for v in tuple(remaining):
            B = G.copy()
            nx.set_node_attributes(B, {x: int(x == v) for x in B}, '_marked')
            matching = nx.algorithms.isomorphism.categorical_node_match('_marked', None)
            if nx.is_isomorphic(A, B, node_match=matching):
                orbit.add(v)
        orbits.append(frozenset(orbit))
        remaining.difference_update(orbit)
    return tuple(orbits)


def orbit_coverage(G: nx.Graph, cycles: Iterable[tuple[Hashable, ...]],
                   orbits: tuple[frozenset, ...] | None = None) -> tuple[bool, ...]:
    """A cycle missing any member of orbit O certifies every root in O.

    This is a SUFFICIENT certificate from the given cycles; it is complete
    only when the input contains at least one representative of every
    root-avoiding dyadic cycle relevant to each orbit.
    """
    if orbits is None:
        orbits = automorphism_orbits(G)
    covered = [False] * len(orbits)
    for C in cycles:
        if not verify_dyadic_cycle(G, C):
            raise ValueError('all supplied cycles must be dyadic witnesses')
        inside = set(C)
        for i, orbit in enumerate(orbits):
            if not orbit <= inside:
                covered[i] = True
    return tuple(covered)


def translate_cycle_away_from(G: nx.Graph, cycle: tuple[Hashable, ...],
                              root: Hashable) -> tuple[Hashable, ...] | None:
    """Find an explicit root-avoiding automorphic image of the given cycle.

    Translation exists iff the automorphism orbit of `root` is not fully
    contained in `cycle`. Root and marked missing vertex are respected by
    colored-vertex graph isomorphism.
    """
    if root not in G or not verify_dyadic_cycle(G, cycle):
        raise ValueError('invalid root or dyadic cycle')
    A = G.copy()
    B = G.copy()
    mark = nx.algorithms.isomorphism.categorical_node_match('_marked', None)
    nx.set_node_attributes(B, {x: int(x == root) for x in B}, '_marked')
    for missing in G:
        if missing in cycle:
            continue
        nx.set_node_attributes(A, {x: int(x == missing) for x in A}, '_marked')
        gm = nx.algorithms.isomorphism.GraphMatcher(A, B, node_match=mark)
        mapping = next(gm.isomorphisms_iter(), None)
        if mapping is not None:
            image = tuple(mapping[x] for x in cycle)
            assert verify_dyadic_cycle(G, image, root)
            return image
    return None


@dataclass(frozen=True)
class EarCertificate:
    """A C-ear P plus an arc of C avoiding root, forming a dyadic cycle."""
    base_cycle: tuple[Hashable, ...]
    ear: tuple[Hashable, ...]
    retained_arc: tuple[Hashable, ...]
    avoiding_cycle: tuple[Hashable, ...]


def single_ear_avoiding_cycle(G: nx.Graph, C: tuple[Hashable, ...],
                              root: Hashable, max_ear_edges: int | None = None
                              ) -> EarCertificate | None:
    """Search for an explicit one-ear rerouting of dyadic C that omits root.

    An ear is a simple path meeting C only at its two distinct endpoints.
    The retained arc between its endpoints must avoid root. Exhaustive for
    one-ear witnesses if max_ear_edges is None; it does not search multi-ear
    reroutings and makes no completeness claim for rooted cycles.
    """
    if not verify_dyadic_cycle(G, C) or root not in C:
        raise ValueError('C must be a dyadic cycle containing root')
    n = len(C)
    C_set = set(C)
    for i in range(n):
        for j in range(i+1, n):
            # Exactly one of the two C arcs avoids root, unless root is
            # an endpoint, in which case neither does.
            forward = tuple(C[i:j+1])
            wrap = tuple(C[j:] + C[:i+1])
            if root not in forward:
                arc, reverse_ear = forward, True
            elif root not in wrap:
                arc, reverse_ear = wrap, False
            else:
                continue
            u, w = C[i], C[j]
            # Enumerate paths whose internal vertices lie outside C;
            # leave the endpoints connected to C.
            excluded = C_set - {u, w}
            H = G.subgraph(set(G) - excluded)
            cutoff = max_ear_edges if max_ear_edges is not None else len(G)-1
            for path in nx.all_simple_paths(H, u, w, cutoff=cutoff):
                if len(path) == 2 and G.has_edge(u, w):
                    # An ordinary chord is a valid one-edge C-ear,
                    # provided it is not an edge of the selected cycle.
                    if (i + 1 == j) or (i == 0 and j == n-1):
                        continue
                if any(x in C_set for x in path[1:-1]):
                    continue
                # The union of a C arc (u...w) and an ear (u...w)
                # yields a cycle with edge count len(arc)+len(path)-2.
                interior = path[-2:0:-1] if reverse_ear else path[1:-1]
                candidate = tuple(arc + tuple(interior))
                if is_dyadic_length(len(candidate)):
                    assert verify_dyadic_cycle(G, candidate, root)
                    return EarCertificate(C, tuple(path), arc, candidate)
    return None


def external_spokes(G: nx.Graph, C: tuple[Hashable, ...]) -> tuple[tuple[Hashable, Hashable], ...]:
    """Edges leaving C, for a simple cycle of any length."""
    if not verify_cycle(G, C):
        raise ValueError('invalid cycle')
    inside = set(C)
    return tuple((u, w) for u in C for w in G.neighbors(u) if w not in inside)


def chord_count(G: nx.Graph, C: tuple[Hashable, ...]) -> int:
    """Non-cycle edges with both endpoints on C."""
    if not verify_cycle(G, C):
        raise ValueError('invalid cycle')
    inside = set(C)
    n = len(C)
    cedges = {frozenset((C[i], C[(i+1)%n])) for i in range(n)}
    return sum(1 for u, v in G.subgraph(inside).edges()
               if frozenset((u, v)) not in cedges)


def cubic_cycle_spoke_identity(G: nx.Graph, C: tuple[Hashable, ...]) -> bool:
    """Every cubic cycle has |cut(C)| = |C| - 2 * chords(C)."""
    if any(d != 3 for _, d in G.degree()):
        raise ValueError('cubic graph required')
    return len(external_spokes(G, C)) == len(C) - 2*chord_count(G, C)

@dataclass(frozen=True)
class SwitchingCertificate:
    """Proof data for a dyadic root-avoiding cycle obtained with C-ears."""
    through_root: tuple[Hashable, ...]
    avoiding_root: tuple[Hashable, ...]
    ears: tuple[tuple[Hashable, ...], ...]
    removed_cycle_edges: tuple[frozenset, ...]
    added_ear_edges: tuple[frozenset, ...]

    @property
    def length_delta(self) -> int:
        return len(self.added_ear_edges) - len(self.removed_cycle_edges)


def cycle_switch_certificate(G: nx.Graph, C: tuple[Hashable, ...],
                             D: tuple[Hashable, ...], root: Hashable
                             ) -> SwitchingCertificate | None:
    """Decompose root-free D relative to dyadic C into exterior C-ears.

    In a cubic graph, each C vertex has exactly one non-C incident edge.
    Therefore each maximal D segment using edges outside C is a path with
    distinct endpoints in C and no internal vertices of C. The number of
    these paths is the exact single-/multi-ear switching count.

    Returns None if C,D have no common vertex. No claim that any such D
    exists; this only provides an independently verifiable certificate.
    """
    if not all(d == 3 for _, d in G.degree()):
        raise ValueError('cubic graph required')
    if not verify_dyadic_cycle(G, C) or not verify_dyadic_cycle(G, D, root):
        raise ValueError('both cycles must be simple dyadic cycles; D avoids root')
    if root not in C:
        raise ValueError('C must contain root')
    if not set(C).intersection(D):
        return None
    eC = {frozenset((C[i], C[(i+1)%len(C)])) for i in range(len(C))}
    eD = {frozenset((D[i], D[(i+1)%len(D)])) for i in range(len(D))}
    cvertices = set(C)
    ears = []
    for i, u in enumerate(D):
        next_vertex = D[(i+1)%len(D)]
        if u not in cvertices or frozenset((u, next_vertex)) in eC:
            continue
        ear = [u]
        j = i
        while True:
            j=(j+1)%len(D)
            ear.append(D[j])
            if D[j] in cvertices:
                break
            if len(ear)>len(D):
                raise AssertionError('exterior path never returned to C')
        assert len(ear)==len(set(ear)) and all(x not in cvertices for x in ear[1:-1])
        ears.append(tuple(ear))
    added = eD - eC
    removed = eC - eD
    assert sum(len(p)-1 for p in ears) == len(added)
    assert len(D) - len(C) == len(added) - len(removed)
    return SwitchingCertificate(C,D,tuple(ears),tuple(removed),tuple(added))
