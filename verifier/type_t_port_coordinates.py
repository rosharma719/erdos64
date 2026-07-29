#!/usr/bin/env python3
"""Symbolic coordinate system for the Type-T port core (``build_core``).

``build_core(j, a, c)`` already encodes a full symbolic addressing scheme in
its vertex *labels*: 13 fixed anchor vertices (``ANCHORS``) and 19 named,
subdivided paths between them, with every internal subdivision vertex
literally labeled ``f"{path_name}:{index}"`` (``add_path`` in
``type_t_port_core_export.py``). This module formalizes that labeling into a
small, documented, machine-checkable API:

* ``parse_label`` -- label -> ``Anchor(name)`` or ``PathPos(path, index)``.
* ``PATH_SPEC`` -- for every one of the 19 paths, its left/right anchor and
  a length formula in terms of ``(Y, a, c)``. This dict *is* the complete
  symbolic description of the core's topology: the topology (which anchors
  a path connects) never changes with ``j``; only 4 of the 19 length
  formulas actually depend on ``Y``/``a``/``c`` (``GROWING_PATHS``).
* ``symbolic_adjacent`` -- decide adjacency of two labels from the label
  strings and ``(j, a, c)`` alone, without ever materializing ``build_core``.
* ``distance_to_nearest_anchor`` -- for a path-internal vertex, the graph
  distance (which, for internal vertices, is realized entirely within their
  own path -- see ``PROOF`` below) to the nearer of its two bounding anchors.
* ``anchor_skeleton`` -- the 13-node, 19-edge weighted multigraph obtained by
  contracting every path to a single weighted edge; used for boundary-case
  (near-anchor) reasoning where a short core path can leave the branch it
  started on.

## PROOF: internal-vertex locality

Every vertex label of the form ``f"{path}:{index}"`` (``1 <= index <=
length(path)-1``) has degree exactly 2 in the bare core: `add_path` adds
edges only along the path's own vertex sequence, and no other call in
``build_core`` ever names a ``f"{path}:{index}"`` label (each path name is
used in exactly one ``add_path`` call, and internal names are freshly
allocated by ``vertex()`` the first time they occur, so no two paths share
an internal vertex). Consequently the only two neighbors of a path-internal
vertex are its two immediate predecessors/successors along that same path,
and a simple path leaving the vertex in one direction must reach the
corresponding end anchor before it can reach any other part of the graph.
This is exactly why ``distance_to_nearest_anchor`` needs no global shortest
path computation: it is ``min(index, length - index)``, checked below by
brute-force all-pairs BFS on every tested instance (``verify_roundtrip``).
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Union

from type_t_port_core_export import ANCHORS, PortCore, build_core, valid_parameters


ANCHOR_SET = frozenset(ANCHORS)

# name -> (left_anchor, right_anchor, length_formula(Y, a, c))
PATH_SPEC: dict[str, tuple[str, str, "callable"]] = {
    "prefix_AC": ("z0", "w_AC", lambda Y, a, c: 1),
    "A_left": ("w_AC", "r_x", lambda Y, a, c: a - 1),
    "A_middle": ("r_x", "s_x", lambda Y, a, c: 7),
    "A_right": ("s_x", "xprime", lambda Y, a, c: 4 * Y - 8 - a),
    "C_left": ("w_AC", "r_y", lambda Y, a, c: c - 1),
    "C_middle": ("r_y", "s_y", lambda Y, a, c: 7),
    "C_right": ("s_y", "yprime", lambda Y, a, c: Y - 8 - c),
    "prefix_BD": ("z0", "w_BD", lambda Y, a, c: 1),
    "B_right": ("w_BD", "xprime", lambda Y, a, c: 3),
    "D_right": ("w_BD", "yprime", lambda Y, a, c: 3),
    "z0x": ("z0", "x", lambda Y, a, c: 1),
    "xxprime": ("x", "xprime", lambda Y, a, c: 1),
    "z0y": ("z0", "y", lambda Y, a, c: 1),
    "yyprime": ("y", "yprime", lambda Y, a, c: 1),
    "xy": ("x", "y", lambda Y, a, c: 1),
    "u_x_r_x": ("u_x", "r_x", lambda Y, a, c: 1),
    "u_x_s_x": ("u_x", "s_x", lambda Y, a, c: 1),
    "u_y_r_y": ("u_y", "r_y", lambda Y, a, c: 1),
    "u_y_s_y": ("u_y", "s_y", lambda Y, a, c: 1),
}

# The only 4 paths whose length formula actually depends on Y/a/c. All other
# 15 paths have a length that is a fixed integer constant for every legal
# (j, a, c). This is the formal version of the task's "only 4 of the 19
# paths grow with j/a/c" claim.
GROWING_PATHS = frozenset({"A_left", "A_right", "C_left", "C_right"})

# The two "branch families": every growing path belongs to exactly one.
FAMILY_OF_PATH = {
    "A_left": "A", "A_middle": "A", "A_right": "A",
    "C_left": "C", "C_middle": "C", "C_right": "C",
}


@dataclass(frozen=True)
class Anchor:
    name: str


@dataclass(frozen=True)
class PathPos:
    path: str
    index: int  # 1 <= index <= length-1 (internal vertex)


Coord = Union[Anchor, PathPos]


def parse_label(label: str) -> Coord:
    if label in ANCHOR_SET:
        return Anchor(label)
    path, _, index_str = label.rpartition(":")
    if not path or path not in PATH_SPEC:
        raise ValueError(f"unrecognized label {label!r}")
    return PathPos(path, int(index_str))


def path_length(path: str, j: int, a: int, c: int) -> int:
    Y = 1 << j
    _, _, formula = PATH_SPEC[path]
    return formula(Y, a, c)


def endpoints(path: str) -> tuple[str, str]:
    left, right, _ = PATH_SPEC[path]
    return left, right


def label_of(path: str, index: int, j: int, a: int, c: int) -> str:
    """Inverse of parse_label, restricted to one path: the label occupying
    coordinate `index` (0 <= index <= length) of `path`."""
    left, right = endpoints(path)
    length = path_length(path, j, a, c)
    if index == 0:
        return left
    if index == length:
        return right
    if not 0 < index < length:
        raise ValueError(f"index {index} out of range for {path} (length {length})")
    return f"{path}:{index}"


def label_positions(label: str, j: int, a: int, c: int) -> list[tuple[str, int]]:
    """All (path, index) positions `label` occupies. A path-internal label
    occupies exactly one; an anchor occupies one per incident path (0 or
    length depending on which end)."""
    coord = parse_label(label)
    if isinstance(coord, PathPos):
        return [(coord.path, coord.index)]
    positions = []
    for path, (left, right, formula) in PATH_SPEC.items():
        if left == label:
            positions.append((path, 0))
        if right == label:
            positions.append((path, path_length(path, j, a, c)))
    return positions


def symbolic_adjacent(label_u: str, label_v: str, j: int, a: int, c: int) -> bool:
    """Two labels are adjacent in the bare core iff they occupy the same
    named path at indices differing by exactly 1. This is the *complete*
    symbolic adjacency rule: it needs no reference to a materialized
    ``PortCore``."""
    if label_u == label_v:
        return False
    pos_u = dict(label_positions(label_u, j, a, c))
    pos_v = dict(label_positions(label_v, j, a, c))
    for path in pos_u.keys() & pos_v.keys():
        if abs(pos_u[path] - pos_v[path]) == 1:
            return True
    return False


def distance_to_nearest_anchor(label: str, j: int, a: int, c: int):
    """Returns (distance, nearest_anchor_name, direction) for a
    path-internal label; (0, label, None) for an anchor label. `direction`
    is 'left' or 'right' (ties broken toward 'left', i.e. smaller index)."""
    coord = parse_label(label)
    if isinstance(coord, Anchor):
        return 0, coord.name, None
    left, right = endpoints(coord.path)
    length = path_length(coord.path, j, a, c)
    if coord.index <= length - coord.index:
        return coord.index, left, "left"
    return length - coord.index, right, "right"


def branch_family(label: str) -> str | None:
    """'A' or 'C' for labels on an A_*/C_* path; None otherwise (anchors and
    the fixed-topology BD/triangle/port paths have no A/C family)."""
    coord = parse_label(label)
    if isinstance(coord, PathPos):
        return FAMILY_OF_PATH.get(coord.path)
    return None


def straight_offset(label_u: str, label_v: str, j: int, a: int, c: int):
    """If `label_u` and `label_v` lie on a *common* path, returns their
    signed index difference (index_v - index_u) on that path; else None.
    When both are internal to the same growing path this is exactly the
    unique-simple-path bulk distance used by the Phase-3 templates (see
    `docstring PROOF` above: leaving the shared path before reaching an end
    anchor is impossible)."""
    pos_u = dict(label_positions(label_u, j, a, c))
    pos_v = dict(label_positions(label_v, j, a, c))
    common = pos_u.keys() & pos_v.keys()
    if not common:
        return None
    # If on multiple shared paths (only possible when both are anchors),
    # report the shortest.
    diffs = [pos_v[p] - pos_u[p] for p in common]
    return min(diffs, key=abs)


# ---------------------------------------------------------------------------
# Anchor skeleton: contract every path to one weighted edge between its two
# anchors. The *topology* (13 nodes, 19 edges, which anchor pairs are
# joined) is identical for every legal (j, a, c) -- only 4 edge weights
# change. This is the structure boundary-case (near-anchor) templates and
# the Phase 6 lifting argument reason about.
# ---------------------------------------------------------------------------

def anchor_skeleton_edges(j: int, a: int, c: int) -> list[tuple[str, str, int, str]]:
    """List of (left_anchor, right_anchor, weight, path_name)."""
    edges = []
    for path, (left, right, formula) in PATH_SPEC.items():
        edges.append((left, right, path_length(path, j, a, c), path))
    return edges


def anchor_skeleton_graph(j: int, a: int, c: int):
    import networkx as nx

    graph = nx.MultiGraph()
    graph.add_nodes_from(ANCHORS)
    for left, right, weight, path in anchor_skeleton_edges(j, a, c):
        graph.add_edge(left, right, weight=weight, path=path)
    return graph


# ---------------------------------------------------------------------------
# Round-trip verification against the materialized core.
# ---------------------------------------------------------------------------

def verify_roundtrip(core: PortCore) -> dict:
    """Checks, exhaustively, that:
    1. Every label parses and (for path-internal labels) reconstructs via
       `label_of` to the same label.
    2. `path_length` matches the actual materialized path length for every
       one of the 19 paths.
    3. `symbolic_adjacent(u, v)` agrees with the materialized adjacency for
       *every* ordered pair of distinct labels (not just edges) -- a full
       O(n^2) cross-check, not a sample.
    4. `distance_to_nearest_anchor` matches true BFS graph distance to the
       nearest of the 13 anchors, for every vertex.
    """
    import networkx as nx

    j, a, c = core.j, core.a, core.c
    labels = core.labels
    n = len(labels)

    # (1) parse / reconstruct
    for label in labels:
        coord = parse_label(label)
        if isinstance(coord, PathPos):
            assert label_of(coord.path, coord.index, j, a, c) == label, label
        else:
            assert coord.name == label

    # (2) path lengths
    for name, seq in core.paths.items():
        assert path_length(name, j, a, c) == len(seq) - 1, (name, seq)

    # (3) full adjacency cross-check
    actual_edges = {frozenset(e) for e in core.edges}
    mismatches = []
    checked_pairs = 0
    for iu in range(n):
        for iv in range(iu + 1, n):
            checked_pairs += 1
            predicted = symbolic_adjacent(labels[iu], labels[iv], j, a, c)
            actual = frozenset((iu, iv)) in actual_edges
            if predicted != actual:
                mismatches.append((labels[iu], labels[iv], predicted, actual))
    if mismatches:
        raise AssertionError(f"adjacency mismatches: {mismatches[:5]} (total {len(mismatches)})")

    # (4) distance-to-nearest-anchor cross-check via true BFS
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(core.edges)
    anchor_vertices = [core.label_to_vertex[name] for name in ANCHORS]
    dist_mismatches = []
    for v in range(n):
        label = labels[v]
        pred_dist, pred_anchor, _ = distance_to_nearest_anchor(label, j, a, c)
        true_dist = min(nx.shortest_path_length(graph, v, av) for av in anchor_vertices)
        if pred_dist != true_dist:
            dist_mismatches.append((label, pred_dist, true_dist))
    if dist_mismatches:
        raise AssertionError(f"distance mismatches: {dist_mismatches[:5]}")

    return {
        "status": "PROVED",
        "parameters": {"j": j, "a": a, "c": c},
        "order": n,
        "pairs_checked_for_adjacency": checked_pairs,
        "edges_checked": len(actual_edges),
        "distances_checked": n,
        "growing_paths": sorted(GROWING_PATHS),
        "fixed_paths": sorted(set(PATH_SPEC) - GROWING_PATHS),
    }


def self_test() -> dict:
    """Runs verify_roundtrip on all three j=4 catalog instances plus a j=5
    instance, and returns a combined report."""
    instances = [(4, 55, 7), (4, 2, 2), (4, 28, 4)]
    # A representative j=5 instance well inside the valid range.
    Y5 = 1 << 5
    valid_parameters(5, 40, 10)
    instances.append((5, 40, 10))
    reports = []
    for j, a, c in instances:
        core = build_core(j, a, c)
        reports.append(verify_roundtrip(core))
    return {"status": "PROVED", "instances": reports}


if __name__ == "__main__":
    import json

    print(json.dumps(self_test(), indent=2))
