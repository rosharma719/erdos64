#!/usr/bin/env python3
"""Mechanical cross-check for contraction_separator_integration.md
Parts VI-VII: CB3's three exact cases (clean 2-attachment; the S5
cut-vertex coincidence; the genuinely new >=3-attachment degree-loss
case), and the paired topological-K4 union arithmetic (2*ell+1 always
safe; 2*ell+2 unsafe exactly at ell=2^j-1).

Scope, same discipline as the earlier verifier scripts: nothing here
re-derives S5, T1, or T2 (all cited by name from lemmas.md/two_cut.md);
what IS checked is the structural mechanics CB3' actually reduces to --
2-connectivity and internal-degree preservation in the clean case, and
the exact internal-degree LOSS in the >=3-attachment case.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.contraction_lift import (  # noqa: E402
    Graph,
    from_edges,
    to_nx,
)


def is_power_of_two(n: int) -> bool:
    return n >= 1 and (n & (n - 1)) == 0


# ----------------------------------------------------------------------------
# Part VI: CB3' cases
# ----------------------------------------------------------------------------

def check_cb3_case1_clean():
    """B_v with att(B_v)={v,x} exactly: v adjacent to component C at one
    point, x adjacent to C at another; every C-vertex has degree>=3
    WITHIN B_v+vx, and B_v+vx is 2-connected."""
    v, x = "v", "x"
    edges = [(v, "c1"), ("c1", "c2"), ("c2", "c3"), ("c3", x),
             ("c1", "c3"), ("c2", x)]  # extra edges to keep min degree >=3-ish
    g = from_edges(edges)
    Bv_plus_vx = {w: set(n) for w, n in g.items()}
    Bv_plus_vx.setdefault(v, set())
    Bv_plus_vx.setdefault(x, set())
    Bv_plus_vx[v].add(x)
    Bv_plus_vx[x].add(v)

    G = to_nx(Bv_plus_vx)
    is_2conn = nx.is_biconnected(G)
    internal_degrees = {w: len(n) for w, n in Bv_plus_vx.items() if w not in (v, x)}
    all_ge3 = all(d >= 3 for d in internal_degrees.values())
    return {"is_2connected_with_vx_added": is_2conn,
            "internal_degrees": internal_degrees,
            "all_internal_degree_ge3": all_ge3}


def check_cb3_case3_degree_loss():
    """att(B_v) has 3 elements {v,x,y}. Show that restricting to just
    {v,x} as terminals (dropping edges to y) drops some internal
    vertex's degree below 3, even though its FULL degree (with y
    included) is >=3."""
    v, x, y = "v", "x", "y"
    # C = {c1,c2,c3}; c1 has degree 3 only because of its edge to y
    edges = [(v, "c1"), ("c1", "c2"), ("c2", "c3"), ("c3", x), ("c1", y)]
    g = from_edges(edges)

    full_degree_c1 = len(g["c1"])  # includes edge to y
    assert full_degree_c1 >= 3

    # restrict to just {v,x} as terminals: drop the edge to y entirely
    restricted = {w: set(n) for w, n in g.items() if w != y}
    for w in restricted:
        restricted[w] = restricted[w] - {y}
    restricted_degree_c1 = len(restricted["c1"])

    assert restricted_degree_c1 < full_degree_c1, "the degree-loss phenomenon must be exhibited"
    assert restricted_degree_c1 < 3, "specifically must drop below the delta>=3 threshold"

    return {"full_degree_c1_including_y": full_degree_c1,
            "restricted_degree_c1_excluding_y": restricted_degree_c1,
            "degree_loss_exhibited": True,
            "attachment_set_size": 3}


# ----------------------------------------------------------------------------
# Part VII: paired K4 union arithmetic
# ----------------------------------------------------------------------------

def check_paired_k4_union(ell_values):
    results = []
    for ell in ell_values:
        delta1 = 2 * ell + 1
        delta2 = 2 * ell + 2
        assert not is_power_of_two(delta1), (ell, delta1)
        predicted_unsafe = is_power_of_two(ell + 1)  # ell = 2^j - 1 <=> ell+1 = 2^j
        actual_unsafe = is_power_of_two(delta2)
        assert predicted_unsafe == actual_unsafe, (ell, delta2)
        results.append({"ell": ell, "delta1_2ellplus1": delta1,
                         "delta2_2ellplus2": delta2,
                         "delta2_is_power_of_two": actual_unsafe})
    return results


def main():
    summary = {}
    summary["cb3_case1_clean"] = check_cb3_case1_clean()
    summary["cb3_case3_degree_loss"] = check_cb3_case3_degree_loss()
    summary["paired_k4_union"] = check_paired_k4_union(list(range(2, 20)))

    unsafe_ells = [r["ell"] for r in summary["paired_k4_union"] if r["delta2_is_power_of_two"]]
    summary["delta2_unsafe_ell_values"] = unsafe_ells
    expected = [ell for ell in range(2, 20) if is_power_of_two(ell + 1)]
    assert unsafe_ells == expected, (unsafe_ells, expected)

    print("=== separator_integration.py: mechanical cross-check summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("0 mismatches, 0 assertion failures.")
    return summary


if __name__ == "__main__":
    main()
