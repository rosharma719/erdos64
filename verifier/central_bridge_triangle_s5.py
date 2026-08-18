#!/usr/bin/env python3
"""Mechanical cross-check for central_bridge_triangle_s5.md Part VI.1:
a cut vertex z lying outside a triangle T cannot separate T's vertices,
so T is forced entirely into one lobe -- and, in a double-S5 gadget
where two independent central-bridge analyses (at triangle vertices x
and y) share the same forced cut vertex z, both attachment-free leaves
L, L' land on the SAME side of z, never opposite sides.

Scope, same discipline as the earlier verifier scripts: this does not
re-derive S5 itself (cited by name, "at most one cut vertex"). What IS
checked is the purely structural consequence on explicit gadgets, via
networkx.articulation_points/node_connected_component -- independent of
the hand argument.
"""

from __future__ import annotations

import networkx as nx


def build_double_s5_gadget():
    """Triangle a-b-c (a,b cubic, each with a central bridge). Both
    bridges B_a, B_b reach a single shared cut vertex z of degree
    exactly 4 (S5): 2 edges (via w1,w2) back into the T/theta side, 2
    edges (l1,l2) into the single attachment-free leaf L=L'.
    """
    G = nx.Graph()
    G.add_edges_from([("a", "b"), ("b", "c"), ("c", "a")])
    G.add_edge("a", "aprime")  # a's external (Theta_a) edge
    G.add_edge("b", "bprime")  # b's external (Theta_b) edge

    # B_a: a's third edge, through w1, reaches z (one of z's two
    # "G_2-side" edges).
    G.add_edges_from([("a", "ba1"), ("ba1", "w1"), ("w1", "z")])
    # B_b: b's third edge, through w2, reaches z (z's other
    # "G_2-side" edge) -- both bridges share the same z, degree stays 4.
    G.add_edges_from([("b", "bb1"), ("bb1", "w2"), ("w2", "z")])

    # z's other two edges: the single attachment-free leaf L=L'.
    G.add_edges_from([("z", "l1"), ("z", "l2"), ("l1", "l2")])

    return G


def check_triangle_not_split_and_leaf_on_other_side() -> dict:
    G = build_double_s5_gadget()
    T = {"a", "b", "c"}

    arts = set(nx.articulation_points(G))
    z_is_cut = "z" in arts
    z_degree = G.degree("z")

    H = G.copy()
    H.remove_node("z")
    comp_of_T_side = nx.node_connected_component(H, "a")
    T_together = T <= comp_of_T_side

    comp_of_leaf = nx.node_connected_component(H, "l1")
    leaf_disjoint_from_T_side = comp_of_leaf.isdisjoint(comp_of_T_side)
    only_two_components = nx.number_connected_components(H) == 2

    return {
        "z_is_cut_vertex": z_is_cut,
        "z_degree": z_degree,
        "T_together_after_removing_z": T_together,
        "leaf_disjoint_from_T_side": leaf_disjoint_from_T_side,
        "exactly_two_lobes": only_two_components,
    }


def main():
    res = check_triangle_not_split_and_leaf_on_other_side()
    print(f"triangle_not_split_and_leaf_on_other_side: {res}")
    ok = (
        res["z_is_cut_vertex"]
        and res["z_degree"] == 4
        and res["T_together_after_removing_z"]
        and res["leaf_disjoint_from_T_side"]
        and res["exactly_two_lobes"]
    )
    failures = 0 if ok else 1
    print(f"assertion_failures: {failures}")
    return failures


if __name__ == "__main__":
    import sys

    sys.exit(1 if main() else 0)
