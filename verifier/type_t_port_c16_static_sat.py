#!/usr/bin/env python3
"""Solve static exact-cover plus complete C4/C8/C16 conflict catalogs."""

from __future__ import annotations

import argparse
import gzip
import json
import time
from pathlib import Path

from pysat.formula import CNF, WCNF
from pysat.solvers import Solver

from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle
from type_t_port_multipole_sat import (
    build_catalog,
    build_exact_cover_cnf,
    enumerate_cycles_exact,
    graph_encodings,
    materialize,
    selected_partition,
)
from type_t_port_triples import powers_up_to


def read_json(path: Path) -> dict:
    return json.loads(
        gzip.open(path, "rt").read() if path.suffix == ".gz" else path.read_text()
    )


def write_json(path: Path | None, payload: dict) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path is None:
        print(rendered, end="")
    elif path.suffix == ".gz":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(gzip.compress(rendered.encode(), mtime=0))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered)


def write_dimacs(path: Path, clauses: list[list[int]], variables: int) -> None:
    text = f"p cnf {variables} {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".gz":
        path.write_bytes(gzip.compress(text.encode(), mtime=0))
    else:
        path.write_text(text)


def solve_bounded(clauses, solver_name: str, max_seconds: float,
                  conflicts_per_solve: int, with_proof: bool = False):
    started = time.monotonic()
    exhaustions = 0
    with Solver(
        name=solver_name, bootstrap_with=clauses, with_proof=with_proof,
    ) as solver:
        while time.monotonic() - started < max_seconds:
            solver.conf_budget(conflicts_per_solve)
            result = solver.solve_limited(expect_interrupt=True)
            if result is None:
                exhaustions += 1
                continue
            return result, solver.get_model(), (
                solver.get_proof() if with_proof and not result else None
            ), exhaustions, time.monotonic() - started
    return None, None, None, exhaustions, time.monotonic() - started


def static_formula(core, short_catalog: dict, c16_catalog: dict):
    _, _, triples, gadgets, _, _ = build_catalog(core)
    pool, triple_var, gadget_var, clauses, _ = build_exact_cover_cnf(
        core, triples, gadgets,
    )
    base_count = len(clauses)
    short_clauses = [
        [-variable for variable in record["support"]]
        for record in short_catalog["supports"]
    ]
    c16_clauses = [
        [-variable for variable in record["support"]]
        for record in c16_catalog["supports"]
    ]
    clauses.extend(short_clauses)
    phi48_count = len(clauses)
    clauses.extend(c16_clauses)
    return {
        "pool": pool,
        "triples": triples,
        "gadgets": gadgets,
        "triple_var": triple_var,
        "gadget_var": gadget_var,
        "clauses": clauses,
        "base_clauses": base_count,
        "short_clauses": len(short_clauses),
        "phi48_clauses": phi48_count,
        "c16_clauses": len(c16_clauses),
    }


def verify_model(core, model, formula):
    selected = set(model)
    triples, gadget = selected_partition(
        selected, formula["triple_var"], formula["gadget_var"],
    )
    graph, adjacency, _, hubs = materialize(core, triples, gadget)
    witnesses = {}
    independent = {}
    for length in powers_up_to(graph.number_of_nodes()):
        cycles, _ = enumerate_cycles_exact(adjacency, length, 1)
        first = cycles[0] if cycles else None
        second = edge_path_cycle(adjacency, length)
        if (first is None) != (second is None):
            raise AssertionError(f"cycle detectors disagree at length {length}")
        if first is not None:
            witnesses[str(length)] = list(first)
            independent[str(length)] = list(second)
    return {
        "triples": [list(item) for item in triples],
        "linked_pairs": [list(pair) for pair in gadget] if gadget else None,
        "hubs": hubs,
        "edges": [list(edge) for edge in sorted(graph.edges())],
        "order": graph.number_of_nodes(),
        "size": graph.number_of_edges(),
        "minimum_degree": min(dict(graph.degree()).values()),
        "power_cycle_witnesses": witnesses,
        "independent_power_cycle_witnesses": independent,
        **graph_encodings(graph),
    }


