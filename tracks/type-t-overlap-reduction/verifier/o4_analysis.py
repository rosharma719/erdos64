"""
O4 / O4a / terminal-spectrum analysis (Erdos #64, task Part 4, 2026-07-25).

For every one-pole candidate (root r degree 2, else delta>=3, connected --
NOT required to be F-clean, that is the "relaxed" population), this script:
  1. checks whether K=H-r has 2 internally-disjoint a-b paths (a,b = r's
     neighbors) via networkx local_node_connectivity;
  2. if not, finds a minimum a-b vertex separator x (O4a);
  3. computes the two O4a lobes D1 (containing a), D2 (containing b) of
     H-{r,x}, and the two-terminal lobes L1=H[D1+{r,x}], L2=H[D2+{r,x}];
  4. computes the terminal path spectra Lambda_1, Lambda_2 (all simple r-x
     path lengths within L1, L2) by explicit enumeration (feasible only
     for small graphs -- this is exhaustive small-n data, not a bound);
  5. checks (Lambda_1+Lambda_2) and (Lambda_i+Lambda_i) against the
     forbidden dyadic set;
  6. separately, enumerates ALL simple a-b paths in K (not just the O4a
     lobes) and looks for admissible pairs (lengths differing by 1 or 2),
     to test O4' directly on data, independent of the O4a failure case.

Both the "actual" (F-clean) and "relaxed" (any cycles allowed) populations
are supported -- the relaxed run is what tells us whether the 2-disjoint-
paths property (O4) follows from degree+connectivity alone or genuinely
needs F-cleanness/minimality (it does NOT need F-cleanness for the
existence of 2 disjoint paths question itself, since that's a pure
connectivity fact about K -- but F-cleanness matters for interpreting the
Lambda-sumset F-avoidance conditions).
"""
from __future__ import annotations
import subprocess
import sys
import itertools
from collections import Counter

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, powers_of_two_up_to, has_cycle_len_dfs, Graph


def read_graph6_line(line: str):
    import networkx as nx
    return nx.from_graph6_bytes(line.strip().encode())


def is_one_pole_nx(G) -> tuple[bool, int | None]:
    deg2 = [v for v in G if G.degree(v) == 2]
    if len(deg2) != 1:
        return False, None
    r = deg2[0]
    if all(G.degree(v) >= 3 for v in G if v != r):
        return True, r
    return False, None


