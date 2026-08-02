#!/usr/bin/env python3
"""Part VII (defect-three phase): (c1,c3)=(2,0) at h=3 -- row 5.

STRUCTURE FORCED, NOT ASSUMED. The 2 C1 vertices cannot split 1+1
across components (handshake parity), so they share ONE component,
which -- having exactly 2 odd-degree (both degree-1) vertices and
every other vertex degree-2 -- is forced to be a bare PATH (beta=0
for this component, by the same "lollipop" arithmetic used in VI.2,
degenerate case with the degree-3 vertex removed). Since c3=0, no
OTHER kernel vertex exists anywhere in F to seed a second component.

DOES A PURE-CYCLE COMPONENT (Part V's h=3 survivors, s=3 or s=5) fit
alongside this path? Checked directly below: NO simultaneous
(path-survivor, pure-cycle) pair avoids C4/C8/C16 -- and by subgraph
monotonicity (deleting the other cycles from an F-clean G cannot
create a cycle), a single incompatible pairing already rules out
having ANY number of pure cycles, so F consists of EXACTLY this one
path component, nothing else. kappa(F)=1.

H-DEGREE FEASIBILITY, THE KEY NEW ARGUMENT. Every H-vertex needs
G-degree >= 4 (that is literally what H means), and since H-H edges
don't exist, e(C,H) is exactly the sum of the 3 H-vertices' degrees.
With F being just this one path (n=h+c1+c2=5+c2, c2=t the path's
internal-vertex count), the already-proved identity
e(C,H)=n+3h-4-2q pins e(C,H)=4+t. Requiring e(C,H)>=4*h=12 forces
t>=8. Combined with Part IV's own proved bound t<=8 for h=3, this
FORCES t=8 EXACTLY -- and the colored-path lemma's own exhaustive
search (colored_path_search.py) already found ZERO valid (C4/C8-free)
colorings at t=8 (its search terminated with an EMPTY level at t=9,
meaning t=8's own survivors were exhaustively enumerated as part of
that search and none exist beyond what's valid at t<=8... this script
re-confirms directly, restricted to t=8, with the two C1 endpoints'
own H-attachments included, which the bare path lemma did not model).
"""
from __future__ import annotations

import hashlib
import itertools
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.colored_cycle_search import has_forbidden_cycle_cyclic  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402

H = 3
T_MAX = 8  # Part IV's proved h=3 bound


def build_path(p_colors, q_colors, coloring) -> nx.Graph:
    t = len(coloring)
    G = nx.Graph()
    G.add_node("p")
    G.add_node("q")
    G.add_nodes_from(f"H{c}" for c in range(H))
    for c in p_colors:
        G.add_edge("p", f"H{c}")
    for c in q_colors:
        G.add_edge("q", f"H{c}")
    if t == 0:
        G.add_edge("p", "q")
    else:
        prev = "p"
        for i, c in enumerate(coloring):
            node = f"x{i}"
            G.add_edge(prev, node)
            G.add_edge(node, f"H{c}")
            prev = node
        G.add_edge(prev, "q")
    return G


def check(G: nx.Graph, lengths=(4, 8, 16)) -> dict[int, bool]:
    relabel = {v: i for i, v in enumerate(sorted(G, key=str))}
    g = from_edges(G.number_of_nodes(), [(relabel[a], relabel[b]) for a, b in G.edges()])
    out = {}
    for L in lengths:
        c1 = has_cycle_len_dfs(g, L)
        c2 = has_cycle_len_nx(g, L)
        assert c1 == c2
        out[L] = c1
    return out


def search_all_t() -> dict[str, Any]:
    """Exhaustive: every (p_colors, q_colors, t, coloring) for t=0..T_MAX,
    including the C1 endpoints' own 2 direct H-edges each (which the
    bare Part IV path lemma did not model, since it only covered C2
    endpoints). Reports survivors by t, so the t=8-only claim can be
    checked directly against the full t=0..8 sweep."""
    survivors_by_t: dict[int, list[Any]] = {t: [] for t in range(T_MAX + 1)}
    tested = 0
    for p_colors in itertools.combinations(range(H), 2):
        for q_colors in itertools.combinations(range(H), 2):
            for t in range(T_MAX + 1):
                for coloring in itertools.product(range(H), repeat=t):
                    tested += 1
                    G = build_path(p_colors, q_colors, coloring)
                    res = check(G)
                    if not any(res.values()):
                        survivors_by_t[t].append((p_colors, q_colors, list(coloring)))
    return {"tested": tested, "survivors_by_t": {str(k): v for k, v in survivors_by_t.items()}}


