#!/usr/bin/env python3
"""Symbolic passage-conflict templates (Phases 1-4 of the template task).

Loads a verified passage-level conflict catalog (``type_t_port_passages.py``
/ ``type_t_port_c16_passage_catalog.py`` output: clauses of the form
``{"support": [[kind, [u, v]], ...], "witness": [...]}``), decodes each
clause's witness cycle into its alternating hub-passage / bare-core-path
segments, expresses every vertex/segment in the symbolic coordinates of
``type_t_port_coordinates.py``, and quotients by the natural symmetry of the
witness cycle (which of the two passages is "first", and the reading
direction) to produce a much smaller set of *templates*.

Currently handles the ``m=2`` shape exactly (2 hub passages, 2 bare-core
paths) -- this covers every available catalog (``C8`` at all three ``j=4``
instances, and the ``C16`` ``m=2``-only catalog). The data model
(``ConflictRecord`` / ``Template``) is written so that higher-``m`` shapes
(``C16`` ``m=3,4,5``, produced by the sibling agent) can be ingested later
by adding one more decoder, without touching the vertex-tag/template-key
machinery below (Phase 5 -- see ``type_t_port_passage_templates.md``).

## Vertex tags (the quotient-by-translation mechanism)

Every deficient core vertex touched by a conflict is classified as one of:

* ``("anchor", name)`` -- literally one of the 13 fixed anchors (includes
  ``u_x``/``u_y``, which are anchors *and* deficient).
* ``("bulk", path, family)`` -- a path-internal vertex farther than
  ``BULK_THRESHOLD`` (12, from the proved ``C16`` core-path-length bound)
  core-edges from *both* of its bounding anchors. Its *absolute* index is
  dropped from the tag -- this is what makes translation act as a genuine
  symmetry on the template.
* ``("near", path, side, offset)`` -- a path-internal vertex within
  ``BULK_THRESHOLD`` of one bounding anchor (``side`` is ``"left"`` or
  ``"right"``, ``offset`` is the exact distance to that anchor). This is
  *not* translation-quotiented (the offset is a load-bearing constant of
  the template), but it is still translation-quotiented in ``j``: as long
  as the path is long enough for the given offset to exist (a condition
  independent of ``j`` once ``j`` is large enough), the same fixed-offset
  picture recurs for every larger instance.

## Core-path segment descriptors

* ``("same", path, length)`` -- the whole bare-core path stays on one named
  path (monotonic index walk); this is the only shape that is bulk-eligible.
* ``("cross", paths, length)`` -- the path visits >= 2 named paths (passes
  through at least one anchor strictly inside the segment); ``paths`` is
  the ordered tuple of path names traversed.

## Canonicalization

The witness cycle for an ``m=2`` conflict has the cyclic shape
``[V0, coreA, V1, passage1, V2, coreB, V3, passage2]`` back to ``V0``. Its
symmetry group (rotating which passage/core path is "first", and reversing
the reading direction) has order 4; ``canonical_key`` computes all 4x2=8
representations (rotation in {0,2,4,6} composed with reversal-or-not) and
keeps the lexicographic minimum as the template key.
"""

from __future__ import annotations

import argparse
import gzip
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from type_t_port_core_export import PortCore, build_core
from type_t_port_coordinates import (
    Anchor,
    PathPos,
    branch_family,
    distance_to_nearest_anchor,
    label_positions,
    parse_label,
)


BULK_THRESHOLD = 12  # proved bound: total core-path length in any C16 conflict is <= 12


# ---------------------------------------------------------------------------
# Witness decoding (generic: works for any m=2 conflict, any target length)
# ---------------------------------------------------------------------------

def split_witness(core: PortCore, witness: list[int]):
    n = len(witness)
    is_core = [v < core.order for v in witness]
    start = next(i for i in range(n) if is_core[i] and not is_core[(i - 1) % n])
    witness = witness[start:] + witness[:start]
    is_core = is_core[start:] + is_core[:start]
    segments = []
    i = 0
    while i < n:
        j = i
        run = [witness[i]]
        cur = is_core[i]
        while j + 1 < n and is_core[j + 1] == cur:
            run.append(witness[j + 1])
            j += 1
        segments.append(("core" if cur else "hub", run))
        i = j + 1
    return segments


