"""Independent verification of port-aware cycle calculus and mixed CSP."""
from __future__ import annotations
import itertools
import json
import sys
from pathlib import Path

import networkx as nx

sys.path.insert(0,str(Path(__file__).resolve().parent))
from partial_triangle_expansion import base_graph, independent_has_cycle_length, cycles
from mixed_gadget_solver import (
    build_replacement, gadgets_from_catalog, choice_library,
    predicted_spectrum, is_forbidden_free, search_assignments,
)
from exoo78_witness import make_certificate, verify_certificate


def test_gadget_profiles_and_permutations():
    G= {g.name:g for g in gadgets_from_catalog()}
    assert set(G)=={'id','T3','H7_skew','H7_uniform'}
    assert G['id'].pair_paths[0] == frozenset({0})
    assert all(x==frozenset({1,2}) for x in G['T3'].pair_paths)
    assert sorted(tuple(sorted(x)) for x in G['H7_skew'].pair_paths) == [
        (2,3,4,5,6),(2,3,4,5,6),(3,4,5,6)]
    assert all(x==frozenset(range(2,7)) for x in G['H7_uniform'].pair_paths)
    assert len(choice_library(list(G.values())))==6
    # All 7-vertex 3-port candidates arise by deleting one vertex from
    # a connected cubic 8-vertex graph; the catalog has all five classes.
    assert all(not(g.internal_cycle_lengths & {4,8}) for g in G.values())


def test_no_other_small_connected_clean_gadgets():
    from census_small_bases import read_catalog
    from mixed_gadget_census import all_bases
    for n in (6,10,12):
        bases=all_bases()[n]
        for B in bases:
            for v in B:
                H=B.copy(); H.remove_node(v)
                if nx.is_connected(H):
                    assert set(map(len, cycles(H))) & {4,8}, (n,v)


def test_12_catalog_completeness_conditional_on_published_count():
    from mixed_gadget_census import all_bases
    Gs=all_bases()[12]
    assert len(Gs)==85
    assert all(len(G)==12 and nx.is_connected(G) and all(d==3 for _,d in G.degree()) for G in Gs)
    # Compare the 85 actual adjacency spectra. These happen to be all
    # distinct here, giving a cheap nonisomorphism certificate.
    import numpy as np
    signatures=[]
    for G in Gs:
        M=nx.to_numpy_array(G,dtype=np.int64)
        A=M.copy();traces=[]
        for k in range(1,10):
            A=A@M
            if k>=3:traces.append(int(A.trace()))
        signatures.append(tuple(traces))
    assert len(set(signatures))==85


def test_csp_agrees_with_plain_bruteforce_k4():
    B=base_graph('k4')
    opts=choice_library(gadgets_from_catalog())
    for F in ({4,8},{4,8,16}):
        observed={tuple(a[u].name for u in B) for a in search_assignments(B,opts,F)}
        expected=set()
        for row in itertools.product(opts,repeat=4):
            chosen=dict(zip(B,row))
            if is_forbidden_free(B,chosen,F):
                expected.add(tuple(ch.name for ch in row))
        assert observed==expected


def test_independent_dfs_oracle_for_mixed_expansions():
    B=base_graph('k4')
    opts=choice_library(gadgets_from_catalog())
    # Deterministic sample of diverse gadgets, orientations and expansion sizes.
    for idx in range(0,len(opts)**4,29):
        digits=[];x=idx
        for _ in range(4):digits.append(x%len(opts));x//=len(opts)
        a={u:opts[digits[u]] for u in B}
        H=build_replacement(B,a)
        assert nx.is_connected(H) and all(d==3 for _,d in H.degree())
        predicted=predicted_spectrum(B,a)
        for p in (4,8,16):
            assert (p in predicted)==independent_has_cycle_length(H,p), (idx,p)


def test_entire_base_census_through_order10():
    from mixed_gadget_census import all_bases
    opts=choice_library(gadgets_from_catalog())
    expected={4:1,6:2,8:5,10:19}
    for n,count in expected.items():
        bases=all_bases()[n]
        assert len(bases)==count
        for B in bases:
            assert next(search_assignments(B,opts,{4,8,16}),None) is None


def test_exoo_78_certificate():
    cert=make_certificate()
    assert verify_certificate(cert)
    disk=json.loads(Path(__file__).with_name('exoo78_certificate.json').read_text())
    assert cert==disk


def test_78_family_isomorphism_classes():
    B=nx.from_graph6_bytes(b'KL`AOWo?[G?R')
    opts=choice_library(gadgets_from_catalog())
    assignments=list(search_assignments(B,opts,{4,8,16}))
    assert len(assignments)==48
    assert all(sum(a[v].gadget.size for v in B)==78 for a in assignments)
    assert all(sum(a[v].gadget.name=='H7_skew' for v in B)==11 for a in assignments)
    classes=[]
    for a in assignments:
        H=build_replacement(B,a)
        for representative in classes:
            if nx.vf2pp_is_isomorphic(H,representative[0]):
                representative[1]+=1
                break
        else:
            classes.append([H,1])
    assert len(classes)==6
    assert sorted(c[1] for c in classes)==[6,6,6,6,12,12]
    assert all(not nx.check_planarity(c[0])[0] for c in classes)


def test_h15_gadget_and_32_cycle_restriction():
    from mixed_gadget_solver import exoo_h15
    from mixed_gadget_census import all_bases
    H=exoo_h15()
    assert H.size==15 and H.internal_cycle_lengths == frozenset({3,5,6,7,9,10,11,12,13,14,15})
    assert sorted(tuple(sorted(x)) for x in H.pair_paths)==[
        tuple(range(3,15)), tuple(range(3,15)), tuple(range(5,15))]
    options=choice_library(gadgets_from_catalog(include_h15=True))
    assert len(options)==9
    # Exact negative result across all 27 bases even when H15 is allowed.
    for n in (4,6,8,10):
        for B in all_bases()[n]:
            assert next(search_assignments(B,options,{4,8,16,32}),None) is None


def test_six_class_78_family_artifact():
    from exoo78_family import family
    from exoo78_witness import BASE_GRAPH6
    data=family()
    disk=json.loads(Path(__file__).with_name('exoo78_family.json').read_text())
    assert data==disk
    B=nx.from_graph6_bytes(BASE_GRAPH6.encode())
    names={x.name:x for x in choice_library(gadgets_from_catalog())}
    assert len(disk['classes'])==6
    for cls in disk['classes']:
        a={int(v):names[name] for v,name in cls['choices'].items()}
        H=build_replacement(B,a)
        for length in (32,64):
            C=[tuple(v) for v in cls[f'cycle_{length}']]
            assert len(C)==length and len(set(C))==length
            assert all(H.has_edge(C[i],C[(i+1)%length]) for i in range(length))
