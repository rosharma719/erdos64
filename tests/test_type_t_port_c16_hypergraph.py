import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))

from type_t_port_core_export import build_core
from type_t_port_multipole_sat import build_catalog
from type_t_port_short_conflicts import (
    build_pair_index,
    build_passages,
    compute_reach_index,
    enumerate_m2_conflicts,
)
from type_t_port_short_conflicts import minimal_supports as minimal_supports_m2
from type_t_port_c16_hypergraph import (
    build_endpoint_sets,
    build_hop_relations,
    compile_instance,
    enumerate_m_conflicts,
    minimal_supports,
    verify_conflicts,
)


def _catalog():
    core = build_core(4, 55, 7)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    return core, triples, gadgets


def _structures(core, triples, gadgets, target_length, max_k):
    by_start = build_passages(triples, gadgets)
    pair_index = build_pair_index(triples, gadgets)
    endpoint_sets = build_endpoint_sets(by_start)
    reach = compute_reach_index(core.adjacency(), max(target_length - 4, 1))
    hopk = build_hop_relations(endpoint_sets, reach, target_length, max_k)
    return endpoint_sets, pair_index, reach, hopk


def test_general_m2_matches_specialized_m2_implementation_on_c8():
    """Correctness cross-check: the general-m search, specialized to m=2,
    must reproduce *exactly* the raw and minimal support sets of the
    independently validated ``enumerate_m2_conflicts`` (used for the C8
    results) on the smallest C16 instance -- both algorithms are searching
    the same mathematical object via genuinely different code paths (direct
    two-sided reach-set intersection vs. a general composed-relation
    pruning oracle)."""
    core, triples, gadgets = _catalog()
    endpoint_sets, pair_index, reach, hopk = _structures(core, triples, gadgets, 8, 1)

    general = enumerate_m_conflicts(core, endpoint_sets, pair_index, reach, hopk, 8, 2)
    assert not general["timed_out"]
    reference = enumerate_m2_conflicts(core, triples, gadgets, 8)
    assert set(general["results"]) == set(reference)

    general_minimal = minimal_supports(general["results"])
    reference_minimal = minimal_supports_m2(reference)
    assert set(general_minimal) == set(reference_minimal)


def test_general_m2_c4_is_vacuous():
    # Phase 1: floor(4/3) = 1 < 2, so m=2 always finds nothing for C4.
    core, triples, gadgets = _catalog()
    endpoint_sets, pair_index, reach, hopk = _structures(core, triples, gadgets, 4, 1)
    general = enumerate_m_conflicts(core, endpoint_sets, pair_index, reach, hopk, 4, 2)
    assert general["results"] == {}


def test_minimal_supports_drops_supersets_of_any_size():
    fake = {
        ("a",): True,
        ("a", "b"): True,
        ("c", "d"): True,
        ("c", "d", "e"): True,
        ("f", "g", "h"): True,
    }
    minimal = minimal_supports(fake)
    assert minimal == {("a",): True, ("c", "d"): True, ("f", "g", "h"): True}


def test_bounded_run_reports_honest_incompleteness():
    """A time-budgeted run that cannot finish must report
    BOUNDED_INCOMPLETE with an explicit vertex-coverage/unchecked-candidate
    accounting -- never silently present a partial result as complete."""
    result = compile_instance(4, 55, 7, target_length=8, m_values=(2,), workers=2,
                              time_budget_seconds=1.0)
    assert result["status"] == "BOUNDED_INCOMPLETE"
    stage = result["per_m"]["2"]
    assert stage["status"] == "BOUNDED_INCOMPLETE"
    assert stage["x1_completed"] < stage["x1_total"] or stage["verification_unchecked"] > 0


def test_verify_conflicts_finds_and_rejects_c8_sample():
    core, triples, gadgets = _catalog()
    endpoint_sets, pair_index, reach, hopk = _structures(core, triples, gadgets, 8, 1)
    general = enumerate_m_conflicts(core, endpoint_sets, pair_index, reach, hopk, 8, 2)
    minimal = minimal_supports(general["results"])
    sample = dict(list(minimal.items())[:100])
    verified, rejected, unchecked = verify_conflicts(4, 55, 7, 8, sample, workers=2)
    assert unchecked == 0
    assert verified, "expected at least one verified C8 conflict"
    assert rejected >= 0
    assert len(verified) + rejected == len(sample)
