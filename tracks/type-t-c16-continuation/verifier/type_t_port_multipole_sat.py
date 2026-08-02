#!/usr/bin/env python3
"""Unlabelled exact-cover and cycle-cut SAT search for cubic multipoles."""

from __future__ import annotations

import argparse
import gzip
import json
import math
import random
import time
from collections import Counter
from pathlib import Path

import networkx as nx
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from type_t_port_core_export import build_core
from type_t_port_triples import (
    LinkedGadget,
    Triple,
    allowed_triples,
    linked_gadgets,
    minimum_cubic_parameters,
    path_incompatibilities,
    powers_up_to,
    safe_pairs,
)
from type_t_port_multiswitch import cycle_edges, full_cycles, update_cycles


def build_catalog(core):
    normal = minimum_cubic_parameters(core.j)
    completion_order = core.order + normal["new_cubic_vertices"]
    deficient = core.deficient_vertices()
    same_bad, _ = path_incompatibilities(core, 2, completion_order)
    pairs = safe_pairs(deficient, same_bad)
    triples = allowed_triples(deficient, pairs)
    gadgets: list[LinkedGadget] = []
    cross_bad = {}
    if core.j % 2 == 0:
        cross_bad, _ = path_incompatibilities(core, 3, completion_order)
        gadgets = linked_gadgets(deficient, pairs, cross_bad)
    return normal, pairs, triples, gadgets, same_bad, cross_bad


