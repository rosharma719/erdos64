#!/usr/bin/env python3
"""
Bounded, independent spot-check of the externally-supplied claim: all
5-sheeted S_5 permutation lifts of the 17 connected cubic pseudographs on 6
vertices (order 30) avoid being an Erdos-Gyarfas counterexample, with the
minimum for a C4,C8-free lift being 44 candidates and all of them containing
a C16. No code/data was supplied for that exhaustive claim (12,075,358
representatives) -- this does NOT attempt to reproduce it exhaustively
(computationally infeasible in this session), but builds the lift
construction from scratch and samples a large number of random voltage
assignments on two concrete, easy-to-verify-correct simple base graphs
(K_{3,3} and the triangular prism, both loopless/multi-edge-free, matrix
#15 and #16 from the independently-verified 17-pseudograph enumeration) to
check the qualitative pattern holds and, more importantly, to see whether
any C4=C8=C16=0 lift turns up that their claim says cannot exist.
"""
import itertools
import random
import sys

sys.path.insert(0, "/home/user/erdos64/external_review/order32_direct_search")
from local_search import count_cycles, has_cycle, is_connected

SHEETS = 5

def spanning_tree_edges(base_edges, n):
    """Return (tree_edges, cotree_edges) via simple BFS spanning tree."""
    adj = {v: [] for v in range(n)}
    for idx, (u, v) in enumerate(base_edges):
        adj[u].append((v, idx))
        adj[v].append((u, idx))
    seen = {0}
    tree_idx = set()
    stack = [0]
    while stack:
        u = stack.pop()
        for v, idx in adj[u]:
            if v not in seen:
                seen.add(v)
                tree_idx.add(idx)
                stack.append(v)
    tree = [base_edges[i] for i in tree_idx]
    cotree = [base_edges[i] for i in range(len(base_edges)) if i not in tree_idx]
    return tree, cotree

def build_lift(base_edges, n_base, voltages):
    """voltages: dict edge-index -> permutation (tuple of length SHEETS),
    identity for tree edges (already assumed baked into `voltages`)."""
    N = n_base * SHEETS
    adj = [set() for _ in range(N)]
    def vid(v, s):
        return v * SHEETS + s
    for idx, (u, v) in enumerate(base_edges):
        g = voltages[idx]
        for s in range(SHEETS):
            a, b = vid(u, s), vid(v, g[s])
            adj[a].add(b)
            adj[b].add(a)
    return adj, N

def random_perm(rng):
    p = list(range(SHEETS))
    rng.shuffle(p)
    return tuple(p)

def base_edges_from_matrix(M, n):
    """Expand an edge-multiplicity matrix (loops on diagonal, contributing
    1 edge per unit since a loop of multiplicity m means m literal loop
    edges each visited by 2 half-edges) into an explicit edge list,
    keeping parallel/loop edges as separate indexed edges (needed since
    each gets its own independent voltage)."""
    edges = []
    for i in range(n):
        for _ in range(M[i][i]):
            edges.append((i, i))
    for i in range(n):
        for j in range(i + 1, n):
            for _ in range(M[i][j]):
                edges.append((i, j))
    return edges

def sample_base(name, base_edges, n_base, trials, rng, verbose_every=None):
    tree, cotree = spanning_tree_edges(base_edges, n_base)
    assert len(cotree) == 4, f"expected 4 cotree edges, got {len(cotree)}"
    all_edges = tree + cotree
    tree_n = len(tree)

    best = None
    c4c8_free = 0
    tested = 0
    exact_ctx = []
    for t in range(trials):
        voltages = {}
        for i in range(tree_n):
            voltages[i] = tuple(range(SHEETS))  # identity on tree (gauge fixed)
        for i in range(tree_n, len(all_edges)):
            voltages[i] = random_perm(rng)
        adj, N = build_lift(all_edges, n_base, voltages)
        degs = [len(s) for s in adj]
        if not all(d == 3 for d in degs):
            continue  # not simple (e.g. loop landed on a fixed sheet)
        if not is_connected(adj, N):
            continue
        tested += 1
        if has_cycle(adj, N, 4):
            continue
        if has_cycle(adj, N, 8):
            continue
        c4c8_free += 1
        c16 = count_cycles(adj, N, 16)
        if best is None or c16 < best:
            best = c16
        if c16 == 0:
            exact_ctx.append(voltages)
    print(f"{name}: trials={trials} simple_connected_tested={tested} "
          f"C4C8_free={c4c8_free} best_C16={best} EXACT_COUNTEREXAMPLES={len(exact_ctx)}")
    return exact_ctx

def main():
    rng = random.Random(42)
    # matrix #16 (loopless, multi-edge-free) from the independently-verified
    # 17-pseudograph enumeration: the triangular-prism-like graph
    prism_matrix = [
        [0, 0, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 0, 0],
        [1, 1, 1, 0, 0, 0],
    ]
    # matrix #15: K_{3,3}
    k33_matrix = [
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
    ]
    for name, M in (("prism(#16)", prism_matrix), ("K33(#15)", k33_matrix)):
        edges = base_edges_from_matrix(M, 6)
        assert len(edges) == 9
        found = sample_base(name, edges, 6, 200000, rng)
        if found:
            print(f"  !!! FOUND {len(found)} candidate(s) for {name}: {found[:3]}")

if __name__ == "__main__":
    sys.exit(main())
