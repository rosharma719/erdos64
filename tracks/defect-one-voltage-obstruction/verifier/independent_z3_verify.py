#!/usr/bin/env python3
"""Independent Python audit of the exhaustive C++ Z3-lift enumeration."""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verifier.cycle_detect import has_cycle_len_dfs
from verifier.z3_lifts import (
    BASE_NAMES,
    lift_detector_graph,
    load_base,
    voltage_vector,
)


ROOT = Path(__file__).resolve().parents[1]
BASES = None


def _initialize() -> None:
    global BASES
    BASES = [load_base(index) for index in range(4)]


def _verify_chunk(task: tuple[int, list[int]]) -> tuple[int, list[dict]]:
    base_index, assignments = task
    base = BASES[base_index]
    failures = []
    for assignment in assignments:
        graph = lift_detector_graph(base, voltage_vector(assignment))
        c8 = has_cycle_len_dfs(graph, 8)
        c16 = has_cycle_len_dfs(graph, 16)
        if c8 or not c16:
            failures.append({"base": base_index, "assignment": assignment, "c8": c8, "c16": c16})
    return len(assignments), failures


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _cycle_is_valid(graph, cycle: list[int]) -> bool:
    return len(cycle) == len(set(cycle)) and all(
        cycle[(i + 1) % len(cycle)] in graph[cycle[i]] for i in range(len(cycle))
    )


def verify(workers: int, chunk_size: int, random_per_base: int) -> dict:
    started = time.monotonic()
    summaries = []
    all_tasks = []
    after8_sets = []
    expected_total = 0
    for base_index in range(4):
        summary_path = ROOT / "logs" / "z3_lifts" / f"base{base_index}-full.json"
        survivor_path = ROOT / "data" / "z3_lifts" / "results" / f"base{base_index}-full.after8.txt"
        summary = json.loads(summary_path.read_text())
        assignments = [int(line) for line in survivor_path.read_text().splitlines()]
        if len(assignments) != summary["survivors"]["8"]:
            raise AssertionError("after8 file count does not match shard summary")
        if assignments != sorted(set(assignments)):
            raise AssertionError("after8 assignment indices are not unique and sorted")
        if summary["survivors"]["16"] != 0:
            raise AssertionError("this verifier expects the recorded after16 set to be empty")
        expected_total += len(assignments)
        after8_sets.append(set(assignments))
        summaries.append(
            {
                "base_index": base_index,
                "summary_sha256": _sha256(summary_path),
                "after8_sha256": _sha256(survivor_path),
                "after8_assignments": len(assignments),
            }
        )
        for offset in range(0, len(assignments), chunk_size):
            all_tasks.append((base_index, assignments[offset : offset + chunk_size]))

    checked = 0
    failures = []
    context = mp.get_context("spawn")
    with context.Pool(processes=workers, initializer=_initialize) as pool:
        for count, chunk_failures in pool.imap_unordered(_verify_chunk, all_tasks, chunksize=1):
            checked += count
            failures.extend(chunk_failures)
    if checked != expected_total:
        raise AssertionError("independent survivor audit did not cover every assignment")

    # Deterministic random audit includes both assignments rejected at C8 and
    # assignments reaching C16. Membership in the retained file is the C++
    # oracle; the Python DFS independently checks the corresponding outcome.
    rng = random.Random(0xE6403)
    random_checked = 0
    random_failures = []
    for base_index in range(4):
        base = load_base(base_index)
        chosen = rng.sample(range(1, 3**13), random_per_base)
        for assignment in chosen:
            graph = lift_detector_graph(base, voltage_vector(assignment))
            c4 = has_cycle_len_dfs(graph, 4)
            c8 = has_cycle_len_dfs(graph, 8)
            expected_c8 = assignment not in after8_sets[base_index]
            c16 = has_cycle_len_dfs(graph, 16) if not c8 else None
            if c4 or c8 != expected_c8 or (not c8 and not c16):
                random_failures.append(
                    {
                        "base": base_index,
                        "assignment": assignment,
                        "c4": c4,
                        "c8": c8,
                        "expected_c8": expected_c8,
                        "c16": c16,
                    }
                )
            random_checked += 1

    # Validate every stored sample witness independently from the search code.
    witness_checks = []
    for base_index in range(4):
        summary_path = ROOT / "logs" / "z3_lifts" / f"base{base_index}-full.json"
        summary = json.loads(summary_path.read_text())
        base = load_base(base_index)
        for length in (8, 16):
            record = summary["first_rejection_witnesses"][str(length)]
            graph = lift_detector_graph(base, voltage_vector(record["assignment"]))
            valid = len(record["cycle"]) == length and _cycle_is_valid(graph, record["cycle"])
            witness_checks.append({"base": base_index, "length": length, "valid": valid})

    elapsed = time.monotonic() - started
    return {
        "schema": "erdos64-z3-independent-audit-v1",
        "detector": "verifier/cycle_detect.py::has_cycle_len_dfs",
        "constructor": "verifier/z3_lifts.py::lift_detector_graph",
        "workers": workers,
        "chunk_size": chunk_size,
        "stage_survivors_checked": checked,
        "stage_survivor_failures": failures,
        "random_seed": "0xE6403",
        "random_assignments_per_base": random_per_base,
        "random_assignments_checked": random_checked,
        "random_failures": random_failures,
        "witness_checks": witness_checks,
        "all_witnesses_valid": all(item["valid"] for item in witness_checks),
        "elapsed_seconds": elapsed,
        "shards": summaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=1000)
    parser.add_argument("--random-per-base", type=int, default=256)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.workers, args.chunk_size, args.random_per_base)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        f"stage_survivors={report['stage_survivors_checked']} "
        f"stage_failures={len(report['stage_survivor_failures'])} "
        f"random={report['random_assignments_checked']} "
        f"random_failures={len(report['random_failures'])} "
        f"witnesses_valid={report['all_witnesses_valid']} "
        f"elapsed={report['elapsed_seconds']:.3f}s"
    )
    return int(
        bool(report["stage_survivor_failures"])
        or bool(report["random_failures"])
        or not report["all_witnesses_valid"]
    )


if __name__ == "__main__":
    raise SystemExit(main())
