#!/usr/bin/env python3
"""Independent checks for static short-cycle and C16 support catalogs."""

from __future__ import annotations

import argparse
import concurrent.futures
import gzip
import itertools
import json
from pathlib import Path

from pysat.solvers import Solver

from type_t_port_c16_hypergraph import (
    build_cycle_projection_cnf,
    gadget_catalog,
    universal_graph,
)
from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle
from type_t_port_multipole_sat import materialize


_WORKER_CORE = None
_WORKER_GADGETS = None


def initialize_worker(j: int, a: int, c: int) -> None:
    global _WORKER_CORE, _WORKER_GADGETS
    _WORKER_CORE = build_core(j, a, c)
    _WORKER_GADGETS = gadget_catalog(_WORKER_CORE)[0]


def verify_materialized_record(record: dict) -> int:
    adjacency = support_materialization(
        _WORKER_CORE, record["gadgets"], _WORKER_GADGETS,
    )
    assert edge_path_cycle(adjacency, 16) is not None
    return len(record["support"])


def read_json(path: Path) -> dict:
    return json.loads(
        gzip.open(path, "rt").read() if path.suffix == ".gz" else path.read_text()
    )


def passage_vertices(record: dict, gadgets: dict):
    variable = record["gadget"]
    gadget = gadgets[variable]
    left, right = record["left"], record["right"]
    if record["length"] == 2:
        token = record["hub_tokens"][0]
        return [left, (variable, token), right]
    assert record["length"] == 3
    assert gadget.kind == "linked_pairs"
    left_side = next(
        index for index, pair in enumerate(gadget.triples) if left in pair
    )
    right_side = next(
        index for index, pair in enumerate(gadget.triples) if right in pair
    )
    assert left_side != right_side
    return [left, (variable, left_side), (variable, right_side), right]


def validate_short_record(core_edges, record, gadgets, target: int) -> None:
    paths = record["core_paths"]
    passages = record["passages"]
    assert len(paths) == len(passages) in (1, 2)
    cycle = list(paths[0])
    for index, passage in enumerate(passages):
        expanded = passage_vertices(passage, gadgets)
        assert cycle[-1] == expanded[0]
        cycle.extend(expanded[1:])
        if index + 1 < len(paths):
            assert cycle[-1] == paths[index + 1][0]
            cycle.extend(paths[index + 1][1:])
    assert cycle[-1] == cycle[0]
    cycle.pop()
    assert len(cycle) == target
    assert len(cycle) == len(set(cycle))
    for path in paths:
        assert all(
            tuple(sorted((left, right))) in core_edges
            for left, right in zip(path, path[1:])
        )
    support = sorted({passage["gadget"] for passage in passages})
    assert support == record["support"]


def support_materialization(core, records, catalog):
    triples = []
    linked = None
    for item in records:
        gadget = catalog[item["variable"]]
        assert gadget.kind == item["kind"]
        attachments = item.get("attachments")
        if attachments is None:
            attachments = (
                item.get("triple") or
                [vertex for pair in item["pairs"] for vertex in pair]
            )
        assert tuple(sorted(attachments)) == gadget.attachments
        if gadget.kind == "triple":
            triples.append(gadget.triples[0])
        else:
            assert linked is None
            linked = gadget.triples
    return materialize(core, triples, linked)[1]


