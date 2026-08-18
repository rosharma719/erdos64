#!/usr/bin/env python3
"""
Generalization of tracks/external-audits/s5_lift_check/enumerate_pseudographs.py
to an ARBITRARY target degree sequence (not just all-3), needed for the
girth-6 (s,a) sub-cases with a>0: the suppressed core there is a multigraph
on (6+2s+a) hubs of degree 3 plus 'a' leaves of degree 1, not a pure cubic
pseudograph.

Same method: backtracking over the edge-multiplicity matrix (upper
triangle + diagonal for loops), respecting each vertex's target degree,
dedup by canonical form (min over all permutations respecting which
vertices share a target degree -- i.e. only permute within same-degree
groups, since a degree-1 and degree-3 vertex can never be interchanged),
then filter for connectivity.
"""
import itertools

def degree(M, v):
    n = len(M)
    d = 2 * M[v][v]
    for u in range(n):
        if u != v:
            d += M[v][u]
    return d

def is_connected(M):
    n = len(M)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in range(n):
            if v != u and M[u][v] > 0 and v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n

def canonical(M, degseq):
    """Exact canonical form via brute permutation within same-degree groups.
    Fine for small n (used for the 6-vertex, all-degree-3 case: 6!=720).
    For larger/mixed cases, dedup_by_isomorphism below (networkx-based) is
    used instead -- this function is kept only for the small sanity-check
    path and cross-validation."""
    n = len(M)
    groups = {}
    for i, d in enumerate(degseq):
        groups.setdefault(d, []).append(i)
    group_perms = [list(itertools.permutations(idxs)) for idxs in groups.values()]
    group_slots = list(groups.values())
    best = None
    for combo in itertools.product(*group_perms):
        perm = [None] * n
        for slot, perm_vals in zip(group_slots, combo):
            for orig, new in zip(slot, perm_vals):
                perm[orig] = new
        rep = tuple(
            M[a][b] if a <= b else M[b][a]
            for i in range(n) for j in range(i, n)
            for a, b in [(perm[i], perm[j])]
        )
        if best is None or rep < best:
            best = rep
    return best

def to_networkx(M):
    """Simple (non-multi) graph with edge multiplicity encoded as a
    'weight' attribute (including self-loops), since networkx's
    Weisfeiler-Lehman hash does not support MultiGraph directly."""
    import networkx as nx
    n = len(M)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        if M[i][i] > 0:
            G.add_edge(i, i, weight=M[i][i])
    for i in range(n):
        for j in range(i + 1, n):
            if M[i][j] > 0:
                G.add_edge(i, j, weight=M[i][j])
    return G

def dedup_by_isomorphism(matrices):
    """Fast dedup for larger n: bucket by Weisfeiler-Lehman hash (cheap,
    near-perfect discriminator in practice) over the weighted simple-graph
    encoding, then confirm true isomorphism only within hash collision
    groups via networkx's exact VF2 check (respecting edge weights) --
    avoids the O(n!) brute permutation cost of `canonical` at this size."""
    import networkx as nx
    from networkx.algorithms.isomorphism import numerical_edge_match
    em = numerical_edge_match("weight", 1)
    buckets = {}
    for M in matrices:
        G = to_networkx(M)
        h = nx.weisfeiler_lehman_graph_hash(G, edge_attr="weight", iterations=4)
        buckets.setdefault(h, []).append((M, G))
    uniques = []
    for h, group in buckets.items():
        reps = []  # list of (M, G) representatives confirmed pairwise non-isomorphic
        for M, G in group:
            is_dup = False
            for repM, repG in reps:
                if nx.is_isomorphic(G, repG, edge_match=em):
                    is_dup = True
                    break
            if not is_dup:
                reps.append((M, G))
        uniques.extend(M for M, G in reps)
    return uniques

def enumerate_degseq(degseq):
    n = len(degseq)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    slots = pairs + [('loop', v) for v in range(n)]
    # remaining_capacity[idx][v] = max additional degree v could still gain
    # from slots[idx:] (2 per loop, 1 per incident pair) -- used for forward
    # checking so a branch that can no longer reach a vertex's target degree
    # is pruned immediately instead of only failing at the end.
    n_slots = len(slots)
    remaining_capacity = [[0] * n for _ in range(n_slots + 1)]
    for idx in range(n_slots - 1, -1, -1):
        remaining_capacity[idx] = remaining_capacity[idx + 1][:]
        slot = slots[idx]
        if isinstance(slot[0], str):
            remaining_capacity[idx][slot[1]] += 2
        else:
            u, v = slot
            remaining_capacity[idx][u] += 1
            remaining_capacity[idx][v] += 1

    results = []

    def backtrack(idx, M, deg):
        if idx == len(slots):
            results.append([row[:] for row in M])
            return
        slot = slots[idx]
        if isinstance(slot[0], str):
            v = slot[1]
            max_here = (degseq[v] - deg[v]) // 2
            for mult in range(0, max(0, max_here) + 1):
                new_deg_v = deg[v] + 2 * mult
                if new_deg_v + remaining_capacity[idx + 1][v] < degseq[v]:
                    continue
                M[v][v] += mult
                deg[v] = new_deg_v
                backtrack(idx + 1, M, deg)
                deg[v] -= 2 * mult
                M[v][v] -= mult
        else:
            u, v = slot
            max_here = min(degseq[u] - deg[u], degseq[v] - deg[v])
            for mult in range(0, max(0, max_here) + 1):
                new_deg_u, new_deg_v = deg[u] + mult, deg[v] + mult
                if (new_deg_u + remaining_capacity[idx + 1][u] < degseq[u] or
                        new_deg_v + remaining_capacity[idx + 1][v] < degseq[v]):
                    continue
                M[u][v] += mult
                M[v][u] += mult
                deg[u], deg[v] = new_deg_u, new_deg_v
                backtrack(idx + 1, M, deg)
                deg[u] -= mult
                deg[v] -= mult
                M[u][v] -= mult
                M[v][u] -= mult

    M = [[0] * n for _ in range(n)]
    backtrack(0, M, [0] * n)
    connected = [M for M in results if is_connected(M)]
    return dedup_by_isomorphism(connected)

def main():
    # sanity check: reproduce the already-verified 17 cubic pseudographs on
    # 6 vertices via this generalized code before trusting it on anything new
    result = enumerate_degseq([3, 3, 3, 3, 3, 3])
    print(f"sanity check, degseq [3]*6: got {len(result)} (expect 17)")
    assert len(result) == 17, "generalized enumerator disagrees with the already-verified cubic-only one!"
    print("PASSED")

if __name__ == "__main__":
    main()
