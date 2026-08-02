import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))

from type_t_port_kernel_cycle_space import (
    cross_validate_kernel_topology,
    enumerate_kernel_cycles,
    is_simple_cycle,
    kernel_from_materialized_graph,
    kernel_vertices,
    self_test,
    spanning_tree_and_fundamental_cycles,
    verify_degree_distribution_reconciliation,
    verify_u_bridge_suppression,
)


def test_u_bridge_suppression_is_legitimate():
    verify_u_bridge_suppression()  # raises if u_x/u_y aren't degree 2


def test_kernel_has_rank_seven():
    from type_t_port_kernel_cycle_space import KERNEL_EDGES

    vertices = kernel_vertices()
    assert len(vertices) == 11
    assert len(KERNEL_EDGES) == 17
    assert len(KERNEL_EDGES) - len(vertices) + 1 == 7


def test_fundamental_cycles_count_matches_rank():
    _vertices, tree_edges, nontree_edges, fundamental_cycles = spanning_tree_and_fundamental_cycles()
    assert len(tree_edges) == 10
    assert len(nontree_edges) == 7
    assert len(fundamental_cycles) == 7


def test_exactly_61_simple_cycles_all_a_c_independent():
    cycles = enumerate_kernel_cycles()
    assert len(cycles) == 61
    for _edges, (const, y_coef, a_coef, c_coef) in cycles:
        assert a_coef == 0
        assert c_coef == 0


def test_empty_edge_set_is_not_a_cycle():
    assert not is_simple_cycle(set())


def test_self_test_proves_completeness():
    result = self_test()
    assert result["status"] == "PROVED"
    assert result["simple_cycles"] == 61
    assert result["distinct_forms"] == 35
    assert result["matches_empirical_fit"] is True


def test_degree_distribution_reconciles_13_anchors_to_11_kernel_vertices():
    report = verify_degree_distribution_reconciliation()
    assert report["degree_4_anchors"] == ["z0"]
    assert len(report["degree_3_anchors"]) == 10
    assert sorted(report["degree_2_anchors_ie_suppressed_into_kernel"]) == ["u_x", "u_y"]
    assert report["sum_d_minus_2_over_branch_anchors"] == 12


def test_kernel_from_materialized_graph_matches_hand_transcribed_table():
    from type_t_port_kernel_cycle_space import KERNEL_EDGES

    mat_vertices, mat_edges = kernel_from_materialized_graph(4, 55, 7)
    assert mat_vertices == set(kernel_vertices())
    assert len(mat_edges) == len(KERNEL_EDGES) == 17


def test_independent_kernel_construction_agrees_across_many_j_a_c():
    report = cross_validate_kernel_topology()
    assert report["status"] == "PROVED"
    assert len(report["instances_checked"]) >= 9
    for inst in report["instances_checked"]:
        assert inst["num_kernel_vertices"] == 11
        assert inst["num_kernel_edges"] == 17
