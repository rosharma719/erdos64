"""Small exact cross-checks of a non-enumerative cycle-space proof mechanism."""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import sys

import networkx as nx
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parent))
from partial_triangle_expansion import base_graph
from mixed_gadget_solver import choice_library, gadgets_from_catalog, build_replacement
from cycle_space_obstruction import (
    local_scores, cycle_basis_masks, expectation_quarters,
    choose_even_subgraph, certify, component_cycles, example_78,
)


def _options():
    return {c.name:c for c in choice_library(gadgets_from_catalog(include_h15=True))}


def test_local_width_scores_and_dominance():
    x=_options()
    assert set(x)=={
        'id:012','T3:012','H7_skew:012','H7_skew:021','H7_skew:201',
        'H7_uniform:012','H15_exoo:012','H15_exoo:102','H15_exoo:120'
    }
    K=base_graph('k4')
    for key, expected in [
        ('id:012',(-1,-1,-1)),
        ('T3:012',(-1,-1,-1)),
        ('H7_uniform:012',(1,1,1)),
    ]:
        weights=local_scores(K,{v:x[key] for v in K})[0]
        assert tuple(weights[k] for k in (3,5,6))==expected
    special=local_scores(K,{v:x['H7_skew:012'] for v in K})[0]
    assert sorted(special[k] for k in (3,5,6))==[-1,1,1]
    h15=local_scores(K,{v:x['H15_exoo:012'] for v in K})[0]
    assert sorted(h15[k] for k in (3,5,6))==[3,7,7]
    for u in x:
        if not u.startswith('H7_skew'):
            continue
        assert all(x[u].gadget.paths(x[u].permutation[i],x[u].permutation[j])
                   <= x['H7_uniform:012'].gadget.paths(i,j)
                   for i,j in ((0,1),(0,2),(1,2)))


def test_cycle_space_exact_expectation_against_all_vectors():
    x=_options()
    bases=[base_graph('k4'),nx.cubical_graph(), nx.petersen_graph()]
    keys=['id:012','T3:012','H7_skew:012','H7_skew:021',
          'H7_uniform:012','H15_exoo:120']
    for B in bases:
        B=nx.convert_node_labels_to_integers(B)
        selected={v:x[keys[(v*3+len(B))%len(keys)]] for v in B}
        scores=local_scores(B,selected)
        basis=cycle_basis_masks(B)
        total=0
        for bits in itertools.product((0,1), repeat=len(basis)):
            states={v:0 for v in B}
            for i,one in enumerate(bits):
                if one:
                    for v in B:
                        states[v]^=basis[i][v]
            total+=sum(scores[v][states[v]] for v in B)
        assert expectation_quarters(B,scores,basis)*(2**len(basis)) == 4*total
        assert expectation_quarters(B,scores,basis) == sum(
            sum(scores[v][p] for p in (3,5,6)) for v in B)


def test_all_skew_on_bridgeless_bases_forces_power():
    sk=_options()['H7_skew:012']
    for B in (base_graph('k4'), nx.cubical_graph(), nx.petersen_graph(),
              nx.random_regular_graph(3,14,seed=89)):
        B=nx.convert_node_labels_to_integers(B)
        a={v:sk for v in B}
        p=certify(B,a)
        assert p is not None
        assert p.score_sum==len(B)
        assert p.average_score_quarters==len(B)
        H=build_replacement(B,a)
        assert len(p.expanded_cycle)==p.lifted_length
        assert set(p.expanded_cycle)<=set(H)
        assert all(H.has_edge(p.expanded_cycle[i],p.expanded_cycle[(i+1)%p.lifted_length])
                   for i in range(p.lifted_length))


def test_inconclusive_does_not_claim_counterexample():
    B=base_graph('k4')
    opts=_options()
    a={v:opts['id:012'] for v in B}
    assert certify(B,a) is None   # K4 has 4-cycles anyway; only sufficient!


def test_all_six_78_graphs_get_explicit_dyadic_certificates():
    for i in range(6):
        p=example_78(i)
        assert p.score_sum==8
        assert p.average_score_quarters==8
        assert p.lifted_length in (32,64)
        assert p.min_length <= p.lifted_length <= p.max_length
        assert len(p.expanded_cycle)==len(set(p.expanded_cycle))==p.lifted_length


