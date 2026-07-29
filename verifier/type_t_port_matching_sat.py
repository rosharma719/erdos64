#!/usr/bin/env python3
"""Perfect-matching completion search for the expanded Type-T port core.

The exact mode is a SAT/CEGAR formulation.  Boolean variables are safe edges
between degree-two core vertices, exact-one constraints make them a perfect
matching, and every discovered dyadic cycle contributes a sound blocking
clause containing precisely the matching edges on that cycle.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import Counter
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose3

from type_t_port_core_export import build_core, graph_encodings


def powers_up_to(order: int) -> tuple[int, ...]:
    values = []
    value = 4
    while value <= order:
        values.append(value)
        value *= 2
    return tuple(values)


def one_edge_incompatibilities(core, lengths: tuple[int, ...]):
    """Pairs closed to a forbidden cycle by one matching edge."""
    deficient = set(core.deficient_vertices())
    targets = {length - 1: length for length in lengths}
    maximum = max(targets, default=0)
    bad: dict[tuple[int, int], set[int]] = {}
    adjacency = core.adjacency()
    for start in deficient:
        used = {start}

        def visit(vertex: int, depth: int) -> None:
            if depth in targets and vertex in deficient and start < vertex:
                bad.setdefault((start, vertex), set()).add(targets[depth])
            if depth == maximum:
                return
            for neighbor in adjacency[vertex]:
                if neighbor not in used:
                    used.add(neighbor)
                    visit(neighbor, depth + 1)
                    used.remove(neighbor)

        visit(start, 0)
    return bad


def safe_edges(core, lengths: tuple[int, ...]):
    deficient = core.deficient_vertices()
    core_edges = set(core.edges)
    incompatible = one_edge_incompatibilities(core, lengths)
    candidates = [
        (u, v) for index, u in enumerate(deficient) for v in deficient[index + 1:]
        if (u, v) not in core_edges and (u, v) not in incompatible
    ]
    return candidates, incompatible


def matching_feasibility(core, candidates):
    import networkx as nx

    graph = nx.Graph()
    graph.add_nodes_from(core.deficient_vertices())
    graph.add_edges_from(candidates)
    matching = nx.max_weight_matching(graph, maxcardinality=True)
    degrees = dict(graph.degree())
    return {
        "safe_edges": len(candidates),
        "minimum_compatibility_degree": min(degrees.values()),
        "maximum_compatibility_degree": max(degrees.values()),
        "maximum_matching_edges": len(matching),
        "perfect_matching_exists": len(matching) * 2 == len(degrees),
    }


def enumerate_cycles_exact(adjacency, length: int, limit: int):
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


def build_cnf(core, candidates, encoding: str):
    pool = IDPool()
    edge_var = {edge: pool.id(("matching_edge", edge)) for edge in candidates}
    incident = {vertex: [] for vertex in core.deficient_vertices()}
    for edge, variable in edge_var.items():
        incident[edge[0]].append(variable)
        incident[edge[1]].append(variable)
    clauses = []
    constraint_clause_ranges = {}
    cardinality_encoding = {
        "sequential": EncType.seqcounter,
        "pairwise": EncType.pairwise,
    }[encoding]
    for vertex in core.deficient_vertices():
        start = len(clauses)
        clauses.extend(CardEnc.equals(
            lits=incident[vertex], bound=1, vpool=pool,
            encoding=cardinality_encoding,
        ).clauses)
        constraint_clause_ranges[vertex] = (start, len(clauses))
    return pool, edge_var, clauses, constraint_clause_ranges


def write_dimacs(path: Path, clauses: list[list[int]], variables: int) -> None:
    cnf = CNF(from_clauses=clauses)
    cnf.nv = max(cnf.nv, variables)
    path.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(path))


def heuristic_search(core, seed: int, steps: int):
    """Seeded 2-switch descent for a C4/C8-free perfect matching."""
    rng = random.Random(seed)
    deficient = list(core.deficient_vertices())
    core_edges = set(core.edges)

    for _ in range(10000):
        rng.shuffle(deficient)
        matching = [
            tuple(sorted((deficient[index], deficient[index + 1])))
            for index in range(0, len(deficient), 2)
        ]
        if not core_edges.intersection(matching):
            break
    else:
        raise RuntimeError("failed to seed a non-core perfect matching")

    def evaluate(candidate):
        adjacency = [set(row) for row in core.adjacency()]
        for u, v in candidate:
            adjacency[u].add(v)
            adjacency[v].add(u)
        adjacency = tuple(frozenset(row) for row in adjacency)
        c4, _ = enumerate_cycles_exact(adjacency, 4, 1_000_000)
        c8, _ = enumerate_cycles_exact(adjacency, 8, 1_000_000)
        return 30 * len(c4) + len(c8), (len(c4), len(c8)), c4 + c8

    score, counts, bad_cycles = evaluate(matching)
    best = (score, counts, list(matching))
    start = time.monotonic()
    performed = 0
    for iteration in range(steps):
        performed = iteration + 1
        edge_index = {edge: index for index, edge in enumerate(matching)}
        cycle = rng.choice(bad_cycles) if bad_cycles and rng.random() < 0.85 else None
        implicated = []
        if cycle:
            for index, u in enumerate(cycle):
                v = cycle[(index + 1) % len(cycle)]
                edge = (u, v) if u < v else (v, u)
                if edge in edge_index:
                    implicated.append(edge_index[edge])
        first = rng.choice(implicated) if implicated else rng.randrange(len(matching))
        second = rng.randrange(len(matching) - 1)
        if second >= first:
            second += 1
        (a, b), (c, d) = matching[first], matching[second]
        switches = [
            (tuple(sorted((a, c))), tuple(sorted((b, d)))),
            (tuple(sorted((a, d))), tuple(sorted((b, c)))),
        ]
        rng.shuffle(switches)
        for edge_one, edge_two in switches:
            if edge_one in core_edges or edge_two in core_edges:
                continue
            old = matching[first], matching[second]
            matching[first], matching[second] = edge_one, edge_two
            new_score, new_counts, new_bad = evaluate(matching)
            temperature = max(0.05, 4.0 * (1.0 - iteration / max(steps, 1)))
            if new_score <= score or rng.random() < math.exp((score - new_score) / temperature):
                score, counts, bad_cycles = new_score, new_counts, new_bad
            else:
                matching[first], matching[second] = old
            break
        if score < best[0]:
            best = (score, counts, list(matching))
        if counts == (0, 0):
            break

    score, counts, matching = best
    adjacency = [set(row) for row in core.adjacency()]
    for u, v in matching:
        adjacency[u].add(v)
        adjacency[v].add(u)
    adjacency = tuple(frozenset(row) for row in adjacency)
    witnesses = {}
    for length in powers_up_to(core.order):
        cycles, _ = enumerate_cycles_exact(adjacency, length, 1)
        if cycles:
            witnesses[str(length)] = list(cycles[0])
    return {
        "status": "C4_C8_FREE" if counts == (0, 0) else "HEURISTIC_LIMIT",
        "method": "seeded simulated-annealing 2-switch descent",
        "parameters": {"j": core.j, "Y": core.Y, "a": core.a, "c": core.c},
        "seed": seed,
        "step_limit": steps,
        "steps_performed": performed,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "C4_count": counts[0],
        "C8_count": counts[1],
        "power_cycle_witnesses": witnesses,
        "matching_edges": [list(edge) for edge in sorted(matching)],
        **graph_encodings(core, matching),
    }


def exact_search(core, max_seconds: float, max_iterations: int,
                 cycle_limit: int, cnf_path: Path | None,
                 proof_path: Path | None, encoding: str):
    lengths = powers_up_to(core.order)
    candidates, incompatible = safe_edges(core, lengths)
    feasibility = matching_feasibility(core, candidates)
    pool, edge_var, clauses, _constraint_clause_ranges = build_cnf(
        core, candidates, encoding,
    )
    base_clause_count = len(clauses)
    start_time = time.monotonic()
    cycle_cuts = Counter()
    learned_cuts: set[tuple[int, ...]] = set()
    iterations = 0
    models_by_shortest = Counter()
    result = "UNKNOWN"
    matching = None
    final_witnesses = {}
    proof = None

    with Glucose3(bootstrap_with=clauses, with_proof=proof_path is not None) as solver:
        while iterations < max_iterations and time.monotonic() - start_time < max_seconds:
            if not solver.solve():
                result = "UNSAT"
                proof = solver.get_proof() if proof_path is not None else None
                break
            iterations += 1
            model = set(solver.get_model())
            matching = [edge for edge, variable in edge_var.items() if variable in model]
            assert len(matching) * 2 == len(core.deficient_vertices())
            adjacency = [set(row) for row in core.adjacency()]
            for u, v in matching:
                adjacency[u].add(v)
                adjacency[v].add(u)
            adjacency = tuple(frozenset(row) for row in adjacency)

            cuts_this_model = set()
            shortest = None
            final_witnesses = {}
            for length in lengths:
                cycles, truncated = enumerate_cycles_exact(adjacency, length, cycle_limit)
                if cycles:
                    shortest = length
                    final_witnesses[str(length)] = list(cycles[0])
                for cycle in cycles:
                    selected = []
                    for index, u in enumerate(cycle):
                        v = cycle[(index + 1) % len(cycle)]
                        edge = (u, v) if u < v else (v, u)
                        if edge in edge_var:
                            selected.append(edge_var[edge])
                    if not selected:
                        raise AssertionError("a dyadic cycle contains no completion edge")
                    clause = tuple(sorted(-variable for variable in selected))
                    if clause not in learned_cuts:
                        cuts_this_model.add(clause)
                if truncated:
                    # A cap affects speed only: all returned cycle clauses are
                    # sound, and the next model is checked again from C4 up.
                    pass
                if cycles:
                    # Shortest-first separation avoids spending thousands of
                    # long-cycle clauses on a model already killed by C4.
                    break
            if shortest is None:
                result = "SAT"
                break
            models_by_shortest[shortest] += 1
            for clause in cuts_this_model:
                solver.add_clause(list(clause))
                clauses.append(list(clause))
                learned_cuts.add(clause)
                cycle_cuts[len(clause)] += 1

        elapsed = time.monotonic() - start_time

    if cnf_path is not None:
        write_dimacs(cnf_path, clauses, pool.top)
    if proof_path is not None and result == "UNSAT":
        proof_path.parent.mkdir(parents=True, exist_ok=True)
        proof_path.write_text("\n".join(proof or ()) + "\n")

    output = {
        "status": result,
        "parameters": {"j": core.j, "Y": core.Y, "a": core.a, "c": core.c},
        "order": core.order,
        "core_edges": core.size,
        "deficient_vertices": len(core.deficient_vertices()),
        "matching_edges_required": len(core.deficient_vertices()) // 2,
        "forbidden_lengths": list(lengths),
        "cardinality_encoding": encoding,
        "one_edge_incompatible_pairs": len(incompatible),
        "one_edge_incompatibility_by_length": {
            str(length): sum(length in reasons for reasons in incompatible.values())
            for length in lengths
        },
        "compatibility": feasibility,
        "sat_variables": pool.top,
        "base_clauses": base_clause_count,
        "learned_cycle_clauses": len(clauses) - base_clause_count,
        "learned_clause_sizes": {
            str(size): count for size, count in sorted(cycle_cuts.items())
        },
        "models_checked": iterations,
        "models_by_shortest_power_cycle": {
            str(length): count for length, count in sorted(models_by_shortest.items())
        },
        "elapsed_seconds": round(elapsed, 6),
        "last_power_cycle_witnesses": final_witnesses,
        "limits": {
            "max_seconds": max_seconds,
            "max_iterations": max_iterations,
            "cycles_per_length_per_model": cycle_limit,
        },
    }
    if matching is not None:
        prefix = "" if result == "SAT" else "last_rejected_"
        output[f"{prefix}matching_edges"] = [list(edge) for edge in sorted(matching)]
        for name, value in graph_encodings(core, matching).items():
            output[f"{prefix}{name}"] = value
    if cnf_path is not None:
        output["cnf"] = str(cnf_path)
    if proof_path is not None and result == "UNSAT":
        output["proof"] = str(proof_path)
    return output


def rooted_orbit_screen(j: int):
    Y = 1 << j
    records = []
    for a in range(2, 4 * Y - 8):
        for c in range(2, Y - 8):
            core = build_core(j, a, c)
            candidates, incompatible = safe_edges(core, powers_up_to(core.order))
            records.append({
                "a": a,
                "c": c,
                "safe_edges": len(candidates),
                "one_edge_incompatible_pairs": len(incompatible),
                **matching_feasibility(core, candidates),
            })
    expected = (4 * Y - 10) * (Y - 10)
    assert len(records) == expected
    # The family is rooted and path-coloured.  The coordinates can be read
    # back as |prefix_AC+A_left| and |prefix_AC+C_left|, so distinct pairs
    # cannot be identified by a valid rooted automorphism.
    return {
        "j": j,
        "Y": Y,
        "root_convention": (
            "z0,x,xprime,y,yprime,w_AC,w_BD,u_x,u_y and the A/B/C/D path "
            "colours are fixed"
        ),
        "orbit_invariant": "(a,c)=(|prefix_AC+A_left|,|prefix_AC+C_left|)",
        "parameter_pairs": expected,
        "rooted_translation_orbits": expected,
        "nontrivial_translation_equivalences": 0,
        "all_compatibility_graphs_matchable": all(
            record["perfect_matching_exists"] for record in records
        ),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int)
    parser.add_argument("--c", type=int)
    parser.add_argument("--screen-rooted-orbits", action="store_true")
    parser.add_argument("--heuristic", action="store_true")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--steps", type=int, default=12000)
    parser.add_argument("--max-seconds", type=float, default=300.0)
    parser.add_argument("--max-iterations", type=int, default=100000)
    parser.add_argument("--cycle-limit", type=int, default=5000)
    parser.add_argument("--encoding", choices=("sequential", "pairwise"),
                        default="sequential")
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.screen_rooted_orbits:
        result = rooted_orbit_screen(args.j)
    else:
        if args.a is None or args.c is None:
            parser.error("exact search requires --a and --c")
        core = build_core(args.j, args.a, args.c)
        result = (
            heuristic_search(core, args.seed, args.steps) if args.heuristic else
            exact_search(
                core, args.max_seconds, args.max_iterations, args.cycle_limit,
                args.cnf, args.proof, args.encoding,
            )
        )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
