#!/usr/bin/env python3
"""Compile static dyadic-cycle supports in a Type-T multipole completion.

The production encoding expands one universal copy of every allowed hub and
projects simple fixed-length cycles onto their selected gadget variables.
Exact-cover co-selectability, the linked-gadget restriction, short-conflict
clauses, and the structural support bound are imposed before AllSAT
enumeration.  A weighted-passage DFS is retained as an alternate search.
"""

from __future__ import annotations

import argparse
import gzip
import heapq
import itertools
import json
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle
from type_t_port_multipole_sat import (
    build_catalog,
    build_exact_cover_cnf,
    materialize,
)


def inclusion_minimal(records: list[dict]) -> list[dict]:
    ordered = sorted(records, key=lambda item: (
        item["support_size"], item["support"],
    ))
    retained = []
    retained_supports = set()
    for record in ordered:
        support = tuple(record["support"])
        if any(
            tuple(subset) in retained_supports
            for size in range(1, len(support))
            for subset in itertools.combinations(support, size)
        ):
            continue
        retained.append(record)
        retained_supports.add(support)
    return retained


@dataclass(frozen=True)
class Gadget:
    variable: int
    kind: str
    attachments: tuple[int, ...]
    triples: tuple[tuple[int, ...], ...]

    def to_json(self) -> dict:
        payload = {
            "variable": self.variable,
            "kind": self.kind,
            "attachments": list(self.attachments),
        }
        if self.kind == "triple":
            payload["triple"] = list(self.triples[0])
        else:
            payload["pairs"] = [list(pair) for pair in self.triples]
        return payload


@dataclass(frozen=True)
class Passage:
    gadget: int
    linked: bool
    left: int
    right: int
    length: int
    hub_tokens: tuple[int, ...]
    passage_kind: str

    def other(self, vertex: int) -> int:
        if vertex == self.left:
            return self.right
        if vertex == self.right:
            return self.left
        raise ValueError(vertex)


def gadget_catalog(core):
    _, _, triples, linked, _, _ = build_catalog(core)
    _, triple_var, linked_var, _, _ = build_exact_cover_cnf(
        core, triples, linked,
    )
    gadgets = {}
    passages = {vertex: [] for vertex in range(core.order)}
    for triple in triples:
        variable = triple_var[triple]
        gadget = Gadget(variable, "triple", triple, (triple,))
        gadgets[variable] = gadget
        for index, left in enumerate(triple):
            for right in triple[index + 1:]:
                passage = Passage(
                    variable, False, left, right, 2, (0,), "ordinary_hub",
                )
                passages[left].append(passage)
                passages[right].append(passage)
    for pairs in linked:
        variable = linked_var[pairs]
        attachments = tuple(sorted(pairs[0] + pairs[1]))
        gadget = Gadget(variable, "linked_pairs", attachments, pairs)
        gadgets[variable] = gadget
        for side, pair in enumerate(pairs):
            passage = Passage(
                variable, True, pair[0], pair[1], 2, (side,),
                f"linked_same_side_{side}",
            )
            passages[pair[0]].append(passage)
            passages[pair[1]].append(passage)
        for left in pairs[0]:
            for right in pairs[1]:
                passage = Passage(
                    variable, True, left, right, 3, (0, 1),
                    "linked_cross_edge",
                )
                passages[left].append(passage)
                passages[right].append(passage)
    for vertex in passages:
        passages[vertex].sort(key=lambda item: (
            item.gadget, item.length, item.hub_tokens, item.left, item.right,
        ))
    return gadgets, passages, triple_var, linked_var


