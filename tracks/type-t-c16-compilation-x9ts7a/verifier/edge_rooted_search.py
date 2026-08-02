"""
Edge-rooted (G,e) search (task Part 6, 2026-07-25, third redirection pass).

Per one_pole.md's suppressed-edge equivalence: a one-pole survivor exists
iff there is a loopless graph G with delta(G)>=3 and an edge e such that
G-e has no 2^k-cycle AND no e-using cycle of G has length 2^k-1. This
script searches directly over (G,e) pairs (G connected, delta>=3, from
geng) instead of over one-pole graphs -- a full failure (both conditions
avoided) corresponds EXACTLY to a one-pole survivor after subdividing e
(replacing e with a length-2 path through a fresh root vertex r).

For every (G,e) pair tested we record, per the task's diagnostic list:
  - whether G-e has a 2^k-cycle (and if so, all such cycles / lengths)
  - all e-using cycle lengths, and their distance to the nearest 2^k-1
  - the SPQR node type where e sits (via spqrtree, root suppressed as in
    the O4' application: this script works with G directly, e's own
    endpoints are exactly the "a,b" of the corresponding one-pole)
  - a coarse "near-failure" score: how close (G,e) comes to satisfying
    the full equivalence (0 = an outright one-pole survivor).
"""
from __future__ import annotations
import subprocess
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, powers_of_two_up_to, has_cycle_len_dfs, Graph

import networkx as nx
import spqrtree


def run_geng(n: int, extra=()):
    cmd = ["geng", "-c", "-d3"] + list(extra) + [str(n)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield line
    proc.wait()


def all_cycle_lengths_through_edge(nxG, u, v, cap=None):
    """All simple cycle lengths using edge (u,v): equivalently 1 + (all
    simple u-v path lengths in G-e)."""
    H = nxG.copy()
    H.remove_edge(u, v)
    lengths = set()
    for path in nx.all_simple_paths(H, u, v, cutoff=cap):
        lengths.add(len(path))  # path has len(path)-1 edges; +1 for edge e = len(path)
    return lengths


def dyadic_cycle_lengths_in(g_dict: Graph, n: int):
    return {L: has_cycle_len_dfs(g_dict, L) for L in powers_of_two_up_to(n)}


def nearest_below_forbidden(ell: int) -> int:
    """distance from ell to the nearest 2^k - 1 (k>=2)."""
    best = None
    p = 4
    while p <= 2 * (ell + 4):
        target = p - 1
        d = abs(ell - target)
        if best is None or d < best:
            best = d
        p *= 2
    return best


def spqr_location_of_edge(nxG, u, v):
    """Locate which SPQR node (of G, treated as-is if 2-connected) the
    edge (u,v) belongs to, and that node's type."""
    if nx.node_connectivity(nxG) < 2:
        return None
    sg = spqrtree.MultiGraph()
    for a, b in nxG.edges():
        sg.add_edge(a, b)
    tree = spqrtree.SPQRTree(sg)
    for node in tree.nodes():
        for e in node.skeleton.edges:
            if not e.virtual and {e.u, e.v} == {u, v}:
                return node.type.value
    return None


def analyze_pair(nxG, u, v, n):
    g = from_edges(n, list(nxG.edges()))
    H_minus_e = {vv: set(nb) for vv, nb in g.items()}
    H_minus_e[u].discard(v)
    H_minus_e[v].discard(u)

    dyadic_spec = dyadic_cycle_lengths_in(H_minus_e, n)
    ge_has_2k = any(dyadic_spec.values())
    power_cycles = [L for L, present in dyadic_spec.items() if present]

    e_lengths = all_cycle_lengths_through_edge(nxG, u, v, cap=n)
    forbidden_minus1 = {2 ** k - 1 for k in range(2, 20) if 2 ** k - 1 <= n}
    e_hits_forbidden_minus1 = bool(e_lengths & forbidden_minus1)

    is_full_failure = (not ge_has_2k) and (not e_hits_forbidden_minus1)

    dist = min((nearest_below_forbidden(ell) for ell in e_lengths), default=None)

    return dict(
        ge_has_2k=ge_has_2k, power_cycles=power_cycles,
        e_lengths=sorted(e_lengths), e_hits_forbidden_minus1=e_hits_forbidden_minus1,
        min_dist_to_2k_minus1=dist, is_full_failure=is_full_failure,
        spqr_type=spqr_location_of_edge(nxG, u, v),
    )


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=4)
    ap.add_argument("--nmax", type=int, default=9)
    args = ap.parse_args()

    total_pairs = 0
    full_failures = []
    near_misses = []  # dist==0 or 1, i.e. e_lengths very close to 2^k-1 but not hitting

    for n in range(args.nmin, args.nmax + 1):
        n_graphs = 0
        for g6 in run_geng(n):
            n_graphs += 1
            G = nx.from_graph6_bytes(g6.encode())
            for (u, v) in list(G.edges()):
                total_pairs += 1
                res = analyze_pair(G, u, v, n)
                if res["is_full_failure"]:
                    full_failures.append((n, g6, u, v, res))
                elif res["min_dist_to_2k_minus1"] is not None and res["min_dist_to_2k_minus1"] <= 1 \
                        and not res["ge_has_2k"]:
                    near_misses.append((n, g6, u, v, res))
        print(f"n={n}: {n_graphs} connected delta>=3 graphs, "
              f"cumulative (G,e) pairs={total_pairs}")

    print(f"\n=== SUMMARY n={args.nmin}..{args.nmax} ===")
    print(f"total (G,e) pairs tested: {total_pairs}")
    print(f"FULL FAILURES (one-pole survivors after subdividing e): {len(full_failures)}")
    for n, g6, u, v, res in full_failures[:10]:
        print(f"  n={n} g6={g6} e=({u},{v}) {res}")
    print(f"\nnear-misses (G-e power-cycle-free, e-cycle length within 1 of "
          f"a forbidden 2^k-1): {len(near_misses)}")
    for n, g6, u, v, res in near_misses[:10]:
        print(f"  n={n} g6={g6} e=({u},{v}) e_lengths={res['e_lengths']} "
              f"dist={res['min_dist_to_2k_minus1']} spqr={res['spqr_type']}")


if __name__ == "__main__":
    main()
