#!/usr/bin/env python3
"""Pure-stdlib certificate generator for partial 7-pole inflation.

Independent of previous run modules. Graph is simple cubic with vertices
numbered by a standard offset per base vertex; ordinary vertices are retained.
"""
from itertools import combinations
from collections import deque
import hashlib, json

T=[(0,1),(1,2),(2,0),(0,4),(1,5),(2,6),(3,4),(3,5),(3,6)]
ports=[4,5,6]

def make_adjacency(n,edges):
    a=[set() for _ in range(n)]
    for x,y in edges:
        assert x!=y and 0<=x<n and 0<=y<n and y not in a[x]
        a[x].add(y);a[y].add(x)
    return a

def all_simple_paths(a,start,end):
    def dfs(path):
        if path[-1]==end:
            yield path
            return
        for y in sorted(a[path[-1]]):
            if y not in path:
                yield from dfs(path+[y])
    yield from dfs([start])

Tadj=make_adjacency(7,T)
paths={ (i,j,k):min((p for p in all_simple_paths(Tadj,i,j) if len(p)-1==k),default=None)
        for i in ports for j in ports if i!=j for k in range(2,7)}
assert all(p is not None for p in paths.values())

def inflate(base_n,base_edges,marked):
    B=make_adjacency(base_n,base_edges)
    assert all(len(nb)==3 for nb in B)
    marked=set(marked)
    ids={};pos=0;external_port={}
    for v in range(base_n):
        if v in marked:
            ids[v]=list(range(pos,pos+7));pos+=7
            for i,w in enumerate(sorted(B[v])):
                external_port[v,w]=ids[v][ports[i]]
        else:
            ids[v]=[pos];pos+=1
            for w in B[v]: external_port[v,w]=ids[v][0]
    E=[]
    for v in marked:
        E.extend((ids[v][i],ids[v][j]) for i,j in T)
    E.extend((external_port[u,v],external_port[v,u]) for u,v in base_edges)
    A=make_adjacency(pos,E)
    assert all(len(x)==3 for x in A)
    return A,ids,external_port

def cycles_of_base(A):
    n=len(A)
    seen=set()
    for s in range(n):
        def dfs(path):
            u=path[-1]
            for v in sorted(A[u]):
                if v==s and len(path)>=3:
                    cyc=tuple(path)
                    canonical=min(cyc,cyc[:1]+tuple(reversed(cyc[1:])))
                    if canonical not in seen:
                        seen.add(canonical)
                        yield canonical
                elif v>s and v not in path:
                    yield from dfs(path+[v])
        yield from dfs([s])

def dyadic_in_interval(lo,hi):
    k=4
    while k <lo:k*=2
    return k if k<=hi else None

def lift_cycle(base_cycle, marked, ids, pmap, target):
    L=len(base_cycle)
    visited=sum(v in marked for v in base_cycle)
    assert L+2*visited<=target<=L+6*visited
    extra=target-(L+2*visited)
    path=[]
    for i,v in enumerate(base_cycle):
        prev=base_cycle[(i-1)%L];nxt=base_cycle[(i+1)%L]
        if v in marked:
            take=min(4,extra);extra-=take
            steps=2+take
            p=paths[(pmap[v,prev]-ids[v][0],pmap[v,nxt]-ids[v][0],steps)]
            path.extend(ids[v][0]+j for j in p)
        else:
            path.append(ids[v][0])
    assert extra==0
    return path

def check_cert(A,c):
    return len(c)==len(set(c)) and all(c[(i+1)%len(c)] in A[v] for i,v in enumerate(c))

def base_cases():
    K4=(4,list(combinations(range(4),2)))
    Petersen=(10,[(i,(i+1)%5) for i in range(5)]+[(i,5+i) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)])
    return [("K4",*K4),("Petersen",*Petersen)]

def process(base, n, edges, marked):
    marked=set(marked)
    B=make_adjacency(n,edges)
    A,ids,pmap=inflate(n,edges,marked)
    candidates=[]
    for C in cycles_of_base(B):
        r=sum(v in marked for v in C)
        k=dyadic_in_interval(len(C)+2*r,len(C)+6*r)
        if k is not None:
            witness=lift_cycle(C,marked,ids,pmap,k)
            assert check_cert(A,witness)
            candidates.append((k,C,witness,r))
    candidates.sort(key=lambda x:(x[0],len(x[1]),x[1]))
    payload={"base":base,"base_n":n,"inflated_n":len(A),"marked":sorted(marked),"marked_count":len(marked),
           "marked_fraction":f"{len(marked)}/{n}",
           "all_degrees_three":all(len(x)==3 for x in A),
           "base_has_perfect_matching": (base=="K4" or base=="Petersen"),
           "density_condition":2*len(marked)>=n,
           "forced_witness_found":bool(candidates)}
    if candidates:
        k,C,witness,r=candidates[0]
        payload.update({"cycle_length":k,"quotient_cycle":list(C),"r":r,"lifted_cycle":witness})
    E=sorted((u,v) for u,x in enumerate(A) for v in x if u<v)
    raw=''.join(f'{u} {v}\n' for u,v in E)
    payload['sha256_edgelist']=hashlib.sha256(raw.encode()).hexdigest()
    return payload,raw

if __name__=='__main__':
    import os
    root=os.path.dirname(__file__)
    results=[]
    for base,n,edges in base_cases():
        sets=[set(s) for k in range(n+1) for s in combinations(range(n),k)] if base=='K4' else [set(),{0,2,4,6},{0,1,2,3,4},{0,2,4,6,8},set(range(6)),set(range(10))]
        for marked in sets:
            p,raw=process(base,n,edges,marked)
            results.append(p)
            if p['forced_witness_found']:
                filename=f"{base.lower()}_{''.join(map(str,sorted(marked)))}.edges"
                open(os.path.join(root,filename),'w').write(raw)
                p['edgelist_filename']=filename
    assert all(p['forced_witness_found'] for p in results if p['density_condition'])
    open(os.path.join(root,'certificates.json'),'w').write(json.dumps(results,indent=2)+'\n')
    print(f"{len(results)} cases, all density-positive cases have independently checkable dyadic cycles")
    for p in results:
        print(p['base'], p['marked'], 'n=',p['inflated_n'], 'density=',p['density_condition'],'cycle=',p.get('cycle_length'))
