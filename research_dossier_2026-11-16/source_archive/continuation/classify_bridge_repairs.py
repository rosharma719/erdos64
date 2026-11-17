"""Classify exact repair type for n16 prime -> n18 bridge exceptions.
In child, a C4 or C8 using bridge xy is a path repair, and a cycle avoiding
xy is a shifted-parent-cycle repair if no untouched parent C survived.
"""
import itertools,time,json,collections
import networkx as nx
from edge_transversals import dyadic_masks

def cycles4or8(g):
 n=len(g);A=[sorted(g[v]) for v in g];out=[]
 for L in (4,8):
  for s in range(n):
   def dfs(u,path,used):
    if len(path)==L:
     if s in A[u] and path[1]<path[-1]:
      out.append((set(path),{frozenset((a,b)) for a,b in zip(path,path[1:]+[s])},L))
     return
    for w in A[u]:
     if w>s and not (used>>w)&1:
      dfs(w,path+[w],used|(1<<w))
   dfs(s,[s],1<<s)
 return out

def run():
 from bridge_root_18 import bridged
 out=collections.Counter();ex=[];t=time.perf_counter();m=0
 with open('/mnt/data/eg-work/prime_n16.g6') as f:lines=[line.strip() for line in f if line.strip()]
 for ig,line in enumerate(lines):
  G=nx.from_graph6_bytes(line.encode()); E,C=dyadic_masks(G); allc=(1<<len(C))-1
  ve=[0]*len(G);ed=[0]*len(E)
  for idx,(vb,eb) in enumerate(C):
   for r in G:
    if vb>>r&1:ve[r]|=1<<idx
   for j in range(len(E)):
    if eb>>j&1:ed[j]|=1<<idx
  for a,b in itertools.combinations(range(len(E)),2):
   e,f=E[a],E[b]
   if len(set(e+f))!=4:continue
   surv=allc&~(ed[a]|ed[b]); roots=[r for r in G if not (surv&~ve[r]&allc)]
   if not roots:continue
   H=bridged(G,e,f); D=cycles4or8(H);bridge=frozenset((16,17))
   for r in roots:
    types=set('path' if bridge in edges else 'shift' for vv,edges,q in D if r not in vv)
    out[(tuple(sorted(types)))]+=1
    if not types:ex.append({'parent_index':ig,'pair':[e,f],'root':r})
  if ig%100==0:print('progress',ig,'counts',dict(out),'time',round(time.perf_counter()-t,1),flush=True)
 print('FINAL',dict(out),'fail',ex[:3],'seconds',round(time.perf_counter()-t,2),flush=True)
 with open('/mnt/data/eg-work/repair_classification.json','w') as f:
  json.dump({'class_counts':{'-'.join(k):v for k,v in out.items()},'errors':ex,'seconds':round(time.perf_counter()-t,2)},f,indent=2)
if __name__=='__main__':run()
