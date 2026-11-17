"""Independent tests for the new partial-expansion calculus."""
import importlib.util
from pathlib import Path

import networkx as nx

SRC = Path(__file__).resolve().with_name('partial_triangle_expansion.py')
spec = importlib.util.spec_from_file_location('partial_triangle_expansion', SRC)
mod = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_exact_spectrum_for_all_subsets_of_small_bases():
    # Independent original/expanded cycle enumeration, not just forbidden-length tests.
    for name in ('k4', 'prism', 'cube'):
        G = mod.base_graph(name)
        nodes = list(G)
        for mask in range(1 << len(nodes)):
            S = {nodes[i] for i in range(len(nodes)) if mask >> i & 1}
            H = mod.triangle_expand(G, S)
            assert len(H) == len(G) + 2 * len(S)
            assert all(d == 3 for _, d in H.degree())
            got = {len(C) for C in mod.cycles(H)}
            expected = mod.predicted_spectrum(G, S)
            assert got == expected, (name, mask, sorted(got ^ expected))


def test_forbidden_constraint_vs_dfs_on_petersen():
    G = mod.base_graph('petersen')
    ns = list(G)
    # Independent DFS for 4/8/16 on representative subsets of every size.
    cases = [set(), set(ns), *({ns[i] for i in range(10) if mask >> i & 1}
                              for mask in range(0, 1 << 10, 17))]
    for S in cases:
        H = mod.triangle_expand(G, S)
        predicted = mod.predicted_spectrum(G, S)
        for p in (4, 8, 16):
            assert (p in predicted) == mod.independent_has_cycle_length(H, p), (S, p)


def test_exhaustive_constraints_vs_dfs_on_small_bases():
    for name in ('k4', 'prism', 'cube'):
        G = mod.base_graph(name)
        ns = list(G)
        permitted = {frozenset(S) for S in mod.viable_subsets(G, {4,8})}
        for mask in range(1 << len(ns)):
            S = {ns[i] for i in range(len(ns)) if mask >> i & 1}
            H = mod.triangle_expand(G, S)
            actual = not (mod.independent_has_cycle_length(H, 4)
                          or mod.independent_has_cycle_length(H, 8))
            assert actual == (frozenset(S) in permitted), (name, S)


def test_count_constraints():
    assert mod.allowed_expansion_counts(3, {4, 8}) == [0, 2]
    assert mod.allowed_expansion_counts(4, {4, 8}) == [1]
    assert mod.allowed_expansion_counts(5, {4, 8}) == [0, 1, 4, 5]
    assert mod.allowed_expansion_counts(6, {4, 8}) == [0, 3, 4, 5, 6]
    assert mod.allowed_expansion_counts(7, {4, 8}) == [0, 2, 3, 4, 5, 6, 7]