def universal_graph(core):
    """The core plus one literal hub (two for linked gadgets) per gadget."""
    gadgets, _, triple_var, linked_var = gadget_catalog(core)
    adjacency = [set(row) for row in core.adjacency()]
    node_gadget = {}
    gadget_nodes = {}
    next_vertex = core.order
    for triple, variable in triple_var.items():
        hub = next_vertex
        next_vertex += 1
        adjacency.append(set())
        for vertex in triple:
            adjacency[hub].add(vertex)
            adjacency[vertex].add(hub)
        node_gadget[hub] = variable
        gadget_nodes[variable] = (hub,)
    for pairs, variable in linked_var.items():
        left, right = next_vertex, next_vertex + 1
        next_vertex += 2
        adjacency.extend((set(), set()))
        for vertex in pairs[0]:
            adjacency[left].add(vertex)
            adjacency[vertex].add(left)
        for vertex in pairs[1]:
            adjacency[right].add(vertex)
            adjacency[vertex].add(right)
        adjacency[left].add(right)
        adjacency[right].add(left)
        node_gadget[left] = node_gadget[right] = variable
        gadget_nodes[variable] = (left, right)
    return (
        tuple(frozenset(row) for row in adjacency), gadgets,
        node_gadget, gadget_nodes, triple_var, linked_var,
    )


