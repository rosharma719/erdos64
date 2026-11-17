"""Exact small-order checks for the orbit, ear, and Hamiltonian lemmas."""
import json
from pathlib import Path
import shutil
import subprocess

import networkx as nx
import pytest

from root_orbit_switching import (
    automorphism_orbits, orbit_coverage, translate_cycle_away_from,
    cubic_cycle_spoke_identity, external_spokes, chord_count,
    single_ear_avoiding_cycle, cycle_switch_certificate,
)
from prime_pole_obstructions import (
    is_cyclically_four_edge_connected_cubic, root_robustness_violations,
    verify_dyadic_cycle,
)
from partial_triangle_expansion import cycles
from rooted_hamiltonian_matching import census

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'root_switching_certificates.json').read_text())


def graph_from_matching(n, matching):
    G=nx.cycle_graph(n)
    G.add_edges_from(tuple(x) for x in matching)
    assert all(d==3 for _, d in G.degree())
    return G


def test_root_orbit_lemma_constructs_actual_cycles():
    samples=[(nx.cubical_graph(),4),(nx.petersen_graph(),8),
             (nx.heawood_graph(),8)]
    for G,target in samples:
        C=next(tuple(c) for c in cycles(G) if len(c)==target)
        orbits=automorphism_orbits(G)
        assert len(orbits)==1 and len(orbits[0])==len(G)
        assert orbit_coverage(G,[C],orbits)==(True,)
        for root in G:
            witness=translate_cycle_away_from(G,C,root)
            assert witness and verify_dyadic_cycle(G,witness,root)
    K4=nx.complete_graph(4)
    C=next(tuple(c) for c in cycles(K4) if len(c)==4)
    assert orbit_coverage(K4,[C])==(False,)
    assert translate_cycle_away_from(K4,C,0) is None


def test_orbit_coverage_is_complete_if_given_every_dyadic_cycle():
    # Nonvertextransitive examples show orbit coverage is about automorphism
    # orbits, not just vertex transitivity.
    catalog=json.loads((HERE/'cubic_catalog_n8_n10.json').read_text())['connected_cubic']['8']
    for encoded in catalog:
        G=nx.from_graph6_bytes(encoded.encode())
        dyadic=[tuple(c) for c in cycles(G) if len(c) in (4,8)]
        orbits=automorphism_orbits(G)
        flags=orbit_coverage(G,dyadic,orbits)
        bad=set(root_robustness_violations(G))
        assert all(covered == (not bool(O&bad)) for covered,O in zip(flags,orbits))


def test_three_connected_nonspanning_cycle_has_four_spokes_and_ears():
    G=nx.petersen_graph()
    C=tuple(DATA['petersen_two_ear']['C'])
    assert cubic_cycle_spoke_identity(G,C)
    assert len(external_spokes(G,C))>=4
    assert len(external_spokes(G,C))==len(C)-2*chord_count(G,C)
    # The component outside C has three or more distinct attachments.
    for comp in nx.connected_components(G.subgraph(set(G)-set(C))):
        attachments={u for u in C if any(w in comp for w in G[u])}
        assert len(attachments)>=3


def test_petersen_requires_two_ears_not_one():
    G=nx.petersen_graph()
    root=0
    Cs=[tuple(c) for c in cycles(G) if len(c)==8]
    through=[c for c in Cs if root in c]
    avoiding=[c for c in Cs if root not in c]
    assert len(Cs)==15 and len(through)==12 and len(avoiding)==3
    assert all(single_ear_avoiding_cycle(G,C,root) is None for C in through)
    record=DATA['petersen_two_ear']
    cert=cycle_switch_certificate(G,tuple(record['C']),tuple(record['D']),root)
    assert cert is not None and len(cert.ears)==2
    assert cert.length_delta==0
    assert len(cert.added_ear_edges)==len(cert.removed_cycle_edges)==4
    assert {tuple(p) for p in cert.ears}=={tuple(p) for p in record['ears']}
    assert verify_dyadic_cycle(G,cert.avoiding_root,root)


