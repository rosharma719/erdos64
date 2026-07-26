"""T8/R1/T8R helpers and finite relaxed-closure verification.

The mathematical proofs live in ``two_cut.md``.  This module makes their
local conclusions executable:

* edge deletion only shrinks cycle and terminal-path spectra;
* a real edge in an R-skeleton may be deleted without destroying the
  closure's 2-connectivity (R1);
* therefore an R-real edge of a minimal Type-A gadget must meet one of the
  exact degree-critical locations in T8R.

The SPQR convention matches ``one_pole.md`` and the installed ``spqrtree``
package: Q nodes are suppressed where possible; skeleton edges are marked
real/virtual; and a virtual edge represents a pertinent two-terminal graph
whose closure by its pole edge is 2-connected.
"""
from __future__ import annotations

import argparse
import itertools
import random
import subprocess
import sys
from collections import Counter

import networkx as nx
import spqrtree

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from bridge_closure_search import find_J_candidates
from brute_spqr import decompose as brute_spqr_decompose
from cycle_detect import from_edges, has_cycle_len_dfs, powers_of_two_up_to


def edge_key(u, v):
    """Stable undirected edge key for integer-labelled research fixtures."""
    return tuple(sorted((u, v)))


def is_2connected(graph: nx.Graph) -> bool:
    return graph.number_of_nodes() >= 3 and nx.is_biconnected(graph)


def dyadic_cycle_spectrum(graph: nx.Graph) -> frozenset[int]:
    vertices = sorted(graph.nodes())
    remap = {vertex: index for index, vertex in enumerate(vertices)}
    simple = from_edges(
        len(vertices),
        [(remap[u], remap[v]) for u, v in graph.edges()],
    )
    return frozenset(
        length for length in powers_of_two_up_to(len(vertices))
        if has_cycle_len_dfs(simple, length)
    )


def terminal_path_spectrum(graph: nx.Graph, x, y) -> frozenset[int]:
    if x not in graph or y not in graph or not nx.has_path(graph, x, y):
        return frozenset()
    return frozenset(
        len(path) - 1 for path in nx.all_simple_paths(graph, x, y)
    )


def sumset(left, right) -> frozenset[int]:
    return frozenset(a + b for a in left for b in right)


def degree_condition_failures(graph: nx.Graph, x, y) -> tuple[str, ...]:
    """Return the exact Type-A degree hypotheses violated by ``graph``."""
    failures = []
    if graph.degree(x) != 1:
        failures.append("x_terminal_degree")
    if graph.degree(y) < 1:
        failures.append("y_terminal_degree")
    if any(graph.degree(v) < 3 for v in graph if v not in (x, y)):
        failures.append("internal_minimum_degree")
    return tuple(failures)


def t8r_edge_is_degree_critical(graph_b: nx.Graph, x, y, edge) -> bool:
    """The exact T8R incidence condition for one edge of B."""
    u, v = edge
    return (
        x in edge
        or any(vertex not in (x, y) and graph_b.degree(vertex) == 3
               for vertex in edge)
        or (y in edge and graph_b.degree(y) == 1)
    )


def edge_deletion_audit(graph_b: nx.Graph, x, y, edge) -> dict:
    """Audit every T6 hypothesis after deleting one edge of B.

    The subset assertions are the executable monotonicity part of T8.  The
    result does not assume that ``graph_b`` is itself a gadget, which makes it
    useful for adversarial fixtures and relaxed-census diagnostics.
    """
    u, v = edge
    if not graph_b.has_edge(u, v):
        raise ValueError(f"edge {edge!r} is not in B")
    if graph_b.has_edge(x, y):
        raise ValueError("T6 requires xy to be absent from B")

    smaller = graph_b.copy()
    smaller.remove_edge(u, v)
    closure = smaller.copy()
    closure.add_edge(x, y)

    cycles_before = dyadic_cycle_spectrum(graph_b)
    cycles_after = dyadic_cycle_spectrum(smaller)
    paths_before = terminal_path_spectrum(graph_b, x, y)
    paths_after = terminal_path_spectrum(smaller, x, y)
    sums_before = sumset(paths_before, paths_before)
    sums_after = sumset(paths_after, paths_after)

    return {
        "edge": edge_key(u, v),
        "degree_failures": degree_condition_failures(smaller, x, y),
        "closure_2connected": is_2connected(closure),
        "simple": not nx.number_of_selfloops(smaller),
        "terminal_edge_absent": not smaller.has_edge(x, y),
        "internal_cycle_spectrum_before": cycles_before,
        "internal_cycle_spectrum_after": cycles_after,
        "internal_cycles_monotone": cycles_after <= cycles_before,
        "terminal_path_spectrum_before": paths_before,
        "terminal_path_spectrum_after": paths_after,
        "terminal_paths_monotone": paths_after <= paths_before,
        "self_sum_before": sums_before,
        "self_sum_after": sums_after,
        "self_sums_monotone": sums_after <= sums_before,
    }


