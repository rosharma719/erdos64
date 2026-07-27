#!/usr/bin/env python3
"""Finite realizability audit for the irreducible Type-B spectrum family.

This program freezes the exact family from ``type_b_compatibility.md``, lists
its first twenty tuples, verifies optimal canonical path-union witnesses for
the smallest tuple, and runs a paired degree-saturation CEGAR certificate for
one fixed minimum-order path template.  OR-Tools constructs the C8 witness
clauses; an independently encoded PySAT instance checks the final UNSAT result.

The certificate concerns one fixed canonical path embedding at order 36.  It
is not an exhaustive search over all embeddings, orders, or Type-B graphs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path

import networkx as nx
from ortools.sat.python import cp_model
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

try:
    from verifier.cycle_detect import (
        find_cycle_len_dfs,
        from_edges,
        has_cycle_len_nx,
    )
    from verifier.type_t_exact_two_a import BALABAN_10_CAGE_LCF
except ModuleNotFoundError:
    from cycle_detect import find_cycle_len_dfs, from_edges, has_cycle_len_nx
    from type_t_exact_two_a import BALABAN_10_CAGE_LCF


FORBIDDEN = {4, 8, 16, 32, 64, 128}


@dataclass(frozen=True, order=True)
class Parameters:
    rho: int
    s: int
    t: int
    u: int
    delta: int
    epsilon: int

    def valid(self) -> bool:
        return (
            self.rho >= 2
            and self.s >= 2
            and self.delta in (1, 2)
            and self.epsilon in (1, 2)
            and self.t > max(self.rho, self.s, 3)
            and self.u > max(self.rho, self.s, 3)
        )


def is_power(value: int) -> bool:
    return value >= 4 and value & (value - 1) == 0


def forced_spectra(params: Parameters) -> tuple[frozenset[int], frozenset[int]]:
    if not params.valid():
        raise ValueError(f"invalid irreducible-family tuple: {params}")
    ell = 2**params.t + 1
    m = 2**params.u + 1
    return (
        frozenset((2, ell, ell + params.delta)),
        frozenset((2**params.rho, 2**params.s + 1, m, m + params.epsilon)),
    )


def guaranteed_internal_lengths(params: Parameters) -> frozenset[int]:
    first, _ = forced_spectra(params)
    ell = 2**params.t + 1
    return frozenset((ell, ell + params.delta, 2**params.rho + 2**params.s - 1))


def is_abstractly_compatible(params: Parameters) -> bool:
    first, second = forced_spectra(params)
    values = (
        guaranteed_internal_lengths(params)
        | {value + 1 for value in first}
        | {value + 1 for value in second}
        | {left + right for left in first for right in second}
    )
    return not any(is_power(value) for value in values)


def bridge_bounds(params: Parameters) -> dict[str, int]:
    first, second = forced_spectra(params)
    n1 = max(first) + 1
    # The two theta suffixes are internally disjoint and form a cycle of
    # length 2^rho+2^s-1; adding x gives the second independent order bound.
    n2 = max(max(second) + 1, 2**params.rho + 2**params.s)
    e1 = math.ceil((3 * n1 - 4) / 2)
    e2 = math.ceil((3 * n2 - 4) / 2)
    return {
        "bridge_1_order": n1,
        "bridge_2_order": n2,
        "bridge_1_size": e1,
        "bridge_2_size": e2,
        "full_order": n1 + n2 - 2,
        "full_size": e1 + e2 + 1,
    }


def tuple_key(params: Parameters) -> tuple:
    first, second = forced_spectra(params)
    bounds = bridge_bounds(params)
    return (
        max(first | second),
        sum(first) + sum(second),
        bounds["full_order"],
        (params.rho, params.s, params.t, params.u),
        (params.delta, params.epsilon),
    )


def first_twenty() -> list[dict]:
    rows = []
    # An omitted valid tuple either has max(rho,s) >= 6 (so t,u >= 7) or
    # has t >= 8 or u >= 8. Its maximum required length is therefore at
    # least 129, whereas every row returned below has maximum at most 34.
    for rho in range(2, 6):
        for s in range(2, 6):
            floor = max(rho, s, 3) + 1
            for t in range(floor, 8):
                for u in range(floor, 8):
                    for delta in (1, 2):
                        for epsilon in (1, 2):
                            params = Parameters(rho, s, t, u, delta, epsilon)
                            first, second = forced_spectra(params)
                            rows.append((tuple_key(params), params, first, second))
    output = []
    for rank, (key, params, first, second) in enumerate(sorted(rows)[:20], 1):
        output.append(
            {
                "rank": rank,
                "parameters": asdict(params),
                "S1": sorted(first),
                "S2": sorted(second),
                "bounds": bridge_bounds(params),
                "ordering_key": [key[0], key[1], key[2], list(key[3]), list(key[4])],
            }
        )
    return output


def edge_set(paths: list[list[int]]) -> set[tuple[int, int]]:
    return {
        tuple(sorted((left, right)))
        for path in paths
        for left, right in zip(path, path[1:])
    }


def _node_key(node) -> tuple[str, str]:
    return (type(node).__name__, repr(node))


def canonical_cycle(cycle: list) -> tuple:
    """Canonicalize an undirected cycle up to rotation and reversal."""
    candidates = []
    for oriented in (cycle, list(reversed(cycle))):
        for offset in range(len(cycle)):
            rotated = tuple(oriented[offset:] + oriented[:offset])
            candidates.append(rotated)
    return min(candidates, key=lambda row: tuple(_node_key(node) for node in row))


def exact_cycles_of_length(graph: nx.Graph, length: int) -> set[tuple]:
    """Independent elementary DFS enumeration for one exact cycle length."""
    result = set()
    for start in sorted(graph, key=_node_key):
        start_key = _node_key(start)
        path = [start]
        used = {start}

        def visit(vertex) -> None:
            if len(path) == length:
                if graph.has_edge(vertex, start):
                    result.add(canonical_cycle(path.copy()))
                return
            for neighbor in graph.neighbors(vertex):
                if neighbor in used or _node_key(neighbor) < start_key:
                    continue
                used.add(neighbor)
                path.append(neighbor)
                visit(neighbor)
                path.pop()
                used.remove(neighbor)

        visit(start)
    return result


def smallest_path_union_witnesses() -> dict:
    result = {}
    for gap in (1, 2):
        n = 18 + gap
        longest = [0, 2, *range(3, n), 1]
        admissible = [0, 2, *range(15, 2, -1), 17, 18, 1]
        first_paths = [[0, 2, 1], longest, admissible]

        if gap == 1:
            theta_4 = [0, 2, 15, 9, 1]
            theta_5 = [0, 2, 3, 17, 18, 1]
        else:
            theta_4 = [0, 2, 19, 18, 1]
            theta_5 = [0, 2, 3, 8, 9, 1]
        second_paths = [longest, admissible, theta_4, theta_5]

        row = {}
        for name, paths in (("B1", first_paths), ("B2", second_paths)):
            edges = sorted(edge_set(paths))
            graph = from_edges(n, edges)
            assert find_cycle_len_dfs(graph, 4) is None
            assert find_cycle_len_dfs(graph, 8) is None
            assert find_cycle_len_dfs(graph, 16) is None
            assert not has_cycle_len_nx(graph, 4)
            assert not has_cycle_len_nx(graph, 8)
            assert not has_cycle_len_nx(graph, 16)
            internal_deficit = sum(
                max(0, 3 - len(graph[vertex]))
                for vertex in range(n)
                if vertex not in (0, 1)
            )
            row[name] = {
                "order": n,
                "paths": paths,
                "edges": edges,
                "degrees": sorted(dict(nx.Graph(edges).degree()).values()),
                "internal_degree_deficit": internal_deficit,
                "extra_edge_lower_bound": math.ceil(internal_deficit / 2),
            }
        result[str(gap)] = row
    return result


def paired_template() -> tuple[list[set[int]], set[tuple[int, int]], dict]:
    # Smallest Pi=(2,2,4,4,1,1), with the optimal path-union witnesses above.
    b1_paths = [
        [0, 2, 1],
        [0, 2, *range(3, 19), 1],
        [0, 2, *range(15, 2, -1), 17, 18, 1],
    ]
    mapping = {0: 0, 2: 1, 1: 19, **{index: index + 17 for index in range(3, 19)}}
    raw_b2 = [
        [0, 1, *range(3, 19), 2],
        [0, 1, *range(15, 2, -1), 17, 18, 2],
        [0, 1, 15, 9, 2],
        [0, 1, 3, 17, 18, 2],
    ]
    b2_paths = [[mapping[v] for v in path] for path in raw_b2]
    bridge_sets = [set(range(19)), {0, 1, *range(19, 36)}]
    fixed = {(0, 1)} | edge_set(b1_paths + b2_paths)
    return bridge_sets, fixed, {"B1": b1_paths, "B2": b2_paths}


def _all_edge_pairs(bridge_sets: list[set[int]]) -> list[tuple[int, int]]:
    pairs = set()
    for vertices in bridge_sets:
        pairs.update(combinations(sorted(vertices), 2))
    pairs.discard((0, 1))
    return sorted(pairs)


def saturation_certificate() -> dict:
    bridge_sets, fixed, paths = paired_template()
    pairs = _all_edge_pairs(bridge_sets)
    model = cp_model.CpModel()
    edge_vars = {pair: model.NewBoolVar(f"e_{pair[0]}_{pair[1]}") for pair in pairs}

    for pair in fixed - {(0, 1)}:
        model.Add(edge_vars[pair] == 1)
    prohibited = set()
    for vertices, gateway in zip(bridge_sets, (2, 19)):
        for vertex in vertices - {0, 1, gateway}:
            prohibited.add(tuple(sorted((0, vertex))))
    prohibited.add((1, 19))  # Lemma NA: no B2 length-two route.
    for pair in prohibited:
        model.Add(edge_vars[pair] == 0)

    for vertex in range(36):
        incident = [var for pair, var in edge_vars.items() if vertex in pair]
        model.Add(sum(incident) + (1 if vertex in (0, 1) else 0) >= 3)

    def expression(left: int, right: int):
        pair = tuple(sorted((left, right)))
        return 1 if pair == (0, 1) else edge_vars[pair]

    c4_clauses = []
    for vertices in bridge_sets:
        for a, b, c, d in combinations(sorted(vertices), 4):
            for cycle in ((a, b, c, d), (a, b, d, c), (a, c, b, d)):
                cycle_pairs = [
                    tuple(sorted((cycle[i], cycle[(i + 1) % 4]))) for i in range(4)
                ]
                model.Add(sum(expression(*pair) for pair in cycle_pairs) <= 3)
                c4_clauses.append(cycle_pairs)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 640031
    solver.parameters.max_time_in_seconds = 120
    learned = []
    statuses = []
    while True:
        status = solver.Solve(model)
        statuses.append(solver.StatusName(status))
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            assert status == cp_model.INFEASIBLE
            break
        edges = [(0, 1)] + [pair for pair, var in edge_vars.items() if solver.Value(var)]
        graph = from_edges(36, edges)
        witness = find_cycle_len_dfs(graph, 8)
        if witness is None:
            raise AssertionError("unexpected C8-free saturation candidate")
        assert has_cycle_len_nx(graph, 8)
        cycle_pairs = [
            tuple(sorted((witness[i], witness[(i + 1) % 8]))) for i in range(8)
        ]
        learned.append({"vertices": witness, "edges": cycle_pairs})
        model.Add(sum(expression(*pair) for pair in cycle_pairs) <= 7)

    # Independent CNF encoding and solver.  This does not reuse CP-SAT's
    # cardinality encoding or propagation.
    pool = IDPool()
    edge_ids = {pair: pool.id(f"e_{pair[0]}_{pair[1]}") for pair in pairs}
    clauses: list[list[int]] = []
    for pair in fixed - {(0, 1)}:
        clauses.append([edge_ids[pair]])
    for pair in prohibited:
        clauses.append([-edge_ids[pair]])
    for vertex in range(36):
        incident = [identifier for pair, identifier in edge_ids.items() if vertex in pair]
        needed = 2 if vertex in (0, 1) else 3
        clauses.extend(
            CardEnc.atleast(
                incident, bound=needed, vpool=pool, encoding=EncType.seqcounter
            ).clauses
        )

    def negative_cycle_clause(cycle_pairs: list[tuple[int, int]]) -> list[int]:
        return [
            -edge_ids[pair] for pair in cycle_pairs if pair != (0, 1)
        ]

    clauses.extend(negative_cycle_clause(cycle) for cycle in c4_clauses)
    clauses.extend(negative_cycle_clause(row["edges"]) for row in learned)
    with Solver(name="g3", bootstrap_with=clauses) as independent:
        independently_unsat = not independent.solve()
    assert independently_unsat

    return {
        "scope": "fixed minimum-order canonical path embedding for Pi=(2,2,4,4,1,1)",
        "full_order": 36,
        "fixed_paths": paths,
        "edge_variables": len(edge_vars),
        "hard_c4_cycles": len(c4_clauses),
        "learned_c8_witnesses": learned,
        "ortools_status": statuses[-1],
        "ortools_iterations": len(learned),
        "independent_solver": "PySAT Glucose3 with independently encoded cardinalities",
        "independent_cnf_variables": pool.top,
        "independent_cnf_clauses": len(clauses),
        "independently_unsat": independently_unsat,
    }


def balaban_mechanism() -> dict:
    host = nx.LCF_graph(70, BALABAN_10_CAGE_LCF, 1)
    assert nx.node_connectivity(host) == 3
    bridge = host.copy()
    bridge.remove_edge(0, 1)
    bridge.add_edges_from(((0, "Y"), ("Y", 1), ("x", "Y")))
    path_11 = ["x", "Y", 1, 2, 3, 4, 5, 6, 63, 62, 61, 0]
    path_13 = ["x", "Y", 1, 2, 3, 4, 5, 6, 7, 8, 27, 28, 69, 0]
    pair_cell = [6, 63, 62, 61, 0, 69, 28, 27, 8, 7]
    ear = [3, 32, 31, 22, 23, 62]
    route_11 = [3, 4, 5, 6, 7, 8, 27, 28, 69, 0, 61, 62]
    reverse_route = list(reversed(route_11))
    c16 = [*ear, *reverse_route[1:-1]]

    def valid_path(path):
        return len(path) == len(set(path)) and all(
            bridge.has_edge(a, b) for a, b in zip(path, path[1:])
        )

    assert valid_path(path_11) and valid_path(path_13)
    assert len(pair_cell) == 10 and all(
        bridge.has_edge(pair_cell[i], pair_cell[(i + 1) % 10])
        for i in range(10)
    )
    assert valid_path(ear) and len(ear) - 1 == 5
    assert valid_path(route_11) and len(route_11) - 1 == 11
    assert len(c16) == len(set(c16)) == 16
    assert all(bridge.has_edge(c16[i], c16[(i + 1) % 16]) for i in range(16))

    networkx_c16 = {
        canonical_cycle(cycle)
        for cycle in nx.simple_cycles(bridge, length_bound=16)
        if len(cycle) == 16
    }
    dfs_c16 = exact_cycles_of_length(bridge, 16)
    assert networkx_c16 == dfs_c16
    path_edges = {
        length: {frozenset(edge) for edge in zip(path, path[1:])}
        for length, path in ((11, path_11), (13, path_13))
    }
    cycle_records = []
    for cycle in sorted(
        dfs_c16, key=lambda row: tuple(_node_key(node) for node in row)
    ):
        edges = {
            frozenset((cycle[index], cycle[(index + 1) % 16]))
            for index in range(16)
        }
        cycle_records.append(
            {
                "vertices": list(cycle),
                "path_11_common_edges": len(edges & path_edges[11]),
                "path_13_common_edges": len(edges & path_edges[13]),
                "path_11_common_vertices": len(set(cycle) & set(path_11)),
                "path_13_common_vertices": len(set(cycle) & set(path_13)),
            }
        )
    assert len(cycle_records) == 3298
    assert all("x" not in row["vertices"] and "Y" not in row["vertices"] for row in cycle_records)
    disjoint_from_pair = sum(
        row["path_11_common_vertices"] == row["path_13_common_vertices"] == 0
        for row in cycle_records
    )
    assert disjoint_from_pair == 672
    return {
        "admissible_pair": [11, 13],
        "pair_symmetric_difference_cycle_length": 10,
        "pair_symmetric_difference_cycle": pair_cell,
        "canonical_c16": list(canonical_cycle(c16)),
        "all_c16_count": len(cycle_records),
        "all_c16": cycle_records,
        "independent_c16_enumerators_agree": True,
        "c16_disjoint_from_both_paths": disjoint_from_pair,
        "all_c16_inside_rigid_host_core": True,
        "host_vertex_connectivity": 3,
        "saturation_ear": ear,
        "ear_length": 5,
        "canonical_union_route": route_11,
        "union_route_length": 11,
        "mechanism": "a length-5 rigid-core ear plus a length-11 canonical-union route",
        "proposed_2t_family_match": False,
        "reason": "11,13 are 2^3+3 and 2^3+5, not 2^t+1 and 2^t+3",
        "classification": "saturation ear inside the 3-connected R-core",
    }


def balaban_two_switch_audit() -> dict:
    """Exhaust the witness-edge 2-switch class while retaining both paths."""
    host = nx.LCF_graph(70, BALABAN_10_CAGE_LCF, 1)
    bridge = host.copy()
    bridge.remove_edge(0, 1)
    bridge.add_edges_from(((0, "Y"), ("Y", 1), ("x", "Y")))
    path_11 = ["x", "Y", 1, 2, 3, 4, 5, 6, 63, 62, 61, 0]
    path_13 = ["x", "Y", 1, 2, 3, 4, 5, 6, 7, 8, 27, 28, 69, 0]
    c16 = [3, 32, 31, 22, 23, 62, 61, 0, 69, 28, 27, 8, 7, 6, 5, 4]

    def node_key(node):
        return (isinstance(node, str), str(node))

    def pair(left, right):
        return tuple(sorted((left, right), key=node_key))

    protected = {
        pair(left, right)
        for path in (path_11, path_13)
        for left, right in zip(path, path[1:])
    }
    all_edges = {pair(left, right) for left, right in bridge.edges()}
    witness_edges = [
        pair(c16[index], c16[(index + 1) % 16]) for index in range(16)
    ]
    removable_witness_edges = sorted(
        set(witness_edges) - protected,
        key=lambda edge: tuple(node_key(node) for node in edge),
    )
    ordered_edges = sorted(
        all_edges, key=lambda edge: tuple(node_key(node) for node in edge)
    )
    records = []
    seen = set()
    counts = {"structural": 0, "C4": 0, "C8": 0, "C16": 0, "clean_through_16": 0}

    for first in removable_witness_edges:
        a, b = first
        for second in ordered_edges:
            if second == first or second in protected or set(first) & set(second):
                continue
            c, d = second
            for added in ((pair(a, c), pair(b, d)), (pair(a, d), pair(b, c))):
                if (
                    added[0][0] == added[0][1]
                    or added[1][0] == added[1][1]
                    or added[0] in all_edges
                    or added[1] in all_edges
                    or added[0] == added[1]
                ):
                    continue
                key = (first, second, *added)
                if key in seen:
                    continue
                seen.add(key)
                mutated = bridge.copy()
                mutated.remove_edges_from((first, second))
                mutated.add_edges_from(added)
                closure = mutated.copy()
                closure.add_edge("x", 0)
                if not nx.is_biconnected(closure):
                    continue
                counts["structural"] += 1
                labels = {node: index for index, node in enumerate(mutated.nodes())}
                reverse = {index: node for node, index in labels.items()}
                adjacency = from_edges(
                    len(labels),
                    [(labels[u], labels[v]) for u, v in mutated.edges()],
                )
                failure = None
                for length in (4, 8, 16):
                    witness = find_cycle_len_dfs(adjacency, length)
                    if witness is not None:
                        literal = [reverse[index] for index in witness]
                        assert len(literal) == len(set(literal)) == length
                        assert all(
                            mutated.has_edge(literal[i], literal[(i + 1) % length])
                            for i in range(length)
                        )
                        failure = (length, literal)
                        counts[f"C{length}"] += 1
                        break
                if failure is None:
                    counts["clean_through_16"] += 1
                records.append(
                    {
                        "removed": [list(first), list(second)],
                        "added": [list(added[0]), list(added[1])],
                        "failure_length": failure[0] if failure else None,
                        "failure_witness": failure[1] if failure else None,
                    }
                )
    assert counts["structural"] == len(records)
    assert counts["clean_through_16"] == 0
    return {
        "operation_class": (
            "all simple degree-preserving 2-switches removing an unprotected edge "
            "of the canonical C16, retaining every edge of the 11/13 paths"
        ),
        "removable_c16_edges": [list(edge) for edge in removable_witness_edges],
        "counts": counts,
        "records": records,
        "scope": "finite mutation certificate, not a theorem about other reroutings",
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("data/type_b_pi0_fixed_template_certificate.json"),
    )
    args = parser.parse_args()
    params = Parameters(2, 2, 4, 4, 1, 1)
    assert is_abstractly_compatible(params)
    report = {
        "family_definition": {
            "parameters": "Pi=(rho,s,t,u,delta,epsilon)",
            "validity": "rho,s>=2; delta,epsilon in {1,2}; t,u>max(rho,s,3)",
            "smallest": asdict(params),
            "smallest_forced_spectra": [
                sorted(spectrum) for spectrum in forced_spectra(params)
            ],
            "completeness_scope": (
                "exactly the one explicit infinite family isolated in the prior phase; "
                "not all abstractly compatible spectra"
            ),
        },
        "first_twenty": first_twenty(),
        "smallest_path_unions": smallest_path_union_witnesses(),
        "fixed_template_saturation": saturation_certificate(),
        "balaban_mechanism": balaban_mechanism(),
        "balaban_two_switch_audit": balaban_two_switch_audit(),
        "assertion_failures": 0,
    }
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    summary = {
        "certificate": str(args.certificate),
        "certificate_sha256": sha256(args.certificate),
        "first_tuple": report["first_twenty"][0],
        "path_union_orders": {
            gap: {bridge: row["order"] for bridge, row in bridges.items()}
            for gap, bridges in report["smallest_path_unions"].items()
        },
        "fixed_template_saturation": {
            key: report["fixed_template_saturation"][key]
            for key in (
                "scope",
                "full_order",
                "edge_variables",
                "hard_c4_cycles",
                "ortools_iterations",
                "ortools_status",
                "independent_cnf_variables",
                "independent_cnf_clauses",
                "independently_unsat",
            )
        },
        "balaban_mechanism": report["balaban_mechanism"]["mechanism"],
        "balaban_two_switch_counts": report["balaban_two_switch_audit"]["counts"],
        "assertion_failures": 0,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
