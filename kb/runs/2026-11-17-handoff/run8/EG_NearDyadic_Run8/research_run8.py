#!/usr/bin/env python3
"""Finite near-dyadic cycle-overlap audit and counterexample families.

Python >=3.10, networkx >=3. Use: python research_run8.py
Produces verified_results.json and reproducible graph6 data.
Two independent cycle testers are applied to every two-C9 candidate.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, permutations
import json, hashlib
from pathlib import Path
import networkx as nx

HERE = Path(__file__).resolve().parent
BASE_EDGES = {tuple(sorted((v,(v+1)%9))) for v in range(9)}


def assignments():
    """Exactly sum_{r=0}^7 C(7,r)*P(7,r)=130922 sequences."""
    for r in range(8):
        for idx in combinations(range(7), r):
            idxset=set(idx)
            for old in permutations(range(2,9), r):
                it=iter(old); fresh=9; seq=[]
                for p in range(7):
                    if p in idxset: seq.append(next(it))
                    else: seq.append(fresh); fresh+=1
                yield r, seq


def make_adj(seq):
    a=[set() for _ in range(16)]
    for u,v in BASE_EDGES: a[u].add(v);a[v].add(u)
    added=[]
    for u,v in zip([1]+seq,seq+[0]):
        if v not in a[u]:
            added.append((u,v));a[u].add(v);a[v].add(u)
    return a,added


def path_exists(adj, u, target, length, seen):
    if not length: return u==target
    for v in adj[u]:
        if v==target:
            if length==1:return True
        elif length>1 and not (seen>>v)&1:
            if path_exists(adj,v,target,length-1,seen|(1<<v)):return True
    return False


def incremental_oracle(seq, girth9=False):
    """Independent edge-insertion certificate: every new forbidden cycle closes a path."""
    a=[set() for _ in range(16)]
    for u,v in BASE_EDGES:a[u].add(v);a[v].add(u)
    newcount=0
    forbidden=[3,4,5,6,7,8,16] if girth9 else [4,8,16]
    for u,v in zip([1]+seq,seq+[0]):
        if v in a[u]:continue
        if len(a[u])==3 or len(a[v])==3:return False
        for L in forbidden:
            if path_exists(a,u,v,L-1,(1<<u)):return False
        a[u].add(v);a[v].add(u);newcount+=1
    return newcount>0


def static_oracle(adj, girth9=False):
    """Direct exhaustive simple-cycle DFS with minimum-vertex canonicalization."""
    if any(len(x)>3 for x in adj): return False
    targets=[3,4,5,6,7,8,16] if girth9 else [4,8,16]
    def search(start, u, visited, level, length):
        if level==length:return start in adj[u]
        for v in adj[u]:
            if v>start and not (visited>>v)&1:
                if search(start,v,visited|(1<<v),level+1,length):return True
        return False
    for length in targets:
        for start in range(len(adj)):
            if len(adj[start])>=2 and search(start,start,1<<start,1,length):return False
    return True


def graph_from_adj(adj):
    g=nx.Graph();g.add_nodes_from(i for i,a in enumerate(adj) if a)
    g.add_edges_from((u,v) for u,vs in enumerate(adj) for v in vs if u<v)
    return g


def all_cycle_edges(g):
    """Third oracle, NetworkX Johnson directed cycle enumeration, dedup undirected."""
    out={}
    for cyc in nx.simple_cycles(g.to_directed()):
        if len(cyc)<3:continue
        edges=frozenset(tuple(sorted((u,v))) for u,v in zip(cyc,cyc[1:]+cyc[:1]))
        out[edges]=len(cyc)
    return out


def two_cycle_enumeration():
    stats=Counter();matches=[];finite_examples=[]
    for r,seq in assignments():
        stats['tested']+=1
        inc=incremental_oracle(seq)
        adj,added=make_adj(seq)
        if not added:
            assert not inc
            continue # identical 9-cycle
        sta=static_oracle(adj)
        assert inc==sta,(r,seq,inc,sta)
        if sta:
            stats['accepted_dyadic_free']+=1
            stats[f'accepted_shared_other_vertices_{r}']+=1
            # both girth checkers
            ginc=incremental_oracle(seq,True)
            gsta=static_oracle(adj,True)
            assert ginc==gsta,(r,seq,'girth mismatch')
            g=graph_from_adj(adj)
            cx=all_cycle_edges(g)
            assert all(l not in (4,8,16) for l in cx.values()),seq
            if gsta:
                assert all(l>=9 for l in cx.values()),seq
                stats['accepted_girth9']+=1
                shared=set(BASE_EDGES)&{tuple(sorted((u,v))) for u,v in zip([1]+seq,seq+[0])}
                stats[f'girth9_shared_path_edges_{len(shared)+1}']+=1
            if len(finite_examples)<4 and r>=2 and r<=3 and not gsta:
                finite_examples.append(dict(seq=seq,vertices=len(g),cycles_by_length=dict(Counter(cx.values()))))
            matches.append((r,seq,gsta))
    assert stats['tested']==130922
    assert stats['accepted_dyadic_free']==151,stats
    assert stats['accepted_girth9']==9,stats
    assert [stats[f'girth9_shared_path_edges_{v}'] for v in (2,3,4)]==[2,3,4],stats
    return dict(statistics=dict(stats),some_non_girth9_examples=finite_examples)


def two_ear_graph(b,c,s):
    g=nx.cycle_graph(9)
    p=9-min(b,9-b)
    q=9-min(c,9-c)
    assert s>=1 and s<min(p,q)
    fresh=9; hub=0
    for i in range(s):g.add_edge(hub,fresh);hub=fresh;fresh+=1
    for endpoint,steps in ((b,p-s),(c,q-s)):
        cur=hub
        for i in range(steps-1):g.add_edge(cur,fresh);cur=fresh;fresh+=1
        g.add_edge(cur,endpoint)
    return g


def ear_algebra(b,c,s):
    # K4-subdivision has 7 simple cycles: four triangles, three 4-cycles.
    A=b;T=c-b;B=9-c
    p=9-min(b,9-b);q=9-min(c,9-c)
    return sorted([9, A+p,B+q,T+p+q-2*s,A+T+q,B+T+p,A+B+p+q-2*s])


def two_ear_enumeration():
    checked=0;valid=[];badfork=[]
    for b,c in combinations(range(2,8),2):
        p=9-min(b,9-b);q=9-min(c,9-c)
        for s in range(1,min(p,q)):
            checked+=1
            g=two_ear_graph(b,c,s)
            assert max(dict(g.degree()).values())<=3
            cycs=sorted(all_cycle_edges(g).values())
            algebra=ear_algebra(b,c,s)
            assert cycs==algebra,(b,c,s,cycs,algebra)
            if min(cycs)>=9 and 16 not in cycs:
                valid.append(dict(b=b,c=c,shared_external_prefix=s,order=len(g),lengths=cycs))
            if (b,c)==(4,5):badfork.append(dict(s=s,cycles=cycs))
    assert len(valid)==27,(checked,len(valid))
    assert not any(x['b']==4 and x['c']==5 for x in valid)
    K4sub=two_ear_graph(3,6,3)
    lens=sorted(all_cycle_edges(K4sub).values())
    assert lens==[9,9,9,9,12,12,12]
    (HERE/'K4_three_subdivision.g6').write_bytes(nx.to_graph6_bytes(K4sub,header=False))
    return dict(checked=checked,valid_count=len(valid),valid_cases=valid,
                forbidden_antipodal_fork=badfork,example_K4_three_subdivision_cycle_lengths=lens)


def edge_certificates(g,allowed):
    ce=all_cycle_edges(g)
    out={}
    for u,v in g.edges():
        e=tuple(sorted((u,v)))
        witness=next((sorted(list(E)) for E,L in ce.items() if L in allowed and e in E),None)
        if witness is not None:out[f'{e[0]}-{e[1]}']=dict(length=len(witness),edges=witness)
    return out


def glue_blocks(base,t):
    g=nx.Graph()
    for j in range(t):
        # vertex 0 common to all copies; local 1..7 distinct
        p=lambda v: 0 if v==0 else 1+7*j+v-1
        g.add_edges_from((p(u),p(v)) for u,v in base.edges())
    return g


def near_dyadic_coverage_counterexamples():
    block=nx.from_graph6_bytes(b'GxaGiC')
    assert len(block)==8 and block.number_of_edges()==11
    cyc=all_cycle_edges(block)
    assert 4 not in cyc.values() and 8 not in cyc.values()
    cover=edge_certificates(block,{3,5})
    assert len(cover)==11,cover
    (HERE/'near_dyad_8vertex_block.g6').write_bytes(nx.to_graph6_bytes(block,header=False))
    glued=glue_blocks(block,4)
    assert len(glued)==29 and glued.number_of_edges()==44
    gluedcyc=all_cycle_edges(glued)
    assert all(l not in {4,8,16} for l in gluedcyc.values())
    assert len(edge_certificates(glued,{3,5}))==44
    (HERE/'near_dyad_glued29.g6').write_bytes(nx.to_graph6_bytes(glued,header=False))
    # Infinite argument: t copies share one vertex -> n=7t+1, e=11t, and all cycles remain in one block.
    assert 2*glued.number_of_edges()/len(glued)>3
    # Uniform 3-subdivision of K4: 4 triangles become 9-cycles, 3 quadrilaterals become 12-cycles.
    k4=nx.complete_graph(4)
    # For k odd >=3, m=(2^k+1)/3 odd >1; all cycles are 3m or 4m, neither dyadic.
    return dict(block_graph6='GxaGiC',block_edge_count=11,
                block_cycles_by_length=dict(Counter(cyc.values())),
                block_witnesses=cover,block_girth=min(cyc.values()),
                glued_29=dict(vertices=len(glued),edges=glued.number_of_edges(),
                average_degree=2*glued.number_of_edges()/len(glued),
                cycles_by_length=dict(Counter(gluedcyc.values()))),
                infinite_family=dict(vertices='7*t+1',edges='11*t',
                  average_degree='22*t/(7*t+1)',holds_average_gt_3='t>=4',
                  dyadic_free=True,every_edge_in_C3_or_C5=True),
                k4_uniform_subdivision=dict(k='odd >=3',m='(2**k+1)//3',
                  vertex_count='6*m-2',edge_count='6*m',
                  cycle_lengths=['3*m=2**k+1','4*m'],
                  degree3_fraction='2/(3*m-1)'))


def main():
    report=dict(
        two_C9=two_cycle_enumeration(),
        two_ears=two_ear_enumeration(),
        saturation_counterexamples=near_dyadic_coverage_counterexamples()
    )
    p=HERE/'verified_results.json';p.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('two-C9 embeddings:', report['two_C9']['statistics'])
    print('two-ear cases',report['two_ears']['checked'],'valid',report['two_ears']['valid_count'])
    print('8-vertex block near-dyadic edge witnesses',len(report['saturation_counterexamples']['block_witnesses']))
    print('29-vertex glued: n,m,avgdeg', report['saturation_counterexamples']['glued_29'])
    print('SHA256',hashlib.sha256(p.read_bytes()).hexdigest())

if __name__=='__main__':main()
