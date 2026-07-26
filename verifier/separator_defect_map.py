#!/usr/bin/env python3
"""Part V: defect contribution of each separator case (S5 cut-vertex,
Type A/B/C 2-cuts), and whether q(G)=1 excludes any of them.

Notation: for a piece P (a lobe or a bridge, a graph with two designated
"terminal" vertices in the 2-cut cases, or a lobe attached at a single cut
vertex in S5), define the SAME defect quantity used throughout this
project, applied to P as its own standalone graph:

    d(P) := 2|V(P)| - 2 - |E(P)|.

This is pure bookkeeping -- P's terminal vertices need not have degree >=3
inside P alone (a lobe's cut vertex has degree exactly 2 inside its own
lobe by S5; a Type-A bridge's degree-1 terminal has degree 1 inside its
own bridge by definition), so d(P) is NOT asserted >=1 the way G2 asserts
q(G)>=1 for a genuine minimal counterexample -- it is just an integer
computed from (|V(P)|,|E(P)|).

Verified here by direct construction: build random synthetic instances of
each configuration (S5 cut-vertex split, Type A/B/C 2-cut unions) and
check the derived closed-form q(G) formula against the DIRECTLY COMPUTED
q(G)=2n-2-m of the assembled whole graph.
"""
from __future__ import annotations

import random
from typing import Any

import networkx as nx


def defect(graph: nx.Graph) -> int:
    return 2 * graph.number_of_nodes() - 2 - graph.number_of_edges()


def random_piece(rng: random.Random, n: int, extra_edges: int, terminals: int) -> tuple[nx.Graph, list[int]]:
    """A connected random graph on n vertices (spanning tree + extra
    random edges) with `terminals` designated vertices (0..terminals-1)."""
    G = nx.Graph()
    nodes = list(range(n))
    G.add_nodes_from(nodes)
    order = nodes[:]
    rng.shuffle(order)
    for i in range(1, len(order)):
        j = rng.randrange(i)
        G.add_edge(order[i], order[j])
    tries = 0
    added = 0
    while added < extra_edges and tries < 20 * extra_edges + 20:
        tries += 1
        u, v = rng.sample(nodes, 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v)
            added += 1
    return G, list(range(terminals))


def s5_cutvertex_check(trials: int, seed: int) -> dict[str, Any]:
    """Build G = two lobes A1,A2 glued at a shared cut vertex v (v has
    degree 2 inside each lobe, matching S5's Step2 dᵢ=2 fact), with EQUAL
    edge count |E(A1)|=|E(A2)| (S5 Step5), and check q(G)=2*d(Ai)."""
    rng = random.Random(seed)
    checked = 0
    failures = []
    for _ in range(trials):
        n_i = rng.randint(4, 9)  # lobe order INCLUDING v
        m_extra = rng.randint(0, 3)
        A1, _ = random_piece(rng, n_i, m_extra, 1)  # vertex 0 = v
        # force |E(A2)|=|E(A1)| by construction: same n_i, retry until match
        for _ in range(200):
            A2, _ = random_piece(rng, n_i, m_extra, 1)
            if A2.number_of_edges() == A1.number_of_edges():
                break
        if A2.number_of_edges() != A1.number_of_edges():
            continue
        # relabel and glue at v (A1's vertex 0 == A2's vertex 0 == v)
        relabel2 = {0: 0}
        offset = A1.number_of_nodes()
        for v in A2:
            if v != 0:
                relabel2[v] = v + offset - 1
        A2r = nx.relabel_nodes(A2, relabel2)
        G = nx.compose(A1, A2r)
        checked += 1
        q_direct = defect(G)
        d1 = defect(A1)
        q_formula = 2 * d1
        if q_direct != q_formula:
            failures.append((sorted(G.edges()), q_direct, q_formula))
    return {"checked": checked, "failures": failures}


def glue_bridges(rng: random.Random, n_terms: list[int], extra: list[int],
                  xy_edge: bool) -> tuple[nx.Graph, list[nx.Graph]]:
    """Build G by gluing len(n_terms) two-terminal bridges at shared
    terminals x=0, y=1 (each bridge Bi has its own extra internal
    vertices 2..n_terms[i]-1), plus the xy edge if requested."""
    G = nx.Graph()
    G.add_nodes_from([0, 1])
    if xy_edge:
        G.add_edge(0, 1)
    bridges = []
    next_label = 2
    for ni, ei in zip(n_terms, extra):
        Bi, _ = random_piece(rng, ni, ei, 2)  # terminals are 0,1 in Bi's own labels
        if Bi.has_edge(0, 1):
            Bi.remove_edge(0, 1)  # the xy edge, if any, is modeled separately, never inside a bridge
        relabel = {0: 0, 1: 1}
        for v in Bi:
            if v not in (0, 1):
                relabel[v] = next_label
                next_label += 1
        Bir = nx.relabel_nodes(Bi, relabel)
        G.add_nodes_from(Bir.nodes())
        G.add_edges_from(Bir.edges())
        bridges.append(Bi)  # keep the ORIGINAL (0,1)-labelled piece for defect()
    return G, bridges


def type_check(trials: int, seed: int, t: int, xy_edge: bool, expected_offset: int) -> dict[str, Any]:
    rng = random.Random(seed)
    checked = 0
    failures = []
    for _ in range(trials):
        n_terms = [rng.randint(3, 7) for _ in range(t)]
        extra = [rng.randint(0, 2) for _ in range(t)]
        G, bridges = glue_bridges(rng, n_terms, extra, xy_edge)
        checked += 1
        q_direct = defect(G)
        d_sum = sum(defect(B) for B in bridges)
        q_formula = d_sum - expected_offset
        if q_direct != q_formula:
            failures.append((sorted(G.edges()), q_direct, q_formula, d_sum))
    return {"checked": checked, "failures": failures}


def main() -> int:
    s5 = s5_cutvertex_check(500, 20260726)
    typeA = type_check(500, 20260727, t=3, xy_edge=False, expected_offset=4)
    typeB = type_check(500, 20260728, t=2, xy_edge=True, expected_offset=3)
    typeC = type_check(500, 20260729, t=2, xy_edge=False, expected_offset=2)

    print(f"S5 cut-vertex  q(G)=2*d(lobe):        checked={s5['checked']:4d} failures={len(s5['failures'])}")
    print(f"Type A (t=3,no xy) q(G)=Sum(d)-4:      checked={typeA['checked']:4d} failures={len(typeA['failures'])}")
    print(f"Type B (t=2,xy)    q(G)=Sum(d)-3:      checked={typeB['checked']:4d} failures={len(typeB['failures'])}")
    print(f"Type C (t=2,no xy) q(G)=Sum(d)-2:      checked={typeC['checked']:4d} failures={len(typeC['failures'])}")

    total_failures = len(s5["failures"]) + len(typeA["failures"]) + len(typeB["failures"]) + len(typeC["failures"])
    return 1 if total_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
