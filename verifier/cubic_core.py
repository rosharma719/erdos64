#!/usr/bin/env python3
"""Cubic-core decomposition checks (task Part I, 2026-07-26 pass).

Independently verifies, on every candidate graph handed to it, the pure
edge-count identities relating q = 2n-2-m to the cubic core C = {deg 3},
the high set H = {deg >= 4}, and F = G[C]:

    e(C,H) = n + 3h - 4 - 2q
    |E(F)| = n - 3h + 2 + q
    beta(F) = |E(F)| - |C| + kappa(F) = q + 2 - 2h + kappa

and, when every vertex of C has an F-neighbour (M2's C-restriction), the
degree-partition identities on C1/C2/C3 (F-degree 1/2/3 respectively):

    2*c1 + c2 = e(C,H)
    c1 = c3 + 2*kappa - 2*beta(F)

It also builds the component-incidence quotient Q and checks the exact
connectivity correspondences proved in defect.md Part I.2, including the
refined (corrected) statement of the "2-connected implies >=2 distinct
H-neighbours" claim, which needs kappa(F) >= 2 as an explicit extra
hypothesis, not just H != empty.

These identities are PURE ALGEBRA given only "H independent" and "every
C-vertex has degree exactly 3" -- they hold for ANY graph with that
partition, not just minimal Erdos-Gyarfas counterexamples. The script
therefore checks them against three independent populations:
 (a) every graph in networkx's graph atlas (all unlabeled graphs, order
     <= 7) that happens to have an independent high-set and a partition
     into degree-3/degree>=4 vertices (no minimality assumed at all);
 (b) the 12 order<=7 "inclusion-minimal delta>=3" fixtures already
     certified by global_core_check.py (minimality assumed, for the M2
     C1/C2/C3 identities which need it);
 (c) randomized synthetic cubic-core constructions (H-vertices wired to
     random C-forests/unicyclic pieces) at larger n, to stress-test beyond
     order 7.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.global_core_check import is_inclusion_minimal_delta_three  # noqa: E402


def cubic_core_partition(graph: nx.Graph) -> tuple[list[int], list[int]]:
    C = sorted((v for v in graph if graph.degree(v) == 3), key=str)
    H = sorted((v for v in graph if graph.degree(v) >= 4), key=str)
    return C, H


def component_incidence_quotient(graph: nx.Graph, C: list[int], H: list[int]):
    """Return (components-of-F, multiplicity dict, adjacency of Q)."""
    F = graph.subgraph(C)
    components = [sorted(comp, key=str) for comp in nx.connected_components(F)]
    comp_of = {v: i for i, comp in enumerate(components) for v in comp}
    mult: dict[tuple[str, int], int] = {}
    for h in H:
        for c in graph.neighbors(h):
            if c in comp_of:
                key = (h, comp_of[c])
                mult[key] = mult.get(key, 0) + 1
    return components, comp_of, mult


def check_identities(graph: nx.Graph) -> dict[str, Any]:
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    C, H = cubic_core_partition(graph)
    c, h = len(C), len(H)
    if c + h != n:
        return {"applicable": False, "reason": "vertex of degree <3 present"}
    high_independent = graph.subgraph(H).number_of_edges() == 0
    if not high_independent:
        return {"applicable": False, "reason": "H not independent"}

    q = 2 * n - 2 - m
    eCH = sum(1 for u, v in graph.edges() if (u in H) != (v in H))
    F = graph.subgraph(C)
    EF = F.number_of_edges()
    kappa = nx.number_connected_components(F) if c > 0 else 0
    betaF = EF - c + kappa if c > 0 else 0

    eCH_pred = n + 3 * h - 4 - 2 * q
    EF_pred = n - 3 * h + 2 + q
    betaF_pred = q + 2 - 2 * h + kappa

    record: dict[str, Any] = {
        "applicable": True,
        "n": n, "m": m, "c": c, "h": h, "q": q,
        "eCH": eCH, "eCH_pred": eCH_pred, "eCH_ok": eCH == eCH_pred,
        "EF": EF, "EF_pred": EF_pred, "EF_ok": EF == EF_pred,
        "kappa": kappa,
        "betaF": betaF, "betaF_pred": betaF_pred, "betaF_ok": betaF == betaF_pred,
    }

    # C1/C2/C3 partition needs every C-vertex to have >=1 F-neighbour
    # (M2's C-restriction) so that 1<=d_F(v)<=3 -- check the hypothesis
    # explicitly rather than assuming it.
    dF = {v: F.degree(v) for v in C}
    every_c_has_f_neighbour = all(dF[v] >= 1 for v in C)
    record["every_c_has_f_neighbour"] = every_c_has_f_neighbour
    if every_c_has_f_neighbour:
        c1 = sum(1 for v in C if dF[v] == 1)
        c2 = sum(1 for v in C if dF[v] == 2)
        c3 = sum(1 for v in C if dF[v] == 3)
        record["c1"] = c1
        record["c2"] = c2
        record["c3"] = c3
        record["partition_ok"] = (c1 + c2 + c3 == c)
        record["eCH_from_partition_ok"] = (2 * c1 + c2 == eCH)
        record["c1_c3_identity_ok"] = (c1 == c3 + 2 * kappa - 2 * betaF)

    # Component-incidence quotient Q and the connectivity correspondences.
    components, comp_of, mult = component_incidence_quotient(graph, C, H)
    distinct_h_neighbors = {
        i: len({h for (h, j) in mult if j == i}) for i in range(len(components))
    }
    record["kappa_components"] = len(components)
    record["distinct_h_neighbor_counts"] = sorted(distinct_h_neighbors.values())

    g_connected = nx.is_connected(graph)
    # I.2(a): G connected => Q connected (via contraction).
    Q = nx.Graph()
    Q.add_nodes_from(H)
    Q.add_nodes_from(f"K{i}" for i in range(len(components)))
    for (hh, i) in mult:
        Q.add_edge(hh, f"K{i}")
    q_connected = nx.is_connected(Q) if Q.number_of_nodes() > 0 else True
    record["g_connected"] = g_connected
    record["q_connected"] = q_connected
    record["contraction_correspondence_ok"] = (not g_connected) or q_connected

    # I.2(b)/(c): the refined 2-/3-connectivity claims, kappa>=2 required.
    try:
        conn = nx.node_connectivity(graph) if n >= 2 else 0
    except Exception:
        conn = 0
    record["node_connectivity"] = conn
    if len(components) >= 2:
        if conn >= 2:
            record["twoconn_ge2_distinct_ok"] = all(
                v >= 2 for v in distinct_h_neighbors.values()
            )
        if conn >= 3:
            record["threeconn_ge3_distinct_ok"] = all(
                v >= 3 for v in distinct_h_neighbors.values()
            )
    else:
        # kappa==1: the unique component's distinct-neighbour count must
        # equal h exactly (every H-vertex has some C-edge, all landing in
        # the single component) -- no extra bound from 2-/3-connectivity.
        if components:
            record["kappa1_distinct_equals_h_ok"] = (
                distinct_h_neighbors.get(0, 0) == h
            )

    return record


def atlas_sweep() -> dict[str, Any]:
    checked = 0
    applicable = 0
    failures = []
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() < 4 or not nx.is_connected(graph):
            continue
        if min(dict(graph.degree()).values()) < 3:
            continue
        checked += 1
        rec = check_identities(graph)
        if not rec["applicable"]:
            continue
        applicable += 1
        keys = [k for k in rec if k.endswith("_ok")]
        if not all(rec[k] for k in keys):
            failures.append((nx.to_graph6_bytes(graph, header=False).decode().strip(), rec))
    return {
        "population": "networkx graph_atlas_g, connected delta>=3, order<=7",
        "checked": checked,
        "applicable_cubic_core_graphs": applicable,
        "failures": failures,
    }


def minimal_core_fixture_sweep() -> dict[str, Any]:
    """The 12 inclusion-minimal-delta>=3 order<=7 fixtures (M2 holds here
    because global_core_check.py's certify() already verified
    every_vertex_touches_cubic for exactly this population)."""
    checked = 0
    failures = []
    for graph in nx.graph_atlas_g():
        if graph.number_of_nodes() < 4 or not nx.is_connected(graph):
            continue
        if not is_inclusion_minimal_delta_three(graph):
            continue
        checked += 1
        rec = check_identities(graph)
        if not rec["applicable"]:
            failures.append((nx.to_graph6_bytes(graph, header=False).decode().strip(), rec))
            continue
        keys = [k for k in rec if k.endswith("_ok")]
        if not all(rec[k] for k in keys):
            failures.append((nx.to_graph6_bytes(graph, header=False).decode().strip(), rec))
    return {
        "population": "inclusion-minimal delta>=3 fixtures, order<=7 (global_core_check.py)",
        "checked": checked,
        "failures": failures,
    }


def random_cubic_core_graph(rng: random.Random, h: int, forest_sizes: list[int]) -> nx.Graph | None:
    """Build a synthetic H-independent, all-C-degree-3 graph: H-vertices
    wired only to C, C forms a disjoint union of small trees/unicyclic
    pieces (F), then top up every C-vertex to degree exactly 3 using
    additional H-attachments distributed round robin. Returns None if a
    simple-graph construction is infeasible with the given parameters."""
    G = nx.Graph()
    c_offset = 0
    all_c = []
    for size in forest_sizes:
        nodes = list(range(c_offset, c_offset + size))
        G.add_nodes_from(nodes)
        # random spanning tree on this piece, then maybe one extra edge
        # (unicyclic) with probability 1/2, to vary kappa/beta(F).
        order = nodes[:]
        rng.shuffle(order)
        for i in range(1, len(order)):
            j = rng.randrange(i)
            G.add_edge(order[i], order[j])
        if size >= 3 and rng.random() < 0.5:
            u, v = rng.sample(nodes, 2)
            if not G.has_edge(u, v):
                G.add_edge(u, v)
        all_c.extend(nodes)
        c_offset += size

    h_nodes = [f"h{i}" for i in range(h)]
    G.add_nodes_from(h_nodes)

    # every C-vertex needs degree exactly 3; give it (3 - current degree)
    # more edges into H, spread round robin, rejecting anything that
    # would make two C-vertices share more than a simple edge or would
    # put an H-H edge.
    needs = {v: 3 - G.degree(v) for v in all_c}
    if any(x < 0 for x in needs.values()):
        return None
    slots = []
    for v, k in needs.items():
        slots.extend([v] * k)
    rng.shuffle(slots)
    hi = 0
    for v in slots:
        # round robin over H, skip if already adjacent (keep simple)
        tries = 0
        while G.has_edge(v, h_nodes[hi % h]) and tries < 2 * h:
            hi += 1
            tries += 1
        if tries >= 2 * h:
            return None
        G.add_edge(v, h_nodes[hi % h])
        hi += 1

    if min(dict(G.degree()).values()) < 3:
        return None
    if G.subgraph(h_nodes).number_of_edges() != 0:
        return None
    if not nx.is_connected(G):
        return None
    return G


def synthetic_sweep(trials: int, seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    checked = 0
    failures = []
    for _ in range(trials):
        h = rng.randint(1, 5)
        n_pieces = rng.randint(1, 4)
        forest_sizes = [rng.randint(2, 6) for _ in range(n_pieces)]
        G = random_cubic_core_graph(rng, h, forest_sizes)
        if G is None:
            continue
        checked += 1
        rec = check_identities(G)
        if not rec["applicable"]:
            failures.append(("<construction invariant broken>", rec))
            continue
        keys = [k for k in rec if k.endswith("_ok")]
        if not all(rec[k] for k in keys):
            failures.append((nx.to_graph6_bytes(G, header=False).decode().strip(), rec))
    return {
        "population": f"synthetic H-independent all-C-degree-3 random graphs, {trials} trials, seed {seed}",
        "checked": checked,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=20260726)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = {
        "schema": "erdos64-cubic-core-v1",
        "atlas": atlas_sweep(),
        "minimal_core_fixtures": minimal_core_fixture_sweep(),
        "synthetic": synthetic_sweep(args.trials, args.seed),
    }
    total_failures = (
        len(report["atlas"]["failures"])
        + len(report["minimal_core_fixtures"]["failures"])
        + len(report["synthetic"]["failures"])
    )
    encoded = json.dumps(report, indent=2, sort_keys=True, default=str) + "\n"
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(
            json.dumps(report, indent=2, sort_keys=True, default=str) + "\n"
        )
    print(
        f"atlas: checked={report['atlas']['checked']} "
        f"applicable={report['atlas']['applicable_cubic_core_graphs']} "
        f"failures={len(report['atlas']['failures'])}"
    )
    print(
        f"minimal-core fixtures: checked={report['minimal_core_fixtures']['checked']} "
        f"failures={len(report['minimal_core_fixtures']['failures'])}"
    )
    print(
        f"synthetic: checked={report['synthetic']['checked']} "
        f"failures={len(report['synthetic']['failures'])}"
    )
    return 1 if total_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
