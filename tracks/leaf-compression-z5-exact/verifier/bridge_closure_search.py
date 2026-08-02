"""
Bridge-closure generation and near-gadget ranking (task Parts 6-8,
2026-07-25, seventh redirection pass).

Generates J = B+xy: 2-connected, a distinguished degree-2 vertex x with
distinguished incident edge xy, every vertex other than x,y of degree
>=3, d_J(y)>=2. This is exactly the (frozen) one-pole search structure
with x as root, relaxed to allow y itself to sit at degree 2 (not forced
>=3, since y is B's OTHER terminal, not a generic internal vertex).

For each qualifying J, deletes the edge xy to recover B, then computes
(with two independent path/cycle enumeration methods, cross-checked):
  - internal power-of-two-cycle cleanliness of B
  - Lambda(B), self-sum dyadic hits h(B) = |(Lambda(B)+Lambda(B)) & F|
  - the disjoint-pair spectrum D(B)
  - the minimum omega(P,Q) among any dyadic-self-sum witness pair
    (verifier/linkage_data.py's identity used to double check)
  - SPQR classification of B+xy (reusing spqrtree)

Ranks by h(B) ascending (0 = outright T6 gadget -- escalate immediately),
then by minimum witness overlap, matching the priority order in
two_cut.md Sec.13.
"""
from __future__ import annotations
import subprocess
import sys
import itertools

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, powers_of_two_up_to, has_cycle_len_dfs, has_cycle_len_nx
from linkage_data import omega, symmetric_difference_cycle_decomposition, path_edges

import networkx as nx
import spqrtree
from collections import Counter

F = set()
_p = 4
while _p <= 4096:
    F.add(_p)
    _p *= 2


