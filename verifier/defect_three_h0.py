#!/usr/bin/env python3
"""Part III.1 (defect-three phase): h=0 case, n=10.

Independent graph6 certificate: every connected cubic graph on 10
vertices contains a C4 or C8 (matching the already-established P4 4-or-8
dichotomy through n=19, re-run standalone here for self-containedness).
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402


def via_geng_cubic(n: int):
    proc = subprocess.Popen(["geng", "-c", "-d3", "-D3", str(n)], stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield nx.from_graph6_bytes(line.encode())
    proc.wait()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    graphs = list(via_geng_cubic(10))
    results = []
    for G in graphs:
        g = from_edges(G.number_of_nodes(), list(G.edges()))
        c4 = has_cycle_len_dfs(g, 4)
        c8 = has_cycle_len_dfs(g, 8)
        c4n = has_cycle_len_nx(g, 4)
        c8n = has_cycle_len_nx(g, 8)
        assert c4 == c4n and c8 == c8n, "detector disagreement"
        results.append((c4, c8))

    all_ok = all(c4 or c8 for c4, c8 in results)
    print(f"n=10 connected cubic graphs: {len(graphs)}; all have C4 or C8: {all_ok}")

    report: dict[str, Any] = {
        "n": 10, "graphs_checked": len(graphs), "all_have_c4_or_c8": all_ok,
    }
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
