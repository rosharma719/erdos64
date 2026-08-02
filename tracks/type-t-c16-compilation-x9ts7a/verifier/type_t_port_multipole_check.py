#!/usr/bin/env python3
"""Independent structural and cycle-cut checks for multipole searches."""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

import networkx as nx

from type_t_port_core_export import build_core
from type_t_port_multipole_sat import build_catalog, materialize
from type_t_port_triples import minimum_cubic_parameters, powers_up_to


def edge_path_cycle(adjacency, length: int):
    """Find an exact cycle as an edge plus a simple path avoiding that edge."""
    edges = [
        (u, v) for u, row in enumerate(adjacency) for v in row if u < v
    ]
    for left, right in edges:
        path = [left]
        used = {left}

        def visit(vertex: int):
            if len(path) == length:
                return tuple(path) if vertex == right else None
            for neighbor in adjacency[vertex]:
                if ((vertex == left and neighbor == right) or
                        (vertex == right and neighbor == left)):
                    continue
                if neighbor in used and neighbor != right:
                    continue
                if neighbor == right and len(path) != length - 1:
                    continue
                used.add(neighbor)
                path.append(neighbor)
                result = visit(neighbor)
                if result is not None:
                    return result
                path.pop()
                used.remove(neighbor)
            return None

        result = visit(left)
        if result is not None:
            return result
    return None


