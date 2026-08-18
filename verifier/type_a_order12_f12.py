"""F12: exhaustive Type-A two-terminal search at order 12, m in {16,17}.

Proposition F12 (see separator_theorem_order32_gap_analysis.md MISSING-1):
every simple two-terminal graph B with |V(B)|=12, d_B(x)=1, d_B(y)>=1,
xy not in E(B), d_B(v)>=3 for every v not in {x,y}, and B+xy simple and
2-connected, contains a C4 or a C8.

Search-box derivation (re-derived independently here, matches the gap
analysis exactly): 2|E(B)| >= d(x)+d(y)+3*10 = 1+d(y)+30 >= 32 (since
d(y)>=1), so |E(B)|>=16. m=16 forces the degree sum to hit the floor
exactly: d(y)=1, every internal vertex exactly 3 -- sequence {1,1,3^10},
max degree 3. m=17 (one extra degree unit above the floor) admits four
sequences: {1,3,3^10}, {1,2,4,3^9}, {1,1,4,4,3^8}, {1,1,5,3^9} -- max
degree 5. B is {C4,C8}-free by hypothesis at every internal step, so
ex(12;{C4,C8})=17 (literature.md L15 table) already caps m<=17 for a
{C4,C8}-free graph -- consistent with the box being exactly {16,17}.

This deliberately reuses the exact same generation + dual-detector +
canonicalization methodology already certified for the order-9/10/11
F-series propositions (type_a_order9_search.py / type_a_order10_direct.py),
trimmed to only what F12 needs: no three-copy lift or terminal-path-
spectrum analysis (F12 is a standalone claim about the bridge B alone, not
about a T6 gadget built from three copies of it).
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

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from type_a_order9_search import (
    c_power_masks,
    compile_c_detector,
    mask_lengths,
    ordered_graph6,
    python_power_mask,
    sha256_file,
)

ORDER = 12
EDGE_LAYERS = (16, 17)
ROOT_PARTITION = "ab" + "z" * (ORDER - 2)


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_output(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def generator_command(edges: int) -> list[str]:
    if edges == 16:
        maximum_degree = 3
    elif edges == 17:
        maximum_degree = 5
    else:
        raise ValueError("F12 only searches m=16,17")
    return [
        "nauty-geng", "-c", "-f", "-d1", f"-D{maximum_degree}",
        str(ORDER), f"{edges}:{edges}", "0/1",
    ]


def edge_bound_derivation() -> dict:
    return {
        "general": (
            "2|E(B)| >= d(x)+d(y)+sum_internal d(v) >= "
            "1+1+3(n-2)=3n-4, hence |E(B)|>=ceil((3n-4)/2)"
        ),
        "order_12": "|E(B)|>=16",
        "m16_degree_sequence": "{1,1,3^10}, max degree 3 (tight floor)",
        "m17_degree_sequences": [
            "{1,3,3^10}", "{1,2,4,3^9}", "{1,1,4,4,3^8}", "{1,1,5,3^9}",
        ],
        "m17_max_degree": 5,
        "upper_cap": "ex(12;{C4,C8})=17 (literature.md L15) caps m<=17 independently",
    }


def prepare_manifest(manifest_path: pathlib.Path, artifact_path: pathlib.Path):
    if manifest_path.exists():
        raise FileExistsError(f"refusing to overwrite {manifest_path}")
    script = pathlib.Path(__file__).resolve()
    c_source = script.with_name("check_power_masks.c")
    commands = {str(edges): generator_command(edges) for edges in EDGE_LAYERS}
    payload = {
        "experiment": "F12-order12-Type-A",
        "status": "PLANNED",
        "created_at": utc_now(),
        "source_commit": git_output("rev-parse", "HEAD"),
        "working_tree_dirty_at_prepare": bool(git_output("status", "--short")),
        "scope": {
            "bridge_order": ORDER,
            "edge_layers": list(EDGE_LAYERS),
            "edge_bound": edge_bound_derivation(),
            "generator_C4_filter": "-f, generator generates only 4-cycle-free graphs",
        },
        "software": {
            "python": platform.python_version(),
            "networkx": nx.__version__,
            "nauty_geng": subprocess.check_output(
                ["sh", "-c", "command -v nauty-geng"], text=True
            ).strip(),
        },
        "programs": {
            "search": {"path": "verifier/type_a_order12_f12.py", "sha256": sha256_file(script)},
            "independent_C_detector": {
                "path": "verifier/check_power_masks.c",
                "sha256": sha256_file(c_source),
            },
        },
        "generator": {
            "commands": commands,
            "shard_modulus": 1,
            "planned_residues": [0],
        },
        "rooted_canonicalization": {
            "command": ["nauty-labelg", "-q", f"-f{ROOT_PARTITION}"],
            "x": "singleton color a at vertex 0 (the degree-1 terminal)",
            "y": "singleton color b at vertex 1",
            "roles_interchangeable": False,
        },
        "filter_order": [
            "geng connected simple C4-free generation",
            "absence of C8 (whole raw graph, before rooting)",
            "oriented d_B(x)=1 terminal choices",
            "d_B(y)>=1 and all internal degrees >=3",
            "xy absent",
            "B+xy 2-connected",
            "rooted oriented isomorphism dedup",
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
        "command": command, "exit_code": exit_code, "stderr": stderr.strip(),
        "raw_count": len(records), "raw_stream_sha256": digest.hexdigest(),
    }


def rooted_entries(graph: nx.Graph, source_g6: str):
    for x in graph:
        if graph.degree(x) != 1:
            continue
        for y in graph:
            if y == x:
                continue
            yield x, y, {"source_g6": source_g6, "source_x": x, "source_y": y}


def passes_internal_degrees(graph: nx.Graph, x, y) -> bool:
    return (
        graph.degree(y) >= 1
        and all(graph.degree(vertex) >= 3 for vertex in graph if vertex not in (x, y))
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
    payload = b"".join(entry["root_relabelled_g6"].encode() + b"\n" for entry in entries)
    command = ["nauty-labelg", "-q", f"-f{ROOT_PARTITION}"]
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
        unique.setdefault(canonical, {**entry, "rooted_canonical_g6": canonical})
    return list(unique.values()), {
        "command": command, "exit_code": proc.returncode,
        "stderr": proc.stderr.decode(errors="replace").strip(),
        "canonical_stream_sha256_before_dedup": digest.hexdigest(),
    }


def run_search(manifest_path: pathlib.Path):
    manifest = json.loads(manifest_path.read_text())
    if manifest["status"] != "PLANNED":
        raise RuntimeError("manifest is not in PLANNED state")
    if set(manifest["generator"]["commands"]) != {"16", "17"}:
        raise RuntimeError("the complete two-layer plan is absent")
    script_sha = sha256_file(pathlib.Path(__file__))
    if script_sha != manifest["programs"]["search"]["sha256"]:
        raise RuntimeError("search source changed after manifest preparation")

    manifest["status"] = "RUNNING"
    manifest["started_at"] = utc_now()
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    binary = pathlib.Path("/tmp/check_power_masks_order12").resolve()
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
                    **entry, "edge_layer": edges,
                    "root_relabelled_g6": root_relabelled_g6(graph, x, y),
                })
        unique, canonical = canonicalize(entries)
        canonical_reports[str(edges)] = canonical
        counts["rooted_isomorphism_count"] = len(unique)
        for entry in unique:
            record = {
                "candidate_id": sha256_bytes(entry["rooted_canonical_g6"].encode())[:20],
                "edge_layer": edges,
                "source": {"g6": entry["source_g6"], "x": entry["source_x"], "y": entry["source_y"]},
                "rooted_canonical_bridge_g6": entry["rooted_canonical_g6"],
            }
            all_records.append(record)
            survivors.append(record)  # every entry that survives to here is a genuine F12 survivor
        counts_by_layer[str(edges)] = dict(sorted(counts.items()))
        detector_reports[str(edges)] = {"raw_bridge_batch": raw_c_report}

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
        "m16_generator": generation_reports["16"]["exit_code"],
        "m17_generator": generation_reports["17"]["exit_code"],
        "m16_labelg": canonical_reports["16"]["exit_code"],
        "m17_labelg": canonical_reports["17"]["exit_code"],
        "m16_raw_C_batch": detector_reports["16"]["raw_bridge_batch"]["exit_code"],
        "m17_raw_C_batch": detector_reports["17"]["raw_bridge_batch"]["exit_code"],
    }
    if survivors:
        manifest["survivors"] = survivors
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(counts_by_layer, indent=2, sort_keys=True))
    if survivors:
        raise SystemExit("F12 SURVIVOR FOUND; stop and independently escalate")
    else:
        print("F12 PROVED: zero survivors across m=16,17.")


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--prepare", action="store_true")
    action.add_argument("--run", action="store_true")
    parser.add_argument("--manifest", type=pathlib.Path,
                         default=pathlib.Path("manifests/F12_order12_manifest.json"))
    parser.add_argument("--artifact", type=pathlib.Path,
                         default=pathlib.Path("data/F12_order12_candidates.jsonl.gz"))
    args = parser.parse_args()
    if args.prepare:
        prepare_manifest(args.manifest, args.artifact)
    else:
        run_search(args.manifest)


if __name__ == "__main__":
    main()
