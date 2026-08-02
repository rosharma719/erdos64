"""
Cross-validation of the power-of-two cycle detector.

Checks:
  1. Two independent existence routines (DFS vs networkx) agree on every
     length L for many random graphs.
  2. Known graphs give known answers (K4, K33, Petersen, C_n, ...).
  3. Any cycle the DFS returns is a genuine simple cycle of the claimed length.
"""
import random
import sys
import networkx as nx
import cycle_detect as cd


def nx_to_g(G):
    return {v: set(G.neighbors(v)) for v in G.nodes()}


def verify_cycle(g, cyc, L):
    """Independently confirm cyc is a simple cycle of length L in g."""
    assert len(cyc) == L, f"length {len(cyc)} != {L}"
    assert len(set(cyc)) == L, "repeated vertex"
    for i in range(L):
        a, b = cyc[i], cyc[(i + 1) % L]
        assert b in g[a], f"non-edge {a}-{b}"
    return True


def test_known():
    # K4: has a 4-cycle
    g = cd.from_edges(4, [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)])
    assert cd.has_cycle_len_dfs(g, 4)
    assert cd.forbidden_cycle_witness(g)[0] == 4
    assert not cd.is_counterexample(g)

    # K_{3,3}: bipartite, has 4-cycles, min degree 3, NOT a counterexample
    E = [(i, 3+j) for i in range(3) for j in range(3)]
    g = cd.from_edges(6, E)
    assert cd.min_degree(g) == 3
    assert cd.has_cycle_len_dfs(g, 4)
    assert not cd.is_counterexample(g)

    # Petersen: girth 5 (no C4), cycle spectrum {5,6,8,9} -> HAS an 8-cycle.
    P = nx.petersen_graph()
    g = nx_to_g(P)
    assert cd.min_degree(g) == 3
    assert not cd.has_cycle_len_dfs(g, 4), "Petersen has no 4-cycle"
    assert cd.has_cycle_len_dfs(g, 8), "Petersen must have an 8-cycle"
    w = cd.forbidden_cycle_witness(g)
    assert w[0] == 8, f"Petersen smallest pow2 cycle should be 8, got {w}"
    verify_cycle(g, w[1], 8)
    assert not cd.is_counterexample(g)

    # C_8 (8-cycle graph): min degree 2, so not a valid instance, but has 8-cyc
    C8 = nx.cycle_graph(8)
    g = nx_to_g(C8)
    assert cd.has_cycle_len_dfs(g, 8)
    assert not cd.has_cycle_len_dfs(g, 4)
    assert cd.min_degree(g) == 2
    assert not cd.is_counterexample(g)  # min degree 2

    # C_7: 7-cycle, no power-of-two cycle at all, but min degree 2
    C7 = nx_to_g(nx.cycle_graph(7))
    assert cd.forbidden_cycle_witness(C7) is None
    assert not cd.is_counterexample(C7)  # excluded by min-degree
    print("known-graph tests: PASS")


def test_cross_random(trials=400, seed=12345):
    rng = random.Random(seed)
    disagreements = 0
    checked = 0
    for _ in range(trials):
        n = rng.randint(4, 11)
        p = rng.uniform(0.2, 0.8)
        G = nx.gnp_random_graph(n, p, seed=rng.randint(0, 10**9))
        g = nx_to_g(G)
        for L in range(3, n + 1):
            a = cd.has_cycle_len_dfs(g, L)
            b = cd.has_cycle_len_nx(g, L)
            checked += 1
            if a != b:
                disagreements += 1
                print(f"DISAGREE n={n} L={L} dfs={a} nx={b} edges={list(G.edges())}")
            if a:
                c = cd.find_cycle_len_dfs(g, L)
                verify_cycle(g, c, L)  # structural re-check of the witness
    print(f"cross-random: {checked} (graph,L) checks, {disagreements} disagreements")
    assert disagreements == 0
    print("cross-random tests: PASS")


if __name__ == "__main__":
    test_known()
    test_cross_random()
    print("ALL DETECTOR TESTS PASS")
