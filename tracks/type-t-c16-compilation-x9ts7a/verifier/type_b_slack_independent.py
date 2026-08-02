#!/usr/bin/env python3
"""Independent witness verifier for Family II (2^2,3^16,4) candidates.

Reads ONLY a saved candidate file (edges + role label) -- it does not call
verifier/type_b_slack_path_search.c's generator, its incremental
cycle-pruning routine, or verifier/type_b_slack_path_sat.py's SAT encoding.
It uses networkx exclusively (a third, independent method after the C
from-scratch DFS and the pysat CNF encoding) to re-derive every claim from
scratch:

  - 19 vertices, 28 edges, connected
  - degree sequence 2,2,4,3^16
  - the fixed distinguished path p_0..p_17 is present as a subgraph
  - the degree-4 vertex matches the claimed role
  - no C4, no C8
  - an internal C16 (witness recorded if present)
  - a simple length-6 a-y path (witness recorded if present)
  - a simple length-14 a-y path (witness recorded if present)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import networkx as nx

N = 19
PATH_EDGES = [(i, i + 1) for i in range(17)]
A, Y, Z = 0, 17, 18


def build_graph(non_path_edges):
    g = nx.Graph()
    g.add_nodes_from(range(N))
    g.add_edges_from(PATH_EDGES)
    g.add_edges_from(tuple(e) for e in non_path_edges)
    return g


def has_cycle_len_nx(g: nx.Graph, L: int):
    for cyc in nx.simple_cycles(g, length_bound=L):
        if len(cyc) == L:
            return cyc
    return None


def find_simple_path_len(g: nx.Graph, u: int, v: int, L: int):
    """A simple path of length L has L+1 vertices. Exhaustive DFS via
    networkx's all_simple_paths with an exact cutoff, then filtered to the
    exact length (all_simple_paths with cutoff=L returns paths of length
    <= L)."""
    for p in nx.all_simple_paths(g, u, v, cutoff=L):
        if len(p) - 1 == L:
            return p
    return None


def verify_one(record: dict) -> dict:
    role = record["role"]
    edges = record["edges"]
    g = build_graph(edges)

    result = {"role": role, "edges": sorted(tuple(sorted(e)) for e in edges)}

    result["n_vertices"] = g.number_of_nodes()
    result["n_edges"] = g.number_of_edges()
    result["connected"] = nx.is_connected(g)

    degrees = sorted(d for _, d in g.degree())
    result["degree_sequence_ok"] = degrees == sorted([2, 2, 4] + [3] * 16)

    for u, v in PATH_EDGES:
        if not g.has_edge(u, v):
            result["path_present"] = False
            break
    else:
        result["path_present"] = True

    degree4_vertices = [v for v, d in g.degree() if d == 4]
    result["degree4_vertices"] = degree4_vertices
    if role == "z":
        result["role_matches_degree4"] = degree4_vertices == [Z]
    else:
        result["role_matches_degree4"] = degree4_vertices == [int(role)]

    c4 = has_cycle_len_nx(g, 4)
    c8 = has_cycle_len_nx(g, 8)
    c16 = has_cycle_len_nx(g, 16)
    result["c4"] = c4 is not None
    result["c8"] = c8 is not None
    result["c16"] = c16 is not None
    if c16 is not None:
        result["c16_witness"] = c16

    ay6 = find_simple_path_len(g, A, Y, 6)
    ay14 = find_simple_path_len(g, A, Y, 14)
    result["has_ay_len6"] = ay6 is not None
    result["has_ay_len14"] = ay14 is not None
    if ay6 is not None:
        result["ay_len6"] = ay6
    if ay14 is not None:
        result["ay_len14"] = ay14

    result["eliminated"] = (
        result["c4"] or result["c8"] or result["c16"]
        or result["has_ay_len6"] or result["has_ay_len14"]
    )
    result["fully_consistent"] = (
        result["connected"]
        and result["degree_sequence_ok"]
        and result["path_present"]
        and result["role_matches_degree4"]
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True,
                         help="JSON Lines file of {role, edges} candidate records")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    records = []
    with args.input.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    verified = [verify_one(r) for r in records]

    n_total = len(verified)
    n_inconsistent = sum(1 for v in verified if not v["fully_consistent"])
    n_survivors = sum(1 for v in verified if not v["eliminated"])

    summary = {
        "input": str(args.input),
        "total_candidates": n_total,
        "structurally_inconsistent": n_inconsistent,
        "not_eliminated_survivors": n_survivors,
        "conclusion": (
            "all candidates independently confirmed eliminated"
            if n_survivors == 0 and n_inconsistent == 0
            else "DISCREPANCY: see per-record detail"
        ),
    }

    args.out.write_text(json.dumps({"summary": summary, "records": verified}, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
