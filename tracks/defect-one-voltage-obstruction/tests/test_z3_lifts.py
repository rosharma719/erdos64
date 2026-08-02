import networkx as nx
import pytest

from verifier.z3_lifts import (
    assignment_index,
    certify_base,
    lift_graph,
    load_base,
    voltage_vector,
)


@pytest.mark.parametrize("base_index", range(4))
def test_base_certificates(base_index):
    base = load_base(base_index)
    certificate = certify_base(base)
    assert certificate["vertices"] == 24
    assert certificate["edges"] == 36
    assert certificate["simple"]
    assert certificate["connected"]
    assert certificate["degree_sequence"] == [3] * 24
    assert certificate["cycle_space_rank"] == 13
    assert len(certificate["tree_edges"]) == 23
    assert len(certificate["cotree_edges"]) == 13
    assert certificate["cycle_status_dfs"] == {"4": False, "8": False, "16": True}
    assert certificate["cycle_status_dfs"] == certificate["cycle_status_networkx"]
    assert len(certificate["cycle16_witness"]) == 16


def test_assignment_encoding_round_trip():
    for index in (0, 1, 2, 3, 17, 3**13 - 1):
        assert assignment_index(voltage_vector(index)) == index


@pytest.mark.parametrize("base_index", range(4))
def test_zero_lift_is_three_base_copies(base_index):
    base = load_base(base_index)
    lifted = lift_graph(base, [0] * 13)
    assert lifted.number_of_nodes() == 72
    assert lifted.number_of_edges() == 108
    assert sorted(dict(lifted.degree()).values()) == [3] * 72
    components = list(nx.connected_components(lifted))
    assert len(components) == 3
    assert sorted(map(len, components)) == [24, 24, 24]


@pytest.mark.parametrize("base_index", range(4))
@pytest.mark.parametrize("assignment", (1, 2, 3, 17, 3**13 - 1))
def test_nonzero_normalized_lifts_are_connected(base_index, assignment):
    base = load_base(base_index)
    lifted = lift_graph(base, voltage_vector(assignment))
    assert lifted.number_of_nodes() == 72
    assert lifted.number_of_edges() == 108
    assert nx.number_of_selfloops(lifted) == 0
    assert sorted(dict(lifted.degree()).values()) == [3] * 72
    assert nx.is_connected(lifted)
