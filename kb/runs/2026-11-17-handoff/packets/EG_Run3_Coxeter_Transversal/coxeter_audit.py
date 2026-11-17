import networkx as nx,itertools,json
G=nx.from_graph6_bytes(open('/mnt/data/EG_Run3/coxeter.g6','rb').read().strip())
n=len(G)
def cycles(k):
 out=set()
 for s in G:
  def dfs(path,seen):
   v=path[-1]
   if len(path)==k:
    if G.has_edge(v,s):out.add(frozenset(path)) if k==3 else out.add(tuple(path) if False else canonical(path))
    return
   for w in G[v]:
    if w>s and w not in seen:dfs(path+[w],seen|{w})
  dfs([s],{s})
 return out
def canonical(p):
 p=tuple(p);q=(p[0],)+tuple(reversed(p[1:]));return min(p,q)
cs={k:cycles(k) for k in (4,8,16)}
print('counts', {k:len(v) for k,v in cs.items()})
for k in (8,16):
 arr=cs[k]
 print(k,'avoid each min/max',min(sum(v not in c for c in arr) for v in G),max(sum(v not in c for c in arr) for v in G))
 for t in (1,2,3):
  bad=[S for S in itertools.combinations(G,t) if all(set(S)&set(c) for c in arr)]
  print('hitting',t,len(bad),'first',bad[:2])
  if bad:break
json.dump({'graph6':open('/mnt/data/EG_Run3/coxeter.g6').read().strip(),'cycle_counts':{str(k):len(v) for k,v in cs.items()}},open('/mnt/data/EG_Run3/coxeter_summary.json','w'))
