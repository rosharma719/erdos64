#!/usr/bin/env python3
"""Specialized ``m=5`` C16 passage-level compiler.

Phase 1 (``type_t_port_c16_compilation.md``) proves ``2 <= m <= floor(L/3)``;
for ``L=16`` this allows ``m`` up to ``5``. At ``m=5`` the ``(m,r,v)``
identity pins the core-path-length composition down to (at most) two cases,
because ``route_total = m + r`` and ``core_total = L - route_total``, and
every one of the ``m=5`` core-path segments must be ``>=1``:

* ``b=0`` (no ``p3``/cross passage used): all five passages are ``p2``
  (route length 2 each), ``route_total = 10``, ``core_total = 6`` split into
  five positive parts -- the only integer partition of 6 into 5 positive
  parts is ``{2,1,1,1,1}`` (up to which of the five *positions* gets the 2).
* ``b=1`` (exactly one ``p3`` passage; two ``p3``s can never coexist, see
  ``type_t_port_passages.drop_multi_p3_supports``): four ``p2`` + one
  ``p3``, ``route_total = 4*2 + 3 = 11``, ``core_total = 5`` split into five
  positive parts -- the only partition of 5 into 5 positive parts is
  ``{1,1,1,1,1}``.

So every ``m=5`` ``C16`` conflict only ever needs bare-core paths of length
1 or 2 -- never the long, expensive intermediate lengths that make the
general ``enumerate_passage_conflicts(..., max_m=5, ...)`` walk explode
(it also re-derives every ``m<5`` conflict in the same pass, which this
compiler skips entirely). This lets a direct, tightly pruned 5-hop DFS
enumerate the *exact* ``m=5`` case directly, using only ``core_adj``
(length-1 reachability) and a length-2 reachability set built directly from
it (both trivial on a sparse, near-path bare core).
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle, validate_literal_cycle
from type_t_port_multipole_sat import build_catalog
from type_t_port_passages import build_passage_catalog, materialize_passages
from type_t_port_short_conflicts import minimal_supports


def _passage_endpoints(p2, p3):
    ep2 = defaultdict(list)
    for (u, v) in p2:
        ep2[u].append(v)
        ep2[v].append(u)
    ep3 = defaultdict(list)
    for (u, v) in p3:
        ep3[u].append(v)
        ep3[v].append(u)
    return ep2, ep3


def _length2_reach(core_adj):
    """w reachable from v by a simple 2-edge core path (some intermediate
    vertex, w != v). Cheap and small on a sparse near-path bare core."""
    order = len(core_adj)
    reach2 = [set() for _ in range(order)]
    for v in range(order):
        for mid in core_adj[v]:
            for w in core_adj[mid]:
                if w != v:
                    reach2[v].add(w)
    return reach2


def enumerate_m5_c16_conflicts(core, p2, p3, time_budget_seconds: float | None = None) -> dict:
    """Exact ``m=5`` search for ``target_length=16`` conflicts, covering
    both the ``b=0`` (five ``p2``s, one core segment of length 2, four of
    length 1) and ``b=1`` (four ``p2``s + one ``p3``, all five core
    segments length 1) cases in a single DFS: at every hop the DFS tries
    every admissible ``(passage, core-step-length)`` combination and simply
    lets the running totals (route length so far, core length so far,
    whether the one allowed ``p3`` has been used, whether the one allowed
    length-2 core step has been used) prune everything that cannot reach
    exactly ``route_total=16`` in exactly 5 hops -- so both cases, and every
    rotation of which of the 5 positions carries the "2" (or, for ``b=1``,
    which of the 5 carries the ``p3``), are explored, without ever needing
    a core-path length other than 1 or 2.
    """
    core_adj = core.adjacency()
    order = core.order
    ep2, ep3 = _passage_endpoints(p2, p3)
    reach2 = _length2_reach(core_adj)

    TARGET = 16
    M = 5
    results: dict[tuple, dict] = {}
    started = time.monotonic()
    truncated = False

    def passage_options(vertex):
        for y in ep2.get(vertex, ()):
            yield "p2", y, 2
        for y in ep3.get(vertex, ()):
            yield "p3", y, 3

    for x1 in range(order):
        if truncated:
            break
        chain: list[tuple] = []
        used = {x1}

        def rec(current_v: int, hop: int, route_used: int, core_used: int,
               p3_used: bool, two_used: bool) -> None:
            nonlocal truncated
            if time_budget_seconds is not None and time.monotonic() - started > time_budget_seconds:
                truncated = True
                return
            remaining_hops = M - hop
            for kind, y, route in passage_options(current_v):
                if y in used:
                    continue
                if kind == "p3" and p3_used:
                    continue
                new_route = route_used + route
                if new_route > TARGET - remaining_hops:  # each remaining hop needs core length >=1
                    continue
                new_p3_used = p3_used or kind == "p3"
                if remaining_hops == 1:
                    # closing hop: single core step (length 1 or, if not
                    # used yet, length 2) directly back to x1.
                    needed = TARGET - new_route - core_used
                    if needed == 1 and x1 in core_adj[y]:
                        key = tuple(sorted(chain + [(kind, (min(current_v, y), max(current_v, y)))]))
                        if key not in results:
                            results[key] = True
                    if needed == 2 and not two_used and x1 in reach2[y]:
                        key = tuple(sorted(chain + [(kind, (min(current_v, y), max(current_v, y)))]))
                        if key not in results:
                            results[key] = True
                    continue
                tag = (kind, (min(current_v, y), max(current_v, y)))
                chain.append(tag)
                used.add(y)
                # length-1 core step
                for x_next in core_adj[y]:
                    if x_next in used or x_next < 0:
                        continue
                    used.add(x_next)
                    rec(x_next, hop + 1, new_route, core_used + 1, new_p3_used, two_used)
                    used.discard(x_next)
                    if truncated:
                        break
                # length-2 core step (only once, only if not used yet)
                if not truncated and not two_used:
                    for x_next in reach2[y]:
                        if x_next in used:
                            continue
                        used.add(x_next)
                        rec(x_next, hop + 1, new_route, core_used + 2, new_p3_used, True)
                        used.discard(x_next)
                        if truncated:
                            break
                used.discard(y)
                chain.pop()
                if truncated:
                    return

        rec(x1, 0, 0, 0, False, False)

    return {"results": results, "truncated": truncated, "elapsed_seconds": time.monotonic() - started}


def verify_conflicts(core, target_length: int, results: dict) -> tuple[dict, int]:
    """Reuses the minimal-graph verification (``materialize_passages`` +
    ``edge_path_cycle``) exactly as in ``type_t_port_c16_passage_hypergraph.py``."""
    verified: dict[tuple, dict] = {}
    rejected = 0
    for support in results:
        graph, adjacency = materialize_passages(core, support)
        witness = edge_path_cycle(adjacency, target_length)
        if witness is None:
            rejected += 1
            continue
        validate_literal_cycle(graph, list(witness))
        verified[support] = {"witness": list(witness)}
    return verified, rejected


def serialize_support(support: tuple) -> list:
    return [[kind, list(key)] for kind, key in support]


def compile_m5(j: int, a: int, c: int, time_budget_seconds: float | None = None) -> dict:
    core = build_core(j, a, c)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    p2, p3 = build_passage_catalog(triples, gadgets)
    raw = enumerate_m5_c16_conflicts(core, p2, p3, time_budget_seconds)
    for support in raw["results"]:
        assert len(support) == 5, f"expected exactly 5 passages, got {len(support)}: {support}"
        assert sum(1 for kind, _ in support if kind == "p3") <= 1
    minimal = minimal_supports(raw["results"])
    verified, rejected = verify_conflicts(core, 16, minimal)
    verified_minimal = minimal_supports(verified)
    return {
        "status": "BOUNDED_INCOMPLETE" if raw["truncated"] else "COMPUTATIONALLY_CERTIFIED",
        "parameters": {"j": j, "Y": 1 << j, "a": a, "c": c},
        "target_length": 16,
        "hub_passages": 5,
        "truncated": raw["truncated"],
        "elapsed_seconds": raw["elapsed_seconds"],
        "raw_candidate_supports": len(raw["results"]),
        "candidate_minimal_supports": len(minimal),
        "verification_rejected": rejected,
        "verified_minimal_supports": len(verified_minimal),
        "support_size_distribution": {
            str(size): sum(1 for key in verified_minimal if len(key) == size)
            for size in sorted({len(key) for key in verified_minimal})
        } if verified_minimal else {},
        "conflicts": [
            {"support": serialize_support(support), "witness": verified_minimal[support]["witness"]}
            for support in sorted(verified_minimal, key=lambda k: (len(k), k))
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--time-budget", type=float, default=None)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_m5(args.j, args.a, args.c, args.time_budget)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.suffix == ".gz":
            args.output.write_bytes(gzip.compress(rendered.encode(), mtime=0))
        else:
            args.output.write_text(rendered)
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
