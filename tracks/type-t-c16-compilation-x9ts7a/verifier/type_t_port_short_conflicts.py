#!/usr/bin/env python3
"""Compile the complete static C4/C8 (and bounded C16) conflict catalog.

This implements the search justified in ``type_t_port_c16_compilation.md``
Phase 1: every dyadic-cycle conflict alternates hub passages and positive
core-path segments, no hub passage can be the *only* passage (the m=1 case
is already excluded by the ``allowed_triples``/``linked_gadgets`` local
safety screen, for every dyadic length), and the number of hub passages is
at most ``floor(L/3)``.

A conflict is therefore a cyclic sequence of hub passages
``x_1 -passage_1-> y_1 -corepath(l_1)-> x_2 -passage_2-> y_2 -> ... ->
x_m -passage_m-> y_m -corepath(l_m)-> x_1``, all ``l_i >= 1``.  Hub-passage
branching (which can be wide -- up to ~100 choices at a busy vertex) is only
tried at actual passage-start vertices; core-path segments are resolved by
one precomputed *reachable-at-exact-length* index per core vertex (cheap,
because the bare core is a sparse near-path structure), never by a live
edge-by-edge walk.  This avoids re-trying every virtual edge at every
intermediate core vertex, which is what made the naive augmented-graph walk
intractable.

Because the reachability index only certifies that *some* simple path of
length ``l`` exists between two endpoints -- not that it is disjoint from
the *other* segments of the same candidate cycle -- this search is a sound,
complete *candidate generator*: every real conflict is found, but some
candidates may not correspond to an actual disjoint decomposition.  Every
candidate is independently re-checked by materializing exactly its hubs and
searching for the literal cycle with ``edge_path_cycle`` (edge plus a
simple avoiding path), a differently organized detector reused unmodified
from the CEGAR checker.  Only supports that pass this second check are kept.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from collections import defaultdict
from pathlib import Path

import networkx as nx

from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle, validate_literal_cycle
from type_t_port_multipole_sat import build_catalog
from type_t_port_triples import LinkedGadget, Triple


VariableTag = tuple  # ("triple", Triple) or ("gadget", LinkedGadget)


def build_passages(triples: list[Triple], gadgets: list[LinkedGadget]):
    """Every candidate hub passage, as both directed endpoints.

    A triple contributes its 3 route-2 sub-pairs; a gadget contributes its
    2 route-2 single-hub sub-pairs and its 4 route-3 cross sub-pairs (one
    per choice of which attachment on each side is used).
    """
    by_start: dict[int, list[tuple[int, int, VariableTag]]] = defaultdict(list)
    for triple in triples:
        u, v, w = triple
        tag = ("triple", triple)
        for a, b in ((u, v), (u, w), (v, w)):
            by_start[a].append((b, 2, tag))
            by_start[b].append((a, 2, tag))
    for gadget in gadgets:
        (p1, p2), (q1, q2) = gadget
        tag = ("gadget", gadget)
        by_start[p1].append((p2, 2, tag))
        by_start[p2].append((p1, 2, tag))
        by_start[q1].append((q2, 2, tag))
        by_start[q2].append((q1, 2, tag))
        for pi in (p1, p2):
            for qj in (q1, q2):
                by_start[pi].append((qj, 3, tag))
                by_start[qj].append((pi, 3, tag))
    return by_start


def compute_reach_index(core_adj, max_length: int):
    """reach[v][l] = frozenset of vertices reachable from v by a simple
    *bare-core* path of length exactly l, for 1 <= l <= max_length."""
    order = len(core_adj)
    reach: list[dict[int, frozenset]] = [dict() for _ in range(order)]
    for start in range(order):
        found = [set() for _ in range(max_length + 1)]
        used = {start}

        def visit(vertex, depth):
            if depth >= 1:
                found[depth].add(vertex)
            if depth == max_length:
                return
            for neighbor in core_adj[vertex]:
                if neighbor not in used:
                    used.add(neighbor)
                    visit(neighbor, depth + 1)
                    used.discard(neighbor)

        visit(start, 0)
        for length in range(1, max_length + 1):
            if found[length]:
                reach[start][length] = frozenset(found[length])
    return reach


def build_pair_index(triples: list[Triple], gadgets: list[LinkedGadget]):
    """(a, b, route) -> list of variable tags realizing that passage."""
    index: dict[tuple[int, int, int], list[VariableTag]] = defaultdict(list)
    for triple in triples:
        u, v, w = triple
        tag = ("triple", triple)
        for a, b in ((u, v), (u, w), (v, w)):
            index[(a, b, 2)].append(tag)
            index[(b, a, 2)].append(tag)
    for gadget in gadgets:
        (p1, p2), (q1, q2) = gadget
        tag = ("gadget", gadget)
        index[(p1, p2, 2)].append(tag)
        index[(p2, p1, 2)].append(tag)
        index[(q1, q2, 2)].append(tag)
        index[(q2, q1, 2)].append(tag)
        for pi in (p1, p2):
            for qj in (q1, q2):
                index[(pi, qj, 3)].append(tag)
                index[(qj, pi, 3)].append(tag)
    return index


def enumerate_m2_conflicts(core, triples: list[Triple], gadgets: list[LinkedGadget],
                           target_length: int) -> dict:
    """Exhaustive, complete search for exactly-two-hub-passage conflicts.

    Correct and complete for any dyadic length whose *only* admissible
    passage count is m=2 -- true for C4 (vacuously: floor(4/3)=1 < 2, so
    this always returns empty) and for C8 (floor(8/3)=2, and m>=2 always,
    so m=2 exactly).  A conflict is
    ``x1 -route1-> y1 -corepath(l1)-> x2 -route2-> y2 -corepath(l2)-> x1``,
    l1,l2 >= 1.  Both endpoint sets (``y1`` reachable at ``l1``, and the
    vertices that reach ``x1`` at ``l2``) are small, precomputed
    reachability-index lookups (using the undirected symmetry
    ``x1 reaches y2 at length l`` iff ``y2 reaches x1 at length l``), so the
    search never scans a vertex's full passage list, however large.
    """
    core_adj = core.adjacency()
    by_start = build_passages(triples, gadgets)
    pair_index = build_pair_index(triples, gadgets)
    max_core_path = target_length - 4
    reach = compute_reach_index(core_adj, max_core_path) if max_core_path >= 1 else []

    results: dict[tuple, dict] = {}
    for x1 in range(core.order):
        for y1, route1, tag1 in by_start.get(x1, ()):
            for route2 in (2, 3):
                core_total = target_length - route1 - route2
                if core_total < 2:
                    continue
                for l1 in range(1, core_total):
                    l2 = core_total - l1
                    landing = reach[y1].get(l1) if l1 <= max_core_path else None
                    if not landing:
                        continue
                    reach_x1 = reach[x1].get(l2) if l2 <= max_core_path else None
                    if not reach_x1:
                        continue
                    for x2 in landing:
                        if x2 == x1 or x2 == y1:
                            continue
                        for y2 in reach_x1:
                            if y2 == x1 or y2 == y1 or y2 == x2:
                                continue
                            tags = pair_index.get((x2, y2, route2))
                            if not tags:
                                continue
                            for tag2 in tags:
                                key = tuple(sorted({tag1, tag2}))
                                if key not in results:
                                    results[key] = {"support": key, "hub_passages": 2}
    return results


def minimal_supports(results: dict[tuple, dict]) -> dict[tuple, dict]:
    """Drop any support that is a strict superset of another retained one.

    C4/C8 supports have size at most 2 (Phase 1, ``v <= floor(L/3)``), so
    this is done in O(n) with a singleton-tag set rather than the O(n^2)
    pairwise-subset scan a general implementation would need; that scan is
    intractable once the candidate count reaches hundreds of thousands.
    """
    sizes = {len(key) for key in results}
    if sizes <= {0, 1, 2}:
        singleton_tags = {key[0] for key in results if len(key) == 1}
        kept = {
            key: value for key, value in results.items()
            if len(key) <= 1 or not (key[0] in singleton_tags or key[1] in singleton_tags)
        }
        return kept
    keys = sorted(results, key=len)
    kept_keys: list[tuple] = []
    for key in keys:
        key_set = set(key)
        if any(set(smaller) < key_set for smaller in kept_keys):
            continue
        kept_keys.append(key)
    return {key: results[key] for key in kept_keys}


def materialize_variables(core, support: tuple):
    """Materialize exactly the hubs named by ``support`` as an ordinary graph."""
    graph = nx.Graph()
    graph.add_nodes_from(range(core.order))
    graph.add_edges_from(core.edges)
    next_vertex = core.order
    for kind, item in support:
        if kind == "triple":
            hub = next_vertex
            next_vertex += 1
            graph.add_edges_from((hub, vertex) for vertex in item)
        elif kind == "gadget":
            (p1, p2), (q1, q2) = item
            left, right = next_vertex, next_vertex + 1
            next_vertex += 2
            graph.add_edges_from(((left, p1), (left, p2), (right, q1), (right, q2), (left, right)))
        else:
            raise AssertionError(f"unknown variable kind {kind}")
    adjacency = tuple(frozenset(graph.neighbors(v)) for v in range(next_vertex))
    return graph, adjacency


def verify_conflicts(core, target_length: int, results: dict[tuple, dict]) -> dict[tuple, dict]:
    """Independently verify every candidate support by a *different* search:
    materialize just those hubs and find the cycle as an edge plus an
    exact-length simple path avoiding it (``edge_path_cycle``, reused
    unmodified from the CEGAR checker as a second, differently organized
    detector).  Candidates that do not reproduce a literal cycle are sound
    but spurious outputs of the reachability-index filter and are dropped,
    not raised as errors -- soundness of the *kept* set is what matters."""
    verified: dict[tuple, dict] = {}
    rejected = 0
    for support in results:
        graph, adjacency = materialize_variables(core, support)
        witness = edge_path_cycle(adjacency, target_length)
        if witness is None:
            rejected += 1
            continue
        validate_literal_cycle(graph, list(witness))
        verified[support] = {"witness": list(witness)}
    return verified, rejected


def serialize_support(support: tuple) -> list:
    serialized = []
    for kind, item in support:
        if kind == "gadget":
            serialized.append([kind, [list(item[0]), list(item[1])]])
        else:
            serialized.append([kind, list(item)])
    return serialized


def compile_instance(j: int, a: int, c: int, lengths: tuple[int, ...] = (4, 8)) -> dict:
    """Compile C4 and C8 (both forced to exactly m=2 hub passages, or
    vacuously empty, by the Phase 1 proof in type_t_port_c16_compilation.md)."""
    core = build_core(j, a, c)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    per_length = {}
    for length in lengths:
        if length not in (4, 8):
            raise ValueError("compile_instance only supports the proven m=2 lengths 4 and 8")
        raw = enumerate_m2_conflicts(core, triples, gadgets, length)
        candidate_minimal = minimal_supports(raw)
        verified, rejected = verify_conflicts(core, length, candidate_minimal)
        minimal = minimal_supports(verified)
        per_length[str(length)] = {
            "target_length": length,
            "raw_candidate_supports": len(raw),
            "candidate_minimal_supports": len(candidate_minimal),
            "verification_rejected": rejected,
            "verified_minimal_supports": len(minimal),
            "support_size_distribution": {
                str(size): sum(1 for key in minimal if len(key) == size)
                for size in sorted({len(key) for key in minimal})
            } if minimal else {},
            "conflicts": [
                {
                    "support": serialize_support(support),
                    "witness": verified[support]["witness"],
                }
                for support in sorted(minimal, key=lambda k: (len(k), k))
            ],
        }
    return {
        "status": "COMPUTATIONALLY_CERTIFIED",
        "parameters": {"j": j, "Y": 1 << j, "a": a, "c": c},
        "catalog_sizes": {"triples": len(triples), "gadgets": len(gadgets)},
        "lengths": per_length,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--lengths", type=int, nargs="+", default=[4, 8])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_instance(args.j, args.a, args.c, tuple(args.lengths))
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.suffix == ".gz":
            args.output.write_bytes(gzip.compress(rendered.encode(), mtime=0))
        else:
            args.output.write_text(rendered)
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
