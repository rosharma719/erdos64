#!/usr/bin/env python3
"""Constructive cycle-space averaging obstruction for three-port gadgets.

This is a theorem-driven (polynomial-time) certificate generator, not a
search over all simple cycles. See ../cycle_space_obstruction.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

import networkx as nx

from mixed_gadget_solver import (
    Choice, build_replacement, choice_library, gadgets_from_catalog,
)
from partial_triangle_expansion import check_cubic_simple


@dataclass(frozen=True)
class Obstruction:
    score_sum: int
    average_score_quarters: int  # E[total cycle score] * 4, for bridgeless bases
    base_cycle: tuple[int, ...]
    lifted_length: int
    min_length: int
    max_length: int
    expanded_cycle: tuple[tuple[int,int], ...]
    certificate_kind: str = "unconditional"


def local_scores(base: nx.Graph, choices: dict[int, Choice]) -> dict[int, tuple[int,int,int,int]]:
    """Score per local 3-bit edge mask 0,3,5,6; zero mask scores zero.

    Neighbors are sorted, so bit k encodes whether that vertex's kth edge
    participates in the even subgraph. Every nonzero degree is exactly two.
    """
    check_cubic_simple(base)
    if set(choices) != set(base):
        raise ValueError('must assign each base vertex')
    result = {}
    for v in base:
        c = choices[v]
        weights = [0]*8
        for i,j,mask in ((0,1,3),(0,2,5),(1,2,6)):
            spectrum = c.gadget.paths(c.permutation[i], c.permutation[j])
            lo,hi = min(spectrum),max(spectrum)
            if len(spectrum) != hi-lo+1:
                raise ValueError('path spectrum is non-interval; width theorem does not apply')
            weights[mask] = hi - 2*lo - 1
        result[v] = tuple(weights)
    return result


def cycle_basis_masks(base: nx.Graph):
    """Return independent F2 cycle generators as per-vertex three-bit masks."""
    nbrs = {v:sorted(base.neighbors(v)) for v in base}
    basis = []
    for C in nx.cycle_basis(base):
        term = {v:0 for v in base}
        for i,u in enumerate(C):
            w=C[(i+1)%len(C)]
            term[u] ^= 1<<nbrs[u].index(w)
            term[w] ^= 1<<nbrs[w].index(u)
        assert all(bin(k).count('1') in (0,2) for k in term.values())
        basis.append(term)
    return basis


def expectation_quarters(base: nx.Graph, scores, basis, fixed:tuple[int,...]=()) -> int:
    """Exact 4*E[score] with fixed leading basis coefficients.

    A random binary cycle-space element induces a uniform affine subspace
    of the 2-bit (four-state) local even-parity edge patterns at every node.
    Each local span thus has size 1, 2, or 4. No floating-point arithmetic.
    """
    k=len(fixed)
    total=0
    for v in base:
        offset=0
        for i,b in enumerate(fixed):
            if b:
                offset ^= basis[i][v]
        span={0}
        for term in basis[k:]:
            b=term[v]
            if b:
                span |= {x^b for x in tuple(span)}
            if len(span)==4:
                break
        assert 4%len(span)==0
        total += (4//len(span))*sum(scores[v][offset^mask] for mask in span)
    return total


def rooted_affine_basis(base: nx.Graph, basis, edge:tuple[int,int]):
    """Affine cycle-space basis conditioned on inclusion of one nonbridge edge.

    For basis bits x, fix the parity equation that edge (u,v) is present.
    Solving for one pivot coefficient expresses the conditional cycle space
    as offset XOR span(new_directions), without enumerating its elements.
    """
    u,v=edge
    if not base.has_edge(u,v):
        raise ValueError('requested edge absent')
    nbrs=sorted(base.neighbors(u))
    mask=1<<nbrs.index(v)
    piv=next((i for i,b in enumerate(basis) if b[u]&mask),None)
    if piv is None:
        return None  # edge is a bridge, no even subgraph can contain it
    offset=basis[piv]
    directions=[]
    for i,b in enumerate(basis):
        if i==piv:
            continue
        if b[u]&mask:
            directions.append({w:b[w]^offset[w] for w in base})
        else:
            directions.append(b)
    return offset,directions


def affine_expectation_quarters(base: nx.Graph, scores, offset, directions) -> int:
    """Exact four times the mean on an affine F2 cycle-space coset."""
    total=0
    for v in base:
        span={0}
        for d in directions:
            bit=d[v]
            if bit:
                span |= {x^bit for x in tuple(span)}
            if len(span)==4:
                break
        total+=(4//len(span))*sum(scores[v][offset[v]^x] for x in span)
    return total


def affine_cycle_witness(base: nx.Graph, scores, offset, directions):
    """Deterministic conditional expectation, preserving the affine constraint."""
    if affine_expectation_quarters(base,scores,offset,directions)<0:
        raise ValueError('negative conditional expectation')
    state=dict(offset)
    for i,d in enumerate(directions):
        remaining=directions[i+1:]
        lo=affine_expectation_quarters(base,scores,state,remaining)
        flipped={v:state[v]^d[v] for v in base}
        hi=affine_expectation_quarters(base,scores,flipped,remaining)
        if hi>lo:
            state=flipped
    assert sum(scores[v][state[v]] for v in base)>=0
    return state


def choose_even_subgraph(base: nx.Graph, scores, basis):
    """Conditional-expectation derandomization; returns a nonempty even subgraph.

    The theorem applies when E[score]>=0 and the base has cycles. To avoid
    selecting the trivial zero subgraph on ties, partition nonzero coefficient
    vectors by their first 1-bit and choose a cylinder with nonnegative
    conditional average. Each subsequent bit is fixed to preserve E>=0.
    """
    if not basis:
        raise ValueError('base has no cycles')
    if expectation_quarters(base,scores,basis) < 0:
        raise ValueError('cycle-space mean is negative; theorem is inconclusive')
    selected=None
    for i in range(len(basis)):
        prefix=(0,)*i+(1,)
        if expectation_quarters(base,scores,basis,prefix)>=0:
            selected=list(prefix)
            break
    if selected is None:
        raise AssertionError('nonempty cycle-space partition unexpectedly has negative mean')
    for i in range(len(selected),len(basis)):
        avg0=expectation_quarters(base,scores,basis,tuple(selected)+(0,))
        avg1=expectation_quarters(base,scores,basis,tuple(selected)+(1,))
        selected.append(0 if avg0>=avg1 else 1)
    states={v:0 for v in base}
    for i,b in enumerate(selected):
        if b:
            for v in base:
                states[v] ^= basis[i][v]
    assert any(states.values())
    assert sum(scores[v][states[v]] for v in base)>=0
    return states


def component_cycles(base: nx.Graph, states) -> list[tuple[int,...]]:
    H=nx.Graph()
    H.add_nodes_from(base)
    ns={v:sorted(base.neighbors(v)) for v in base}
    for u,v in base.edges():
        if states[u]&(1<<ns[u].index(v)):
            assert states[v]&(1<<ns[v].index(u))
            H.add_edge(u,v)
    assert all(H.degree[v] in (0,2) for v in H)
    result=[]
    for comp in nx.connected_components(H):
        if len(comp)<3:
            continue
        C=list(nx.cycle_basis(H.subgraph(comp)))
        assert len(C)==1
        result.append(tuple(C[0]))
    return result


def lift_cycle(base: nx.Graph, choices, C, target):
    """Choose path lengths constructively, then return a real expanded cycle."""
    ns={v:sorted(base.neighbors(v)) for v in base}
    items=[]
    for i,v in enumerate(C):
        a=ns[v].index(C[i-1]);b=ns[v].index(C[(i+1)%len(C)])
        ch=choices[v]
        lohi=ch.gadget.paths(ch.permutation[a],ch.permutation[b])
        lo,hi=min(lohi),max(lohi)
        assert len(lohi)==hi-lo+1
        items.append((v, ch, a, b, lo, hi))
    left=target-len(C)-sum(x[4] for x in items)
    if left<0 or left>sum(x[5]-x[4] for x in items):
        raise ValueError('requested length not in lifted interval')
    result=[]
    for v,ch,a,b,lo,hi in items:
        use=lo+min(left,hi-lo)
        left-=use-lo
        if ch.gadget.graph6 is None:
            path=[0]
        else:
            h=nx.from_graph6_bytes(ch.gadget.graph6.encode())
            src=ch.gadget.ports[ch.permutation[a]]
            dst=ch.gadget.ports[ch.permutation[b]]
            path=next(p for p in nx.all_simple_paths(h,src,dst) if len(p)-1==use)
        result.extend((v,w) for w in path)
    assert left==0
    graph=build_replacement(base,choices)
    assert len(result)==target==len(set(result))
    assert all(graph.has_edge(result[i], result[(i+1)%len(result)]) for i in range(len(result)))
    return tuple(result)


def _certificate_from_even_subgraph(base, choices, scores, states,
                                     mean4, kind) -> Obstruction:
    def cycle_score(C):
        value=0
        for i,v in enumerate(C):
            ns=sorted(base.neighbors(v))
            a=ns.index(C[i-1]);b=ns.index(C[(i+1)%len(C)])
            value+=scores[v][(1<<a)|(1<<b)]
        return value

    C=next((C for C in component_cycles(base,states) if cycle_score(C)>=0),None)
    assert C is not None
    m=len(C);M=len(C)
    for i,v in enumerate(C):
        ns=sorted(base.neighbors(v))
        a=ns.index(C[i-1]);b=ns.index(C[(i+1)%len(C)])
        ch=choices[v]
        paths=ch.gadget.paths(ch.permutation[a],ch.permutation[b])
        m+=min(paths);M+=max(paths)
    assert M>=2*m
    target=1<<(m-1).bit_length()
    assert m<=target<=M
    lifted=lift_cycle(base,choices,C,target)
    assert cycle_score(C)==M-2*m
    return Obstruction(sum(sum(scores[v][j] for j in (3,5,6)) for v in base),
                       mean4,tuple(C),target,m,M,lifted,kind)


def certify(base: nx.Graph, choices:dict[int,Choice], *,
            conditioned_edges:bool=False) -> Obstruction | None:
    """Prove a power-of-two cycle exists using cycle-space expectations.

    Unconditional average gives the analytic global density inequality.
    Optionally, stronger edge-conditioned affine averages are tried next.
    None means this sufficient obstruction did not fire; nothing more.
    """
    scores=local_scores(base,choices)
    basis=cycle_basis_masks(base)
    if not basis:
        return None
    mean4=expectation_quarters(base,scores,basis)
    if mean4>=0:
        states=choose_even_subgraph(base,scores,basis)
        return _certificate_from_even_subgraph(base, choices, scores, states,
                                                mean4,'unconditional')
    if conditioned_edges:
        for u,v in base.edges():
            affine=rooted_affine_basis(base,basis,(u,v))
            if affine is None:
                continue
            offset,directions=affine
            edge_mean4=affine_expectation_quarters(base,scores,offset,directions)
            if edge_mean4>=0:
                states=affine_cycle_witness(base,scores,offset,directions)
                return _certificate_from_even_subgraph(base,choices,scores,states,
                              edge_mean4,f'edge-conditioned:{u}-{v}')
    return None


def example_78(class_index:int=0) -> Obstruction:
    """Reproduce an exact certificate for one known 78-vertex family member."""
    data=json.loads(Path(__file__).with_name('exoo78_family.json').read_text())
    base=nx.from_graph6_bytes(data['base_graph6'].encode())
    opts={ch.name:ch for ch in choice_library(gadgets_from_catalog())}
    chosen={int(v):opts[name] for v,name in data['classes'][class_index]['choices'].items()}
    proof=certify(base,chosen)
    assert proof is not None
    return proof


if __name__=='__main__':
    p=example_78()
    print('H7/identity 78-vertex family:')
    print('sum of three local scores =',p.score_sum)
    print('cycle-space mean score =',p.average_score_quarters,'/ 4')
    print('forced base cycle length =',len(p.base_cycle))
    print('lift interval =',p.min_length,p.max_length)
    print('explicit power-of-two cycle =',p.lifted_length,'vertices')
