"""
Vine-graph cycle-spectrum experiment (Erdos #64 redirection, 2026-07-25).

Builds "vine graphs": a forward Hamiltonian path x0-x1-...-x_{n-1} plus a set
of extra chords ("the vine") chosen so every vertex reaches degree >=3 (the
sparsest / max-D choice is a near-perfect-matching of the path's degree-2/1
slots, landing exactly on a cubic graph, D = n/2-2, the S3b-extremal case).
We then also generate variants with a few EXTRA chords added on top of the
minimal vine (raising some vertices to degree 4, lowering D below the cubic
extremal value) to get graphs at several different D for the same n.

For every resulting simple, connected, delta>=3 graph we record:
  - n, m, D = 2n-2-m
  - the full dyadic cycle spectrum (present / missing lengths in {4,8,...})
  - #missing dyadic lengths

and test the candidate charging lemma

    V1: "a vine graph with D defects has at most D missing dyadic cycle
         lengths among {4,8,...,<=n}."

reporting PROVED-ON-SAMPLE / DISPROVED with the smallest witness found.
This is exploratory (small n only); see defect.md S6 and lemmas.md for the
recorded verdict.
"""
from __future__ import annotations
import itertools
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cycle_detect import from_edges, min_degree, powers_of_two_up_to, has_cycle_len_dfs, Graph


def minimal_vine_edges(n: int, seed: int = 0) -> list[tuple[int, int]] | None:
    """Path 0..n-1 plus a randomized-greedy minimal chord set bringing every
    vertex to degree >=3. Returns None if the greedy construction fails
    (retry with a different seed)."""
    rng = random.Random(seed)
    deg = [0] * n
    edges = set()

    def add(a, b):
        if a == b or (a, b) in edges or (b, a) in edges:
            return False
        edges.add((min(a, b), max(a, b)))
        deg[a] += 1
        deg[b] += 1
        return True

    for i in range(n - 1):
        add(i, i + 1)

    # repeatedly connect two distinct vertices that are both still below 3,
    # preferring vertices far apart on the path (keeps it "vine"-like, not a
    # dense clump); fall back to any valid pair.
    for _ in range(10 * n):
        need = [v for v in range(n) if deg[v] < 3]
        if not need:
            break
        rng.shuffle(need)
        placed = False
        for a, b in itertools.combinations(need, 2):
            if add(a, b):
                placed = True
                break
        if not placed:
            return None
    if any(d < 3 for d in deg):
        return None
    return sorted(edges)


def add_excess_chords(edges: list[tuple[int, int]], n: int, k: int, seed: int) -> list[tuple[int, int]] | None:
    """Add k extra chords between existing degree>=3 vertices (raising them
    to degree 4+, lowering D) without creating multi-edges."""
    rng = random.Random(seed + 9999)
    edges = set(edges)
    verts = list(range(n))
    added = 0
    attempts = 0
    while added < k and attempts < 200:
        attempts += 1
        a, b = rng.sample(verts, 2)
        if a == b or (min(a, b), max(a, b)) in edges:
            continue
        edges.add((min(a, b), max(a, b)))
        added += 1
    if added < k:
        return None
    return sorted(edges)


def analyze(n: int, edges: list[tuple[int, int]]) -> dict:
    g = from_edges(n, edges)
    m = len(edges)
    D = 2 * n - 2 - m
    spectrum = {L: has_cycle_len_dfs(g, L) for L in powers_of_two_up_to(n)}
    missing = [L for L, present in spectrum.items() if not present]
    return dict(n=n, m=m, D=D, mindeg=min_degree(g), missing=missing,
                num_missing=len(missing), edges=edges)


def main():
    results = []
    violations = []
    for n in range(9, 22):
        for base_seed in range(6):
            base = minimal_vine_edges(n, seed=base_seed)
            if base is None:
                continue
            for k in range(0, 4):
                variant = base if k == 0 else add_excess_chords(base, n, k, seed=base_seed * 100 + k)
                if variant is None:
                    continue
                st = analyze(n, variant)
                if st["mindeg"] < 3:
                    continue
                results.append(st)
                if st["num_missing"] > st["D"]:
                    violations.append(st)

    print(f"generated {len(results)} vine-graph instances, n=9..21, "
          f"D varied via 0-3 excess chords on top of a minimal (cubic-ish) vine")
    print(f"V1 candidate ('#missing dyadic lengths <= D'): "
          f"{'HOLDS on every instance' if not violations else f'{len(violations)} VIOLATIONS'}")
    if violations:
        v = min(violations, key=lambda s: s["n"])
        print(f"smallest witness: n={v['n']} m={v['m']} D={v['D']} "
              f"missing={v['missing']} (#missing={v['num_missing']} > D={v['D']})")
        print(f"edges: {v['edges']}")
    # also report the D-vs-missing distribution for the report
    from collections import defaultdict
    by_D = defaultdict(list)
    for r in results:
        by_D[r["D"]].append(r["num_missing"])
    print("\nD -> [min,max] #missing dyadic lengths observed:")
    for D in sorted(by_D):
        vals = by_D[D]
        print(f"  D={D}: n(instances)={len(vals)}  missing in [{min(vals)},{max(vals)}]")


if __name__ == "__main__":
    main()