def _build_spqr_tree(graph: nx.Graph, ordered_edges):
    multigraph = spqrtree.MultiGraph()
    for u, v in ordered_edges:
        multigraph.add_edge(u, v)
    return spqrtree.SPQRTree(multigraph)


def _skeleton_simple_graph(node) -> nx.Graph:
    skeleton = nx.Graph()
    skeleton.add_nodes_from(node.skeleton.vertices)
    skeleton.add_edges_from((edge.u, edge.v) for edge in node.skeleton.edges)
    return skeleton


def spqr_validation_errors(tree, graph: nx.Graph) -> list[str]:
    """Validate the package output against the reduced-SPQR definition.

    ``spqrtree==0.1.2`` can be insertion-order-sensitive.  In particular it
    sometimes labels a connectivity-2 skeleton as R.  No R1/T8R conclusion is
    allowed to use a tree until this independent structural validator passes.
    """
    errors = []
    nodes = tree.nodes()
    real_edges = []
    for index, node in enumerate(nodes):
        simple = _skeleton_simple_graph(node)
        kind = node.type.value
        if nx.number_of_selfloops(simple):
            errors.append(f"node {index} has a skeleton loop")
        if kind == "R":
            if simple.number_of_nodes() < 4 or not nx.is_connected(simple):
                errors.append(f"R node {index} is too small or disconnected")
            elif nx.node_connectivity(simple) < 3:
                errors.append(f"R node {index} is not 3-connected")
            if simple.number_of_edges() != len(node.skeleton.edges):
                errors.append(f"R node {index} has parallel skeleton edges")
        elif kind == "S":
            if (simple.number_of_nodes() < 3
                    or simple.number_of_edges() != simple.number_of_nodes()
                    or any(degree != 2 for _, degree in simple.degree())):
                errors.append(f"S node {index} is not a simple cycle")
        elif kind == "P":
            if (node.skeleton.num_vertices() != 2
                    or node.skeleton.num_edges() < 3):
                errors.append(f"P node {index} is not a bond of size at least 3")
        elif kind == "Q":
            if (node.skeleton.num_vertices() != 2
                    or node.skeleton.num_edges() != 1):
                errors.append(f"Q node {index} is not a single edge")
        else:
            errors.append(f"node {index} has unknown type {kind!r}")

        expected_virtual = len(node.children) + int(node.parent is not None)
        actual_virtual = sum(edge.virtual for edge in node.skeleton.edges)
        if actual_virtual != expected_virtual:
            errors.append(
                f"node {index} has {actual_virtual} virtual edges, "
                f"expected {expected_virtual}"
            )
        real_edges.extend(
            edge_key(edge.u, edge.v)
            for edge in node.skeleton.edges if not edge.virtual
        )
        if node.parent is not None and node.parent.type.value == kind:
            errors.append(f"adjacent reduced nodes {index}/parent share type {kind}")

    expected_real = sorted(edge_key(u, v) for u, v in graph.edges())
    if sorted(real_edges) != expected_real:
        errors.append("real skeleton edges do not partition the host edges")
    return errors


def validated_spqr_tree(graph: nx.Graph):
    """Return a definition-validated reduced tree and attempt metadata."""
    if not is_2connected(graph):
        raise ValueError("SPQR decomposition requires a simple 2-connected graph")
    base = sorted(edge_key(u, v) for u, v in graph.edges())
    orderings = [("sorted", base), ("reverse_sorted", list(reversed(base)))]
    for offset in range(1, len(base)):
        orderings.append((f"rotation_{offset}", base[offset:] + base[:offset]))
    for seed in range(16):
        shuffled = base[:]
        random.Random(seed).shuffle(shuffled)
        orderings.append((f"shuffle_seed_{seed}", shuffled))

    attempted = []
    for name, ordered_edges in orderings:
        tree = _build_spqr_tree(graph, ordered_edges)
        errors = spqr_validation_errors(tree, graph)
        attempted.append({"ordering": name, "errors": errors})
        if not errors:
            return tree, {
                "package": "spqrtree==0.1.2",
                "validated": True,
                "accepted_ordering": name,
                "attempt_count": len(attempted),
                "rejected_attempts": attempted[:-1],
            }
    raise RuntimeError(
        "spqrtree produced no definition-valid reduced decomposition: "
        + repr(attempted)
    )


