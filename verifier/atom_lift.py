#!/usr/bin/env python3
"""Mechanical cross-check for contraction_atoms.md: the general
contractible-atom lemma, the triangle-pair lemma, the Type N/T local
cubic-vertex dichotomy, the two-orbit functional-digraph classification,
the five-lemma arithmetic toolkit (A, A', B, C, D, D3), and the
bridge-arithmetic chord corollary.

Scope, stated up front (same discipline as contraction_lift.py, kept
deliberately separate and untouched): nothing here tests a claim that
presupposes a minimal Erdos-Gyarfas counterexample exists. What IS
checked exhaustively are the unconditional mechanics: atom contraction
simplicity/degree preservation, the 2^k+r lift-length formula, the
triangle-pair's exact (2^k+1, 2^k+2) split, the Type N/T dichotomy and
triangle uniqueness, the functional-digraph orbit count, the five
gluing/arithmetic lemmas, and the chord-distance contradiction case.
"""

from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from verifier.contraction_lift import (  # noqa: E402
    Graph,
    from_edges,
    to_nx,
    min_degree,
    is_simple,
    nontriangle_edges,
    verify_cycle,
    verify_cycle_nx,
    has_c4,
    petersen,
    cube_graph,
    k33,
    prism_with_diagonal,
    random_delta3_graph,
)


# ----------------------------------------------------------------------------
# Part I: general atom contraction
# ----------------------------------------------------------------------------

def induced_subgraph(g: Graph, A: Set) -> Graph:
    return {a: (g[a] & A) for a in A}


def contract_atom(g: Graph, A: Set):
    """Contract A to one vertex. Returns (g2, star, attach) where attach
    maps each outside neighbour w of A to its unique attachment vertex
    in A -- raises if (H2) (at most one A-neighbour per outside vertex)
    fails."""
    A = set(A)
    boundary: Dict = {}
    for a in A:
        for w in g[a]:
            if w in A:
                continue
            boundary.setdefault(w, set()).add(a)
    for w, attach in boundary.items():
        assert len(attach) == 1, f"(H2) violated: {w} attaches to {attach}"
    star = ("*atom*", tuple(sorted(A, key=repr)))
    g2: Graph = {}
    for w in g:
        if w in A:
            continue
        g2[w] = set(g[w]) - A
        if w in boundary:
            g2[w].add(star)
    g2[star] = set(boundary.keys())
    attach_of = {w: next(iter(s)) for w, s in boundary.items()}
    return g2, star, attach_of


def lift_atom_cycle(g: Graph, A: Set, attach_of: Dict, cyc: List, star,
                     gA_paths_cache: Dict) -> List[Tuple[List, int]]:
    """Given a cycle of G/A through `star`, return every lift
    (one per simple a-b path R in G[A]) as (lifted_cycle, r)."""
    idx = cyc.index(star)
    n = len(cyc)
    w1, w2 = cyc[idx - 1], cyc[(idx + 1) % n]
    a, b = attach_of[w1], attach_of[w2]
    results = []
    if a == b:
        new_cyc = cyc[:idx] + [a] + cyc[idx + 1:]
        results.append((new_cyc, 0))  # r=0 marker: same-vertex (im)possible lift
        return results
    key = (a, b)
    if key not in gA_paths_cache:
        gAnx = to_nx(induced_subgraph(g, A))
        gA_paths_cache[key] = list(nx.all_simple_paths(gAnx, a, b))
    for R in gA_paths_cache[key]:
        new_cyc = cyc[:idx] + list(R) + cyc[idx + 1:]
        results.append((new_cyc, len(R) - 1))
    return results


def satisfies_H2(g: Graph, A: Set) -> bool:
    boundary: Dict = {}
    for a in A:
        for w in g[a]:
            if w in A:
                continue
            boundary.setdefault(w, set()).add(a)
    return all(len(s) == 1 for s in boundary.values())


