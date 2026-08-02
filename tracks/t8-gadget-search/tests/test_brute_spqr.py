import networkx as nx

from verifier.brute_spqr import decompose


def test_definition_first_decomposition_validates_entire_graph_atlas():
    checked = 0
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() >= 3 and nx.is_biconnected(graph):
            result = decompose(graph)
            assert result.validation["validated"]
            checked += 1
    assert checked == 538


def test_crossing_separation_pairs_are_fully_split():
    # spqrtree 0.1.2 leaves an invalid connectivity-2 pseudo-R node on this
    # fixture for every tested insertion ordering.  Exhaustive split pairs
    # recover the reduced R-R-S path: two K4 skeletons and one triangle.
    graph = nx.from_graph6_bytes(b"FCZv_")
    result = decompose(graph)
    assert sorted(node.type for node in result.nodes) == ["R", "R", "S"]
    assert sorted(len(node.vertices) for node in result.nodes) == [3, 4, 4]
    assert sum(len(neighbors) for neighbors in result.adjacency.values()) == 4
    assert all(nx.node_connectivity(node.simple_graph()) >= 3
               for node in result.nodes if node.type == "R")
