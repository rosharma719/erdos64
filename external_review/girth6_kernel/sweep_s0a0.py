#!/usr/bin/env python3
"""
Bounded sweep of the girth-6, (s=0,a=0) case across all 17 independently-
verified hub topologies, sampling random length-distributions (summing to
12 across the topology's abstract edges/loops) rather than exhaustively
enumerating all compositions (infeasible in reasonable time: up to ~126,000
per topology, times labeling search for each). This is honestly a sample,
not a proof of this sub-case -- reported as such.
"""
import random
import sys
import time

from verify_s0a0 import (build_skeleton, abstract_edges, internal_only_ok,
                          labeling_feasible)

# the 17 independently-verified connected cubic pseudographs on 6 vertices
MATRICES = [
    [[1,0,0,0,0,1],[0,1,0,0,0,1],[0,0,1,0,1,0],[0,0,0,1,1,0],[0,0,1,1,0,1],[1,1,0,0,1,0]],
    [[1,0,0,0,0,1],[0,1,0,0,0,1],[0,0,1,0,1,0],[0,0,0,0,2,1],[0,0,1,2,0,0],[1,1,0,1,0,0]],
    [[1,0,0,0,0,1],[0,1,0,0,0,1],[0,0,0,1,1,1],[0,0,1,0,2,0],[0,0,1,2,0,0],[1,1,1,0,0,0]],
    [[1,0,0,0,0,1],[0,1,0,0,1,0],[0,0,1,1,0,0],[0,0,1,0,1,1],[0,1,0,1,0,1],[1,0,0,1,1,0]],
    [[1,0,0,0,0,1],[0,1,0,0,1,0],[0,0,0,1,0,2],[0,0,1,0,2,0],[0,1,0,2,0,0],[1,0,2,0,0,0]],
    [[1,0,0,0,0,1],[0,1,0,0,1,0],[0,0,0,1,1,1],[0,0,1,0,1,1],[0,1,1,1,0,0],[1,0,1,1,0,0]],
    [[1,0,0,0,0,1],[0,1,0,0,1,0],[0,0,0,2,0,1],[0,0,2,0,1,0],[0,1,0,1,0,1],[1,0,1,0,1,0]],
    [[1,0,0,0,0,1],[0,0,0,0,1,2],[0,0,0,2,1,0],[0,0,2,0,1,0],[0,1,1,1,0,0],[1,2,0,0,0,0]],
    [[1,0,0,0,0,1],[0,0,0,0,2,1],[0,0,0,2,0,1],[0,0,2,0,1,0],[0,2,0,1,0,0],[1,1,1,0,0,0]],
    [[1,0,0,0,0,1],[0,0,0,1,1,1],[0,0,0,1,1,1],[0,1,1,0,1,0],[0,1,1,1,0,0],[1,1,1,0,0,0]],
    [[1,0,0,0,0,1],[0,0,0,1,1,1],[0,0,0,1,2,0],[0,1,1,0,0,1],[0,1,2,0,0,0],[1,1,0,1,0,0]],
    [[0,0,0,0,1,2],[0,0,0,1,1,1],[0,0,0,2,1,0],[0,1,2,0,0,0],[1,1,1,0,0,0],[2,1,0,0,0,0]],
    [[0,0,0,0,1,2],[0,0,0,1,2,0],[0,0,0,2,0,1],[0,1,2,0,0,0],[1,2,0,0,0,0],[2,0,1,0,0,0]],
    [[0,0,0,0,1,2],[0,0,1,1,0,1],[0,1,0,1,1,0],[0,1,1,0,1,0],[1,0,1,1,0,0],[2,1,0,0,0,0]],
    [[0,0,0,0,1,2],[0,0,1,1,1,0],[0,1,0,2,0,0],[0,1,2,0,0,0],[1,1,0,0,0,1],[2,0,0,0,1,0]],
    [[0,0,0,1,1,1],[0,0,0,1,1,1],[0,0,0,1,1,1],[1,1,1,0,0,0],[1,1,1,0,0,0],[1,1,1,0,0,0]],
    [[0,0,0,1,1,1],[0,0,1,0,1,1],[0,1,0,1,0,1],[1,0,1,0,1,0],[1,1,0,1,0,0],[1,1,1,0,0,0]],
]

def random_distribution(slots, total, rng, min_per_loop=1):
    """Random non-negative integers per slot summing to `total`, with loops
    forced >=1 (a 0-length loop is a literal self-loop, invalid)."""
    mins = [min_per_loop if slot[0] == "loop" else 0 for slot in slots]
    remaining = total - sum(mins)
    if remaining < 0:
        return None
    # stars and bars via random cut points
    cuts = sorted(rng.randint(0, remaining) for _ in range(len(slots) - 1))
    extra = [cuts[0]] + [cuts[i] - cuts[i - 1] for i in range(1, len(cuts))] + [remaining - cuts[-1]] if cuts else [remaining]
    return [m + e for m, e in zip(mins, extra)]

def main():
    rng = random.Random(123)
    t0 = time.time()
    budget = 150
    total_tested = 0
    total_internal_ok = 0
    feasible_found = []
    for idx, M in enumerate(MATRICES):
        slots = abstract_edges(M)
        n_slots = len(slots)
        trials = 0
        internal_ok_here = 0
        while time.time() - t0 < budget * (idx + 1) / len(MATRICES):
            dist = random_distribution(slots, 12, rng)
            if dist is None:
                break
            trials += 1
            lengths = {slot: d for slot, d in zip(slots, dist)}
            if not internal_only_ok(M, lengths):
                continue
            internal_ok_here += 1
            adj, positions = build_skeleton(M, lengths)
            if len(positions) != 12:
                continue
            if labeling_feasible(adj, positions):
                feasible_found.append((idx, dict(lengths)))
        total_tested += trials
        total_internal_ok += internal_ok_here
        print(f"topology #{idx}: trials={trials} internal_ok={internal_ok_here} "
              f"(elapsed {time.time()-t0:.0f}s)", flush=True)
    print()
    print(f"TOTAL: {total_tested} distributions sampled across 17 topologies, "
          f"{total_internal_ok} passed the internal-cycle pre-filter")
    print("FEASIBLE (labeling avoids all forbidden cycles):", feasible_found or "NONE FOUND")

if __name__ == "__main__":
    sys.exit(main())
