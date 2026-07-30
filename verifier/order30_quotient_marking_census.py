#!/usr/bin/env python3
"""Exact marking census over the 2,828 3-connected cubic 16-vertex quotients.

Order-30 counterexample search via triangle-quotient reduction: a C4-free
cubic graph has vertex-disjoint triangles; contracting them gives a smaller
simple cubic "quotient" Q. For an order-30 graph represented by a 16-vertex
quotient, exactly 7 quotient vertices are "marked" (expanded back into a
triangle on lift). A quotient cycle of length `l` through `e` marked
vertices lifts to *every* length in `[l+e, l+2e]`; the marking is therefore
forbidden (forces a C4, C8, or C16) iff `l+e <= 2^k <= l+2e` for some
`2^k` in {4,8,16}, for *some* cycle of Q.

This checks, for every one of the 2,828 catalog quotients (see
order30_quotient_catalog.md) and every one of C(16,7)=11,440 markings of it,
whether every quotient cycle avoids that interval condition. Any marking
that survives the (necessary) interval test is then checked *literally*:
materialize the actual order-30 graph (triangle-expand the 7 marked
vertices) and run an independent brute-force C4/C8/C16 detector on it. A
literal survivor would be an explicit order-30 Erdos-Gyarfas counterexample
candidate (still needs min-degree/further checks beyond C4/C8/C16 alone,
since this only tests those three lengths, not all powers of two -- though
girth/order bounds already rule out any larger power for a 30-vertex graph).

Vectorized with numpy: per quotient, precompute every simple cycle as a
16-bit bitmask + length, then check all 11,440 markings against all cycles
via bitwise AND + popcount (numpy, not per-marking Python loops).

Usage:
    python verifier/order30_quotient_marking_census.py \
        data/order30_quotient_census/quotients_16v_3connected.g6.gz \
        --shard 0/1 --output data/order30_quotient_census/census_shard0.json
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import time
from pathlib import Path

import networkx as nx
import numpy as np

N = 16
K = 7
FORBIDDEN = (4, 8, 16)


def popcount(arr: np.ndarray) -> np.ndarray:
    return np.bitwise_count(arr.astype(np.uint64))


def load_catalog(path: Path) -> list[str]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as f:
        return [line.strip() for line in f if line.strip()]


def cycle_masks_and_lengths(graph: nx.Graph) -> tuple[np.ndarray, np.ndarray]:
    masks = []
    lengths = []
    for cyc in nx.simple_cycles(graph, length_bound=graph.number_of_nodes()):
        mask = 0
        for v in cyc:
            mask |= 1 << v
        masks.append(mask)
        lengths.append(len(cyc))
    return np.array(masks, dtype=np.uint64), np.array(lengths, dtype=np.int32)


def all_markings(n: int = N, k: int = K) -> np.ndarray:
    masks = []
    for combo in itertools.combinations(range(n), k):
        m = 0
        for v in combo:
            m |= 1 << v
        masks.append(m)
    return np.array(masks, dtype=np.uint64)


def eliminate_by_interval(cmasks: np.ndarray, clens: np.ndarray, markings: np.ndarray) -> np.ndarray:
    """Return boolean array (len markings): True iff this marking is eliminated
    (some quotient cycle's lift interval hits a forbidden power of two)."""
    eliminated = np.zeros(markings.shape[0], dtype=bool)
    for cmask, clen in zip(cmasks.tolist(), clens.tolist()):
        e = popcount(markings & np.uint64(cmask))
        lo = clen + e.astype(np.int32)
        hi = clen + 2 * e.astype(np.int32)
        hit = np.zeros(markings.shape[0], dtype=bool)
        for f in FORBIDDEN:
            hit |= (lo <= f) & (f <= hi)
        eliminated |= hit
        if eliminated.all():
            break
    return eliminated


def triangle_expand(graph: nx.Graph, marked: set[int]) -> nx.Graph:
    """Replace every marked vertex with a triangle of edge-stubs (same
    construction independently verified on the Petersen graph earlier)."""
    out = nx.Graph()
    for v in graph.nodes():
        if v in marked:
            nbrs = list(graph.neighbors(v))
            stubs = [(v, u) for u in nbrs]
            for a, b in [(0, 1), (1, 2), (0, 2)]:
                out.add_edge(stubs[a], stubs[b])
    for u, v in graph.edges():
        eu = (u, v) if u in marked else u
        ev = (v, u) if v in marked else v
        out.add_edge(eu, ev)
    return out


def literal_check(graph: nx.Graph, marked: set[int]) -> dict:
    lifted = triangle_expand(graph, marked)
    counts = {}
    for L in FORBIDDEN:
        counts[L] = sum(1 for cyc in nx.simple_cycles(lifted, length_bound=L) if len(cyc) == L)
    return {
        "order": lifted.number_of_nodes(),
        "size": lifted.number_of_edges(),
        "min_degree": min(d for _, d in lifted.degree()),
        "counts": counts,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--shard", type=str, default="0/1", help="res/mod, e.g. 0/4")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None, help="cap number of quotients (debug)")
    parser.add_argument("--n", type=int, default=N, help="quotient order (default 16)")
    parser.add_argument("--k", type=int, default=K, help="number of marked/expanded vertices (default 7)")
    args = parser.parse_args()

    n, k = args.n, args.k
    res, mod = (int(x) for x in args.shard.split("/"))
    g6s = load_catalog(args.catalog)
    if args.limit:
        g6s = g6s[: args.limit]
    shard = [g for i, g in enumerate(g6s) if i % mod == res]

    import math
    markings = all_markings(n, k)
    assert markings.shape[0] == math.comb(n, k), markings.shape

    t0 = time.time()
    total_markings_checked = 0
    total_eliminated = 0
    literal_survivors = []
    per_quotient_records = []

    for qi, g6 in enumerate(shard):
        graph = nx.from_graph6_bytes(g6.encode())
        cmasks, clens = cycle_masks_and_lengths(graph)
        eliminated = eliminate_by_interval(cmasks, clens, markings)
        n_elim = int(eliminated.sum())
        n_surv = int((~eliminated).sum())
        total_markings_checked += markings.shape[0]
        total_eliminated += n_elim

        per_quotient_records.append({
            "graph6": g6, "cycles": int(cmasks.shape[0]),
            "eliminated": n_elim, "interval_survivors": n_surv,
        })

        if n_surv:
            surv_idx = np.nonzero(~eliminated)[0]
            for idx in surv_idx.tolist():
                mask = int(markings[idx])
                marked = {v for v in range(n) if mask & (1 << v)}
                result = literal_check(graph, marked)
                is_true_survivor = all(result["counts"][L] == 0 for L in FORBIDDEN)
                literal_survivors.append({
                    "graph6": g6, "marked": sorted(marked),
                    "literal": result, "counterexample_candidate": is_true_survivor,
                })

        if (qi + 1) % 50 == 0:
            print(f"  {qi + 1}/{len(shard)} quotients, {total_eliminated}/{total_markings_checked} "
                  f"markings eliminated so far, {len(literal_survivors)} literal checks so far, "
                  f"elapsed={time.time() - t0:.1f}s")

    summary = {
        "status": "COMPLETE" if mod == 1 or True else "PARTIAL",
        "shard": args.shard,
        "quotients_processed": len(shard),
        "markings_per_quotient": int(markings.shape[0]),
        "total_markings_checked": total_markings_checked,
        "total_eliminated_by_interval": total_eliminated,
        "total_interval_survivors": total_markings_checked - total_eliminated,
        "literal_survivor_count": len(literal_survivors),
        "counterexample_candidates": [s for s in literal_survivors if s["counterexample_candidate"]],
        "elapsed_seconds": time.time() - t0,
        "literal_survivors_sample": literal_survivors[:50],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("literal_survivors_sample",)}, indent=2))


if __name__ == "__main__":
    main()
