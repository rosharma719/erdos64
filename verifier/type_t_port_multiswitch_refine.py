#!/usr/bin/env python3
"""Beam/tabu refinement of a C4/C8-free Type-T port matching."""

import argparse
import collections
import json
import math
import random
import time

from type_t_port_core_export import build_core
from type_t_port_matching_sat import one_edge_incompatibilities, powers_up_to, enumerate_cycles_exact
from type_t_port_multiswitch import (
    cycle_edges, edge, full_cycles, random_repair, update_cycles,
)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True); ap.add_argument('--output',required=True)
    ap.add_argument('--seed',type=int,required=True); ap.add_argument('--steps',type=int,default=300)
    ap.add_argument('--beam',type=int,default=8); ap.add_argument('--audit-every',type=int,default=50)
    ns=ap.parse_args(); rng=random.Random(ns.seed)
    payload=json.load(open(ns.input)); q=payload['parameters']
    core=build_core(q['j'],q['a'],q['c']); vertices=core.deficient_vertices()
    bad=one_edge_incompatibilities(core,powers_up_to(core.order)); core_edges=set(core.edges)
    allowed={edge(u,v) for i,u in enumerate(vertices) for v in vertices[i+1:]
             if edge(u,v) not in core_edges and edge(u,v) not in bad}
    matching=[tuple(x) for x in payload['matching_edges']]
    adjacency=[set(x) for x in core.adjacency()]
    for u,v in matching: adjacency[u].add(v);adjacency[v].add(u)
    cycles={L:full_cycles(adjacency,L) for L in (4,8,16)}
    assert not cycles[4] and not cycles[8]
    best=(len(cycles[16]),sorted(matching)); best_it=0; accepted=0
    start=time.monotonic(); tabu=collections.deque(maxlen=40)

    for it in range(ns.steps):
        idx={uv:i for i,uv in enumerate(matching)}
        participation=collections.Counter()
        for cy in cycles[16]: participation.update(cycle_edges(cy)&idx.keys())
        top=[uv for uv,_ in participation.most_common(max(8,len(matching)//4))]
        candidates=[]
        for trial in range(ns.beam):
            p=rng.random(); k=2 if p<.5 else (3 if p<.82 else 4)
            selected={idx[rng.choice(top)] if top else rng.randrange(len(matching))}
            while len(selected)<k: selected.add(rng.randrange(len(matching)))
            selected=sorted(selected); removed=[matching[i] for i in selected]
            added=random_repair([x for uv in removed for x in uv],allowed,rng,removed)
            if added is None or tuple(sorted(added)) in tabu: continue
            rs,ads=set(removed),set(added)
            for u,v in removed: adjacency[u].remove(v);adjacency[v].remove(u)
            for u,v in added: adjacency[u].add(v);adjacency[v].add(u)
            c4=update_cycles(cycles[4],adjacency,rs,ads,4)
            c8=update_cycles(cycles[8],adjacency,rs,ads,8) if not c4 else {()}
            if not c4 and not c8:
                c16=update_cycles(cycles[16],adjacency,rs,ads,16)
                candidates.append((len(c16),rng.random(),selected,removed,added,c16))
            for u,v in added: adjacency[u].remove(v);adjacency[v].remove(u)
            for u,v in removed: adjacency[u].add(v);adjacency[v].add(u)
        if not candidates: continue
        score,_,selected,removed,added,c16=min(candidates)
        current=len(cycles[16]); temp=max(.15,12*(1-it/max(1,ns.steps)))
        if score<=current or rng.random()<math.exp((current-score)/temp):
            for u,v in removed: adjacency[u].remove(v);adjacency[v].remove(u)
            for u,v in added: adjacency[u].add(v);adjacency[v].add(u)
            for off,i in enumerate(selected): matching[i]=added[off]
            cycles[16]=c16; accepted+=1; tabu.append(tuple(sorted(removed)))
            if score<best[0]: best=(score,sorted(matching));best_it=it
        if ns.audit_every and it and it%ns.audit_every==0:
            assert cycles[16]==full_cycles(adjacency,16),(it,len(cycles[16]))

    score,matching=best; adjacency=[set(x) for x in core.adjacency()]
    for u,v in matching: adjacency[u].add(v);adjacency[v].add(u)
    exact={str(L):len(full_cycles(adjacency,L)) for L in (4,8,16)}
    witnesses={}; frozen=tuple(map(frozenset,adjacency))
    for L in (16,32,64,128):
        found,_=enumerate_cycles_exact(frozen,L,1)
        if found:witnesses[str(L)]=list(found[0])
    out={**payload,'refinement':{'method':'exact-incremental beam/tabu 2/3/4-switch',
          'parent':ns.input,'seed':ns.seed,'steps':ns.steps,'beam':ns.beam,
          'accepted':accepted,'best_iteration':best_it,'elapsed_seconds':time.monotonic()-start},
          'exact_short_profile':exact,'power_cycle_witnesses':witnesses,
          'matching_edges':[list(x) for x in matching]}
    with open(ns.output,'w') as f:json.dump(out,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps({'parameters':q,'seed':ns.seed,'parent':ns.input,'accepted':accepted,
                      'best_iteration':best_it,'elapsed_seconds':out['refinement']['elapsed_seconds'],
                      'exact_short_profile':exact}))

if __name__=='__main__':main()
