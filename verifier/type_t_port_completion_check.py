#!/usr/bin/env python3
"""Independent checks for the expanded Type-T port core and completions."""

from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path

from type_t_port_core_export import PortCore, build_core, graph_encodings, to_networkx


def is_power_of_two_cycle(length: int) -> bool:
    return length >= 4 and length & (length - 1) == 0


def connected(adjacency: tuple[frozenset[int], ...]) -> bool:
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == len(adjacency)


def all_undirected_cycles(adjacency: tuple[frozenset[int], ...]):
    """Enumerate each undirected simple cycle once, from its least vertex."""
    cycles: list[tuple[int, ...]] = []
    for start in range(len(adjacency)):
        path = [start]
        used = {start}

        def visit(vertex: int) -> None:
            for neighbor in adjacency[vertex]:
                if neighbor == start:
                    if len(path) >= 3 and path[1] < path[-1]:
                        cycles.append(tuple(path))
                elif neighbor > start and neighbor not in used:
                    used.add(neighbor)
                    path.append(neighbor)
                    visit(neighbor)
                    path.pop()
                    used.remove(neighbor)

        visit(start)
    return cycles


def find_cycle_exact(adjacency: tuple[frozenset[int], ...], length: int):
    """First exact-length cycle from a least-vertex rooted DFS."""
    for start in range(len(adjacency)):
        path = [start]
        used = {start}

        def visit(vertex: int):
            if len(path) == length:
                return tuple(path) if start in adjacency[vertex] else None
            for neighbor in adjacency[vertex]:
                if neighbor <= start or neighbor in used:
                    continue
                used.add(neighbor)
                path.append(neighbor)
                result = visit(neighbor)
                if result is not None:
                    return result
                path.pop()
                used.remove(neighbor)
            return None

        result = visit(start)
        if result is not None:
            return result
    return None


def find_cycle_networkx(core: PortCore, matching: list[tuple[int, int]], length: int):
    import networkx as nx

    graph = to_networkx(core, matching)
    for cycle in nx.simple_cycles(graph, length_bound=length):
        if len(cycle) == length:
            return tuple(cycle)
    return None


def concatenate(*paths: tuple[int, ...]) -> tuple[int, ...]:
    result: list[int] = []
    for path in paths:
        if result and result[-1] != path[0]:
            raise AssertionError("named paths do not concatenate")
        result.extend(path if not result else path[1:])
    return tuple(result)


def audit_core(core: PortCore) -> dict:
    Y = core.Y
    adjacency = core.adjacency()
    names = core.label_to_vertex
    degrees = Counter(map(len, adjacency))

    assert core.order == 5 * Y + 7
    assert core.size == 5 * Y + 13
    assert core.size - core.order + 1 == 7
    assert connected(adjacency)
    assert all(u != v for u, v in core.edges)
    assert len(core.edges) == len(set(core.edges))

    A = concatenate(core.paths["prefix_AC"], core.paths["A_left"],
                    core.paths["A_middle"], core.paths["A_right"])
    C = concatenate(core.paths["prefix_AC"], core.paths["C_left"],
                    core.paths["C_middle"], core.paths["C_right"])
    B = concatenate(core.paths["prefix_BD"], core.paths["B_right"])
    D = concatenate(core.paths["prefix_BD"], core.paths["D_right"])
    assert (len(A) - 1, len(B) - 1, len(C) - 1, len(D) - 1) == (
        4 * Y - 1, 4, Y - 1, 4,
    )
    assert A[:2] == C[:2] and set(A[2:]).isdisjoint(C[2:])
    assert B[:2] == D[:2] and set(B[2:]).isdisjoint(D[2:])
    assert set(A[1:-1]).isdisjoint(B[1:-1])
    assert set(C[1:-1]).isdisjoint(D[1:-1])

    assert adjacency[names["u_x"]] == frozenset((names["r_x"], names["s_x"]))
    assert adjacency[names["u_y"]] == frozenset((names["r_y"], names["s_y"]))
    assert len(core.paths["A_middle"]) - 1 == 7
    assert len(core.paths["C_middle"]) - 1 == 7

    expected_degree_three = {
        "x", "xprime", "y", "yprime", "w_AC", "w_BD",
        "r_x", "s_x", "r_y", "s_y",
    }
    assert len(adjacency[names["z0"]]) == 4
    assert all(len(adjacency[names[name]]) == 3 for name in expected_degree_three)
    deficient = core.deficient_vertices()
    assert len(deficient) == 5 * Y - 4
    assert len(deficient) % 2 == 0
    assert degrees == Counter({2: 5 * Y - 4, 3: 10, 4: 1})

    cycles = all_undirected_cycles(adjacency)
    spectrum = Counter(map(len, cycles))
    assert len(cycles) == 61
    assert not any(is_power_of_two_cycle(length) for length in spectrum)

    return {
        "j": core.j,
        "Y": Y,
        "a": core.a,
        "c": core.c,
        "order": core.order,
        "size": core.size,
        "cycle_rank": core.size - core.order + 1,
        "degree_counts": {str(degree): count for degree, count in sorted(degrees.items())},
        "deficient_vertices": len(deficient),
        "matching_edges_required": len(deficient) // 2,
        "simple_cycles": len(cycles),
        "cycle_spectrum_multiplicity": {
            str(length): count for length, count in sorted(spectrum.items())
        },
        "power_cycle_lengths": [
            length for length in spectrum if is_power_of_two_cycle(length)
        ],
    }


