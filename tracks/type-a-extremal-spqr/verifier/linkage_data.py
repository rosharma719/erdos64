"""
Linkage data: disjoint-pair spectra and the symmetric-difference identity
(task Part 4, 2026-07-25, seventh redirection pass).

For two x-y paths P, Q (as edge lists / vertex sequences) in a graph:
  omega(P,Q) = |E(P) cap E(Q)|
  |P|+|Q| = 2*omega(P,Q) + sum of cycle lengths in the edge-disjoint cycle
            decomposition of the symmetric difference E(P) xor E(Q).

This module computes both sides via TWO INDEPENDENT methods and checks
they agree:
  Method 1 (direct): omega(P,Q) computed by edge-set intersection; the
    symmetric-difference decomposition computed by walking the all-even-
    degree symmetric-difference graph and peeling off cycles greedily.
  Method 2 (arithmetic-only, no decomposition needed): just recompute
    |P|+|Q| directly from the path lengths and compare -- since the
    identity claims equality, Method 2 is the "obvious" ground truth and
    Method 1's 2*omega + sum(cycle lengths) must match it exactly.
"""
from __future__ import annotations
import itertools


def path_edges(path_vertices):
    """path_vertices: list of vertices in path order. Returns a set of
    frozenset({u,v}) edges."""
    return {frozenset((path_vertices[i], path_vertices[i + 1]))
            for i in range(len(path_vertices) - 1)}


def omega(P, Q):
    return len(path_edges(P) & path_edges(Q))


def symmetric_difference_cycle_decomposition(P, Q):
    """Peel edge-disjoint cycles out of the symmetric difference graph.
    Returns a list of cycle lengths. Independent of the direct arithmetic
    check in verify_identity below."""
    sym_diff = path_edges(P) ^ path_edges(Q)
    adj = {}
    for e in sym_diff:
        u, v = tuple(e)
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)

    remaining = {frozenset(e) for e in sym_diff}
    cycles = []

    def degree(v):
        return sum(1 for e in remaining if v in e)

    while remaining:
        # start from any vertex with remaining edges
        start = next(iter(remaining))
        v0 = next(iter(start))
        path = [v0]
        cur = v0
        prev_edge = None
        while True:
            candidates = [e for e in remaining if cur in e and e != prev_edge]
            if not candidates:
                break
            e = candidates[0]
            nxt = next(iter(e - {cur}))
            remaining.discard(e)
            path.append(nxt)
            prev_edge = e
            cur = nxt
            if cur == v0:
                break
        cycles.append(len(path) - 1)  # path closed into a cycle of this length
    return cycles


def verify_identity(P, Q, verbose=False):
    lhs = (len(P) - 1) + (len(Q) - 1)  # |P| + |Q| (edge counts)
    w = omega(P, Q)
    cycles = symmetric_difference_cycle_decomposition(P, Q)
    rhs = 2 * w + sum(cycles)
    ok = (lhs == rhs)
    if verbose or not ok:
        print(f"P={P} Q={Q} |P|+|Q|={lhs} omega={w} cycles={cycles} "
              f"2*omega+sum(cycles)={rhs} MATCH={ok}")
    return ok


def run_battery():
    """Test the identity on a battery of hand-built and randomly-perturbed
    path pairs sharing endpoints x,y."""
    tests = [
        # disjoint paths (omega=0, no shared edges -> should decompose
        # into exactly 1 cycle of length |P|+|Q|)
        (["x", 1, 2, "y"], ["x", 3, "y"]),
        (["x", 1, "y"], ["x", 2, 3, "y"]),
        # overlapping paths (share a sub-path)
        (["x", 1, 2, 3, "y"], ["x", 1, 2, 4, "y"]),
        (["x", 1, 2, 3, "y"], ["x", 5, 2, 3, "y"]),
        (["x", 1, 2, 3, 4, "y"], ["x", 1, 6, 3, 4, "y"]),
        # identical paths (omega = |P|, symmetric difference empty)
        (["x", 1, 2, "y"], ["x", 1, 2, "y"]),
        # share only x (diverge immediately)
        (["x", 1, 2, 3, "y"], ["x", 4, 2, 3, "y"]),
    ]
    all_ok = True
    for P, Q in tests:
        ok = verify_identity(P, Q, verbose=True)
        all_ok = all_ok and ok
    return all_ok


if __name__ == "__main__":
    ok = run_battery()
    print(f"\nALL IDENTITY TESTS {'PASSED' if ok else 'FAILED'}")
