"""Restricted direct Type-A bridge search at order 10 and m in {13,14}.

This deliberately generates bridges B, not closures J.  The generator's
``-f`` option removes C4s at generation time; exact Python and independent C
detectors then check C8 and every direct three-copy lift.  A complete 1/1
manifest must exist before ``--run`` is accepted.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import json
import pathlib
import platform
import subprocess
import sys
from collections import Counter

import networkx as nx

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from type_a_order9_search import (
    c_power_masks,
    compile_c_detector,
    construct_three_copy_lift,
    mask_lengths,
    ordered_graph6,
    python_power_mask,
    sha256_file,
)


ORDER = 10
EDGE_LAYERS = (13, 14)
ROOT_PARTITION = "ab" + "z" * (ORDER - 2)
DYADIC_LENGTHS = {4, 8, 16}


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_output(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def generator_command(edges: int) -> list[str]:
    if edges == 13:
        # Degree sum 26 attains 1+1+8*3 exactly, so maximum degree is 3.
        maximum_degree = 3
    elif edges == 14:
        # Only two excess degree units exist above 1+1+8*3.
        maximum_degree = 5
    else:
        raise ValueError("the certified order-10 search has only m=13,14")
    return [
        "geng", "-c", "-f", "-d1", f"-D{maximum_degree}",
        str(ORDER), f"{edges}:{edges}", "0/1",
    ]


def edge_bound_derivation() -> dict:
    return {
        "general": (
            "2|E(B)| >= d(x)+d(y)+sum_internal d(v) >= "
            "1+1+3(n-2)=3n-4, hence |E(B)|>=ceil((3n-4)/2)"
        ),
        "order_10": "|E(B)|>=13",
        "m13_max_degree": "degree sum attains the lower bound, so Delta(B)<=3",
        "m14_max_degree": (
            "two excess degree units above the lower bound imply Delta(B)<=5"
        ),
    }


def prepare_manifest(manifest_path: pathlib.Path, artifact_path: pathlib.Path):
    if manifest_path.exists():
        raise FileExistsError(f"refusing to overwrite {manifest_path}")
    script = pathlib.Path(__file__).resolve()
    c_source = script.with_name("check_power_masks.c")
    commands = {str(edges): generator_command(edges) for edges in EDGE_LAYERS}
    payload = {
        "experiment": "E24b-order10-direct-Type-A",
        "status": "PLANNED",
        "created_at": utc_now(),
        "source_commit": git_output("rev-parse", "HEAD"),
        "working_tree_dirty_at_prepare": bool(git_output("status", "--short")),
        "scope": {
            "bridge_order": ORDER,
            "edge_layers": list(EDGE_LAYERS),
            "three_copy_order": 3 * (ORDER - 2) + 2,
            "edge_bound": edge_bound_derivation(),
            "generator_C4_filter": (
                "-f, confirmed by installed geng -help as only generate "
                "4-cycle-free graphs"
            ),
        },
        "software": {
            "python": platform.python_version(),
            "networkx": nx.__version__,
            "nauty_geng": subprocess.check_output(
                ["sh", "-c", "command -v geng"], text=True
            ).strip(),
        },
        "programs": {
            "search": {
                "path": "verifier/type_a_order10_direct.py",
                "sha256": sha256_file(script),
            },
            "independent_C_detector": {
                "path": "verifier/check_power_masks.c",
                "sha256": sha256_file(c_source),
            },
        },
        "generator": {
            "commands": commands,
            "shard_modulus": 1,
            "planned_residues": [0],
            "layers": {
                str(edges): {
                    "edges": edges,
                    "residue": 0,
                    "modulus": 1,
                    "status": "PLANNED",
                }
                for edges in EDGE_LAYERS
            },
        },
        "rooted_canonicalization": {
            "command": ["labelg", "-q", f"-f{ROOT_PARTITION}"],
            "x": "singleton color a at vertex 0",
            "y": "singleton color b at vertex 1",
            "roles_interchangeable": False,
        },
        "filter_order": [
            "geng connected simple C4-free generation",
            "absence of C8",
            "oriented d_B(x)=1 terminal choices",
            "d_B(y)>=1 and all internal degrees >=3",
            "xy absent",
            "B+xy 2-connected",
            "rooted oriented isomorphism",
            "internal power-cycle cleanliness",
            "terminal dyadic self-sum cleanliness",
            "direct three-copy lift verification",
        ],
        "outputs": {"candidate_records_gzip": str(artifact_path)},
        "counts_by_edge_layer": None,
        "checksums": None,
        "exit_codes": None,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def collect_layer(edges: int) -> tuple[list[str], dict]:
    command = generator_command(edges)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None
    digest = hashlib.sha256()
    records = []
    for raw in proc.stdout:
        digest.update(raw)
        records.append(raw.strip().decode())
    stderr = proc.stderr.read().decode(errors="replace") if proc.stderr else ""
    exit_code = proc.wait()
    if exit_code:
        raise RuntimeError(f"geng m={edges} exited {exit_code}: {stderr}")
    return records, {
        "command": command,
        "exit_code": exit_code,
        "stderr": stderr.strip(),
        "raw_count": len(records),
        "raw_stream_sha256": digest.hexdigest(),
    }


def rooted_entries(graph: nx.Graph, source_g6: str):
    for x in graph:
        if graph.degree(x) != 1:
            continue
        for y in graph:
            if y == x:
                continue
            yield x, y, {
                "source_g6": source_g6,
                "source_x": x,
                "source_y": y,
            }


def passes_internal_degrees(graph: nx.Graph, x, y) -> bool:
    return (
        graph.degree(y) >= 1
        and all(graph.degree(vertex) >= 3
                for vertex in graph if vertex not in (x, y))
    )


def root_relabelled_g6(graph: nx.Graph, x, y) -> str:
    remaining = sorted(set(graph) - {x, y})
    mapping = {x: 0, y: 1}
    mapping.update({vertex: index + 2 for index, vertex in enumerate(remaining)})
    rooted = nx.Graph()
    rooted.add_nodes_from(range(len(graph)))
    rooted.add_edges_from((mapping[u], mapping[v]) for u, v in graph.edges())
    return ordered_graph6(rooted)


def canonicalize(entries: list[dict]) -> tuple[list[dict], dict]:
    payload = b"".join(
        entry["root_relabelled_g6"].encode() + b"\n" for entry in entries
    )
    command = ["labelg", "-q", f"-f{ROOT_PARTITION}"]
    proc = subprocess.run(command, input=payload, capture_output=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode(errors="replace"))
    outputs = proc.stdout.decode().splitlines()
    if len(outputs) != len(entries):
        raise RuntimeError("labelg output cardinality mismatch")
    unique = {}
    digest = hashlib.sha256()
    for entry, canonical in zip(entries, outputs, strict=True):
        digest.update(canonical.encode() + b"\n")
        unique.setdefault(canonical, {
            **entry,
            "rooted_canonical_g6": canonical,
        })
    return list(unique.values()), {
        "command": command,
        "exit_code": proc.returncode,
        "stderr": proc.stderr.decode(errors="replace").strip(),
        "canonical_stream_sha256_before_dedup": digest.hexdigest(),
    }


def analyze_root(entry: dict) -> dict:
    graph_b = nx.from_graph6_bytes(entry["rooted_canonical_g6"].encode())
    if graph_b.degree(0) != 1 or graph_b.has_edge(0, 1):
        raise AssertionError("rooted canonicalization changed the terminal roles")
    internal_mask = python_power_mask(graph_b)
    paths = list(nx.all_simple_paths(graph_b, 0, 1, cutoff=ORDER - 1))
    spectrum = sorted({len(path) - 1 for path in paths})
    hits = sorted({a + b for a in spectrum for b in spectrum} & DYADIC_LENGTHS)
    lift, mappings = construct_three_copy_lift(graph_b, 0, 1)
    simple = (not nx.number_of_selfloops(lift)
              and lift.number_of_edges() == 3 * graph_b.number_of_edges())
    connected = nx.is_connected(lift)
    minimum_degree = min(dict(lift.degree()).values())
    if not (simple and connected and len(lift) == 26 and minimum_degree >= 3):
        raise AssertionError("three-copy lift failed a structural invariant")
    return {
        **entry,
        "bridge_g6": ordered_graph6(graph_b),
        "lift_g6": ordered_graph6(lift),
        "terminal_degrees": {"x": 1, "y": graph_b.degree(1)},
        "internal_python_mask": internal_mask,
        "Lambda": spectrum,
        "dyadic_self_sum_hits": hits,
        "h": len(hits),
        "self_sum_clean": not hits,
        "lift_python_mask": python_power_mask(lift),
        "lift_structure": {
            "simple": simple,
            "connected": connected,
            "order": len(lift),
            "edges": lift.number_of_edges(),
            "minimum_degree": minimum_degree,
        },
        "mapping_rule": (
            "shared terminals 0,1; copy i uses internal labels "
            "2+8*i through 9+8*i"
        ),
        "mapping_count": len(mappings),
    }


def run_search(manifest_path: pathlib.Path):
    manifest = json.loads(manifest_path.read_text())
    if manifest["status"] != "PLANNED":
        raise RuntimeError("the order-10 manifest is not in PLANNED state")
    if set(manifest["generator"]["layers"]) != {"13", "14"}:
        raise RuntimeError("the complete two-layer plan is absent")
    script_sha = sha256_file(pathlib.Path(__file__))
    if script_sha != manifest["programs"]["search"]["sha256"]:
        raise RuntimeError("search source changed after manifest preparation")

    manifest["status"] = "RUNNING"
    manifest["started_at"] = utc_now()
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    binary = pathlib.Path(".venv/check_power_masks_order10").resolve()
    compile_report = compile_c_detector(binary)
    artifact_path = pathlib.Path(manifest["outputs"]["candidate_records_gzip"])
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    counts_by_layer = {}
    generation_reports = {}
    canonical_reports = {}
    detector_reports = {}
    all_records = []
    survivors = []
    for edges in EDGE_LAYERS:
        raw, generation = collect_layer(edges)
        generation_reports[str(edges)] = generation
        raw_c_masks, raw_c_report = c_power_masks(binary, raw)
        counts = Counter(raw_graphs=len(raw))
        entries = []
        for g6, c_mask in zip(raw, raw_c_masks, strict=True):
            graph = nx.from_graph6_bytes(g6.encode())
            python_mask = python_power_mask(graph)
            if python_mask != c_mask:
                raise AssertionError("Python/C disagreement on a generated bridge")
            if c_mask & 1:
                counts["generator_C4_violations"] += 1
            if c_mask & 2:
                continue
            counts["C8_free_graphs"] += 1
            for x, y, entry in rooted_entries(graph, g6):
                counts["oriented_degree1_x_pairs"] += 1
                if not passes_internal_degrees(graph, x, y):
                    continue
                counts["internal_degree_filtered_pairs"] += 1
                if graph.has_edge(x, y):
                    continue
                counts["terminal_edge_absent_pairs"] += 1
                closure = graph.copy()
                closure.add_edge(x, y)
                if not nx.is_biconnected(closure):
                    continue
                counts["closure_2connected_pairs"] += 1
                entries.append({
                    **entry,
                    "edge_layer": edges,
                    "root_relabelled_g6": root_relabelled_g6(graph, x, y),
                })
        unique, canonical = canonicalize(entries)
        canonical_reports[str(edges)] = canonical
        counts["rooted_isomorphism_count"] = len(unique)
        analyzed = [analyze_root(entry) for entry in unique]
        lift_masks, lift_c_report = c_power_masks(
            binary, [entry["lift_g6"] for entry in analyzed]
        )
        for entry, lift_c_mask in zip(analyzed, lift_masks, strict=True):
            entry["lift_C_mask"] = lift_c_mask
            if entry["lift_python_mask"] != lift_c_mask:
                raise AssertionError("Python/C disagreement on an order-10 lift")
            internal_clean = entry["internal_python_mask"] == 0
            lift_clean = entry["lift_python_mask"] == 0
            equivalence = internal_clean and entry["self_sum_clean"]
            counts["internally_power_free"] += internal_clean
            counts["self_sum_clean"] += entry["self_sum_clean"]
            counts["three_copy_power_free"] += lift_clean
            counts["three_copy_equivalence_agrees"] += lift_clean == equivalence
            counts[f"h={entry['h']}"] += 1
            record = {
                "candidate_id": sha256_bytes(
                    entry["rooted_canonical_g6"].encode()
                )[:20],
                "edge_layer": edges,
                "source": {
                    "g6": entry["source_g6"],
                    "x": entry["source_x"],
                    "y": entry["source_y"],
                },
                "rooted_canonical_bridge_g6": entry["rooted_canonical_g6"],
                "bridge_g6": entry["bridge_g6"],
                "terminal_degrees": entry["terminal_degrees"],
                "internal_power_cycles": {
                    "python_mask": entry["internal_python_mask"],
                    "C_mask": 0,
                    "lengths": mask_lengths(entry["internal_python_mask"]),
                    "clean": internal_clean,
                },
                "terminal_paths": {
                    "Lambda": entry["Lambda"],
                    "dyadic_self_sum_hits": entry["dyadic_self_sum_hits"],
                    "h": entry["h"],
                    "clean": entry["self_sum_clean"],
                },
                "three_copy_lift": {
                    **entry["lift_structure"],
                    "g6": entry["lift_g6"],
                    "mapping_rule": entry["mapping_rule"],
                    "python_mask": entry["lift_python_mask"],
                    "C_mask": entry["lift_C_mask"],
                    "cycle_lengths_present": mask_lengths(
                        entry["lift_python_mask"]
                    ),
                    "power_cycle_free": lift_clean,
                },
                "equivalence_agrees": lift_clean == equivalence,
            }
            all_records.append(record)
            if lift_clean:
                survivors.append(record)
        counts_by_layer[str(edges)] = dict(sorted(counts.items()))
        detector_reports[str(edges)] = {
            "raw_bridge_batch": raw_c_report,
            "lift_batch": lift_c_report,
        }

    with gzip.open(artifact_path, "wt", encoding="utf-8", compresslevel=9) as output:
        for record in all_records:
            output.write(json.dumps(record, sort_keys=True) + "\n")

    manifest["completed_at"] = utc_now()
    manifest["status"] = "SURVIVOR_FOUND" if survivors else "COMPLETE"
    manifest["counts_by_edge_layer"] = counts_by_layer
    manifest["generator_reports"] = generation_reports
    manifest["canonicalization_reports"] = canonical_reports
    manifest["detector_reports"] = detector_reports
    manifest["checksums"] = {
        "search_script_sha256_at_completion": script_sha,
        "C_detector_source_sha256": compile_report["source_sha256"],
        "C_detector_binary_sha256": compile_report["binary_sha256"],
        "candidate_records_gzip_sha256": sha256_file(artifact_path),
        "candidate_records_gzip_bytes": artifact_path.stat().st_size,
    }
    manifest["exit_codes"] = {
        "search": 0,
        "C_detector_compile": compile_report["exit_code"],
        "m13_generator": generation_reports["13"]["exit_code"],
        "m14_generator": generation_reports["14"]["exit_code"],
        "m13_labelg": canonical_reports["13"]["exit_code"],
        "m14_labelg": canonical_reports["14"]["exit_code"],
        "m13_raw_C_batch": detector_reports["13"]["raw_bridge_batch"]["exit_code"],
        "m14_raw_C_batch": detector_reports["14"]["raw_bridge_batch"]["exit_code"],
        "m13_lift_C_batch": detector_reports["13"]["lift_batch"]["exit_code"],
        "m14_lift_C_batch": detector_reports["14"]["lift_batch"]["exit_code"],
    }
    if survivors:
        manifest["survivors"] = survivors
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(counts_by_layer, indent=2, sort_keys=True))
    if survivors:
        raise SystemExit("TYPE-A SURVIVOR FOUND; stop and independently escalate")


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--prepare", action="store_true")
    action.add_argument("--run", action="store_true")
    parser.add_argument(
        "--manifest", type=pathlib.Path,
        default=pathlib.Path("manifests/E24_order10_manifest.json"),
    )
    parser.add_argument(
        "--artifact", type=pathlib.Path,
        default=pathlib.Path("data/E24_order10_candidates.jsonl.gz"),
    )
    args = parser.parse_args()
    if args.prepare:
        prepare_manifest(args.manifest, args.artifact)
    else:
        run_search(args.manifest)


if __name__ == "__main__":
    main()