def phase0_audit() -> dict:
    records = []
    for j in (4, 5, 6):
        Y = 1 << j
        a_values = (2, (4 * Y - 7) // 2, 4 * Y - 9)
        c_values = (2, (Y - 7) // 2, Y - 9)
        for a in a_values:
            for c in c_values:
                records.append(audit_core(build_core(j, a, c)))
    reference_spectra = {}
    for j in (4, 5, 6):
        spectra = {
            json.dumps(record["cycle_spectrum_multiplicity"], sort_keys=True)
            for record in records if record["j"] == j
        }
        assert len(spectra) == 1
        reference_spectra[str(j)] = next(
            record["cycle_spectrum_multiplicity"] for record in records
            if record["j"] == j
        )
    return {
        "status": "PASS",
        "instances_checked": len(records),
        "formulas": {
            "order": "5*2^j+7",
            "size": "5*2^j+13",
            "cycle_rank": 7,
            "deficient_vertices": "5*2^j-4",
            "matching_edges_required": "(5*2^j-4)/2",
        },
        "reference_spectra": reference_spectra,
        "instances": records,
    }


def audit_completion(path: Path, second_detector: bool = True) -> dict:
    import networkx as nx

    payload = json.loads(path.read_text())
    parameters = payload["parameters"]
    core = build_core(parameters["j"], parameters["a"], parameters["c"])
    matching = [tuple(sorted(edge)) for edge in payload["matching_edges"]]
    deficient = set(core.deficient_vertices())
    endpoints = [vertex for edge in matching for vertex in edge]
    assert len(matching) == len(deficient) // 2
    assert len(endpoints) == len(set(endpoints)) == len(deficient)
    assert set(endpoints) == deficient
    assert not set(matching) & set(core.edges)

    graph = to_networkx(core, matching)
    assert not graph.is_multigraph()
    assert graph.number_of_nodes() == core.order
    assert graph.number_of_edges() == core.size + len(matching)
    assert min(dict(graph.degree()).values()) >= 3
    assert nx.is_connected(graph)

    adjacency = tuple(frozenset(graph.neighbors(v)) for v in range(core.order))
    witnesses = {}
    agreement = {}
    power = 4
    while power <= core.order:
        first = find_cycle_exact(adjacency, power)
        second = find_cycle_networkx(core, matching, power) if second_detector else None
        if second_detector:
            assert (first is None) == (second is None)
        agreement[str(power)] = first is not None
        if first is not None:
            witnesses[str(power)] = list(first)
        power *= 2

    encodings = graph_encodings(core, matching)
    if "graph6" in payload:
        assert payload["graph6"] == encodings["graph6"]
    if "sparse6" in payload:
        assert payload["sparse6"] == encodings["sparse6"]
    return {
        "status": "PASS",
        "parameters": parameters,
        "order": core.order,
        "size": graph.number_of_edges(),
        "minimum_degree": min(dict(graph.degree()).values()),
        "detectors_agree": second_detector,
        "power_cycle_presence": agreement,
        "power_cycle_witnesses": witnesses,
        "power_cycle_free": not witnesses,
        **encodings,
    }


def first_power_cycle(adjacency):
    power = 4
    while power <= len(adjacency):
        witness = find_cycle_exact(adjacency, power)
        if witness is not None:
            return power, witness
        power *= 2
    return None


def near_miss_repair_audit(path: Path) -> dict:
    payload = json.loads(path.read_text())
    parameters = payload["parameters"]
    core = build_core(parameters["j"], parameters["a"], parameters["c"])
    matching = [tuple(sorted(edge)) for edge in payload["matching_edges"]]
    all_edges = list(core.edges) + matching

    deletion_outcomes = Counter()
    clean_deletions = []
    for deleted in all_edges:
        adjacency = [set() for _ in range(core.order)]
        for edge in all_edges:
            if edge == deleted:
                continue
            u, v = edge
            adjacency[u].add(v)
            adjacency[v].add(u)
        witness = first_power_cycle(tuple(frozenset(row) for row in adjacency))
        deletion_outcomes["power_cycle_free" if witness is None else str(witness[0])] += 1
        if witness is None:
            clean_deletions.append(list(deleted))

    core_edges = set(core.edges)
    switch_outcomes = Counter()
    valid_switches = 0
    clean_switches = []
    for first in range(len(matching)):
        for second in range(first + 1, len(matching)):
            (a, b), (c, d) = matching[first], matching[second]
            for replacement in (
                (tuple(sorted((a, c))), tuple(sorted((b, d)))),
                (tuple(sorted((a, d))), tuple(sorted((b, c)))),
            ):
                if any(edge in core_edges for edge in replacement):
                    switch_outcomes["invalid_core_edge"] += 1
                    continue
                valid_switches += 1
                candidate = list(matching)
                candidate[first], candidate[second] = replacement
                adjacency = [set(row) for row in core.adjacency()]
                for u, v in candidate:
                    adjacency[u].add(v)
                    adjacency[v].add(u)
                witness = first_power_cycle(tuple(frozenset(row) for row in adjacency))
                switch_outcomes["power_cycle_free" if witness is None else str(witness[0])] += 1
                if witness is None:
                    clean_switches.append({
                        "removed": [list(matching[first]), list(matching[second])],
                        "added": [list(edge) for edge in replacement],
                    })

    return {
        "status": "PASS",
        "parameters": parameters,
        "baseline_power_cycles": payload.get("power_cycle_witnesses", {}),
        "single_edge_deletions": {
            "tested": len(all_edges),
            "all_invalidate_minimum_degree_three": True,
            "first_power_cycle_distribution": dict(sorted(deletion_outcomes.items())),
            "power_cycle_free_deletions": clean_deletions,
        },
        "matching_two_switches": {
            "unordered_matching_edge_pairs": len(matching) * (len(matching) - 1) // 2,
            "two_reconnections_per_pair": True,
            "valid_degree_preserving_switches": valid_switches,
            "outcomes": dict(sorted(switch_outcomes.items())),
            "power_cycle_free_repairs": clean_switches,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase0", action="store_true")
    parser.add_argument("--completion", type=Path)
    parser.add_argument("--repair-audit", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--skip-second-detector", action="store_true")
    args = parser.parse_args()
    modes = int(args.phase0) + int(args.completion is not None) + int(args.repair_audit is not None)
    if modes != 1:
        parser.error("choose exactly one of --phase0, --completion, and --repair-audit")
    if args.phase0:
        result = phase0_audit()
    elif args.completion is not None:
        result = audit_completion(args.completion, not args.skip_second_detector)
    else:
        result = near_miss_repair_audit(args.repair_audit)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
