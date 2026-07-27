#!/usr/bin/env python3
"""Audit the extremal layer in the 20-vertex Pi0 bridge reduction."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import networkx as nx

try:
    from verifier.cycle_detect import find_cycle_len_dfs, from_edges, has_cycle_len_nx
except ModuleNotFoundError:
    from cycle_detect import find_cycle_len_dfs, from_edges, has_cycle_len_nx


EXPECTED_SHA256 = "bf81b89b826ae3153c7497addb26025796b982a52a5e39210754f15620226562"
EXPECTED_GRAPHS = 304


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/c48_n19e29.s6"))
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("data/type_b_one_slack_extremal_certificate.json"),
    )
    args = parser.parse_args()
    assert sha256(args.input) == EXPECTED_SHA256

    histogram: Counter[int] = Counter()
    c4_disagreements = 0
    c8_disagreements = 0
    checked = 0
    for line in args.input.read_bytes().splitlines():
        graph = nx.from_sparse6_bytes(line)
        assert graph.number_of_nodes() == 19
        assert graph.number_of_edges() == 29
        assert nx.is_connected(graph)
        adjacency = from_edges(19, list(graph.edges()))
        common_c4 = any(
            len(set(graph[left]) & set(graph[right])) >= 2
            for left in graph
            for right in graph
            if left < right
        )
        dfs_c4 = find_cycle_len_dfs(adjacency, 4) is not None
        dfs_c8 = find_cycle_len_dfs(adjacency, 8) is not None
        nx_c8 = has_cycle_len_nx(adjacency, 8)
        c4_disagreements += common_c4 != dfs_c4
        c8_disagreements += dfs_c8 != nx_c8
        assert not common_c4 and not dfs_c4 and not dfs_c8 and not nx_c8
        histogram[sum(degree == 2 for _, degree in graph.degree())] += 1
        checked += 1

    eligible = sum(count for twos, count in histogram.items() if twos <= 2)
    assert checked == EXPECTED_GRAPHS
    assert eligible == 0
    assert c4_disagreements == c8_disagreements == 0
    report = {
        "scope": "20-vertex Pi0 bridge, 19-vertex remainder, extremal 29-edge layer only",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "graphs_checked": checked,
        "degree_two_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "graphs_with_at_most_two_degree_two_vertices": eligible,
        "c4_detector_disagreements": c4_disagreements,
        "c8_detector_disagreements": c8_disagreements,
        "conclusion": "the 29-edge one-slack remainder layer is empty",
        "unresolved": "the 28-edge remainder layer",
        "assertion_failures": 0,
    }
    args.certificate.parent.mkdir(parents=True, exist_ok=True)
    args.certificate.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print("certificate_sha256", sha256(args.certificate))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