def run_geng(n: int):
    cmd = ["geng", "-c", "-d2", str(n)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield line
    proc.wait()


def all_simple_path_lengths(G, s, t, cutoff=None):
    import networkx as nx
    return [len(p) - 1 for p in nx.all_simple_paths(G, s, t, cutoff=cutoff)]


def analyze_candidate(G, r, n_cap_for_paths=16):
    """Full O4/O4a/spectrum analysis for one one-pole candidate (G, r)."""
    import networkx as nx
    nbrs = list(G.neighbors(r))
    assert len(nbrs) == 2
    a, b = nbrs
    K = G.copy()
    K.remove_node(r)

    conn = nx.node_connectivity(K, a, b)  # exact local vertex connectivity a-b
    result = dict(n=G.number_of_nodes(), r=r, a=a, b=b, local_conn=conn)

    if conn >= 2:
        result["o4_holds_directly"] = True
        return result
    result["o4_holds_directly"] = False

    cut = nx.minimum_node_cut(K, a, b)
    result["separator"] = sorted(cut)
    if len(cut) != 1:
        result["note"] = f"separator size {len(cut)} != 1 (unexpected for conn={conn})"
        return result
    x = next(iter(cut))
    result["x"] = x

    Hminus = G.copy()
    Hminus.remove_nodes_from([r, x])
    comps = list(nx.connected_components(Hminus))
    d1 = next(c for c in comps if a in c)
    d2 = next(c for c in comps if b in c)
    result["num_components_H_minus_rx"] = len(comps)
    result["d1_size"] = len(d1)
    result["d2_size"] = len(d2)

    L1 = G.subgraph(set(d1) | {r, x}).copy()
    L2 = G.subgraph(set(d2) | {r, x}).copy()
    result["deg_L1_x"] = L1.degree(x)
    result["deg_L2_x"] = L2.degree(x)

    if G.number_of_nodes() <= n_cap_for_paths:
        lam1 = sorted(set(all_simple_path_lengths(L1, r, x)))
        lam2 = sorted(set(all_simple_path_lengths(L2, r, x)))
    else:
        lam1, lam2 = None, None
    result["lambda1"] = lam1
    result["lambda2"] = lam2

    if lam1 is not None and lam2 is not None:
        cross_sum = sorted({l1 + l2 for l1 in lam1 for l2 in lam2})
        self_sum1 = sorted({l1 + l1b for l1 in lam1 for l1b in lam1})
        self_sum2 = sorted({l2 + l2b for l2 in lam2 for l2b in lam2})
        forb = set(powers_of_two_up_to(2 * G.number_of_nodes()))
        result["cross_sum"] = cross_sum
        result["cross_sum_hits_dyadic"] = sorted(set(cross_sum) & forb)
        result["self_sum1_hits_dyadic"] = sorted(set(self_sum1) & forb)
        result["self_sum2_hits_dyadic"] = sorted(set(self_sum2) & forb)
        result["valid_one_pole_if_double_L1"] = (
            L1.degree(x) >= 2 and not result["self_sum1_hits_dyadic"])
        result["valid_one_pole_if_double_L2"] = (
            L2.degree(x) >= 2 and not result["self_sum2_hits_dyadic"])

    return result


def find_admissible_pairs(G, r, cutoff=None):
    """All simple a-b path lengths in K=H-r, and admissible (diff 1 or 2) pairs."""
    import networkx as nx
    nbrs = list(G.neighbors(r))
    a, b = nbrs
    K = G.copy()
    K.remove_node(r)
    lengths = sorted(set(all_simple_path_lengths(K, a, b, cutoff=cutoff)))
    pairs = [(l1, l2) for l1, l2 in itertools.combinations(lengths, 2) if abs(l1 - l2) in (1, 2)]
    return lengths, pairs


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=5)
    ap.add_argument("--nmax", type=int, default=12)
    ap.add_argument("--require-f-clean", action="store_true",
                     help="only analyze candidates with no power-of-two cycle "
                          "(the 'actual' population, vs default 'relaxed')")
    ap.add_argument("--path-cap", type=int, default=13,
                     help="max n for which full path enumeration is attempted")
    args = ap.parse_args()

    total = 0
    o4_direct = 0
    o4_fails = 0
    spectra_examples = []
    failure_examples = []

    for n in range(args.nmin, args.nmax + 1):
        n_this = 0
        for g6 in run_geng(n):
            G = read_graph6_line(g6)
            ok, r = is_one_pole_nx(G)
            if not ok:
                continue
            if args.require_f_clean:
                g = from_edges(n, list(G.edges()))
                if any(has_cycle_len_dfs(g, L) for L in powers_of_two_up_to(n)):
                    continue
            n_this += 1
            total += 1
            res = analyze_candidate(G, r, n_cap_for_paths=args.path_cap)
            if res.get("o4_holds_directly"):
                o4_direct += 1
            else:
                o4_fails += 1
                if len(failure_examples) < 15:
                    failure_examples.append((n, g6, res))
            if res.get("lambda1") is not None and len(spectra_examples) < 12:
                spectra_examples.append((n, g6, res))
        print(f"n={n}: {n_this} one-pole candidates analyzed "
              f"({'F-clean only' if args.require_f_clean else 'relaxed'})")

    print(f"\n=== SUMMARY n={args.nmin}..{args.nmax} "
          f"({'F-clean' if args.require_f_clean else 'relaxed'}) ===")
    print(f"total candidates: {total}")
    print(f"O4 holds directly (2 disjoint a-b paths): {o4_direct} "
          f"({100*o4_direct/total:.1f}%)" if total else "")
    print(f"O4 fails (needs O4a structure): {o4_fails} "
          f"({100*o4_fails/total:.1f}%)" if total else "")

    print(f"\n--- {len(failure_examples)} smallest O4-failure examples ---")
    for n, g6, res in sorted(failure_examples, key=lambda t: t[0])[:10]:
        print(f"n={n} g6={g6} x={res.get('x')} "
              f"d1={res.get('d1_size')} d2={res.get('d2_size')} "
              f"deg_L1(x)={res.get('deg_L1_x')} deg_L2(x)={res.get('deg_L2_x')}")

    print(f"\n--- up to 12 representative terminal spectra ---")
    for n, g6, res in spectra_examples:
        print(f"n={n} g6={g6}")
        print(f"  Lambda1={res['lambda1']}  Lambda2={res['lambda2']}")
        print(f"  cross_sum hits dyadic: {res['cross_sum_hits_dyadic']}  "
              f"self1 hits dyadic: {res['self_sum1_hits_dyadic']}  "
              f"self2 hits dyadic: {res['self_sum2_hits_dyadic']}")
        print(f"  valid one-pole if double L1: {res['valid_one_pole_if_double_L1']}  "
              f"if double L2: {res['valid_one_pole_if_double_L2']}")


if __name__ == "__main__":
    main()
