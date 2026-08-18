#!/usr/bin/env python3
"""General-``m`` passage-level ``C16`` conflict compiler, ``m`` in ``{2..5}``.

This reuses the oracle-pruned general-``m`` search machinery built for the
(superseded) gadget-level attempt in ``type_t_port_c16_hypergraph.py``
(``build_hop_relations`` composed-relation pruning oracle,
``enumerate_m_conflicts``'s endpoint-set-first / tag-second hop search,
cross-``m`` ``known_minimal`` domination pruning) but feeds it *passage*-level
inputs instead of gadget-level ones. That machinery was built to cope with
per-vertex branching up to ~1500 (raw triple/gadget identities); at the
passage level the same per-vertex branching is only ~70 (distinct
``(endpoint, route)`` passages -- see ``type_t_port_c16_passage_projection.md``
Phase 3), so it is directly usable here with no further specialization for
``m=2,3,4`` and, per ``type_t_port_c16_passage_m5.py``'s (m,r,v)-identity
analysis, ``m=5`` on its own is additionally exact-length-constrained enough
to be cheap either way.

**Two-``p3``-passage exclusion.** Unlike gadget-level identities, passage
*tags* are already unique per geometric passage, so the general search's
"pair_index" here is literally an identity map (one tag per passage). But
the physical "a completed graph selects exactly one linked-pair gadget"
constraint (``type_t_port_passages.drop_multi_p3_supports``) still applies
and is *not* automatically excluded by this search for ``m<5`` (it *is*
automatically excluded for ``m=5`` by the tight core-length arithmetic --
see ``type_t_port_c16_passage_m5.py``'s docstring), so every raw result is
passed through ``drop_multi_p3_supports`` before minimality/verification.

**Lower-shadow pruning.** ``enumerate_m_conflicts``'s ``known_minimal``
parameter is used to seed each stage with every smaller, already-verified
minimal conflict -- not just smaller ``m`` values of the *same* target
length, but also the already-compiled ``C8`` catalog (any completion
containing a ``C8`` is already forbidden regardless of what else it
contains). A candidate whose support is a superset of an existing minimal
conflict is dropped during generation, before it is ever counted, verified,
or stored -- distinguished in the report from post-hoc ``minimal_supports``
(which only removes redundancy *within* one already-fully-generated batch).
"""

from __future__ import annotations

import time
from collections import defaultdict
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait

from type_t_port_c16_hypergraph import build_hop_relations, enumerate_m_conflicts
from type_t_port_c16_hypergraph import minimal_supports as minimal_supports_general
from type_t_port_core_export import build_core
from type_t_port_multipole_check import edge_path_cycle, validate_literal_cycle
from type_t_port_passages import drop_multi_p3_supports, materialize_passages
from type_t_port_short_conflicts import compute_reach_index


def build_passage_endpoint_sets(p2: dict, p3: dict) -> dict[int, list[tuple[int, int]]]:
    ep: dict[int, set] = defaultdict(set)
    for (u, v) in p2:
        ep[u].add((v, 2))
        ep[v].add((u, 2))
    for (u, v) in p3:
        ep[u].add((v, 3))
        ep[v].add((u, 3))
    return {v: sorted(s) for v, s in ep.items()}


def build_passage_pair_index(p2: dict, p3: dict) -> dict[tuple[int, int, int], list[tuple]]:
    """Passage tags are already unique per geometric passage (unlike
    gadget/triple identities), so this is a direct identity map, not a
    multiplicity list -- built for interface compatibility with the reused
    ``enumerate_m_conflicts``, which expects a ``pair_index``."""
    index: dict[tuple[int, int, int], list[tuple]] = {}
    for (u, v) in p2:
        tag = ("p2", (u, v))
        index[(u, v, 2)] = [tag]
        index[(v, u, 2)] = [tag]
    for (u, v) in p3:
        tag = ("p3", (u, v))
        index[(u, v, 3)] = [tag]
        index[(v, u, 3)] = [tag]
    return index


# --- verification (materialize_passages + edge_path_cycle, parallel) -------

_worker_core = None


def _init_worker(j: int, a: int, c: int) -> None:
    global _worker_core
    _worker_core = build_core(j, a, c)


def _verify_chunk(args):
    target_length, supports = args
    out, rejected = [], 0
    for support in supports:
        graph, adjacency = materialize_passages(_worker_core, support)
        witness = edge_path_cycle(adjacency, target_length)
        if witness is None:
            rejected += 1
            continue
        validate_literal_cycle(graph, list(witness))
        out.append((support, list(witness)))
    return out, rejected


def verify_conflicts(j: int, a: int, c: int, target_length: int, results: dict,
                     workers: int = 1, chunk_size: int = 1500,
                     deadline: float | None = None) -> tuple[dict, int, int]:
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


def serialize_support(support: tuple) -> list:
    return [[kind, list(key)] for kind, key in support]


def load_known_minimal_from_conflicts(conflicts: list, known_minimal: dict[int, set]) -> int:
    """Seed ``known_minimal`` (as used by ``enumerate_m_conflicts``) from an
    already-serialized conflict list (e.g. the compiled ``C8`` catalog) --
    lower-shadow pruning across *target lengths*, not just across ``m``
    within one length: any completion already forbidden by a smaller C8
    conflict is forbidden regardless of what else a larger C16 candidate
    contains."""
    added = 0
    for record in conflicts:
        support = tuple(sorted((kind, tuple(key)) for kind, key in record["support"]))
        key_set = frozenset(support)
        if key_set not in known_minimal[len(support)]:
            known_minimal[len(support)].add(key_set)
            added += 1
    return added
