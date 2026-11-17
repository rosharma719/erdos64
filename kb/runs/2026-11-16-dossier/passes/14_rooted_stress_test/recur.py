"""Recursive gadget family test.
A piece P is (graph, (t1,t2,t3)) where t_i are the three terminals (each has
exactly one missing edge).  G(P, wiring) = K4 on {u, w, X, Y} with X, Y replaced
by copies of P: terminals of each copy are joined to u, w and the other copy
according to the permutation `wiring`.  P_next = G - c for a root-critical
vertex c, terminals = N(c).  Writes candidate graphs and checks criticality with
the external C checker (exhaustive), reporting critical vertices.
"""
import itertools, subprocess, sys, networkx as nx

CHECK = sys.argv[1]; MAXN = int(sys.argv[2])

def build(P, perm1, perm2):
    g0, term = P
    G = nx.Graph(); G.add_edge('u', 'w')
    copies = []
    for tag, perm in (('X', perm1), ('Y', perm2)):
        m = {v: (tag, v) for v in g0}
        G.add_edges_from((m[a], m[b]) for a, b in g0.edges())
        t = [m[term[i]] for i in perm]
        copies.append(t)
    (x1, x2, x3), (y1, y2, y3) = copies
    G.add_edges_from([('u', x1), ('u', y1), ('w', x2), ('w', y2), (x3, y3)])
    return nx.convert_node_labels_to_integers(G, label_attribute='orig')

def critical(G):
    s = nx.to_graph6_bytes(G, header=False)
    out = subprocess.run([CHECK, '2'], input=s, capture_output=True).stdout.decode()
    return [int(l.split()[-1]) for l in out.splitlines() if 'ROOT-CRITICAL' in l]

tri = (nx.complete_graph(3), (0, 1, 2))
level = [tri]
seen = []
while True:
    nxt = []
    for P in level:
        for p1 in itertools.permutations(range(3)):
            for p2 in itertools.permutations(range(3)):
                G = build(P, p1, p2)
                if len(G) > MAXN: continue
                if any(nx.is_isomorphic(G, H) for H in seen): continue
                seen.append(G)
                assert all(d == 3 for _, d in G.degree()) and nx.node_connectivity(G) == 3
                crit = critical(G)
                print(f"n={len(G)} wiring={p1},{p2} critical={crit} g6={nx.to_graph6_bytes(G, header=False).decode().strip()}", flush=True)
                for c in crit:
                    h = G.copy(); nb = list(h[c]); h.remove_node(c)
                    nxt.append((h, tuple(nb)))
    if not nxt: break
    # dedupe pieces by isomorphism of the piece with terminals marked
    uniq = []
    for h, t in nxt:
        hh = h.copy(); nx.set_node_attributes(hh, {v: (v in t) for v in hh}, 'term')
        if not any(nx.is_isomorphic(hh, o, node_match=lambda a, b: a['term'] == b['term']) for o, _ in uniq):
            uniq.append((hh, (h, t)))
    level = [p for _, p in uniq]
    print('next level pieces:', len(level), 'piece order', len(level[0][0]), flush=True)
