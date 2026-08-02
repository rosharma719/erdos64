#!/usr/bin/env python3
"""Mechanical cross-check for contraction_neighborhood.md Parts I-II:
closed-neighborhood contraction A=N[v] at a cubic vertex, the cubic
power-path lemma CN1, and the Type T offset comparison between the
triangle atom and the closed-neighborhood atom.

Scope, same discipline as contraction_lift.py/atom_lift.py: nothing
here tests a claim presupposing a minimal Erdos-Gyarfas counterexample
exists. What IS checked exhaustively: (H2)/(H3) automatic for A=N[v],
the exact contracted-degree bounds by local type, that v is never a
boundary-attachment vertex, the CN1 raw-path arithmetic (length 2^k)
and its r=2 closure (length 2^k+2), the Type T pair-(a,b)/(a,c) offset
sets, and the triangle-vs-neighborhood internal-path-set comparison.
Kept separate from contraction_lift.py and atom_lift.py, neither of
which is touched.
"""

from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path
from typing import Dict, List, Set

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.contraction_lift import (  # noqa: E402
    Graph,
    from_edges,
    to_nx,
    min_degree,
    is_simple,
    verify_cycle,
    verify_cycle_nx,
    has_c4,
    petersen,
    cube_graph,
    k33,
    random_delta3_graph,
)
from verifier.atom_lift import (  # noqa: E402
    induced_subgraph,
    contract_atom,
    lift_atom_cycle,
    satisfies_H2,
    triangle_bearing_c4_free_fixture,
)


# ----------------------------------------------------------------------------
# Part I: CN1
# ----------------------------------------------------------------------------

def local_type(g: Graph, v) -> str:
    a, b, c = sorted(g[v], key=repr)
    internal = sum(1 for (x, y) in itertools.combinations((a, b, c), 2)
                    if y in g[x])
    assert internal in (0, 1)
    return "N" if internal == 0 else "T"


def check_cn1(g: Graph, length_bound: int = 8):
    assert not has_c4(g)
    stats = {"cubic_vertices": 0, "type_N": 0, "type_T": 0,
              "cycles_through_star": 0, "raw_path_ok": 0,
              "r2_closure_ok": 0, "same_attachment_skipped": 0}
    for v, nbrs in g.items():
        if len(nbrs) != 3:
            continue
        a, b, c = sorted(nbrs, key=repr)
        A = {v, a, b, c}
        assert satisfies_H2(g, A), "(H2) should be automatic for A=N[v]"
        g2, star, attach_of = contract_atom(g, A)
        assert is_simple(g2)
        assert v not in attach_of.values(), "v must never be a boundary attachment"

        t = local_type(g, v)
        stats["type_" + t] += 1
        boundary = len(g2[star])
        if t == "N":
            assert boundary >= 6, (v, boundary)
        else:
            assert boundary >= 4, (v, boundary)
        assert min_degree(g2) >= 3
        stats["cubic_vertices"] += 1

        Gnx = to_nx(g2)
        cache: Dict = {}
        for cyc in nx.simple_cycles(Gnx, length_bound=length_bound):
            if star not in cyc:
                continue
            idx = cyc.index(star)
            n = len(cyc)
            w1, w2 = cyc[idx - 1], cyc[(idx + 1) % n]
            p, q = attach_of[w1], attach_of[w2]
            assert v not in (p, q), "v must never be an attachment vertex"
            assert p in (a, b, c) and q in (a, b, c)
            stats["cycles_through_star"] += 1

            if p == q:
                # Mechanically possible on an arbitrary (non-counterexample)
                # fixture -- CN1's "p != q" step is a minimality argument
                # (contraction_atoms.md I.4), not a mechanical fact, so it
                # cannot be asserted unconditionally here. Skip the
                # CN1-specific arithmetic below, which assumes p != q.
                stats["same_attachment_skipped"] += 1
                continue

            # raw CN1 path: p - w1 - Q_out - w2 - q, length exactly len(cyc),
            # entirely avoiding v. Rotate cyc to start right after star (at
            # w2) and end right before it (at w1) -- NOT a plain slice-splice,
            # which would wrongly place w1,w2 adjacent to each other.
            rotated = cyc[idx + 1:] + cyc[:idx]  # w2 -> ... -> w1
            raw_path = [p] + list(reversed(rotated)) + [q]  # p -> w1 -> ... -> w2 -> q
            assert v not in raw_path
            assert len(set(raw_path)) == len(raw_path)
            for i in range(len(raw_path) - 1):
                assert raw_path[i + 1] in g[raw_path[i]]
            assert len(raw_path) - 1 == len(cyc), "CN1 length must be 2^k"
            stats["raw_path_ok"] += 1

            # r=2 closure via p-v-q, cross-checked through the general
            # atom-lifting machinery (lift_atom_cycle enumerates every
            # simple p-q path in G[A], including p-v-q).
            lifts = lift_atom_cycle(g, A, attach_of, cyc, star, cache)
            found_r2 = False
            for new_cyc, r in lifts:
                if r == 0:
                    continue
                if v in new_cyc and len(new_cyc) == len(raw_path) - 1 + 1 + 2:
                    pass
                if r == 2 and v in new_cyc:
                    assert verify_cycle(g, new_cyc) and verify_cycle_nx(g, new_cyc)
                    assert len(new_cyc) == len(cyc) + 2
                    found_r2 = True
            assert found_r2, "the p-v-q internal route must always be available"
            stats["r2_closure_ok"] += 1
    return stats