def solve_static(core, short_catalog: dict, c16_catalog: dict,
                 solver_name: str, max_seconds: float,
                 conflicts_per_solve: int, cnf_path: Path | None,
                 proof_path: Path | None,
                 independent_solvers: tuple[str, ...]) -> dict:
    formula = static_formula(core, short_catalog, c16_catalog)
    result, model, proof, exhaustions, elapsed = solve_bounded(
        formula["clauses"], solver_name, max_seconds, conflicts_per_solve,
        proof_path is not None,
    )
    status = "SAT" if result is True else "UNSAT" if result is False else "UNKNOWN"
    if cnf_path is not None:
        write_dimacs(cnf_path, formula["clauses"], formula["pool"].top)
    if proof_path is not None and status == "UNSAT":
        text = "\n".join(proof or []) + "\n"
        proof_path.parent.mkdir(parents=True, exist_ok=True)
        if proof_path.suffix == ".gz":
            proof_path.write_bytes(gzip.compress(text.encode(), mtime=0))
        else:
            proof_path.write_text(text)
    confirmations = {}
    if status in {"SAT", "UNSAT"}:
        for independent_solver in independent_solvers:
            with Solver(
                name=independent_solver, bootstrap_with=formula["clauses"],
            ) as solver:
                independent_result = solver.solve()
                confirmations[independent_solver] = (
                    "SAT" if independent_result else "UNSAT"
                )
        if confirmations and set(confirmations.values()) != {status}:
            raise AssertionError(
                f"independent solvers disagree with {status}: {confirmations}"
            )
    output = {
        "status": status,
        "parameters": {
            "j": core.j, "Y": core.Y, "a": core.a, "c": core.c,
        },
        "catalog_completeness": {
            "short": short_catalog.get("complete"),
            "c16": c16_catalog.get("complete"),
        },
        "formula": {
            "variables": formula["pool"].top,
            "base_exact_cover_clauses": formula["base_clauses"],
            "short_conflict_clauses": formula["short_clauses"],
            "phi48_clauses": formula["phi48_clauses"],
            "c16_conflict_clauses": formula["c16_clauses"],
            "total_clauses": len(formula["clauses"]),
        },
        "solver": solver_name,
        "elapsed_seconds": round(elapsed, 6),
        "conflict_budget_exhaustions": exhaustions,
        "independent_solver_confirmations": confirmations,
    }
    if model is not None and status == "SAT":
        output["completion"] = verify_model(core, model, formula)
    if cnf_path is not None:
        output["cnf"] = str(cnf_path)
    if proof_path is not None and status == "UNSAT":
        output["proof"] = str(proof_path)
    return output


def maxsat(core, short_catalog: dict, c16_catalog: dict) -> dict:
    from pysat.examples.rc2 import RC2

    if not c16_catalog.get("complete"):
        raise ValueError("MaxSAT requires a complete C16 support catalog")
    formula = static_formula(core, short_catalog, c16_catalog)
    hard_count = formula["phi48_clauses"]
    wcnf = WCNF()
    for clause in formula["clauses"][:hard_count]:
        wcnf.append(clause)
    for clause in formula["clauses"][hard_count:]:
        wcnf.append(clause, weight=1)
    started = time.monotonic()
    with RC2(wcnf, solver="cadical195") as solver:
        model = solver.compute()
        optimum = solver.cost
    return {
        "status": "OPTIMUM",
        "objective": "violated minimal C16 gadget supports",
        "optimum": optimum,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "completion": verify_model(core, model, formula),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--short-catalog", type=Path, required=True)
    parser.add_argument("--c16-catalog", type=Path, required=True)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--max-seconds", type=float, default=300.0)
    parser.add_argument("--conflicts-per-solve", type=int, default=100_000)
    parser.add_argument(
        "--independent-solvers", default="cadical195,lingeling",
        help="comma-separated fresh solvers used to confirm a definite result",
    )
    parser.add_argument("--maxsat", action="store_true")
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    core = build_core(args.j, args.a, args.c)
    short = read_json(args.short_catalog)
    c16 = read_json(args.c16_catalog)
    result = (
        maxsat(core, short, c16) if args.maxsat else
        solve_static(
            core, short, c16, args.solver, args.max_seconds,
            args.conflicts_per_solve, args.cnf, args.proof,
            tuple(filter(None, args.independent_solvers.split(","))),
        )
    )
    write_json(args.output, result)


if __name__ == "__main__":
    main()
