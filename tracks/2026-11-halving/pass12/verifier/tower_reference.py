#!/usr/bin/env python3
"""Standalone NetworkX graph-level oracle for pass-XII triangle-tower certificates.

No dependency on the shared gadget solver. Identity has 3 stubs at one vertex.
Usage: python tower_reference.py --generate graphs.txt --output output.txt
"""
import argparse
import itertools
from pathlib import Path
import networkx as nx

class Pole:
    def __init__(self, graph, ports):
        self.graph = graph
        self.ports = tuple(ports)

def compose(parts):
    g = nx.Graph(); port_map = []
    for p in parts:
        start = len(g)
        m = {v: start+i for i,v in enumerate(sorted(p.graph))}
        g.add_nodes_from(m.values())
        g.add_edges_from((m[u],m[v]) for u,v in p.graph.edges())
        port_map.append(tuple(m[v] for v in p.ports))
    for i in range(3):
        g.add_edge(port_map[i][2],port_map[(i+1)%3][1])
    return Pole(g,tuple(pp[0] for pp in port_map))

def examples():
    ident=Pole(nx.empty_graph(1),(0,0,0))
    tri=compose((ident,ident,ident))
    p5=compose((ident,ident,tri))
    skew=compose((ident,tri,tri))
    p9=compose((ident,ident,skew))
    h15=compose((ident,skew,skew))
    uniform_graph=nx.from_graph6_bytes(b'FOpso')
    uniform_ports=tuple(sorted(v for v,d in uniform_graph.degree() if d==2))
    assert len(uniform_ports)==3
    uniform=Pole(uniform_graph,uniform_ports)
    return dict(I=ident,T=tri,P5=p5,S=skew,P9=p9,H=h15,U=uniform)

def graph_records(out):
    data=examples()
    with open(out,'w') as f:
        for name,p in data.items():
            edges=sorted(tuple(sorted(e)) for e in p.graph.edges())
            fields=[name,len(p.graph),*p.ports,len(edges)]
            fields+=list(itertools.chain.from_iterable(edges))
            f.write(' '.join(str(x) for x in fields)+'\n')
    return data

def graph_stream(records):
    for name,p in records.items():
        g=p.graph;n=len(g)
        cycles=sorted({len(c) for c in nx.simple_cycles(g) if len(c)>=3})
        paths=[]
        for a,b in ((0,1),(0,2),(1,2)):
            paths.append(sorted({len(q)-1 for q in nx.all_simple_paths(g,p.ports[a],p.ports[b])}))
        print('TYPE|'+name+'|'+str(n)+'|'+','.join(map(str,cycles))+'|'+'|'.join(','.join(map(str,v)) for v in paths))

TYPES={'I':(1,(0,)),'T':(3,(1,)),'S':(7,(2,3)),'H':(15,(3,5))}

def case_stream():
    for kinds in itertools.combinations_with_replacement(TYPES,3):
        N=sum(TYPES[k][0] for k in kinds)
        options=list(itertools.product(*(TYPES[k][1] for k in kinds)))
        admissible=[a for a in options if not any(3+sum(a)<=q<=N for q in (4,8,16,32,64))]
        label=''.join(kinds)
        if admissible:
            options_str=';'.join(','.join(map(str,a)) for a in admissible)
        else: options_str='-'
        print(f'CASE|{label}|{N}|{options_str}')
    all_types={'I':(1,(0,)),'T':(3,(1,)),'S':(7,(2,3)),'U':(7,(2,)),'H':(15,(3,5))}
    for kinds in itertools.combinations_with_replacement(all_types,3):
        N=sum(all_types[k][0] for k in kinds)
        opts=itertools.product(*(all_types[k][1] for k in kinds))
        admissible=[a for a in opts if not any(3+sum(a)<=q<=N for q in (4,8,16,32,64))]
        print(f'K4|{"".join(kinds)}|{N}|'+ (';'.join(','.join(map(str,a)) for a in admissible) if admissible else '-'))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--generate')
    parser.add_argument('--output')
    a=parser.parse_args()
    if a.generate:
        graph_records(a.generate)
    if a.output:
        import contextlib
        with open(a.output,'w') as f,contextlib.redirect_stdout(f):
            graph_stream(examples());case_stream()
    else:
        graph_stream(examples());case_stream()

if __name__=='__main__':main()