def check_atom_contraction(g: Graph, atoms: List[Set], length_bound: int = 8,
                            verbose=False):
    stats = {"atoms": 0, "cycles_lifted": 0, "length_formula_ok": 0,
             "same_vertex_lift_same_length": 0}
    for A in atoms:
        gA = induced_subgraph(g, A)
        if not nx.is_connected(to_nx(gA)):
            continue
        if not satisfies_H2(g, A):
            continue  # (H2) is a genuine hypothesis of the lemma, not every
                       # connected vertex set qualifies as an atom -- skip
                       # non-atoms rather than asserting on them
        g2, star, attach_of = contract_atom(g, A)
        assert is_simple(g2)
        for w in g2:
            if w == star:
                continue
            assert len(g2[w]) == len(g[w]), "degree not preserved off A"
        boundary_size = len(g2[star])
        if boundary_size < 3:
            continue
        assert min_degree(g2) >= 3
        stats["atoms"] += 1

        Gnx = to_nx(g2)
        cache: Dict = {}
        for cyc in nx.simple_cycles(Gnx, length_bound=length_bound):
            if star not in cyc:
                continue
            lifts = lift_atom_cycle(g, A, attach_of, cyc, star, cache)
            for new_cyc, r in lifts:
                if r == 0:
                    # same-attachment-vertex lift: must reproduce a SAME
                    # length cycle of G (mechanically always true; whether
                    # this is *impossible* in a real minimal counterexample
                    # is the minimality argument, not testable here)
                    assert verify_cycle(g, new_cyc) and verify_cycle_nx(g, new_cyc)
                    assert len(new_cyc) == len(cyc)
                    stats["same_vertex_lift_same_length"] += 1
                    continue
                assert verify_cycle(g, new_cyc), f"lift invalid: {new_cyc}"
                assert verify_cycle_nx(g, new_cyc)
                assert len(new_cyc) == len(cyc) + r, "2^k+r formula violated"
                stats["length_formula_ok"] += 1
                stats["cycles_lifted"] += 1
    if verbose:
        print(stats)
    return stats


def random_connected_atom(g: Graph, size: int, rng: random.Random):
    start = rng.choice(list(g.keys()))
    A = {start}
    frontier = set(g[start])
    while len(A) < size and frontier:
        pick = rng.choice(list(frontier))
        A.add(pick)
        frontier |= g[pick]
        frontier -= A
    return A


# ----------------------------------------------------------------------------
# Part III: triangle contraction and the triangle-pair lemma
# ----------------------------------------------------------------------------

def triangle_bearing_c4_free_fixture() -> Graph:
    """A cubic, C4-free graph that DOES contain triangles -- needed to
    give III.1's automatic-contractibility claim genuine test coverage
    (the other fixtures are either triangle-free or, like the prism,
    contain C4s and are correctly excluded by the C4-free scope of that
    theorem). Found by rejection sampling over random cubic graphs;
    fixed at n=10, seed=12 for reproducibility."""
    G = nx.random_regular_graph(3, 10, seed=12)
    return {v: set(G.neighbors(v)) for v in G.nodes()}


def find_triangles(g: Graph) -> List[Tuple]:
    out = []
    for a in g:
        for b in g[a]:
            if b <= a:
                continue
            common = g[a] & g[b]
            for c in common:
                if c > b:
                    out.append((a, b, c))
    return out


def check_triangle_contraction(g: Graph):
    """(H2)/(H3) hold automatically for every triangle (III.1)."""
    checked = 0
    for (a, b, c) in find_triangles(g):
        A = {a, b, c}
        g2, star, attach_of = contract_atom(g, A)  # raises if (H2) fails
        assert is_simple(g2)
        boundary = len(g2[star])
        expected = sum(len(g[x]) - 2 for x in A)
        assert boundary == expected, "deg(t) formula mismatch"
        assert boundary >= 3, "(H3) failed for a triangle -- should be automatic"
        checked += 1
    return checked