def test_bridge_base_uses_exact_local_distributions():
    # Subdivide an edge in each of two K4 graphs, then join the new nodes.
    # This yields a connected cubic graph with a single bridge and 10 vertices.
    A=nx.complete_graph(4)
    B=nx.relabel_nodes(nx.complete_graph(4),lambda v:v+5)
    A.remove_edge(0,1);A.add_edges_from([(0,4),(1,4)])
    B.remove_edge(5,6);B.add_edges_from([(5,9),(6,9)])
    G=nx.compose(A,B);G.add_edge(4,9)
    sk=_options()['H7_skew:012']
    scores=local_scores(G,{v:sk for v in G})
    basis=cycle_basis_masks(G)
    mean=expectation_quarters(G,scores,basis)
    total=0
    for bits in itertools.product((0,1),repeat=len(basis)):
        states={v:0 for v in G}
        for i,b in enumerate(bits):
            if b:
                for v in G:states[v]^=basis[i][v]
        total+=sum(scores[v][states[v]] for v in G)
    assert mean*2**len(basis) == 4*total
    if mean>=0:
        assert certify(G,{v:sk for v in G}) is not None


def test_edge_conditioning_strengthens_global_mean_without_search():
    B=base_graph('k4')
    opts=_options()
    # Global width score has negative mean, but an edge-conditioned cycle
    # space still has nonnegative mean and yields an actual expanded cycle.
    a={v:opts[key] for v,key in enumerate((
        'id:012','H7_uniform:012','H7_skew:012','T3:012'))}
    sc=local_scores(B,a);basis=cycle_basis_masks(B)
    assert expectation_quarters(B,sc,basis)<0
    assert certify(B,a) is None
    p=certify(B,a,conditioned_edges=True)
    assert p is not None and p.certificate_kind.startswith('edge-conditioned')
    H=build_replacement(B,a)
    assert p.lifted_length&(p.lifted_length-1)==0
    assert all(H.has_edge(p.expanded_cycle[i],p.expanded_cycle[(i+1)%p.lifted_length])
               for i in range(p.lifted_length))


def test_edge_conditioning_means_are_exact():
    from cycle_space_obstruction import rooted_affine_basis, affine_expectation_quarters
    B=nx.petersen_graph()
    basis=cycle_basis_masks(B)
    opts=_options()
    a={v:opts['H7_skew:012' if v%3 else 'T3:012'] for v in B}
    scores=local_scores(B,a)
    for e in B.edges():
        off,directions=rooted_affine_basis(B,basis,e)
        mean4=affine_expectation_quarters(B,scores,off,directions)
        total=0
        for bits in itertools.product((0,1),repeat=len(directions)):
            state=dict(off)
            for i,b in enumerate(bits):
                if b:
                    for v in B:state[v]^=directions[i][v]
            assert state[e[0]] & (1<<sorted(B.neighbors(e[0])).index(e[1]))
            total+=sum(scores[v][state[v]] for v in B)
        assert mean4 * (2**len(directions))==4*total


def test_stored_cycle_space_certificates_are_valid_independently():
    data=json.loads(Path(__file__).with_name('cycle_space_78_certificates.json').read_text())
    family=json.loads(Path(__file__).with_name('exoo78_family.json').read_text())
    B=nx.from_graph6_bytes(data['base_graph6'].encode())
    assert len(data['classes'])==len(family['classes'])==6
    opts=_options()
    for i,part in enumerate(data['classes']):
        selected={int(v):opts[name] for v,name in family['classes'][i]['choices'].items()}
        G=build_replacement(B,selected)
        chain=[tuple(a) for a in part['expanded_cycle']]
        power=part['power_of_two_length']
        assert power>=4 and power&(power-1)==0
        assert len(chain)==power==len(set(chain))
        assert all(G.has_edge(chain[j],chain[(j+1)%len(chain)])
                   for j in range(len(chain)))
        assert part['minimum_lift_length']<=power<=part['maximum_lift_length']
