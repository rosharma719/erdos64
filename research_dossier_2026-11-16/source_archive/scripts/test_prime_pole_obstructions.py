"""Unit and independently checked small-order tests of structural pass V."""
from itertools import permutations
import json
from pathlib import Path

import networkx as nx
import pytest

from three_cut_transfer import PoleSignature, pole_signature, three_sum_of_cubic_graphs, split_independent_cyclic_three_cut
from prime_pole_obstructions import (
    stride_two_runs, even_stride_score, parity_cut_certificate,
    triangle_leaf_crossing_witness, dyadic_cycle_avoiding_vertex,
    verify_dyadic_cycle, is_cyclically_four_edge_connected_cubic,
    root_robustness_violations,
)

HERE = Path(__file__).resolve().parent


def signature_of_deletion(graph: nx.Graph, v):
    other = graph.copy()
    ports = tuple(graph.neighbors(v))
    other.remove_node(v)
    return pole_signature(other, ports)


def test_stride_two_runs_retain_gaps_correctly():
    assert stride_two_runs({2, 4, 8, 10, 11, 13}, 0) == ((2, 4), (8, 10))
    assert stride_two_runs({2, 4, 8, 10, 11, 13}, 1) == ((11, 13),)
    assert stride_two_runs({1, 3}, 0) == ()
    with pytest.raises(ValueError):
        stride_two_runs({2, 4}, 2)


def test_old_invariant_erases_even_paths_but_parity_score_retains_them():
    examples = (
        (nx.complete_bipartite_graph(3, 3), -9, -3),
        (nx.cubical_graph(), -9, 3),
        (nx.heawood_graph(), -15, 9),
    )
    for g, old, new in examples:
        sig = signature_of_deletion(g, next(iter(g)))
        assert all(all(x % 2 == 0 for x in st) for st in sig.pair_paths)
        assert sum(sig.best_subinterval_weights()) == old
        assert even_stride_score(sig) == new


def test_parity_score_detects_cut_which_old_mean_does_not():
    A = signature_of_deletion(nx.complete_bipartite_graph(3, 3), 0)
    B = signature_of_deletion(nx.cubical_graph(), 0)
    assert sum(A.best_subinterval_weights()) + sum(B.best_subinterval_weights()) == -18
    assert even_stride_score(A) + even_stride_score(B) == 0
    cert = parity_cut_certificate(A, B, use_mean=True)
    assert cert is not None and cert.dyadic_length == 8
    for p in permutations((0, 1, 2)):
        g, cut = three_sum_of_cubic_graphs(nx.complete_bipartite_graph(3, 3), 0,
                                           nx.cubical_graph(), 0, p)
        split = split_independent_cyclic_three_cut(g, cut)
        a, b = pole_signature(split.A, split.port_A), pole_signature(split.B, split.port_B)
        c = parity_cut_certificate(a, b, use_mean=True)
        assert c is not None and c.dyadic_length == 8
        # Verify an explicit crossed cycle, independently of score arithmetic.
        i, j = c.terminal_pair
        witness_a = next(x for x in nx.all_simple_paths(split.A, split.port_A[i], split.port_A[j])
                         if len(x) - 1 == c.interval_a[0])
        witness_b = next(x for x in nx.all_simple_paths(split.B, split.port_B[j], split.port_B[i])
                         if len(x) - 1 == c.dyadic_length - 2 - c.interval_a[0])
        cycle = tuple(witness_a + witness_b)
        assert verify_dyadic_cycle(g, cycle)


def test_parity_score_is_sufficient_not_necessary():
    A = signature_of_deletion(nx.complete_bipartite_graph(3, 3), 0)
    assert even_stride_score(A) == -3
    assert parity_cut_certificate(A, A, use_mean=True) is None
    cert = parity_cut_certificate(A, A)
    assert cert is not None and cert.dyadic_length == 8


def test_parity_certificate_does_not_infer_missing_lengths():
    A = PoleSignature(frozenset(), (frozenset({2, 6}),) * 3)
    B = PoleSignature(frozenset(), (frozenset({2, 6}),) * 3)
    assert even_stride_score(A) == -9
    # The attainable crossed lengths are {6,10,14}; none is dyadic.
    assert parity_cut_certificate(A, B) is None
    assert parity_cut_certificate(A, B, use_mean=True) is None
    C = PoleSignature(frozenset(), (frozenset({3, 5, 7}),) * 3)
    assert parity_cut_certificate(A, C) is None
    assert parity_cut_certificate(C, C, parity=1) is not None  # 3+3+2=8


def test_triangle_leaf_exact_missing_predecessor_rule():
    triangle = signature_of_deletion(nx.complete_graph(4), 0)
    assert triangle.pair_paths == (frozenset({1, 2}),) * 3
    for G in (nx.complete_graph(4), nx.petersen_graph(), nx.heawood_graph()):
        sig = signature_of_deletion(G, 0)
        hit = triangle_leaf_crossing_witness(sig)
        assert hit is not None
        (i, j), path_length, k = hit
        assert path_length in {k-3, k-4}
        assert path_length in sig.paths(i, j)
        assert k & (k-1) == 0


def test_root_robustness_is_stronger_than_prime_cycle_existence():
    K4 = nx.complete_graph(4)
    assert root_robustness_violations(K4) == tuple(K4.nodes())
    for H in (nx.complete_bipartite_graph(3, 3), nx.petersen_graph(),
              nx.heawood_graph(), nx.dodecahedral_graph()):
        assert root_robustness_violations(H) == ()
        for v in H:
            witness = dyadic_cycle_avoiding_vertex(H, v)
            assert witness is not None and verify_dyadic_cycle(H, witness, v)


def test_small_prime_census_falsification_check():
    # Catalogs consist of 5, 19, and 85 nonisomorphic connected cubic graphs,
    # respectively, validated in the previous research passes.
    smaller = json.loads((HERE / 'cubic_catalog_n8_n10.json').read_text())['connected_cubic']
    samples = {
        4: [nx.complete_graph(4)],
        6: [nx.circular_ladder_graph(3), nx.complete_bipartite_graph(3, 3)],
        8: [nx.from_graph6_bytes(s.encode()) for s in smaller['8']],
        10: [nx.from_graph6_bytes(s.encode()) for s in smaller['10']],
        12: [nx.from_graph6_bytes(s.encode()) for s in json.loads((HERE / 'cubic_catalog_n12.json').read_text())],
    }
    primes = {}
    for n, graphs in samples.items():
        candidates = [g for g in graphs if is_cyclically_four_edge_connected_cubic(g)]
        primes[n] = len(candidates)
        for g in candidates:
            violations = root_robustness_violations(g)
            if n == 4:
                assert violations == tuple(g.nodes())
            else:
                assert not violations
    assert primes == {4: 1, 6: 1, 8: 2, 10: 5, 12: 18}


def test_prime_hypothesis_cannot_be_extended_to_all_cubic_graphs():
    smaller = json.loads((HERE / 'cubic_catalog_n8_n10.json').read_text())['connected_cubic']
    bad = []
    for graph6 in smaller['8']:
        g = nx.from_graph6_bytes(graph6.encode())
        if root_robustness_violations(g):
            bad.append((graph6, root_robustness_violations(g)))
            assert not is_cyclically_four_edge_connected_cubic(g)
    assert len(bad) == 2
