import networkx as nx

from verifier.global_core_check import (
    atlas_report,
    certify,
    is_inclusion_minimal_delta_three,
    is_two_degenerate_with_order,
)


def test_adversarial_atlas_has_no_global_core_failures():
    report = atlas_report()
    assert report["graphs_checked"] > 0
    assert report["failures"] == []


def test_k4_exercises_degree_critical_equality_boundary():
    graph = nx.complete_graph(4)
    assert is_inclusion_minimal_delta_three(graph)
    record = certify(graph)
    assert record["m"] == 2 * record["n"] - 2
    assert record["c4"]
    assert all(check["deficit"] == 0 for check in record["deletion_checks"])


def test_nonminimal_graph_is_rejected_adversarially():
    graph = nx.complete_graph(5)
    assert not is_inclusion_minimal_delta_three(graph)


def test_peeling_rejects_a_three_core():
    works, _ = is_two_degenerate_with_order(nx.complete_graph(4))
    assert not works
