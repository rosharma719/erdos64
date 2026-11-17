#!/usr/bin/env python3
"""Verify explicit H15 edge bijection, with degree-derived terminals only."""
from pathlib import Path
import json
import networkx as nx
cert=json.loads((Path(__file__).resolve().parents[1]/'h15_isomorphism_certificate.json').read_text())
A=nx.from_graph6_bytes(cert['tower_graph6'].encode())
B=nx.from_graph6_bytes(cert['exoo_graph6'].encode())
map_={int(k):v for k,v in cert['tower_to_exoo'].items()}
assert len(A)==len(B)==15
assert len(map_)==15 and set(map_.values())==set(B)
assert sorted(n for n,d in A.degree() if d==2)==cert['tower_ports']
assert sorted(n for n,d in B.degree() if d==2)==cert['exoo_ports']
assert sorted(map_[n] for n,d in A.degree() if d==2)==cert['exoo_ports']
assert {tuple(sorted((map_[a],map_[b]))) for a,b in A.edges()}=={tuple(sorted(e)) for e in B.edges()}
print('H15_ISOMORPHISM|15|21|3|OK')