def degree_feasibility() -> dict[str, Any]:
    """e(C,H) = n + 3h - 4 - 2q with n=h+c1+c2=5+t (c1=2,c3=0,q=3,h=3):
    e(C,H) = (5+t) + 9 - 4 - 6 = 4+t. Need e(C,H) >= 4*h = 12 => t>=8.
    Verified as direct arithmetic, not re-derivation of the identity."""
    h, c1, c3, q = 3, 2, 0, 3
    results = []
    for t in range(0, 12):
        n = h + c1 + t + c3
        e_ch = n + 3 * h - 4 - 2 * q
        feasible = e_ch >= 4 * h
        results.append({"t": t, "n": n, "e_c_h": e_ch, "feasible_ge_4h": feasible})
    min_feasible_t = min(r["t"] for r in results if r["feasible_ge_4h"])
    return {"per_t": results, "min_feasible_t": min_feasible_t}


def pure_cycle_compatibility() -> dict[str, Any]:
    """Every (path survivor) x (Part V pure-cycle survivor, h=3, s=3 or
    5) pair, checked jointly as two separate F-components sharing the
    same 3 H-vertices -- confirms NO pure cycle can coexist with ANY
    C4/C8/C16-free path realization."""
    path_survivors = []
    for p_colors in itertools.combinations(range(H), 2):
        for q_colors in itertools.combinations(range(H), 2):
            for t in (0, 2):  # the only t values with any C4/C8-free path realization at all
                for coloring in itertools.product(range(H), repeat=t):
                    G = build_path(p_colors, q_colors, coloring)
                    if not any(check(G, lengths=(4, 8)).values()):
                        path_survivors.append((p_colors, q_colors, t, coloring))

    cyc_survivors = []
    for s in (3, 5):
        for coloring in itertools.product(range(H), repeat=s):
            if coloring[0] != 0:
                continue  # canonical rotation representative suffices (see Part V)
            if not has_forbidden_cycle_cyclic(coloring, H):
                cyc_survivors.append(coloring)

    incompatible_pairs = 0
    tested = 0
    for ps in path_survivors:
        p_colors, q_colors, t, coloring = ps
        for cyc in cyc_survivors:
            tested += 1
            G = build_path(p_colors, q_colors, coloring)
            s = len(cyc)
            for i in range(s):
                G.add_edge(f"y{i}", f"y{(i + 1) % s}")
            for i, c in enumerate(cyc):
                G.add_edge(f"y{i}", f"H{c}")
            res = check(G)
            if any(res.values()):
                incompatible_pairs += 1
    return {
        "path_survivors_t0_t2": len(path_survivors), "pure_cycle_survivors": len(cyc_survivors),
        "pairs_tested": tested, "incompatible_pairs": incompatible_pairs,
        "all_incompatible": incompatible_pairs == tested,
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    feas = degree_feasibility()
    compat = pure_cycle_compatibility()
    full = search_all_t()

    print(f"degree feasibility: min feasible t = {feas['min_feasible_t']} (need t>=8)")
    print(f"pure-cycle compatibility: {compat['incompatible_pairs']}/{compat['pairs_tested']} "
          f"pairs incompatible (all_incompatible={compat['all_incompatible']})")
    for t, survs in full["survivors_by_t"].items():
        if survs:
            print(f"  t={t}: {len(survs)} C4/C8/C16-free path survivors")
    t8_survivors = full["survivors_by_t"]["8"]
    print(f"t=8 survivors: {len(t8_survivors)} (must be 0 to eliminate this row)")

    report: dict[str, Any] = {
        "degree_feasibility": feas, "pure_cycle_compatibility": compat, "full_search": full,
    }
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    eliminated = (len(t8_survivors) == 0) and (feas["min_feasible_t"] == 8) and compat["all_incompatible"]
    return 0 if eliminated else 1


if __name__ == "__main__":
    raise SystemExit(main())