def decode_m2_witness(core: PortCore, conflict: dict) -> dict:
    """Decode an m=2 conflict's witness into (core_A, passage1, core_B,
    passage2) and cross-check against ``support``. Raises if the witness
    isn't exactly the m=2 shape (2 core runs, 2 hub runs)."""
    segs = split_witness(core, conflict["witness"])
    kinds = [k for k, _ in segs]
    if kinds != ["core", "hub", "core", "hub"]:
        raise ValueError(f"not an m=2 witness shape: {kinds}")
    core_a, core_b = segs[0][1], segs[2][1]
    passage1 = (core_a[-1], core_b[0])
    passage2 = (core_b[-1], core_a[0])
    support_kind = {tuple(sorted(uv)): kind for kind, uv in conflict["support"]}
    got = {tuple(sorted(passage1)), tuple(sorted(passage2))}
    if support_kind.keys() != got:
        raise AssertionError(f"witness/support mismatch: {support_kind.keys()} vs {got}")
    kind1 = support_kind[tuple(sorted(passage1))]
    kind2 = support_kind[tuple(sorted(passage2))]
    return {
        "core_A": core_a, "core_B": core_b,
        "passage1": passage1, "kind1": kind1,
        "passage2": passage2, "kind2": kind2,
    }


# ---------------------------------------------------------------------------
# Symbolic tags
# ---------------------------------------------------------------------------

def vertex_tag(label: str, j: int, a: int, c: int, threshold: int = BULK_THRESHOLD):
    coord = parse_label(label)
    if isinstance(coord, Anchor):
        return ("anchor", coord.name)
    dist, _anchor, side = distance_to_nearest_anchor(label, j, a, c)
    fam = branch_family(label) or ""
    if dist > threshold:
        return ("bulk", coord.path, fam)
    return ("near", coord.path, side, dist)


def generic_vertex_tag(label: str):
    """Drops the near/bulk distance-threshold bucketing entirely (Phase 3
    finding: the near/bulk split of the ``vertex_tag`` function is a
    *reporting* artifact of the distance-12 cutoff, not a real geometric
    distinction, for path-internal vertices on a `same`-mode core path --
    the exact offset is recoverable from the (already recorded) core-path
    length once you know which end of the branch a passage starts counting
    from, and free translation makes the absolute value irrelevant to the
    template's validity). Anchors keep their literal name (structurally
    load-bearing: an anchor's local neighborhood genuinely differs from
    another's)."""
    coord = parse_label(label)
    if isinstance(coord, Anchor):
        return ("anchor", coord.name)
    return ("generic", coord.path, "")


def _path_step(labels, u_vertex, v_vertex, j, a, c):
    lu, lv = labels[u_vertex], labels[v_vertex]
    pu = dict(label_positions(lu, j, a, c))
    pv = dict(label_positions(lv, j, a, c))
    candidates = [p for p in pu.keys() & pv.keys() if abs(pu[p] - pv[p]) == 1]
    if not candidates:
        raise AssertionError(f"{lu} -> {lv} is not a bare-core edge under the coordinate model")
    return candidates[0], (1 if pv[candidates[0]] - pu[candidates[0]] == 1 else -1)


def core_path_descriptor(run, labels, j, a, c):
    length = len(run) - 1
    paths_used, directions = [], []
    for i in range(length):
        p, d = _path_step(labels, run[i], run[i + 1], j, a, c)
        paths_used.append(p)
        directions.append(d)
    if len(set(paths_used)) == 1 and len(set(directions)) == 1:
        return ("same", paths_used[0], length)
    return ("cross", tuple(paths_used), length)


def reverse_segment(token):
    if token[0] == "passage":
        return token
    _tag, mode, detail, length = token
    if mode == "same":
        return token
    return ("core", "cross", tuple(reversed(detail)), length)


def _sanitize(token):
    """Replace None with '' so tuples compare orderably across mixed types."""
    return tuple("" if x is None else x for x in token)


