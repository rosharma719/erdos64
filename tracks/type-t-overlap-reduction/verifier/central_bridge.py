#!/usr/bin/env python3
"""Mechanical cross-check for contraction_central_bridge.md Parts I-V:
CB1 (central bridge always has >=2 attachments), the endpoint-return
cycle list, the topological-K4 construction and its exact seven-cycle
enumeration, the NPT substitution table, the first-excursion
containment fact, and a structural (non-minimality-certified) instance
of a two-excursion CB2 itinerary.

Scope, same discipline as the earlier verifier scripts: nothing here
tests a claim presupposing a minimal Erdos-Gyarfas counterexample
exists, beyond citing S5 (already established elsewhere in this
project) for CB1's proof -- the computational check of CB1 here is a
structural cut-vertex check, not a re-derivation of S5 itself. Nothing
here claims to certify CB2 as true; only a structurally valid instance
is exhibited, explicitly not proved minimal/canonical.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.contraction_lift import (  # noqa: E402
    Graph,
    from_edges,
    to_nx,
    verify_cycle,
    verify_cycle_nx,
)


def is_power_of_two(n: int) -> bool:
    return n >= 1 and (n & (n - 1)) == 0


# ----------------------------------------------------------------------------
# Part I.1: CB1
# ----------------------------------------------------------------------------

def check_cb1():
    """Build a theta with a component C attached ONLY at v (the cubic
    branch-vertex), and confirm v is a cut vertex -- the structural fact
    CB1's proof invokes S5 to forbid for a genuinely cubic v."""
    p, q, v = "p", "q", "v"
    edges = [(p, v), (v, q)]
    # P1, P2 (arbitrary lengths, just to have a real theta)
    P1 = [p, "p1a", "p1b", q]
    P2 = [p, "p2a", "p2b", "p2c", q]
    for path in (P1, P2):
        for i in range(len(path) - 1):
            edges.append((path[i], path[i + 1]))
    # component C attached ONLY at v
    C = ["w", "c1", "c2"]
    edges += [(v, "w"), ("w", "c1"), ("c1", "c2"), ("c2", "w")]
    g = from_edges(edges)

    G = to_nx(g)
    G_minus_v = G.copy()
    G_minus_v.remove_node(v)
    comps = list(nx.connected_components(G_minus_v))
    # C's vertices should be isolated from Theta's vertices once v is removed
    c_comp = next(c for c in comps if "w" in c)
    theta_verts = {p, q, "p1a", "p1b", "p2a", "p2b", "p2c"}
    assert c_comp.isdisjoint(theta_verts), "C should be severed from Theta by removing v"
    assert len(comps) >= 2, "v must be a cut vertex here"
    return {"components_after_removing_v": len(comps), "v_is_cut_vertex": True}


# ----------------------------------------------------------------------------
# Part III: endpoint return
# ----------------------------------------------------------------------------

def build_theta(p_label, q_label, v_label, M, N, prefix=""):
    edges = [(p_label, v_label), (v_label, q_label)]
    P1 = [p_label] + [f"{prefix}p1_{i}" for i in range(M - 1)] + [q_label]
    P2 = [p_label] + [f"{prefix}p2_{i}" for i in range(N - 1)] + [q_label]
    for path in (P1, P2):
        for i in range(len(path) - 1):
            edges.append((path[i], path[i + 1]))
    return edges, P1, P2


def check_endpoint_return(M: int, N: int, ell: int, with_pq_edge: bool):
    p, q, v = "p", "q", "v"
    edges, P1, P2 = build_theta(p, q, v, M, N, prefix=f"er_{M}_{N}_{ell}_{with_pq_edge}_")
    if with_pq_edge:
        edges.append((p, q))
    # R: v -> p, length ell, fresh vertices (x = p, endpoint return)
    mid = [f"R_{M}_{N}_{ell}_{with_pq_edge}_{i}" for i in range(ell - 1)]
    Rchain = [v] + mid + [p]
    for i in range(len(Rchain) - 1):
        edges.append((Rchain[i], Rchain[i + 1]))
    g = from_edges(edges)

    results = {}
    # ell+1: R (v...p, full) + direct edge pv closes the cycle
    cyc = Rchain  # v,...,p; closes p->v via direct edge
    assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc)
    results["ell_plus_1"] = len(cyc)
    assert results["ell_plus_1"] == ell + 1

    # ell+1+M: R (v...p, minus p) + P1 (p...q, full) + edge qv closes it
    cyc = Rchain[:-1] + P1  # v,mid...,p,p1's,q ; closes q->v via direct edge
    assert verify_cycle(g, cyc), cyc
    assert verify_cycle_nx(g, cyc)
    results["ell_plus_1_plus_M"] = len(cyc)
    assert results["ell_plus_1_plus_M"] == ell + 1 + M

    cyc = Rchain[:-1] + P2
    assert verify_cycle(g, cyc), cyc
    assert verify_cycle_nx(g, cyc)
    results["ell_plus_1_plus_N"] = len(cyc)
    assert results["ell_plus_1_plus_N"] == ell + 1 + N

    if with_pq_edge:
        cyc = Rchain[:-1] + [p, q]  # v,...,p,q ; closes q->v via direct edge
        assert verify_cycle(g, cyc), cyc
        assert verify_cycle_nx(g, cyc)
        results["ell_plus_2"] = len(cyc)
        assert results["ell_plus_2"] == ell + 2

    return results


