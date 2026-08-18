#!/usr/bin/env python3
"""
Girth-6 kernel closure attempt, case (s=0, a=0): no antipodal x_i chords, no
doubled-attachment kernel vertices. Degree sequence 2^12 3^6 -- 6 hub
(internal-degree-3) vertices, 12 single-boundary-attachment (internal-
degree-2) vertices, |E(H)|=21.

The 6 hubs, viewed with internal edges only (ignoring the 12 boundary
attachments), form a connected cubic PSEUDOGRAPH on 6 vertices (loops and
multi-edges allowed, since a hub-to-hub "edge" is really a suppressed path
of some length, and a loop is a path that leaves and returns to the same
hub). This is exactly the same object independently enumerated and verified
in tracks/external-audits/s5_lift_check/enumerate_pseudographs.py (17 of them) --
reused directly here rather than re-derived, since it was already proven
correct there (own from-scratch backtracking enumeration, degree+
connectivity+canonical-form verified).

Method (same discipline as girth-7's verify_skeletons.py): build the actual
skeleton graph (6 hubs + up to 12 path-internal vertices) for a given
topology and a given assignment of path lengths to its abstract edges/loops,
enumerate all H-internal simple path lengths between any two boundary
positions by brute-force DFS (no distance formula to get wrong), then run
an exact backtracking search over all ways to assign the 6 boundary labels
(2 slots each of 12 positions) avoiding any cycle length in {4,8,16} or
below girth 6.
"""
import itertools
import sys

GIRTH = 6
FORBIDDEN = {4, 8, 16}
N_LABELS = 6  # 6-cycle boundary
N_POSITIONS = 12  # single-attachment kernel vertices for s=0,a=0

def cycle_lengths_ok(ell, d):
    """d=0: same label, spine ell+2. d in {1,2,3}: distinct labels at
    cyclic distance d on a 6-cycle, spine ell+4 closed via arc d or 6-d."""
    if d == 0:
        L = ell + 2
        return L not in FORBIDDEN and L >= GIRTH
    for L in (ell + d + 4, ell + (6 - d) + 4):
        if L in FORBIDDEN or L < GIRTH:
            return False
    return True

def all_simple_path_lengths(adj, u, v):
    lengths = set()
    def dfs(cur, visited, dist):
        if cur == v:
            lengths.add(dist)
            return
        for nxt in adj[cur]:
            if nxt not in visited:
                visited.add(nxt)
                dfs(nxt, visited, dist + 1)
                visited.remove(nxt)
    dfs(u, {u}, 0)
    return lengths

def skeleton_degrees_ok(matrix, adj):
    """Post-build validation: every hub must have degree exactly 3 in the
    built skeleton, and every path-internal position exactly 2. Catches
    the case where two parallel abstract edges/loops between the same hub
    pair both get length 0 and silently collapse into one set-membership
    edge (found by hand-tracing a spurious 'feasible' result on topology
    #12: two length-0 copies of the (0,5) edge collapsed, leaving hub 0
    and hub 5 at degree 2 instead of 3 -- an invalid, non-cubic graph that
    must never be accepted as a real candidate)."""
    for i in range(6):
        if len(adj[f"H{i}"]) != 3:
            return False
    for node, nbrs in adj.items():
        if not (isinstance(node, str) and node.startswith("H")):
            if len(nbrs) != 2:
                return False
    return True

def build_skeleton(matrix, lengths):
    """matrix: 6x6 edge-multiplicity matrix (diagonal=loops). lengths: dict
    mapping each concrete abstract edge instance (i,j,copy_idx) or loop
    (i,i,copy_idx) to its path length (# internal vertices, >=0 for a plain
    edge, >=1 for a loop since a 0-length loop would be a literal self-loop).
    Returns (adjacency dict over hub ids 'H0'..'H5' and path-position tuples,
    list of the path-internal positions in a fixed order)."""
    adj = {f"H{i}": set() for i in range(6)}
    positions = []
    def add(a, b):
        adj[a].add(b); adj[b].add(a)
    for i in range(6):
        for c in range(matrix[i][i]):
            L = lengths[("loop", i, c)]
            assert L >= 1
            prev = f"H{i}"
            for k in range(L):
                node = ("loop", i, c, k)
                adj[node] = set()
                positions.append(node)
                add(prev, node)
                prev = node
            add(prev, f"H{i}")
    for i in range(6):
        for j in range(i + 1, 6):
            for c in range(matrix[i][j]):
                L = lengths[("edge", i, j, c)]
                prev = f"H{i}"
                for k in range(L):
                    node = ("edge", i, j, c, k)
                    adj[node] = set()
                    positions.append(node)
                    add(prev, node)
                    prev = node
                add(prev, f"H{j}")
    return adj, positions