def canonicalize_cyclic(cyclic: list[tuple]) -> tuple:
    """The m=2 witness symmetry group (order 4: rotate-by-2, reflect) applied
    to an already-built ``[V0,S0,V1,S1,V2,S2,V3,S3]`` cyclic token list.
    Shared by real conflict records (``build_conflict_record``) and by the
    Phase-3 from-first-principles enumerator (``enumerate_bulk_shapes``),
    so both use exactly the same notion of "the same template"."""

    def reversed_cyclic(seq):
        rev = [reverse_segment(t) if t[0] == "core" else t for t in seq[::-1]]
        return rev[1:] + rev[:1]

    candidates = []
    for base in (cyclic, reversed_cyclic(cyclic)):
        for r in (0, 2, 4, 6):
            rotated = base[r:] + base[:r]
            candidates.append(tuple(_sanitize(t) for t in rotated))
    return min(candidates)


def wildcard_branch_names(cyclic: list[tuple]) -> list[list[tuple]]:
    """Replaces every literal ``same``-mode path name with a positional
    wildcard ``W0``, ``W1``, ... (assigned in first-occurrence order).
    Returns *all* branch-relabelings to minimize over (only 2 distinct
    branches ever occur in an m=2 conflict, so at most 2 relabelings) --
    the caller must run ``canonicalize_cyclic`` on every one and take the
    overall minimum, since the rotate/reflect symmetry and the branch-swap
    symmetry interact (a rotation can pair a length with the *other*
    branch's route -- see ``type_t_port_passage_templates.md`` Phase 3).
    This is the "abstract from which literal growing branch" quotient that
    collapses the same-mode catalog to a handful of universal shapes."""
    names: list[str] = []
    for t in cyclic:
        if t[0] == "generic" and t[1] not in names:
            names.append(t[1])
        if t[0] == "core" and t[1] == "same" and t[2] not in names:
            names.append(t[2])
    mapping = {name: f"W{idx}" for idx, name in enumerate(names)}

    def remap(token, extra=None):
        m = mapping if extra is None else extra
        if token[0] == "generic":
            return ("generic", m.get(token[1], token[1]), token[2])
        if token[0] == "core":
            if token[1] == "same":
                return ("core", "same", m.get(token[2], token[2]), token[3])
            return token
        return token

    wildcarded = [remap(t) for t in cyclic]
    if len(names) < 2:
        return [wildcarded]
    swapped_map = {"W0": "W1", "W1": "W0"}
    swapped = [remap(t, swapped_map) for t in wildcarded]
    return [wildcarded, swapped]


def abstracted_key(core_a, core_b, labels, decoded, j, a, c) -> tuple:
    """The fully branch-name-abstracted template key: generic vertex tags
    (anchor identity kept, growing-branch identity wildcarded) plus
    wildcard_branch_names, then canonicalized. This is the key that
    collapses ``same``-mode C8 conflicts to exactly 8 templates (4
    length-compositions x same/cross-branch), stable across all three
    tested j=4 instances."""
    v0 = generic_vertex_tag(labels[core_a[0]])
    v1 = generic_vertex_tag(labels[core_a[-1]])
    v2 = generic_vertex_tag(labels[core_b[0]])
    v3 = generic_vertex_tag(labels[core_b[-1]])
    s0 = ("core",) + core_path_descriptor(core_a, labels, j, a, c)
    s1 = ("passage", decoded["kind1"])
    s2 = ("core",) + core_path_descriptor(core_b, labels, j, a, c)
    s3 = ("passage", decoded["kind2"])
    cyclic = [v0, s0, v1, s1, v2, s2, v3, s3]
    candidates = wildcard_branch_names(cyclic)
    return min(canonicalize_cyclic(candidate) for candidate in candidates)


# ---------------------------------------------------------------------------
# Full conflict record + canonicalization
# ---------------------------------------------------------------------------

@dataclass
class ConflictRecord:
    parameters: tuple[int, int, int]
    raw_support: tuple
    witness: tuple
    is_bulk: bool
    is_crossing: bool
    canonical_key: tuple
    abstract_key: tuple
    passage_kinds: tuple[str, str]
    core_lengths: tuple[int, int]
    vertex_tags: tuple


