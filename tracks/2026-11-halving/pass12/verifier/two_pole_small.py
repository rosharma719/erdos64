#!/usr/bin/env python3
"""Independent atlas-based exhaustive unlabelled two-pole check up to order 6."""
import networkx as nx
for n in (4,6):
    graphs=[g for g in nx.graph_atlas_g() if len(g)==n and nx.is_connected(g)
            and sorted(d for v,d in g.degree())==[2,2]+[3]*(n-2)]
    clean=[g for g in graphs if not {4,8}.intersection(len(c) for c in nx.simple_cycles(g) if len(c)>=3)]
    print(f'2POLE|{n}|{len(graphs)}|{len(clean)}')
