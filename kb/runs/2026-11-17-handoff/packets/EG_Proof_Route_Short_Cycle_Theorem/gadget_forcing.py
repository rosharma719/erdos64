"""Reproducible 7-pole substitution and exact dyadic-cycle witness generator.

No networkx dependencies. Run: python gadget_forcing.py
The substitution is elementary; no claim of literature priority.
"""
from itertools import combinations
import json,hashlib

# Offsets: 0:a,1:b,2:c,3:w,4:x,5:y,6:z.
INTERNAL=[(0,1),(1,2),(2,0),(0,4),(1,5),(2,6),(3,4),(3,5),(3,6)]
PORT=[4,5,6]

def graph(edges,n):
    a=[set() for _ in range(n)]
    for u,v in edges:
        assert u!=v and v not in a[u]
        a[u].add(v);a[v].add(u)
    return a

def all_internal_paths(s,t):
    a=graph(INTERNAL,7)
    def rec(u,path):
        if u==t:
            yield tuple(path)
            return
        for v in sorted(a[u]):
            if v not in path:yield from rec(v,path+[v])
    return list(rec(s,[s]))

PATHS={(s,t):all_internal_paths(s,t) for s in PORT for t in PORT if s!=t}
assert {len(p)-1 for p in PATHS[(4,5)]}==set(range(2,7))

def inflate(base_n,base_edges):
    adj=graph(base_edges,base_n)
    assert all(len(x)==3 for x in adj), 'base graph must be cubic'
    edges=[]
    for v in range(base_n):
        edges.extend((7*v+u,7*v+w) for u,w in INTERNAL)
    port={}
    for v in range(base_n):
        for index,neighbor in enumerate(sorted(adj[v])):
            port[v,neighbor]=7*v+PORT[index]
    for u,v in base_edges:
        edges.append((port[u,v],port[v,u]))
    G=graph(edges,7*base_n)
    assert all(len(x)==3 for x in G)
    return G,port

def find_cycle_of_length(G,k):
    # Basic exact DFS, vertex-minimal rooting for no duplicate search branches.
    for start in range(len(G)):
        def go(u,path,seen):
            if len(path)==k:
                if start in G[u]:return path
                return None
            for v in sorted(G[u]):
                if v>start and v not in seen:
                    result=go(v,path+[v],seen|{v})
                    if result:return result
            return None
        res=go(start,[start],{start})
        if res:return res
    return None

def witness_for_base_cycle(base_cycle,port,lengths):
    assert len(base_cycle)==len(lengths)
    q=len(base_cycle)
    result=[]
    for i,v in enumerate(base_cycle):
        before=base_cycle[(i-1)%q]
        after=base_cycle[(i+1)%q]
        start=port[v,before];end=port[v,after]
        s=start%7;t=end%7
        candidates=sorted(p for p in PATHS[s,t] if len(p)-1==lengths[i])
        assert candidates
        result.extend(7*v+z for z in candidates[0])
    return result

def is_cycle(G,seq):
    return len(seq)==len(set(seq)) and all(seq[(i+1)%len(seq)] in G[seq[i]] for i in range(len(seq)))

def summarize(base_n,base_edges,name):
    G,port=inflate(base_n,base_edges)
    assert not find_cycle_of_length(G,4)
    assert not find_cycle_of_length(G,8)
    # Check 7-pole paths cover 2..6 for every terminal pair.
    for s,t in PATHS:
        assert {len(p)-1 for p in PATHS[s,t]}==set(range(2,7))
    # K4 base has 4 triangles, each avoids a whole 7-vertex gadget.
    rooted={}
    if base_n==4:
        for omitted in range(4):
            tri=tuple(v for v in range(4) if v!=omitted)
            cert=witness_for_base_cycle(tri,port,[4,4,5])
            assert len(cert)==16 and is_cycle(G,cert)
            assert all(v//7!=omitted for v in cert)
            rooted[str(omitted)]=cert
    # Fixed base Petersen 5-cycle supports length 16 (3+2+2+2+2=11 internal +5=16)
    if name=='petersen_base':
        pent=(0,1,2,3,4)
        cert=witness_for_base_cycle(pent,port,[3,2,2,2,2])
        assert len(cert)==16 and is_cycle(G,cert)
        rooted['base_pentagon']=cert
    serialized=''.join(f'{u}:{",".join(map(str,sorted(n)))}\n' for u,n in enumerate(G)).encode()
    return G,{'name':name,'n':len(G),'m':sum(map(len,G))//2,
              'sha256_adjacency':hashlib.sha256(serialized).hexdigest(),
              'c4':False,'c8':False,'rooted_C16_witnesses':rooted}

if __name__=='__main__':
    K4=list(combinations(range(4),2))
    G4,out4=summarize(4,K4,'k4_base')
    # Petersen graph: 0..4 outer cycle, 5..9 inner star, 5 spokes.
    Petersen= [(i,(i+1)%5) for i in range(5)]+[(i,5+i) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)]
    GP,outP=summarize(10,Petersen,'petersen_base')
    assert not find_cycle_of_length(G4,4) and not find_cycle_of_length(G4,8)
    assert not find_cycle_of_length(GP,4) and not find_cycle_of_length(GP,8)
    output={'k4':out4,'petersen':outP}
    open('forcing_certificates.json','w').write(json.dumps(output,indent=2)+'\n')
    open('inflated_k4.edges','w').write(''.join(f'{u} {v}\n' for u in range(len(G4)) for v in sorted(G4[u]) if u<v))
    open('inflated_petersen.edges','w').write(''.join(f'{u} {v}\n' for u in range(len(GP)) for v in sorted(GP[u]) if u<v))
    print(json.dumps(output,indent=2))
