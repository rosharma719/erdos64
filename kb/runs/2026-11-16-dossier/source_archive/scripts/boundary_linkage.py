"""Exact (matching, total length) signatures for cycles across arbitrary edge cuts.

Cut edges are separately indexed, even when multiple cut edges meet one
vertex.  A pairing of two such ports at the same vertex is a length-zero
path.  Graphs are simple, undirected, and networkx-based.

This module is an exact, small-graph proof/checking oracle.  The exhaustive path
enumeration is exponential and is deliberately NOT presented as a scalable solver.
"""

from __future__ import annotations

from itertools import combinations

import networkx as nx


def perfect_matchings(items):
    """Yield canonical pair partitions of an even tuple of distinct items."""
    items = tuple(sorted(items))
    if len(items) % 2:
        raise ValueError("An even number of terminals is required")
    if not items:
        yield ()
        return
    head = items[0]
    for i in range(1, len(items)):
        partner = items[i]
        remaining = items[1:i] + items[i + 1:]
        for rest in perfect_matchings(remaining):
            yield ((head, partner),) + rest


def alternating_connected(matching_a, matching_b):
    """Do two perfect matchings on the same indices form one alternating circuit?"""
    vertices = {v for pair in matching_a for v in pair}
    if vertices != {v for pair in matching_b for v in pair} or not vertices:
        return False
    # With edge multiplicity, each index has degree two.  Connectivity is
    # sufficient for the union to be a single circuit, including the 2-cycle.
    adjacency = {v: set() for v in vertices}
    for pair in matching_a + matching_b:
        u, v = pair
        adjacency[u].add(v)
        adjacency[v].add(u)
    visited, agenda = set(), [next(iter(vertices))]
    while agenda:
        v = agenda.pop()
        if v not in visited:
            visited.add(v)
            agenda.extend(adjacency[v] - visited)
    return visited == vertices


def linkage_lengths(graph, ports, matching, forbidden=()):
    """Total edge counts of pairwise vertex-disjoint paths for a matching.

    `ports` maps edge indices to endpoint vertices on this side.  A root can be
    excluded with `forbidden`.  Path choices are simple and mutually disjoint.
    """
    forbidden = set(forbidden)
    if any(ports[x] in forbidden for pair in matching for x in pair):
        return frozenset()
    H = graph.subgraph(set(graph.nodes()) - forbidden)
    candidates = []
    for i, j in matching:
        u, v = ports[i], ports[j]
        if u not in H or v not in H:
            return frozenset()
        paths = ((u,),) if u == v else tuple(tuple(path) for path in nx.all_simple_paths(H, u, v))
        if not paths:
            return frozenset()
        candidates.append(paths)

    totals = set()

    def extend(index, occupied, length):
        if index == len(candidates):
            totals.add(length)
            return
        for path in candidates[index]:
            nodes = set(path)
            if not (nodes & occupied):
                extend(index + 1, occupied | nodes, length + len(path) - 1)

    extend(0, set(), 0)
    return frozenset(totals)


def crossing_cycle_lengths(graph, side_a, root=None, max_crossings=None):
    """Exact lengths of *simple* cycles meeting both sides of any edge cut.

    Return (crossing-length set, keyed details).  A key is a tuple containing
    the selected cut indices and the two endpoint matchings.  The corresponding
    set gives cycle lengths of exactly that state.  `root` forbids cycles
    through that vertex.  Does not include cycles wholly within one side.
    """
    A = set(side_a)
    B = set(graph.nodes()) - A
    if not A or not B:
        raise ValueError("Both cut shores must be nonempty")
    cut = sorted((u, v) if u in A else (v, u)
                 for u, v in graph.edges()
                 if (u in A) != (v in A))
    port_a = {i: edge[0] for i, edge in enumerate(cut)}
    port_b = {i: edge[1] for i, edge in enumerate(cut)}
    HA, HB = graph.subgraph(A), graph.subgraph(B)
    all_lengths = set()
    states = {}
    cache_a, cache_b = {}, {}
    upper = len(cut) if max_crossings is None else min(max_crossings, len(cut))
    for count in range(2, upper + 1, 2):
        for used in combinations(range(len(cut)), count):
            matchings = tuple(perfect_matchings(used))
            for ma in matchings:
                cache_a.setdefault(ma, linkage_lengths(HA, port_a, ma, forbidden=(root,) if root in A else ()))
                if not cache_a[ma]:
                    continue
                for mb in matchings:
                    if not alternating_connected(ma, mb):
                        continue
                    cache_b.setdefault(mb, linkage_lengths(HB, port_b, mb, forbidden=(root,) if root in B else ()))
                    if not cache_b[mb]:
                        continue
                    lengths = frozenset(count + a + b for a in cache_a[ma] for b in cache_b[mb])
                    states[(used, ma, mb)] = lengths
                    all_lengths.update(lengths)
    return frozenset(all_lengths), states


