#!/usr/bin/env python3
"""Exact arithmetic audit for Type-T path-cell decompositions.

This is not a graph-realizability search.  It classifies positive cell-arc
compositions with prescribed divergent totals, independently brute-forces the
small range, and sweeps every permitted cell count for the four cross-theta
length types through exponent 12.
"""

from __future__ import annotations

import json
from functools import lru_cache
from itertools import combinations


MIN_EXPONENT = 2
MAX_EXPONENT = 12
BRUTE_MAX_TOTAL = 10


def forbidden(value: int) -> bool:
    return value >= 4 and value & (value - 1) == 0


def compositions(total: int, parts: int):
    """Yield every positive ordered composition of total into parts."""
    if parts == 1:
        yield (total,)
        return
    for cuts in combinations(range(1, total), parts - 1):
        points = (0,) + cuts + (total,)
        yield tuple(points[index + 1] - points[index] for index in range(parts))


def classification(total_a: int, total_b: int, cells: int) -> str:
    """Return FORCED, UNIVERSALLY_SAFE, or ESCAPABLE_BUT_NOT_UNIVERSAL."""
    assert 1 <= cells <= min(total_a, total_b)
    total = total_a + total_b
    assert total >= 3 * cells
    if cells == 1:
        return "FORCED" if forbidden(total) else "UNIVERSALLY_SAFE"
    if total == 3 * cells:
        return "UNIVERSALLY_SAFE"
    if total == 3 * cells + 1:
        return "FORCED"
    return "ESCAPABLE_BUT_NOT_UNIVERSAL"


def allocate(cell_sums: tuple[int, ...], total_a: int):
    """Allocate positive a_i with a_i < cell_sum_i and prescribed sum."""
    allocation = [1] * len(cell_sums)
    remaining = total_a - len(cell_sums)
    for index, cell_sum in enumerate(cell_sums):
        increment = min(remaining, cell_sum - 2)
        allocation[index] += increment
        remaining -= increment
    assert remaining == 0
    other = [cell_sum - value for cell_sum, value in zip(cell_sums, allocation)]
    return tuple(allocation), tuple(other)


def safe_witness(total_a: int, total_b: int, cells: int):
    """Construct a safe decomposition whenever the classification permits it."""
    total = total_a + total_b
    if cells == 1:
        if forbidden(total):
            return None
        return ((total_a,), (total_b,))

    # Reserve cells-2 safe triangles.  U=7 is the unique obstruction to
    # writing U>=6 as a sum of two nonforbidden integers at least three.
    remainder = total - 3 * (cells - 2)
    last_two = next(
        (
            (left, remainder - left)
            for left in range(3, remainder - 2)
            if not forbidden(left) and not forbidden(remainder - left)
        ),
        None,
    )
    if last_two is None:
        return None
    cell_sums = (3,) * (cells - 2) + last_two
    assert all(not forbidden(value) for value in cell_sums)
    return allocate(cell_sums, total_a)


def unsafe_witness(total_a: int, total_b: int, cells: int):
    """Construct a decomposition containing a forbidden cell, if one exists."""
    total = total_a + total_b
    if cells == 1:
        if not forbidden(total):
            return None
        return ((total_a,), (total_b,))
    if total == 3 * cells:
        return None
    extra = total - (4 + 3 * (cells - 1))
    cell_sums = (4, 3 + extra) + (3,) * (cells - 2)
    return allocate(cell_sums, total_a)


def cell_lengths(witness):
    if witness is None:
        return None
    first, second = witness
    return tuple(a + b for a, b in zip(first, second))


@lru_cache(maxsize=None)
def brute_classification(total_a: int, total_b: int, cells: int) -> str:
    saw_safe = False
    saw_unsafe = False
    for first in compositions(total_a, cells):
        for second in compositions(total_b, cells):
            if any(a + b < 3 for a, b in zip(first, second)):
                continue
            hit = any(forbidden(a + b) for a, b in zip(first, second))
            saw_unsafe |= hit
            saw_safe |= not hit
    if saw_unsafe and not saw_safe:
        return "FORCED"
    if saw_safe and not saw_unsafe:
        return "UNIVERSALLY_SAFE"
    assert saw_safe and saw_unsafe
    return "ESCAPABLE_BUT_NOT_UNIVERSAL"


