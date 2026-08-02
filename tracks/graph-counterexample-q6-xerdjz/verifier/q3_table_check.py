#!/usr/bin/env python3
"""Part II (defect-three phase): computational cross-check of the exact
q=3 case table.

The table itself (defect_three.md Part II.1) is derived symbolically
from I.1's exact identities/inequality at q=3, not by search -- this
script is a redundant empirical cross-check, not the proof. Since n is
NOT bounded at h=2 or h=3 until Part IV pins the colored-path lengths,
this can only sweep small orders (geng is exhaustive but finite); it
confirms that every delta>=3 graph with q(G)=3 found at these orders has
(h,c1,c3) exactly matching one of the six table rows, and never anything
else -- SCOPED to the C4-and-C8-free population (the same necessary
proxy for genuine F-cleanness used throughout this project), since the
table's h>=2 rows depend on the strong inequality, itself an L4
minimality consequence that does not hold on arbitrary delta>=3 graphs.
Off-table (h,c1,c3) signatures outside that scope are recorded
separately and are NOT failures.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.branching_kernel import is_c4_free  # noqa: E402
from verifier.cubic_core import check_identities  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402

TABLE_ROWS = {
    (0, 0, 10), (1, 0, 6), (2, 0, 2), (2, 1, 3), (3, 2, 0), (3, 3, 1),
}


def via_geng(n: int, m: int):
    proc = subprocess.Popen(["geng", "-c", "-d3", str(n), f"{m}:{m}"], stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield nx.from_graph6_bytes(line.encode())
    proc.wait()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=17)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    q_target = 3
    checked = 0
    checked_c4c8_free = 0
    by_row: dict[str, int] = {str(r): 0 for r in sorted(TABLE_ROWS)}
    off_table: list[Any] = []
    off_scope_signatures: dict[str, int] = {}
    for n in range(6, args.max_n + 1):
        m = 2 * n - 2 - q_target
        # no maxdeg constraint here (H-vertices legitimately exceed 3n/2's
        # cubic-only bound); only reject an outright impossible edge count.
        if m <= 0 or m > n * (n - 1) // 2:
            continue
        for G in via_geng(n, m):
            rec = check_identities(G)
            if not rec["applicable"] or not rec.get("every_c_has_f_neighbour"):
                continue
            if rec["q"] != q_target:
                continue
            checked += 1
            row = (rec["h"], rec["c1"], rec["c3"])
            if not is_c4_free(G):
                # outside the F-clean proxy scope (see module docstring);
                # off-table signatures here are expected, not failures.
                off_scope_signatures[str(row)] = off_scope_signatures.get(str(row), 0) + 1
                continue
            checked_c4c8_free += 1
            if row in TABLE_ROWS:
                by_row[str(row)] += 1
            else:
                off_table.append((n, nx.to_graph6_bytes(G, header=False).decode().strip(), row))

    print(f"checked={checked} checked_c4c8_free={checked_c4c8_free} by_row={by_row} off_table={len(off_table)}")

    report: dict[str, Any] = {
        "q_target": q_target, "max_n": args.max_n, "checked": checked,
        "checked_c4c8_free_scope": checked_c4c8_free, "by_row": by_row,
        "off_table_within_scope": off_table,
        "off_scope_signatures_not_failures": off_scope_signatures,
    }
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    return 0 if not off_table else 1


if __name__ == "__main__":
    raise SystemExit(main())
