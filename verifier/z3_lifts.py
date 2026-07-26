#!/usr/bin/env python3
"""Reference implementation and certification tools for cyclic Z3 lifts."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.cycle_detect import (
    find_cycle_len_dfs,
    from_edges,
    has_cycle_len_dfs,
    has_cycle_len_nx,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "z3_lifts"
BASE_NAMES = ("base0_markstroem", "base1_hss", "base2_hss", "base3_hss")
GROUP_ORDER = (3, 12, 3, 4)
SOURCE_FILES = (
    "markstroem.txt",
    "24-node-cubic-no-4-8-cycles-p18-free.1.txt",
    "24-node-cubic-no-4-8-cycles-p18-free.2.txt",
    "24-node-cubic-no-4-8-cycles-p18-free.3.txt",
)
SOURCE_SHA256 = (
    "7d4a44e4364f2eeda386daa6d71fb36b94b702db7745c297237dcf8b0e6a6d15",
    "564bde427ad306fe699156229c16f0048ce40efc30f5b72bf494d7b0033f8f98",
    "93bb0199c3e79460514f0e25e3e5bb9d24bcf2cdde14613e1e14c49e10c9bda4",
    "44a3945f9108581730b985cb77696fd767c2a7f4cc6d69cabbe548218943f269",
)


@dataclass(frozen=True)
class Base:
    index: int
    name: str
    graph: nx.Graph
    edges: tuple[tuple[int, int], ...]
    tree_edges: tuple[tuple[int, int], ...]
    cotree_edges: tuple[tuple[int, int], ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def canonical_bfs_tree(graph: nx.Graph) -> tuple[tuple[int, int], ...]:
    """Label-canonical BFS: root 0 and scan every neighbor increasingly."""
    seen = {0}
    queue = [0]
    tree = []
    while queue:
        u = queue.pop(0)
        for v in sorted(graph.neighbors(u)):
            if v not in seen:
                seen.add(v)
                queue.append(v)
                tree.append(tuple(sorted((u, v))))
    if len(seen) != graph.number_of_nodes():
        raise ValueError("base graph is disconnected")
    return tuple(sorted(tree))


def load_base(index: int) -> Base:
    name = BASE_NAMES[index]
    edge_path = DATA / f"{name}.edges"
    lines = edge_path.read_text().splitlines()
    n, declared_m = map(int, lines[0].split())
    edges = tuple(tuple(map(int, line.split())) for line in lines[1:])
    if len(edges) != declared_m:
        raise ValueError(f"{edge_path}: declared {declared_m}, read {len(edges)}")
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(edges)
    tree = canonical_bfs_tree(graph)
    cotree = tuple(sorted(set(edges) - set(tree)))
    return Base(index, name, graph, edges, tree, cotree)


def voltage_vector(index: int, coordinates: int = 13) -> tuple[int, ...]:
    if not 0 <= index < 3**coordinates:
        raise ValueError("assignment index is outside the normalized search space")
    values = []
    for _ in range(coordinates):
        values.append(index % 3)
        index //= 3
    return tuple(values)


def assignment_index(values: Sequence[int]) -> int:
    result = 0
    power = 1
    for value in values:
        if value not in (0, 1, 2):
            raise ValueError("Z3 voltages must be 0, 1, or 2")
        result += value * power
        power *= 3
    return result


def lift_graph(base: Base, values: Sequence[int]) -> nx.Graph:
    if len(values) != len(base.cotree_edges):
        raise ValueError("one voltage is required per cotree edge")
    voltage = {edge: 0 for edge in base.tree_edges}
    voltage.update(zip(base.cotree_edges, values))
    lifted = nx.Graph()
    lifted.add_nodes_from(range(3 * base.graph.number_of_nodes()))
    for u, v in base.edges:  # stored with u < v: this is the canonical orientation
        a = voltage[(u, v)]
        for sheet in range(3):
            lifted.add_edge(3 * u + sheet, 3 * v + (sheet + a) % 3)
    return lifted


def lift_detector_graph(base: Base, values: Sequence[int]):
    """Construct the same lift directly in the detector's adjacency format."""
    if len(values) != len(base.cotree_edges):
        raise ValueError("one voltage is required per cotree edge")
    voltage = {edge: 0 for edge in base.tree_edges}
    voltage.update(zip(base.cotree_edges, values))
    lifted = {v: set() for v in range(3 * base.graph.number_of_nodes())}
    for u, v in base.edges:
        a = voltage[(u, v)]
        for sheet in range(3):
            left = 3 * u + sheet
            right = 3 * v + (sheet + a) % 3
            lifted[left].add(right)
            lifted[right].add(left)
    return lifted


