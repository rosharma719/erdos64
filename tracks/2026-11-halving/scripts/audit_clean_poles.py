#!/usr/bin/env python3
"""Audit connected cubic 3-poles of orders 3,5,7,9,11 from capped catalogs.

IMPORTANT: this is conditional on the completeness of the supplied cubic catalogs;
only order 5 is also independently checked by direct enumeration here.
"""
from __future__ import annotations
import itertools
import json
import sys
from pathlib import Path
import networkx as nx

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from mixed_gadget_solver import make_gadget, exoo_h15


def capped_bases(order: int) -> list[nx.Graph]:
    if order == 4:
        return [nx.complete_graph(4)]
    if order == 6:
        return [nx.circular_ladder_graph(3), nx.complete_bipartite_graph(3,3)]
    if order == 12:
        return [nx.from_graph6_bytes(s.encode()) for s in json.loads((HERE/'cubic_catalog_n12.json').read_text())]
    cat=json.loads((HERE/'cubic_catalog_n8_n10.json').read_text())
    return [nx.from_graph6_bytes(s.encode()) for s in cat['connected_cubic'][str(order)]]



def record_from_graph6(g6: str) -> dict:
    """Describe a pole from its graph6 alone: ports are the degree-2 vertices.

    The Gadget objects from mixed_gadget_solver store port labels that need not
    match the vertex order of their graph6 string (make_gadget writes graph6 in
    node-iteration order, not label order). Deriving everything from the graph6
    keeps each stored record self-consistent.
    """
    G = nx.from_graph6_bytes(g6.encode())
    ports = sorted(v for v in G if G.degree(v) == 2)
    assert len(ports) == 3, f"expected exactly three degree-2 vertices, found {len(ports)}"
    assert all(G.degree(v) == 3 for v in G if v not in ports), "non-port vertex of degree != 3"
    assert nx.is_connected(G), "pole must be connected"
    pairs = [(ports[0], ports[1]), (ports[0], ports[2]), (ports[1], ports[2])]
    paths = [sorted({len(q) - 1 for q in nx.all_simple_paths(G, a, b)}) for a, b in pairs]
    cyc = sorted({len(c) for c in nx.simple_cycles(G.to_directed()) if len(c) >= 3})
    return {'graph6': g6, 'ports': ports, 'path_length_sets': paths, 'internal_cycles': cyc,
            'is_clean': not any(L >= 4 and L & (L - 1) == 0 for L in cyc)}

def no_power_two_cycle(gadget) -> bool:
    return not any(v >= 4 and (v & (v-1)) == 0 for v in gadget.internal_cycle_lengths)


def pole_isomorphic(A, B) -> bool:
    GA=nx.from_graph6_bytes(A.graph6.encode());GB=nx.from_graph6_bytes(B.graph6.encode())
    for x in GA: GA.nodes[x]['port'] = x in A.ports
    for x in GB: GB.nodes[x]['port'] = x in B.ports
    return nx.is_isomorphic(GA,GB,node_match=lambda a,b:a['port']==b['port'])


def enumerate_clean_from_capped(order:int):
    outputs=[]
    bases=capped_bases(order+1)
    for G in bases:
        for root in G:
            H=G.copy(); H.remove_node(root)
            if not nx.is_connected(H):continue
            cand=make_gadget('candidate',H,G.neighbors(root))
            if not no_power_two_cycle(cand):continue
            if not any(pole_isomorphic(cand, known) for known in outputs):outputs.append(cand)
    return len(bases),outputs


def brute_5() -> int:
    # Exhaustively enumerate all 2^10 simple graphs on 5 labeled vertices.
    edges=list(itertools.combinations(range(5),2))
    count=0
    for mask in range(1<<len(edges)):
        G=nx.Graph();G.add_nodes_from(range(5));G.add_edges_from(e for j,e in enumerate(edges) if mask>>j&1)
        if sorted(d for _,d in G.degree()) != [2,2,2,3,3]:continue
        if not nx.is_connected(G):continue
        count+=1
        # Every candidate must contain a 4-cycle; this checks the hand proof.
        for p in itertools.permutations(range(5),4):
            if len(set(p))==4 and all(G.has_edge(p[i],p[(i+1)%4]) for i in range(4)):
                break
        else:raise AssertionError('Found counterexample to order-5 lemma')
    return count


def main():
    report={'order5_labeled_degree_pattern_graphs':brute_5(),'census':{}}
    for order in (3,5,7,9,11):
        base_count, survivors=enumerate_clean_from_capped(order)
        report['census'][str(order)]={'capped_connected_cubic_classes':base_count,
            'surviving_unordered_marked_3_pole_classes':len(survivors),
            'representatives':[record_from_graph6(g.graph6) for g in survivors]}
    h15=exoo_h15()
    rec=record_from_graph6(h15.graph6)
    assert sorted(map(tuple,rec['path_length_sets'])) == sorted(tuple(sorted(p)) for p in h15.pair_paths), \
        'graph6-derived path sets disagree with the gadget object'
    assert rec['is_clean'] == no_power_two_cycle(h15)
    report['one_known_15_vertex_example']=rec
    assert [report['census'][str(k)]['surviving_unordered_marked_3_pole_classes'] for k in (3,5,7,9,11)] == [1,0,2,0,0]
    assert report['one_known_15_vertex_example']['is_clean']
    out=HERE/'clean_pole_small_audit.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print('Independent labeled order-5 check:',report['order5_labeled_degree_pattern_graphs'],'graphs, all contain C4')
    print('order, cap-cubic classes, clean 3-pole classes')
    for k,item in report['census'].items():print(k,item['capped_connected_cubic_classes'],item['surviving_unordered_marked_3_pole_classes'])
    print('Exoo H15 clean:',report['one_known_15_vertex_example']['is_clean'])
    print('Wrote:',out)

if __name__=='__main__':main()
