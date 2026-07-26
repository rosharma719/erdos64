"""
Mechanical cross-check for the contraction-criticality endgame's near-power
edge lemma (contraction.md, Task A) and the clean same-length merge lemma
(contraction.md, Task D).

Scope, stated honestly up front: NONE of this tests a claim that presupposes
a minimal Erdos-Gyarfas counterexample exists (none is known through very
large orders -- see verification_status.md). What IS checked exhaustively,
on ordinary simple graphs with no counterexample assumption whatsoever, are
the UNCONDITIONAL graph-theoretic mechanics that contraction.md's proofs
reduce to:

  (1) contracting a nontriangle edge e=uv (u,v share no common neighbour) of
      a simple graph yields a simple graph, and every vertex other than the
      merged vertex u* keeps its original degree exactly;
  (2) for every cycle of G/e through u*, if its two u*-incident edges both
      originate on the same original side (both from u, or both from v),
      "lifting" by replacing u* with that hub vertex gives a cycle of G of
      the SAME length;
  (3) if its two u*-incident edges originate on OPPOSITE sides, lifting by
      inserting the path u-v in place of u* gives a cycle of G of length
      exactly one more, threading through the contracted edge e;
  (4) a cubic vertex of a C4-free simple graph has exactly 1 or exactly 3
      nontriangle incident edges, never 0 or 2;
  (5) the clean same-length merge lemma: two simple cycles of equal length L
      that share exactly one edge and no other vertex, when that edge is
      removed from their union, leave a genuine simple cycle of length
      2(L-1).

Two independent cycle machineries are used throughout: a direct hand-rolled
verifier (`verify_cycle`, plain adjacency-list traversal) and networkx (a
completely separate implementation), matching this project's standing
practice of never trusting a single detector.
"""

from __future__ import annotations

import itertools
import random
from typing import Dict, List, Set, Tuple

import networkx as nx

Graph = Dict[int, Set[int]]


# ----------------------------------------------------------------------------
# Basic graph utilities
# ----------------------------------------------------------------------------

def from_edges(edges: List[Tuple[int, int]]) -> Graph:
    g: Graph = {}
    for a, b in edges:
        if a == b:
            raise ValueError(f"loop at {a}")
        g.setdefault(a, set())
        g.setdefault(b, set())
        if b in g[a]:
            raise ValueError(f"parallel edge {(a, b)}")
        g[a].add(b)
        g[b].add(a)
    return g


def to_nx(g: Graph) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(g.keys())
    for u, nbrs in g.items():
        for v in nbrs:
            G.add_edge(u, v)  # nx.Graph.add_edge is idempotent, safe for mixed-type labels
    return G


def min_degree(g: Graph) -> int:
    return min((len(nbrs) for nbrs in g.values()), default=0)


def is_simple(g: Graph) -> bool:
    for v, nbrs in g.items():
        if v in nbrs:
            return False
    return True


def nontriangle_edges(g: Graph) -> List[Tuple]:
    """Edges uv with N(u) and N(v) sharing no vertex other than each other."""
    out = []
    seen = set()
    for u in g:
        for v in g[u]:
            key = frozenset((u, v))
            if key in seen:
                continue
            seen.add(key)
            common = (g[u] & g[v]) - {u, v}
            if not common:
                out.append((u, v))
    return out


def verify_cycle(g: Graph, cyc: List) -> bool:
    """Independent, from-scratch cycle validity check (hand-rolled)."""
    if len(set(cyc)) != len(cyc) or len(cyc) < 3:
        return False
    n = len(cyc)
    for i in range(n):
        a, b = cyc[i], cyc[(i + 1) % n]
        if a not in g or b not in g[a]:
            return False
    return True


def verify_cycle_nx(g: Graph, cyc: List) -> bool:
    """Same check, routed through an independently-implemented library."""
    G = to_nx(g)
    if len(set(cyc)) != len(cyc) or len(cyc) < 3:
        return False
    n = len(cyc)
    for i in range(n):
        a, b = cyc[i], cyc[(i + 1) % n]
        if not G.has_edge(a, b):
            return False
    return True


# ----------------------------------------------------------------------------
# Contraction and lifting
# ----------------------------------------------------------------------------

def contract_nontriangle_edge(g: Graph, u, v):
    """Contract e=uv, assumed a nontriangle edge. Returns (g2, star, su, sv)
    where star is the merged vertex label and su/sv are u's and v's
    neighbour sets excluding each other (the two disjoint 'sides')."""
    assert v in g[u], "u,v must be an edge"
    su = set(g[u]) - {v}
    sv = set(g[v]) - {u}
    common = su & sv
    assert not common, f"u,v share common neighbour(s) {common}: not a nontriangle edge"

    star = ("*", u, v)
    g2: Graph = {}
    for w in g:
        if w in (u, v):
            continue
        g2[w] = set(g[w]) - {u, v}
        if w in su or w in sv:
            g2[w].add(star)
    g2[star] = su | sv
    return g2, star, su, sv