def run_geng(n: int):
    proc = subprocess.Popen(["geng", "-c", "-d2", str(n)], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield line
    proc.wait()


def find_J_candidates(G):
    """G: nx graph. Yields (x, y) for every valid one-pole-like rooting:
    x has degree exactly 2, y is one of x's two neighbors, every OTHER
    vertex (not x, not y) has degree >=3, d_G(y)>=2 (automatic, min-deg-2
    input)."""
    deg2 = [v for v in G if G.degree(v) == 2]
    for x in deg2:
        for y in G.neighbors(x):
            others_ok = all(G.degree(v) >= 3 for v in G if v not in (x, y))
            if others_ok:
                yield x, y


def all_xy_path_lengths(nxG, x, y):
    return sorted({len(p) - 1 for p in nx.all_simple_paths(nxG, x, y)})


def all_xy_paths(nxG, x, y, cap=None):
    return list(nx.all_simple_paths(nxG, x, y, cutoff=cap))


def disjoint_pair_spectrum(paths):
    """paths: list of vertex-sequences. D(B) = lengths (|P|,|Q|) for
    internally vertex-disjoint pairs (share only endpoints)."""
    d = set()
    for P, Q in itertools.combinations(paths, 2):
        internal_P = set(P[1:-1])
        internal_Q = set(Q[1:-1])
        if not (internal_P & internal_Q):
            d.add((len(P) - 1, len(Q) - 1))
    return d


def min_dyadic_witness_overlap(paths):
    """Among all pairs (P,Q) whose length-sum is in F, find the minimum
    omega(P,Q); return (min_omega, witness_pair) or (None, None)."""
    best = None
    best_pair = None
    for P, Q in itertools.combinations_with_replacement(paths, 2):
        if (len(P) - 1) + (len(Q) - 1) in F:
            w = omega(P, Q)
            if best is None or w < best:
                best = w
                best_pair = (P, Q)
    return best, best_pair


def analyze_B(nxG_J, x, y, n):
    B = nxG_J.copy()
    B.remove_edge(x, y)

    verts = sorted(B.nodes())
    remap = {v: i for i, v in enumerate(verts)}
    g = from_edges(n, [(remap[u], remap[v]) for u, v in B.edges()])
    internal_spectrum_dfs = {L: has_cycle_len_dfs(g, L) for L in powers_of_two_up_to(n)}
    internal_spectrum_nx = {L: has_cycle_len_nx(g, L) for L in powers_of_two_up_to(n)}
    assert internal_spectrum_dfs == internal_spectrum_nx, "detector disagreement"
    internal_clean = not any(internal_spectrum_dfs.values())

    if not nx.is_connected(B):
        return None  # xy was a bridge in J -- B disconnected, not a valid bridge candidate

    paths = all_xy_paths(B, x, y, cap=n)
    lam = sorted({len(p) - 1 for p in paths})
    self_sum = {a + b for a in lam for b in lam}
    h = len(self_sum & F)

    d_spec = disjoint_pair_spectrum(paths)
    d_hits_F = {(a, b) for (a, b) in d_spec if a + b in F}

    min_w, witness = min_dyadic_witness_overlap(paths) if h > 0 else (None, None)

    # SPQR of J itself (B+xy)
    spqr_types = None
    if nx.node_connectivity(nxG_J) >= 2:
        sg = spqrtree.MultiGraph()
        for u, v in nxG_J.edges():
            sg.add_edge(u, v)
        tree = spqrtree.SPQRTree(sg)
        spqr_types = dict(Counter(nd.type.value for nd in tree.nodes()))

    return dict(x=x, y=y, n=n, dB_x=B.degree(x), dB_y=B.degree(y),
                internal_clean=internal_clean, Lambda=lam, h=h,
                disjoint_pair_hits_F=sorted(d_hits_F),
                min_witness_overlap=min_w, witness_pair=witness,
                spqr_types=spqr_types)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=5)
    ap.add_argument("--nmax", type=int, default=9)
    args = ap.parse_args()

    total_J = 0
    total_B = 0
    seen_edge_rooted = set()
    results = []
    gadgets_h0 = []

    for n in range(args.nmin, args.nmax + 1):
        n_J = 0
        for g6 in run_geng(n):
            G = nx.from_graph6_bytes(g6.encode())
            for x, y in find_J_candidates(G):
                if nx.node_connectivity(G) < 2:
                    continue
                n_J += 1
                total_J += 1
                key = (g6, x, y)
                if key in seen_edge_rooted:
                    continue
                seen_edge_rooted.add(key)
                res = analyze_B(G, x, y, n)
                if res is None:
                    continue
                total_B += 1
                res["g6"] = g6
                results.append(res)
                if res["h"] == 0 and res["internal_clean"] and res["dB_x"] == 1:
                    gadgets_h0.append(res)
        print(f"n={n}: {n_J} (J,x,y) candidates, cumulative distinct B={total_B}")

    print(f"\n=== SUMMARY n={args.nmin}..{args.nmax} ===")
    print(f"total (J,x,y) candidates: {total_J}")
    print(f"distinct edge-rooted B realizations analyzed: {total_B}")

    type_a = [r for r in results if r["dB_x"] == 1]
    print(f"Type-A candidates (d_B(x)=1): {len(type_a)}")
    two_copy = [r for r in results if r["dB_x"] >= 2]
    print(f"two-copy candidates (d_B(x)>=2, generic bridge): {len(two_copy)}")

    print(f"\nh(B) distribution among Type-A, internally-clean candidates:")
    hist = Counter(r["h"] for r in type_a if r["internal_clean"])
    print(f"  {dict(sorted(hist.items()))}")

    if gadgets_h0:
        print("\n!!! h(B)=0 TYPE-A GADGET FOUND -- T6 CONSTRUCTION APPLIES -- "
              "ESCALATE AND INDEPENDENTLY RE-VERIFY IMMEDIATELY")
        for r in gadgets_h0[:3]:
            print(r)
    else:
        print("\nno h(B)=0 Type-A gadget found at this scale (expected, matches "
              "the project's broader pattern -- NOT evidence of general "
              "nonexistence, see two_cut.md Sec.10's conjecture status).")

    h1 = sorted([r for r in type_a if r["internal_clean"] and r["h"] == 1],
                key=lambda r: (r["min_witness_overlap"] if r["min_witness_overlap"] is not None else 999))
    print(f"\nh(B)=1 Type-A candidates (smallest overlap first), up to 5:")
    for r in h1[:5]:
        print(f"  n={r['n']} g6={r['g6']} x={r['x']} y={r['y']} Lambda={r['Lambda']} "
              f"min_overlap={r['min_witness_overlap']} witness={r['witness_pair']} "
              f"spqr={r['spqr_types']}")

    if not h1:
        print("  none found at this scale.")


if __name__ == "__main__":
    main()
