#!/usr/bin/env python3
"""Reproducible census of simultaneous triangle expansions of all cubic n=8/10 bases.

The checked fixture contains 5/19 connected isomorphism classes. Completeness is
conditional on the published enumeration of connected cubic graphs at these orders.
"""

from collections import Counter, defaultdict
import json
from pathlib import Path

import networkx as nx

from partial_triangle_expansion import (
    independent_has_cycle_length, predicted_spectrum, triangle_expand, viable_subsets
)

HERE = Path(__file__).resolve().parent
EXPECTED_COUNTS = {8: 5, 10: 19}


def read_catalog():
    raw = json.loads((HERE / 'cubic_catalog_n8_n10.json').read_text())['connected_cubic']
    bases = {}
    for s, encoded in raw.items():
        n = int(s)
        gs = [nx.from_graph6_bytes(e.encode('ascii')) for e in encoded]
        assert len(gs) == EXPECTED_COUNTS[n]
        assert all(len(G) == n and nx.is_connected(G) and all(d == 3 for _, d in G.degree()) for G in gs)
        assert all(not nx.is_isomorphic(gs[i], gs[j]) for i in range(len(gs)) for j in range(i + 1, len(gs)))
        bases[n] = gs
    return bases


def unique_isomorphism_classes(graphs):
    classes = []
    for G in graphs:
        if all(not nx.is_isomorphic(G, H) for H in classes):
            classes.append(G)
    return classes


def run():
    bases = read_catalog()
    for n, graphs in sorted(bases.items()):
        by_order = defaultdict(list)
        subsets_by_order = Counter()
        for i, G in enumerate(graphs):
            for S in viable_subsets(G, {4, 8}):
                H = triangle_expand(G, S)
                order = len(H)
                subsets_by_order[order] += 1
                # Independent DFS oracle does not depend on the expansion formula.
                assert not independent_has_cycle_length(H, 4), (n, i, S, 4)
                assert not independent_has_cycle_length(H, 8), (n, i, S, 8)
                assert independent_has_cycle_length(H, 16), (n, i, S, 16)
                assert 16 in predicted_spectrum(G, S)
                by_order[order].append(H)
        print(f'base order {n}: {len(graphs)} connected cubic classes')
        if not by_order: print('  no 4/8-free partial expansions')
        for order, expanded_graphs in sorted(by_order.items()):
            iso = unique_isomorphism_classes(expanded_graphs)
            planar = [H for H in iso if nx.check_planarity(H)[0]]
            print(f'  expanded order {order}: labeled choices={subsets_by_order[order]}, iso classes={len(iso)}, planar classes={len(planar)}, all have C16=yes')
            if order == 24:
                assert len(iso) == len(planar) == 1
                print('  planar order-24 graph6 witness: ' + nx.to_graph6_bytes(nx.convert_node_labels_to_integers(iso[0]),header=False).decode().strip())
        if n == 8:
            assert not by_order
        if n == 10:
            assert dict(subsets_by_order) == {24: 2, 26: 9, 28: 10, 30: 1}
            assert {k: len(unique_isomorphism_classes(v)) for k,v in by_order.items()} == {24: 1, 26: 2, 28: 1, 30: 1}


if __name__ == '__main__':
    run()
