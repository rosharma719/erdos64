#!/usr/bin/env python3
"""Single-hub compatibility for minimum cubic Type-T multipoles.

An attachment route of length ``r`` between two deficient core vertices
closes a dyadic cycle precisely when the core contains a simple path of
length ``2^k-r`` between them.  This module enumerates those paths, builds
the safe-pair graph, enumerates its triangles, and constructs the exceptional
linked-double-hub gadgets required when ``j`` is even.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx
from ortools.sat.python import cp_model
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Glucose3

from type_t_port_core_export import build_core


Pair = tuple[int, int]
Triple = tuple[int, int, int]
LinkedGadget = tuple[Pair, Pair]


def powers_up_to(order: int) -> tuple[int, ...]:
    values: list[int] = []
    value = 4
    while value <= order:
        values.append(value)
        value *= 2
    return tuple(values)


def minimum_cubic_parameters(j: int) -> dict:
    deficient = 5 * (1 << j) - 4
    if j % 2:
        new_vertices = deficient // 3
        new_new_edges = 0
        triples = new_vertices
        pairs = 0
    else:
        new_vertices = (deficient + 2) // 3
        new_new_edges = 1
        triples = new_vertices - 2
        pairs = 2
    assert 3 * new_vertices == deficient + 2 * new_new_edges
    return {
        "deficient_vertices": deficient,
        "new_cubic_vertices": new_vertices,
        "new_new_edges": new_new_edges,
        "triple_hubs": triples,
        "linked_double_hubs": pairs,
        "incidence_identity": "3*t=|D|+2*e",
    }


def path_incompatibilities(core, route_length: int, completion_order: int):
    """Enumerate every relevant simple path and aggregate by endpoint pair.

    The returned reason map records the number of simple paths for every
    forbidden resulting cycle length and retains one literal path witness.
    """
    cycle_lengths = powers_up_to(completion_order)
    target_to_cycle = {
        length - route_length: length for length in cycle_lengths
        if length > route_length
    }
    maximum = max(target_to_cycle, default=0)
    deficient = set(core.deficient_vertices())
    adjacency = core.adjacency()
    reasons: dict[Pair, dict[int, dict]] = {}
    path_counts = Counter()

    for start in sorted(deficient):
        path = [start]
        used = {start}

        def visit(vertex: int, depth: int) -> None:
            if depth in target_to_cycle and vertex in deficient and start < vertex:
                cycle_length = target_to_cycle[depth]
                pair = (start, vertex)
                record = reasons.setdefault(pair, {}).setdefault(
                    cycle_length, {"paths": 0, "witness": list(path)},
                )
                record["paths"] += 1
                path_counts[cycle_length] += 1
            if depth == maximum:
                return
            for neighbor in adjacency[vertex]:
                if neighbor not in used:
                    used.add(neighbor)
                    path.append(neighbor)
                    visit(neighbor, depth + 1)
                    path.pop()
                    used.remove(neighbor)

        visit(start, 0)
    return reasons, dict(sorted(path_counts.items()))


def safe_pairs(deficient: tuple[int, ...], incompatible: dict[Pair, dict]) -> list[Pair]:
    return [
        pair for pair in combinations(deficient, 2)
        if pair not in incompatible
    ]


def allowed_triples(deficient: tuple[int, ...], pairs: list[Pair]) -> list[Triple]:
    graph = nx.Graph()
    graph.add_nodes_from(deficient)
    graph.add_edges_from(pairs)
    triples: list[Triple] = []
    for u in deficient:
        larger = {v for v in graph[u] if v > u}
        for v in sorted(larger):
            for w in sorted(larger & set(graph[v])):
                if w > v:
                    triples.append((u, v, w))
    return triples


def linked_gadgets(deficient: tuple[int, ...], pairs: list[Pair],
                   cross_incompatible: dict[Pair, dict]) -> list[LinkedGadget]:
    """All locally safe two-pair gadgets, modulo swapping their two hubs."""
    pair_set = set(pairs)
    cross_safe = {vertex: set() for vertex in deficient}
    for u, v in combinations(deficient, 2):
        if (u, v) not in cross_incompatible:
            cross_safe[u].add(v)
            cross_safe[v].add(u)
    gadgets: list[LinkedGadget] = []
    for first in pairs:
        u, v = first
        possible = sorted(cross_safe[u] & cross_safe[v])
        for x, y in combinations(possible, 2):
            second = (x, y)
            if first < second and second in pair_set:
                gadgets.append((first, second))
    return gadgets


def _distribution(values) -> dict[str, int]:
    return {str(key): value for key, value in sorted(Counter(values).items())}


def exact_cover_status(deficient: tuple[int, ...], triples: list[Triple],
                       gadgets: list[LinkedGadget] | None) -> dict:
    pool = IDPool()
    triple_vars = {triple: pool.id(("triple", triple)) for triple in triples}
    gadget_vars = {
        gadget: pool.id(("linked", gadget)) for gadget in (gadgets or [])
    }
    incident = {vertex: [] for vertex in deficient}
    for triple, variable in triple_vars.items():
        for vertex in triple:
            incident[vertex].append(variable)
    for gadget, variable in gadget_vars.items():
        for vertex in gadget[0] + gadget[1]:
            incident[vertex].append(variable)
    clauses: list[list[int]] = []
    for vertex in deficient:
        clauses.extend(CardEnc.equals(
            incident[vertex], 1, vpool=pool, encoding=EncType.seqcounter,
        ).clauses)
    if gadgets is not None:
        clauses.extend(CardEnc.equals(
            list(gadget_vars.values()), 1, vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses)
    with Glucose3(bootstrap_with=clauses) as solver:
        feasible = solver.solve()
        model = set(solver.get_model()) if feasible else set()

    cp = cp_model.CpModel()
    cp_triples = {
        triple: cp.new_bool_var(f"triple_{index}")
        for index, triple in enumerate(triples)
    }
    cp_gadgets = {
        gadget: cp.new_bool_var(f"linked_{index}")
        for index, gadget in enumerate(gadgets or [])
    }
    for vertex in deficient:
        cp.add_exactly_one(
            [variable for triple, variable in cp_triples.items()
             if vertex in triple] +
            [variable for gadget, variable in cp_gadgets.items()
             if vertex in gadget[0] + gadget[1]]
        )
    if gadgets is not None:
        cp.add_exactly_one(cp_gadgets.values())
    cp_solver = cp_model.CpSolver()
    cp_solver.parameters.num_search_workers = 1
    cp_solver.parameters.random_seed = 0
    cp_solver.parameters.max_time_in_seconds = 30.0
    cp_status_code = cp_solver.solve(cp)
    cp_status = cp_solver.status_name(cp_status_code)
    cp_feasible = cp_status_code in (cp_model.FEASIBLE, cp_model.OPTIMAL)
    if cp_status_code != cp_model.UNKNOWN:
        assert cp_feasible == feasible
    return {
        "status": "SAT" if feasible else "UNSAT",
        "pysat_solver": "glucose3",
        "cp_sat_status": cp_status,
        "variables": pool.top,
        "clauses": len(clauses),
        "selected_triples": [
            list(triple) for triple, variable in triple_vars.items()
            if variable in model
        ],
        "selected_linked_gadget": next((
            [list(pair) for pair in gadget]
            for gadget, variable in gadget_vars.items() if variable in model
        ), None),
    }


def analyze(j: int, a: int, c: int, include_catalog: bool = False) -> dict:
    core = build_core(j, a, c)
    normal_form = minimum_cubic_parameters(j)
    assert len(core.deficient_vertices()) == normal_form["deficient_vertices"]
    completion_order = core.order + normal_form["new_cubic_vertices"]
    deficient = core.deficient_vertices()

    same_bad, same_path_counts = path_incompatibilities(
        core, route_length=2, completion_order=completion_order,
    )
    pairs = safe_pairs(deficient, same_bad)
    triples = allowed_triples(deficient, pairs)
    graph = nx.Graph()
    graph.add_nodes_from(deficient)
    graph.add_edges_from(pairs)
    maximum_clique, maximum = nx.max_weight_clique(graph, weight=None)
    maximum_sets = [tuple(sorted(maximum_clique))]
    triple_degree = Counter(vertex for triple in triples for vertex in triple)

    cross_bad: dict[Pair, dict] = {}
    cross_path_counts: dict[int, int] = {}
    gadgets: list[LinkedGadget] | None = None
    if j % 2 == 0:
        cross_bad, cross_path_counts = path_incompatibilities(
            core, route_length=3, completion_order=completion_order,
        )
        gadgets = linked_gadgets(deficient, pairs, cross_bad)

    cover = exact_cover_status(deficient, triples, gadgets)
    catalog_payload = {
        "allowed_pairs": [list(pair) for pair in pairs],
        "allowed_triples": [list(triple) for triple in triples],
        "linked_pair_gadgets": (
            [[list(pair) for pair in gadget] for gadget in gadgets]
            if gadgets is not None else []
        ),
    }
    catalog_bytes = json.dumps(
        catalog_payload, separators=(",", ":"), sort_keys=True,
    ).encode()
    result = {
        "status": "PASS",
        "parameters": {"j": j, "Y": 1 << j, "a": a, "c": c},
        "core": {
            "order": core.order,
            "edges": core.size,
            "deficient_vertices": len(deficient),
        },
        "minimum_cubic_completion": {
            **normal_form,
            "completion_order": completion_order,
            "forbidden_cycle_lengths": list(powers_up_to(completion_order)),
        },
        "same_hub_route": {
            "length": 2,
            "forbidden_core_path_lengths": [
                length - 2 for length in powers_up_to(completion_order)
            ],
            "incompatible_pairs": len(same_bad),
            "enumerated_forbidden_paths_by_cycle_length": {
                str(key): value for key, value in same_path_counts.items()
            },
            "allowed_pairs": len(pairs),
        },
        "allowed_triple_hypergraph": {
            "edges": len(triples),
            "vertex_degree_minimum": min(triple_degree.values()),
            "vertex_degree_maximum": max(triple_degree.values()),
            "vertex_degree_distribution": _distribution(triple_degree.values()),
            "pair_graph_components": sorted(
                (len(component) for component in nx.connected_components(graph)),
                reverse=True,
            ),
            "maximum_safe_attachment_set_size": maximum,
            "maximum_safe_attachment_sets": [list(item) for item in maximum_sets],
            "safe_sets_of_size_at_least_four_exist": maximum >= 4,
        },
        "linked_double_hubs": {
            "applicable": j % 2 == 0,
            "opposite_hub_route_length": 3 if j % 2 == 0 else None,
            "forbidden_core_path_lengths": (
                [length - 3 for length in powers_up_to(completion_order)]
                if j % 2 == 0 else []
            ),
            "cross_incompatible_pairs": len(cross_bad),
            "enumerated_forbidden_paths_by_cycle_length": {
                str(key): value for key, value in cross_path_counts.items()
            },
            "locally_allowed_gadgets": len(gadgets or []),
        },
        "local_exact_cover": cover,
        "catalog": {
            "sha256": hashlib.sha256(catalog_bytes).hexdigest(),
            "included": include_catalog,
        },
    }
    if include_catalog:
        result["catalog"].update(catalog_payload)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--include-catalog", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(args.j, args.a, args.c, args.include_catalog)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.suffix == ".gz":
            args.output.write_bytes(gzip.compress(rendered.encode(), mtime=0))
        else:
            args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
