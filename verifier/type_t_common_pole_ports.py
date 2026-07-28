#!/usr/bin/env python3
"""Symbolic audit of shared ports in the degree-four common-pole core.

The program verifies the attachment-route formulas, degree-four localization
rules, and an explicit scalable E2_parallel two-port incidence family.  It is
not a SAT model, a graph census, or a completion of the MA2 leaf remainders.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict


def is_power_of_two(value: int) -> bool:
    return value >= 4 and value & (value - 1) == 0


def is_forbidden_port_route(value: int) -> bool:
    return is_power_of_two(value + 2)


def same_branch_routes(length: int, other: int, a: int, b: int):
    """Generic port, same A/B branch, including the triangle detour."""
    assert 0 < a < b < length
    return (
        b - a,
        a + 2 + length - b,
        a + 3 + length - b,
        a + other + length - b,
    )


def different_branch_routes(M: int, N: int, a: int, b: int):
    """Generic port, one attachment on A and one on B."""
    assert 0 < a < M and 0 < b < N
    return (
        a + b,
        (M - a) + (N - b),
        a + 2 + (N - b),
        (M - a) + 2 + b,
        a + 3 + (N - b),
        (M - a) + 3 + b,
    )


def far_pole_routes(length: int, other: int, a: int):
    """q=x' to an internal point; its port cannot be the triangle vertex y."""
    assert 0 < a < length
    return (length - a, a + 2, a + 3, a + other)


def near_pole_routes_avoiding_y(length: int, other: int, a: int):
    """p=z_0 to y' on a branch, when the shared port is forced to be y."""
    assert 0 < a < length
    return (a, length - a + 2, length - a + other)


def center_routes_avoiding_y(length: int, other: int, a: int):
    """v=x to y' on a branch, with shared port y removed from the return route."""
    assert 0 < a < length
    return (1 + a, 1 + length - a, 1 + other + a, 1 + other + length - a)


# An affine edge length is k*Y + b + ca*a + cc*c.
Affine = tuple[int, int, int, int]


def affine_add(*values: Affine) -> Affine:
    return tuple(sum(value[index] for value in values) for index in range(4))  # type: ignore[return-value]


def affine_value(value: Affine, Y: int, a: int, c: int) -> int:
    k, b, ca, cc = value
    return k * Y + b + ca * a + cc * c


def family_edges():
    """Full triangle + two canonical thetas + two translated P paths.

    E2_parallel has AC and BD prefixes of length one.  Put
      |A|=4Y-1, |B|=4, |C|=Y-1, |D|=4,
    and put the two port attachment pairs at distances (a,a+7) on A and
    (c,c+7) on C.
    """
    return [
        ("prefix_AC", "z0", "w_AC", (0, 1, 0, 0)),
        ("A_left", "w_AC", "r_x", (0, -1, 1, 0)),
        ("A_middle", "r_x", "s_x", (0, 7, 0, 0)),
        ("A_right", "s_x", "xprime", (4, -8, -1, 0)),
        ("C_left", "w_AC", "r_y", (0, -1, 0, 1)),
        ("C_middle", "r_y", "s_y", (0, 7, 0, 0)),
        ("C_right", "s_y", "yprime", (1, -8, 0, -1)),
        ("prefix_BD", "z0", "w_BD", (0, 1, 0, 0)),
        ("B_right", "w_BD", "xprime", (0, 3, 0, 0)),
        ("D_right", "w_BD", "yprime", (0, 3, 0, 0)),
        ("z0x", "z0", "x", (0, 1, 0, 0)),
        ("xxprime", "x", "xprime", (0, 1, 0, 0)),
        ("z0y", "z0", "y", (0, 1, 0, 0)),
        ("yyprime", "y", "yprime", (0, 1, 0, 0)),
        ("xy", "x", "y", (0, 1, 0, 0)),
        ("u_x_r_x", "u_x", "r_x", (0, 1, 0, 0)),
        ("u_x_s_x", "u_x", "s_x", (0, 1, 0, 0)),
        ("u_y_r_y", "u_y", "r_y", (0, 1, 0, 0)),
        ("u_y_s_y", "u_y", "s_y", (0, 1, 0, 0)),
    ]


