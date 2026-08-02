from verifier.bridge_compatibility import (
    BridgeRecord,
    evaluate_candidate,
    search_typed_candidates,
)


def bridge(*, c=5, e=8, dx=1, dy=2, lam=(5, 6), cycles=()):
    return BridgeRecord(c, e, dx, dy, frozenset(lam), frozenset(cycles))


def test_valid_abstract_type_a_tied_signature_triple():
    result = evaluate_candidate([bridge(), bridge(), bridge()], "A")
    assert result.accepted
    assert result.bridge_type == "A"
    assert result.terminal_degree_profile["common_degree_one_terminal"] == "x"
    assert result.t5_maximality_status is True
    assert result.pairwise_cross_compatible is True
    assert result.realizability == ["ABSTRACT"] * 3


def test_type_a_rejected_by_t5_before_cross_sum_is_checked():
    smaller_clean = bridge(c=4, e=7)
    result = evaluate_candidate([smaller_clean, bridge(), bridge()], "A")
    assert not result.accepted
    assert result.rejection_stage == "T5_maximality"
    assert result.t5_maximality_status is False
    assert result.pairwise_cross_compatible is None
    assert "pairwise_cross_spectrum" not in result.filters_applied


def test_type_a_rejected_by_cross_sum_power():
    bad = bridge(lam=(2, 3))
    result = evaluate_candidate([bad, bad, bad], "A")
    assert not result.accepted
    assert result.t5_maximality_status is True
    assert result.rejection_stage == "pairwise_cross_spectrum"
    assert result.pairwise_cross_compatible is False


def test_valid_abstract_type_b_pair():
    result = evaluate_candidate([bridge(), bridge()], "B")
    assert result.accepted
    assert result.terminal_edge is True
    assert result.terminal_edge_status is True
    assert result.t5_maximality_status is True


def test_type_b_rejects_missing_common_degree_one_terminal():
    result = evaluate_candidate(
        [bridge(dx=1, dy=2), bridge(dx=2, dy=1)], "B"
    )
    assert not result.accepted
    assert result.rejection_stage == "type_structure"


def test_valid_abstract_type_c_pair():
    result = evaluate_candidate(
        [bridge(dx=1, dy=2), bridge(dx=2, dy=1)], "C"
    )
    assert result.accepted
    assert result.terminal_degree_profile["assembled_dx"] == 3
    assert result.terminal_degree_profile["assembled_dy"] == 3
    assert result.t5_maximality_status is None


def test_type_c_rejects_terminal_degree_coverage_failure():
    result = evaluate_candidate(
        [bridge(dx=1, dy=1), bridge(dx=1, dy=1)], "C"
    )
    assert not result.accepted
    assert result.rejection_stage == "type_structure"


def test_three_way_equal_signature_all_self_sum_clean_fixture():
    records = [bridge(c=7, e=11)] * 3
    result = evaluate_candidate(records, "A")
    assert result.self_sum_clean == [True, True, True]
    assert result.signatures == [(7, 11)] * 3
    assert result.t5_maximality_status is True
    assert result.accepted


def test_partially_tied_fixture_lost_by_old_strict_model():
    records = [
        bridge(c=7, e=11, lam=(5, 6)),
        bridge(c=7, e=11, lam=(5, 6)),
        bridge(c=6, e=10, lam=(4, 5)),
    ]
    result = evaluate_candidate(records, "A")
    assert result.self_sum_clean == [True, True, False]
    assert result.t5_maximality_status is True
    assert result.pairwise_cross_compatible is True
    assert result.accepted


def test_search_emits_only_exact_type_sizes_and_complete_records():
    evaluations = search_typed_candidates(
        [bridge(), bridge(dx=2, dy=1), bridge(lam=(4, 5))]
    )
    expected_sizes = {"A": 3, "B": 2, "C": 2}
    assert evaluations
    assert all(len(result.bridges) == expected_sizes[result.bridge_type]
               for result in evaluations)
    assert all(result.structural_status for result in evaluations)
    for result in evaluations:
        record = result.as_dict()
        assert set((
            "bridge_type", "terminal_degree_profile", "signatures",
            "self_sum_clean", "internal_cycle_clean", "realizability",
            "t5_maximality_status", "pairwise_cross_compatible",
        )) <= record.keys()
