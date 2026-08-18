#!/usr/bin/env python3
"""Finite checks for the exact-two-attachment Type-T A bottleneck.

This checker distinguishes the actual triangle-anchored geometry from an
abstract pole-to-pole A template.  In the actual geometry the known length-2
path lies in the central bridge and shares the forced gateway edge xY with
every other bridge path.  It therefore does not close an admissible path to a
cycle of length ell+2.  The guaranteed cycles instead have lengths ell and
ell+1 (and the corresponding delta-shifted values), plus the two routes
through the other nontrivial bridge at the same 2-cut.

The script checks finite incidence mechanics and arithmetic only.  It is not
proof-assistant verification and does not construct a minimal counterexample.
"""

from __future__ import annotations

import json

import networkx as nx


BALABAN_10_CAGE_LCF = [
    -9, -25, -19, 29, 13, 35, -13, -29, 19, 25, 9, -29, 29, 17,
    33, 21, 9, -13, -31, -9, 25, 17, 9, -31, 27, -9, 17, -19,
    -29, 27, -17, -9, -29, 33, -25, 25, -21, 17, -17, 29, 35,
    -29, 17, -17, 21, -25, 25, -33, 29, 9, 17, -27, 29, 19,
    -17, 9, -27, 31, -9, -17, -25, 9, 31, 13, -9, -21, -33,
    -17, -29, 29,
]


def is_forbidden_power(n: int) -> bool:
    return n >= 4 and n & (n - 1) == 0


def add_named_path(
    graph: nx.Graph, start: str, end: str, length: int, prefix: str
) -> list[str]:
    assert length >= 1
    internal = [f"{prefix}_{i}" for i in range(length - 1)]
    path = [start, *internal, end]
    graph.add_edges_from(zip(path, path[1:]))
    return path


def verify_cycle(graph: nx.Graph, vertices: list[str]) -> bool:
    return (
        len(vertices) >= 3
        and len(vertices) == len(set(vertices))
        and all(
            graph.has_edge(vertices[i], vertices[(i + 1) % len(vertices)])
            for i in range(len(vertices))
        )
    )


def guaranteed_cycle_table(ell: int, delta: int, rho: int, s: int) -> dict:
    assert ell >= 5 and delta in (1, 2) and rho >= 2 and s >= 2
    return {
        "inside_K_suffix_plus_YX": [ell, ell + delta],
        "trivial_edge_xX": [ell + 1, ell + delta + 1],
        "other_bridge_near_power_route": [
            ell + 2**rho,
            ell + delta + 2**rho,
        ],
        "other_bridge_power_route": [
            ell + 2**s + 1,
            ell + delta + 2**s + 1,
        ],
        "isolated_length_two_path": [3, 2 + 2**rho, 2**s + 3],
    }


def symbolic_arithmetic_check() -> dict:
    offsets_checked = ["0", "1", "2^rho", "2^s+1"]
    direct_formula_agreement = 0

    for delta in (1, 2):
        for rho in range(2, 8):
            for s in range(2, 8):
                offsets = (0, 1, 2**rho, 2**s + 1)
                forbidden_by_formula = {
                    value
                    for exponent in range(2, 13)
                    for offset in offsets
                    for value in (
                        2**exponent - offset,
                        2**exponent - offset - delta,
                    )
                    if 5 <= value <= 512
                }
                forbidden_direct = {
                    ell
                    for ell in range(5, 513)
                    if any(
                        is_forbidden_power(length)
                        for name, lengths in guaranteed_cycle_table(
                            ell, delta, rho, s
                        ).items()
                        if name != "isolated_length_two_path"
                        for length in lengths
                    )
                }
                assert forbidden_by_formula == forbidden_direct
                direct_formula_agreement += 1

                # An explicit infinite family: once t exceeds all fixed theta
                # exponents, ell=2^t+1 leaves every guaranteed length strictly
                # between or with at least two nonzero binary digits relative
                # to adjacent powers of two.
                t = max(rho, s, 3) + 1
                ell = 2**t + 1
                table = guaranteed_cycle_table(ell, delta, rho, s)
                assert not any(
                    is_forbidden_power(length)
                    for lengths in table.values()
                    for length in lengths
                )
                admissible_pair = (ell, ell + delta)
                assert not any(
                    is_forbidden_power(a + b)
                    for a in admissible_pair
                    for b in admissible_pair
                )

    return {
        "delta_values": [1, 2],
        "offsets_checked": offsets_checked,
        "finite_parameter_rows": direct_formula_agreement,
        "exact_forbidden_form": "ell = 2^k-d or 2^k-d-delta",
        "infinite_safe_family": "ell=2^t+1, t>max(rho,s,3)",
        "infinite_family_pair_self_sum_clean": True,
        "arithmetic_alone_contradiction": False,
    }