def simple_cycle_edge_sets(edges):
    """Enumerate every undirected simple cycle as its edge-index set."""
    adjacency = defaultdict(list)
    for index, (_, u, v, _) in enumerate(edges):
        adjacency[u].append((v, index))
        adjacency[v].append((u, index))

    cycles = set()
    for start in sorted(adjacency):
        def visit(vertex, seen, used_edges):
            for neighbor, edge_index in adjacency[vertex]:
                if neighbor == start and len(used_edges) >= 2:
                    cycles.add(tuple(sorted((*used_edges, edge_index))))
                elif neighbor not in seen and neighbor >= start:
                    visit(neighbor, seen | {neighbor}, (*used_edges, edge_index))

        visit(start, {start}, ())
    return sorted(cycles)


def affine_form_label(form: Affine) -> str:
    k, b, ca, cc = form
    assert ca == 0 and cc == 0
    if k == 0:
        return str(b)
    suffix = "" if b == 0 else f"{b:+d}"
    return f"{k}Y{suffix}"


def symbolic_family_safe(form: Affine) -> bool:
    """Prove the reported affine bands miss powers for Y=2^j>=16."""
    k, b, ca, cc = form
    assert ca == cc == 0
    if k == 0:
        return b in {3, 6, 7, 9, 10}
    if k == 1:
        return b in {-4, -3, -2, 1, 2, 3, 6, 7, 8}
    if k == 4:
        return b in {-4, -3, -2, 1, 2, 3, 6, 7, 8}
    if k == 5:
        return b in {-11, -10, -8, -7, -6, -5, -3, -2, -1, 0, 2, 3}
    return False


