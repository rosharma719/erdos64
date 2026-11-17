#!/usr/bin/env python3
"""Exact restricted-family census on all cubic bases of order <=10.

Connected cubic base catalogs: 1,2,5,19 nonisomorphic classes at n=4,6,8,10.
Every assignment of the 1/3/7-vertex gadgets (optionally H15) with all
port orientations is tested by an exact cycle-length constraint solver.
The n=12 fixture is also available, but running the FULL n=12 assignment
census is intentionally not claimed here: some cases are expensive.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import argparse
import json
import time
import networkx as nx
from census_small_bases import read_catalog
from mixed_gadget_solver import gadgets_from_catalog, choice_library, search_assignments


def all_bases():
    n12 = [nx.from_graph6_bytes(s.encode()) for s in json.loads(Path(__file__).with_name('cubic_catalog_n12.json').read_text())]
    return {
        4:[nx.complete_graph(4)],
        6:[nx.circular_ladder_graph(3),nx.complete_bipartite_graph(3,3)],
        **read_catalog(),
        12:n12,
    }


def run(include_h15=False, forbidden=None):
    if forbidden is None: forbidden={4,8,16}
    choices=choice_library(gadgets_from_catalog(include_h15=include_h15))
    print('oriented choices:', len(choices), [c.name for c in choices],flush=True)
    base_counts=Counter()
    survivor_counts=Counter()
    start=time.perf_counter()
    for n,graphs in sorted(all_bases().items()):
        if n>10: continue
        for i,B in enumerate(graphs):
            witness=next(search_assignments(B,choices,forbidden),None)
            if witness is not None:
                survivor_counts[n]+=1
                print(f'  base {n}, class {i}: found one assignment, expanded order={sum(ch.gadget.size for ch in witness.values())}',flush=True)
            base_counts[n]+=1
        print(f'base order {n}: checked {base_counts[n]} cubic classes, classes with survivors={survivor_counts[n]}',flush=True)
    print('complete restricted census:',dict(base_counts),'surviving base classes:',dict(survivor_counts), 'forbidden:',sorted(forbidden),
          'H15 included:',include_h15,'elapsed_s:',round(time.perf_counter()-start,2),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-h15',action='store_true')
    parser.add_argument('--forbid',type=int,nargs='+',default=[4,8,16])
    args=parser.parse_args()
    run(args.include_h15,set(args.forbid))
