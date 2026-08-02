#!/usr/bin/env python3
"""Mechanical cross-check for contraction_mixed_witness.md: the four
combined-endpoint orbits (T1, T2a, T2b, T2c) at a Type N vertex, the
NPT-theta / 4-branch-fan / vertex-hub arithmetic, and the two new
arithmetic lemmas (E: 2^x+2^y-1 never a power of two; F: 2^s+2 never a
power of two) plus the two supporting identities used in T2c.

Scope, same discipline as the earlier verifier scripts: nothing here
tests a claim presupposing a minimal Erdos-Gyarfas counterexample
exists. What IS checked: the orbit-counting result (4 orbits of size 6
under the diagonal S3 action), and the exact cycle-length arithmetic of
every clean configuration in the summary table, by direct gadget
construction with two independent cycle checkers. Kept separate from
contraction_lift.py / atom_lift.py / neighborhood_lift.py, none of
which are touched.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.contraction_lift import (  # noqa: E402
    Graph,
    from_edges,
    verify_cycle,
    verify_cycle_nx,
)


def is_power_of_two(n: int) -> bool:
    return n >= 1 and (n & (n - 1)) == 0


# ----------------------------------------------------------------------------
# Arithmetic lemmas E, F and the two supporting identities
# ----------------------------------------------------------------------------

def check_arithmetic_extensions(max_exp: int = 9):
    checked = {"lemma_E": 0, "lemma_F": 0, "odd_sum_plus_one": 0,
               "triple_sum_minus_two": 0}
    for x in range(2, max_exp + 1):
        for y in range(2, max_exp + 1):
            assert not is_power_of_two(2 ** x + 2 ** y - 1), (x, y, "E")
            checked["lemma_E"] += 1
            assert not is_power_of_two(2 ** x + 2 ** y + 1), (x, y, "odd+1")
            checked["odd_sum_plus_one"] += 1
        assert not is_power_of_two(2 ** x + 2), (x, "F")
        checked["lemma_F"] += 1
    for x in range(2, max_exp - 2):
        for y in range(2, max_exp - 2):
            for z in range(2, max_exp - 2):
                assert not is_power_of_two(2 ** x + 2 ** y + 2 ** z - 2), (x, y, z)
                checked["triple_sum_minus_two"] += 1
    return checked


# ----------------------------------------------------------------------------
# Part III.1: combined endpoint orbits
# ----------------------------------------------------------------------------

def check_combined_orbits():
    elts = ("a", "b", "c")
    functions = []
    for fa in elts:
        if fa == "a":
            continue
        for fb in elts:
            if fb == "b":
                continue
            for fc in elts:
                if fc == "c":
                    continue
                functions.append({"a": fa, "b": fb, "c": fc})
    assert len(functions) == 8
    pairs = [frozenset(p) for p in itertools.combinations(elts, 2)]

    def relabel_f(f, perm):
        return {perm[x]: perm[f[x]] for x in elts}

    def relabel_pair(p, perm):
        return frozenset(perm[x] for x in p)

    def canon(f, p):
        best = None
        for permtuple in itertools.permutations(elts):
            perm = dict(zip(elts, permtuple))
            rf = relabel_f(f, perm)
            rp = relabel_pair(p, perm)
            key = (tuple(rf[x] for x in elts), tuple(sorted(rp)))
            if best is None or key < best:
                best = key
        return best

    orbits: Dict = {}
    for f in functions:
        for p in pairs:
            key = canon(f, p)
            orbits.setdefault(key, []).append(1)

    assert len(orbits) == 4, len(orbits)
    sizes = sorted(len(v) for v in orbits.values())
    assert sizes == [6, 6, 6, 6], sizes
    return {"num_orbits": len(orbits), "orbit_sizes": sizes}


# ----------------------------------------------------------------------------
# Part IV: gadget arithmetic
# ----------------------------------------------------------------------------

def build_parallel_paths(p, q, lengths: List[int]):
    """Internally vertex-disjoint p-q paths of the given lengths (edge
    counts). Returns (graph, list_of_path_vertex_lists)."""
    edges = []
    path_lists = []
    for idx, L in enumerate(lengths):
        assert L >= 1
        mid = [f"path{idx}_m{i}" for i in range(L - 1)]
        chain = [p] + mid + [q]
        for i in range(len(chain) - 1):
            edges.append((chain[i], chain[i + 1]))
        path_lists.append(chain)
    g = from_edges(edges)
    return g, path_lists


def pairwise_cycle_length(path_a: List, path_b: List) -> int:
    """Union of two p-q paths (sharing only endpoints) as a cycle length."""
    return (len(path_a) - 1) + (len(path_b) - 1)


def check_theta_gadget(r: int, s: int):
    """T1/T2b-style: v-path (len 2, via literal vertex v), P (len 2^r-1),
    Q (len 2^s), all sharing endpoints p,q. Checks all 3 pairwise cycles."""
    p, q = "p", "q"
    v = "v"
    lenP = 2 ** r - 1
    lenQ = 2 ** s
    g, paths = build_parallel_paths(p, q, [lenP, lenQ])
    # add the v-path explicitly (length 2, via a real vertex v)
    g.setdefault(v, set())
    g[v] |= {p, q}
    g[p].add(v)
    g[q].add(v)
    vpath = [p, v, q]
    P, Q = paths

    results = {}
    for name, (x, y) in (("v_P", (vpath, P)), ("v_Q", (vpath, Q)), ("P_Q", (P, Q))):
        cyc = x + list(reversed(y[1:-1]))  # x forward, y backward, closing at p
        assert verify_cycle(g, cyc), (name, cyc)
        assert verify_cycle_nx(g, cyc)
        results[name] = len(cyc)

    assert results["v_P"] == 2 ** r + 1
    assert results["v_Q"] == 2 ** s + 2
    assert results["P_Q"] == 2 ** r + 2 ** s - 1
    assert not any(is_power_of_two(x) for x in results.values())
    return results


def check_fan_gadget(ra: int, rb: int, s: int):
    """T2a-style: 4 parallel a-b paths (v-path len2, P_a len 2^ra-1,
    P_b len 2^rb-1, Q_ab len 2^s). Checks all C(4,2)=6 pairwise cycles."""
    p, q = "a", "b"
    v = "v"
    lens = [2 ** ra - 1, 2 ** rb - 1, 2 ** s]
    g, paths = build_parallel_paths(p, q, lens)
    g.setdefault(v, set())
    g[v] |= {p, q}
    g[p].add(v)
    g[q].add(v)
    vpath = [p, v, q]
    all_paths = {"v": vpath, "Pa": paths[0], "Pb": paths[1], "Qab": paths[2]}

    predicted = {
        frozenset(["v", "Pa"]): 2 ** ra + 1,
        frozenset(["v", "Pb"]): 2 ** rb + 1,
        frozenset(["v", "Qab"]): 2 ** s + 2,
        frozenset(["Pa", "Pb"]): 2 ** ra + 2 ** rb - 2,
        frozenset(["Pa", "Qab"]): 2 ** ra + 2 ** s - 1,
        frozenset(["Pb", "Qab"]): 2 ** rb + 2 ** s - 1,
    }
    results = {}
    for name1, name2 in itertools.combinations(all_paths, 2):
        x, y = all_paths[name1], all_paths[name2]
        cyc = x + list(reversed(y[1:-1]))
        assert verify_cycle(g, cyc), (name1, name2, cyc)
        assert verify_cycle_nx(g, cyc)
        key = frozenset([name1, name2])
        results[key] = len(cyc)
        assert results[key] == predicted[key], (name1, name2, results[key], predicted[key])
        assert not is_power_of_two(results[key])
    return {"_".join(sorted(k)): v for k, v in results.items()}


def check_t2c_gadget(ra: int, rb: int, rc: int, s: int):
    """T2c-style: v adjacent to a,b,c (star, Type N); P_a: a->b (len
    2^ra-1); P_b: b->a (len 2^rb-1); P_c: c->a (len 2^rc-1); Q_bc: b->c
    (len 2^s). All internally disjoint. Checks 3 vertex-hub merges plus
    the closed triangle P_a+Q_bc+P_c avoiding v."""
    v, a, b, c = "v", "a", "b", "c"
    edges = [(v, a), (v, b), (v, c)]

    def chain(prefix, x, y, L):
        mid = [f"{prefix}m{i}" for i in range(L - 1)]
        seq = [x] + mid + [y]
        for i in range(len(seq) - 1):
            edges.append((seq[i], seq[i + 1]))
        return seq

    Pa = chain("pa_", a, b, 2 ** ra - 1)
    Pb = chain("pb_", b, a, 2 ** rb - 1)
    Pc = chain("pc_", c, a, 2 ** rc - 1)
    Qbc = chain("q_", b, c, 2 ** s)
    g = from_edges(edges)

    results = {}

    # v-a-Pa-b-Qbc-c-v
    cyc = [v, a] + Pa[1:-1] + [b] + Qbc[1:-1] + [c]
    assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc)
    results["Pa_Qbc_v"] = len(cyc)
    assert results["Pa_Qbc_v"] == 2 ** ra + 2 ** s + 1

    # v-a-[Pb reversed]-b-Qbc-c-v
    cyc = [v, a] + list(reversed(Pb[1:-1])) + [b] + Qbc[1:-1] + [c]
    assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc)
    results["Pb_Qbc_v"] = len(cyc)
    assert results["Pb_Qbc_v"] == 2 ** rb + 2 ** s + 1

    # v-b-Qbc-c-Pc-a-v
    cyc = [v, b] + Qbc[1:-1] + [c] + Pc[1:-1] + [a]
    assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc)
    results["Qbc_Pc_v"] = len(cyc)
    assert results["Qbc_Pc_v"] == 2 ** s + 2 ** rc + 1

    # closed triangle Pa + Qbc + Pc, avoiding v
    cyc = Pa[:-1] + Qbc[:-1] + Pc[:-1]
    assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc)
    results["triangle_no_v"] = len(cyc)
    assert results["triangle_no_v"] == 2 ** ra + 2 ** rc + 2 ** s - 2

    for val in results.values():
        assert not is_power_of_two(val)
    return results


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    summary = {}
    summary["arithmetic_extensions"] = check_arithmetic_extensions()
    summary["combined_orbits"] = check_combined_orbits()

    t1_results = [check_theta_gadget(r, s) for (r, s) in
                  [(2, 2), (2, 3), (3, 2), (3, 4)]]
    summary["T1_and_T2b_theta_gadgets"] = t1_results

    fan_results = [check_fan_gadget(ra, rb, s) for (ra, rb, s) in
                   [(2, 2, 2), (2, 3, 2), (3, 4, 5)]]
    summary["T2a_fan_gadgets"] = fan_results

    t2c_results = [check_t2c_gadget(ra, rb, rc, s) for (ra, rb, rc, s) in
                   [(2, 2, 2, 2), (2, 3, 4, 2), (3, 2, 5, 4)]]
    summary["T2c_hub_gadgets"] = t2c_results

    print("=== mixed_witness.py: mechanical cross-check summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("0 mismatches, 0 assertion failures.")
    return summary


if __name__ == "__main__":
    main()