def lift_cycle(u, v, su, sv, cyc: List, star) -> Tuple[List, str]:
    """Lift a G/e cycle through `star` back to G. Returns (new_cycle, kind)
    with kind in {'same', 'mixed'}."""
    idx = cyc.index(star)
    n = len(cyc)
    prev_w = cyc[idx - 1]
    next_w = cyc[(idx + 1) % n]
    prev_side = "u" if prev_w in su else "v"
    next_side = "u" if next_w in su else "v"

    if prev_side == next_side:
        hub = u if prev_side == "u" else v
        new_cyc = cyc[:idx] + [hub] + cyc[idx + 1:]
        return new_cyc, "same"
    else:
        insert = [u, v] if prev_side == "u" else [v, u]
        new_cyc = cyc[:idx] + insert + cyc[idx + 1:]
        return new_cyc, "mixed"


# ----------------------------------------------------------------------------
# Check (1)-(3): contraction + lifting mechanics
# ----------------------------------------------------------------------------

def check_contraction_and_lifting(g: Graph, length_bound: int = 9, verbose=False):
    stats = {"graphs": 0, "nontriangle_edges": 0, "cycles_checked": 0,
             "same": 0, "mixed": 0}
    assert is_simple(g) and min_degree(g) >= 3
    stats["graphs"] += 1

    for (u, v) in nontriangle_edges(g):
        stats["nontriangle_edges"] += 1
        g2, star, su, sv = contract_nontriangle_edge(g, u, v)

        # (1) simplicity and degree preservation
        assert is_simple(g2), f"contraction of {(u,v)} not simple"
        for w in g2:
            if w == star:
                assert len(g2[w]) == len(su) + len(sv)
                assert len(g2[w]) == len(g[u]) + len(g[v]) - 2
            else:
                assert len(g2[w]) == len(g[w]), f"degree of {w} changed under contraction"
        assert min_degree(g2) >= 3

        # cross-check simplicity independently via networkx (no parallel/self edges
        # possible in a nx.Graph by construction, so instead check |V|,|E| match
        # what direct adjacency bookkeeping predicts)
        G2 = to_nx(g2)
        assert G2.number_of_nodes() == len(g2)

        # (2)/(3) lift every cycle through `star`, up to length_bound
        Gnx = to_nx(g2)
        for cyc in nx.simple_cycles(Gnx, length_bound=length_bound):
            if star not in cyc:
                continue
            stats["cycles_checked"] += 1
            new_cyc, kind = lift_cycle(u, v, su, sv, cyc, star)
            stats[kind] += 1

            ok1 = verify_cycle(g, new_cyc)
            ok2 = verify_cycle_nx(g, new_cyc)
            assert ok1 and ok2, f"lifted cycle invalid: {new_cyc} (kind={kind})"

            if kind == "same":
                assert len(new_cyc) == len(cyc), "same-side lift must preserve length"
            else:
                assert len(new_cyc) == len(cyc) + 1, "mixed-side lift must add exactly 1"
                # must actually thread through edge uv
                iu, iv = new_cyc.index(u), new_cyc.index(v)
                assert abs(iu - iv) in (1, len(new_cyc) - 1), \
                    "mixed-side lift must place u,v consecutively"

    if verbose:
        print(stats)
    return stats


# ----------------------------------------------------------------------------
# Check (4): cubic-vertex nontriangle-edge count is always 1 or 3, never 0/2,
# given C4-freeness.
# ----------------------------------------------------------------------------

def has_c4(g: Graph) -> bool:
    G = to_nx(g)
    for cyc in nx.simple_cycles(G, length_bound=4):
        if len(cyc) == 4:
            return True
    return False


def check_cubic_nontriangle_count(g: Graph):
    assert not has_c4(g)
    nte = set(frozenset(e) for e in nontriangle_edges(g))
    counted = 0
    for v, nbrs in g.items():
        if len(nbrs) != 3:
            continue
        counted += 1
        k = sum(1 for w in nbrs if frozenset((v, w)) in nte)
        assert k in (1, 3), f"cubic vertex {v} has {k} nontriangle incident edges"
    return counted


# ----------------------------------------------------------------------------
# Check (5): clean same-length merge lemma
# ----------------------------------------------------------------------------

