#!/usr/bin/env python3
"""Independent verifier of the supplied 165-vertex 4-regular graph.

Reads just an edge list and JSON SHA-256; uses no graph library and no
imports from construction program.
"""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
r=json.loads((root/'high_degree_obstruction.json').read_text())
raw=(root/'line_graph_no_c4_c8.edges').read_bytes()
assert hashlib.sha256(raw).hexdigest()==r['edge_list_sha256']
E=[tuple(map(int,line.split())) for line in raw.decode().splitlines()]
n=r['line_graph_vertices']
a=[set() for _ in range(n)]
for u,v in E:
    assert 0<=u<v<n and v not in a[u]
    a[u].add(v);a[v].add(u)
assert len(E)==2*n and all(len(x)==4 for x in a)
assert all(a[u]&a[v] for u,v in E), 'edge without triangle'

def exists(k):
    for s in range(n):
        def walk(u,seen,length):
            if length==k:return s in a[u]
            return any(walk(v,seen|{v},length+1) for v in a[u] if v>s and v not in seen)
        if walk(s,{s},1):return True
    return False
assert not exists(4)
assert not exists(8)
print('PASS: 165 vertices, 330 edges, degree 4, every edge triangular, no C4/C8; SHA256',r['edge_list_sha256'])
