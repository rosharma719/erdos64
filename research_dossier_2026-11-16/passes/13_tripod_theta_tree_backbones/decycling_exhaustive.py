import networkx as nx,itertools,time,json,ast,collections,pathlib
p=pathlib.Path('/mnt/data/eg-work/check24.py').read_text()
strings=ast.literal_eval(p.split('strings=',1)[1].split('\n\n',1)[0])

def alltrees(G):
 n=len(G);m=n//4+1 if n%4==0 else (n+2)//4
 need=1 if n%4==0 else 0
 A=[sum(1<<v for v in G[u]) for u in range(n)]
 for t in itertools.combinations(range(n),m):
  mask=sum(1<<v for v in t)
  if sum((A[u]&mask).bit_count() for u in t)!=2*need:continue
  T=((1<<n)-1)^mask
  s=(T&-T).bit_length()-1;seen=1<<s;f=seen
  while f:
   nn=0;mm=f
   while mm:
    b=mm&-mm;mm-=b;nn|=A[b.bit_length()-1]
   f=nn&T&~seen;seen|=f
  if seen==T:yield mask

def cycs(G,L):
 n=len(G);A=[list(G[v]) for v in range(n)];out=set()
 for s in range(n):
  def dfs(u,d,seen):
   if d==L:
    if s in A[u]:out.add(seen)
    return
   for v in A[u]:
    if v>s and not seen>>v&1:dfs(v,d+1,seen|1<<v)
  dfs(s,1,1<<s)
 return list(out)

def analyze(G,L=16):
 n=len(G); allv=(1<<n)-1; cs=cycs(G,L)
 levels=collections.Counter(); jcount=0; best=100; best_j=None; maxmin=0
 per_root_best=[100]*n
 for j in alltrees(G):
  jcount+=1;cov=0; level=0
  cm=sorted([((c&j).bit_count(),allv^c) for c in cs])
  for k,x in cm:
   cov |=x;level=max(level,k)
   if cov==allv:break
  levels[level]+=1
  if level<best:best=level;best_j=j
  for r in range(n):
   k=min((k for k,x in cm if x>>r&1),default=999)
   if k<per_root_best[r]:per_root_best[r]=k
 return {'n':n,'cycles':len(cs),'decompositions':jcount,'best_global_k':best,'best_J':[v for v in range(n) if best_j>>v&1],'levels':dict(sorted(levels.items())),'per_root_best_max':max(per_root_best),'per_root_best':per_root_best}

if __name__=='__main__':
 for i,s in enumerate(strings):
  t=time.time();r=analyze(nx.from_graph6_bytes(s.encode()));r['graph']=i+1;r['sec']=round(time.time()-t,2)
  print(json.dumps(r),flush=True)
