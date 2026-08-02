#!/usr/bin/env python3
"""Exact-incremental 2/3/4-switch search for Type-T port cores."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import defaultdict

from type_t_port_core_export import build_core
from type_t_port_matching_sat import (
    enumerate_cycles_exact,
    one_edge_incompatibilities,
    powers_up_to,
)


def edge(u, v):
    return (u, v) if u < v else (v, u)


def cycle_edges(cycle):
    return frozenset(edge(cycle[i], cycle[(i + 1) % len(cycle)])
                     for i in range(len(cycle)))


def canonical_cycle(path):
    # path has each cycle vertex exactly once.
    n = len(path)
    k = min(range(n), key=path.__getitem__)
    forward = tuple(path[(k + i) % n] for i in range(n))
    reverse = tuple(path[(k - i) % n] for i in range(n))
    return min(forward, reverse)


def cycles_through_edge(adjacency, uv, length):
    """All simple exact-length cycles using uv, after uv is present."""
    u, v = uv
    result = set()
    path = [u]
    used = {u}

    def visit(x, depth):
        if depth == length - 1:
            if x == v:
                result.add(canonical_cycle(path))
            return
        for y in adjacency[x]:
            if edge(x, y) == uv or y in used:
                continue
            # v must be the final endpoint.
            if y == v and depth + 1 != length - 1:
                continue
            used.add(y)
            path.append(y)
            visit(y, depth + 1)
            path.pop()
            used.remove(y)

    visit(u, 0)
    return result


def full_cycles(adjacency, length):
    cycles, truncated = enumerate_cycles_exact(
        tuple(frozenset(row) for row in adjacency), length, 10_000_000
    )
    assert not truncated
    return {canonical_cycle(list(cycle)) for cycle in cycles}


def update_cycles(cycles, adjacency, removed, added, length):
    kept = {cy for cy in cycles if cycle_edges(cy).isdisjoint(removed)}
    for uv in added:
        kept.update(cycles_through_edge(adjacency, uv, length))
    return kept


def random_allowed_matching(vertices, allowed, rng):
    # Dense compatibility graph: randomized greedy plus small restart suffices.
    for _ in range(10000):
        unmatched = set(vertices)
        result = []
        while unmatched:
            u = min(unmatched, key=lambda x: sum(edge(x, y) in allowed for y in unmatched if y != x))
            options = [v for v in unmatched if v != u and edge(u, v) in allowed]
            if not options:
                break
            v = rng.choice(options)
            unmatched.remove(u)
            unmatched.remove(v)
            result.append(edge(u, v))
        if not unmatched:
            return result
    raise RuntimeError("could not seed allowed matching")


def random_repair(endpoints, allowed, rng, old_edges):
    # Return a random perfect matching of the selected endpoints, preferably changed.
    endpoints = tuple(endpoints)
    for _ in range(200):
        pool = list(endpoints)
        rng.shuffle(pool)
        pairs = []
        okay = True
        while pool:
            u = pool.pop()
            options = [i for i, v in enumerate(pool) if edge(u, v) in allowed]
            if not options:
                okay = False
                break
            i = rng.choice(options)
            v = pool.pop(i)
            pairs.append(edge(u, v))
        if okay and set(pairs) != set(old_edges):
            return pairs
    return None


def search(j, a, c, seed, steps, audit_every, long_witnesses=True,
           stop_after_clean=False):
    rng = random.Random(seed)
    core = build_core(j, a, c)
    vertices = core.deficient_vertices()
    bad = one_edge_incompatibilities(core, powers_up_to(core.order))
    core_edges = set(core.edges)
    allowed = {
        edge(u, v)
        for i, u in enumerate(vertices) for v in vertices[i + 1:]
        if edge(u, v) not in core_edges and edge(u, v) not in bad
    }
    matching = random_allowed_matching(vertices, allowed, rng)
    adjacency = [set(row) for row in core.adjacency()]
    for u, v in matching:
        adjacency[u].add(v)
        adjacency[v].add(u)

    cycles = {4: full_cycles(adjacency, 4), 8: full_cycles(adjacency, 8)}
    cycles16_initialized = False
    best = None
    best_iteration = None
    accepted = 0
    tabu = {}
    start = time.monotonic()

    def state_score(csets):
        return (len(csets[4]), len(csets[8]), len(csets.get(16, ())))

    for iteration in range(steps):
        current_score = state_score(cycles)
        if current_score[:2] == (0, 0) and not cycles16_initialized:
            cycles[16] = full_cycles(adjacency, 16)
            cycles16_initialized = True
            current_score = state_score(cycles)
            best = (current_score, sorted(matching))
            best_iteration = iteration
            if stop_after_clean:
                break

        # Bias one chosen matching edge toward a shortest bad cycle.
        if cycles[4]:
            target = rng.choice(tuple(cycles[4]))
        elif cycles[8]:
            target = rng.choice(tuple(cycles[8]))
        elif cycles16_initialized and cycles[16]:
            target = rng.choice(tuple(cycles[16]))
        else:
            target = None
        index = {uv: i for i, uv in enumerate(matching)}
        implicated = []
        if target:
            implicated = [index[uv] for uv in cycle_edges(target) if uv in index]

        p = rng.random()
        k = 2 if p < 0.62 else (3 if p < 0.88 else 4)
        selected = set()
        if implicated:
            selected.add(rng.choice(implicated))
        while len(selected) < k:
            selected.add(rng.randrange(len(matching)))
        selected = sorted(selected)
        removed = [matching[i] for i in selected]
        endpoints = [v for uv in removed for v in uv]
        added = random_repair(endpoints, allowed, rng, removed)
        if added is None:
            continue
        removed_set = set(removed)
        added_set = set(added)
        signature = tuple(sorted(added_set))
        if tabu.get(signature, -1) > iteration:
            continue

        for u, v in removed:
            adjacency[u].remove(v); adjacency[v].remove(u)
        for u, v in added:
            adjacency[u].add(v); adjacency[v].add(u)

        proposed = {}
        proposed[4] = update_cycles(cycles[4], adjacency, removed_set, added_set, 4)
        # Once a lexicographic level is zero, never regress it.
        reject = not cycles[4] and bool(proposed[4])
        if not reject:
            proposed[8] = update_cycles(cycles[8], adjacency, removed_set, added_set, 8)
            reject = not cycles[8] and bool(proposed[8])
        if not reject and cycles16_initialized:
            proposed[16] = update_cycles(cycles[16], adjacency, removed_set, added_set, 16)

        if reject:
            accept = False
        else:
            new_score = state_score(proposed)
            # Lexicographic scalar only while reaching short-cycle freedom.
            if current_score[0] or current_score[1]:
                old_value = current_score[0] * 1_000_000 + current_score[1] * 10_000
                new_value = new_score[0] * 1_000_000 + new_score[1] * 10_000
                temperature = max(200.0, 20000.0 * (1 - iteration / max(1, steps)))
            else:
                old_value, new_value = current_score[2], new_score[2]
                temperature = max(0.2, 35.0 * (1 - iteration / max(1, steps)))
            accept = new_value <= old_value or rng.random() < math.exp((old_value - new_value) / temperature)

        if accept:
            for offset, i in enumerate(selected):
                matching[i] = added[offset]
            cycles.update(proposed)
            accepted += 1
            for uv in removed:
                tabu[uv] = iteration + 19
            score = state_score(cycles)
            if score[:2] == (0, 0) and (best is None or score < best[0]):
                best = (score, sorted(matching))
                best_iteration = iteration
        else:
            for u, v in added:
                adjacency[u].remove(v); adjacency[v].remove(u)
            for u, v in removed:
                adjacency[u].add(v); adjacency[v].add(u)

        if audit_every and iteration and iteration % audit_every == 0:
            for length in (4, 8) + ((16,) if cycles16_initialized else ()):
                assert cycles[length] == full_cycles(adjacency, length), (iteration, length)

    if best is None:
        best = (state_score(cycles), sorted(matching))
        best_iteration = steps
    best_score, best_matching = best
    best_adjacency = [set(row) for row in core.adjacency()]
    for u, v in best_matching:
        best_adjacency[u].add(v); best_adjacency[v].add(u)
    exact = {}
    witnesses = {}
    participating = set()
    matching_set = set(best_matching)
    for length in (4, 8, 16):
        found = full_cycles(best_adjacency, length)
        exact[str(length)] = len(found)
        for cy in found:
            participating.update(cycle_edges(cy) & matching_set)
        if found:
            witnesses[str(length)] = list(min(found))
    # Long-cycle enumeration is witness-only: exact counts are infeasible here.
    frozen = tuple(frozenset(row) for row in best_adjacency)
    if long_witnesses:
        for length in (32, 64, 128):
            found, _ = enumerate_cycles_exact(frozen, length, 1)
            if found:
                witnesses[str(length)] = list(found[0])
                participating.update(cycle_edges(found[0]) & matching_set)
    return {
        "parameters": {"j": j, "a": a, "c": c},
        "seed": seed,
        "steps": steps,
        "accepted": accepted,
        "elapsed_seconds": time.monotonic() - start,
        "best_iteration": best_iteration,
        "exact_short_profile": exact,
        "long_profile": "witness-only, counts not computed",
        "power_cycle_witnesses": witnesses,
        "matching_edges_participating_in_exact_C16_or_long_witnesses": len(participating),
        "matching_edges": [list(uv) for uv in best_matching],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--j', type=int, default=5)
    ap.add_argument('--a', type=int, required=True)
    ap.add_argument('--c', type=int, required=True)
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--steps', type=int, default=2000)
    ap.add_argument('--audit-every', type=int, default=0)
    ap.add_argument('--no-long-witnesses', action='store_true')
    ap.add_argument('--stop-after-clean', action='store_true')
    ap.add_argument('--output', required=True)
    ns = ap.parse_args()
    result = search(ns.j, ns.a, ns.c, ns.seed, ns.steps, ns.audit_every,
                    not ns.no_long_witnesses, ns.stop_after_clean)
    with open(ns.output, 'w') as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps({k: result[k] for k in ('parameters','seed','steps','accepted','elapsed_seconds','best_iteration','exact_short_profile','matching_edges_participating_in_exact_C16_or_long_witnesses')}))


if __name__ == '__main__':
    main()
