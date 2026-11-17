#!/usr/bin/env python3
"""Independent check of the displayed 8-vertex representatives.

Uses NetworkX undirected graph traversal and DFS, NOT masks or the generation
logic from bounds_audit. All possible degree-2 attachments are checked.
"""
from itertools import combinations
import json
import networkx as nx

p='/mnt/data/eg_run7_work/eight_vertex_certificate.json'
J=json.load(open(p))

def has_exact_cycle(G,length):
    # Start at the lexicographically smallest node of the cycle, then DFS.
    for start in sorted(G):
        def dfs(path,used):
            if len(path)==length:
                return G.has_edge(path[-1],start)
            for v in G.neighbors(path[-1]):
                if v>start and v not in used:
                    if dfs(path+[v],used|{v}):return True
            return False
        if dfs([start],{start}):return True
    return False

for e in J['max_edge_examples']:
    G=nx.Graph();G.add_nodes_from(range(8));G.add_edges_from(e['edges'])
    assert G.number_of_edges()==11
    assert max(nx.core_number(G).values())<=2
    assert not has_exact_cycle(G,4) and not has_exact_cycle(G,8)
    for u,v in combinations(range(8),2):
        H=G.copy();H.add_node(8);H.add_edges_from([(8,u),(8,v)])
        assert has_exact_cycle(H,4) or has_exact_cycle(H,8)
    print('VERIFIED',e['graph6'],'n=8 m=11; all 28 new two-neighbor attachments create C4 or C8')
assert not nx.is_isomorphic(nx.from_graph6_bytes(J['max_edge_examples'][0]['graph6'].encode()),
                             nx.from_graph6_bytes(J['max_edge_examples'][1]['graph6'].encode()))
print('Independently checked: two non-isomorphic extremal candidates.')