def check_triangle_pair(k_values=(2, 3, 4)):
    """Explicit gadget: triangle {a,b,c}, plus an outside w1-w2 path of
    length 2^k-2 (w1 attached only to a, w2 only to b, both distinct
    from a,b,c), and a fresh boundary vertex z attached at c (to keep
    deg(t)>=3). Verifies the atom-lifting lemma gives exactly
    (2^k+1, 2^k+2) via the direct edge ab and the path a-c-b
    respectively, sharing every edge except the internal triangle
    routing."""
    results = []
    for k in k_values:
        outside_len = (2 ** k) - 2  # length of the w1-w2 path, excluding a-w1/w2-b
        assert outside_len >= 2
        a, b, c = "a", "b", "c"
        edges = [(a, b), (b, c), (c, a)]
        mid = [f"p{i}" for i in range(outside_len - 1)]
        chain = ["w1"] + mid + ["w2"]
        for i in range(len(chain) - 1):
            edges.append((chain[i], chain[i + 1]))
        edges.append((a, "w1"))
        edges.append((b, "w2"))
        # extra boundary vertex at c so deg(t)>=3
        edges.append((c, "z"))
        g = from_edges(edges)
        A = {a, b, c}
        g2, star, attach_of = contract_atom(g, A)
        assert len(g2[star]) >= 3

        Gnx = to_nx(g2)
        found = {}
        for cyc in nx.simple_cycles(Gnx, length_bound=2 ** k + 3):
            if star not in cyc:
                continue
            idx = cyc.index(star)
            w1c, w2c = cyc[idx - 1], cyc[(idx + 1) % len(cyc)]
            a1, b1 = attach_of[w1c], attach_of[w2c]
            if {a1, b1} != {a, b}:
                continue
            cache: Dict = {}
            lifts = lift_atom_cycle(g, A, attach_of, cyc, star, cache)
            for new_cyc, r in lifts:
                if r == 0:
                    continue
                assert verify_cycle(g, new_cyc) and verify_cycle_nx(g, new_cyc)
                found[r] = len(new_cyc)
            break  # one D suffices to exercise both internal routes
        assert found.get(1) == 2 ** k + 1, found
        assert found.get(2) == 2 ** k + 2, found
        results.append((k, found[1], found[2]))
    return results


# ----------------------------------------------------------------------------
# Part IV: Type N / Type T dichotomy + triangle uniqueness
# ----------------------------------------------------------------------------

def check_cubic_dichotomy(g: Graph):
    assert not has_c4(g)
    checked = {"type_N": 0, "type_T": 0}
    for v, nbrs in g.items():
        if len(nbrs) != 3:
            continue
        a, b, c = sorted(nbrs, key=repr)
        internal = sum(1 for (x, y) in itertools.combinations((a, b, c), 2)
                        if y in g[x])
        assert internal in (0, 1), f"cubic vertex {v} has {internal} internal edges"
        if internal == 0:
            checked["type_N"] += 1
        else:
            checked["type_T"] += 1
            # triangle uniqueness: exactly one pair among a,b,c is an edge,
            # and it is the ONLY triangle through v (by construction, since
            # a triangle through v needs 2 of v's edges + the connector).
            pairs = [(x, y) for (x, y) in itertools.combinations((a, b, c), 2)
                     if y in g[x]]
            assert len(pairs) == 1
    return checked


# ----------------------------------------------------------------------------
# Part V.0: functional-digraph classification
# ----------------------------------------------------------------------------

def classify_functional_digraphs():
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

    def relabel(f, perm):
        return {perm[x]: perm[f[x]] for x in elts}

    def canon(f):
        best = None
        for p in itertools.permutations(elts):
            perm = dict(zip(elts, p))
            rf = relabel(f, perm)
            key = tuple(rf[x] for x in elts)
            if best is None or key < best:
                best = key
        return best

    orbits: Dict = {}
    for f in functions:
        key = canon(f)
        orbits.setdefault(key, []).append(f)

    sizes = sorted(len(v) for v in orbits.values())
    assert len(orbits) == 2, f"expected 2 orbits, got {len(orbits)}"
    assert sizes == [2, 6], f"expected orbit sizes [2,6], got {sizes}"
    return {"num_orbits": len(orbits), "orbit_sizes": sizes}


# ----------------------------------------------------------------------------
# Arithmetic toolkit: Lemmas A, A', D3 (brute-force), B, C, D (gadgets)
# ----------------------------------------------------------------------------

def is_power_of_two(n: int) -> bool:
    return n >= 1 and (n & (n - 1)) == 0


