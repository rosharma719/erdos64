"""
Bridge-signature library (task Part 5, 2026-07-25, fifth redirection pass).

Enumerates two-terminal graphs B (terminals x,y) satisfying T1's exact
hypothesis:
  - B+xy is 2-connected (checked directly, not assumed);
  - every internal (non-x,y) vertex has degree >= 3 in B;
  - internal cycles of B avoid F = {2^k : k>=2}.

For each qualifying B, stores
  Sigma(B) = (|V(B)|-2, |E(B)|, d_B(x), d_B(y), Lambda(B), C(B))
where Lambda(B) is the x-y path length spectrum and C(B) is the internal
cycle length spectrum -- both computed with TWO independent
implementations (DFS backtracking and networkx-based simple_cycles/
all_simple_paths enumeration -- the same dual-detector discipline used
since E0) and cross-checked to agree before being trusted.

Deduplicates by signature, keeping >=1 concrete graph6 realization per
signature.
"""
from __future__ import annotations
import subprocess
import sys
import itertools
from collections import defaultdict

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, powers_of_two_up_to, has_cycle_len_dfs, has_cycle_len_nx

import networkx as nx


def run_geng(n: int, extra=()):
    cmd = ["geng", "-c"] + list(extra) + [str(n)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield line
    proc.wait()


def all_simple_path_lengths_dfs(nxG, s, t):
    """DFS-based enumeration, independent of networkx's own path finder."""
    adj = {v: set(nxG.neighbors(v)) for v in nxG.nodes()}
    lengths = set()
    visited = {s}
    path = [s]

    def dfs(u):
        if u == t:
            lengths.add(len(path) - 1)
            return
        for w in adj[u]:
            if w in visited:
                continue
            visited.add(w)
            path.append(w)
            dfs(w)
            path.pop()
            visited.discard(w)

    dfs(s)
    return lengths


def all_simple_path_lengths_nx(nxG, s, t):
    return {len(p) - 1 for p in nx.all_simple_paths(nxG, s, t)}


def is_valid_bridge_candidate(nxG, x, y):
    if x == y or not nxG.has_node(x) or not nxG.has_node(y):
        return False
    for v in nxG.nodes():
        if v in (x, y):
            continue
        if nxG.degree(v) < 3:
            return False
    return True


def bridge_plus_xy_is_2connected(nxG, x, y):
    H = nxG.copy()
    if not H.has_edge(x, y):
        H.add_edge(x, y)
    if H.number_of_nodes() < 3:
        return H.number_of_nodes() == 2  # trivial K2 edge case
    return nx.node_connectivity(H) >= 2


def signature_of(nxG, x, y, n):
    lam_dfs = all_simple_path_lengths_dfs(nxG, x, y)
    lam_nx = all_simple_path_lengths_nx(nxG, x, y)
    assert lam_dfs == lam_nx, f"Lambda mismatch: dfs={lam_dfs} nx={lam_nx}"

    verts = sorted(nxG.nodes())
    remap = {v: i for i, v in enumerate(verts)}
    g = from_edges(n, [(remap[u], remap[v]) for u, v in nxG.edges()])
    c_dfs = {L for L in powers_of_two_up_to(n) if has_cycle_len_dfs(g, L)}
    c_nx = {L for L in powers_of_two_up_to(n) if has_cycle_len_nx(g, L)}
    assert c_dfs == c_nx, f"C mismatch: dfs={c_dfs} nx={c_nx}"

    internal_ok = not c_dfs  # internal cycles must avoid F entirely
    sig = (n - 2, nxG.number_of_edges(), nxG.degree(x), nxG.degree(y),
           frozenset(lam_dfs), frozenset(c_dfs))
    return sig, internal_ok


def build_library(nmin=3, nmax=8):
    library = {}  # signature -> list of (n, g6, x, y)
    total_checked = 0
    total_qualifying = 0

    for n in range(nmin, nmax + 1):
        for g6 in run_geng(n):
            G = nx.from_graph6_bytes(g6.encode())
            verts = list(G.nodes())
            for x, y in itertools.combinations(verts, 2):
                total_checked += 1
                if not is_valid_bridge_candidate(G, x, y):
                    continue
                if not bridge_plus_xy_is_2connected(G, x, y):
                    continue
                sig, internal_ok = signature_of(G, x, y, n)
                if not internal_ok:
                    continue
                total_qualifying += 1
                library.setdefault(sig, []).append((n, g6, x, y))

    return library, total_checked, total_qualifying


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=3)
    ap.add_argument("--nmax", type=int, default=7)
    args = ap.parse_args()

    library, total_checked, total_qualifying = build_library(args.nmin, args.nmax)

    print(f"total (graph, x, y) candidates checked: {total_checked}")
    print(f"total qualifying bridge realizations (T1 + internal degree + "
          f"internal F-clean): {total_qualifying}")
    print(f"distinct SIGNATURES (deduplicated): {len(library)}")

    by_c = sum(1 for k, v in library.items() if len(v) > 1)
    print(f"signatures with >1 realization: {by_c}")

    print("\nsample signatures (up to 15):")
    for sig, reals in list(library.items())[:15]:
        c_internal, m, dx, dy, lam, c = sig
        n, g6, x, y = reals[0]
        print(f"  internal_verts={c_internal} edges={m} d(x)={dx} d(y)={dy} "
              f"Lambda={sorted(lam)} C_internal={sorted(c)} "
              f"| example: n={n} g6={g6} x={x} y={y} (#realizations={len(reals)})")

    return library


if __name__ == "__main__":
    main()
