#!/usr/bin/env python3
"""Analyze a reduced Type-T matching UNSAT core semantically.

This is a provenance and conflict-hypergraph checker, not a claim that the
input is a clause-minimal MUS.  It reconstructs the deterministic matching
CNF, separates retained cardinality clauses from cycle cuts, maps every cut
back to matching edges and literal ordinary cycles, and tests whether each
short-cycle family is essential to the reduced contradiction.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import tempfile
import time
from collections import Counter, defaultdict, deque
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Glucose3
from pysat.solvers import Solver

from type_t_port_core_export import build_core
from type_t_port_matching_sat import build_cnf, powers_up_to, safe_edges


def load_dimacs(path: Path) -> tuple[int, list[list[int]]]:
    opener = gzip.open if path.suffix == ".gz" else open
    variables = 0
    clauses = []
    current = []
    with opener(path, "rt") as source:
        for raw in source:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                _, kind, variables_text, _clauses_text = line.split()
                assert kind == "cnf"
                variables = int(variables_text)
                continue
            for literal_text in line.split():
                literal = int(literal_text)
                if literal == 0:
                    clauses.append(current)
                    current = []
                else:
                    current.append(literal)
    assert not current
    return variables, clauses


def canonical_cycle(path: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    least = min(range(len(path)), key=path.__getitem__)
    forward = tuple(path[(least + index) % len(path)] for index in range(len(path)))
    reverse = tuple(path[(least - index) % len(path)] for index in range(len(path)))
    return min(forward, reverse)


def classify_cut(core, matching_edges: set[tuple[int, int]]):
    """Return short realizations, or the first available longer dyadic ones."""
    adjacency = [set(row) for row in core.adjacency()]
    for u, v in matching_edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    anchor = min(matching_edges)
    adjacency[anchor[0]].remove(anchor[1])
    adjacency[anchor[1]].remove(anchor[0])
    remaining = matching_edges - {anchor}
    start, target = anchor
    witnesses = {}

    def search_length(length: int):
        path = [start]
        used_vertices = {start}
        found = []

        def visit(vertex: int, depth: int, used_matching: frozenset[tuple[int, int]]) -> None:
            if found:
                return
            if depth == length - 1:
                if vertex == target and used_matching == remaining:
                    found.append(canonical_cycle(path))
                return
            if len(remaining - used_matching) > length - 1 - depth:
                return
            for neighbor in adjacency[vertex]:
                if neighbor in used_vertices:
                    continue
                edge = tuple(sorted((vertex, neighbor)))
                used_vertices.add(neighbor)
                path.append(neighbor)
                visit(
                    neighbor, depth + 1,
                    used_matching | ({edge} if edge in remaining else set()),
                )
                path.pop()
                used_vertices.remove(neighbor)

        visit(start, 0, frozenset())
        return found[0] if found else None

    for length in (4, 8, 16):
        witness = search_length(length)
        if witness is not None:
            witnesses[length] = witness
    # The observed j=4 closures use only short cuts.  Retain exact support for
    # a sweep class that first reaches C32/C64 without paying that long DFS on
    # every already-classified short clause.
    if not witnesses:
        for length in powers_up_to(core.order):
            if length <= 16:
                continue
            witness = search_length(length)
            if witness is not None:
                witnesses[length] = witness
    if not witnesses:
        raise AssertionError(f"cycle cut has no dyadic realization: {matching_edges}")
    return witnesses


def concatenate(*paths: tuple[int, ...]) -> tuple[int, ...]:
    result = []
    for path in paths:
        assert not result or result[-1] == path[0]
        result.extend(path if not result else path[1:])
    return tuple(result)


def coordinate_system(core):
    branches = {
        "A": concatenate(core.paths["prefix_AC"], core.paths["A_left"],
                         core.paths["A_middle"], core.paths["A_right"]),
        "B": concatenate(core.paths["prefix_BD"], core.paths["B_right"]),
        "C": concatenate(core.paths["prefix_AC"], core.paths["C_left"],
                         core.paths["C_middle"], core.paths["C_right"]),
        "D": concatenate(core.paths["prefix_BD"], core.paths["D_right"]),
    }
    locations = defaultdict(list)
    for branch, vertices in branches.items():
        for coordinate, vertex in enumerate(vertices):
            locations[vertex].append({"branch": branch, "coordinate": coordinate})
    return branches, locations


def verify_drat(cnf_path: Path, proof_path: Path, checker: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="type-t-core-check-") as directory:
        directory_path = Path(directory)
        cnf_plain = directory_path / "core.cnf"
        proof_plain = directory_path / "core.drat"
        for source_path, destination in ((cnf_path, cnf_plain), (proof_path, proof_plain)):
            opener = gzip.open if source_path.suffix == ".gz" else open
            with opener(source_path, "rb") as source, destination.open("wb") as target:
                while block := source.read(1 << 20):
                    target.write(block)
        started = time.monotonic()
        process = subprocess.run(
            [str(checker), str(cnf_plain), str(proof_plain), "-w"],
            text=True, capture_output=True, check=False,
        )
    transcript = process.stdout + process.stderr
    if process.returncode != 0 or "s VERIFIED" not in transcript:
        raise AssertionError(f"DRAT verification failed:\n{transcript}")
    return {
        "status": "VERIFIED",
        "checker": str(checker),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "transcript": transcript.strip(),
    }


def analyze(cnf_path: Path, j: int, a: int, c: int,
            run_family_tests: bool, proof_path: Path | None,
            drat_trim: Path | None) -> dict:
    core = build_core(j, a, c)
    candidates, _incompatible = safe_edges(core, powers_up_to(core.order))
    pool, edge_var, base_clauses, ranges = build_cnf(
        core, candidates, "sequential",
    )
    reverse_edge_var = {variable: edge for edge, variable in edge_var.items()}
    variables, reduced_clauses = load_dimacs(cnf_path)
    assert variables == pool.top

    base_occurrences = defaultdict(deque)
    for vertex, (start, end) in ranges.items():
        for local_index, clause_index in enumerate(range(start, end)):
            key = tuple(sorted(base_clauses[clause_index]))
            base_occurrences[key].append((vertex, local_index, clause_index))

    retained_base = []
    cut_clauses = []
    classified_clause_kinds = []
    for reduced_index, clause in enumerate(reduced_clauses):
        key = tuple(sorted(clause))
        if base_occurrences[key]:
            vertex, local_index, original_index = base_occurrences[key].popleft()
            retained_base.append({
                "reduced_clause_index": reduced_index,
                "original_clause_index": original_index,
                "vertex": vertex,
                "vertex_label": core.labels[vertex],
                "local_index": local_index,
                "subkind": "at_least_one" if local_index == 0 else "sequential_at_most_one",
            })
            classified_clause_kinds.append("base")
        else:
            if not all(literal < 0 and -literal in reverse_edge_var for literal in clause):
                raise AssertionError(f"unclassified reduced clause {clause}")
            cut_clauses.append((reduced_index, clause))
            classified_clause_kinds.append("cut")

    branches, locations = coordinate_system(core)
    path_by_edge = {}
    for path_name, vertices in core.paths.items():
        for u, v in zip(vertices, vertices[1:]):
            path_by_edge[tuple(sorted((u, v)))] = path_name

    cut_records = []
    length_counts = Counter()
    motif_counts = Counter()
    used_primary_variables = set()
    used_deficient_vertices = set()
    for ordinal, (reduced_index, clause) in enumerate(cut_clauses):
        matching = {reverse_edge_var[-literal] for literal in clause}
        witnesses = classify_cut(core, matching)
        source_length = min(witnesses)
        length_counts[source_length] += 1
        used_primary_variables.update(-literal for literal in clause)
        used_deficient_vertices.update(vertex for edge in matching for vertex in edge)

        witness = witnesses[source_length]
        witness_edges = {
            tuple(sorted((witness[index], witness[(index + 1) % len(witness)])))
            for index in range(len(witness))
        }
        core_path_names = sorted({
            path_by_edge[edge] for edge in witness_edges
            if edge not in matching
        })
        motif_counts[(source_length, len(matching), tuple(core_path_names))] += 1
        hulls = {}
        for branch in branches:
            coordinates = [
                location["coordinate"] for vertex in witness
                for location in locations[vertex] if location["branch"] == branch
            ]
            if coordinates:
                hulls[branch] = [min(coordinates), max(coordinates)]
        endpoint_records = []
        for u, v in sorted(matching):
            endpoint_records.append({
                "vertices": [u, v],
                "labels": [core.labels[u], core.labels[v]],
                "locations": [locations[u], locations[v]],
            })
        cut_records.append({
            "ordinal": ordinal,
            "reduced_clause_index": reduced_index,
            "clause": clause,
            "matching_edges": endpoint_records,
            "realizable_lengths": sorted(witnesses),
            "source_length": source_length,
            "canonical_cycle_witnesses": {
                str(length): list(cycle) for length, cycle in sorted(witnesses.items())
            },
            "source_cycle_core_paths": core_path_names,
            "source_cycle_coordinate_hulls": hulls,
        })

    vertex_base_counts = Counter(record["vertex"] for record in retained_base)
    alo_vertices = {
        record["vertex"] for record in retained_base
        if record["subkind"] == "at_least_one"
    }
    family_tests = {}
    if run_family_tests:
        source_length_by_index = {
            record["reduced_clause_index"]: record["source_length"]
            for record in cut_records
        }
        for mode in ("remove", "keep"):
            for length in (4, 8, 16):
                selected = []
                for index, clause in enumerate(reduced_clauses):
                    kind = classified_clause_kinds[index]
                    if kind == "base":
                        selected.append(clause)
                    elif mode == "remove" and source_length_by_index[index] != length:
                        selected.append(clause)
                    elif mode == "keep" and source_length_by_index[index] == length:
                        selected.append(clause)
                started = time.monotonic()
                with Solver(name="cadical195", bootstrap_with=selected) as solver:
                    sat = solver.solve()
                    stats = solver.accum_stats()
                family_tests[f"{mode}_{length}"] = {
                    "status": "SAT" if sat else "UNSAT",
                    "clauses": len(selected),
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                    "stats": stats,
                }

    proof_verification = None
    if proof_path is not None:
        if drat_trim is None:
            raise ValueError("--proof requires --drat-trim")
        proof_verification = verify_drat(cnf_path, proof_path, drat_trim)

    return {
        "status": "PASS",
        "core_kind": "aggressively reduced proof-dependency core; not claimed MUS",
        "parameters": {"j": j, "Y": 1 << j, "a": a, "c": c},
        "source": str(cnf_path),
        "variables": variables,
        "clauses": len(reduced_clauses),
        "original_final_clauses": 109419 if (j, a, c) == (4, 2, 2) else None,
        "reduction_fraction": (
            1.0 - len(reduced_clauses) / 109419
            if (j, a, c) == (4, 2, 2) else None
        ),
        "retained_matching_cardinality_clauses": len(retained_base),
        "retained_cycle_cuts": len(cut_records),
        "cycle_cut_sizes": dict(sorted(Counter(len(record["clause"]) for record in cut_records).items())),
        "cycle_cut_source_lengths": {
            str(length): count for length, count in sorted(length_counts.items())
        },
        "support": {
            "deficient_vertices_in_cycle_cuts": len(used_deficient_vertices),
            "deficient_vertices_total": len(core.deficient_vertices()),
            "safe_matching_variables_in_cycle_cuts": len(used_primary_variables),
            "safe_matching_variables_total": len(edge_var),
            "cardinality_blocks_with_retained_clauses": len(vertex_base_counts),
            "cardinality_blocks_total": len(core.deficient_vertices()),
            "vertices_with_retained_at_least_one_clause": len(alo_vertices),
            "vertices_without_retained_at_least_one_clause": [
                {"vertex": vertex, "label": core.labels[vertex]}
                for vertex in core.deficient_vertices() if vertex not in alo_vertices
            ],
        },
        "family_essentiality_tests": family_tests,
        "proof_verification": proof_verification,
        "motif_clusters": [{
            "source_length": key[0],
            "matching_edges": key[1],
            "core_path_names": list(key[2]),
            "cuts": count,
        } for key, count in sorted(
            motif_counts.items(), key=lambda item: (-item[1], item[0]),
        )],
        "retained_cardinality_by_vertex": [{
            "vertex": vertex,
            "label": core.labels[vertex],
            "retained_clauses": vertex_base_counts[vertex],
            "retains_at_least_one": vertex in alo_vertices,
        } for vertex in core.deficient_vertices()],
        "cuts": cut_records,
    }


def write_json(path: Path, payload: dict) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".gz":
        with path.open("wb") as raw:
            with gzip.GzipFile(
                filename=path.stem, mode="wb", compresslevel=9,
                fileobj=raw, mtime=0,
            ) as compressed:
                compressed.write(rendered.encode())
    else:
        path.write_text(rendered)


def _gzip_deterministic(source_path: Path, destination_path: Path) -> None:
    with source_path.open("rb") as source, destination_path.open("wb") as raw:
        with gzip.GzipFile(
            filename=destination_path.stem, mode="wb", compresslevel=9,
            fileobj=raw, mtime=0,
        ) as destination:
            while block := source.read(1 << 20):
                destination.write(block)


def _extract_class_proof_core(task: tuple[str, str]) -> dict:
    class_directory_text, checker_text = task
    class_directory = Path(class_directory_text)
    checker = Path(checker_text)
    summary_path = class_directory / "proof_core_summary.json"
    core_gzip_path = class_directory / "proof_core.cnf.gz"
    analysis_gzip_path = class_directory / "proof_core_analysis.json.gz"
    if summary_path.exists() and core_gzip_path.exists() and analysis_gzip_path.exists():
        result = json.loads(summary_path.read_text())
        if result.get("schema_version") == 4:
            return {**result, "resumed": True}

    exact = json.loads((class_directory / "result.json").read_text())
    if exact["status"] != "UNSAT":
        return {
            "class_id": exact["class_id"], "status": "SKIPPED",
            "reason": f"exact status {exact['status']}", "resumed": False,
        }
    parameters = exact["parameters"]
    core = build_core(parameters["j"], parameters["a"], parameters["c"])
    candidates, _ = safe_edges(core, powers_up_to(core.order))
    pool, edge_var, base, ranges = build_cnf(core, candidates, "sequential")
    reverse = {variable: edge for edge, variable in edge_var.items()}
    checker_sha256 = hashlib.sha256(checker.read_bytes()).hexdigest()
    checker_commit_process = subprocess.run(
        ["git", "-C", str(checker.parent), "rev-parse", "HEAD"],
        text=True, capture_output=True, check=False,
    )
    checker_git_commit = (
        checker_commit_process.stdout.strip()
        if checker_commit_process.returncode == 0 else None
    )

    with tempfile.TemporaryDirectory(prefix=f"{exact['class_id']}-core-") as directory:
        temporary = Path(directory)
        final_cnf = temporary / "final.cnf"
        proof = temporary / "final.drat"
        raw_core = temporary / "proof_core.cnf"
        raw_core_proof = temporary / "proof_core.drat"
        with gzip.open(class_directory / "final.cnf.gz", "rb") as source, final_cnf.open("wb") as target:
            while block := source.read(1 << 20):
                target.write(block)
        formula = CNF(from_file=str(final_cnf))
        started = time.monotonic()
        with Glucose3(bootstrap_with=formula.clauses, with_proof=True) as solver:
            sat = solver.solve()
            if sat:
                raise AssertionError(f"final CNF became SAT for {exact['class_id']}")
            proof_lines = solver.get_proof()
        proof.write_text("\n".join(proof_lines) + "\n")
        extraction = subprocess.run([
            str(checker), str(final_cnf), str(proof),
            "-c", str(raw_core), "-l", str(raw_core_proof), "-w",
        ], text=True, capture_output=True, check=False)
        extraction_text = extraction.stdout + extraction.stderr
        if extraction.returncode != 0 or "s VERIFIED" not in extraction_text:
            raise AssertionError(f"proof-core extraction failed:\n{extraction_text}")
        verification = subprocess.run([
            str(checker), str(raw_core), str(raw_core_proof), "-w",
        ], text=True, capture_output=True, check=False)
        verification_text = verification.stdout + verification.stderr
        if verification.returncode != 0 or "s VERIFIED" not in verification_text:
            raise AssertionError(f"proof-core verification failed:\n{verification_text}")

        variables, clauses = load_dimacs(raw_core)
        assert variables == pool.top
        with Solver(name="cadical195", bootstrap_with=clauses) as independent_solver:
            independent_sat = independent_solver.solve()
            independent_stats = independent_solver.accum_stats()
        if independent_sat:
            raise AssertionError(f"proof core became SAT for {exact['class_id']}")
        base_occurrences = defaultdict(deque)
        for vertex, (start, end) in ranges.items():
            for local_index, clause_index in enumerate(range(start, end)):
                base_occurrences[tuple(sorted(base[clause_index]))].append(
                    (vertex, local_index, clause_index)
                )
        retained_base_records = []
        cuts = []
        for reduced_index, clause in enumerate(clauses):
            key = tuple(sorted(clause))
            if base_occurrences[key]:
                vertex, local_index, original_index = base_occurrences[key].popleft()
                retained_base_records.append({
                    "reduced_clause_index": reduced_index,
                    "original_clause_index": original_index,
                    "vertex": vertex,
                    "vertex_label": core.labels[vertex],
                    "local_index": local_index,
                    "subkind": (
                        "at_least_one" if local_index == 0
                        else "sequential_at_most_one"
                    ),
                    "clause": clause,
                })
            else:
                if not all(literal < 0 and -literal in reverse for literal in clause):
                    raise AssertionError(f"unknown proof-core clause {clause}")
                cuts.append((reduced_index, clause))
        branches, locations = coordinate_system(core)
        path_by_edge = {}
        for path_name, vertices in core.paths.items():
            for u, v in zip(vertices, vertices[1:]):
                path_by_edge[tuple(sorted((u, v)))] = path_name
        length_counts = Counter()
        supported_variables = set()
        supported_vertices = set()
        chord_counts = Counter()
        motif_counts = Counter()
        cut_records = []
        for ordinal, (reduced_index, clause) in enumerate(cuts):
            matching = {reverse[-literal] for literal in clause}
            witnesses = classify_cut(core, matching)
            source_length = min(witnesses)
            length_counts[source_length] += 1
            chord_counts[len(matching)] += 1
            supported_variables.update(-literal for literal in clause)
            supported_vertices.update(vertex for edge in matching for vertex in edge)
            witness = witnesses[source_length]
            witness_edges = {
                tuple(sorted((witness[index], witness[(index + 1) % len(witness)])))
                for index in range(len(witness))
            }
            core_path_names = sorted({
                path_by_edge[edge] for edge in witness_edges if edge not in matching
            })
            motif_counts[(source_length, len(matching), tuple(core_path_names))] += 1
            hulls = {}
            for branch in branches:
                coordinates = [
                    location["coordinate"] for vertex in witness
                    for location in locations[vertex]
                    if location["branch"] == branch
                ]
                if coordinates:
                    hulls[branch] = [min(coordinates), max(coordinates)]
            cut_records.append({
                "ordinal": ordinal,
                "reduced_clause_index": reduced_index,
                "clause": clause,
                "matching_edges": [{
                    "vertices": [u, v],
                    "labels": [core.labels[u], core.labels[v]],
                    "locations": [locations[u], locations[v]],
                } for u, v in sorted(matching)],
                "matching_edge_count": len(matching),
                "source_length": source_length,
                "total_core_path_edges": source_length - len(matching),
                "realizable_lengths": sorted(witnesses),
                "canonical_cycle_witnesses": {
                    str(length): list(cycle)
                    for length, cycle in sorted(witnesses.items())
                },
                "source_cycle_core_paths": core_path_names,
                "source_cycle_coordinate_hulls": hulls,
            })
        _gzip_deterministic(raw_core, core_gzip_path)
        semantic_analysis = {
            "schema_version": 1,
            "status": "PASS",
            "class_id": exact["class_id"],
            "parameters": parameters,
            "core_kind": "DRAT proof-dependency core; not claimed MUS",
            "variables": variables,
            "clauses": len(clauses),
            "retained_matching_cardinality_clauses": retained_base_records,
            "retained_cycle_cuts": cut_records,
            "motif_clusters": [{
                "source_length": key[0],
                "matching_edges": key[1],
                "core_path_names": list(key[2]),
                "cuts": count,
            } for key, count in sorted(
                motif_counts.items(), key=lambda item: (-item[1], item[0]),
            )],
            "coordinate_note": (
                "The ordinary core is branched, so the minimal support is represented "
                "by a hull on each intrinsic A/B/C/D coordinate path rather than by "
                "one misleading global scalar interval."
            ),
        }
        write_json(analysis_gzip_path, semantic_analysis)
        result = {
            "schema_version": 4,
            "class_id": exact["class_id"],
            "parameters": parameters,
            "status": "VERIFIED_UNSAT_PROOF_CORE",
            "resumed": False,
            "original_clauses": len(formula.clauses),
            "proof_core_clauses": len(clauses),
            "reduction_fraction": 1.0 - len(clauses) / len(formula.clauses),
            "retained_matching_cardinality_clauses": len(retained_base_records),
            "retained_cycle_cuts": len(cuts),
            "cycle_cut_source_lengths": {
                str(length): count for length, count in sorted(length_counts.items())
            },
            "cycle_cut_chord_counts": {
                str(chords): count for chords, count in sorted(chord_counts.items())
            },
            "support": {
                "deficient_vertices": len(supported_vertices),
                "deficient_vertices_total": len(core.deficient_vertices()),
                "safe_matching_variables": len(supported_variables),
                "safe_matching_variables_total": len(edge_var),
            },
            "proof_lines": len(proof_lines),
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "proof_core_cnf_gzip": str(core_gzip_path),
            "proof_core_cnf_gzip_sha256": hashlib.sha256(
                core_gzip_path.read_bytes()
            ).hexdigest(),
            "proof_core_analysis_gzip": str(analysis_gzip_path),
            "proof_core_analysis_gzip_sha256": hashlib.sha256(
                analysis_gzip_path.read_bytes()
            ).hexdigest(),
            "motif_clusters": len(motif_counts),
            "drat_extraction_verified": True,
            "drat_core_reverified": True,
            "drat_checker": str(checker),
            "drat_checker_sha256": checker_sha256,
            "drat_checker_git_commit": checker_git_commit,
            "drat_extraction_transcript_sha256": hashlib.sha256(
                extraction_text.encode()
            ).hexdigest(),
            "drat_reverification_transcript_sha256": hashlib.sha256(
                verification_text.encode()
            ).hexdigest(),
            "independent_core_solver": {
                "solver": "cadical195",
                "status": "UNSAT",
                "stats": independent_stats,
            },
        }
        summary_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return result


def sweep_proof_cores(sweep_directory: Path, checker: Path, workers: int) -> dict:
    class_directories = sorted(
        path.parent for path in sweep_directory.glob("class_*/result.json")
    )
    tasks = [(str(path), str(checker)) for path in class_directories]
    records = []
    started = time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_extract_class_proof_core, task): task[0] for task in tasks}
        for future in as_completed(futures):
            record = future.result()
            records.append(record)
            print(
                f"[{len(records)}/{len(tasks)}] {record['class_id']} "
                f"{record['status']} core={record.get('proof_core_clauses')} "
                f"resumed={record.get('resumed')}",
                flush=True,
            )
    records.sort(key=lambda record: record["class_id"])
    complete = all(record["status"] == "VERIFIED_UNSAT_PROOF_CORE" for record in records)
    summary = {
        "status": "COMPLETE" if complete else "INCOMPLETE",
        "classes": len(records),
        "workers": workers,
        "wall_seconds": round(time.monotonic() - started, 6),
        "records": records,
    }
    (sweep_directory / "proof_core_sweep.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--sweep-dir", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--j", type=int)
    parser.add_argument("--a", type=int)
    parser.add_argument("--c", type=int)
    parser.add_argument("--workers", type=int, default=max(1, min(4, os.cpu_count() or 1)))
    parser.add_argument("--skip-family-tests", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if (args.cnf is None) == (args.sweep_dir is None):
        parser.error("choose exactly one of --cnf and --sweep-dir")
    if args.sweep_dir is not None:
        if args.drat_trim is None:
            parser.error("--sweep-dir requires --drat-trim")
        summary = sweep_proof_cores(args.sweep_dir, args.drat_trim, args.workers)
        print(json.dumps({
            "status": summary["status"], "classes": summary["classes"],
            "wall_seconds": summary["wall_seconds"],
        }, sort_keys=True))
        return
    if None in (args.j, args.a, args.c) or args.output is None:
        parser.error("single-core analysis requires --j, --a, --c, and --output")
    result = analyze(
        args.cnf, args.j, args.a, args.c, not args.skip_family_tests,
        args.proof, args.drat_trim,
    )
    write_json(args.output, result)
    print(json.dumps({
        "status": result["status"],
        "clauses": result["clauses"],
        "retained_matching_cardinality_clauses": result["retained_matching_cardinality_clauses"],
        "retained_cycle_cuts": result["retained_cycle_cuts"],
        "cycle_cut_source_lengths": result["cycle_cut_source_lengths"],
        "support": result["support"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
