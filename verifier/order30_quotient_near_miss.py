#!/usr/bin/env python3
"""Mine the already-exhaustive order-16/order-18 quotient catalogs for genuine
order-30 near-miss graphs: markings whose interval test never hits {4} or {8}
(only {16}), i.e. candidates with literal C4=0, C8=0, C16>0.

Every marking in the order-16 (7-triangle) and order-18 (6-triangle) census
was eliminated -- forces at least one of {4,8,16} -- but the census only
recorded *that* a marking was eliminated, not *which* forbidden length(s)
were responsible. This script re-runs the same interval test, this time
tracking hits against {4}, {8}, and {16} separately, to find the markings
that are "cleanest": never forced to hit 4 or 8, only 16. Those get a full
literal C4/C8/C16 count (not just existence) to report the actual near-miss
profile, ranked by total obstruction count (a genuine, exact figure, unlike
the interval test which only proves existence, not the count).

Usage:
    python verifier/order30_quotient_near_miss.py \
        data/order30_quotient_census/quotients_16v_3connected.g6.gz --n 16 --k 7 \
        --output data/order30_quotient_census/near_miss_16v_3connected.json
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
import time
from pathlib import Path

import networkx as nx
import numpy as np

FORBIDDEN = (4, 8, 16)


def popcount(arr: np.ndarray) -> np.ndarray:
    return np.bitwise_count(arr.astype(np.uint64))


def load_catalog(path: Path) -> list[str]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as f:
        return [line.strip() for line in f if line.strip()]


def cycle_masks_and_lengths(graph: nx.Graph) -> tuple[np.ndarray, np.ndarray]:
    masks, lengths = [], []
    for cyc in nx.simple_cycles(graph, length_bound=graph.number_of_nodes()):
        mask = 0
        for v in cyc:
            mask |= 1 << v
        masks.append(mask)
        lengths.append(len(cyc))
    order = sorted(range(len(lengths)), key=lambda i: lengths[i])
    return (np.array([masks[i] for i in order], dtype=np.uint64),
            np.array([lengths[i] for i in order], dtype=np.int32))


def all_markings(n: int, k: int) -> np.ndarray:
    masks = []
    for combo in itertools.combinations(range(n), k):
        m = 0
        for v in combo:
            m |= 1 << v
        masks.append(m)
    return np.array(masks, dtype=np.uint64)


def per_forbidden_hits(cmasks: np.ndarray, clens: np.ndarray, markings: np.ndarray) -> dict[int, np.ndarray]:
    """Return {4: bool array, 8: bool array, 16: bool array} -- for each
    marking, whether *some* quotient cycle's lift interval hits that
    specific forbidden length."""
    hits = {f: np.zeros(markings.shape[0], dtype=bool) for f in FORBIDDEN}
    for cmask, clen in zip(cmasks.tolist(), clens.tolist()):
        e = popcount(markings & np.uint64(cmask))
        lo = clen + e.astype(np.int32)
        hi = clen + 2 * e.astype(np.int32)
        for f in FORBIDDEN:
            hits[f] |= (lo <= f) & (f <= hi)
    return hits


def triangle_expand(graph: nx.Graph, marked: set[int]) -> nx.Graph:
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


def literal_counts(graph: nx.Graph, marked: set[int]) -> dict[int, int]:
    lifted = triangle_expand(graph, marked)
    return {L: sum(1 for c in nx.simple_cycles(lifted, length_bound=L) if len(c) == L) for L in FORBIDDEN}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top", type=int, default=25, help="keep the top-N lowest-obstruction candidates")
    args = parser.parse_args()

    n, k = args.n, args.k
    g6s = load_catalog(args.catalog)
    markings = all_markings(n, k)
    assert markings.shape[0] == math.comb(n, k)

    t0 = time.time()
    clean16_candidates = []  # (graph6, marked_set) never hitting 4 or 8
    best_by_total: list[tuple[int, str, list[int], dict]] = []

    for qi, g6 in enumerate(g6s):
        graph = nx.from_graph6_bytes(g6.encode())
        cmasks, clens = cycle_masks_and_lengths(graph)
        hits = per_forbidden_hits(cmasks, clens, markings)
        clean = (~hits[4]) & (~hits[8])  # never forces C4 or C8 from any single quotient cycle
        idxs = np.nonzero(clean)[0]
        for idx in idxs.tolist():
            mask = int(markings[idx])
            marked = sorted(v for v in range(n) if mask & (1 << v))
            clean16_candidates.append((g6, marked))

        if (qi + 1) % 500 == 0:
            print(f"  {qi + 1}/{len(g6s)} quotients scanned, "
                  f"{len(clean16_candidates)} clean(C4=0,C8=0)-by-interval candidates so far, "
                  f"elapsed={time.time() - t0:.1f}s", flush=True)

    print(f"scan done: {len(clean16_candidates)} candidates never forcing C4/C8 via a single quotient cycle "
          f"out of {len(g6s) * markings.shape[0]:,} total markings, elapsed={time.time() - t0:.1f}s")

    literal_results = []
    for g6, marked in clean16_candidates:
        graph = nx.from_graph6_bytes(g6.encode())
        counts = literal_counts(graph, set(marked))
        literal_results.append({
            "graph6": g6, "marked": marked, "counts": counts,
            "total": sum(counts.values()),
        })

    literal_results.sort(key=lambda r: (r["counts"][4], r["counts"][8], r["total"]))

    summary = {
        "catalog": str(args.catalog), "n": n, "k": k,
        "quotients_scanned": len(g6s),
        "interval_clean_candidates": len(clean16_candidates),
        "literal_checked": len(literal_results),
        "elapsed_seconds": time.time() - t0,
        "best_candidates": literal_results[: args.top],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2))
    print(json.dumps({k2: v for k2, v in summary.items() if k2 != "best_candidates"}, indent=2))
    if literal_results:
        print("best candidate:", json.dumps(literal_results[0], indent=2))


if __name__ == "__main__":
    main()
