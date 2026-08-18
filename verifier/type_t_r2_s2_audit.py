#!/usr/bin/env python3
"""Independent audit of the interrupted Type-T R_2/S_2 candidate.

This verifier checks only finite incidence/path mechanics.  The theorem is a
hand-written consequence of C4-freeness; this script is not a proof-assistant
formalization and does not construct a minimal counterexample (the audited
local configuration is proved incompatible with C4-freeness).

Two independent checks are used:

1. definition-first symbolic edge accounting for both claimed detour lengths;
2. a NetworkX realization of the joint two-theta local structure, including
   cubic triangle vertices, distinct external neighbours, exact central-bridge
   attachment sets, the forced R_2/S_2 routes, and direct cycle enumeration.

A separate Heawood-based C4-free bridge is a regression for the upstream
logical gap: an isolated shortest path of length 2 need not belong to the
admissible pair supplied by the cited theorem.
"""

from __future__ import annotations

import json

import networkx as nx


def path_edges(path: list[str]) -> set[frozenset[str]]:
    return {frozenset((a, b)) for a, b in zip(path, path[1:])}


def is_cycle_on_edges(path: list[str], edges: set[frozenset[str]]) -> bool:
    return (
        len(path) >= 3
        and len(path) == len(set(path))
        and all(
            frozenset((path[i], path[(i + 1) % len(path)])) in edges
            for i in range(len(path))
        )
    )


def symbolic_incidence_check() -> dict:
    """Exhaust the two detour lengths asserted by the interrupted claim."""
    rows = []
    for ell_prime in (3, 4):
        internal = [f"u{i}" for i in range(ell_prime - 2)]
        detour = ["x", "Y", *internal, "X"]
        edges = path_edges(detour)
        edges |= {
            frozenset(("x", "X")),
            frozenset(("x", "Y")),
            frozenset(("Y", "X")),
        }

        # ell'=3 closes against xX; ell'=4 loses the forced common prefix
        # xY and closes its length-3 suffix against the triangle edge YX.
        forced_cycle = detour if ell_prime == 3 else detour[1:]
        assert is_cycle_on_edges(forced_cycle, edges)
        assert len(forced_cycle) == 4
        rows.append(
            {
                "ell_prime": ell_prime,
                "detour": detour,
                "forced_cycle": forced_cycle,
                "forced_cycle_length": 4,
            }
        )

    # The representative one-common-terminal R_2/S_2 incidence.  Cubicity
    # forces the first post-triangle edges yy' and xx'.
    r2 = ["x", "y", "yprime", "r", "z"]
    s2 = ["y", "x", "xprime", "s", "z"]
    neighborhoods = {
        "x": {"y", "z", "xprime"},
        "y": {"x", "z", "yprime"},
    }
    assert set(r2[1:3]) == {"y", "yprime"}
    assert set(s2[1:3]) == {"x", "xprime"}
    assert r2[2] == next(iter(neighborhoods["y"] - {"x", "z"}))
    assert s2[2] == next(iter(neighborhoods["x"] - {"y", "z"}))

    joint_edges = path_edges(r2) | path_edges(s2)
    joint_edges |= {
        frozenset(("x", "y")),
        frozenset(("y", "z")),
        frozenset(("z", "x")),
    }
    c4_r = ["y", "yprime", "r", "z"]
    c4_s = ["x", "xprime", "s", "z"]
    assert is_cycle_on_edges(c4_r, joint_edges)
    assert is_cycle_on_edges(c4_s, joint_edges)

    # This is the committed 1+4+4 construction as an ordered closed walk:
    # R_2 from x to z, reverse S_2 from z to y, then the edge yx.
    candidate_walk = r2 + list(reversed(s2))[1:]
    candidate_internal_repetitions = sorted(
        vertex for vertex in set(candidate_walk) if candidate_walk.count(vertex) > 1
    )
    assert candidate_internal_repetitions == ["x", "y"]

    # Symmetric difference cancels the two copies of xy from R_2 and S_2;
    # adding the proposed closing xy leaves a C7, not a C9, when all other
    # named vertices are distinct.
    symmetric_cycle = ["x", "y", "yprime", "r", "z", "s", "xprime"]
    assert is_cycle_on_edges(symmetric_cycle, joint_edges)
    assert len(symmetric_cycle) == 7

    return {
        "single_detour_cases": rows,
        "degree_forced_r2": r2,
        "degree_forced_s2": s2,
        "forced_c4s": [c4_r, c4_s],
        "claimed_walk_length": 9,
        "claimed_walk_repeated_vertices": candidate_internal_repetitions,
        "symmetric_difference_cycle_length": 7,
    }


def add_path(graph: nx.Graph, path: list[str]) -> None:
    graph.add_edges_from(zip(path, path[1:]))


def add_theta_branches(
    graph: nx.Graph, pole: str, external: str, owner: str, rho: int = 3, s: int = 3
) -> set[str]:
    """Add the P1/P2 branches of Theta_owner; P0 already lies in T+external."""
    theta_vertices = {owner, pole, external}
    for label, length in (("p1", 2**rho - 1), ("p2", 2**s)):
        internal = [f"{owner}_{label}_{i}" for i in range(length - 1)]
        path = [external, *internal, pole]
        add_path(graph, path)
        theta_vertices.update(internal)
    return theta_vertices