def build_conflict_record(core: PortCore, conflict: dict) -> ConflictRecord:
    j, a, c = core.j, core.a, core.c
    labels = core.labels
    decoded = decode_m2_witness(core, conflict)
    core_a, core_b = decoded["core_A"], decoded["core_B"]

    v0 = vertex_tag(labels[core_a[0]], j, a, c)
    v1 = vertex_tag(labels[core_a[-1]], j, a, c)
    v2 = vertex_tag(labels[core_b[0]], j, a, c)
    v3 = vertex_tag(labels[core_b[-1]], j, a, c)
    core_desc_a = core_path_descriptor(core_a, labels, j, a, c)
    core_desc_b = core_path_descriptor(core_b, labels, j, a, c)
    s0 = ("core",) + core_desc_a
    s1 = ("passage", decoded["kind1"])
    s2 = ("core",) + core_desc_b
    s3 = ("passage", decoded["kind2"])

    cyclic = [v0, s0, v1, s1, v2, s2, v3, s3]
    canonical_key = canonicalize_cyclic(cyclic)
    abstract_key = abstracted_key(core_a, core_b, labels, decoded, j, a, c)

    is_crossing = core_desc_a[0] == "cross" or core_desc_b[0] == "cross"
    is_bulk = (
        not is_crossing
        and all(tag[0] == "bulk" for tag in (v0, v1, v2, v3))
    )

    return ConflictRecord(
        parameters=(j, a, c),
        raw_support=tuple(tuple(x) for x in conflict["support"]),
        witness=tuple(conflict["witness"]),
        is_bulk=is_bulk,
        is_crossing=is_crossing,
        canonical_key=canonical_key,
        abstract_key=abstract_key,
        passage_kinds=(decoded["kind1"], decoded["kind2"]),
        core_lengths=(core_desc_a[2], core_desc_b[2]),
        vertex_tags=(v0, v1, v2, v3),
    )


# ---------------------------------------------------------------------------
# Loading catalogs
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Phase 3: first-principles enumeration of bulk length-compositions
# ---------------------------------------------------------------------------

def enumerate_bulk_shapes(target_length: int, cross_branch: bool) -> dict:
    """Symbolically enumerates every possible m=2 bulk length-composition
    (route1, l1, route2, l2) with route_i in {2,3} (p2/p3), l1,l2 >= 1,
    route1+l1+route2+l2 == target_length, quotiented by the *same*
    canonicalize_cyclic symmetry the real conflict records use -- so "every
    concrete clause is explained by exactly one derived template, and every
    derived template generates only genuine conflicts" can be checked by
    literal equality of keys, not by re-clustering.

    ``route1 == route2 == 3`` (two different p3 passages in one clause) is
    excluded: a completed graph selects exactly one linked-pair gadget ever
    (the exact-cover "exactly one gadget" constraint), so it has exactly
    one hub_L-hub_R joining edge in existence. Every p3 passage's route
    crosses that one edge, so two *different* p3 passages can never be
    simultaneously present in one simple cycle -- realizing both would
    require traversing that single edge twice. This is a global
    exact-cover fact, not a per-clause arithmetic one, so it cannot be
    derived from cycle-length arithmetic alone (`materialize_passages`
    tests each named passage with its own fresh synthetic hub pair and
    will happily "verify" a two-p3 clause -- soundly, but vacuously, since
    no real completion ever has two joining edges to draw from). Excluding
    it here matches the generator-level fix in
    `type_t_port_c16_passage_catalog.enumerate_m2_passage_conflicts` /
    `type_t_port_c16_passage_hypergraph.enumerate_passage_conflicts`
    (commit 8617422, "Exclude structurally-vacuous two-p3-passage
    supports").

    ``cross_branch=False``: both core segments forced onto one wildcard
    branch label (same-branch shapes). ``cross_branch=True``: the two core
    segments get *distinct* wildcard branch labels, and the two possible
    branch-role assignments are minimized over (a branch pair is unordered).
    """

    def make_cyclic(r1, l1, r2, l2, branch_a, branch_b):
        vtag = lambda br: ("bulk", br, "X")
        return [
            vtag(branch_a), ("core", "same", branch_a, l1), vtag(branch_a),
            ("passage", "p2" if r1 == 2 else "p3"),
            vtag(branch_b), ("core", "same", branch_b, l2), vtag(branch_b),
            ("passage", "p2" if r2 == 2 else "p3"),
        ]

    def key_for(r1, l1, r2, l2):
        if not cross_branch:
            return canonicalize_cyclic(make_cyclic(r1, l1, r2, l2, "BRANCH", "BRANCH"))
        k1 = canonicalize_cyclic(make_cyclic(r1, l1, r2, l2, "BX", "BY"))
        k2 = canonicalize_cyclic(make_cyclic(r1, l1, r2, l2, "BY", "BX"))
        return min(k1, k2)

    shapes: dict[tuple, list[tuple]] = defaultdict(list)
    for r1 in (2, 3):
        for r2 in (2, 3):
            if r1 == 3 and r2 == 3:
                continue
            core_total = target_length - r1 - r2
            if core_total < 2:
                continue
            for l1 in range(1, core_total):
                l2 = core_total - l1
                shapes[key_for(r1, l1, r2, l2)].append((r1, l1, r2, l2))
    return dict(shapes)


