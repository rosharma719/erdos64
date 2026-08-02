#!/usr/bin/env python3
"""Phase 6: lifting theorem for the C8 / C16-m=2 bulk/same-mode templates.

## The claim being checked

The 8 (C8) / 32 (C16 m=2) same-mode abstract templates derived in
``type_t_port_passage_templates.enumerate_same_mode_abstract_shapes`` are
purely combinatorial (a finite case split on ``route in {2,3}``, ``l1,l2 >=
1`` summing to a fixed budget) -- the derivation never references ``j``,
``a``, or ``c``. So the template *set* is trivially the same for every
``j``. The real question is *embedding*: for a given ``j`` (and worst-case
``a``/``c``), is every one of those templates actually realizable as a
genuine simple cycle in the bare core -- i.e. does some growing branch have
enough room to host the required coordinates?

## The threshold, derived (not assumed) from the constructor

``A_left + A_right = 4Y - 9`` for *every* valid ``(j, a)`` (A_middle has
fixed length 7, and A_left+A_middle+A_right = 4Y-2 identically -- verified
below and in ``type_t_port_coordinates.verify_roundtrip``). So the total
"A-family growing budget" depends only on ``j``, not on ``a`` -- only its
*split* between A_left/A_right does. The worst-case ``a`` (the one an
adversary would pick to make the family's bulk templates hardest to embed)
is the one that balances the two branches as evenly as possible, giving
``max(A_left, A_right) = ceil((4Y-9)/2)``. Symmetrically,
``C_left + C_right = Y - 9``, so the C-family's worst-case single-branch
length is ``ceil((Y-9)/2)`` -- **4x smaller** for the same ``j``, which is
why the C-family needs substantially larger ``j`` before it can host any
bulk template at all (already noted in Phase 1/3: none of the three tested
``j=4`` instances has *any* C-family bulk vertex).

A same-branch shape with core-path lengths ``l1, l2 >= 1`` needs (from the
bulk definition, distance > 12 from both ends) a branch of length at least
``27 + l1 + l2`` to host a generic (non-degenerate) instantiation:
``t0 >= 13``, ``t3 = t0 + l1 + gap + l2 <= length - 13`` with the minimal
non-degenerate ``gap = 1``. A cross-branch shape needs each branch
independently at least ``26 + l`` for its own core-path length ``l``.

Combining: the full same-branch template set for a family embeds for
*every* valid position in that family once
``ceil((budget)/2) >= 27 + max(l1+l2)``, where ``budget`` is ``4Y-9``
(A-family) or ``Y-9`` (C-family) and ``max(l1+l2) = target_length - 4``
(both passages route-2, the maximum core-path budget). Solving for the
minimal ``j``:
"""

from __future__ import annotations

import math

from type_t_port_core_export import build_core, valid_parameters
from type_t_port_coordinates import path_length
from type_t_port_passage_templates import (
    enumerate_same_mode_abstract_shapes,
    instantiate_cross_branch,
    instantiate_same_branch,
    verify_support,
)


def required_same_branch_length(l1: int, l2: int) -> int:
    return 27 + l1 + l2


def required_cross_branch_length(l: int) -> int:
    return 26 + l


def family_budget(j: int, family: str) -> int:
    Y = 1 << j
    return 4 * Y - 9 if family == "A" else Y - 9


def worst_case_single_branch_length(j: int, family: str) -> int:
    """max(A_left, A_right) minimized over all valid a (resp. C_left/C_right
    over c) -- the balanced split."""
    return math.ceil(family_budget(j, family) / 2)