# ----------------------------------------------------------------------------
# Part IV: topological K4
# ----------------------------------------------------------------------------

def build_topological_k4(M: int, N: int, ell: int, d: int, prefix=""):
    p, q, v = f"{prefix}p", f"{prefix}q", f"{prefix}v"
    x = f"{prefix}x"
    edges = [(p, v), (v, q)]
    # P1 split at x: p..x length d, x..q length M-d
    px_mid = [f"{prefix}px_{i}" for i in range(d - 1)]
    px_chain = [p] + px_mid + [x]
    xq_mid = [f"{prefix}xq_{i}" for i in range(M - d - 1)]
    xq_chain = [x] + xq_mid + [q]
    for chain in (px_chain, xq_chain):
        for i in range(len(chain) - 1):
            edges.append((chain[i], chain[i + 1]))
    # P2: p..q length N
    p2_mid = [f"{prefix}p2_{i}" for i in range(N - 1)]
    p2_chain = [p] + p2_mid + [q]
    for i in range(len(p2_chain) - 1):
        edges.append((p2_chain[i], p2_chain[i + 1]))
    # R = vx: v..x length ell
    r_mid = [f"{prefix}r_{i}" for i in range(ell - 1)]
    r_chain = [v] + r_mid + [x]
    for i in range(len(r_chain) - 1):
        edges.append((r_chain[i], r_chain[i + 1]))
    g = from_edges(edges)
    return g, dict(p=p, q=q, v=v, x=x)


def check_topological_k4(M: int, N: int, ell: int, d: int):
    g, verts = build_topological_k4(M, N, ell, d, prefix=f"k4_{M}_{N}_{ell}_{d}_")
    predicted = sorted([
        N + 2,
        ell + d + 1,
        ell + (M - d) + 1,
        M + N,
        M + 2,
        ell + (M - d) + N + 1,
        ell + d + N + 1,
    ])

    G = to_nx(g)
    max_len = max(predicted) + 1
    found_lengths = []
    for cyc in nx.simple_cycles(G, length_bound=max_len):
        found_lengths.append(len(cyc))
    found_lengths.sort()

    assert found_lengths == predicted, (found_lengths, predicted)
    assert len(found_lengths) == 7, len(found_lengths)
    return {"predicted": predicted, "found_via_independent_enumeration": found_lengths}


def check_npt_k4_substitution(r_values, s_values, ell_d_pairs):
    results = []
    for r in r_values:
        for s in s_values:
            for (assignment, M, N) in (("M=2^r-1,N=2^s", 2 ** r - 1, 2 ** s),
                                        ("M=2^s,N=2^r-1", 2 ** s, 2 ** r - 1)):
                closed = {
                    "N_plus_2": N + 2,
                    "M_plus_N": M + N,
                    "M_plus_2": M + 2,
                }
                for name, val in closed.items():
                    assert not is_power_of_two(val), (r, s, assignment, name, val)
                for (ell, d) in ell_d_pairs:
                    if not (1 <= d <= M - 1):
                        continue
                    open_vals = {
                        "ell_d_1": ell + d + 1,
                        "ell_Md_1": ell + (M - d) + 1,
                        "ell_Md_N_1": ell + (M - d) + N + 1,
                        "ell_d_N_1": ell + d + N + 1,
                    }
                    results.append({"r": r, "s": s, "assignment": assignment,
                                     "ell": ell, "d": d, "closed_safe": closed,
                                     "open_values": open_vals})
    return results


# ----------------------------------------------------------------------------
# Part V: first-excursion containment, and a structural CB2 instance
# ----------------------------------------------------------------------------

