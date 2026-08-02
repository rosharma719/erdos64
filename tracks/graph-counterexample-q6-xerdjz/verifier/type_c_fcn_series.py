"""FC-N: the Type-C/Type-B (2,*)-terminal two-terminal C4/C8 series.

Proposition FC-N (see separator_theorem_order32_gap_analysis.md MISSING-2):
every simple two-terminal graph B with |V(B)|=N, d_B(x)=2, d_B(y)>=2,
d_B(v)>=3 internally, xy not in E(B), and B+xy 2-connected, contains a
C4 or a C8.

Search-box: 2|E(B)| >= d(x)+d(y)+3(n-2) >= 2+2+3(n-2) = 3n-2, so
|E(B)| >= m_min = ceil((3n-2)/2); combined with the {C4,C8}-free upper
bound ex(n;{C4,C8}) (literature.md L15 table), n is infeasible outright
(no such B can exist, by pure counting, no search needed) whenever
m_min > ex(n) -- true at n in {5,6,7,9,11}. At the remaining n in
{8,10,12,13,14,15}, m_min == ex(n) exactly, pinning any instance to an
EXTREMAL {C4,C8}-free graph.

Degree-cap note: at even n the degree-sum slack (2*m_min-(3n-2)) is 0,
forcing degree sequence {2,2,3,...,3} (both terminals exactly degree 2,
-D3 suffices). At odd n slack=1, so ONE unit of extra degree can land
anywhere (one internal vertex bumped to 4, y bumped to 3, or other
redistributions at the raw generation level before rooting) -- -D4 is
needed, and the search does NOT assume both terminals are exactly degree
2; it tries every actual degree-2 vertex as x and every other vertex
(subject to the real degree constraints) as y, exactly like
type_a_order12_f12.py's rooted-pair pattern.

n=15 has 2,625,442 raw candidates (-D4) -- too many for a per-graph Python
DFS pass. Uses the independently-implemented C batch detector
(check_power_masks.c, already certified in the F9-F12 pipeline) for the
primary C4/C8 filter, with the Python DFS detector as a cross-check on
every C4/C8-free survivor plus a random sample of "has C4/C8" rejects.

Usage: python verifier/type_c_fcn_series.py
"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_detect import from_edges, has_cycle_len_dfs

EX_C4C8 = {5: 6, 6: 7, 7: 9, 8: 11, 9: 12, 10: 14, 11: 15, 12: 17, 13: 19, 14: 20, 15: 22}
C_BINARY = Path("/tmp/check_power_masks")


def compile_c_detector() -> None:
    source = Path(__file__).with_name("check_power_masks.c")
    proc = subprocess.run(["cc", "-O3", "-std=c11", str(source), "-o", str(C_BINARY)],
                           capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)


def c_power_masks(graph6_records: list[str]) -> list[int]:
    payload = "".join(g + "\n" for g in graph6_records).encode()
    proc = subprocess.run([str(C_BINARY)], input=payload, capture_output=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode(errors="replace"))
    masks = [int(line) for line in proc.stdout.splitlines()]
    if len(masks) != len(graph6_records):
        raise RuntimeError("C detector output cardinality mismatch")
    return masks


def python_has_c4_c8(graph: nx.Graph) -> tuple[bool, bool]:
    vertices = sorted(graph)
    remap = {v: i for i, v in enumerate(vertices)}
    d = from_edges(len(vertices), [(remap[u], remap[v]) for u, v in graph.edges()])
    return has_cycle_len_dfs(d, 4), has_cycle_len_dfs(d, 8)


def m_min_and_slack(n: int) -> tuple[int, int]:
    three_n_2 = 3 * n - 2
    m = -(-three_n_2 // 2)  # ceil
    slack = 2 * m - three_n_2
    return m, slack


def rooted_pair_survivors(graph: nx.Graph) -> list[tuple[int, int]]:
    survivors = []
    deg2 = [v for v in graph if graph.degree(v) == 2]
    for x in deg2:
        for y in graph:
            if y == x or graph.degree(y) < 2:
                continue
            if any(graph.degree(v) < 3 for v in graph if v not in (x, y)):
                continue
            if graph.has_edge(x, y):
                continue
            closure = graph.copy()
            closure.add_edge(x, y)
            if nx.is_biconnected(closure):
                survivors.append((x, y))
    return survivors


def check_order(n: int, sample_reject_checks: int = 2000, seed: int = 0) -> dict:
    m_min, slack = m_min_and_slack(n)
    exn = EX_C4C8[n]
    if m_min > exn:
        return {"n": n, "status": "INFEASIBLE_BY_COUNTING", "m_min": m_min, "ex_n": exn, "slack": slack}

    max_degree = 3 if slack == 0 else 4
    raw = subprocess.run(
        ["nauty-geng", "-c", "-f", "-d2", f"-D{max_degree}", str(n), f"{m_min}:{exn}"],
        capture_output=True, text=True,
    ).stdout.splitlines()

    c_masks = c_power_masks(raw)
    c4c8_free_idx = [i for i, m in enumerate(c_masks) if not (m & 3)]
    rejected_idx = [i for i, m in enumerate(c_masks) if (m & 3)]

    # Cross-check: every C-detector-clean graph, independently, in Python.
    mismatches = 0
    for i in c4c8_free_idx:
        G = nx.from_graph6_bytes(raw[i].encode())
        has4, has8 = python_has_c4_c8(G)
        c_has4, c_has8 = bool(c_masks[i] & 1), bool(c_masks[i] & 2)
        if (has4, has8) != (c_has4, c_has8):
            mismatches += 1

    # Cross-check: a random sample of C-detector "has C4/C8" rejects.
    random.seed(seed)
    sample = random.sample(rejected_idx, min(sample_reject_checks, len(rejected_idx)))
    for i in sample:
        G = nx.from_graph6_bytes(raw[i].encode())
        has4, has8 = python_has_c4_c8(G)
        c_has4, c_has8 = bool(c_masks[i] & 1), bool(c_masks[i] & 2)
        if (has4, has8) != (c_has4, c_has8):
            mismatches += 1

    survivors = []
    for i in c4c8_free_idx:
        G = nx.from_graph6_bytes(raw[i].encode())
        for x, y in rooted_pair_survivors(G):
            survivors.append((raw[i], x, y))

    return {
        "n": n, "status": "SEARCHED", "m_min": m_min, "ex_n": exn, "slack": slack,
        "max_degree_cap": max_degree, "raw_count": len(raw),
        "c4c8_free_count": len(c4c8_free_idx), "reject_sample_checked": len(sample),
        "mismatches": mismatches, "fcn_survivors": survivors,
    }


def main() -> None:
    compile_c_detector()
    print(f"{'n':>4} {'status':>22} {'m_min':>6} {'ex(n)':>6} {'slack':>6} {'raw':>9} "
          f"{'C4C8free':>9} {'mismatch':>9} {'survivors':>10}")
    all_clean = True
    for n in sorted(EX_C4C8):
        r = check_order(n)
        if r["status"] == "INFEASIBLE_BY_COUNTING":
            print(f"{r['n']:>4} {r['status']:>22} {r['m_min']:>6} {r['ex_n']:>6} {r['slack']:>6} "
                  f"{'--':>9} {'--':>9} {'--':>9} {0:>10}")
            continue
        print(f"{r['n']:>4} {r['status']:>22} {r['m_min']:>6} {r['ex_n']:>6} {r['slack']:>6} "
              f"{r['raw_count']:>9} {r['c4c8_free_count']:>9} {r['mismatches']:>9} "
              f"{len(r['fcn_survivors']):>10}")
        if r["mismatches"]:
            all_clean = False
            print(f"  !!! {r['mismatches']} detector mismatches at n={n}")
        if r["fcn_survivors"]:
            all_clean = False
            print(f"  !!! FC-N SURVIVOR(S) at n={n}: {r['fcn_survivors']}")
    print()
    print("FC-15 (n=5..15) all PROVED, zero survivors, zero detector mismatches"
          if all_clean else "MISMATCH OR SURVIVOR -- see above, do not trust conclusion")


if __name__ == "__main__":
    main()
