import networkx as nx

from verifier.brute_spqr import decompose
from verifier.order9_spqr_obstructions import (
    canonical_cycle,
    classify_cycle_support,
    cycle_edges,
)


def test_canonical_shortest_cycle_is_label_deterministic():
    graph = nx.complete_graph(4)
    assert canonical_cycle(graph, 4) == (0, 1, 2, 3)
    assert cycle_edges((0, 1, 2, 3)) == [(0, 1), (1, 2), (2, 3), (0, 3)]


def test_support_classifier_handles_R_P_and_S_mechanisms():
    rigid = nx.complete_graph(4)
    rigid_cycle = cycle_edges((0, 1, 2, 3))
    kind, _ = classify_cycle_support(decompose(rigid), rigid_cycle)
    assert kind == "contained_in_one_R_node"

    series = nx.cycle_graph(4)
    kind, _ = classify_cycle_support(
        decompose(series), cycle_edges((0, 1, 2, 3))
    )
    assert kind == "represented_by_an_S_node_cycle"

    theta = nx.Graph([(0, 1), (0, 2), (2, 1), (0, 3), (3, 4), (4, 1)])
    kind, _ = classify_cycle_support(
        decompose(theta), cycle_edges((0, 2, 1))
    )
    assert kind == "created_by_two_P_node_expansions"
