"""
SPQR-based classification of one-pole two-terminal structure (task Part 5,
2026-07-25).

Uses the `spqrtree` PyPI package (pure-Python implementation of the
Gutwenger-Mutzel 2001 triconnected-components/SPQR-tree algorithm, with
Hopcroft-Tarjan 1973 corrections and Di Battista-Tamassia 1996 data
structures) -- a real, citable, previously-published algorithm, NOT a
custom heuristic built for this project.

For each one-pole candidate (H, root r, neighbors a,b), builds the SPQR
tree of K+ab where K=H-r (2-connected by the O4' application in
one_pole.md -- suppressing the degree-2 root and adding the edge ab).
Reports the multiset of node types (S=series/cycle, P=parallel/bond,
R=rigid/3-connected, Q=single edge). Per one_pole.md's SPQR scoping
section: S and P nodes are already fully explained by the terminal-path
arithmetic (series = length addition, parallel = Lambda_i+Lambda_j cycle
formation); R nodes are exactly where the "no further 2-cut" pieces
requiring genuinely new tools (e.g. ear decomposition WITHIN a rigid
piece) live. This script does not attempt to interpret R-node internals
beyond flagging them -- that is future work, not claimed here.
"""
from __future__ import annotations
import subprocess
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, powers_of_two_up_to, has_cycle_len_dfs


def read_graph6_line(line: str):
    import networkx as nx
    return nx.from_graph6_bytes(line.strip().encode())


def is_one_pole_nx(G):
    deg2 = [v for v in G if G.degree(v) == 2]
    if len(deg2) != 1:
        return False, None
    r = deg2[0]
    if all(G.degree(v) >= 3 for v in G if v != r):
        return True, r
    return False, None


def run_geng(n: int):
    cmd = ["geng", "-c", "-d2", str(n)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield line
    proc.wait()


def build_K_plus_ab(G, r):
    a, b = list(G.neighbors(r))
    K = G.copy()
    K.remove_node(r)
    has_ab_already = K.has_edge(a, b)
    if not has_ab_already:
        K.add_edge(a, b)
    return K, a, b, has_ab_already


def spqr_node_type_multiset(nx_graph):
    import spqrtree
    g = spqrtree.MultiGraph()
    for u, v in nx_graph.edges():
        g.add_edge(u, v)
    tree = spqrtree.SPQRTree(g)
    counts = Counter(node.type.value for node in tree.nodes())
    return counts, tree


def classify(G, r):
    K, a, b, had_ab = build_K_plus_ab(G, r)
    if K.number_of_nodes() < 2:
        return dict(n=G.number_of_nodes(), skipped="K too small")
    try:
        counts, tree = spqr_node_type_multiset(K)
    except Exception as e:
        return dict(n=G.number_of_nodes(), error=str(e))
    return dict(
        n=G.number_of_nodes(), a=a, b=b, ab_preexisting=had_ab,
        node_counts=dict(counts),
        num_nodes=sum(counts.values()),
        has_rigid=counts.get("R", 0) > 0,
        pure_series_parallel=(counts.get("R", 0) == 0),
    )


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=5)
    ap.add_argument("--nmax", type=int, default=10)
    args = ap.parse_args()

    total = 0
    pure_sp = 0
    has_rigid = 0
    smallest_rigid = None
    node_type_totals = Counter()

    for n in range(args.nmin, args.nmax + 1):
        n_this = 0
        for g6 in run_geng(n):
            G = read_graph6_line(g6)
            ok, r = is_one_pole_nx(G)
            if not ok:
                continue
            n_this += 1
            total += 1
            res = classify(G, r)
            if "error" in res or "skipped" in res:
                continue
            node_type_totals.update(res["node_counts"])
            if res["pure_series_parallel"]:
                pure_sp += 1
            else:
                has_rigid += 1
                if smallest_rigid is None or n < smallest_rigid[0]:
                    smallest_rigid = (n, g6, res)
        print(f"n={n}: {n_this} one-pole candidates classified")

    print(f"\n=== SPQR SUMMARY n={args.nmin}..{args.nmax} (relaxed population) ===")
    print(f"total candidates: {total}")
    print(f"pure series-parallel (no R node): {pure_sp} "
          f"({100*pure_sp/total:.1f}%)" if total else "")
    print(f"contains at least one rigid (R) node: {has_rigid} "
          f"({100*has_rigid/total:.1f}%)" if total else "")
    print(f"node-type totals across all candidates: {dict(node_type_totals)}")
    if smallest_rigid:
        n, g6, res = smallest_rigid
        print(f"\nsmallest candidate containing a rigid piece: n={n} g6={g6}")
        print(f"  node counts: {res['node_counts']}")


if __name__ == "__main__":
    main()
