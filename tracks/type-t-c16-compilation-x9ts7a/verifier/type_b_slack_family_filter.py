#!/usr/bin/env python3
"""Filter candidate 19-vertex, 28-edge one-slack remainder graphs (R) for the
20-vertex Pi0 bridge reduction (see type_b_one_slack.md, Section 4).

Stage 1: C8/C16-freeness (C4-freeness is already guaranteed by the geng -f
generation box). Cross-checked with two independent detectors from
verifier/cycle_detect.py (DFS backtracking and networkx simple_cycles).

Stage 2: for every graph surviving stage 1, test whether there exists a
vertex z and an endpoint v equal to the graph's unique/selected degree-2
vertex such that G-z has a Hamiltonian path with v as one endpoint. This is
the necessary geometric condition from Section 1 (P covers R-x except the
single off-path vertex z). A graph with no such (z, v) pair is eliminated:
no valid embedding of the required distinguished path exists in it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import networkx as nx

try:
    from verifier.cycle_detect import find_cycle_len_dfs, from_edges, has_cycle_len_nx
except ModuleNotFoundError:
    from cycle_detect import find_cycle_len_dfs, from_edges, has_cycle_len_nx


def has_ham_path_from(adj: dict, vertices: set, start: int) -> bool:
    """Exhaustive DFS: does the induced graph on `vertices` have a Hamiltonian
    path starting at `start`? Exact, exponential worst case, fine for n<=18
    sparse graphs."""
    n = len(vertices)
    visited = {start}
    path = [start]

    def dfs(u: int) -> bool:
        if len(path) == n:
            return True
        for w in adj[u]:
            if w in vertices and w not in visited:
                visited.add(w)
                path.append(w)
                if dfs(w):
                    return True
                path.pop()
                visited.discard(w)
        return False

    return dfs(start)


def stage1_c8_c16_free(adj: dict, n: int) -> tuple[bool, bool, bool]:
    """Returns (survives, c8_disagree, c16_disagree)."""
    dfs_c8 = find_cycle_len_dfs(adj, 8) is not None
    nx_c8 = has_cycle_len_nx(adj, 8)
    c8_disagree = dfs_c8 != nx_c8
    survives_c8 = not dfs_c8 and not nx_c8

    survives_c16 = True
    c16_disagree = False
    if n >= 16:
        dfs_c16 = find_cycle_len_dfs(adj, 16) is not None
        nx_c16 = has_cycle_len_nx(adj, 16)
        c16_disagree = dfs_c16 != nx_c16
        survives_c16 = not dfs_c16 and not nx_c16

    return survives_c8 and survives_c16, c8_disagree, c16_disagree


def stage2_path_exists(adj: dict, n: int, deg2_vertices: list) -> bool:
    """True iff some (z, v) with v in deg2_vertices, z != v, deg(z)>=3 admits a
    Hamiltonian path on V-{z} starting at v."""
    all_v = set(range(n))
    for v in deg2_vertices:
        for z in range(n):
            if z == v:
                continue
            if len(adj[z]) < 3:
                continue
            remaining = all_v - {z}
            if has_ham_path_from(adj, remaining, v):
                return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--deg2-count", type=int, required=True,
                         help="expected number of degree-2 vertices")
    parser.add_argument("--out-survivors", type=Path, required=True)
    parser.add_argument("--out-report", type=Path, required=True)
    args = parser.parse_args()

    checked = 0
    c4_violations = 0
    c8c16_survivors = 0
    c8_disagreements = 0
    c16_disagreements = 0
    stage2_survivors = []

    with args.input.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            graph = nx.from_graph6_bytes(line.encode())
            n = graph.number_of_nodes()
            assert n == 19
            assert graph.number_of_edges() == 28
            assert nx.is_connected(graph)
            degrees = [d for _, d in graph.degree()]
            deg2_vertices = [v for v, d in graph.degree() if d == 2]
            assert len(deg2_vertices) == args.deg2_count, (checked, degrees)

            adj = from_edges(n, list(graph.edges()))
            has_c4 = find_cycle_len_dfs(adj, 4) is not None
            if has_c4:
                c4_violations += 1
                checked += 1
                continue

            survives, c8_dis, c16_dis = stage1_c8_c16_free(adj, n)
            c8_disagreements += c8_dis
            c16_disagreements += c16_dis
            checked += 1
            if not survives:
                continue
            c8c16_survivors += 1

            if stage2_path_exists(adj, n, deg2_vertices):
                stage2_survivors.append(sorted(graph.edges()))

    args.out_survivors.parent.mkdir(parents=True, exist_ok=True)
    args.out_survivors.write_text(json.dumps(stage2_survivors, indent=2) + "\n")

    report = {
        "label": args.label,
        "input": str(args.input),
        "graphs_checked": checked,
        "c4_violations_found": c4_violations,
        "c8_c16_free_survivors": c8c16_survivors,
        "c8_detector_disagreements": c8_disagreements,
        "c16_detector_disagreements": c16_disagreements,
        "stage2_ham_path_survivors": len(stage2_survivors),
        "conclusion": (
            "layer eliminated: no candidate admits the required distinguished path"
            if not stage2_survivors
            else "layer NOT eliminated: survivors require further theorem work"
        ),
    }
    args.out_report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
