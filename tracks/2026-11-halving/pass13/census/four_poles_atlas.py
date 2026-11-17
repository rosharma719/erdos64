#!/usr/bin/env python3
"""Independent order-6 clean 4-pole census from NetworkX graph atlas.
No nauty, no imported project graph enumeration or cycle checker.
"""
import itertools
import math
import networkx as nx

n = 6
edges = list(itertools.combinations(range(n), 2))
def canmask(g):
    best = (1 << len(edges))-1
    for p in itertools.permutations(range(n)):
        mapping = {i:p[i] for i in range(n)}
        gg = nx.relabel_nodes(g, mapping)
        mask = sum((1 << j) for j, (a,b) in enumerate(edges) if gg.has_edge(a,b))
        if mask < best: best = mask
    return best

def aut_count(g):
    return sum(all(g.has_edge(a,b)==g.has_edge(p[a],p[b])
                   for a,b in edges) for p in itertools.permutations(range(n)))

rows = []
for g in nx.graph_atlas_g():
    if len(g)!=n or not nx.is_connected(g): continue
    if sorted(dict(g.degree()).values()) != [2,2,2,2,3,3]: continue
    cycles = {len(c) for c in nx.simple_cycles(nx.DiGraph(g)) if len(c)>=3}
    if any(x in cycles for x in (4,8,16)): continue
    k=canmask(g)
    rows.append((k, math.factorial(n)//aut_count(g), len(list(nx.bridges(g))), sorted(cycles)))
for mask, labeled, bridges, cycles in sorted(rows):
    print(f'{mask:04x}\t{labeled}\t{bridges}\t{",".join(map(str,cycles))}')
