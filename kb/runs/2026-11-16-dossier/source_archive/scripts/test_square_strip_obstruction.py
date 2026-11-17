"""Independent checks of the square-strip theorem and rooted min-max witnesses."""
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx
import pytest

from bridge_reduction import add_edge_bridge
from bridge_family_robustness import cubic_ladder
from prime_pole_obstructions import is_cyclically_four_edge_connected_cubic
from square_strip_obstruction import (
    canonical_square, squares, square_edges, square_intersection_graph, square_strips,
    rooted_square_forest, rooted_square_minmax, square_survival_bound,
    untouched_square_after_bridges,
)

DIR = Path(__file__).resolve().parent


def complete_small_prime_catalog():
    catalog = json.loads((DIR/'cubic_catalog_n8_n10.json').read_text())['connected_cubic']
    for order in ('8','10'):
        for g6 in catalog[order]:
            G = nx.from_graph6_bytes(g6.encode())
            if is_cyclically_four_edge_connected_cubic(G):
                yield G
    for g6 in json.loads((DIR/'cubic_catalog_n12.json').read_text()):
        G = nx.from_graph6_bytes(g6.encode())
        if is_cyclically_four_edge_connected_cubic(G):
            yield G


def brute_root_square_transversal(G, root):
    rootfree = [set(square_edges(C)) for C in squares(G) if root not in C]
    if not rootfree:
        return 0
    E = [frozenset(e) for e in G.edges()]
    for k in range(1, len(E)+1):
        for selection in combinations(E,k):
            if all(any(e in C for e in selection) for C in rootfree):
                return k
    raise AssertionError('impossible: each square has an edge')


def test_cube_exception():
    G = nx.cubical_graph()
    S = squares(G)
    assert len(S)==6
    assert max(Counter(v for C in S for v in C).values())==3
    assert max(dict(square_intersection_graph(G).degree()).values()) > 2


def test_square_strip_classification_all_prime_catalogs():
    counts = Counter()
    for G in complete_small_prime_catalog():
        n=len(G)
        S=squares(G)
        oracle=tuple(sorted(set(canonical_square(tuple(C)) for C in nx.simple_cycles(G) if len(C)==4)))
        assert S==oracle
        counts[n]+=1
        if n==8 and nx.is_isomorphic(G,nx.cubical_graph()):
            continue
        assert max(Counter(v for C in S for v in C).values(),default=0)<=2
        assert max(Counter(e for C in S for e in square_edges(C)).values(),default=0)<=2
        H=square_intersection_graph(G)
        assert all(d<=2 for _,d in H.degree())
        assert all(len(H[u][v]['shared_edges'])==1 for u,v in H.edges())
        strips=square_strips(G)
        for strip in strips:
            k=len(strip['squares'])
            if strip['is_cycle']:
                assert k>=4
                assert strip['vertices']==frozenset(G)
                assert not strip['boundary_edges']
            else:
                assert len(strip['vertices'])==2*k+2
                assert len(strip['boundary_edges'])==4
        for r in G:
            if n>=10:
                value,packing,cover=rooted_square_minmax(G,r)
                assert value==brute_root_square_transversal(G,r)
                assert len(packing)==len(cover)==value
                assert not any(rooted_square_forest(G,r).subgraph(c).number_of_edges() != len(c)-1 for c in nx.connected_components(rooted_square_forest(G,r)))
    assert counts == Counter({8:2,10:5,12:18})


def test_unbounded_ladder_minmax_certificates():
    for k in (4,5,7,10):
        for twisted in (False,True):
            G=cubic_ladder(k,mobius=twisted)
            for root in range(2*k):
                if k==4 and not twisted:  # Q8 is the exceptional cube
                    continue
                value,packing,cover=rooted_square_minmax(G,root)
                assert value==(k-1)//2  # ceil((k-2)/2)
                assert all(root not in C for C in packing)
                assert all(set(C).isdisjoint(D) for C,D in combinations(packing,2))
                assert all(any(e in square_edges(C) for e in cover)
                           for C in squares(G) if root not in C)


