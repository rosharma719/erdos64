#!/usr/bin/env python3
"""Pass XIII: exact low-connector cycles in cubic coherent decycling partitions.

The assertions validate constructive elementary lemmas, not an Erdős-Gyárfás proof.
Run: python pass13_tree_backbone.py
"""
from itertools import combinations
from collections import Counter
import networkx as nx


def three_arm(s):
    """Cubic graph with tree-centre 0 and s connector vertices; s>=3.
    Each connector has one neighbour in each of the three tree branches.
    """
    assert s >= 3
    G = nx.Graph()
    G.add_nodes_from(range(4*s-2))
    J = set(range(3*s-2, 4*s-2))
    for i in range(3):
        arm = [1 + i*(s-1) + a for a in range(s-1)]
        G.add_edge(0, arm[0])
        G.add_edges_from(zip(arm[:-1], arm[1:]))
        slots = arm[:-1] + [arm[-1], arm[-1]]
        for k, a in enumerate(slots):
            G.add_edge(a, 3*s-2+(k+i)%s)
    return G, J


def tree_partition_ok(G, J, near=False):
    J = set(J)
    T = G.subgraph(set(G)-J)
    H = G.subgraph(J)
    return nx.is_tree(T) and H.number_of_edges() == (1 if near else 0)


def cut_crossings(G, J):
    T=G.subgraph(set(G)-set(J)).copy()
    ans=[]
    for u,v in T.edges():
        T.remove_edge(u,v)
        A,B=list(nx.connected_components(T))
        mixed=[j for j in J if (set(G[j]) & A) and (set(G[j]) & B)]
        ans.append({'edge':tuple(sorted((u,v))), 'side_sizes':(len(A),len(B)),
                    'crossing_connectors':len(mixed), 'connector_ids':mixed})
        T.add_edge(u,v)
    return ans


def fundamental(G,T,j,a,b):
    path=nx.shortest_path(T,a,b)
    return {frozenset(x) for x in list(zip(path[:-1],path[1:]))+[(a,j),(j,b)]}


def is_one_cycle(edges):
    H=nx.Graph()
    H.add_edges_from(tuple(e) for e in edges)
    return H.number_of_nodes()>=3 and nx.is_connected(H) and all(d==2 for _,d in H.degree())


def xor_cycle(G,T,j,k,a,b,c,d):
    P=nx.shortest_path(T,a,b)
    Q=nx.shortest_path(T,c,d)
    pE={frozenset(z) for z in zip(P[:-1],P[1:])}
    qE={frozenset(z) for z in zip(Q[:-1],Q[1:])}
    assert pE & qE, 'Tree paths must have a shared edge'
    C=fundamental(G,T,j,a,b)^fundamental(G,T,k,c,d)
    assert is_one_cycle(C)
    assert len(C)==len(P)-1+len(Q)-1-2*len(pE&qE)+4
    return C


def branch_indices(T,r):
    S=T.copy();S.remove_node(r)
    return {v:i for i,cc in enumerate(nx.connected_components(S)) for v in cc}


def avoid_root_at_most_two(G,J,r):
    """Construct a simple cycle avoiding r using <=2 connector vertices.
    Preconditions: cubic G, induced tree T, J independent, |J|>=3.
    """
    J=set(J);T=G.subgraph(set(G)-J).copy()
    assert len(J)>=3 and all(d==3 for _,d in G.degree())
    assert tree_partition_ok(G,J)
    if r in J:
        j=next(j for j in J if j!=r)
        a,b=list(G[j])[:2]
        cycle=fundamental(G,T,j,a,b)
    else:
        parts=branch_indices(T,r)
        one=None
        for j in J:
            N=list(G[j]);
            if r in N:continue
            for a,b in combinations(N,2):
                if parts[a]==parts[b]:
                    one=fundamental(G,T,j,a,b)
                    break
            if one is not None:break
        if one is not None:
            cycle=one
        else:
            assert T.degree(r)==3
            # In the one-connector obstruction, each j meets all three branches.
            assert all({parts[a] for a in G[j]}=={0,1,2} for j in J)
            j,k=list(J)[:2]
            na={parts[a]:a for a in G[j]}
            nb={parts[a]:a for a in G[k]}
            cycle=xor_cycle(G,T,j,k,na[0],na[1],nb[0],nb[1])
    H=nx.Graph();H.add_edges_from(tuple(e) for e in cycle)
    assert is_one_cycle(cycle) and r not in H and len(set(H)&J)<=2
    return cycle


def bridge(G,e,f):
    e=tuple(e);f=tuple(f)
    assert not set(e)&set(f)
    x=max(G)+1;y=x+1
    H=G.copy();H.remove_edges_from((e,f))
    H.add_edges_from(((e[0],x),(e[1],x),(x,y),(f[0],y),(f[1],y)))
    return H,x,y


