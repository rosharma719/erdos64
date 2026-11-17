#!/usr/bin/env python3
"""Construct explicit 4-regular graph whose edges are all triangular, but C4/C8 absent.

Cyclic voltage lift of Petersen to girth>=9, then take its line graph.
"""
import networkx as nx, random, json, hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
B=nx.petersen_graph()
E=sorted(tuple(sorted(e)) for e in B.edges())
# Only simple base cycles lengths <=8 need nonzero voltage, because girth(B)=5.
C=set()
for cyc in nx.simple_cycles(B,length_bound=8):
 if len(cyc)>=5:
  key=min(tuple(cyc[i:]+cyc[:i]) for i in range(len(cyc)))
  C.add(key)
print('base cycles length<=8:', {i:sum(len(x)==i for x in C) for i in range(5,9)})

def weight(c, volt, p):
 acc=0
 for i,u in enumerate(c):
  v=c[(i+1)%len(c)]
  acc+=(1 if u<v else -1)*volt[min(u,v),max(u,v)]
 return acc%p

r=random.Random(20261117)
for p in [11,13,17,19,23]:
 for attempt in range(50000):
  v={e:r.randrange(p) for e in E}
  if all(weight(c,v,p)!=0 for c in C):break
 else:continue
 break
else:raise RuntimeError('Failed to find voltage assignment')
print('p=',p,'tries=',attempt+1)
L=nx.Graph()
for t in range(p):
 for u,vv in E:
  L.add_edge((u,t),(vv,(t+v[u,vv])%p))
assert L.number_of_nodes()==10*p
assert all(d==3 for _,d in L.degree())
# Compute graph girth by BFS; <=8 would invalidate construction.
def girth(G):
 g=10**9
 for s in G:
  dist={s:0};parent={s:None};q=[s]
  for x in q:
   for y in G[x]:
    if y not in dist:
     dist[y]=dist[x]+1;parent[y]=x;q.append(y)
    elif parent[x]!=y:
     g=min(g,dist[x]+dist[y]+1)
 return g
assert girth(L)>=9
A=nx.line_graph(L)
assert A.number_of_nodes()==15*p
assert all(d==4 for _,d in A.degree())
# Each line graph edge belongs to some triangle from the original degree-3 vertex.
for a,b in A.edges():
 assert set(A[a]).intersection(A[b])
# The absence of an 8-cycle is a consequence of base girth>=9.
# Check with an independent bounded DFS oracle as additional verification.
def has_k(G,k):
 labels={v:i for i,v in enumerate(G)}
 adj=[set(labels[v] for v in G[u]) for u in G]
 for s in range(len(adj)):
  def go(u, seen, depth):
   if depth==k:return s in adj[u]
   for w in adj[u]:
    if w>s and w not in seen:
     if go(w,seen|{w},depth+1):return True
   return False
  if go(s,{s},1):return True
 return False
assert not has_k(A,4)
assert not has_k(A,8)
N={v:i for i,v in enumerate(sorted(A.nodes()))}
raw=''.join(f'{min(N[x],N[y])} {max(N[x],N[y])}\n' for x,y in sorted(A.edges(),key=lambda e:tuple(sorted((N[e[0]],N[e[1]])))))
raw=''.join(sorted(raw.splitlines(keepends=True),key=lambda s:tuple(map(int,s.split()))))
(R/'line_graph_no_c4_c8.edges').write_text(raw)
report={'prime':p,'base_girth':girth(L),'base_vertices':L.number_of_nodes(),'line_graph_vertices':A.number_of_nodes(),
        'line_graph_edges':A.number_of_edges(),'line_graph_degree':4,'c4':False,'c8':False,
        'every_edge_in_triangle':True,'edge_list_sha256':hashlib.sha256(raw.encode()).hexdigest(),
        'petersen_voltage':{f'{u}-{v}':int(vv) for (u,v),vv in v.items()}}
(R/'high_degree_obstruction.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
