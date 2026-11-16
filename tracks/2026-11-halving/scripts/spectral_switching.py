"""Exact dyadic spectral isolation and independent-cycle-switch certificates.

Small-instance oracle; no unproved global conjecture is used.
"""
from __future__ import annotations

from itertools import combinations
from math import gcd


def is_dyadic(n: int) -> bool:
    return n >= 4 and n & (n - 1) == 0


def isolated_context_length(lengths, target_length: int, min_exponent: int = 3) -> tuple[int, int]:
    """Find m>=0 such that m+2+x is dyadic iff x==target_length.

    lengths is an arbitrary finite subset of nonnegative integers.  A two-port
    context consists of a simple path of length m with two additional cut
    edges, one from each side of the path.  It can isolate any specified x.
    """
    lengths = set(lengths)
    if target_length < 0 or any(x < 0 for x in lengths):
        raise ValueError('path lengths must be nonnegative')
    for k in range(max(2, min_exponent), 1000):
        power = 1 << k
        m = power - target_length - 2
        if m < 1:  # require two distinct context boundary vertices
            continue
        if all(is_dyadic(m + 2 + x) == (x == target_length) for x in lengths):
            return m, power
    raise ArithmeticError('unexpected: dyadic isolation failed')


def complete_sequence_step(weights: list[int] | tuple[int, ...]) -> int | None:
    """Return step d if subset sums are *certified* to cover [0,sum] in step d.

    The sufficient criterion is gcd d, and sorted weights/d form a complete
    sequence: first is 1, every later value <= 1+sum(previous).  Return None
    for sequences this criterion does not certify. No necessity is claimed.
    """
    if not weights or any(x <= 0 for x in weights):
        return None
    d = 0
    for x in weights:
        d = gcd(d, x)
    a = sorted(x // d for x in weights)
    reachable = 0
    for x in a:
        if x > reachable + 1:
            return None
        reachable += x
    return d


def subset_sum_certificate(weights, target):
    """Return indices of weights summing to target; use exact DP as an oracle."""
    if target < 0:
        return None
    dp = {0: ()}
    for i, w in enumerate(weights):
        for x, inds in list(dp.items()):
            if x + w <= target and x + w not in dp:
                dp[x + w] = inds + (i,)
    return dp.get(target)


def complete_switch_dyadic_witness(base_length, weights):
    """Find dyadic cycle length certified by complete-sequence increments.

    Returns (power, chosen_weight_indices) or None. This proves a cycle exists
    only if a separate certificate confirms the corresponding switches can
    be independently applied to one simple cycle.
    """
    step = complete_sequence_step(weights)
    if step is None:
        return None
    total = sum(weights)
    power = 4
    while power < base_length:
        power <<= 1
    while power <= base_length + total:
        if (power - base_length) % step == 0:
            indices = subset_sum_certificate(weights, power - base_length)
            assert indices is not None
            return power, indices
        power <<= 1
    return None


def make_switch_graph(base_length: int, switches: list[tuple[int, int, int]]):
    """Build a cycle with independent external bypass paths.

    Each (start, end, bypass_length) replaces the forward base arc start..end;
    start/end inclusive supports must be disjoint. The base path and bypass
    paths share only their two endpoints, and bypass interiors are disjoint.
    Returns (G, base_cycle, certificate_switches).
    """
    import networkx as nx
    if base_length < 3:
        raise ValueError('base length must be >=3')
    G = nx.cycle_graph(base_length)
    occupied = set()
    cert = []
    fresh = base_length
    for i, j, path_length in switches:
        if not 0 <= i < j < base_length or path_length < 1:
            raise ValueError('invalid switch')
        support = set(range(i, j + 1))
        if occupied & support:
            raise ValueError('switch base arcs must have disjoint vertex supports')
        occupied |= support
        middle = list(range(fresh, fresh + path_length - 1))
        fresh += len(middle)
        route = (i, *middle, j)
        G.add_edges_from(zip(route, route[1:]))
        cert.append((i, j, route))
    return G, list(range(base_length)), cert


def reconstruct_switch_cycle(graph, base_cycle, switches, selected_indices):
    """Reconstruct a single simple cycle after selected arc replacements.

    This validation is deliberately independent of the numeric sumset test.
    """
    selected = set(selected_indices)
    replacements = {}
    used_vertices = set()
    for pos, (i,j,path) in enumerate(switches):
        if pos in selected:
            if len(path) < 2 or path[0] != base_cycle[i] or path[-1] != base_cycle[j]:
                raise ValueError('invalid bypass path')
            replacements[i] = (j, list(path))
            inside = set(path[1:-1])
            if inside & used_vertices or inside & set(base_cycle):
                raise ValueError('bypass interiors must be disjoint from base cycle and one another')
            used_vertices |= inside
    cycle = [base_cycle[0]]
    i = 0
    while i < len(base_cycle) - 1:
        if i in replacements:
            j, path = replacements[i]
            cycle.extend(path[1:]); i = j
        else:
            i += 1; cycle.append(base_cycle[i])
    if len(cycle) != len(set(cycle)) or len(cycle) < 3:
        raise ValueError('reconstructed object is not a simple cycle')
    if any(not graph.has_edge(u,v) for u,v in zip(cycle,cycle[1:]+cycle[:1])):
        raise ValueError('reconstructed cycle contains a non-edge')
    return cycle


def independent_switch_lengths(graph, base_cycle, switches):
    """Length set obtained by all subsets of independently certified bypasses."""
    n = len(switches)
    lengths = set()
    for mask in range(1<<n):
        chosen = [i for i in range(n) if mask & (1<<i)]
        lengths.add(len(reconstruct_switch_cycle(graph,base_cycle,switches,chosen)))
    return lengths


def make_series_switch_pole(arc_lengths, bypass_lengths, tail_length=1):
    """Two-terminal pole built from an ordinary path and disjoint parallel detours.

    Every selected replacement switches an entire base subpath, so the terminal
    path spectrum contains base_length+subset_sums(bypass_lengths-arc_lengths).
    The base segments have disjoint interiors; shared consecutive segment
    endpoints are allowed here because terminal *paths* remain simple.
    """
    import networkx as nx
    if (len(arc_lengths) != len(bypass_lengths) or
        any(a < 1 for a in arc_lengths) or any(b < 2 for b in bypass_lengths) or
        tail_length < 0):
        raise ValueError('invalid series-pole lengths')
    base_length = sum(arc_lengths) + tail_length
    G = nx.path_graph(base_length+1)
    next_vertex = base_length+1
    start = 0
    records=[]
    for a,b in zip(arc_lengths,bypass_lengths):
        stop=start+a
        middle=list(range(next_vertex,next_vertex+b-1))
        next_vertex += len(middle)
        path=[start]+middle+[stop]
        G.add_edges_from(zip(path,path[1:]))
        records.append((start,stop,path))
        start=stop
    return G,(0,base_length),records


def terminal_path_lengths(graph, source, target):
    """Slow independent length-spectrum oracle, for small pole examples."""
    import networkx as nx
    return {len(p)-1 for p in nx.all_simple_paths(graph,source,target)}


def switching_length_polynomial(base_length, increments, requirements=None):
    """Exact Laurent-polynomial coefficient dictionary for independent switches.

    requirements maps switch indices to True (must select) or False (must omit).
    Coefficients count switch subsets, assuming certified independent switches.
    """
    requirements = {} if requirements is None else dict(requirements)
    coeff = {base_length: 1}
    for i, d in enumerate(increments):
        if i in requirements:
            if requirements[i]:
                coeff = {k + d:v for k,v in coeff.items()}
            continue
        nxt = dict(coeff)
        for k,v in coeff.items():
            nxt[k+d] = nxt.get(k+d,0) + v
        coeff = nxt
    return coeff


def rooted_switch_length_polynomial(base_cycle, switches, root):
    """Exact length polynomial of switch variants avoiding a prescribed vertex.

    Assumes all switch base arcs have pairwise disjoint interiors, all bypass
    interiors avoid the base cycle, and all bypass interiors are disjoint.
    Root-on-base endpoints always survive; roots internal to a replaced arc
    force that detour on. Roots internal to a bypass force that detour off.
    """
    requirements = {}
    if root in base_cycle:
        if any(root == path[0] or root == path[-1] for i,j,path in switches):
            return {}
        for i,(start,stop,path) in enumerate(switches):
            if root in base_cycle[start+1:stop]:
                requirements[i] = True
        if not requirements:
            return {}  # root remains on the base cycle in every variant
    else:
        for i,(start,stop,path) in enumerate(switches):
            if root in path[1:-1]:
                requirements[i] = False
    diffs = [len(path)-1-(j-i) for i,j,path in switches]
    return switching_length_polynomial(len(base_cycle),diffs,requirements)