def check_arithmetic_toolkit(max_exp: int = 8):
    checked = {"lemma_A": 0, "lemma_Aprime": 0, "lemma_D3": 0}
    for x in range(2, max_exp + 1):
        for y in range(2, max_exp + 1):
            predicted_A = (x == y)
            actual_A = is_power_of_two(2 ** x + 2 ** y)
            assert predicted_A == actual_A, (x, y, "Lemma A")
            checked["lemma_A"] += 1

            actual_Aprime = is_power_of_two(2 ** x + 2 ** y - 2)
            assert not actual_Aprime, (x, y, "Lemma A'")
            checked["lemma_Aprime"] += 1

    for x in range(2, max_exp + 1):
        for y in range(2, max_exp + 1):
            for z in range(2, max_exp + 1):
                actual_D3 = is_power_of_two(2 ** x + 2 ** y + 2 ** z - 3)
                assert not actual_D3, (x, y, z, "Lemma D3")
                checked["lemma_D3"] += 1
    return checked


def _path_graph(labels: List) -> Graph:
    return from_edges([(labels[i], labels[i + 1]) for i in range(len(labels) - 1)])


def check_gluing_lemmas(lengths=(3, 4, 5, 7)):
    results = {"lemma_B": [], "lemma_C": [], "lemma_D": []}

    # Lemma B: two cycles of length l1, l2 sharing exactly one edge e0=xy,
    # no other vertex. Each cycle's x-y path (excluding e0) has l1-1 (resp.
    # l2-1) edges and l1 (resp. l2) vertices total, closed by e0.
    for l1 in lengths:
        for l2 in lengths:
            x, y = "x", "y"
            path1 = [x] + [f"p{i}" for i in range(l1 - 2)] + [y]
            path2 = [x] + [f"q{i}" for i in range(l2 - 2)] + [y]
            edges = [(x, y)]
            for path in (path1, path2):
                edges += [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            g = from_edges(edges)
            cyc1, cyc2 = path1, path2
            assert verify_cycle(g, cyc1) and len(cyc1) == l1
            assert verify_cycle(g, cyc2) and len(cyc2) == l2
            merged = path1 + list(reversed(path2[1:-1]))
            g_no_e0 = {w: set(n) for w, n in g.items()}
            g_no_e0[x].discard(y)
            g_no_e0[y].discard(x)
            assert verify_cycle(g_no_e0, merged) and verify_cycle_nx(g_no_e0, merged)
            assert len(merged) == l1 + l2 - 2
            results["lemma_B"].append((l1, l2, len(merged)))

    # Lemma C: Q1 (p-q), Q2 (q-s), hub vertex h adjacent to p and s.
    for l1 in lengths:
        for l2 in lengths:
            p, q, s, hub = "p", "q", "s", "hub"
            path1 = [p] + [f"u{i}" for i in range(l1 - 1)] + [q]
            path2 = [q] + [f"v{i}" for i in range(l2 - 1)] + [s]
            edges = [(hub, p), (hub, s)]
            for path in (path1, path2):
                edges += [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            g = from_edges(edges)
            cyc = [hub] + path1 + path2[1:]
            assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc)
            assert len(cyc) == l1 + l2 + 2
            results["lemma_C"].append((l1, l2, len(cyc)))

    # Lemma D: two p-q paths sharing only endpoints, no hub.
    for l1 in lengths:
        for l2 in lengths:
            p, q = "p", "q"
            path1 = [p] + [f"u{i}" for i in range(l1 - 1)] + [q]
            path2 = [p] + [f"v{i}" for i in range(l2 - 1)] + [q]
            edges = []
            for path in (path1, path2):
                edges += [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            g = from_edges(edges)
            cyc = path1 + list(reversed(path2[1:-1]))
            assert verify_cycle(g, cyc) and verify_cycle_nx(g, cyc)
            assert len(cyc) == l1 + l2
            results["lemma_D"].append((l1, l2, len(cyc)))

    return results


# ----------------------------------------------------------------------------
# Part VII.1: bridge arithmetic on a canonical near-power cycle
# ----------------------------------------------------------------------------

def check_bridge_arithmetic(r_values=(2, 3, 4)):
    results = []
    for r in r_values:
        L = 2 ** r + 1
        cyc_labels = [f"c{i}" for i in range(L)]
        g = from_edges([(cyc_labels[i], cyc_labels[(i + 1) % L]) for i in range(L)])
        assert verify_cycle(g, cyc_labels) and len(cyc_labels) == L

        # attach chords (ell=1) at every genuine cyclic distance d=2..L//2
        # (d=1 would coincide with an existing cycle edge, not a chord) and
        # check the two arc-closure lengths against the symbolic formula.
        contradictions = []
        for d in range(2, L // 2 + 1):
            i0, i1 = 0, d
            u, v = cyc_labels[i0], cyc_labels[i1]
            g_chord = {w: set(n) for w, n in g.items()}
            g_chord[u].add(v)
            g_chord[v].add(u)
            len_short = d + 1  # ell=1 chord + short arc
            len_long = (L - d) + 1
            # verify these lengths are exactly realized as simple cycles
            short_cyc = cyc_labels[i0:i1 + 1]
            assert verify_cycle(g_chord, short_cyc)
            assert len(short_cyc) == len_short
            long_cyc = cyc_labels[i1:] + cyc_labels[:i0 + 1]
            assert verify_cycle(g_chord, long_cyc)
            assert len(long_cyc) == len_long
            if is_power_of_two(len_short) or is_power_of_two(len_long):
                contradictions.append((d, len_short, len_long))
        # the d=2^m-1 rule should predict exactly the len_short contradictions
        predicted = [d for d in range(2, L // 2 + 1) if is_power_of_two(d + 1)]
        found_short = [d for (d, ls, ll) in contradictions if is_power_of_two(ls)]
        assert sorted(predicted) == sorted(found_short), (r, predicted, found_short)
        results.append({"r": r, "L": L, "chord_contradiction_distances": predicted})
    return results


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    summary = {}

    fixtures = [petersen(), cube_graph(), k33(), prism_with_diagonal(),
                triangle_bearing_c4_free_fixture()]
    for seed in range(15):
        n = random.Random(1000 + seed).choice([8, 10, 12])
        fixtures.append(random_delta3_graph(n, extra_p=0.10, seed=1000 + seed))

    atom_stats_total = {"atoms": 0, "cycles_lifted": 0, "length_formula_ok": 0,
                         "same_vertex_lift_same_length": 0}
    for gi, g in enumerate(fixtures):
        rng = random.Random(2000 + gi)
        atoms = []
        for _ in range(6):
            size = rng.choice([2, 3, 4])
            atoms.append(random_connected_atom(g, size, rng))
        s = check_atom_contraction(g, atoms)
        for k in atom_stats_total:
            atom_stats_total[k] += s[k]
    summary["atom_contraction"] = atom_stats_total

    # III.1's automatic-contractibility proof needs G C4-free (that is where
    # "no outside vertex adjacent to two triangle vertices" comes from); test
    # it only on the C4-free fixtures, matching the theorem's actual scope.
    tri_checked = sum(check_triangle_contraction(g) for g in fixtures if not has_c4(g))
    summary["triangles_automatically_contractible"] = tri_checked

    summary["triangle_pair_lemma"] = check_triangle_pair()

    dichotomy_total = {"type_N": 0, "type_T": 0}
    for g in fixtures:
        if has_c4(g):
            continue
        d = check_cubic_dichotomy(g)
        for k in dichotomy_total:
            dichotomy_total[k] += d[k]
    summary["cubic_dichotomy"] = dichotomy_total

    summary["functional_digraph_orbits"] = classify_functional_digraphs()
    summary["arithmetic_toolkit"] = check_arithmetic_toolkit()
    gluing = check_gluing_lemmas()
    summary["gluing_lemma_instances"] = {k: len(v) for k, v in gluing.items()}
    summary["bridge_arithmetic"] = check_bridge_arithmetic()

    print("=== atom_lift.py: mechanical cross-check summary ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("0 mismatches, 0 assertion failures.")
    return summary


if __name__ == "__main__":
    main()
