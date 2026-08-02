#!/usr/bin/env python3
"""Part V (defect-three phase): classification of pure-C2 F-cycle
components.

A pure-C2 F-component is a cycle v_1..v_s (s>=3) of C2-vertices, each
v_i attached to a unique H-neighbour chi(i) (indices mod s -- this is
the wraparound the task explicitly warns must be checked separately
from the linear path automaton). Two independent necessary conditions
for such a component to be compatible with F-cleanness:

  (0) s itself must not be a power of two (the cycle IS already a
      length-s cycle of G, entirely within F, regardless of any H
      attachment).
  (1) the cycle-plus-H graph (cycle edges + one spoke per vertex to its
      H-colour) must contain no C4 and no C8 (same two mechanisms as
      the linear lemma, mechanism (a) same-colour at cyclic distance 2
      or 6, mechanism (b) two disjoint sub-arcs of the cycle between a
      fixed colour pair summing to 4 edges -- but now "distance" and
      "sub-arc" are computed CYCLICALLY, and a sub-arc may also cross
      the wraparound seam).

This script builds the actual graph directly (cycle edges + spokes) and
checks C4/C8 with the same dual detector used throughout the project,
for every candidate s and every colouring up to symmetry-breaking
(fix chi(1)=0, since a global colour permutation and cyclic rotation
of a component are graph isomorphisms).
"""
from __future__ import annotations

import hashlib
import itertools
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402


def is_power_of_two(n: int) -> bool:
    return n >= 1 and (n & (n - 1)) == 0


def build_cyclic_graph(coloring: tuple[int, ...], h: int) -> nx.Graph:
    s = len(coloring)
    G = nx.Graph()
    G.add_nodes_from(f"p{i}" for i in range(s))
    G.add_nodes_from(f"H{c}" for c in range(h))
    for i in range(s):
        G.add_edge(f"p{i}", f"p{(i + 1) % s}")
    for i, c in enumerate(coloring):
        G.add_edge(f"p{i}", f"H{c}")
    return G


def has_forbidden_cycle_cyclic(coloring: tuple[int, ...], h: int) -> bool:
    """Checks C4/C8 only (the scope of mechanisms (a)/(b), matching Part
    IV's linear lemma exactly). The whole-cycle-is-a-power-of-two
    condition (0) is checked separately by the caller via
    is_power_of_two(s), covering C16/C32/... as a distinct, simpler
    necessary condition that does not depend on the colouring at all."""
    G = build_cyclic_graph(coloring, h)
    relabel = {v: i for i, v in enumerate(sorted(G, key=str))}
    g = from_edges(G.number_of_nodes(), [(relabel[u], relabel[v]) for u, v in G.edges()])
    c4 = has_cycle_len_dfs(g, 4)
    c8 = has_cycle_len_dfs(g, 8)
    c4n = has_cycle_len_nx(g, 4)
    c8n = has_cycle_len_nx(g, 8)
    assert c4 == c4n and c8 == c8n, f"detector disagreement coloring={coloring}"
    return c4 or c8


def classify(h: int, s_max: int) -> dict[str, Any]:
    valid_by_s: dict[int, list[tuple[int, ...]]] = {}
    for s in range(3, s_max + 1):
        if is_power_of_two(s):
            continue
        survivors = []
        for rest in itertools.product(range(h), repeat=s - 1):
            coloring = (0,) + rest
            if not has_forbidden_cycle_cyclic(coloring, h):
                survivors.append(coloring)
        if survivors:
            valid_by_s[s] = survivors
    return {
        "h": h, "s_max_searched": s_max,
        "valid_s_values": sorted(valid_by_s.keys()),
        "example_per_s": {str(k): list(v[0]) for k, v in valid_by_s.items()},
        "count_per_s": {str(k): len(v) for k, v in valid_by_s.items()},
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--s-max", type=int, default=14)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report: dict[str, Any] = {}
    for h in (1, 2, 3):
        r = classify(h, args.s_max)
        report[f"h{h}"] = r
        print(f"h={h}: valid cyclic s (up to {args.s_max}) = {r['valid_s_values']}")

    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
