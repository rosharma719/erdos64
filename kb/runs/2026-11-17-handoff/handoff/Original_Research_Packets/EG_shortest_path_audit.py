#!/usr/bin/env python3
"""Small exact obstruction to an overstrong rooted Erdős–Gyárfás claim.

Uses Python stdlib only.  Run: python EG_shortest_path_audit.py
Cubic graph G: triangle with each corner bridged to a copy of K5 minus
edges (0,1), (0,2), (3,4).  Every cycle through triangle vertex 0 has
length 3.  Consequently some cubic vertices have no dyadic cycle through
 them, even though the whole graph has C4s.
"""
from collections import deque
from itertools import combinations

def construct():
    # vertices 0,1,2 are a triangle; caps occupy [3,7],[8,12],[13,17]
    n=18
    adj=[set() for _ in range(n)]
    def add(a,b):
        assert a!=b and b not in adj[a]
        adj[a].add(b);adj[b].add(a)
    for u,v in [(0,1),(1,2),(2,0)]: add(u,v)
    missing={(0,1),(0,2),(3,4)}
    for k in range(3):
        off=3+5*k
        for u,v in combinations(range(5),2):
            if (u,v) not in missing: add(off+u,off+v)
        add(k,off)  # single bridge to a copy of the cap
    return adj

def all_lengths_through(adj, root):
    # Exact DFS over all simple rooted cycles, no library heuristics.
    lengths=set()
    def dfs(cur, visited, length):
        for nxt in adj[cur]:
            if nxt == root:
                if length >= 3: lengths.add(length)
            elif not (visited >> nxt)&1:
                dfs(nxt, visited | (1<<nxt), length+1)
    for x in adj[root]: dfs(x, (1<<root)|(1<<x), 2)
    return lengths

def two_degenerate(adj, remove=None):
    alive=set(range(len(adj))) - ({remove} if remove is not None else set())
    while alive:
        available=[v for v in alive if len(adj[v] & alive)<=2]
        if not available: return False
        alive.remove(min(available))
    return True

def has_cycle4(adj):
    return any(len(adj[u]&adj[v])>=2 for u in range(len(adj)) for v in range(u+1,len(adj)))

def main():
    adj=construct()
    assert len(adj)==18 and all(len(s)==3 for s in adj)
    seen={0};q=deque([0])
    while q:
        for x in adj[q.popleft()]:
            if x not in seen:seen.add(x);q.append(x)
    assert len(seen)==18
    assert all_lengths_through(adj,0)=={3}
    assert two_degenerate(adj, remove=0)
    assert has_cycle4(adj)
    # A dyadic cycle needs >=4 edges.
    print('PASS: connected 18-vertex cubic graph; 27 edges')
    print('PASS: lengths of all cycles through root vertex 0 = [3]')
    print('PASS: G - vertex 0 is 2-degenerate')
    print('PASS: G contains C4 elsewhere, so it does not refute EG')
    print('Edges:',sorted((u,v) for u,s in enumerate(adj) for v in s if u<v))

if __name__=='__main__': main()
