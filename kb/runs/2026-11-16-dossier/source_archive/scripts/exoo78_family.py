#!/usr/bin/env python3
"""Classify the 48 admissible 78-vertex replacements of one 12-vertex base.

Output includes one graph6 and independent explicit C32/C64 witness for
all six isomorphism classes. This is a limited base-graph classification,
not a global 78-vertex census.
"""
from __future__ import annotations
from pathlib import Path
import json
import networkx as nx
from mixed_gadget_solver import (
    build_replacement, choice_library, gadgets_from_catalog,
    search_assignments, predicted_spectrum,
)
from exoo78_witness import BASE_GRAPH6, explicit_lift
from partial_triangle_expansion import independent_has_cycle_length


def family():
    B=nx.from_graph6_bytes(BASE_GRAPH6.encode())
    opts=choice_library(gadgets_from_catalog())
    classes=[]
    assignments=0
    for a in search_assignments(B,opts,{4,8,16}):
        assignments+=1
        H=build_replacement(B,a)
        for cls in classes:
            if nx.vf2pp_is_isomorphic(H,cls['graph']):
                cls['multiplicity']+=1
                break
        else:
            classes.append({'graph':H,'assignment':a,'multiplicity':1})
    assert assignments==48 and len(classes)==6
    result=[]
    for cls in classes:
        H=cls['graph'];a=cls['assignment']
        assert len(H)==78 and nx.is_connected(H) and all(d==3 for _,d in H.degree())
        assert not nx.check_planarity(H)[0]
        assert all(not independent_has_cycle_length(H,p) for p in (4,8,16))
        assert {32,64} <= predicted_spectrum(B,a)
        result.append({
            'assignments_in_class':cls['multiplicity'],
            'choices':{str(u):a[u].name for u in sorted(a)},
            'expanded_graph6':nx.to_graph6_bytes(nx.convert_node_labels_to_integers(H),header=False).decode().strip(),
            'cycle_32':[[int(u),int(v)] for u,v in explicit_lift(B,a,32)],
            'cycle_64':[[int(u),int(v)] for u,v in explicit_lift(B,a,64)],
        })
    assert sorted(cls['assignments_in_class'] for cls in result)==[6,6,6,6,12,12]
    return {'base_graph6':BASE_GRAPH6,'choices_count':assignments,
            'isomorphism_class_count':len(classes),'classes':result}


if __name__=='__main__':
    data=family()
    path=Path(__file__).with_name('exoo78_family.json')
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(f"verified {data['choices_count']} assignments, {data['isomorphism_class_count']} isomorphism classes")
    print(path)
