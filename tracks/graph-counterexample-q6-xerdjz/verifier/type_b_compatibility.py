#!/usr/bin/env python3
"""Independent finite checks for the global Type-B compatibility audit.

The universal cycle decomposition, arithmetic family, and T9B theorem are
proved in ``type_b_compatibility.md``.  This script checks their finite
mechanics on explicit graphs, exhaustively regresses bounded parameter boxes,
and verifies the recorded Balaban C16 witness.  It is not a proof-assistant
formalization, an all-orders bridge search, or a realizability certificate for
the infinite forced-core spectra.
"""

from __future__ import annotations

import json
from itertools import combinations

import networkx as nx

try:
    from verifier.type_t_exact_two_a import BALABAN_10_CAGE_LCF
except ModuleNotFoundError:  # Direct execution from the repository root.
    from type_t_exact_two_a import BALABAN_10_CAGE_LCF


def is_forbidden_power(value: int) -> bool:
    return value >= 4 and value & (value - 1) == 0


def edge_key(left: object, right: object) -> frozenset[object]:
    return frozenset((left, right))


def path_edges(path: list[object]) -> set[frozenset[object]]:
    return {edge_key(left, right) for left, right in zip(path, path[1:])}


def cycle_edges(cycle: list[object]) -> set[frozenset[object]]:
    return {
        edge_key(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    }


def add_path(
    graph: nx.Graph,
    start: str,
    end: str,
    length: int,
    prefix: str,
    owner: str,
    owners: dict[frozenset[object], str],
) -> list[str]:
    internal = [f"{prefix}_{index}" for index in range(length - 1)]
    path = [start, *internal, end]
    for left, right in zip(path, path[1:]):
        graph.add_edge(left, right)
        key = edge_key(left, right)
        assert key not in owners
        owners[key] = owner
    return path


def parallel_bridge(
    graph: nx.Graph,
    lengths: list[int],
    prefix: str,
    owner: str,
    owners: dict[frozenset[object], str],
) -> list[list[str]]:
    return [
        add_path(graph, "x", "y", length, f"{prefix}{index}", owner, owners)
        for index, length in enumerate(lengths)
    ]


def simple_cycle_lengths(graph: nx.Graph) -> set[int]:
    return {len(cycle) for cycle in nx.simple_cycles(graph)}


def terminal_spectrum(graph: nx.Graph) -> set[int]:
    if "x" not in graph or "y" not in graph or not nx.has_path(graph, "x", "y"):
        return set()
    return {len(path) - 1 for path in nx.all_simple_paths(graph, "x", "y")}


def cycle_decomposition_check() -> dict:
    graph = nx.Graph()
    owners: dict[frozenset[object], str] = {}
    lambda_1 = [2, 5, 7]
    lambda_2 = [4, 6, 9]
    paths_1 = parallel_bridge(graph, lambda_1, "a", "B1", owners)
    paths_2 = parallel_bridge(graph, lambda_2, "b", "B2", owners)
    graph.add_edge("x", "y")
    owners[edge_key("x", "y")] = "E"

    categories: dict[str, set[int]] = {
        "internal_B1": set(),
        "internal_B2": set(),
        "edge_plus_B1": set(),
        "edge_plus_B2": set(),
        "cross_B1_B2": set(),
    }
    owner_to_category = {
        frozenset(("B1",)): "internal_B1",
        frozenset(("B2",)): "internal_B2",
        frozenset(("E", "B1")): "edge_plus_B1",
        frozenset(("E", "B2")): "edge_plus_B2",
        frozenset(("B1", "B2")): "cross_B1_B2",
    }

    cycle_count = 0
    for cycle in nx.simple_cycles(graph):
        support = frozenset(owners[edge] for edge in cycle_edges(cycle))
        assert support in owner_to_category
        categories[owner_to_category[support]].add(len(cycle))
        cycle_count += 1

    expected = {
        "internal_B1": {a + b for a, b in combinations(lambda_1, 2)},
        "internal_B2": {a + b for a, b in combinations(lambda_2, 2)},
        "edge_plus_B1": {1 + value for value in lambda_1},
        "edge_plus_B2": {1 + value for value in lambda_2},
        "cross_B1_B2": {a + b for a in lambda_1 for b in lambda_2},
    }
    assert categories == expected

    # Deletion cannot add an internal cycle or a terminal path.
    bridge_1 = graph.edge_subgraph(
        edge for path in paths_1 for edge in zip(path, path[1:])
    ).copy()
    original_paths = terminal_spectrum(bridge_1)
    original_cycles = simple_cycle_lengths(bridge_1)
    deletion_rows = 0
    for edge in list(bridge_1.edges()):
        reduced = bridge_1.copy()
        reduced.remove_edge(*edge)
        assert terminal_spectrum(reduced) <= original_paths
        assert simple_cycle_lengths(reduced) <= original_cycles
        deletion_rows += 1

    return {
        "fixture_terminal_spectra": [lambda_1, lambda_2],
        "cycle_count": cycle_count,
        "category_lengths": {
            key: sorted(values) for key, values in sorted(categories.items())
        },
        "all_cycles_have_exactly_one_support_category": True,
        "edge_deletions_checked_for_monotonicity": deletion_rows,
    }


def add_shared_gateway_bridge(
    graph: nx.Graph,
    gateway: str,
    suffix_lengths: list[int],
    prefix: str,
) -> list[list[str]]:
    graph.add_edge("x", gateway)
    paths = []
    for index, suffix_length in enumerate(suffix_lengths):
        internal = [f"{prefix}{index}_{j}" for j in range(suffix_length - 1)]
        suffix = [gateway, *internal, "y"]
        graph.add_edges_from(zip(suffix, suffix[1:]))
        paths.append(["x", *suffix])
    return paths


def triangle_gateway_mapping_check() -> dict:
    ell, delta, rho, s, m, epsilon = 7, 2, 2, 3, 11, 1
    bridge_1 = nx.Graph()
    paths_1 = add_shared_gateway_bridge(
        bridge_1, "Y", [1, ell - 1, ell + delta - 1], "a"
    )
    bridge_2 = nx.Graph()
    paths_2 = add_shared_gateway_bridge(
        bridge_2,
        "xp",
        [2**rho - 1, 2**s, m - 1, m + epsilon - 1],
        "b",
    )

    spectrum_1 = terminal_spectrum(bridge_1)
    spectrum_2 = terminal_spectrum(bridge_2)
    expected_1 = {2, ell, ell + delta}
    expected_2 = {2**rho, 2**s + 1, m, m + epsilon}
    assert spectrum_1 == expected_1
    assert spectrum_2 == expected_2
    assert 2 not in spectrum_2

    forced_edge_1 = edge_key("x", "Y")
    forced_edge_2 = edge_key("x", "xp")
    assert all(forced_edge_1 in path_edges(path) for path in paths_1)
    assert all(forced_edge_2 in path_edges(path) for path in paths_2)
    assert all(forced_edge_1 not in path_edges(path) for path in paths_2)

    edge_plus = {1 + value for value in spectrum_1 | spectrum_2}
    cross = {left + right for left in spectrum_1 for right in spectrum_2}
    theta_internal_cycle = 2**rho + 2**s - 1
    assert theta_internal_cycle in simple_cycle_lengths(bridge_2)
    return {
        "parameters": {
            "ell": ell,
            "delta": delta,
            "rho": rho,
            "s": s,
            "m": m,
            "epsilon": epsilon,
        },
        "spectrum_1": sorted(spectrum_1),
        "spectrum_2": sorted(spectrum_2),
        "known_length_two_bridge": "B1 only",
        "B1_paths_share_xY": True,
        "B2_paths_share_xxp": True,
        "edge_plus_lengths": sorted(edge_plus),
        "cross_lengths": sorted(cross),
        "theta_internal_cycle_length": theta_internal_cycle,
    }


def paired_core(
    rho: int,
    s: int,
    t: int,
    u: int,
    delta: int,
    epsilon: int,
) -> tuple[set[int], set[int]]:
    ell = 2**t + 1
    m = 2**u + 1
    return (
        {2, ell, ell + delta},
        {2**rho, 2**s + 1, m, m + epsilon},
    )


def paired_arithmetic_check() -> dict:
    patterns = {
        "1,1": [0, 1, 1, 2],
        "1,2": [0, 1, 2, 3],
        "2,1": [0, 1, 2, 3],
        "2,2": [0, 2, 2, 4],
    }
    observed_exceptions: dict[str, list[list[int]]] = {
        str(offset): [] for offset in range(5)
    }
    for t in range(1, 13):
        for u in range(1, 13):
            for offset in range(5):
                if is_forbidden_power(2**t + 2**u + 2 + offset):
                    observed_exceptions[str(offset)].append([t, u])
    expected_exceptions = {
        "0": [[1, 2], [2, 1]],
        "1": [],
        "2": [[1, 1], [2, 3], [3, 2]],
        "3": [],
        "4": [[1, 3], [3, 1]],
    }
    assert observed_exceptions == expected_exceptions

    parameter_rows = 0
    values_checked = 0
    for rho in range(2, 7):
        for s in range(2, 7):
            minimum = max(rho, s, 3) + 1
            for t in range(minimum, minimum + 4):
                for u in range(minimum, minimum + 4):
                    for delta in (1, 2):
                        for epsilon in (1, 2):
                            first, second = paired_core(
                                rho, s, t, u, delta, epsilon
                            )
                            ell, m = 2**t + 1, 2**u + 1
                            internal_forced = {
                                ell,
                                ell + delta,
                                2**rho + 2**s - 1,
                            }
                            forced = (
                                internal_forced
                                | {1 + value for value in first}
                                | {1 + value for value in second}
                                | {a + b for a in first for b in second}
                            )
                            assert not any(is_forbidden_power(v) for v in forced)
                            parameter_rows += 1
                            values_checked += len(forced)

                            offsets = sorted(
                                [0, epsilon, delta, delta + epsilon]
                            )
                            assert offsets == patterns[f"{delta},{epsilon}"]
                            assert not any(
                                is_forbidden_power(ell + m + offset)
                                for offset in offsets
                            )

    return {
        "delta_epsilon_patterns": patterns,
        "exact_small_exponent_power_exceptions": expected_exceptions,
        "exception_classification_rows_checked": 12 * 12 * 5,
        "finite_parameter_rows": parameter_rows,
        "forced_values_checked": values_checked,
        "infinite_family": (
            "ell=2^t+1, m=2^u+1, "
            "t,u>max(rho,s,3), delta,epsilon in {1,2}"
        ),
        "all_finite_regressions_forced_table_clean": True,
        "scope": "forced spectrum cores only; no bridge realizability claim",
    }


def balaban_diagnostic_check() -> dict:
    host = nx.LCF_graph(70, BALABAN_10_CAGE_LCF, 1)
    assert nx.node_connectivity(host) == 3

    bridge = host.copy()
    bridge.remove_edge(0, 1)
    bridge.add_edges_from(((0, "Y"), ("Y", 1), ("x", "Y")))

    path_11 = ["x", "Y", 1, 2, 3, 4, 5, 6, 63, 62, 61, 0]
    path_13 = ["x", "Y", 1, 2, 3, 4, 5, 6, 7, 8, 27, 28, 69, 0]
    witness_16 = [0, 69, 28, 27, 8, 7, 6, 5, 4, 3, 32, 31, 22, 23, 62, 61]

    for path, length in ((path_11, 11), (path_13, 13)):
        assert len(path) - 1 == length
        assert len(path) == len(set(path))
        assert all(bridge.has_edge(a, b) for a, b in zip(path, path[1:]))
    assert len(witness_16) == len(set(witness_16)) == 16
    assert all(
        bridge.has_edge(witness_16[i], witness_16[(i + 1) % 16])
        for i in range(16)
    )
    assert not {"x", "Y"} & set(witness_16)

    witness_edges = cycle_edges(witness_16)
    intersections = {
        "11": {
            "common_edges": len(path_edges(path_11) & witness_edges),
            "common_vertices": len(set(path_11) & set(witness_16)),
        },
        "13": {
            "common_edges": len(path_edges(path_13) & witness_edges),
            "common_vertices": len(set(path_13) & set(witness_16)),
        },
    }
    assert intersections["11"]["common_edges"] == 5
    assert intersections["13"]["common_edges"] == 9

    terminals = {"x", 0}
    assert all(
        "x" in edge
        or any(vertex not in terminals and bridge.degree(vertex) == 3 for vertex in edge)
        for edge in bridge.edges()
    )

    return {
        "host_vertex_connectivity": 3,
        "admissible_paths": {"11": path_11, "13": path_13},
        "c16_witness": witness_16,
        "c16_avoids_gateway_vertices": True,
        "c16_location": "Balaban rigid core",
        "path_intersections": intersections,
        "t9b_degree_incidence_violations": 0,
        "fixture_failure": "internal C16",
    }


def main() -> int:
    result = {
        "cycle_decomposition": cycle_decomposition_check(),
        "triangle_gateway_mapping": triangle_gateway_mapping_check(),
        "paired_arithmetic": paired_arithmetic_check(),
        "balaban_diagnostic": balaban_diagnostic_check(),
        "assertion_failures": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
