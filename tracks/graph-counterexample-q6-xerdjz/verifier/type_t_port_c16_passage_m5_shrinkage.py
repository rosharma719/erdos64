#!/usr/bin/env python3
"""Measure how much the pending ``m=5`` rerun would shrink the ``m=5`` layer.

``type_t_port_c16_passage_m5.py`` was run before the ``m=4`` layer existed,
so its 2,944,894 supports are complete only *relative to the ``C8/m2/m3``
lower shadow*: a five-passage support that contains one of the 3,971,519
certified ``m=4`` conflicts is subsumed and must not become its own clause.
The full rerun is mechanical but costs real CPU (see
``type_t_port_c16_passage_projection.md``, Phase 7), so this script answers
the cheaper question first: *how much does it actually matter?*

Method (deliberately a bounded sample, and labelled as one):

1. Regenerate the complete ``m=4`` support set in-process (it is committed
   summary-only, so it is not loadable from disk).
2. Re-run the ``m=5`` search on a spread subset of canonical start vertices,
   with the same ``C8/m2/m3`` shadow the committed ``m=5`` layer used, so the
   sampled supports are exactly the ones that layer contains for those starts.
3. Count how many of those five-passage supports contain one of the five
   four-subsets that the ``m=4`` layer certifies as a conflict.

The result is a per-start-vertex domination rate.  It is an estimate of the
shrinkage, not the shrunk catalog: only the full rerun produces that.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

from type_t_port_core_export import build_core
from type_t_port_multipole_sat import build_catalog
from type_t_port_passages import build_passage_catalog

import type_t_port_c16_passage_m4 as m4
import type_t_port_c16_passage_m5 as m5


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--lower-shadow", type=Path, action="append", default=[])
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--m5-start-stride", type=int, default=14,
                        help="sample every Nth canonical start vertex for the m=5 side")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    core = build_core(args.j, args.a, args.c)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    p2, p3 = build_passage_catalog(triples, gadgets)

    shadow_m4 = m4.load_lower_shadow(args.lower_shadow)
    shadow_m5 = m5.load_lower_shadow(args.lower_shadow)

    started = time.monotonic()
    m4_raw = m4.enumerate_m4_parallel(core, p2, p3, shadow_m4, args.workers)
    m4_seconds = time.monotonic() - started
    m4_sets = {frozenset(support) for support in m4_raw["results"]}
    assert m4_raw["x1_completed"] == core.order, "m=4 shadow regeneration must be complete"

    starts = list(range(0, core.order, args.m5_start_stride))
    started = time.monotonic()
    sampled = m5.enumerate_m5_c16_conflicts(
        core, p2, p3, lower_shadow=shadow_m5, start_vertices=starts
    )
    m5_seconds = time.monotonic() - started
    assert not sampled["truncated"]

    dominated = 0
    for support in sampled["results"]:
        keys = sorted(support)
        if any(frozenset(part) in m4_sets for part in itertools.combinations(keys, 4)):
            dominated += 1
    total = len(sampled["results"])

    report = {
        "status": "BOUNDED_SAMPLE_ESTIMATE",
        "parameters": {"j": args.j, "a": args.a, "c": args.c},
        "m4_layer_regenerated_supports": len(m4_sets),
        "m4_regeneration_seconds": m4_seconds,
        "m5_sample_start_vertices": starts,
        "m5_sample_start_count": len(starts),
        "m5_start_total": core.order,
        "m5_sample_seconds": m5_seconds,
        "m5_sampled_supports": total,
        "m5_sampled_supports_dominated_by_an_m4_conflict": dominated,
        "m5_sampled_supports_surviving": total - dominated,
        "domination_rate_on_sample": (dominated / total) if total else None,
        "caveat": (
            "This is a per-start-vertex SAMPLE of the committed m=5 layer, not the rerun. "
            "The sampled starts are a stride subset of the 87 canonical starts, and per-start "
            "support counts are strongly non-uniform under the least-passage-endpoint "
            "canonicalization, so the domination rate here should be read as an order-of-"
            "magnitude indicator for the pending rerun, not as the exact final m=5 count."
        ),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
