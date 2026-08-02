import networkx as nx
import pytest

from verifier.bridge_signature import (
    bridge_plus_xy_is_2connected,
    is_valid_bridge_candidate,
    signature_of,
)


def test_direct_terminal_edge_is_rejected_for_simple_t6_bridge():
    graph = nx.complete_graph(4)
    assert graph.has_edge(0, 1)
    assert not is_valid_bridge_candidate(graph, 0, 1)
    assert not bridge_plus_xy_is_2connected(graph, 0, 1)
    with pytest.raises(ValueError, match="exclude the direct terminal edge"):
        signature_of(graph, 0, 1, graph.number_of_nodes())


def test_absent_terminal_edge_is_modeled_by_separate_closure_edge():
    graph = nx.complete_graph(4)
    graph.remove_edge(0, 1)
    assert is_valid_bridge_candidate(graph, 0, 1)
    assert bridge_plus_xy_is_2connected(graph, 0, 1)
    signature, internal_ok = signature_of(graph, 0, 1, 4)
    assert signature[2:4] == (2, 2)
    assert signature[5] == frozenset({4})
    assert not internal_ok

