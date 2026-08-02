"""Adversarial finite audit for R2 and the reduced SPQR leaf theorems."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys
from collections import Counter

import networkx as nx

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from bridge_closure_search import find_J_candidates
from brute_spqr import decompose
from gadget_criticality import (
    leaf_spqr_classification,
    parallel_union_preserves_2connectivity,
    r2_holds_for_edge,
    rigid_leaf_dichotomy,
    sumset,
    t8r_edge_is_degree_critical,
    terminal_path_spectrum,
)


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def synthetic_parallel_fixture() -> dict:
    left = nx.path_graph([0, 2, 1])
    right = nx.path_graph([0, 3, 4, 1])
    union = parallel_union_preserves_2connectivity([left, right], 0, 1)
    theta = union.copy()
    theta.add_edge(0, 1)
    decomposition = decompose(theta)
    p_edges = decomposition.real_p_edges()
    return {
        "union_2connected": nx.is_biconnected(union),
        "real_P_edges": [list(edge) for edge in p_edges],
        "R2_holds": all(r2_holds_for_edge(theta, edge) for edge in p_edges),
        "P_node_tree_degrees": [
            len(decomposition.adjacency[index])
            for index, node in enumerate(decomposition.nodes) if node.type == "P"
        ],
    }


def atlas_audit() -> dict:
    counts = Counter()
    violations = []
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() < 3 or not nx.is_biconnected(graph):
            continue
        counts["biconnected_graphs"] += 1
        decomposition = decompose(graph)
        for index, node in enumerate(decomposition.nodes):
            if node.type == "P" and len(decomposition.adjacency[index]) <= 1:
                violations.append({
                    "kind": "leaf_P",
                    "g6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                    "node": index,
                })
            if node.type == "P":
                counts["P_nodes"] += 1
        for edge in decomposition.real_p_edges():
            counts["real_P_edges"] += 1
            if r2_holds_for_edge(graph, edge):
                counts["R2_preserved"] += 1
            else:
                violations.append({
                    "kind": "R2",
                    "g6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
                    "edge": list(edge),
                })
    return {"counts": dict(sorted(counts.items())), "violations": violations}


def relaxed_closure_audit(nmin=5, nmax=8) -> dict:
    counts = Counter()
    violations = []
    generator_reports = []
    for order in range(nmin, nmax + 1):
        command = ["geng", "-c", "-d2", str(order)]
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        assert proc.stdout is not None
        raw_count = 0
        for line in proc.stdout:
            raw_count += 1
            graph_j = nx.from_graph6_bytes(line.strip().encode())
            if not nx.is_biconnected(graph_j):
                continue
            for x, y in find_J_candidates(graph_j):
                counts["rooted_closures"] += 1
                graph_b = graph_j.copy()
                graph_b.remove_edge(x, y)
                decomposition = decompose(graph_j)
                all_rp_tight = True
                for node in decomposition.nodes:
                    if node.type not in ("R", "P"):
                        continue
                    for skeleton_edge in node.edges:
                        if skeleton_edge.virtual:
                            continue
                        edge = skeleton_edge.endpoints
                        if not graph_b.has_edge(*edge):
                            continue
                        if not t8r_edge_is_degree_critical(graph_b, x, y, edge):
                            all_rp_tight = False
                for edge in decomposition.real_p_edges():
                    if set(edge) == {x, y}:
                        counts["excluded_closure_P_edges"] += 1
                        continue
                    counts["real_P_B_edge_instances"] += 1
                    if r2_holds_for_edge(graph_j, edge):
                        counts["R2_preserved"] += 1
                    else:
                        violations.append({
                            "kind": "R2",
                            "order": order,
                            "g6": line.strip(),
                            "x": x,
                            "y": y,
                            "edge": list(edge),
                        })
                    if t8r_edge_is_degree_critical(graph_b, x, y, edge):
                        counts["T8P_degree_critical"] += 1
                    else:
                        counts["T8P_noncritical_deletion_certificates"] += 1

                leaves = leaf_spqr_classification(
                    graph_j, graph_b, x, y, decomposition=decomposition
                )
                counts["S_leaf_instances"] += len(leaves["S_leaves"])
                counts["P_leaf_instances"] += len(leaves["P_leaves"])
                for leaf in leaves["S_leaves"]:
                    counts[f"S_leaf_{leaf['classification']}"] += 1
                if not leaves["valid_Type_A_leaf_classification"]:
                    violations.append({
                        "kind": "leaf_classification",
                        "order": order,
                        "g6": line.strip(),
                        "x": x,
                        "y": y,
                        "report": leaves,
                    })
                dichotomy = rigid_leaf_dichotomy(
                    graph_j, graph_b, x, y, decomposition=decomposition
                )
                counts[f"rigid_leaf_{dichotomy['case']}"] += 1
                paths = terminal_path_spectrum(graph_b, x, y)
                self_sum_hits = sorted(sumset(paths, paths) & {4, 8})
                if all_rp_tight:
                    counts["RP_tight_rooted_closures"] += 1
                if all_rp_tight and graph_b.degree(y) >= 2 and not self_sum_hits:
                    counts["rigid_clean_tight_prerequisite_closures"] += 1
                    counts[
                        "rigid_clean_tight_leaf_holds"
                        if dichotomy["holds"]
                        else "rigid_clean_tight_leaf_failures"
                    ] += 1
                elif not dichotomy["holds"]:
                    counts["out_of_scope_rigid_leaf_shape_failures"] += 1
                    for hit in self_sum_hits:
                        counts[f"out_of_scope_leaf_failure_self_sum_{hit}"] += 1
                if (all_rp_tight and graph_b.degree(y) >= 2
                        and not self_sum_hits and not dichotomy["holds"]):
                    violations.append({
                        "kind": "rigid_clean_tight_leaf_dichotomy",
                        "order": order,
                        "g6": line.strip(),
                        "x": x,
                        "y": y,
                        "self_sum_hits": self_sum_hits,
                        "report": dichotomy,
                    })
        stderr = proc.stderr.read() if proc.stderr else ""
        exit_code = proc.wait()
        generator_reports.append({
            "order": order,
            "command": command,
            "raw_graphs": raw_count,
            "exit_code": exit_code,
            "stderr": stderr.strip(),
        })
        if exit_code:
            raise RuntimeError(f"geng failed at order {order}")
    return {
        "range": [nmin, nmax],
        "counts": dict(sorted(counts.items())),
        "generator_reports": generator_reports,
        "violations": violations[:20],
        "violation_count": len(violations),
    }


def run(output: pathlib.Path) -> dict:
    script = pathlib.Path(__file__)
    synthetic = synthetic_parallel_fixture()
    atlas = atlas_audit()
    relaxed = relaxed_closure_audit()
    failure_count = len(atlas["violations"]) + relaxed["violation_count"]
    report = {
        "experiment": "E24c-R2-SPQR-leaf-audit",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "script": str(script),
        "script_sha256": sha256_file(script),
        "synthetic_P_fixture": synthetic,
        "graph_atlas": atlas,
        "relaxed_closures": relaxed,
        "failure_count": failure_count,
        "status": "COMPLETE" if failure_count == 0 else "FAILURE_FOUND",
        "exit_code": 0 if failure_count == 0 else 1,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=pathlib.Path,
        default=pathlib.Path("manifests/E24_spqr_audit_manifest.json"),
    )
    args = parser.parse_args()
    report = run(args.output)
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["failure_count"]:
        raise SystemExit("SPQR ADVERSARIAL FAILURE FOUND")


if __name__ == "__main__":
    main()