def abstract_edges(matrix):
    """List the abstract edge/loop slots needing a length assignment."""
    slots = []
    for i in range(6):
        for c in range(matrix[i][i]):
            slots.append(("loop", i, c))
    for i in range(6):
        for j in range(i + 1, 6):
            for c in range(matrix[i][j]):
                slots.append(("edge", i, j, c))
    return slots

def cyclic_dist(i, j, m=N_LABELS):
    d = abs(i - j) % m
    return min(d, m - d)

def labeling_feasible(adj, positions):
    n = len(positions)
    if n != N_POSITIONS:
        return None  # shouldn't happen if lengths sum correctly
    pair_lengths = {}
    for a in range(n):
        for b in range(a + 1, n):
            pair_lengths[(a, b)] = all_simple_path_lengths(adj, positions[a], positions[b])
    label_of = [-1] * n
    label_count = [0] * N_LABELS

    def check(idx, lbl):
        for j in range(n):
            if j == idx or label_of[j] == -1:
                continue
            key = (min(idx, j), max(idx, j))
            d = cyclic_dist(lbl, label_of[j])
            for ell in pair_lengths[key]:
                if not cycle_lengths_ok(ell, d):
                    return False
        return True

    def backtrack(idx):
        if idx == n:
            return True
        for lbl in range(N_LABELS):
            if label_count[lbl] >= 2:
                continue
            if check(idx, lbl):
                label_of[idx] = lbl
                label_count[lbl] += 1
                if backtrack(idx + 1):
                    return True
                label_count[lbl] -= 1
                label_of[idx] = -1
        return False

    return backtrack(0)

def internal_only_ok(matrix, lengths):
    """Pre-filter: pure hub-to-hub or loop cycles that don't touch the
    boundary at all must also avoid {4,8,16} and stay >=6. A loop of path
    length L forms a cycle of length L+1. Two parallel edges (or edge+edge,
    or edge+loop-arm via a hub) between the same hub pair form a cycle
    whose length is the sum of their (length+1) each -- i.e. for two
    parallel abstract edges of lengths La, Lb between i,j: cycle length
    (La+1)+(Lb+1). Checked directly on the built skeleton via BFS distances
    between hubs through each specific edge, not assumed algebraically,
    to avoid the same class of formula bugs found in the girth-7 work."""
    adj, positions = build_skeleton(matrix, lengths)
    # loops: direct check
    for i in range(6):
        for c in range(matrix[i][i]):
            L = lengths[("loop", i, c)]
            cyc = L + 1
            if cyc in FORBIDDEN or cyc < GIRTH:
                return False
    # any two distinct abstract edges/loops incident to the same hub pair
    # (including a hub to itself via two different loops) can combine into
    # a cycle; rather than hand-enumerate, just check ALL cycles in the pure
    # hub+path skeleton (no boundary) directly up to a safe bound using the
    # already-built adjacency, since this graph is small.
    return not has_forbidden_cycle(adj, FORBIDDEN, GIRTH)

def has_forbidden_cycle(adj, forbidden_lengths, min_len, max_len=None):
    """Generic exact check over an arbitrary-hashable-node graph: does any
    simple cycle of a forbidden length, or shorter than min_len, exist?
    DFS-based, node-label-agnostic (the girth-7/girth-6 work elsewhere uses
    a bitmask version restricted to integer 0..n-1 labels; this graph's
    nodes are structured tuples, so a plain adjacency-set DFS is used
    instead -- small graphs here, exactness matters far more than speed)."""
    nodes = list(adj.keys())
    if max_len is None:
        max_len = max(forbidden_lengths | {min_len})
    for s in nodes:
        found = [False]
        def dfs(u, depth, visited):
            if found[0]:
                return
            if depth >= 3 and s in adj[u]:
                L = depth
                if L in forbidden_lengths or L < min_len:
                    found[0] = True
                    return
            if depth >= max_len:
                return
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    dfs(v, depth + 1, visited)
                    visited.remove(v)
                    if found[0]:
                        return
        dfs(s, 1, {s})
        if found[0]:
            return True
    return False

def main():
    pass

if __name__ == "__main__":
    sys.exit(main())
