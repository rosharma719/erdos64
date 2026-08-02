"""
One-R-node target search (task Part 7, 2026-07-25, fourth redirection pass).

Searches the RELAXED one-pole population (root r degree 2, else delta>=3,
connected -- cycles of any length allowed, not required F-clean) for
candidates whose reduced SPQR tree of K+ab (K=H-r, ab closed per O4')
contains >=2 R-nodes. For every such candidate, for every LEAF R-node,
checks:
  - terminal degree >=2 at both poles (should hold automatically, R-nodes
    are 3-connected -- verified, not just asserted)
  - internal min degree >=3 (same)
  - whether H_{P_R} (attach a fresh root to both poles) is lexicographically
    smaller than H -- O6's actual hypothesis
  - whether the poles have a common neighbor OUTSIDE the leaf's own
    territory -- O7's condition, checked directly on the concrete graph
    (not assumed)

This does NOT yet search for genuine F-clean multi-R survivors (none are
known -- that is exactly what would disprove Erdos-Gyarfas). It tests
whether examples satisfying O6's structural PREREQUISITES (degree
conditions) but failing O7 (i.e. HAVING an external common neighbor) are
common in the relaxed population -- if so, that is exactly the kind of
"additional condition" (namely O7's own conclusion, which uses F-cleanness
of H to derive a contradiction) that would need to distinguish genuine
one-pole survivors from generic multi-R-node graphs.
"""
from __future__ import annotations
import subprocess
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, powers_of_two_up_to, has_cycle_len_dfs

import networkx as nx
import spqrtree


