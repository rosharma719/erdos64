#!/usr/bin/env python3
"""Exact n=8 audit for 2-degenerate, (C4,C8)-free graphs.

Source is NetworkX graph atlas, which contains one isomorphism representative
of each of the 1044 simple graphs on seven vertices. The enumeration is
*complete conditional on correctness of this standard atlas*.

No dependency on other run scripts.
"""
from collections import Counter
from itertools import combinations
import json
import networkx as nx


def masks(g):
    return [sum(1 << int(v) for v in g[u]) for u in range(len(g))]


def no_4cycle(a):
    return all(((a[u] & a[v]).bit_count() < 2)
               for u in range(len(a)) for v in range(u+1,len(a)))


def path_length(a, u, v, wanted):
    def visit(x, seen, d):
        if d==wanted:
            return x == v
        choices = a[x] & ~seen
        while choices:
            bit = choices & -choices
            choices ^= bit
            if visit(bit.bit_length()-1, seen|bit, d+1):
                return True
        return False
    return visit(u,1<<u,0)


def has_8cycle(a):
    n=len(a)
    if n<8: return False
    for s in range(n):
        # count only cycles in which s is the smallest vertex
        def recurse(v,seen,length):
            if length==8:
                return bool(a[v]&(1<<s))
            choices=a[v]&~seen&~((1<<(s+1))-1)
            while choices:
                bit=choices&-choices
                choices^=bit
                if recurse(bit.bit_length()-1,seen|bit,length+1):return True
            return False
        if recurse(s,1<<s,1):return True
    return False


def grow(a, subset):
    n=len(a)
    b=a.copy();b.append(sum(1<<u for u in subset))
    for u in subset:b[u]|=1<<n
    return b


def graph_from_masks(a):
    n=len(a)
    h=nx.Graph();h.add_nodes_from(range(n))
    h.add_edges_from((u,v) for u in range(n) for v in range(u+1,n) if a[u]&(1<<v))
    return h


def main():
    atlas7=[G for G in nx.graph_atlas_g() if len(G)==7]
    assert len(atlas7)==1044
    count=Counter();witnesses=[]
    for h in atlas7:
        if max(nx.core_number(h).values())>2:continue
        a=masks(h)
        if not no_4cycle(a):continue
        count['source_7_2deg_C4']+=1
        for k in range(3):
            for subset in combinations(range(7),k):
                b=grow(a,subset)
                if not no_4cycle(b):continue
                count['n8_2deg_C4_candidates']+=1
                edges=sum(x.bit_count() for x in b)//2
                count['n8_max_C4_edges']=max(edges,count['n8_max_C4_edges'])
                if has_8cycle(b):continue
                count['n8_2deg_C4_C8_candidates']+=1
                count['n8_max_C4_C8_edges']=max(edges,count['n8_max_C4_C8_edges'])
                if edges==11:witnesses.append(b)
    assert count['n8_max_C4_edges']==11
    assert count['n8_max_C4_C8_edges']==11
    assert len(witnesses)==10

    representatives=[]
    for b in witnesses:
        g=graph_from_masks(b)
        if not any(nx.is_isomorphic(g,k) for k in representatives):
            representatives.append(g)
    assert len(representatives)==2

    # Extending with a vertex of degree exactly 2 gives a new C4 iff its
    # endpoints have a common neighbour; a new C8 iff an old simple
    # endpoint-to-endpoint path of length 6 exists.
    for b in witnesses:
        for u,v in combinations(range(8),2):
            assert ((b[u]&b[v]).bit_count()>=1 or path_length(b,u,v,6)), (u,v,b)
            c=grow(b,(u,v))
            assert not (no_4cycle(c) and not has_8cycle(c))
    count['n8_extremals_with_valid_2_attachment']=0
    count['n8_extremal_iso_classes']=len(representatives)
    payload={**count,'max_edge_examples':[]}
    for g in representatives:
        payload['max_edge_examples'].append({'graph6':nx.to_graph6_bytes(g,header=False).decode().strip(),
            'edges':sorted(map(list,g.edges())),'degrees':sorted(dict(g.degree()).values())})
    with open('/mnt/data/eg_run7_work/eight_vertex_certificate.json','w') as f:json.dump(payload,f,indent=2)
    print(json.dumps(payload,indent=2))

if __name__=='__main__':main()
