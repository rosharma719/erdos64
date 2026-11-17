#!/usr/bin/env python3
"""Reconstruct and validate a 78-vertex C4/C8/C16-free Exoo-type graph.

Computes explicit power-of-two cycles C32/C64 as machine-checkable
certificates. No reliance on the main cycle-length CSP to verify the
absence of C4/C8/C16 (a separate DFS oracle is used).
"""
from __future__ import annotations
from pathlib import Path
import json

import networkx as nx

from mixed_gadget_solver import (
    build_replacement, choice_library, gadgets_from_catalog,
    search_assignments, predicted_spectrum
)
from partial_triangle_expansion import independent_has_cycle_length, cycles

HERE = Path(__file__).resolve().parent
BASE_GRAPH6 = 'KL`AOWo?[G?R'


def representative():
    base=nx.from_graph6_bytes(BASE_GRAPH6.encode())
    opts=choice_library(gadgets_from_catalog())
    assignment=next(search_assignments(base,opts,{4,8,16}))
    assert sum(ch.gadget.size for ch in assignment.values())==78
    return base,assignment


def port_path(base, u, prev, nex, choice, length):
    gadget=choice.gadget
    if gadget.graph6 is None:
        assert length==0
        return [(u,0)]
    H=nx.from_graph6_bytes(gadget.graph6.encode())
    ns=sorted(base.neighbors(u))
    i=gadget.ports[choice.permutation[ns.index(prev)]]
    j=gadget.ports[choice.permutation[ns.index(nex)]]
    for path in nx.all_simple_paths(H,i,j):
        if len(path)-1==length:
            return [(u,v) for v in path]
    raise AssertionError('no gadget path of requested length')


def explicit_lift(base, choices, target):
    """Produce a simple cycle of precisely `target` nodes in the built graph."""
    for C in cycles(base):
        C=tuple(C)
        opts=[]
        for i,u in enumerate(C):
            neighbors=sorted(base.neighbors(u))
            a=neighbors.index(C[i-1]); b=neighbors.index(C[(i+1)%len(C)])
            choice=choices[u]
            opts.append(sorted(choice.gadget.paths(choice.permutation[a],choice.permutation[b])))
        # Dynamic programming with backtracking in (cycle index, used lengths).
        reachable={0:()}
        for lengths in opts:
            nxt={}
            for total,seq in reachable.items():
                for l in lengths:
                    if len(C)+total+l<=target:
                        nxt.setdefault(total+l,seq+(l,))
            reachable=nxt
        if target-len(C) not in reachable:
            continue
        seq=reachable[target-len(C)]
        result=[]
        for i,u in enumerate(C):
            result.extend(port_path(base,u,C[i-1],C[(i+1)%len(C)],choices[u],seq[i]))
        H=build_replacement(base,choices)
        assert len(result)==target and len(set(result))==target
        assert all(H.has_edge(result[i],result[(i+1)%len(result)]) for i in range(len(result)))
        return result
    raise AssertionError(f'no {target}-cycle found')


def make_certificate():
    B,assigned=representative()
    H=build_replacement(B,assigned)
    assert len(H)==78 and H.number_of_edges()==117 and nx.is_connected(H)
    assert all(d==3 for _,d in H.degree())
    for p in (4,8,16):
        assert not independent_has_cycle_length(H,p),p
    spectrum=predicted_spectrum(B,assigned)
    assert {32,64} <= spectrum
    cert={
        'base_graph6':BASE_GRAPH6,
        'gadget_library':{
            c.gadget.name: {'graph6': c.gadget.graph6, 'ports': list(c.gadget.ports)}
            for c in choice_library(gadgets_from_catalog()) if c.gadget.graph6 is not None
        },
        'vertex_choices':{str(u):assigned[u].name for u in sorted(assigned)},
        'expanded_order':len(H),
        'expanded_edges':H.number_of_edges(),
        'forbidden_checked_by_independent_dfs':[4,8,16],
        'present_power_of_two_cycles':{
            str(p):[[int(u),int(v)] for u,v in explicit_lift(B,assigned,p)] for p in (32,64)
        }
    }
    return cert


def verify_certificate(cert):
    B=nx.from_graph6_bytes(cert['base_graph6'].encode())
    opts={c.name:c for c in choice_library(gadgets_from_catalog())}
    assignments={int(u):opts[name] for u,name in cert['vertex_choices'].items()}
    H=build_replacement(B,assignments)
    assert len(H)==cert['expanded_order']==78 and H.number_of_edges()==cert['expanded_edges']==117
    assert nx.is_connected(H) and all(deg==3 for _,deg in H.degree())
    assert all(not independent_has_cycle_length(H,p) for p in cert['forbidden_checked_by_independent_dfs'])
    for length,cycle in cert['present_power_of_two_cycles'].items():
        path=[tuple(v) for v in cycle]
        assert len(path)==int(length) and len(set(path))==len(path)
        assert all(H.has_edge(path[i],path[(i+1)%len(path)]) for i in range(len(path)))
    return True


if __name__=='__main__':
    data=make_certificate()
    assert verify_certificate(data)
    target=HERE/'exoo78_certificate.json'
    target.write_text(json.dumps(data,indent=2)+'\n')
    print('verified 78-vertex cubic graph; no C4/C8/C16; explicit C32/C64 paths')
    print('certificate:',target)
