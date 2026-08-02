import hashlib
import json
from collections import Counter
from pathlib import Path

import networkx as nx

from verifier.type_b_equality_order import (
    EXPECTED_EXTREMAL_COUNT,
    EXPECTED_MCKAY_SHA256,
)


ROOT = Path(__file__).resolve().parents[1]


def test_equality_degree_and_edge_arithmetic():
    # H has sixteen ordinary internal vertices of degree at least three and
    # the gateway/y pair of degree at least two.
    assert (16 * 3 + 2 * 2 + 1) // 2 == 26
    assert 27 + 1 + 27 + 1 + 1 == 57


def test_authoritative_extremal_input_and_degree_histogram():
    path = ROOT / "data/c48_n18e27.s6"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED_MCKAY_SHA256
    histogram = Counter()
    lines = path.read_bytes().splitlines()
    assert len(lines) == EXPECTED_EXTREMAL_COUNT
    for line in lines:
        graph = nx.from_sparse6_bytes(line)
        assert graph.number_of_nodes() == 18
        assert graph.number_of_edges() == 27
        histogram[sum(degree == 2 for _, degree in graph.degree())] += 1
    assert dict(sorted(histogram.items())) == {
        3: 18,
        4: 103,
        5: 220,
        6: 187,
        7: 39,
        8: 2,
        9: 1,
    }


def test_frozen_equality_order_certificate():
    certificate = json.loads(
        (ROOT / "data/type_b_equality_order_certificate.json").read_text()
    )
    assert certificate["near_extremal_26"]["dfs_route"]["graphs_checked"] == 101546
    assert certificate["near_extremal_26"]["networkx_route"]["graphs_checked"] == 101546
    assert certificate["near_extremal_26"]["dfs_route"]["c8_free_graphs"] == 0
    assert certificate["near_extremal_26"]["networkx_route"]["c8_free_graphs"] == 0
    assert certificate["extremal_27"][
        "graphs_with_at_most_two_degree_two_vertices"
    ] == 0
    assert certificate["candidate_bridge_remainders"] == 0
    assert certificate["extendable_equality_path_union_cores"] == 0
