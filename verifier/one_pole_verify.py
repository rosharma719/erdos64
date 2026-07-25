"""
Independent verifier for one-pole search survivors (task Part 5).

Two independence layers, both required to trust a survivor:
  1. Re-check the one-pole candidate itself with the OTHER cycle detector
     (has_cycle_len_nx, networkx-based -- independent implementation from
     the DFS backtracking used in one_pole_search.py's primary pass).
  2. Explicitly build the DOUBLED graph (two copies of H glued at the root,
     per S4/S5's construction) and independently verify from scratch that
     it (a) has min degree >=3 everywhere, (b) has no power-of-two cycle --
     using BOTH detectors on the doubled graph, not just re-using the
     un-doubled result. This is the graph that would actually refute
     Erdos-Gyarfas, so it gets the full independent check, not the root
     alone.

Run with no arguments: reads verifier/one_pole_survivors.json (written by
one_pole_search.py) and re-verifies every entry. If that file is absent or
empty, reports that there is nothing to verify (this is the expected/normal
state -- it means no survivor has been found yet).
"""
from __future__ import annotations
import json
import os
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import (from_edges, min_degree, powers_of_two_up_to,
                           has_cycle_len_dfs, has_cycle_len_nx, Graph)


def read_graph6(g6: str) -> Graph:
    import networkx as nx
    G = nx.from_graph6_bytes(g6.strip().encode())
    n = G.number_of_nodes()
    return from_edges(n, list(G.edges()))


def double_at_root(g: Graph, root: int) -> Graph:
    """Two disjoint copies of g, vertices of copy 2 relabeled by +n except
    the root, which is identified with copy 1's root."""
    n = len(g)
    edges = []
    for u in g:
        for v in g[u]:
            if u < v:
                edges.append((u, v))
    edges2 = []
    for (u, v) in edges:
        u2 = u if u == root else u + n
        v2 = v if v == root else v + n
        edges2.append((u2, v2))
    all_edges = edges + edges2
    new_n = 2 * n - 1
    # relabel to a contiguous 0..new_n-1 range
    verts = sorted({x for e in all_edges for x in e})
    assert len(verts) == new_n, (len(verts), new_n)
    remap = {v: i for i, v in enumerate(verts)}
    remapped = [(remap[a], remap[b]) for a, b in all_edges]
    return from_edges(new_n, remapped)


def verify_one(entry: dict) -> bool:
    n, g6, root = entry["n"], entry["g6"], entry["root"]
    g = read_graph6(g6)
    print(f"--- verifying n={n} g6={g6} root={root} ---")

    # Layer 1: re-check H itself with the independent nx-based detector.
    for L in powers_of_two_up_to(n):
        dfs_result = has_cycle_len_dfs(g, L)
        nx_result = has_cycle_len_nx(g, L)
        status = "OK" if dfs_result == nx_result else "MISMATCH!!"
        print(f"  H: L={L} dfs={dfs_result} nx={nx_result} [{status}]")
        if dfs_result != nx_result:
            print("  DETECTOR DISAGREEMENT on H itself -- ABORT, do not trust")
            return False
        if dfs_result:
            print(f"  H actually HAS a length-{L} cycle -- not a real survivor")
            return False

    # Layer 2: build the doubled graph and fully re-verify from scratch.
    H2 = double_at_root(g, root)
    n2 = len(H2)
    md = min_degree(H2)
    print(f"  doubled graph: n={n2}, min_degree={md}")
    if md < 3:
        print("  DOUBLED GRAPH HAS MIN DEGREE < 3 -- construction is broken, ABORT")
        return False
    for L in powers_of_two_up_to(n2):
        dfs_result = has_cycle_len_dfs(H2, L)
        nx_result = has_cycle_len_nx(H2, L)
        status = "OK" if dfs_result == nx_result else "MISMATCH!!"
        print(f"  H2: L={L} dfs={dfs_result} nx={nx_result} [{status}]")
        if dfs_result != nx_result:
            print("  DETECTOR DISAGREEMENT on doubled graph -- ABORT, do not trust")
            return False
        if dfs_result:
            print(f"  DOUBLED GRAPH HAS a length-{L} cycle -- doubling created a "
                  f"forbidden cycle, H does NOT yield a counterexample")
            return False

    print(f"  CONFIRMED: doubled graph n={n2} has min degree {md} >= 3 and "
          f"NO power-of-two cycle, independently re-verified with both "
          f"detectors. This is a genuine Erdos-Gyarfas counterexample "
          f"IF this result is correct -- escalate immediately, do not "
          f"just log it.")
    return True


def main():
    path = "verifier/one_pole_survivors.json"
    if not os.path.exists(path):
        print(f"{path} not found -- nothing to verify. This is the expected "
              f"state when one_pole_search.py has not yet found any survivor.")
        return
    with open(path) as f:
        entries = json.load(f)
    if not entries:
        print(f"{path} is empty -- no survivors to verify.")
        return
    all_confirmed = True
    for entry in entries:
        ok = verify_one(entry)
        all_confirmed = all_confirmed and ok
    print(f"\n=== {'ALL CONFIRMED' if all_confirmed else 'SOME FAILED VERIFICATION'} "
          f"({len(entries)} entries) ===")


if __name__ == "__main__":
    main()
