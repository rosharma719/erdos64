import networkx as nx

from verifier.type_a_order10_direct import (
    canonicalize,
    edge_bound_derivation,
    generator_command,
    passes_internal_degrees,
    root_relabelled_g6,
    rooted_entries,
)


def test_order10_generator_layers_and_sound_degree_caps():
    assert generator_command(13) == [
        "geng", "-c", "-f", "-d1", "-D3", "10", "13:13", "0/1"
    ]
    assert generator_command(14) == [
        "geng", "-c", "-f", "-d1", "-D5", "10", "14:14", "0/1"
    ]
    assert "3n-4" in edge_bound_derivation()["general"]


def test_direct_root_filter_and_oriented_canonicalization():
    graph = nx.complete_graph(4)
    graph.add_edge(0, 4)
    # x=4, y=1 gives all three other K4 vertices internal degree 3.
    entries = list(rooted_entries(graph, "fixture"))
    assert any((x, y) == (4, 1) for x, y, _ in entries)
    assert passes_internal_degrees(graph, 4, 1)
    rooted = root_relabelled_g6(graph, 4, 1)
    unique, report = canonicalize([{
        "root_relabelled_g6": rooted,
        "source_g6": "fixture",
        "source_x": 4,
        "source_y": 1,
        "edge_layer": 7,
    }])
    assert report["exit_code"] == 0
    assert len(unique) == 1
    decoded = nx.from_graph6_bytes(unique[0]["rooted_canonical_g6"].encode())
    assert decoded.degree(0) == 1
    assert not decoded.has_edge(0, 1)
