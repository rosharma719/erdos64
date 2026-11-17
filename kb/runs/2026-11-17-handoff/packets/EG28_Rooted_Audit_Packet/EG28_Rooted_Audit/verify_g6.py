#!/usr/bin/env python3
"""Exact rooted C16 checker for graph6 cubic graphs.

Usage:
    python verify_g6.py controls.g6 --output controls.json
    python verify_g6.py markstrom_28.g6 --expect-count 251 --strict --output results.json

Exactness:
 - C16: two internally disjoint length-8 paths joining the same pair of endpoints.
 - C4/C8: exhaustive bounded simple-cycle search.
 - cyclic 3-cuts: exhaustive triples of edges, connected-components and cycle-rank.
 - 3-vertex-connectivity: NetworkX node connectivity.

A result for 251 input graphs is NOT proof of exhaustiveness unless the input
is independently certified to be the complete 28-vertex family.
"""
import argparse
from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path
import networkx as nx


def graph_from_g6(line):
    g = nx.from_graph6_bytes(line.strip().encode('ascii'))
    if any(g.has_edge(v, v) for v in g):
        raise ValueError('loops')
    return nx.convert_node_labels_to_integers(g, ordering='sorted')


def find_cycle_dfs(g, length, avoiding=None):
    """Independent exhaustive simple-cycle oracle, one certificate or None."""
    adj = [tuple(sorted(g[v])) for v in range(len(g))]
    n = len(adj)
    if n-(avoiding is not None) < length:
        return None
    def walk(start, u, seen, path):
        if len(path) == length:
            return tuple(path) if start in adj[u] else None
        for v in adj[u]:
            if v <= start or v == avoiding or seen & (1 << v):
                continue
            hit = walk(start, v, seen | (1 << v), path + [v])
            if hit is not None:
                return hit
        return None
    for start in range(n):
        if start == avoiding:
            continue
        hit = walk(start, start, 1 << start, [start])
        if hit:
            return hit
    return None


def length_eight_paths(g, source, avoiding=None):
    """Enumerate all simple 8-edge paths from source, with vertex bitmasks."""
    adj = [tuple(g[v]) for v in range(len(g))]
    stack = [(source, (source,), 1 << source)]
    while stack:
        u, path, mask = stack.pop()
        if len(path) == 9:
            yield path, mask
            continue
        for v in adj[u]:
            if v != avoiding and not ((mask >> v) & 1):
                stack.append((v, path + (v,), mask | (1 << v)))


def find_c16_mitm(g, avoiding=None):
    """Exact C16 oracle: two internally disjoint 8-paths with identical endpoints."""
    n = len(g)
    if n - (avoiding is not None) < 16:
        return None
    for start in range(n):
        if start == avoiding:
            continue
        groups = defaultdict(list)
        for path, mask in length_eight_paths(g, start, avoiding):
            last = path[-1]
            group = groups[last]
            endpoints_mask = (1 << start) | (1 << last)
            # Every pair of internally disjoint 8-paths forms exactly one 16-cycle.
            for other, old_mask in group:
                if mask & old_mask == endpoints_mask:
                    result = path + other[-2:0:-1]
                    assert len(result) == 16 and len(set(result)) == 16
                    return result
            group.append((path, mask))
    return None


def cycle_valid(g, cycle, length, avoiding=None):
    c = list(cycle)
    return (len(c) == length and len(set(c)) == length
            and (avoiding is None or avoiding not in c)
            and all(g.has_edge(c[i], c[(i+1) % length]) for i in range(length)))


def cyclic_three_edge_cut(g):
    """Exact witness triple or None, meaningful for connected cubic graphs."""
    edges = list(g.edges())
    vs = list(g.nodes())
    adj = {v: tuple(g[v]) for v in vs}
    for banned3 in combinations(range(len(edges)), 3):
        banned = {frozenset(edges[j]) for j in banned3}
        seen = set()
        cyc_components = []
        for start in vs:
            if start in seen:
                continue
            todo=[start]
            seen.add(start)
            vertices=[]
            while todo:
                u=todo.pop();vertices.append(u)
                for v in adj[u]:
                    if frozenset((u, v)) in banned:
                        continue
                    if v not in seen:
                        seen.add(v);todo.append(v)
            if len(vertices) == len(vs):
                break
            vc=set(vertices)
            internal=sum(1 for u in vertices for v in adj[u]
                         if v in vc and frozenset((u,v)) not in banned)//2
            if internal >= len(vertices):
                cyc_components.append(sorted(vertices))
                if len(cyc_components)>1:
                    return {'edges': [list(edges[j]) for j in banned3],
                            'cyclic_components':cyc_components}
    return None


