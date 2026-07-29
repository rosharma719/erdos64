#!/usr/bin/env python3
"""Canonicalize and sweep ordinary Type-T j=4 port-completion cores.

The rooted/path-coloured Type-T object is intentionally forgotten here.  A
class consists only of the expanded ordinary uncoloured graph; its deficient
set is intrinsic because it is exactly the set of degree-two vertices.

Canonical graph identifiers and automorphism orders come from nauty 2.9.3.
NetworkX independently constructs and verifies every explicit isomorphism
map.  ``shortg`` independently checks the number of uncoloured classes.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import statistics
import subprocess
import tempfile
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from type_t_port_core_export import build_core, graph_encodings, to_networkx


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run_filter(command: list[str], payload: str) -> tuple[list[str], str]:
    process = subprocess.run(
        command, input=payload, text=True, capture_output=True, check=True,
    )
    return process.stdout.splitlines(), process.stderr


def nauty_version() -> str:
    process = subprocess.run(
        ["labelg", "-help"], text=True, capture_output=True, check=False,
    )
    text = process.stdout + process.stderr
    # Homebrew's binary does not print its version in -help.  Record the
    # package version when brew is available, otherwise keep an exact hash.
    try:
        version = subprocess.run(
            ["brew", "list", "--versions", "nauty"], text=True,
            capture_output=True, check=True,
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        version = "version unavailable"
    binary = Path(subprocess.run(
        ["which", "labelg"], text=True, capture_output=True, check=True,
    ).stdout.strip())
    return f"{version}; labelg_sha256={sha256_bytes(binary.read_bytes())}"


def classify_j4() -> dict:
    import networkx as nx

    sources = []
    graph6_rows = []
    for a in range(2, 56):
        for c in range(2, 8):
            core = build_core(4, a, c)
            sources.append((a, c, core))
            graph6_rows.append(graph_encodings(core)["graph6"])
    payload = "\n".join(graph6_rows) + "\n"

    canonical_rows, labelg_stderr = run_filter(["labelg", "-q", "-g"], payload)
    assert len(canonical_rows) == len(sources) == 324

    sparse_rows, sparse_stderr = run_filter(
        ["labelg", "-q", "-g", "-S"], payload,
    )
    traces_rows, traces_stderr = run_filter(
        ["labelg", "-q", "-g", "-t"], payload,
    )
    assert len(set(sparse_rows)) == len(set(traces_rows)) == 324

    short_rows, shortg_stderr = run_filter(["shortg", "-q"], payload)
    canonical_groups: dict[str, list[int]] = {}
    for index, canonical in enumerate(canonical_rows):
        canonical_groups.setdefault(canonical, []).append(index)
    assert len(short_rows) == len(canonical_groups)
    assert set(short_rows) == set(canonical_groups)

    count_rows, countg_stderr = run_filter(
        ["countg", "-q", "-V", "--a"], "\n".join(canonical_rows) + "\n",
    )
    group_sizes = []
    for row in count_rows:
        match = re.fullmatch(r"Graph (\d+) : groupsize=([0-9.eE+-]+)", row.strip())
        if match:
            group_sizes.append(int(float(match.group(2))))
    assert len(group_sizes) == 324

    classes = []
    maps = []
    representative_g6 = []
    representative_s6 = []
    distance_signature_hashes = []
    wl_hashes = []
    networkx_automorphism_orders = []
    for _, _, core in sources:
        graph = to_networkx(core)
        vertex_profiles = []
        for vertex in graph:
            histogram = Counter(nx.single_source_shortest_path_length(graph, vertex).values())
            vertex_profiles.append(tuple(histogram.get(distance, 0) for distance in range(core.order)))
        distance_signature = tuple(sorted(vertex_profiles))
        distance_signature_hashes.append(
            sha256_bytes(repr(distance_signature).encode())
        )
        wl_hashes.append(nx.weisfeiler_lehman_graph_hash(graph, iterations=20))
        automorphisms = nx.algorithms.isomorphism.GraphMatcher(
            graph, graph,
        ).isomorphisms_iter()
        order = 0
        for _mapping in automorphisms:
            order += 1
            if order > 1:
                break
        networkx_automorphism_orders.append(order)
    assert len(set(distance_signature_hashes)) == 324
    assert len(set(wl_hashes)) == 324
    assert set(networkx_automorphism_orders) == {1}
    for class_number, (_, indices) in enumerate(
        sorted(canonical_groups.items(), key=lambda item: sources[item[1][0]][:2])
    ):
        representative_index = indices[0]
        a_rep, c_rep, representative_core = sources[representative_index]
        canonical_g6 = canonical_rows[representative_index]
        canonical_graph = nx.from_graph6_bytes(canonical_g6.encode())
        representative_graph = to_networkx(representative_core)
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            representative_graph, canonical_graph,
        )
        representative_to_canonical = next(matcher.isomorphisms_iter())
        assert len(representative_to_canonical) == representative_core.order

        canonical_s6 = nx.to_sparse6_bytes(
            canonical_graph, header=False,
        ).decode().strip()
        class_id = f"class_{class_number:03d}_a{a_rep:02d}_c{c_rep:02d}"
        members = []
        for source_index in indices:
            a, c, core = sources[source_index]
            source_graph = to_networkx(core)
            member_matcher = nx.algorithms.isomorphism.GraphMatcher(
                source_graph, representative_graph,
            )
            member_to_representative = next(member_matcher.isomorphisms_iter())
            if len(indices) == 1:
                assert member_to_representative == {
                    vertex: vertex for vertex in range(core.order)
                }
            mapped_edges = {
                tuple(sorted((member_to_representative[u], member_to_representative[v])))
                for u, v in core.edges
            }
            assert mapped_edges == set(representative_core.edges)
            members.append({"a": a, "c": c})
            maps.append({
                "class_id": class_id,
                "source": {"a": a, "c": c},
                "source_to_representative": [
                    member_to_representative[vertex] for vertex in range(core.order)
                ],
                "source_to_canonical": [
                    representative_to_canonical[member_to_representative[vertex]]
                    for vertex in range(core.order)
                ],
            })

        automorphism_orders = {group_sizes[index] for index in indices}
        assert len(automorphism_orders) == 1
        classes.append({
            "class_id": class_id,
            "representative": {"j": 4, "Y": 16, "a": a_rep, "c": c_rep},
            "members": members,
            "class_size": len(members),
            "canonical_graph6": canonical_g6,
            "canonical_sparse6": canonical_s6,
            "canonical_graph6_sha256": sha256_bytes((canonical_g6 + "\n").encode()),
            "automorphism_group_size": next(iter(automorphism_orders)),
            "distance_profile_signature_sha256": distance_signature_hashes[representative_index],
            "weisfeiler_lehman_20_hash": wl_hashes[representative_index],
        })
        representative_g6.append(canonical_g6)
        representative_s6.append(canonical_s6)

    return {
        "status": "PASS",
        "scope": (
            "ordinary uncoloured expanded cores; equivalence transfers only the "
            "relaxed same-vertex completion problem, not rooted Type-T semantics"
        ),
        "j": 4,
        "rooted_translations": 324,
        "ordinary_isomorphism_classes": len(classes),
        "class_size_distribution": {
            str(size): sum(len(item["members"]) == size for item in classes)
            for size in sorted({len(item["members"]) for item in classes})
        },
        "automorphism_group_size_distribution": {
            str(size): sum(item["automorphism_group_size"] == size for item in classes)
            for size in sorted({item["automorphism_group_size"] for item in classes})
        },
        "canonicalizer": nauty_version(),
        "labelg_command": ["labelg", "-q", "-g"],
        "shortg_independent_class_count": len(short_rows),
        "shortg_command": ["shortg", "-q"],
        "sparse_nauty_unique_classes": len(set(sparse_rows)),
        "sparse_nauty_command": ["labelg", "-q", "-g", "-S"],
        "traces_unique_classes": len(set(traces_rows)),
        "traces_command": ["labelg", "-q", "-g", "-t"],
        "independent_distance_profile_classes": len(set(distance_signature_hashes)),
        "independent_WL20_classes": len(set(wl_hashes)),
        "networkx_automorphism_orders_verified": len(networkx_automorphism_orders),
        "networkx_explicit_maps_verified": len(maps),
        "stderr": {
            "labelg": labelg_stderr.strip(),
            "shortg": shortg_stderr.strip(),
            "countg": countg_stderr.strip(),
            "sparse_nauty": sparse_stderr.strip(),
            "traces": traces_stderr.strip(),
        },
        "classes": classes,
        "isomorphism_maps": maps,
        "representative_graph6_stream": representative_g6,
        "representative_sparse6_stream": representative_s6,
    }


def write_classification(result: dict, data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    classes_payload = {key: value for key, value in result.items() if key not in {
        "isomorphism_maps", "representative_graph6_stream", "representative_sparse6_stream",
    }}
    (data_dir / "classes.json").write_text(
        json.dumps(classes_payload, indent=2, sort_keys=True) + "\n"
    )
    (data_dir / "isomorphism_maps.json").write_text(json.dumps({
        "scope": result["scope"],
        "maps": result["isomorphism_maps"],
    }, indent=2, sort_keys=True) + "\n")
    (data_dir / "representatives.g6").write_text(
        "\n".join(result["representative_graph6_stream"]) + "\n"
    )
    (data_dir / "representatives.s6").write_text(
        "\n".join(result["representative_sparse6_stream"]) + "\n"
    )


def _solve_class(task: tuple) -> dict:
    (class_id, a, c, output_dir_string, max_seconds, max_iterations,
     cycle_limit, independent_solvers) = task
    from pysat.formula import CNF
    from pysat.solvers import Solver
    from type_t_port_matching_sat import exact_search

    output_dir = Path(output_dir_string) / class_id
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / "result.json"
    cnf_gz_path = output_dir / "final.cnf.gz"
    if result_path.exists() and cnf_gz_path.exists():
        existing = json.loads(result_path.read_text())
        if existing.get("status") in {"UNSAT", "SAT"}:
            return {**existing, "class_id": class_id, "resumed": True}

    core = build_core(4, a, c)
    temporary_cnf = output_dir / "final.cnf.incomplete"
    result = exact_search(
        core, max_seconds=max_seconds, max_iterations=max_iterations,
        cycle_limit=cycle_limit, cnf_path=temporary_cnf, proof_path=None,
        encoding="sequential",
    )
    result["class_id"] = class_id
    result["resumed"] = False
    result["final_cnf_independent_solvers"] = {}
    if result["status"] == "UNSAT":
        cnf = CNF(from_file=str(temporary_cnf))
        for solver_name in independent_solvers:
            started = time.monotonic()
            with Solver(name=solver_name, bootstrap_with=cnf.clauses) as solver:
                solved = solver.solve()
                stats = solver.accum_stats()
            if solved is not False:
                raise AssertionError(f"{solver_name} did not confirm UNSAT for {class_id}")
            result["final_cnf_independent_solvers"][solver_name] = {
                "status": "UNSAT",
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "stats": stats,
            }
        with temporary_cnf.open("rb") as source, cnf_gz_path.open("wb") as compressed:
            with gzip.GzipFile(
                filename="final.cnf", mode="wb", compresslevel=9,
                fileobj=compressed, mtime=0,
            ) as target:
                while block := source.read(1 << 20):
                    target.write(block)
        result.pop("cnf", None)
        result["final_cnf_gzip"] = str(cnf_gz_path)
        result["final_cnf_gzip_sha256"] = hashlib.sha256(cnf_gz_path.read_bytes()).hexdigest()
        temporary_cnf.unlink()
    elif temporary_cnf.exists():
        temporary_cnf.unlink()

    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def sweep(classes_path: Path, output_dir: Path, workers: int, max_seconds: float,
          max_iterations: int, cycle_limit: int, independent_solvers: tuple[str, ...]) -> dict:
    classification = json.loads(classes_path.read_text())
    tasks = []
    for item in classification["classes"]:
        representative = item["representative"]
        tasks.append((
            item["class_id"], representative["a"], representative["c"],
            str(output_dir), max_seconds, max_iterations, cycle_limit,
            independent_solvers,
        ))
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    records = []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_solve_class, task): task[0] for task in tasks}
        for future in as_completed(futures):
            record = future.result()
            records.append(record)
            print(
                f"[{len(records)}/{len(tasks)}] {record['class_id']} "
                f"{record['status']} models={record.get('models_checked')} "
                f"resumed={record.get('resumed')}",
                flush=True,
            )
            if record["status"] == "SAT":
                for pending in futures:
                    pending.cancel()
                break
    records.sort(key=lambda item: item["class_id"])
    status_counts = {
        status: sum(record["status"] == status for record in records)
        for status in sorted({record["status"] for record in records})
    }
    summary = {
        "status": "COMPLETE" if len(records) == len(tasks) and status_counts == {"UNSAT": len(tasks)} else "INCOMPLETE",
        "classes_expected": len(tasks),
        "classes_finished": len(records),
        "status_counts": status_counts,
        "workers": workers,
        "limits": {
            "max_seconds_per_class": max_seconds,
            "max_iterations_per_class": max_iterations,
            "cycles_per_length_per_model": cycle_limit,
        },
        "independent_solvers": list(independent_solvers),
        "wall_seconds": round(time.monotonic() - started, 6),
        "records": [{
            "class_id": record["class_id"],
            "parameters": record["parameters"],
            "status": record["status"],
            "models_checked": record.get("models_checked"),
            "learned_cycle_clauses": record.get("learned_cycle_clauses"),
            "models_by_shortest_power_cycle": record.get("models_by_shortest_power_cycle"),
            "elapsed_seconds": record.get("elapsed_seconds"),
            "resumed": record.get("resumed"),
            "final_cnf_gzip_sha256": record.get("final_cnf_gzip_sha256"),
            "final_cnf_independent_solvers": record.get("final_cnf_independent_solvers"),
        } for record in records],
    }
    (output_dir / "sweep.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def write_inventory(data_dir: Path) -> dict:
    """Validate and hash the complete exact/proof-core artifact set."""
    classes = json.loads((data_dir / "classes.json").read_text())
    class_ids = [item["class_id"] for item in classes["classes"]]
    if len(class_ids) != 324 or len(set(class_ids)) != 324:
        raise AssertionError("classification does not contain 324 distinct classes")
    exact_sweep = json.loads((data_dir / "sweep.json").read_text())
    if exact_sweep.get("status") != "COMPLETE" or exact_sweep.get("status_counts") != {"UNSAT": 324}:
        raise AssertionError("exact sweep summary is not complete UNSAT over 324 classes")
    proof_sweep = json.loads((data_dir / "proof_core_sweep.json").read_text())
    if proof_sweep.get("status") != "COMPLETE" or proof_sweep.get("classes") != 324:
        raise AssertionError("proof-core sweep summary is not complete over 324 classes")

    files = []
    aggregate_rows = []
    total_bytes = 0
    exact_records = []
    proof_records = []
    global_motif_cuts = Counter()
    global_motif_classes = Counter()
    for class_id in class_ids:
        class_dir = data_dir / class_id
        result = json.loads((class_dir / "result.json").read_text())
        if result.get("status") != "UNSAT":
            raise AssertionError(f"{class_id} exact status is not UNSAT")
        confirmations = result.get("final_cnf_independent_solvers", {})
        if set(confirmations) != {"cadical195", "lingeling"} or any(
            item.get("status") != "UNSAT" for item in confirmations.values()
        ):
            raise AssertionError(f"{class_id} lacks both independent UNSAT confirmations")
        proof = json.loads((class_dir / "proof_core_summary.json").read_text())
        if proof.get("schema_version") != 4 or proof.get("status") != "VERIFIED_UNSAT_PROOF_CORE":
            raise AssertionError(f"{class_id} lacks a schema-4 verified proof core")
        if not proof.get("drat_extraction_verified") or not proof.get("drat_core_reverified"):
            raise AssertionError(f"{class_id} proof trace was not independently verified")
        if proof.get("independent_core_solver", {}).get("status") != "UNSAT":
            raise AssertionError(f"{class_id} proof core lacks independent UNSAT confirmation")
        with gzip.open(class_dir / "proof_core_analysis.json.gz", "rt") as source:
            analysis = json.load(source)
        if analysis.get("status") != "PASS" or analysis.get("class_id") != class_id:
            raise AssertionError(f"{class_id} semantic proof-core analysis is invalid")
        if len(analysis["retained_matching_cardinality_clauses"]) != proof[
            "retained_matching_cardinality_clauses"
        ] or len(analysis["retained_cycle_cuts"]) != proof["retained_cycle_cuts"]:
            raise AssertionError(f"{class_id} semantic proof-core counts disagree")
        for motif in analysis["motif_clusters"]:
            key = (
                motif["source_length"], motif["matching_edges"],
                tuple(motif["core_path_names"]),
            )
            global_motif_cuts[key] += motif["cuts"]
            global_motif_classes[key] += 1
        exact_records.append(result)
        proof_records.append(proof)

        for relative in (
            Path(class_id) / "result.json",
            Path(class_id) / "final.cnf.gz",
            Path(class_id) / "proof_core_summary.json",
            Path(class_id) / "proof_core.cnf.gz",
            Path(class_id) / "proof_core_analysis.json.gz",
        ):
            path = data_dir / relative
            digest = sha256_bytes(path.read_bytes())
            size = path.stat().st_size
            files.append({"path": str(relative), "bytes": size, "sha256": digest})
            aggregate_rows.append(f"{relative}\t{size}\t{digest}\n")
            total_bytes += size
        if files[-4]["sha256"] != result.get("final_cnf_gzip_sha256"):
            raise AssertionError(f"{class_id} final CNF hash mismatch")
        if files[-2]["sha256"] != proof.get("proof_core_cnf_gzip_sha256"):
            raise AssertionError(f"{class_id} proof-core CNF hash mismatch")
        if files[-1]["sha256"] != proof.get("proof_core_analysis_gzip_sha256"):
            raise AssertionError(f"{class_id} proof-core analysis hash mismatch")

    def number_summary(values: list[int | float]) -> dict:
        return {
            "minimum": min(values),
            "median": statistics.median(values),
            "maximum": max(values),
            "sum": sum(values),
        }

    shortest_counts = Counter()
    learned_clause_sizes = Counter()
    for result in exact_records:
        shortest_counts.update({
            int(length): count
            for length, count in result["models_by_shortest_power_cycle"].items()
        })
        learned_clause_sizes.update({
            int(size): count for size, count in result["learned_clause_sizes"].items()
        })
    proof_length_counts = Counter()
    proof_length_class_incidence = Counter()
    for proof in proof_records:
        local = {
            int(length): count
            for length, count in proof["cycle_cut_source_lengths"].items()
        }
        proof_length_counts.update(local)
        proof_length_class_incidence.update(local.keys())
    aggregate = {
        "status": "PASS",
        "classes": len(class_ids),
        "exact": {
            "status_counts": {"UNSAT": len(exact_records)},
            "models_checked": number_summary([r["models_checked"] for r in exact_records]),
            "learned_cycle_clauses": number_summary([
                r["learned_cycle_clauses"] for r in exact_records
            ]),
            "final_clauses": number_summary([
                r["base_clauses"] + r["learned_cycle_clauses"] for r in exact_records
            ]),
            "sat_variables": number_summary([r["sat_variables"] for r in exact_records]),
            "safe_edges": number_summary([
                r["compatibility"]["safe_edges"] for r in exact_records
            ]),
            "cegar_elapsed_seconds": number_summary([
                r["elapsed_seconds"] for r in exact_records
            ]),
            "models_by_shortest_power_cycle": {
                str(length): count for length, count in sorted(shortest_counts.items())
            },
            "learned_clause_sizes": {
                str(size): count for size, count in sorted(learned_clause_sizes.items())
            },
            "classes_with_higher_order_cuts_by_source_length": {
                str(length): sum(
                    result["models_by_shortest_power_cycle"].get(str(length), 0) > 0
                    for result in exact_records
                ) for length in (4, 8, 16, 32, 64)
            },
            "independent_solver_elapsed_seconds": {
                solver: number_summary([
                    r["final_cnf_independent_solvers"][solver]["elapsed_seconds"]
                    for r in exact_records
                ]) for solver in ("cadical195", "lingeling")
            },
        },
        "proof_cores": {
            "status_counts": {"VERIFIED_UNSAT_PROOF_CORE": len(proof_records)},
            "original_clauses": number_summary([
                r["original_clauses"] for r in proof_records
            ]),
            "proof_core_clauses": number_summary([
                r["proof_core_clauses"] for r in proof_records
            ]),
            "reduction_fraction": number_summary([
                r["reduction_fraction"] for r in proof_records
            ]),
            "retained_matching_cardinality_clauses": number_summary([
                r["retained_matching_cardinality_clauses"] for r in proof_records
            ]),
            "retained_cycle_cuts": number_summary([
                r["retained_cycle_cuts"] for r in proof_records
            ]),
            "cycle_cut_source_lengths": {
                str(length): count for length, count in sorted(proof_length_counts.items())
            },
            "classes_using_source_length": {
                str(length): proof_length_class_incidence[length]
                for length in sorted(proof_length_class_incidence)
            },
            "deficient_vertex_support": number_summary([
                r["support"]["deficient_vertices"] for r in proof_records
            ]),
            "safe_matching_variable_support": number_summary([
                r["support"]["safe_matching_variables"] for r in proof_records
            ]),
            "motif_clusters": number_summary([r["motif_clusters"] for r in proof_records]),
            "extraction_elapsed_seconds": number_summary([
                r["elapsed_seconds"] for r in proof_records
            ]),
            "global_topology_aware_motif_clusters": len(global_motif_cuts),
            "global_motif_clusters": [{
                "source_length": key[0],
                "matching_edges": key[1],
                "core_path_names": list(key[2]),
                "retained_cuts": cuts,
                "classes": global_motif_classes[key],
            } for key, cuts in sorted(
                global_motif_cuts.items(), key=lambda item: (-item[1], item[0]),
            )],
        },
    }
    aggregate_path = data_dir / "aggregate_summary.json"
    aggregate_path.write_text(json.dumps(aggregate, indent=2, sort_keys=True) + "\n")

    for relative in map(Path, (
        "classes.json", "isomorphism_maps.json", "representatives.g6",
        "representatives.s6", "sweep.json", "proof_core_sweep.json",
        "aggregate_summary.json",
    )):
        path = data_dir / relative
        digest = sha256_bytes(path.read_bytes())
        size = path.stat().st_size
        files.append({"path": str(relative), "bytes": size, "sha256": digest})
        aggregate_rows.append(f"{relative}\t{size}\t{digest}\n")
        total_bytes += size

    inventory = {
        "status": "PASS",
        "scope": "all exact class results, final CNFs, proof-core summaries, and proof-core CNFs",
        "classes": len(class_ids),
        "files": len(files),
        "total_bytes": total_bytes,
        "aggregate_sha256": sha256_bytes("".join(aggregate_rows).encode()),
        "entries": files,
    }
    (data_dir / "inventory.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n"
    )
    return inventory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classify", action="store_true")
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--classes", type=Path)
    parser.add_argument("--workers", type=int, default=max(1, min(4, os.cpu_count() or 1)))
    parser.add_argument("--max-seconds", type=float, default=300.0)
    parser.add_argument("--max-iterations", type=int, default=1_000_000)
    parser.add_argument("--cycle-limit", type=int, default=20_000)
    parser.add_argument("--independent-solvers", default="cadical195,lingeling")
    args = parser.parse_args()
    if sum((args.classify, args.sweep, args.inventory)) != 1:
        parser.error("choose exactly one of --classify, --sweep, and --inventory")
    if args.classify:
        result = classify_j4()
        write_classification(result, args.data_dir)
        print(json.dumps({
            "status": result["status"],
            "rooted_translations": result["rooted_translations"],
            "ordinary_isomorphism_classes": result["ordinary_isomorphism_classes"],
            "automorphism_group_size_distribution": result["automorphism_group_size_distribution"],
        }, sort_keys=True))
    elif args.sweep:
        classes_path = args.classes or args.data_dir / "classes.json"
        summary = sweep(
            classes_path, args.data_dir, args.workers, args.max_seconds,
            args.max_iterations, args.cycle_limit,
            tuple(value for value in args.independent_solvers.split(",") if value),
        )
        print(json.dumps({key: summary[key] for key in (
            "status", "classes_expected", "classes_finished", "status_counts", "wall_seconds",
        )}, sort_keys=True))
    else:
        inventory = write_inventory(args.data_dir)
        print(json.dumps({key: inventory[key] for key in (
            "status", "classes", "files", "total_bytes", "aggregate_sha256",
        )}, sort_keys=True))


if __name__ == "__main__":
    main()
