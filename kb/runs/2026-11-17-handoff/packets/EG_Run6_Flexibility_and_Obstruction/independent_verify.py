#!/usr/bin/env python3
"""Independent edge-list-only verifier: no imports from generator."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
cases=json.loads((root/'certificates.json').read_text())

def has_cycle(adj,k):
    n=len(adj)
    for s in range(n):
        def search(path,seen):
            u=path[-1]
            if len(path)==k:return s in adj[u]
            return any(search(path+[v],seen|{v}) for v in adj[u] if v>s and v not in seen)
        if search([s],{s}):return True
    return False

for c in cases:
    if not c['forced_witness_found']:continue
    path=root/c['edgelist_filename']
    raw=path.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==c['sha256_edgelist']
    es=[tuple(map(int,line.split())) for line in raw.decode().splitlines()]
    n=c['inflated_n'];adj=[set() for _ in range(n)]
    assert len(es)==3*n//2
    for u,v in es:
        assert 0<=u<v<n and v not in adj[u]
        adj[u].add(v);adj[v].add(u)
    assert all(len(x)==3 for x in adj)
    witness=c['lifted_cycle']
    assert len(witness)==c['cycle_length']==len(set(witness))
    assert all(witness[(i+1)%len(witness)] in adj[v] for i,v in enumerate(witness))
    if c['base']=='K4' and c['marked_count']==4:
        assert not has_cycle(adj,4)
        assert not has_cycle(adj,8)
        assert has_cycle(adj,16)
    if c['base']=='Petersen' and c['marked_count']==10:
        assert not has_cycle(adj,4)
        assert not has_cycle(adj,8)
print('VERIFIED',sum(c['forced_witness_found'] for c in cases),'certificates and graph hashes; full-inflation examples have C16 but no C4/C8')
