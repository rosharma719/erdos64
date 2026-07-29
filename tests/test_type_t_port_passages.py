import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))

from type_t_port_core_export import build_core
from type_t_port_multipole_sat import build_catalog
from type_t_port_passages import build_passage_catalog, verify_at_most_one_supplier
from type_t_port_c16_passage_catalog import (
    compile_instance_passages,
    enumerate_m2_passage_conflicts,
)


def _catalog():
    core = build_core(4, 55, 7)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    return core, triples, gadgets


def test_passage_catalog_much_smaller_than_gadget_catalog():
    core, triples, gadgets = _catalog()
    p2, p3 = build_passage_catalog(triples, gadgets)
    total_passages = len(p2) + len(p3)
    total_gadget_objects = len(triples) + len(gadgets)
    # every triple/gadget supplies multiple passages, so there must be
    # substantially fewer distinct passages than (3 or 6) * objects would
    # suggest if suppliers were mostly disjoint
    assert total_passages < 3 * total_gadget_objects


def test_at_most_one_supplier_holds():
    core, triples, gadgets = _catalog()
    p2, p3 = build_passage_catalog(triples, gadgets)
    result = verify_at_most_one_supplier(p2, p3)
    assert result["status"] == "PROVED"
    assert result["distinct_supplier_pairs_checked"] > 0


def test_c4_passage_conflicts_empty():
    core, triples, gadgets = _catalog()
    p2, p3 = build_passage_catalog(triples, gadgets)
    results = enumerate_m2_passage_conflicts(core, p2, p3, 4)
    assert results == {}


def test_c8_passage_compilation_is_sound_and_compressed():
    result = compile_instance_passages(4, 55, 7, lengths=(4, 8))
    c8 = result["lengths"]["8"]
    assert c8["verified_minimal_supports"] > 0
    # this is the headline compression claim: passage-level C8 for (4,55,7)
    # must be far smaller than the already-verified gadget-level count
    assert c8["verified_minimal_supports"] < 543_601 / 20
    sizes = {int(k) for k in c8["support_size_distribution"]}
    assert sizes <= {2}, "no unit passage conflicts are expected for C8"
