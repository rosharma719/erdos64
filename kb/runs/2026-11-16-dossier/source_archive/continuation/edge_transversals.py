from itertools import combinations
import networkx as nx, json,time
strings=['W??G?C??KCCBa?OCgO@O@C??O?IG??G?K`??CO?K@???C@@','WK?Y?CAGK?G`?G??_?O_@????@WOO@O?C@O??OOK??O??D@','W?GG?C??CO?FW?P?q??g@?_@A?GA??a?E?_??GAH?_??A?P','W?O@??O@COO@O_O?c?@?`c??P?GGG?W?C@@??o?G@@??E?@']

def dyadic_masks(g):
 n=len(g); A={i:sorted(g.neighbors(i)) for i in g}; E=sorted(tuple(sorted(e)) for e in g.edges()); Eindex={e:i for i,e in enumerate(E)}
 cycles=[]
 for L in (4,8,16,32):
  if L>n:continue
  for s in range(n):
   def dfs(u,path,visited):
    if len(path)==L:
     if s in A[u] and path[1]<path[-1]:
      edgebits=0
      for a,b in zip(path,path[1:]+[path[0]]):edgebits|=1<<Eindex[tuple(sorted((a,b)))]
      cycles.append((sum(1<<v for v in path),edgebits))
     return
    for v in A[u]:
     if v>s and not (visited>>v)&1:
      dfs(v,path+[v],visited|(1<<v))
   dfs(s,[s],1<<s)
 return E,cycles

def transversals(g):
 E,C=dyadic_masks(g);N=len(C);allc=(1<<N)-1
 masks_v=[];masks_e=[]
 for v in g:
  masks_v.append(sum(1<<i for i,(vb,eb) in enumerate(C) if (vb>>v)&1))
 for j in range(len(E)):
  masks_e.append(sum(1<<i for i,(vb,eb) in enumerate(C) if (eb>>j)&1))
 failures_per_root=[]; examples={}
 for r in g:
  fatal=[]
  for i,j in combinations(range(len(E)),2):
   if (masks_v[r]|masks_e[i]|masks_e[j])==allc:
    fatal.append((i,j))
  failures_per_root.append(len(fatal))
  if fatal:examples[r]=[(E[i],E[j]) for i,j in fatal[:3]]
 pairs_unrooted=sum((masks_e[i]|masks_e[j])==allc for i,j in combinations(range(len(E)),2))
 return N,max(failures_per_root),sum(x>0 for x in failures_per_root),sum(failures_per_root),pairs_unrooted,examples
if __name__=='__main__':
 for s in strings:
  g=nx.from_graph6_bytes(s.encode());t=time.perf_counter()
  print(s,'results',transversals(g),'time',round(time.perf_counter()-t,2),flush=True)
