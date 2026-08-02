#!/usr/bin/env python3
"""Kernel/cycle-space proof that the bare core's 35 affine cycle-length
forms are complete for EVERY valid (j,a,c), not just the tested j=4,5,6.

``build_core(j,a,c)`` (``type_t_port_core_export.py``) always wires the
same 13 anchor vertices together via the same 19 named subdivided paths;
only 4 of the 19 path *lengths* depend on ``j``/``a``/``c``
(``A_left=a-1``, ``A_right=4Y-8-a``, ``C_left=c-1``, ``C_right=Y-8-c``,
``Y=2^j``), the topology itself never changes. Two of the 13 anchors,
``u_x`` and ``u_y``, are themselves degree-2 pass-through points (confirmed
directly against a built core below) -- each pair ``u_x_r_x``+``u_x_s_x``
(resp. ``u_y_r_y``+``u_y_s_y``) is really one subdivided kernel edge
``r_x``-``s_x`` (resp. ``r_y``-``s_y``) of length 2, running in parallel
with the length-7 ``A_middle``/``C_middle`` edge between the same pair.

Suppressing those two degree-2 anchors gives the true **kernel multigraph**:
**11 vertices, 17 edges, cyclomatic rank exactly 7** (``17-11+1=7``,
matching the documented ``m0-n0+1=7``). This module builds that kernel
directly from ``build_core``'s topology (independent of ``j``/``a``/``c``
by construction -- there is no numeric fitting anywhere in this file),
enumerates all ``2^7=128`` binary cycle-space vectors via a spanning tree
and its 7 fundamental cycles, classifies each nonzero vector as a genuine
simple cycle or not (connected edge-support, every included vertex has
degree exactly 2 within it) -- a purely topological question, answerable
once, independent of the actual edge lengths -- and computes each valid
cycle's length **symbolically** as ``(const, Y_coef, a_coef, c_coef)``
rather than by plugging in numbers.

Result (this module's ``self_test``): **exactly 61 valid simple cycles**
(matching the documented count exactly), **every one has ``a_coef=0`` and
``c_coef=0``** (proving, not just observing at 9 sampled (a,c) pairs, that
every cycle's length is a pure function of ``Y`` alone -- the ``a``/``c``
contributions always cancel), and the resulting 35 distinct
``(Y_coef, const)`` pairs with their multiplicities are **exactly** the 35
forms independently fit from the j=4,5,6 spectra in
``type_t_port_core_affine_dyadic_check.py`` -- set equality, multiplicities
included, with zero mismatches.

Combined with that module's 2-adic proof that none of the 35 forms is ever
a power of two for any j>=4, this closes the completeness gap: **the bare
core H(j,a,c) avoids every dyadic cycle length, for every valid j>=4 and
every valid a,c, PROVED** (not conditional, not sampled).
"""

from __future__ import annotations

from collections import Counter, deque

from type_t_port_core_export import build_core, valid_parameters


# (left anchor, right anchor, name, symbolic length as (const, Y_coef, a_coef, c_coef))
# i.e. length = const + Y_coef*Y + a_coef*a + c_coef*c
KERNEL_EDGES: list[tuple[str, str, str, tuple[int, int, int, int]]] = [
    ("z0", "w_AC", "prefix_AC", (1, 0, 0, 0)),
    ("w_AC", "r_x", "A_left", (-1, 0, 1, 0)),
    ("r_x", "s_x", "A_middle", (7, 0, 0, 0)),
    ("r_x", "s_x", "u_x_bridge", (2, 0, 0, 0)),  # u_x_r_x(1) + u_x_s_x(1), u_x suppressed
    ("s_x", "xprime", "A_right", (-8, 4, -1, 0)),
    ("w_AC", "r_y", "C_left", (-1, 0, 0, 1)),
    ("r_y", "s_y", "C_middle", (7, 0, 0, 0)),
    ("r_y", "s_y", "u_y_bridge", (2, 0, 0, 0)),  # u_y_r_y(1) + u_y_s_y(1), u_y suppressed
    ("s_y", "yprime", "C_right", (-8, 1, 0, -1)),
    ("z0", "w_BD", "prefix_BD", (1, 0, 0, 0)),
    ("w_BD", "xprime", "B_right", (3, 0, 0, 0)),
    ("w_BD", "yprime", "D_right", (3, 0, 0, 0)),
    ("z0", "x", "z0x", (1, 0, 0, 0)),
    ("x", "xprime", "xxprime", (1, 0, 0, 0)),
    ("z0", "y", "z0y", (1, 0, 0, 0)),
    ("y", "yprime", "yyprime", (1, 0, 0, 0)),
    ("x", "y", "xy", (1, 0, 0, 0)),
]


