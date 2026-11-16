import os, json, collections, itertools
import networkx as nx
edges = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "extremal24_edges.json")))
def spec(G):
    adj = {v: set(G[v]) for v in G}; cnt = collections.Counter()
    order = {v: i for i, v in enumerate(G)}
    def dfs(s, v, vis, L):
        for w in adj[v]:
            if w == s and L >= 3: cnt[L] += 1
            elif order[w] > order[s] and w not in vis:
                vis.add(w); dfs(s, w, vis, L + 1); vis.discard(w)
    for s in G: dfs(s, s, {s}, 1)
    return {L: c // 2 for L, c in sorted(cnt.items())}
P = nx.petersen_graph()
named = {"Petersen": P, "K4": nx.complete_graph(4), "K33": nx.complete_bipartite_graph(3,3),
         "prism": nx.circular_ladder_graph(3), "cube": nx.hypercube_graph(3), "Heawood": nx.heawood_graph(),
         "Franklin?": None, "Pappus": nx.pappus_graph(), "Mobius-Kantor": nx.moebius_kantor_graph(),
         "Tietze": nx.LCF_graph(12, [2, 6, -2], 4) if False else None, "Franklin": nx.LCF_graph(12, [5, -5], 6), "Frucht": nx.frucht_graph(), "truncated-tetrahedron": nx.truncated_tetrahedron_graph(), "Desargues": nx.desargues_graph(), "dodecahedron": nx.dodecahedral_graph()}
for name, E in edges.items():
    G = nx.Graph(E)
    tris = [frozenset(c) for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    rep = {}
    for i, t in enumerate(tris):
        for v in t: rep[v] = ("T", i)
    Q = nx.MultiGraph()
    for v in G: Q.add_node(rep.get(v, v))
    for u, v in G.edges():
        a, b = rep.get(u, u), rep.get(v, v)
        if a != b: Q.add_edge(a, b)
    simple = all(Q.number_of_edges(a, b) <= 1 for a, b in itertools.combinations(Q.nodes, 2))
    S = nx.Graph(Q)
    degs = sorted(dict(Q.degree()).values())
    ident = [k for k, H in named.items() if H is not None and H.number_of_nodes() == S.number_of_nodes() and nx.is_isomorphic(S, H)]
    tnodes = [x for x in S if isinstance(x, tuple)]
    unodes = [x for x in S if not isinstance(x, tuple)]
    print(f"== {name}: {len(tris)} triangles -> quotient on {S.number_of_nodes()} vertices, simple={simple}, "
          f"cubic={set(degs)=={3}}, bipartite={nx.is_bipartite(S)}, girth-spectrum={spec(S)}, known={ident}")
    print(f"   untruncated vertices: {len(unodes)}; do they form an independent set? "
          f"{S.subgraph(unodes).number_of_edges()==0}; pairwise distances among them: "
          f"{sorted(collections.Counter(nx.shortest_path_length(S,a,b) for a,b in itertools.combinations(unodes,2)).items())}")
    # second-level: triangles in the quotient?
    t2 = [c for c in nx.enumerate_all_cliques(S) if len(c) == 3]
    print(f"   triangles in the quotient: {len(t2)}; quotient aut order: ", end="")
    GM = nx.algorithms.isomorphism.GraphMatcher(S, S)
    print(sum(1 for _ in GM.isomorphisms_iter()))
