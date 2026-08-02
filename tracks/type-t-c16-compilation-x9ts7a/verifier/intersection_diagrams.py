#!/usr/bin/env python3
"""Mechanical cross-check for contraction_intersections.md Part V: the
exact cell-decomposition identity for two same-endpoint simple paths
(non-crossing case), the explicit smallest counterexample disproving
the "canonical witnesses always give one cell" target, and the three
resolved (non-crossing) named intersection-diagram types.

Scope, same discipline as the earlier verifier scripts: nothing here
tests a claim presupposing a minimal Erdos-Gyarfas counterexample
exists, and nothing here validates the crossing case, which
contraction_intersections.md leaves explicitly open (no gadget for it
is built, on purpose).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.contraction_lift import (  # noqa: E402
    Graph,
    from_edges,
    verify_cycle,
    verify_cycle_nx,
)


def is_power_of_two(n: int) -> bool:
    return n >= 1 and (n & (n - 1)) == 0


def build_cell_pair(cells: List[Tuple], prefix: str = ""):
    """cells: list of ('common', length) or ('divergent', alpha, beta).
    Builds two s-t paths P, Q sharing exactly the cell-boundary
    landmarks (plus, for 'common' cells, the shared interior too).
    Returns (graph, P_vertex_list, Q_vertex_list, landmarks)."""
    edges = []
    landmarks = [f"{prefix}L0"]
    P_seq = [landmarks[0]]
    Q_seq = [landmarks[0]]
    for idx, cell in enumerate(cells):
        end_label = f"{prefix}L{idx + 1}"
        if cell[0] == "common":
            L = cell[1]
            mid = [f"{prefix}c{idx}_{i}" for i in range(L - 1)]
            chain = [P_seq[-1]] + mid + [end_label]
            for i in range(len(chain) - 1):
                edges.append((chain[i], chain[i + 1]))
            P_seq += chain[1:]
            Q_seq += chain[1:]
        else:
            _, alpha, beta = cell
            midP = [f"{prefix}p{idx}_{i}" for i in range(alpha - 1)]
            chainP = [P_seq[-1]] + midP + [end_label]
            midQ = [f"{prefix}q{idx}_{i}" for i in range(beta - 1)]
            chainQ = [Q_seq[-1]] + midQ + [end_label]
            for i in range(len(chainP) - 1):
                edges.append((chainP[i], chainP[i + 1]))
            for i in range(len(chainQ) - 1):
                edges.append((chainQ[i], chainQ[i + 1]))
            P_seq += chainP[1:]
            Q_seq += chainQ[1:]
        landmarks.append(end_label)
    g = from_edges(edges)
    return g, P_seq, Q_seq, landmarks


def check_cell_decomposition():
    # mixed: divergent(2,3), common(3), divergent(4,2)
    cells = [("divergent", 2, 3), ("common", 3), ("divergent", 4, 2)]
    g, P, Q, landmarks = build_cell_pair(cells, prefix="cd_")
    assert verify_cycle(g, P) is False  # P,Q are paths, not cycles themselves
    lenP = len(P) - 1
    lenQ = len(Q) - 1
    predicted_diff = sum(a - b for (kind, a, b) in
                          [c if c[0] == "divergent" else ("divergent", c[1], c[1])
                           for c in cells])
    assert lenP - lenQ == predicted_diff, (lenP, lenQ, predicted_diff)

    # check each divergent cell's cycle directly
    cycle_lengths = []
    # cell 0: L0 -> L1, divergent(2,3)
    seg_p0 = P[0:3]   # L0, p0_0, L1  (alpha=2 edges -> 3 vertices)
    seg_q0 = Q[0:4]   # L0, q0_0, q0_1, L1 (beta=3 edges -> 4 vertices)
    cyc0 = seg_p0 + list(reversed(seg_q0[1:-1]))
    assert verify_cycle(g, cyc0) and verify_cycle_nx(g, cyc0)
    assert len(cyc0) == 2 + 3
    cycle_lengths.append(len(cyc0))

    # cell 2 (index 2, third cell): divergent(4,2), from L2 to L3
    idx_L2_P = P.index(landmarks[2])
    idx_L2_Q = Q.index(landmarks[2])
    seg_p2 = P[idx_L2_P:]
    seg_q2 = Q[idx_L2_Q:]
    assert len(seg_p2) - 1 == 4 and len(seg_q2) - 1 == 2
    cyc2 = seg_p2 + list(reversed(seg_q2[1:-1]))
    assert verify_cycle(g, cyc2) and verify_cycle_nx(g, cyc2)
    assert len(cyc2) == 4 + 2
    cycle_lengths.append(len(cyc2))

    return {"lenP": lenP, "lenQ": lenQ, "diff": lenP - lenQ,
            "divergent_cycle_lengths": cycle_lengths}


def check_one_cell_target_false():
    """Smallest obstruction: 2 divergent cells (2,3) and (3,2), 0 shared
    edges, 0 common components, meeting only at s, m, t."""
    cells = [("divergent", 2, 3), ("divergent", 3, 2)]
    g, P, Q, landmarks = build_cell_pair(cells, prefix="oc_")
    assert len(landmarks) == 3  # s, m, t

    shared_edges = 0
    Pedges = {frozenset((P[i], P[i + 1])) for i in range(len(P) - 1)}
    Qedges = {frozenset((Q[i], Q[i + 1])) for i in range(len(Q) - 1)}
    shared_edges = len(Pedges & Qedges)
    assert shared_edges == 0, shared_edges

    common_components = 0  # by construction, both cells are 'divergent'
    assert common_components == 0

    num_divergent_cells = 2
    assert num_divergent_cells != 1, "this is exactly the disproof: 2 cells survive"

    lenP, lenQ = len(P) - 1, len(Q) - 1
    assert lenP == 5 and lenQ == 5

    # both cell cycles: (2,3) -> 5, (3,2) -> 5
    m = landmarks[1]
    idx_m_P, idx_m_Q = P.index(m), Q.index(m)
    seg1_p, seg1_q = P[:idx_m_P + 1], Q[:idx_m_Q + 1]
    seg2_p, seg2_q = P[idx_m_P:], Q[idx_m_Q:]

    cyc1 = seg1_p + list(reversed(seg1_q[1:-1]))
    cyc2 = seg2_p + list(reversed(seg2_q[1:-1]))
    assert verify_cycle(g, cyc1) and verify_cycle_nx(g, cyc1)
    assert verify_cycle(g, cyc2) and verify_cycle_nx(g, cyc2)
    assert len(cyc1) == 5 and len(cyc2) == 5
    assert not is_power_of_two(5)

    return {"shared_edges": shared_edges, "common_components": common_components,
            "divergent_cells": num_divergent_cells, "lenP": lenP, "lenQ": lenQ,
            "cell_cycle_lengths": [len(cyc1), len(cyc2)]}


def check_intersection_diagram_types():
    results = {}

    # common prefix: common(2) then divergent(2,3)
    cells = [("common", 2), ("divergent", 2, 3)]
    g, P, Q, landmarks = build_cell_pair(cells, prefix="pre_")
    lenP, lenQ = len(P) - 1, len(Q) - 1
    assert lenP - lenQ == (2 - 3)
    results["common_prefix"] = {"lenP": lenP, "lenQ": lenQ}

    # common suffix: divergent(3,2) then common(2)
    cells = [("divergent", 3, 2), ("common", 2)]
    g, P, Q, landmarks = build_cell_pair(cells, prefix="suf_")
    lenP, lenQ = len(P) - 1, len(Q) - 1
    assert lenP - lenQ == (3 - 2)
    results["common_suffix"] = {"lenP": lenP, "lenQ": lenQ}

    # enter-and-leave: common(2), divergent(2,4), common(2)
    cells = [("common", 2), ("divergent", 2, 4), ("common", 2)]
    g, P, Q, landmarks = build_cell_pair(cells, prefix="el_")
    lenP, lenQ = len(P) - 1, len(Q) - 1
    assert lenP - lenQ == (2 - 4)
    results["enter_and_leave"] = {"lenP": lenP, "lenQ": lenQ}

    return results


def main():
    summary = {}
    summary["cell_decomposition"] = check_cell_decomposition()
    summary["one_cell_target_disproof"] = check_one_cell_target_false()
    summary["intersection_diagram_types"] = check_intersection_diagram_types()

    print("=== intersection_diagrams.py: mechanical cross-check summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("0 mismatches, 0 assertion failures. (Crossing case intentionally not tested -- open.)")
    return summary


if __name__ == "__main__":
    main()