def verify_u_bridge_suppression() -> None:
    """Confirm u_x, u_y are really degree-2 in a built core, i.e. that
    merging their two incident paths into one kernel edge is legitimate."""
    core = build_core(4, 55, 7)
    adjacency = core.adjacency()
    for name in ("u_x", "u_y"):
        vertex = core.label_to_vertex[name]
        degree = len(adjacency[vertex])
        if degree != 2:
            raise AssertionError(f"{name} has degree {degree}, expected 2 -- bridge suppression is invalid")


# ---------------------------------------------------------------------------
# Independent cross-check: KERNEL_EDGES above was hand-transcribed directly
# from build_core's add_path(...) arguments -- the same derivation style as
# coordinates.py::PATH_SPEC (just with u_x/u_y already pre-suppressed by
# hand). To make the "kernel topology is (j,a,c)-independent" claim and the
# "13 anchors vs 11 branch vertices, 19 paths vs 17 kernel edges" reconcile-
# ment genuinely checked rather than asserted, this section derives the
# kernel a SECOND way with no hardcoded topology at all: it materializes
# build_core(j,a,c), computes raw vertex degree from the edge list, keeps
# only degree!=2 vertices as kernel vertices, and walks each degree-2 chain
# generically (a topological-minor "suppress degree-2 vertices" pass that
# would work on any graph) to discover kernel edges -- then checks this
# agrees with KERNEL_EDGES, exactly, at several distinct (j,a,c) instances
# (spanning j=4,5,6, extreme and interior a,c).
# ---------------------------------------------------------------------------

def kernel_from_materialized_graph(j: int, a: int, c: int):
    """Purely graph-theoretic re-derivation: no reference to KERNEL_EDGES,
    ANCHORS' meaning, or PATH_SPEC. Returns (vertex_set, edge_list) where
    edge_list items are (u_label, v_label, length) with u_label<v_label."""
    core = build_core(j, a, c)
    n = core.order
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in core.edges:
        adj[u].append(v)
        adj[v].append(u)
    degree = [len(adj[x]) for x in range(n)]
    branch = [x for x in range(n) if degree[x] != 2]
    branch_set = set(branch)

    visited: set[frozenset] = set()
    edges_out: list[tuple[str, str, int]] = []
    for v in branch:
        for w in adj[v]:
            e0 = frozenset((v, w))
            if e0 in visited:
                continue
            visited.add(e0)
            prev, cur, length = v, w, 1
            while cur not in branch_set:
                nxts = [x for x in adj[cur] if x != prev]
                if len(nxts) != 1:
                    raise AssertionError(f"vertex {cur} degree-2 chain broken: {nxts}")
                nxt = nxts[0]
                visited.add(frozenset((cur, nxt)))
                prev, cur, length = cur, nxt, length + 1
            edges_out.append((core.labels[v], core.labels[cur], length))
    return {core.labels[x] for x in branch}, edges_out


