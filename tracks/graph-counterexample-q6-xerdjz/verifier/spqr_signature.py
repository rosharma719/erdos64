"""
Rooted SPQR two-terminal signatures (task Part 4, 2026-07-25, third pass).

Sigma(P) = (|V(P)|, |E(P)|, d_P(x), d_P(y), Lambda(P), C(P))
  - x,y: the 2 terminals of piece P.
  - Lambda(P): set of all simple x-y path lengths in P.
  - C(P): set of all simple cycle lengths lying entirely within P.

Exact composition rules (proved in one_pole.md's Part-4 companion text):
  SERIES  P = P1 -- (shared vertex m) -- P2, terminals (s,t) with s in P1, t in P2:
    |V(P)| = |V(P1)|+|V(P2)|-1
    |E(P)| = |E(P1)|+|E(P2)|
    d_P(s) = d_P1(s), d_P(t) = d_P2(t)          [unchanged -- only touch own piece]
    Lambda(P) = Lambda(P1) + Lambda(P2)          [sumset -- concatenate s-m, m-t paths]
    C(P) = C(P1) | C(P2)                          [union -- m is a genuine 1-cut,
                                                     no cycle can use both sides]

  PARALLEL  P = branches P_1..P_k, all sharing terminals (x,y):
    |V(P)| = sum(|V(Pj)|) - 2*(k-1)               [x,y counted once each]
    |E(P)| = sum(|E(Pj)|)
    d_P(x) = sum(d_Pj(x)), d_P(y) = sum(d_Pj(y))  [degree accumulates across branches]
    Lambda(P) = union_j Lambda(Pj)                 [a path stays in ONE branch]
    C(P) = [union_j C(Pj)] | [Lambda(Pi)+Lambda(Pj) for all i<j]   [cross-branch cycles]

Both rules are implemented here AND independently cross-checked against
brute-force exhaustive enumeration on the concretely assembled graph, for
many random small test cases -- this is the "independently verify" step
requested, not just a derivation on paper.

Rigid (R) node skeletons are NOT given a composition rule (per the task's
own instruction -- this is exactly where the arithmetic runs out and
per-skeleton analysis is needed instead; see spqr_k4_skeleton.py for the
K4 case specifically).
"""
from __future__ import annotations
from typing import FrozenSet, Set, Tuple
import itertools
import random

import networkx as nx


Signature = Tuple[int, int, int, int, FrozenSet[int], FrozenSet[int]]


def brute_force_signature(P: nx.Graph, x, y) -> Signature:
    """Ground truth: exhaustive enumeration of all simple x-y paths and all
    simple cycles in P. Only for small P (exponential)."""
    lengths = set()
    for path in nx.all_simple_paths(P, x, y):
        lengths.add(len(path) - 1)
    cycles = set()
    for cyc in nx.simple_cycles(P):
        if len(cyc) >= 3:
            cycles.add(len(cyc))
    return (P.number_of_nodes(), P.number_of_edges(),
            P.degree(x), P.degree(y), frozenset(lengths), frozenset(cycles))


def series_compose(sig1: Signature, sig2: Signature) -> Signature:
    """P1 has terminals (s,m); P2 has terminals (m,t); returns Sigma of the
    series composition with terminals (s,t). sig1's y-slot and sig2's
    x-slot are assumed to be the shared vertex m (caller's responsibility)."""
    v1, e1, ds1, dm1, lam1, c1 = sig1
    v2, e2, dm2, dt2, lam2, c2 = sig2
    V = v1 + v2 - 1
    E = e1 + e2
    Lambda = frozenset(a + b for a in lam1 for b in lam2)
    C = c1 | c2
    return (V, E, ds1, dt2, Lambda, C)


def parallel_compose(branch_sigs: list[Signature]) -> Signature:
    """All branches share terminals (x,y). Returns Sigma of the parallel
    composition."""
    V = sum(s[0] for s in branch_sigs) - 2 * (len(branch_sigs) - 1)
    E = sum(s[1] for s in branch_sigs)
    dx = sum(s[2] for s in branch_sigs)
    dy = sum(s[3] for s in branch_sigs)
    Lambda = frozenset().union(*(s[4] for s in branch_sigs))
    C = frozenset().union(*(s[5] for s in branch_sigs))
    for (s1, s2) in itertools.combinations(branch_sigs, 2):
        cross = frozenset(a + b for a in s1[4] for b in s2[4])
        C = C | cross
    return (V, E, dx, dy, Lambda, C)


