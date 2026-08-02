#!/usr/bin/env python3
"""Part II (leaf-compression phase): eliminate q=1 for a genuine minimal
Erdos-Gyarfas counterexample.

This is NARROWER than the previous phase's abstract D1 statement (which
concerned ANY graph satisfying property (2) alone, without requiring an
actual power-of-two-cycle-free structure). Here we use the full strength
of G being an actual minimal counterexample (order-minimal, F-clean) via
the leaf-graph theorem (defect.md leaf-compression Part I).

Proof structure (defect.md leaf-compression Part II):
  II.1 h>=2: excluded immediately by h<=q (I.3), since q=1 forces h<=1.
  II.2 h=0:  q=1 forces n=6 exactly (cubic case); every connected cubic
             6-vertex graph contains a C4 -- proved via the 2-regular
             complement (C6 or 2*C3), independently re-checked by a
             complete geng enumeration.
  II.3 h=1:  c1=0 is forced directly (needs 2 distinct H-neighbours,
             impossible with |H|=1); the identity then forces c3=2;
             the two C3 vertices' F-neighbour structure forces a C4
             through the unique H-vertex z.

This script verifies both the small algebraic claims (c1=0, c3=2 whenever
h=1,q=1) and the C4-mechanism directly, by EXHAUSTIVELY generating every
h=1, property-(2), q=1 graph via the same validated route as the previous
phase's d1_search.py (matching its own exhaustive n=6..12 result: every
such graph already contains a C4 or C8 -- this script checks specifically
that it is C4, via exactly the z-a-u-b-z mechanism, not merely "some
forbidden cycle exists").
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cubic_core import check_identities, cubic_core_partition  # noqa: E402
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.d1_search import is_property2_fast, via_geng  # noqa: E402


def check_h0_case() -> dict[str, Any]:
    """q=1, h=0 forces n=6 (cubic case, q=n/2-2). Every connected cubic
    6-vertex graph's 2-regular complement is C6 or 2*C3; both give a
    direct explicit C4 witness in the ORIGINAL graph. Cross-checked
    against a complete geng enumeration (exactly 2 such graphs)."""
    C6 = nx.Graph()
    C6.add_nodes_from(range(6))
    C6.add_edges_from((i, (i + 1) % 6) for i in range(6))
    two_triangles = nx.Graph()
    two_triangles.add_nodes_from(range(6))
    two_triangles.add_edges_from([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)])

    results = []
    for name, complement_graph in (("complement_of_C6", C6), ("complement_of_2C3", two_triangles)):
        G = nx.complement(complement_graph)
        g = from_edges(6, list(G.edges()))
        dfs = has_cycle_len_dfs(g, 4)
        nxr = has_cycle_len_nx(g, 4)
        assert dfs == nxr, f"{name}: detector disagreement"
        results.append({
            "case": name,
            "n": G.number_of_nodes(),
            "m": G.number_of_edges(),
            "regular_cubic": sorted(dict(G.degree()).values()) == [3] * 6,
            "has_c4": dfs,
        })

    exhaustive = list(via_geng(6))
    exhaustive_c4 = []
    for G in exhaustive:
        g = from_edges(6, list(G.edges()))
        exhaustive_c4.append(has_cycle_len_dfs(g, 4))

    return {
        "n_forced": 6,
        "complement_case_results": results,
        "all_complement_cases_have_c4": all(r["has_c4"] for r in results),
        "exhaustive_geng_count": len(exhaustive),
        "exhaustive_geng_all_have_c4": all(exhaustive_c4),
    }


def check_h1_case(n_max: int) -> dict[str, Any]:
    """Exhaustively generate every property-(2), delta>=3, m=2n-3
    (q=1) graph with EXACTLY h=1, for n up to n_max (same geng route as
    d1_search.py), and verify: c1=0, c3=2 (both forced algebraically),
    and a C4 exists via precisely the z-a-u-b-z mechanism (not just
    'some C4 exists somewhere')."""
    checked = 0
    algebra_failures = []
    mechanism_failures = []
    mechanism_confirmed = 0
    for n in range(7, n_max + 1):
        for G in via_geng(n):
            if not is_property2_fast(G):
                continue
            C, H = cubic_core_partition(G)
            if len(H) != 1:
                continue
            checked += 1
            rec = check_identities(G)
            assert rec["applicable"] and rec["every_c_has_f_neighbour"]
            c1, c3 = rec["c1"], rec["c3"]
            if c1 != 0 or c3 != 2:
                algebra_failures.append((n, nx.to_graph6_bytes(G, header=False).decode().strip(), c1, c3))
                continue

            z = H[0]
            F = G.subgraph(C)
            c3_vertices = [v for v in C if F.degree(v) == 3]
            assert len(c3_vertices) == 2
            u, v_other = c3_vertices

            found_c4_via_mechanism = False
            for u_pick in (u, v_other):
                f_neighbors = [w for w in F.neighbors(u_pick)]
                candidates = [w for w in f_neighbors if w != v_other]
                c2_neighbors = [w for w in candidates if F.degree(w) == 2]
                if len(c2_neighbors) < 2:
                    continue
                a, b = c2_neighbors[0], c2_neighbors[1]
                edges_needed = [(z, a), (a, u_pick), (u_pick, b), (b, z)]
                if all(G.has_edge(x, y) for x, y in edges_needed):
                    found_c4_via_mechanism = True
                    break

            g = from_edges(G.number_of_nodes(), list(G.edges()))
            has_c4 = has_cycle_len_dfs(g, 4)
            if not found_c4_via_mechanism or not has_c4:
                mechanism_failures.append({
                    "n": n, "g6": nx.to_graph6_bytes(G, header=False).decode().strip(),
                    "found_c4_via_mechanism": found_c4_via_mechanism, "has_c4": has_c4,
                })
            else:
                mechanism_confirmed += 1

    return {
        "n_range": (7, n_max),
        "h1_q1_graphs_checked": checked,
        "algebra_failures": algebra_failures,
        "mechanism_confirmed": mechanism_confirmed,
        "mechanism_failures": mechanism_failures,
    }


def main() -> int:
    import argparse
    import json
    import hashlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-n-max", type=int, default=11)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    h0 = check_h0_case()
    h1 = check_h1_case(args.h1_n_max)

    print("=== h=0 case ===")
    print(f"n forced to {h0['n_forced']}; both complement cases have C4: "
          f"{h0['all_complement_cases_have_c4']}")
    print(f"exhaustive geng n=6 cubic count: {h0['exhaustive_geng_count']} "
          f"(all have C4: {h0['exhaustive_geng_all_have_c4']})")

    print("\n=== h=1 case ===")
    print(f"checked {h1['h1_q1_graphs_checked']} graphs, n={h1['n_range']}")
    print(f"algebra failures (c1!=0 or c3!=2): {len(h1['algebra_failures'])}")
    print(f"C4-via-mechanism confirmed: {h1['mechanism_confirmed']}")
    print(f"mechanism failures: {len(h1['mechanism_failures'])}")

    ok = (
        h0["all_complement_cases_have_c4"]
        and h0["exhaustive_geng_all_have_c4"]
        and h0["exhaustive_geng_count"] == 2
        and not h1["algebra_failures"]
        and not h1["mechanism_failures"]
    )
    print(f"\nq=1 IMPOSSIBLE for h=0 and h=1 (checked ranges): {ok}")

    report = {"h0": h0, "h1": h1, "all_checks_pass": ok}
    encoded = json.dumps(report, indent=2, sort_keys=True, default=str)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
