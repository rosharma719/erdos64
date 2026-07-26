"""
Rigid-core lemma verification (task Part 1, 2026-07-25, third redirection pass).

Checks: "every nontrivial simple 2-connected series-parallel graph has
>=2 vertices of degree exactly 2" -- against every connected min-degree->=2
graph geng can generate for small n, filtered to 2-connected + SP (no
R-node in its SPQR tree, historically via `spqrtree`). New theorem-level
R-node uses must pass `gadget_criticality.py`'s structural validation because
the package is now known to be insertion-order-sensitive on some fixtures.

Also includes the two hand-built "counterexamples" that turned out to be
WRONG (both actually contain a K4-minor) -- kept here as an explicit
regression check: they must be classified as NOT series-parallel, or the
lemma writeup in one_pole.md is compromised.
"""
from __future__ import annotations
import subprocess
from collections import Counter

import networkx as nx
import spqrtree


def is_sp(G) -> bool:
    sg = spqrtree.MultiGraph()
    for a, b in G.edges():
        sg.add_edge(a, b)
    tree = spqrtree.SPQRTree(sg)
    counts = Counter(n.type.value for n in tree.nodes())
    return counts.get("R", 0) == 0


def run_geng(n: int):
    proc = subprocess.Popen(["geng", "-c", "-d2", str(n)], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield line
    proc.wait()


def regression_check():
    """The two flawed hand-examples from the first attempt at O5 -- must
    both be correctly flagged as NOT series-parallel (they contain K4)."""
    diamond_plus_uv = nx.Graph()
    diamond_plus_uv.add_edges_from(
        [("u", "m1"), ("u", "m2"), ("v", "m1"), ("v", "m2"), ("m1", "m2"), ("u", "v")])
    assert not is_sp(diamond_plus_uv), "regression FAILED: diamond+uv misclassified as SP"

    double_diamond = nx.Graph()
    double_diamond.add_edges_from([
        ("u", "m1"), ("u", "m2"), ("v", "m1"), ("v", "m2"), ("m1", "m2"),
        ("u", "m3"), ("u", "m4"), ("v", "m3"), ("v", "m4"), ("m3", "m4")])
    assert not is_sp(double_diamond), "regression FAILED: double-diamond misclassified as SP"

    print("regression check PASSED: both flawed hand-examples correctly "
          "rejected as non-series-parallel (both contain a K4-minor).")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=3)
    ap.add_argument("--nmax", type=int, default=8)
    args = ap.parse_args()

    regression_check()
    print()

    total_2conn = 0
    total_sp = 0
    violations = []

    for n in range(args.nmin, args.nmax + 1):
        n_2conn = n_sp = 0
        for g6 in run_geng(n):
            G = nx.from_graph6_bytes(g6.encode())
            if nx.node_connectivity(G) < 2:
                continue
            n_2conn += 1
            if not is_sp(G):
                continue
            n_sp += 1
            deg2 = [v for v, d in G.degree() if d == 2]
            if len(deg2) < 2:
                violations.append((n, g6, deg2))
        total_2conn += n_2conn
        total_sp += n_sp
        print(f"n={n}: 2-connected={n_2conn} series-parallel={n_sp} "
              f"(cumulative 2conn={total_2conn} sp={total_sp})")

    print(f"\n=== SUMMARY n={args.nmin}..{args.nmax} ===")
    print(f"total 2-connected graphs: {total_2conn}")
    print(f"total series-parallel (no R node): {total_sp}")
    print(f"violations of '>=2 degree-2 vertices' among SP graphs: {len(violations)}")
    for v in violations[:10]:
        print("  VIOLATION:", v)


if __name__ == "__main__":
    main()
