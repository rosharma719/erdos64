#!/usr/bin/env python3
"""
Theoretical (non-iterative) counterexample search: instead of local search
or brute enumeration, construct specific, well-understood ALGEBRAIC/
COMBINATORIAL graph families by formula and check each named candidate
exactly for min-degree-3 and absence of any power-of-2 cycle. No
optimization, no annealing, no random moves -- each graph is a deterministic
function of a small integer parameter, motivated by known structure
(generalized Petersen graphs, circulants), and there are only a handful of
parameter choices to check per family, checked exactly.

Cycle counting reused from external_review/order32_direct_search/local_search.py
(already validated against the Petersen graph's known exact cycle counts).
"""
import sys
sys.path.insert(0, "/home/user/erdos64/external_review/order32_direct_search")
from local_search import count_cycles, has_cycle, is_connected

def girth(adj, n):
    for L in range(3, n + 1):
        if has_cycle(adj, n, L):
            return L
    return None

def check(adj, n, name):
    degs = sorted(len(s) for s in adj)
    ok_deg = all(d == 3 for d in degs)
    conn = is_connected(adj, n)
    g = girth(adj, n) if conn and ok_deg else None
    c4 = count_cycles(adj, n, 4) if conn and ok_deg else None
    c8 = count_cycles(adj, n, 8) if conn and ok_deg else None
    c16 = count_cycles(adj, n, 16) if conn and ok_deg else None
    is_ctx = ok_deg and conn and c4 == 0 and c8 == 0 and c16 == 0
    print(f"{name:30s} n={n:3d} cubic={ok_deg} conn={conn} girth={g} "
          f"C4={c4} C8={c8} C16={c16}  COUNTEREXAMPLE={is_ctx}")
    return is_ctx

def gen_petersen(n, k):
    """GP(n,k): outer cycle u_0..u_{n-1}, inner u_i->v_i, v_i-v_{i+k}."""
    N = 2 * n
    adj = [set() for _ in range(N)]
    def add(a, b):
        adj[a].add(b); adj[b].add(a)
    for i in range(n):
        add(i, (i + 1) % n)              # outer cycle
        add(i, n + i)                    # spoke
        add(n + i, n + (i + k) % n)      # inner star polygon, step k
    return adj, N

def gen_circulant(n, conns):
    """Circulant graph on Z_n with connection set conns (each c gives edges
    i <-> i+c mod n; include n/2 for a self-paired antipodal connection)."""
    adj = [set() for _ in range(n)]
    for i in range(n):
        for c in conns:
            j = (i + c) % n
            if j != i:
                adj[i].add(j); adj[j].add(i)
    return adj, n

def gen_igraph(n, j, k):
    """I(n,j,k): generalizes GP(n,k)=I(n,1,k) with a non-trivial outer step j
    too (outer u_i-u_{i+j}, inner v_i-v_{i+k}, spokes u_i-v_i)."""
    N = 2 * n
    adj = [set() for _ in range(N)]
    def add(a, b):
        adj[a].add(b); adj[b].add(a)
    for i in range(n):
        add(i, (i + j) % n)
        add(i, n + i)
        add(n + i, n + (i + k) % n)
    return adj, N

def main():
    found = []
    print("=== Generalized Petersen graphs GP(15,k), order 30 ===")
    for k in range(1, 8):  # k and 15-k give isomorphic graphs; 1..7 covers all
        adj, n = gen_petersen(15, k)
        if check(adj, n, f"GP(15,{k})"):
            found.append(f"GP(15,{k})")

    print()
    print("=== Cubic circulants C_30(a, 15), order 30 (antipodal + distance a) ===")
    for a in range(1, 15):
        adj, n = gen_circulant(30, {a, 15})
        if check(adj, n, f"C_30({a},15)"):
            found.append(f"C_30({a},15)")

    print()
    print("=== Cubic circulants C_30(a,b,c) with 3 distinct non-antipodal pairs")
    print("    (only possible if one of a,b,c is self-paired, i.e., =15; already")
    print("    covered above -- otherwise 3 paired distances give degree 6, not 3)")

    print()
    print("=== I-graphs I(15,j,k), order 30 (outer step j != 1 too) ===")
    for j in (2, 3, 4):
        for k in range(1, 8):
            if k == j:
                continue
            adj, n = gen_igraph(15, j, k)
            if check(adj, n, f"I(15,{j},{k})"):
                found.append(f"I(15,{j},{k})")

    print()
    print("FOUND COUNTEREXAMPLES:", found if found else "NONE")

if __name__ == "__main__":
    sys.exit(main())
