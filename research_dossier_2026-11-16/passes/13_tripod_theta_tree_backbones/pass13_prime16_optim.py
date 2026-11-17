import networkx as nx,collections,time,json,sys
sys.path.insert(0,'/mnt/data/eg-work')
from decycling_prime_scan import check
s=open('/mnt/data/eg-work/prime_n16.g6').read().splitlines()
assert len(s)==607
ct=collections.Counter();hard=[];start=time.time();nc=0
for i,line in enumerate(s):
 G=nx.from_graph6_bytes(line.encode());r=check(G);ct[r['best']]+=1;nc+=1
 if r['best']>=3:hard.append({'idx':i,'g6':line,'result':r})
 if i%100==0:print('PROGRESS',i+1,dict(ct),'seconds',round(time.time()-start,2),flush=True)
print('FINAL',dict(ct),'hard',len(hard),'seconds',round(time.time()-start,2),flush=True)
if hard:print(hard[:2])
json.dump({'counts':dict(ct),'hard':hard,'classes':nc},open('/mnt/data/eg-work/pass13_prime16_optim.json','w'),indent=2)
