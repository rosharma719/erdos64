#!/usr/bin/env python3
"""Extract a minimal unsatisfiable core of quotient-cycle constraints for
each quotient in an already-closed marking census (order16/order18: every
k-marking is eliminated). Per quotient, the full cycle list is "UNSAT" (no
k-subset of V(Q) avoids every cycle's forbidden lift interval) -- this finds
a small IRREDUCIBLE subset of cycles that is already UNSAT by itself, via
greedy deletion: repeatedly try dropping a cycle; keep it dropped if the
remaining set is still UNSAT over all C(n,k) markings.

This turns "784 million individual checks" into "a few dozen small
recurring obstruction patterns" -- the human-lemma-shaped output the
project has been asking for, not a new computation, just a compression of
what the exhaustive census already proved.

Usage:
    python verifier/order30_quotient_unsat_core.py \
        data/order30_quotient_census/quotients_16v_3connected.g6.gz --n 16 --k 7 \
        --sample 100 --output data/order30_quotient_census/unsat_cores_16v_3connected.json
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
import random
import time
from collections import Counter
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


def is_unsat(cmasks: np.ndarray, clens: np.ndarray, markings: np.ndarray) -> bool:
    """True iff every marking is eliminated by this cycle subset alone."""
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
            return True
    return eliminated.all()


def minimal_unsat_core(cmasks: np.ndarray, clens: np.ndarray, markings: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Greedy deletion MUS extraction: drop cycles one at a time (longest
    first, so the core tends toward short/cheap cycles) while the remainder
    stays UNSAT."""
    order = np.argsort(-clens)  # try dropping long cycles first
    keep = list(range(len(clens)))
    idx_order = [int(i) for i in order]
    for i in idx_order:
        if i not in keep:
            continue
        trial = [j for j in keep if j != i]
        if not trial:
            continue
        if is_unsat(cmasks[trial], clens[trial], markings):
            keep = trial
    keep = sorted(keep)
    return cmasks[keep], clens[keep]


def core_signature(clens: np.ndarray) -> str:
    return ",".join(str(x) for x in sorted(clens.tolist()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--sample", type=int, default=200, help="number of quotients to core-extract (random sample)")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    n, k = args.n, args.k
    g6s = load_catalog(args.catalog)
    random.seed(args.seed)
    sample = g6s if len(g6s) <= args.sample else random.sample(g6s, args.sample)

    markings = all_markings(n, k)
    assert markings.shape[0] == math.comb(n, k)

    t0 = time.time()
    core_sizes = []
    signatures = Counter()
    examples: dict[str, dict] = {}

    for qi, g6 in enumerate(sample):
        graph = nx.from_graph6_bytes(g6.encode())
        cmasks, clens = cycle_masks_and_lengths(graph)
        assert is_unsat(cmasks, clens, markings), f"quotient {g6} is NOT fully eliminated -- census assumption violated!"
        core_cmasks, core_clens = minimal_unsat_core(cmasks, clens, markings)
        core_sizes.append(int(core_clens.shape[0]))
        sig = core_signature(core_clens)
        signatures[sig] += 1
        if sig not in examples:
            examples[sig] = {"graph6": g6, "core_lengths": sorted(core_clens.tolist())}

        if (qi + 1) % 25 == 0:
            print(f"  {qi + 1}/{len(sample)} quotients cored, "
                  f"avg core size so far={sum(core_sizes) / len(core_sizes):.2f}, "
                  f"distinct signatures so far={len(signatures)}, elapsed={time.time() - t0:.1f}s", flush=True)

    summary = {
        "catalog": str(args.catalog), "n": n, "k": k,
        "quotients_sampled": len(sample),
        "core_size_min": min(core_sizes), "core_size_max": max(core_sizes),
        "core_size_mean": sum(core_sizes) / len(core_sizes),
        "core_size_histogram": dict(Counter(core_sizes)),
        "distinct_length_signatures": len(signatures),
        "top_signatures": [
            {"lengths": sig, "count": cnt, "example": examples[sig]}
            for sig, cnt in signatures.most_common(20)
        ],
        "elapsed_seconds": time.time() - t0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2))
    print(json.dumps({k2: v for k2, v in summary.items() if k2 != "top_signatures"}, indent=2))
    print("top 5 signatures:")
    for row in summary["top_signatures"][:5]:
        print(" ", row["count"], row["lengths"])


if __name__ == "__main__":
    main()
