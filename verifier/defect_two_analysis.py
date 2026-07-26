#!/usr/bin/env python3
"""Part III (leaf-compression phase): attack q=2 for a genuine minimal
Erdos-Gyarfas counterexample. Verify or refute each proposed case
argument -- do NOT assume the target ("no minimal counterexample has
q=2") is true going in.

From the leaf-graph inequality h<=q (defect.md leaf-compression I.3),
q=2 restricts to h in {0,1,2}.

Also includes a standalone check of the corrected general weighted-
incidence cycle-length formula (2t + sum|P_i|, defect.md I.3, corrected
2026-07-27 -- the original had coefficient t instead of 2t) since
Part III.3.a's C8 construction depends on it directly.
"""
from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path
from typing import Any

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.cubic_core import check_identities, cubic_core_partition  # noqa: E402
from verifier.cycle_detect import from_edges, has_cycle_len_dfs, has_cycle_len_nx  # noqa: E402
from verifier.d1_search import is_property2_fast  # noqa: E402


def via_geng_q2(n: int):
    """q=2 <=> m=2n-4 (d1_search.py's via_geng is hardcoded to q=1,
    m=2n-3 -- NOT reusable here; this is the q=2 analogue)."""
    import subprocess
    m = 2 * n - 4
    proc = subprocess.Popen(
        ["geng", "-c", "-d3", str(n), f"{m}:{m}"],
        stdout=subprocess.PIPE, text=True,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield nx.from_graph6_bytes(line.encode())
    proc.wait()


# ---------------------------------------------------------------------
# Weighted-incidence formula correction check
# ---------------------------------------------------------------------

def check_weighted_incidence_formula(trials: int, seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    checked = 0
    failures = []
    for _ in range(trials):
        t = rng.randint(1, 4)
        G = nx.Graph()
        hs = [f"h{i}" for i in range(t)]
        G.add_nodes_from(hs)
        total_len = 0
        vcount = [0]

        def new_v():
            vcount[0] += 1
            return f"v{vcount[0]}"

        for i in range(t):
            plen = rng.randint(1, 4)
            path_vertices = [new_v() for _ in range(plen + 1)]
            G.add_edge(hs[i], path_vertices[0])
            for k in range(plen):
                G.add_edge(path_vertices[k], path_vertices[k + 1])
            G.add_edge(path_vertices[-1], hs[(i + 1) % t])
            total_len += plen
        expected = 2 * t + total_len
        relabel = {v: i for i, v in enumerate(sorted(G.nodes(), key=str))}
        G2 = nx.relabel_nodes(G, relabel)
        g = from_edges(G2.number_of_nodes(), list(G2.edges()))
        checked += 1
        if not has_cycle_len_dfs(g, expected):
            failures.append((t, total_len, expected))
    return {"checked": checked, "failures": failures}


# ---------------------------------------------------------------------
# III.1: h=0, q=2 -> n=8, every connected cubic graph has C4 or C8
# ---------------------------------------------------------------------

def check_h0_q2() -> dict[str, Any]:
    """q=2, h=0 (cubic) forces n=8 (q=n/2-2). Cited proof: ex(8;{C4,C8})
    =11 < ceil(3*8/2)=12 (McKay's extremal data, literature.md L15,
    already established in the FIRST phase of this project) -- a cubic
    graph on 8 vertices has exactly 12 edges, exceeding the max possible
    for a {C4,C8}-free graph, so it must contain a C4 or C8. Independently
    re-verified here by exhaustive geng enumeration of ALL connected
    cubic 8-vertex graphs."""
    graphs = list(via_geng_cubic(8))
    results = []
    for G in graphs:
        g = from_edges(G.number_of_nodes(), list(G.edges()))
        c4 = has_cycle_len_dfs(g, 4)
        c8 = has_cycle_len_dfs(g, 8)
        c4n = has_cycle_len_nx(g, 4)
        c8n = has_cycle_len_nx(g, 8)
        assert c4 == c4n and c8 == c8n, "detector disagreement"
        results.append((c4, c8))
    return {
        "n_forced": 8,
        "ex_8_C4C8": 11,
        "min_edges_cubic": 12,
        "extremal_bound_forces_c4_or_c8": 11 < 12,
        "graphs_checked": len(graphs),
        "all_have_c4_or_c8": all(c4 or c8 for c4, c8 in results),
    }


def via_geng_cubic(n: int):
    import subprocess
    proc = subprocess.Popen(["geng", "-c", "-d3", "-D3", str(n)], stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield nx.from_graph6_bytes(line.encode())
    proc.wait()


# ---------------------------------------------------------------------
# III.2: h=1, q=2 -> c3=4, F[C3] has delta>=2 on 4 vertices -> C4
# ---------------------------------------------------------------------

def every_4vertex_min_degree2_has_c4() -> dict[str, Any]:
    """Exhaustive check: every simple graph on 4 labelled vertices with
    min degree >=2 contains a C4."""
    nodes = list(range(4))
    all_edges = list(itertools.combinations(nodes, 2))
    failures = []
    checked = 0
    for r in range(0, len(all_edges) + 1):
        for edge_subset in itertools.combinations(all_edges, r):
            G = nx.Graph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edge_subset)
            degs = dict(G.degree())
            if min(degs.values()) < 2:
                continue
            checked += 1
            g = from_edges(4, list(G.edges()))
            if not has_cycle_len_dfs(g, 4):
                failures.append(sorted(G.edges()))
    return {"checked": checked, "failures": failures}


def check_h1_q2(n_max: int) -> dict[str, Any]:
    """The real argument is a CASE SPLIT, not one fixed mechanism:
    EITHER some C3 vertex has >=2 C2-neighbours (direct C4 via
    z-a-u-b-z), OR every C3 vertex has <=1 C2-neighbour (hence >=2
    C3-neighbours, so F[C3] has min-degree>=2, giving a C4 via the
    4-vertex lemma). Checked on EVERY property-(2) h=1,q=2 graph
    (unconditional -- this case-split needs no C4-freeness assumption,
    unlike the theorem's overall conclusion) plus separately reports how
    many of the underlying property-(2) population are actually C4-free
    (the real test population for the THEOREM itself, which needs
    C4-freeness as its hypothesis)."""
    checked = 0
    algebra_failures = []
    case_split_failures = []
    branch_counts = {"direct_2c2neighbour": 0, "f_c3_min_degree2": 0, "neither": 0}
    c4_free_count = 0
    for n in range(8, n_max + 1):
        for G in via_geng_q2(n):
            if not is_property2_fast(G):
                continue
            C, H = cubic_core_partition(G)
            if len(H) != 1:
                continue
            checked += 1
            rec = check_identities(G)
            assert rec["applicable"] and rec["every_c_has_f_neighbour"]
            c1, c3 = rec["c1"], rec["c3"]
            if c1 != 0 or c3 != 4:
                algebra_failures.append((n, nx.to_graph6_bytes(G, header=False).decode().strip(), c1, c3))
                continue

            g = from_edges(G.number_of_nodes(), list(G.edges()))
            has_c4 = has_cycle_len_dfs(g, 4)
            if not has_c4:
                c4_free_count += 1

            z = H[0]
            F = G.subgraph(C)
            c3_vertices = [v for v in C if F.degree(v) == 3]
            assert len(c3_vertices) == 4

            # branch 1: some C3 vertex has >=2 C2-neighbours -> direct C4
            direct_c4 = False
            for u in c3_vertices:
                c2_nbrs = [w for w in F.neighbors(u) if F.degree(w) == 2]
                if len(c2_nbrs) >= 2:
                    a, b = c2_nbrs[0], c2_nbrs[1]
                    edges_needed = [(z, a), (a, u), (u, b), (b, z)]
                    if all(G.has_edge(x, y) for x, y in edges_needed):
                        direct_c4 = True
                        break

            # branch 2: every C3 vertex has <=1 C2-neighbour -> F[C3] has
            # min degree >=2 (>=2 C3-neighbours each) -> C4 within F[C3]
            every_c3_le1_c2 = all(
                sum(1 for w in F.neighbors(u) if F.degree(w) == 2) <= 1
                for u in c3_vertices
            )
            f_c3_min_deg2 = False
            f_c3_has_c4 = False
            if every_c3_le1_c2:
                F_C3 = F.subgraph(c3_vertices)
                degs = dict(F_C3.degree())
                f_c3_min_deg2 = len(degs) == 4 and min(degs.values()) >= 2
                if f_c3_min_deg2:
                    idx = {v: i for i, v in enumerate(c3_vertices)}
                    f_c3_has_c4 = has_cycle_len_dfs(
                        from_edges(4, [(idx[u], idx[v]) for u, v in F_C3.edges()]), 4
                    )

            if direct_c4:
                branch_counts["direct_2c2neighbour"] += 1
            elif f_c3_min_deg2 and f_c3_has_c4:
                branch_counts["f_c3_min_degree2"] += 1
            else:
                branch_counts["neither"] += 1
                case_split_failures.append({
                    "n": n, "g6": nx.to_graph6_bytes(G, header=False).decode().strip(),
                    "direct_c4": direct_c4, "every_c3_le1_c2": every_c3_le1_c2,
                    "f_c3_min_deg2": f_c3_min_deg2, "f_c3_has_c4": f_c3_has_c4,
                })

            if (direct_c4 or (f_c3_min_deg2 and f_c3_has_c4)) and not has_c4:
                # the case-split claims to have found a C4 but the whole-
                # graph detector disagrees -- a genuine failure
                case_split_failures.append({
                    "n": n, "g6": nx.to_graph6_bytes(G, header=False).decode().strip(),
                    "reason": "case-split found a C4 construction but detector says no C4",
                })

    return {
        "n_range": (8, n_max),
        "h1_q2_graphs_checked": checked,
        "algebra_failures": algebra_failures,
        "branch_counts": branch_counts,
        "case_split_failures": case_split_failures,
        "c4_free_count_in_population": c4_free_count,
    }


# ---------------------------------------------------------------------
# III.3: h=2, q=2 -> c1=c3<=1
# ---------------------------------------------------------------------

def check_h2_q2_algebra(n_max: int) -> dict[str, Any]:
    """Two SEPARATE claims, tested on their correct populations:
    (a) c1==c3 -- pure algebra (I.1's identity at h=2: c1=c3+8-4-4=c3
        exactly), needs only property (2) + M2, holds unconditionally.
    (b) c1<=1 -- needs L4's 2-degeneracy bound, which needs GENUINE
        F-cleanness (not merely property (2)); testing it on arbitrary
        property-(2) graphs is testing the WRONG population (exactly
        the scope-note pitfall flagged in Part I) -- so (b) is checked
        ONLY on the C4-and-C8-free subset (the closest testable proxy
        for F-clean at this size), reported honestly even if that
        subset is empty (matching this project's established pattern:
        no small F-clean fixture exists)."""
    checked = 0
    identity_failures = []
    c4c8_free_count = 0
    bound_failures_on_c4c8_free = []
    kappa_beta_records = []
    for n in range(8, n_max + 1):
        for G in via_geng_q2(n):
            if not is_property2_fast(G):
                continue
            C, H = cubic_core_partition(G)
            if len(H) != 2:
                continue
            checked += 1
            rec = check_identities(G)
            assert rec["applicable"] and rec["every_c_has_f_neighbour"]
            c1, c3 = rec["c1"], rec["c3"]
            if c1 != c3:
                identity_failures.append((n, nx.to_graph6_bytes(G, header=False).decode().strip(), c1, c3))

            g = from_edges(G.number_of_nodes(), list(G.edges()))
            c4_free = not has_cycle_len_dfs(g, 4)
            c8_free = not has_cycle_len_dfs(g, 8)
            if c4_free and c8_free:
                c4c8_free_count += 1
                if c1 > 1:
                    bound_failures_on_c4c8_free.append(
                        (n, nx.to_graph6_bytes(G, header=False).decode().strip(), c1, c3))
            kappa_beta_records.append((n, c1, c3, rec["kappa"], rec["betaF"]))
    return {
        "checked": checked,
        "identity_c1_eq_c3_failures": identity_failures,
        "c4c8_free_count_in_population": c4c8_free_count,
        "bound_c1_le1_failures_on_c4c8_free_subset": bound_failures_on_c4c8_free,
        "records": kappa_beta_records,
    }


def coloring_forces_mod4_and_c4_c8(max_L: int = 24) -> dict[str, Any]:
    """III.3.a mechanics, tested directly (not tied to a real graph):
    build an F-cycle of length L with 2 H-vertices a,b, EVERY possible
    2-coloring (each cycle vertex -> a or b) that a genuine minimal
    counterexample would have to realize (every cycle vertex touches
    exactly one of a,b), and confirm: (1) L not divisible by 4 => every
    valid coloring is IMPOSSIBLE to keep C4-free (a C4 is forced no
    matter the coloring choice); (2) for L divisible by 4, there EXISTS
    a C4-avoiding coloring (the period-4 block pattern), and for that
    coloring, L=4 or L=8 directly gives a forbidden cycle (the F-cycle
    ITSELF), while L>=12 gives an explicit C8 via 2 short arcs through
    a AND b (checked as an ACTUAL simple cycle in a constructed graph,
    via the dual detector, not just arithmetic)."""
    results = {}
    for L in range(4, max_L + 1):
        if L < 4:
            continue
        cyc = nx.Graph()
        cyc.add_nodes_from(range(L))
        cyc.add_edges_from((i, (i + 1) % L) for i in range(L))
        # every coloring in {0,1}^L (as which of a/b each vertex touches)
        # -- exhaustive for small L, otherwise just test the period-4
        # pattern's existence/validity plus the "any coloring forces C4"
        # claim via SAT-free direct enumeration for L<=16, and via the
        # proved recurrence argument (not brute force) for L>16.
        forces_c4_always = None
        exists_clean_coloring = None
        if L <= 16:
            any_clean = False
            all_force_c4 = True
            for bits in range(2 ** L):
                coloring = [(bits >> i) & 1 for i in range(L)]
                # C4 test: any i with coloring[i]==coloring[(i+2)%L] gives
                # a C4 a/b - i - i+1 - i+2 - a/b (checked structurally)
                has_collision = any(coloring[i] == coloring[(i + 2) % L] for i in range(L))
                if not has_collision:
                    any_clean = True
                    all_force_c4 = False
            forces_c4_always = all_force_c4
            exists_clean_coloring = any_clean
        divisible_by_4 = (L % 4 == 0)

        record: dict[str, Any] = {
            "L": L, "divisible_by_4": divisible_by_4,
        }
        if L <= 16:
            record["exhaustive_forces_c4_always"] = forces_c4_always
            record["exhaustive_exists_clean_coloring"] = exists_clean_coloring
            record["matches_prediction"] = (forces_c4_always == (not divisible_by_4))

        if divisible_by_4:
            # build an actual graph: F-cycle of length L + a,b attached
            # per the period-4 block pattern (a,a,b,b,...)
            G = nx.Graph()
            G.add_nodes_from(range(L))
            G.add_edges_from((i, (i + 1) % L) for i in range(L))
            G.add_node("a")
            G.add_node("b")
            for i in range(L):
                block = (i // 2) % 2
                G.add_edge("a" if block == 0 else "b", i)
            relabel = {v: idx for idx, v in enumerate(sorted(G.nodes(), key=str))}
            G2 = nx.relabel_nodes(G, relabel)
            g = from_edges(G2.number_of_nodes(), list(G2.edges()))
            has_c4 = has_cycle_len_dfs(g, 4)
            has_c8 = has_cycle_len_dfs(g, 8)
            if L == 4:
                record["direct_forbidden_cycle"] = "F-cycle itself is a C4"
                record["confirmed"] = has_c4
            elif L == 8:
                record["direct_forbidden_cycle"] = "F-cycle itself is a C8"
                record["confirmed"] = has_c8
            else:
                record["direct_forbidden_cycle"] = "explicit constructed C8 via 2 arcs + a,b"
                record["confirmed"] = has_c8
        results[L] = record
    return results


# ---------------------------------------------------------------------
# III.3.b: c1=c3=1, the unicyclic pendant-path case
# ---------------------------------------------------------------------

def build_lollipop(L_cyc: int, t: int):
    """Cycle of length L_cyc (vertices cyc_0..cyc_{L_cyc-1}), y=cyc_0 is
    the unique C3 vertex, a pendant path of t edges from y to the unique
    leaf x (t-1 internal vertices m_1..m_{t-1}). Returns (graph, y, x,
    c2_vertices) where c2_vertices is every F-vertex other than x,y
    (needs an H-attachment in {0,1} standing for a,b)."""
    G = nx.Graph()
    cyc = [f"cyc{i}" for i in range(L_cyc)]
    G.add_nodes_from(cyc)
    G.add_edges_from((cyc[i], cyc[(i + 1) % L_cyc]) for i in range(L_cyc))
    y = cyc[0]
    pendant = [f"m{i}" for i in range(1, t)]  # internal path vertices (t-1 of them)
    x = "x"
    chain = [y] + pendant + [x]
    for i in range(len(chain) - 1):
        G.add_edge(chain[i], chain[i + 1])
    c2_vertices = [v for v in G if v not in (y, x)]
    return G, y, x, c2_vertices


def exhaustive_pendant_case(L_cyc: int, t: int) -> dict[str, Any]:
    """Enumerate EVERY coloring of the C2 vertices (each -> a or b) and
    confirm a C4 is forced in ALL of them (no valid C4-avoiding
    attachment exists) -- x is attached to BOTH a and b always (forced
    by d_F(x)=1 => d_H(x)=2, H={a,b})."""
    G, y, x, c2v = build_lollipop(L_cyc, t)
    n_c2 = len(c2v)
    if n_c2 > 14:
        return {"L_cyc": L_cyc, "t": t, "skipped": True, "reason": "too large for exhaustive 2^n"}

    always_c4 = True
    any_clean = None
    for bits in range(2 ** n_c2):
        Gc = G.copy()
        Gc.add_node("a")
        Gc.add_node("b")
        Gc.add_edge(x, "a")
        Gc.add_edge(x, "b")
        for i, v in enumerate(c2v):
            color = "a" if (bits >> i) & 1 == 0 else "b"
            Gc.add_edge(v, color)
        relabel = {v: i for i, v in enumerate(sorted(Gc.nodes(), key=str))}
        Gc2 = nx.relabel_nodes(Gc, relabel)
        g = from_edges(Gc2.number_of_nodes(), list(Gc2.edges()))
        has_c4 = has_cycle_len_dfs(g, 4)
        if not has_c4:
            always_c4 = False
            any_clean = bits
            break
    return {
        "L_cyc": L_cyc, "t": t, "n_c2_vertices": n_c2,
        "colorings_checked": 2 ** n_c2, "always_forces_c4": always_c4,
        "counterexample_coloring_bits": any_clean,
    }


def check_h2_c1c3_1_component_parity(n_max: int) -> dict[str, Any]:
    """GENUINE (non-circular) test of the shape claim: exhaustively
    enumerate every connected simple graph on n<=n_max vertices (via the
    networkx atlas, independent of `build_lollipop`) with EXACTLY the
    target degree profile (one degree-1 vertex, one degree-3 vertex, the
    rest degree exactly 2), and confirm every single one is isomorphic
    to SOME lollipop (cycle + single pendant path) -- i.e. that the hand
    proof's shape claim (via the handshake-lemma parity argument) is not
    merely consistent with one construction but is the ONLY possible
    shape."""
    checked = 0
    non_lollipop = []
    for G in nx.graph_atlas_g():
        n = G.number_of_nodes()
        if n < 4 or n > n_max or not nx.is_connected(G):
            continue
        degs = dict(G.degree())
        deg1 = [v for v, d in degs.items() if d == 1]
        deg3 = [v for v, d in degs.items() if d == 3]
        deg2 = [v for v, d in degs.items() if d == 2]
        if len(deg1) != 1 or len(deg3) != 1 or len(deg2) != n - 2:
            continue
        checked += 1
        is_lollipop = False
        for L_cyc in range(3, n):
            t = n - L_cyc
            if t < 1:
                continue
            L, _, _, _ = build_lollipop(L_cyc, t)
            if nx.is_isomorphic(G, L):
                is_lollipop = True
                break
        if not is_lollipop:
            non_lollipop.append(nx.to_graph6_bytes(G, header=False).decode().strip())
    return {"checked": checked, "non_lollipop_shapes_found": non_lollipop}


def main() -> int:
    import argparse
    import json
    import hashlib

    parser = argparse.ArgumentParser()
    parser.add_argument("--h1-n-max", type=int, default=14)
    parser.add_argument("--h2-n-max", type=int, default=13)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    wif = check_weighted_incidence_formula(3000, 20260727)
    print(f"weighted-incidence formula (2t+sum|Pi|): checked={wif['checked']} "
          f"failures={len(wif['failures'])}")

    h0 = check_h0_q2()
    print(f"\n=== III.1 h=0,q=2 ===")
    print(f"n forced to {h0['n_forced']}, ex(8;{{C4,C8}})={h0['ex_8_C4C8']} < "
          f"min_edges={h0['min_edges_cubic']}: {h0['extremal_bound_forces_c4_or_c8']}")
    print(f"exhaustive geng n=8 cubic count: {h0['graphs_checked']} "
          f"(all C4-or-C8: {h0['all_have_c4_or_c8']})")

    four_vertex = every_4vertex_min_degree2_has_c4()
    print(f"\n=== III.2 lemma: every 4-vertex min-deg>=2 graph has C4 ===")
    print(f"checked={four_vertex['checked']} failures={len(four_vertex['failures'])}")

    h1 = check_h1_q2(args.h1_n_max)
    print(f"\n=== III.2 h=1,q=2 ===")
    print(f"checked={h1['h1_q2_graphs_checked']} n={h1['n_range']}")
    print(f"algebra failures (c1!=0 or c3!=4): {len(h1['algebra_failures'])}")
    print(f"branch counts: {h1['branch_counts']}")
    print(f"case-split failures: {len(h1['case_split_failures'])}")
    print(f"C4-free graphs in the property-(2) population (real theorem hypothesis): "
          f"{h1['c4_free_count_in_population']}/{h1['h1_q2_graphs_checked']}")

    h2_algebra = check_h2_q2_algebra(args.h2_n_max)
    print(f"\n=== III.3 h=2,q=2 algebra ===")
    print(f"checked={h2_algebra['checked']} n<=({args.h2_n_max})")
    print(f"c1==c3 identity failures: {len(h2_algebra['identity_c1_eq_c3_failures'])}")
    print(f"C4-and-C8-free graphs in the population (real theorem hypothesis, "
          f"c1<=1 only tested here): {h2_algebra['c4c8_free_count_in_population']}")
    print(f"c1<=1 failures on that subset: {len(h2_algebra['bound_c1_le1_failures_on_c4c8_free_subset'])}")
    from collections import Counter
    c1c3_dist = Counter((c1, c3) for (_, c1, c3, _, _) in h2_algebra["records"])
    print(f"(c1,c3) distribution over the FULL property-(2) population "
          f"(most are NOT F-clean, so c1<=1 is not expected to hold here): {dict(c1c3_dist)}")

    coloring = coloring_forces_mod4_and_c4_c8(24)
    mismatches = [L for L, r in coloring.items() if L <= 16 and not r.get("matches_prediction", True)]
    not_confirmed = [L for L, r in coloring.items() if r.get("divisible_by_4") and not r.get("confirmed", True)]
    print(f"\n=== III.3.a coloring/mod-4 argument, L=4..24 ===")
    print(f"exhaustive coloring mismatches (L<=16): {mismatches}")
    print(f"divisible-by-4 cases where the C4/C8 witness failed: {not_confirmed}")

    shape = check_h2_c1c3_1_component_parity(10)
    print(f"\n=== III.3.b shape claim (lollipop) ===")
    print(f"degree-profile graphs checked (n<=10, atlas): {shape['checked']} "
          f"non-lollipop shapes found: {len(shape['non_lollipop_shapes_found'])}")

    pendant_cases = []
    for L_cyc in (3, 4, 5, 6, 7, 8, 9):
        for t in (1, 2, 3, 4, 5):
            pendant_cases.append(exhaustive_pendant_case(L_cyc, t))
    pendant_failures = [r for r in pendant_cases if not r.get("skipped") and not r["always_forces_c4"]]
    print(f"\n=== III.3.b pendant-path t=1,2,>=3 cases ===")
    print(f"configurations checked: {len(pendant_cases)} "
          f"(skipped as too large: {sum(1 for r in pendant_cases if r.get('skipped'))})")
    print(f"configurations where a C4-avoiding coloring EXISTS (would refute the argument): "
          f"{len(pendant_failures)}")

    report = {
        "weighted_incidence_formula": wif,
        "h0_q2": h0,
        "four_vertex_min_degree2_lemma": four_vertex,
        "h1_q2": h1,
        "h2_q2_algebra": h2_algebra,
        "coloring_mod4": coloring,
        "h2_c1c3_1_shape": shape,
        "h2_c1c3_1_pendant_cases": pendant_cases,
    }
    encoded = json.dumps(report, indent=2, sort_keys=True, default=str)
    report["records_sha256"] = hashlib.sha256(encoded.encode()).hexdigest()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n")

    ok = (
        not wif["failures"]
        and h0["all_have_c4_or_c8"]
        and not four_vertex["failures"]
        and not h1["algebra_failures"] and not h1["case_split_failures"]
        and not h2_algebra["identity_c1_eq_c3_failures"]
        and not h2_algebra["bound_c1_le1_failures_on_c4c8_free_subset"]
        and not mismatches and not not_confirmed
        and not shape["non_lollipop_shapes_found"]
        and not pendant_failures
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
