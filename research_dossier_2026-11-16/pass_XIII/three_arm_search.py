import random,time,sys,networkx as nx,json,itertools

def build(s,p1,p2):
 n=4*s-2;j0=3*s-2;A=[[] for _ in range(n)]
 def ae(u,v):A[u].append(v);A[v].append(u)
 for i,p in enumerate((tuple(range(s)),p1,p2)):
  arm=[1+i*(s-1)+k for k in range(s-1)]
  ae(0,arm[0]);
  for a,b in zip(arm,arm[1:]):ae(a,b)
  slots=arm[:-1]+[arm[-1],arm[-1]]
  for k,v in enumerate(slots): ae(v,j0+p[k])
 return A

def has_q(A,q):
 n=len(A)
 for start in range(n):
  b=1<<start
  def dfs(u,d,vis):
   if d==q:
    return start in A[u]
   for v in A[u]:
    if v>start and not (vis>>v&1) and dfs(v,d+1,vis|1<<v):return True
   return False
  if dfs(start,1,b):return True
 return False

def graph(A):
 G=nx.Graph();G.add_nodes_from(range(len(A)))
 for i,N in enumerate(A):
  for j in N:
   if i<j:G.add_edge(i,j)
 return G

def check(s,N=100000,seed=123):
 rng=random.Random(seed);p=list(range(s));t=time.time();found=[];ct={4:0,8:0}
 for trial in range(1,N+1):
  p1=p.copy();rng.shuffle(p1);p2=p.copy();rng.shuffle(p2)
  A=build(s,p1,p2)
  if has_q(A,4):ct[4]+=1;continue
  if has_q(A,8):ct[8]+=1;continue
  G=graph(A)
  print('NO-4/8',{'s':s,'trial':trial,'perms':[p1,p2],'g6':nx.to_graph6_bytes(G,header=False).decode().strip(),'conn':nx.node_connectivity(G)},flush=True)
  found.append((p1,p2))
  if len(found)==4:break
  if trial%2500==0:print('PROGRESS',s,trial,'sec',round(time.time()-t,2),flush=True)
 print('FINAL',s,'trials',trial,'q4 rejects',ct[4],'q8 rejects',ct[8],'found',len(found),'sec',round(time.time()-t,2),flush=True)
 return found
if __name__=='__main__':
 for s in [7,8,9]:check(s,int(sys.argv[1]) if len(sys.argv)>1 else 10000,seed=20261116+s)