def bridge_data(
    graph: nx.Graph, theta_vertices: set[str], seed: str, center: str
) -> tuple[set[str], nx.Graph]:
    outside = graph.copy()
    outside.remove_nodes_from(theta_vertices)
    component = set(nx.node_connected_component(outside, seed))
    attachments = {center}
    for vertex in component:
        attachments.update(set(graph.neighbors(vertex)) & theta_vertices)

    bridge = nx.Graph()
    bridge.add_nodes_from(component | attachments)
    for a, b in graph.edges():
        if a in component and (b in component or b in attachments):
            bridge.add_edge(a, b)
        elif b in component and a in attachments:
            bridge.add_edge(a, b)
    return attachments, bridge


def networkx_joint_realization_check() -> dict:
    """Realize the complete local R_2/S_2 incidence and enumerate cycles."""
    graph = nx.Graph()
    graph.add_edges_from((("x", "y"), ("y", "z"), ("z", "x")))
    graph.add_edges_from((("x", "xprime"), ("y", "yprime")))

    theta_x = add_theta_branches(graph, "z", "xprime", "x")
    theta_y = add_theta_branches(graph, "z", "yprime", "y")

    r2 = ["x", "y", "yprime", "r", "z"]
    s2 = ["y", "x", "xprime", "s", "z"]
    add_path(graph, r2)
    add_path(graph, s2)

    assert graph.degree("x") == 3
    assert graph.degree("y") == 3
    assert "xprime" != "yprime"
    assert not ({"y", "z"} & set(graph.neighbors("xprime")))
    assert not ({"x", "z"} & set(graph.neighbors("yprime")))

    attachments_x, bridge_x = bridge_data(graph, theta_x, "y", "x")
    attachments_y, bridge_y = bridge_data(graph, theta_y, "x", "y")
    assert attachments_x == {"x", "z"}
    assert attachments_y == {"y", "z"}
    assert all(bridge_x.has_edge(a, b) for a, b in zip(r2, r2[1:]))
    assert all(bridge_y.has_edge(a, b) for a, b in zip(s2, s2[1:]))

    cycles = list(nx.simple_cycles(graph, length_bound=4))
    cycle_sets = {frozenset(cycle) for cycle in cycles if len(cycle) == 4}
    expected = {
        frozenset(("y", "yprime", "r", "z")),
        frozenset(("x", "xprime", "s", "z")),
    }
    assert expected <= cycle_sets

    return {
        "x_degree": graph.degree("x"),
        "y_degree": graph.degree("y"),
        "external_neighbors_distinct": True,
        "theta_x_branch_lengths": [2, 7, 8],
        "theta_y_branch_lengths": [2, 7, 8],
        "attachments_Bx": sorted(attachments_x),
        "attachments_By": sorted(attachments_y),
        "R2": r2,
        "S2": s2,
        "forced_c4_vertex_sets_present": sorted(sorted(cycle) for cycle in expected),
        "f_clean_realization_exists": False,
    }


def theorem_inference_counterexample() -> dict:
    """Refute 'shortest=2, therefore the admissible pair is 2 and 3/4'.

    Subdivide one edge 0-1 of the Heawood graph by Y and attach terminal x
    to Y.  Use X=0.  The bridge closure B+xX is 2-connected, every internal
    vertex has degree at least 3, and B is C4-free.  Its terminal spectrum
    contains 2, but every admissible pair supplied by the length-difference
    conclusion lies strictly above 2.
    """
    bridge = nx.heawood_graph()
    bridge.remove_edge(0, 1)
    bridge.add_edges_from(((0, "Y"), ("Y", 1), ("x", "Y")))

    closure = bridge.copy()
    closure.add_edge("x", 0)
    assert nx.is_biconnected(closure)
    assert min(bridge.degree(v) for v in bridge if v not in {"x", 0}) >= 3
    assert bridge.degree("x") == 1
    assert bridge.degree("Y") == 3

    path_lengths = sorted(
        {len(path) - 1 for path in nx.all_simple_paths(bridge, "x", 0)}
    )
    cycle_lengths = sorted({len(cycle) for cycle in nx.simple_cycles(bridge)})
    admissible_pairs = [
        [a, b]
        for i, a in enumerate(path_lengths)
        for b in path_lengths[i + 1 :]
        if b - a in (1, 2)
    ]

    assert path_lengths == [2, 7, 9, 11, 13, 15]
    assert 3 not in path_lengths and 4 not in path_lengths
    assert admissible_pairs == [[7, 9], [9, 11], [11, 13], [13, 15]]
    assert 4 not in cycle_lengths
    assert 8 in cycle_lengths  # negative inference fixture, not F-clean

    return {
        "closure_biconnected": True,
        "internal_min_degree": 3,
        "terminal_path_lengths": path_lengths,
        "admissible_pairs": admissible_pairs,
        "c4_free": True,
        "f_clean": False,
        "contains_c8": True,
        "inference_refuted": True,
    }


def main() -> int:
    result = {
        "symbolic_incidence": symbolic_incidence_check(),
        "networkx_joint_realization": networkx_joint_realization_check(),
        "theorem_inference_counterexample": theorem_inference_counterexample(),
        "assertion_failures": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
