#!/usr/bin/env python3
"""Classify clean 4-poles: bridge-joined pairs of T-list poles, or something else.
Usage: python3 classify_four_poles.py FILE.g6 ...   (graph6 of clean 4-poles)"""
import sys, os, itertools, collections
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__))
L = {name: nx.from_graph6_bytes(s.encode()) for name, s in
     [("U", "FCptO"), ("S", "FCZTO"), ("H", "N?AA@AODAOP_KGGoGH?")]}
L["T"] = nx.complete_graph(3)
def lname(G):
    for n, H in L.items():
        if G.number_of_nodes() == H.number_of_nodes() and nx.is_isomorphic(G, H): return n
    return None
def cyc(G): return sorted({len(c) for c in nx.simple_cycles(G.to_directed()) if len(c) >= 3})
def clean(G): return not any(l >= 4 and l & (l - 1) == 0 for l in cyc(G))
def suppress(G, x):
    a, b = list(G[x])
    if G.has_edge(a, b): return None
    H = G.copy(); H.remove_node(x); H.add_edge(a, b); return H
rows = []
for f in sys.argv[1:]:
    for line in open(f):
        g6 = line.strip()
        if not g6: continue
        G = nx.from_graph6_bytes(g6.encode()); n = G.number_of_nodes()
        bridges = list(nx.bridges(G))
        kind = None
        if bridges:
            parts = []
            for u, v in bridges:
                H = G.copy(); H.remove_edge(u, v)
                comps = [H.subgraph(c).copy() for c in nx.connected_components(H)]
                parts.append(sorted(str(lname(c)) + f"({c.number_of_nodes()})" for c in comps))
            kind = "bridge: " + " | ".join("+".join(p) for p in parts)
        else:
            sup = []
            for x in [v for v in G if G.degree(v) == 2]:
                H = suppress(G, x)
                if H is not None and clean(H) and lname(H): sup.append(lname(H))
            conn = nx.node_connectivity(G)
            kind = f"2-connected (kappa={conn}); suppressing a port gives clean " + (",".join(sorted(set(sup))) if sup else "nothing in L")
        rows.append((n, kind, cyc(G), g6))
by = collections.Counter((n, k) for n, k, _, _ in rows)
for (n, k), c in sorted(by.items()):
    print(f"N={n:2d}  x{c}  {k}")
print("\nexamples of non-bridge ones:")
seen = set()
for n, k, cy, g6 in rows:
    if not k.startswith("bridge") and (n, k) not in seen:
        seen.add((n, k)); print(f"  N={n} {g6} cycles={cy}")