def enumerate_same_mode_abstract_shapes(target_length: int) -> dict:
    """Phase-3 first-principles derivation of the ``abstract_key`` same-mode
    template set directly -- i.e. using the *exact same* tag vocabulary
    (``generic_vertex_tag`` / ``wildcard_branch_names`` / ``canonicalize_cyclic``)
    the real ``build_conflict_record`` pipeline uses on catalog data, so
    "every concrete clause maps to exactly one derived template" can be
    checked by literal set equality against ``cluster()``'s
    ``by_abstract_key`` output, not by a parallel/re-implemented notion of
    sameness. Excludes route1==route2==3 -- see `enumerate_bulk_shapes`
    docstring: two different p3 passages can never coexist in one clause
    (exactly one joining edge ever exists in a completed graph)."""
    shapes: dict[tuple, list[tuple]] = defaultdict(list)
    for r1 in (2, 3):
        for r2 in (2, 3):
            if r1 == 3 and r2 == 3:
                continue
            core_total = target_length - r1 - r2
            if core_total < 2:
                continue
            for l1 in range(1, core_total):
                l2 = core_total - l1
                for branch_a, branch_b in (("W0", "W0"), ("W0", "W1")):
                    v = lambda br: ("generic", br, "")
                    cyclic = [
                        v(branch_a), ("core", "same", branch_a, l1), v(branch_a),
                        ("passage", "p2" if r1 == 2 else "p3"),
                        v(branch_b), ("core", "same", branch_b, l2), v(branch_b),
                        ("passage", "p2" if r2 == 2 else "p3"),
                    ]
                    candidates = wildcard_branch_names(cyclic)
                    key = min(canonicalize_cyclic(cand) for cand in candidates)
                    shapes[key].append((r1, l1, r2, l2, branch_a == branch_b))
    return dict(shapes)


def realized_shape_keys(cluster_result: dict) -> set:
    """The set of canonical keys that are actually bulk in a clustered
    catalog -- used to cross-check completeness/soundness of
    ``enumerate_bulk_shapes`` against real data."""
    return {k for k, v in cluster_result["by_key"].items() if v[0].is_bulk}


# ---------------------------------------------------------------------------
# Phase 2 (last step) / Phase 6: instantiate a template at fresh coordinates
# and independently verify the resulting passage pair is a genuine conflict.
# ---------------------------------------------------------------------------

def instantiate_same_branch(core: PortCore, branch: str, t0: int, r1: int, l1: int,
                             r2: int, l2: int, gap: int):
    """Builds one concrete instance of a same-branch bulk shape starting at
    branch-coordinate t0, with the second core segment starting `gap` past
    the end of the first (the free translation parameter the template does
    not constrain). Returns the passage `support` list (materialize_passages
    format) or None if the coordinates fall outside the branch."""
    j, a, c = core.j, core.a, core.c
    from type_t_port_coordinates import path_length, label_of

    length = path_length(branch, j, a, c)
    t1 = t0 + l1
    t2 = t1 + gap
    t3 = t2 + l2
    if not (0 < t0 < length and 0 < t1 < length and 0 < t2 < length and 0 < t3 < length):
        return None
    lbl = lambda t: label_of(branch, t, j, a, c)
    v = core.label_to_vertex
    kind1 = "p2" if r1 == 2 else "p3"
    kind2 = "p2" if r2 == 2 else "p3"
    support = [
        [kind1, [v[lbl(t1)], v[lbl(t2)]]],
        [kind2, [v[lbl(t3)], v[lbl(t0)]]],
    ]
    return support


