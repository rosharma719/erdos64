#!/usr/bin/env python3
"""Verify the safe-4-pole cycle decomposition on a completed Type-T port graph.

Every completed Type-T `j=4` instance has degree sequence `(4,3^{n-1})` with
`z0` (vertex 0 in the core-export labelling) the unique degree-4 vertex.
Removing `z0` leaves a connected "4-pole" whose 4 terminals (its former
neighbours) each have degree exactly 2. Consequently, for every power of two
`2^k`:

    N_{2^k}(G) = N_{2^k}(G - z0) + sum_{ {u,v} subset terminals } N_{u,v}(2^k - 2)

i.e. every dyadic cycle in the completed graph is either an "internal" cycle
of the 4-pole, or a terminal-to-terminal path of the shifted length `2^k-2`
closed through `z0` and its two cap edges. Each terminal-path witness is also
claimed to use at most `floor((2^k-3)/3)` completion "passages" (hub
vertices, i.e. vertices with index >= the bare-core order `5*2^j+7`), since
each hub contributes exactly 2 edges of path length.

This script independently checks both claims by brute-force simple-cycle /
simple-path enumeration (networkx), for any completed-graph JSON with the
`{parameters:{j,a,c}, completion:{edges}, best_short_cycle_counts}` schema
used under data/type_t_port_c16/ and data/type_t_port_multipole/.

Usage:
    python verifier/type_t_port_safe_4pole.py data/type_t_port_c16/*.json [--k 4]
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

import networkx as nx


def load_completed_graph(path: Path) -> tuple[nx.Graph, dict]:
    payload = json.loads(path.read_text())
    edges = payload["completion"]["edges"]
    graph = nx.Graph()
    graph.add_edges_from((u, v) for u, v in edges)
    return graph, payload


def core_order(j: int) -> int:
    return 5 * (1 << j) + 7


def count_cycles_len(graph: nx.Graph, length: int) -> int:
    return sum(1 for cyc in nx.simple_cycles(graph, length_bound=length) if len(cyc) == length)


def simple_paths_len(adj: dict[int, list[int]], a: int, b: int, length: int) -> list[list[int]]:
    """All simple a->b paths with exactly `length` edges (DFS, exact-length pruning)."""
    results: list[list[int]] = []
    visited = {a}
    path = [a]

    def dfs(u: int, depth: int) -> None:
        if depth == length:
            if u == b:
                results.append(list(path))
            return
        for w in adj[u]:
            if w in visited:
                continue
            if w == b and depth + 1 != length:
                continue
            visited.add(w)
            path.append(w)
            dfs(w, depth + 1)
            path.pop()
            visited.discard(w)

    dfs(a, 0)
    return results


def verify_instance(path: Path, k: int) -> bool:
    graph, payload = load_completed_graph(path)
    params = payload["parameters"]
    j, a, c = params["j"], params["a"], params["c"]
    n0 = core_order(j)
    target = 1 << k
    shifted = target - 2
    bound_m = (target - 3) // 3

    z0_candidates = [v for v, d in graph.degree() if d == 4]
    ok_header = f"{path.name}  (j={j},a={a},c={c})  target=C{target}"
    if len(z0_candidates) != 1:
        print(f"{ok_header}: FAIL - expected exactly one degree-4 vertex, found {z0_candidates}")
        return False
    z0 = z0_candidates[0]

    terminals = list(graph.neighbors(z0))
    pole = graph.copy()
    pole.remove_node(z0)

    if not nx.is_connected(pole):
        print(f"{ok_header}: FAIL - pole graph (G-z0) is disconnected")
        return False
    if len(terminals) != 4 or any(pole.degree(t) != 2 for t in terminals):
        print(f"{ok_header}: FAIL - terminals not exactly 4 degree-2 vertices: "
              f"{[(t, pole.degree(t)) for t in terminals]}")
        return False

    internal = count_cycles_len(pole, target)

    adj = {v: list(pole.neighbors(v)) for v in pole.nodes()}
    terminal_total = 0
    max_m_seen = 0
    m_hist: dict[int, int] = {}
    for u, v in itertools.combinations(terminals, 2):
        for p in simple_paths_len(adj, u, v, shifted):
            terminal_total += 1
            m = sum(1 for node in p if node >= n0)
            m_hist[m] = m_hist.get(m, 0) + 1
            max_m_seen = max(max_m_seen, m)

    predicted = internal + terminal_total
    reported = payload.get("best_short_cycle_counts", {}).get(str(target))

    decomposition_ok = reported is None or predicted == reported
    bound_ok = max_m_seen <= bound_m

    status = "OK" if decomposition_ok and bound_ok else "FAIL"
    print(f"{ok_header}: {status}  internal={internal} terminal_paths={terminal_total} "
          f"predicted_total={predicted} reported={reported}  "
          f"max_m={max_m_seen} (bound {bound_m})  m_hist={dict(sorted(m_hist.items()))}")
    return decomposition_ok and bound_ok


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--k", type=int, default=4, help="verify the 2^k cycle length (default 4 -> C16)")
    args = parser.parse_args()

    all_ok = True
    for path in args.paths:
        try:
            all_ok &= verify_instance(path, args.k)
        except Exception as exc:  # noqa: BLE001 - report and continue across a batch
            print(f"{path.name}: ERROR - {exc}")
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