def family_audit():
    edges = family_edges()
    cycles = simple_cycle_edge_sets(edges)
    assert len(cycles) == 61

    forms = []
    for cycle in cycles:
        form = affine_add(*(edges[index][3] for index in cycle))
        # Translation invariance is exact: every cycle cancels a and c.
        assert form[2:] == (0, 0)
        assert symbolic_family_safe(form), form
        forms.append(form)

    expected_bands = {
        0: {3, 6, 7, 9, 10},
        1: {-4, -3, -2, 1, 2, 3, 6, 7, 8},
        4: {-4, -3, -2, 1, 2, 3, 6, 7, 8},
        5: {-11, -10, -8, -7, -6, -5, -3, -2, -1, 0, 2, 3},
    }
    actual_bands = defaultdict(set)
    for k, b, _, _ in forms:
        actual_bands[k].add(b)
    assert dict(actual_bands) == expected_bands

    numerical_checks = 0
    spectra_by_exponent = {}
    for R in range(6, 15):
        Y = 2 ** (R - 2)
        A_length = 4 * Y - 1
        C_length = Y - 1
        positions = (
            (2, 2),
            (A_length // 2, C_length // 2),
            (A_length - 8, C_length - 8),
        )
        spectra = set()
        for a, c in positions:
            lengths = tuple(sorted(affine_value(form, Y, a, c) for form in forms))
            assert not any(is_power_of_two(length) for length in lengths)
            spectra.add(lengths)
            numerical_checks += len(lengths)
        assert len(spectra) == 1
        spectra_by_exponent[str(R)] = {
            "Y": Y,
            "A_attachment_positions": [2, A_length // 2, A_length - 8],
            "C_attachment_positions": [2, C_length // 2, C_length - 8],
            "minimum_cycle": min(next(iter(spectra))),
            "maximum_cycle": max(next(iter(spectra))),
        }

    # The one-port family is an edge-deletion subgraph of this clean core.
    one_port_edges = [edge for edge in edges if not edge[0].startswith("u_y_")]
    one_port_cycles = simple_cycle_edge_sets(one_port_edges)
    assert len(one_port_cycles) == 40

    return {
        "simple_cycles_two_port_core": len(cycles),
        "simple_cycles_one_port_core": len(one_port_cycles),
        "distinct_affine_cycle_forms": len(set(forms)),
        "affine_form_multiplicities": dict(sorted(Counter(affine_form_label(form) for form in forms).items())),
        "affine_bands": {str(k): sorted(values) for k, values in expected_bands.items()},
        "numerical_cycle_values_checked": numerical_checks,
        "spectra_by_exponent": spectra_by_exponent,
    }


def route_audit():
    M, N = 31, 8
    same_a = same_branch_routes(M, N, 5, 12)
    same_b = same_branch_routes(N, M, 2, 6)
    different = different_branch_routes(M, N, 5, 3)
    q_to_a = far_pole_routes(M, N, 5)
    p_to_yprime = near_pole_routes_avoiding_y(M, N, 5)
    x_to_yprime = center_routes_avoiding_y(M, N, 5)

    assert same_a == (7, 26, 27, 32)
    assert same_b == (4, 6, 7, 35)
    assert different == (8, 31, 12, 31, 13, 32)
    assert q_to_a == (26, 7, 8, 13)
    assert p_to_yprime == (5, 28, 34)
    assert x_to_yprime == (6, 27, 14, 35)

    # The translated family uses separation seven on the two near-power paths.
    for R in range(6, 15):
        Y = 2 ** (R - 2)
        routes_x = same_branch_routes(4 * Y - 1, 4, 2, 9)
        routes_y = same_branch_routes(Y - 1, 4, 2, 9)
        assert not any(is_forbidden_port_route(route) for route in (*routes_x, *routes_y))

    return {
        "same_A_example": same_a,
        "same_B_example": same_b,
        "different_AB_example": different,
        "far_pole_to_A_example": q_to_a,
        "z0_to_yprime_example_avoiding_port_y": p_to_yprime,
        "x_to_yprime_example_avoiding_port_y": x_to_yprime,
        "translated_family_route_checks": 18,
    }


def main():
    routes = route_audit()
    family = family_audit()
    same_pair_distinct_ports_cycle = 4
    assert is_power_of_two(same_pair_distinct_ports_cycle)

    location_classes = [
        "two internal points on A",
        "two internal points on B",
        "one internal point on each of A and B",
        "xprime with one internal branch point",
        "z0 with x (the fixed triangle port y)",
        "z0 with yprime lying on A or B (port forced to y)",
        "x with yprime lying on A or B (port forced to y)",
        "two theta poles (degree-four adjacency impossible; abstractly exposes C4)",
    ]

    output = {
        "assertion_failures": 0,
        "scope": (
            "degree-four E2 port-location arithmetic and full displayed rooted incidence cores; "
            "not an MA2-leaf completion, SAT model, or graph-realizability certificate"
        ),
        "location_classes": location_classes,
        "route_audit": routes,
        "degree_four_rules": {
            "port_u_on_relevant_theta": False,
            "port_u_can_be_first_neighbor_or_shared_prefix_vertex": False,
            "z0_or_x_as_attachment_forces_port_u": "y (symmetrically x for the y-theta)",
            "immediate_split_first_neighbor_can_be_attachment": False,
            "continued_prefix_first_neighbor_spare_incidence": 1,
            "later_prefix_vertex_degree": "not determined by M1",
        },
        "simultaneous_ports": {
            "same_attachment_pair_distinct_ports": {
                "status": "CONTRADICTION",
                "cycle_length": same_pair_distinct_ports_cycle,
            },
            "same_port_same_pair": "one literal port path",
            "same_port_pairs_share_one_attachment": "port degree at least 4 including its leaf incidence",
            "same_port_disjoint_pairs": "port degree at least 5 including its leaf incidence",
        },
        "infinite_E2_parallel_two_port_family": family,
        "result": "EXPLICIT INFINITE PORT RESIDUAL",
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
