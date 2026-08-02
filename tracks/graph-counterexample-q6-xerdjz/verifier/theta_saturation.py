#!/usr/bin/env python3
"""Mechanical cross-check for contraction_saturation.md Part VI: the
same-branch (3-formula) and cross-branch (4-formula) theta-bridge
arithmetic, and the internal-vertex-count growth used in the S5
cut-vertex saturation argument.

Scope, same discipline as the earlier verifier scripts: nothing here
tests a claim presupposing a minimal Erdos-Gyarfas counterexample
exists, and nothing here tests or claims to resolve VI.5's saturation
target, which contraction_saturation.md leaves explicitly open.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.contraction_lift import (  # noqa: E402
    Graph,
    from_edges,
    verify_cycle,
    verify_cycle_nx,
)


def is_power_of_two(n: int) -> bool:
    return n >= 1 and (n & (n - 1)) == 0


def build_theta(L0: int, L1: int, L2: int, prefix: str = "th_"):
    """Theta graph: poles x,y joined by three internally-disjoint paths
    of lengths L0,L1,L2. Returns (graph, [branch0_seq, branch1_seq,
    branch2_seq]), each a full x-to-y vertex list."""
    x, y = f"{prefix}x", f"{prefix}y"
    edges = []
    branches = []
    for bi, L in enumerate((L0, L1, L2)):
        mid = [f"{prefix}b{bi}_{i}" for i in range(L - 1)]
        seq = [x] + mid + [y]
        for i in range(len(seq) - 1):
            edges.append((seq[i], seq[i + 1]))
        branches.append(seq)
    g = from_edges(edges)
    return g, branches


def path_between(seq: List, i: int, j: int) -> List:
    """Sub-list of seq from index i to index j inclusive (i<j)."""
    assert i < j
    return seq[i:j + 1]


def check_same_branch_bridge(L0: int, L1: int, L2: int, i: int, j: int, ell: int):
    """Bridge of length ell between branch-0 positions i<j (distance
    d=j-i). Verifies all 3 VI.3 cycle lengths."""
    g, branches = build_theta(L0, L1, L2, prefix=f"sb_{L0}_{L1}_{L2}_{i}_{j}_{ell}_")
    b0, b1, b2 = branches
    u, w = b0[i], b0[j]
    d = j - i

    # add bridge u -- w, length ell, fresh vertices
    mid = [f"bridge_{L0}_{L1}_{L2}_{i}_{j}_{ell}_{k}" for k in range(ell - 1)]
    chain = [u] + mid + [w]
    for k in range(len(chain) - 1):
        g.setdefault(chain[k], set())
        g.setdefault(chain[k + 1], set())
        g[chain[k]].add(chain[k + 1])
        g[chain[k + 1]].add(chain[k])

    results = {}
    x, y = b0[0], b0[-1]

    # (1) bridge + short arc u..w along branch0
    short_arc = path_between(b0, i, j)
    cyc1 = chain[:-1] + list(reversed(short_arc[1:]))
    assert verify_cycle(g, cyc1) and verify_cycle_nx(g, cyc1)
    results["local"] = len(cyc1)
    assert results["local"] == ell + d

    # (2) bridge + (w -> y along b0, forward) + y + (b1 interior, y->x order)
    #     + x + (x -> u along b0, forward) -> closes back to u=cyc[0].
    x_to_u = b0[0:i + 1]            # x ... u  (forward order)
    w_to_y = b0[j:]                  # w ... y  (forward order)
    cyc2 = ([u] + mid + [w]
             + list(w_to_y[1:-1]) + [y]
             + list(reversed(b1[1:-1])) + [x]
             + list(x_to_u[1:-1]))
    assert verify_cycle(g, cyc2), cyc2
    assert verify_cycle_nx(g, cyc2)
    results["via_branch1"] = len(cyc2)
    assert results["via_branch1"] == ell + (L0 - d) + L1

    # (3) same, routed through branch2 instead of branch1
    cyc3 = ([u] + mid + [w]
             + list(w_to_y[1:-1]) + [y]
             + list(reversed(b2[1:-1])) + [x]
             + list(x_to_u[1:-1]))
    assert verify_cycle(g, cyc3), cyc3
    assert verify_cycle_nx(g, cyc3)
    results["via_branch2"] = len(cyc3)
    assert results["via_branch2"] == ell + (L0 - d) + L2

    return results


def check_cross_branch_bridge(L0: int, L1: int, L2: int, d0: int, d1: int, ell: int):
    """Bridge of length ell between a branch-0 point at distance d0 from
    x, and a branch-1 point at distance d1 from x. Verifies all 4 VI.4
    cycle lengths."""
    tag = f"cb_{L0}_{L1}_{L2}_{d0}_{d1}_{ell}_"
    g, branches = build_theta(L0, L1, L2, prefix=tag)
    b0, b1, b2 = branches
    u, w = b0[d0], b1[d1]

    mid = [f"{tag}bridge{k}" for k in range(ell - 1)]
    chain = [u] + mid + [w]
    for k in range(len(chain) - 1):
        g.setdefault(chain[k], set())
        g.setdefault(chain[k + 1], set())
        g[chain[k]].add(chain[k + 1])
        g[chain[k + 1]].add(chain[k])

    x_to_u = b0[0:d0 + 1]      # x..u
    u_to_y = b0[d0:]            # u..y
    x_to_w = b1[0:d1 + 1]       # x..w
    w_to_y = b1[d1:]            # w..y
    x, y = b0[0], b0[-1]

    results = {}

    # (1) via x only: u -bridge- w -[x_to_w rev]- x -[x_to_u]- u
    cyc1 = [u] + mid + [w] + list(reversed(x_to_w[:-1])) + list(x_to_u[1:-1])
    assert verify_cycle(g, cyc1), cyc1
    assert verify_cycle_nx(g, cyc1)
    results["via_x"] = len(cyc1)
    assert results["via_x"] == ell + d0 + d1

    # (2) via y only: u -bridge- w -[w_to_y]- y -[u_to_y rev]- u
    cyc2 = [u] + mid + [w] + list(w_to_y[1:-1]) + [y] + list(reversed(u_to_y[1:-1]))
    assert verify_cycle(g, cyc2), cyc2
    assert verify_cycle_nx(g, cyc2)
    results["via_y"] = len(cyc2)
    assert results["via_y"] == ell + (L0 - d0) + (L1 - d1)

    # (3) via x then full branch2 to y:
    #     u -bridge- w -[w->x along b1]- x -[branch2, x->y]- y -[y->u along b0]- u
    cyc3 = ([u] + mid + [w]
             + list(reversed(x_to_w[1:-1])) + [x]
             + list(b2[1:-1]) + [y]
             + list(reversed(u_to_y[1:-1])))
    assert verify_cycle(g, cyc3), cyc3
    assert verify_cycle_nx(g, cyc3)
    results["via_x_then_branch2"] = len(cyc3)
    assert results["via_x_then_branch2"] == ell + d1 + (L0 - d0) + L2

    # (4) via y then full branch2 to x:
    #     u -bridge- w -[w->y along b1]- y -[branch2, y->x]- x -[x->u along b0]- u
    cyc4 = ([u] + mid + [w]
             + list(w_to_y[1:-1]) + [y]
             + list(reversed(b2[1:-1])) + [x]
             + list(x_to_u[1:-1]))
    assert verify_cycle(g, cyc4), cyc4
    assert verify_cycle_nx(g, cyc4)
    results["via_y_then_branch2"] = len(cyc4)
    assert results["via_y_then_branch2"] == ell + (L1 - d1) + d0 + L2

    return results


def check_cut_vertex_bound(rs_values):
    results = []
    for r, s in rs_values:
        internal = 1 + (2 ** r - 2) + (2 ** s - 1)
        assert internal == 2 ** r + 2 ** s - 2
        assert internal > 1, "the S5 argument needs >1 internal vertex to be nontrivial"
        results.append({"r": r, "s": s, "internal_vertices": internal})
    return results


def main():
    summary = {}

    same_branch = [
        check_same_branch_bridge(L0=7, L1=4, L2=5, i=2, j=5, ell=1),
        check_same_branch_bridge(L0=9, L1=3, L2=4, i=1, j=4, ell=2),
        check_same_branch_bridge(L0=8, L1=6, L2=3, i=3, j=6, ell=1),
    ]
    summary["same_branch_bridge_arithmetic"] = same_branch

    cross_branch = [
        check_cross_branch_bridge(L0=7, L1=4, L2=5, d0=2, d1=1, ell=1),
        check_cross_branch_bridge(L0=9, L1=3, L2=4, d0=3, d1=1, ell=2),
        check_cross_branch_bridge(L0=8, L1=6, L2=3, d0=4, d1=2, ell=1),
    ]
    summary["cross_branch_bridge_arithmetic"] = cross_branch

    summary["cut_vertex_bound"] = check_cut_vertex_bound(
        [(r, s) for r in range(2, 6) for s in range(2, 6)]
    )

    print("=== theta_saturation.py: mechanical cross-check summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("0 mismatches, 0 assertion failures. "
          "(VI.5 saturation target intentionally not tested -- open.)")
    return summary


if __name__ == "__main__":
    main()
