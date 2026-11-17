import networkx as nx, random, itertools, sys, time
sys.path.insert(0,'/mnt/data/eg-work')
from bridge_root_18 import root_missing,bridged
rng=random.Random(20261116)
with open('/mnt/data/eg-work/prime_n16.g6') as f:lines=[x.strip() for x in f if x.strip()]
checked=0;t=time.perf_counter()
for j in range(80):
 g=nx.from_graph6_bytes(lines[rng.randrange(len(lines))].encode())
 pairs=[(e,f) for e,f in itertools.combinations(g.edges(),2) if len(set(e+f))==4]
 e,f=rng.choice(pairs);h=bridged(g,e,f)
 roots=list(range(len(h)))
 from_fast,by_q=root_missing(h,roots)
 d=h.to_directed();cyc=nx.simple_cycles(d,length_bound=8)
 coverage=0
 for C in cyc:
  if len(C) in (4,8):
   coverage|=((1<<len(h))-1)^sum(1<<v for v in C)
 from_nx=[r for r in roots if not coverage>>r&1]
 assert sorted(from_fast)==from_nx,(j,from_fast,from_nx)
 checked+=1
print('Independent directed-cycle oracle agrees for',checked,'random prime bridge children n18. Time',round(time.perf_counter()-t,2),'s')
