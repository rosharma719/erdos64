import networkx as nx

from verifier.type_a_extremal_check import (
    manual_2connected,
    manual_terminal_choices,
    nx_terminal_choices,
)


def subdivided_k4_type_a_bridge():
    graph_j = nx.complete_graph(4)
    graph_j.remove_edge(0, 1)
    graph_j.add_node(4)
    graph_j.add_edges_from([(0, 4), (4, 1)])
    graph_b = graph_j.copy()
    graph_b.remove_edge(4, 1)
    return graph_b


def test_manual_2connectivity_matches_basic_fixtures():
    for graph, expected in (
        (nx.cycle_graph(5), True),
        (nx.path_graph(5), False),
        (nx.complete_graph(4), True),
    ):
        adjacency = {vertex: set(graph.neighbors(vertex)) for vertex in graph}
        assert manual_2connected(adjacency) is expected
        assert nx.is_biconnected(graph) is expected


def test_independent_terminal_choice_checkers_find_type_a_fixture():
    graph_b = subdivided_k4_type_a_bridge()
    expected = {(4, 1)}
    assert nx_terminal_choices(graph_b) == expected
    assert manual_terminal_choices(graph_b) == expected
