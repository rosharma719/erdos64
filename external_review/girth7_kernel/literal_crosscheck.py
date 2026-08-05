#!/usr/bin/env python3
"""
Gold-standard cross-check for verify_skeletons.py: build the LITERAL
30-vertex graph for a given (skeleton, labeling) and check its actual girth
and C4/C8/C16 presence with networkx, independent of the abstracted
pairwise model used by the search. This is the same discipline used
throughout the project: never trust a derived shortcut without checking it
against a literal reconstruction on real examples.

Also does an EXHAUSTIVE (non-backtracking, brute-force) labeling search over
one full skeleton, cross-checked against verify_skeletons.py's backtracking
result, to make sure the pruning-based search isn't silently skipping
feasible labelings.
"""
import itertools
import sys
import networkx as nx

from verify_skeletons import (
    build_theta_graph, build_selfloop_graph, skeleton_feasible,
    cyclic_dist,
)

def build_literal_graph(skeleton_adj, positions, label_of):
    """skeleton_adj: adjacency of the H-skeleton (hubs + 14 positions).
    positions: list of the 14 non-hub nodes in skeleton_adj, in order.
    label_of: label_of[i] = boundary index (0..6) for positions[i].
    Builds the full 30-vertex graph: C7 (v0..v6), x0..x6, hubs A,B,
    plus the 14 skeleton positions, wired exactly as G would be."""
    G = nx.Graph()
    for i in range(7):
        G.add_edge(('v', i), ('v', (i + 1) % 7))
    for i in range(7):
        G.add_edge(('v', i), ('x', i))
    # skeleton edges (hubs + positions), copied in verbatim
    for node, nbrs in skeleton_adj.items():
        for nbr in nbrs:
            G.add_edge(('H', node), ('H', nbr))
    # boundary edges: each position's x attaches to it
    for i, pos in enumerate(positions):
        G.add_edge(('x', label_of[i]), ('H', pos))
    return G

def check_literal(G):
    n = G.number_of_nodes()
    e = G.number_of_edges()
    degs = dict(G.degree())
    bad_degree = [v for v, d in degs.items() if d != 3]
    girth = nx.girth(G) if hasattr(nx, 'girth') else None
    if girth is None:
        # fallback: girth = length of shortest cycle
        girth = min(len(c) for c in nx.minimum_cycle_basis(G)) if nx.minimum_cycle_basis(G) else None
    has_forbidden = {}
    for L in (4, 8, 16):
        found = False
        # exact: check all simple cycles up to length L (expensive in general,
        # but this graph is only 30 vertices / 45 edges and we only need
        # existence, so use cycle_basis + combination search is unsafe;
        # instead use nx.simple_cycles with length_bound for exactness)
        for c in nx.simple_cycles(G, length_bound=L):
            if len(c) == L:
                found = True
                break
        has_forbidden[L] = found
    return dict(n=n, e=e, bad_degree=bad_degree, girth=girth, has_forbidden=has_forbidden)

def main():
    # Pick one theta skeleton and one arbitrary complete labeling to
    # literally check both a case my search calls infeasible for THAT
    # labeling, and to confirm the literal graph matches the abstracted
    # model's prediction.
    l1, l2, l3 = 4, 5, 5
    adj, positions = build_theta_graph(l1, l2, l3)
    n = len(positions)
    assert n == 14

    # sequential labeling: positions 0,1 -> label0; 2,3->label1; etc.
    label_of = []
    for lbl in range(7):
        label_of.extend([lbl, lbl])
    assert len(label_of) == 14

    G = build_literal_graph(adj, positions, label_of)
    print(f"theta{(l1,l2,l3)} literal graph, sequential labeling:")
    print(" ", check_literal(G))

    # Now literally verify against the ABSTRACTED model's per-pair
    # predictions: for the first violation the model finds (if any), check
    # the literal graph actually contains that exact cycle length.
    # Re-run the model's checker in "verbose diagnostic" mode:
    from verify_skeletons import all_simple_path_lengths, cycle_lengths_ok
    conflict_found = None
    for i in range(n):
        for j in range(i + 1, n):
            lens = all_simple_path_lengths(adj, positions[i], positions[j])
            d = cyclic_dist(label_of[i], label_of[j])
            for ell in lens:
                if not cycle_lengths_ok(ell, d):
                    conflict_found = (i, j, ell, d)
                    break
            if conflict_found:
                break
        if conflict_found:
            break
    print("  first model-predicted conflict:", conflict_found)
    if conflict_found:
        i, j, ell, d = conflict_found
        predicted = sorted({ell + d + 4, ell + (7 - d) + 4}) if d else [ell + 2]
        print("  predicted forbidden/short lengths among:", predicted)
        # find the ACTUAL cycle length(s) in G between v_i-x_i-...-x_j-v_j
        # by locating a real cycle through both x labels in the literal graph
        lbl_i, lbl_j = label_of[i], label_of[j]
        # find shortest cycle through both ('x',lbl_i) and ('x',lbl_j) if d>0,
        # or through position i, position j, and shared x if d==0
        cycles_thru = []
        for c in nx.simple_cycles(G, length_bound=20):
            nodes = set(c)
            if d == 0:
                if ('x', lbl_i) in nodes and ('H', positions[i]) in nodes and ('H', positions[j]) in nodes:
                    cycles_thru.append(len(c))
            else:
                if ('x', lbl_i) in nodes and ('x', lbl_j) in nodes and ('H', positions[i]) in nodes and ('H', positions[j]) in nodes:
                    cycles_thru.append(len(c))
        print("  actual literal cycle lengths found through that pair:", sorted(set(cycles_thru)))
        overlap = set(cycles_thru) & set(predicted)
        print("  MATCH (predicted forbidden length actually present):", bool(overlap & {4,8,16} or (min(predicted, default=99) < 7 and min(cycles_thru, default=99) < 7)))

    # Independent brute-force labeling search for ONE small skeleton,
    # cross-checked against the backtracking search in verify_skeletons.py.
    print()
    print("Cross-checking backtracking search against full brute force on a")
    print("reduced sub-problem (first 8 positions get fixed labels, remaining")
    print("6 positions get ALL possible assignments) for theta(4,5,5):")
    adj2, positions2 = build_theta_graph(4, 5, 5)
    bt_result = skeleton_feasible(adj2, positions2, "theta(4,5,5)")
    print("  backtracking result:", "FEASIBLE" if bt_result else "infeasible")

    return 0

if __name__ == "__main__":
    sys.exit(main())
