#!/usr/bin/env python3
"""Mine canonical local witness patterns from the completed E24 leaf-R data.

This script does not generate graphs and does not recompute an SPQR census. It
streams E23 and E24 in their preserved common order, uses the stored R-skeleton
and stored leaf annotations, and extracts a canonical C4/C8 in each archived
leaf pertinent graph.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
E23 = ROOT / "data" / "E23_order9_candidates.jsonl.gz"
E24 = ROOT / "data" / "E24_order9_spqr_obstructions.jsonl.gz"
E23_SHA = "9f530d95918406bec166cc3e09fa5edf0d7b8f8ff58613b9ffae83c85851e446"
E24_SHA = "e6723280ec82e02f125730958279e219b61d5939ecd8b8dba8cce1732684ca0e"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_key(u: int, v: int) -> tuple[int, int]:
    return tuple(sorted((u, v)))


def canonical_cycle(graph: nx.Graph, length: int) -> tuple[int, ...] | None:
    best = None
    for root in sorted(graph):
        path = [root]
        seen = {root}

        def dfs(current: int) -> None:
            nonlocal best
            if len(path) == length:
                if graph.has_edge(current, root):
                    forward = tuple(path)
                    reverse = (root,) + tuple(reversed(path[1:]))
                    candidate = min(forward, reverse)
                    if best is None or candidate < best:
                        best = candidate
                return
            for neighbor in sorted(graph.neighbors(current)):
                if neighbor <= root or neighbor in seen:
                    continue
                seen.add(neighbor)
                path.append(neighbor)
                dfs(neighbor)
                path.pop()
                seen.remove(neighbor)

        dfs(root)
        if best is not None:
            break
    return best


def cycle_pattern(
    cycle: tuple[int, ...],
    poles: set[int],
    degree: dict[int, int],
    converted_edges: set[tuple[int, int]],
) -> str:
    """Dihedral canonical word; parent poles are deliberately interchangeable."""

    def vertex_label(v: int) -> str:
        location = "p" if v in poles else "i"
        tightness = "3" if degree[v] == 3 else "+"
        return location + tightness

    candidates = []
    n = len(cycle)
    for direction in (1, -1):
        for start in range(n):
            pairs = []
            for offset in range(n):
                i = (start + direction * offset) % n
                j = (i + direction) % n
                edge_label = "V" if edge_key(cycle[i], cycle[j]) in converted_edges else "R"
                pairs.append(f"{vertex_label(cycle[i])}:{edge_label}")
            candidates.append("/".join(pairs))
    return f"C{n}|" + min(candidates)


def mine() -> dict:
    if sha256(E23) != E23_SHA or sha256(E24) != E24_SHA:
        raise AssertionError("archived input checksum mismatch")

    exact = Counter()
    coarse = Counter()
    spectra = Counter()
    real_only_spectra = Counter()
    orientation_class = Counter()
    residual_structural_class = Counter()
    representatives = {}
    records = 0
    candidate_records = 0
    e23_count = 0
    e24_count = 0
    with gzip.open(E23, "rt") as left, gzip.open(E24, "rt") as right:
        while True:
            line23 = left.readline()
            line24 = right.readline()
            if not line23 and not line24:
                break
            if not line23 or not line24:
                raise AssertionError("E23/E24 record-count mismatch")
            e23_count += 1
            e24_count += 1
            item23 = json.loads(line23)
            item24 = json.loads(line24)
            if item23["candidate_id"] != item24["candidate_id"]:
                raise AssertionError("E23/E24 common order was not preserved")
            leaves = item24["leaf_R_nodes"]
            if not leaves:
                continue
            candidate_records += 1
            if "R_nodes" in item23["spqr"]:
                r_nodes = item23["spqr"]["R_nodes"]
            else:
                r_nodes = [
                    node
                    for node in item23["spqr"]["complete_reduced_decomposition"]["nodes"]
                    if node["type"] == "R"
                ]
            for leaf in leaves:
                records += 1
                matching_nodes = [
                    node
                    for node in r_nodes
                    if len(node["degree_profile"]) == leaf["skeleton_order"]
                    and len(node["skeleton_edges"]) == leaf["skeleton_size"]
                    and sum(not edge["virtual"] for edge in node["skeleton_edges"])
                    == leaf["original_real_edge_count"]
                    and any(
                        edge["virtual"]
                        and {edge["u"], edge["v"]}
                        == set(leaf["parent_virtual_edge"]["edge"])
                        for edge in node["skeleton_edges"]
                    )
                    and sorted(
                        vertex["vertex"]
                        for vertex in node["degree_profile"]
                        if vertex["vertex"] == 0
                        or (vertex["vertex"] not in (0, 1) and vertex["B_degree"] == 3)
                        or (vertex["vertex"] == 1 and item23["terminal_degrees"]["y"] == 1)
                    )
                    == leaf["tight_vertices"]
                    and (
                        leaf["tight_cover_exists"]
                        or sorted(
                            list(edge_key(*edge["edge"]))
                            for edge in node["real_edges"]
                            if edge["in_B"]
                        )
                        == sorted(leaf["uncovered_real_B_edges"])
                    )
                ]
                if len(matching_nodes) != 1:
                    raise AssertionError(
                        "stored leaf R-node does not map uniquely into E23: "
                        f"candidate={item24['candidate_id']} leaf={leaf} "
                        f"matches={[node['index'] for node in matching_nodes]}"
                    )
                node = matching_nodes[0]
                graph = nx.Graph()
                graph.add_nodes_from(vertex["vertex"] for vertex in node["degree_profile"])
                real_edges = set()
                for edge in node["skeleton_edges"]:
                    if not edge["virtual"]:
                        key = edge_key(edge["u"], edge["v"])
                        graph.add_edge(*key)
                        real_edges.add(key)
                converted = {
                    edge_key(*edge)
                    for edge in leaf["converted_terminal_edges_after_suppression"]
                }
                if len(converted) > 1:
                    raise AssertionError("a core leaf has multiple suppressed-S neighbors")
                graph.add_edges_from(converted)
                parent = edge_key(*leaf["parent_virtual_edge"]["edge"])
                if graph.has_edge(*parent) and parent not in real_edges:
                    graph.remove_edge(*parent)

                spectrum = tuple(leaf["internal_C4_C8_spectrum"])
                length = min(spectrum)
                real_graph = nx.Graph()
                real_graph.add_nodes_from(graph.nodes())
                real_graph.add_edges_from(real_edges)
                real_spectrum = tuple(
                    candidate_length
                    for candidate_length in (4, 8)
                    if canonical_cycle(real_graph, candidate_length) is not None
                )
                # Among shortest witnesses, prefer zero virtual expansions;
                # only then use the lexicographically canonical full witness.
                cycle = canonical_cycle(real_graph, length)
                if cycle is None:
                    cycle = canonical_cycle(graph, length)
                if cycle is None:
                    raise AssertionError("archived leaf spectrum has no local witness")
                if len(cycle) != min(spectrum):
                    raise AssertionError("canonical local witness contradicts stored spectrum")

                degree = {
                    vertex["vertex"]: vertex["B_degree"]
                    for vertex in node["degree_profile"]
                }
                poles = set(parent)
                witness_edges = {
                    edge_key(cycle[i], cycle[(i + 1) % length]) for i in range(length)
                }
                virtual_used = len(witness_edges & converted)
                degree3 = sum(degree[v] == 3 for v in cycle)
                pole_count = len(set(cycle) & poles)
                terminal_two_paths = pole_count == 2
                pattern = cycle_pattern(cycle, poles, degree, converted)
                exact[pattern] += 1
                coarse[(length, virtual_used, degree3, pole_count, terminal_two_paths)] += 1
                spectra[spectrum] += 1
                real_only_spectra[real_spectrum] += 1
                leaf_orientation = (
                    "root_side_exposed_after_terminal_S_suppression"
                    if converted
                    else "genuine_original_remote_R_leaf"
                )
                orientation_class[(leaf_orientation, bool(real_spectrum))] += 1
                if not real_spectrum:
                    residual_structural_class[item24["structural_class"]] += 1
                representatives.setdefault(
                    pattern,
                    {
                        "candidate_id": item24["candidate_id"],
                        "leaf_node": leaf["node"],
                        "cycle": list(cycle),
                        "parent_poles": sorted(poles),
                        "converted_virtual_edges": [list(edge) for edge in sorted(converted)],
                        "skeleton_order": leaf["skeleton_order"],
                        "skeleton_size": leaf["skeleton_size"],
                        "tight_cover_exists": leaf["tight_cover_exists"],
                    },
                )

    if records != 75745 or e23_count != 129040 or e24_count != 129040:
        raise AssertionError("archived completeness counts changed")

    exact_rows = []
    for pattern, count in sorted(exact.items(), key=lambda item: (-item[1], item[0])):
        exact_rows.append(
            {
                "pattern": pattern,
                "count": count,
                "representative": representatives[pattern],
            }
        )
    coarse_rows = [
        {
            "cycle_length": key[0],
            "virtual_expansions_used": key[1],
            "degree3_vertices_on_witness": key[2],
            "parent_poles_on_witness": key[3],
            "two_terminal_paths_form_cycle": key[4],
            "count": count,
        }
        for key, count in sorted(coarse.items(), key=lambda item: (-item[1], item[0]))
    ]
    return {
        "schema": "erdos64-leaf-r-patterns-v1",
        "method": "stream and join preserved E23/E24 records; no graph generation and no SPQR recomputation",
        "inputs": {
            "E23": {"path": str(E23.relative_to(ROOT)), "sha256": E23_SHA, "records": 129040},
            "E24": {"path": str(E24.relative_to(ROOT)), "sha256": E24_SHA, "records": 129040},
        },
        "script": {
            "path": str(Path(__file__).resolve().relative_to(ROOT)),
            "sha256": sha256(Path(__file__).resolve()),
        },
        "candidate_records_with_leaf_R": candidate_records,
        "leaf_R_records": records,
        "stored_spectra": {",".join(map(str, key)): value for key, value in sorted(spectra.items())},
        "real_edge_only_spectra": {
            (",".join(map(str, key)) if key else "clean"): value
            for key, value in sorted(real_only_spectra.items())
        },
        "leaf_orientation_classes": {
            orientation: {
                "records": sum(
                    count
                    for (kind, _), count in orientation_class.items()
                    if kind == orientation
                ),
                "real_edge_C4_C8_positive": orientation_class[(orientation, True)],
                "real_edge_C4_C8_clean": orientation_class[(orientation, False)],
            }
            for orientation in (
                "genuine_original_remote_R_leaf",
                "root_side_exposed_after_terminal_S_suppression",
            )
        },
        "real_edge_clean_by_structural_class": dict(
            sorted(residual_structural_class.items())
        ),
        "exact_pattern_definition": "dihedral cyclic word of pole/internal, B-degree=3/high, and real/converted-virtual edge labels; parent poles interchangeable",
        "exact_patterns_required_for_full_coverage": len(exact_rows),
        "exact_patterns": exact_rows,
        "coarse_pattern_count": len(coarse_rows),
        "coarse_patterns": coarse_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = mine()
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        f"leaf_R={report['leaf_R_records']} exact_patterns="
        f"{report['exact_patterns_required_for_full_coverage']} "
        f"coarse_patterns={report['coarse_pattern_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
