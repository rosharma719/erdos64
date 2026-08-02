#!/usr/bin/env python3
"""Adversarial checks for the global minimal-counterexample lemmas.

The proof is in ``lemmas.md``.  This program exhausts NetworkX's graph atlas
(all unlabeled graphs through seven vertices), selects graphs that are
inclusion-minimal subject to minimum degree at least three, and checks the
three conclusions under exactly the graph-theoretic hypotheses used by the
proof.  It is validation, not a proof of any unbounded statement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Any

import networkx as nx


def is_two_degenerate_with_order(graph: nx.Graph) -> tuple[bool, list[int]]:
    """Return a peeling order; its forward degrees are at most two."""
    work = {v: set(graph.neighbors(v)) for v in graph}
    order: list[int] = []
    while work:
        eligible = [v for v, neighbors in work.items() if len(neighbors) <= 2]
        if not eligible:
            return False, order
        v = min(eligible)
        order.append(v)
        for u in tuple(work[v]):
            work[u].remove(v)
        del work[v]
    return True, order


def forward_degrees(graph: nx.Graph, order: list[int]) -> list[int]:
    position = {v: i for i, v in enumerate(order)}
    return [sum(position[u] > position[v] for u in graph.neighbors(v)) for v in order]


def has_cycle_length(graph: nx.Graph, length: int) -> bool:
    """Exact small-graph simple-cycle test, with reversal/start symmetry cut."""
    if length < 3 or graph.number_of_nodes() < length:
        return False
    for start in sorted(graph):
        path = [start]
        used = {start}

        def visit(v: int) -> bool:
            if len(path) == length:
                return graph.has_edge(v, start) and path[1] < path[-1]
            for u in sorted(graph.neighbors(v)):
                if u <= start or u in used:
                    continue
                used.add(u)
                path.append(u)
                if visit(u):
                    return True
                path.pop()
                used.remove(u)
            return False

        if visit(start):
            return True
    return False


def is_inclusion_minimal_delta_three(graph: nx.Graph) -> bool:
    """Every proper (induced or non-induced) subgraph has minimum degree <=2."""
    n = graph.number_of_nodes()
    if n == 0 or min(dict(graph.degree()).values()) < 3:
        return False

    # A proper spanning subgraph with delta>=3 exists iff deleting some one
    # edge already preserves delta>=3.
    for u, v in graph.edges():
        if graph.degree(u) >= 4 and graph.degree(v) >= 4:
            return False

    vertices = sorted(graph)
    # Any subgraph on a proper vertex set is dominated by the induced graph on
    # that set, so it suffices to test induced subgraphs.
    for size in range(4, n):
        for subset in combinations(vertices, size):
            subgraph = graph.subgraph(subset)
            if min(dict(subgraph.degree()).values()) >= 3:
                return False
    return True


def certify(graph: nx.Graph) -> dict[str, Any]:
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    cubic = sorted(v for v in graph if graph.degree(v) == 3)
    high = sorted(v for v in graph if graph.degree(v) >= 4)
    every_vertex_touches_cubic = all(
        any(graph.degree(u) == 3 for u in graph.neighbors(v)) for v in graph
    )
    high_independent = graph.subgraph(high).number_of_edges() == 0
    cross_edges = sum(1 for u, v in graph.edges() if (u in cubic) != (v in cubic))

    deletion_checks = []
    for v in cubic:
        reduced = graph.copy()
        reduced.remove_node(v)
        two_degenerate, order = is_two_degenerate_with_order(reduced)
        fwd = forward_degrees(reduced, order) if two_degenerate else []
        caps = [min(2, len(order) - 1 - i) for i in range(len(order))]
        deficit = sum(cap - actual for cap, actual in zip(caps, fwd))
        deletion_checks.append(
            {
                "vertex": v,
                "two_degenerate": two_degenerate,
                "order": order,
                "forward_degrees": fwd,
                "deficit": deficit,
            }
        )

    q = 2 * n - 2 - m
    c4 = has_cycle_length(graph, 4)
    degree_excess = sum(graph.degree(v) - 3 for v in graph)
    return {
        "n": n,
        "m": m,
        "graph6": nx.to_graph6_bytes(graph, header=False).decode().strip(),
        "cubic_vertices": cubic,
        "high_vertices": high,
        "every_vertex_touches_cubic": every_vertex_touches_cubic,
        "high_independent": high_independent,
        "cross_edges": cross_edges,
        "two_thirds": 3 * len(cubic) >= 2 * n,
        "coarse_edge_bound": m <= 2 * n - 2,
        "c4": c4,
        "sharp_edge_bound_if_c4_free": c4 or m <= 2 * n - 3,
        "q": q,
        "q_nonnegative": q >= 0,
        "q_positive_if_c4_free": c4 or q >= 1,
        "degree_excess": degree_excess,
        "degree_excess_identity": degree_excess == n - 4 - 2 * q,
        "degree_excess_bound_if_c4_free": c4 or degree_excess <= n - 6,
        "deletion_checks": deletion_checks,
    }


def atlas_report() -> dict[str, Any]:
    candidates = []
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() < 4 or not nx.is_connected(graph):
            continue
        if is_inclusion_minimal_delta_three(graph):
            candidates.append(certify(graph))

    failures = []
    for record in candidates:
        required = [
            record["every_vertex_touches_cubic"],
            record["high_independent"],
            record["two_thirds"],
            record["coarse_edge_bound"],
            record["sharp_edge_bound_if_c4_free"],
            record["q_nonnegative"],
            record["q_positive_if_c4_free"],
            record["degree_excess_identity"],
            record["degree_excess_bound_if_c4_free"],
            all(check["two_degenerate"] for check in record["deletion_checks"]),
            all(check["deficit"] == record["q"] for check in record["deletion_checks"]),
        ]
        if not all(required):
            failures.append(record["graph6"])

    canonical = json.dumps(candidates, sort_keys=True, separators=(",", ":")).encode()
    return {
        "schema": "erdos64-global-core-small-v1",
        "source": "networkx.graph_atlas_g (all unlabeled graphs through order 7)",
        "selection": "connected and every proper subgraph has minimum degree at most 2",
        "graphs_checked": len(candidates),
        "orders": {
            str(n): sum(record["n"] == n for record in candidates) for n in range(4, 8)
        },
        "c4_free_graphs": sum(not record["c4"] for record in candidates),
        "equality_m_2n_minus_2": sum(
            record["m"] == 2 * record["n"] - 2 for record in candidates
        ),
        "failures": failures,
        "records_sha256": hashlib.sha256(canonical).hexdigest(),
        "records": candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = atlas_report()
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(
        f"checked={report['graphs_checked']} c4_free={report['c4_free_graphs']} "
        f"equality={report['equality_m_2n_minus_2']} failures={len(report['failures'])}"
    )
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
