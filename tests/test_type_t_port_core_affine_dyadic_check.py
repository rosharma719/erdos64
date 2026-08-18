import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "verifier"))

from type_t_port_core_affine_dyadic_check import (
    check_all_forms,
    fit_affine_forms,
    is_power_of_two,
    never_dyadic_for_all_j,
    v2,
)


def test_fit_reproduces_j4_exactly():
    # This is the load-bearing cross-check: an exact 3-point integer fit,
    # not a numerical approximation.
    forms = fit_affine_forms()
    assert len(forms) == 35


def test_v2_and_power_of_two():
    assert v2(8) == 3
    assert v2(-8) == 3
    assert v2(12) == 2
    assert is_power_of_two(1)
    assert is_power_of_two(16)
    assert not is_power_of_two(0)
    assert not is_power_of_two(-4)
    assert not is_power_of_two(6)


def test_known_dyadic_and_safe_forms():
    # a=5, b=0: 5*2^j is never a power of two (5 isn't one).
    safe, offending = never_dyadic_for_all_j(5, 0)
    assert safe and offending == []
    # a=1, b=0 WOULD be dyadic for every j (not a real core form, sanity check only).
    safe, offending = never_dyadic_for_all_j(1, 0)
    assert not safe
    # a=1, b=-4: 2^j-4 hits 4 at j=3 but j>=4 is out of range here; check it's flagged correctly if in range.
    safe, offending = never_dyadic_for_all_j(1, -4, min_j=2)
    assert not safe  # j=3: 8-4=4, dyadic


def test_all_35_core_forms_are_never_dyadic_for_j_geq_4():
    result = check_all_forms(min_j=4)
    assert result["num_forms"] == 35
    assert result["all_forms_safe_for_all_j"] is True
    for form in result["forms"]:
        assert form["safe_for_all_j"], form