def to_spqr_tree(graph: nx.Graph):
    return validated_spqr_tree(graph)[0]


def real_r_edges(graph: nx.Graph) -> list[tuple]:
    """Return real edges in definition-validated R-node skeletons.

    The exhaustive split-pair implementation is authoritative at n<=9.  The
    external package remains an independent fast cross-check when its output
    passes ``spqr_validation_errors``.
    """
    return brute_spqr_decompose(graph).real_r_edges()


def r1_holds_for_edge(graph: nx.Graph, edge) -> bool:
    smaller = graph.copy()
    smaller.remove_edge(*edge)
    return is_2connected(smaller)


def expansion_preserves_2connectivity(
    skeleton: nx.Graph,
    expansions: dict[tuple, nx.Graph],
) -> nx.Graph:
    """Replace skeleton edges by pertinent expansions and verify R1b.

    Each expansion uses the original edge endpoints as its poles, meets all
    other pieces only at those poles, and must become 2-connected when the
    pole edge is restored.  Internal vertex labels must be globally disjoint.
    The returned expanded graph is asserted 2-connected.
    """
    if not is_2connected(skeleton):
        raise ValueError("the skeleton must be 2-connected")
    expanded = nx.Graph()
    expanded.add_nodes_from(skeleton.nodes())
    used_internal = set()
    for u, v in skeleton.edges():
        key = edge_key(u, v)
        if key not in expansions:
            expanded.add_edge(u, v)
            continue
        piece = expansions[key].copy()
        if u not in piece or v not in piece:
            raise ValueError(f"expansion {key} does not contain both poles")
        if piece.has_edge(u, v):
            raise ValueError(f"expansion {key} must omit its pole edge")
        closure = piece.copy()
        closure.add_edge(u, v)
        if not is_2connected(closure):
            raise ValueError(f"expansion {key} has a non-2-connected closure")
        internal = set(piece) - {u, v}
        if internal & (set(skeleton) | used_internal):
            raise ValueError("expansion internal vertices must be fresh")
        used_internal |= internal
        expanded = nx.compose(expanded, piece)
    if not is_2connected(expanded):
        raise AssertionError("R1b failed for a valid expansion family")
    return expanded


def spqr_decomposition_record(graph_j: nx.Graph, graph_b: nx.Graph, x, y) -> dict:
    """Serialize the reduced decomposition and its exact T8R annotations."""
    decomposition = brute_spqr_decompose(graph_j)
    # Root the otherwise-unrooted reduced tree at the unique skeleton holding
    # the distinguished real closure edge xy.
    root_candidates = [
        index for index, node in enumerate(decomposition.nodes)
        if any(not edge.virtual and set((edge.u, edge.v)) == {x, y}
               for edge in node.edges)
    ]
    if len(root_candidates) != 1:
        raise AssertionError("closure edge xy must occur as one unique real edge")
    root = root_candidates[0]
    order = []
    parent = {root: None}
    parent_token = {root: None}
    queue = [root]
    while queue:
        current = queue.pop(0)
        order.append(current)
        for neighbor, token in decomposition.adjacency[current]:
            if neighbor == parent[current]:
                continue
            parent[neighbor] = current
            parent_token[neighbor] = token
            queue.append(neighbor)
    output_index = {source: index for index, source in enumerate(order)}

    package_cross_check = None
    try:
        package_tree, package_validation = validated_spqr_tree(graph_j)
        package_cross_check = {
            **package_validation,
            "node_type_counts": dict(sorted(Counter(
                node.type.value for node in package_tree.nodes()
            ).items())),
        }
    except RuntimeError as error:
        package_cross_check = {
            "package": "spqrtree==0.1.2",
            "validated": False,
            "error": str(error),
        }

    records = []
    for index, source_index in enumerate(order):
        node = decomposition.nodes[source_index]
        skeleton_edges = sorted(
            ({"u": edge_key(edge.u, edge.v)[0],
              "v": edge_key(edge.u, edge.v)[1],
              "virtual": edge.virtual, "token": edge.token}
             for edge in node.edges),
            key=lambda item: (item["u"], item["v"], item["virtual"],
                              -1 if item["token"] is None else item["token"]),
        )
        real_edges = []
        for item in skeleton_edges:
            if item["virtual"]:
                continue
            edge = (item["u"], item["v"])
            in_b = graph_b.has_edge(*edge)
            real_edges.append({
                "edge": list(edge),
                "in_B": in_b,
                "is_closure_xy": set(edge) == {x, y},
                "r1_2connected_after_deletion": (
                    r1_holds_for_edge(graph_j, edge)
                    if node.type == "R" and set(edge) != {x, y}
                    else None
                ),
                "t8r_degree_critical": (
                    t8r_edge_is_degree_critical(graph_b, x, y, edge)
                    if node.type == "R" and in_b else None
                ),
            })
        degree_profile = []
        skeleton_graph = node.simple_graph()
        for vertex in sorted(node.vertices):
            role = "x" if vertex == x else "y" if vertex == y else "internal"
            degree_profile.append({
                "vertex": vertex,
                "role": role,
                "skeleton_degree": skeleton_graph.degree(vertex),
                "J_degree": graph_j.degree(vertex),
                "B_degree": graph_b.degree(vertex),
            })
        children = [neighbor for neighbor, _ in decomposition.adjacency[source_index]
                    if parent.get(neighbor) == source_index]
        poles = [x, y] if parent[source_index] is None else list(next(
            edge.endpoints for edge in node.edges
            if edge.virtual and edge.token == parent_token[source_index]
        ))
        records.append({
            "index": index,
            "type": node.type,
            "poles": poles,
            "parent": (None if parent[source_index] is None
                       else output_index[parent[source_index]]),
            "children": [output_index[child] for child in children],
            "skeleton_edges": skeleton_edges,
            "real_edges": real_edges,
            "degree_profile": degree_profile,
        })
    return {
        "validation": decomposition.validation,
        "package_cross_check": package_cross_check,
        "node_type_counts": dict(sorted(Counter(r["type"] for r in records).items())),
        "nodes": records,
    }