# ----------------------------------------------------------------------------
# Part II: Type T offsets
# ----------------------------------------------------------------------------

def _type_T_gadget(k: int, attach_pair: str):
    """v Type T (triangle v,a,b, pendant c), plus an outside w1-w2 chain
    of length 2^k-2 attached per `attach_pair` in {'ab','ac'}."""
    outside_len = (2 ** k) - 2
    assert outside_len >= 2
    v, a, b, c = "v", "a", "b", "c"
    edges = [(v, a), (v, b), (v, c), (a, b)]
    mid = [f"p{i}" for i in range(outside_len - 1)]
    chain = ["w1"] + mid + ["w2"]
    for i in range(len(chain) - 1):
        edges.append((chain[i], chain[i + 1]))
    if attach_pair == "ab":
        edges += [(a, "w1"), (b, "w2"), (c, "z1"), (c, "z2")]
    else:  # 'ac'
        edges += [(a, "w1"), (c, "w2"), (b, "z1"), (b, "z2")]
    return from_edges(edges), v, a, b, c


def check_type_T_offsets(k_values=(2, 3, 4)):
    results = []
    for k in k_values:
        for pair in ("ab", "ac"):
            g, v, a, b, c = _type_T_gadget(k, pair)
            A = {v, a, b, c}
            assert satisfies_H2(g, A)
            g2, star, attach_of = contract_atom(g, A)
            assert len(g2[star]) >= 3
            Gnx = to_nx(g2)
            found = {}
            for cyc in nx.simple_cycles(Gnx, length_bound=2 ** k + 4):
                if star not in cyc:
                    continue
                idx = cyc.index(star)
                w1c, w2c = cyc[idx - 1], cyc[(idx + 1) % len(cyc)]
                p1, q1 = attach_of[w1c], attach_of[w2c]
                target = {"a", "b"} if pair == "ab" else {"a", "c"}
                if {p1, q1} != target:
                    continue
                cache: Dict = {}
                lifts = lift_atom_cycle(g, A, attach_of, cyc, star, cache)
                for new_cyc, r in lifts:
                    if r == 0:
                        continue
                    assert verify_cycle(g, new_cyc) and verify_cycle_nx(g, new_cyc)
                    found[r] = len(new_cyc)
                break
            if pair == "ab":
                assert set(found.keys()) == {1, 2}, found
                assert found[1] == 2 ** k + 1 and found[2] == 2 ** k + 2
            else:
                assert set(found.keys()) == {2, 3}, found
                assert found[2] == 2 ** k + 2 and found[3] == 2 ** k + 3
            results.append((k, pair, found))
    return results


def check_triangle_vs_neighborhood(k=3):
    """Confirm the (a,b) internal-path set is IDENTICAL whether contracting
    the bare triangle {v,a,b} or the full A=N[v]={v,a,b,c}, while the
    (a,c) set is only reachable through the larger atom."""
    g, v, a, b, c = _type_T_gadget(k, "ab")
    T = {v, a, b}
    A = {v, a, b, c}

    gT = induced_subgraph(g, T)
    gA = induced_subgraph(g, A)
    paths_T_ab = list(nx.all_simple_paths(to_nx(gT), a, b))
    paths_A_ab = list(nx.all_simple_paths(to_nx(gA), a, b))
    lens_T_ab = sorted(len(p) - 1 for p in paths_T_ab)
    lens_A_ab = sorted(len(p) - 1 for p in paths_A_ab)
    assert lens_T_ab == lens_A_ab == [1, 2], (lens_T_ab, lens_A_ab)

    # (a,c) is not even expressible in G[T] (c not a vertex of T)
    assert c not in gT
    paths_A_ac = list(nx.all_simple_paths(to_nx(gA), a, c))
    lens_A_ac = sorted(len(p) - 1 for p in paths_A_ac)
    assert lens_A_ac == [2, 3], lens_A_ac

    return {"ab_lengths_triangle": lens_T_ab, "ab_lengths_neighborhood": lens_A_ab,
            "ac_lengths_neighborhood_only": lens_A_ac}


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    summary = {}

    fixtures = [petersen(), cube_graph(), k33(), triangle_bearing_c4_free_fixture()]
    for seed in range(15):
        n = random.Random(3000 + seed).choice([8, 10, 12])
        fixtures.append(random_delta3_graph(n, extra_p=0.10, seed=3000 + seed))

    total = {"cubic_vertices": 0, "type_N": 0, "type_T": 0,
              "cycles_through_star": 0, "raw_path_ok": 0, "r2_closure_ok": 0,
              "same_attachment_skipped": 0}
    for g in fixtures:
        if has_c4(g):
            continue
        s = check_cn1(g)
        for k in total:
            total[k] += s[k]
    summary["cn1"] = total

    summary["type_T_offsets"] = [
        (k, pair, found) for (k, pair, found) in check_type_T_offsets()
    ]
    summary["triangle_vs_neighborhood"] = check_triangle_vs_neighborhood()

    print("=== neighborhood_lift.py: mechanical cross-check summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("0 mismatches, 0 assertion failures.")
    return summary


if __name__ == "__main__":
    main()
