"""Independent check of rooted.c witnesses: each witness must be a simple cycle
of the stated power-of-two length in the graph, and the union of 'avoided'
sets over a graph's witnesses must be all vertices."""
import sys, networkx as nx
def load_g6(path): return [nx.from_graph6_bytes(l.strip().encode()) for l in open(path) if l.strip()]
def load_el(path):
    g = nx.Graph(); g.add_edges_from(tuple(map(int, l.split())) for l in open(path) if l.strip()); return [g]
mode, gpath, wpath = sys.argv[1:4]
gs = load_g6(gpath) if mode == 'g6' else load_el(gpath)
avoid = {i: set() for i in range(len(gs))}
nw = 0
for line in open(wpath):
    if not line.startswith('W '): continue
    _, gi, r, L, *cyc = line.split(); gi, r, L = int(gi) - 1, int(r), int(L); cyc = list(map(int, cyc))
    g = gs[gi]
    assert len(cyc) == L and len(set(cyc)) == L and L & (L - 1) == 0 and L >= 4
    assert all(g.has_edge(cyc[i], cyc[(i + 1) % L]) for i in range(L))
    assert r not in cyc
    avoid[gi] |= set(g) - set(cyc); nw += 1
for i, g in enumerate(gs):
    assert all(d == 3 for _, d in g.degree()), ('not cubic', i)
    assert avoid[i] == set(g), ('uncovered roots', i, len(set(g) - avoid[i]))
print(f'OK: {len(gs)} cubic graphs, {nw} witness cycles, every vertex avoided by a verified dyadic cycle')