def abstract_pole_model_check() -> dict:
    """Check the pole-to-pole model stated in the continuation request.

    This is the generic A template of contraction_leaf_blocks.md Case 3, not
    the actual triangle-gateway specialization.  Its outside theta offsets are
    2, 2^rho-1, 2^s, and optionally the pole edge 1.
    """
    rows = 0
    for delta in (1, 2):
        for rho in range(2, 8):
            for s in range(2, 8):
                t = max(rho, s, 2) + 1
                ell = 2**t
                offsets = (1, 2, 2**rho - 1, 2**s)
                lengths = [
                    ell + offset + shift
                    for offset in offsets
                    for shift in (0, delta)
                ]
                assert not any(is_forbidden_power(length) for length in lengths)
                rows += 1
    return {
        "outside_theta_offsets": ["1 (if pole edge)", "2", "2^rho-1", "2^s"],
        "guaranteed_pair_for_each_offset": ["ell+d", "ell+delta+d"],
        "infinite_safe_family": "ell=2^t, t>max(rho,s,2)",
        "finite_parameter_rows": rows,
        "arithmetic_alone_contradiction": False,
        "is_actual_triangle_gateway_model": False,
    }


def actual_gateway_realization_check(
    ell: int = 9, delta: int = 2, rho: int = 3, s: int = 4
) -> dict:
    graph = nx.Graph()
    graph.add_edges_from((("x", "Y"), ("Y", "X"), ("x", "X")))

    p1_suffix = add_named_path(graph, "Y", "X", ell - 1, "p1")
    p2_suffix = add_named_path(graph, "Y", "X", ell + delta - 1, "p2")
    p1 = ["x", *p1_suffix]
    p2 = ["x", *p2_suffix]
    short_path = ["x", "Y", "X"]

    near_route = add_named_path(graph, "x", "X", 2**rho, "near")
    power_route = add_named_path(graph, "x", "X", 2**s + 1, "power")

    short_edges = {
        frozenset((a, b)) for a, b in zip(short_path, short_path[1:])
    }
    for path in (p1, p2):
        path_edges = {frozenset((a, b)) for a, b in zip(path, path[1:])}
        assert short_edges & path_edges == {frozenset(("x", "Y"))}
        assert set(short_path[1:-1]) & set(path[1:-1]) == {"Y"}

    table = guaranteed_cycle_table(ell, delta, rho, s)
    explicit_cycles = {
        "inside_K_suffix_plus_YX": [
            p1_suffix,
            p2_suffix,
        ],
        "trivial_edge_xX": [p1, p2],
        "other_bridge_near_power_route": [
            p1 + list(reversed(near_route))[1:-1],
            p2 + list(reversed(near_route))[1:-1],
        ],
        "other_bridge_power_route": [
            p1 + list(reversed(power_route))[1:-1],
            p2 + list(reversed(power_route))[1:-1],
        ],
    }

    observed = {}
    for name, cycles in explicit_cycles.items():
        assert all(verify_cycle(graph, cycle) for cycle in cycles)
        observed[name] = [len(cycle) for cycle in cycles]
        assert observed[name] == table[name]

    assert not verify_cycle(graph, short_path + p1[1:-1])

    return {
        "parameters": {"ell": ell, "delta": delta, "rho": rho, "s": s},
        "short_path": short_path,
        "short_path_shares_gateway_edge_with_each_admissible_path": True,
        "requested_ell_plus_two_closure_is_guaranteed": False,
        "verified_cycle_lengths": observed,
    }


