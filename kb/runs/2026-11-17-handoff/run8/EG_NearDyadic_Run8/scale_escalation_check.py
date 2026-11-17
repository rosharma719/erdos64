#!/usr/bin/env python3
"""Independent finite check of the two-edge-overlap obstruction at g=9.

Generates a theta graph of two C9s sharing a path of length t, t=2,3,4.
Then exhausts *all* distinct ways of adding a third C9 that uses the
new third edge at vertex 1, modulo the labels of fresh interior vertices.
No networkx needed for this search. For t=2 there are 0 possibilities,
matching the theorem; t=3 and 4 have possibilities, so a stronger claim
about individual off-path edges at longer overlaps would be false.
"""
from collections import Counter


def theta(t,cap=23):
    adj=[set() for _ in range(cap)]
    def add(a,b):adj[a].add(b);adj[b].add(a)
    for i in range(t):add(i,i+1)
    fresh=t+1
    for arm in range(2):
        v=0
        for j in range(8-t):
            add(v,fresh);v=fresh;fresh+=1
        add(v,t)
    return adj,fresh


def exact_path(adj,u,v,steps,mask):
    if steps==0:return u==v
    for z in adj[u]:
        if z==v:
            if steps==1:return True
        elif steps>1 and not(mask & (1<<z)):
            if exact_path(adj,z,v,steps-1,mask|(1<<z)):return True
    return False


def search(t):
    adj,n=theta(t)
    x=1
    ends=set(adj[x])
    first=n
    adj[x].add(first);adj[first].add(x)
    nodes=0;goods=[]
    def walk(current,seq,fresh,mask):
        nonlocal nodes
        nodes+=1
        depth=len(seq)-1
        if depth==8:
            if current in ends:goods.append(tuple(seq))
            return
        candidates=(list(range(n))+[fresh]) if depth<7 else list(ends)
        for z in candidates:
            if z==x or mask & (1<<z):continue
            if z in adj[current]:inserted=False
            else:
                if len(adj[current])>=3 or len(adj[z])>=3:continue
                if any(exact_path(adj,current,z,L-1,1<<current)
                       for L in [3,4,5,6,7,8,16]):continue
                adj[current].add(z);adj[z].add(current);inserted=True
            walk(z,seq+[z],fresh+int(z==fresh),mask|(1<<z))
            if inserted:adj[current].remove(z);adj[z].remove(current)
    walk(first,[x,first],first+1,(1<<x)|(1<<first))
    return dict(shared_path_edges=t,visited_states=nodes,
                third_C9_witnesses=len(goods),witness_sequences=[list(z) for z in goods[:12]])


if __name__=='__main__':
    for t in (2,3,4):
        print(search(t))