def cross_validate_kernel_topology() -> dict:
    """Checks that (a) the hand-transcribed KERNEL_EDGES table and (b) the
    graph-degree-derived kernel_from_materialized_graph agree exactly --
    same vertex set, same edge-endpoint multiset, and (numerically, at each
    tested instance) the same edge lengths -- across several distinct
    (j,a,c). This is the concrete check behind the claim that the kernel
    topology never changes with j/a/c, and confirms the u_x/u_y (13 anchors
    vs 11 branch vertices) and 19-paths-vs-17-kernel-edges reconciliations
    against actual materialized adjacency, not just by construction."""
    instances = [
        (4, 55, 7), (4, 2, 2), (4, 28, 4),
        (5, 40, 10), (5, 2, 2), (5, 119, 23),
        (6, 2, 2), (6, 247, 55), (6, 120, 28),
    ]
    for j, a, c in instances:
        valid_parameters(j, a, c)

    hand_endpoint_multiset = sorted(tuple(sorted((u, v))) for u, v, _n, _l in KERNEL_EDGES)

    reports = []
    reference_signature = None
    for j, a, c in instances:
        Y = 1 << j
        mat_vertices, mat_edges = kernel_from_materialized_graph(j, a, c)
        mat_endpoint_multiset = sorted(tuple(sorted((u, v))) for u, v, _l in mat_edges)

        if mat_endpoint_multiset != hand_endpoint_multiset:
            raise AssertionError(
                f"(j={j},a={a},c={c}): materialized-graph kernel edge "
                f"endpoints disagree with hand-transcribed KERNEL_EDGES:\n"
                f"materialized={mat_endpoint_multiset}\nhand={hand_endpoint_multiset}"
            )
        if mat_vertices != set(kernel_vertices()):
            raise AssertionError(
                f"(j={j},a={a},c={c}): materialized-graph kernel vertex set "
                f"{mat_vertices} disagrees with hand-derived {set(kernel_vertices())}"
            )

        # numeric length cross-check: every materialized edge's length must
        # match some KERNEL_EDGES entry evaluated at this (Y,a,c), matched
        # by endpoint pair (there are two parallel r_x-s_x and two parallel
        # r_y-s_y entries, so match multiset-wise per endpoint pair).
        hand_lengths_by_pair: dict[tuple[str, str], list[int]] = {}
        for u, v, _n, (const, yc, ac, cc) in KERNEL_EDGES:
            key = tuple(sorted((u, v)))
            length = const + yc * Y + ac * a + cc * c
            hand_lengths_by_pair.setdefault(key, []).append(length)
        mat_lengths_by_pair: dict[tuple[str, str], list[int]] = {}
        for u, v, length in mat_edges:
            key = tuple(sorted((u, v)))
            mat_lengths_by_pair.setdefault(key, []).append(length)
        for key in hand_lengths_by_pair:
            if sorted(hand_lengths_by_pair[key]) != sorted(mat_lengths_by_pair.get(key, [])):
                raise AssertionError(
                    f"(j={j},a={a},c={c}): length mismatch on {key}: "
                    f"hand={sorted(hand_lengths_by_pair[key])} "
                    f"materialized={sorted(mat_lengths_by_pair.get(key, []))}"
                )

        signature = (frozenset(mat_vertices), tuple(mat_endpoint_multiset))
        if reference_signature is None:
            reference_signature = signature
        elif signature != reference_signature:
            raise AssertionError(f"(j={j},a={a},c={c}): abstract kernel signature differs from reference")

        reports.append({
            "j": j, "a": a, "c": c,
            "num_kernel_vertices": len(mat_vertices),
            "num_kernel_edges": len(mat_edges),
        })

    return {
        "status": "PROVED",
        "instances_checked": reports,
        "topology_identical_across_all_instances": True,
        "agrees_with_hand_transcribed_KERNEL_EDGES": True,
    }


def kernel_vertices() -> list[str]:
    verts = set()
    for u, v, _name, _length in KERNEL_EDGES:
        verts.add(u)
        verts.add(v)
    return sorted(verts)


