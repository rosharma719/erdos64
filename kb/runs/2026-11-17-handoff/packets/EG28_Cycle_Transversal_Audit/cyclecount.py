import networkx as nx
from collections import Counter
from itertools import combinations
P='/mnt/data/EG28_Rooted_Audit/controls.g6'
def enumerate_cycles(G,L):
 adj=[list(G.neighbors(v)) for v in range(len(G))]; out=set()
 for s in range(len(G)):
  def dfs(v,mask,path):
   if len(path)==L:
    if s in adj[v]:
     a=tuple(path);b=(s,)+tuple(reversed(path[1:]));out.add(min(a,b))
    return
   for w in adj[v]:
    if w>s and not(mask>>w&1):dfs(w,mask|(1<<w),path+[w])
  dfs(s,1<<s,[s])
 return out
for j,line in enumerate(open(P)):
 if j<2:continue
 G=nx.from_graph6_bytes(line.strip().encode());C=enumerate_cycles(G,16); n=len(G)
 covers=Counter(v for c in C for v in c)
 missing=[len(C)-covers[v] for v in range(n)]
 # minimum hitting set <=3
 hitting=[]
 for k in range(1,5):
  hitting=[s for s in combinations(range(n),k) if all(any(v in c for v in s) for c in C)]
  if hitting:break
 print(j-1,'cycles',len(C),'min_avoiding',min(missing),'max_avoiding',max(missing),'hitting',k,'sets',len(hitting),'min_incidence',min(covers.values()),'max_incidence',max(covers.values()))
