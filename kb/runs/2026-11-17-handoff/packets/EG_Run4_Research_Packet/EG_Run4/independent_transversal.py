import itertools,networkx as nx
from pathlib import Path
G=nx.from_graph6_bytes(Path(__file__).with_name('coxeter.g6').read_bytes().strip())
# Independent DFS with directed-edge orientation filter; retain vertex-set masks only.
def masks(k):
 out=set()
 for s in G:
  stack=[(s,[s],1<<s)]
  while stack:
   u,path,used=stack.pop()
   if len(path)==k:
    if G.has_edge(u,s) and path[1]<path[-1]:out.add(used)
    continue
   for v in G[u]:
    if v>s and not used&(1<<v):stack.append((v,path+[v],used|(1<<v)))
 return out
for k,tau,w in [(8,6,(0,1,3,6,9,14)),(16,5,(0,1,3,9,15))]:
 C=masks(k)
 print('length',k,'unique vertex sets',len(C))
 assert all(any(not(c&sum(1<<v for v in S)) for c in C) for r in range(tau) for S in itertools.combinations(range(28),r))
 assert all(c&sum(1<<v for v in w) for c in C)
 print('verified tau',tau)
