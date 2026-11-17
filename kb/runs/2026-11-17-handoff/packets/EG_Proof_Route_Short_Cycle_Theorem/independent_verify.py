"""Independent checks using NetworkX, with no import of the construction module."""
import json,hashlib,networkx as nx
from collections import Counter

def audit(filename,certificate):
    raw=open(filename).read()
    G=nx.Graph()
    G.add_edges_from(tuple(map(int,line.split())) for line in raw.splitlines() if line.strip())
    assert nx.is_connected(G)
    assert all(d==3 for _,d in G.degree())
    seen={k:set() for k in [3,4,5,8]}
    for cyc in nx.simple_cycles(nx.to_directed(G),length_bound=8):
        k=len(cyc)
        if k not in seen:continue
        # edge-set canonicalization, no repeated undirected cycles
        edge_set=frozenset(frozenset((cyc[i],cyc[(i+1)%k])) for i in range(k))
        seen[k].add(edge_set)
    assert not seen[4] and not seen[8]
    E={frozenset(e) for e in G.edges()}
    covered=set().union(*(c for k in (3,5) for c in seen[k]))
    absent=sorted(tuple(sorted(e)) for e in E-covered)
    assert absent, 'Proposed short-cycle edge-cover theorem would fail here'
    for label,C in certificate['rooted_C16_witnesses'].items():
        assert len(C)==16 and len(set(C))==16
        assert all(G.has_edge(C[i],C[(i+1)%16]) for i in range(16))
        if filename=='inflated_k4.edges':
            assert all(v//7!=int(label) for v in C)
    print(filename,'n',len(G),'m',G.number_of_edges(),
          'C3',len(seen[3]),'C5',len(seen[5]),'C4',len(seen[4]),'C8',len(seen[8]),
          'uncovered_by_3_or_5',len(absent),
          'rooted C16 certs',len(certificate['rooted_C16_witnesses']))
    return {'n':len(G),'m':G.number_of_edges(),
            'cycles':{str(k):len(seen[k]) for k in seen},
            'edges_not_on_C3_or_C5':absent}

if __name__=='__main__':
    certs=json.load(open('forcing_certificates.json'))
    output={'k4':audit('inflated_k4.edges',certs['k4']),
            'petersen':audit('inflated_petersen.edges',certs['petersen'])}
    open('independent_results.json','w').write(json.dumps(output,indent=2)+'\n')
    G=nx.read_edgelist('inflated_k4.edges',nodetype=int)
    with open('inflated_k4.g6','wb') as f:f.write(nx.to_graph6_bytes(G,header=False))