def instantiate_cross_branch(core: PortCore, branch_a: str, branch_b: str,
                              t0: int, r1: int, l1: int, r2: int, l2: int, t2: int):
    """Cross-branch analogue: core segment 1 (length l1) lives on branch_a
    starting at t0; core segment 2 (length l2) lives on branch_b starting at
    t2 (a free, independently chosen coordinate on the other branch)."""
    j, a, c = core.j, core.a, core.c
    from type_t_port_coordinates import path_length, label_of

    len_a, len_b = path_length(branch_a, j, a, c), path_length(branch_b, j, a, c)
    t1 = t0 + l1
    t3 = t2 + l2
    if not (0 < t0 < len_a and 0 < t1 < len_a):
        return None
    if not (0 < t2 < len_b and 0 < t3 < len_b):
        return None
    lbl_a = lambda t: label_of(branch_a, t, j, a, c)
    lbl_b = lambda t: label_of(branch_b, t, j, a, c)
    v = core.label_to_vertex
    kind1 = "p2" if r1 == 2 else "p3"
    kind2 = "p2" if r2 == 2 else "p3"
    support = [
        [kind1, [v[lbl_a(t1)], v[lbl_b(t2)]]],
        [kind2, [v[lbl_b(t3)], v[lbl_a(t0)]]],
    ]
    return support


def verify_support(core: PortCore, support, target_length: int) -> bool:
    from type_t_port_passages import materialize_passages
    from type_t_port_multipole_check import edge_path_cycle

    support_tuples = [(kind, tuple(uv)) for kind, uv in support]
    _graph, adjacency = materialize_passages(core, support_tuples)
    cycle = edge_path_cycle(adjacency, target_length)
    return cycle is not None


# ---------------------------------------------------------------------------
# Phase 5: general-m infrastructure (for ingesting the sibling agent's
# C16 m=3,4,5 output later, without redoing the m=2 template machinery).
#
# Everything above (vertex_tag / generic_vertex_tag / core_path_descriptor /
# canonicalize_cyclic / wildcard_branch_names) is already m-agnostic -- it
# operates on one core-path run or one pair of labels at a time. The only
# m=2-specific piece is `decode_m2_witness` (which hard-codes the
# "core,hub,core,hub" shape) and the fixed rotate-by-2/reflect symmetry
# group used inline in `canonicalize_cyclic`. This section generalizes both
# to arbitrary m, and is self-tested by checking it reproduces the m=2
# results bit-for-bit on the real C8/C16 catalogs.
# ---------------------------------------------------------------------------

