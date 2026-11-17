"""Complete bridge-step rootedness check at order 18 from known 607 prime n16 graphs.
Build only exceptional bridge-root pairs with no untouched dyadic parent cycle.
"""
import itertools, time, json, collections
import networkx as nx
from edge_transversals import dyadic_masks

def root_missing(H, required_roots):
 """Find each desired vertex a dyadic-cycle avoiding witness, q 4/8/16.
 Reverse DFS root avoidance, early exit on first success per root.
 """
 n=len(H); adj=[tuple(H[v]) for v in range(n)]
 missing=[]; qtrials={}
 for root in required_roots:
  ok=False
  allowed=(1<<n)-1-(1<<root)
  for q in (4,8,16):
   if q>n-1:break
   def dfs(cur,s,depth,used):
    if depth==q:
     return s in adj[cur]
    for nxt in adj[cur]:
     if nxt>s and (allowed>>nxt)&1 and not (used>>nxt)&1:
      if dfs(nxt,s,depth+1,used|(1<<nxt)):
       return True
    return False
   for s in range(n):
    if s==root:continue
    if dfs(s,s,1,1<<s):
     ok=True; qtrials[root]=q;break
   if ok:break
  if not ok:missing.append(root)
 return missing,qtrials

def bridged(G,e,f):
 n=len(G);H=G.copy();H.remove_edges_from((e,f));H.add_edges_from(((e[0],n),(e[1],n),(n,n+1),(f[0],n+1),(f[1],n+1)))
 return H

def run():
 ngraphs=0; total_pairs=0;root_exceptions=0;exceptional_bridges=0;unrooted_bridge=0
 remaining_bad=[]; sorted_rep=collections.Counter();start=time.perf_counter()
 with open('/mnt/data/eg-work/prime_n16.g6') as f:
  lines=[line.strip() for line in f if line.strip()]
 for idx,line in enumerate(lines):
  G=nx.from_graph6_bytes(line.encode());E,C=dyadic_masks(G);N=len(C)
  allc=(1<<N)-1
  mask_v=[0]*len(G); mask_e=[0]*len(E)
  for i,(vbits,ebits) in enumerate(C):
   bit=1<<i
   for v in range(len(G)):
    if vbits>>v&1:mask_v[v]|=bit
   while ebits:
    low=ebits&-ebits
    j=low.bit_length()-1;mask_e[j]|=bit;ebits^=low
  for a,b in itertools.combinations(range(len(E)),2):
   e,f=E[a],E[b]
   if len(set(e+f))!=4:continue
   total_pairs+=1
   surviving=allc & ~(mask_e[a]|mask_e[b])
   exceptions=[r for r in G if not (surviving & ~mask_v[r] & allc)]
   if not surviving:
    exceptions.extend([len(G),len(G)+1]);unrooted_bridge+=1
   if not exceptions:continue
   exceptional_bridges+=1;root_exceptions+=len(exceptions)
   H=bridged(G,e,f)
   missing,qtrials=root_missing(H,exceptions)
   sorted_rep.update(qtrials.values())
   if missing:
    remaining_bad.append({'parent_g6':line,'pair':[e,f],'root':missing,'n':len(H),'parent_index':idx})
    print('COUNTEREXAMPLE',remaining_bad[-1],flush=True)
    break
  ngraphs+=1
  if idx%75==0 or remaining_bad:
   print(json.dumps({'progress':idx+1,'total_base':len(lines),'pairs':total_pairs,'exception_bridges':exceptional_bridges,'root_exceptions':root_exceptions,'bad':len(remaining_bad),'repairs':sorted_rep,'sec':round(time.perf_counter()-start,1)}),flush=True)
  if remaining_bad:break
 print('FINAL',json.dumps({'base_graphs':ngraphs,'total_bridged_pairs':total_pairs,'exception_bridges':exceptional_bridges,'exception_roots':root_exceptions,'newroot_exception_bridges':unrooted_bridge,'repair_length_counts':sorted_rep,'bad':remaining_bad,'elapsed_sec':round(time.perf_counter()-start,1)}),flush=True)
 with open('/mnt/data/eg-work/bridge18_results.json','w') as o:
  json.dump({'base_graphs':ngraphs,'total_bridged_pairs':total_pairs,'exception_bridges':exceptional_bridges,'exception_roots':root_exceptions,'newroot_exception_bridges':unrooted_bridge,'repair_length_counts':sorted_rep,'bad':remaining_bad,'elapsed_sec':round(time.perf_counter()-start,1)},o,indent=2)

if __name__=='__main__':run()