def build_exact_cover_cnf(core, triples: list[Triple],
                          gadgets: list[LinkedGadget]):
    pool = IDPool()
    triple_var = {triple: pool.id(("triple", triple)) for triple in triples}
    gadget_var = {gadget: pool.id(("linked", gadget)) for gadget in gadgets}
    incident = {vertex: [] for vertex in core.deficient_vertices()}
    for triple, variable in triple_var.items():
        for vertex in triple:
            incident[vertex].append(variable)
    for gadget, variable in gadget_var.items():
        for vertex in gadget[0] + gadget[1]:
            incident[vertex].append(variable)
    clauses: list[list[int]] = []
    ranges = {}
    for vertex in core.deficient_vertices():
        start = len(clauses)
        clauses.extend(CardEnc.equals(
            incident[vertex], 1, vpool=pool, encoding=EncType.seqcounter,
        ).clauses)
        ranges[vertex] = (start, len(clauses))
    if core.j % 2 == 0:
        clauses.extend(CardEnc.equals(
            list(gadget_var.values()), 1, vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses)
    elif gadget_var:
        raise AssertionError("odd-j completion unexpectedly has linked gadgets")
    return pool, triple_var, gadget_var, clauses, ranges


def random_exact_cover(core, triples: list[Triple], gadgets: list[LinkedGadget],
                       seed: int, restarts: int = 100,
                       node_limit: int = 20_000) -> dict:
    """Randomized Algorithm-X feasibility probe, independent of SAT."""
    rng = random.Random(seed)
    deficient = frozenset(core.deficient_vertices())
    by_vertex = {vertex: [] for vertex in deficient}
    for triple in triples:
        for vertex in triple:
            by_vertex[vertex].append(triple)
    starts: list[LinkedGadget | None]
    starts = list(gadgets) if core.j % 2 == 0 else [None]
    rng.shuffle(starts)
    nodes = 0

    class SearchLimit(Exception):
        pass

    def cover(uncovered: frozenset[int], chosen: list[Triple]):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit:
            raise SearchLimit
        if not uncovered:
            return list(chosen)
        feasible = {
            vertex: [
                triple for triple in by_vertex[vertex]
                if set(triple) <= uncovered
            ] for vertex in uncovered
        }
        vertex = min(uncovered, key=lambda item: len(feasible[item]))
        options = feasible[vertex]
        rng.shuffle(options)
        for triple in options:
            result = cover(uncovered - set(triple), chosen + [triple])
            if result is not None:
                return result
        return None

    try:
        for attempt, gadget in enumerate(starts[:restarts], 1):
            occupied = set(gadget[0] + gadget[1]) if gadget is not None else set()
            result = cover(deficient - occupied, [])
            if result is not None:
                return {
                    "status": "SAT",
                    "seed": seed,
                    "attempts": attempt,
                    "search_nodes": nodes,
                    "triples": [list(item) for item in sorted(result)],
                    "linked_pairs": (
                        [list(pair) for pair in gadget] if gadget is not None else None
                    ),
                }
    except SearchLimit:
        pass
    return {
        "status": "UNKNOWN",
        "seed": seed,
        "attempts": min(restarts, len(starts)),
        "search_nodes": nodes,
        "node_limit": node_limit,
    }


def selected_partition(model: set[int], triple_var, gadget_var):
    triples = sorted(
        triple for triple, variable in triple_var.items() if variable in model
    )
    selected_gadgets = [
        gadget for gadget, variable in gadget_var.items() if variable in model
    ]
    if len(selected_gadgets) > 1:
        raise AssertionError("more than one linked gadget selected")
    return triples, selected_gadgets[0] if selected_gadgets else None


def partition_from_payload_for_phase(completion: dict):
    triples = [tuple(sorted(item)) for item in completion["triples"]]
    linked = completion.get("linked_pairs")
    gadget = None
    if linked is not None:
        gadget = tuple(sorted(tuple(sorted(pair)) for pair in linked))
    return triples, gadget


def materialize(core, triples: list[Triple], gadget: LinkedGadget | None,
                triple_var=None, gadget_var=None):
    graph = nx.Graph()
    graph.add_nodes_from(range(core.order))
    graph.add_edges_from(core.edges)
    hub_variable: dict[int, int] = {}
    hub_records = []
    next_vertex = core.order
    for triple in sorted(triples):
        hub = next_vertex
        next_vertex += 1
        graph.add_edges_from((hub, vertex) for vertex in triple)
        if triple_var is not None:
            hub_variable[hub] = triple_var[triple]
        hub_records.append({"vertex": hub, "kind": "triple", "attachments": list(triple)})
    if gadget is not None:
        left_hub, right_hub = next_vertex, next_vertex + 1
        next_vertex += 2
        graph.add_edges_from((left_hub, vertex) for vertex in gadget[0])
        graph.add_edges_from((right_hub, vertex) for vertex in gadget[1])
        graph.add_edge(left_hub, right_hub)
        if gadget_var is not None:
            variable = gadget_var[gadget]
            hub_variable[left_hub] = variable
            hub_variable[right_hub] = variable
        hub_records.extend((
            {"vertex": left_hub, "kind": "linked_pair", "attachments": list(gadget[0])},
            {"vertex": right_hub, "kind": "linked_pair", "attachments": list(gadget[1])},
        ))
    adjacency = tuple(
        frozenset(graph.neighbors(vertex)) for vertex in range(next_vertex)
    )
    return graph, adjacency, hub_variable, hub_records


def enumerate_cycles_exact(adjacency, length: int, limit: int):
    """Enumerate canonical undirected cycles, stopping at ``limit``."""
    cycles = []
    truncated = False
    for start in range(len(adjacency)):
        path = [start]
        used = {start}

        def visit(vertex: int) -> None:
            nonlocal truncated
            if len(cycles) >= limit:
                truncated = True
                return
            if len(path) == length:
                if start in adjacency[vertex] and path[1] < path[-1]:
                    cycles.append(tuple(path))
                return
            for neighbor in adjacency[vertex]:
                if neighbor <= start or neighbor in used:
                    continue
                used.add(neighbor)
                path.append(neighbor)
                visit(neighbor)
                path.pop()
                used.remove(neighbor)
                if truncated:
                    return

        visit(start)
        if truncated:
            break
    return cycles, truncated


def first_cycle_profile(adjacency, lengths: tuple[int, ...]) -> dict:
    witnesses = {}
    for length in lengths:
        cycles, _ = enumerate_cycles_exact(adjacency, length, 1)
        if cycles:
            witnesses[str(length)] = list(cycles[0])
    return witnesses


def graph_encodings(graph) -> dict[str, str]:
    return {
        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
        "sparse6": nx.to_sparse6_bytes(graph, header=False).decode().strip(),
    }


def local_exchange_search(core, triples_catalog: list[Triple],
                          gadgets: list[LinkedGadget], seed: int,
                          steps: int, target_length: int = 16) -> dict:
    """Randomized 2--4-triple exchanges preserving an exact cover."""
    rng = random.Random(seed)
    pool, triple_var, gadget_var, clauses, _ = build_exact_cover_cnf(
        core, triples_catalog, gadgets,
    )
    del pool
    with Solver(name="glucose3", bootstrap_with=clauses) as solver:
        if not solver.solve():
            return {"status": "BASE_UNSAT", "steps": 0}
        model = set(solver.get_model())
    triples, gadget = selected_partition(model, triple_var, gadget_var)
    triples = list(sorted(triples))
    graph, adjacency_frozen, _, _ = materialize(core, triples, gadget)
    adjacency = [set(row) for row in adjacency_frozen]
    triple_hubs = list(range(core.order, core.order + len(triples)))
    catalog_set = set(triples_catalog)
    by_vertex = {vertex: [] for vertex in core.deficient_vertices()}
    for triple in triples_catalog:
        for vertex in triple:
            by_vertex[vertex].append(triple)

    cycles = {4: full_cycles(adjacency, 4), 8: full_cycles(adjacency, 8)}
    cycles16_initialized = (
        target_length >= 16 and not cycles[4] and not cycles[8]
    )
    if cycles16_initialized:
        cycles[16] = full_cycles(adjacency, 16)

    def score(state):
        return (
            len(state.get(4, ())), len(state.get(8, ())),
            len(state.get(16, ())) if 16 in state else 10**9,
        )

    def alternative_partition(vertices: frozenset[int], count: int,
                              old: frozenset[Triple]):
        chosen: list[Triple] = []

        def visit(remaining: frozenset[int]):
            if not remaining:
                candidate = frozenset(chosen)
                return list(chosen) if candidate != old else None
            vertex = min(
                remaining,
                key=lambda item: sum(set(triple) <= remaining
                                     for triple in by_vertex[item]),
            )
            options = [
                triple for triple in by_vertex[vertex]
                if triple in catalog_set and set(triple) <= remaining
            ]
            rng.shuffle(options)
            for triple in options:
                chosen.append(triple)
                result = visit(remaining - set(triple))
                if result is not None:
                    return result
                chosen.pop()
            return None

        result = visit(vertices)
        return result if result is not None and len(result) == count else None

    best_score = score(cycles)
    best_triples = list(triples)
    best_cycles = {length: set(found) for length, found in cycles.items()}
    accepted = 0
    started = time.monotonic()
    performed = 0
    for iteration in range(steps):
        performed = iteration + 1
        active_length = 4 if cycles[4] else 8 if cycles[8] else 16
        target_cycle = rng.choice(tuple(cycles[active_length]))
        implicated = [
            vertex - core.order for vertex in target_cycle
            if vertex in triple_hubs
        ]
        count = rng.choices((2, 3, 4), weights=(65, 28, 7))[0]
        selected = set(implicated[:1]) if implicated else set()
        while len(selected) < count:
            selected.add(rng.randrange(len(triples)))
        selected = sorted(selected)
        old_triples = [triples[index] for index in selected]
        vertices = frozenset(vertex for triple in old_triples for vertex in triple)
        replacement = alternative_partition(
            vertices, count, frozenset(old_triples),
        )
        if replacement is None:
            continue
        rng.shuffle(replacement)
        removed = set()
        added = set()
        for index, old, new in zip(selected, old_triples, replacement, strict=True):
            hub = core.order + index
            removed.update((min(hub, vertex), max(hub, vertex)) for vertex in old)
            added.update((min(hub, vertex), max(hub, vertex)) for vertex in new)
        for u, v in removed:
            adjacency[u].remove(v)
            adjacency[v].remove(u)
        for u, v in added:
            adjacency[u].add(v)
            adjacency[v].add(u)

        proposed = {
            4: update_cycles(cycles[4], adjacency, removed, added, 4),
            8: update_cycles(cycles[8], adjacency, removed, added, 8),
        }
        if target_length >= 16 and not proposed[4] and not proposed[8]:
            if cycles16_initialized:
                proposed[16] = update_cycles(
                    cycles[16], adjacency, removed, added, 16,
                )
            else:
                proposed[16] = full_cycles(adjacency, 16)
        current_score = score(cycles)
        proposed_score = score(proposed)
        current_scalar = current_score[0] * 10**8 + current_score[1] * 10**5 + current_score[2]
        proposed_scalar = proposed_score[0] * 10**8 + proposed_score[1] * 10**5 + proposed_score[2]
        temperature = max(0.05, 1000 * (1 - iteration / max(steps, 1)))
        accept = (
            proposed_scalar <= current_scalar or
            rng.random() < math.exp(
                max(-700, (current_scalar - proposed_scalar) / temperature),
            )
        )
        if accept:
            for index, new in zip(selected, replacement, strict=True):
                triples[index] = new
            cycles.update(proposed)
            if 16 in proposed:
                cycles16_initialized = True
            accepted += 1
            if score(cycles) < best_score:
                best_score = score(cycles)
                best_triples = list(triples)
                best_cycles = {
                    length: set(found) for length, found in cycles.items()
                }
        else:
            for u, v in added:
                adjacency[u].remove(v)
                adjacency[v].remove(u)
            for u, v in removed:
                adjacency[u].add(v)
                adjacency[v].add(u)
        if ((target_length == 8 and best_score[:2] == (0, 0)) or
                (target_length >= 16 and best_score == (0, 0, 0))):
            break

    best_graph, best_adjacency, _, _ = materialize(core, best_triples, gadget)
    witnesses = first_cycle_profile(
        best_adjacency, powers_up_to(best_graph.number_of_nodes()),
    )
    return {
        "status": (
            "C4_C8_FREE" if target_length == 8 and best_score[:2] == (0, 0)
            else "C4_C8_C16_FREE" if best_score == (0, 0, 0)
            else "HEURISTIC_LIMIT"
        ),
        "parameters": {"j": core.j, "Y": core.Y, "a": core.a, "c": core.c},
        "seed": seed,
        "step_limit": steps,
        "target_length": target_length,
        "steps_performed": performed,
        "accepted_exchanges": accepted,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "best_short_cycle_counts": {
            str(length): (
                len(best_cycles[length]) if length in best_cycles else None
            ) for length in (4, 8, 16)
        },
        "power_cycle_witnesses": witnesses,
        "completion": {
            "triples": [list(item) for item in best_triples],
            "linked_pairs": [list(pair) for pair in gadget] if gadget else None,
            "edges": [list(edge) for edge in sorted(best_graph.edges())],
            **graph_encodings(best_graph),
        },
    }


def write_dimacs(path: Path, clauses: list[list[int]], variables: int) -> None:
    formula = CNF(from_clauses=clauses)
    formula.nv = max(formula.nv, variables)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".gz":
        text = f"p cnf {formula.nv} {len(formula.clauses)}\n" + "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in formula.clauses
        )
        path.write_bytes(gzip.compress(text.encode(), mtime=0))
    else:
        formula.to_file(str(path))