def decode_general_witness(core: PortCore, conflict: dict) -> dict:
    """General-m witness decoder: returns the cyclic list of core runs and
    hub runs (2m segments total, m of each, alternating), and the list of
    m passages (endpoints + kind) in cyclic order. Works for any m >= 1 (a
    single-hub-passage m=1 witness would be `[core_run, hub_run]` -- not
    reachable per the Phase 1 proof `m>=2`, but the code does not assume
    m=2 anywhere)."""
    segs = split_witness(core, conflict["witness"])
    kinds = [k for k, _ in segs]
    if len(kinds) % 2 != 0 or kinds != ["core", "hub"] * (len(kinds) // 2):
        raise ValueError(f"not a clean alternating core/hub witness: {kinds}")
    m = len(kinds) // 2
    core_runs = [segs[2 * i][1] for i in range(m)]
    hub_runs = [segs[2 * i + 1][1] for i in range(m)]
    passages = []
    support_kind = {tuple(sorted(uv)): kind for kind, uv in conflict["support"]}
    for i in range(m):
        u, v = core_runs[i][-1], core_runs[(i + 1) % m][0]
        key = tuple(sorted((u, v)))
        if key not in support_kind:
            raise AssertionError(f"witness passage {key} not found in support {support_kind}")
        passages.append({"endpoints": (u, v), "kind": support_kind[key]})
    if len(support_kind) != m:
        raise AssertionError(f"support has {len(support_kind)} entries but witness implies m={m}")
    return {"m": m, "core_runs": core_runs, "hub_runs": hub_runs, "passages": passages}


def build_cyclic_tokens(core: PortCore, decoded: dict, tag_fn=vertex_tag) -> list[tuple]:
    """General-m analogue of the [V0,S0,V1,S1,...] token list built inline
    in `build_conflict_record` / `abstracted_key` for m=2. `tag_fn` is
    either `vertex_tag` (raw, offset-preserving) or a `(label) -> tag`
    callable like `generic_vertex_tag` (branch-name-preserving, offset-
    dropped) -- passed as a 1-arg wrapper by the caller for the latter."""
    j, a, c = core.j, core.a, core.c
    labels = core.labels
    m = decoded["m"]
    tokens = []
    for i in range(m):
        run = decoded["core_runs"][i]
        v_start = tag_fn(labels[run[0]], j, a, c) if tag_fn is vertex_tag else tag_fn(labels[run[0]])
        s_core = ("core",) + core_path_descriptor(run, labels, j, a, c)
        v_end = tag_fn(labels[run[-1]], j, a, c) if tag_fn is vertex_tag else tag_fn(labels[run[-1]])
        s_passage = ("passage", decoded["passages"][i]["kind"])
        tokens.extend([v_start, s_core, v_end, s_passage])
    return tokens


def canonicalize_cyclic_general(tokens: list[tuple], m: int) -> tuple:
    """General-m symmetry group: dihedral of order 2m (rotate by 2 -- one
    full core+hub segment pair -- composed with reflection), acting on a
    4m-length token list [V,S_core,V,S_passage]*m. Reduces to
    `canonicalize_cyclic`'s order-4 group when m=2."""

    def reversed_tokens(seq):
        rev = [reverse_segment(t) if t[0] == "core" else t for t in seq[::-1]]
        return rev[1:] + rev[:1]

    candidates = []
    for base in (tokens, reversed_tokens(tokens)):
        for r in range(0, 4 * m, 4):
            rotated = base[r:] + base[:r]
            candidates.append(tuple(_sanitize(t) for t in rotated))
    return min(candidates)


def general_conflict_keys(core: PortCore, conflict: dict) -> dict:
    """Drop-in general-m replacement for the raw/abstract key pair computed
    in `build_conflict_record`, for future m=3,4,5 ingestion. Returns both
    the raw (offset-preserving) key and, for m=2 only (higher-m branch
    wildcarding is a Phase-7+ extension -- see the module docstring/manifest
    for exactly where to resume), the branch-abstracted key."""
    decoded = decode_general_witness(core, conflict)
    raw_tokens = build_cyclic_tokens(core, decoded, tag_fn=vertex_tag)
    raw_key = canonicalize_cyclic_general(raw_tokens, decoded["m"])
    result = {"m": decoded["m"], "raw_key": raw_key}
    if decoded["m"] == 2:
        generic_tag_fn = lambda label: generic_vertex_tag(label)
        generic_tokens = build_cyclic_tokens(core, decoded, tag_fn=generic_tag_fn)
        candidates = wildcard_branch_names(generic_tokens)
        result["abstract_key"] = min(
            canonicalize_cyclic_general(cand, decoded["m"]) for cand in candidates
        )
    return result


def self_test_general_m2_matches_specialized(core: PortCore, conflicts: list[dict]) -> dict:
    """Regression check: `general_conflict_keys` must reproduce exactly the
    same raw/abstract keys as the specialized m=2 `build_conflict_record`
    pipeline, on real catalog data."""
    mismatches = 0
    checked = 0
    for conflict in conflicts:
        record = build_conflict_record(core, conflict)
        general = general_conflict_keys(core, conflict)
        checked += 1
        if general["raw_key"] != record.canonical_key or general["abstract_key"] != record.abstract_key:
            mismatches += 1
    return {"status": "PROVED" if mismatches == 0 else "FAILED", "checked": checked, "mismatches": mismatches}


def load_c8_catalog(path: Path):
    with gzip.open(path) as f:
        data = json.load(f)
    params = data["parameters"]
    j, a, c = params["j"], params["a"], params["c"]
    conflicts = data["lengths"]["8"]["conflicts"]
    return (j, a, c), conflicts


def load_c16_m2_catalog(path: Path):
    with gzip.open(path) as f:
        data = json.load(f)
    params = data["parameters"]
    j, a, c = params["j"], params["a"], params["c"]
    return (j, a, c), data["conflicts"]


# ---------------------------------------------------------------------------
# Clustering / reporting
# ---------------------------------------------------------------------------

def cluster(core: PortCore, conflicts: list[dict]) -> dict:
    records = [build_conflict_record(core, conf) for conf in conflicts]
    by_key: dict[tuple, list[ConflictRecord]] = defaultdict(list)
    by_abstract_key: dict[tuple, list[ConflictRecord]] = defaultdict(list)
    for rec in records:
        by_key[rec.canonical_key].append(rec)
        by_abstract_key[rec.abstract_key].append(rec)
    bulk_keys = {k for k, v in by_key.items() if v[0].is_bulk}

    same_abstract = {k: v for k, v in by_abstract_key.items() if not v[0].is_crossing}
    cross_abstract = {k: v for k, v in by_abstract_key.items() if v[0].is_crossing}

    return {
        "records": records,
        "by_key": dict(by_key),
        "by_abstract_key": dict(by_abstract_key),
        "n_clauses": len(records),
        "n_templates": len(by_key),
        "n_bulk_templates": len(bulk_keys),
        "n_boundary_templates": len(by_key) - len(bulk_keys),
        "n_bulk_clauses": sum(len(v) for k, v in by_key.items() if k in bulk_keys),
        "n_boundary_clauses": sum(len(v) for k, v in by_key.items() if k not in bulk_keys),
        "multiplicity_distribution": Counter(len(v) for v in by_key.values()),
        "n_abstract_templates": len(by_abstract_key),
        "n_same_mode_clauses": sum(len(v) for v in same_abstract.values()),
        "n_same_mode_abstract_templates": len(same_abstract),
        "n_crossing_clauses": sum(len(v) for v in cross_abstract.values()),
        "n_crossing_abstract_templates": len(cross_abstract),
    }


def summarize_instance(path: Path, loader) -> dict:
    (j, a, c), conflicts = loader(path)
    core = build_core(j, a, c)
    result = cluster(core, conflicts)
    return {
        "path": str(path),
        "parameters": {"j": j, "a": a, "c": c},
        "n_clauses": result["n_clauses"],
        "n_templates": result["n_templates"],
        "n_bulk_templates": result["n_bulk_templates"],
        "n_boundary_templates": result["n_boundary_templates"],
        "n_bulk_clauses": result["n_bulk_clauses"],
        "n_boundary_clauses": result["n_boundary_clauses"],
        "multiplicity_distribution": {
            str(k): v for k, v in sorted(result["multiplicity_distribution"].items())
        },
        "n_abstract_templates": result["n_abstract_templates"],
        "n_same_mode_clauses": result["n_same_mode_clauses"],
        "n_same_mode_abstract_templates": result["n_same_mode_abstract_templates"],
        "n_crossing_clauses": result["n_crossing_clauses"],
        "n_crossing_abstract_templates": result["n_crossing_abstract_templates"],
        "_result": result,
    }


C8_CATALOGS = [
    Path("data/type_t_port_c16_passages/j4_a55_c7_phi48_passages.json.gz"),
    Path("data/type_t_port_c16_passages/j4_a2_c2_phi48_passages.json.gz"),
    Path("data/type_t_port_c16_passages/j4_a28_c4_phi48_passages.json.gz"),
]

C16_M2_CATALOG = Path("data/type_t_port_c16_passages/j4_a55_c7_c16_passages_m2only.json.gz")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["c8", "c16m2"], default="c8")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.mode == "c8":
        summaries = [summarize_instance(p, load_c8_catalog) for p in C8_CATALOGS]
    else:
        summaries = [summarize_instance(C16_M2_CATALOG, load_c16_m2_catalog)]

    for s in summaries:
        s.pop("_result", None)

    payload = {"mode": args.mode, "instances": summaries}
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
