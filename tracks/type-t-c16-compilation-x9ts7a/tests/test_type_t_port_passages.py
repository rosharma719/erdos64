import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))

from type_t_port_core_export import build_core
from type_t_port_multipole_sat import build_catalog
from type_t_port_passages import build_passage_catalog, drop_multi_p3_supports, verify_at_most_one_supplier
from type_t_port_c16_passage_catalog import (
    compile_instance_passages,
    enumerate_m2_passage_conflicts,
    verify_passage_conflicts as verify_specialized,
)
from type_t_port_c16_passage_hypergraph import (
    enumerate_passage_conflicts,
    verify_passage_conflicts as verify_general,
)
from type_t_port_short_conflicts import minimal_supports


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
    assert c8["verified_minimal_supports"] == 4218
    sizes = {int(k) for k in c8["support_size_distribution"]}
    assert sizes <= {2}, "no unit passage conflicts are expected for C8"


def test_two_independent_algorithms_agree_exactly_on_c8():
    # Regression test for a real bug: verify_passage_conflicts used to
    # materialize a full supplying triple/gadget rather than just the
    # claimed passage, letting edge_path_cycle "verify" a support via an
    # unrelated cycle through the supplier's unused edges. Caught only by
    # disagreement between the m=2-specialized search and this
    # independently implemented general-m augmented-graph walk; both must
    # now agree exactly.
    core, triples, gadgets = _catalog()
    p2, p3 = build_passage_catalog(triples, gadgets)

    raw_specialized = enumerate_m2_passage_conflicts(core, p2, p3, 8)
    minimal_specialized = minimal_supports(raw_specialized)
    verified_specialized, _ = verify_specialized(core, 8, minimal_specialized, p2, p3)
    final_specialized = set(minimal_supports(verified_specialized))

    raw_general = enumerate_passage_conflicts(core, p2, p3, 8, max_m=2, time_budget_seconds=60)
    minimal_general = minimal_supports(raw_general["results"])
    verified_general, _ = verify_general(core, 8, minimal_general, p2, p3)
    final_general = set(minimal_supports(verified_general))

    assert final_specialized == final_general
    assert len(final_specialized) == 4218


def test_two_p3_passages_never_coexist_in_a_support():
    # A completed graph ever contains at most one linked-pair gadget (the
    # exact-cover selects exactly one), so at most one p3-supplying
    # structure -- and hence at most one p3 passage -- can ever be
    # physically present. Supports naming two p3 passages are sound but
    # permanently vacuous and must be dropped, not just deduplicated.
    core, triples, gadgets = _catalog()
    p2, p3 = build_passage_catalog(triples, gadgets)
    raw = enumerate_m2_passage_conflicts(core, p2, p3, 8)
    for kind_key_pairs in raw:
        p3_count = sum(1 for kind, _ in kind_key_pairs if kind == "p3")
        assert p3_count <= 1

    fake = {
        (("p2", (1, 2)), ("p3", (3, 4))): {},
        (("p3", (5, 6)), ("p3", (7, 8))): {},
        (("p3", (9, 10)),): {},
    }
    kept, dropped = drop_multi_p3_supports(fake)
    assert dropped == 1
    assert set(kept) == {(("p2", (1, 2)), ("p3", (3, 4))), (("p3", (9, 10)),)}


def test_j5_c8_passage_compilation():
    # j=5 is odd: no linked gadget exists at all, so p3 is always empty.
    # Sanity check the passage pipeline still works correctly on a
    # differently-shaped (larger, gadget-free) instance.
    core = build_core(5, 2, 2)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    assert gadgets == []
    p2, p3 = build_passage_catalog(triples, gadgets)
    assert p3 == {}
    raw = enumerate_m2_passage_conflicts(core, p2, p3, 8)
    minimal = minimal_supports(raw)
    verified, rejected = verify_specialized(core, 8, minimal, p2, p3)
    final = minimal_supports(verified)
    assert len(final) == 25553


def test_same_gadget_complementary_p3_pairs_would_be_unsound_if_kept():
    # External review correction: dropping p3-p3 supports isn't merely a
    # compression. For a gadget with sides {a,b}/{c,d}, selecting it forces
    # p3[a,c] AND p3[b,d] true SIMULTANEOUSLY via forward channeling (all
    # four cross passages become available together) -- so a static clause
    # forbidding both would directly contradict that channeling axiom for
    # any completion selecting this gadget: unsound, not vacuous. Confirm
    # such pairs really are among what gets excluded (not just a
    # hypothetical), and that the exclusion is unconditional.
    core, triples, gadgets = _catalog()
    p2, p3 = build_passage_catalog(triples, gadgets)

    complementary_pairs = set()
    for gadget in gadgets:
        (p1, p2_side), (q1, q2_side) = gadget
        pair_a = ("p3", (min(p1, q1), max(p1, q1)))
        pair_b = ("p3", (min(p2_side, q2_side), max(p2_side, q2_side)))
        complementary_pairs.add(tuple(sorted({pair_a, pair_b})))
        pair_c = ("p3", (min(p1, q2_side), max(p1, q2_side)))
        pair_d = ("p3", (min(p2_side, q1), max(p2_side, q1)))
        complementary_pairs.add(tuple(sorted({pair_c, pair_d})))

    assert len(complementary_pairs) > 0

    # the generator must never produce ANY of these as a support, since it
    # excludes every p3-p3 combination unconditionally
    raw = enumerate_m2_passage_conflicts(core, p2, p3, 8)
    assert not (set(raw.keys()) & complementary_pairs)
