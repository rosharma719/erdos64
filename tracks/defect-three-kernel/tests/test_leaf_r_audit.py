import json
from pathlib import Path

import networkx as nx

from verifier.leaf_r_patterns import canonical_cycle, cycle_pattern
from verifier.leaf_r_replacement_search import adjacency_masks, has_c4, has_cycle


ROOT = Path(__file__).resolve().parents[1]


def test_cycle_helpers_distinguish_c4_and_c8():
    c4 = nx.cycle_graph(4)
    c8 = nx.cycle_graph(8)
    path8 = nx.path_graph(8)

    assert canonical_cycle(c4, 4) == (0, 1, 2, 3)
    assert canonical_cycle(c8, 4) is None
    assert canonical_cycle(c8, 8) == tuple(range(8))
    assert has_c4(adjacency_masks(c4))
    assert not has_c4(adjacency_masks(c8))
    assert has_cycle(adjacency_masks(c8), 8)
    assert not has_cycle(adjacency_masks(path8), 8)


def test_pattern_is_dihedrally_canonical():
    cycle = (0, 1, 2, 3)
    degree = {0: 3, 1: 4, 2: 3, 3: 4}
    converted = {(0, 1)}
    expected = cycle_pattern(cycle, {0, 2}, degree, converted)

    assert cycle_pattern((1, 2, 3, 0), {0, 2}, degree, converted) == expected
    assert cycle_pattern((0, 3, 2, 1), {0, 2}, degree, converted) == expected


def test_leaf_r_manifests_have_complete_accounting():
    patterns = json.loads(
        (ROOT / "manifests" / "leaf_r_patterns_manifest.json").read_text()
    )
    orientations = patterns["leaf_orientation_classes"]
    genuine = orientations["genuine_original_remote_R_leaf"]
    exposed = orientations["root_side_exposed_after_terminal_S_suppression"]

    assert patterns["leaf_R_records"] == 75_745
    assert genuine == {
        "records": 72_927,
        "real_edge_C4_C8_positive": 72_927,
        "real_edge_C4_C8_clean": 0,
    }
    assert exposed == {
        "records": 2_818,
        "real_edge_C4_C8_positive": 2_210,
        "real_edge_C4_C8_clean": 608,
    }
    assert sum(row["count"] for row in patterns["exact_patterns"]) == 75_745
    assert patterns["exact_patterns_required_for_full_coverage"] == 42

    replacement = json.loads(
        (ROOT / "manifests" / "leaf_r_replacement_small_manifest.json").read_text()
    )
    totals = replacement["totals"]
    assert totals["skeletons"] == 87_004
    assert totals["edge_rooted_pairs"] == 1_802_018
    assert totals["C4_free_after_parent_deletion"] == 10
    assert totals["C4_C8_free_after_parent_deletion"] == 0
