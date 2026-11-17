"""Construct a *selective, non-exhaustive* 28-vertex C4/C8-free test subset
by vertex-to-triangle expansions of known 24-vertex extremal graphs.
Every generated graph has a triangle and is outside the prime class.
"""
from pathlib import Path
import networkx as nx
from verify_g6 import find_cycle_dfs

HERE=Path(__file__).resolve().parent


def expand_triangle(G,v):
    g=G.copy()
    ngh=sorted(g[v])
    g.remove_node(v)
    top=max(g.nodes())+1
    tri=[top,top+1,top+2]
    g.add_edges_from([(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])])
    g.add_edges_from(zip(ngh,tri))
    return nx.convert_node_labels_to_integers(g,ordering='sorted')


def uniq(graphs):
    seen={}
    kept=[]
    for g in graphs:
        key=nx.weisfeiler_lehman_graph_hash(g,iterations=4)
        b=seen.setdefault(key,[])
        if any(nx.is_isomorphic(g,old) for old in b):
            continue
        b.append(g);kept.append(g)
    return kept


seed=[nx.from_graph6_bytes(line.encode()) for line in (HERE/'controls.g6').read_text().splitlines()][2:]
for n in (26,28):
    new=[]
    for g in seed:
        for v in g:
            gg=expand_triangle(g,v)
            if find_cycle_dfs(gg,4) is None and find_cycle_dfs(gg,8) is None:
                new.append(gg)
    seed=uniq(new)
    print('order',n,'expansion survivors before iso',len(new),'nonisomorphic',len(seed),flush=True)
    (HERE/f'triangle_expansion_n{n}.g6').write_text(''.join(nx.to_graph6_bytes(g,header=False).decode() for g in seed))