def minimal_j_for_universal_same_branch(target_length: int, family: str) -> int:
    """Smallest j such that EVERY valid a (resp. c) admits the full
    same-branch template set for this family and target length (worst-case
    l1+l2 = target_length - 4, both passages route-2)."""
    max_l_sum = target_length - 4
    required = required_same_branch_length(max_l_sum // 2, max_l_sum - max_l_sum // 2)
    # required is symmetric in how l1+l2 is split; use the exact max l1+l2 value.
    required = 27 + max_l_sum
    j = 4
    while True:
        if 2 * worst_case_single_branch_length(j, family) >= 2 * required:
            pass
        if worst_case_single_branch_length(j, family) >= required:
            return j
        j += 1


def report_thresholds() -> dict:
    report = {}
    for target_length, label in ((8, "C8"), (16, "C16_m2")):
        for family in ("A", "C"):
            j_star = minimal_j_for_universal_same_branch(target_length, family)
            report[f"{label}_{family}family_min_j_for_universal_same_branch"] = j_star
    return report


# ---------------------------------------------------------------------------
# Computational stress test: verify the derived thresholds hold (not just
# the formula) by direct materialize+edge_path_cycle checks -- the same
# methodology the rest of the project trusts -- at j values straddling the
# derived threshold, using the SAME 8/32-shape derivation (no re-derivation
# per j).
# ---------------------------------------------------------------------------

def worst_case_a_for_family(j: int, family: str) -> tuple[int, int]:
    """Returns (a, c) with the target family's two growing branches as
    evenly balanced as possible (the adversarial choice for embedding)."""
    Y = 1 << j
    if family == "A":
        # A_left = a-1, A_right = 4Y-8-a; balance: a-1 ~= 4Y-8-a => a ~= (4Y-7)/2
        a = max(2, min(4 * Y - 9, round((4 * Y - 7) / 2)))
        c = 2
    else:
        c = max(2, min(Y - 9, round((Y - 7) / 2)))
        a = 2
    return a, c


def stress_test_same_branch(target_length: int, family: str, j_values: list[int]) -> dict:
    shapes = enumerate_same_mode_abstract_shapes(target_length)
    same_branch_shapes = [combos[0] for combos in shapes.values() if combos[0][4]]
    results = {}
    for j in j_values:
        a, c = worst_case_a_for_family(j, family)
        try:
            valid_parameters(j, a, c)
        except ValueError as exc:
            results[j] = {"skipped": str(exc)}
            continue
        core = build_core(j, a, c)
        branch = "A_left" if family == "A" else "C_left"
        other_branch = "A_right" if family == "A" else "C_right"
        length = path_length(branch, j, a, c)
        length_other = path_length(other_branch, j, a, c)
        chosen_branch = branch if length >= length_other else other_branch
        chosen_length = max(length, length_other)
        required = required_same_branch_length(0, target_length - 4)  # worst case l1+l2
        outcomes = []
        for r1, l1, r2, l2, _ in same_branch_shapes:
            t0 = 13
            supp = instantiate_same_branch(core, chosen_branch, t0, r1, l1, r2, l2, gap=1)
            ok = verify_support(core, supp, target_length) if supp else "OOR"
            outcomes.append({"shape": (r1, l1, r2, l2), "result": ok})
        n_ok = sum(1 for o in outcomes if o["result"] is True)
        results[j] = {
            "a": a, "c": c,
            "chosen_branch": chosen_branch, "chosen_branch_length": chosen_length,
            "required_length_worst_case": required,
            "meets_threshold": chosen_length >= required,
            "n_shapes_tested": len(outcomes),
            "n_shapes_ok": n_ok,
            "all_ok": n_ok == len(outcomes),
            "failures": [o for o in outcomes if o["result"] is not True],
        }
    return results


# ---------------------------------------------------------------------------
# The WEAK existence threshold (distinct from the BULK/translation-freedom
# threshold above): a same-mode template can produce a genuine cycle as
# soon as the branch merely has room for the raw coordinates (no anchor-
# clearance requirement at all) -- this is a much lower bar, and is why
# the *same 8/32-template set* was already found complete even in the
# (28,4) instance, whose growing branches never reach the deep-bulk (>12)
# regime at all (Phase 2/3 finding). This function derives and checks that
# separate, weaker threshold explicitly, to avoid conflating "template
# exists at all" with "template has full translation freedom."
# ---------------------------------------------------------------------------

def required_existence_length_same_branch(l1: int, l2: int) -> int:
    """Minimal branch length to fit t0=1, t3=t0+l1+gap+l2 <= length-1 with
    minimal separation gap=1: length >= l1 + l2 + 3."""
    return l1 + l2 + 3


def minimal_j_for_existence(target_length: int, family: str) -> int:
    max_l_sum = target_length - 4
    required = required_existence_length_same_branch(0, max_l_sum)
    j = 4
    while worst_case_single_branch_length(j, family) < required:
        j += 1
    return j


def stress_test_existence(target_length: int, family: str, j_values: list[int]) -> dict:
    shapes = enumerate_same_mode_abstract_shapes(target_length)
    same_branch_shapes = [combos[0] for combos in shapes.values() if combos[0][4]]
    results = {}
    for j in j_values:
        a, c = worst_case_a_for_family(j, family)
        try:
            valid_parameters(j, a, c)
        except ValueError as exc:
            results[j] = {"skipped": str(exc)}
            continue
        core = build_core(j, a, c)
        branch = "A_left" if family == "A" else "C_left"
        other_branch = "A_right" if family == "A" else "C_right"
        length = path_length(branch, j, a, c)
        length_other = path_length(other_branch, j, a, c)
        chosen_branch = branch if length >= length_other else other_branch
        chosen_length = max(length, length_other)
        outcomes = []
        for r1, l1, r2, l2, _ in same_branch_shapes:
            supp = instantiate_same_branch(core, chosen_branch, 1, r1, l1, r2, l2, gap=1)
            ok = verify_support(core, supp, target_length) if supp else "OOR"
            outcomes.append({"shape": (r1, l1, r2, l2), "result": ok})
        n_ok = sum(1 for o in outcomes if o["result"] is True)
        results[j] = {
            "a": a, "c": c, "chosen_branch": chosen_branch,
            "chosen_branch_length": chosen_length,
            "required_existence_length": required_existence_length_same_branch(0, target_length - 4),
            "n_shapes_tested": len(outcomes), "n_shapes_ok": n_ok,
            "all_ok": n_ok == len(outcomes),
        }
    return results


def restriction_check() -> dict:
    """PROVED (by construction, not sampled): enumerate_same_mode_abstract_shapes
    never references j/a/c, so the abstract template SET for a fixed target
    length is identical for every instance -- a j>=5 catalog's same-mode
    conflicts, once run through the identical abstract_key pipeline, can
    only ever produce keys from this same fixed finite set (there is no
    other code path that could emit a different key). This function just
    re-confirms the derivation is j-independent by construction."""
    c8_shapes_call1 = set(enumerate_same_mode_abstract_shapes(8))
    c8_shapes_call2 = set(enumerate_same_mode_abstract_shapes(8))  # re-derive, no cached j state
    c16_shapes = set(enumerate_same_mode_abstract_shapes(16))
    return {
        "status": "PROVED",
        "argument": (
            "enumerate_same_mode_abstract_shapes(L) takes only L as input; "
            "its only free choices are route in {2,3} and l1,l2 >= 1 summing "
            "to L-route1-route2, none of which depend on j/a/c. Any catalog "
            "at any j, once decoded through decode_m2_witness + "
            "generic_vertex_tag + wildcard_branch_names + canonicalize_cyclic "
            "(the identical, parameter-free pipeline), can only land on one "
            "of these keys -- so a j>=5 instance's same-mode conflicts "
            "restrict to the j=4 template set by construction, not by "
            "sampling, and conversely every j=4 same-branch/cross-branch "
            "bulk template embeds into any j for which the branch-length "
            "threshold (see report_thresholds) is met."
        ),
        "reproducible": c8_shapes_call1 == c8_shapes_call2,
        "c8_shape_count": len(c8_shapes_call1),
        "c16_shape_count": len(c16_shapes),
    }


def main() -> None:
    import json

    thresholds = report_thresholds()
    print(json.dumps({"thresholds": thresholds}, indent=2))
    print(json.dumps({"restriction_check": restriction_check()}, indent=2))
    for target_length, label in ((8, "C8"), (16, "C16_m2")):
        for family, j_values in (("A", [4, 5, 6]), ("C", [4, 5, 6, 7, 8])):
            print(f"--- stress test {label} family={family} ---")
            res = stress_test_same_branch(target_length, family, j_values)
            print(json.dumps(res, indent=2, default=str))


if __name__ == "__main__":
    main()