def write_proof(path: Path, proof: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(proof) + "\n"
    if path.suffix == ".gz":
        path.write_bytes(gzip.compress(text.encode(), mtime=0))
    else:
        path.write_text(text)


def exact_search(core, max_seconds: float, max_iterations: int,
                 cycle_limit: int, seed: int, cnf_path: Path | None,
                 proof_path: Path | None, solver_name: str = "cadical195",
                 conflicts_per_solve: int = 100_000,
                 resume: dict | None = None,
                 phase_completion: dict | None = None) -> dict:
    normal, pairs, triples, gadgets, same_bad, cross_bad = build_catalog(core)
    lengths = powers_up_to(core.order + normal["new_cubic_vertices"])
    if resume is not None:
        assert resume["status"] == "UNKNOWN"
        assert resume["parameters"] == {
            "j": core.j, "Y": core.Y, "a": core.a, "c": core.c,
        }
    heuristic = (
        resume["heuristic_exact_cover"] if resume is not None
        else random_exact_cover(core, triples, gadgets, seed)
    )
    if heuristic["status"] == "SAT":
        h_triples = [tuple(item) for item in heuristic["triples"]]
        h_gadget = (
            tuple(tuple(pair) for pair in heuristic["linked_pairs"])
            if heuristic["linked_pairs"] is not None else None
        )
        h_graph, h_adjacency, _, _ = materialize(core, h_triples, h_gadget)
        heuristic["power_cycle_witnesses"] = first_cycle_profile(h_adjacency, lengths)
        heuristic.update(graph_encodings(h_graph))

    pool, triple_var, gadget_var, clauses, _ranges = build_exact_cover_cnf(
        core, triples, gadgets,
    )
    variable_gadget = {
        variable: {
            "variable": variable,
            "kind": "triple",
            "attachments": list(triple),
        } for triple, variable in triple_var.items()
    }
    variable_gadget.update({
        variable: {
            "variable": variable,
            "kind": "linked_pairs",
            "pairs": [list(pair) for pair in gadget],
        } for gadget, variable in gadget_var.items()
    })
    base_clauses = len(clauses)
    learned: dict[tuple[int, ...], dict] = {}
    models_by_shortest = Counter()
    cuts_by_length = Counter()
    cuts_by_size = Counter()
    iterations = 0
    result = "UNKNOWN"
    last_partition = None
    last_witnesses = (
        dict(resume.get("last_power_cycle_witnesses", {}))
        if resume is not None else {}
    )
    proof = None
    solve_budget_exhaustions = 0
    previous_elapsed = 0.0
    if resume is not None:
        previous_elapsed = float(resume["elapsed_seconds"])
        previous_sat = resume["sat"]
        iterations = int(previous_sat["models_checked"])
        solve_budget_exhaustions = int(previous_sat["solve_budget_exhaustions"])
        models_by_shortest.update({
            int(key): value for key, value
            in previous_sat["models_by_shortest_power_cycle"].items()
        })
        for record in resume["cycle_cuts"]:
            clause = tuple(record["clause"])
            if clause not in learned:
                learned[clause] = record
                clauses.append(list(clause))
                cuts_by_length[record["cycle_length"]] += 1
                cuts_by_size[len(clause)] += 1
    started = time.monotonic()

    with Solver(
        name=solver_name, bootstrap_with=clauses,
        with_proof=proof_path is not None,
    ) as solver:
        if phase_completion is not None:
            phase_triples, phase_gadget = partition_from_payload_for_phase(
                phase_completion,
            )
            selected_variables = {
                triple_var[triple] for triple in phase_triples
            }
            if phase_gadget is not None:
                selected_variables.add(gadget_var[phase_gadget])
            solver.set_phases([
                variable if variable in selected_variables else -variable
                for variable in list(triple_var.values()) + list(gadget_var.values())
            ])
        while (iterations < max_iterations and
               time.monotonic() - started < max_seconds):
            solver.conf_budget(conflicts_per_solve)
            solve_result = solver.solve_limited(expect_interrupt=True)
            if solve_result is None:
                solve_budget_exhaustions += 1
                continue
            if not solve_result:
                result = "UNSAT"
                proof = solver.get_proof() if proof_path is not None else None
                break
            iterations += 1
            model = set(solver.get_model())
            selected_triples, selected_gadget = selected_partition(
                model, triple_var, gadget_var,
            )
            graph, adjacency, hub_variable, hubs = materialize(
                core, selected_triples, selected_gadget, triple_var, gadget_var,
            )
            if graph.number_of_nodes() != core.order + normal["new_cubic_vertices"]:
                raise AssertionError("wrong completion order")
            if min(dict(graph.degree()).values()) < 3 or not nx.is_connected(graph):
                raise AssertionError("invalid cubic multipole completion")
            last_partition = (selected_triples, selected_gadget, graph, hubs)
            last_witnesses = {}
            shortest = None
            new_cuts = []
            for length in lengths:
                cycles, _truncated = enumerate_cycles_exact(
                    adjacency, length, cycle_limit,
                )
                if not cycles:
                    continue
                shortest = length
                last_witnesses[str(length)] = list(cycles[0])
                for cycle in cycles:
                    variables = sorted({
                        hub_variable[vertex] for vertex in cycle
                        if vertex in hub_variable
                    })
                    if not variables:
                        raise AssertionError("dyadic cycle uses no selected hub")
                    clause = tuple(-variable for variable in variables)
                    if clause not in learned:
                        record = {
                            "cycle_length": length,
                            "cycle": list(cycle),
                            "clause": list(clause),
                            "gadgets": [variable_gadget[item] for item in variables],
                        }
                        learned[clause] = record
                        new_cuts.append(clause)
                        cuts_by_length[length] += 1
                        cuts_by_size[len(clause)] += 1
                break
            if shortest is None:
                result = "SAT"
                break
            models_by_shortest[shortest] += 1
            if not new_cuts:
                raise AssertionError("rejected model produced no new cycle cut")
            for clause in new_cuts:
                solver.add_clause(list(clause))
                clauses.append(list(clause))

    elapsed = time.monotonic() - started
    if cnf_path is not None:
        write_dimacs(cnf_path, clauses, pool.top)
    if proof_path is not None and result == "UNSAT":
        write_proof(proof_path, proof or [])

    independent = {}
    if result == "UNSAT":
        for name in ("cadical195", "lingeling"):
            with Solver(name=name, bootstrap_with=clauses) as solver:
                independent[name] = "UNSAT" if not solver.solve() else "SAT"

    output = {
        "status": result,
        "parameters": {"j": core.j, "Y": core.Y, "a": core.a, "c": core.c},
        "core_order": core.order,
        "completion_order": core.order + normal["new_cubic_vertices"],
        "minimum_cubic_completion": normal,
        "forbidden_cycle_lengths": list(lengths),
        "catalog": {
            "allowed_pairs": len(pairs),
            "allowed_triples": len(triples),
            "linked_pair_gadgets": len(gadgets),
            "same_hub_incompatible_pairs": len(same_bad),
            "opposite_hub_incompatible_pairs": len(cross_bad),
        },
        "heuristic_exact_cover": heuristic,
        "sat": {
            "solver": solver_name,
            "conflicts_per_solve": conflicts_per_solve,
            "solve_budget_exhaustions": solve_budget_exhaustions,
            "variables": pool.top,
            "base_clauses": base_clauses,
            "learned_cycle_clauses": len(learned),
            "final_clauses": len(clauses),
            "models_checked": iterations,
            "models_by_shortest_power_cycle": {
                str(key): value for key, value in sorted(models_by_shortest.items())
            },
            "cycle_cuts_by_source_length": {
                str(key): value for key, value in sorted(cuts_by_length.items())
            },
            "cycle_cuts_by_clause_size": {
                str(key): value for key, value in sorted(cuts_by_size.items())
            },
            "independent_final_cnf_solvers": independent,
        },
        "elapsed_seconds": round(previous_elapsed + elapsed, 6),
        "elapsed_seconds_this_run": round(elapsed, 6),
        "resumed": resume is not None,
        "phase_completion_supplied": phase_completion is not None,
        "limits": {
            "max_seconds": max_seconds,
            "max_iterations": max_iterations,
            "cycles_per_shortest_length_per_model": cycle_limit,
        },
        "last_power_cycle_witnesses": last_witnesses,
        "cycle_cuts": list(learned.values()),
    }
    if last_partition is not None:
        selected_triples, selected_gadget, graph, hubs = last_partition
        prefix = "" if result == "SAT" else "last_rejected_"
        output[prefix + "completion"] = {
            "triples": [list(item) for item in selected_triples],
            "linked_pairs": (
                [list(pair) for pair in selected_gadget]
                if selected_gadget is not None else None
            ),
            "hubs": hubs,
            "edges": [list(edge) for edge in sorted(graph.edges())],
            **graph_encodings(graph),
        }
    elif resume is not None:
        for key in ("completion", "last_rejected_completion"):
            if key in resume:
                output[key] = resume[key]
    if cnf_path is not None:
        output["cnf"] = str(cnf_path)
    if proof_path is not None and result == "UNSAT":
        output["proof"] = str(proof_path)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--max-seconds", type=float, default=300.0)
    parser.add_argument("--max-iterations", type=int, default=100_000)
    parser.add_argument("--cycle-limit", type=int, default=500)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--conflicts-per-solve", type=int, default=100_000)
    parser.add_argument("--local-steps", type=int, default=0)
    parser.add_argument("--local-target-length", type=int, choices=(8, 16), default=16)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--phase-completion", type=Path)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    core = build_core(args.j, args.a, args.c)
    if args.local_steps:
        _, _, triples, gadgets, _, _ = build_catalog(core)
        result = local_exchange_search(
            core, triples, gadgets, args.seed, args.local_steps,
            args.local_target_length,
        )
    else:
        resume = None
        if args.resume is not None:
            resume = json.loads(
                gzip.open(args.resume, "rt").read()
                if args.resume.suffix == ".gz" else args.resume.read_text()
            )
        phase_completion = None
        if args.phase_completion is not None:
            phase_payload = json.loads(
                gzip.open(args.phase_completion, "rt").read()
                if args.phase_completion.suffix == ".gz"
                else args.phase_completion.read_text()
            )
            phase_completion = phase_payload.get("completion", phase_payload)
        result = exact_search(
            core, args.max_seconds, args.max_iterations, args.cycle_limit,
            args.seed, args.cnf, args.proof, args.solver,
            args.conflicts_per_solve, resume, phase_completion,
        )
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
