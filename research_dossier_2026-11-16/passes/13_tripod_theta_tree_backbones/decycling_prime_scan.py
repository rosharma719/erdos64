import json,sys,time,collections,networkx as nx
sys.path.insert(0,'/mnt/data/eg-work')
from decycling_exhaustive import alltrees,cycs

def check(G,stop_at=3):
 n=len(G); allv=(1<<n)-1
 cs=[];cc={}
 for q in (4,8,16):
  if q<n:xs=cycs(G,q);cc[q]=len(xs);cs.extend(xs)
 best=99; bestmask=0;levels=collections.Counter();jcnt=0
 for j in alltrees(G):
  jcnt+=1; cov=0;k=0
  for count,miss in sorted(((c&j).bit_count(),allv^c) for c in cs):
   cov|=miss;k=max(k,count)
   if cov==allv:break
  if cov!=allv:k=99
  levels[k]+=1
  if k<best:best=k;bestmask=j
  if best<=1:break
 return {'best':best,'J_count':jcnt,'levels':dict(levels),'cycle_counts':cc,'bestmask':bestmask}

if __name__=='__main__':
 s=open('/mnt/data/eg-work/prime_n16.g6').read().splitlines()
 out=[];t0=time.time();cnt=collections.Counter()
 for idx,line in enumerate(s):
  G=nx.from_graph6_bytes(line.encode())
  if cycs(G,4):continue
  r=check(G);cnt[r['best']]+=1
  if r['best']>=3: out.append({'index':idx,'g6':line,'results':r})
  if idx%100==0:print('progress',idx,dict(cnt),'sec',round(time.time()-t0,1),flush=True)
 print('FINAL',dict(cnt),'hard',len(out),'elapsed',round(time.time()-t0,2));print('SAMPLE',out[:3]);
 json.dump({'stats':dict(cnt),'hard':out},open('/mnt/data/eg-work/decycling_prime16_results.json','w'),indent=2)