def graph_as_detector_dict(graph: nx.Graph):
    return from_edges(graph.number_of_nodes(), sorted(graph.edges()))


def certify_base(base: Base) -> dict:
    g6_path = DATA / f"{base.name}.g6"
    s6_path = DATA / f"{base.name}.s6"
    edge_path = DATA / f"{base.name}.edges"
    g6 = g6_path.read_text().strip()
    s6 = s6_path.read_text().strip()
    decoded_g6 = nx.from_graph6_bytes(g6.encode())
    decoded_s6 = nx.from_sparse6_bytes(s6.encode())
    if set(decoded_g6.edges()) != set(base.graph.edges()):
        raise AssertionError("graph6 does not match edge list")
    if set(decoded_s6.edges()) != set(base.graph.edges()):
        raise AssertionError("sparse6 does not match edge list")

    detector_graph = graph_as_detector_dict(base.graph)
    dfs = {length: has_cycle_len_dfs(detector_graph, length) for length in (4, 8, 16)}
    independent = {
        length: has_cycle_len_nx(detector_graph, length) for length in (4, 8, 16)
    }
    if dfs != independent:
        raise AssertionError("the independent base cycle detectors disagree")
    witness = find_cycle_len_dfs(detector_graph, 16)

    return {
        "index": base.index,
        "name": base.name,
        "authoritative_source_file": SOURCE_FILES[base.index],
        "authoritative_source_sha256": SOURCE_SHA256[base.index],
        "artifact_sha256": {
            "graph6": sha256(g6_path),
            "sparse6": sha256(s6_path),
            "edges": sha256(edge_path),
        },
        "graph6": g6,
        "sparse6": s6,
        "vertices": base.graph.number_of_nodes(),
        "edges": base.graph.number_of_edges(),
        "simple": not base.graph.is_multigraph()
        and nx.number_of_selfloops(base.graph) == 0,
        "connected": nx.is_connected(base.graph),
        "degree_sequence": sorted((d for _, d in base.graph.degree()), reverse=True),
        "cycle_space_rank": base.graph.number_of_edges()
        - base.graph.number_of_nodes()
        + nx.number_connected_components(base.graph),
        "automorphism_group_order": GROUP_ORDER[base.index],
        "cycle_status_dfs": {str(k): v for k, v in dfs.items()},
        "cycle_status_networkx": {str(k): v for k, v in independent.items()},
        "cycle16_witness": witness,
        "canonical_tree_rule": "BFS rooted at 0; vertices and neighbors scanned increasingly",
        "tree_edges": base.tree_edges,
        "cotree_edges": base.cotree_edges,
    }


def certify_all_bases() -> dict:
    records = [certify_base(load_base(index)) for index in range(4)]
    return {
        "schema": "erdos64-z3-bases-v1",
        "authoritative_repository": "https://github.com/rbsandeep/Erdos-Gyarfas",
        "authoritative_branch": "special-graphs",
        "authoritative_commit": "f7bea75afecb07dab552047ece2d551722f32272",
        "canonicalization": "nauty labelg 2.9.3, then graph6 decoding",
        "automorphism_oracle": "nauty countg 2.9.3 (-V --a), values stored below",
        "markstroem_cross_check": {
            "source": "MathWorld / House of Graphs 51419",
            "matched_invariants": {
                "vertices": 24,
                "edges": 36,
                "cubic": True,
                "planar": True,
                "automorphism_group_order": 3,
                "cycles_4_8_16": [False, False, True],
            },
        },
        "bases": records,
    }


def assignment_cycle_status(base: Base, index: int, lengths: Iterable[int]) -> dict[int, bool]:
    graph = graph_as_detector_dict(lift_graph(base, voltage_vector(index)))
    return {length: has_cycle_len_dfs(graph, length) for length in lengths}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--certify-bases", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.certify_bases:
        parser.error("select --certify-bases")
    report = certify_all_bases()
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
