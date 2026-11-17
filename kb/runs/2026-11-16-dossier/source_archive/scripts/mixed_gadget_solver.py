#!/usr/bin/env python3
"""Exact 3-port cubic vertex replacement and forbidden-cycle constraint search.

On any simple cubic base, each non-internal simple cycle projects to a
simple base cycle. Its possible lengths are the base cycle length plus the
Minkowski sum of terminal-to-terminal simple-path lengths of its gadgets.
The paths are *attachment-aware*: different terminal pairs may differ.

This is research software, not a proof of the Erdős-Gyárfás conjecture.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from typing import Iterable
import json

import networkx as nx

from partial_triangle_expansion import check_cubic_simple, cycles


@dataclass(frozen=True)
class Gadget:
    """An internal graph and ordered port vertices, each of internal degree 2.

    Special case: a single unexpanded degree-3 vertex with repeated ports.
    Ports represent the ends of the THREE external edges. The pair paths
    have lengths measured in internal edges, excluding external base edges.
    """
    name: str
    graph6: str | None
    ports: tuple[int, int, int] | None
    pair_paths: tuple[frozenset[int], frozenset[int], frozenset[int]]
    internal_cycle_lengths: frozenset[int]
    size: int

    def paths(self, i: int, j: int) -> frozenset[int]:
        if i == j:
            raise ValueError('distinct terminal indices required')
        return self.pair_paths[PAIR_INDEX[tuple(sorted((i, j)))]]


PAIR_INDEX = {(0, 1): 0, (0, 2): 1, (1, 2): 2}


def make_gadget(name: str, H: nx.Graph, ports: Iterable[int]) -> Gadget:
    ports = tuple(ports)
    mapping = {u:i for i,u in enumerate(sorted(H))}
    if set(ports) - set(mapping):
        raise ValueError('port vertex absent')
    H = nx.relabel_nodes(H, mapping, copy=True)
    ports = tuple(mapping[u] for u in ports)
    if len(ports) != 3 or len(set(ports)) != 3:
        raise ValueError('three distinct port vertices required')
    if not nx.is_connected(H) or set(ports) - set(H):
        raise ValueError('gadgets must be connected and ports present')
    if len(H) % 2 != 1 or not all(H.degree[v] == (2 if v in ports else 3) for v in H):
        raise ValueError('degree-2 ports, degree-3 internal vertices required')
    ps = tuple(frozenset(len(path)-1 for path in nx.all_simple_paths(H, ports[i], ports[j]))
               for i, j in PAIR_INDEX)
    return Gadget(name, nx.to_graph6_bytes(H, header=False).decode().strip(),
                  ports, ps, frozenset(len(C) for C in cycles(H)), len(H))


def exoo_h15() -> Gadget:
    """Build the 15-vertex Exoo gadget from two H7 copies and a new vertex.

    Uses Garcia (2026), arXiv:2609.04686, Section 3. H7 attachment
    vertices are (u,v,w)=(0,1,2), with edges as stated in that paper.
    H15 ports are (z, u_B, u_A).
    """
    h7_edges=[(1,3),(3,4),(4,2),(5,1),(2,6),(3,5),(5,0),(0,6),(6,4)]
    H=nx.Graph()
    H.add_edges_from((a,b) for a,b in h7_edges)
    H.add_edges_from((a+7,b+7) for a,b in h7_edges)
    # z=14, attach vA--vB, wA--z--wB
    H.add_edges_from(((1,8),(2,14),(14,9)))
    return make_gadget('H15_exoo',H,(14,7,0))


def gadgets_from_catalog(include_h15: bool = False) -> list[Gadget]:
    """Gadget library: identity, triangle, plus two 7-vertex rooted classes.

    Every 7-vertex candidate formed by deleting a vertex from a connected
    cubic graph on 8 vertices is included up to port-preserving isomorphism.
    Order-8 catalog is from the prior census fixture.
    """
    catalog = json.loads(Path(__file__).with_name('cubic_catalog_n8_n10.json').read_text())
    bases = [nx.from_graph6_bytes(s.encode()) for s in catalog['connected_cubic']['8']]
    chosen = []
    for G in bases:
        for v in G:
            H = G.copy()
            port_vertices = tuple(sorted(G.neighbors(v)))
            H.remove_node(v)
            if not nx.is_connected(H) or {len(c) for c in cycles(H)} & {4, 8}:
                continue
            # canonical relabeling must be consistent with chosen port vertices
            old = sorted(H)
            trans = {u:i for i,u in enumerate(old)}
            H = nx.relabel_nodes(H, trans)
            p = tuple(trans[u] for u in port_vertices)
            # Dedup port-unordered gadget isomorphism, checking terminal markings.
            marked = H.copy()
            nx.set_node_attributes(marked, {u: {'port': u in p} for u in marked})
            if any(nx.is_isomorphic(marked, known[0],
                    node_match=lambda a,b:a['port'] == b['port']) for known in chosen):
                continue
            chosen.append((marked, H, p))
    if len(chosen) != 2:
        raise AssertionError(f'expected two distinct 7-vertex gadgets; found {len(chosen)}')
    result = [Gadget('id', None, None, (frozenset({0}),)*3, frozenset(), 1)]
    result.append(make_gadget('T3', nx.cycle_graph(3), (0,1,2)))
    for _, H, p in chosen:
        raw = make_gadget('H7', H, p)
        tag = 'H7_uniform' if len(set(raw.pair_paths)) == 1 else 'H7_skew'
        result.append(make_gadget(tag, H, p))
    if include_h15:
        result.append(exoo_h15())
    return result


@dataclass(frozen=True)
class Choice:
    gadget: Gadget
    """ports[index] gives gadget-port index for sorted base neighbor[index]."""
    permutation: tuple[int,int,int]

    @property
    def name(self) -> str:
        return self.gadget.name + ':' + ''.join(map(str,self.permutation))


def choice_library(gadgets: list[Gadget]) -> list[Choice]:
    """All distinct *path-spectrum* port orientations, keeping one graph representative.

    Port-isomorphic representations can yield the same possible lengths;
    those are safely deduplicated for cycle-avoidance SAT/CSP searching.
    """
    out: list[Choice] = []
    for gadget in gadgets:
        seen = set()
        for perm in permutations((0,1,2)):
            signature = tuple(gadget.paths(perm[i],perm[j]) for i,j in PAIR_INDEX)
            if signature in seen:
                continue
            seen.add(signature)
            out.append(Choice(gadget, perm))
    return out


def build_replacement(base: nx.Graph, by_vertex: dict[int, Choice]) -> nx.Graph:
    check_cubic_simple(base)
    if set(base) != set(by_vertex):
        raise ValueError('each base vertex needs one choice')
    H = nx.Graph()
    port = {}
    for u in base:
        choice = by_vertex[u]
        gadget = choice.gadget
        if gadget.graph6 is None:
            H.add_node((u,0))
            for v in base.neighbors(u):
                port[u,v] = (u,0)
            continue
        sub = nx.from_graph6_bytes(gadget.graph6.encode())
        H.add_nodes_from((u,i) for i in sub)
        H.add_edges_from(((u,i),(u,j)) for i,j in sub.edges())
        ns = sorted(base.neighbors(u))
        for k,v in enumerate(ns):
            port[u,v] = (u, gadget.ports[choice.permutation[k]])
    for u,v in base.edges():
        H.add_edge(port[u,v], port[v,u])
    return H


def bit_sum(left: int, right: int, max_length: int) -> int:
    """Bitset convolution; bit k denotes a possible total internal length k."""
    res = 0
    while right:
        bit = right & -right
        res |= left << (bit.bit_length()-1)
        right ^= bit
    return res & ((1 << (max_length+1))-1)


def length_mask(base: nx.Graph, cycle: tuple[int, ...], choices: dict[int,Choice], cap:int) -> int:
    out = 1 << len(cycle)   # L external base edges
    for i,u in enumerate(cycle):
        ns = sorted(base.neighbors(u))
        a=ns.index(cycle[i-1]); b=ns.index(cycle[(i+1)%len(cycle)])
        choice=choices[u]
        lengths=choice.gadget.paths(choice.permutation[a],choice.permutation[b])
        out = bit_sum(out, sum(1<<x for x in lengths), cap)
        if not out: break
    return out


def predicted_spectrum(base: nx.Graph, choices: dict[int,Choice]) -> set[int]:
    """Full exact cycle-length spectrum (small graphs only)."""
    check_cubic_simple(base)
    cap=sum(ch.gadget.size for ch in choices.values())
    lengths=set().union(*(ch.gadget.internal_cycle_lengths for ch in choices.values()))
    for C in cycles(base):
        mask=length_mask(base,tuple(C),choices,cap)
        lengths.update(k for k in range(3,cap+1) if mask>>k & 1)
    return lengths


def is_forbidden_free(base: nx.Graph, choices: dict[int,Choice], forbidden:set[int]) -> bool:
    cap=max(forbidden,default=0)
    if any(ch.gadget.internal_cycle_lengths.intersection(forbidden) for ch in choices.values()):
        return False
    F=sum(1<<p for p in forbidden)
    return all(not(length_mask(base,tuple(C),choices,cap) & F) for C in cycles(base))


def search_assignments(base: nx.Graph, choices:list[Choice], forbidden:set[int], *,
                       max_extra_vertices:int|None=None, max_results:int|None=None):
    """Cycle-CSP with exact interval pruning and attachment-aware port choices.

    Every gadget path-length spectrum in this bundled library is a contiguous
    interval. A base cycle therefore contributes the *full* integer interval
    [L + sum(min paths), L + sum(max paths)].

    At a partial assignment, for every base cycle we test whether SOME choice
    of remaining per-vertex path intervals could put the entire lifted
    interval in a forbidden-free gap. If none exists, all completions fail,
    so pruning is sound. Overlapping cycles are handled by backtracking.
    """
    from functools import lru_cache

    check_cubic_simple(base)
    options=[x for x in choices if not(x.gadget.internal_cycle_lengths & forbidden)]
    if not options: return
    base_cycles=[tuple(C) for C in cycles(base)]
    # Prefer vertices participating in short cycles, for early propagation.
    order=sorted(base, key=lambda u: -sum((15-len(C)) if len(C)<15 else 1
                              for C in base_cycles if u in C))
    n=len(order)
    m=len(base_cycles)
    by_vertex={u:[] for u in base}
    bounds=[]
    all_pairs=set()
    for ci,C in enumerate(base_cycles):
        per_vertex={}
        for i,u in enumerate(C):
            ns=sorted(base.neighbors(u))
            a=ns.index(C[i-1]); b=ns.index(C[(i+1)%len(C)])
            entries=[]
            for choice in options:
                p=choice.gadget.paths(choice.permutation[a], choice.permutation[b])
                lo,hi=min(p),max(p)
                if len(p)!=hi-lo+1:
                    raise ValueError('spectrum gap: requires the general set-convolution engine')
                entries.append((lo,hi))
                all_pairs.add((lo,hi))
            per_vertex[u]=entries
            by_vertex[u].append(ci)
        bounds.append(per_vertex)

    # Overapproximate future choices for each cycle independently: it is safe
    # to ignore conflicts with other cycles while deciding impossibility.
    future_pairs=[{(0,0)}]
    for i in range(1,n+1):
        future_pairs.append({(a+x,b+y) for a,b in future_pairs[-1]
                             for x,y in all_pairs})
    forbidden_sorted=sorted(forbidden)
    @lru_cache(maxsize=None)
    def potentially_safe(L:int, unassigned:int, so_far_min:int, so_far_max:int)->bool:
        for dmin,dmax in future_pairs[unassigned]:
            lo=L+so_far_min+dmin
            hi=L+so_far_max+dmax
            if all(not(lo <= p <= hi) for p in forbidden_sorted):
                return True
        return False

    cmin=[0]*m
    cmax=[0]*m
    left=[len(C) for C in base_cycles]
    if any(not potentially_safe(len(C),len(C),0,0) for C in base_cycles):
        return
    assigned={}
    count=0
    def dfs(depth:int,extra:int):
        nonlocal count
        if max_results is not None and count >= max_results:
            return
        if depth==n:
            count+=1
            yield dict(assigned)
            return
        u=order[depth]
        affected=by_vertex[u]
        for oi, choice in enumerate(options):
            extra2=extra+choice.gadget.size-1
            if max_extra_vertices is not None and extra2>max_extra_vertices:
                continue
            assigned[u]=choice
            for ci in affected:
                x,y=bounds[ci][u][oi]
                cmin[ci]+=x
                cmax[ci]+=y
                left[ci]-=1
            feasible=all(potentially_safe(len(base_cycles[ci]),left[ci],cmin[ci],cmax[ci])
                         for ci in affected)
            if feasible:
                yield from dfs(depth+1,extra2)
            for ci in affected:
                x,y=bounds[ci][u][oi]
                cmin[ci]-=x
                cmax[ci]-=y
                left[ci]+=1
        assigned.pop(u,None)
    yield from dfs(0,0)



def main():
    import argparse
    from partial_triangle_expansion import base_graph
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',default='petersen',choices=['k4','prism','cube','petersen'])
    parser.add_argument('--forbid',type=int,nargs='+',default=[4,8,16])
    parser.add_argument('--max-extra',type=int,default=20)
    parser.add_argument('--include-h15',action='store_true')
    parser.add_argument('--max-results',type=int,default=None)
    args=parser.parse_args()
    G=base_graph(args.base)
    choices=choice_library(gadgets_from_catalog(include_h15=args.include_h15))
    counts=Counter()
    for assignment in search_assignments(G,choices,set(args.forbid),max_extra_vertices=args.max_extra,max_results=args.max_results):
        counts[len(G)+sum(c.gadget.size-1 for c in assignment.values())]+=1
    print('choices:',[(c.name,c.gadget.pair_paths) for c in choices])
    print('base',args.base,'forbidden',args.forbid,'max-extra',args.max_extra,'valid_by_output_order',dict(sorted(counts.items())))


if __name__=='__main__':main()
