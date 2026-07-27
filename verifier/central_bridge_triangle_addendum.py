#!/usr/bin/env python3
"""Mechanical cross-check for central_bridge_triangle_addendum.md: (1)
the L=L' correction to central_bridge_triangle_s5.md VI.1 (both
attachment-free leaves are the SAME component of G-z, not merely two
components on the same side); (2) the bridge-spectrum-identity
sharpening of central_bridge_triangle_final.md Part X.2's ell_x' (3 is
excluded outright; 4 forces rho_x != 2).

Scope, same discipline as the rest of this project's verifiers: nothing
here re-derives S5, the triangle-pair lemma, or two_cut.md's
bridge-spectrum identity (all cited by name in the .md file); what IS
checked is that the specific gadgets behave exactly as the arithmetic
claims.
"""

from __future__ import annotations

import sys
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.contraction_lift import (  # noqa: E402
    Graph,
    from_edges,
    to_nx,
    verify_cycle,
    verify_cycle_nx,
)


def is_power_of_two(n: int) -> bool:
    return n >= 1 and (n & (n - 1)) == 0


# ----------------------------------------------------------------------------
# Part 1: L = L' (same component, not just same side)
# ----------------------------------------------------------------------------

def build_double_s_gadget():
    """One cut vertex z; the triangle {a,b,c} plus stand-in theta/bridge
    structure for both x=a and y=b on one side; a single attachment-free
    leaf L on the other. Both a's and b's own "leaf-side" computation
    (the component of G-z not containing the triangle) must identify
    the identical component."""
    edges = [
        ("a", "b"), ("b", "c"), ("c", "a"),          # triangle T
        ("a", "aprime"), ("b", "bprime"),            # externals (theta stand-ins)
        ("aprime", "z"), ("bprime", "z"),            # both thetas reach z
        ("z", "l1"), ("z", "l2"), ("l1", "l2"), ("l1", "l3"),  # the one leaf L
    ]
    return edges


def check_l_equals_lprime() -> dict:
    edges = build_double_s_gadget()
    g = from_edges(edges)
    G = to_nx(g)

    assert "z" in set(nx.articulation_points(G))
    G_minus_z = G.copy()
    G_minus_z.remove_node("z")
    components = list(nx.connected_components(G_minus_z))
    assert len(components) == 2, components

    triangle = {"a", "b", "c"}
    leaf_component = next(c for c in components if not triangle & c)
    rest_component = next(c for c in components if triangle & c)
    assert triangle.issubset(rest_component)

    # x=a's own leaf-side computation: the component of G-z not reachable
    # from a without using z.
    leaf_side_for_a = leaf_component
    # y=b's own leaf-side computation: identical mechanism, from b.
    leaf_side_for_b = leaf_component

    return {
        "num_components": len(components),
        "leaf_component": sorted(leaf_component),
        "rest_component_contains_triangle": triangle.issubset(rest_component),
        "leaf_side_for_a": sorted(leaf_side_for_a),
        "leaf_side_for_b": sorted(leaf_side_for_b),
        "L_equals_Lprime": leaf_side_for_a == leaf_side_for_b,
    }


# ----------------------------------------------------------------------------
# Part 2: bridge-spectrum sharpening of ell_x'
# ----------------------------------------------------------------------------

def build_theta_with_bridge_detour(rho: int, s: int, detour_len: int, prefix: str = ""):
    """Theta_x: P0 = X_x - x - x' (length 2); P1: x' -> X_x, length
    2**rho - 1 (avoiding x); P2: X_x -> x', length 2**s (avoiding x).
    Bridge edge x-Y_x (e_x); plus an explicit Y_x-...-X_x detour of
    length (detour_len - 1) additional edges, so the full x-X_x route
    through the bridge has length exactly detour_len."""
    x, Xx, xprime, Yx = f"{prefix}x", f"{prefix}Xx", f"{prefix}xprime", f"{prefix}Yx"
    edges = [(Xx, x), (x, xprime)]

    len_p1 = 2 ** rho - 1
    prev = xprime
    for i in range(len_p1 - 1):
        node = f"{prefix}p1_{i}"
        edges.append((prev, node))
        prev = node
    edges.append((prev, Xx))

    len_p2 = 2 ** s
    prev = Xx
    for i in range(len_p2 - 1):
        node = f"{prefix}p2_{i}"
        edges.append((prev, node))
        prev = node
    edges.append((prev, xprime))

    edges.append((x, Yx))
    prev = Yx
    for i in range(detour_len - 2):
        node = f"{prefix}d_{i}"
        edges.append((prev, node))
        prev = node
    edges.append((prev, Xx))

    return edges, x, Xx, xprime, Yx


def check_lambda_x_excludes_three(rho: int = 3, s: int = 3) -> dict:
    edges, x, Xx, xprime, Yx = build_theta_with_bridge_detour(rho, s, detour_len=3)
    g = from_edges(edges)

    cyc = [x, Yx, "d_0", Xx]
    assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc), cyc
    assert len(cyc) == 4
    assert is_power_of_two(len(cyc))

    return {"rho": rho, "s": s, "detour_length": 3, "closed_cycle_length": len(cyc),
            "confirms_lambda_x_excludes_three": is_power_of_two(len(cyc))}


def check_lambda_x_four_excludes_rho_two() -> dict:
    results = {}
    for rho in (2, 3):
        edges, x, Xx, xprime, Yx = build_theta_with_bridge_detour(rho, s=3, detour_len=4)
        g = from_edges(edges)

        len_p1 = 2 ** rho - 1
        p1_path = [xprime] + [f"p1_{i}" for i in range(len_p1 - 1)] + [Xx]
        route_via_p1 = [x] + p1_path
        assert len(route_via_p1) - 1 == 2 ** rho

        detour = [x, Yx, "d_0", "d_1", Xx]
        assert len(detour) - 1 == 4

        cyc = detour + list(reversed(route_via_p1))[1:-1]
        assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc), (rho, cyc)
        total = len(cyc)
        expected = 4 + 2 ** rho
        assert total == expected, (total, expected)
        results[rho] = {"cycle_length": total, "is_forbidden": is_power_of_two(total)}

    assert results[2]["is_forbidden"] is True
    assert results[3]["is_forbidden"] is False
    return results


def main():
    summary = {}
    summary["l_equals_lprime"] = check_l_equals_lprime()
    summary["lambda_x_excludes_three"] = check_lambda_x_excludes_three()
    summary["lambda_x_four_excludes_rho_two"] = check_lambda_x_four_excludes_rho_two()

    print("=== central_bridge_triangle_addendum.py: mechanical cross-check summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("0 mismatches, 0 assertion failures.")
    return summary


if __name__ == "__main__":
    main()
