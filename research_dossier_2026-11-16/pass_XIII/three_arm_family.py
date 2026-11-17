import networkx as nx,itertools,json,sys

def build(s):
 G=nx.Graph();r=0
 connector=list(range(3*s-2,4*s-2)) # T: 0 + 3*(s-1) = 3s-2
 G.add_nodes_from(range(4*s-2))
 for i in range(3):
  arm=[1+i*(s-1)+k for k in range(s-1)]
  G.add_edge(r,arm[0]);G.add_edges_from(zip(arm[:-1],arm[1:]))
  slots=arm[:-1]+[arm[-1],arm[-1]]
  assert len(slots)==s
  for k,v in enumerate(slots): G.add_edge(v,connector[(k+i)%s])
 assert all(d==3 for _,d in G.degree())
 return G,list(range(3*s-2,4*s-2))

def prime(G):
 if nx.node_connectivity(G)!=3:return False
 E=list(G.edges())
 for edges in itertools.combinations(E,3):
  H=G.copy();H.remove_edges_from(edges)
  cs=list(nx.connected_components(H))
  if len(cs)>1 and min(map(len,cs))>1:return False
 return True

def cycles(G,q):
 A=[list(G[v]) for v in G];n=len(G);out={}
 for st in range(n):
  def dfs(u,d,m):
   if d==q:
    if st in A[u]:out[m]=True
    return
   for v in A[u]:
    if v>st and m>>v&1==0:dfs(v,d+1,m|1<<v)
  dfs(st,1,1<<st)
 return list(out)

if __name__=='__main__':
 for s in range(3,11):
  G,J=build(s);q={x:cycles(G,x) for x in [4,8,16,32] if x<len(G)}
  avoiding=[];r=0
  for size in range(1,s+1):
   reach=0
   for cs in q.values():
    for c in cs:
     if c>>r&1==0 and (c & sum(1<<j for j in J)).bit_count()<=size:
      reach=1;break
    if reach:break
   if reach:avoiding.append(size)
  print({'s':s,'n':len(G),'node_conn':nx.node_connectivity(G),'prime':prime(G) if s<=7 else None,'dyadic_counts':{k:len(x) for k,x in q.items()},'r0_min_connector':min(avoiding,default=None),'g6':nx.to_graph6_bytes(G,header=False).decode().strip() if s<=6 else None},flush=True)
