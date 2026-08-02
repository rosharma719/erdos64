"""
Defect-ordered experimental model (Erdos #64 redirection, 2026-07-25).

For real small connected delta>=3 graphs (from geng), compute:
  - n, m, excess = 2m-3n, D = 2n-2-m
  - full power-of-two cycle-length spectrum (present / missing dyadic lengths)
  - the proved bound D <= floor(n/2)-2  (defect.md S3b)
  - the disproved target n <= 2D+3      (defect.md S4)
  - whether G minus a degree-3 vertex x1 is 2-degenerate, for every choice
    of x1 (defect.md S2b open question)

This is a consistency/data-gathering tool, not a source of new theorems: the
two inequalities above are already proved/disproved unconditionally in
defect.md from S1 alone, so every graph must satisfy them exactly as
predicted. The 2-degeneracy check is the genuinely open computational
question and is reported per-graph, honestly, with no claim of generality.
"""
from __future__ import annotations
import sys
import subprocess
from typing import Dict, List, Set, Tuple

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, min_degree, powers_of_two_up_to, has_cycle_len_dfs, Graph


def read_graph6_line(line: str) -> Graph:
    import networkx as nx
    G = nx.from_graph6_bytes(line.strip().encode())
    n = G.number_of_nodes()
    edges = list(G.edges())
    return from_edges(n, edges)


def is_2_degenerate_after_removing(g: Graph, x1: int) -> bool:
    """True iff g - x1 is 2-degenerate: repeatedly peel a vertex of degree
    <=2 in the remaining graph; 2-degenerate iff this empties the graph."""
    remaining = {v: set(nbrs) for v, nbrs in g.items() if v != x1}
    for v in remaining:
        remaining[v] = remaining[v] - {x1}
    changed = True
    while remaining and changed:
        changed = False
        low = [v for v, nbrs in remaining.items() if len(nbrs) <= 2]
        for v in low:
            for w in remaining[v]:
                remaining[w].discard(v)
            del remaining[v]
            changed = True
    return len(remaining) == 0


def defect_stats(g: Graph) -> Dict:
    n = len(g)
    m = sum(len(nbrs) for nbrs in g.values()) // 2
    excess = 2 * m - 3 * n
    D = 2 * n - 2 - m
    mindeg = min_degree(g)

    spectrum = {}
    for L in powers_of_two_up_to(n):
        spectrum[L] = has_cycle_len_dfs(g, L)
    missing = [L for L, present in spectrum.items() if not present]

    bound_3b_holds = D <= (n // 2) - 2          # proved bound
    target_disproof_holds = not (n <= 2 * D + 3)  # disproof: this should ALWAYS hold

    deg3_vertices = [v for v in g if len(g[v]) == 3]
    degeneracy_results = {}
    for x1 in deg3_vertices:
        degeneracy_results[x1] = is_2_degenerate_after_removing(g, x1)

    return dict(
        n=n, m=m, excess=excess, D=D, mindeg=mindeg,
        spectrum_present=[L for L, p in spectrum.items() if p],
        spectrum_missing=missing,
        bound_3b_holds=bound_3b_holds,
        target_disproof_holds=target_disproof_holds,
        deg3_vertices=deg3_vertices,
        degeneracy_after_removal=degeneracy_results,
        any_deg3_gives_2degenerate=any(degeneracy_results.values()) if degeneracy_results else None,
        all_deg3_give_2degenerate=all(degeneracy_results.values()) if degeneracy_results else None,
    )


def run_geng_stream(n: int, extra_args: List[str]) -> List[str]:
    cmd = ["geng", "-c"] + extra_args + [str(n)]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    lines = [l for l in out.stdout.splitlines() if l.strip()]
    return lines


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=4)
    ap.add_argument("--nmax", type=int, default=12)
    ap.add_argument("--cubic-only", action="store_true")
    ap.add_argument("--c4free", action="store_true")
    args = ap.parse_args()

    total_graphs = 0
    bound_violations = 0
    disproof_violations = 0
    always_2deg = 0
    sometimes_not_2deg = 0
    never_2deg = 0
    example_not_2deg = None
    v1_violations = []

    for n in range(args.nmin, args.nmax + 1):
        extra = ["-d3"]
        if args.cubic_only:
            extra += ["-D3"]
        if args.c4free:
            extra += ["-f"]
        lines = run_geng_stream(n, extra)
        for g6 in lines:
            g = read_graph6_line(g6)
            if min_degree(g) < 3:
                continue
            st = defect_stats(g)
            total_graphs += 1
            if not st["bound_3b_holds"]:
                bound_violations += 1
                print(f"BOUND-3b VIOLATION n={n} g6={g6} D={st['D']}")
            if not st["target_disproof_holds"]:
                disproof_violations += 1
                print(f"DISPROOF-EXPECTATION VIOLATED (target held!) n={n} g6={g6} D={st['D']}")
            if len(st["spectrum_missing"]) > st["D"]:
                v1_violations.append((n, g6, st))
            dr = st["degeneracy_after_removal"]
            if dr:
                if st["all_deg3_give_2degenerate"]:
                    always_2deg += 1
                elif st["any_deg3_gives_2degenerate"]:
                    sometimes_not_2deg += 1
                else:
                    never_2deg += 1
                    if example_not_2deg is None:
                        example_not_2deg = (n, g6, st)
        print(f"n={n}: {len(lines)} connected delta>=3 graphs processed "
              f"(cumulative total={total_graphs})")

    print("\n=== SUMMARY ===")
    print(f"total graphs checked: {total_graphs}")
    print(f"D<=floor(n/2)-2 (proved bound) violations: {bound_violations}  (must be 0)")
    print(f"n<=2D+3 held anywhere (would refute the S4 disproof): {disproof_violations}  (must be 0)")
    print(f"graphs where EVERY degree-3 x1 gives 2-degenerate G-x1: {always_2deg}")
    print(f"graphs where SOME but not all degree-3 x1 work:         {sometimes_not_2deg}")
    print(f"graphs where NO degree-3 x1 gives 2-degenerate G-x1:    {never_2deg}")
    if example_not_2deg:
        n, g6, st = example_not_2deg
        print(f"example with no working x1: n={n} g6={g6} D={st['D']} deg3={st['deg3_vertices']}")
    print(f"\nV1 candidate ('#missing dyadic lengths <= D') violations: {len(v1_violations)}")
    if v1_violations:
        n, g6, st = min(v1_violations, key=lambda t: t[0])
        print(f"smallest V1 violation: n={n} g6={g6} D={st['D']} "
              f"missing={st['spectrum_missing']} (#missing={len(st['spectrum_missing'])})")


if __name__ == "__main__":
    main()
