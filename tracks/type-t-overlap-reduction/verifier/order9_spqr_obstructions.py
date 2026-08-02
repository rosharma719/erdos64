"""Mine shortest forbidden-cycle support from the existing E23 artifact.

No candidates are generated here.  The checksummed 129,040-record E23 gzip
artifact is streamed, each stored rooted closure is definition-first
decomposed again, and one canonical shortest B-cycle is projected onto its
reduced SPQR tree.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import itertools
import json
import multiprocessing as mp
import pathlib
import sys
import time
from collections import Counter

import networkx as nx

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from brute_spqr import decompose
from gadget_criticality import (
    leaf_spqr_classification,
    rigid_leaf_dichotomy,
    t8r_edge_is_degree_critical,
    terminal_path_spectrum,
)
from type_a_order9_search import python_power_mask, sha256_file


INPUT_ARTIFACT = pathlib.Path("data/E23_order9_candidates.jsonl.gz")
INPUT_SHA256 = "9f530d95918406bec166cc3e09fa5edf0d7b8f8ff58613b9ffae83c85851e446"


def edge_key(u, v):
    return tuple(sorted((u, v)))


def canonical_cycle(graph: nx.Graph, length: int) -> tuple[int, ...] | None:
    """Lexicographically first undirected simple cycle of an exact length."""
    best = None
    for root in sorted(graph):
        path = [root]
        seen = {root}

        def dfs(current):
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
        if best is not None and best[0] == root:
            # Later roots cannot improve a tuple beginning at this root.
            break
    return best


def cycle_edges(cycle) -> list[tuple[int, int]]:
    return [
        edge_key(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    ]


def real_edge_owners(decomposition) -> dict[tuple[int, int], int]:
    owners = {}
    for index, node in enumerate(decomposition.nodes):
        for edge in node.edges:
            if edge.virtual:
                continue
            key = edge.endpoints
            if key in owners:
                raise AssertionError("a real edge has two SPQR owners")
            owners[key] = index
    return owners


def _tree_graph(decomposition) -> nx.Graph:
    tree = nx.Graph()
    tree.add_nodes_from(range(len(decomposition.nodes)))
    for node, neighbors in decomposition.adjacency.items():
        for neighbor, token in neighbors:
            tree.add_edge(node, neighbor, token=token)
    return tree


def _element_used_at(node_index, owner, edge, decomposition, tree):
    if owner == node_index:
        return ("real", edge)
    path = nx.shortest_path(tree, node_index, owner)
    neighbor = path[1]
    token = tree.edges[node_index, neighbor]["token"]
    return ("virtual", token)


def classify_cycle_support(
    decomposition,
    edges,
    *,
    root_local_s_nodes=frozenset(),
) -> tuple[str, list[int]]:
    owners = real_edge_owners(decomposition)
    support = sorted({owners[edge] for edge in edges})
    if set(support) & set(root_local_s_nodes):
        return "touching_root_local_terminal_subdivision", support
    if len(support) == 1 and decomposition.nodes[support[0]].type == "R":
        return "contained_in_one_R_node", support

    tree = _tree_graph(decomposition)
    for index, node in enumerate(decomposition.nodes):
        if node.type != "P":
            continue
        used = {
            _element_used_at(index, owners[edge], edge, decomposition, tree)
            for edge in edges
        }
        if len(used) == 2:
            return "created_by_two_P_node_expansions", support

    for index, node in enumerate(decomposition.nodes):
        if node.type != "S":
            continue
        used = {
            _element_used_at(index, owners[edge], edge, decomposition, tree)
            for edge in edges
        }
        elements = {
            ("virtual", edge.token) if edge.virtual
            else ("real", edge.endpoints)
            for edge in node.edges
        }
        if used == elements:
            return "represented_by_an_S_node_cycle", support
    return "spread_across_multiple_SPQR_nodes", support


def _minimum_tight_cover(real_edges, eligible_vertices):
    eligible = sorted(eligible_vertices)
    for size in range(len(eligible) + 1):
        for subset in itertools.combinations(eligible, size):
            chosen = set(subset)
            if all(chosen & set(edge) for edge in real_edges):
                return list(subset)
    return None


def leaf_r_records(decomposition, graph_b, x, y, leaf_report, dichotomy):
    suppressed = set(dichotomy.get("suppressed_S_nodes", []))
    core = set(range(len(decomposition.nodes))) - suppressed
    if len(core) <= 1:
        return []
    tree = _tree_graph(decomposition)
    core_tree = tree.subgraph(core)
    records = []
    for index, degree in core_tree.degree():
        node = decomposition.nodes[index]
        if degree != 1 or node.type != "R":
            continue
        parent = next(iter(core_tree.neighbors(index)))
        parent_token = tree.edges[index, parent]["token"]
        parent_edge = next(
            edge for edge in node.edges
            if edge.virtual and edge.token == parent_token
        )

        transformed = nx.Graph()
        transformed.add_nodes_from(node.vertices)
        real_b_edges = []
        converted_terminal_edges = []
        for edge in node.edges:
            if edge.virtual:
                neighbor = next(
                    neighbor for neighbor, token in decomposition.adjacency[index]
                    if token == edge.token
                )
                if neighbor in suppressed:
                    transformed.add_edge(*edge.endpoints)
                    converted_terminal_edges.append(list(edge.endpoints))
            else:
                transformed.add_edge(*edge.endpoints)
                if graph_b.has_edge(*edge.endpoints):
                    real_b_edges.append(edge.endpoints)
        pertinent = transformed.copy()
        if pertinent.has_edge(*parent_edge.endpoints):
            pertinent.remove_edge(*parent_edge.endpoints)
        paths = terminal_path_spectrum(
            pertinent, parent_edge.endpoints[0], parent_edge.endpoints[1]
        )
        eligible = {
            vertex for vertex in node.vertices
            if (vertex == x
                or (vertex not in (x, y) and graph_b.degree(vertex) == 3)
                or (vertex == y and graph_b.degree(y) == 1))
        }
        cover = _minimum_tight_cover(real_b_edges, eligible)
        internal_mask = python_power_mask(pertinent)
        records.append({
            "node": index,
            "parent_core_node": parent,
            "parent_virtual_edge": {
                "edge": list(parent_edge.endpoints),
                "token": parent_token,
            },
            "skeleton_order": len(node.vertices),
            "skeleton_size": len(node.edges),
            "original_real_edge_count": sum(not edge.virtual for edge in node.edges),
            "real_B_edge_count": len(real_b_edges),
            "converted_terminal_edges_after_suppression": converted_terminal_edges,
            "tight_vertices": sorted(eligible),
            "minimum_tight_vertex_cover": cover,
            "tight_cover_exists": cover is not None,
            "uncovered_real_B_edges": (
                [] if cover is not None else [list(edge) for edge in real_b_edges]
            ),
            "internal_C4_C8_spectrum": [
                length for bit, length in enumerate((4, 8))
                if internal_mask & (1 << bit)
            ],
            "terminal_path_spectrum_across_parent": sorted(paths),
        })
    return records


def analyze_candidate(item: dict) -> dict:
    graph_b = nx.from_graph6_bytes(item["bridge_g6"].encode())
    x, y = 0, 1
    # E23's bridge record retains the source rooted labeling while labelg's
    # canonical closure may permute the common-color internal vertices.  Build
    # the exactly corresponding closure from the stored B rather than mixing
    # those two isomorphic labelings.
    graph_j = graph_b.copy()
    if graph_j.has_edge(x, y):
        raise AssertionError("stored Type-A bridge contains xy")
    graph_j.add_edge(x, y)
    decomposition = decompose(graph_j)

    length = 4 if item["bridge_mask"] & 1 else 8
    cycle = canonical_cycle(graph_b, length)
    if cycle is None:
        raise AssertionError("stored forbidden-cycle mask has no witness")
    edges = cycle_edges(cycle)
    leaf_report = leaf_spqr_classification(
        graph_j, graph_b, x, y, decomposition=decomposition
    )
    root_local = {
        leaf["node"] for leaf in leaf_report["S_leaves"]
        if leaf["classification"] != "forbidden_remote_or_large_S_leaf"
    }
    classification, support_nodes = classify_cycle_support(
        decomposition, edges, root_local_s_nodes=root_local
    )

    tight = {"R": True, "P": True}
    edge_counts = {"R": 0, "P": 0}
    for node in decomposition.nodes:
        if node.type not in tight:
            continue
        for edge in node.edges:
            if edge.virtual or not graph_b.has_edge(*edge.endpoints):
                continue
            edge_counts[node.type] += 1
            tight[node.type] &= t8r_edge_is_degree_critical(
                graph_b, x, y, edge.endpoints
            )
    dichotomy = rigid_leaf_dichotomy(
        graph_j, graph_b, x, y, decomposition=decomposition
    )
    r_leaves = leaf_r_records(
        decomposition, graph_b, x, y, leaf_report, dichotomy
    )
    return {
        "candidate_id": item["candidate_id"],
        "structural_class": item["structural_class"],
        "canonical_shortest_forbidden_cycle": {
            "length": length,
            "vertices": list(cycle),
            "edges": [list(edge) for edge in edges],
        },
        "support_classification": classification,
        "support_nodes": support_nodes,
        "R_edge_count": edge_counts["R"],
        "P_edge_count": edge_counts["P"],
        "R_edges_tight": tight["R"],
        "P_edges_tight": tight["P"],
        "RP_edges_tight": tight["R"] and tight["P"],
        "S_leaf_classifications": [
            leaf["classification"] for leaf in leaf_report["S_leaves"]
        ],
        "P_leaf_count": len(leaf_report["P_leaves"]),
        "rigid_leaf_tree_shape": dichotomy,
        "leaf_R_nodes": r_leaves,
    }


def _update_aggregate(aggregate, record):
    groups = ["all", record["structural_class"]]
    if record["RP_edges_tight"]:
        groups.append("RP-tight")
    for group in groups:
        aggregate[group]["candidates"] += 1
        aggregate[group][record["support_classification"]] += 1
        aggregate[group][
            f"shortest_C{record['canonical_shortest_forbidden_cycle']['length']}"
        ] += 1
    aggregate["leaf_R"]["records"] += len(record["leaf_R_nodes"])
    for leaf in record["leaf_R_nodes"]:
        aggregate["leaf_R"][
            f"skeleton_n{leaf['skeleton_order']}_m{leaf['skeleton_size']}"
        ] += 1
        aggregate["leaf_R"][
            "tight_cover_exists" if leaf["tight_cover_exists"]
            else "tight_cover_missing"
        ] += 1
        spectrum = ",".join(map(str, leaf["internal_C4_C8_spectrum"])) or "clean"
        aggregate["leaf_R"][f"internal_spectrum_{spectrum}"] += 1


def run(input_path: pathlib.Path, output_path: pathlib.Path,
        manifest_path: pathlib.Path, workers: int):
    started = time.monotonic()
    if sha256_file(input_path) != INPUT_SHA256:
        raise RuntimeError("E23 input artifact checksum mismatch")
    items = []
    with gzip.open(input_path, "rt", encoding="utf-8") as source:
        for record in source:
            parsed = json.loads(record)
            items.append({
                "candidate_id": parsed["candidate_id"],
                "closure_g6": parsed["rooted_canonical_closure_g6"],
                "bridge_g6": parsed["bridge_g6"],
                "bridge_mask": parsed["internal_power_cycles"]["python_mask"],
                "structural_class": parsed["structural_class"],
            })
    if len(items) != 129040:
        raise RuntimeError("E23 input record count mismatch")

    aggregate = {
        group: Counter() for group in
        ("all", "SP-eligible", "rigid-forced", "RP-tight", "leaf_R")
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(output_path, "wt", encoding="utf-8", compresslevel=9) as output:
        if workers > 1:
            with mp.Pool(workers) as pool:
                records = pool.imap(analyze_candidate, items, chunksize=32)
                for record in records:
                    output.write(json.dumps(record, sort_keys=True) + "\n")
                    _update_aggregate(aggregate, record)
        else:
            for item in items:
                record = analyze_candidate(item)
                output.write(json.dumps(record, sort_keys=True) + "\n")
                _update_aggregate(aggregate, record)

    script = pathlib.Path(__file__)
    report = {
        "experiment": "E24d-order9-shortest-cycle-SPQR-support",
        "status": "COMPLETE",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "candidate_generation": "none; streamed existing E23 records",
        "input": {
            "path": str(input_path),
            "sha256": INPUT_SHA256,
            "records": len(items),
        },
        "output": {
            "path": str(output_path),
            "sha256": sha256_file(output_path),
            "bytes": output_path.stat().st_size,
            "records": len(items),
        },
        "script": {
            "path": str(script),
            "sha256": sha256_file(script),
        },
        "workers": workers,
        "classification_priority": [
            "touching_root_local_terminal_subdivision",
            "contained_in_one_R_node",
            "created_by_two_P_node_expansions",
            "represented_by_an_S_node_cycle",
            "spread_across_multiple_SPQR_nodes",
        ],
        "aggregate": {
            group: dict(sorted(counts.items()))
            for group, counts in aggregate.items()
        },
        "exit_code": 0,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["aggregate"], indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=pathlib.Path, default=INPUT_ARTIFACT)
    parser.add_argument(
        "--output", type=pathlib.Path,
        default=pathlib.Path("data/E24_order9_spqr_obstructions.jsonl.gz"),
    )
    parser.add_argument(
        "--manifest", type=pathlib.Path,
        default=pathlib.Path("manifests/E24_order9_spqr_manifest.json"),
    )
    parser.add_argument("--workers", type=int, default=max(1, mp.cpu_count()))
    args = parser.parse_args()
    run(args.input, args.output, args.manifest, args.workers)


if __name__ == "__main__":
    main()
