#!/usr/bin/env python3
"""Square-strip structure of cyclically four-edge-connected cubic graphs.

The structural theorems are proven in the companion note.  The algorithms
are transparent certificate builders and do not assume any graph order bound.
The separate prime-cubic predicate is used in the tests, not in these routines.
"""
from __future__ import annotations

from itertools import combinations
import networkx as nx


def canonical_square(vertices: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Canonical unoriented 4-cycle on integer-labeled graph vertices."""
    seq = tuple(vertices)
    return min(s[k:] + s[:k] for s in (seq, seq[::-1]) for k in range(4))


def squares(G: nx.Graph) -> tuple[tuple[int, int, int, int], ...]:
    """Enumerate all unoriented 4-cycles, independent of a general cycle solver."""
    if G.is_directed() or G.is_multigraph() or nx.number_of_selfloops(G):
        raise ValueError('require finite simple undirected graph')
    if not all(isinstance(v, int) for v in G):
        raise ValueError('canonical square certificate requires integer labels')
    found = set()
    for a, b in G.edges():
        for c in G.neighbors(a):
            if c == b:
                continue
            for d in G.neighbors(b):
                if d != a and d != c and G.has_edge(c, d):
                    found.add(canonical_square((a, b, d, c)))
    return tuple(sorted(found))


def square_edges(C: tuple[int, ...]) -> frozenset[frozenset[int]]:
    return frozenset(frozenset((C[i], C[(i+1)%4])) for i in range(4))


def square_intersection_graph(G: nx.Graph) -> nx.Graph:
    """Vertices are canonical squares; adjacency means sharing >=1 edge.

    In a cyclically four-edge-connected cubic graph of order >=10,
    each adjacency is along exactly one edge and all components are paths or cycles.
    """
    H = nx.Graph()
    cs = squares(G)
    H.add_nodes_from(cs)
    es = {C: square_edges(C) for C in cs}
    for A, B in combinations(cs, 2):
        common = es[A] & es[B]
        if common:
            H.add_edge(A, B, shared_edges=frozenset(common))
    return H


def square_strips(G: nx.Graph) -> tuple[dict, ...]:
    """Return checkable signatures of square-overlap components.

    No input prime assumptions are made; users may inspect degree/cut failures.
    """
    H = square_intersection_graph(G)
    result = []
    for node_set in nx.connected_components(H):
        component = H.subgraph(node_set)
        V = frozenset(v for C in node_set for v in C)
        boundary = frozenset(frozenset((u,v)) for u,v in G.edges() if (u in V) != (v in V))
        result.append({
            'squares': tuple(sorted(node_set)),
            'vertices': V,
            'overlap_degrees': tuple(sorted(d for _,d in component.degree())),
            'is_cycle': (len(node_set)>=3 and all(d==2 for _,d in component.degree())),
            'boundary_edges': boundary,
        })
    return tuple(sorted(result, key=lambda x:x['squares']))


def untouched_square_after_bridges(G: nx.Graph, square_family,
                                  roots, damaged_edges) -> tuple[int,...] | None:
    """A checkable original square missing roots and all damaged original edges."""
    root_set=set(roots)
    damaged={frozenset(e) for e in damaged_edges}
    for C in square_family:
        if not root_set.intersection(C) and not square_edges(C).intersection(damaged):
            if all(G.has_edge(C[i], C[(i+1)%4]) for i in range(4)):
                return tuple(C)
    return None


def square_survival_bound(s: int, bridge_steps: int, *, at_least_ten_vertices: bool=True) -> bool:
    """Sufficient for rooted 4-cycle after any bridge sequence from a prime cubic graph.

    For n>=10, any root is on <=2 original squares and each original edge
    is on <=2.  The only n=8 exception to the vertex bound is the cube.
    """
    if bridge_steps<0 or s<0:
        raise ValueError('nonnegative inputs required')
    if not at_least_ten_vertices:
        raise ValueError('n=8 cube exception must be handled separately')
    return s > 4*bridge_steps + 2


def rooted_square_forest(G: nx.Graph, root: int) -> nx.Graph:
    """Overlap graph of 4-cycles avoiding root. Theorem: path forest for prime cubic n>=10."""
    if root not in G:
        raise ValueError('root absent')
    H = square_intersection_graph(G)
    H.remove_nodes_from([C for C in H if root in C])
    return H


def _path_nodes(H: nx.Graph, component: set) -> tuple:
    """Deterministically order a connected path of square nodes."""
    T = H.subgraph(component)
    if any(d > 2 for _, d in T.degree()) or T.number_of_edges() != len(T)-1:
        raise ValueError('root-free square overlap must be a path forest')
    start = min((node for node in T if T.degree(node) <= 1))
    seq = [start]
    previous = None
    while True:
        choices = [x for x in T.neighbors(seq[-1]) if x != previous]
        if not choices:
            break
        previous, nxt = seq[-1], choices[0]
        seq.append(nxt)
    assert len(seq) == len(T)
    return tuple(seq)


def rooted_square_minmax(G: nx.Graph, root: int) -> tuple[int, tuple, tuple]:
    """Exact rooted square transversal/packing certificate for prime cubic n>=10.

    Returns (optimal cardinality, vertex-disjoint square packing, edge cover).
    Both witnesses can be verified independently; optimality needs the
    proved square-strip theorem.  Raises if rooted square overlap is not a forest.
    """
    H = rooted_square_forest(G, root)
    packing = []
    covering_edges = []
    for component in nx.connected_components(H):
        P = _path_nodes(H, component)
        packing.extend(P[::2])
        for i in range(0, len(P)-1, 2):
            shared = H[P[i]][P[i+1]]['shared_edges']
            if len(shared) != 1:
                raise ValueError('non-prime square overlap')
            covering_edges.append(next(iter(shared)))
        if len(P) % 2:
            covering_edges.append(min(square_edges(P[-1]), key=lambda e:tuple(sorted(e))))
    assert len(packing) == len(covering_edges)
    assert all(root not in C for C in packing)
    assert all(not (set(C) & set(D)) for C,D in combinations(packing,2))
    for C in H:
        assert square_edges(C) & set(covering_edges)
    return len(packing), tuple(packing), tuple(covering_edges)


FOUR_PORTS = ('LT', 'LB', 'RT', 'RB')


def ladder_four_pole_spectrum(k: int, u: str, v: str) -> tuple[int, ...]:
    """Exact simple-path lengths between ports of an open k-square ladder.

    LT/LB are the two left terminals, RT/RB the two right terminals.
    Proven from bipartite parity/vertex-count upper bounds and monotone
    zigzag paths (switching rails at chosen rungs).
    """
    if k < 1 or u not in FOUR_PORTS or v not in FOUR_PORTS or u == v:
        raise ValueError('need k>=1 and two distinct 4-pole terminals')
    if u[0] == v[0]:  # two terminals on the same end
        return tuple(range(1, 2*k+2, 2))
    same_rail = u[1] == v[1]
    lo = k if same_rail else k+1
    hi = (2*k + (k % 2)) if same_rail else (2*k + (1 - k % 2))
    return tuple(range(lo, hi+1, 2))


def ladder_four_pole_path(k: int, u: str, v: str, length: int) -> tuple[tuple[int,int], ...]:
    """Construct an explicit simple path for a permitted terminal length.

    Vertices are (rail, column), with rail 0=top, 1=bottom and 0<=column<=k.
    This is a pure constructive witness, with no graph search.
    """
    if length not in ladder_four_pole_spectrum(k, u, v):
        raise ValueError('length not in the exact port spectrum')
    ports = {'LT':(0,0), 'LB':(1,0), 'RT':(0,k), 'RB':(1,k)}
    start, end = ports[u],ports[v]
    if start[1] == end[1]:
        # Traverse out along one rail, cross a rung, return along the other.
        j=(length-1)//2
        col=start[1]
        direction = 1 if col == 0 else -1
        path=[start]
        for step in range(1,j+1):
            path.append((start[0],col+direction*step))
        path.append((1-start[0],col+direction*j))
        for step in range(j-1,-1,-1):
            path.append((1-start[0],col+direction*step))
    else:
        # Reverse so travel always from left to right.
        reverse = start[1] == k
        start0, end0 = (end,start) if reverse else (start,end)
        switches=length-k
        rungs = set(range(switches))  # distinct rung columns 0..k
        rail=start0[0]
        path=[start0]
        for col in range(k+1):
            if col in rungs:
                rail = 1-rail
                path.append((rail,col))
            if col < k:
                path.append((rail,col+1))
        if reverse:
            path.reverse()
    assert len(path) == length+1 and path[0] == start and path[-1] == end
    assert len(path) == len(set(path))
    assert all((abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1) for a,b in zip(path,path[1:]))
    return tuple(path)