def analyze(g, g6, strict=False, independent=True):
    n=len(g)
    if any(g.degree(v) != 3 for v in g):
        raise ValueError(f'non-cubic input: {g6}')
    if not nx.is_connected(g):
        raise ValueError(f'disconnected input: {g6}')
    if strict and n!=28:
        raise ValueError('strict census input must be order 28')
    c4=find_cycle_dfs(g,4)
    c8=find_cycle_dfs(g,8)
    tri=sum(nx.triangles(g).values())//3
    if strict and (c4 is not None or c8 is not None):
        raise ValueError('strict candidate has forbidden cycle')
    connected3=nx.node_connectivity(g)>=3
    cut = cyclic_three_edge_cut(g) if tri==0 and connected3 else None
    prime = connected3 and tri==0 and cut is None
    # Successive dyadic witnesses cover every vertex not lying on their cycle.
    # For the Markström 28-vertex C4/C8-free family this reduces exactly to C16.
    if n>28:
        raise ValueError('this bounded oracle is designed for graphs with n<=28')
    remaining=set(range(n))
    witnesses=[]
    bad=[]
    while remaining:
        root=min(remaining)
        hit=None
        for target in (4,8,16):
            if target>n:
                continue
            if target==4 and c4 is None or target==8 and c8 is None:
                continue
            candidate = (find_c16_mitm(g,avoiding=root) if target==16
                         else find_cycle_dfs(g,target,avoiding=root))
            if candidate is not None:
                hit=candidate
                break
            if independent and target==16:
                assert find_cycle_dfs(g,16,avoiding=root) is None, ('oracles disagree',g6,root)
        if hit is None:
            bad.append(root)
            remaining.remove(root)
        else:
            assert cycle_valid(g,hit,len(hit),root)
            if independent and len(hit)==16:
                assert find_cycle_dfs(g,16,avoiding=root) is not None, ('oracles disagree',g6,root)
            witnesses.append({'avoid_root':root,'length':len(hit),'cycle':list(hit)})
            remaining.difference_update(set(range(n))-set(hit))
    return {'graph6':g6, 'n':n, 'triangles':tri, 'has_C4':bool(c4), 'has_C8':bool(c8),
            'three_vertex_connected':connected3, 'cyclic_three_cut_witness':cut,
            'cyclically_four_edge_connected':prime,
            'root_critical_vertices':bad,
            'dyadic_witnesses':witnesses,
            'dyadic_witness_count':len(witnesses)}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('g6file',type=Path)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--expect-count',type=int)
    p.add_argument('--strict',action='store_true')
    p.add_argument('--skip-independent',action='store_true')
    a=p.parse_args()
    lines=[l.strip() for l in a.g6file.read_text().splitlines() if l.strip() and not l.startswith('#')]
    if a.expect_count is not None and len(lines)!=a.expect_count:
        raise ValueError(f'Expected exactly {a.expect_count} graphs, found {len(lines)}')
    results=[]
    for i,line in enumerate(lines):
        g=graph_from_g6(line)
        x=analyze(g,line,a.strict,not a.skip_independent)
        results.append(x)
        print(f'{i+1}/{len(lines)} n={x["n"]} prime={x["cyclically_four_edge_connected"]} critical={x["root_critical_vertices"]}',flush=True)
    summary={'total_input':len(lines),
             'C4_C8_free':sum(not x['has_C4'] and not x['has_C8'] for x in results),
             'prime_C4_C8_free':sum(x['cyclically_four_edge_connected'] and not x['has_C4'] and not x['has_C8'] for x in results),
             'root_critical':sum(bool(x['root_critical_vertices']) for x in results),
             'prime_root_critical':sum(x['cyclically_four_edge_connected'] and bool(x['root_critical_vertices']) for x in results)}
    a.output.write_text(json.dumps({'summary':summary,'results':results},indent=2))
    print('SUMMARY:',json.dumps(summary,sort_keys=True))

if __name__=='__main__':
    main()
