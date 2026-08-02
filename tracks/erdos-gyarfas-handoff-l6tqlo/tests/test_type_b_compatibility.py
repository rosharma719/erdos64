from verifier.type_b_compatibility import (
    balaban_diagnostic_check,
    cycle_decomposition_check,
    paired_arithmetic_check,
    triangle_gateway_mapping_check,
)


def test_type_b_cycle_decomposition_has_five_exact_categories():
    result = cycle_decomposition_check()
    assert result["all_cycles_have_exactly_one_support_category"]
    assert set(result["category_lengths"]) == {
        "internal_B1",
        "internal_B2",
        "edge_plus_B1",
        "edge_plus_B2",
        "cross_B1_B2",
    }


def test_triangle_gateway_maps_length_two_to_only_first_bridge():
    result = triangle_gateway_mapping_check()
    assert result["known_length_two_bridge"] == "B1 only"
    assert result["B1_paths_share_xY"]
    assert result["B2_paths_share_xxp"]
    assert result["theta_internal_cycle_length"] == 11


def test_paired_forced_core_family_survives_bounded_regression():
    result = paired_arithmetic_check()
    assert result["all_finite_regressions_forced_table_clean"]
    assert result["finite_parameter_rows"] == 1600
    assert result["delta_epsilon_patterns"]["2,2"] == [0, 2, 2, 4]
    assert result["exact_small_exponent_power_exceptions"]["2"] == [
        [1, 1],
        [2, 3],
        [3, 2],
    ]


def test_balaban_c16_is_in_rigid_core_and_meets_both_paths():
    result = balaban_diagnostic_check()
    assert result["c16_location"] == "Balaban rigid core"
    assert result["path_intersections"]["11"]["common_edges"] == 5
    assert result["path_intersections"]["13"]["common_edges"] == 9
    assert result["t9b_degree_incidence_violations"] == 0