def heawood_hypothesis_check() -> dict:
    bridge = nx.heawood_graph()
    bridge.remove_edge(0, 1)
    bridge.add_edges_from(((0, "Y"), ("Y", 1), ("x", "Y")))
    closure = bridge.copy()
    closure.add_edge("x", 0)

    path_lengths = sorted(
        {len(path) - 1 for path in nx.all_simple_paths(bridge, "x", 0)}
    )
    cycle_lengths = sorted({len(cycle) for cycle in nx.simple_cycles(bridge)})
    edge_cross_failures = [
        [length, length + 1]
        for length in path_lengths
        if is_forbidden_power(length + 1)
    ]
    self_power_sums = sorted(
        {
            a + b
            for a in path_lengths
            for b in path_lengths
            if is_forbidden_power(a + b)
        }
    )

    assert nx.is_biconnected(closure)
    assert min(bridge.degree(v) for v in bridge if v not in {"x", 0}) == 3
    assert path_lengths == [2, 7, 9, 11, 13, 15]
    assert cycle_lengths == [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    assert edge_cross_failures == [[7, 8], [15, 16]]
    assert self_power_sums == [4, 16]

    return {
        "internal_min_degree": 3,
        "closure_biconnected": True,
        "terminal_degrees_in_K": [bridge.degree("x"), bridge.degree(0)],
        "terminal_path_lengths": path_lengths,
        "internal_cycle_lengths": cycle_lengths,
        "internal_power_cycle_clean": False,
        "trivial_edge_cross_failures": edge_cross_failures,
        "self_power_sums": self_power_sums,
        "actual_type_t_f_clean": False,
    }


def balaban_local_counterexample_check() -> dict:
    host = nx.LCF_graph(70, BALABAN_10_CAGE_LCF, 1)
    assert host.number_of_nodes() == 70
    assert host.number_of_edges() == 105
    assert set(dict(host.degree()).values()) == {3}
    assert nx.girth(host) == 10

    bridge = host.copy()
    bridge.remove_edge(0, 1)
    bridge.add_edges_from(((0, "Y"), ("Y", 1), ("x", "Y")))
    closure = bridge.copy()
    closure.add_edge("x", 0)

    short_path_lengths = sorted(
        {
            len(path) - 1
            for path in nx.all_simple_paths(bridge, "x", 0, cutoff=14)
        }
    )
    admissible_pairs = [
        [a, b]
        for i, a in enumerate(short_path_lengths)
        for b in short_path_lengths[i + 1 :]
        if b - a in (1, 2)
    ]
    cycle_16 = next(
        cycle
        for cycle in nx.simple_cycles(bridge, length_bound=16)
        if len(cycle) == 16
    )

    assert nx.girth(bridge) == 10
    assert nx.is_biconnected(closure)
    assert min(bridge.degree(v) for v in bridge if v not in {"x", 0}) == 3
    assert short_path_lengths == [2, 11, 13]
    assert admissible_pairs == [[11, 13]]
    assert len(cycle_16) == 16

    return {
        "host_order": 70,
        "host_size": 105,
        "host_cubic": True,
        "bridge_girth": 10,
        "closure_biconnected": True,
        "internal_min_degree": 3,
        "terminal_path_lengths_through_14": short_path_lengths,
        "admissible_pairs_through_14": admissible_pairs,
        "shortest_path_belongs_to_admissible_pair": False,
        "contains_c4_or_c8": False,
        "contains_c16": True,
        "full_power_cycle_clean": False,
    }


def build_serial_cells(arc_pairs: list[tuple[int, int]]) -> nx.Graph:
    graph = nx.Graph()
    junctions = [f"j{i}" for i in range(len(arc_pairs) + 1)]
    for index, (first, second) in enumerate(arc_pairs):
        add_named_path(
            graph, junctions[index], junctions[index + 1], first, f"a{index}"
        )
        add_named_path(
            graph, junctions[index], junctions[index + 1], second, f"b{index}"
        )
    return graph


def overlap_cell_check() -> dict:
    cases = {
        1: [(2, 5), (4, 2)],
        2: [(1, 5), (4, 2)],
    }
    result = {}
    for delta, arc_pairs in cases.items():
        first_length = sum(pair[0] for pair in arc_pairs)
        second_length = sum(pair[1] for pair in arc_pairs)
        signed_differences = [b - a for a, b in arc_pairs]
        graph = build_serial_cells(arc_pairs)
        cycle_lengths = sorted({len(cycle) for cycle in nx.simple_cycles(graph)})

        assert second_length - first_length == delta
        assert sum(signed_differences) == delta
        assert cycle_lengths == sorted({a + b for a, b in arc_pairs})
        assert 4 not in cycle_lengths and 8 not in cycle_lengths

        result[str(delta)] = {
            "path_lengths": [first_length, second_length],
            "cell_arc_pairs": [list(pair) for pair in arc_pairs],
            "cell_signed_differences": signed_differences,
            "cell_cycle_lengths": cycle_lengths,
            "forces_c4_or_c8_from_delta_alone": False,
            "scope": "path-incidence counterexample; internal degrees are not 3",
        }
    return result


def main() -> int:
    result = {
        "actual_gateway_realization": actual_gateway_realization_check(),
        "symbolic_arithmetic": symbolic_arithmetic_check(),
        "abstract_pole_model": abstract_pole_model_check(),
        "heawood_hypothesis_table": heawood_hypothesis_check(),
        "balaban_local_counterexample": balaban_local_counterexample_check(),
        "overlap_cells": overlap_cell_check(),
        "assertion_failures": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
