import json
from pathlib import Path

from verifier.type_b_realizability import (
    Parameters,
    balaban_mechanism,
    bridge_bounds,
    first_twenty,
    forced_spectra,
    is_abstractly_compatible,
    smallest_path_union_witnesses,
)


ROOT = Path(__file__).resolve().parents[1]


def test_exact_irreducible_family_functions():
    params = Parameters(2, 2, 4, 4, 1, 1)
    assert forced_spectra(params) == (
        frozenset((2, 17, 18)),
        frozenset((4, 5, 17, 18)),
    )
    assert is_abstractly_compatible(params)
    assert bridge_bounds(params)["full_order"] == 36


def test_first_twenty_have_exact_ordering_prefix():
    rows = first_twenty()
    assert len(rows) == 20
    assert rows[0]["parameters"] == {
        "rho": 2,
        "s": 2,
        "t": 4,
        "u": 4,
        "delta": 1,
        "epsilon": 1,
    }
    assert [row["ordering_key"] for row in rows] == sorted(
        row["ordering_key"] for row in rows
    )


def test_smallest_path_union_bounds_are_attained():
    rows = smallest_path_union_witnesses()
    assert rows["1"]["B1"]["order"] == 19
    assert rows["1"]["B2"]["order"] == 19
    assert rows["2"]["B1"]["order"] == 20
    assert rows["2"]["B2"]["order"] == 20
    assert rows["1"]["B1"]["extra_edge_lower_bound"] == 7
    assert rows["1"]["B2"]["extra_edge_lower_bound"] == 6


def test_balaban_mechanism_is_ear_not_admissible_pair_cell():
    result = balaban_mechanism()
    assert result["pair_symmetric_difference_cycle_length"] == 10
    assert result["ear_length"] + result["union_route_length"] == 16
    assert result["proposed_2t_family_match"] is False
    assert result["all_c16_count"] == 3298
    assert result["independent_c16_enumerators_agree"]
    assert result["c16_disjoint_from_both_paths"] == 672


def test_frozen_fixed_template_certificate():
    certificate = json.loads(
        (ROOT / "data/type_b_pi0_fixed_template_certificate.json").read_text()
    )
    saturation = certificate["fixed_template_saturation"]
    assert saturation["ortools_status"] == "INFEASIBLE"
    assert saturation["independently_unsat"]
    assert saturation["full_order"] == 36
    assert certificate["balaban_mechanism"]["all_c16_count"] == 3298
    assert certificate["balaban_two_switch_audit"]["counts"] == {
        "C4": 135,
        "C8": 316,
        "C16": 375,
        "clean_through_16": 0,
        "structural": 826,
    }