def run_geng(n: int):
    proc = subprocess.Popen(["geng", "-c", "-d2", str(n)], stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        line = line.strip()
        if line:
            yield line
    proc.wait()


def is_one_pole(G):
    deg2 = [v for v in G if G.degree(v) == 2]
    if len(deg2) != 1:
        return False, None
    r = deg2[0]
    if all(G.degree(v) >= 3 for v in G if v != r):
        return True, r
    return False, None


def build_Ke(G, r):
    a, b = list(G.neighbors(r))
    K = G.copy()
    K.remove_node(r)
    had_ab = K.has_edge(a, b)
    if not had_ab:
        K.add_edge(a, b)
    return K, a, b, had_ab


def spqr_tree_of(K):
    if nx.node_connectivity(K) < 2:
        return None
    sg = spqrtree.MultiGraph()
    for u, v in K.edges():
        sg.add_edge(u, v)
    return spqrtree.SPQRTree(sg)


def is_f_clean(G, n):
    g = from_edges(n, list(G.edges()))
    return not any(has_cycle_len_dfs(g, L) for L in powers_of_two_up_to(n))


def check_leaf_r_node(G, H_n, node, all_nodes):
    """node: an SPQRNode of type R with exactly one virtual edge (leaf).
    Returns dict of diagnostics, or None if not actually a leaf."""
    virtual_edges = [e for e in node.skeleton.edges if e.virtual]
    real_edges = [e for e in node.skeleton.edges if not e.virtual]
    if len(virtual_edges) != 1:
        return None  # not a leaf
    x, y = virtual_edges[0].u, virtual_edges[0].v

    # pertinent graph P_R: real edges of this node's skeleton only, as an
    # actual subgraph of G restricted to the real vertices touched here.
    P_vertices = set()
    for e in real_edges:
        P_vertices.add(e.u)
        P_vertices.add(e.v)
    P_R = G.subgraph(P_vertices).copy()
    # remove any edge that isn't actually a real skeleton edge of this node
    # (subgraph() would include extra edges among these vertices if the
    # original graph has them but the node's skeleton doesn't list them --
    # for a true leaf R-node's pertinent graph this shouldn't happen, but
    # check explicitly rather than assume)
    skeleton_real_pairs = {frozenset((e.u, e.v)) for e in real_edges}
    extra = [frozenset(e) for e in P_R.edges() if frozenset(e) not in skeleton_real_pairs]

    tdeg_x = P_R.degree(x) if x in P_R else 0
    tdeg_y = P_R.degree(y) if y in P_R else 0
    internal_min_deg = min((P_R.degree(v) for v in P_R if v not in (x, y)), default=None)

    order_HP = P_R.number_of_nodes() + 1
    edges_HP = P_R.number_of_edges() + 2
    lex_smaller = (order_HP, edges_HP) < (H_n, G.number_of_edges())

    # O7 check: common neighbor of x,y outside P_R's vertex set
    common = (set(G.neighbors(x)) & set(G.neighbors(y))) - P_vertices
    o7_holds = len(common) == 0

    return dict(x=x, y=y, P_R_order=P_R.number_of_nodes(), P_R_edges=P_R.number_of_edges(),
                extra_edges_flag=len(extra) > 0, tdeg_x=tdeg_x, tdeg_y=tdeg_y,
                internal_min_deg=internal_min_deg, order_HP=order_HP, edges_HP=edges_HP,
                lex_smaller_than_H=lex_smaller, external_common_neighbors=sorted(common),
                o7_holds=o7_holds)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=5)
    ap.add_argument("--nmax", type=int, default=10)
    args = ap.parse_args()

    total_one_pole = 0
    multi_r_examples = []
    r_count_hist = Counter()

    for n in range(args.nmin, args.nmax + 1):
        n_this = 0
        for g6 in run_geng(n):
            G = nx.from_graph6_bytes(g6.encode())
            ok, r = is_one_pole(G)
            if not ok:
                continue
            n_this += 1
            total_one_pole += 1
            K, a, b, had_ab = build_Ke(G, r)
            tree = spqr_tree_of(K)
            if tree is None:
                r_count_hist["K+ab not 2-connected"] += 1
                continue
            nodes = tree.nodes()
            r_nodes = [nd for nd in nodes if nd.type.value == "R"]
            r_count_hist[len(r_nodes)] += 1
            if len(r_nodes) >= 2:
                fclean = is_f_clean(G, n)
                leaf_diagnostics = []
                for rn in r_nodes:
                    d = check_leaf_r_node(G, n, rn, nodes)
                    if d is not None:
                        leaf_diagnostics.append(d)
                multi_r_examples.append((n, g6, r, len(r_nodes), fclean, leaf_diagnostics))
        print(f"n={n}: {n_this} one-pole candidates, "
              f"R-node-count histogram so far: {dict(r_count_hist)}")

    print(f"\n=== SUMMARY n={args.nmin}..{args.nmax} ===")
    print(f"total one-pole candidates: {total_one_pole}")
    print(f"R-node count distribution: {dict(r_count_hist)}")
    print(f"candidates with >=2 R-nodes: {len(multi_r_examples)}")

    fully_satisfying = 0
    any_o7_failure = 0
    for n, g6, r, nr, fclean, diags in multi_r_examples:
        has_full_pass = any(d["lex_smaller_than_H"] and d["o7_holds"] for d in diags)
        has_o7_fail_with_lex_smaller = any(
            d["lex_smaller_than_H"] and not d["o7_holds"] for d in diags)
        if has_full_pass:
            fully_satisfying += 1
        if has_o7_fail_with_lex_smaller:
            any_o7_failure += 1
    print(f"\nof the {len(multi_r_examples)} relaxed multi-R examples:")
    print(f"  have >=1 leaf R-node with lex_smaller=True AND O7_holds=True "
          f"(i.e. pass every currently-proved local condition): {fully_satisfying}")
    print(f"  have >=1 leaf R-node with lex_smaller=True but O7 FAILS "
          f"(external common neighbor present): {any_o7_failure}")

    f_clean_multi_r = [e for e in multi_r_examples if e[4]]
    print(f"of which F-CLEAN (genuine survivors -- NONE expected): {len(f_clean_multi_r)}")
    if f_clean_multi_r:
        print("  !!! F-CLEAN MULTI-R-NODE ONE-POLE SURVIVOR FOUND -- escalate immediately")
        for e in f_clean_multi_r[:5]:
            print("   ", e)

    print(f"\nsmallest relaxed (non-F-clean) multi-R examples, with O6/O7 leaf "
          f"diagnostics (up to 5):")
    for n, g6, r, nr, fclean, diags in sorted(multi_r_examples, key=lambda t: t[0])[:5]:
        print(f"  n={n} g6={g6} root={r} #R-nodes={nr} F-clean={fclean}")
        for d in diags:
            print(f"    leaf R-node poles=({d['x']},{d['y']}) P_R order/edges="
                  f"{d['P_R_order']}/{d['P_R_edges']} tdeg=({d['tdeg_x']},{d['tdeg_y']}) "
                  f"internal_min_deg={d['internal_min_deg']} "
                  f"lex_smaller_than_H={d['lex_smaller_than_H']} "
                  f"O7_holds(no ext common nbr)={d['o7_holds']} "
                  f"external_common_neighbors={d['external_common_neighbors']}")


if __name__ == "__main__":
    main()