def dyadic_masks(G):
    A={v:set(G[v]) for v in G};n=len(G);out=[]
    for q in (4,8,16,32):
        if q>=n:continue
        masks=set()
        for s in G:
            def dfs(u,d,mask):
                if d==q:
                    if s in A[u]:masks.add(mask)
                    return
                for v in A[u]:
                    if v>s and not mask>>v&1:dfs(v,d+1,mask|1<<v)
            dfs(s,1,1<<s)
        out += [(q,z) for z in masks]
    return out


def main():
    # Structural theorem verified in graphs spanning both residue classes.
    table=[]
    for s in range(3,8):
        G,J=three_arm(s);T=G.subgraph(set(G)-J)
        assert tree_partition_ok(G,J)
        cuts=cut_crossings(G,J)
        for c in cuts:
            assert c['crossing_connectors'] == 2 if min(c['side_sizes'])==1 else c['crossing_connectors']>=3
        for r in G:
            C=avoid_root_at_most_two(G,J,r)
        # Check every relevant pairwise XOR construction, rather than just a witness.
        pairs=0
        for c in cuts:
            if min(c['side_sizes'])<=1:continue
            h=c['edge'];T0=T.copy();T0.remove_edge(*h);A,B=list(nx.connected_components(T0))
            indices=c['connector_ids']
            for j,k in combinations(indices,2):
                a=next(z for z in G[j] if z in A)
                b=next(z for z in G[j] if z in B)
                z=next(z for z in G[k] if z in A)
                w=next(z for z in G[k] if z in B)
                X=xor_cycle(G,T,j,k,a,b,z,w)
                assert frozenset(h) not in X
                pairs+=1
        table.append({'n':len(G),'induced_tree_order':len(T), 'connectors':len(J),
                      'internal_tree_edges':sum(min(c['side_sizes'])>1 for c in cuts),
                      'minimum_cut_crossing':min(c['crossing_connectors'] for c in cuts),
                      'checked_pairwise_XOR':pairs,'root_witnesses':len(G)})

    G,J=three_arm(3)
    assert nx.is_isomorphic(G,nx.petersen_graph())
    D=dyadic_masks(G)
    # Explicit Petersen rooted obstruction for the fixed coherent partition.
    root_free=[(q,c) for q,c in D if not (c&1)]
    assert len(root_free)>0 and all(q==8 and (c&sum(1<<j for j in J)).bit_count()==3 for q,c in root_free)
    print('PETERSEN_CERTIFICATE', {'g6':nx.to_graph6_bytes(G,header=False).decode().strip(),
                                  'root':0,'J':sorted(J),
                                  'total_dyadic_cycles':len(D),'root_free':len(root_free),
                                  'root_free_J_counts':dict(Counter((c&sum(1<<j for j in J)).bit_count() for _,c in root_free))})
    # Bridge transfer n=14 -> 16 with both edges T-J: obtain near-independent J.
    G,J=three_arm(4);T=set(G)-J
    cross=[tuple(sorted((u,v))) for u,v in G.edges() if (u in J)^(v in J)]
    e,f=next((e,f) for e,f in combinations(cross,2) if not set(e)&set(f))
    H,x,y=bridge(G,e,f)
    assert tree_partition_ok(H,J|{y},near=True)
    # Both edges of T instead: two-tree complement, independent J'.
    tedges=[tuple(sorted((u,v))) for u,v in G.edges() if u in T and v in T]
    e,f=next((e,f) for e,f in combinations(tedges,2) if not set(e)&set(f))
    H,x,y=bridge(G,e,f)
    J2=J|{y}
    assert H.subgraph(J2).number_of_edges()==0
    assert len(list(nx.connected_components(H.subgraph(set(H)-J2))))==2
    assert nx.is_forest(H.subgraph(set(H)-J2))
    # Reverse parity: bridge the sole J-J edge and any T edge in coherent n=16 partition.
    G,J=three_arm(4);cross=[tuple(sorted((u,v))) for u,v in G.edges() if (u in J)^(v in J)]
    e,f=next((e,f) for e,f in combinations(cross,2) if not set(e)&set(f))
    H,x,y=bridge(G,e,f);J2=J|{y}
    jj=tuple(next(iter(H.subgraph(J2).edges())))
    ff=next((a,b) for a,b in H.edges() if a not in J2 and b not in J2 and not set((a,b))&set(jj))
    K,xx,yy=bridge(H,jj,ff)
    assert tree_partition_ok(K,J2,near=False)
    print('BRIDGE_PARTITION_TEST',{'14_to_16':'coherent/near-independent',
                                   '14_to_16_both_tree_edges':'independent/two-tree forest',
                                   '16_to_18_bridge_JJ':'coherent/independent'})
    for row in table:print('TREE_CERTIFICATE',row)

if __name__=='__main__':main()
