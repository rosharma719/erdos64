import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))

from type_t_port_core_export import build_core
from type_t_port_multipole_sat import build_catalog
from type_t_port_short_conflicts import (
    build_pair_index,
    build_passages,
    enumerate_m2_conflicts,
    materialize_variables,
    minimal_supports,
)
from type_t_port_multipole_check import edge_path_cycle, validate_literal_cycle


def _catalog():
    core = build_core(4, 55, 7)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    return core, triples, gadgets


def test_c4_is_always_empty():
    # Phase 1: floor(4/3) = 1 < 2 = the minimum possible number of hub
    # passages, so no C4 conflict can exist beyond the base local screen.
    core, triples, gadgets = _catalog()
    results = enumerate_m2_conflicts(core, triples, gadgets, 4)
    assert results == {}


def test_passage_and_pair_index_agree_on_size():
    core, triples, gadgets = _catalog()
    by_start = build_passages(triples, gadgets)
    pair_index = build_pair_index(triples, gadgets)
    assert sum(len(v) for v in by_start.values()) == sum(len(v) for v in pair_index.values())
    # 3 sub-pairs * 2 directions per triple, 6 sub-pairs * 2 directions per gadget
    assert sum(len(v) for v in by_start.values()) == 6 * len(triples) + 12 * len(gadgets)


def test_c8_candidates_materialize_to_a_real_cycle():
    core, triples, gadgets = _catalog()
    results = enumerate_m2_conflicts(core, triples, gadgets, 8)
    assert results, "expected at least one C8 conflict at (4,55,7)"
    minimal = minimal_supports(results)
    assert minimal, "minimality filter should not remove every conflict"
    sizes = {len(key) for key in minimal}
    assert sizes <= {1, 2}
    sample = list(minimal)[:200]
    verified = 0
    for support in sample:
        graph, adjacency = materialize_variables(core, support)
        witness = edge_path_cycle(adjacency, 8)
        if witness is not None:
            validate_literal_cycle(graph, list(witness))
            verified += 1
    assert verified > 0


def test_minimal_supports_drops_supersets_of_unit_conflicts():
    fake = {
        ("a",): {},
        ("a", "b"): {},
        ("c", "d"): {},
    }
    minimal = minimal_supports(fake)
    assert minimal == {("a",): {}, ("c", "d"): {}}
