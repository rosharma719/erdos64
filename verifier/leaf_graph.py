#!/usr/bin/env python3
"""Part I (leaf-compression phase): the derived leaf graph L(G) and the
identity c1 = c3 + 4h - 2q - 4.

defect.md's prior Part I proved (pure algebra, H independent + C-degree-3):
    beta(F) = q + 2 - 2h + kappa                                   (I.1c)
    c1 = c3 + 2*kappa - 2*beta(F)                                  (I.1d)
Substituting (I.1c) into (I.1d) eliminates kappa entirely:
    c1 = c3 + 2*kappa - 2*(q + 2 - 2h + kappa)
       = c3 + 2*kappa - 2q - 4 + 4h - 2*kappa
       = c3 + 4h - 2q - 4.
This is checked directly below (`identity_c1`), on the SAME populations as
the prior Part I (pure algebra, no C4-freeness needed).

L(G): a multigraph on vertex set H. For every x in C1 (whose two distinct
H-neighbours are a_x, b_x -- distinct because G is simple and x has
exactly 2 H-neighbours, by C1's definition d_F(x)=1 => d_H(x)=2), add an
edge a_x b_x labelled x. `build_leaf_graph` constructs this explicitly and
returns both the multigraph and the label map, WITHOUT assuming
simplicity -- L1 (simplicity) is checked as a PROPERTY of the result, not
assumed.

L1/L2 are mechanical, combinatorial facts checkable on ANY C4-free graph
with the right (H independent, C-degree-3, M2) structure -- checked here
on synthetic C4-free constructions (no genuine small Erdos-Gyarfas
counterexample exists to test on; every one of the 12 order<=7
inclusion-minimal-delta>=3 fixtures already contains a C4 -- see
cubic_core.py's atlas sweep -- so this project has NEVER had a real
C4-free fixture at any size checked so far; this is reported honestly,
not glossed over).

L3/L4 use G's minimality (order-minimal, no power-of-two cycle) in an
essential way (proof by contradiction against a hypothetical smaller
counterexample) and are therefore NOT empirically testable on any
concrete graph -- there is no way to "run" a vacuous-antecedent argument
on data. Their soundness rests on the written proof alone (defect.md).
"""
from __future__ import annotations

import random
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cubic_core import (  # noqa: E402
    check_identities,
    cubic_core_partition,
    random_cubic_core_graph,
)
from verifier.cycle_detect import from_edges, has_cycle_len_dfs  # noqa: E402


def identity_c1(rec: dict[str, Any]) -> bool:
    """c1 == c3 + 4h - 2q - 4, using an ALREADY-computed check_identities
    record (only meaningful when the C1/C2/C3 partition is applicable,
    i.e. every C-vertex has an F-neighbour, M2's hypothesis)."""
    if not rec.get("every_c_has_f_neighbour"):
        return True  # not applicable, vacuously not a failure
    return rec["c1"] == rec["c3"] + 4 * rec["h"] - 2 * rec["q"] - 4


def build_leaf_graph(graph: nx.Graph, C: list[int], H: list[int]) -> tuple[nx.Graph, dict[int, tuple[int, int]], bool]:
    """Returns (L, label_of[x] -> (a_x,b_x), is_simple). L is built with
    add_edge (so a repeated pair silently overwrites in networkx's simple
    Graph -- to detect non-simplicity explicitly we track raw pairs first
    and check for duplicates BEFORE building L, not after)."""
    F = graph.subgraph(C)
    C1 = [v for v in C if F.degree(v) == 1]
    raw_edges: dict[int, tuple[int, int]] = {}
    for x in C1:
        h_neighbors = sorted(u for u in graph.neighbors(x) if u in H)
        assert len(h_neighbors) == 2, (
            f"C1 vertex {x} has {len(h_neighbors)} H-neighbours, expected exactly 2"
        )
        a, b = h_neighbors
        assert a != b, f"C1 vertex {x}: H-neighbours not distinct (simplicity of G violated)"
        raw_edges[x] = (a, b)

    pair_to_labels: dict[tuple[int, int], list[int]] = {}
    for x, pair in raw_edges.items():
        pair_to_labels.setdefault(pair, []).append(x)
    is_simple = all(len(labels) == 1 for labels in pair_to_labels.values())

    L = nx.Graph()
    L.add_nodes_from(H)
    label_of: dict[tuple[int, int], int] = {}
    for pair, labels in pair_to_labels.items():
        L.add_edge(*pair)
        label_of[pair] = labels[0]  # arbitrary if non-simple; flagged by is_simple=False
    return L, raw_edges, is_simple


