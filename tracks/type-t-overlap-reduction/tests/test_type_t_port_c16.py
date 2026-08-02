import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))

from type_t_port_c16_hypergraph import (  # noqa: E402
    gadget_catalog,
    inclusion_minimal,
    universal_graph,
)
from type_t_port_core_export import build_core  # noqa: E402
from type_t_port_multipole_check import edge_path_cycle  # noqa: E402
from type_t_port_multipole_sat import materialize  # noqa: E402


def test_j4_a28_c4_universal_gadget_graph_counts():
    core = build_core(4, 28, 4)
    adjacency, gadgets, node_gadget, _, triple_var, linked_var = universal_graph(
        core
    )
    assert len(triple_var) == 1225
    assert len(linked_var) == 4371
    assert len(gadgets) == 5596
    assert len(adjacency) == 10054
    assert sum(map(len, adjacency)) // 2 == 25623
    assert len(node_gadget) == 9967


def test_linked_gadget_can_be_a_unary_c16_support():
    core = build_core(4, 28, 4)
    gadgets, _, _, _ = gadget_catalog(core)
    gadget = gadgets[1226]
    assert gadget.kind == "linked_pairs"
    adjacency = materialize(core, [], gadget.triples)[1]
    cycle = edge_path_cycle(adjacency, 16)
    assert cycle is not None
    assert len(cycle) == 16


def test_support_minimization_removes_supersets():
    records = [
        {"support": [2, 7], "support_size": 2},
        {"support": [2, 7, 11], "support_size": 3},
        {"support": [3, 9, 12], "support_size": 3},
    ]
    assert [item["support"] for item in inclusion_minimal(records)] == [
        [2, 7],
        [3, 9, 12],
    ]


def test_committed_short_conflict_catalog_is_complete():
    root = Path(__file__).resolve().parents[1]
    path = root / "data/type_t_port_c16/j4_a28_c4_short_conflicts.json.gz"
    with gzip.open(path, "rt") as source:
        catalog = json.load(source)
    assert catalog["complete"]
    assert catalog["raw_supports_by_length"] == {"4": 0, "8": 241779}
    assert catalog["minimal_supports"] == 227725
    assert catalog["support_size_distribution"] == {"1": 371, "2": 227354}