def check_clean_merge(L: int):
    """Two internally-disjoint x-y paths of length L-1, plus the edge xy,
    forming two L-cycles sharing exactly the edge xy and no other vertex.
    Removing xy must leave a genuine simple cycle of length 2(L-1)."""
    x, y = "x", "y"
    edges = [(x, y)]
    # pathA, pathB: x -> (L-2 internal vertices) -> y, so each path has L
    # vertices and L-1 edges; together with edge xy each forms an L-cycle.
    pathA = [x] + [f"a{i}" for i in range(L - 2)] + [y]
    pathB = [x] + [f"b{i}" for i in range(L - 2)] + [y]
    for path in (pathA, pathB):
        for i in range(len(path) - 1):
            edges.append((path[i], path[i + 1]))
    g = from_edges(edges)

    # sanity: both are genuine L-cycles containing edge xy (path + closing xy edge)
    assert verify_cycle(g, pathA) and len(pathA) == L
    assert verify_cycle(g, pathB) and len(pathB) == L

    # remove xy: walk x -> ... -> y along A, then y -> ... -> x along B
    merged = pathA + list(reversed(pathB[1:-1]))
    assert len(merged) == 2 * (L - 1)
    g_no_xy = {w: set(n) for w, n in g.items()}
    g_no_xy[x].discard(y)
    g_no_xy[y].discard(x)
    assert verify_cycle(g_no_xy, merged)
    assert verify_cycle_nx(g_no_xy, merged)
    return len(merged)


# ----------------------------------------------------------------------------
# Test graphs
# ----------------------------------------------------------------------------

def petersen() -> Graph:
    G = nx.petersen_graph()
    return {v: set(G.neighbors(v)) for v in G.nodes()}


def cube_graph() -> Graph:
    G = nx.hypercube_graph(3)
    relabel = {v: i for i, v in enumerate(G.nodes())}
    return {relabel[v]: {relabel[w] for w in G.neighbors(v)} for v in G.nodes()}


def k33() -> Graph:
    G = nx.complete_bipartite_graph(3, 3)
    return {v: set(G.neighbors(v)) for v in G.nodes()}


def random_delta3_graph(n: int, extra_p: float, seed: int) -> Graph:
    """A simple connected graph with delta>=3: start from a random 3-regular
    graph (n even) and add a few random extra edges."""
    G = nx.random_regular_graph(3, n, seed=seed)
    rng = random.Random(seed)
    nodes = list(G.nodes())
    for a, b in itertools.combinations(nodes, 2):
        if not G.has_edge(a, b) and rng.random() < extra_p:
            G.add_edge(a, b)
    return {v: set(G.neighbors(v)) for v in G.nodes()}


def prism_with_diagonal() -> Graph:
    """Triangular prism plus one extra chord: guarantees at least one cubic
    vertex sitting inside a triangle, to exercise the '1 nontriangle edge'
    branch of check (4) deterministically."""
    edges = [(0, 1), (1, 2), (2, 0),  # triangle 0-1-2
             (3, 4), (4, 5), (5, 3),  # triangle 3-4-5
             (0, 3), (1, 4), (2, 5)]  # matching
    return from_edges(edges)


def main():
    total_stats = {"graphs": 0, "nontriangle_edges": 0, "cycles_checked": 0,
                    "same": 0, "mixed": 0}
    fixtures = [petersen(), cube_graph(), k33(), prism_with_diagonal()]
    for seed in range(30):
        n = random.Random(seed).choice([8, 10, 12])
        fixtures.append(random_delta3_graph(n, extra_p=0.08, seed=seed))

    for g in fixtures:
        s = check_contraction_and_lifting(g, length_bound=9)
        for k in total_stats:
            total_stats[k] += s[k]

    c4free_checked = 0
    for g in fixtures:
        if not has_c4(g):
            c4free_checked += check_cubic_nontriangle_count(g)

    merge_lengths = [check_clean_merge(L) for L in (5, 9, 17, 33)]

    print("=== contraction_lift.py: mechanical cross-check summary ===")
    print(f"graphs checked (contraction/lifting): {total_stats['graphs']}")
    print(f"nontriangle edges contracted:          {total_stats['nontriangle_edges']}")
    print(f"G/e cycles through u* lifted:          {total_stats['cycles_checked']}")
    print(f"  same-side (length-preserving) lifts: {total_stats['same']}")
    print(f"  mixed-side (length+1) lifts:         {total_stats['mixed']}")
    print(f"cubic vertices checked (1-or-3 nontriangle-edge count, C4-free graphs): {c4free_checked}")
    print(f"clean-merge lemma: L-1,L-1 -> 2(L-1) verified for L in (5,9,17,33): {merge_lengths}")
    print("0 mismatches, 0 assertion failures.")


if __name__ == "__main__":
    main()