def validate_witness(total_a: int, total_b: int, cells: int, witness, safe: bool):
    if witness is None:
        return
    first, second = witness
    assert len(first) == len(second) == cells
    assert all(value > 0 for value in first + second)
    assert sum(first) == total_a and sum(second) == total_b
    hit = any(forbidden(value) for value in cell_lengths(witness))
    assert hit is not safe


def path_totals(kind: str, left: int, right: int):
    if kind == "R_R":
        return 2**left, 2**right
    if kind == "R_S":
        return 2**left, 2**right + 1
    if kind == "S_R":
        return 2**left + 1, 2**right
    if kind == "S_S":
        return 2**left + 1, 2**right + 1
    raise AssertionError(kind)


def main():
    brute_rows = 0
    for total_a in range(1, BRUTE_MAX_TOTAL + 1):
        for total_b in range(1, BRUTE_MAX_TOTAL + 1):
            for cells in range(1, min(total_a, total_b, (total_a + total_b) // 3) + 1):
                expected = classification(total_a, total_b, cells)
                assert brute_classification(total_a, total_b, cells) == expected
                validate_witness(
                    total_a, total_b, cells, safe_witness(total_a, total_b, cells), True
                )
                validate_witness(
                    total_a, total_b, cells, unsafe_witness(total_a, total_b, cells), False
                )
                brute_rows += 1

    sweep_rows = 0
    class_counts = {
        "FORCED": 0,
        "UNIVERSALLY_SAFE": 0,
        "ESCAPABLE_BUT_NOT_UNIVERSAL": 0,
    }
    for kind in ("R_R", "R_S", "S_R", "S_S"):
        for left in range(MIN_EXPONENT, MAX_EXPONENT + 1):
            for right in range(MIN_EXPONENT, MAX_EXPONENT + 1):
                total_a, total_b = path_totals(kind, left, right)
                maximum_cells = min(total_a, total_b, (total_a + total_b) // 3)
                for cells in range(1, maximum_cells + 1):
                    result = classification(total_a, total_b, cells)
                    class_counts[result] += 1
                    # Checking every permitted k is cheap; materializing O(k)
                    # witnesses for every large row would obscure the exact sweep.
                    if cells in {1, 2, maximum_cells}:
                        validate_witness(
                            total_a,
                            total_b,
                            cells,
                            safe_witness(total_a, total_b, cells),
                            True,
                        )
                        validate_witness(
                            total_a,
                            total_b,
                            cells,
                            unsafe_witness(total_a, total_b, cells),
                            False,
                        )
                    sweep_rows += 1

    examples = {}
    for name, total_a, total_b, cells in (
        ("equal_R_R_safe_escape", 4, 4, 2),
        ("mixed_universal_claim_counterexample", 4, 5, 2),
        ("S_S_universal_claim_counterexample", 5, 5, 2),
    ):
        safe = safe_witness(total_a, total_b, cells)
        unsafe = unsafe_witness(total_a, total_b, cells)
        examples[name] = {
            "totals": [total_a, total_b],
            "cells": cells,
            "safe": [list(safe[0]), list(safe[1]), list(cell_lengths(safe))],
            "unsafe": [list(unsafe[0]), list(unsafe[1]), list(cell_lengths(unsafe))],
        }

    print(
        json.dumps(
            {
                "assertion_failures": 0,
                "theorem": {
                    "k=1": "FORCED iff m+n is a forbidden power of two; otherwise UNIVERSALLY_SAFE",
                    "k>=2,m+n=3k": "UNIVERSALLY_SAFE",
                    "k>=2,m+n=3k+1": "FORCED",
                    "k>=2,m+n>=3k+2": "ESCAPABLE_BUT_NOT_UNIVERSAL",
                },
                "brute_force": {
                    "max_total_each_path": BRUTE_MAX_TOTAL,
                    "all_cell_counts": True,
                    "rows": brute_rows,
                },
                "exponent_sweep": {
                    "minimum": MIN_EXPONENT,
                    "maximum": MAX_EXPONENT,
                    "pair_types": ["R_R", "R_S", "S_R", "S_S"],
                    "all_cell_counts": True,
                    "rows": sweep_rows,
                    "classification_counts": class_counts,
                },
                "smallest_examples": examples,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
