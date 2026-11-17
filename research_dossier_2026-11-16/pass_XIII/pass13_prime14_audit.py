import sys,time,json,collections,networkx as nx
sys.path.insert(0,'/mnt/data/eg-work')
from prime_root_census import prism,mobius,all_bridge_candidates,add_to_bucket
from decycling_exhaustive import alltrees
from pass13_tree_backbone import tree_partition_ok,cut_crossings,avoid_root_at_most_two,dyadic_masks

def generate():
 by={8:[prism(4),mobius(4)]}
 for n in (10,12,14):
  bk=collections.defaultdict(list)
  if n==10:
   for H in (prism(5),mobius(5),nx.petersen_graph()):add_to_bucket(bk,H)
  for G in by[n-2]:
   for H in all_bridge_candidates(G):add_to_bucket(bk,H)
  by[n]=[G for B in bk.values() for G in B]
 assert (len(by[10]),len(by[12]),len(by[14]))==(5,18,84)
 return by

def main():
 t0=time.time();by=generate();S={}
 for n in (10,14):
  total=0;worst=collections.Counter();root_exception_graphs=0;example=None
  for G in by[n]:
   n0=len(G);D=dyadic_masks(G)
   Jmask=next(alltrees(G));J={r for r in range(n0) if Jmask>>r&1}
   assert tree_partition_ok(G,J) and len(J)==(n+2)//4
   cuts=cut_crossings(G,J)
   assert all(c['crossing_connectors'] >= (2 if min(c['side_sizes'])==1 else 3) for c in cuts)
   for r in G:avoid_root_at_most_two(G,J,r)
   coverage=[]
   for r in G:
    complexity=min((c&Jmask).bit_count() for q,c in D if not c>>r&1)
    coverage.append(complexity)
   mx=max(coverage);worst[mx]+=1
   # exact one-J escape classification by root and partition
   if any((not any(((c&Jmask).bit_count()==1 and not(c>>r&1)) for _,c in D)) for r in G):
    root_exception_graphs+=1
    if example is None:example={'graph6':nx.to_graph6_bytes(G,header=False).decode().strip(),'J':sorted(J),'worst_root_dyadic_connector_count':mx}
   total+=1
  S[n]={'number_graphs':total,'worst_root_dyadic_connector_complexity_distribution':dict(worst),
        'has_a_root_requiring_at_least_two_connectors_for_dyadic':root_exception_graphs,
        'example':example}
 print(json.dumps({'summary':S,'elapsed_seconds':round(time.time()-t0,3)},indent=2),flush=True)
 json.dump(S,open('/mnt/data/eg-work/pass13_prime14_audit.json','w'),indent=2)
if __name__=='__main__':main()