def build_cycle_projection_cnf(core, target: int,
                               support_size: int | None = None,
                               extension_forbidden_supports: list[list[int]] | None = None,
                               require_extension: bool = True):
    if edge_path_cycle(core.adjacency(), target) is not None:
        raise ValueError(
            f"the fixed core itself contains a C{target}; the conflict is empty"
        )
    (adjacency, gadgets, node_gadget, gadget_nodes,
     triple_var, linked_var) = universal_graph(core)
    pool = IDPool()
    position = {
        (index, vertex): pool.id(("position", index, vertex))
        for index in range(target) for vertex in range(len(adjacency))
    }
    used = {
        variable: pool.id(("used_gadget", variable)) for variable in gadgets
    }
    clauses = []
    selected = {}
    extension_clause_count = 0
    if require_extension:
        (_, cover_triple_var, cover_linked_var, cover_clauses,
         _) = build_exact_cover_cnf(
            core, tuple(triple_var), tuple(linked_var),
        )
        if cover_triple_var != triple_var or cover_linked_var != linked_var:
            raise AssertionError("exact-cover primary variable IDs changed")
        primary_variables = set(gadgets)
        selected = {
            variable: pool.id(("selected_gadget", variable))
            for variable in primary_variables
        }

        def remap(literal: int) -> int:
            original = abs(literal)
            mapped = (
                selected[original] if original in primary_variables else
                pool.id(("cover_auxiliary", original))
            )
            return mapped if literal > 0 else -mapped

        clauses.extend([
            [remap(literal) for literal in clause]
            for clause in cover_clauses
        ])
        for variable in gadgets:
            clauses.append([-used[variable], selected[variable]])
        for support in extension_forbidden_supports or []:
            clauses.append([-selected[variable] for variable in support])
        extension_clause_count = len(clauses)
    for index in range(target):
        clauses.extend(CardEnc.equals(
            [position[index, vertex] for vertex in range(len(adjacency))],
            1, vpool=pool, encoding=EncType.seqcounter,
        ).clauses)
    for vertex in range(len(adjacency)):
        clauses.extend(CardEnc.atmost(
            [position[index, vertex] for index in range(target)],
            1, vpool=pool, encoding=EncType.seqcounter,
        ).clauses)

    # Break the target rotations by putting the least deficient core vertex
    # used by the cycle at position zero.  Every represented cycle contains a
    # hub passage and hence at least two deficient core vertices.  Hub node
    # numbers are larger than every core number, so this preserves one of the
    # two orientations of every literal cycle while removing all rotations.
    deficient = tuple(sorted(core.deficient_vertices()))
    deficient_set = set(deficient)
    for vertex in range(len(adjacency)):
        if vertex not in deficient_set:
            clauses.append([-position[0, vertex]])
    for anchor_index, anchor in enumerate(deficient):
        for smaller in deficient[:anchor_index]:
            for index in range(1, target):
                clauses.append([
                    -position[0, anchor], -position[index, smaller],
                ])
    for index in range(target):
        following = (index + 1) % target
        for vertex, neighbors in enumerate(adjacency):
            clauses.append(
                [-position[index, vertex]] +
                [position[following, neighbor] for neighbor in neighbors]
            )
    for hub, variable in node_gadget.items():
        for index in range(target):
            clauses.append([-position[index, hub], used[variable]])
    for variable, nodes in gadget_nodes.items():
        clauses.append(
            [-used[variable]] + [
                position[index, node]
                for node in nodes for index in range(target)
            ]
        )
    incident = {vertex: [] for vertex in core.deficient_vertices()}
    for variable, gadget in gadgets.items():
        for vertex in gadget.attachments:
            incident[vertex].append(used[variable])
    for variables in incident.values():
        clauses.extend(CardEnc.atmost(
            variables, 1, vpool=pool, encoding=EncType.seqcounter,
        ).clauses)
    clauses.extend(CardEnc.atmost(
        [used[variable] for variable in linked_var.values()],
        1, vpool=pool, encoding=EncType.seqcounter,
    ).clauses)
    support_bound = target // 3
    clauses.extend(CardEnc.atmost(
        list(used.values()), support_bound, vpool=pool,
        encoding=EncType.seqcounter,
    ).clauses)
    if support_size is not None:
        if not 1 <= support_size <= support_bound:
            raise ValueError(
                f"support size must lie in [1, {support_bound}]"
            )
        clauses.extend(CardEnc.equals(
            list(used.values()), support_size, vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses)
    clauses.append(list(used.values()))
    return {
        "adjacency": adjacency,
        "gadgets": gadgets,
        "node_gadget": node_gadget,
        "gadget_nodes": gadget_nodes,
        "triple_var": triple_var,
        "linked_var": linked_var,
        "pool": pool,
        "position": position,
        "used": used,
        "selected": selected,
        "clauses": clauses,
        "support_bound": support_bound,
        "require_extension": require_extension,
        "extension_clause_count": extension_clause_count,
    }


def compile_length_sat(core, target: int, max_seconds: float | None = None,
                       conflicts_per_solve: int = 100_000,
                       forbidden_supports: list[list[int]] | None = None,
                       existing_records: list[dict] | None = None,
                       support_size: int | None = None,
                       require_extension: bool = True) -> dict:
    encoding = build_cycle_projection_cnf(
        core, target, support_size,
        extension_forbidden_supports=forbidden_supports,
        require_extension=require_extension,
    )
    clauses = encoding["clauses"]
    position = encoding["position"]
    used = encoding["used"]
    gadgets = encoding["gadgets"]
    adjacency = encoding["adjacency"]
    existing_records = existing_records or []
    supports = {
        tuple(record["support"]): record for record in existing_records
    }
    models = 0
    budget_exhaustions = 0
    started = time.monotonic()
    complete = False
    forbidden_supports = forbidden_supports or []
    for support in forbidden_supports:
        clauses.append([-used[variable] for variable in support])
    for support in supports:
        clauses.append([-used[variable] for variable in support])
    base_clauses = len(clauses)
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        while max_seconds is None or time.monotonic() - started < max_seconds:
            solver.conf_budget(conflicts_per_solve)
            result = solver.solve_limited(expect_interrupt=True)
            if result is None:
                budget_exhaustions += 1
                continue
            if not result:
                complete = True
                break
            models += 1
            model = set(solver.get_model())
            cycle = [
                next(
                    vertex for vertex in range(len(adjacency))
                    if position[index, vertex] in model
                ) for index in range(target)
            ]
            if len(cycle) != len(set(cycle)):
                raise AssertionError("cycle projection repeats a vertex")
            if not all(
                cycle[(index + 1) % target] in adjacency[cycle[index]]
                for index in range(target)
            ):
                raise AssertionError("cycle projection uses a nonedge")
            support = tuple(sorted(
                variable for variable, literal in used.items() if literal in model
            ))
            literal_support = tuple(sorted({
                encoding["node_gadget"][vertex] for vertex in cycle
                if vertex in encoding["node_gadget"]
            }))
            if support != literal_support:
                raise AssertionError("gadget projection is not exact")
            if not 1 <= len(support) <= encoding["support_bound"]:
                raise AssertionError("support bound violated")
            supports.setdefault(support, {
                "support": list(support),
                "support_size": len(support),
                "cycle": cycle,
                "gadgets": [gadgets[variable].to_json() for variable in support],
            })
            block = [-used[variable] for variable in support]
            solver.add_clause(block)
            clauses.append(block)

    ordered = list(supports.values())
    minimal = inclusion_minimal(ordered)
    return {
        "status": "PASS" if complete else "TIME_LIMIT",
        "complete": complete and support_size is None,
        "projection_complete": complete,
        "support_size_stratum": support_size,
        "method": "SAT projection of simple cycles in the universal gadget graph",
        "target_length": target,
        "support_bound": encoding["support_bound"],
        "universal_graph": {
            "vertices": len(adjacency),
            "edges": sum(map(len, adjacency)) // 2,
            "core_vertices": core.order,
            "gadgets": len(gadgets),
        },
        "encoding": {
            "variables": encoding["pool"].top,
            "base_clauses": base_clauses,
            "requires_phi48_exact_cover_extension": require_extension,
            "extension_clauses": encoding["extension_clause_count"],
            "preloaded_forbidden_supports": len(forbidden_supports),
            "preloaded_target_supports": len(existing_records),
            "projection_blocks": models,
            "final_clauses": len(clauses),
            "conflict_budget_exhaustions": budget_exhaustions,
        },
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "enumerated_support_models_this_run": models,
        "distinct_supports": len(ordered),
        "minimal_supports": len(minimal),
        "support_size_distribution": {
            str(key): value for key, value in sorted(Counter(
                item["support_size"] for item in minimal
            ).items())
        },
        "supports": minimal,
    }


def lower_bound_distances(core, passages):
    """All-pairs optimistic weighted distances, ignoring gadget conflicts."""
    weighted = [dict() for _ in range(core.order)]
    for u, v in core.edges:
        weighted[u][v] = weighted[v][u] = 1
    for vertex, items in passages.items():
        for passage in items:
            other = passage.other(vertex)
            current = weighted[vertex].get(other)
            if current is None or passage.length < current:
                weighted[vertex][other] = passage.length
    distances = []
    for start in range(core.order):
        row = [10**9] * core.order
        row[start] = 0
        queue = [(0, start)]
        while queue:
            distance, vertex = heapq.heappop(queue)
            if distance != row[vertex]:
                continue
            for neighbor, weight in weighted[vertex].items():
                candidate = distance + weight
                if candidate < row[neighbor]:
                    row[neighbor] = candidate
                    heapq.heappush(queue, (candidate, neighbor))
        distances.append(tuple(row))
    return tuple(distances)


def _canonical_support(selected: dict[int, Gadget]) -> tuple[int, ...]:
    return tuple(sorted(selected))


def compile_length(core, target: int, include_linked: bool = True,
                   max_seconds: float | None = None) -> dict:
    gadgets, passages, _, _ = gadget_catalog(core)
    if not include_linked:
        passages = {
            vertex: [item for item in items if not item.linked]
            for vertex, items in passages.items()
        }
    lower = lower_bound_distances(core, passages)
    deficient = set(core.deficient_vertices())
    adjacency = core.adjacency()
    supports: dict[tuple[int, ...], dict] = {}
    statistics = Counter()
    started = time.monotonic()
    complete = True

    for start in sorted(deficient):
        if max_seconds is not None and time.monotonic() - started >= max_seconds:
            complete = False
            break
        used_core = {start}
        used_hubs: set[tuple[int, int]] = set()
        selected: dict[int, Gadget] = {}
        occupied: set[int] = set()
        steps: list[dict] = []

        def emit() -> None:
            support = _canonical_support(selected)
            if not support:
                return
            hub_passages = sum(step["kind"] == "passage" for step in steps)
            if hub_passages > target // 3:
                raise AssertionError("support-bound violation")
            record = {
                "support": list(support),
                "support_size": len(support),
                "hub_passages": hub_passages,
                "steps": [dict(step) for step in steps],
                "gadgets": [selected[variable].to_json() for variable in support],
            }
            old = supports.get(support)
            if old is None or tuple(map(str, record["steps"])) < tuple(map(str, old["steps"])):
                supports[support] = record
            statistics["literal_cycles"] += 1

        def visit(vertex: int, length: int, linked_variable: int | None) -> None:
            statistics["states"] += 1
            if length + lower[vertex][start] > target:
                statistics["distance_prunes"] += 1
                return

            for neighbor in adjacency[vertex]:
                new_length = length + 1
                if new_length > target:
                    continue
                if neighbor == start:
                    if new_length == target and steps:
                        steps.append({
                            "kind": "core", "left": vertex,
                            "right": start, "length": 1,
                        })
                        emit()
                        steps.pop()
                    continue
                if neighbor in used_core:
                    continue
                used_core.add(neighbor)
                steps.append({
                    "kind": "core", "left": vertex,
                    "right": neighbor, "length": 1,
                })
                visit(neighbor, new_length, linked_variable)
                steps.pop()
                used_core.remove(neighbor)

            if vertex not in deficient or vertex < start:
                return
            for passage in passages[vertex]:
                destination = passage.other(vertex)
                new_length = length + passage.length
                if new_length > target or destination < start:
                    continue
                if destination == start:
                    closes = new_length == target
                else:
                    closes = False
                    if destination in used_core:
                        continue
                variable = passage.gadget
                gadget = gadgets[variable]
                tokens = {(variable, token) for token in passage.hub_tokens}
                if tokens & used_hubs:
                    continue
                already_selected = variable in selected
                if already_selected:
                    if not passage.linked:
                        continue
                else:
                    if occupied.intersection(gadget.attachments):
                        continue
                    if passage.linked and linked_variable not in (None, variable):
                        continue
                if closes:
                    if new_length != target:
                        continue
                used_hubs.update(tokens)
                if not already_selected:
                    selected[variable] = gadget
                    occupied.update(gadget.attachments)
                steps.append({
                    "kind": "passage",
                    "left": vertex,
                    "right": destination,
                    "length": passage.length,
                    "gadget": variable,
                    "hub_tokens": list(passage.hub_tokens),
                    "passage_kind": passage.passage_kind,
                })
                next_linked = variable if passage.linked else linked_variable
                if closes:
                    emit()
                else:
                    used_core.add(destination)
                    visit(destination, new_length, next_linked)
                    used_core.remove(destination)
                steps.pop()
                if not already_selected:
                    occupied.difference_update(gadget.attachments)
                    del selected[variable]
                used_hubs.difference_update(tokens)

        visit(start, 0, None)

    ordered = list(supports.values())
    minimal = inclusion_minimal(ordered)
    return {
        "status": "PASS" if complete else "TIME_LIMIT",
        "complete": complete,
        "target_length": target,
        "include_linked_gadgets": include_linked,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "statistics": dict(sorted(statistics.items())),
        "distinct_supports": len(ordered),
        "minimal_supports": len(minimal),
        "support_size_distribution": {
            str(key): value for key, value in sorted(Counter(
                item["support_size"] for item in minimal
            ).items())
        },
        "supports": minimal,
    }


def read_json(path: Path) -> dict:
    return json.loads(
        gzip.open(path, "rt").read() if path.suffix == ".gz" else path.read_text()
    )


def cegar_seed_records(path: Path, target: int,
                       forbidden_supports: list[list[int]]) -> list[dict]:
    payload = read_json(path)
    unary = {
        support[0] for support in forbidden_supports if len(support) == 1
    }
    binary = {
        tuple(support) for support in forbidden_supports if len(support) == 2
    }
    records = {}
    for record in payload["cycle_cuts"]:
        if record["cycle_length"] != target:
            continue
        support = tuple(sorted(-literal for literal in record["clause"]))
        if any(variable in unary for variable in support):
            continue
        if any(
            tuple(sorted((support[left], support[right]))) in binary
            for left in range(len(support))
            for right in range(left + 1, len(support))
        ):
            continue
        records.setdefault(support, {
            "support": list(support),
            "support_size": len(support),
            "gadgets": record["gadgets"],
            "source": "independently verified prior CEGAR cut",
            "source_cycle": record["cycle"],
        })
    return list(records.values())


def unary_seed_records(core, target: int,
                       forbidden_supports: list[list[int]]) -> list[dict]:
    """Exhaust all one-gadget supports by direct graph materialization."""
    forbidden_unary = {
        support[0] for support in forbidden_supports if len(support) == 1
    }
    gadgets, _, _, _ = gadget_catalog(core)
    records = []
    for variable, gadget in gadgets.items():
        if variable in forbidden_unary:
            continue
        triples = list(gadget.triples) if gadget.kind == "triple" else []
        linked = gadget.triples if gadget.kind == "linked_pairs" else None
        adjacency = materialize(core, triples, linked)[1]
        cycle = edge_path_cycle(adjacency, target)
        if cycle is None:
            continue
        records.append({
            "support": [variable],
            "support_size": 1,
            "gadgets": [gadget.to_json()],
            "source": "exhaustive direct one-gadget materialization",
            "source_cycle": list(cycle),
        })
    return records


def write_json(path: Path | None, payload: dict) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path is None:
        print(rendered, end="")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".gz":
        path.write_bytes(gzip.compress(rendered.encode(), mtime=0))
    else:
        path.write_text(rendered)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--length", type=int, default=16)
    parser.add_argument("--triples-only", action="store_true")
    parser.add_argument("--max-seconds", type=float)
    parser.add_argument("--conflicts-per-solve", type=int, default=100_000)
    parser.add_argument("--method", choices=("sat", "dfs"), default="sat")
    parser.add_argument(
        "--no-extension-filter", action="store_true",
        help="enumerate structurally co-selectable supports without requiring a Phi4,8 exact-cover extension",
    )
    parser.add_argument("--forbid-catalog", type=Path)
    parser.add_argument("--resume-catalog", type=Path)
    parser.add_argument(
        "--merge-catalog", type=Path, action="append", default=[],
        help="merge supports from another partial catalog (repeatable)",
    )
    parser.add_argument("--seed-cegar", type=Path)
    parser.add_argument(
        "--seed-unary", action="store_true",
        help="exhaustively seed every one-gadget target-cycle support",
    )
    parser.add_argument(
        "--support-size", type=int,
        help="enumerate one exact support-size stratum (1 through floor(L/3))",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    core = build_core(args.j, args.a, args.c)
    forbidden = None
    if args.forbid_catalog is not None:
        forbidden = [
            item["support"] for item in read_json(args.forbid_catalog)["supports"]
        ]
    existing = (
        read_json(args.resume_catalog)["supports"]
        if args.resume_catalog is not None else None
    )
    if args.merge_catalog:
        combined = {
            tuple(record["support"]): record for record in (existing or [])
        }
        for path in args.merge_catalog:
            for record in read_json(path)["supports"]:
                combined.setdefault(tuple(record["support"]), record)
        existing = list(combined.values())
    if args.seed_cegar is not None:
        seeded = cegar_seed_records(
            args.seed_cegar, args.length, forbidden or [],
        )
        combined = {
            tuple(record["support"]): record for record in (existing or [])
        }
        for record in seeded:
            combined.setdefault(tuple(record["support"]), record)
        existing = list(combined.values())
    if args.seed_unary:
        combined = {
            tuple(record["support"]): record for record in (existing or [])
        }
        for record in unary_seed_records(core, args.length, forbidden or []):
            combined.setdefault(tuple(record["support"]), record)
        existing = list(combined.values())
    result = (
        compile_length_sat(
            core, args.length, args.max_seconds,
            conflicts_per_solve=args.conflicts_per_solve,
            forbidden_supports=forbidden,
            existing_records=existing,
            support_size=args.support_size,
            require_extension=not args.no_extension_filter,
        )
        if args.method == "sat" else
        compile_length(
            core, args.length, not args.triples_only, args.max_seconds,
        )
    )
    write_json(args.output, result)


if __name__ == "__main__":
    main()
