#!/usr/bin/env python3
"""Independent finite checks for the general square-family bridge theorem.

The mathematical proof for k>=7 (and arbitrary t with k>4t+2) is incidence
counting. Enumeration appears ONLY for finite exceptions k=4,5,6, the isolated
Petersen base and a counterexample to the path-only bridge-repair conjecture.
"""
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random

import networkx as nx
import pytest

from bridge_reduction import (
    add_edge_bridge, cycle_is_valid, enumerate_dyadic_root_witnesses,
    is_dyadic, edge,
)
from bridge_family_robustness import (
    bridge_sequence, cubic_ladder, disjoint_edge_pairs,
    guaranteed_root_robust_after_bridges, incidence_counts,
    ladder_square_family, square_survival_depth,
    surviving_original_cycle, weighted_incidence,
)
from prime_pole_obstructions import (
    dyadic_cycle_avoiding_vertex, is_cyclically_four_edge_connected_cubic,
    verify_dyadic_cycle,
)


def test_square_family_structural_incidence_all_k():
    for k in range(4, 27):
        for mobius in (False, True):
            G = cubic_ladder(k, mobius=mobius)
            F = ladder_square_family(k, mobius=mobius)
            assert len(F) == k
            assert all(len(C) == 4 and cycle_is_valid(G, C) for C in F)
            vc, ec = incidence_counts(F)
            assert set(vc) == set(G)
            assert set(vc.values()) == {2}
            assert max(ec.values()) == 2
            W, alpha, beta = weighted_incidence(F, [Fraction(1, k)]*k)
            assert (W, alpha, beta) == (1, Fraction(2, k), Fraction(2, k))
            for t in range(0, 7):
                assert guaranteed_root_robust_after_bridges(F, [1]*k, t) == (k > 4*t+2)
            assert square_survival_depth(k) == (k-3)//4


