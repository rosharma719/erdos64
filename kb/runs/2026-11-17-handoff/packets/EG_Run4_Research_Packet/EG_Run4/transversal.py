import itertools,json,networkx as nx
from pathlib import Path
G=nx.from_graph6_bytes(Path(__file__).with_name('coxeter.g6').read_bytes().strip())
n=len(G)
def cycles(k):
    result=set()
    def dfs(start,path,seen):
        u=path[-1]
        if len(path)==k:
            if G.has_edge(u,start):
                p=tuple(path);result.add(min(p,(p[0],)+tuple(reversed(p[1:]))))
            return
        for v in G[u]:
            if v>start and not (seen>>v)&1:dfs(start,path+[v],seen|(1<<v))
    for s in G:dfs(s,[s],1<<s)
    return result
C8=cycles(8);C16=cycles(16)
assert (len(C8),len(C16))==(21,609)
def transversal(C):
    masks=[sum(1<<v for v in c) for c in C]
    for k in range(n+1):
        for S in itertools.combinations(range(n),k):
            m=sum(1<<v for v in S)
            if all(m & c for c in masks):return k,S
for name,cs in [('C8',C8),('C16',C16),('C8_or_C16',C8|C16)]:
    print(name,transversal(cs))
