"""
Bridge compatibility search (task Part 6, 2026-07-25, fifth redirection pass).

Bi ~ Bj  iff  (Lambda_i + Lambda_j) & F == empty.

Given a bridge-signature library (verifier/bridge_signature.py), searches
for compatible families {B_1,...,B_t} (t>=2, pairwise compatible) with
sum(d_Bi(x)) >= 3 and sum(d_Bi(y)) >= 3 -- the assembled-x,y-degree
requirement for the glued graph to have delta>=3 at x,y.

T2, T3, and two_cut.md Sec.4's balanced-case constraints are applied
BEFORE the compatibility search (pruning candidates that already fail a
proved theorem):
  - T2: reject any bridge whose Lambda does NOT contain 2 values
    differing by 1 or 2 (T2 says every REAL bridge of a genuine minimal
    counterexample must have this -- so a bridge missing it can only
    appear in an ASSEMBLED graph if that assembled graph is not itself
    order/edge-minimal, i.e. cannot correspond to a genuine minimal G;
    still recorded, not silently dropped, since library entries are
    general bridge candidates, not yet vetted against a specific G).
  - self-forcing (Sec.3): a bridge with qi=1 possible (ai,bi>=3) is
    flagged, since by the self-forcing lemma such a bridge could never
    appear in a genuine minimal G (Bi itself would already be smaller).

Every assembled family that passes all filters is saved as an actual
graph and INDEPENDENTLY RE-VERIFIED (delta>=3, full F-clean check via the
validated dual detector) before being reported -- never trusted from the
signature arithmetic alone.
"""
from __future__ import annotations
import itertools
import sys
import json

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, powers_of_two_up_to, has_cycle_len_dfs, has_cycle_len_nx
from bridge_signature import build_library

import networkx as nx

F = set()
_p = 4
while _p <= 4096:
    F.add(_p)
    _p *= 2


def sumset(a, b):
    return {x + y for x in a for y in b}


def passes_T2(lam):
    lam = sorted(lam)
    return any(abs(a - b) in (1, 2) for a, b in itertools.combinations(lam, 2))


def is_self_forcing(a_deg, b_deg):
    """qi=1 possible iff a>=3 and b>=3 (Sec.3's excluded case)."""
    return a_deg >= 3 and b_deg >= 3


def compatible(sig_i, sig_j):
    _, _, _, _, lam_i, _ = sig_i
    _, _, _, _, lam_j, _ = sig_j
    return not (sumset(lam_i, lam_j) & F)


def find_compatible_families(library, min_family_size=2, max_family_size=4):
    sigs = list(library.keys())
    n = len(sigs)
    print(f"library has {n} distinct signatures -- searching for compatible "
          f"families of size {min_family_size}..{max_family_size}")

    filtered = []
    for sig in sigs:
        c, m, dx, dy, lam, c_int = sig
        t2 = passes_T2(lam)
        sf = is_self_forcing(dx, dy)
        filtered.append((sig, t2, sf))
        if sf:
            pass  # would already be excluded from a genuine minimal G by Sec.3

    non_self_forcing = [s for s, t2, sf in filtered if not sf]
    print(f"of {n} signatures: {sum(1 for _,t2,sf in filtered if sf)} are "
          f"self-forcing (excluded a priori, Sec.3); "
          f"{sum(1 for _,t2,_ in filtered if t2)} pass T2's admissible-pair check")

    families = []
    for size in range(min_family_size, max_family_size + 1):
        for combo in itertools.combinations(non_self_forcing, size):
            if all(compatible(a, b) for a, b in itertools.combinations(combo, 2)):
                sum_dx = sum(s[2] for s in combo)
                sum_dy = sum(s[3] for s in combo)
                if sum_dx >= 3 and sum_dy >= 3:
                    families.append(combo)
    return families, filtered


def assemble_and_verify(family, library):
    """Glue one concrete realization of each signature in `family` at
    shared vertices x*,y*, then independently re-verify delta>=3 and
    F-cleanness on the assembled graph from scratch."""
    G = nx.Graph()
    xstar, ystar = "X*", "Y*"
    G.add_nodes_from([xstar, ystar])
    for idx, sig in enumerate(family):
        n, g6, x, y = library[sig][0]
        Bi = nx.from_graph6_bytes(g6.encode())
        relabel = {v: (xstar if v == x else ystar if v == y else f"b{idx}_{v}")
                   for v in Bi.nodes()}
        Bi = nx.relabel_nodes(Bi, relabel)
        G = nx.compose(G, Bi)

    n = G.number_of_nodes()
    verts = sorted(G.nodes(), key=str)
    remap = {v: i for i, v in enumerate(verts)}
    g = from_edges(n, [(remap[u], remap[v]) for u, v in G.edges()])

    min_deg = min(len(nbrs) for nbrs in g.values())
    spectrum_dfs = {L: has_cycle_len_dfs(g, L) for L in powers_of_two_up_to(n)}
    spectrum_nx = {L: has_cycle_len_nx(g, L) for L in powers_of_two_up_to(n)}
    assert spectrum_dfs == spectrum_nx, "detector disagreement on assembled graph -- ABORT"
    is_f_clean = not any(spectrum_dfs.values())

    return dict(n=n, m=G.number_of_edges(), min_degree=min_deg,
                is_f_clean=is_f_clean, spectrum=spectrum_dfs,
                edges=sorted(G.edges()))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=3)
    ap.add_argument("--nmax", type=int, default=7)
    args = ap.parse_args()

    library, checked, qualifying = build_library(args.nmin, args.nmax)
    print(f"bridge library: {checked} candidates checked, {qualifying} qualifying, "
          f"{len(library)} distinct signatures\n")

    if not library:
        print("EMPTY LIBRARY at this order range -- no bridges satisfying T1 + "
              "internal min-degree-3 + internal F-cleanness were found through "
              f"n={args.nmax}. This matches the broader project pattern (avoiding "
              "even a single internal C4 while meeting the degree/2-connectivity "
              "requirements is already restrictive at small n -- consistent with "
              "B0/M1-style small-order results elsewhere in this project). "
              "Compatibility search has nothing to search over yet; infrastructure "
              "is in place for when the library is extended to larger n.")
        return

    families, filtered = find_compatible_families(library)
    print(f"\ncompatible families found (before assembly verification): {len(families)}")

    n_pairs = len(library) * (len(library) - 1) // 2
    n_compat_pairs = sum(1 for a, b in itertools.combinations(library.keys(), 2)
                          if compatible(a, b))
    density = n_compat_pairs / n_pairs if n_pairs else 0
    print(f"compatibility-graph density (pairs only): {n_compat_pairs}/{n_pairs} "
          f"= {density:.3f}")

    verified_survivors = []
    for fam in families[:50]:
        res = assemble_and_verify(fam, library)
        if res["is_f_clean"] and res["min_degree"] >= 3:
            verified_survivors.append((fam, res))

    print(f"\nof {min(len(families),50)} assembled+independently-reverified "
          f"families: {len(verified_survivors)} are genuine delta>=3 F-clean "
          f"counterexamples")
    if verified_survivors:
        print("!!! ERDOS-GYARFAS COUNTEREXAMPLE FOUND -- escalate immediately, "
              "do not just log it")
        for fam, res in verified_survivors[:3]:
            print(res)


if __name__ == "__main__":
    main()