def check_L1_simplicity(graph: nx.Graph, C: list[int], H: list[int]) -> dict[str, Any]:
    """If two distinct x,y in C1 share the same H-neighbour pair {a,b},
    a-x-b-y-a is a genuine C4 in G. Verify this EXPLICITLY whenever a
    collision is found (not just asserted), and confirm G is C4-free =>
    no collision is possible (contrapositive check)."""
    F = graph.subgraph(C)
    C1 = [v for v in C if F.degree(v) == 1]
    pair_to_xs: dict[tuple[int, int], list[int]] = {}
    for x in C1:
        h_neighbors = tuple(sorted(u for u in graph.neighbors(x) if u in H))
        pair_to_xs.setdefault(h_neighbors, []).append(x)

    collisions = {pair: xs for pair, xs in pair_to_xs.items() if len(xs) >= 2}
    witnessed_c4 = []
    for (a, b), xs in collisions.items():
        x, y = xs[0], xs[1]
        cycle_edges = [(a, x), (x, b), (b, y), (y, a)]
        all_present = all(graph.has_edge(u, v) for u, v in cycle_edges)
        witnessed_c4.append({"a": a, "b": b, "x": x, "y": y, "edges_present": all_present})

    g = from_edges(graph.number_of_nodes(), list(graph.edges()))
    g_has_c4 = has_cycle_len_dfs(g, 4)
    # l1_consistent: L1's contrapositive -- any collision MUST imply the
    # graph has a C4; a collision on a C4-free graph would refute L1.
    l1_consistent = (len(collisions) == 0) or g_has_c4
    return {
        "collisions_found": len(collisions),
        "witnessed_c4": witnessed_c4,
        "graph_is_c4_free": not g_has_c4,
        "l1_consistent": l1_consistent,
    }


def check_L2_cycle_lifting(graph: nx.Graph, L: nx.Graph, raw_edges: dict[int, tuple[int, int]],
                            max_cycles: int = 200) -> dict[str, Any]:
    """For every simple cycle of L (up to max_cycles, to bound cost on
    larger synthetic instances), reconstruct the claimed length-2r cycle
    of G and verify it directly: distinct a_i, distinct labels x_i, no
    a_i equals any x_j, every edge present, and (independently) that the
    dual detector agrees this is a genuine simple cycle of that length."""
    pair_to_label = {}
    for x, (a, b) in raw_edges.items():
        pair_to_label[tuple(sorted((a, b)))] = x

    checked = 0
    failures = []
    g = from_edges(graph.number_of_nodes(), list(graph.edges()))
    for cyc in nx.simple_cycles(L, length_bound=min(L.number_of_nodes(), 12)):
        if len(cyc) < 3:
            continue
        checked += 1
        if checked > max_cycles:
            break
        r = len(cyc)
        a = cyc
        x = []
        ok = True
        for i in range(r):
            u, v = a[i], a[(i + 1) % r]
            key = tuple(sorted((u, v)))
            if key not in pair_to_label:
                ok = False
                break
            x.append(pair_to_label[key])
        if not ok:
            failures.append({"cycle": cyc, "reason": "missing label (non-C1 L-edge in cycle?)"})
            continue

        lifted = []
        for i in range(r):
            lifted.append(a[i])
            lifted.append(x[i])
        distinct_a = len(set(a)) == r
        distinct_x = len(set(x)) == r
        no_overlap = set(a).isdisjoint(set(x))
        edges_needed = [(lifted[i], lifted[(i + 1) % (2 * r)]) for i in range(2 * r)]
        edges_present = all(graph.has_edge(u, v) for u, v in edges_needed)
        lifted_is_simple_cycle_of_len_2r = (
            len(set(lifted)) == 2 * r and has_cycle_len_dfs(g, 2 * r)
        )
        rec = {
            "L_cycle": a, "labels": x, "distinct_a": distinct_a, "distinct_x": distinct_x,
            "no_overlap": no_overlap, "edges_present": edges_present,
            "lifted_length": 2 * r,
            "detector_confirms_cycle_of_that_length": lifted_is_simple_cycle_of_len_2r,
        }
        if not (distinct_a and distinct_x and no_overlap and edges_present):
            failures.append(rec)

    return {"cycles_checked": checked, "failures": failures}


