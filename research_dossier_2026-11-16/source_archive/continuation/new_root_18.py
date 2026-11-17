from bridge_root_18 import bridged
from edge_transversals import dyadic_masks
import networkx as nx,itertools,json,time
from collections import Counter

def has_cycle_4or8_avoiding(G,avoid):
 A=[tuple(G[v]) for v in G];n=len(G)
 for L in (4,8):
  for s in range(n):
   if s==avoid:continue
   def dfs(u,d,mask):
    if d==L: return s in A[u]
    for w in A[u]:
     if w>s and w!=avoid and not (mask>>w)&1:
      if dfs(w,d+1,mask|(1<<w)):return True
    return False
   if dfs(s,1,1<<s):return L
 return None

t=time.perf_counter(); cnt=Counter();bad=[]
with open('/mnt/data/eg-work/prime_n16.g6') as f:lines=[x.strip() for x in f if x.strip()]
for idx,line in enumerate(lines):
 G=nx.from_graph6_bytes(line.encode());E,C=dyadic_masks(G);C=[x for x in C if x[0].bit_count()<=8]
 allc=(1<<len(C))-1;me=[0]*len(E)
 for i,(vb,eb) in enumerate(C):
  for j in range(len(E)):
   if (eb>>j)&1:me[j]|=1<<i
 for a,b in itertools.combinations(range(len(E)),2):
  e,f=E[a],E[b]
  if len(set(e+f))!=4:continue
  if (allc&~(me[a]|me[b])):continue
  cnt['exceptional_newroot_bridges']+=1
  H=bridged(G,e,f)
  q=has_cycle_4or8_avoiding(H,16)
  if q:cnt[f'repair_q{q}']+=1
  else:
   bad.append({'index':idx,'pair':(e,f),'graph6':line})
   print('COUNTER',bad[-1],flush=True)
   break
 if bad:break
print('FINAL',dict(cnt),'bad',bad,'seconds',round(time.perf_counter()-t,2))
with open('/mnt/data/eg-work/new_root18_results.json','w') as f:json.dump({'count':dict(cnt),'bad':bad},f,indent=2)
