import networkx as nx,time
strings=['W??G?C??KCCBa?OCgO@O@C??O?IG??G?K`??CO?K@???C@@','WK?Y?CAGK?G`?G??_?O_@????@WOO@O?C@O??OOK??O??D@','W?GG?C??CO?FW?P?q??g@?_@A?GA??a?E?_??GAH?_??A?P','W?O@??O@COO@O_O?c?@?`c??P?GGG?W?C@@??o?G@@??E?@']

def cycs(g,L):
 n=len(g); A=[list(g[v]) for v in range(n)]; masks={};count=0; vco=[0]*n
 for s in range(n):
  def dfs(u,depth,seen):
   nonlocal count
   if depth==L:
    if s in A[u]:
     count+=1
     for v in seen: vco[v]+=1
    return
   for v in A[u]:
    if v>s and v not in seen:
     seen.add(v); dfs(v,depth+1,seen);seen.remove(v)
  dfs(s,1,{s})
 return count//2,[x//2 for x in vco]
for st in strings:
 g=nx.from_graph6_bytes(st.encode());t=time.perf_counter();lengths={L:cycs(g,L) for L in (4,8,16)}
 cover=[sum(lengths[L][0]-lengths[L][1][v] for L in lengths) for v in g]
 print('g6',st,'2conn',nx.node_connectivity(g),'3cuts',nx.edge_connectivity(g),'counts',{L:ls[0] for L,ls in lengths.items()},'root-critical',[v for v in g if cover[v]==0],'minavoiding',min(cover),'elapsed',time.perf_counter()-t,flush=True)
import sys
sys.path.insert(0,'/mnt/data/eg-work/tracks/2026-11-halving/scripts')
from fractional_bridge_resilience_lp import solve_fractional_resilience
for st in strings:
 g=nx.from_graph6_bytes(st.encode()); t=time.perf_counter(); d=solve_fractional_resilience(g)
 print('rho',round(d.resilience,6),'cycles',d.cycle_count,'vertex_cap',round(d.vertex_cap,4),'elapsed',round(time.perf_counter()-t,2),flush=True)
