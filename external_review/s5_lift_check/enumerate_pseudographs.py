#!/usr/bin/env python3
"""
Independent verification of the claimed "17 connected cubic pseudographs on
6 vertices (including loops and parallel edges)" -- brute-force enumeration
via backtracking over the edge-multiplicity matrix (upper triangle + diagonal
for loops), degree-3 constraint, dedup by canonical form (min over all 720
vertex permutations), then filter for connectivity. No external tool
dependency, so nothing to misconfigure.
"""
import itertools

N = 6

def degree(M, v):
    d = 2 * M[v][v]
    for u in range(N):
        if u != v:
            d += M[v][u]
    return d

def is_connected(M):
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in range(N):
            if v != u and M[u][v] > 0 and v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == N

def canonical(M):
    best = None
    for perm in itertools.permutations(range(N)):
        rep = tuple(
            M[perm[i]][perm[j]] if i != j else M[perm[i]][perm[i]]
            for i in range(N) for j in range(N) if i <= j
        )
        if best is None or rep < best:
            best = rep
    return best

def enumerate_all():
    pairs = [(i, j) for i in range(N) for j in range(i + 1, N)]
    loops = list(range(N))
    slots = pairs + [('loop', v) for v in loops]
    results = []

    def backtrack(idx, M):
        if idx == len(slots):
            if all(degree(M, v) == 3 for v in range(N)):
                results.append([row[:] for row in M])
            return
        remaining = len(slots) - idx
        slot = slots[idx]
        if isinstance(slot[0], str):
            v = slot[1]
            max_here = (3 - degree(M, v)) // 2
            for mult in range(0, max(0, max_here) + 1):
                M[v][v] += mult
                backtrack(idx + 1, M)
                M[v][v] -= mult
        else:
            u, v = slot
            max_here = min(3 - degree(M, u), 3 - degree(M, v))
            for mult in range(0, max(0, max_here) + 1):
                M[u][v] += mult
                M[v][u] += mult
                backtrack(idx + 1, M)
                M[u][v] -= mult
                M[v][u] -= mult

    M = [[0] * N for _ in range(N)]
    backtrack(0, M)
    return results

def main():
    all_matrices = enumerate_all()
    connected = [M for M in all_matrices if is_connected(M)]
    seen_canon = {}
    for M in connected:
        c = canonical(M)
        if c not in seen_canon:
            seen_canon[c] = M
    print(f"raw degree-3 matrices found: {len(all_matrices)}")
    print(f"connected: {len(connected)}")
    print(f"non-isomorphic connected cubic pseudographs on 6 vertices: {len(seen_canon)}")
    for i, M in enumerate(seen_canon.values()):
        has_loop = any(M[v][v] > 0 for v in range(N))
        has_multi = any(M[i][j] > 1 for i in range(N) for j in range(i + 1, N))
        print(f"  #{i}: loops={has_loop} multi-edges={has_multi} matrix={M}")

if __name__ == "__main__":
    main()