@pytest.mark.parametrize('k', (4,5,6))
@pytest.mark.parametrize('mobius', (False, True))
def test_all_one_step_bridges_of_small_ladders(k, mobius):
    """Exhaustive over edges and every old/new root for the finite exceptions."""
    G = cubic_ladder(k, mobius=mobius)
    checked = 0
    for e, f in disjoint_edge_pairs(G):
        H, x, y = add_edge_bridge(G, e, f)
        assert all(H.degree(v) == 3 for v in H)
        # Independent oracle: directed NetworkX simple-cycle enumeration.
        independent = [set(C) for C in nx.simple_cycles(nx.DiGraph(H))
                       if is_dyadic(len(C))]
        for r in H:
            assert any(r not in C for C in independent), (k, mobius, e, f, r)
            witness = dyadic_cycle_avoiding_vertex(H, r)
            assert witness is not None, (k, mobius, e, f, r)
            assert verify_dyadic_cycle(H, witness, r)
        checked += 1
    assert checked == (3*k * (3*k-1)//2 - 3*(2*k))  # pairs sharing endpoint


def test_every_single_bridge_of_petersen_is_root_robust():
    G = nx.petersen_graph()
    checked = 0
    for e, f in disjoint_edge_pairs(G):
        H, _, _ = add_edge_bridge(G, e, f)
        independent = [set(C) for C in nx.simple_cycles(nx.DiGraph(H))
                       if is_dyadic(len(C))]
        for r in H:
            assert any(r not in C for C in independent)
            witness = dyadic_cycle_avoiding_vertex(H, r)
            assert witness is not None
            assert verify_dyadic_cycle(H, witness, r)
        checked += 1
    assert checked == 75


def test_multi_bridge_bound_and_new_roots():
    for k, t in ((12,2), (15,3), (20,4)):
        for mobius in (False, True):
            G = cubic_ladder(k, mobius=mobius)
            F = ladder_square_family(k, mobius=mobius)
            rng = random.Random(10*k+int(mobius))
            H = G.copy()
            for j in range(t):
                choices = list(disjoint_edge_pairs(H))
                e,f = choices[rng.randrange(len(choices))]
                H,_,_ = add_edge_bridge(H,e,f)
            for r in H:
                C = surviving_original_cycle(H, F, r)
                assert C is not None, (k,t,mobius,r)
                assert cycle_is_valid(H, C, r) and is_dyadic(len(C))


def test_path_only_bridge_repair_is_false_in_prime_family():
    data = json.loads((Path(__file__).parent/'shift_only_bridge_certificate.json').read_text())
    G = nx.from_graph6_bytes(data['base_graph6'].encode())
    e, f = data['bridge_edges']
    root = data['old_root']
    H,x,y = add_edge_bridge(G,e,f)
    assert len(G) == 12 and len(H) == 14
    assert is_cyclically_four_edge_connected_cubic(G)
    assert is_cyclically_four_edge_connected_cubic(H)
    assert all(dyadic_cycle_avoiding_vertex(G, r) is not None for r in G)
    assert all(dyadic_cycle_avoiding_vertex(H, r) is not None for r in H)

    # Independent child graph oracle: none of its rooted dyadic cycles use xy.
    D = nx.DiGraph(H)
    D.remove_node(root)
    child_dyadic = [tuple(C) for C in nx.simple_cycles(D) if is_dyadic(len(C))]
    assert child_dyadic
    assert all(not any(
        v == x and (C[(i+1)%len(C)] == y or C[(i-1)%len(C)] == y)
        for i, v in enumerate(C)) for C in child_dyadic)

    witness = data['base_cycle']
    assert cycle_is_valid(G, witness, root) and len(witness) == 7
    assert sum(edge(witness[j], witness[(j+1)%len(witness)]) in (edge(*e), edge(*f))
               for j in range(len(witness))) == 1
    predicted = list(enumerate_dyadic_root_witnesses(G, e, f, root))
    assert predicted and all(w.kind == 'lift' and w.shift == 1 and w.length == 8
                             for w in predicted)
    assert any(tuple(w.base_object) == tuple(witness) for w in predicted)
    assert all(cycle_is_valid(H, w.expanded_cycle, root) for w in predicted)


def test_invalid_depth_rejected():
    with pytest.raises(ValueError):
        guaranteed_root_robust_after_bridges([(0,1,2,3)], [1], -1)
    with pytest.raises(ValueError):
        cubic_ladder(3)


def test_all_bridges_from_K4_produce_root_robust_K33():
    G = nx.complete_graph(4)
    assert len(list(disjoint_edge_pairs(G))) == 3
    for e, f in disjoint_edge_pairs(G):
        H, _, _ = add_edge_bridge(G, e, f)
        assert nx.is_isomorphic(H, nx.complete_bipartite_graph(3, 3))
        assert all(dyadic_cycle_avoiding_vertex(H, r) is not None for r in H)


def test_three_connectivity_alone_does_not_ensure_bridge_stability():
    data = json.loads((Path(__file__).parent /
                       'nonprime_bridge_failure_certificate.json').read_text())
    G = nx.from_graph6_bytes(data['base_graph6'].encode())
    e, f = data['bridge_edges']
    H, x, y = add_edge_bridge(G, e, f)
    r = data['old_root']
    assert nx.is_isomorphic(G, nx.circular_ladder_graph(3))
    assert all(d == 3 for _, d in G.degree())
    assert all(d == 3 for _, d in H.degree())
    assert nx.node_connectivity(G) == nx.node_connectivity(H) == 3
    assert not is_cyclically_four_edge_connected_cubic(G)
    assert not is_cyclically_four_edge_connected_cubic(H)
    assert all(dyadic_cycle_avoiding_vertex(G, v) is not None for v in G)
    assert dyadic_cycle_avoiding_vertex(H, r) is None
    # Independent graph-level exhaustive oracle for the specified failure.
    assert not any(r not in C and is_dyadic(len(C))
                   for C in nx.simple_cycles(nx.DiGraph(H)))
