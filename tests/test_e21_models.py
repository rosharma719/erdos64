from verifier.three_bridge_search import (
    abstract_search,
    check_T5_consistency_strict_order,
    check_T5_consistency_with_ties,
    reconcile_models,
)


def test_e21_reconciliation_counts_and_exact_delta():
    result = reconcile_models()
    assert result.input_spectra == 84
    assert result.spectra_after_T2 == 65
    assert result.triple_candidates == 47_905
    assert result.pairwise_cross_compatible == 547
    assert result.old_strict_survivors == 318
    assert result.corrected_tied_survivors == 547
    assert result.newly_represented == 229
    assert result.newly_with_exactly_two_clean == 203
    assert result.newly_with_three_clean == 26
    assert result.delta_exactly_old_representation_gap


def test_equal_signature_all_clean_triple_requires_ties():
    triple = [frozenset({5, 6})] * 3
    assert not check_T5_consistency_strict_order(triple)
    assert check_T5_consistency_with_ties(triple)


def test_partially_tied_clean_triple_requires_ties():
    # {5,6} is self-sum-clean; {4,5} is not (4+4=8).  The two clean
    # bridges must tie at the maximum, which the old strict model lost.
    triple = [frozenset({5, 6}), frozenset({5, 6}), frozenset({4, 5})]
    assert not check_T5_consistency_strict_order(triple)
    assert check_T5_consistency_with_ties(triple)


def test_old_and_corrected_model_public_search_counts():
    old, _ = abstract_search("old_strict_order")
    corrected, _ = abstract_search("corrected_tied_signature")
    assert len(old) == 318
    assert len(corrected) == 547

