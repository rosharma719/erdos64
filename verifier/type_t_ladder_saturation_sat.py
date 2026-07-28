#!/usr/bin/env python3
"""Two algorithmic checks of the ladder's prerequisite consistency.

Variables:
  a := (X_x = y), where y is cubic;
  b := (X_y = x), where x is cubic.

The identical-terminal row requires a and b.  Taking the already-proved pole
forcing theorem as an input gives not a and not b.  The resulting CNF is
UNSAT before saturation variables exist.  This checks that the two stated
prerequisites are inconsistent; it does not independently prove pole forcing.
"""

from __future__ import annotations

import json
from itertools import product


# Positive integers are positive literals; negative integers are negations.
A = 1
B = 2
CNF = ((A,), (B,), (-A,), (-B,))


def clause_value(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)


def exhaustive_models():
    models = []
    audited = []
    for values in product((False, True), repeat=2):
        assignment = {A: values[0], B: values[1]}
        satisfied = all(clause_value(clause, assignment) for clause in CNF)
        audited.append({"a": values[0], "b": values[1], "satisfies": satisfied})
        if satisfied:
            models.append(assignment)
    return audited, models


def simplify(cnf: tuple[tuple[int, ...], ...], variable: int, value: bool):
    true_lit = variable if value else -variable
    false_lit = -true_lit
    reduced = []
    for clause in cnf:
        if true_lit in clause:
            continue
        new_clause = tuple(lit for lit in clause if lit != false_lit)
        if not new_clause:
            return None
        reduced.append(new_clause)
    return tuple(reduced)


def dpll(cnf: tuple[tuple[int, ...], ...]) -> bool:
    if not cnf:
        return True
    if any(not clause for clause in cnf):
        return False
    unit = next((clause[0] for clause in cnf if len(clause) == 1), None)
    if unit is not None:
        reduced = simplify(cnf, abs(unit), unit > 0)
        return False if reduced is None else dpll(reduced)
    variable = abs(cnf[0][0])
    for value in (False, True):
        reduced = simplify(cnf, variable, value)
        if reduced is not None and dpll(reduced):
            return True
    return False


def main():
    audited, models = exhaustive_models()
    exhaustive_unsat = not models
    dpll_unsat = not dpll(CNF)
    assert exhaustive_unsat and dpll_unsat
    print(
        json.dumps(
            {
                "assertion_failures": 0,
                "variables": {"a": "X_x=y", "b": "X_y=x"},
                "clauses": {
                    "identical_terminal": [[A], [B]],
                    "pole_forcing": [[-A], [-B]],
                },
                "assignments_audited": audited,
                "exhaustive_unsat": exhaustive_unsat,
                "second_algorithm_dpll_unsat": dpll_unsat,
                "saturation_variables_created": 0,
                "Q_variables_created": 0,
                "scope": (
                    "consistency check taking pole forcing as an input; "
                    "not an independent proof and not an abstract ladder SAT model"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
