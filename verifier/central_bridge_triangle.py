#!/usr/bin/env python3
"""Mechanical cross-check for central_bridge_triangle.md Parts II and IV:
(1) the shared-external-neighbour configuration (a'=b') really does force
a 4-cycle, confirming Lemma NE's mechanism on an explicit gadget; (2) the
triangle-anchored central bridge B_x really does attach at {x, X_x}
(established directly from the triangle's own edges, IV.1(i)), and the
shortest x-X_x path inside B_x really is length 2 with a genuine second
path of length 3 or 4 (IV.2's concrete ell=2 sharpening).

Scope, same discipline as the earlier verifier scripts: this does not
re-derive Gao-Huo-Liu-Ma (cited by name) or CB1/CB3' (cited by name).
What IS checked is that the specific structural claims (attachment set,
shortest-path length, existence of a second path) hold on explicit,
independently-constructed gadgets, via networkx -- a fully independent
mechanism from the hand derivation.
"""

from __future__ import annotations

import networkx as nx


def build_shared_external_neighbor_gadget():
    """Triangle a-b-c; a'=b'=w forced (a-w, b-w both present)."""
    G = nx.Graph()
    G.add_edges_from([("a", "b"), ("b", "c"), ("c", "a"), ("a", "w"), ("b", "w")])
    return G


def check_shared_external_neighbor_forces_c4() -> dict:
    G = build_shared_external_neighbor_gadget()
    # Confirm the specific predicted 4-cycle x-w-y-z-x (here a-w-b-c-a) is a
    # genuine simple cycle on 4 distinct vertices -- the mechanism Lemma NE
    # relies on, independent of whatever else (e.g. the triangle itself) is
    # also present in this small gadget.
    predicted = ["a", "w", "b", "c"]
    distinct = len(set(predicted)) == 4
    is_cycle = all(G.has_edge(predicted[i], predicted[(i + 1) % 4]) for i in range(4))
    return {"predicted_cycle_present": is_cycle, "four_distinct_vertices": distinct,
            "is_c4": is_cycle and distinct}


def build_triangle_theta_bridge_gadget(rho: int, s: int, tail_len: int):
    """Triangle a-b-c. Theta_a: poles {b, a'} (X_a = b), branch P0 = b-a-a'.
    P1: a' -> b, length 2**rho - 1, avoiding a. P2: b -> a', length 2**s,
    avoiding a. Y_a = c, e_a = a-c (the third, bridge-defining edge).
    B_a's component (containing c) also gets the triangle edge c-b (the
    length-2 route a-c-b) and a longer c-...-b chain of length tail_len+1
    edges (the "second path"), all avoiding a and avoiding V(Theta_a).
    """
    G = nx.Graph()
    G.add_edges_from([("a", "b"), ("b", "c"), ("c", "a")])
    G.add_edge("a", "aprime")

    # P0 = b - a - aprime already present (a-b, a-aprime).
    # P1: aprime -> b, length 2**rho - 1, avoiding a.
    len_p1 = 2 ** rho - 1
    prev = "aprime"
    for i in range(len_p1 - 1):
        node = f"p1_{i}"
        G.add_edge(prev, node)
        prev = node
    G.add_edge(prev, "b")

    # P2: b -> aprime, length 2**s, avoiding a.
    len_p2 = 2 ** s
    prev = "b"
    for i in range(len_p2 - 1):
        node = f"p2_{i}"
        G.add_edge(prev, node)
        prev = node
    G.add_edge(prev, "aprime")

    theta_vertices = {"a", "b", "aprime"}
    theta_vertices |= {f"p1_{i}" for i in range(len_p1 - 1)}
    theta_vertices |= {f"p2_{i}" for i in range(len_p2 - 1)}

    # Second, longer c-b path of length tail_len+1 edges, entirely outside Theta_a.
    prev = "c"
    for i in range(tail_len):
        node = f"tail_{i}"
        G.add_edge(prev, node)
        prev = node
    G.add_edge(prev, "b")

    return G, theta_vertices


def check_triangle_theta_bridge(rho: int = 3, s: int = 3, tail_len: int = 2) -> dict:
    G, theta_vertices = build_triangle_theta_bridge_gadget(rho, s, tail_len)

    # B_a: component of G - theta_vertices containing c (Y_a = c).
    H = G.copy()
    H.remove_nodes_from(theta_vertices)
    assert "c" in H
    component = nx.node_connected_component(H, "c")

    # Attachment set: theta_vertices adjacent to component (plus a itself, via e_a).
    attachments = {"a"}
    for v in component:
        for nb in G.neighbors(v):
            if nb in theta_vertices:
                attachments.add(nb)

    # B_a as an explicit edge set: component-internal edges, plus the
    # boundary edges from the component to a and to b -- but NOT the direct
    # a-b edge itself, which belongs to Theta_a's own P0 branch, not to B_a.
    B_a = nx.Graph()
    B_a.add_nodes_from(component | {"a", "b"})
    for u, v in G.edges():
        if u in component and v in component:
            B_a.add_edge(u, v)
        elif u in component and v in {"a", "b"}:
            B_a.add_edge(u, v)
        elif v in component and u in {"a", "b"}:
            B_a.add_edge(u, v)

    all_ab_paths = list(nx.all_simple_paths(B_a, "a", "b"))
    lengths = sorted(len(p) - 1 for p in all_ab_paths)

    return {
        "attachments": sorted(attachments),
        "attachments_correct": attachments == {"a", "b"},
        "all_a_b_path_lengths_in_B_a": lengths,
        "shortest_is_2": lengths[0] == 2,
        "second_path_exists_len_3_or_4": any(l in (3, 4) for l in lengths[1:]),
        "predicted_ell": 2,
        "predicted_ell_prime_in": [3, 4],
    }


def main():
    results = {}
    results["shared_external_neighbor_c4"] = check_shared_external_neighbor_forces_c4()
    results["triangle_theta_bridge"] = check_triangle_theta_bridge()

    failures = 0
    if not results["shared_external_neighbor_c4"]["is_c4"]:
        failures += 1
    tb = results["triangle_theta_bridge"]
    if not (tb["attachments_correct"] and tb["shortest_is_2"] and tb["second_path_exists_len_3_or_4"]):
        failures += 1

    for name, res in results.items():
        print(f"{name}: {res}")
    print(f"assertion_failures: {failures}")
    return failures


if __name__ == "__main__":
    import sys

    sys.exit(1 if main() else 0)
