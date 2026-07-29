#!/usr/bin/env python3
"""Passage-level static C4/C8 (and, later, C16) conflict compilation.

This mirrors ``type_t_port_short_conflicts.enumerate_m2_conflicts`` exactly
in its join logic (reachability-index symmetry, ``pair_index``-style O(1)
lookups) but is keyed on *passages* -- ``(vertex, vertex, route)`` -- rather
than on the specific triple/gadget tag that happens to supply them. Since a
single passage is supplied by many different tags (14.5 on average, up to
127, on the smallest j=4 instance), this collapses what were previously
many redundant gadget-level clauses expressing the same geometric fact into
one passage-level clause, per the soundness argument in
``type_t_port_c16_passage_projection.md`` Phase 5 (a completion contains the
witnessed cycle whenever *some* selected gadget supplies each named
passage, regardless of which one).
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path

from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle, validate_literal_cycle
from type_t_port_multipole_sat import build_catalog
from type_t_port_passages import build_passage_catalog
from type_t_port_short_conflicts import compute_reach_index, materialize_variables, minimal_supports


def enumerate_m2_passage_conflicts(core, p2, p3, target_length: int) -> dict:
    """Exhaustive m=2 search at passage granularity. Correct/complete for
    any length whose only admissible passage count is m=2 (C4: vacuously
    empty; C8: forced exactly, see the Phase 1 proof)."""
    core_adj = core.adjacency()
    passage_of_route = {2: p2, 3: p3}
    max_core_path = target_length - 4
    reach = compute_reach_index(core_adj, max_core_path) if max_core_path >= 1 else []

    results: dict[tuple, dict] = {}
    for route1, suppliers1 in passage_of_route.items():
        for (x1, y1) in suppliers1:
            for route2, suppliers2 in passage_of_route.items():
                core_total = target_length - route1 - route2
                if core_total < 2:
                    continue
                for l1 in range(1, core_total):
                    l2 = core_total - l1
                    landing = reach[y1].get(l1) if l1 <= max_core_path else None
                    if not landing:
                        continue
                    reach_x1 = reach[x1].get(l2) if l2 <= max_core_path else None
                    if not reach_x1:
                        continue
                    for x2 in landing:
                        if x2 == x1 or x2 == y1:
                            continue
                        for y2 in reach_x1:
                            if y2 == x1 or y2 == y1 or y2 == x2:
                                continue
                            key2 = (min(x2, y2), max(x2, y2))
                            if key2 not in suppliers2:
                                continue
                            passage1 = ("p2" if route1 == 2 else "p3", (x1, y1))
                            passage2 = ("p2" if route2 == 2 else "p3", (min(x2, y2), max(x2, y2)))
                            key = tuple(sorted({passage1, passage2}))
                            if key not in results:
                                results[key] = {"support": key}
    return results


def verify_passage_conflicts(core, target_length: int, results: dict, p2, p3) -> dict:
    """Independent re-check: materialize ONE arbitrary supplier per named
    passage (any supplier works, per the lifting argument -- that is
    exactly the claim being spot-checked here) and confirm the cycle via
    edge_path_cycle, the differently organized detector."""
    verified: dict[tuple, dict] = {}
    rejected = 0
    for support in results:
        tags = set()
        for kind, key in support:
            suppliers = p2[key] if kind == "p2" else p3[key]
            tags.add(suppliers[0])
        graph, adjacency = materialize_variables(core, tuple(sorted(tags)))
        witness = edge_path_cycle(adjacency, target_length)
        if witness is None:
            rejected += 1
            continue
        validate_literal_cycle(graph, list(witness))
        verified[support] = {"witness": list(witness), "example_suppliers": [list(t) for t in tags]}
    return verified, rejected


def serialize_passage_support(support: tuple) -> list:
    return [[kind, list(key)] for kind, key in support]


def compile_instance_passages(j: int, a: int, c: int, lengths: tuple[int, ...] = (4, 8)) -> dict:
    core = build_core(j, a, c)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    p2, p3 = build_passage_catalog(triples, gadgets)
    per_length = {}
    for length in lengths:
        if length not in (4, 8):
            raise ValueError("only the proven m=2 lengths 4 and 8 are supported here")
        raw = enumerate_m2_passage_conflicts(core, p2, p3, length)
        candidate_minimal = minimal_supports(raw)
        verified, rejected = verify_passage_conflicts(core, length, candidate_minimal, p2, p3)
        minimal = minimal_supports(verified)
        per_length[str(length)] = {
            "target_length": length,
            "raw_candidate_supports": len(raw),
            "candidate_minimal_supports": len(candidate_minimal),
            "verification_rejected": rejected,
            "verified_minimal_supports": len(minimal),
            "support_size_distribution": {
                str(size): sum(1 for key in minimal if len(key) == size)
                for size in sorted({len(key) for key in minimal})
            } if minimal else {},
            "conflicts": [
                {"support": serialize_passage_support(support), "witness": verified[support]["witness"]}
                for support in sorted(minimal, key=lambda k: (len(k), k))
            ],
        }
    return {
        "status": "COMPUTATIONALLY_CERTIFIED",
        "parameters": {"j": j, "Y": 1 << j, "a": a, "c": c},
        "catalog_sizes": {"triples": len(triples), "gadgets": len(gadgets), "p2_passages": len(p2), "p3_passages": len(p3)},
        "lengths": per_length,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--lengths", type=int, nargs="+", default=[4, 8])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_instance_passages(args.j, args.a, args.c, tuple(args.lengths))
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