def validate_literal_cycle(graph: nx.Graph, cycle: list[int]) -> None:
    assert len(cycle) == len(set(cycle))
    assert all(
        graph.has_edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def partition_from_payload(payload: dict):
    triples = [tuple(item) for item in payload["triples"]]
    linked = payload["linked_pairs"]
    gadget = tuple(tuple(pair) for pair in linked) if linked is not None else None
    return triples, gadget


def validate_partition(core, completion: dict) -> dict:
    normal = minimum_cubic_parameters(core.j)
    triples, gadget = partition_from_payload(completion)
    covered = [vertex for triple in triples for vertex in triple]
    if gadget is not None:
        covered.extend(gadget[0] + gadget[1])
    deficient = core.deficient_vertices()
    assert len(covered) == len(set(covered)) == len(deficient)
    assert set(covered) == set(deficient)
    assert len(triples) == normal["triple_hubs"]
    assert (gadget is not None) == (core.j % 2 == 0)
    graph, adjacency, _, hubs = materialize(core, triples, gadget)
    assert graph.number_of_nodes() == core.order + normal["new_cubic_vertices"]
    assert not graph.is_multigraph()
    assert nx.is_connected(graph)
    assert min(dict(graph.degree()).values()) >= 3
    assert all(graph.degree(record["vertex"]) == 3 for record in hubs)
    if "edges" in completion:
        assert sorted(map(tuple, completion["edges"])) == sorted(graph.edges())
    if "graph6" in completion:
        actual = nx.to_graph6_bytes(graph, header=False).decode().strip()
        assert completion["graph6"] == actual
    if "sparse6" in completion:
        actual = nx.to_sparse6_bytes(graph, header=False).decode().strip()
        assert completion["sparse6"] == actual
    return {
        "order": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "minimum_degree": min(dict(graph.degree()).values()),
        "connected": True,
        "adjacency": adjacency,
    }


def graph_for_cut(core, descriptions: list[dict]):
    triples = []
    linked = None
    for item in descriptions:
        if item["kind"] == "triple":
            triples.append(tuple(item["attachments"]))
        elif item["kind"] == "linked_pairs":
            assert linked is None
            linked = tuple(tuple(pair) for pair in item["pairs"])
        else:
            raise AssertionError(f"unknown gadget kind {item['kind']}")
    return materialize(core, triples, linked)[1]


def read_dimacs(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    clauses = []
    variables = None
    declared = None
    with opener(path, "rt") as source:
        for line in source:
            if not line or line[0] == "c":
                continue
            if line.startswith("p "):
                _, _, variables_text, clauses_text = line.split()
                variables, declared = int(variables_text), int(clauses_text)
                continue
            literals = [int(item) for item in line.split()]
            assert literals[-1] == 0
            clauses.append(tuple(literals[:-1]))
    assert declared == len(clauses)
    return variables, clauses


def audit(path: Path, verify_all_cuts: bool = True) -> dict:
    payload = json.loads(
        gzip.open(path, "rt").read() if path.suffix == ".gz" else path.read_text()
    )
    parameters = payload["parameters"]
    core = build_core(parameters["j"], parameters["a"], parameters["c"])
    if "catalog" not in payload and "completion" in payload:
        structural = validate_partition(core, payload["completion"])
        adjacency = structural.pop("adjacency")
        graph, _, _, _ = materialize(
            core, *partition_from_payload(payload["completion"]),
        )
        independent = {}
        for length_text, cycle in payload["power_cycle_witnesses"].items():
            length = int(length_text)
            assert len(cycle) == length
            validate_literal_cycle(graph, cycle)
            found = edge_path_cycle(adjacency, length)
            assert found is not None
            independent[length_text] = list(found)
        for length_text, count in payload["best_short_cycle_counts"].items():
            if count == 0:
                assert edge_path_cycle(adjacency, int(length_text)) is None
        return {
            "status": "PASS",
            "source": str(path),
            "parameters": parameters,
            "search_status": payload["status"],
            "structural_completion_check": structural,
            "independent_cycle_witnesses": independent,
            "reported_zero_cycle_lengths_verified": [
                int(length) for length, count
                in payload["best_short_cycle_counts"].items() if count == 0
            ],
        }
    normal, pairs, triples, gadgets, same_bad, cross_bad = build_catalog(core)
    assert payload["minimum_cubic_completion"] == normal
    assert payload["catalog"] == {
        "allowed_pairs": len(pairs),
        "allowed_triples": len(triples),
        "linked_pair_gadgets": len(gadgets),
        "same_hub_incompatible_pairs": len(same_bad),
        "opposite_hub_incompatible_pairs": len(cross_bad),
    }

    completion_key = (
        "completion" if payload["status"] == "SAT" else "last_rejected_completion"
    )
    structural = None
    detector_results = {}
    if completion_key in payload:
        structural = validate_partition(core, payload[completion_key])
        adjacency = structural.pop("adjacency")
        graph, _, _, _ = materialize(
            core, *partition_from_payload(payload[completion_key]),
        )
        for length_text, cycle in payload["last_power_cycle_witnesses"].items():
            length = int(length_text)
            assert len(cycle) == length
            validate_literal_cycle(graph, cycle)
            independent = edge_path_cycle(adjacency, length)
            assert independent is not None
            detector_results[length_text] = list(independent)
        if payload["status"] == "SAT":
            for length in powers_up_to(graph.number_of_nodes()):
                assert edge_path_cycle(adjacency, length) is None

    cuts = payload["cycle_cuts"]
    checked = cuts if verify_all_cuts else cuts[:100]
    for record in checked:
        variables = sorted(-literal for literal in record["clause"])
        assert variables == sorted(item["variable"] for item in record["gadgets"])
        assert record["cycle_length"] in payload["forbidden_cycle_lengths"]
        adjacency = graph_for_cut(core, record["gadgets"])
        assert edge_path_cycle(adjacency, record["cycle_length"]) is not None

    cnf_audit = None
    if "cnf" in payload:
        cnf_path = Path(payload["cnf"])
        if not cnf_path.is_absolute():
            cnf_path = path.parents[2] / cnf_path
        variables, clauses = read_dimacs(cnf_path)
        clause_set = set(clauses)
        assert variables == payload["sat"]["variables"]
        assert len(clauses) == payload["sat"]["final_clauses"]
        assert all(tuple(record["clause"]) in clause_set for record in cuts)
        cnf_audit = {"variables": variables, "clauses": len(clauses)}

    return {
        "status": "PASS",
        "source": str(path),
        "parameters": parameters,
        "search_status": payload["status"],
        "structural_completion_check": structural,
        "independent_cycle_witnesses": detector_results,
        "cycle_cuts_checked": len(checked),
        "all_cycle_cuts_checked": len(checked) == len(cuts),
        "cnf": cnf_audit,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("--sample-cuts", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.result.resolve(), not args.sample_cuts)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
