"""Independent graph-level checks of the exact three-cut transfer theorem."""
from itertools import permutations

import networkx as nx
import pytest

from partial_triangle_expansion import cycles
from three_cut_transfer import (
    PoleSignature, cap_pole, cut_mean_obstruction, cut_width_obstruction,
    cycle_lengths_from_signatures, forbidden_crossing_lengths, glue_poles,
    is_dyadic, no_dyadic_crossing_gap_witness, pole_signature,
    split_independent_cyclic_three_cut, three_sum_of_cubic_graphs,
    verify_transfer,
)


def test_prism_3_cut_exact_spectrum_and_width_inconclusive():
    G,cut=three_sum_of_cubic_graphs(nx.complete_graph(4),0,nx.complete_graph(4),0)
    split=split_independent_cyclic_three_cut(G,cut)
    assert {len(split.A),len(split.B)}=={3}
    sig_a=pole_signature(split.A,split.port_A)
    sig_b=pole_signature(split.B,split.port_B)
    assert sig_a.pair_paths==(frozenset({1,2}),)*3
    assert sig_b.pair_paths==(frozenset({1,2}),)*3
    assert sig_a.width_weights()==(-1,-1,-1)
    assert cut_width_obstruction(sig_a,sig_b) is None
    assert not cut_mean_obstruction(sig_a,sig_b)
    assert forbidden_crossing_lengths(sig_a,sig_b)=={4}
    assert no_dyadic_crossing_gap_witness(sig_a,sig_b) is None
    assert cycle_lengths_from_signatures(sig_a,sig_b)=={3,4,5,6}
    assert verify_transfer(G,cut)
    assert nx.is_isomorphic(G,glue_poles(split))
    assert nx.is_isomorphic(cap_pole(split.A,split.port_A),nx.complete_graph(4))


def test_exact_transfer_all_six_permutations_petersen_plus_k4():
    for p in permutations((0,1,2)):
        G,cut=three_sum_of_cubic_graphs(nx.petersen_graph(),0,nx.complete_graph(4),0,p)
        assert nx.is_connected(G)
        assert nx.edge_connectivity(G)==3
        assert verify_transfer(G,cut)


def test_exact_transfer_two_petersen_graphs():
    G,cut=three_sum_of_cubic_graphs(nx.petersen_graph(),0,nx.petersen_graph(),0)
    split=split_independent_cyclic_three_cut(G,cut)
    assert nx.is_isomorphic(cap_pole(split.A,split.port_A), nx.petersen_graph())
    assert nx.is_isomorphic(cap_pole(split.B,split.port_B), nx.petersen_graph())
    assert verify_transfer(G,cut)


def test_bad_cut_rejected_and_non_cyclic_not_promoted():
    G,cut=three_sum_of_cubic_graphs(nx.complete_graph(4),0,nx.complete_graph(4),0)
    with pytest.raises(ValueError):
        split_independent_cyclic_three_cut(G,tuple(G.edges())[:3])
    with pytest.raises(ValueError):
        split_independent_cyclic_three_cut(nx.complete_graph(4),[(0,1),(0,2),(0,3)])
    with pytest.raises(ValueError):
        split_independent_cyclic_three_cut(G,[cut[0],cut[0],cut[1]])


def test_interval_gap_witness_and_mean_certificate():
    # Synthetic three-port signatures, deliberately separate from existence
    # claims about cubic graph gadgets. These verify the algebraic criteria.
    A=PoleSignature(frozenset({5}), (frozenset({3,4,5,6}),)*3)
    B=PoleSignature(frozenset({7}), (frozenset({3,4,5,6}),)*3)
    assert A.width_weights()==(-1,-1,-1)
    assert not cut_mean_obstruction(A,B)
    assert forbidden_crossing_lengths(A,B)=={8}
    assert no_dyadic_crossing_gap_witness(A,B) is None
    C=PoleSignature(frozenset({5}), (frozenset({4,5,6,7,8}),)*3)
    assert C.width_weights()==(-1,-1,-1)
    D=PoleSignature(frozenset({5}), (frozenset({3,4,5,6,7,8,9}),)*3)
    assert D.width_weights()==(2,2,2)
    assert cut_mean_obstruction(C,D)
    cert=cut_width_obstruction(C,D)
    assert cert is not None and is_dyadic(cert[-1])
    # E and F cross in [9,15], strictly between powers 8 and 16.
    E=PoleSignature(frozenset(), (frozenset(range(3,6)),)*3)
    F=PoleSignature(frozenset(), (frozenset(range(4,9)),)*3)
    gap=no_dyadic_crossing_gap_witness(E,F)
    assert gap is not None and all((lo,hi,lp,up)==(9,15,8,16)
                                   for _,_,lo,hi,lp,up in gap)
    assert not forbidden_crossing_lengths(E,F)


def test_noninterval_paths_do_not_trigger_width_shortcut():
    A=PoleSignature(frozenset(),(frozenset({3,7}),)*3)
    B=PoleSignature(frozenset(),(frozenset({2,6}),)*3)
    assert A.width_weights() is None
    assert cut_width_obstruction(A,B) is None
    assert no_dyadic_crossing_gap_witness(A,B) is None
    assert forbidden_crossing_lengths(A,B)==set()


def test_7_vertex_skew_spectrum_obstruction_all_orientations():
    from mixed_gadget_solver import gadgets_from_catalog
    from three_cut_transfer import dyadic_cut_cycle_witness
    skew=next(g for g in gadgets_from_catalog() if g.name=='H7_skew')
    pole=nx.from_graph6_bytes(skew.graph6.encode())
    G=cap_pole(pole,skew.ports)
    cap=('__cap__',)
    for p in permutations((0,1,2)):
        joined,cut=three_sum_of_cubic_graphs(G,cap,G,cap,p)
        split=split_independent_cyclic_three_cut(joined,cut)
        sig_a=pole_signature(split.A,split.port_A)
        sig_b=pole_signature(split.B,split.port_B)
        assert sum(sig_a.width_weights())==1
        assert sum(sig_b.width_weights())==1
        assert cut_mean_obstruction(sig_a,sig_b)
        bound=cut_width_obstruction(sig_a,sig_b)
        assert bound is not None
        witness=dyadic_cut_cycle_witness(split)
        assert witness is not None
        assert is_dyadic(witness.length)
        assert witness.length in {len(C) for C in cycles(joined)}


def test_gapped_spectra_certified_by_contained_interval():
    from three_cut_transfer import cut_subinterval_mean_obstruction, cut_subinterval_width_obstruction
    A=PoleSignature(frozenset(),(frozenset({2,3,4,5,6,10}),)*3)
    B=PoleSignature(frozenset(),(frozenset({2,3,4,5,6,20}),)*3)
    assert A.width_weights() is None and B.width_weights() is None
    assert A.best_contiguous_subinterval(0,1)==(2,6)
    assert A.best_subinterval_weights()==(1,1,1)
    assert B.best_subinterval_weights()==(1,1,1)
    assert cut_subinterval_mean_obstruction(A,B)
    cert=cut_subinterval_width_obstruction(A,B)
    assert cert is not None and cert[-1]==8
    assert 8 in forbidden_crossing_lengths(A,B)
