"""Detect saturated triangle seven-poles and their direct-port interaction graph.
Independent of gadget_forcing and pentagon_local_exhaust.
For graphs with no C4/C8, every triangle with all 3 outbound edges on
5-cycles has the canonical 7-vertex structure as proved in the note.
"""
import networkx as nx, json

def canon_edge(u,v):return frozenset((u,v))

def all_pentagon_edges(G):
    result=set()
    for cyc in nx.simple_cycles(nx.to_directed(G),length_bound=5):
        if len(cyc)!=5:continue
        for i in range(5):result.add(canon_edge(cyc[i],cyc[(i+1)%5]))
    return result

def saturated_triangles(G):
    covered=all_pentagon_edges(G)
    tri=sorted(tuple(sorted(c)) for c in nx.enumerate_all_cliques(G) if len(c)==3)
    gadgets=[]
    for T in tri:
        Tset=set(T)
        ports=[]
        for a in T:
            ext=list(set(G[a])-Tset)
            if len(ext)!=1:continue
            ports.append(ext[0])
        if len(ports)!=3:continue
        out=[(a,p) for a,p in zip(T,ports)]
        if not all(canon_edge(a,p) in covered for a,p in out):continue
        common=set(G[ports[0]])&set(G[ports[1]])&set(G[ports[2]])
        assert len(common)==1,(T,ports,common)
        w=next(iter(common))
        verts=set(T)|set(ports)|{w}
        assert len(verts)==7
        gadgets.append({'triangle':list(T),'ports':ports,'center':w,'vertices':sorted(verts)})
    return gadgets

def audit(filename):
    G=nx.Graph()
    G.add_edges_from(tuple(map(int,l.split())) for l in open(filename) if l.strip())
    assert all(d==3 for _,d in G.degree())
    H=nx.Graph();S=saturated_triangles(G)
    H.add_nodes_from(range(len(S)))
    visited=set()
    for s in S:
        sverts=set(s['vertices'])
        assert not (visited & sverts), 'Overlapping saturated gadgets: theorem would fail'
        visited|=sverts
    port_owner={p:i for i,s in enumerate(S) for p in s['ports']}
    exterior_stubs=[]
    for i,s in enumerate(S):
        for p in s['ports']:
            ext=next(t for t in G[p] if t not in set(s['vertices']))
            if ext in port_owner:
                j=port_owner[ext]
                assert j!=i
                if i<j:H.add_edge(i,j)
            else: exterior_stubs.append((p,ext))
    assert sum(dict(H.degree()).values())+len(exterior_stubs)==3*len(S)
    print(filename,'gadgets',len(S),'quotient edges',H.number_of_edges(),
          'quotient cycle lengths',[len(c) for c in nx.cycle_basis(H)],
          'boundary edges to other vertices',len(exterior_stubs))
    return {'gadgets':S,'quotient_edges':sorted([list(e) for e in H.edges()]),
            'quotient_has_cycle':not nx.is_forest(H),
            'external_stubs':len(exterior_stubs)}

if __name__=='__main__':
    results={}
    for name in ('inflated_k4.edges','inflated_petersen.edges'):
        results[name]=audit(name)
    open('saturated_triangle_quotient_results.json','w').write(json.dumps(results,indent=2)+'\n')