def test_small_prime_switching_number_at_most_two():
    catalogs=json.loads((HERE/'cubic_catalog_n8_n10.json').read_text())['connected_cubic']
    G12=json.loads((HERE/'cubic_catalog_n12.json').read_text())
    examples={6:[nx.circular_ladder_graph(3),nx.complete_bipartite_graph(3,3)],
              8:[nx.from_graph6_bytes(s.encode()) for s in catalogs['8']],
              10:[nx.from_graph6_bytes(s.encode()) for s in catalogs['10']],
              12:[nx.from_graph6_bytes(s.encode()) for s in G12]}
    counts={}
    for n, graphs in examples.items():
        scores={1:0,2:0}
        for G in graphs:
            if not is_cyclically_four_edge_connected_cubic(G):
                continue
            dyadic=[tuple(c) for c in cycles(G) if len(c)>=4 and len(c)&(len(c)-1)==0]
            for root in G:
                through=[C for C in dyadic if root in C]
                avoiding=[D for D in dyadic if root not in D]
                assert avoiding and through
                best=999
                for C in through:
                    for D in avoiding:
                        cert=cycle_switch_certificate(G,C,D,root)
                        if cert is not None:
                            best=min(best,len(cert.ears))
                            if best==1:break
                    if best==1:break
                assert best in (1,2)
                scores[best]+=1
        counts[n]=scores
    assert counts=={6:{1:6,2:0},8:{1:16,2:0},
                    10:{1:40,2:10},12:{1:212,2:4}}


def test_hamiltonian_rooted_complete_census():
    expected={
        4:(1,0,0,1), 6:(1,1,0,0), 8:(14,9,0,5),
        10:(80,50,30,0), 12:(768,524,244,0),
        14:(8817,5925,2892,0), 16:(123472,82460,41009,3),
    }
    for n, quadruple in expected.items():
        counts,matchings=census(n)
        assert tuple(counts.get(k,0) for k in ['admissible','C4','C8','survive'])==quadruple
        assert DATA['statistics'][str(n)]=={k:counts.get(k,0) for k in ['admissible','C4','C8','survive']}
        assert [list(map(list,m)) for m in matchings]==[s['matching'] for s in DATA['survivors'].get(str(n),[])]
    for bad in (3,5,18):
        with pytest.raises(ValueError):census(bad)


def test_every_small_hamiltonian_root_critical_survivor_nonprime_except_K4():
    witnesses=[]
    for n, rows in DATA['survivors'].items():
        n=int(n)
        for row in rows:
            G=graph_from_matching(n,row['matching'])
            assert nx.to_graph6_bytes(G,header=False).decode().strip()==row['graph6']
            assert 0 in root_robustness_violations(G)
            if n==4:
                assert nx.is_isomorphic(G,nx.complete_graph(4))
                assert is_cyclically_four_edge_connected_cubic(G)
            else:
                assert not is_cyclically_four_edge_connected_cubic(G)
                edges=[tuple(e) for e in row['cyclic_three_cut']['edges']]
                H=G.copy();H.remove_edges_from(edges)
                components=list(nx.connected_components(H))
                assert sorted(map(len,components))==row['cyclic_three_cut']['sizes']
                assert len(components)==2
                assert all(G.subgraph(nodes).number_of_edges()>=len(nodes) for nodes in components)
            if n==16:witnesses.append(G)
    assert len(witnesses)==3
    assert all(nx.is_isomorphic(witnesses[0],G) for G in witnesses[1:])


def test_independent_cpp_enumerator_when_compiler_present(tmp_path):
    compiler=shutil.which('g++')
    if compiler is None:pytest.skip('g++ not available')
    src=HERE/'rooted_hamiltonian_census.cpp'
    binary=tmp_path/'root_census'
    subprocess.run([compiler,'-O2','-std=c++17',str(src),'-o',str(binary)],check=True,timeout=30)
    for n in (8,14,16):
        r=subprocess.run([str(binary),str(n)],capture_output=True,text=True,check=True,timeout=30)
        row=DATA['statistics'][str(n)]
        for key,lookup in [('filtered matchings','admissible'),('C4','C4'),('C8','C8'),('survive','survive')]:
            assert f'{key}={row[lookup]}' in r.stderr
        listed=[l for l in r.stdout.splitlines() if l.strip()]
        assert len(listed)==row['survive']
