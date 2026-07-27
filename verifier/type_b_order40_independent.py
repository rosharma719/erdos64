#!/usr/bin/env python3
"""Generic independent (networkx-only) witness verifier for the order-40
frontier candidates. Reads only a saved candidate file (edges, plus nv/
path/a/y passed on the command line) -- does not call either generator's
internal functions. Re-derives every claim from scratch: vertex/edge
counts, connectivity, degree sequence, path presence, C4/C8/C16-freeness,
and the three closing-path witnesses (lengths 2, 6, 14).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import networkx as nx


def has_cycle_len_nx(g: nx.Graph, L: int):
    for cyc in nx.simple_cycles(g, length_bound=L):
        if len(cyc) == L:
            return cyc
    return None


def find_simple_path_len(g: nx.Graph, u: int, v: int, L: int):
    for p in nx.all_simple_paths(g, u, v, cutoff=L):
        if len(p) - 1 == L:
            return p
    return None


def verify_one(record: dict, nv: int, path_edges: list, a: int, y: int,
                expected_degree_seq) -> dict:
    edges = record["edges"]
    g = nx.Graph()
    g.add_nodes_from(range(nv))
    g.add_edges_from(path_edges)
    g.add_edges_from(tuple(e) for e in edges)

    result = {"edges": sorted(tuple(sorted(e)) for e in edges)}
    result["n_vertices"] = g.number_of_nodes()
    result["n_edges"] = g.number_of_edges()
    result["connected"] = nx.is_connected(g)

    degrees = sorted(d for _, d in g.degree())
    result["degree_sequence_ok"] = degrees == sorted(expected_degree_seq)
    result["path_present"] = all(g.has_edge(u, v) for u, v in path_edges)

    c4 = has_cycle_len_nx(g, 4)
    c8 = has_cycle_len_nx(g, 8)
    c16 = has_cycle_len_nx(g, 16)
    result["c4"] = c4 is not None
    result["c8"] = c8 is not None
    result["c16"] = c16 is not None
    if c16 is not None:
        result["c16_witness"] = c16

    ay2 = find_simple_path_len(g, a, y, 2)
    ay6 = find_simple_path_len(g, a, y, 6)
    ay14 = find_simple_path_len(g, a, y, 14)
    result["has_ay_len2"] = ay2 is not None
    result["has_ay_len6"] = ay6 is not None
    result["has_ay_len14"] = ay14 is not None
    if ay2 is not None:
        result["ay_len2"] = ay2
    if ay6 is not None:
        result["ay_len6"] = ay6
    if ay14 is not None:
        result["ay_len14"] = ay14

    result["eliminated"] = (
        result["c4"] or result["c8"] or result["c16"]
        or result["has_ay_len2"] or result["has_ay_len6"] or result["has_ay_len14"]
    )
    result["fully_consistent"] = (
        result["connected"] and result["degree_sequence_ok"] and result["path_present"]
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--nv", type=int, required=True)
    parser.add_argument("--path-len", type=int, required=True,
                         help="number of path edges (0..path_len are consecutive)")
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--y", type=int, required=True)
    parser.add_argument("--degree-seq", type=str, required=True,
                         help="comma-separated expected degree sequence")
    args = parser.parse_args()

    path_edges = [(i, i + 1) for i in range(args.path_len)]
    expected_degree_seq = [int(x) for x in args.degree_seq.split(",")]

    records = []
    with args.input.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    verified = [verify_one(r, args.nv, path_edges, args.a, args.y, expected_degree_seq)
                for r in records]
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
