import networkx as nx
import pytest

from verifier.gadget_criticality import (
    degree_condition_failures,
    edge_deletion_audit,
    expansion_preserves_2connectivity,
    is_2connected,
    leaf_spqr_classification,
    parallel_union_preserves_2connectivity,
    r1_holds_for_edge,
    r2_holds_for_edge,
    real_p_edges,
    real_r_edges,
    rigid_leaf_dichotomy,
    spqr_validation_errors,
    spqr_decomposition_record,
    t8r_edge_is_degree_critical,
    validated_spqr_tree,
)


def subdivided_clique(order):
    """Subdivide clique edge a-y as a-x-y; return closure J and B=J-xy."""
    clique_vertices = ["a", "y"] + [f"v{i}" for i in range(order - 2)]
    graph_j = nx.complete_graph(clique_vertices)
    graph_j.remove_edge("a", "y")
    graph_j.add_edges_from([("a", "x"), ("x", "y")])
    graph_b = graph_j.copy()
    graph_b.remove_edge("x", "y")
    return graph_j, graph_b, "x", "y"


def test_t8_edge_deletion_monotonicity_and_unique_x_edge_criticality():
    _, graph_b, x, y = subdivided_clique(4)
    audit = edge_deletion_audit(graph_b, x, y, (x, "a"))
    assert audit["internal_cycles_monotone"]
    assert audit["terminal_paths_monotone"]
    assert audit["self_sums_monotone"]
    assert audit["simple"]
    assert audit["terminal_edge_absent"]
    assert "x_terminal_degree" in audit["degree_failures"]


def test_t8_edge_can_break_closure_2connectivity():
    graph_j = nx.cycle_graph(4)
    x, y = 0, 1
    graph_b = graph_j.copy()
    graph_b.remove_edge(x, y)
    audit = edge_deletion_audit(graph_b, x, y, (2, 3))
    assert not audit["closure_2connected"]


def test_degree_critical_cases_are_exact():
    # Both terminal degrees one: the y-edge is terminal-critical.
    internal = [0, 1, 2, 3]
    graph_b = nx.complete_graph(internal)
    graph_b.add_edges_from([("x", 0), ("y", 1)])
    assert not degree_condition_failures(graph_b, "x", "y")
    smaller = graph_b.copy()
    smaller.remove_edge("y", 1)
    assert "y_terminal_degree" in degree_condition_failures(
        smaller, "x", "y"
    )

    # In a subdivided K5, a-v0 has two internal degree-4 endpoints.  Its
    # deletion preserves every degree condition exactly as T8 states.
    graph_j, graph_b, x, y = subdivided_clique(5)
    assert graph_b.degree("a") == graph_b.degree("v0") == 4
    audit = edge_deletion_audit(graph_b, x, y, ("a", "v0"))
    assert not audit["degree_failures"]
    assert audit["closure_2connected"]
    assert not t8r_edge_is_degree_critical(graph_b, x, y, ("a", "v0"))


def test_r1_on_every_small_3connected_graph_from_graph_atlas():
    checked = 0
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() < 4 or not nx.is_connected(graph):
            continue
        if nx.node_connectivity(graph) < 3:
            continue
        for edge in graph.edges():
            checked += 1
            assert r1_holds_for_edge(graph, edge)
    assert checked > 0


def test_r1_real_r_edge_preserves_2connectivity():
    graph = nx.complete_graph(4)
    assert (0, 1) in real_r_edges(graph)
    assert r1_holds_for_edge(graph, (0, 1))


def test_insertion_order_unstable_pseudo_r_node_is_rejected():
    # With the package's default edge insertion order, GCpbeo can place
    # edge 3-6 in a connectivity-2 skeleton mislabeled R.  A different
    # deterministic insertion order yields the valid reduced decomposition,
    # in which 3-6 belongs to an S-node.  R1 must never consume the bad label.
    graph = nx.from_graph6_bytes(b"GCpbeo")
    tree, validation = validated_spqr_tree(graph)
    assert validation["validated"]
    assert not spqr_validation_errors(tree, graph)
    assert (3, 6) not in real_r_edges(graph)
    assert not r1_holds_for_edge(graph, (3, 6))


