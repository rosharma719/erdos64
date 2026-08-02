#!/usr/bin/env python3
"""Part IV (defect-three phase): the colored degree-2 path lemma,
verified by direct graph construction (implementation 1) and used to
build the minimal finite-state automaton (implementation 2, in
colored_path_automaton.py).

Setup: a path v_1..v_t of C2-vertices, each v_i with a unique H-neighbour
chi(i) in a fixed color set of size h. The realized graph is the path
edges plus the attachment edges chi(i)-v_i, with NO edges inside H (H
independent). We want the exact maximum t such that SOME coloring
chi:{1..t}->H avoids creating a C4 or C8 in this graph.

KEY STRUCTURAL FACT USED FOR CORRECTNESS (prefix-closure): if a coloring
of length t is C4/C8-free, every PREFIX of it (any chi restricted to
{1..t'} for t'<t) is also C4/C8-free, because shortening the path can
only REMOVE potential cycles (fewer vertices/edges), never add one. So a
breadth-first search that, at each length, keeps EVERY valid coloring
and extends it by every possible next color, extending until NO valid
coloring at the current length admits ANY valid extension, finds the
TRUE maximum -- not merely "no counterexample found below a cutoff": if
level t+1 is empty while level t is not, then by prefix-closure no valid
word of length >t can exist either (its own length-(t+1) prefix would
have to be valid, but none is), so t is provably the exact maximum.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402


def build_graph(coloring: tuple[int, ...], h: int) -> nx.Graph:
    """Vertices: path positions 0..t-1 (labelled 'p0'..), H-colors
    0..h-1 (labelled 'H0'..). Path edges p_i-p_{i+1}; attachment edges
    p_i - H_{chi(i)}."""
    G = nx.Graph()
    t = len(coloring)
    G.add_nodes_from(f"p{i}" for i in range(t))
    G.add_nodes_from(f"H{c}" for c in range(h))
    for i in range(t - 1):
        G.add_edge(f"p{i}", f"p{i+1}")
    for i, c in enumerate(coloring):
        G.add_edge(f"p{i}", f"H{c}")
    return G


def has_forbidden_cycle(coloring: tuple[int, ...], h: int) -> tuple[bool, dict[str, Any]]:
    G = build_graph(coloring, h)
    relabel = {v: i for i, v in enumerate(sorted(G, key=str))}
    g = from_edges(G.number_of_nodes(), [(relabel[u], relabel[v]) for u, v in G.edges()])
    c4 = has_cycle_len_dfs(g, 4)
    c8 = has_cycle_len_dfs(g, 8)
    c4n = has_cycle_len_nx(g, 4)
    c8n = has_cycle_len_nx(g, 8)
    assert c4 == c4n and c8 == c8n, f"detector disagreement on {coloring}"
    return (c4 or c8), {"c4": c4, "c8": c8}


def max_length_search(h: int) -> dict[str, Any]:
    """Prefix-closed BFS: level t = every valid (C4/C8-free) coloring of
    length exactly t. Terminates the FIRST time a level is empty --
    proving (by prefix-closure) that the previous level's length is the
    true maximum, not an arbitrary cutoff."""
    level: list[tuple[int, ...]] = [()]
    max_valid_length = 0
    witness_per_length: dict[int, tuple[int, ...]] = {0: ()}
    levels_sizes: dict[int, int] = {0: 1}
    while level:
        next_level = []
        for word in level:
            for c in range(h):
                candidate = word + (c,)
                bad, _ = has_forbidden_cycle(candidate, h)
                if not bad:
                    next_level.append(candidate)
        if not next_level:
            break
        t = len(next_level[0])
        levels_sizes[t] = len(next_level)
        witness_per_length[t] = next_level[0]
        max_valid_length = t
        level = next_level
    return {
        "h": h,
        "max_valid_length": max_valid_length,
        "levels_sizes": levels_sizes,
        "witness_per_length": {k: list(v) for k, v in witness_per_length.items()},
        "final_level_all_words": [list(w) for w in level] if max_valid_length <= 12 else None,
    }


def main() -> int:
    import argparse
    import json
    import hashlib

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from verifier.z3_certificate import compact_json

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    expected = {1: 2, 2: 5, 3: 8}
    report = {}
    all_ok = True
    for h in (1, 2, 3):
        r = max_length_search(h)
        report[str(h)] = r
        ok = (r["max_valid_length"] == expected[h])
        all_ok &= ok
        print(f"h={h}: max valid length = {r['max_valid_length']} "
              f"(expected {expected[h]}, match={ok}); "
              f"level sizes = {r['levels_sizes']}")

    encoded = compact_json(report)
    checksum = hashlib.sha256(encoded.encode()).hexdigest()
    report["records_sha256"] = checksum
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