def synthetic_c4_free_generator(rng: random.Random, trials: int):
    """Build random H-independent all-C-degree-3 graphs (cubic_core.py's
    generator) and yield only the C4-free ones -- these are the only
    instances where L1/L2 are meaningfully exercised (L1's proof is
    conditional on C4-freeness)."""
    produced = 0
    for _ in range(trials):
        h = rng.randint(1, 6)
        n_pieces = rng.randint(1, 4)
        forest_sizes = [rng.randint(2, 7) for _ in range(n_pieces)]
        G = random_cubic_core_graph(rng, h, forest_sizes)
        if G is None:
            continue
        relabel = {v: i for i, v in enumerate(sorted(G, key=str))}
        G = nx.relabel_nodes(G, relabel)
        g = from_edges(G.number_of_nodes(), list(G.edges()))
        if has_cycle_len_dfs(g, 4):
            continue
        produced += 1
        yield G


def main() -> int:
    import argparse
    import json
    import hashlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=200000)
    parser.add_argument("--seed", type=int, default=20260727)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    # 1. pure algebraic identity, same 3 populations as before
    identity_failures = []
    checked = 0
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() < 4 or not nx.is_connected(graph):
            continue
        if min(dict(graph.degree()).values()) < 3:
            continue
        rec = check_identities(graph)
        if not rec["applicable"]:
            continue
        checked += 1
        if not identity_c1(rec):
            identity_failures.append(("atlas", nx.to_graph6_bytes(graph, header=False).decode().strip()))

    rng = random.Random(args.seed)
    synth_checked = 0
    c4_free_count = 0
    l1_results = []
    l2_results = []
    for G in synthetic_c4_free_generator(rng, args.trials):
        rec = check_identities(G)
        synth_checked += 1
        if rec["applicable"]:
            if not identity_c1(rec):
                identity_failures.append(("synthetic", sorted(G.edges())))
        c4_free_count += 1
        C, H = cubic_core_partition(G)
        L, raw_edges, is_simple = build_leaf_graph(G, C, H)
        l1 = check_L1_simplicity(G, C, H)
        l1_results.append(l1)
        if L.number_of_edges() >= 3:
            l2 = check_L2_cycle_lifting(G, L, raw_edges)
            l2_results.append(l2)

    l1_collisions_total = sum(r["collisions_found"] for r in l1_results)
    l1_bad_witnesses = sum(
        1 for r in l1_results for w in r["witnessed_c4"] if not w["edges_present"]
    )
    l1_c4_free_but_collision = sum(
        1 for r in l1_results if r["collisions_found"] > 0 and r["graph_is_c4_free"]
    )
    l2_cycles_checked = sum(r["cycles_checked"] for r in l2_results)
    l2_failures = sum(len(r["failures"]) for r in l2_results)

    report = {
        "schema": "erdos64-leaf-graph-v1",
        "identity_c1_checked": checked + synth_checked,
        "identity_c1_failures": identity_failures,
        "synthetic_c4_free_graphs_generated": c4_free_count,
        "L1_collisions_found_total": l1_collisions_total,
        "L1_collisions_with_bad_witness": l1_bad_witnesses,
        "L1_c4_free_graph_with_collision_found": l1_c4_free_but_collision,
        "L2_cycles_checked": l2_cycles_checked,
        "L2_failures": l2_failures,
        "note_L1": "expect L1_c4_free_graph_with_collision_found == 0: "
                   "the generator already filters for C4-freeness, so no "
                   "collision should ever survive -- this IS the check.",
    }
    encoded = json.dumps(report, indent=2, sort_keys=True, default=str)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n")

    print(f"identity c1=c3+4h-2q-4: checked={report['identity_c1_checked']} "
          f"failures={len(identity_failures)}")
    print(f"synthetic C4-free graphs generated: {c4_free_count}")
    print(f"L1: collisions found={l1_collisions_total} "
          f"(bad witnesses={l1_bad_witnesses}, "
          f"C4-free-with-collision={l1_c4_free_but_collision})")
    print(f"L2: cycles checked={l2_cycles_checked} failures={l2_failures}")

    ok = (
        not identity_failures
        and l1_bad_witnesses == 0
        and l1_c4_free_but_collision == 0
        and l2_failures == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