def test_r1b_expanding_skeleton_edges_preserves_2connectivity():
    skeleton = nx.cycle_graph(3)
    expansions = {}
    for index, (u, v) in enumerate(skeleton.edges()):
        internal = 10 + index
        piece = nx.Graph([(u, internal), (internal, v)])
        expansions[tuple(sorted((u, v)))] = piece
    expanded = expansion_preserves_2connectivity(skeleton, expansions)
    assert expanded.number_of_nodes() == 6
    assert is_2connected(expanded)
    assert all(nx.is_connected(nx.subgraph_view(
        expanded, filter_node=lambda candidate, removed=removed:
        candidate != removed
    )) for removed in expanded)


def test_r2_parallel_union_and_real_p_edge_deletion():
    left = nx.path_graph([0, 2, 1])
    right = nx.path_graph([0, 3, 4, 1])
    union = parallel_union_preserves_2connectivity([left, right], 0, 1)
    assert nx.is_biconnected(union)

    # A direct pole edge plus the two expansions is a simple P-node fixture.
    theta = union.copy()
    theta.add_edge(0, 1)
    assert (0, 1) in real_p_edges(theta)
    assert r2_holds_for_edge(theta, (0, 1))


def test_r2_on_every_validated_graph_atlas_p_edge():
    checked = 0
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() < 3 or not nx.is_biconnected(graph):
            continue
        for edge in real_p_edges(graph):
            checked += 1
            assert r2_holds_for_edge(graph, edge)
    assert checked > 0


def test_leaf_s_and_p_classification_on_rigid_and_sp_eligible_fixtures():
    rigid_j, rigid_b, x, y = subdivided_clique(4)
    rigid = leaf_spqr_classification(rigid_j, rigid_b, x, y)
    assert rigid["valid_Type_A_leaf_classification"]
    assert not rigid["P_leaves"]
    assert [leaf["classification"] for leaf in rigid["S_leaves"]] == [
        "rigid_root_triangle_x"
    ]
    assert rigid_leaf_dichotomy(rigid_j, rigid_b, x, y)["case"] == "single_R"

    # Replace one K4 edge a-b by a-x-y-b.  Dropping xy leaves both terminals
    # degree one while the four K4 vertices retain internal degree three.
    sp_j = nx.complete_graph(4)
    sp_j.remove_edge(0, 1)
    sp_j.add_nodes_from([4, 5])
    sp_j.add_edges_from([(0, 4), (4, 5), (5, 1)])
    sp_b = sp_j.copy()
    sp_b.remove_edge(4, 5)
    sp = leaf_spqr_classification(sp_j, sp_b, 4, 5)
    assert sp["valid_Type_A_leaf_classification"]
    assert not sp["P_leaves"]
    assert [leaf["classification"] for leaf in sp["S_leaves"]] == [
        "SP_quadrilateral_xy"
    ]
    assert rigid_leaf_dichotomy(sp_j, sp_b, 4, 5)["case"] == "single_R"


def test_sp_eligible_and_rigid_forced_structural_fixtures():
    # A cycle is series-parallel; choosing an edge between two degree-2
    # vertices makes both B-terminal degrees one after the closure edge drops.
    sp_closure = nx.cycle_graph(4)
    sp_b = sp_closure.copy()
    sp_b.remove_edge(0, 1)
    sp_record = spqr_decomposition_record(sp_closure, sp_b, 0, 1)
    assert sp_b.degree(0) == sp_b.degree(1) == 1
    assert "R" not in sp_record["node_type_counts"]

    # Subdividing a K4 edge creates exactly one degree-2 vertex and retains
    # a genuine R-node.  Every real R-edge of B meets an internal degree-3
    # vertex, so the finite fixture satisfies T8R's incidence conclusion.
    rigid_j, rigid_b, x, y = subdivided_clique(4)
    record = spqr_decomposition_record(rigid_j, rigid_b, x, y)
    assert [v for v in rigid_j if rigid_j.degree(v) == 2] == [x]
    assert record["node_type_counts"]["R"] == 1
    r_real = [edge for node in record["nodes"] if node["type"] == "R"
              for edge in node["real_edges"] if edge["in_B"]]
    assert r_real
    assert all(edge["r1_2connected_after_deletion"] for edge in r_real)
    assert all(edge["t8r_degree_critical"] for edge in r_real)


def test_terminal_edge_inside_b_is_rejected():
    _, graph_b, x, y = subdivided_clique(4)
    graph_b.add_edge(x, y)
    with pytest.raises(ValueError, match="xy to be absent"):
        edge_deletion_audit(graph_b, x, y, (x, "a"))
