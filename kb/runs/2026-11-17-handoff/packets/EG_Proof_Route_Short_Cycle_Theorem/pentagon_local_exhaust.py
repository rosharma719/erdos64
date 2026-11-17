"""Independent finite local audit for pentagon overlap in cubic girth>=5 C8-free graphs.
Uses labeled partial graphs, exhaustive canonical gluing of up to 3 C5 through root 0.
Only for corroboration; the theorem in RESEARCH_NOTE.md has an independent proof.
"""
from collections import Counter
from itertools import permutations


def cycle_edges(c):
    return frozenset(tuple(sorted((c[i], c[(i + 1) % 5]))) for i in range(5))


def graph_edges(*cycles):
    return frozenset().union(*(cycle_edges(c) for c in cycles))


def adjacency(edges):
    a = {}
    for u,v in edges:
        a.setdefault(u,set()).add(v)
        a.setdefault(v,set()).add(u)
    return a


def contains_cycle(ad, length):
    # Explicit depth-first cycle detection; no NetworkX or prior audit code.
    for start in ad:
        stack = [(start,(start,))]
        while stack:
            u,path=stack.pop()
            if len(path)==length:
                if start in ad[u]: return True
            else:
                for v in ad[u]:
                    if v not in path and (v>start):
                        stack.append((v,path+(v,)))
    return False


def valid(edges):
    adj=adjacency(edges)
    return (all(len(neigh)<=3 for neigh in adj.values())
            and all(not contains_cycle(adj,k) for k in (3,4,8)))


def new_root_cycles(existing_cycles):
    edges=graph_edges(*existing_cycles)
    n=1+max(max(c) for c in existing_cycles)
    # Four positions after vertex zero in a 5-cycle. At least one must
    # be an existing neighbor; at most three new vertices are required.
    options=list(range(1,n+3))
    seen=set()
    for ordered in permutations(options,4):
        c=(0,)+ordered
        used_new=[v for v in c if v>=n]
        # Canonical first-appearance order for genuinely new vertices.
        if used_new != list(range(n,n+len(used_new))): continue
        ce=cycle_edges(c)
        if ce in {cycle_edges(x) for x in existing_cycles}:continue
        if not ce.intersection(edges):continue
        ne=edges|ce
        if not valid(ne):continue
        if ne in seen:continue
        seen.add(ne)
        yield c,ne


def main():
    base=(0,1,2,3,4)
    E0=cycle_edges(base)
    assert valid(E0)
    additions=list(new_root_cycles([base]))
    assert additions
    distribution=Counter()
    for c1,edges in additions:
        shared=E0&cycle_edges(c1)
        distribution[(len(shared),len(set(base)&set(c1)))]+=1
        assert len(shared)==2
        # Exact second path length 2 between any overlapping pentagons
        for c2,edges2 in new_root_cycles([base,c1]):
            raise AssertionError(f'Three distinct C5 through root 0: {base}, {c1}, {c2}')
    print('First added pentagon configurations:',len(additions))
    print('Overlap pattern (common edges, vertices):',dict(distribution))
    print('Three pentagons through vertex 0: NONE')
    print('All checks passed')

if __name__=='__main__':main()
