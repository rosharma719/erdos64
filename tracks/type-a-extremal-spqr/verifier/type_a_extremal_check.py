"""Independent compact Type-A checks on McKay--Afzaly extremal files.

The order-9 and order-11 sparse6 files contain every extremal
``{C4,C8}``-free graph at their respective orders.  For every graph this
module checks all ordered terminal pairs twice:

* NetworkX degree and biconnectivity predicates;
* an independent adjacency-set implementation which tests connectivity
  after deleting each vertex directly.

The cycle-free provenance is also rechecked with the repository's two exact
cycle detectors.  Shared sparse6 decoding is the only common preprocessing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import sys

import networkx as nx

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx


SOURCE_PAGE = "https://users.cecs.anu.edu.au/~bdm/data/extremal.html"
FILES = {
    9: {
        "path": "data/extremal/c48_n9e12.s6",
        "source": (
            "https://users.cecs.anu.edu.au/~bdm/data/extremal/"
            "c48_n9e12.s6"
        ),
        "edges": 12,
        "records": 33,
        "sha256": "ab93fb789a63defcb189f69f6e7f8a3bcac1057c77837dfd20211d644416ca98",
    },
    11: {
        "path": "data/extremal/c48_n11e15.s6",
        "source": (
            "https://users.cecs.anu.edu.au/~bdm/data/extremal/"
            "c48_n11e15.s6"
        ),
        "edges": 15,
        "records": 245,
        "sha256": "fa5c5158ad641d1f2124feea75255e8077144fcdaeb7b051cd45f32470bbe0f2",
    },
}


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def detector_graph(graph: nx.Graph):
    vertices = sorted(graph)
    remap = {vertex: index for index, vertex in enumerate(vertices)}
    return from_edges(
        len(vertices), [(remap[u], remap[v]) for u, v in graph.edges()]
    )


def nx_terminal_choices(graph: nx.Graph) -> set[tuple[int, int]]:
    """Definition check using NetworkX's independent biconnectivity code."""
    choices = set()
    for x in graph:
        for y in graph:
            if x == y:
                continue
            if graph.degree(x) != 1 or graph.degree(y) < 1:
                continue
            if graph.has_edge(x, y):
                continue
            if any(graph.degree(vertex) < 3
                   for vertex in graph if vertex not in (x, y)):
                continue
            closure = graph.copy()
            closure.add_edge(x, y)
            if nx.is_biconnected(closure):
                choices.add((x, y))
    return choices


def _connected_without(adjacency: dict[int, set[int]], removed: int) -> bool:
    remaining = [vertex for vertex in adjacency if vertex != removed]
    if not remaining:
        return True
    seen = {remaining[0]}
    stack = [remaining[0]]
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor != removed and neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen) == len(remaining)


def manual_2connected(adjacency: dict[int, set[int]]) -> bool:
    """Definition-only 2-connectivity check, independent of NetworkX."""
    return len(adjacency) >= 3 and all(
        _connected_without(adjacency, removed) for removed in adjacency
    )


def manual_terminal_choices(graph: nx.Graph) -> set[tuple[int, int]]:
    """Terminal and closure check using only adjacency sets and DFS."""
    adjacency = {vertex: set(graph.neighbors(vertex)) for vertex in graph}
    choices = set()
    for x in adjacency:
        for y in adjacency:
            if x == y:
                continue
            if len(adjacency[x]) != 1 or len(adjacency[y]) < 1:
                continue
            if y in adjacency[x]:
                continue
            if any(len(adjacency[vertex]) < 3
                   for vertex in adjacency if vertex not in (x, y)):
                continue
            closure = {vertex: set(neighbors)
                       for vertex, neighbors in adjacency.items()}
            closure[x].add(y)
            closure[y].add(x)
            if manual_2connected(closure):
                choices.add((x, y))
    return choices


def check_file(order: int, metadata: dict) -> dict:
    path = pathlib.Path(metadata["path"])
    if sha256_file(path) != metadata["sha256"]:
        raise RuntimeError(f"checksum mismatch for {path}")
    lines = [line.strip() for line in path.read_bytes().splitlines() if line]
    if len(lines) != metadata["records"]:
        raise RuntimeError(f"record-count mismatch for {path}")

    nx_survivors = []
    manual_survivors = []
    detector_disagreements = 0
    malformed = 0
    for index, line in enumerate(lines):
        graph = nx.from_sparse6_bytes(line)
        if (len(graph) != order
                or graph.number_of_edges() != metadata["edges"]
                or nx.number_of_selfloops(graph)):
            malformed += 1
            continue
        simple = detector_graph(graph)
        for length in (4, 8):
            left = has_cycle_len_dfs(simple, length)
            right = has_cycle_len_nx(simple, length)
            detector_disagreements += left != right
            if left or right:
                malformed += 1
        nx_choices = nx_terminal_choices(graph)
        manual_choices = manual_terminal_choices(graph)
        nx_survivors.extend((index, x, y) for x, y in sorted(nx_choices))
        manual_survivors.extend(
            (index, x, y) for x, y in sorted(manual_choices)
        )
    if nx_survivors != manual_survivors:
        raise AssertionError("the independent terminal-choice checkers disagree")
    if detector_disagreements or malformed:
        raise AssertionError("extremal input validation failed")
    return {
        "order": order,
        "Turan_number": metadata["edges"],
        "source": metadata["source"],
        "local_path": metadata["path"],
        "sha256": metadata["sha256"],
        "sparse6_records": len(lines),
        "oriented_terminal_choices_tested": len(lines) * order * (order - 1),
        "cycle_detector_disagreements": detector_disagreements,
        "networkx_survivors": len(nx_survivors),
        "manual_survivors": len(manual_survivors),
        "checker_agreement": True,
    }


def run(output: pathlib.Path | None = None) -> dict:
    report = {
        "experiment": "E24a-Type-A-extremal-certificates",
        "source_page": SOURCE_PAGE,
        "download_date": "2026-07-25 America/New_York",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "definition": {
            "d_B(x)": 1,
            "d_B(y)": ">=1",
            "internal_minimum_degree": 3,
            "terminal_edge": "xy absent",
            "closure": "B+xy simple and 2-connected",
        },
        "checker_A": "NetworkX is_biconnected",
        "checker_B": "direct connectivity-after-every-vertex-deletion DFS",
        "orders": {str(order): check_file(order, metadata)
                   for order, metadata in FILES.items()},
        "status": "COMPLETE",
        "exit_code": 0,
    }
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
