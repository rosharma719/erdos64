import networkx as nx,random,sys,collections,time,json,itertools
sys.path.insert(0,'/mnt/data/eg-work')
from decycling_prime_scan import check
from decycling_exhaustive import cycs
from bridge_root_18 import bridged
s=open('/mnt/data/eg-work/prime_n16.g6').read().splitlines()
rng=random.Random(20261116); candidates=[]
for i,line in enumerate(s):
 G=nx.from_graph6_bytes(line.encode());
 if cycs(G,4):continue
 E=list(G.edges());pairs=[(e,f) for e,f in itertools.combinations(E,2) if len(set(e+f))==4];rng.shuffle(pairs)
 for e,f in pairs[:12]:
  H=bridged(G,e,f)
  if not cycs(H,4):candidates.append((i,line,e,f,H))
print('candidate no-C4 primes18',len(candidates),flush=True)
rng.shuffle(candidates);summary=collections.Counter();hard=[];t=time.time()
for z,(i,line,e,f,H) in enumerate(candidates[:300]):
 result=check(H)
 summary[result['best']]+=1
 if result['best']>=3: hard.append({'index':i,'parent':line,'edges':[e,f],'result':result})
 if z%50==0:print('progress',z,summary,'sec',round(time.time()-t,2),flush=True)
print('FINAL',summary,'hard',len(hard),'sec',round(time.time()-t,2))
if hard:print('COUNTEREXAMPLE TO 2-connector',hard[0])
json.dump({'counts':dict(summary),'hard':hard,'total_candidates':len(candidates)},open('/mnt/data/eg-work/decycling_prime18_sample.json','w'),indent=2)
