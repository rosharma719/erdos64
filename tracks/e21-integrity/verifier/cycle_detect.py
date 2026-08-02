"""
Power-of-two cycle detection for the Erdos--Gyarfas conjecture (Erdos #64).

A "power-of-two cycle" is a simple cycle whose length is in {4, 8, 16, 32, ...}.
The conjecture: every finite simple graph with minimum degree >= 3 contains one.

This module provides EXHAUSTIVE, exact detection of a simple cycle of a given
length L, plus helpers to check the full forbidden set {2^k : k>=2, 2^k<=n}.

Two independent existence routines are provided and cross-checked in the tests:
  * has_cycle_len_dfs   -- backtracking simple-path search rooted at min vertex
  * has_cycle_len_nx    -- via networkx.simple_cycles(length_bound=L)

Correctness principle: to DETECT existence of a simple cycle of exact length L
we search, for every possible smallest vertex s of the cycle, simple paths that
start at s, use only vertices > s (so each cycle is found from its min vertex),
and close back to s after exactly L edges.  This is exhaustive: every simple
cycle has a unique smallest vertex and is rooted there exactly once.
"""

from __future__ import annotations
import itertools
from typing import Dict, List, Optional, Sequence, Set, Tuple

Graph = Dict[int, Set[int]]  # adjacency: vertex -> set of neighbors


# ----------------------------------------------------------------------------
# Graph utilities (no external deps for the core detector)
# ----------------------------------------------------------------------------

def from_edges(n: int, edges: Sequence[Tuple[int, int]]) -> Graph:
    """Build adjacency dict on vertices 0..n-1 from an undirected edge list.
    Rejects loops and records simple (no multi) adjacency."""
    g: Graph = {v: set() for v in range(n)}
    for (a, b) in edges:
        if a == b:
            raise ValueError(f"loop at {a} -- graph must be simple")
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError(f"edge {(a,b)} out of range 0..{n-1}")
        g[a].add(b)
        g[b].add(a)
    return g


def min_degree(g: Graph) -> int:
    return min((len(nbrs) for nbrs in g.values()), default=0)


def degree_sequence(g: Graph) -> List[int]:
    return sorted((len(nbrs) for nbrs in g.values()), reverse=True)


def powers_of_two_up_to(n: int) -> List[int]:
    """Forbidden cycle lengths that can fit in an n-vertex graph: 4,8,...,<=n."""
    out = []
    p = 4
    while p <= n:
        out.append(p)
        p *= 2
    return out


# ----------------------------------------------------------------------------
# Detector A: backtracking simple-path search, rooted at the minimum vertex.
# ----------------------------------------------------------------------------

def find_cycle_len_dfs(g: Graph, L: int) -> Optional[List[int]]:
    """Return a simple cycle (as a vertex list of length L) of exactly length L,
    or None if none exists.  Exhaustive.

    A cycle of length L has L vertices and L edges.  We enumerate each cycle
    from its unique smallest vertex s, requiring the path to stay within
    vertices >= s and to visit s only as start/return.  Orientation is fixed by
    requiring the first step to go to a neighbor smaller than the last step's
    vertex is not needed for mere existence; we simply return the first found.
    """
    if L < 3:
        return None
    verts = sorted(g.keys())
    for s in verts:
        # neighbors of s that are > s (candidates for both the 2nd vertex and
        # the closing vertex). We keep everything in the induced subgraph on
        # vertices >= s so that s is the minimum of any cycle we find.
        allowed = s  # only use vertices >= s
        # DFS
        path = [s]
        visited = {s}

        def dfs(u: int, depth: int) -> Optional[List[int]]:
            # depth = number of edges used so far (len(path)-1)
            if depth == L - 1:
                # need to close back to s with one more edge
                if s in g[u]:
                    return path + []  # a full cycle: path has L vertices
                return None
            # prune: still need (L-1-depth) more vertices, all distinct and >= s
            for w in g[u]:
                if w < allowed:
                    continue
                if w in visited:
                    continue
                path.append(w)
                visited.add(w)
                res = dfs(w, depth + 1)
                if res is not None:
                    return res
                path.pop()
                visited.discard(w)
            return None

        res = dfs(s, 0)
        if res is not None and len(res) == L:
            return res
    return None


def has_cycle_len_dfs(g: Graph, L: int) -> bool:
    return find_cycle_len_dfs(g, L) is not None


# ----------------------------------------------------------------------------
# Detector B: via networkx simple_cycles with a length bound (independent).
# ----------------------------------------------------------------------------

def has_cycle_len_nx(g: Graph, L: int) -> bool:
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(g.keys())
    for u, nbrs in g.items():
        for v in nbrs:
            if u < v:
                G.add_edge(u, v)
    # simple_cycles on an undirected graph yields each cycle once; length_bound
    # caps the enumeration. We only need to see one of length exactly L.
    for cyc in nx.simple_cycles(G, length_bound=L):
        if len(cyc) == L:
            return True
    return False


# ----------------------------------------------------------------------------
# Top-level: does the graph satisfy the conjecture (has SOME power-of-two cycle)?
# ----------------------------------------------------------------------------

def forbidden_cycle_witness(g: Graph, detector=find_cycle_len_dfs
                            ) -> Optional[Tuple[int, List[int]]]:
    """If g contains any power-of-two cycle, return (L, cycle) for the smallest
    such L; else None (meaning g is a COUNTEREXAMPLE candidate if min-deg>=3)."""
    n = len(g)
    for L in powers_of_two_up_to(n):
        c = detector(g, L)
        if c is not None:
            return (L, c)
    return None


def is_counterexample(g: Graph, verbose: bool = False) -> bool:
    """True iff g is simple, has min degree >= 3, and contains NO power-of-two
    cycle.  This is the definition of a counterexample to Erdos #64."""
    md = min_degree(g)
    if md < 3:
        if verbose:
            print(f"min degree {md} < 3 -- not a valid instance")
        return False
    w = forbidden_cycle_witness(g)
    if w is not None:
        if verbose:
            L, cyc = w
            print(f"has a {L}-cycle: {cyc} -- NOT a counterexample")
        return False
    if verbose:
        print(f"min degree {md} >= 3 and no power-of-two cycle -- COUNTEREXAMPLE")
    return True


if __name__ == "__main__":
    # tiny smoke test: K4 has a 4-cycle (0-1-2-3-0) so it is NOT a counterexample
    g = from_edges(4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)])
    print("K4 min-degree:", min_degree(g))
    print("K4 witness:", forbidden_cycle_witness(g))
    print("K4 is_counterexample:", is_counterexample(g, verbose=True))
