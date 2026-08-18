#!/usr/bin/env python3
"""
EXHAUSTIVE (not sampled) closure attempt for girth-6, case (s=0,a=0).

Every one of the 17 hub topologies has exactly 9 abstract edge/loop slots
(a fixed fact of cubic degree-sum arithmetic: 6 vertices * 3 = 18 half-
edges, and every loop or edge slot consumes exactly 2 half-edges, so
there are always 18/2=9 slots regardless of topology). Distributing the
12 suppressed single-attachment vertices among 9 slots (loops needing
>=1 each) is a composition of 12 into 9 non-negative parts -- at most
C(20,8)=125,970 per topology, ~2.1M total across all 17. This is small
enough to enumerate COMPLETELY via the standard stars-and-bars bijection,
not sample, giving an exhaustive result for this sub-case rather than
statistical evidence.
"""
import itertools
import sys
import time

from verify_s0a0 import build_skeleton, abstract_edges, internal_only_ok, labeling_feasible, skeleton_degrees_ok
from sweep_s0a0 import MATRICES

def compositions(total, k, mins):
    """All ways to write total = sum(parts), len(parts)==k, parts[i]>=mins[i].
    Stars-and-bars: reduce to compositions of (total-sum(mins)) into k
    non-negative parts, then add mins back."""
    reduced = total - sum(mins)
    if reduced < 0:
        return
    if k == 1:
        yield (reduced + mins[0],)
        return
    for combo in itertools.combinations(range(reduced + k - 1), k - 1):
        parts = []
        prev = -1
        for c in combo:
            parts.append(c - prev - 1)
            prev = c
        parts.append(reduced + k - 1 - 1 - prev)
        yield tuple(p + m for p, m in zip(parts, mins))

def run_topology(idx, M, deadline=None):
    slots = abstract_edges(M)
    mins = [1 if s[0] == "loop" else 0 for s in slots]
    n_slots = len(slots)
    total_checked = 0
    internal_ok_count = 0
    feasible = []
    for dist in compositions(12, n_slots, mins):
        total_checked += 1
        lengths = {slot: d for slot, d in zip(slots, dist)}
        adj_precheck, positions_precheck = build_skeleton(M, lengths)
        if not skeleton_degrees_ok(M, adj_precheck) or len(positions_precheck) != 12:
            continue  # degenerate (e.g. parallel length-0 edges collapsed)
        if not internal_only_ok(M, lengths):
            continue
        internal_ok_count += 1
        adj, positions = adj_precheck, positions_precheck
        if labeling_feasible(adj, positions):
            feasible.append(dict(lengths))
    return total_checked, internal_ok_count, feasible

def main():
    t0 = time.time()
    grand_total = 0
    grand_internal_ok = 0
    all_feasible = []
    for idx, M in enumerate(MATRICES):
        checked, internal_ok, feasible = run_topology(idx, M)
        grand_total += checked
        grand_internal_ok += internal_ok
        all_feasible.extend((idx, f) for f in feasible)
        print(f"topology #{idx}: EXHAUSTIVE compositions={checked} "
              f"internal_ok={internal_ok} feasible={len(feasible)} "
              f"(elapsed {time.time()-t0:.0f}s)", flush=True)
    print()
    print(f"GRAND TOTAL exhaustive compositions checked: {grand_total}")
    print(f"passed internal-cycle pre-filter: {grand_internal_ok}")
    print(f"FEASIBLE (labeling avoids all forbidden cycles): {all_feasible or 'NONE -- case (s=0,a=0) FULLY ELIMINATED'}")

if __name__ == "__main__":
    sys.exit(main())