def test_square_rich_non_ladder_prime_example():
    G=cubic_ladder(9)
    H,x,y=add_edge_bridge(G,(0,1),(4,5))
    H=nx.convert_node_labels_to_integers(H)
    assert len(H)==20 and is_cyclically_four_edge_connected_cubic(H)
    assert len(squares(H))==7
    assert sorted(len(s['squares']) for s in square_strips(H))==[3,4]
    assert square_survival_bound(len(squares(H)),1)
    for root in H:
        val,pack,cover=rooted_square_minmax(H,root)
        assert val>=3  # Any two deleted edges miss a root-free square


def test_square_counting_depth_bound_and_explicit_witness():
    G=cubic_ladder(12)
    family=squares(G)
    # Destroy two original upper-rim edges at each step.  We verify the
    # certificate using the actual surviving original graph edges.
    H=G.copy()
    for t,(a,b) in enumerate(((0,1),(4,5),(8,9)),start=1):
        # use a second lower-rim edge to make a bridge; each bridge can
        # destroy at most four original squares
        H,_,_=add_edge_bridge(H,(a,b),(a+12,b+12))
        assert square_survival_bound(len(family),t) == (len(family)>4*t+2)
        if square_survival_bound(len(family),t):
            for root in H:
                assert untouched_square_after_bridges(H,family,[root],[])


def test_invalid_formula_on_generic_graph_not_silently_applied():
    cube=nx.cubical_graph()
    with pytest.raises(ValueError):
        rooted_square_minmax(cube,0)


def test_exact_four_terminal_strip_spectra_and_constructive_paths():
    from square_strip_obstruction import FOUR_PORTS, ladder_four_pole_spectrum, ladder_four_pole_path
    for k in range(1,7):
        graph=nx.grid_2d_graph(2,k+1)
        ports={'LT':(0,0),'LB':(1,0),'RT':(0,k),'RB':(1,k)}
        for u,v in combinations(FOUR_PORTS,2):
            predicted=set(ladder_four_pole_spectrum(k,u,v))
            independently={len(p)-1 for p in nx.all_simple_paths(graph,ports[u],ports[v])}
            assert predicted==independently,(k,u,v,predicted,independently)
            for length in predicted:
                path=ladder_four_pole_path(k,u,v,length)
                assert len(path)-1==length
                assert all(graph.has_edge(a,b) for a,b in zip(path,path[1:]))


def test_six_squares_in_two_strips_force_a_second_bridge_to_keep_a_square():
    G=cubic_ladder(10)
    H,_,_=add_edge_bridge(G,(0,10),(5,15))
    H=nx.convert_node_labels_to_integers(H)
    assert is_cyclically_four_edge_connected_cubic(H)
    assert len(squares(H))==6
    assert sorted(len(s['squares']) for s in square_strips(H))==[3,3]
    tau=[rooted_square_minmax(H,r)[0] for r in H]
    assert min(tau)==3  # strictly stronger than the s>6 count criterion
    family=squares(H)
    # Independent verification: all valid next bridge edge pairs preserve a
    # 4-cycle for every old/new root, without using the min-max algorithm.
    for e,f in combinations(H.edges(),2):
        if set(e)&set(f):
            continue
        damaged={frozenset(e),frozenset(f)}
        survivors=[C for C in family if not square_edges(C)&damaged]
        assert survivors
        assert all(any(root not in C for C in survivors) for root in H)


def test_22_vertex_certificate_reproduces_graph_and_transversals():
    cert=json.loads((DIR/'square_strip_22_certificate.json').read_text())
    graph=nx.from_graph6_bytes(cert['graph6'].encode())
    assert len(graph)==cert['order']==22
    assert graph.number_of_edges()==cert['edges']==33
    assert is_cyclically_four_edge_connected_cubic(graph)
    assert [list(C) for C in squares(graph)]==cert['canonical_squares']
    assert sorted(len(s['squares']) for s in square_strips(graph))==cert['strip_lengths']
    assert {str(r):rooted_square_minmax(graph,r)[0] for r in graph}==cert['rooted_square_transversal']
    assert min(rooted_square_minmax(graph,r)[0] for r in graph)==3