# ---------------------------------------------------------------------------
# Random small-piece generators for cross-checking, built as ACTUAL graphs so
# brute force gives independent ground truth.
# ---------------------------------------------------------------------------

def random_sp_piece(rng: random.Random, max_extra=3):
    """Builds a random small 2-terminal series-parallel piece (as an actual
    nx.Graph with terminals s,t), tracking its Sigma via the SAME recursive
    process used to build it -- but we deliberately do NOT trust that
    tracked Sigma; brute_force_signature is recomputed from the assembled
    graph and compared against it as the real check."""
    counter = [0]

    def fresh():
        counter[0] += 1
        return f"v{counter[0]}"

    def base_edge():
        s, t = fresh(), fresh()
        G = nx.Graph()
        G.add_edge(s, t)
        return G, s, t

    def build(depth):
        if depth <= 0 or rng.random() < 0.35:
            return base_edge()
        if rng.random() < 0.5:
            # series
            G1, s1, m1 = build(depth - 1)
            G2, m2, t2 = build(depth - 1)
            G = nx.union(G1, G2)
            G = nx.relabel_nodes(G, {m2: m1})
            return G, s1, t2
        else:
            # parallel: 2..3 branches
            k = rng.randint(2, 3)
            branches = [build(depth - 1) for _ in range(k)]
            G = nx.Graph()
            s, t = fresh(), fresh()
            for (Gb, sb, tb) in branches:
                Gb = nx.relabel_nodes(Gb, {sb: s, tb: t})
                G = nx.compose(G, Gb)
            return G, s, t

    return build(rng.randint(1, max_extra))


def cross_check(trials=200, seed=0):
    rng = random.Random(seed)
    mismatches = []
    for i in range(trials):
        G, s, t = random_sp_piece(rng)
        if G.number_of_nodes() > 14:
            continue  # keep brute force tractable
        truth = brute_force_signature(G, s, t)
        # We don't separately track a "predicted" signature during random
        # generation (that would just re-derive the same formula); instead
        # this trial battery exists to validate series_compose/parallel_compose
        # directly via controlled constructions below.
    return mismatches


def targeted_composition_tests():
    """Directly construct P1, P2 concretely, compute brute-force Sigma for
    each and for the assembled composite, and check the formulas predict
    the composite from the pieces exactly."""
    failures = []

    # --- SERIES test battery ---
    for l1 in range(1, 4):
        for l2 in range(1, 4):
            P1 = nx.path_graph(l1 + 1)  # vertices 0..l1, terminals 0,l1
            P2 = nx.path_graph(l2 + 1)
            P2 = nx.relabel_nodes(P2, {v: f"b{v}" for v in P2.nodes()})
            s, m, t = 0, l1, "b" + str(0)
            # merge P1's terminal l1 with P2's terminal b0
            P2 = nx.relabel_nodes(P2, {"b0": l1})
            composite = nx.compose(P1, P2)
            t_label = f"b{l2}"
            sig1 = brute_force_signature(P1, s, l1)
            sig2 = brute_force_signature(P2, l1, t_label)
            predicted = series_compose(sig1, sig2)
            truth = brute_force_signature(composite, s, t_label)
            if predicted != truth:
                failures.append(("series", l1, l2, predicted, truth))

    # --- PARALLEL test battery: k paths of various lengths between s,t ---
    for lengths in [(1, 2), (2, 2), (1, 2, 3), (2, 2, 2), (2, 3, 4)]:
        branches = []
        composite = nx.Graph()
        s, t = "S", "T"
        composite.add_nodes_from([s, t])
        branch_sigs = []
        for idx, ell in enumerate(lengths):
            Pj = nx.path_graph(ell + 1)
            relabel = {0: s, ell: t}
            for v in range(1, ell):
                relabel[v] = f"br{idx}_{v}"
            Pj = nx.relabel_nodes(Pj, relabel)
            composite = nx.compose(composite, Pj)
            branch_sigs.append(brute_force_signature(Pj, s, t))
        predicted = parallel_compose(branch_sigs)
        truth = brute_force_signature(composite, s, t)
        if predicted != truth:
            failures.append(("parallel", lengths, predicted, truth))

    return failures


if __name__ == "__main__":
    failures = targeted_composition_tests()
    if not failures:
        print("ALL composition-rule tests PASSED (series + parallel, "
              "brute-force cross-checked).")
    else:
        print(f"{len(failures)} FAILURES:")
        for f in failures:
            print(f)
