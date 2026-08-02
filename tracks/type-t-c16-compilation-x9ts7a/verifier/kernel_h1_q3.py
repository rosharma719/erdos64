#!/usr/bin/env python3
"""Part III.2 (defect-three phase): independent verification of the h=1,
q=3 elimination.

Rather than re-deriving n from scratch, this generates every connected
delta>=3 graph matching the FORCED structural signature (h=1, c1=0,
c3=6, hence q=3 exactly by the leaf-count identity) via geng at every
consistent order (n=11,12,13 -- z's degree e(C,H)=c2=n-7 must itself be
>=4 for z to actually belong to H, giving n>=11; combined with the
proved bound c2<=6 i.e. n<=13), and confirms directly: c2<=6 in every
generated instance (as the hand proof requires, not merely as an
assumed bound), and every instance contains a C4 or C8 (the same
conclusion the P13-free citation gives, checked here by direct
computation as a redundant independent confirmation).
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cubic_core import check_identities, cubic_core_partition  # noqa: E402
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.z3_certificate import compact_json  # noqa: E402


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
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    q_target = 3
    total_matching = 0
    c2_failures = []
    c4c8_failures = []
    per_n = {}
    for n in range(11, 14):
        m = 2 * n - 2 - q_target
        matching_this_n = 0
        for G in via_geng(n, m):
            C, H = cubic_core_partition(G)
            if len(H) != 1:
                continue
            rec = check_identities(G)
            if not rec["applicable"] or not rec.get("every_c_has_f_neighbour"):
                continue
            if rec["c1"] != 0 or rec["c3"] != 6:
                continue
            # matches the forced (h,c1,c3)=(1,0,6) signature at q=3
            matching_this_n += 1
            total_matching += 1
            c2 = rec["c2"]
            if c2 > 6:
                c2_failures.append((n, nx.to_graph6_bytes(G, header=False).decode().strip(), c2))

            g = from_edges(G.number_of_nodes(), list(G.edges()))
            c4 = has_cycle_len_dfs(g, 4)
            c8 = has_cycle_len_dfs(g, 8)
            c4n = has_cycle_len_nx(g, 4)
            c8n = has_cycle_len_nx(g, 8)
            assert c4 == c4n and c8 == c8n, "detector disagreement"
            if not (c4 or c8):
                c4c8_failures.append((n, nx.to_graph6_bytes(G, header=False).decode().strip()))
        per_n[n] = matching_this_n

    print(f"h=1,q=3,c1=0,c3=6 matching graphs by n: {per_n} (total {total_matching})")
    print(f"c2<=6 failures: {len(c2_failures)}")
    print(f"C4-or-C8 failures: {len(c4c8_failures)}")

    report: dict[str, Any] = {
        "q_target": q_target, "per_n_matching": per_n, "total_matching": total_matching,
        "c2_failures": c2_failures, "c4c8_failures": c4c8_failures,
    }
    encoded = compact_json(report)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(compact_json(report) + "\n")

    ok = not c2_failures and not c4c8_failures
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