def dyadic_density_certificate(A, B, shift, exponent, lo, hi):
    """Pigeonhole certificate that `2**exponent` is in `shift + A + B`.

    On the integer window I=[lo,hi], reflect J=(2**exponent-shift)-I.
    The certificate is valid if |A cap I|+|B cap J|>|I|.
    An actual pair is returned for independent verification.
    """
    if hi < lo or exponent < 2:
        raise ValueError("Provide a nonempty window and exponent >= 2")
    target = 2**exponent - shift
    A = set(A)
    B = set(B)
    observed_a = sorted(a for a in A if lo <= a <= hi)
    observed_b = sorted(b for b in B if target - hi <= b <= target - lo)
    margin = len(observed_a) + len(observed_b) - (hi - lo + 1)
    witness = next(((a, target - a) for a in observed_a if target - a in B), None)
    if margin > 0 and witness is None:
        raise AssertionError("Invalid density certificate")
    return {"margin": margin, "certified": margin > 0, "witness": witness,
            "reflected_target": target, "window": (lo, hi)}


def boundary_signature(graph, ports, forbidden=()):
    """Context-independent cycle and linkage signature of an indexed h-pole.

    `ports` is a sequence of h vertices; repetitions are allowed.  An indexed
    port denotes one external edge to be added when gluing.  The length values
    count edges entirely inside the pole.  There may be many different path
    realizations per matching, but only their total lengths are retained.
    """
    forbidden = frozenset(forbidden)
    if any(p not in graph for p in ports):
        raise ValueError("Every port must lie in the graph")
    h = len(ports)
    pmap = dict(enumerate(ports))
    linkages = {}
    for count in range(2, h + 1, 2):
        for chosen in combinations(range(h), count):
            for matching in perfect_matchings(chosen):
                linkages[(chosen, matching)] = linkage_lengths(
                    graph, pmap, matching, forbidden)
    H = graph.subgraph(set(graph) - set(forbidden))
    internal = frozenset(len(cycle) for cycle in nx.simple_cycles(H))
    return {"h": h, "linkages": linkages, "internal": internal}


def compose_signatures(left, right):
    """All simple-cycle lengths after joining equally indexed pole ports.

    Exactly one new edge of length one is inserted for each port index.
    Every graph cycle is internal to one pole or crosses the edge cut.
    """
    if left['h'] != right['h']:
        raise ValueError("Port counts must agree")
    result = set(left['internal']) | set(right['internal'])
    for (used, ma), lengths_a in left['linkages'].items():
        if not lengths_a:
            continue
        for mb in perfect_matchings(used):
            if not alternating_connected(ma, mb):
                continue
            lengths_b = right['linkages'][(used, mb)]
            result.update(len(used) + a + b for a in lengths_a for b in lengths_b)
    return frozenset(result)


def glue_poles(left, ports_left, right, ports_right):
    """Create a graph by gluing labeled poles through their indexed ports."""
    if len(ports_left) != len(ports_right):
        raise ValueError('Both poles need the same number of ports')
    G = nx.disjoint_union(nx.convert_node_labels_to_integers(left),
                          nx.convert_node_labels_to_integers(right))
    # Preserve correct port lookup even for arbitrary original vertex labels.
    left_index = {node: i for i, node in enumerate(left.nodes())}
    right_index = {node: i + len(left) for i, node in enumerate(right.nodes())}
    for u, v in zip(ports_left, ports_right):
        if G.has_edge(left_index[u], right_index[v]):
            raise ValueError('Parallel port edges require a multigraph')
        G.add_edge(left_index[u], right_index[v])
    return G


def reflected_density_certificate(A, B, shift, exponent, window):
    """Parity-aware additive density test on *any finite integer window*.

    If |A intersect W| + |B intersect (target-W)| > |W|, then the
    Minkowski sum `shift + A + B` contains 2**exponent.  This is sharp.
    """
    if exponent < 2:
        raise ValueError('Exponent must be >= 2 for simple-graph cycles')
    W = set(window)
    if not W:
        raise ValueError('Window must be nonempty')
    A, B = set(A), set(B)
    target = 2**exponent - shift
    margin = len(A & W) + len(B & {target - a for a in W}) - len(W)
    pair = next(((a, target - a) for a in A & W if target - a in B), None)
    assert not (margin > 0 and pair is None)
    return {"certified": margin > 0, "margin": margin, "witness": pair,
            "target": target, "window_size": len(W)}
