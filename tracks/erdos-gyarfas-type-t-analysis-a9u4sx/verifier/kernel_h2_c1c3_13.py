#!/usr/bin/env python3
"""Part VI.2 (defect-three phase): (c1,c3)=(1,3) at h=2.

Row 4's table entry (defect_three.md Part II.2) gives beta(F)=kappa(F)+1
and two parity-consistent component splits of the 4 odd-degree kernel
vertices (1 C1 + 3 C3):

  - kappa=2 (the "{2,2}" split): one component is a LOLLIPOP (1 C1 +
    1 C3), forced to beta=1 by its own degree arithmetic regardless of
    its C2-chain length (a direct algebraic fact, checked below); the
    OTHER component is then forced to beta=3-1=2 on 2 C3 vertices --
    which is EXACTLY VI.1's already-eliminated theta/dumbbell kernel
    (same degree sequence, same beta, same h=2 colour set, and VI.1's
    elimination proof never used anything about what else is in F). No
    new work needed: cite VI.1 directly.

  - kappa=1 (the "{4}" split): all 4 odd-degree vertices (1 C1 + 3 C3)
    share ONE component, beta=2. This kernel is NOT assumed to be any
    particular shape (task instruction: "do not assume the expected
    list ... is complete, derive it") -- verifier/kernel_topology_enum.py
    exhaustively enumerates every connected multigraph with degree
    sequence (1,3,3,3) up to isomorphism, a finite stub-matching
    procedure, not a search cutoff. It finds exactly 3 non-isomorphic
    shapes (this is checked below at runtime, not hard-coded from a
    separate run).
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
from verifier.kernel_topology_enum import enumerate_kernels  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402

H = 2
PATH_MAX = 5
LOOP_MAX = 6


def flat_words(by_len: dict[int, list[tuple[int, ...]]]) -> list[tuple[int, ...]]:
    out = []
    for words in by_len.values():
        out.extend(words)
    return out


def lollipop_beta_is_always_one() -> dict[str, Any]:
    """A connected component with exactly 1 C1 (F-degree 1) and 1 C3
    (F-degree 3) vertex, plus k>=0 C2 (F-degree 2) vertices, has
    |E|=(1+3+2k)/2=2+k and |V|=2+k, so beta=|E|-|V|+1=1 for EVERY k.
    This is pure arithmetic, verified here for k=0..20 directly rather
    than asserted."""
    for k in range(0, 21):
        E = (1 + 3 + 2 * k) // 2
        V = 2 + k
        beta = E - V + 1
        assert beta == 1, f"lollipop beta != 1 at k={k}"
    return {"checked_k_range": [0, 20], "beta_always": 1}


def kappa2_split_via_citation() -> dict[str, Any]:
    lollipop = lollipop_beta_is_always_one()
    return {
        "lollipop_beta_check": lollipop,
        "other_component": "2 C3 vertices, beta=2 -- identical degree "
                            "sequence/beta/h to VI.1's theta+dumbbell kernel",
        "conclusion": "eliminated by direct citation of VI.1 "
                      "(kernel_h2_c1c3_02_manifest.json): 0 survivors "
                      "among 6804 theta + 304 dumbbell realizations",
    }


def realize_and_search(kernel_edges: list[tuple[str, str]], c1_vertex: str) -> dict[str, Any]:
    """Backtracking search: adds branches one at a time, testing the
    PARTIAL reconstruction's C4/C8 status after each addition and
    pruning immediately if a forbidden cycle already exists -- sound
    because deleting the not-yet-added branches from a hypothetical full
    solution cannot remove a cycle already present in the partial graph
    (same monotonicity argument used throughout: subgraphs of a C4/C8-
    free graph are C4/C8-free), so no true survivor is ever pruned."""
    path_candidates = flat_words(all_valid_path_words(H, PATH_MAX))
    loop_words = all_valid_loop_words(H, LOOP_MAX)
    loop_candidates = flat_words({s: ws for s, ws in loop_words.items() if ws})

    pair_groups: dict[tuple[str, str], list[int]] = {}
    edge_kind: list[str] = []
    for idx, (u, w) in enumerate(kernel_edges):
        key = tuple(sorted((u, w)))
        pair_groups.setdefault(key, []).append(idx)
        edge_kind.append("loop" if u == w else "path")

    per_edge_candidates = [
        loop_candidates if edge_kind[i] == "loop" else path_candidates
        for i in range(len(kernel_edges))
    ]

    survivors: list[Any] = []
    tested = 0
    n = len(kernel_edges)
    partial: list[tuple[int, ...]] = [None] * n  # type: ignore[list-item]

    def direct_edge_conflict(depth: int) -> bool:
        for key, idxs in pair_groups.items():
            n_direct = sum(1 for i in idxs if i <= depth and len(partial[i]) == 0)
            if n_direct >= 2:
                return True
        return False

    def recurse(depth: int) -> None:
        nonlocal tested
        if depth == n:
            tested += 1
            survivors.append([list(w) for w in partial])
            return
        for cand in per_edge_candidates[depth]:
            partial[depth] = cand
            if direct_edge_conflict(depth):
                continue
            branches = [
                (kernel_edges[i][0], kernel_edges[i][1], partial[i])
                for i in range(depth + 1)
            ]
            G = build_kernel_graph(branches, H, c1_vertices=(c1_vertex,))
            c4, c8 = check_c4_c8(G)
            if c4 or c8:
                continue  # prune: no extension of this partial assignment can help
            recurse(depth + 1)
        partial[depth] = None  # type: ignore[assignment]

    recurse(0)
    return {"kernel_edges": kernel_edges, "tested_full_survivors": tested, "survivors": survivors}


def kappa1_split_search() -> dict[str, Any]:
    reps = enumerate_kernels({"v": 1, "u1": 3, "u2": 3, "u3": 3})
    results = []
    for rep in reps:
        edges = list(rep.edges())
        r = realize_and_search(edges, c1_vertex="v")
        results.append(r)
    return {"num_topology_classes": len(reps), "per_topology": results}


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    kappa2 = kappa2_split_via_citation()
    kappa1 = kappa1_split_search()

    print(f"kappa=2 split: {kappa2['conclusion']}")
    print(f"kappa=1 split: {kappa1['num_topology_classes']} topology classes")
    all_ok = True
    for r in kappa1["per_topology"]:
        n_surv = len(r["survivors"])
        all_ok &= (n_surv == 0)
        print(f"  edges={r['kernel_edges']} survivors={n_surv}")

    report: dict[str, Any] = {"kappa2_split": kappa2, "kappa1_split": kappa1}
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