def check_first_excursion():
    """Two SEPARATE components C (=B_v, containing w) and C' attached to
    Theta at different points. Confirm a walk from w, avoiding Theta,
    cannot reach C' without first touching Theta (i.e. without first
    exiting B_v)."""
    p, q, v = "p", "q", "v"
    edges = [(p, v), (v, q)]
    P1 = [p, "m1", "m2", q]
    for i in range(len(P1) - 1):
        edges.append((P1[i], P1[i + 1]))
    # B_v: w attached to v, plus internal structure, exits Theta at "m1"
    edges += [(v, "w"), ("w", "bv1"), ("bv1", "m1")]
    # C': a DIFFERENT component, attached at "m2" and "q" only
    edges += [("cp1", "cp2"), ("cp2", "m2"), ("cp1", "q")]
    g = from_edges(edges)

    G = to_nx(g)
    theta_verts = {p, q, v, "m1", "m2"}
    G_minus_theta = G.copy()
    G_minus_theta.remove_nodes_from(theta_verts)
    comps = list(nx.connected_components(G_minus_theta))
    w_comp = next(c for c in comps if "w" in c)
    cp_comp = next(c for c in comps if "cp1" in c)
    assert w_comp != cp_comp, "B_v and C' must be genuinely separate components"
    assert "cp1" not in w_comp and "cp2" not in w_comp
    # BFS from w avoiding Theta entirely except at the moment of exit
    return {"B_v_component": sorted(w_comp), "Cprime_component": sorted(cp_comp),
            "genuinely_separate": True}


def check_cb2_structural_instance():
    """Build a two-excursion w-to-p itinerary: w -(B_v)- y1 -(theta arc)-
    y2 -(B')- p. Confirms it is a genuine simple path respecting the
    itinerary definition. Does NOT certify it is the canonical/shortest
    choice -- that is explicitly not claimed."""
    p, q, v = "p", "q", "v"
    edges = [(p, v), (v, q)]
    P1 = [p, "y2", "y1", "m3", q]  # p - y2 - y1 - m3 - q
    for i in range(len(P1) - 1):
        edges.append((P1[i], P1[i + 1]))
    P2 = [p, "n1", "n2", "n3", "n4", q]
    for i in range(len(P2) - 1):
        edges.append((P2[i], P2[i + 1]))
    # B_v: w -> y1 (first excursion)
    edges += [(v, "w"), ("w", "bv1"), ("bv1", "y1")]
    # B' (separate component): y2 -> p directly via a short excursion
    edges += [("y2", "bp1"), ("bp1", "p")]
    g = from_edges(edges)

    G = to_nx(g)
    theta_verts = {p, q, v, "y1", "y2", "m3", "n1", "n2", "n3", "n4"}
    G_minus_theta = G.copy()
    G_minus_theta.remove_nodes_from(theta_verts)
    comps = list(nx.connected_components(G_minus_theta))
    w_comp = next(c for c in comps if "w" in c)
    bp_comp = next(c for c in comps if "bp1" in c)
    assert w_comp != bp_comp

    itinerary_path = ["v", "w", "bv1", "y1", "y2", "bp1", "p"]
    assert verify_cycle is not None  # keep import used
    # confirm it's a genuine simple path (not a cycle claim)
    assert len(set(itinerary_path)) == len(itinerary_path)
    for i in range(len(itinerary_path) - 1):
        assert itinerary_path[i + 1] in g[itinerary_path[i]], (itinerary_path[i], itinerary_path[i + 1])

    return {"itinerary": itinerary_path,
            "first_excursion_component": sorted(w_comp),
            "second_excursion_component": sorted(bp_comp),
            "genuinely_two_excursions": w_comp != bp_comp,
            "note": "structurally valid instance; NOT certified minimal/canonical"}


def main():
    summary = {}
    summary["cb1"] = check_cb1()

    endpoint_results = []
    for (M, N, ell, with_pq) in [(7, 4, 3, False), (5, 9, 2, True), (8, 6, 5, False)]:
        endpoint_results.append({"M": M, "N": N, "ell": ell, "pq_edge": with_pq,
                                  "result": check_endpoint_return(M, N, ell, with_pq)})
    summary["endpoint_return"] = endpoint_results

    k4_results = []
    for (M, N, ell, d) in [(7, 4, 3, 2), (9, 3, 2, 4), (8, 6, 5, 3)]:
        k4_results.append({"M": M, "N": N, "ell": ell, "d": d,
                            "result": check_topological_k4(M, N, ell, d)})
    summary["topological_k4"] = k4_results

    summary["npt_k4_substitution_sample"] = check_npt_k4_substitution(
        r_values=[2, 3, 4], s_values=[2, 3, 4], ell_d_pairs=[(3, 1), (5, 2)]
    )[:4]  # sample of the full table for the printed summary

    summary["first_excursion"] = check_first_excursion()
    summary["cb2_structural_instance"] = check_cb2_structural_instance()

    print("=== central_bridge.py: mechanical cross-check summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("0 mismatches, 0 assertion failures. "
          "(CB2 minimality/canonicity intentionally not tested -- open.)")
    return summary


if __name__ == "__main__":
    main()
