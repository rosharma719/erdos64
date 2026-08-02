import subprocess

import networkx as nx

from verifier.type_a_order9_search import (
    BRIDGE_MIN_EDGES,
    CLOSURE_MAX_EDGES,
    CLOSURE_MIN_EDGES,
    canonicalize_rooted,
    candidate_root_pairs,
    c_power_masks,
    compile_c_detector,
    construct_three_copy_lift,
    generator_command,
    mask_lengths,
    passes_degree_filter,
    python_power_mask,
    root_relabelled_g6,
)


def subdivided_k4_closure():
    graph = nx.complete_graph(4)
    graph.remove_edge(0, 1)
    graph.add_node(4)
    graph.add_edges_from([(0, 4), (4, 1)])
    return graph, 4, 1


def test_exact_generator_bounds_and_biconnected_flag():
    assert BRIDGE_MIN_EDGES == 12
    assert CLOSURE_MIN_EDGES == 13
    assert CLOSURE_MAX_EDGES == 30
    assert generator_command() == [
        "geng", "-C", "-d2", "9", "13:30", "0/1"
    ]


def test_rooted_oriented_canonicalization_deduplicates_only_colored_isomorphs():
    graph, x, y = subdivided_k4_closure()
    relabelled = nx.relabel_nodes(graph, {0: 3, 1: 2, 2: 0, 3: 1, 4: 4})
    entries = [
        {"root_relabelled_g6": root_relabelled_g6(graph, x, y)},
        {"root_relabelled_g6": root_relabelled_g6(relabelled, 4, 2)},
    ]
    unique, report = canonicalize_rooted(entries)
    assert report["exit_code"] == 0
    assert len(unique) == 1
    canonical = nx.from_graph6_bytes(unique[0]["rooted_canonical_g6"].encode())
    assert canonical.has_edge(0, 1)
    assert canonical.degree(0) == 2


def test_root_filter_and_three_copy_lift_invariants():
    graph_j, x, y = subdivided_k4_closure()
    assert (x, y) in list(candidate_root_pairs(graph_j))
    assert passes_degree_filter(graph_j, x, y)
    graph_b = graph_j.copy()
    graph_b.remove_edge(x, y)
    lift, mappings = construct_three_copy_lift(graph_b, x, y)
    assert len(lift) == 3 * (len(graph_b) - 2) + 2
    assert lift.number_of_edges() == 3 * graph_b.number_of_edges()
    assert nx.is_connected(lift)
    assert min(dict(lift.degree()).values()) >= 3
    assert all(mapping[x] == 0 and mapping[y] == 1 for mapping in mappings)


def test_three_copy_cycle_equivalence_on_synthetic_bridges():
    fixtures = []
    # A single path gives a theta lift; add two path lengths to exercise
    # both clean and dirty self-sum cases without assuming degree hypotheses.
    for lengths in ((2,), (2, 3), (3, 4)):
        graph = nx.Graph()
        next_vertex = 2
        for length in lengths:
            path = [0]
            for _ in range(length - 1):
                path.append(next_vertex)
                next_vertex += 1
            path.append(1)
            nx.add_path(graph, path)
        fixtures.append(graph)
    for graph_b in fixtures:
        lift, _ = construct_three_copy_lift(graph_b, 0, 1)
        internal_clean = python_power_mask(graph_b) == 0
        lam = {len(path) - 1 for path in nx.all_simple_paths(graph_b, 0, 1)}
        self_sum_clean = not ({a + b for a in lam for b in lam} & {4, 8, 16})
        assert (python_power_mask(lift) == 0) == (
            internal_clean and self_sum_clean
        )


def test_independent_c_masks_match_python(tmp_path):
    binary = tmp_path / "check_power_masks"
    report = compile_c_detector(binary)
    assert report["exit_code"] == 0
    graphs = [
        nx.cycle_graph(4),
        nx.cycle_graph(8),
        nx.cycle_graph(16),
        nx.complete_graph(5),
    ]
    graph6 = [nx.to_graph6_bytes(graph, header=False).decode().strip()
              for graph in graphs]
    c_masks, batch = c_power_masks(binary, graph6)
    assert batch["exit_code"] == 0
    assert c_masks == [python_power_mask(graph) for graph in graphs]
    assert [mask_lengths(mask) for mask in c_masks[:3]] == [[4], [8], [16]]
