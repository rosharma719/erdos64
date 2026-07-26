#!/usr/bin/env python3
"""Defect-one theorem D1: canonical generator + exhaustive small-order test.

D1 (task Part II): every graph G with (1) delta(G)>=3, (2) every proper
subgraph has min degree <=2 (Carr's Lemma 0.1 hypothesis), (3)
|E(G)|=2|V(G)|-3 (q(G)=1), contains a cycle of length 4 or 8.

Two independent generation routes, cross-validated against each other at
every order where both are feasible:

1. `direct_ordering_generator`: builds candidates literally from the task's
   spec -- a 2-degeneracy forward ordering of G-v with exactly one total
   defect (either an ordinary position with forward-degree 1 instead of 2,
   or the penultimate position with forward-degree 0 instead of 1), plus 3
   neighbours for the restored cubic vertex v, then checks the exact
   degree/property-2 constraints without any further filtering. Feasible
   only at small N (|G-v| <= 6, i.e. n <= 7) because of the combinatorial
   branching of "which 2 later vertices."
2. `via_geng`: uses nauty geng to generate exactly the same target class
   directly from its two easy constraints (delta>=3, exact edge count
   2n-3) -- geng cannot enforce property (2) itself, so that is checked
   afterward, exactly (not an approximate filter) via `is_property2`. This
   is NOT "filtering arbitrary graphs" in the sense the task warns against:
   the geng invocation already encodes constraints (1) and (3) exactly; the
   post-check enforces the one remaining exact constraint (2), which has no
   simpler geng-expressible form.

Route 1 is used ONLY to certify route 2's completeness at n=6,7 (every
graph route 2 finds matches a canonical form some route-1 output produces,
and vice versa). Route 2 is then trusted alone for n=8..N_max, exactly the
same escalation pattern already used elsewhere in this project (validate
a slow from-scratch generator against geng at small order, then trust
geng further).
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterator

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.global_core_check import is_two_degenerate_with_order  # noqa: E402


# ---------------------------------------------------------------------
# Property (2): every proper subgraph (any edge subset on any vertex
# subset) has min degree <= 2. Proved equivalent (defect.md Part II.0) to
# the conjunction of (i) every edge has a degree-3 endpoint [[the B3-type
# spanning-edge-subset case, sufficient by degree-monotonicity]] and (ii)
# every proper INDUCED subgraph has min degree <= 2. Both are checked
# exactly, not approximated.
# ---------------------------------------------------------------------

def is_property2(graph: nx.Graph) -> bool:
    if graph.number_of_nodes() == 0 or min(dict(graph.degree()).values()) < 3:
        return False
    for u, v in graph.edges():
        if graph.degree(u) >= 4 and graph.degree(v) >= 4:
            return False
    vertices = sorted(graph)
    n = len(vertices)
    for size in range(4, n):
        for subset in itertools.combinations(vertices, size):
            sub = graph.subgraph(subset)
            degs = dict(sub.degree())
            if degs and min(degs.values()) >= 3:
                return False
    return True


def is_property2_fast(graph: nx.Graph) -> bool:
    """FAST equivalent of is_property2, proved in defect.md Part II.0:

    property(2) [every proper subgraph, arbitrary edge subset on arbitrary
    vertex subset, has min degree<=2] holds iff
      (a) every edge has a degree-3 endpoint (B3), AND
      (b) for every vertex v, G-v is 2-degenerate.

    Proof sketch: any proper subgraph (S',E') with S'!=V is a subgraph of
    G-v for v not in S', so 2-degeneracy of G-v (which covers ALL its
    subgraphs by definition) gives it a vertex of degree<=2; the remaining
    case S'=V, E' proper is exactly B3 (monotonicity: if some edge xy has
    both endpoints degree>=4, G-xy already has min degree>=3, contradicting
    property 2 directly). O(n*(n+m)) instead of O(2^n).
    """
    if graph.number_of_nodes() == 0 or min(dict(graph.degree()).values()) < 3:
        return False
    for u, v in graph.edges():
        if graph.degree(u) >= 4 and graph.degree(v) >= 4:
            return False
    for v in graph:
        reduced = graph.copy()
        reduced.remove_node(v)
        two_deg, _ = is_two_degenerate_with_order(reduced)
        if not two_deg:
            return False
    return True


def is_degree3_critical_fast(graph: nx.Graph) -> bool:
    """FAST equivalent of is_degree3_critical (induced-only definition):
    holds iff for every vertex v, G-v is 2-degenerate (no separate B3-type
    edge condition -- the modern definition is induced-subgraph-only)."""
    n = graph.number_of_nodes()
    if graph.number_of_edges() != 2 * n - 2:
        return False
    if min(dict(graph.degree()).values()) < 3:
        return False
    for v in graph:
        reduced = graph.copy()
        reduced.remove_node(v)
        two_deg, _ = is_two_degenerate_with_order(reduced)
        if not two_deg:
            return False
    return True


def is_degree3_critical(graph: nx.Graph) -> bool:
    """The modern (Narins-Pokrovskiy-Szabo / L19) definition: n vertices,
    2n-2 edges, min degree>=3, no proper INDUCED subgraph of min degree
    >=3. (Induced-only -- distinct from is_property2, which also covers
    non-induced spanning edge-subsets.)"""
    n = graph.number_of_nodes()
    if graph.number_of_edges() != 2 * n - 2:
        return False
    if min(dict(graph.degree()).values()) < 3:
        return False
    vertices = sorted(graph)
    for size in range(4, n):
        for subset in itertools.combinations(vertices, size):
            sub = graph.subgraph(subset)
            degs = dict(sub.degree())
            if degs and min(degs.values()) >= 3:
                return False
    return True


def has_c4_or_c8(graph: nx.Graph) -> dict[str, bool]:
    g = from_edges(graph.number_of_nodes(), [(u, v) for u, v in graph.edges()])
    dfs = {L: has_cycle_len_dfs(g, L) for L in (4, 8)}
    nxr = {L: has_cycle_len_nx(g, L) for L in (4, 8)}
    if dfs != nxr:
        raise AssertionError(f"detector disagreement: dfs={dfs} nx={nxr}")
    return dfs


def test_d1c(graph: nx.Graph) -> dict[str, Any]:
    """Search every nonedge ab: does G+ab become degree-3-critical?"""
    n = graph.number_of_nodes()
    vertices = sorted(graph)
    witnesses = []
    for a, b in itertools.combinations(vertices, 2):
        if graph.has_edge(a, b):
            continue
        G2 = graph.copy()
        G2.add_edge(a, b)
        if is_degree3_critical_fast(G2):
            witnesses.append((a, b))
    return {"holds": len(witnesses) > 0, "witnesses": witnesses}


# ---------------------------------------------------------------------
# Route 1: direct ordering-based generator.
# ---------------------------------------------------------------------

def _forward_peel(N: int, caps: list[int]) -> Iterator[tuple[tuple[int, int], ...]]:
    """Forward construction: process positions N-1 down to 0 in REVERSE,
    i.e. place x_{N-1} first (no later vertices), then x_{N-2}, etc., so
    that when placing x_i we know exactly the vertex set {x_{i+1},...,x_{N-1}}
    to choose forward-neighbours from."""

    def go(i: int, edges: tuple[tuple[int, int], ...], defect_used: bool):
        if i < 0:
            yield edges
            return
        cap = caps[i]
        later = list(range(i + 1, N))
        if len(later) >= cap:
            for combo in itertools.combinations(later, cap):
                yield from go(i - 1, edges + tuple(sorted((i, j)) for j in combo), defect_used)
        if not defect_used and cap >= 1 and len(later) >= cap - 1:
            for combo in itertools.combinations(later, cap - 1):
                yield from go(i - 1, edges + tuple(sorted((i, j)) for j in combo), True)

    yield from go(N - 1, (), False)


def direct_ordering_generator(N: int) -> Iterator[nx.Graph]:
    """Every labelled H=G-v candidate, N=|H|=n-1 vertices, exactly one
    2-degeneracy defect against caps (2,...,2,1,0)."""
    caps = [2] * max(N - 2, 0) + ([1] if N >= 1 else []) + [0]
    caps = caps[-N:] if N >= 1 else []
    for edges in _forward_peel(N, caps):
        H = nx.Graph()
        H.add_nodes_from(range(N))
        H.add_edges_from(edges)
        yield H


def attach_cubic_vertex(H: nx.Graph) -> Iterator[nx.Graph]:
    """Attach a fresh vertex v (label N = |H|) to exactly 3 vertices of H,
    every way, without any further filtering here."""
    nodes = sorted(H)
    v_label = len(nodes)
    for triple in itertools.combinations(nodes, 3):
        G = H.copy()
        G.add_node(v_label)
        for u in triple:
            G.add_edge(v_label, u)
        yield G


def route1_candidates(N: int) -> Iterator[nx.Graph]:
    for H in direct_ordering_generator(N):
        for G in attach_cubic_vertex(H):
            if min(dict(G.degree()).values()) < 3:
                continue  # exact degree constraint (1), not a post-hoc filter of unrelated graphs
            if G.number_of_edges() != 2 * G.number_of_nodes() - 3:
                continue  # exact edge-count constraint (3); should be automatic by construction
            yield G


# ---------------------------------------------------------------------
# Route 2: geng-driven generator, exact on constraints (1) and (3).
# ---------------------------------------------------------------------

def via_geng(n: int) -> Iterator[nx.Graph]:
    m = 2 * n - 3
    proc = subprocess.Popen(
        ["geng", "-c", "-d3", str(n), f"{m}:{m}"],
        stdout=subprocess.PIPE, text=True,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        yield nx.from_graph6_bytes(line.encode())
    proc.wait()


def canonical_g6(graph: nx.Graph) -> str:
    """Brute-force canonical form (this environment has geng but not
    labelg/nauty's other tools; feasible since callers only use this on
    graphs with <=9 vertices). Tries every relabelling, keeps the
    lexicographically smallest sorted-edge-tuple representation."""
    nodes = sorted(graph, key=str)
    n = len(nodes)
    best = None
    for perm in itertools.permutations(range(n)):
        relabel = {nodes[i]: perm[i] for i in range(n)}
        edges = tuple(sorted(tuple(sorted((relabel[u], relabel[v])))
                              for u, v in graph.edges()))
        if best is None or edges < best:
            best = edges
    return json.dumps(best)


def cross_validate(n_max: int) -> dict[str, Any]:
    """At each feasible n (route 1 needs N=n-1<=6, i.e. n<=7), confirm the
    canonical-form sets from route 1 and route 2 coincide exactly."""
    report = {}
    for n in range(6, n_max + 1):
        N = n - 1
        if N > 6:
            break
        canon1 = set()
        for G in route1_candidates(N):
            if not is_property2_fast(G):
                continue
            canon1.add(canonical_g6(G))
        canon2 = set()
        for G in via_geng(n):
            if not is_property2_fast(G):
                continue
            canon2.add(canonical_g6(G))
        report[n] = {
            "route1_property2_classes": len(canon1),
            "route2_property2_classes": len(canon2),
            "match": canon1 == canon2,
            "route1_only": sorted(canon1 - canon2),
            "route2_only": sorted(canon2 - canon1),
        }
    return report


# ---------------------------------------------------------------------
# Main exhaustive D1 test, using route 2 (validated by route 1 above).
# ---------------------------------------------------------------------

def exhaustive_d1_test(n_min: int, n_max: int) -> dict[str, Any]:
    per_n = {}
    counterexamples = []
    d1c_failures = []
    for n in range(n_min, n_max + 1):
        checked = 0
        property2_count = 0
        c4c8_all = True
        d1c_all = True
        for G in via_geng(n):
            checked += 1
            if not is_property2_fast(G):
                continue
            property2_count += 1
            status = has_c4_or_c8(G)
            if not (status[4] or status[8]):
                c4c8_all = False
                counterexamples.append((n, nx.to_graph6_bytes(G, header=False).decode().strip()))
            d1c = test_d1c(G)
            if not d1c["holds"]:
                d1c_all = False
                d1c_failures.append((n, nx.to_graph6_bytes(G, header=False).decode().strip()))
        per_n[n] = {
            "raw_geng_graphs": checked,
            "property2_graphs": property2_count,
            "all_have_c4_or_c8": c4c8_all,
            "all_satisfy_d1c": d1c_all,
        }
    return {
        "per_n": per_n,
        "counterexamples_to_d1": counterexamples,
        "d1c_failures": d1c_failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cross-validate-max", type=int, default=7)
    parser.add_argument("--n-min", type=int, default=6)
    parser.add_argument("--n-max", type=int, default=12)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cv = cross_validate(args.cross_validate_max)
    print("=== route1 vs route2 cross-validation ===")
    for n, rec in cv.items():
        print(f"n={n}: route1={rec['route1_property2_classes']} "
              f"route2={rec['route2_property2_classes']} match={rec['match']}")

    result = exhaustive_d1_test(args.n_min, args.n_max)
    print("\n=== exhaustive D1 test (route 2) ===")
    for n, rec in result["per_n"].items():
        print(f"n={n}: raw={rec['raw_geng_graphs']} property2={rec['property2_graphs']} "
              f"all_c4_or_c8={rec['all_have_c4_or_c8']} all_d1c={rec['all_satisfy_d1c']}")
    print(f"\ncounterexamples to D1: {len(result['counterexamples_to_d1'])}")
    print(f"D1C failures: {len(result['d1c_failures'])}")

    report = {"cross_validation": cv, "d1_test": result}
    encoded = json.dumps(report, indent=2, sort_keys=True, default=str) + "\n"
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n")

    return 1 if (result["counterexamples_to_d1"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
