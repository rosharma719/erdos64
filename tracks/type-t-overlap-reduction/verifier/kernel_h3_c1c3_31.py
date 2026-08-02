#!/usr/bin/env python3
"""Part VII (defect-three phase): (c1,c3)=(3,1) at h=3 -- row 6.

Row 6's parity-consistent splits (II.2): kappa=1 puts all 4 odd-degree
vertices (3 C1 + 1 C3) in one component, forced (a tree on 4 vertices
with degree sequence (1,1,1,3), beta=kappa-1=0) to be the unique STAR
K_{1,3} (centre u, degree 3, C3; leaves v1,v2,v3, degree 1 each, C1).
kappa=2 splits into a LOLLIPOP (1 C3 + 1 C1, beta=1 by the same
degree-arithmetic identity used throughout -- a cycle through the C3
vertex plus a pendant path to the C1 vertex) and a bare PATH (the
other 2 C1's, beta=0, structurally identical to row 5's path
component, but now sharing the SAME 3 H-vertices and H-degree budget
with the lollipop).

Both cases are searched by backtracking (add one branch at a time,
prune the instant a partial reconstruction already has a C4/C8/C16),
using ONLY candidate words already proved complete by Part IV (paths)
and VI.1 (self-loops), plus the H-degree>=4-per-colour feasibility
check applied as a final filter on whatever survives the cycle test.
"""
from __future__ import annotations

import hashlib
import itertools
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.kernel_reconstruction import (  # noqa: E402
    all_valid_loop_words, all_valid_path_words, build_kernel_graph, check_c4_c8,
)
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402

H = 3
PATH_MAX = 8   # Part IV's proved h=3 bound
LOOP_MAX = 6   # extends past VI.1's empirically-found h=2 cutoff; re-checked fresh for h=3 below


def flat_words(by_len):
    out = []
    for words in by_len.values():
        out.extend(words)
    return out


def check_c16(G) -> bool:
    relabel = {v: i for i, v in enumerate(sorted(G, key=str))}
    g = from_edges(G.number_of_nodes(), [(relabel[a], relabel[b]) for a, b in G.edges()])
    c16 = has_cycle_len_dfs(g, 16)
    assert c16 == has_cycle_len_nx(g, 16)
    return c16


def h_degree_ok(G) -> bool:
    return all(G.degree(f"H{c}") >= 4 for c in range(H))


def loop_candidates_h3():
    """h=3 self-loop survivors, freshly computed (VI.1's search was h=2
    only) -- reused verbatim as the loop-branch candidate generator."""
    words = all_valid_loop_words(H, LOOP_MAX)
    return words, flat_words({s: w for s, w in words.items() if w})


def star_search() -> dict[str, Any]:
    path_by_len = all_valid_path_words(H, PATH_MAX)
    path_candidates = flat_words(path_by_len)

    survivors = []
    tested_full = 0
    color_pairs = list(itertools.combinations(range(H), 2))

    def recurse(depth, branches, c1_colors):
        nonlocal tested_full
        if depth == 3:
            G = build_kernel_graph(branches, H, c1_vertices=())
            for v_name, colors in c1_colors.items():
                for c in colors:
                    G.add_edge(v_name, f"H{c}")
            if h_degree_ok(G):
                if not check_c16(G):
                    tested_full += 1
                    survivors.append({
                        "leaf_colors": {k: list(v) for k, v in c1_colors.items()},
                        "branches": [(b[0], b[1], list(b[2])) for b in branches],
                    })
            return
        vname = f"v{depth + 1}"
        for colors in color_pairs:
            for word in path_candidates:
                branch = ("u", vname, word)
                G = build_kernel_graph(branches + [branch], H, c1_vertices=())
                for name, cs in list(c1_colors.items()) + [(vname, colors)]:
                    for c in cs:
                        G.add_edge(name, f"H{c}")
                c4, c8 = check_c4_c8(G)
                if c4 or c8:
                    continue
                new_c1 = dict(c1_colors)
                new_c1[vname] = colors
                recurse(depth + 1, branches + [branch], new_c1)

    recurse(0, [], {})
    return {"topology": "star", "survivors": survivors, "tested_full_h_degree_ok_no_c16": tested_full}


def lollipop_plus_path_search() -> dict[str, Any]:
    path_by_len = all_valid_path_words(H, PATH_MAX)
    path_candidates = flat_words(path_by_len)
    loop_words, loop_candidates = loop_candidates_h3()

    survivors = []
    color_pairs = list(itertools.combinations(range(H), 2))

    def full_check(loop_w, pendant_w, w_colors, path_w, p_colors, q_colors):
        branches = [("u1", "u1", loop_w), ("u1", "w", pendant_w), ("p", "q", path_w)]
        G = build_kernel_graph(branches, H, c1_vertices=())
        for c in w_colors:
            G.add_edge("w", f"H{c}")
        for c in p_colors:
            G.add_edge("p", f"H{c}")
        for c in q_colors:
            G.add_edge("q", f"H{c}")
        c4, c8 = check_c4_c8(G)
        if c4 or c8:
            return None
        if check_c16(G):
            return None
        if not h_degree_ok(G):
            return None
        return G

    tested = 0
    for loop_w in loop_candidates:
        for pendant_w in path_candidates:
            # prune early: lollipop-only partial check
            branches = [("u1", "u1", loop_w), ("u1", "w", pendant_w)]
            for w_colors in color_pairs:
                G_partial = build_kernel_graph(branches, H, c1_vertices=())
                for c in w_colors:
                    G_partial.add_edge("w", f"H{c}")
                c4, c8 = check_c4_c8(G_partial)
                if c4 or c8:
                    continue
                for path_w in path_candidates:
                    for p_colors in color_pairs:
                        for q_colors in color_pairs:
                            tested += 1
                            G = full_check(loop_w, pendant_w, w_colors, path_w, p_colors, q_colors)
                            if G is not None:
                                survivors.append({
                                    "loop": list(loop_w), "pendant": list(pendant_w), "w_colors": list(w_colors),
                                    "path": list(path_w), "p_colors": list(p_colors), "q_colors": list(q_colors),
                                })
    return {"topology": "lollipop+path", "tested": tested, "survivors": survivors}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--skip-lollipop", action="store_true")
    args = parser.parse_args()

    star = star_search()
    print(f"star: survivors(H-degree-ok, no C16)={len(star['survivors'])} "
          f"(full_check_count={star['tested_full_h_degree_ok_no_c16']})")

    report: dict[str, Any] = {"star": star}

    if not args.skip_lollipop:
        lollipop = lollipop_plus_path_search()
        print(f"lollipop+path: tested={lollipop['tested']} survivors={len(lollipop['survivors'])}")
        report["lollipop_plus_path"] = lollipop

    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    ok = not star["survivors"]
    if "lollipop_plus_path" in report:
        ok = ok and not report["lollipop_plus_path"]["survivors"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