def _add(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(x + y for x, y in zip(a, b))


def spanning_tree_and_fundamental_cycles():
    vertices = kernel_vertices()
    parent = {v: v for v in vertices}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree_edges: list[int] = []
    nontree_edges: list[int] = []
    for index, (u, v, _name, _length) in enumerate(KERNEL_EDGES):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            tree_edges.append(index)
        else:
            nontree_edges.append(index)

    tree_adjacency: dict[str, list[tuple[str, int]]] = {v: [] for v in vertices}
    for index in tree_edges:
        u, v, _name, _length = KERNEL_EDGES[index]
        tree_adjacency[u].append((v, index))
        tree_adjacency[v].append((u, index))

    def tree_path_edges(start: str, end: str) -> set[int]:
        parent_edge: dict[str, int | None] = {start: None}
        parent_node: dict[str, str | None] = {start: None}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current == end:
                break
            for neighbor, edge_index in tree_adjacency[current]:
                if neighbor not in parent_edge:
                    parent_edge[neighbor] = edge_index
                    parent_node[neighbor] = current
                    queue.append(neighbor)
        path: set[int] = set()
        node = end
        while node != start:
            edge_index = parent_edge[node]
            path.add(edge_index)
            node = parent_node[node]
        return path

    fundamental_cycles: list[set[int]] = []
    for index in nontree_edges:
        u, v, _name, _length = KERNEL_EDGES[index]
        fundamental_cycles.append(tree_path_edges(u, v) | {index})

    return vertices, tree_edges, nontree_edges, fundamental_cycles


def is_simple_cycle(edge_indices: set[int]) -> bool:
    if not edge_indices:
        return False
    degree: Counter[str] = Counter()
    for index in edge_indices:
        u, v, _name, _length = KERNEL_EDGES[index]
        degree[u] += 1
        degree[v] += 1
    if any(d != 2 for d in degree.values()):
        return False
    adjacency: dict[str, list[str]] = {v: [] for v in degree}
    for index in edge_indices:
        u, v, _name, _length = KERNEL_EDGES[index]
        adjacency[u].append(v)
        adjacency[v].append(u)
    start = next(iter(degree))
    seen = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen == set(degree)


def enumerate_kernel_cycles() -> list[tuple[frozenset[int], tuple[int, int, int, int]]]:
    """Every valid simple kernel cycle, as (edge-index set, symbolic length)."""
    _vertices, _tree, _nontree, fundamental_cycles = spanning_tree_and_fundamental_cycles()
    rank = len(fundamental_cycles)
    results = []
    for mask in range(1, 1 << rank):
        edge_set: set[int] = set()
        for bit in range(rank):
            if mask & (1 << bit):
                edge_set ^= fundamental_cycles[bit]
        if is_simple_cycle(edge_set):
            total = (0, 0, 0, 0)
            for index in edge_set:
                _u, _v, _name, length = KERNEL_EDGES[index]
                total = _add(total, length)
            results.append((frozenset(edge_set), total))
    return results


def verify_degree_distribution_reconciliation() -> dict:
    """Reconciles the documented 13-anchor / 19-path description with the
    11-vertex / 17-edge kernel: computes the raw degree of every one of the
    13 named ANCHORS in a materialized core and checks it against the
    documented degree distribution n2=5Y-4 (includes u_x,u_y plus all
    path-internal vertices), n3=10, n4=1 (type_t_port_completion.md
    Section 1). The 11 kernel vertices are exactly the deg>=3 anchors
    (1 deg-4 + 10 deg-3); u_x,u_y are the 2 anchors that fall inside n2
    instead, which is why they get suppressed into the two parallel
    "*_bridge" kernel edges rather than appearing as kernel vertices."""
    core = build_core(4, 55, 7)
    adjacency = core.adjacency()
    degrees = {name: len(adjacency[core.label_to_vertex[name]]) for name in
               ("z0", "x", "xprime", "y", "yprime", "w_AC", "w_BD",
                "r_x", "s_x", "r_y", "s_y", "u_x", "u_y")}
    deg4 = [n for n, d in degrees.items() if d == 4]
    deg3 = [n for n, d in degrees.items() if d == 3]
    deg2 = [n for n, d in degrees.items() if d == 2]
    if deg4 != ["z0"]:
        raise AssertionError(f"expected exactly z0 at degree 4, got {deg4}")
    if len(deg3) != 10:
        raise AssertionError(f"expected 10 anchors at degree 3, got {deg3}")
    if sorted(deg2) != ["u_x", "u_y"]:
        raise AssertionError(f"expected exactly u_x,u_y at degree 2 among anchors, got {deg2}")
    if set(deg4) | set(deg3) != set(kernel_vertices()):
        raise AssertionError("deg>=3 anchors do not match the 11 kernel vertices exactly")
    return {
        "degree_4_anchors": deg4,
        "degree_3_anchors": sorted(deg3),
        "degree_2_anchors_ie_suppressed_into_kernel": sorted(deg2),
        "matches_11_kernel_vertices": True,
        "sum_d_minus_2_over_branch_anchors": sum(d - 2 for d in degrees.values() if d != 2),
    }


def self_test() -> dict:
    verify_u_bridge_suppression()
    degree_reconciliation = verify_degree_distribution_reconciliation()
    topology_cross_check = cross_validate_kernel_topology()

    vertices = kernel_vertices()
    rank = len(KERNEL_EDGES) - len(vertices) + 1
    if rank != 7:
        raise AssertionError(f"expected rank 7, got {rank}")

    cycles = enumerate_kernel_cycles()
    if len(cycles) != 61:
        raise AssertionError(f"expected 61 simple kernel cycles, got {len(cycles)}")

    form_counts: Counter[tuple[int, int]] = Counter()
    for _edges, (const, y_coef, a_coef, c_coef) in cycles:
        if a_coef != 0 or c_coef != 0:
            raise AssertionError(f"cycle length depends on a or c: {(const, y_coef, a_coef, c_coef)}")
        form_counts[(y_coef, const)] += 1

    from type_t_port_core_affine_dyadic_check import fit_affine_forms

    fitted = fit_affine_forms()
    fitted_forms = {(a, b): m for a, b, m in fitted}
    kernel_forms = dict(form_counts)
    if kernel_forms != fitted_forms:
        raise AssertionError(
            f"kernel-derived forms disagree with the empirically-fit forms: "
            f"only-kernel={set(kernel_forms) - set(fitted_forms)} "
            f"only-fitted={set(fitted_forms) - set(kernel_forms)} "
            f"mismatched-multiplicity={{k: (kernel_forms.get(k), fitted_forms.get(k)) for k in set(kernel_forms) | set(fitted_forms) if kernel_forms.get(k) != fitted_forms.get(k)}}"
        )

    return {
        "status": "PROVED",
        "kernel_vertices": len(vertices),
        "kernel_edges": len(KERNEL_EDGES),
        "rank": rank,
        "simple_cycles": len(cycles),
        "distinct_forms": len(form_counts),
        "matches_empirical_fit": True,
        "degree_distribution_reconciliation": degree_reconciliation,
        "independent_topology_cross_check": topology_cross_check,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(self_test(), indent=2))
