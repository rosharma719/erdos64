#!/usr/bin/env python3
"""Mechanical cross-check for central_bridge_triangle_final.md Part X.0:
over all 4 rows of central_bridge_triangle.md Part V.1's (X_x,X_y)
table, the two admissible-pair terminal sets {x,X_x} and {y,X_y} always
either coincide or share exactly one element -- never four distinct
vertices (the "crossing" configuration is arithmetically impossible,
since both sets are 2-subsets of the single 3-element triangle T).

This is an exhaustive check over all 4 possible configurations (not a
sampled search): X_x ranges over T\\{x} (2 choices), X_y over T\\{y}
(2 choices), 2*2=4 total, matching the table exactly.
"""

from __future__ import annotations


def check_terminal_pair_exhaustion() -> dict:
    x, y, z0 = "x", "y", "z0"
    T = {x, y, z0}

    rows = []
    for X_x in T - {x}:
        for X_y in T - {y}:
            pair1 = frozenset({x, X_x})
            pair2 = frozenset({y, X_y})
            shared = pair1 & pair2
            rows.append({
                "X_x": X_x, "X_y": X_y,
                "pair1": sorted(pair1), "pair2": sorted(pair2),
                "identical": pair1 == pair2,
                "shared_count": len(shared),
            })

    all_ok = all(r["identical"] or r["shared_count"] == 1 for r in rows)
    never_four_distinct = all(len(set(r["pair1"]) | set(r["pair2"])) <= 3 for r in rows)
    return {
        "num_rows": len(rows),
        "rows": rows,
        "all_identical_or_one_shared": all_ok,
        "never_four_distinct_terminals": never_four_distinct,
    }


def main():
    res = check_terminal_pair_exhaustion()
    print(f"terminal_pair_exhaustion: num_rows={res['num_rows']}")
    for r in res["rows"]:
        print(f"  {r}")
    ok = (
        res["num_rows"] == 4
        and res["all_identical_or_one_shared"]
        and res["never_four_distinct_terminals"]
    )
    failures = 0 if ok else 1
    print(f"assertion_failures: {failures}")
    return failures


if __name__ == "__main__":
    import sys

    sys.exit(1 if main() else 0)
