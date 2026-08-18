#!/usr/bin/env python3
"""Specialized ``m=5`` C16 passage-level compiler.

Phase 1 (``type_t_port_c16_compilation.md``) proves ``2 <= m <= floor(L/3)``;
for ``L=16`` this allows ``m`` up to ``5``. At ``m=5`` the ``(m,r,v)``
identity pins the core-path-length composition down to (at most) two cases,
because ``route_total = m + r`` and ``core_total = L - route_total``, and
every one of the ``m=5`` core-path segments must be ``>=1``:

* ``b=0`` (no ``p3``/cross passage used): all five passages are ``p2``
  (route length 2 each), ``route_total = 10``, ``core_total = 6`` split into
  five positive parts -- the only integer partition of 6 into 5 positive
  parts is ``{2,1,1,1,1}`` (up to which of the five *positions* gets the 2).
* ``b=1`` (exactly one ``p3`` passage; two ``p3``s can never coexist, see
  ``type_t_port_passages.drop_multi_p3_supports``): four ``p2`` + one
  ``p3``, ``route_total = 4*2 + 3 = 11``, ``core_total = 5`` split into five
  positive parts -- the only partition of 5 into 5 positive parts is
  ``{1,1,1,1,1}``.

So every ``m=5`` ``C16`` conflict only ever needs bare-core paths of length
1 or 2 -- never the long, expensive intermediate lengths that make the
general ``enumerate_passage_conflicts(..., max_m=5, ...)`` walk explode
(it also re-derives every ``m<5`` conflict in the same pass, which this
compiler skips entirely). This lets a direct, tightly pruned 5-hop DFS
enumerate the *exact* ``m=5`` case directly, using only ``core_adj``
(length-1 reachability) and a length-2 reachability set built directly from
it (both trivial on a sparse, near-path bare core).
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


def _length2_paths(core_adj):
    """All literal simple two-edge core paths ``v-mid-w``.

    Retaining ``mid`` (rather than just the reachable endpoint ``w``) lets
    the DFS enforce vertex simplicity before emitting a candidate.  The
    independent verifier remains in place as a second implementation.
    """
    order = len(core_adj)
    paths2 = [[] for _ in range(order)]
    for v in range(order):
        for mid in core_adj[v]:
            for w in core_adj[mid]:
                if w != v:
                    paths2[v].append((mid, w))
    return paths2


def enumerate_m5_c16_conflicts(core, p2, p3, time_budget_seconds: float | None = None,
                               lower_shadow: dict[int, set[frozenset]] | None = None,
                               start_vertices: list[int] | None = None) -> dict:
    """Exact ``m=5`` search for ``target_length=16`` conflicts, covering
    both the ``b=0`` (five ``p2``s, one core segment of length 2, four of
    length 1) and ``b=1`` (four ``p2``s + one ``p3``, all five core
    segments length 1) cases in a single DFS: at every hop the DFS tries
    every admissible ``(passage, core-step-length)`` combination and simply
    lets the running totals (route length so far, core length so far,
    whether the one allowed ``p3`` has been used, whether the one allowed
    length-2 core step has been used) prune everything that cannot reach
    exactly ``route_total=16`` in exactly 5 hops -- so both cases, and every
    rotation of which of the 5 positions carries the "2" (or, for ``b=1``,
    which of the 5 carries the ``p3``), are explored, without ever needing
    a core-path length other than 1 or 2.
    """
    core_adj = tuple(tuple(sorted(row)) for row in core.adjacency())
    order = core.order
    paths2 = _length2_paths(core_adj)

    # The DFS's hottest objects are passage tags and used-vertex sets.
    # Compile them once to small integers and a Python-int bitmask; convert
    # back to the public tuple representation only after enumeration.
    tags = sorted(
        [("p2", key) for key in p2] + [("p3", key) for key in p3]
    )
    tag_to_id = {tag: index for index, tag in enumerate(tags)}
    passage_options: list[list[tuple[int, int, int, bool]]] = [list() for _ in range(order)]
    for tag_id, (kind, (u, v)) in enumerate(tags):
        route = 2 if kind == "p2" else 3
        is_p3 = kind == "p3"
        passage_options[u].append((tag_id, v, route, is_p3))
        passage_options[v].append((tag_id, u, route, is_p3))
    for options in passage_options:
        options.sort()

    lower_ids: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    for size, supports in (lower_shadow or {}).items():
        for support in supports:
            try:
                encoded = tuple(sorted(tag_to_id[tag] for tag in support))
            except KeyError as error:
                raise AssertionError(f"lower-shadow passage absent from current catalog: {error}") from error
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
        # Kept for a future certified m=4 lower shadow.  It is not entered
        # for the present C8/m2/m3 seed.
        for size, known in lower_ids.items():
            if size > len(chain_ids) + 1:
                continue
            for part in itertools.combinations(chain_ids, size - 1):
                if tuple(sorted((*part, tag_id))) in known:
                    return True
        return False

    TARGET = 16
    M = 5
    result_ids: set[tuple[int, ...]] = set()
    started = time.monotonic()
    truncated = False
    shadow_pruned = 0
    x1_completed = 0
    start_vertices = list(range(order)) if start_vertices is None else start_vertices

    for x1 in start_vertices:
        if truncated:
            break
        chain: list[int] = []
        initial_used = 1 << x1

        def rec(current_v: int, hop: int, route_used: int, core_used: int,
               p3_used: bool, two_used: bool, used_mask: int,
               selected_ids: int, triple_blocked: int) -> None:
            nonlocal truncated, shadow_pruned
            if time_budget_seconds is not None and time.monotonic() - started > time_budget_seconds:
                truncated = True
                return
            remaining_hops = M - hop
            for tag_id, y, route, is_p3 in passage_options[current_v]:
                # Canonical rotation: every alternating cycle is explored
                # from its least passage endpoint.  This removes its other
                # nine endpoint/orientation starts without losing a cycle.
                y_bit = 1 << y
                if used_mask & y_bit or y < x1:
                    continue
                # The length identity leaves exactly two mutually exclusive
                # compositions: one p3 with all unit core segments, or all
                # p2 with exactly one length-2 core segment.  A branch that
                # combines p3 with a length-2 segment can never total 16.
                if is_p3 and (p3_used or two_used):
                    continue
                tag_bit = 1 << tag_id
                if (tag_id in known_singletons
                        or pair_forbidden[tag_id] & selected_ids
                        or triple_blocked & tag_bit
                        or (lower_ids and extends_large_shadow(chain, tag_id))):
                    shadow_pruned += 1
                    continue
                new_route = route_used + route
                if new_route > TARGET - remaining_hops:  # each remaining hop needs core length >=1
                    continue
                new_p3_used = p3_used or is_p3
                if remaining_hops == 1:
                    # closing hop: single core step (length 1 or, if not
                    # used yet, length 2) directly back to x1.
                    needed = TARGET - new_route - core_used
                    if needed == 1 and x1 in core_adj[y]:
                        result_ids.add(tuple(sorted((*chain, tag_id))))
                    if needed == 2 and not two_used:
                        for mid, w in paths2[y]:
                            if w == x1 and not used_mask & (1 << mid):
                                result_ids.add(tuple(sorted((*chain, tag_id))))
                                break
                    continue
                chain.append(tag_id)
                next_selected_ids = selected_ids | (1 << tag_id)
                next_triple_blocked = triple_blocked
                for old_id in chain[:-1]:
                    lo, hi = (old_id, tag_id) if old_id < tag_id else (tag_id, old_id)
                    next_triple_blocked |= triple_forbidden[lo * tag_count + hi]
                passage_used = used_mask | y_bit
                # length-1 core step
                for x_next in core_adj[y]:
                    next_bit = 1 << x_next
                    if passage_used & next_bit or x_next < x1:
                        continue
                    rec(x_next, hop + 1, new_route, core_used + 1,
                        new_p3_used, two_used, passage_used | next_bit,
                        next_selected_ids, next_triple_blocked)
                    if truncated:
                        break
                # length-2 core step (only once, only if not used yet)
                if not truncated and not two_used and not new_p3_used:
                    for mid, x_next in paths2[y]:
                        mid_bit = 1 << mid
                        next_bit = 1 << x_next
                        if passage_used & (mid_bit | next_bit) or x_next < x1:
                            continue
                        rec(x_next, hop + 1, new_route, core_used + 2,
                            new_p3_used, True, passage_used | mid_bit | next_bit,
                            next_selected_ids, next_triple_blocked)
                        if truncated:
                            break
                chain.pop()
                if truncated:
                    return

        rec(x1, 0, 0, 0, False, False, initial_used, 0, 0)
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
    return enumerate_m5_c16_conflicts(
        core, p2, p3, lower_shadow=lower_shadow, start_vertices=start_vertices
    )


def enumerate_m5_parallel(core, p2, p3, lower_shadow, workers: int) -> dict:
    """Partition canonical start vertices exactly across worker processes."""
    workers = max(1, min(workers, core.order))
    if workers == 1:
        return enumerate_m5_c16_conflicts(core, p2, p3, lower_shadow=lower_shadow)
    # Round-robin assignment spreads dense and sparse start vertices more
    # evenly than contiguous ranges.  ``fork`` keeps the large immutable
    # lower-shadow index copy-on-write on Unix/macOS.
    chunks = [list(range(core.order))[index::workers] for index in range(workers)]
    started = time.monotonic()
    results = {}
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


def verify_m5_support(core, support: tuple, core_adj=None, paths2=None) -> list[int] | None:
    """Independently reconstruct the literal alternating cycle for one support.

    Unlike the global generator, this starts from a *fixed* five-passage
    support and searches only for the required core matching: five unit
    core segments when one passage is p3, or four unit segments and one
    literal two-edge core path when all passages are p2.  It constructs the
    resulting literal 16-vertex witness from core edges and fresh passage
    hubs and checks simplicity.  The generic materialized-graph verifier is
    retained as a separate cross-check in ``compile_m5``.
    """
    if len(support) != 5:
        return None
    endpoints = [vertex for _kind, key in support for vertex in key]
    if len(set(endpoints)) != 10:
        return None
    p3_count = sum(kind == "p3" for kind, _key in support)
    if p3_count not in (0, 1):
        return None

    mate = {}
    endpoint_tag = {}
    for tag in support:
        _kind, (u, v) = tag
        mate[u], mate[v] = v, u
        endpoint_tag[u] = endpoint_tag[v] = tag
    endpoint_set = frozenset(endpoints)
    core_adj = core_adj or tuple(tuple(sorted(row)) for row in core.adjacency())
    paths2 = paths2 or _length2_paths(core_adj)
    start = min(endpoint_set)
    pieces = []

    def rec(current: int, hop: int, used_mask: int, two_used: bool):
        y = mate[current]
        y_bit = 1 << y
        if used_mask & y_bit:
            return None
        next_used = used_mask | y_bit
        tag = endpoint_tag[current]
        lengths = (1,) if p3_count or two_used else (1, 2)
        for core_length in lengths:
            candidates = ((None, vertex) for vertex in core_adj[y]) if core_length == 1 else paths2[y]
            for mid, x_next in candidates:
                closing = hop == 4
                if closing:
                    if x_next != start:
                        continue
                elif x_next == start or x_next not in endpoint_set:
                    continue
                if mid is not None and (mid in endpoint_set or next_used & (1 << mid)):
                    continue
                if not closing and next_used & (1 << x_next):
                    continue
                new_two_used = two_used or core_length == 2
                if closing and not p3_count and not new_two_used:
                    continue
                core_path = (y, x_next) if mid is None else (y, mid, x_next)
                pieces.append((current, tag, y, core_path))
                if closing:
                    return list(pieces)
                used_after_core = next_used | (1 << x_next)
                if mid is not None:
                    used_after_core |= 1 << mid
                found = rec(x_next, hop + 1, used_after_core, new_two_used)
                if found is not None:
                    return found
                pieces.pop()
        return None

    found = rec(start, 0, 1 << start, False)
    if found is None:
        return None

    passage_routes = {}
    next_vertex = core.order
    for tag in support:
        kind, (u, v) = tag
        if kind == "p2":
            passage_routes[tag] = (u, next_vertex, v)
            next_vertex += 1
        else:
            passage_routes[tag] = (u, next_vertex, next_vertex + 1, v)
            next_vertex += 2
    witness = []
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
    if len(witness) != 16 or len(set(witness)) != 16:
        return None
    return witness


def verify_m5_conflicts(core, results: dict) -> tuple[dict, int]:
    verified = {}
    rejected = 0
    core_adj = tuple(tuple(sorted(row)) for row in core.adjacency())
    paths2 = _length2_paths(core_adj)
    for support in results:
        witness = verify_m5_support(core, support, core_adj, paths2)
        if witness is None:
            rejected += 1
        else:
            verified[support] = {"witness": witness}
    return verified, rejected


def verify_m5_conflicts_count(core, results: dict) -> tuple[int, int]:
    """Exhaustively verify without retaining one redundant witness per support."""
    accepted = rejected = 0
    core_adj = tuple(tuple(sorted(row)) for row in core.adjacency())
    paths2 = _length2_paths(core_adj)
    for support in results:
        if verify_m5_support(core, support, core_adj, paths2) is None:
            rejected += 1
        else:
            accepted += 1
    return accepted, rejected


def support_commitment(ordered_supports: list[tuple]) -> str:
    """Canonical binary SHA-256 commitment to a sorted m5 support catalog."""
    digest = hashlib.sha256(b"type-t-passage-m5-supports-v1\0")
    for support in ordered_supports:
        for kind, (u, v) in support:
            digest.update(b"2" if kind == "p2" else b"3")
            digest.update(u.to_bytes(2, "big"))
            digest.update(v.to_bytes(2, "big"))
        digest.update(b"\n")
    return digest.hexdigest()


def compile_m5(j: int, a: int, c: int, time_budget_seconds: float | None = None,
               lower_shadow: dict[int, set[frozenset]] | None = None,
               workers: int = 1, summary_only: bool = False) -> dict:
    core = build_core(j, a, c)
    _normal, _pairs, triples, gadgets, _same_bad, _cross_bad = build_catalog(core)
    p2, p3 = build_passage_catalog(triples, gadgets)
    lower_shadow = lower_shadow or {}
    if workers > 1 and time_budget_seconds is None:
        raw = enumerate_m5_parallel(core, p2, p3, lower_shadow, workers)
    else:
        raw = enumerate_m5_c16_conflicts(
            core, p2, p3, time_budget_seconds, lower_shadow
        )
    for support in raw["results"]:
        assert len(support) == 5, f"expected exactly 5 passages, got {len(support)}: {support}"
        assert sum(1 for kind, _ in support if kind == "p3") <= 1
    # Every candidate in this specialized stage has support size exactly
    # five, so within-stage strict-superset minimalization is a no-op.
    # Smaller certified supports were already removed during the DFS.
    candidates = raw["results"]
    verification_started = time.monotonic()
    if summary_only:
        verified_count, rejected = verify_m5_conflicts_count(core, candidates)
        verified = None
    else:
        verified, rejected = verify_m5_conflicts(core, candidates)
        verified_count = len(verified)
    if summary_only and rejected:
        raise AssertionError(
            f"support-local verifier rejected {rejected} generated supports; "
            "cannot form a summary-only commitment"
        )
    verification_seconds = time.monotonic() - verification_started
    unchecked = 0
    # A bounded, evenly-spaced cross-check retains the pre-existing generic
    # exact-cycle finder as a genuinely different implementation without
    # paying its multi-million-support cost on a stage already exhaustively
    # checked by the support-local verifier above.
    ordered_supports = sorted(candidates if summary_only else verified)
    commitment = support_commitment(ordered_supports)
    generic_sample_size = min(2000, len(ordered_supports))
    if generic_sample_size:
        sample_indices = {
            index * len(ordered_supports) // generic_sample_size
            for index in range(generic_sample_size)
        }
        generic_sample = {ordered_supports[index]: True for index in sample_indices}
        generic_verified, generic_rejected, generic_unchecked = verify_conflicts_generic(
            j, a, c, 16, generic_sample, workers=workers
        )
        assert not generic_rejected and not generic_unchecked
        assert set(generic_verified) == set(generic_sample)
    else:
        generic_rejected = generic_unchecked = 0
        generic_verified = {}
    return {
        "status": "BOUNDED_INCOMPLETE" if raw["truncated"] or unchecked else "COMPUTATIONALLY_CERTIFIED",
        "parameters": {"j": j, "Y": 1 << j, "a": a, "c": c},
        "target_length": 16,
        "hub_passages": 5,
        "truncated": raw["truncated"],
        "elapsed_seconds": raw["elapsed_seconds"],
        "workers": workers,
        "lower_shadow_seed_size": sum(len(values) for values in lower_shadow.values()),
        "lower_shadow_pruned_branches": raw["lower_shadow_pruned_branches"],
        "x1_completed": raw["x1_completed"],
        "x1_total": raw["x1_total"],
        "raw_candidate_supports": len(raw["results"]),
        "candidate_minimal_supports": len(candidates),
        "verification_rejected": rejected,
        "verification_unchecked": unchecked,
        "verification_seconds": verification_seconds,
        "verification_method": "exhaustive support-local alternating reconstruction plus literal simple-witness check",
        "generic_edge_path_cycle_crosscheck_sample": generic_sample_size,
        "generic_edge_path_cycle_crosscheck_rejected": generic_rejected,
        "verified_minimal_supports": verified_count,
        "support_size_distribution": {"5": verified_count} if verified_count else {},
        "support_commitment_sha256": commitment,
        "support_commitment_format": "SHA-256 over sorted supports; prefix type-t-passage-m5-supports-v1\\0, then per support five records kind-byte ('2'/'3') + u:uint16be + v:uint16be, followed by newline",
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
    """Find committed conflict lists in either catalog schema."""
    if "lengths" in document:
        return [stage.get("conflicts", []) for stage in document["lengths"].values()]
    if "per_m" in document:
        return [stage.get("conflicts", []) for stage in document["per_m"].values()]
    return [document.get("conflicts", [])]


def load_lower_shadow(paths: list[Path]) -> dict[int, set[frozenset]]:
    lower_shadow: dict[int, set[frozenset]] = defaultdict(set)
    for path in paths:
        payload = path.read_bytes()
        if path.suffix == ".gz":
            payload = gzip.decompress(payload)
        document = json.loads(payload)
        for conflicts in _conflict_lists(document):
            for record in conflicts:
                support = frozenset((kind, tuple(key)) for kind, key in record["support"])
                if len(support) < 5:
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
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--summary-only", action="store_true",
                        help="commit count/hash plus generic sample, not every redundant witness record")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    lower_shadow = load_lower_shadow(args.lower_shadow)
    result = compile_m5(args.j, args.a, args.c, args.time_budget, lower_shadow,
                        args.workers, args.summary_only)
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
