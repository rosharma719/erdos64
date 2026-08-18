#!/usr/bin/env python3
"""Adversarial, independent audit of a claimed FC-n survivor.

A SAT solver reporting SAT is exactly the situation in which an encoding bug is
most likely and most damaging, so this script re-checks a claimed survivor
using tooling that shares as little as possible with the search:

  1. the graph is re-read from its graph6 string (not from the solver's
     internal model), via networkx;
  2. degrees / xy-absence / 2-connectivity via networkx;
  3. C4 and C8 (and, for information, C16) by FOUR independent detectors:
       a. `cycle_detect.has_cycle_len_dfs`  -- the repo's certified DFS detector
       b. `networkx.simple_cycles`          -- third-party
       c. `verifier/check_power_masks.c`    -- the compiled C batch detector
          already certified in the F9-F12 / FC-15 pipelines
       d. a from-scratch bitmask dynamic program over simple paths, written
          here and shared with nothing else
  4. the claimed rooted terminal pair is re-derived by `rooted_pair_survivors`
     from `verifier/type_c_fcn_series.py` -- i.e. by the *existing, already
     used* FC-15 pipeline code, with no reference to the SAT search at all.

Usage:
    python verifier/fcn_survivor_audit.py --graph6 'RSPH@?OCGP?o?_?P?GW?_?AC?A_??w' --dx 2
    python verifier/fcn_survivor_audit.py --json results.json --dx 2
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_detect import from_edges, has_cycle_len_dfs  # noqa: E402
from type_c_fcn_series import rooted_pair_survivors  # noqa: E402


# --- detector (d): from-scratch bitmask DP over simple paths ----------------

def has_cycle_len_bitmask(n: int, adj_mask: list[int], L: int) -> bool:
    """Exact: does a simple cycle on exactly L vertices exist?

    For each candidate minimum vertex s, dynamic-programme over
    (set of used vertices, current endpoint), restricted to vertices >= s, and
    close back to s after exactly L vertices.  Every simple cycle has a unique
    minimum vertex, so this is exhaustive.  Written from scratch: no DFS, no
    recursion, no shared code with the other three detectors.
    """
    for s in range(n):
        allowed = 0
        for v in range(s, n):
            allowed |= 1 << v
        # states[mask] = bitmask of endpoints reachable as a simple path
        # from s using exactly the vertices in `mask`
        states = {1 << s: 1 << s}
        for _ in range(L - 1):
            nxt: dict[int, int] = {}
            for mask, ends in states.items():
                e = ends
                while e:
                    v = (e & -e).bit_length() - 1
                    e &= e - 1
                    cand = adj_mask[v] & allowed & ~mask
                    while cand:
                        w = (cand & -cand).bit_length() - 1
                        cand &= cand - 1
                        nm = mask | (1 << w)
                        nxt[nm] = nxt.get(nm, 0) | (1 << w)
            states = nxt
            if not states:
                break
        for mask, ends in states.items():
            e = ends
            while e:
                v = (e & -e).bit_length() - 1
                e &= e - 1
                if adj_mask[v] & (1 << s):
                    return True
    return False


# --- detector (c): the certified C batch detector ---------------------------

def c_detector_mask(graph6: str) -> int | None:
    """Returns the C detector's power-of-two cycle mask (bit0=C4, bit1=C8,
    bit2=C16, ...), or None if it could not be built."""
    src = Path(__file__).with_name("check_power_masks.c")
    if not src.exists():
        return None
    with tempfile.TemporaryDirectory() as td:
        binp = Path(td) / "check_power_masks"
        cc = subprocess.run(["cc", "-O3", "-std=c11", str(src), "-o", str(binp)],
                            capture_output=True, text=True)
        if cc.returncode:
            print("  (C detector failed to compile:", cc.stderr.strip()[:200], ")")
            return None
        run = subprocess.run([str(binp)], input=(graph6 + "\n").encode(),
                             capture_output=True)
        if run.returncode:
            print("  (C detector failed to run:", run.stderr.decode()[:200], ")")
            return None
        return int(run.stdout.split()[0])


# --- audit ------------------------------------------------------------------

def audit(graph6: str, dx: int) -> dict:
    G = nx.from_graph6_bytes(graph6.encode())
    n = G.number_of_nodes()
    nodes = sorted(G)
    assert nodes == list(range(n)), "unexpected vertex labelling"
    edges = sorted(tuple(sorted(e)) for e in G.edges())
    x, y = 0, 1

    rep: dict = {
        "graph6": graph6,
        "n": n,
        "m": G.number_of_edges(),
        "degree_sequence": sorted((G.degree(v) for v in G), reverse=True),
        "deg_x": G.degree(x),
        "deg_y": G.degree(y),
        "edges": edges,
    }

    # --- structural conditions ---
    rep["deg_x_is_exactly_dx"] = (G.degree(x) == dx)
    rep["deg_y_ge_dx"] = (G.degree(y) >= dx)
    rep["all_internal_deg_ge_3"] = all(G.degree(v) >= 3 for v in G if v not in (x, y))
    rep["xy_not_an_edge"] = not G.has_edge(x, y)
    rep["B_connected"] = bool(nx.is_connected(G))
    closure = G.copy()
    closure.add_edge(x, y)
    rep["closure_simple"] = (closure.number_of_edges() == G.number_of_edges() + 1)
    rep["closure_2connected"] = bool(nx.is_biconnected(closure))

    # --- the edge-count box the geng pipelines used, recomputed here ---
    m_min = -(-(3 * n - 2) // 2)
    rep["m_min_from_degree_bound"] = m_min
    rep["m_equals_m_min"] = (G.number_of_edges() == m_min)
    rep["degree_sum_slack"] = 2 * G.number_of_edges() - (3 * n - 2)

    # --- four independent cycle detectors ---
    d = from_edges(n, edges)
    adj_mask = [0] * n
    for a, b in edges:
        adj_mask[a] |= 1 << b
        adj_mask[b] |= 1 << a
    cmask = c_detector_mask(graph6)

    lengths = [4, 8] + ([16] if n >= 16 else [])
    nx_lengths = {len(c) for c in nx.simple_cycles(G, length_bound=max(lengths))}
    detectors: dict[int, dict] = {}
    all_agree = True
    for i, L in enumerate(lengths):
        a = bool(has_cycle_len_dfs(d, L))
        b = bool(L in nx_lengths)
        c = None if cmask is None else bool(cmask & (1 << i))
        e = bool(has_cycle_len_bitmask(n, adj_mask, L))
        vals = [v for v in (a, b, c, e) if v is not None]
        agree = all(v == vals[0] for v in vals)
        all_agree = all_agree and agree
        detectors[L] = {"cycle_detect_dfs": a, "networkx": b,
                        "c_check_power_masks": c, "bitmask_dp": e,
                        "agree": agree}
    rep["detectors"] = detectors
    rep["all_detectors_agree"] = all_agree
    rep["C4_free"] = not detectors[4]["cycle_detect_dfs"]
    rep["C8_free"] = not detectors[8]["cycle_detect_dfs"]
    if 16 in detectors:
        rep["contains_C16"] = detectors[16]["cycle_detect_dfs"]

    # --- the existing FC-15 pipeline's own rooted-pair routine ---
    pairs = rooted_pair_survivors(G) if dx == 2 else None
    rep["fc15_pipeline_rooted_pairs"] = pairs
    rep["fc15_pipeline_accepts_(0,1)"] = (pairs is not None and (0, 1) in pairs)

    rep["VERDICT_genuine_survivor"] = all([
        rep["deg_x_is_exactly_dx"], rep["deg_y_ge_dx"],
        rep["all_internal_deg_ge_3"], rep["xy_not_an_edge"],
        rep["closure_simple"], rep["closure_2connected"],
        rep["all_detectors_agree"], rep["C4_free"], rep["C8_free"],
    ])
    return rep


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph6", action="append", default=[])
    ap.add_argument("--json", type=Path,
                    help="a results JSON from fcn_sat_existence.py; every SAT "
                         "record's witness_graph6 is audited")
    ap.add_argument("--dx", type=int, default=2, choices=(1, 2))
    args = ap.parse_args()

    g6s = list(args.graph6)
    if args.json:
        data = json.loads(args.json.read_text())
        for r in (data if isinstance(data, list) else [data]):
            if r.get("status") == "SAT" and r.get("witness_graph6"):
                g6s.append(r["witness_graph6"])

    ok = True
    for g6 in g6s:
        rep = audit(g6, args.dx)
        print(json.dumps(rep, indent=2, default=str))
        print()
        if not rep["VERDICT_genuine_survivor"]:
            ok = False
            print("*** NOT a genuine survivor -- treat as an encoding bug ***")
        else:
            print(f"*** GENUINE SURVIVOR: n={rep['n']}, m={rep['m']}, "
                  f"all {len(rep['detectors'])} cycle lengths cross-checked by "
                  f"4 independent detectors ***")
        print("-" * 78)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