def audit(short_path: Path, c16_path: Path, j: int, a: int, c: int,
          cegar_path: Path | None = None, completion_path: Path | None = None,
          workers: int = 1):
    core = build_core(j, a, c)
    short = read_json(short_path)
    c16 = read_json(c16_path)
    gadgets, _, _, _ = gadget_catalog(core)
    core_edges = set(core.edges)
    short_sets = []
    short_counts = {4: 0, 8: 0}
    for record in short["supports"]:
        for target in record["cycle_lengths"]:
            validate_short_record(core_edges, record, gadgets, target)
            short_counts[target] += 1
        short_sets.append(frozenset(record["support"]))

    adjacency, _, node_gadget, _, _, _ = universal_graph(core)
    for record in c16["supports"]:
        cycle = record.get("cycle")
        if cycle is not None:
            assert len(cycle) == len(set(cycle)) == 16
            assert all(
                cycle[(index + 1) % 16] in adjacency[cycle[index]]
                for index in range(16)
            )
            support = frozenset(
                node_gadget[vertex] for vertex in cycle if vertex in node_gadget
            )
            assert sorted(support) == record["support"]
        else:
            # Seeded CEGAR records store their original materialized-graph
            # witness rather than universal-graph vertex identifiers.  The
            # independent materialization check below is authoritative for
            # both record forms.
            support = frozenset(record["support"])
        assert not any(short_support <= support for short_support in short_sets)

    if workers == 1:
        initialize_worker(j, a, c)
        verified_sizes = [
            verify_materialized_record(record) for record in c16["supports"]
        ]
    else:
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=workers,
            initializer=initialize_worker,
            initargs=(j, a, c),
        ) as executor:
            verified_sizes = list(executor.map(
                verify_materialized_record, c16["supports"], chunksize=64,
            ))
    c16_sizes = {}
    for size in verified_sizes:
        c16_sizes[size] = c16_sizes.get(size, 0) + 1

    projection_exhaustion = None
    if c16["complete"]:
        encoding = build_cycle_projection_cnf(
            core, 16,
            extension_forbidden_supports=[list(item) for item in short_sets],
        )
        clauses = list(encoding["clauses"])
        used = encoding["used"]
        for support in short_sets:
            clauses.append([-used[variable] for variable in support])
        for record in c16["supports"]:
            clauses.append([-used[variable] for variable in record["support"]])
        with Solver(name="lingeling", bootstrap_with=clauses) as solver:
            exhausted = not solver.solve()
        assert exhausted
        projection_exhaustion = {
            "solver": "lingeling",
            "status": "UNSAT",
            "clauses": len(clauses),
            "variables": encoding["pool"].top,
        }

    cegar = None
    if cegar_path is not None:
        payload = read_json(cegar_path)
        unary = {
            next(iter(item)) for item in short_sets if len(item) == 1
        }
        binary = {
            tuple(sorted(item)) for item in short_sets if len(item) == 2
        }
        checked = 0
        missing = []
        for record in payload["cycle_cuts"]:
            if record["cycle_length"] != 8:
                continue
            support = tuple(sorted(-literal for literal in record["clause"]))
            covered = (
                any(variable in unary for variable in support) or
                any(tuple(pair) in binary for pair in itertools.combinations(support, 2))
            )
            checked += 1
            if not covered:
                missing.append(support)
        assert not missing
        cegar = {"c8_cuts_checked": checked, "missing": 0}

    completion = None
    if completion_path is not None:
        payload = read_json(completion_path)
        selected = set()
        triple_lookup = {
            gadget.triples[0]: variable for variable, gadget in gadgets.items()
            if gadget.kind == "triple"
        }
        linked_lookup = {
            gadget.triples: variable for variable, gadget in gadgets.items()
            if gadget.kind == "linked_pairs"
        }
        data = payload.get("completion", payload)
        selected.update(triple_lookup[tuple(sorted(item))] for item in data["triples"])
        linked = tuple(sorted(tuple(sorted(pair)) for pair in data["linked_pairs"]))
        selected.add(linked_lookup[linked])
        violations = [
            item for item in short_sets if item <= selected
        ]
        assert not violations
        completion = {"selected_gadgets": len(selected), "short_violations": 0}

    return {
        "status": "PASS",
        "parameters": {"j": j, "a": a, "c": c},
        "short_catalog": {
            "complete": short["complete"],
            "supports": len(short_sets),
            "verified_by_length": {
                str(key): value for key, value in short_counts.items()
            },
        },
        "c16_catalog": {
            "complete": c16["complete"],
            "supports": len(c16["supports"]),
            "verified_support_sizes": {
                str(key): value for key, value in sorted(c16_sizes.items())
            },
            "independent_projection_exhaustion": projection_exhaustion,
        },
        "cegar_cross_check": cegar,
        "saved_completion_cross_check": completion,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--short-catalog", type=Path, required=True)
    parser.add_argument("--c16-catalog", type=Path, required=True)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--cegar", type=Path)
    parser.add_argument("--completion", type=Path)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(
        args.short_catalog, args.c16_catalog, args.j, args.a, args.c,
        args.cegar, args.completion, args.workers,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)


if __name__ == "__main__":
    main()