def run_relaxed_fixture_audit(nmin=5, nmax=8) -> dict:
    """Test R1/T8R classification on the exact E22 relaxed population."""
    counts = Counter()
    r1_violations = []
    for n in range(nmin, nmax + 1):
        proc = subprocess.Popen(
            ["geng", "-c", "-d2", str(n)],
            stdout=subprocess.PIPE,
            text=True,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            graph_j = nx.from_graph6_bytes(line.strip().encode())
            if not is_2connected(graph_j):
                continue
            for x, y in find_J_candidates(graph_j):
                counts["rooted_closure_fixtures"] += 1
                graph_b = graph_j.copy()
                graph_b.remove_edge(x, y)
                for edge in real_r_edges(graph_j):
                    if set(edge) == {x, y}:
                        counts["excluded_closure_edges"] += 1
                        continue
                    counts["R_real_B_edges"] += 1
                    if not r1_holds_for_edge(graph_j, edge):
                        r1_violations.append((n, line.strip(), x, y, edge))
                    if t8r_edge_is_degree_critical(graph_b, x, y, edge):
                        counts["T8R_degree_critical"] += 1
                    else:
                        counts["T8R_deletable_certificate"] += 1
                        audit = edge_deletion_audit(graph_b, x, y, edge)
                        assert not audit["degree_failures"]
                        assert audit["closure_2connected"]
        return_code = proc.wait()
        if return_code:
            raise RuntimeError(f"geng exited {return_code} at n={n}")
    return {
        "range": [nmin, nmax],
        "counts": dict(sorted(counts.items())),
        "r1_violations": r1_violations,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nmin", type=int, default=5)
    parser.add_argument("--nmax", type=int, default=8)
    args = parser.parse_args()
    report = run_relaxed_fixture_audit(args.nmin, args.nmax)
    print(f"relaxed rooted closures audited: "
          f"{report['counts'].get('rooted_closure_fixtures', 0)}")
    print(f"real R-skeleton B-edges checked: "
          f"{report['counts'].get('R_real_B_edges', 0)}")
    print(f"R1 violations: {len(report['r1_violations'])}")
    print(f"T8R degree-critical incidences: "
          f"{report['counts'].get('T8R_degree_critical', 0)}")
    print(f"noncritical deletion certificates (hence not minimal gadgets): "
          f"{report['counts'].get('T8R_deletable_certificate', 0)}")
    if report["r1_violations"]:
        raise SystemExit("R1 COUNTEREXAMPLE IN RELAXED FIXTURES")


if __name__ == "__main__":
    main()
