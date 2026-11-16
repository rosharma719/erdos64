"""Check the truncation formula on the four 24-vertex extremal graphs:
cycle lengths of G = {3} ∪ { l + s : C a cycle of the triangle-quotient Q, l=|C|, t=|C ∩ truncated|, t <= s <= 2t }."""
import os, json, itertools, collections
import networkx as nx
edges = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "extremal24_edges.json")))
def cycles(G):
    adj = {v: set(G[v]) for v in G}; idx = {v: i for i, v in enumerate(G)}; out = []
    def dfs(s, v, path, vis):
        for w in adj[v]:
            if w == s and len(path) >= 3 and idx[path[1]] < idx[path[-1]]: out.append(tuple(path))
            elif idx[w] > idx[s] and w not in vis:
                vis.add(w); path.append(w); dfs(s, w, path, vis); path.pop(); vis.discard(w)
    for s in G: dfs(s, s, [s], {s})
    return out
for name, E in edges.items():
    G = nx.Graph(E)
    tris = [frozenset(c) for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    rep = {v: ("T", i) for i, t in enumerate(tris) for v in t}
    Q = nx.Graph((rep.get(u, u), rep.get(v, v)) for u, v in G.edges() if rep.get(u, u) != rep.get(v, v))
    actual = {len(c) for c in cycles(G)}
    pred = {3}
    worst = collections.Counter()
    for c in cycles(Q):
        l = len(c); t = sum(1 for x in c if isinstance(x, tuple))
        pred |= set(range(l + t, l + 2 * t + 1))
        for p in (4, 8, 16):
            if l + t <= p <= l + 2 * t: worst[p] += 1
    print(f"{name}: formula matches actual spectrum: {pred == actual}; quotient cycles whose window contains 4/8/16: {dict(worst)}")
    # how do quotient cycles dodge 8?  list (l, t) pairs with l <= 8
    pairs = collections.Counter((len(c), sum(1 for x in c if isinstance(x, tuple))) for c in cycles(Q) if len(c) <= 8)
    print("   (length, truncated count) of quotient cycles up to length 8:", sorted(pairs.items()))
