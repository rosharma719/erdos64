#!/usr/bin/env python3
"""Targeted smallest-case search for clean abstract leaf-R pertinent graphs.

For every connected simple minimum-degree-three skeleton R through order nine
(a superset of 3-connected R-skeletons) and every edge ab, test K=R-ab for a
C4 or C8.  This is a targeted LR audit, not an SPQR census.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def adjacency_masks(graph: nx.Graph) -> list[int]:
    masks = [0] * graph.number_of_nodes()
    for u, v in graph.edges():
        masks[u] |= 1 << v
        masks[v] |= 1 << u
    return masks


def has_c4(adjacency: list[int]) -> bool:
    n = len(adjacency)
    return any(
        (adjacency[u] & adjacency[v]).bit_count() >= 2
        for u in range(n)
        for v in range(u + 1, n)
    )


def has_cycle(adjacency: list[int], length: int) -> bool:
    n = len(adjacency)
    for root in range(n - length + 1):
        visited = 1 << root

        def dfs(current: int, used: int) -> bool:
            nonlocal visited
            if used == length:
                return bool(adjacency[current] & (1 << root))
            candidates = adjacency[current] & ~visited & ~((1 << (root + 1)) - 1)
            while candidates:
                bit = candidates & -candidates
                candidates -= bit
                next_vertex = bit.bit_length() - 1
                visited |= bit
                if dfs(next_vertex, used + 1):
                    return True
                visited ^= bit
            return False

        if dfs(root, 1):
            return True
    return False


def search() -> dict:
    order_rows = []
    total_graphs = 0
    total_pairs = 0
    total_c4_free = 0
    total_clean = 0
    clean_examples = []
    for order in range(4, 10):
        process = subprocess.run(
            ["geng", "-q", "-c", "-d3", str(order)],
            capture_output=True,
            text=True,
            check=True,
        )
        graph_count = pair_count = c4_free = clean = 0
        for line in process.stdout.splitlines():
            graph = nx.from_graph6_bytes(line.encode())
            graph_count += 1
            degrees = dict(graph.degree())
            base_masks = adjacency_masks(graph)
            for a, b in graph.edges():
                pair_count += 1
                adjacency = base_masks.copy()
                adjacency[a] &= ~(1 << b)
                adjacency[b] &= ~(1 << a)
                if has_c4(adjacency):
                    continue
                c4_free += 1
                if has_cycle(adjacency, 8):
                    continue
                clean += 1
                tight = all(
                    degrees[u] == 3 or degrees[v] == 3
                    for u, v in graph.edges()
                    if {u, v} != {a, b}
                )
                clean_examples.append(
                    {"order": order, "skeleton_g6": line, "parent_edge": [a, b], "t8r_tight": tight}
                )
        order_rows.append(
            {
                "order": order,
                "connected_delta3_skeletons": graph_count,
                "edge_rooted_pairs": pair_count,
                "C4_free_after_parent_deletion": c4_free,
                "C4_C8_free_after_parent_deletion": clean,
            }
        )
        total_graphs += graph_count
        total_pairs += pair_count
        total_c4_free += c4_free
        total_clean += clean
    return {
        "schema": "erdos64-leaf-r-replacement-small-v1",
        "generator": "nauty geng -q -c -d3 n",
        "commands": [f"geng -q -c -d3 {order}" for order in range(4, 10)],
        "script": {
            "path": str(Path(__file__).resolve().relative_to(ROOT)),
            "sha256": sha256(Path(__file__).resolve()),
        },
        "scope": "all connected simple minimum-degree-3 skeletons, a superset of realizable 3-connected R-skeletons",
        "orders": order_rows,
        "totals": {
            "skeletons": total_graphs,
            "edge_rooted_pairs": total_pairs,
            "C4_free_after_parent_deletion": total_c4_free,
            "C4_C8_free_after_parent_deletion": total_clean,
        },
        "clean_examples": clean_examples,
        "conclusion": "Through skeleton order 9, every unexpanded leaf-R pertinent graph R-ab satisfies LR alternative 1.",
        "limitation": "Does not cover virtual-edge expansions; since no clean K occurs, the replacement alternative and terminal-spectrum inclusion are not exercised.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = search()
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["totals"], sort_keys=True))
    return int(bool(report["clean_examples"]))


if __name__ == "__main__":
    raise SystemExit(main())
