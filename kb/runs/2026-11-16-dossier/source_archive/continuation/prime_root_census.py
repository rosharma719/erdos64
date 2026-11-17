#!/usr/bin/env python3
"""Construct cyclically 4-edge connected cubic graphs by all disjoint bridges.
Kingan & Kingan theorem; count at n=12 is a check against a separate catalog.
Dedup uses WL hashing + exact NX isomorphism.
"""
import networkx as nx
import collections, itertools, time, sys, json
import numpy as np

def prism(k):return nx.circular_ladder_graph(k)
def mobius(k):
 g=nx.cycle_graph(2*k);g.add_edges_from((i,i+k) for i in range(k));return g

def bridged(G,e,f):
 H=G.copy();n=len(G);H.remove_edges_from([e,f]);H.add_edges_from([(e[0],n),(e[1],n),(n,n+1),(f[0],n+1),(f[1],n+1)]);return H

def layer_hash(G):
 A=nx.to_numpy_array(G,dtype=np.int64)
 P=A.copy(); traces=[]
 for k in range(2,11):
  P=P@A
  if k>=3:traces.append(int(np.trace(P)))
 return tuple(traces)

def witness_missing_roots(G):
 n=len(G); A=[list(G[v]) for v in range(n)]; allbits=(1<<n)-1; covered=0; Dcount={4:0,8:0,16:0}
 for q in [4,8,16,32]:
  if q>n-1:break
  def dfs(u,s,depth,mask):
   nonlocal covered
   if covered==allbits: return
   if depth==q:
    if s in A[u]:
     Dcount[q]+=1;covered|=(allbits^mask)
    return
   for v in A[u]:
    if v>s and not (mask>>v)&1:
     dfs(v,s,depth+1,mask | (1<<v))
     if covered==allbits:return
  for s in range(n):
   dfs(s,s,1,1<<s)
   if covered==allbits:break
  if covered==allbits:break
 return [v for v in G if not (covered>>v)&1],Dcount

def all_bridge_candidates(G):
 edges=list(G.edges())
 for e,f in itertools.combinations(edges,2):
  if len(set(e+f))==4:
   yield bridged(G,e,f)

def add_to_bucket(buckets, H):
 h=layer_hash(H);B=buckets[h]
 if not any(nx.is_isomorphic(H,F) for F in B):
  B.append(H);return True
 return False

def run(nmax):
 byorder={8:[prism(4),mobius(4)]}
 for n in range(8,nmax+1,2):
  t0=time.perf_counter()
  if n>8:
   buckets=collections.defaultdict(list)
   if n==10:
    for H in [prism(5),mobius(5),nx.petersen_graph()]:add_to_bucket(buckets,H)
   for G in byorder[n-2]:
    for H in all_bridge_candidates(G):
     add_to_bucket(buckets,H)
   byorder[n]=[G for B in buckets.values() for G in B]
  t=time.perf_counter();bad=[];Dcounter=collections.Counter()
  for ix,G in enumerate(byorder[n]):
   miss,count=witness_missing_roots(G)
   if miss:bad.append({'i':ix,'g6':nx.to_graph6_bytes(G,header=False).decode().strip(),'missing_roots':miss,'counts':count})
   Dcounter.update(k for k,c in count.items() if c>0)
  print(json.dumps({'n':n,'classes':len(byorder[n]),'root_critical_classes':len(bad),'examples':bad[:3],'cycle_coverage_classes':Dcounter,'sec_generation':round(t-t0,2),'seconds_check':round(time.perf_counter()-t,2)}),flush=True)
  if n==12:assert len(byorder[n])==18, f'Expected 18 prime order 12, got {len(byorder[n])}'
  if bad:
   with open(f'/mnt/data/eg-work/bad_n{n}.json','w') as f:json.dump(bad,f,indent=2)
  if n>=16:
   with open(f'/mnt/data/eg-work/prime_n{n}.g6','w') as f:
    f.write('\n'.join(nx.to_graph6_bytes(G,header=False).decode().strip() for G in byorder[n]))

if __name__=='__main__':run(int(sys.argv[1]))
