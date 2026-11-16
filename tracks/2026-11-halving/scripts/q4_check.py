"""Independent check of the q(G) >= 4 claim, written for this audit.

Setting (all facts used are hand-checked in the audit notes):
  G minimal counterexample, C = degree-3 vertices, H = degree>=4 vertices (h=|H|),
  F = G[C], C_i = {v in C : deg_F(v) = i}.  Every C2 vertex has exactly one hub.
  C4-freeness => a C2 vertex has at most one F-neighbour attached to each hub.
We bound how many C2 vertices a component of F[C2] can have when G has no C4, C8.
A component of F[C2] is a path or a cycle; colour each vertex by its hub.
"""
import itertools, sys

def has_cycle_len(adj, L):
    n = len(adj)
    def dfs(start, v, vis, depth):
        if depth == L - 1:
            return start in adj[v]
        for w in adj[v]:
            if w > start and not (vis >> w) & 1:
                if dfs(start, w, vis | (1 << w), depth + 1):
                    return True
        return False
    return any(dfs(s, s, 1 << s, 0) for s in range(n))

def build(words_cyclic, h):
    """words_cyclic: list of (word, is_cycle). Hubs are vertices 0..h-1."""
    adj = [set() for _ in range(h)]
    for word, cyc in words_cyclic:
        base = len(adj)
        for i, c in enumerate(word):
            adj.append(set())
            v = base + i
            adj[v].add(c); adj[c].add(v)
            if i:
                adj[v].add(v - 1); adj[v - 1].add(v)
        if cyc:
            a, b = base, base + len(word) - 1
            adj[a].add(b); adj[b].add(a)
    return adj

def clean(words_cyclic, h):
    adj = build(words_cyclic, h)
    return not has_cycle_len(adj, 4) and not has_cycle_len(adj, 8)

for h in (1, 2, 3):
    # longest clean path words, by extension (cleanness is hereditary to prefixes)
    level = [(c,) for c in range(h)]
    t = 1
    while True:
        nxt = [w + (c,) for w in level for c in range(h) if clean([(w + (c,), False)], h)]
        if not nxt:
            break
        level = nxt; t += 1
    tmax = t
    # clean cyclic words: length must be <= tmax+1, else it contains a path word of tmax+1 vertices
    cyc = []
    for L in range(3, tmax + 2):
        for w in itertools.product(range(h), repeat=L):
            if min(w[i:] + w[:i] for i in range(L)) != w:
                continue  # one representative per rotation
            if clean([(w, True)], h):
                cyc.append(w)
    # pairs of clean cyclic components that are jointly clean
    pairs = [(a, b) for a, b in itertools.combinations_with_replacement(cyc, 2)
             if clean([(a, True), (b, True)], h)]
    print(f"h={h}: longest clean path = {tmax} vertices; clean cyclic words = {cyc}; "
          f"jointly clean pairs = {pairs}")
    sys.stdout.flush()
