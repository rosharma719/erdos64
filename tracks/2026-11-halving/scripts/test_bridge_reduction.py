#!/usr/bin/env python3
"""Independent small-instance tests for the exact bridge cycle decomposition."""
import itertools
import json
import networkx as nx
import pytest

from bridge_reduction import (
    add_edge_bridge, bridge_cycle_from_path, cycle_edges,
    cycle_is_valid, edge, enumerate_bridge_witnesses,
    enumerate_dyadic_root_witnesses, forbidden_rooted_bridge_conditions,
    is_dyadic, lift_cycle, validate_bridge,
)
from partial_triangle_expansion import cycles
from prime_pole_obstructions import is_cyclically_four_edge_connected_cubic


def brute_cycle_edge_sets(H):
    """Independent oracle via directed cycle enumeration, not the base solver."""
    D = nx.DiGraph()
    D.add_nodes_from(H)
    D.add_edges_from(H.edges())
    D.add_edges_from((b, a) for a, b in H.edges())
    return {cycle_edges(c) for c in nx.simple_cycles(D) if len(c) >= 3}


@pytest.mark.parametrize("graph,edges", [
    (nx.complete_graph(4), ((0, 1), (2, 3))),
    (nx.cubical_graph(), ((0, 1), (4, 5))),
    (nx.petersen_graph(), ((1, 2), (3, 4))),
])
def test_cycle_decomposition_matches_independent_oracle(graph, edges):
    G, (e, f) = graph, edges
    H, x, y = add_edge_bridge(G, e, f)
    witnessed = list(enumerate_bridge_witnesses(G, e, f))
    assert all(cycle_is_valid(H, w.expanded_cycle) for w in witnessed)
    assert {cycle_edges(w.expanded_cycle) for w in witnessed} == brute_cycle_edge_sets(H)
    assert len(witnessed) == len({cycle_edges(w.expanded_cycle) for w in witnessed})


def test_four_predecessor_cases_are_exhaustive():
    G = nx.petersen_graph()
    e, f = (1, 2), (3, 4)
    witnessed = list(enumerate_bridge_witnesses(G, e, f))
    assert set(w.shift for w in witnessed) == {0, 1, 2, 3}
    for w in witnessed:
        if is_dyadic(w.length):
            source_length = len(w.base_object) if w.kind == "lift" else len(w.base_object)-1
            assert source_length == w.length - w.shift


def test_parent_can_be_rootcritical_but_its_bridge_is_root_robust():
    G = nx.complete_graph(4)
    assert all(not any(v not in C and is_dyadic(len(C)) for C in cycles(G)) for v in G)
    H, x, y = add_edge_bridge(G, (0, 1), (2, 3))
    assert nx.is_isomorphic(H, nx.complete_bipartite_graph(3, 3))
    for root in H:
        W = next(enumerate_dyadic_root_witnesses(G, (0, 1), (2, 3), root), None)
        assert W is not None
        assert cycle_is_valid(H, W.expanded_cycle, root)
        assert is_dyadic(W.length)


def test_petersen_root_requires_shift_or_new_path():
    G = nx.petersen_graph()
    e, f = edge(1, 2), edge(3, 4)
    old_unmodified = [
        C for C in cycles(G)
        if len(C) == 8 and 0 not in C and e not in cycle_edges(C) and f not in cycle_edges(C)
    ]
    assert old_unmodified == []
    H, x, y = add_edge_bridge(G, e, f)
    W = list(enumerate_dyadic_root_witnesses(G, e, f, 0))
    assert any(w.kind == "lift" and w.shift == 2 and w.length == 8 for w in W)
    assert any(w.kind == "path" and w.length in (4, 8) for w in W)
    assert all(cycle_is_valid(H, w.expanded_cycle, 0) for w in W)


def test_new_bridge_vertex_has_no_path_type_witness():
    G = nx.petersen_graph()
    H, x, y = add_edge_bridge(G, (1, 2), (3, 4))
    for root in (x, y):
        witnesses = list(enumerate_dyadic_root_witnesses(G, (1, 2), (3, 4), root))
        assert witnesses
        assert all(w.kind == "lift" for w in witnesses)


def test_n14_prime_requires_bridge_path_to_avoid_root():
    # A concrete case discovered in a NONEXHAUSTIVE sample of order-14
    # cubic graphs. At root 3, no lifted base cycle is dyadic and
    # root-avoiding; the new bridge path supplies an 8-cycle.
    G = nx.from_graph6_bytes(b'MGBAOWo?[_?Ra?K?_')
    e, f, root = (0, 12), (9, 11), 3
    assert is_cyclically_four_edge_connected_cubic(G)
    H, x, y = add_edge_bridge(G, e, f)
    assert is_cyclically_four_edge_connected_cubic(H)
    W = list(enumerate_dyadic_root_witnesses(G, e, f, root))
    assert W
    assert all(w.kind == "path" for w in W)
    assert any(w.length == 8 and w.base_object == (0, 5, 1, 2, 8, 9) for w in W)
    assert all(cycle_is_valid(H, w.expanded_cycle, root) for w in W)


def test_rooted_witnesses_exact_against_independent_child_oracle():
    G = nx.cubical_graph()
    e, f = (0, 1), (4, 5)
    H, x, y = add_edge_bridge(G, e, f)
    allC = list(brute_cycle_edge_sets(H))
    for root in H:
        predicted = {cycle_edges(w.expanded_cycle) for w in
                     enumerate_dyadic_root_witnesses(G, e, f, root)}
        actual = {C for C in allC if len(C) in (4, 8, 16) and
                  all(root not in E for E in C)}
        assert predicted == actual


def test_bridge_validation_rejects_shared_endpoints():
    with pytest.raises(ValueError):
        add_edge_bridge(nx.complete_graph(4), (0, 1), (1, 2))
