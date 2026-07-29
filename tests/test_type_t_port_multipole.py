import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))

from type_t_port_core_export import build_core
from type_t_port_multipole_sat import materialize
from type_t_port_triples import analyze, minimum_cubic_parameters


def test_minimum_cubic_normal_forms():
    assert minimum_cubic_parameters(4) == {
        "deficient_vertices": 76,
        "new_cubic_vertices": 26,
        "new_new_edges": 1,
        "triple_hubs": 24,
        "linked_double_hubs": 2,
        "incidence_identity": "3*t=|D|+2*e",
    }
    assert minimum_cubic_parameters(5) == {
        "deficient_vertices": 156,
        "new_cubic_vertices": 52,
        "new_new_edges": 0,
        "triple_hubs": 52,
        "linked_double_hubs": 0,
        "incidence_identity": "3*t=|D|+2*e",
    }


def test_j4_a2_c2_single_hub_and_local_cover():
    result = analyze(4, 2, 2)
    assert result["status"] == "PASS"
    assert result["same_hub_route"]["allowed_pairs"] == 652
    hypergraph = result["allowed_triple_hypergraph"]
    assert hypergraph["edges"] == 925
    assert hypergraph["maximum_safe_attachment_set_size"] == 6
    assert hypergraph["safe_sets_of_size_at_least_four_exist"]
    assert result["linked_double_hubs"]["locally_allowed_gadgets"] == 3037
    assert result["local_exact_cover"]["status"] == "SAT"
    assert result["local_exact_cover"]["cp_sat_status"] == "OPTIMAL"

    cover = result["local_exact_cover"]
    triples = [tuple(item) for item in cover["selected_triples"]]
    linked = tuple(tuple(pair) for pair in cover["selected_linked_gadget"])
    core = build_core(4, 2, 2)
    graph, _, _, hubs = materialize(core, triples, linked)
    assert graph.number_of_nodes() == 113
    assert graph.number_of_edges() == 170
    assert min(dict(graph.degree()).values()) == 3
    assert all(graph.degree(item["vertex"]) == 3 for item in hubs)
