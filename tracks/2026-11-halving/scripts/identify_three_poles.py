#!/usr/bin/env python3
# Usage: python3 identify_three_poles.py FILE.g6 ...  (prints port-pair path sets, internal cycle lengths, capped graph6)
import sys, itertools, networkx as nx
def paths(G, s, t):
    out = set(); stack = [(s, {s}, 0)]
    while stack:
        v, vis, L = stack.pop()
        if v == t: out.add(L); continue
        for w in G[v]:
            if w not in vis: stack.append((w, vis | {w}, L + 1))
    return sorted(out)
def show(L): return f"[{L[0]},{L[-1]}]" if L == list(range(L[0], L[-1] + 1)) else str(L)
def cycles(G):
    return sorted({len(c) for c in nx.simple_cycles(G.to_directed()) if len(c) >= 3})
for f in sys.argv[1:]:
    for line in open(f):
        G = nx.from_graph6_bytes(line.strip().encode())
        ports = [v for v in G if G.degree(v) == 2]
        sets = sorted(show(paths(G, a, b)) for a, b in itertools.combinations(ports, 2))
        H = G.copy(); H.add_edges_from(("cap", p) for p in ports)
        print(f"{line.strip()}: n={G.number_of_nodes()} port-pair paths={sets} internal cycles={cycles(G)} "
              f"capped g6={nx.to_graph6_bytes(nx.convert_node_labels_to_integers(H), header=False).decode().strip()}")
