#!/usr/bin/env python3
"""General-m passage-level dyadic-cycle conflict enumeration.

The gadget-level general-m attempt (``type_t_port_c16_hypergraph.py``) was
intractable because a naive augmented-graph walk re-tries every candidate
*supplier* of a passage at every intermediate core vertex, and some
vertices sit in 1000+ candidate passages once every triple/gadget
*identity* is counted separately. At the passage level there are only
~1300 distinct passages total on a j=4 instance (vs ~3500-5600
triples/gadgets), and the maximum number of distinct passages touching a
single vertex drops from ~1500 to ~70 (see
``type_t_port_c16_passage_projection.md`` Phase 3) -- small enough that
the straightforward augmented-graph walk this module implements is
tractable directly, with no need for the m=2-specialized reachability-join
trick used in ``type_t_port_c16_passage_catalog.py`` (which this module's
C4/C8 output is cross-checked against as a correctness regression test).

Model: the augmented graph has one weight-1 edge per bare-core edge and one
weight-2 (``p2``) or weight-3 (``p3``) edge per passage. A vertex has at
most one *hub* edge in any real completion (see
``type_t_port_passages.py``'s at-most-one-supplier proof and the
per-vertex-degree argument in this module's docstring below), so a single
simple cycle can use at most one passage at any given vertex -- enforced
by forbidding two consecutive "virtual" (passage) edges in the walk,
exactly as argued for the gadget-level augmented graph in the first
(superseded) attempt in ``type_t_port_short_conflicts.py``'s docstring.

Although a *selected gadget* can simultaneously make several passages
available at one of its vertices (e.g. a linked gadget's ``q1`` supplies
both ``p2[q1,q2]`` and the cross passages ``p3[q1,p1]``, ``p3[q1,p2]``),
any one *cycle* can still only use one of them, because ``q1`` has only
one hub edge in total and a simple cycle uses each vertex's edges at most
once.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from pathlib import Path

from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle, validate_literal_cycle
from type_t_port_multipole_sat import build_catalog
from type_t_port_passages import build_passage_catalog, materialize_passages
from type_t_port_short_conflicts import minimal_supports


def enumerate_passage_conflicts(core, p2, p3, target_length: int,
                                max_m: int | None = None,
                                time_budget_seconds: float | None = None) -> dict:
    """Complete augmented-graph search for passage-level conflicts of a
    given target dyadic length, for any admissible m (Phase 1: 2<=m<=floor(L/3))."""
    core_adj = core.adjacency()
    if max_m is None:
        max_m = max(1, target_length // 3)

    virt: dict[int, list[tuple[int, int, tuple]]] = {v: [] for v in range(core.order)}
    for (u, v) in p2:
        tag = ("p2", (u, v))
        virt[u].append((v, 2, tag))
        virt[v].append((u, 2, tag))
    for (u, v) in p3:
        tag = ("p3", (u, v))
        virt[u].append((v, 3, tag))
        virt[v].append((u, 3, tag))

    def edges_from(vertex):
        for neighbor in core_adj[vertex]:
            yield neighbor, 1, "core", None
        for neighbor, weight, tag in virt[vertex]:
            yield neighbor, weight, "virtual", tag

    results: dict[tuple, dict] = {}
    started = time.monotonic()
    truncated = False

    for start in range(core.order):
        if truncated:
            break
        for n1, w1, kind1, tag1 in edges_from(start):
            if n1 <= start or w1 > target_length:
                continue
            if time_budget_seconds is not None and time.monotonic() - started > time_budget_seconds:
                truncated = True
                break
            start_virtual = kind1 == "virtual"
            support0 = frozenset({tag1}) if start_virtual else frozenset()
            m0 = 1 if start_virtual else 0
            path = [start, n1]
            used = {start, n1}

            def visit(vertex, weight, arrived_virtual, support, m_used):
                nonlocal truncated
                if time_budget_seconds is not None and time.monotonic() - started > time_budget_seconds:
                    truncated = True
                    return
                for neighbor, w, kind, tag in edges_from(vertex):
                    if kind == "virtual" and arrived_virtual:
                        continue
                    new_m = m_used + (1 if kind == "virtual" else 0)
                    if new_m > max_m:
                        continue
                    new_weight = weight + w
                    if new_weight > target_length:
                        continue
                    if neighbor == start:
                        if new_weight != target_length:
                            continue
                        if kind == "virtual" and start_virtual:
                            continue
                        if not (path[1] < vertex):
                            continue
                        new_support = support | ({tag} if kind == "virtual" else set())
                        if not new_support:
                            raise AssertionError("pure-core cycle found; core is dyadic-cycle-free")
                        key = tuple(sorted(new_support))
                        if key not in results:
                            results[key] = {"support": key}
                        continue
                    if neighbor < start or neighbor in used:
                        continue
                    new_support = support | ({tag} if kind == "virtual" else set())
                    used.add(neighbor)
                    path.append(neighbor)
                    visit(neighbor, new_weight, kind == "virtual", new_support, new_m)
                    path.pop()
                    used.discard(neighbor)
                    if truncated:
                        return

            visit(n1, w1, start_virtual, support0, m0)

    return {"results": results, "truncated": truncated, "elapsed_seconds": time.monotonic() - started}


def verify_passage_conflicts(core, target_length: int, results: dict, p2, p3) -> tuple[dict, int]:
    """Materialize a MINIMAL graph containing exactly the claimed passages
    (not a real supplier's full triple/gadget -- see
    ``type_t_port_passages.materialize_passages`` for why that would be
    unsound as a check) and confirm the cycle."""
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--max-m", type=int, default=None)
    parser.add_argument("--time-budget", type=float, default=None)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    core = build_core(args.j, args.a, args.c)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    p2, p3 = build_passage_catalog(triples, gadgets)
    raw = enumerate_passage_conflicts(core, p2, p3, args.length, args.max_m, args.time_budget)
    minimal = minimal_supports(raw["results"])
    verified, rejected = verify_passage_conflicts(core, args.length, minimal, p2, p3)
    verified_minimal = minimal_supports(verified)
    result = {
        "status": "BOUNDED_INCOMPLETE" if raw["truncated"] else "COMPUTATIONALLY_CERTIFIED",
        "parameters": {"j": args.j, "a": args.a, "c": args.c, "length": args.length},
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
            {"support": [[kind, list(key)] for kind, key in support], "witness": verified[support]["witness"]}
            for support in sorted(verified_minimal, key=lambda k: (len(k), k))
        ],
    }
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
