import json, itertools, collections, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
import networkx as nx
from networkx.algorithms import isomorphism
m = json.load(open(os.path.join(ROOT, "manifests", "z3_bases_manifest.json")))
def from_g6(s): return nx.from_graph6_bytes(s.encode())
def cycles_by_len(G):
    n = G.number_of_nodes(); adj = {v: set(G[v]) for v in G}
    cnt = collections.Counter()
    def dfs(s, v, vis, L):
        for w in adj[v]:
            if w == s and L >= 3: cnt[L] += 1
            elif w > s and w not in vis:
                vis.add(w); dfs(s, w, vis, L + 1); vis.discard(w)
    for s in G: dfs(s, s, {s}, 1)
    return {L: c // 2 for L, c in sorted(cnt.items())}
P = nx.petersen_graph()
out = {}
for b in m["bases"]:
    G = from_g6(b["graph6"]); name = b["name"]
    spec = cycles_by_len(G)
    tri = [c for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    tri_vertices = set(v for t in tri for v in t)
    # nontrivial 3-edge cuts (both sides >= 2 vertices... require each side to contain a cycle: >=3 vertices)
    cuts = []
    E = list(G.edges())
    for trip in itertools.combinations(E, 3):
        H = G.copy(); H.remove_edges_from(trip)
        comps = list(nx.connected_components(H))
        if len(comps) == 2 and min(len(c) for c in comps) >= 4:
            cuts.append((trip, sorted(len(c) for c in comps)))
    print(f"== {name}: bipartite={nx.is_bipartite(G)} planar={nx.check_planarity(G)[0]} "
          f"girth={min(spec)} aut={b['automorphism_group_order']} diam={nx.diameter(G)}")
    print("   cycle counts by length:", spec)
    print("   missing lengths in 3..24:", [L for L in range(3, 25) if L not in spec])
    print(f"   triangles={len(tri)} disjoint={len(tri_vertices)==3*len(tri)} ; 3-edge-cuts with both sides >=4: {len(cuts)}",
          collections.Counter(tuple(s) for _, s in cuts))
    out[name] = G
json.dump({k: sorted(map(sorted, G.edges())) for k, G in out.items()}, open(os.path.join(HERE, "extremal24_edges.json"), "w"))
