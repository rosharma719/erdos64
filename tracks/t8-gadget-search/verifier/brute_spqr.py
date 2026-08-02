"""Definition-first SPQR decomposition for the project's small graphs.

The installed ``spqrtree==0.1.2`` implementation is fast but can be
insertion-order-sensitive.  This module supplies a deliberately small-order,
exhaustive split-pair decomposition used as an independent fallback and
cross-check for the order-nine census.  It follows the reduced convention in
``one_pole.md``: Q nodes are suppressed when an edge can remain real in an
S/P/R skeleton, and adjacent S-S or P-P nodes are merged.

This is not intended as an unrestricted large-graph SPQR implementation.
Its exhaustive pair scans are appropriate for the n<=9 research range.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import networkx as nx


def _vertex_key(vertex):
    return (type(vertex).__name__, repr(vertex))


def _pair(u, v):
    return tuple(sorted((u, v), key=_vertex_key))


@dataclass(frozen=True)
class SplitEdge:
    u: object
    v: object
    virtual: bool = False
    token: int | None = None

    @property
    def endpoints(self):
        return _pair(self.u, self.v)


@dataclass
class SplitNode:
    type: str
    edges: list[SplitEdge]

    @property
    def vertices(self):
        return {endpoint for edge in self.edges for endpoint in (edge.u, edge.v)}

    def simple_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.vertices)
        graph.add_edges_from((edge.u, edge.v) for edge in self.edges)
        return graph


@dataclass
class BruteSPQR:
    nodes: list[SplitNode]
    adjacency: dict[int, list[tuple[int, int]]]
    validation: dict

    def real_r_edges(self):
        return sorted(
            {
                edge.endpoints
                for node in self.nodes if node.type == "R"
                for edge in node.edges if not edge.virtual
            },
            key=lambda edge: tuple(_vertex_key(v) for v in edge),
        )


def _simple_graph(edges):
    graph = nx.Graph()
    graph.add_edges_from((edge.u, edge.v) for edge in edges)
    return graph


def _parallel_free(edges):
    return len({edge.endpoints for edge in edges}) == len(edges)


def _classify_terminal_piece(edges):
    graph = _simple_graph(edges)
    order = graph.number_of_nodes()
    if order == 2:
        if len(edges) >= 3:
            return "P"
        if len(edges) == 1:
            return "Q"
        return None
    if (_parallel_free(edges) and order >= 3
            and graph.number_of_edges() == order
            and nx.is_connected(graph)
            and all(degree == 2 for _, degree in graph.degree())):
        return "S"
    if (_parallel_free(edges) and order >= 4 and nx.is_connected(graph)
            and nx.node_connectivity(graph) >= 3):
        return "R"
    return None


def _split_bridges(edges, u, v):
    graph = _simple_graph(edges)
    reduced = graph.copy()
    reduced.remove_nodes_from([u, v])
    components = list(nx.connected_components(reduced))
    components.sort(key=lambda component: tuple(
        sorted((_vertex_key(vertex) for vertex in component))
    ))
    direct = [edge for edge in edges if set((edge.u, edge.v)) == {u, v}]
    bridges = []
    for component in components:
        allowed = set(component) | {u, v}
        component_edges = [
            edge for edge in edges
            if edge.u in allowed and edge.v in allowed
            and set((edge.u, edge.v)) != {u, v}
            and (edge.u in component or edge.v in component)
        ]
        if component_edges:
            bridges.append(component_edges)
    bridges.extend([[edge] for edge in direct])
    return bridges, len(components), len(direct)


def _choose_split_pair(edges):
    graph = _simple_graph(edges)
    candidates = []
    for u, v in combinations(sorted(graph.nodes(), key=_vertex_key), 2):
        bridges, component_count, direct_count = _split_bridges(edges, u, v)
        is_separator = component_count >= 2
        has_parallel = direct_count >= 2
        if not (is_separator or has_parallel):
            continue
        if len(bridges) < 2:
            continue
        candidates.append((
            -len(bridges),
            _vertex_key(u),
            _vertex_key(v),
            u,
            v,
            bridges,
            component_count,
            direct_count,
        ))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[:3])
    return candidates[0][3:]


class _Builder:
    def __init__(self):
        self.nodes = []
        self.next_token = 0

    def token(self):
        token = self.next_token
        self.next_token += 1
        return token

    def decompose(self, edges):
        kind = _classify_terminal_piece(edges)
        if kind is not None:
            self.nodes.append(SplitNode(kind, list(edges)))
            return

        split = _choose_split_pair(edges)
        if split is None:
            graph = _simple_graph(edges)
            raise RuntimeError(
                "piece is neither S/P/Q/R nor splittable: "
                f"vertices={sorted(graph.nodes(), key=_vertex_key)!r}, "
                f"edges={[edge.endpoints for edge in edges]!r}"
            )
        u, v, bridges, component_count, direct_count = split
        nontrivial = [bridge for bridge in bridges if len(bridge) != 1
                      or bridge[0].endpoints != _pair(u, v)]
        direct = [bridge[0] for bridge in bridges if len(bridge) == 1
                  and bridge[0].endpoints == _pair(u, v)]

        # Exactly two nontrivial split components and no direct pole edge:
        # pair them directly by one virtual edge in each skeleton.
        if component_count == 2 and direct_count == 0:
            token = self.token()
            for bridge in nontrivial:
                child = list(bridge) + [SplitEdge(u, v, True, token)]
                self.decompose(child)
            return

        # Three or more split components meet in a P-node.  Direct pole edges
        # remain real/virtual in that bond; every nontrivial bridge gets a
        # paired virtual edge.
        central_edges = list(direct)
        for bridge in nontrivial:
            token = self.token()
            central_edges.append(SplitEdge(u, v, True, token))
            child = list(bridge) + [SplitEdge(u, v, True, token)]
            self.decompose(child)
        if len(central_edges) < 3:
            raise RuntimeError("split did not produce a valid P bond")
        self.nodes.append(SplitNode("P", central_edges))


def _token_occurrences(nodes):
    occurrences = {}
    for index, node in enumerate(nodes):
        for edge in node.edges:
            if edge.virtual:
                occurrences.setdefault(edge.token, []).append(index)
    return occurrences


def _reduce_same_type(nodes):
    nodes = list(nodes)
    while True:
        occurrences = _token_occurrences(nodes)
        merge = None
        for token, owners in sorted(occurrences.items()):
            if len(owners) != 2:
                continue
            left, right = owners
            if nodes[left].type == nodes[right].type and nodes[left].type in ("S", "P"):
                merge = token, left, right
                break
        if merge is None:
            return nodes
        token, left, right = merge
        combined = [
            edge for index in (left, right) for edge in nodes[index].edges
            if not (edge.virtual and edge.token == token)
        ]
        replacement = SplitNode(nodes[left].type, combined)
        nodes = [node for index, node in enumerate(nodes)
                 if index not in (left, right)] + [replacement]


def _validate(nodes, original: nx.Graph):
    errors = []
    for index, node in enumerate(nodes):
        classified = _classify_terminal_piece(node.edges)
        if classified != node.type:
            errors.append(
                f"node {index} recorded {node.type} but classifies as {classified}"
            )
    occurrences = _token_occurrences(nodes)
    if any(len(owners) != 2 for owners in occurrences.values()):
        errors.append("a virtual token does not occur exactly twice")

    adjacency_graph = nx.Graph()
    adjacency_graph.add_nodes_from(range(len(nodes)))
    for token, owners in occurrences.items():
        if len(owners) == 2:
            adjacency_graph.add_edge(*owners, token=token)
            if nodes[owners[0]].type == nodes[owners[1]].type in ("S", "P"):
                errors.append("the decomposition is not reduced")
    if len(nodes) > 1 and not nx.is_tree(adjacency_graph):
        errors.append("virtual-edge adjacency is not a tree")

    actual_real = sorted(
        (edge.endpoints for node in nodes for edge in node.edges
         if not edge.virtual),
        key=lambda edge: tuple(_vertex_key(v) for v in edge),
    )
    expected_real = sorted(
        (_pair(u, v) for u, v in original.edges()),
        key=lambda edge: tuple(_vertex_key(v) for v in edge),
    )
    if actual_real != expected_real:
        errors.append("real skeleton edges do not partition the original graph")
    return errors, occurrences


def decompose(graph: nx.Graph) -> BruteSPQR:
    if graph.number_of_nodes() < 3 or not nx.is_biconnected(graph):
        raise ValueError("the host graph must be simple and 2-connected")
    if isinstance(graph, nx.MultiGraph) or nx.number_of_selfloops(graph):
        raise ValueError("the host graph must be loopless and simple")
    builder = _Builder()
    builder.decompose([SplitEdge(u, v) for u, v in graph.edges()])
    nodes = _reduce_same_type(builder.nodes)
    errors, occurrences = _validate(nodes, graph)
    if errors:
        raise RuntimeError("invalid brute SPQR decomposition: " + repr(errors))
    adjacency = {index: [] for index in range(len(nodes))}
    for token, (left, right) in occurrences.items():
        adjacency[left].append((right, token))
        adjacency[right].append((left, token))
    for neighbors in adjacency.values():
        neighbors.sort()
    return BruteSPQR(
        nodes=nodes,
        adjacency=adjacency,
        validation={
            "engine": "definition_first_exhaustive_split_pairs",
            "validated": True,
            "order_limit": 9,
            "node_count": len(nodes),
        },
    )
