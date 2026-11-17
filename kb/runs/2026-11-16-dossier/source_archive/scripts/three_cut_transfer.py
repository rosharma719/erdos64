#!/usr/bin/env python3
"""Exact transfer of simple-cycle lengths across independent cyclic 3-edge cuts.

Main mathematical identity, for a matching cut (a_i,b_i), i=0,1,2:
  lengths(G) = internal(A) U internal(B)
        U union_{i<j} (2 + paths_A(a_i,a_j) + paths_B(b_i,b_j)).

The production-facing interface takes a *specified cut* rather than searching
for one. Small-graph validation may enumerate cuts, but the structural identity
is independent of any enumeration or small-graph bound.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Hashable, Iterable

import networkx as nx

from partial_triangle_expansion import cycles


@dataclass(frozen=True)
class PoleSignature:
    """Three-port graph signature (internal edges measured, no cut edges)."""
    internal_cycles: frozenset[int]
    pair_paths: tuple[frozenset[int], frozenset[int], frozenset[int]]

    def __post_init__(self):
        if len(self.pair_paths) != 3 or any(not p for p in self.pair_paths):
            raise ValueError('every terminal pair must have a path')

    def paths(self, i: int, j: int) -> frozenset[int]:
        if i == j or not 0 <= i < 3 or not 0 <= j < 3:
            raise ValueError('distinct port indices 0,1,2 are required')
        return self.pair_paths[{(0,1):0,(0,2):1,(1,2):2}[tuple(sorted((i,j)))]]

    def interval(self, i: int, j: int) -> tuple[int,int] | None:
        paths = self.paths(i,j)
        a,b = min(paths),max(paths)
        return (a,b) if len(paths)==b-a+1 else None

    def best_contiguous_subinterval(self, i: int, j: int) -> tuple[int,int]:
        """Maximize (b-2a-1) over integer intervals contained in pair paths.

        This works even when the *full* path spectrum is not an interval.
        It is a sound sufficient obstruction because it uses only lengths
        that actually occur in the pole.
        """
        lengths = sorted(self.paths(i,j))
        runs=[]
        start=last=lengths[0]
        for x in lengths[1:]:
            if x==last+1:
                last=x
            else:
                runs.append((start,last))
                start=last=x
        runs.append((start,last))
        return max(runs,key=lambda ab:(ab[1]-2*ab[0]-1,-ab[0]))

    def best_subinterval_weights(self) -> tuple[int,int,int]:
        blocks=[self.best_contiguous_subinterval(i,j) for i,j in ((0,1),(0,2),(1,2))]
        return tuple(b-2*a-1 for a,b in blocks)

    def width_weights(self) -> tuple[int,int,int] | None:
        """Certified width contributions b-2a-1; None if a spectrum has gaps."""
        intervals = [self.interval(i,j) for i,j in ((0,1),(0,2),(1,2))]
        if any(x is None for x in intervals):
            return None
        return tuple(b-2*a-1 for a,b in intervals)


@dataclass(frozen=True)
class Split:
    """A specific cyclic 3-cut, oriented from the A-side to the B-side."""
    A: nx.Graph
    B: nx.Graph
    port_A: tuple[Hashable,Hashable,Hashable]
    port_B: tuple[Hashable,Hashable,Hashable]
    cut_edges: tuple[tuple[Hashable,Hashable], ...]


def _is_cycle_in_component(graph: nx.Graph) -> bool:
    return len(graph) >= 3 and len(graph.edges()) >= len(graph)


def split_independent_cyclic_three_cut(
    graph: nx.Graph, edges: Iterable[tuple[Hashable,Hashable]],
    *, require_three_edge_connected: bool = True,
) -> Split:
    """Check a supplied cyclic cut and return its two three-terminal poles.

    The cut must be a matching, and removing it must produce exactly two
    connected sides, each containing a cycle. For 3-edge-connected cubic
    graphs all cyclic 3-cuts automatically satisfy the matching condition.
    """
    if not isinstance(graph,nx.Graph) or graph.is_multigraph() or graph.is_directed():
        raise ValueError('requires simple undirected graph')
    if not nx.is_connected(graph) or any(graph.degree(v)!=3 for v in graph):
        raise ValueError('requires connected cubic graph')
    if require_three_edge_connected and nx.edge_connectivity(graph) < 3:
        raise ValueError('requires a 3-edge-connected cubic graph')
    cut=tuple(edges)
    if len(cut)!=3 or len({frozenset(e) for e in cut})!=3 or any(len(e)!=2 for e in cut):
        raise ValueError('cut must contain three distinct edges')
    if any(not graph.has_edge(u,v) for u,v in cut):
        raise ValueError('cut contains an absent edge')
    if len({u for e in cut for u in e})!=6:
        raise ValueError('cut must be an independent matching')
    remainder=graph.copy()
    remainder.remove_edges_from(cut)
    components=list(nx.connected_components(remainder))
    if len(components)!=2:
        raise ValueError('cut must split graph into exactly two connected sides')
    s,t=components
    A=graph.subgraph(s).copy()
    B=graph.subgraph(t).copy()
    if not _is_cycle_in_component(A) or not _is_cycle_in_component(B):
        raise ValueError('both sides must be cyclic')
    aligned=[]
    for u,v in cut:
        if u in t and v in s:
            u,v=v,u
        if u not in s or v not in t:
            raise ValueError('all three edges must cross the cut')
        aligned.append((u,v))
    return Split(A,B,tuple(u for u,v in aligned),tuple(v for u,v in aligned),tuple(aligned))


def pole_signature(graph: nx.Graph, ports: tuple[Hashable,Hashable,Hashable]) -> PoleSignature:
    """Exhaustive small-graph reference implementation for the exact signature.

    Computing general simple-path spectra is exponential in worst case. For
    large graphs use certified partial intervals / dynamic decomposition.
    """
    if len(ports)!=3 or len(set(ports))!=3 or any(p not in graph for p in ports):
        raise ValueError('expected three distinct port vertices')
    if not nx.is_connected(graph):
        raise ValueError('pole must be connected')
    if any(graph.degree(p)!=2 for p in ports):
        raise ValueError('ports must have degree two')
    if any(graph.degree(v)!=3 for v in graph if v not in ports):
        raise ValueError('nonport vertices must have degree three')
    pair_paths=tuple(
        frozenset(len(path)-1 for path in nx.all_simple_paths(graph,ports[i],ports[j]))
        for i,j in ((0,1),(0,2),(1,2))
    )
    return PoleSignature(frozenset(len(C) for C in cycles(graph)),pair_paths)


def cycle_lengths_from_signatures(A: PoleSignature, B: PoleSignature) -> frozenset[int]:
    """Exact simple-cycle spectrum after gluing the three pairs of ports."""
    lengths=set(A.internal_cycles)|set(B.internal_cycles)
    for i,j in ((0,1),(0,2),(1,2)):
        lengths.update(2+a+b for a in A.paths(i,j) for b in B.paths(i,j))
    return frozenset(lengths)


def is_dyadic(n: int) -> bool:
    return n >= 4 and (n & (n-1)) == 0


def forbidden_crossing_lengths(A:PoleSignature,B:PoleSignature)->frozenset[int]:
    return frozenset(
        2+a+b
        for i,j in ((0,1),(0,2),(1,2))
        for a in A.paths(i,j) for b in B.paths(i,j)
        if is_dyadic(2+a+b)
    )


def cut_width_obstruction(A:PoleSignature,B:PoleSignature):
    """Sufficient certificate requiring only the six interval endpoints.

    Returns (terminal_pair, min_cycle_length, max_cycle_length, dyadic_length)
    when one of the three crossing cycle intervals contains a power of two
    due to M>=2m. This is strictly weaker than the exact transfer check.
    """
    Wa,Wb=A.width_weights(),B.width_weights()
    if Wa is None or Wb is None:
        return None
    for k,(i,j) in enumerate(((0,1),(0,2),(1,2))):
        a0,a1=A.interval(i,j)
        b0,b1=B.interval(i,j)
        m,M=2+a0+b0,2+a1+b1
        if Wa[k]+Wb[k]>=0:
            p=1<<(m-1).bit_length()
            assert m<=p<=M
            return ((i,j),m,M,p)
    return None


def cut_subinterval_width_obstruction(A:PoleSignature,B:PoleSignature):
    """Sufficient dyadic witness for arbitrary, possibly gapped path spectra.

    Uses the best *contained* integer interval in each of the six spectra.
    The exact cut transfer remains the definitive test when sets are known.
    """
    for i,j in ((0,1),(0,2),(1,2)):
        a0,a1=A.best_contiguous_subinterval(i,j)
        b0,b1=B.best_contiguous_subinterval(i,j)
        m,M=2+a0+b0,2+a1+b1
        if M>=2*m:
            p=1<<(m-1).bit_length()
            assert m<=p<=M
            return ((i,j),m,M,p)
    return None


def cut_subinterval_mean_obstruction(A:PoleSignature,B:PoleSignature)->bool:
    """Orientation-independent dyadic obstruction, valid for gapped spectra."""
    return sum(A.best_subinterval_weights())+sum(B.best_subinterval_weights())>=0


def cut_mean_obstruction(A:PoleSignature,B:PoleSignature) -> bool:
    """Orientation-specific mean criterion: sum of three pair scores >=0."""
    Wa,Wb=A.width_weights(),B.width_weights()
    if Wa is None or Wb is None:
        return False
    return sum(Wa)+sum(Wb)>=0


def no_dyadic_crossing_gap_witness(A:PoleSignature,B:PoleSignature):
    """For full interval spectra, certify each crossing interval fits a dyadic gap.

    Returns 3 tuples (i,j,lo,hi,lower_power,upper_power), or None if a
    terminal pair has gaps or a cross interval contains a power of two.
    """
    certificate=[]
    for i,j in ((0,1),(0,2),(1,2)):
        ai,bi=A.interval(i,j) or (None,None)
        aj,bj=B.interval(i,j) or (None,None)
        if ai is None or aj is None:
            return None
        lo,hi=2+ai+aj,2+bi+bj
        high=1<<(lo-1).bit_length()
        if high==lo or hi>=high:
            return None
        certificate.append((i,j,lo,hi,high//2,high))
    return tuple(certificate)


def glue_poles(split:Split) -> nx.Graph:
    """Rebuild original graph from its extracted two poles and cut edges."""
    G=nx.compose(split.A,split.B)
    G.add_edges_from(split.cut_edges)
    return G


def verify_transfer(graph:nx.Graph, cut:Iterable[tuple[Hashable,Hashable]]) -> bool:
    """Small-graph differential test of the transfer identity."""
    split=split_independent_cyclic_three_cut(graph,cut)
    A=pole_signature(split.A,split.port_A)
    B=pole_signature(split.B,split.port_B)
    actual=frozenset(len(C) for C in cycles(graph))
    assert nx.is_isomorphic(graph,glue_poles(split))
    return cycle_lengths_from_signatures(A,B)==actual


def three_sum_of_cubic_graphs(G:nx.Graph,remove_G:Hashable,H:nx.Graph,remove_H:Hashable,
                              permutation:tuple[int,int,int]=(0,1,2)):
    """Form a 3-edge sum by removing one vertex from each cubic graph.

    Returns (joined_graph, oriented_cut_edges); all vertex IDs are tagged.
    """
    if set(permutation)!={0,1,2}:
        raise ValueError('permutation must contain 0,1,2')
    if not nx.is_connected(G) or not nx.is_connected(H):
        raise ValueError('connected factors required')
    if any(G.degree(v)!=3 for v in G) or any(H.degree(v)!=3 for v in H):
        raise ValueError('cubic factors required')
    if remove_G not in G or remove_H not in H:
        raise ValueError('deleted vertex missing')
    ports_G=sorted(G.neighbors(remove_G))
    ports_H=sorted(H.neighbors(remove_H))
    if len(set(ports_G))!=3 or len(set(ports_H))!=3:
        raise ValueError('each distinguished vertex needs distinct neighbors')
    A=nx.relabel_nodes(G.copy(),lambda x:('A',x))
    B=nx.relabel_nodes(H.copy(),lambda x:('B',x))
    A.remove_node(('A',remove_G))
    B.remove_node(('B',remove_H))
    joined=nx.compose(A,B)
    cut=tuple((('A',ports_G[i]),('B',ports_H[permutation[i]])) for i in range(3))
    joined.add_edges_from(cut)
    return joined,cut


def cap_pole(graph:nx.Graph,ports:tuple[Hashable,Hashable,Hashable]):
    """Cubic completion of a three-port pole by adding a new degree-three vertex."""
    cap=('__cap__',)
    if cap in graph:
        raise ValueError('reserved cap label exists')
    G=graph.copy()
    G.add_edges_from((cap,v) for v in ports)
    if any(G.degree(v)!=3 for v in G):
        raise AssertionError('completion was not cubic')
    return G


@dataclass(frozen=True)
class CutWitness:
    """Independent certificate: a simple dyadic cycle across the supplied cut."""
    terminal_pair: tuple[int,int]
    length: int
    vertices: tuple[Hashable,...]


def dyadic_cut_cycle_witness(split:Split) -> CutWitness | None:
    """Construct an actual cycle if one is forced by an exact cross spectrum.

    Intended for independently verifiable small/medium cases. Produces no
    false witness; absence of one requires complete path spectra to certify.
    """
    A=pole_signature(split.A,split.port_A)
    B=pole_signature(split.B,split.port_B)
    cut_graph=glue_poles(split)
    for i,j in ((0,1),(0,2),(1,2)):
        for a in sorted(A.paths(i,j)):
            for b in sorted(B.paths(i,j)):
                p=2+a+b
                if not is_dyadic(p):
                    continue
                pa=next(x for x in nx.all_simple_paths(split.A,split.port_A[i],split.port_A[j])
                        if len(x)-1==a)
                pb=next(x for x in nx.all_simple_paths(split.B,split.port_B[j],split.port_B[i])
                        if len(x)-1==b)
                C=tuple(pa+pb)
                assert len(C)==p==len(set(C))
                assert all(cut_graph.has_edge(C[k],C[(k+1)%p]) for k in range(p))
                return CutWitness((i,j),p,C)
    return None
