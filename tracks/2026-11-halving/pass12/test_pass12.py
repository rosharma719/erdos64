"""Pass XII regressions, separate from the existing solver."""
import sys
from pathlib import Path
import networkx as nx
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'verifier'))
from tower_reference import examples,TYPES


def test_clean_tower_profiles():
    expected={
     'I':[(0,),(0,),(0,)],
     'T':[(1,2)]*3,
     'S':[(2,3,4,5,6),(2,3,4,5,6),(3,4,5,6)],
     'H':[(3,4,5,6,7,8,9,10,11,12,13,14)]*2+[(5,6,7,8,9,10,11,12,13,14)],
     'U':[(2,3,4,5,6)]*3}
    for name,kind in examples().items():
        if name in expected:
            values=sorted(tuple(sorted({len(p)-1 for p in nx.all_simple_paths(kind.graph,kind.ports[i],kind.ports[j])}))
                   for i,j in ((0,1),(0,2),(1,2)))
            assert values==sorted(expected[name])


def test_unclean_interval_counterexample():
    P=examples()['P5']
    vals={len(p)-1 for p in nx.all_simple_paths(P.graph,P.ports[0],P.ports[1])}
    assert vals=={1,3,4}
    assert 4 in {len(c) for c in nx.simple_cycles(P.graph)}


def test_20_and_35_case_tables():
    import itertools
    from tower_reference import TYPES
    opt={'I':(1,(0,)),'T':(3,(1,)),'S':(7,(2,3)),'U':(7,(2,)),'H':(15,(3,5))}
    for table in (TYPES,opt):
        good=[]
        for z in itertools.combinations_with_replacement(table,3):
            N=sum(table[k][0] for k in z)
            for amin in itertools.product(*(table[k][1] for k in z)):
                L=3+sum(amin)
                if all(not L<=q<=N for q in (4,8,16,32,64)):
                    good.append((''.join(z),amin))
        assert good==[('III',(0,0,0)),('ITT',(0,1,1)),('ISS',(0,3,3))]


def test_degree_derived_terminal_isomorphism():
    import json
    cert=json.loads((HERE/'h15_isomorphism_certificate.json').read_text())
    A=nx.from_graph6_bytes(cert['tower_graph6'].encode())
    B=nx.from_graph6_bytes(cert['exoo_graph6'].encode())
    mapping={int(k):v for k,v in cert['tower_to_exoo'].items()}
    assert sorted(mapping[x] for x,d in A.degree() if d==2)==sorted(x for x,d in B.degree() if d==2)
    assert {frozenset((mapping[a],mapping[b])) for a,b in A.edges()}=={frozenset(e) for e in B.edges()}
