#!/usr/bin/env python3
"""Independent prerequisite audit for the proposed Type-T ladder states.

The identical-terminal ladder requires X_x=y and X_y=x in a T2 triangle,
where x,y are cubic and z is non-cubic.  Pole forcing permits only a
non-cubic aligned pole.  Therefore the transfer graph has no initial state.
This script also checks the reported even-k abstract ladder arithmetic; it
does not claim that colored core is a Type-T graph realization.
"""

from __future__ import annotations

import json


def forbidden(value: int) -> bool:
    return value >= 4 and value & (value - 1) == 0


def pole_rows():
    rows = []
    for x_pole in ("y", "z"):
        for y_pole in ("x", "z"):
            x_pole_cubic = x_pole == "y"
            y_pole_cubic = y_pole == "x"
            survives = not x_pole_cubic and not y_pole_cubic
            rows.append(
                {
                    "X_x": x_pole,
                    "X_y": y_pole,
                    "identical_terminal": x_pole == "y" and y_pole == "x",
                    "pole_forcing_survives": survives,
                    "terminal_relation": (
                        "one_common_terminal" if survives else "eliminated"
                    ),
                }
            )
    return rows


def abstract_ladder_row(k: int) -> dict:
    assert k >= 2 and k % 2 == 0
    rho = 2
    while 3 * k > 2**rho:
        rho += 1
    length = 2**rho
    residual = length - 3 * k
    assert residual >= 0 and residual % 2 == 0
    first_cell = 6 + 2 * residual
    assert not forbidden(first_cell)
    assert not forbidden(6)
    # Alternating (1,5)/(5,1) gives each rail base total 3k.
    assert 3 * k + residual == length
    return {
        "k": k,
        "rho": rho,
        "t_min": rho + 2,
        "residual": residual,
        "rail_lengths": [length, length],
        "cell_lengths": [first_cell] + [6] * (k - 1),
        "abstract_core_clean": True,
        "type_t_prerequisite_survives": False,
    }


def main():
    rows = pole_rows()
    survivors = [row for row in rows if row["pole_forcing_survives"]]
    identical = [row for row in rows if row["identical_terminal"]]
    assert len(rows) == 4
    assert len(survivors) == 1
    assert survivors[0]["X_x"] == survivors[0]["X_y"] == "z"
    assert len(identical) == 1
    assert not identical[0]["pole_forcing_survives"]

    ladders = [abstract_ladder_row(k) for k in range(2, 14, 2)]
    assert ladders[0]["rho"] == 3
    assert ladders[0]["t_min"] == 5

    print(
        json.dumps(
            {
                "assertion_failures": 0,
                "pole_rows": rows,
                "surviving_rows": survivors,
                "identical_terminal_initial_states": 0,
                "accepting_ladder_states": 0,
                "abstract_even_k_ladder_checks": ladders,
                "scope": (
                    "prerequisite audit plus abstract arithmetic; "
                    "not a saturation or graph-realizability search"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
