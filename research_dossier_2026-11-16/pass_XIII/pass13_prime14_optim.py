import sys,collections,time,json,networkx as nx
sys.path.insert(0,'/mnt/data/eg-work')
from pass13_prime14_audit import generate
from decycling_exhaustive import alltrees
from pass13_tree_backbone import dyadic_masks

def best(G):
 n=len(G);allv=(1<<n)-1;D=dyadic_masks(G)
 best=100;hist=collections.Counter();partitions=0;bestmask=None
 for j in alltrees(G):
  partitions+=1;cov=0;k=0
  for cost,miss in sorted(((c&j).bit_count(),allv^c) for _,c in D):
   cov|=miss;k=max(k,cost)
   if cov==allv:break
  if cov==allv:
   hist[k]+=1
   if k<best:best=k;bestmask=j
  else:hist[99]+=1
 return best,partitions,hist,bestmask

def main():
 t=time.time();by=generate();D={}
 for n in (10,14):
  stats=collections.Counter();hard=[];ex=[]
  for ix,G in enumerate(by[n]):
   k,jc,h,j=best(G);stats[k]+=1
   if k>=3:hard.append({'idx':ix,'g6':nx.to_graph6_bytes(G,header=False).decode().strip(),'best':k,'partitions':jc,'hist':dict(h)})
   if len(ex)<3:ex.append({'best':k,'partitions':jc,'hist':dict(h)})
  D[n]={'stats':dict(stats),'hard':hard,'examples':ex}
 print(json.dumps({'results':D,'seconds':round(time.time()-t,2)},indent=2))
 json.dump(D,open('/mnt/data/eg-work/pass13_prime14_optim.json','w'),indent=2)
if __name__=='__main__':main()
