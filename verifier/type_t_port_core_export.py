#!/usr/bin/env python3
"""Materialize the Type-T E2_parallel port core as an ordinary graph.

This module deliberately does not import ``type_t_common_pole_ports.py``.
The earlier verifier reasons with affine weighted edges; this exporter starts
from the geometric branch description and creates every subdivision vertex
and every ordinary edge explicitly.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ANCHORS = (
    "z0", "x", "xprime", "y", "yprime", "w_AC", "w_BD",
    "r_x", "s_x", "r_y", "s_y", "u_x", "u_y",
)


@dataclass(frozen=True)
class PortCore:
    j: int
    a: int
    c: int
    labels: tuple[str, ...]
    edges: tuple[tuple[int, int], ...]
    paths: dict[str, tuple[int, ...]]

    @property
    def Y(self) -> int:
        return 1 << self.j

    @property
    def order(self) -> int:
        return len(self.labels)

    @property
    def size(self) -> int:
        return len(self.edges)

    @property
    def label_to_vertex(self) -> dict[str, int]:
        return {label: vertex for vertex, label in enumerate(self.labels)}

    def adjacency(self) -> tuple[frozenset[int], ...]:
        neighbors = [set() for _ in self.labels]
        for u, v in self.edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        return tuple(frozenset(row) for row in neighbors)

    def deficient_vertices(self) -> tuple[int, ...]:
        adjacency = self.adjacency()
        return tuple(v for v in range(self.order) if len(adjacency[v]) == 2)

    def to_json(self) -> dict:
        return {
            "family": "Type-T E2_parallel common-pole two-port core",
            "parameters": {"j": self.j, "Y": self.Y, "a": self.a, "c": self.c},
            "order": self.order,
            "size": self.size,
            "labels": list(self.labels),
            "edges": [list(edge) for edge in self.edges],
            "named_paths": {name: list(path) for name, path in self.paths.items()},
            "deficient_vertices": list(self.deficient_vertices()),
        }


def valid_parameters(j: int, a: int, c: int) -> None:
    if j < 4:
        raise ValueError("the explicit family requires j >= 4")
    Y = 1 << j
    if not 2 <= a <= 4 * Y - 9:
        raise ValueError(f"a must lie in [2,{4 * Y - 9}]")
    if not 2 <= c <= Y - 9:
        raise ValueError(f"c must lie in [2,{Y - 9}]")


def build_core(j: int, a: int, c: int) -> PortCore:
    """Expand the family directly, with unique internal path vertices."""
    valid_parameters(j, a, c)
    Y = 1 << j
    labels = list(ANCHORS)
    label_to_vertex = {label: i for i, label in enumerate(labels)}
    edges: list[tuple[int, int]] = []
    paths: dict[str, tuple[int, ...]] = {}

    def vertex(label: str) -> int:
        if label not in label_to_vertex:
            label_to_vertex[label] = len(labels)
            labels.append(label)
        return label_to_vertex[label]

    def add_path(name: str, left: str, right: str, length: int) -> None:
        if length < 1:
            raise ValueError(f"nonpositive length for {name}: {length}")
        sequence = [vertex(left)]
        for index in range(1, length):
            sequence.append(vertex(f"{name}:{index}"))
        sequence.append(vertex(right))
        paths[name] = tuple(sequence)
        edges.extend(
            (min(u, v), max(u, v)) for u, v in zip(sequence, sequence[1:])
        )

    # AC bundle: one common edge, then the long A and C branches.
    add_path("prefix_AC", "z0", "w_AC", 1)
    add_path("A_left", "w_AC", "r_x", a - 1)
    add_path("A_middle", "r_x", "s_x", 7)
    add_path("A_right", "s_x", "xprime", 4 * Y - 8 - a)
    add_path("C_left", "w_AC", "r_y", c - 1)
    add_path("C_middle", "r_y", "s_y", 7)
    add_path("C_right", "s_y", "yprime", Y - 8 - c)

    # BD bundle and the fixed triangle/two P0 paths.
    add_path("prefix_BD", "z0", "w_BD", 1)
    add_path("B_right", "w_BD", "xprime", 3)
    add_path("D_right", "w_BD", "yprime", 3)
    add_path("z0x", "z0", "x", 1)
    add_path("xxprime", "x", "xprime", 1)
    add_path("z0y", "z0", "y", 1)
    add_path("yyprime", "y", "yprime", 1)
    add_path("xy", "x", "y", 1)

    # The two literal shared ports.
    add_path("u_x_r_x", "u_x", "r_x", 1)
    add_path("u_x_s_x", "u_x", "s_x", 1)
    add_path("u_y_r_y", "u_y", "r_y", 1)
    add_path("u_y_s_y", "u_y", "s_y", 1)

    if len(edges) != len(set(edges)):
        raise AssertionError("the expanded core is not simple")
    return PortCore(j, a, c, tuple(labels), tuple(sorted(edges)), paths)


def to_networkx(core: PortCore, extra_edges: Iterable[tuple[int, int]] = ()):
    import networkx as nx

    graph = nx.Graph()
    graph.add_nodes_from(range(core.order))
    graph.add_edges_from(core.edges)
    graph.add_edges_from(extra_edges)
    return graph


def graph_encodings(core: PortCore, extra_edges: Iterable[tuple[int, int]] = ()) -> dict[str, str]:
    import networkx as nx

    graph = to_networkx(core, extra_edges)
    return {
        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
        "sparse6": nx.to_sparse6_bytes(graph, header=False).decode().strip(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--encodings", action="store_true")
    args = parser.parse_args()

    core = build_core(args.j, args.a, args.c)
    payload = core.to_json()
    if args.encodings:
        payload.update(graph_encodings(core))
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
