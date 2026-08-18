"""Complete rooted order-nine Type-A closure and three-copy census (E23b).

The pipeline is deliberately finite and manifest-driven:

1. generate every unlabeled simple biconnected J on 9 vertices in the exact
   edge range 13..30 with nauty ``geng -C -d2``;
2. enumerate oriented closure edges xy with d_J(x)=2 and apply the Type-A
   degree filter after deleting xy;
3. deduplicate color-preserving rooted isomorphism classes with nauty
   ``labelg`` (x and y occupy distinct singleton color classes);
4. construct every three-copy lift and test C4/C8/C16 directly with the
   validated Python DFS and an independent C implementation;
5. record the definition-first reduced SPQR decomposition and keep
   SP-eligible/rigid-forced statistics separate;
6. only for internally clean bridges, enumerate Lambda, dyadic witnesses,
   overlap, symmetric-difference cycles, and SPQR locations.

Run ``--prepare`` before ``--run``.  The latter refuses an incomplete shard
plan, so a partially launched split can never be reported complete.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import itertools
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys
from collections import Counter

import networkx as nx

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, has_cycle_len_dfs
from gadget_criticality import spqr_decomposition_record
from linkage_data import (
    omega,
    symmetric_difference_cycle_decomposition,
)


ORDER = 9
BRIDGE_MIN_EDGES = 12
CLOSURE_MIN_EDGES = 13
CLOSURE_MAX_EDGES = 30
FORBIDDEN_LIFT_LENGTHS = (4, 8, 16)
ROOT_PARTITION = "ab" + "z" * (ORDER - 2)


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_output(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def nauty_version():
    located = shutil.which("geng")
    if located is None:
        raise RuntimeError("geng is not installed")
    executable = pathlib.Path(located).resolve()
    parts = executable.parts
    version = "unknown"
    if "nauty" in parts:
        index = parts.index("nauty")
        if index + 1 < len(parts):
            version = parts[index + 1]
    return {"version": version, "geng_path": str(executable)}


def generator_command(residue=0, modulus=1):
    return [
        "geng", "-C", "-d2", str(ORDER),
        f"{CLOSURE_MIN_EDGES}:{CLOSURE_MAX_EDGES}",
        f"{residue}/{modulus}",
    ]


def edge_bound_derivation():
    return {
        "B_lower": (
            "d_B(x)=1, d_B(y)>=1, and seven internal degrees >=3 give "
            "degree sum >=23; parity forces >=24, hence |E(B)|>=12"
        ),
        "J_lower": "J adds the absent closure edge xy, hence |E(J)|>=13",
        "J_upper": (
            "d_J(x)=2, so at most all C(8,2)=28 edges away from x plus "
            "its two incident edges: |E(J)|<=30"
        ),
    }


def prepare_manifest(manifest_path: pathlib.Path, artifact_path: pathlib.Path):
    if manifest_path.exists():
        raise FileExistsError(f"refusing to overwrite existing manifest {manifest_path}")
    script = pathlib.Path(__file__).resolve()
    c_source = script.with_name("check_power_masks.c")
    commit = git_output("rev-parse", "HEAD")
    status = git_output("status", "--short")
    command = generator_command()
    payload = {
        "experiment": "E23b-order9-Type-A",
        "status": "PLANNED",
        "created_at": utc_now(),
        "source_commit": commit,
        "working_tree_dirty_at_prepare": bool(status),
        "scope": {
            "bridge_order": ORDER,
            "bridge_order_definition": "|V(B)|",
            "three_copy_order": 3 * (ORDER - 2) + 2,
            "forbidden_lengths": list(FORBIDDEN_LIFT_LENGTHS),
            "edge_bounds": edge_bound_derivation(),
        },
        "software": {
            "python": platform.python_version(),
            "networkx": nx.__version__,
            "nauty": nauty_version(),
            "biconnected_flag": "-C (confirmed from installed geng -help)",
        },
        "programs": {
            "search": {"path": str(script.relative_to(pathlib.Path.cwd())),
                       "sha256": sha256_file(script)},
            "independent_C_detector": {
                "path": str(c_source.relative_to(pathlib.Path.cwd())),
                "sha256": sha256_file(c_source),
                "compile_command": [
                    "cc", "-O3", "-std=c11", str(c_source),
                    "-o", ".venv/check_power_masks",
                ],
            },
        },
        "generator": {
            "command": command,
            "command_string": " ".join(command),
            "shard_modulus": 1,
            "planned_residues": [0],
            "shards": [{"residue": 0, "modulus": 1, "status": "PLANNED"}],
        },
        "rooted_canonicalization": {
            "command": ["labelg", "-q", f"-f{ROOT_PARTITION}"],
            "partition": {
                "x": "singleton a at vertex 0",
                "y": "singleton b at vertex 1",
                "other_vertices": "common z cell",
            },
            "roles_interchangeable": False,
        },
        "outputs": {"candidate_records_gzip": str(artifact_path)},
        "counts": None,
        "checksums": None,
        "exit_codes": None,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"prepared complete 1/1 shard plan at {manifest_path}")


def root_relabelled_g6(graph: nx.Graph, x, y) -> str:
    remaining = sorted(set(graph) - {x, y})
    mapping = {x: 0, y: 1}
    mapping.update({vertex: index + 2 for index, vertex in enumerate(remaining)})
    rooted = nx.Graph()
    rooted.add_nodes_from(range(len(graph)))
    rooted.add_edges_from((mapping[u], mapping[v]) for u, v in graph.edges())
    return ordered_graph6(rooted)


def ordered_graph6(graph: nx.Graph) -> str:
    """Encode integer labels in numerical order, independent of insertion."""
    ordered = nx.Graph()
    ordered.add_nodes_from(sorted(graph))
    ordered.add_edges_from(graph.edges())
    return nx.to_graph6_bytes(ordered, header=False).decode().strip()


def candidate_root_pairs(graph: nx.Graph):
    for x in graph:
        if graph.degree(x) != 2:
            continue
        for y in graph.neighbors(x):
            yield x, y


def passes_degree_filter(graph_j: nx.Graph, x, y) -> bool:
    return (
        graph_j.degree(x) == 2
        and graph_j.has_edge(x, y)
        and graph_j.degree(y) >= 2
        and all(graph_j.degree(vertex) >= 3
                for vertex in graph_j if vertex not in (x, y))
    )


def canonicalize_rooted(entries):
    input_bytes = b"".join(
        entry["root_relabelled_g6"].encode() + b"\n" for entry in entries
    )
    command = ["labelg", "-q", f"-f{ROOT_PARTITION}"]
    proc = subprocess.run(command, input=input_bytes, capture_output=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode(errors="replace"))
    canonical = proc.stdout.decode().splitlines()
    if len(canonical) != len(entries):
        raise RuntimeError("labelg did not return one graph per rooted input")
    unique = {}
    canonical_digest = hashlib.sha256()
    for entry, g6 in zip(entries, canonical, strict=True):
        canonical_digest.update(g6.encode() + b"\n")
        entry = {**entry, "rooted_canonical_g6": g6}
        unique.setdefault(g6, entry)
    return list(unique.values()), {
        "command": command,
        "exit_code": proc.returncode,
        "stderr": proc.stderr.decode(errors="replace").strip(),
        "canonical_stream_sha256_before_dedup": canonical_digest.hexdigest(),
    }


def collect_rooted_population():
    command = generator_command()
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None
    raw_digest = hashlib.sha256()
    raw_closures = rooted_edges = degree_filtered = 0
    entries = []
    for raw in proc.stdout:
        raw_digest.update(raw)
        raw_closures += 1
        g6 = raw.strip().decode()
        graph = nx.from_graph6_bytes(g6.encode())
        for x, y in candidate_root_pairs(graph):
            rooted_edges += 1
            if not passes_degree_filter(graph, x, y):
                continue
            degree_filtered += 1
            entries.append({
                "source_closure_g6": g6,
                "source_x": x,
                "source_y": y,
                "root_relabelled_g6": root_relabelled_g6(graph, x, y),
            })
    stderr = proc.stderr.read().decode(errors="replace") if proc.stderr else ""
    exit_code = proc.wait()
    if exit_code:
        raise RuntimeError(f"geng exited {exit_code}: {stderr}")
    unique, labelg_report = canonicalize_rooted(entries)
    return unique, {
        "generator_command": command,
        "generator_exit_code": exit_code,
        "generator_stderr": stderr.strip(),
        "raw_generator_stream_sha256": raw_digest.hexdigest(),
        "raw_closure_count": raw_closures,
        "rooted_edge_count": rooted_edges,
        "degree_filtered_count": degree_filtered,
        "rooted_isomorphism_count": len(unique),
        "labelg": labelg_report,
    }


def graph_to_detector_dict(graph: nx.Graph):
    vertices = sorted(graph)
    remap = {vertex: index for index, vertex in enumerate(vertices)}
    return from_edges(
        len(vertices), [(remap[u], remap[v]) for u, v in graph.edges()]
    )


def python_power_mask(graph: nx.Graph) -> int:
    simple = graph_to_detector_dict(graph)
    mask = 0
    for bit, length in enumerate(FORBIDDEN_LIFT_LENGTHS):
        if length <= len(simple) and has_cycle_len_dfs(simple, length):
            mask |= 1 << bit
    return mask


def mask_lengths(mask):
    return [length for bit, length in enumerate(FORBIDDEN_LIFT_LENGTHS)
            if mask & (1 << bit)]


def construct_three_copy_lift(graph_b: nx.Graph, x, y):
    lift = nx.Graph()
    mappings = []
    internal = sorted(set(graph_b) - {x, y})
    for copy_index in range(3):
        mapping = {x: 0, y: 1}
        mapping.update({
            vertex: 2 + copy_index * len(internal) + index
            for index, vertex in enumerate(internal)
        })
        mappings.append(mapping)
        lift = nx.compose(lift, nx.relabel_nodes(graph_b, mapping, copy=True))
    return lift, mappings


def compile_c_detector(binary: pathlib.Path):
    source = pathlib.Path(__file__).with_name("check_power_masks.c")
    command = ["cc", "-O3", "-std=c11", str(source), "-o", str(binary)]
    proc = subprocess.run(command, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    version = subprocess.check_output(["cc", "--version"], text=True).splitlines()[0]
    return {
        "command": command,
        "exit_code": proc.returncode,
        "compiler_version": version,
        "source_sha256": sha256_file(source),
        "binary_sha256": sha256_file(binary),
    }


def c_power_masks(binary: pathlib.Path, graph6_records):
    payload = b"".join(g6.encode() + b"\n" for g6 in graph6_records)
    proc = subprocess.run([str(binary)], input=payload, capture_output=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode(errors="replace"))
    masks = [int(line) for line in proc.stdout.splitlines()]
    if len(masks) != len(graph6_records):
        raise RuntimeError("C detector output cardinality mismatch")
    return masks, {
        "exit_code": proc.returncode,
        "stderr": proc.stderr.decode(errors="replace").strip(),
        "input_count": len(graph6_records),
        "input_stream_sha256": sha256_bytes(payload),
        "output_stream_sha256": sha256_bytes(proc.stdout),
    }


def minimal_candidate_analysis(entry):
    graph_j = nx.from_graph6_bytes(entry["root_relabelled_g6"].encode())
    x, y = 0, 1
    if not passes_degree_filter(graph_j, x, y):
        raise AssertionError("root relabeling changed the degree filter")
    graph_b = graph_j.copy()
    graph_b.remove_edge(x, y)
    lift, mappings = construct_three_copy_lift(graph_b, x, y)
    if graph_b.has_edge(x, y):
        raise AssertionError("B contains the forbidden terminal edge")
    simple = (not nx.number_of_selfloops(lift)
              and lift.number_of_edges() == 3 * graph_b.number_of_edges())
    connected = nx.is_connected(lift)
    minimum_degree = min(dict(lift.degree()).values())
    if not (simple and connected and len(lift) == 23 and minimum_degree >= 3):
        raise AssertionError("three-copy lift failed a structural invariant")
    bridge_g6 = ordered_graph6(graph_b)
    lift_g6 = ordered_graph6(lift)
    return {
        **entry,
        "bridge_g6": bridge_g6,
        "lift_g6": lift_g6,
        "bridge_edges": graph_b.number_of_edges(),
        "dB_y": graph_b.degree(y),
        "structural_class": (
            "SP-eligible" if graph_b.degree(y) == 1 else "rigid-forced"
        ),
        "bridge_python_mask": python_power_mask(graph_b),
        "lift_python_mask": python_power_mask(lift),
        "lift_structure": {
            "simple": simple,
            "connected": connected,
            "order": len(lift),
            "edges": lift.number_of_edges(),
            "minimum_degree": minimum_degree,
        },
        "mapping_rule": (
            "shared terminals 0,1; copy i internal vertices occupy "
            "2+7*i through 8+7*i"
        ),
    }


def _path_edges(path):
    return {frozenset((u, v)) for u, v in zip(path, path[1:])}


def _divergence_reconvergence_pairs(left, right):
    positions_right = {vertex: index for index, vertex in enumerate(right)}
    common = [vertex for vertex in left if vertex in positions_right]
    pairs = []
    for start, end in zip(common, common[1:]):
        li, lj = left.index(start), left.index(end)
        ri, rj = positions_right[start], positions_right[end]
        if li > lj or ri > rj:
            continue
        if left[li:lj + 1] != right[ri:rj + 1]:
            pairs.append((start, end))
    return pairs


def internally_clean_details(graph_b, decomposition_record):
    paths = list(nx.all_simple_paths(graph_b, 0, 1, cutoff=ORDER - 1))
    spectrum = sorted({len(path) - 1 for path in paths})
    hits = sorted({a + b for a in spectrum for b in spectrum}
                  & set(FORBIDDEN_LIFT_LENGTHS))
    nodes_by_pair = {}
    for node in decomposition_record["nodes"]:
        vertices = {item["vertex"] for item in node["degree_profile"]}
        for u, v in itertools.combinations(sorted(vertices), 2):
            nodes_by_pair.setdefault((u, v), []).append(node["index"])
    witnesses = {str(hit): [] for hit in hits}
    for left_index, left in enumerate(paths):
        for right_index in range(left_index, len(paths)):
            right = paths[right_index]
            total = len(left) + len(right) - 2
            if total not in hits:
                continue
            shared_edges = len(_path_edges(left) & _path_edges(right))
            cycles = symmetric_difference_cycle_decomposition(left, right)
            divergence = []
            for u, v in _divergence_reconvergence_pairs(left, right):
                divergence.append({
                    "vertices": [u, v],
                    "spqr_nodes_containing_both": nodes_by_pair.get(tuple(sorted((u, v))), []),
                })
            witnesses[str(total)].append({
                "path_indices": [left_index, right_index],
                "paths": [left, right],
                "shared_edge_count": shared_edges,
                "omega_cross_check": omega(left, right),
                "symmetric_difference_cycle_count": len(cycles),
                "symmetric_difference_cycle_lengths": sorted(cycles),
                "divergence_reconvergence": divergence,
            })
    minimum_overlap = {
        hit: min((w["shared_edge_count"] for w in witnesses[hit]), default=None)
        for hit in witnesses
    }
    return {
        "terminal_paths": paths,
        "Lambda": spectrum,
        "dyadic_self_sum_hits": hits,
        "h": len(hits),
        "minimum_shared_edge_count_by_hit": minimum_overlap,
        "witnesses": witnesses,
    }


def final_candidate_record(entry):
    graph_j = nx.from_graph6_bytes(entry["root_relabelled_g6"].encode())
    graph_b = graph_j.copy()
    graph_b.remove_edge(0, 1)
    decomposition = spqr_decomposition_record(
        graph_j, graph_b, 0, 1, cross_check_package=False
    )
    has_r = decomposition["node_type_counts"].get("R", 0) > 0
    if entry["structural_class"] == "rigid-forced" and not has_r:
        raise AssertionError("rigid-forced closure has no validated R-node")
    if entry["structural_class"] == "SP-eligible":
        spqr_output = {
            "series_parallel": not has_r,
            "complete_reduced_decomposition": decomposition,
        }
    else:
        r_nodes = [node for node in decomposition["nodes"] if node["type"] == "R"]
        spqr_output = {
            "R_node_count": len(r_nodes),
            "R_nodes": r_nodes,
            "node_type_counts": decomposition["node_type_counts"],
            "validation": decomposition["validation"],
        }

    internal_clean = entry["bridge_python_mask"] == 0
    near = internally_clean_details(graph_b, decomposition) if internal_clean else None
    self_sum_clean = internal_clean and near["h"] == 0
    lift_clean = entry["lift_python_mask"] == 0
    if lift_clean != self_sum_clean:
        raise AssertionError("three-copy equivalence failed")

    candidate_id = sha256_bytes(entry["rooted_canonical_g6"].encode())[:20]
    return {
        "candidate_id": candidate_id,
        "source": {
            "closure_g6": entry["source_closure_g6"],
            "x": entry["source_x"],
            "y": entry["source_y"],
        },
        "rooted_canonical_closure_g6": entry["rooted_canonical_g6"],
        "bridge_g6": entry["bridge_g6"],
        "bridge_order": ORDER,
        "bridge_edges": entry["bridge_edges"],
        "terminal_degrees": {"x": 1, "y": entry["dB_y"]},
        "structural_class": entry["structural_class"],
        "spqr": spqr_output,
        "internal_power_cycles": {
            "python_mask": entry["bridge_python_mask"],
            "C_mask": entry["bridge_c_mask"],
            "lengths": mask_lengths(entry["bridge_python_mask"]),
            "clean": internal_clean,
        },
        "three_copy_lift": {
            **entry["lift_structure"],
            "g6": entry["lift_g6"],
            "mapping_rule": entry["mapping_rule"],
            "python_mask": entry["lift_python_mask"],
            "C_mask": entry["lift_c_mask"],
            "cycle_lengths_present": mask_lengths(entry["lift_python_mask"]),
            "power_cycle_free": lift_clean,
        },
        "equivalence": {
            "internal_clean_and_self_sum_clean": self_sum_clean,
            "lift_power_cycle_free": lift_clean,
            "agrees": lift_clean == self_sum_clean,
        },
        "near_gadget": near,
    }


def run_search(manifest_path: pathlib.Path, workers: int):
    manifest = json.loads(manifest_path.read_text())
    generator = manifest["generator"]
    planned = set(generator["planned_residues"])
    shard_residues = {shard["residue"] for shard in generator["shards"]}
    expected = set(range(generator["shard_modulus"]))
    if planned != expected or shard_residues != expected:
        raise RuntimeError("manifest does not contain a complete shard plan")
    if manifest["status"] != "PLANNED":
        raise RuntimeError(f"manifest status is {manifest['status']!r}, not PLANNED")

    manifest["status"] = "RUNNING"
    manifest["started_at"] = utc_now()
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    population, generation = collect_rooted_population()
    print(f"raw closures={generation['raw_closure_count']} rooted edges="
          f"{generation['rooted_edge_count']} degree-filtered="
          f"{generation['degree_filtered_count']} rooted-isomorphism="
          f"{generation['rooted_isomorphism_count']}")

    # The records are small enough for the n=9 range; deterministic map order
    # is retained even when workers>1.
    if workers > 1:
        import multiprocessing as mp
        with mp.Pool(workers) as pool:
            analyzed = list(pool.imap(minimal_candidate_analysis, population, chunksize=64))
    else:
        analyzed = [minimal_candidate_analysis(entry) for entry in population]

    binary = pathlib.Path(".venv/check_power_masks").resolve()
    compile_report = compile_c_detector(binary)
    bridge_masks, bridge_c_report = c_power_masks(
        binary, [entry["bridge_g6"] for entry in analyzed]
    )
    lift_masks, lift_c_report = c_power_masks(
        binary, [entry["lift_g6"] for entry in analyzed]
    )
    for entry, bridge_mask, lift_mask in zip(
        analyzed, bridge_masks, lift_masks, strict=True
    ):
        entry["bridge_c_mask"] = bridge_mask
        entry["lift_c_mask"] = lift_mask
        if entry["bridge_python_mask"] != bridge_mask:
            raise AssertionError("Python/C disagreement on B")
        if entry["lift_python_mask"] != lift_mask:
            raise AssertionError("Python/C disagreement on three-copy lift")

    artifact = pathlib.Path(manifest["outputs"]["candidate_records_gzip"])
    artifact.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    h_histogram = Counter()
    minimum_positive_h = None
    survivors = []
    with gzip.open(artifact, "wt", encoding="utf-8", compresslevel=9) as output:
        # SPQR serialization is the expensive second phase.  Keep output
        # deterministic and stream records directly into the compressed file.
        if workers > 1:
            import multiprocessing as mp
            with mp.Pool(workers) as pool:
                records = pool.imap(final_candidate_record, analyzed, chunksize=16)
                for record in records:
                    output.write(json.dumps(record, sort_keys=True) + "\n")
                    _update_counts(counts, h_histogram, survivors, record)
        else:
            for entry in analyzed:
                record = final_candidate_record(entry)
                output.write(json.dumps(record, sort_keys=True) + "\n")
                _update_counts(counts, h_histogram, survivors, record)

    positives = [value for value in h_histogram if value > 0]
    minimum_positive_h = min(positives, default=None)
    if survivors:
        preserved = [preserve_survivor(record) for record in survivors]
        manifest["status"] = "SURVIVOR_FOUND"
        manifest["stopped_at"] = utc_now()
        manifest["survivor_artifacts"] = preserved
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        raise SystemExit(
            "TYPE-A COUNTEREXAMPLE SURVIVOR FOUND; preserve artifact and "
            "run standalone escalation before any further shard"
        )

    counts.update({
        "raw_closure_count": generation["raw_closure_count"],
        "rooted_edge_count": generation["rooted_edge_count"],
        "degree_filtered_count": generation["degree_filtered_count"],
        "rooted_isomorphism_count": generation["rooted_isomorphism_count"],
    })
    manifest["status"] = "COMPLETE"
    manifest["completed_at"] = utc_now()
    manifest["generator"]["shards"][0].update({
        "status": "COMPLETE",
        "exit_code": generation["generator_exit_code"],
        "raw_closure_count": generation["raw_closure_count"],
        "raw_stream_sha256": generation["raw_generator_stream_sha256"],
    })
    manifest["counts"] = dict(sorted(counts.items()))
    manifest["near_gadgets"] = {
        "h_histogram_among_internally_clean": {
            str(key): value for key, value in sorted(h_histogram.items())
        },
        "minimum_observed_positive_h": minimum_positive_h,
        "overlap_program_instantiated": bool(h_histogram),
    }
    manifest["checksums"] = {
        "raw_generator_stream_sha256": generation["raw_generator_stream_sha256"],
        "canonical_rooted_stream_sha256_before_dedup": generation["labelg"][
            "canonical_stream_sha256_before_dedup"
        ],
        "candidate_records_gzip_sha256": sha256_file(artifact),
        "candidate_records_gzip_bytes": artifact.stat().st_size,
        "search_script_sha256_at_completion": sha256_file(pathlib.Path(__file__)),
        "C_detector_source_sha256": compile_report["source_sha256"],
        "C_detector_binary_sha256": compile_report["binary_sha256"],
    }
    manifest["commands"] = {
        "generator": generation["generator_command"],
        "rooted_canonicalization": generation["labelg"]["command"],
        "C_detector_compile": compile_report["command"],
        "run": [
            sys.executable, str(pathlib.Path(__file__)), "--run",
            "--manifest", str(manifest_path), "--workers", str(workers),
        ],
    }
    manifest["exit_codes"] = {
        "generator": generation["generator_exit_code"],
        "labelg": generation["labelg"]["exit_code"],
        "C_detector_compile": compile_report["exit_code"],
        "C_detector_bridge_batch": bridge_c_report["exit_code"],
        "C_detector_lift_batch": lift_c_report["exit_code"],
        "search": 0,
    }
    manifest["detector_batches"] = {
        "bridge": bridge_c_report,
        "three_copy_lift": lift_c_report,
    }
    manifest["generator"]["stderr"] = generation["generator_stderr"]
    manifest["rooted_canonicalization"]["stderr"] = generation["labelg"]["stderr"]
    manifest["software"]["C_compiler"] = compile_report["compiler_version"]
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest["counts"], indent=2, sort_keys=True))
    print(f"candidate artifact: {artifact} ({artifact.stat().st_size} bytes)")


def _update_counts(counts, h_histogram, survivors, record):
    counts["candidate_records"] += 1
    counts[record["structural_class"]] += 1
    if (record["structural_class"] == "SP-eligible"
            and record["spqr"]["series_parallel"]):
        counts["SP_eligible_series_parallel"] += 1
    if record["internal_power_cycles"]["clean"]:
        counts["internally_power_free"] += 1
        h = record["near_gadget"]["h"]
        h_histogram[h] += 1
    if record["three_copy_lift"]["power_cycle_free"]:
        counts["three_copy_power_free"] += 1
        survivors.append(record)
    if record["equivalence"]["agrees"]:
        counts["three_copy_equivalence_agrees"] += 1


def preserve_survivor(record):
    """Create the full stop-and-escalate artifact bundle required by T6."""
    directory = pathlib.Path("data/counterexamples") / record["candidate_id"]
    directory.mkdir(parents=True, exist_ok=True)
    graph_b = nx.from_graph6_bytes(record["bridge_g6"].encode())
    lift, mappings = construct_three_copy_lift(graph_b, 0, 1)
    graph6 = ordered_graph6(lift)
    sparse6 = nx.to_sparse6_bytes(lift, header=False).decode().strip()
    cycle_spectrum = sorted({len(cycle) for cycle in nx.simple_cycles(lift)})
    automorphisms = sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(
        lift, lift
    ).isomorphisms_iter())
    invariants = {
        "order": len(lift),
        "edges": lift.number_of_edges(),
        "girth": nx.girth(lift),
        "diameter": nx.diameter(lift),
        "degree_sequence": sorted((degree for _, degree in lift.degree()), reverse=True),
        "vertex_connectivity": nx.node_connectivity(lift),
        "automorphism_group_size": automorphisms,
        "full_cycle_length_spectrum": cycle_spectrum,
        "python_power_mask_rerun": python_power_mask(lift),
    }
    (directory / "lift.g6").write_text(graph6 + "\n")
    (directory / "lift.s6").write_text(sparse6 + "\n")
    (directory / "lift.edges.json").write_text(
        json.dumps(sorted([sorted(edge) for edge in lift.edges()]), indent=2) + "\n"
    )
    (directory / "bridge.g6").write_text(record["bridge_g6"] + "\n")
    (directory / "bridge.s6").write_text(
        nx.to_sparse6_bytes(graph_b, header=False).decode().strip() + "\n"
    )
    (directory / "bridge.edges.json").write_text(
        json.dumps(sorted([sorted(edge) for edge in graph_b.edges()]), indent=2) + "\n"
    )
    (directory / "three_copy_mappings.json").write_text(
        json.dumps(mappings, indent=2, sort_keys=True) + "\n"
    )
    (directory / "invariants.json").write_text(
        json.dumps(invariants, indent=2, sort_keys=True) + "\n"
    )
    standalone = f'''#!/usr/bin/env python3
N = {len(lift)}
EDGES = {sorted([tuple(sorted(edge)) for edge in lift.edges()])!r}
ADJ = {{v: set() for v in range(N)}}
for u, v in EDGES:
    assert u != v and v not in ADJ[u]
    ADJ[u].add(v); ADJ[v].add(u)
assert min(map(len, ADJ.values())) >= 3
def has_cycle(length):
    for root in range(N):
        path = [root]; seen = {{root}}
        def dfs(current):
            if len(path) == length:
                return root in ADJ[current]
            for nxt in ADJ[current]:
                if nxt < root or nxt in seen: continue
                seen.add(nxt); path.append(nxt)
                if dfs(nxt): return True
                path.pop(); seen.remove(nxt)
            return False
        if dfs(root): return True
    return False
assert all(not has_cycle(length) for length in (4, 8, 16))
print("STANDALONE COUNTEREXAMPLE VERIFICATION PASS")
'''
    (directory / "verify_standalone.py").write_text(standalone)
    return {
        "candidate_id": record["candidate_id"],
        "directory": str(directory),
        "lift_g6_sha256": sha256_file(directory / "lift.g6"),
        "standalone_verifier_sha256": sha256_file(directory / "verify_standalone.py"),
    }


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--prepare", action="store_true")
    action.add_argument("--run", action="store_true")
    parser.add_argument(
        "--manifest", type=pathlib.Path,
        default=pathlib.Path("manifests/E23_order9_manifest.json"),
    )
    parser.add_argument(
        "--artifact", type=pathlib.Path,
        default=pathlib.Path("data/E23_order9_candidates.jsonl.gz"),
    )
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()
    if args.prepare:
        prepare_manifest(args.manifest, args.artifact)
    else:
        run_search(args.manifest, args.workers)


if __name__ == "__main__":
    main()
