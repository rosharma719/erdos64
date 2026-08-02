#!/usr/bin/env python3
"""Exhaust the order-36 equality layer for the smallest Type-B tuple.

For either 19-vertex bridge, delete the terminal ``x`` of bridge degree one.
The required length-18 path shows that the resulting graph H is connected and
has order 18.  Exactly sixteen vertices have degree at least three, while the
gateway and y have degree at least two.  Hence 26 <= |E(H)| <= 27, where the
upper bound is ex(18,{C4,C8})=27.

The 26-edge layer is generated locally by geng and checked twice, using two
unrelated exact C8 detectors. The 27-edge layer is McKay's authoritative
complete extremal file; its contents are checked with two exact detectors and
its degree distribution is independently recomputed. This program proves no
eligible H exists, so it covers every path embedding without enumerating those
embeddings individually.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import networkx as nx

try:
    from verifier.cycle_detect import (
        find_cycle_len_dfs,
        from_edges,
        has_cycle_len_nx,
    )
except ModuleNotFoundError:
    from cycle_detect import find_cycle_len_dfs, from_edges, has_cycle_len_nx


EXPECTED_MCKAY_SHA256 = (
    "c21bfccdc139f3abac60141b886423fb4daa88dc05fa084715a012dd04460359"
)
EXPECTED_NEAR_COUNT = 101_546
EXPECTED_EXTREMAL_COUNT = 570


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(line: bytes) -> nx.Graph:
    return nx.from_graph6_bytes(line.strip())


def adjacency(graph: nx.Graph):
    return from_edges(graph.number_of_nodes(), list(graph.edges()))


def has_c4_by_common_neighbors(graph: nx.Graph) -> bool:
    nodes = list(graph)
    return any(
        len(set(graph[left]) & set(graph[right])) >= 2
        for index, left in enumerate(nodes)
        for right in nodes[index + 1 :]
    )


def audit_near_extremal(detector: str) -> dict:
    command = [
        "geng",
        "-c",
        "-q",
        "-f",
        "-d2",
        "-D3",
        "18",
        "26:26",
    ]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert process.stdout is not None
    checked = 0
    c8_free = 0
    stream_hash = hashlib.sha256()
    for line in process.stdout:
        stream_hash.update(line)
        graph = decode_graph6(line)
        checked += 1
        assert graph.number_of_nodes() == 18
        assert graph.number_of_edges() == 26
        assert nx.is_connected(graph)
        assert sorted(dict(graph.degree()).values()) == [2, 2] + [3] * 16
        assert not has_c4_by_common_neighbors(graph)
        graph_adjacency = adjacency(graph)
        if detector == "dfs":
            has_c8 = find_cycle_len_dfs(graph_adjacency, 8) is not None
        elif detector == "networkx":
            has_c8 = has_cycle_len_nx(graph_adjacency, 8)
        else:
            raise ValueError(detector)
        if not has_c8:
            c8_free += 1
    stderr = process.stderr.read().decode().strip() if process.stderr else ""
    return_code = process.wait()
    assert return_code == 0
    assert checked == EXPECTED_NEAR_COUNT
    assert c8_free == 0
    return {
        "command": " ".join(command),
        "detector": detector,
        "graphs_checked": checked,
        "c8_free_graphs": c8_free,
        "graph6_stream_sha256": stream_hash.hexdigest(),
        "geng_stderr": stderr,
        "exit_status": return_code,
    }


def nauty_canonical_lines(path: Path) -> list[bytes]:
    result = subprocess.run(
        ["labelg", "-q", "-g", str(path)],
        check=True,
        capture_output=True,
    )
    return sorted(result.stdout.splitlines())


def audit_extremal(mckay_path: Path) -> dict:
    assert sha256(mckay_path) == EXPECTED_MCKAY_SHA256
    canonical_mckay = nauty_canonical_lines(mckay_path)
    assert len(canonical_mckay) == EXPECTED_EXTREMAL_COUNT

    degree_two_histogram: Counter[int] = Counter()
    c4_disagreements = 0
    c8_disagreements = 0
    for line in canonical_mckay:
        graph = decode_graph6(line)
        assert graph.number_of_nodes() == 18
        assert graph.number_of_edges() == 27
        assert nx.is_connected(graph)
        graph_adjacency = adjacency(graph)
        common_neighbor_c4 = has_c4_by_common_neighbors(graph)
        dfs_c4 = find_cycle_len_dfs(graph_adjacency, 4) is not None
        if common_neighbor_c4 != dfs_c4:
            c4_disagreements += 1
        dfs_c8 = find_cycle_len_dfs(graph_adjacency, 8) is not None
        nx_c8 = has_cycle_len_nx(graph_adjacency, 8)
        if dfs_c8 != nx_c8:
            c8_disagreements += 1
        assert not common_neighbor_c4 and not dfs_c4
        assert not dfs_c8 and not nx_c8
        degree_two_histogram[sum(degree == 2 for _, degree in graph.degree())] += 1

    eligible = sum(
        count for degree_twos, count in degree_two_histogram.items() if degree_twos <= 2
    )
    assert c4_disagreements == c8_disagreements == 0
    assert eligible == 0
    canonical_bytes = b"\n".join(canonical_mckay) + b"\n"
    return {
        "authoritative_input": str(mckay_path),
        "authoritative_input_sha256": sha256(mckay_path),
        "canonical_set_sha256": hashlib.sha256(canonical_bytes).hexdigest(),
        "graphs_checked": len(canonical_mckay),
        "degree_two_histogram": {
            str(key): value for key, value in sorted(degree_two_histogram.items())
        },
        "graphs_with_at_most_two_degree_two_vertices": eligible,
        "c4_detector_disagreements": c4_disagreements,
        "c8_detector_disagreements": c8_disagreements,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mckay-input", type=Path, default=Path("data/c48_n18e27.s6")
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("data/type_b_equality_order_certificate.json"),
    )
    args = parser.parse_args()

    report = {
        "scope": "all Pi0 Type-B realizations at full order 36",
        "reduction": {
            "bridge_order": 19,
            "deleted_terminal": "x, whose bridge degree is one",
            "remainder_order": 18,
            "remainder_edge_range": [26, 27],
            "degree_condition": (
                "sixteen vertices have degree at least three and the gateway/y "
                "pair have degree at least two"
            ),
            "why_all_path_embeddings_are_covered": (
                "the required length-18 terminal path is Hamiltonian at bridge "
                "order 19; the reduction uses no assumption about the other paths"
            ),
        },
        "near_extremal_26": {
            "dfs_route": audit_near_extremal("dfs"),
            "networkx_route": audit_near_extremal("networkx"),
        },
        "extremal_27": audit_extremal(args.mckay_input),
        "candidate_bridge_remainders": 0,
        "extendable_equality_path_union_cores": 0,
        "conclusion": "Pi0 has no Type-B realization at full order 36",
        "formalization": "computer-assisted exhaustive finite computation; not proof-assistant formal verification",
        "assertion_failures": 0,
    }
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print("certificate_sha256", sha256(args.certificate))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
