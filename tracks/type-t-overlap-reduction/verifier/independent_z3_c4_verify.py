#!/usr/bin/env python3
"""Exhaustive independent Python C4 audit of every nonzero Z3 assignment."""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.cycle_detect import has_cycle_len_dfs
from verifier.z3_lifts import lift_detector_graph, load_base, voltage_vector


BASES = None
ASSIGNMENTS = 3**13


def _initialize() -> None:
    global BASES
    BASES = [load_base(index) for index in range(4)]


def _check_range(task: tuple[int, int, int]) -> tuple[int, list[int]]:
    base_index, start, end = task
    base = BASES[base_index]
    failures = []
    for assignment in range(start, end):
        graph = lift_detector_graph(base, voltage_vector(assignment))
        if has_cycle_len_dfs(graph, 4):
            failures.append(assignment)
    return end - start, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=5000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    tasks = []
    for base_index in range(4):
        for start in range(1, ASSIGNMENTS, args.chunk_size):
            tasks.append((base_index, start, min(start + args.chunk_size, ASSIGNMENTS)))

    started = time.monotonic()
    checked = 0
    failures = []
    context = mp.get_context("spawn")
    with context.Pool(processes=args.workers, initializer=_initialize) as pool:
        for count, chunk_failures in pool.imap_unordered(_check_range, tasks, chunksize=1):
            checked += count
            failures.extend(chunk_failures)
    elapsed = time.monotonic() - started
    report = {
        "schema": "erdos64-z3-independent-c4-audit-v1",
        "detector": "verifier/cycle_detect.py::has_cycle_len_dfs",
        "constructor": "verifier/z3_lifts.py::lift_detector_graph",
        "assignment_ranges": [[1, ASSIGNMENTS]] * 4,
        "assignments_checked": checked,
        "expected_assignments": 4 * (ASSIGNMENTS - 1),
        "failures": failures,
        "workers": args.workers,
        "chunk_size": args.chunk_size,
        "elapsed_seconds": elapsed,
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"checked={checked} c4_failures={len(failures)} elapsed={elapsed:.3f}s")
    return int(checked != report["expected_assignments"] or bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
