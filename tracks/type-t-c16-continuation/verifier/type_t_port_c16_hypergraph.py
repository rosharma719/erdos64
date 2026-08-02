#!/usr/bin/env python3
"""General bounded-``m`` dyadic-cycle conflict enumerator (C16 Phase 3).

**Status: superseded for practical use by the passage-level compilers**
(``type_t_port_c16_passage_hypergraph.py``, ``type_t_port_c16_passage_general.py``
-- see ``type_t_port_c16_passage_projection.md``). This module operates at
*gadget* granularity (one Boolean variable per triple/gadget *identity*),
which the passage-level projection later showed is 107-207x more clauses
than necessary for the same geometric information (many different
triples/gadgets can supply the same geometric passage). Its own diagnostic
run on the ``m=2`` stage alone -- 2,509,952 raw candidates,
1,503,692 candidate-minimal, ~37 minutes -- is recorded in
``type_t_port_c16_passage_projection.md`` Phase 0 as exactly the scale
measurement that motivated the passage-level pivot; it was never advanced
past that single stage in practice. Retained here (working code, tests
passing) as the historical/diagnostic implementation and because its
domination-pruning and hop-relation-oracle techniques were reused directly
in the passage-level general-``m`` compiler.

``type_t_port_c16_compilation.md`` Phase 1 proves that every dyadic-cycle
conflict alternates ``m`` hub passages with ``m`` positive-length bare-core
paths, that ``m=1`` is already excluded (for every dyadic length) by the
``allowed_triples``/``linked_gadgets`` local-safety screen, and that
``2 <= m <= floor(L/3)``.  ``type_t_port_short_conflicts.py`` implements the
``m=2`` case, which is *all* of C4 (vacuous) and C8 (``m=2`` forced).  For
C16 (``L=16``), ``m`` ranges over ``{2,3,4,5}``, and the ``m=2`` trick of
directly intersecting two independent reach-sets does not generalize: an
*intermediate* passage's landing vertex is unconstrained by "must reach the
start" (only the *last* segment has that constraint), so a naive recursive
search would, at every intermediate landing vertex, need to try every
passage *starting there* -- and some core vertices start 1000+ candidate
passages (measured on the smallest instance below), which is intractable to
do inside multi-level recursion.

The fix implemented here avoids that blowup with two ideas:

1. **Endpoint collapsing.** A vertex's *raw* passage list can be huge because
   many different Boolean variables (triples/gadgets) can realize the *same*
   ``(endpoint, route)`` pair (measured up to ~1500 raw passages at a single
   vertex on the smallest instance, but only ~70 *distinct* ``(endpoint,
   route)`` pairs -- an over 20x collapse).  All of the search's vertex-level
   reachability logic (``build_endpoint_sets``, ``build_hop_relations``)
   works on this deduplicated ``(vertex, route)`` relation; the *specific*
   Boolean-variable tags realizing a chosen ``(vertex, endpoint, route)`` hop
   are only looked up (via ``pair_index``, already built in
   ``type_t_port_short_conflicts.py``) once a hop is actually chosen -- never
   scanned to decide which hop to try next.

2. **A precomputed, composed ``k``-hop relation as a pruning oracle.**
   ``build_hop_relations`` computes, once, ``HOPK[k][v] = {length: set of w}``
   -- every vertex reachable from ``v`` via exactly ``k`` (passage then
   core-path) hops using exactly that much total length -- by *relation
   composition* (``HOPK[k] = HOPK[k-1] joined with HOPK[1]``), entirely in
   terms of the small deduplicated endpoint sets and the (already fast,
   sparse-core) ``reach`` index from ``type_t_port_short_conflicts.py``.
   This stays polynomial (seconds, not hours) because it only ever
   propagates *sets of vertices*, never enumerates paths.  The recursive
   search then uses ``HOPK[m - hops_placed - 1]`` as an admissibility oracle:
   after tentatively taking a hop to ``x_next``, it only recurses if
   ``x1 in HOPK[remaining_hops][x_next][remaining_budget]`` -- i.e. only if
   the *rest* of the cycle can possibly be completed at all.  This prunes
   every dead branch immediately, before it can fan out into another
   1000-wide passage list.

As in ``type_t_port_short_conflicts.py``, this is a sound, complete
*candidate generator*: the vertex/route-level reachability that drives the
search is proved (Phase 1) to contain every real conflict, but individual
raw candidates are not checked for full segment-disjointness during
generation.  Every surviving candidate support is independently
materialized and re-checked via ``edge_path_cycle`` (a differently
organized detector, reused unmodified) before being trusted; candidates that
fail are dropped as sound-but-spurious, exactly as in the ``m=2`` code.

**Cross-``m`` domination pruning.** A conflict clause naming a smaller
Boolean-variable support already subsumes (dominates) every superset of it,
so once a support is confirmed as a genuine, *verified* minimal conflict at
some ``m``, it is used to prune candidate generation at every larger ``m``
searched afterwards (``known_minimal`` in ``enumerate_m_conflicts``) --
this is sound because pruning only ever discards candidates already implied
by an established fact, and it is a large practical win because a very
common source of larger-``m`` cycles is one that happens to revisit an
already-known small poisoned pair.

**Honesty.** Full completeness for a given ``m`` requires the generation
pass to finish for every starting vertex *and* every surviving candidate to
be independently verified. Given how explosively the raw candidate volume
grows with ``m`` (measured below), that is not always achievable in a
bounded time budget; see ``compile_instance`` for exactly how partial runs
are reported (``x1 covered`` / ``x1 total``, `timed_out`, and an explicit
``COMPUTATIONALLY_CERTIFIED`` vs ``BOUNDED_INCOMPLETE`` status per length).
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import sys
import time
from collections import defaultdict
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, as_completed, wait
from itertools import combinations
from pathlib import Path

from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle, validate_literal_cycle
from type_t_port_multipole_sat import build_catalog
from type_t_port_short_conflicts import (
    build_pair_index,
    build_passages,
    compute_reach_index,
    materialize_variables,
    serialize_support,
)
VariableTag = tuple


# ---------------------------------------------------------------------------
# Vertex-level reachability structures (shared across every m).
# ---------------------------------------------------------------------------

def build_endpoint_sets(by_start: dict) -> dict[int, list[tuple[int, int]]]:
    """Collapse each vertex's raw passage list to distinct ``(endpoint,
    route)`` pairs.  This is the key size reduction that makes intermediate
    (non-closing) hops tractable: on the smallest C16 instance the busiest
    vertex has 1517 raw passages but only 71 distinct ``(endpoint, route)``
    pairs -- the search below only ever iterates this small collapsed set,
    never the raw per-tag list, at an intermediate hop."""
    endpoint_sets: dict[int, list[tuple[int, int]]] = {}
    for v, entries in by_start.items():
        endpoint_sets[v] = sorted({(y, route) for (y, route, _tag) in entries})
    return endpoint_sets


def build_hop_relations(endpoint_sets: dict, reach: list, max_len: int, max_k: int):
    """``HOPK[k][v] = {length: frozenset(w)}``: vertices reachable from ``v``
    via exactly ``k`` (passage-then-core-path) hops using exactly that total
    length, capped at ``max_len``.  ``HOPK[1]`` is built directly from
    ``endpoint_sets`` and ``reach``; ``HOPK[k]`` for ``k>1`` is the
    relational composition ``HOPK[k-1] . HOPK[1]``.  Every step only unions
    small vertex *sets*, so the cost stays polynomial in the (deduplicated,
    small) endpoint-set and reach-set sizes -- never proportional to a raw
    per-vertex passage count.  Returned as a list indexed ``1..max_k``
    (index 0 is unused/``None``)."""
    hop1: dict[int, dict[int, frozenset]] = {}
    for v, pairs in endpoint_sets.items():
        lengths: dict[int, set] = defaultdict(set)
        for y, route in pairs:
            for l, wset in reach[y].items():
                total = route + l
                if total <= max_len:
                    lengths[total].update(wset)
        if lengths:
            hop1[v] = {l: frozenset(w) for l, w in lengths.items()}

    hopk: list = [None, hop1]
    for _k in range(2, max_k + 1):
        prev = hopk[-1]
        current: dict[int, dict[int, frozenset]] = {}
        for v, lenmap in prev.items():
            acc: dict[int, set] = defaultdict(set)
            for len_a, mids in lenmap.items():
                if len_a >= max_len:
                    continue
                for mid in mids:
                    hop_b = hop1.get(mid)
                    if not hop_b:
                        continue
                    for len_b, ws in hop_b.items():
                        total = len_a + len_b
                        if total <= max_len:
                            acc[total].update(ws)
            if acc:
                current[v] = {l: frozenset(w) for l, w in acc.items()}
        hopk.append(current)
    return hopk


# ---------------------------------------------------------------------------
# The general-m search.
# ---------------------------------------------------------------------------

def enumerate_m_conflicts(core, endpoint_sets: dict, pair_index: dict, reach: list,
                          hopk: list, target_length: int, m: int,
                          known_minimal: dict[int, set] | None = None,
                          deadline: float | None = None,
                          x1_range=None) -> dict:
    """Stream-generate every candidate support realizing an ``m``-hub-passage
    cycle of exactly ``target_length``, alternating passages (looked up
    endpoint-set-first, tag-second) and core paths (looked up via the
    precomputed ``reach`` index), pruned at every intermediate hop by the
    ``hopk`` completion oracle.  ``known_minimal`` (a ``{size: set[frozenset
    support]}`` map of *already independently verified* minimal conflicts
    from smaller ``m``) is used to drop any candidate that is a superset of
    an established conflict -- sound because such a candidate is already
    forbidden by the smaller clause, so it would only ever be dropped again
    by ``minimal_supports`` even if fully verified.

    Returns a dict with the raw ``results`` (support tuple -> True) plus
    coverage bookkeeping (``x1_completed``, ``x1_total``, ``timed_out``) so
    that partial runs are honestly reportable.
    """
    results: dict[tuple, bool] = {}
    known_minimal = known_minimal or {}

    def dominated(key_set: frozenset) -> bool:
        for size in range(1, len(key_set)):
            pool = known_minimal.get(size)
            if not pool:
                continue
            for sub in combinations(key_set, size):
                if frozenset(sub) in pool:
                    return True
        return False

    rng = x1_range if x1_range is not None else range(core.order)
    x1_completed: list[int] = []
    timed_out = False

    for x1 in rng:
        if deadline is not None and time.time() > deadline:
            timed_out = True
            break
        chain: list[tuple] = []
        used = {x1}

        def close(current_v: int, length_used: int) -> None:
            remaining_budget = target_length - length_used
            for y, route in endpoint_sets.get(current_v, ()):
                if y in used:
                    continue
                l = remaining_budget - route
                if l < 1:
                    continue
                wset = reach[y].get(l)
                if not (wset and x1 in wset):
                    continue
                tags_last = pair_index.get((current_v, y, route))
                if not tags_last:
                    continue
                per_hop_tags = [entry[3] for entry in chain] + [tags_last]
                for combo in itertools.product(*per_hop_tags):
                    key = tuple(sorted(set(combo)))
                    if key in results:
                        continue
                    if dominated(frozenset(key)):
                        continue
                    results[key] = True

        def rec(current_v: int, hops_placed: int, length_used: int) -> None:
            remaining_hops = m - hops_placed
            if remaining_hops == 1:
                close(current_v, length_used)
                return
            remaining_budget = target_length - length_used
            min_rest = (remaining_hops - 1) * 3  # each further hop costs >=2 route +>=1 core path
            for y, route in endpoint_sets.get(current_v, ()):
                if y in used:
                    continue
                max_l = remaining_budget - route - min_rest
                if max_l < 1:
                    continue
                reach_y = reach[y]
                for l in range(1, max_l + 1):
                    wset = reach_y.get(l)
                    if not wset:
                        continue
                    new_len = length_used + route + l
                    k_left = remaining_hops - 1
                    budget_left = target_length - new_len
                    for x_next in wset:
                        if x_next in used:
                            continue
                        reachable = hopk[k_left].get(x_next, {}).get(budget_left)
                        if not reachable or x1 not in reachable:
                            continue  # pruning oracle: no way to complete the cycle from here
                        tags = pair_index.get((current_v, y, route))
                        if not tags:
                            continue
                        chain.append((current_v, y, route, tags))
                        used.add(y)
                        used.add(x_next)
                        rec(x_next, hops_placed + 1, new_len)
                        used.discard(y)
                        used.discard(x_next)
                        chain.pop()

        rec(x1, 0, 0)
        x1_completed.append(x1)

    return {
        "results": results,
        "x1_completed": x1_completed,
        "x1_total": core.order,
        "timed_out": timed_out,
    }


def minimal_supports(results: dict) -> dict:
    """Drop any support that is a strict superset of another retained one,
    generalized to any support size (Phase 1 bounds support size at
    ``floor(L/3) <= 5`` for every length considered here).  For a size-``k``
    candidate this checks at most ``sum_{s=1}^{k-1} C(k,s)`` (<=30 for
    ``k=5``) subset memberships against a hash set indexed by size, so the
    whole pass is ``O(n)`` in the candidate count -- the ``O(n^2)`` pairwise
    scan a naive implementation would need is intractable once candidate
    counts reach the hundreds of thousands to millions seen here."""
    by_size: dict[int, set] = defaultdict(set)
    kept: dict[tuple, bool] = {}
    for key in sorted(results, key=len):
        key_set = frozenset(key)
        dominated = False
        for size in range(1, len(key_set)):
            pool = by_size.get(size)
            if not pool:
                continue
            for sub in combinations(key_set, size):
                if frozenset(sub) in pool:
                    dominated = True
                    break
            if dominated:
                break
        if dominated:
            continue
        kept[key] = results[key]
        by_size[len(key_set)].add(key_set)
    return kept


# ---------------------------------------------------------------------------
# Independent verification (parallel: this is the dominant cost at scale).
# ---------------------------------------------------------------------------

_worker_core = None


def _init_worker(j: int, a: int, c: int) -> None:
    global _worker_core
    _worker_core = build_core(j, a, c)


def _verify_chunk(args):
    target_length, supports = args
    out = []
    rejected = 0
    for support in supports:
        graph, adjacency = materialize_variables(_worker_core, support)
        witness = edge_path_cycle(adjacency, target_length)
        if witness is None:
            rejected += 1
            continue
        validate_literal_cycle(graph, list(witness))
        out.append((support, list(witness)))
    return out, rejected


def verify_conflicts(j: int, a: int, c: int, target_length: int, results: dict,
                     workers: int = 1, chunk_size: int = 2000,
                     deadline: float | None = None) -> tuple[dict, int, int]:
    """Independently verify every candidate support by materializing exactly
    those hubs and searching for the literal cycle with ``edge_path_cycle``
    (reused unmodified from the CEGAR checker, as in
    ``type_t_port_short_conflicts.verify_conflicts``) -- a differently
    organized detector than the reachability-index search that generated the
    candidates. Candidates that fail are dropped as sound-but-spurious, not
    raised as errors. Runs in a process pool (this call is the dominant cost
    at scale: ~3.7ms/candidate single-threaded on the smallest instance) with
    ``workers`` processes, each rebuilding the (picklable, deterministic)
    core once via an initializer rather than re-pickling it per task.

    If ``deadline`` (a ``time.time()`` timestamp) is given and is reached
    before every chunk has completed, outstanding chunks are abandoned and
    the unchecked candidate count is returned as the third element -- so a
    caller can honestly report ``BOUNDED_INCOMPLETE`` (verified-so-far, not
    ``UNSAT``/complete) rather than silently truncating the result.  Returns
    ``(verified, rejected_count, unchecked_count)``.
    """
    supports = list(results)
    if not supports:
        return {}, 0, 0
    chunks = [supports[i:i + chunk_size] for i in range(0, len(supports), chunk_size)]
    verified: dict[tuple, dict] = {}
    rejected_total = 0
    unchecked = 0
    if workers <= 1:
        _init_worker(j, a, c)
        for index, chunk in enumerate(chunks):
            if deadline is not None and time.time() > deadline:
                unchecked += sum(len(c) for c in chunks[index:])
                break
            found, rejected = _verify_chunk((target_length, chunk))
            rejected_total += rejected
            for support, witness in found:
                verified[support] = {"witness": witness}
        return verified, rejected_total, unchecked
    with ProcessPoolExecutor(max_workers=workers, initializer=_init_worker,
                             initargs=(j, a, c)) as pool:
        remaining = {pool.submit(_verify_chunk, (target_length, chunk)): chunk for chunk in chunks}
        while remaining:
            timeout = None if deadline is None else max(deadline - time.time(), 0.0)
            done, not_done = wait(remaining, timeout=timeout, return_when=FIRST_COMPLETED)
            for future in done:
                found, rejected = future.result()
                rejected_total += rejected
                for support, witness in found:
                    verified[support] = {"witness": witness}
                del remaining[future]
            if deadline is not None and time.time() > deadline and not_done:
                for future in not_done:
                    future.cancel()
                    unchecked += len(remaining.pop(future, ()))
                break
    return verified, rejected_total, unchecked


# ---------------------------------------------------------------------------
# Orchestration.
# ---------------------------------------------------------------------------

def compile_instance(j: int, a: int, c: int, target_length: int = 16,
                     m_values: tuple[int, ...] | None = None,
                     time_budget_seconds: float | dict[int, float] | None = None,
                     workers: int = 1) -> dict:
    """Run the staged C16 (or general dyadic-length) hypergraph search:
    ``m=2,3,...,floor(L/3)`` in increasing order, each stage pruned by every
    smaller stage's *verified* minimal conflicts (``known_minimal``).
    ``time_budget_seconds`` is ``None`` (unbounded), a single float applied
    to every stage, or a ``{m: seconds}`` dict for per-``m`` budgets; each
    stage's generation phase and verification phase each independently get
    the *full* budget (they are different, sequential costs, so this is not
    double counting wall-clock -- it bounds the worst case per phase).
    Returns a structured report with an honest per-``m`` and overall status
    (``COMPUTATIONALLY_CERTIFIED`` only if every stage finished generation
    for every vertex and every surviving candidate was verified;
    ``BOUNDED_INCOMPLETE`` otherwise, with the exact vertex coverage and
    unchecked-candidate counts reported so the gap is reproducible, never
    silently rounded up to "complete" or treated as ``UNSAT``).
    """
    core = build_core(j, a, c)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    by_start = build_passages(triples, gadgets)
    pair_index = build_pair_index(triples, gadgets)
    endpoint_sets = build_endpoint_sets(by_start)
    core_adj = core.adjacency()

    max_m = max(m_values) if m_values else target_length // 3
    reach_cap = max(target_length - 4, 1)
    reach = compute_reach_index(core_adj, reach_cap)
    hopk = build_hop_relations(endpoint_sets, reach, target_length, max(max_m - 1, 1))

    m_range = m_values if m_values else tuple(range(2, target_length // 3 + 1))

    known_minimal: dict[int, set] = defaultdict(set)
    per_m: dict[str, dict] = {}
    all_complete = True

    for m in m_range:
        if isinstance(time_budget_seconds, dict):
            budget = time_budget_seconds.get(m)
        else:
            budget = time_budget_seconds

        gen_start = time.time()
        gen_deadline = (gen_start + budget) if budget else None
        gen = enumerate_m_conflicts(
            core, endpoint_sets, pair_index, reach, hopk, target_length, m,
            known_minimal=known_minimal, deadline=gen_deadline,
        )
        gen_time = time.time() - gen_start
        raw = gen["results"]
        raw_minimal = minimal_supports(raw)

        verify_start = time.time()
        verify_deadline = (verify_start + budget) if budget else None
        verified, rejected, unchecked = verify_conflicts(
            j, a, c, target_length, raw_minimal, workers=workers, deadline=verify_deadline,
        )
        verify_time = time.time() - verify_start
        minimal = minimal_supports(verified)

        stage_complete = (not gen["timed_out"]) and unchecked == 0
        all_complete = all_complete and stage_complete

        for support in minimal:
            known_minimal[len(support)].add(frozenset(support))

        per_m[str(m)] = {
            "hub_passages": m,
            "generation_timed_out": gen["timed_out"],
            "x1_completed": len(gen["x1_completed"]),
            "x1_total": gen["x1_total"],
            "generation_seconds": gen_time,
            "verification_seconds": verify_time,
            "raw_candidate_supports": len(raw),
            "candidate_minimal_supports": len(raw_minimal),
            "verification_rejected": rejected,
            "verification_unchecked": unchecked,
            "verified_minimal_supports": len(minimal),
            "support_size_distribution": {
                str(size): sum(1 for key in minimal if len(key) == size)
                for size in sorted({len(key) for key in minimal})
            } if minimal else {},
            "status": "COMPLETE" if stage_complete else "BOUNDED_INCOMPLETE",
            "conflicts": [
                {
                    "support": serialize_support(support),
                    "witness": minimal[support]["witness"],
                }
                for support in sorted(minimal, key=lambda k: (len(k), k))
            ],
        }

    return {
        "status": "COMPUTATIONALLY_CERTIFIED" if all_complete else "BOUNDED_INCOMPLETE",
        "parameters": {"j": j, "Y": 1 << j, "a": a, "c": c},
        "catalog_sizes": {"triples": len(triples), "gadgets": len(gadgets)},
        "target_length": target_length,
        "hub_passage_values_attempted": list(m_range),
        "per_m": per_m,
        "combined_verified_minimal_supports": sum(
            len(known_minimal[size]) for size in known_minimal
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--target-length", type=int, default=16)
    parser.add_argument("--m-values", type=int, nargs="+", default=None)
    parser.add_argument("--time-budget-seconds", type=float, default=None,
                        help="per-hub-passage-count wall-clock budget; omit for unbounded")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compile_instance(
        args.j, args.a, args.c, args.target_length,
        tuple(args.m_values) if args.m_values else None,
        args.time_budget_seconds, args.workers,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.suffix == ".gz":
            args.output.write_bytes(gzip.compress(rendered.encode(), mtime=0))
        else:
            args.output.write_text(rendered)
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
