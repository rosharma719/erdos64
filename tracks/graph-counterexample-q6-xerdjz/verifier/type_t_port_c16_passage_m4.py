#!/usr/bin/env python3
"""Specialized ``m=4`` C16 passage-level compiler.

Phase 1 (``type_t_port_c16_compilation.md``) proves ``2 <= m <= floor(L/3)``;
for ``L=16`` this allows ``m`` up to ``5``.  ``m=2,3`` were compiled by the
oracle-pruned general search (``type_t_port_c16_passage_general.py``) and
``m=5`` by the tight specialized compiler
(``type_t_port_c16_passage_m5.py``).  This module closes the remaining
``m=4`` layer.

**Why ``m=4`` needs its own compiler rather than either neighbour.**
The ``(m,r,v)`` identity gives ``route_total = 2*(m-b) + 3*b = m + (m + b)``
with ``b`` the number of ``p3`` passages, and ``b <= 1`` always
(``type_t_port_passages.drop_multi_p3_supports``).  For ``m=4``:

* ``b=0``: ``route_total = 8``, so ``core_total = 8`` split into **four**
  positive parts -- partitions ``{5,1,1,1}``, ``{4,2,1,1}``, ``{3,3,1,1}``,
  ``{3,2,2,1}``, ``{2,2,2,2}``.
* ``b=1``: ``route_total = 9``, so ``core_total = 7`` into four positive
  parts -- ``{4,1,1,1}``, ``{3,2,1,1}``, ``{2,2,2,1}``.

So unlike ``m=5`` (where the only partitions are ``{2,1,1,1,1}`` and
``{1,1,1,1,1}``, i.e. core segments of length 1 or 2 only), ``m=4`` genuinely
needs *simple* bare-core paths of every length up to **5**.  The ``m=5``
compiler's hard-coded ``core_adj``/``paths2`` pair therefore does not
generalize; this module replaces it with a precomputed table of every simple
core path of length ``1..5`` (only 1,554 directed paths on the ``(4,55,7)``
core, which has 76 vertices of degree 2, 10 of degree 3 and one of degree 4),
carrying each path's *internal* vertex bitmask so the DFS can enforce
whole-cycle vertex simplicity, not just endpoint distinctness.

Conversely the general ``enumerate_m_conflicts`` route is unattractive here
for the same reason it was at ``m=5``: it re-derives every ``m<4`` conflict
in the same pass, and -- decisively -- its downstream verification uses the
generic ``materialize_passages + edge_path_cycle`` checker, which costs
~2 ms per candidate (896 s for the 417,864 ``m=3`` candidates).  At ``m=4``'s
scale that verification alone runs into hours.  This module reuses the
``m=5`` answer to that: an exhaustive *support-local* alternating
reconstruction that builds the literal 16-vertex witness directly, with the
generic checker retained as an independent cross-check on an evenly spaced
sample.

Every claim this module emits is machine-checked: generation covers all 87
canonical start vertices with no time budget, every surviving support is
individually reconstructed into a literal simple 16-cycle, an evenly spaced
sample is re-verified through the structurally different generic checker, and
an unpruned re-run over a subset of start vertices cross-validates the
lower-shadow pruning itself (``--shadow-audit-starts``).
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import multiprocessing
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from type_t_port_core_export import build_core
from type_t_port_multipole_sat import build_catalog
from type_t_port_passages import build_passage_catalog
from type_t_port_c16_passage_general import verify_conflicts as verify_conflicts_generic

TARGET = 16
M = 4
#: ``b=0`` gives ``core_total=8`` over four positive parts, so no single core
#: segment can exceed ``8 - 3 = 5``.
MAX_CORE_SEGMENT = TARGET - 2 * M - (M - 1)


def core_path_table(core_adj, max_length: int = MAX_CORE_SEGMENT):
    """Every simple core path of length ``1..max_length``, by start vertex.

    Returns ``paths[v] -> tuple[(length, end, interior_mask, sequence)]``
    where ``interior_mask`` is the bitmask of the path's *interior* vertices
    (neither endpoint is in the mask) and ``sequence`` is the explicit vertex
    list.  The generator ANDs the mask against its running used-vertex mask,
    which is what makes whole-cycle simplicity -- not merely endpoint
    distinctness -- checkable in one integer operation; the verifier uses the
    explicit sequence to materialize a literal witness.

    The table is small: on the ``(4,55,7)`` core (order 87, degrees
    76x2 + 10x3 + 1x4) there are 1,554 directed simple paths of length <= 5
    in total, so precomputing it costs nothing and removes all core-side
    branching from the hot DFS.
    """
    order = len(core_adj)
    paths: list[list[tuple[int, int, int, tuple[int, ...]]]] = [[] for _ in range(order)]

    def walk(start: int, vertex: int, length: int, interior: int, used: int,
             acc: list[int]) -> None:
        if length == max_length:
            return
        for neighbor in core_adj[vertex]:
            bit = 1 << neighbor
            if used & bit:
                continue
            acc.append(neighbor)
            paths[start].append((length + 1, neighbor, interior, tuple(acc)))
            walk(start, neighbor, length + 1, interior | bit, used | bit, acc)
            acc.pop()

    for start in range(order):
        walk(start, start, 0, 0, 1 << start, [start])
        paths[start].sort()
    return [tuple(row) for row in paths]


def enumerate_m4_c16_conflicts(core, p2, p3, time_budget_seconds: float | None = None,
                               lower_shadow: dict[int, set[frozenset]] | None = None,
                               start_vertices: list[int] | None = None,
                               use_lower_shadow: bool = True) -> dict:
    """Exact ``m=4`` search for ``target_length=16`` passage conflicts.

    A single DFS covers both compositions (``b=0``: four ``p2`` passages and
    core segments summing to 8; ``b=1``: three ``p2`` plus one ``p3`` and core
    segments summing to 7) and every assignment of which position carries
    which segment length, by carrying the running route/core totals and
    letting the arithmetic prune: with ``k`` passages still to place, the
    partial state needs ``route_used + core_used + 3*k <= 16`` (each remaining
    passage contributes route ``>=2`` and core ``>=1``).

    Canonicalization matches the ``m=5`` compiler: each alternating cycle is
    generated exactly once, from its numerically least *passage endpoint*
    (``x1``), with the first step of the walk always the passage at ``x1``.
    Interior core vertices are exempt from the ``>= x1`` restriction (they are
    not passage endpoints and cannot serve as a start).
    """
    core_adj = tuple(tuple(sorted(row)) for row in core.adjacency())
    order = core.order
    paths = core_path_table(core_adj)

    tags = sorted([("p2", key) for key in p2] + [("p3", key) for key in p3])
    tag_to_id = {tag: index for index, tag in enumerate(tags)}
    passage_options: list[list[tuple[int, int, int, bool]]] = [list() for _ in range(order)]
    for tag_id, (kind, (u, v)) in enumerate(tags):
        route = 2 if kind == "p2" else 3
        is_p3 = kind == "p3"
        passage_options[u].append((tag_id, v, route, is_p3))
        passage_options[v].append((tag_id, u, route, is_p3))
    for options in passage_options:
        options.sort()
    has_passage = [bool(options) for options in passage_options]

    # Only core steps landing on a passage endpoint can continue the walk;
    # dropping the rest here removes a dead branch per hop.
    open_steps = [
        tuple((length, end, interior)
              for length, end, interior, _sequence in paths[v] if has_passage[end])
        for v in range(order)
    ]
    # Closing steps are indexed by (from, to) so the last hop is a direct
    # lookup on the required exact length rather than a scan.
    close_steps: list[dict[int, tuple[tuple[int, int], ...]]] = []
    for v in range(order):
        by_end: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for length, end, interior, _sequence in paths[v]:
            by_end[end].append((length, interior))
        close_steps.append({end: tuple(items) for end, items in by_end.items()})

    lower_ids: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    if use_lower_shadow:
        for size, supports in (lower_shadow or {}).items():
            for support in supports:
                try:
                    encoded = tuple(sorted(tag_to_id[tag] for tag in support))
                except KeyError as error:
                    raise AssertionError(
                        f"lower-shadow passage absent from current catalog: {error}"
                    ) from error
                lower_ids[size].add(encoded)
    tag_count = len(tags)
    pair_forbidden = [0] * tag_count
    for first, second in lower_ids.pop(2, ()):
        pair_forbidden[first] |= 1 << second
        pair_forbidden[second] |= 1 << first
    triple_forbidden = [0] * (tag_count * tag_count)
    for first, second, third in lower_ids.pop(3, ()):
        triple_forbidden[first * tag_count + second] |= 1 << third
        triple_forbidden[first * tag_count + third] |= 1 << second
        triple_forbidden[second * tag_count + third] |= 1 << first
    known_singletons = {item[0] for item in lower_ids.pop(1, ())}

    def extends_large_shadow(chain_ids: list[int], tag_id: int) -> bool:
        # Only reachable if a shadow of size >=4 is supplied; the C8/m2/m3
        # seed has sizes 2 and 3 only, so this is dead code for the intended
        # run and is kept solely so an enlarged shadow cannot be silently
        # ignored.
        for size, known in lower_ids.items():
            if size > len(chain_ids) + 1:
                continue
            for part in itertools.combinations(chain_ids, size - 1):
                if tuple(sorted((*part, tag_id))) in known:
                    return True
        return False

    result_ids: set[tuple[int, ...]] = set()
    started = time.monotonic()
    truncated = False
    shadow_pruned = 0
    x1_completed = 0
    start_vertices = list(range(order)) if start_vertices is None else list(start_vertices)

    for x1 in start_vertices:
        if truncated:
            break
        chain: list[int] = []

        def rec(current_v: int, hop: int, route_used: int, core_used: int,
                p3_used: bool, used_mask: int, selected_ids: int,
                triple_blocked: int) -> None:
            nonlocal truncated, shadow_pruned
            if time_budget_seconds is not None and time.monotonic() - started > time_budget_seconds:
                truncated = True
                return
            remaining_after = M - hop - 1  # passages still to place after this one
            for tag_id, y, route, is_p3 in passage_options[current_v]:
                y_bit = 1 << y
                # Canonical rotation: every passage endpoint of the cycle is
                # >= x1, and the walk always leaves x1 through its passage.
                if used_mask & y_bit or y < x1:
                    continue
                if is_p3 and p3_used:
                    continue
                tag_bit = 1 << tag_id
                if (tag_id in known_singletons
                        or pair_forbidden[tag_id] & selected_ids
                        or triple_blocked & tag_bit
                        or (lower_ids and extends_large_shadow(chain, tag_id))):
                    shadow_pruned += 1
                    continue
                new_route = route_used + route
                # Each remaining passage needs route >=2 and core >=1; the
                # current hop still needs core >=1.
                if new_route + core_used + 1 + 3 * remaining_after > TARGET:
                    continue
                passage_used = used_mask | y_bit
                if remaining_after == 0:
                    needed = TARGET - new_route - core_used
                    if needed < 1 or needed > MAX_CORE_SEGMENT:
                        continue
                    for length, interior in close_steps[y].get(x1, ()):
                        if length == needed and not passage_used & interior:
                            result_ids.add(tuple(sorted((*chain, tag_id))))
                            break
                    continue
                new_p3_used = p3_used or is_p3
                chain.append(tag_id)
                next_selected_ids = selected_ids | tag_bit
                next_triple_blocked = triple_blocked
                for old_id in chain[:-1]:
                    lo, hi = (old_id, tag_id) if old_id < tag_id else (tag_id, old_id)
                    next_triple_blocked |= triple_forbidden[lo * tag_count + hi]
                budget = TARGET - new_route - core_used - 3 * remaining_after
                for length, x_next, interior in open_steps[y]:
                    if length > budget:
                        break  # open_steps is sorted by length
                    next_bit = 1 << x_next
                    if x_next < x1 or passage_used & (next_bit | interior):
                        continue
                    rec(x_next, hop + 1, new_route, core_used + length,
                        new_p3_used, passage_used | next_bit | interior,
                        next_selected_ids, next_triple_blocked)
                    if truncated:
                        break
                chain.pop()
                if truncated:
                    return

        rec(x1, 0, 0, 0, False, 1 << x1, 0, 0)
        if not truncated:
            x1_completed += 1

    results = {
        tuple(tags[tag_id] for tag_id in support): True
        for support in result_ids
    }
    return {
        "results": results,
        "truncated": truncated,
        "elapsed_seconds": time.monotonic() - started,
        "lower_shadow_pruned_branches": shadow_pruned,
        "x1_completed": x1_completed,
        "x1_total": len(start_vertices),
    }


_enumeration_worker_args = None


def _init_enumeration_worker(core, p2, p3, lower_shadow) -> None:
    global _enumeration_worker_args
    _enumeration_worker_args = (core, p2, p3, lower_shadow)


def _enumerate_start_chunk(start_vertices: list[int]) -> dict:
    core, p2, p3, lower_shadow = _enumeration_worker_args
    return enumerate_m4_c16_conflicts(
        core, p2, p3, lower_shadow=lower_shadow, start_vertices=start_vertices
    )


def enumerate_m4_parallel(core, p2, p3, lower_shadow, workers: int) -> dict:
    workers = max(1, min(workers, core.order))
    if workers == 1:
        return enumerate_m4_c16_conflicts(core, p2, p3, lower_shadow=lower_shadow)
    chunks = [list(range(core.order))[index::workers] for index in range(workers)]
    started = time.monotonic()
    results: dict = {}
    completed = 0
    pruned = 0
    context = multiprocessing.get_context("fork")
    with ProcessPoolExecutor(
        max_workers=workers,
        mp_context=context,
        initializer=_init_enumeration_worker,
        initargs=(core, p2, p3, lower_shadow),
    ) as pool:
        for partial in pool.map(_enumerate_start_chunk, chunks):
            results.update(partial["results"])
            completed += partial["x1_completed"]
            pruned += partial["lower_shadow_pruned_branches"]
    return {
        "results": results,
        "truncated": False,
        "elapsed_seconds": time.monotonic() - started,
        "lower_shadow_pruned_branches": pruned,
        "x1_completed": completed,
        "x1_total": core.order,
    }


def serialize_support(support: tuple) -> list:
    return [[kind, list(key)] for kind, key in support]


def verify_m4_support(core, support: tuple, core_adj=None, paths=None) -> list[int] | None:
    """Independently reconstruct the literal alternating 16-cycle for one
    ``m=4`` support.

    Unlike the generator (which walks the whole instance and discovers
    supports), this starts from a *fixed* four-passage support, is driven by
    the support's own endpoint pairing, and searches only for a compatible
    core matching.  It then materializes the literal cycle out of core edges
    and fresh hub vertices and checks that it has exactly 16 distinct
    vertices, which is what "``C16`` conflict" actually means.
    """
    if len(support) != 4:
        return None
    endpoints = [vertex for _kind, key in support for vertex in key]
    if len(set(endpoints)) != 8:
        return None
    p3_count = sum(kind == "p3" for kind, _key in support)
    if p3_count not in (0, 1):
        return None
    core_total = TARGET - (2 * (M - p3_count) + 3 * p3_count)

    mate: dict[int, int] = {}
    endpoint_tag: dict[int, tuple] = {}
    for tag in support:
        _kind, (u, v) = tag
        mate[u], mate[v] = v, u
        endpoint_tag[u] = endpoint_tag[v] = tag
    endpoint_set = frozenset(endpoints)
    endpoint_mask = 0
    for vertex in endpoint_set:
        endpoint_mask |= 1 << vertex
    core_adj = core_adj or tuple(tuple(sorted(row)) for row in core.adjacency())
    paths = paths or core_path_table(core_adj)
    start = min(endpoint_set)
    pieces: list[tuple[int, tuple, int, tuple[int, ...]]] = []

    def rec(current: int, hop: int, used_mask: int, core_left: int):
        y = mate[current]
        y_bit = 1 << y
        if used_mask & y_bit:
            return None
        next_used = used_mask | y_bit
        tag = endpoint_tag[current]
        closing = hop == M - 1
        for length, end, interior, sequence in paths[y]:
            if closing:
                if end != start or length != core_left:
                    continue
            else:
                if end == start or end not in endpoint_set:
                    continue
                if length > core_left - (M - 1 - hop):
                    continue
                if next_used & (1 << end):
                    continue
            # A support endpoint already carries one passage edge and one
            # core edge in the cycle, so it can never also be interior to a
            # core segment (that would make its degree 3).
            if next_used & interior or endpoint_mask & interior:
                continue
            pieces.append((current, tag, y, sequence))
            if closing:
                return list(pieces)
            found = rec(end, hop + 1, next_used | (1 << end) | interior, core_left - length)
            if found is not None:
                return found
            pieces.pop()
        return None

    found = rec(start, 0, 1 << start, core_total)
    if found is None:
        return None

    passage_routes: dict[tuple, tuple[int, ...]] = {}
    next_vertex = core.order
    for tag in support:
        kind, (u, v) = tag
        if kind == "p2":
            passage_routes[tag] = (u, next_vertex, v)
            next_vertex += 1
        else:
            passage_routes[tag] = (u, next_vertex, next_vertex + 1, v)
            next_vertex += 2
    witness: list[int] = []
    for current, tag, y, core_path in found:
        route = passage_routes[tag]
        if route[0] != current:
            route = tuple(reversed(route))
        if not witness:
            witness.append(current)
        witness.extend(route[1:])
        witness.extend(core_path[1:])
    if witness[-1] == witness[0]:
        witness.pop()
    if len(witness) != TARGET or len(set(witness)) != TARGET:
        return None
    return witness


def verify_m4_conflicts_count(core, results) -> tuple[int, int]:
    accepted = rejected = 0
    core_adj = tuple(tuple(sorted(row)) for row in core.adjacency())
    paths = core_path_table(core_adj)
    for support in results:
        if verify_m4_support(core, support, core_adj, paths) is None:
            rejected += 1
        else:
            accepted += 1
    return accepted, rejected


def verify_m4_conflicts(core, results) -> tuple[dict, int]:
    verified: dict[tuple, dict] = {}
    rejected = 0
    core_adj = tuple(tuple(sorted(row)) for row in core.adjacency())
    paths = core_path_table(core_adj)
    for support in results:
        witness = verify_m4_support(core, support, core_adj, paths)
        if witness is None:
            rejected += 1
        else:
            verified[support] = {"witness": witness}
    return verified, rejected


_verify_worker_core = None


def _init_verify_worker(j: int, a: int, c: int) -> None:
    global _verify_worker_core
    _verify_worker_core = build_core(j, a, c)


def _verify_chunk_local(supports: list[tuple]) -> tuple[int, int]:
    return verify_m4_conflicts_count(_verify_worker_core, supports)


def verify_m4_parallel(j: int, a: int, c: int, supports: list[tuple],
                       workers: int) -> tuple[int, int]:
    if workers <= 1 or not supports:
        return verify_m4_conflicts_count(build_core(j, a, c), supports)
    chunk = max(1, len(supports) // (workers * 4))
    chunks = [supports[i:i + chunk] for i in range(0, len(supports), chunk)]
    accepted = rejected = 0
    context = multiprocessing.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=context,
                             initializer=_init_verify_worker,
                             initargs=(j, a, c)) as pool:
        for part_accepted, part_rejected in pool.map(_verify_chunk_local, chunks):
            accepted += part_accepted
            rejected += part_rejected
    return accepted, rejected


def support_commitment(ordered_supports: list[tuple]) -> str:
    """Canonical binary SHA-256 commitment to a sorted ``m=4`` support set."""
    digest = hashlib.sha256(b"type-t-passage-m4-supports-v1\0")
    for support in ordered_supports:
        for kind, (u, v) in support:
            digest.update(b"2" if kind == "p2" else b"3")
            digest.update(u.to_bytes(2, "big"))
            digest.update(v.to_bytes(2, "big"))
        digest.update(b"\n")
    return digest.hexdigest()


def shadow_audit(core, p2, p3, lower_shadow, start_vertices: list[int],
                 pruned_results) -> dict:
    """Cross-validate the lower-shadow pruning itself.

    Re-runs the same DFS over ``start_vertices`` with *no* shadow pruning and
    checks that filtering its output by "contains no certified smaller
    conflict" reproduces exactly the pruned run's output on those starts.
    A pruning bug (dropping a support that is not in fact dominated) shows up
    here as a nonempty difference.
    """
    pruned = enumerate_m4_c16_conflicts(
        core, p2, p3, lower_shadow=lower_shadow, start_vertices=start_vertices
    )
    unpruned = enumerate_m4_c16_conflicts(
        core, p2, p3, lower_shadow=lower_shadow, start_vertices=start_vertices,
        use_lower_shadow=False,
    )
    shadow_sets = [frozenset(support) for supports in (lower_shadow or {}).values()
                   for support in supports]
    by_size: dict[int, set[frozenset]] = defaultdict(set)
    for support in shadow_sets:
        by_size[len(support)].add(support)
    filtered = set()
    for support in unpruned["results"]:
        keys = frozenset(support)
        dominated = False
        for size, known in by_size.items():
            if size >= len(support):
                continue
            if any(frozenset(part) in known for part in itertools.combinations(sorted(keys), size)):
                dominated = True
                break
        if not dominated:
            filtered.add(tuple(sorted(support)))
    pruned_set = {tuple(sorted(support)) for support in pruned["results"]}
    return {
        "start_vertices": sorted(start_vertices),
        "unpruned_raw_supports": len(unpruned["results"]),
        "unpruned_after_domination_filter": len(filtered),
        "pruned_run_supports": len(pruned_set),
        "only_in_pruned_run": len(pruned_set - filtered),
        "only_in_filtered_unpruned_run": len(filtered - pruned_set),
        "agrees": pruned_set == filtered,
    }


def subcatalog_crossvalidation(core, p2, p3, trials: int, passages_per_trial: int,
                               seed: int = 20260730) -> list[dict]:
    """Cross-validate this compiler against a structurally different search.

    ``type_t_port_c16_passage_hypergraph.enumerate_passage_conflicts`` is the
    independently written general-``m`` augmented-graph walk that already
    cross-validated the ``C8`` passage catalog (and, by disagreeing with the
    ``m=2`` specialization, exposed the ``verify_passage_conflicts`` bug).  It
    is far too slow to run at ``max_m=4`` on the full 1,302-passage catalog,
    but it is perfectly fast on a *restricted* catalog -- and restricting the
    passage catalog changes nothing about the bare core, so on any subset both
    searches must return exactly the same size-4 supports.

    Each trial draws a random passage subset, runs both searches with no
    lower-shadow pruning, and compares the size-4 support sets exactly.  A
    length-arithmetic slip, a canonicalization slip (missing rotations), or a
    core-path-table slip in this module would show up as a nonempty symmetric
    difference on some trial.
    """
    import random

    from type_t_port_c16_passage_hypergraph import enumerate_passage_conflicts

    rng = random.Random(seed)
    all_tags = [("p2", key) for key in p2] + [("p3", key) for key in p3]
    reports = []
    for trial in range(trials):
        chosen = rng.sample(all_tags, min(passages_per_trial, len(all_tags)))
        sub_p2 = {key: p2[key] for kind, key in chosen if kind == "p2"}
        sub_p3 = {key: p3[key] for kind, key in chosen if kind == "p3"}
        mine = enumerate_m4_c16_conflicts(
            core, sub_p2, sub_p3, use_lower_shadow=False,
        )
        mine_set = {tuple(sorted(support)) for support in mine["results"]}
        theirs = enumerate_passage_conflicts(core, sub_p2, sub_p3, TARGET, max_m=M)
        theirs_set = {
            tuple(sorted(support))
            for support in theirs["results"]
            if len(support) == M and sum(1 for kind, _ in support if kind == "p3") <= 1
        }
        assert not theirs["truncated"]
        reports.append({
            "trial": trial,
            "p2_passages": len(sub_p2),
            "p3_passages": len(sub_p3),
            "m4_supports_this_module": len(mine_set),
            "m4_supports_general_walk": len(theirs_set),
            "only_this_module": len(mine_set - theirs_set),
            "only_general_walk": len(theirs_set - mine_set),
            "agrees": mine_set == theirs_set,
        })
    return reports


def compile_m4(j: int, a: int, c: int, time_budget_seconds: float | None = None,
               lower_shadow: dict[int, set[frozenset]] | None = None,
               workers: int = 1, summary_only: bool = False,
               generic_sample: int = 2000,
               shadow_audit_starts: tuple[int, ...] = (),
               crossvalidation_trials: int = 0,
               crossvalidation_passages: int = 40) -> dict:
    core = build_core(j, a, c)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    p2, p3 = build_passage_catalog(triples, gadgets)
    lower_shadow = lower_shadow or {}
    if workers > 1 and time_budget_seconds is None:
        raw = enumerate_m4_parallel(core, p2, p3, lower_shadow, workers)
    else:
        raw = enumerate_m4_c16_conflicts(core, p2, p3, time_budget_seconds, lower_shadow)
    for support in raw["results"]:
        assert len(support) == 4, f"expected exactly 4 passages, got {len(support)}: {support}"
        assert sum(1 for kind, _ in support if kind == "p3") <= 1
    # Every candidate in this stage has support size exactly four, so
    # within-stage strict-superset minimalization is a no-op; smaller
    # certified supports were removed during the DFS by the lower shadow.
    candidates = raw["results"]

    verification_started = time.monotonic()
    if summary_only:
        verified_count, rejected = verify_m4_parallel(j, a, c, list(candidates), workers)
        verified = None
    else:
        verified, rejected = verify_m4_conflicts(core, candidates)
        verified_count = len(verified)
    if summary_only and rejected:
        raise AssertionError(
            f"support-local verifier rejected {rejected} generated supports; "
            "cannot form a summary-only commitment"
        )
    verification_seconds = time.monotonic() - verification_started

    ordered_supports = sorted(candidates if summary_only else verified)
    commitment = support_commitment(ordered_supports)

    generic_sample_size = min(generic_sample, len(ordered_supports))
    if generic_sample_size:
        sample_indices = {
            index * len(ordered_supports) // generic_sample_size
            for index in range(generic_sample_size)
        }
        generic_batch = {ordered_supports[index]: True for index in sorted(sample_indices)}
        generic_verified, generic_rejected, generic_unchecked = verify_conflicts_generic(
            j, a, c, TARGET, generic_batch, workers=workers
        )
        assert not generic_rejected and not generic_unchecked
        assert set(generic_verified) == set(generic_batch)
        generic_sample_size = len(generic_batch)
    else:
        generic_rejected = generic_unchecked = 0
        generic_verified = {}

    audit = None
    if shadow_audit_starts:
        audit = shadow_audit(core, p2, p3, lower_shadow, list(shadow_audit_starts), candidates)
        assert audit["agrees"], f"lower-shadow pruning audit disagreed: {audit}"

    crossvalidation = None
    if crossvalidation_trials:
        crossvalidation = subcatalog_crossvalidation(
            core, p2, p3, crossvalidation_trials, crossvalidation_passages
        )
        assert all(report["agrees"] for report in crossvalidation), crossvalidation

    return {
        "status": "BOUNDED_INCOMPLETE" if raw["truncated"] else "COMPUTATIONALLY_CERTIFIED",
        "parameters": {"j": j, "Y": 1 << j, "a": a, "c": c},
        "target_length": TARGET,
        "hub_passages": M,
        "truncated": raw["truncated"],
        "elapsed_seconds": raw["elapsed_seconds"],
        "workers": workers,
        "max_core_segment_length": MAX_CORE_SEGMENT,
        "lower_shadow_seed_size": sum(len(values) for values in lower_shadow.values()),
        "lower_shadow_pruned_branches": raw["lower_shadow_pruned_branches"],
        "x1_completed": raw["x1_completed"],
        "x1_total": raw["x1_total"],
        "raw_candidate_supports": len(raw["results"]),
        "candidate_minimal_supports": len(candidates),
        "verification_rejected": rejected,
        "verification_unchecked": 0,
        "verification_seconds": verification_seconds,
        "verification_method": "exhaustive support-local alternating reconstruction plus literal simple-witness check",
        "generic_edge_path_cycle_crosscheck_sample": generic_sample_size,
        "generic_edge_path_cycle_crosscheck_rejected": generic_rejected,
        "lower_shadow_pruning_audit": audit,
        "independent_algorithm_crossvalidation": crossvalidation,
        "verified_minimal_supports": verified_count,
        "support_size_distribution": {"4": verified_count} if verified_count else {},
        "support_commitment_sha256": commitment,
        "support_commitment_format": "SHA-256 over sorted supports; prefix type-t-passage-m4-supports-v1\\0, then per support four records kind-byte ('2'/'3') + u:uint16be + v:uint16be, followed by newline",
        "conflicts_omitted": summary_only,
        "conflicts": [] if summary_only else [
            {"support": serialize_support(support), "witness": verified[support]["witness"]}
            for support in ordered_supports
        ],
        "generic_crosscheck_conflicts": [
            {"support": serialize_support(support), "witness": generic_verified[support]["witness"]}
            for support in sorted(generic_verified)
        ],
    }


def _conflict_lists(document: dict) -> list[list]:
    if "lengths" in document:
        return [stage.get("conflicts", []) for stage in document["lengths"].values()]
    if "per_m" in document:
        return [stage.get("conflicts", []) for stage in document["per_m"].values()]
    return [document.get("conflicts", [])]


def load_lower_shadow(paths: list[Path], max_size: int = M - 1) -> dict[int, set[frozenset]]:
    lower_shadow: dict[int, set[frozenset]] = defaultdict(set)
    for path in paths:
        payload = path.read_bytes()
        if path.suffix == ".gz":
            payload = gzip.decompress(payload)
        document = json.loads(payload)
        for conflicts in _conflict_lists(document):
            for record in conflicts:
                support = frozenset((kind, tuple(key)) for kind, key in record["support"])
                if len(support) <= max_size:
                    lower_shadow[len(support)].add(support)
    return dict(lower_shadow)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j", type=int, required=True)
    parser.add_argument("--a", type=int, required=True)
    parser.add_argument("--c", type=int, required=True)
    parser.add_argument("--time-budget", type=float, default=None)
    parser.add_argument("--lower-shadow", type=Path, action="append", default=[],
                        help="existing C8/C16 catalog whose conflicts prune supersets (repeatable)")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--summary-only", action="store_true",
                        help="commit count/hash plus generic sample, not every redundant witness record")
    parser.add_argument("--generic-sample", type=int, default=2000)
    parser.add_argument("--shadow-audit-starts", type=str, default="",
                        help="comma-separated canonical start vertices to re-run WITHOUT shadow "
                             "pruning, checking that the domination filter reproduces the pruned "
                             "output exactly on those starts")
    parser.add_argument("--crossvalidation-trials", type=int, default=0,
                        help="random passage-subcatalog trials cross-checked against the "
                             "independently implemented general-m walk")
    parser.add_argument("--crossvalidation-passages", type=int, default=40)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    lower_shadow = load_lower_shadow(args.lower_shadow)
    audit_starts = tuple(int(part) for part in args.shadow_audit_starts.split(",") if part.strip())
    result = compile_m4(args.j, args.a, args.c, args.time_budget, lower_shadow,
                        args.workers, args.summary_only, args.generic_sample,
                        audit_starts, args.crossvalidation_trials,
                        args.crossvalidation_passages)
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
